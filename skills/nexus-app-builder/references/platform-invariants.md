# 平台不变量（共用）

跨技能口径必须一致：

- CLI 命令是 `nexus`，npm 包前缀是 `@pc-nexus/*`。
- Manifest 文件名固定为 `manifest.yaml`（不是 `.json` 或 `.yml`）。
- Node.js ≥ 24（以当前 `@pc-nexus/cli` engines 为准）。
- **没有** `nexus install`：`nexus distribute` 后须企业管理员在「应用审核」中安装。
- 裸 CLI：`nexus deploy` **不**自动构建前端；有前端时须先 `npm run build-web`，`resources[].path` 指向 `web/main/dist`。
- `nexus-app-builder` 技能内的 `scripts.deploy_nexus_app`：部署时会尝试 `npm run build-web`（无该脚本则跳过）；不要以为裸 `nexus deploy` 也一样。其它技能包不含该脚本。
- 环境**类型**与**名称**不同：类型为 Development / Staging / Production；CLI `-e` 传的是名称。默认名常为 `development` / `staging` / `production`，也可有自定义 Development 类型名称。
- 公有云 CLI / 开发者中心只可 `deploy` 到 **Development / Staging 类型**（自定义 Development 名可用）；**Production 类型**由「应用发布」自动部署（NEVER `nexus deploy` 到 Production 类型）。私有部署用 `nexus packup` 上传 `.npk`。
- 版本按类型：Development 不低于原版本；Staging / Production 须高于原版本。
- `nexus logs` / `nexus serve` 仅 Development 类型；Staging / Production 用开发者中心或企业日志设置。
- Agent **绝不**在对话中索要或接收 API 令牌；引导用户在自己的终端执行 `nexus login`。
- UI Invoke 超时约 **5 秒**；长任务用异步队列，勿堵在前端直接 invoke 的 Resolver。
- `display` 条件不是安全边界；敏感操作在服务端鉴权。

CLI 完整参数优先以本机 `nexus <cmd> --help` 为准；与内置文档冲突时以 CLI / 已安装 SDK 类型为准。  
**核心流程与约束看随包 references；完整字段 / API / scope 看官方在线文档。**
