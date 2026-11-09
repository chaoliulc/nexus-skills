# 安全审查方法（内置）

白盒、证据驱动。默认 **manifest 驱动按需加载规则**，勿一次读入全部规则文件。

## 执行步骤

1. 在**目标项目外**建临时目录：`ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/nexus-security-review.XXXXXX")"`
2. 运行（在本 skill 目录）：
   ```bash
   python3 -m scripts.summarize_manifest <project-root> --format markdown
   python3 -m scripts.summarize_manifest <project-root> --format json -o "$ARTIFACT_DIR/manifest-summary.json"
   ```
3. 先读摘要：entrypoints、scopes、egress、remotes、exposer、events、storage、observations（线索≠已确认漏洞）。
4. 加载 `assets/security-rules/_global-nexus.mdc`，再按信号加载分类 `_index-*.mdc`，仅在命中启发式时读子规则。
5. 扫描产物一律写入 `ARTIFACT_DIR`，**禁止**写入被审项目源码树。
6. 除非用户要求修复，不改应用代码。

## 信号 → 规则分类

| 信号                                     | 加载                        |
| ---------------------------------------- | --------------------------- |
| scope / 写操作 / `as: "app"`             | `nexus-authn-authz`         |
| webhook / exposer                        | `nexus-webhook-entrypoints` |
| external.fetch / remotes / fetch.request | `nexus-egress-remotes`      |
| XSS/RCE/SSRF 等 sink                     | `nexus-injection`           |
| 全局状态 / 存储 key 作用域               | `nexus-tenant-isolation`    |
| 凭据 / env / KVS secret                  | `nexus-secrets-storage`     |
| 过宽 scope、CSP、通配域名                | `nexus-manifest-config`     |

## 必须覆盖

- AuthZ：`as: "app"` 越权、Resolver/Exposer 缺授权、`display` 绕过
- 注入与输入校验；租户隔离（FaaS warm start、全局缓存、存储 key）
- 密钥与存储；出站/CSP/NIT；Webhook/事件公开入口

## 报告

已确认发现按 CVSS v3.1 排序，含：向量与评分、可利用性与影响、文件证据与来源→汇聚点、CWE、可复现验证步骤。  
不可利用的加固观察放「需验证」。标注假设与证据缺口。

## 已知限制（勿夸大工具能力）

- 无跨过程官方 SAST；结论须说明是代码追踪而非自动分析器。
- 无公开 REST endpoint↔scope 映射 → 不能机械判定最小化 scope。
- Semgrep 仅社区 ruleset；自定义 Nexus rules 未内置。
- `summarize_manifest.py` 只解析 manifest，不解析业务代码。

通用就绪 → `nexus-app-reviewer`；现网故障 → `nexus-app-debugger`。
