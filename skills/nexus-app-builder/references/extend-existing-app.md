# 改已有应用（意图 B）

1. 先读仓库与 `manifest.yaml`：模块连线、resource path、functions、scopes。
2. **跳过** `nexus create`；保留无关改动与既有约定。
3. 按改动面加载参考：UI → Custom UI guide；Resolver/事件 → Backend guide；权限/egress → Manifest guide + 在线文档。
4. 有前端时改完 **ALWAYS** `npm run build-web` 再部署（裸 `nexus deploy` 不会自动构建）。
5. 用户要求部署/分发时用本包 `scripts.deploy_nexus_app`；权限变更后需重新 distribute + 管理员安装。

开发中的普通编译错误在本 skill 内修复；复杂现网故障 → `nexus-app-debugger`。
