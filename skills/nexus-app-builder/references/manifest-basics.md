# Manifest 最小要点（内置）

文件名固定为 `manifest.yaml`（不是 `.json` / `.yml`）。`app.id` 由 `nexus create` 生成，**禁止**手动改写。

## 常见顶层字段

| 字段                                          | 作用                                                                    |
| --------------------------------------------- | ----------------------------------------------------------------------- |
| `app.id` / `app.version`                      | 应用身份与版本（语义化版本）                                            |
| `extensions[]`                                | 扩展点：`key`、`target`、可选 `resource` / `resolver` / `display`       |
| `resources[]`                                 | Custom UI 静态资源；`path` 通常为 `web/main/dist`                       |
| `functions[]`                                 | 后端函数：`key` + `handler`（`<file>.<export>`，相对 `src/`，无扩展名） |
| `permissions.scopes`                          | PingCode REST / 平台能力所需 scope                                      |
| `permissions.external`                        | 出站与 CSP：`fetch.backend` / `fetch.client`、fonts/styles/scripts/…    |
| `event.triggers[]`                            | 系统 / 生命周期 / Webhook / 定时事件                                    |
| `remotes` / `endpoints` / `exposer`           | 远程调用与对外 HTTP                                                     |
| `storage` / `async` / `environment.variables` | 存储、队列、环境变量                                                    |

应用显示名在开发者中心配置，**不**要求 `app.name` 出现在 manifest。

## 连线一致性（发布阻塞级）

1. `extensions[].resource` ≡ 某个 `resources[].key`
2. `extensions[].resolver.function` ≡ 某个 `functions[].key`
3. 前端 `invoke("name")` ≡ 后端 `resolver.define("name")`（独立于 function key，区分大小写）
4. `functions[].handler` 指向真实文件的具名导出（如 `index.resolver`）
5. 实际调用的外部域名 / scope 已在 `permissions` 声明

## 原则

- 缺 scope → 运行时 403；改权限后需重新 `deploy` + `distribute` + 管理员确认安装。
- `display` 只控制前端可见性，**不是**鉴权。
- 版本按环境**类型**：Development 不低于原版本；Staging **高于**原版本；Production 须**严格高于**原版本。公有云 CLI 只可 `deploy` 到 Development / Staging 类型（`-e` 为名称，自定义 Development 名可用）；Production 类型由「应用发布」自动部署。

完整字段、扩展点属性、context → 在线文档或本包较长指南（builder 的 `references/nexus-app-manifest-guide.md`）。
