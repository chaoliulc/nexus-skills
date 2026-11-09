# 新建应用（意图 A）

1. 前置：Node ≥ 24、`@pc-nexus/cli`、`nexus whoami --json`（未登录则引导用户本机 `nexus login`）。
2. 模板与扩展点：见主 `SKILL.md` 模板表；`target` 从 `list-nexus-extensions.md` + 在线文档**逐字**复制。
3. 脚手架（在本 skill 目录下）：

```bash
python3 -m scripts.create_nexus_app \
  --template react-custom-ui \
  --name <app-name> \
  --directory <parent-directory>
```

4. 定制：`ui-resolver-min-path.md`；深读 Custom UI / Backend / Manifest guides。
5. 仅当用户要求时：`build-web`（若有前端）→ `deploy_nexus_app` →（可选）distribute；说明管理员安装。

NEVER 手搓无 `app.id` 的工程；`create` 失败则 STOP 并给出交互式终端命令。
