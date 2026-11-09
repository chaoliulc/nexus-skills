#!/usr/bin/env python3
"""
Search Nexus developer documentation at https://developer.pingcode.com.

The script fetches sitemap.xml, scores each URL by keyword matches against
the URL, title and description, then downloads the most promising pages and
extracts readable text from <main> until it has gathered enough relevant
content.

Default docs site is https://developer.pingcode.com. Override with --base-url
or NEXUS_DOCS_BASE_URL when pointing at another docs host.

Examples:
    python3 -m scripts.search_nexus_docs "custom ui react"
    python3 -m scripts.search_nexus_docs manifest permissions --max-pages 3
    python3 -m scripts.search_nexus_docs "resolver" --json
    python3 -m scripts.search_nexus_docs "scopes" --base-url https://developer.pingcode.com
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urlparse, urlunparse


DEFAULT_BASE_URL = "https://developer.pingcode.com"
DEFAULT_TIMEOUT = 20

# Mutable module state set by configure_base_url() / main().
BASE_URL = DEFAULT_BASE_URL
SITEMAP_URL = f"{DEFAULT_BASE_URL}/sitemap.xml"
USER_AGENT = f"nexus-docs-search/1.0 (+{DEFAULT_BASE_URL})"


def configure_base_url(base_url):
    """Set docs site base URL used for sitemap fetch and URL scoring."""
    global BASE_URL, SITEMAP_URL, USER_AGENT
    base = (base_url or DEFAULT_BASE_URL).rstrip("/")
    BASE_URL = base
    SITEMAP_URL = f"{base}/sitemap.xml"
    USER_AGENT = f"nexus-docs-search/1.0 (+{base})"


def normalize_docs_url(url):
    """Rewrite sitemap <loc> host to the configured BASE_URL host.

    Production sitemap.xml may still list alternate docs hosts while
    --base-url / NEXUS_DOCS_BASE_URL points at developer.pingcode.com. Keep path
    / query / fragment; only align scheme + netloc with BASE_URL.
    """
    try:
        target = urlparse(BASE_URL)
        src = urlparse(url)
        if not src.scheme or not src.netloc or not target.netloc:
            return url
        if src.netloc == target.netloc and src.scheme == (target.scheme or src.scheme):
            return url
        return urlunparse(
            (
                target.scheme or src.scheme,
                target.netloc,
                src.path,
                src.params,
                src.query,
                src.fragment,
            )
        )
    except Exception:
        return url


class TextExtractor(HTMLParser):
    """Minimal HTML-to-text extractor that tracks <title> and <main>."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "header", "footer"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = 0
        self.title_depth = 0
        self.main_depth = 0
        self.in_skip = 0
        self.title_parts = []
        self.parts = []
        self._href_stack = []

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t == "title":
            self.title_depth += 1
        elif t == "main":
            self.main_depth += 1
        elif t in self.SKIP_TAGS:
            self.in_skip += 1

        if t in ("p", "div", "section", "article", "br", "li", "h1", "h2",
                 "h3", "h4", "h5", "h6", "tr", "table", "ul", "ol"):
            self.parts.append("\n")
        if t == "td" or t == "th":
            self.parts.append("\t")
        if t == "a":
            href = dict(attrs).get("href")
            self._href_stack.append(href)

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "title" and self.title_depth:
            self.title_depth -= 1
        elif t == "main" and self.main_depth:
            self.main_depth -= 1
        elif t in self.SKIP_TAGS and self.in_skip:
            self.in_skip -= 1
        if t == "a" and self._href_stack:
            self._href_stack.pop()

    def handle_data(self, data):
        if self.in_skip:
            return
        if self.title_depth:
            self.title_parts.append(data)
        if self.main_depth > 0:
            self.parts.append(data)

    def get_title(self):
        return _normalize_whitespace("".join(self.title_parts))

    def get_text(self):
        return _normalize_whitespace("".join(self.parts))


def _normalize_whitespace(text):
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def http_get(url, timeout=DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def fetch_sitemap():
    """Return list of (url, lastmod) tuples from the sitemap."""
    raw = http_get(SITEMAP_URL)
    entries = []
    for block in re.findall(r"<url>(.*?)</url>", raw, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block, re.S)
        if not loc:
            continue
        url = normalize_docs_url(html.unescape(loc.group(1).strip()))
        lastmod = ""
        m = re.search(r"<lastmod>(.*?)</lastmod>", block, re.S)
        if m:
            lastmod = m.group(1).strip()
        entries.append((url, lastmod))
    return entries


def tokenize(query):
    return [t for t in re.split(r"[\s_\-/,.]+", query.lower()) if t]


def score_url(url, terms):
    """Score a URL against search terms using its path segments."""
    path = (urlparse(url).path or "").lower()
    segments = [s for s in re.split(r"[/\-_.]", path) if s]

    score = 0
    for term in terms:
        if term in path:
            score += 5
        for seg in segments:
            if term == seg:
                score += 10
            elif term in seg:
                score += 3
    return score


def fetch_page_meta(url):
    """Fetch a page and return (title, description, html_length)."""
    try:
        raw = http_get(url)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return "", "", 0

    title = ""
    m = re.search(r"<title>(.*?)</title>", raw, re.S | re.I)
    if m:
        title = html.unescape(m.group(1).strip())

    desc = ""
    m = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        raw, re.S | re.I,
    )
    if not m:
        m = re.search(
            r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            raw, re.S | re.I,
        )
    if m:
        desc = html.unescape(m.group(1).strip())

    return title, desc, len(raw)


