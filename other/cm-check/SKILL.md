---
name: cm-check
description: 用户说“检查工作流是否安装正确”“为什么找不到 cm 命令”时使用。默认查询 npm 稳定版，有新版自动升级已管理的 CM 安装，再检查插件、核心 Skills、兼容包装与模板引用；不测试或修改业务代码。
---

# cm-check — 双运行时一致性自检

执行前读取 `../../runtime/project-context.md` 与 `../../runtime/logging.md`。Codex 入口为 `$cm-check`；Claude Code 跨平台入口为 `/cm-check`，macOS/Linux 另有历史别名 `/cm:check`。

## 默认先检查更新

从当前 Skill 路径解析 `{CM_WORKFLOW_ROOT}`。每次完整 `cm-check`，在启动检查控制器前执行一次：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-check-update.mjs" \
  --skill-dir "{CM_WORKFLOW_ROOT}/skills/cm-check" --runtime codex
```

Claude Code 将 `--runtime` 改为 `claude`。默认发现 npm `latest` 稳定新版就升级，
无需 `--upgrade` 或再问一次；固定包为 `@aibyzero/cm-workflow`，复用现有安装器的
`--yes`、范围限制和失败回滚。只更新 CM 的已管理文件，不安装业务依赖或改业务项目。
当前还有 CM 开发、审查或发布任务在运行时，先完成或暂停该任务，不能并发替换其运行时。
用户明确说“只检查，不升级”时跳过此前置步骤，并注明未查询更新。

按 JSON 结果处理，不把退出码 0 一律解释成最新版：

- `updated`：已升级并回读版本；使用返回的 `workflowRoot`，重新读取其中的本 Skill 和
  `references/js-host.md`，直接进入下方检查，不再次运行更新步骤。其他 Skills 在新会话加载。
- `current` / `ahead`：检查返回的管理目录；若当前会话仍引用旧缓存，重新读取该目录的
  Skill/接线文档，提醒新开会话。不降级比 npm 更新的版本。
- `offline`：继续当前本地检查，报告“无法确认最新版”；本地 PASSED 不代表版本最新。
- `unmanaged`：源码仓库、Pi/BYZ 或其他管理器安装仅报告本地/远程版本，不改其源码或
  改换安装方式；明确说明自动升级未执行，沿用当前根检查。
- `blocked` / 非零退出 / 无有效结果：停止并报告原因，不绕过失败继续宣布通过。

当前自动安装支持 macOS Codex 的个人本地市场安装，以及 macOS/Linux Claude 安装。
Windows 或其他安装方式有新版时，明确提示使用原平台安装器；不伪称已更新。
查询有时限，联网只查询公共包版本并下载指定包，不发送项目代码或配置。

## 升级后检查

按选定根目录的[JS 会话入口](references/js-host.md)启动控制器：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-check-host.mjs" serve \
  --skill-dir "{CM_WORKFLOW_ROOT}/skills/cm-check" --project "$PWD" --runtime codex
```

Claude Code 将 `--runtime` 改为 `claude`。这一项说明本次检查跑在哪个运行时，
机械检查用它给 coder/reviewer 打标；不传则记 `未判定`，不对是否派发下结论。

用户说「快速检查」「只看装没装对」「别跑全套」时追加 `--quick`：更新与机械检查照常跑，
机械通过后直接收口，不进八组语义检查。结论为 `MECHANICAL_ONLY`，**不是 PASSED**——
语义八组一组没读，不得据此宣称安装完整无断链。机械失败仍照常报 FAILED/BLOCKED，
快速模式不跳过任何失败。默认（不带该参数）仍是完整检查。
耗时差别很大：更新约 1 秒、机械检查约 12 秒，其余时间几乎全在语义八组逐文件取证上。

如果配置文件不在项目根目录，可额外传 `--config {CONFIG_PATH}`；不传时会读取项目根
目录的 `.cm-workflow.yml` / `.yaml` / `.json`。

不要启动前另跑一遍机械检查。收到check_runtime时按原平台入口执行一次：macOS/Linux/WSL和Git Bash用cm-check-runtime.sh，Windows PowerShell用cm-check-runtime.ps1；原cm-check-entry.mjs仍保留为单独机械检查入口。PowerShell仍依赖CLAUDE_CODE_GIT_BASH_PATH或Git for Windows Bash，缺失如实阻断，不跳过、不自动安装。
`invocation.args` 已包含 `--print-effective`，宿主须原样执行，以保留有效配置检查；不要把此参数加到 `serve` 命令上。
原实际结果回传后，JS在机械失败时保留输出并停止；通过才发check_semantic，在该请求内执行以下八组检查，再由JS校验覆盖和汇总。

## 语义检查

