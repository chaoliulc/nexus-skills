# 仅咨询 / 方案（意图 C）

适用：架构可行性、概念解释、实现建议——**不**创建工程、不部署、不登录。

## 做法

1. 用本包 `references/`（L1）回答流程与硬约束。
2. 需要准确 target / scope / API 字段时，按 `docs-online.md` 上官方文档或 `search_nexus_docs`（英文关键词）。
3. 给出最小示例与取舍；明确「若要实现，下一步可走新建或改已有」。
4. **停止**：不运行 `nexus create` / `deploy` / `distribute`，不索要登录。

若用户中途改为「帮我建出来」→ 切到 `create-new-app.md` 或 `extend-existing-app.md`。
