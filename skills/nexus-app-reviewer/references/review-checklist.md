# 发布前审查清单（内置）

先审计，默认不改代码。运行 `nexus lint` 收集机械证据；除非用户要求，不 `deploy` / `distribute`。

## 发布阻塞

- Manifest 引用了缺失的 handler / resource / function key
- `invoke('name')` 与 `resolver.define('name')` 不一致
- `extensions[].resolver.function` ∉ `functions[].key`
- `extensions[].resource` ∉ `resources[].key`
- 实际 API/外部 fetch 所需 scope 或 `external.fetch` 未声明
- `functions[].handler` 格式非法或文件/导出不存在
- Node &lt; 24，或 `@pc-nexus/*` / 模块语法导致 lint/构建失败
- `resources[].path` 未指向 `web/main/dist`，或缺少 `build` / `build-web` 脚本  
  （干净 checkout 无 `dist` 正常，勿仅因 dist 缺失阻塞）
- 主用户流程不可达（错误 target / display 恒 false）
- `app.version` 缺失或非有效 semver

## 架构与可维护性

- 扩展点 `target` 与 UX 面匹配；逐字对照官方列表
- 敏感逻辑在后端；前端不持凭据/不做授权裁决
- `display` 非安全边界
- UI Invoke 无长耗时（5s）；长任务走异步队列
- 错误处理覆盖主路径

## 轻量安全信号（深度 → `nexus-security-reviewer`）

- 宽 scope 未见使用；用户触发路径上 `as: "app"` 无授权
- 硬编码密钥；Webhook/Exposer 无可见认证/授权
- 外部域名未声明；过宽 CSP / `unsafe-eval`

无法机械判定 scope 是否最小化（无公开 endpoint↔scope 表）→ 标「需人工核对文档」。

## 验证就绪

- 有合理的本地验证方式说明或脚本（如 `lint` / `build` / `build-web`）；缺测试框架时标「建议」而非默认阻塞
- 主用户路径可说明如何手工验证（扩展点可见、关键 invoke 成功）
- 若仓库已有测试：抽查是否与当前模块相关、是否明显过期；无测试不单独作为阻塞，除非用户明确要求测试覆盖

## 运维就绪

- `app.id` / `app.version` 齐全（不要误报缺 `app.name`）
- 版本规则（按环境类型）：Development 不低于原版本；Staging / Production 须高于原版本
- 公有云只可 CLI `deploy` 到 Development / Staging **类型**（`-e` 为名称，自定义 Development 名可用）；Production **类型**走「应用发布」，勿建议对其 `nexus deploy`
- scripts / `.gitignore` 健全；分发后须管理员安装（无 `nexus install`）
- `nexus logs` 仅 Development **类型**；Staging / Production 排障依赖开发者中心或企业设置的日志

## 输出格式

```markdown
# Nexus 应用审查结果

## 摘要

- 就绪状态：就绪 | 需修改 | 阻塞
- 最高风险领域：…
- 专业 skill 交接：无 | 安全 | 调试

## 发现

1. [严重|警告|信息] …
   - 证据 / 影响 / 建议

## 建议下一步
```