1. **Codex 入口**（按 `installMode` 分流）：`cm-idea/cm-init/cm-prd/cm-ai/cm-test/cm-security/cm-fix/cm-refactor/cm-check/cm-runtime` 十个核心 Skill 与独立 `external-expert` Skill 均有合法 frontmatter，两种模式都查。`plugin` 模式另查 `.codex-plugin/plugin.json` 的 `skills` 指向 `./skills/`；`claude-compat` 模式没有该清单文件（安装器不生成），这一半记 `not_applicable` 并说明，不记 blocked。
2. **共享真相**：十个核心 Skill 引用 `runtime/` 合同；`external-expert` 引用共享外部专家合同；`compat/claude-commands/cm-*.md` 只是 macOS/Linux 旧入口薄包装，不再复制业务规则。
3. **流程链路**：`cm-ai` 的 N1–N8 引用全部存在；`cm-prd` 的 greenfield/brownfield/change-mode 全部存在；`cm-idea` 引用 `idea-to-prd`；`cm-prd/cm-ai/cm-test/cm-qa-engineer` 共用 `runtime/test-contract.md`；`cm-prd/cm-ai/cm-test/cm-security/cm-fix/cm-refactor/external-expert` 共用 `runtime/logging.md` 与统一 writer；`cm-test --generate-cases` 生成校验后的 inferred 草稿并硬停止。
4. **角色链路**：N3 引用的 `cm-*-engineer/manager/expert` Skill 存在；Claude `agents/` 中每个兼容角色能找到对应工种 Skill。Codex 不依赖这些 `.md` agent 文件；配套完整性核对用户级 `runtimes.yml` 的安装器/cm-runtime 生成方与 cm-workflow-config 消费方，cm-runtime 是独立工具、不配工种。
5. **状态与审查**：`.cm-specs-status`、`.cm-status.json`、`.cm-run.json`、`tasks.md`、可选 `test-cases.json`、`METRICS.md`、`LESSONS.md`、`运行日志.jsonl` 及 `.reviews/` 的生成方与消费方配对；项目日志保持权威，全局日志只是私有可重建镜像；N4 凭证头包含 reviewer/independent/task/round/at/scope；`cm-fix` 收口前机械检查修后审查凭证；`.external/` 不得冒充 N4/N5 凭证。
6. **模板路径**：所有 `{CM_WORKFLOW_ROOT}/templates/...` 引用都对应真实文件，重点核对 `templates/rules/`、`templates/ui-lens/`、`templates/hooks/`、`templates/refactor/`。
7. **版本**（按 `installMode` 分流）：`plugin` 模式核对根 `VERSION` 与 `.codex-plugin/plugin.json` 一致，并核对根 `README.md` 不宣称不存在的入口或安装路径；`claude-compat` 模式的版本标志是 `templates/cm-VERSION`，根 `VERSION` 与根 `README.md` 均不由安装器生成（`install.sh` 只写 `templates/cm-VERSION`），这两项记 `not_applicable` 并说明，不记 blocked。
8. **私有调用清零**：Codex 核心 Skill 不得残留 `TaskCreate`、`TodoWrite`、`codex:review`、`~/.claude/commands`；兼容包装中出现 `/cm:*` 是合法的 macOS/Linux 旧入口。

传入 `--project` 时机械检查额外输出「运行时声明对照」：按项目 > 用户级默认 > 未声明读取
`runtimes.available`，声明的一家若本机 CLI 不可解析只打 `WARN`（可解析≠配额可用，不算失败）；
并逐行打印 coder/reviewer 的 `route_state`，`declared-adapter` 标「已声明未派发」。这是诊断，不是授权。
`route_state` 相对当前运行时才有意义：按 `--runtime` > `CM_RUNTIME` 取值，两者都没有时
记 `未判定`，不得把未指定运行时读成「审查通道没派出去」。

外部能力只做降级提示，不应导致插件自检失败：状态条、后台定时更新器、子代理、隔离 CLI
审查通道与 external-expert 浏览器 transport 都是可选增强。浏览器不可用时必须能输出
手工 handoff packet，不能把可选通道缺失报成核心运行时失败。

## 输出

```text
🔍 cm-check  (plugin v{X.Y.Z})
版本更新: {已升级 旧版 → 新版 / 已是最新 / 本地领先 / 无法确认 / 未执行及原因}
Codex 入口: {通过/失败}
Claude 兼容: {通过/失败}
流程与角色: {通过/断链清单}
状态与审查: {通过/断链清单}
模板与版本: {通过/不一致清单}
可选增强: {已配置/降级项}
结论: PASSED / FAILED ({N} 处) / BLOCKED（附未查完的组） / MECHANICAL_ONLY（--quick，未做语义检查）
```

第 1、7 组的 `not_applicable` 只适用于另一种安装模式独有的产物，且必须写明缺的是哪个文件、为何本模式不该有；
其余各组以及本模式确实拥有的产物，证据不足一律记 blocked，不得借 `not_applicable` 放行。

除上述安装升级外，只报告可复现的断链，不自动修复项目文件或配置。
独立的 `cm-check-host.mjs`、`cm-check-entry.mjs`、`cm-check-runtime.sh/.ps1` 仍只检查，
不会联网升级；CI、安装器与发版校验调用这些入口，不递归触发更新。

代码漏洞扫描请使用相邻 `../cm-security/SKILL.md`；cm-check 的安装/结构检查不代替漏洞扫描。
