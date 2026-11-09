# PingCode Nexus Skills

PingCode Nexus 让你可以直接在 PingCode 平台上构建和部署自定义应用——项目页面、工作项面板、仪表盘部件、Wiki 内容块、事件处理函数、Webhook 等等。Nexus Skills 插件打包了多个面向 Nexus 的技能，让智能体可以脚手架应用、发布前审查、排查故障、做白盒安全审计，并围绕 Nexus CLI、Resolver、Custom UI、manifest 权限等平台专属概念提供结构化工作流。

## 知识原则

**核心知识随包内置；完整平台参考通过官方在线文档按需获取。**

| | 内置 | 在线 |
| --- | --- | --- |
| 内容 | 流程、硬约束、连线、最小示例、高频排障/审查方法 | 完整字段、扩展点、API/scope 等明细 |
| 来源 | 各技能 `SKILL.md`、`references/`、`assets/` | [developer.pingcode.com](https://developer.pingcode.com) |

## 包含内容

### 技能

插件在 `skills/` 下提供四个技能，每个带有宿主可加载的 `SKILL.md`：

**Nexus App Builder**（`skills/nexus-app-builder/`）按意图分支：纯咨询、新建、改已有、按需部署分发——不强制跑完创建→分发全链路。覆盖 `nexus create`、模板、Custom UI / Native UI、事件/Webhook、扩展点与 scope。

**Nexus App Debugger**（`skills/nexus-app-debugger/`）对已有故障做证据优先的定位与复验：部署失败、白屏、Resolver、scopes、Invoke 超时、事件/Webhook 等。

**Nexus App Reviewer**（`skills/nexus-app-reviewer/`）发布前就绪审查：manifest 连线、架构、运行时、依赖与明显风险信号（非深度安全审计）。

**Nexus Security Reviewer**（`skills/nexus-security-reviewer/`）结构化白盒安全审计：AuthZ、注入、租户隔离、密钥、egress、Webhook/Exposer，规则资产驱动。

| 组件 | 能力 | 示例 |
| --- | --- | --- |
| **App Builder** | 脚手架、定制、按需部署分发 | `nexus create`、`deploy`、`distribute`、扩展点 |
| **App Debugger** | 现网/部署故障诊断 | logs、白屏、Resolver、权限 |
| **App Reviewer** | 发布前就绪检查 | manifest 连线、部署就绪 |
| **Security Reviewer** | 白盒安全审计 | AuthZ、租户隔离、Webhook |

插件元数据见根目录 `plugin.json`，以及 `.cursor-plugin/`、`.claude-plugin/`、`.plugin/`、`.agents/` 等宿主清单。

## 前置条件

- [PingCode 开发者账号](https://developer.pingcode.com)
- [PingCode 注册企业](https://pingcode.com/signup)（分发、安装、验证）
- **Node.js 24+**（`@pc-nexus/cli` 要求 `node >=24`；`npx skills` 安装也需要可用的 Node）
- **Python 3**（可选；技能内文档搜索等辅助脚本用到）

## 安装

推荐优先用 **skills CLI**（跨宿主）。也可用各宿主的插件安装方式。有 GitHub 读取权限时可用下方仓库路径直装；否则先 clone，再按本地路径安装。

### skills CLI（推荐）

```bash
npx skills@latest add pingcode-org/nexus-skills --all
```

全局 / 指定技能：

```bash
npx skills@latest add pingcode-org/nexus-skills --all --global
npx skills@latest add pingcode-org/nexus-skills --skill nexus-app-builder
```

本地目录：

```bash
npx skills@latest add /path/to/nexus-skills --all
```

### Cursor

清单见 `.cursor-plugin/plugin.json`。

从 Git 安装（仓库可访问时）：

```text
/add-plugin nexus-skills@https://github.com/pingcode-org/nexus-skills
```

若已上架 Cursor Marketplace，可用 `/add-plugin nexus-skills`。

本地开发或无法访问远程时，拷贝到 Cursor 本地插件目录：

```bash
mkdir -p ~/.cursor/plugins/local
rsync -a --delete --exclude .git /path/to/nexus-skills/ ~/.cursor/plugins/local/nexus-skills/
```

然后 **Developer: Reload Window**，在 **Customize → Plugins** 确认出现 **Nexus Skills（Local）** 及四个 skill。不要使用指向仓外的软链（会被跳过）；源码变更后需重新 rsync。企业版若关闭本地插件导入，需管理员开启 **Allow Local Plugin Imports**。

### Claude Code

```text
/plugin marketplace add pingcode-org/nexus-skills
/plugin install nexus-skills@pingcode-nexus-skills
```

本地 checkout 时，把上面的 `pingcode-org/nexus-skills` 换成本地路径。清单见 `.claude-plugin/`。

### OpenAI Codex

```bash
codex plugin marketplace add pingcode-org/nexus-skills --ref main
codex plugin add nexus-skills@pingcode-nexus-skills
```

本地 checkout 时把 marketplace 源换成本地路径。

### Agent Plugins / 其他客户端

本仓库遵循 [Agent Plugins](https://agent-plugins.org/) 约定：根目录 `plugin.json`，技能位于 `skills/*/SKILL.md`（由 `skills/` 目录发现）。各客户端用其支持的 Git URL 或本地目录安装后，重启宿主以重新索引。

> 说明：当前 Nexus CLI **没有** `nexus skills install`；请用上方 skills CLI 或各宿主插件方式安装。

## 验证安装

### 1. 技能层

> 帮我构建一个展示客户支持工单的项目页面。

应得结构化 Nexus 工作流（意图分支 → 模板 → create → 定制），而非泛泛代码片段。

- **审查：**「部署前帮我审查这个 Nexus 应用。」
- **调试：**「工作项面板部署后白屏——帮我排查。」
- **安全：**「做一次白盒安全审查，给出带证据的发现。」

### 2. Builder 意图分支

> 我想用 React Custom UI 创建仪表盘部件，从外部 API 拉数。从哪里开始？

应覆盖模板（`react-custom-ui`）、扩展点、Resolver/Bridge、外部域名、`build-web` 与按需部署——且纯问答时不强制登录。

## 可尝试的提示词

- `创建一个工作项面板，展示来自外部 API 的相关支持工单。`
- `构建一个 Wiki 内容块，嵌入可切换柱状/折线/饼图的图表。`
- `添加一个仪表盘部件，按优先级汇总未关闭工作项。`
- `创建一个事件处理函数，在工作项状态变更时发 Webhook。`
- `我的 nexus create 一直失败——帮我看看！`
- `把我的 Nexus 应用部署到开发环境。`
- `同时读项目和 wiki 数据需要哪些 scopes？`
- `部署前帮我审查这个应用的质量和安全信号。`
- `白盒安全审计，重点看 asApp 越权和 Webhook 认证。`
- `nexus deploy 报错——我应该检查什么？`

## 认证

```bash
nexus login
```

在 [PingCode 开放平台](https://developer.pingcode.com/console/signup) 创建个人访问令牌，**只在你自己的终端输入——永远不要把令牌粘贴到对话中。**

```bash
nexus whoami --json
```

> **重要：** 没有 `nexus install`。`nexus distribute` 后须企业管理员在「应用审核」中安装；安装完成前不要宣称已上线。

## 故障排查

### 智能体没有使用 Nexus 技能

- 确认已通过 `npx skills@latest add pingcode-org/nexus-skills --all`（或对应宿主插件命令）安装
- 确认存在 `nexus-app-builder`、`nexus-app-debugger`、`nexus-app-reviewer`、`nexus-security-reviewer` 且各有 `SKILL.md`
- 重启宿主以重新索引

### 认证错误

- 重新 `nexus login`；用 `nexus whoami --json` 确认

### `nexus create` 失败

- 交互式提示问题：在用户自己的终端运行 `nexus create <name> --template <template>`
- `nexus: command not found` → `npm install -g @pc-nexus/cli`
- Node 过低 → Node.js 24+
- 未登录 → 引导本机 `nexus login`

### 部署后白屏 / 资源 404

- 裸 `nexus deploy` 不自动构建前端；先 `npm run build-web`
- `resources[].path` 指向 `web/main/dist`
- `npm run build-web && nexus deploy -e development`

## 了解更多

- [PingCode Nexus 开发者文档](https://developer.pingcode.com)
- [PingCode 开放平台](https://developer.pingcode.com/console/signup)

## 许可证

本仓库采用 [MIT](LICENSE) 许可证。