def score_page(url, title, description, terms):
    """Score a page using URL, title and description."""
    score = score_url(url, terms)
    haystack = (title + " " + description).lower()
    for term in terms:
        if term in haystack:
            score += 8
    return score


def extract_text(raw_html):
    parser = TextExtractor()
    try:
        parser.feed(raw_html)
        parser.close()
    except Exception:
        pass
    return parser.get_title(), parser.get_text()


def snippet_for(text, terms, max_len=500):
    """Pick a snippet around the first term match, otherwise the beginning."""
    if not text:
        return ""
    lowered = text.lower()
    positions = []
    for term in terms:
        idx = lowered.find(term)
        if idx >= 0:
            positions.append(idx)
    if positions:
        center = min(positions)
        start = max(0, center - 150)
        end = min(len(text), center + max_len - 150)
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(text) else ""
        return prefix + text[start:end].strip() + suffix
    return text[:max_len].strip()


def search(query, max_pages=3, max_snippet=600, min_score=1):
    terms = tokenize(query)
    if not terms:
        return {"query": query, "results": [], "error": "empty query"}

    entries = fetch_sitemap()

    # First pass: rank by URL only (no network per page beyond sitemap).
    url_scored = [
        (score_url(url, terms), url, lastmod)
        for url, lastmod in entries
    ]
    url_scored = [(s, u, l) for s, u, l in url_scored if s > 0]
    url_scored.sort(key=lambda x: (-x[0], x[1]))

    # Fetch top candidates to refine by title/description.
    candidates = url_scored[: max(max_pages * 4, 10)]
    refined = []
    for score, url, lastmod in candidates:
        title, desc, _ = fetch_page_meta(url)
        final_score = score_page(url, title, desc, terms)
        refined.append((final_score, url, title, desc, lastmod))
    refined.sort(key=lambda x: (-x[0], x[1]))

    # Second pass: fetch content of the best pages until we have enough.
    results = []
    seen = set()
    for score, url, title, desc, lastmod in refined:
        if len(results) >= max_pages:
            break
        if score < min_score or url in seen:
            continue
        seen.add(url)

        try:
            raw = http_get(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            results.append({
                "url": url,
                "title": title,
                "score": score,
                "error": str(exc),
            })
            continue

        page_title, text = extract_text(raw)
        final_title = page_title or title
        body_score = 0
        lowered_text = text.lower()
        for term in terms:
            body_score += lowered_text.count(term)
        total_score = score + min(body_score, 50)

        results.append({
            "url": url,
            "title": final_title,
            "description": desc,
            "score": total_score,
            "lastmod": lastmod,
            "snippet": snippet_for(text, terms, max_snippet),
            "content_length": len(text),
        })

    return {"query": query, "terms": terms, "results": results}


def format_text(result):
    lines = []
    lines.append(f"# Search: {result['query']}")
    lines.append(f"Terms: {', '.join(result['terms'])}")
    lines.append(f"Results: {len(result['results'])}\n")
    for i, r in enumerate(result["results"], 1):
        lines.append(f"## {i}. {r.get('title') or '(no title)'}")
        lines.append(f"URL: {r['url']}")
        lines.append(f"Score: {r['score']}")
        if r.get("lastmod"):
            lines.append(f"Last modified: {r['lastmod']}")
        if r.get("description"):
            lines.append(f"Description: {r['description']}")
        if r.get("error"):
            lines.append(f"Error: {r['error']}")
        lines.append("")
        lines.append(r.get("snippet", ""))
        lines.append("\n" + "-" * 80 + "\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search Nexus developer documentation online (default: developer.pingcode.com).",
    )
    parser.add_argument("query", help="Search keywords (e.g. 'custom ui react')")
    parser.add_argument(
        "--max-pages", type=int, default=3,
        help="Maximum number of pages to return (default: 3)",
    )
    parser.add_argument(
        "--max-snippet", type=int, default=600,
        help="Maximum snippet length per page (default: 600)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("NEXUS_DOCS_BASE_URL", DEFAULT_BASE_URL),
        help="Docs site base URL (default: https://developer.pingcode.com; "
             "override with NEXUS_DOCS_BASE_URL)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    configure_base_url(args.base_url)

    try:
        result = search(args.query, args.max_pages, args.max_snippet)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))

    if not result["results"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
