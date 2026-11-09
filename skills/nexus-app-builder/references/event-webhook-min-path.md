# 事件 / Webhook 最小路径（内置）

适用模板：`event-typescript` / `webhook-typescript`（通常无前端）。

## 1. 新建（仅新建时）

```bash
python3 -m scripts.create_nexus_app \
  --template event-typescript \
  --name <app-name> \
  --directory <parent-directory>
# 或 --template webhook-typescript
```

## 2. 要点

1. 在 `manifest.yaml` 声明 `event` / webhook trigger，并与 `functions[].key`、handler 连线一致。
2. 事件名、filter **逐字**来自官方文档（`search_nexus_docs "events"` / `webhook`）；勿编造。
3. Webhook：注意公开入口认证/授权；安全深挖交 `nexus-security-reviewer`。
4. 本地联调：部署后可用 `nexus serve -e development`（`-f` 限定函数）；事件不触发见 debugger playbook。
5. 深读：`nexus-backend-developer-guide.md` 事件/Webhook 章节——按需跳读。

已有工程：跳过 create；改订阅或 handler 后按需 deploy/distribute。
