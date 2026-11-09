# Nexus Security Reviewer

结构化白盒安全审查：身份、授权、租户隔离、凭据与外部入口。

## 内容

- `SKILL.md` — 审计方法入口
- `references/security-audit-method.md` — 证据驱动流程
- `assets/security-rules/` — 按需加载的规则资产
- `scripts/summarize_manifest.py`、`search_nexus_docs.py`

## 快速检查

> 对这个 Nexus 应用做白盒安全审查，重点看 Resolver 越权。

应给出带代码证据、成立条件、影响与修复建议的发现；产物写到项目外的 `ARTIFACT_DIR`。
