# Native UI 最小路径（内置）

适用模板：`react-native-ui` / `angular-native-ui`（`Nx*` 由宿主原生渲染）。

与 Custom UI **不是**同一条渲染路径：NEVER 在 Custom UI 里当 Native 用 `@pc-nexus/react` 的 `Nx*`；NEVER 在 Native UI 里按 iframe Bridge 套路硬套。

## 1. 新建（仅新建时）

```bash
python3 -m scripts.create_nexus_app \
  --template react-native-ui \
  --name <app-name> \
  --directory <parent-directory>
```

## 2. 要点

1. 用平台 `Nx*` 组件与 Native 推荐的上下文 API（如文档中的 `useAppContext` / `NexusReconciler` 路径）；细节以官方在线文档为准：`search_nexus_docs "native ui"` / `react hooks`。
2. `manifest.yaml` 仍须 modules / resources / functions / scopes 连线正确（见 `manifest-basics.md`）。
3. 构建与部署：按模板 `package.json` scripts；有前端构建步骤时先构建再 `nexus deploy`（或 `deploy_nexus_app`）。
4. 排障：白屏 / 不显示 → `nexus-app-debugger`；字段级 API → 在线文档，不编造。

已有 Native UI 工程：跳过 create，读 manifest 与源码后改。
