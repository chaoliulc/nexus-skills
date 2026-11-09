# Nexus App Reviewer

实现正确性、可维护性、平台用法与发布就绪检查（非深度安全审计，非现网排障）。

## 内容

- `SKILL.md` — 审查边界与工作流
- `references/review-checklist.md` — 通过 / 阻塞 / 建议清单
- `scripts/search_nexus_docs.py` — 字段级规范按需查证

## 快速检查

> 部署前帮我审查这个 Nexus 应用能不能发布。

应产出结构化就绪报告；明显安全信号可建议转 `nexus-security-reviewer`。
