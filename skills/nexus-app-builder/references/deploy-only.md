# 仅部署 / 分发（意图 D）

适用：应用**已有**可部署工程，用户只要部署或分发——不新建、不大改功能。

## 做法

1. 确认目录含 `manifest.yaml` 与有效 `app.id`；未登录则引导本机 `nexus login`。
2. 有 Custom UI / 前端改动或产物过期时：先 `npm run build-web`（或本包 `deploy_nexus_app`，默认会尝试构建）。
3. 部署（公有云只可 deploy 到 **Development / Staging 类型**；`--env` 为环境**名**，默认常为 `development` / `staging`，自定义 Development 名也可用。NEVER deploy 到 Production **类型**，Production 由「应用发布」自动部署）：

```bash
# 在 nexus-app-builder 技能目录下
python3 -m scripts.deploy_nexus_app --app-dir <app-dir> --deploy --env development
# 或：--env staging（Staging 类型，版本号须高于原版本）
# 或：--env <custom-dev-name>（自定义 Development 类型名）
```

4. 仅当用户要求分发到站点时：

```bash
python3 -m scripts.deploy_nexus_app --app-dir <app-dir> --distribute --site <domain> --env development
```

站点只传域名（如 `acme.pingcode.com`）。版本按**类型**：Development ≥ 原版本；Staging / Production **高于**原版本（Production 类型非 CLI 自行 deploy）。
5. 分发后说明：无 `nexus install`，须企业管理员在「应用审核」安装；安装前勿宣称已上线。

若部署失败或安装后不可见 → 交接 `nexus-app-debugger`。若还要改功能 → 改用 `extend-existing-app.md`。
