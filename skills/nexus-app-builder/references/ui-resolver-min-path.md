# Custom UI + Resolver 最小可运行路径（内置）

目标：不依赖在线文档也能搭通「面板 → Bridge invoke → Resolver → 返回」。替换扩展点 / 加 REST 前再查在线参考。

## 1. 工程入口

- **新建应用**：先脚手架（见下）；禁止手搓无 `app.id` 的工程。
- **已有应用**：跳过 create，从第 2 节核对 `manifest.yaml` 连线后直接改代码。

```bash
# 仅新建时
nexus create my-panel --template react-custom-ui
# 或：python3 -m scripts.create_nexus_app --template react-custom-ui --name my-panel --directory <parent>
```

## 2. Manifest 连线（节选）

```yaml
app:
  id: "<由 create 生成>"
  version: "1.0.0"

resources:
  - key: main
    path: web/main/dist

functions:
  - key: resolver
    handler: index.resolver

extensions:
  - key: workitem-panel
    title: Demo Panel
    target: pcm:pjm:workitem:panel # 须逐字来自官方列表，勿编造
    resource: main
    resolver:
      function: resolver
```

## 3. 后端 Resolver

`src/resolvers/index.ts`（再由 `src/index.ts` 导出 `resolver`）：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (_context, payload) => {
  return `Hello, ${payload}`;
});

export { resolver };
```

`src/index.ts`：

```typescript
export { resolver } from "./resolvers";
```

## 4. 前端 Bridge

`web/main/src/App.tsx`（示意）：

```typescript
import { invoke } from "@pc-nexus/bridge";

const text = await invoke<string>("greeting", "Nexus");
```

`invoke` 第一个参数必须与 `resolver.define` 名称一致。

## 5. 包与版本

| 包                 | 位置            |
| ------------------ | --------------- |
| `@pc-nexus/core`   | 应用根          |
| `@pc-nexus/bridge` | `web/main`      |
| `@pc-nexus/cli`    | 全局，Node ≥ 24 |

以项目 `package.json` 已安装版本为准。

## 6. 构建与验证

```bash
npm run build-web          # 裸 nexus deploy 不会自动构建；本包 deploy_nexus_app 会尝试构建
nexus lint
nexus deploy -e development --non-interactive
# 或：python3 -m scripts.deploy_nexus_app --app-dir . --deploy --env development
# 需要安装到站点时：nexus distribute -s <site> -e development → 管理员审核安装
```

## 硬约束

- UI Invoke 超时约 **5s**；长任务用 `async.queues` / consumers。
- 调 PingCode REST：服务端 `api.invoke`，声明 `permissions.scopes`；用户身份用 `as: "user"`，应用身份用 `as: "app"` 且须服务端授权。
- 调外部 HTTPS：声明 `permissions.external.fetch.backend`（或前端 `client`）。
- Custom UI 在 iframe 中运行；用 `@pc-nexus/bridge`，不要套用 Native UI 的 `Nx*` 组件路径。

排障：白屏 / invoke 失败 / 403 → `nexus-app-debugger`；发布前连线检查 → `nexus-app-reviewer`。
