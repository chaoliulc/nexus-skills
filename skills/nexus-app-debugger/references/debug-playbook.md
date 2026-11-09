# 调试剧本（内置）

定位到根因即停止。低成本检查优先于读大段源码。

## 原则

- **一次一个动作**；确认结果再下一步。
- **自己跑诊断命令**（`nexus lint` / `logs` / `deploy`）；交互式除外：`nexus login`、`nexus serve` 由用户本机执行。
- **`--no-verify` 仅诊断**，禁止带它发布。
- 多缺陷时：先修部署，再查运行时。

## 分类路由

| 症状                | 优先路径                                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| `nexus deploy` 失败 | 环境 → lint → 对照错误表                                                 |
| 安装后不可见        | 管理员是否安装 / 权限变更后是否重装                                      |
| 白屏 / 资源 404     | `npm run build-web`、`resources[].path=web/main/dist`、DevTools          |
| Resolver undefined  | `invoke` 名 ↔ `resolver.define`；`resolver.function` ↔ `functions[].key` |
| 403 / Unauthorized  | scopes、重新 distribute+安装；前端无应用身份                             |
| 外部 API 被拦       | `permissions.external.fetch.*`                                           |
| UI Invoke 超时      | 5s 限制；长任务改异步队列                                                |
| 事件/Webhook 不触发 | 已部署分发、事件名、tunnel、filter                                       |
| 仅生产异常          | 开发者中心日志（CLI logs 仅 Development **类型**）                        |

## 基线命令

```bash
node -v && nexus --version
nexus lint
ls -la web/main/dist/          # 有 Custom UI 时
nexus deploy -e development --verbose --non-interactive   # -e 为环境名；自定义 Development 类型名也可
nexus logs -e development -l 100
# 可选：nexus serve -e development
# 指定函数：nexus serve -e development -f <function-key>
```

`nexus logs` / `nexus serve` **仅 Development 类型**（默认名常为 `development`）；前端 `console.*` 只在浏览器 DevTools。

## 常见错误速查

| 症状 / 错误                | 修复要点                                                      |
| -------------------------- | ------------------------------------------------------------- |
| `command not found: nexus` | `npm install -g @pc-nexus/cli`                                |
| Node &lt; 24               | 升级到 Node 24+                                               |
| manifest 校验失败          | `nexus lint`；文件名 `manifest.yaml`；key 连线                |
| 白屏 / 404                 | `build-web` 后再 deploy；检查 path                            |
| invoke undefined           | 对齐 invoke / define / function key 三处                      |
| `ERR_FUNCTION_*`           | 补全/修正 `extensions[].resolver` 与 `functions`              |
| 403 调 REST                | 补 scope → deploy → distribute → 管理员确认                   |
| `ERR_FETCH_PERMISSION_*`   | 声明 external fetch 域名                                      |
| UI Invoke &gt; 5s          | 缩短 Resolver 或改异步队列                                    |
| 事件未触发                 | 部署分发、事件名逐字、serve 隧道抢占                          |
| Staging / Production 版本失败 | 版本须高于原版本；公有云 Production **类型**由「应用发布」部署，勿对其 `nexus deploy` |
| HMR 无效                   | `nexus.json` 的 resource key/port 与 manifest/Dev Server 一致 |
| CSP 拦截                   | `permissions.external` 对应类别声明 HTTPS URL                 |

## Handler 与 Invoke

- `handler`: `<file>.<export>`，相对 `src/`，无扩展名（如 `index.resolver`）。
- Manifest function key ≠ invoke 名称；两层都要匹配。

## 复验与清理

修复后走同一证据路径复验；删除临时 `[DEBUG]` 日志；再 `nexus lint`；需要时 redeploy。

纯咨询 / 加功能 → `nexus-app-builder`；发布就绪 → `nexus-app-reviewer`；深度 AuthZ → `nexus-security-reviewer`。
