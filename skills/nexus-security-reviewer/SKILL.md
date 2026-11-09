---
name: nexus-security-reviewer
description: >-
  对 PingCode Nexus 应用执行结构化白盒安全审查，产出证据驱动的审计报告（含 CVSS、代码证据与验证步骤）。
  适用于安全审查、漏洞评估、AuthZ、租户隔离、Webhook/Exposer 加固或静态分析。
  不要用于通用 PingCode 配置审查、发布就绪泛查（nexus-app-reviewer）或现网故障诊断（nexus-app-debugger）。
license: MIT
metadata:
  maintainer: pingcode
  namespace: nexus
  labels: nexus,security,audit
---

# Nexus Security Reviewer

## 何时使用

用户明确要求安全审查 / 审计 / 越权与租户隔离 / Webhook 加固 / 完整静态分析时使用。

## MUST

1. 按 `references/security-audit-method.md` 执行：**manifest 摘要脚本 → 全局规则 → 按需分类规则**。
2. 遵守 `references/boundaries.md`、`references/platform-invariants.md`。
3. 产物写入项目外的 `ARTIFACT_DIR`；强调服务端鉴权，`display` 非安全边界。
4. 已确认发现含证据、成立条件、影响、CVSS、修复建议与可复现验证步骤。
5. 不在对话中接收 token；发现硬编码凭据时指导轮换与移除。
6. 除非用户要求修复，不改应用代码。
7. **知识原则**：审计方法与规则资产用随包内置的 `assets/` / `references/`；特定接口权限与入口规范按需官方在线或 `search_nexus_docs` 查证（`docs-online.md`）。

## NEVER

- 无代码/配置证据的高危断言
- 夸大工具能力（无官方跨过程 SAST、无 endpoint↔scope 映射表）
- 用未核实资料判定权限/API 规范
- 把扫描产物写入被审项目源码树
- 把发布质量清单整份重做（`nexus-app-reviewer`）或替代现网排障（`nexus-app-debugger`）

## 工作流摘要

1. `ARTIFACT_DIR=...`；在本 skill 目录运行 `python3 -m scripts.summarize_manifest <root> ...`
2. 读摘要与 `observations`（线索需规则验证）。
3. 加载 `assets/security-rules/_global-nexus.mdc`，再按信号加载 `_index-*.mdc` / 子规则。
4. 追踪 来源 → 校验/授权 → 汇聚点；确认可利用性后再写入正式发现。
5. 输出 Markdown 审计报告；告知用户 `ARTIFACT_DIR` 路径。

聚焦模式（例如「只看 AuthZ」）：全局基线 + 该分类索引与匹配子规则。  
完整扫描：遵循 `assets/security-rules/nexus-auditing/static-analysis-nexus.mdc`（社区 Semgrep / npm audit / gitleaks，若本机可用）。

## 交接

修复实现可交 `nexus-app-builder`；审查中发现现网故障线索可提示 `nexus-app-debugger`；通用就绪检查属 `nexus-app-reviewer`。
