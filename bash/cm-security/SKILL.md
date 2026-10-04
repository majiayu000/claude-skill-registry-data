---
name: cm-security
description: 用户运行 cm-security，或要求代码安全扫描、漏洞检查、密钥泄露排查、依赖漏洞检查时使用。默认检查当前分支相对主分支及已跟踪未提交修改，结合业务地图复核；--all 检查全部已跟踪文件。只报告问题，不自动修复、安装、升级或发布。安装自检用 cm-check，功能测试与覆盖率用 cm-test。
---

# cm-security — 代码安全扫描与业务复核

先读 `../../runtime/project-context.md`、`../../runtime/logging.md` 和 [执行合同](references/scan-contract.md)。
本 Skill 是独立只读安全入口；不改变 cm-test、任务完成门禁或发布授权。
Codex 用 `$cm-security`，Claude Code 用 `/cm-security`；macOS/Linux 兼容 `/cm:security`。

## 用法

```text
$cm-security
$cm-security {项目路径}
$cm-security {项目路径} --all
$cm-security {项目路径} --semgrep-rules {已审查的外部本地规则文件}
$cm-security {项目路径} --osv-db {外部离线数据库缓存目录}
```

## 执行

1. 省略项目时解析当前 Git 仓库根。显式路径也定位到该仓库根；无 Git/HEAD、主分支缺失或有歧义时停止并说明，不猜基准，不自动 fetch。`--all` 不要求主分支，但仍要求 Git/HEAD。
2. 先确认地图在 Git index 中为普通已跟踪文件，再加载业务地图，只读核对受影响的入口、调用方、权限与数据流。地图缺失、陈旧或失真时，从相关代码补足本次分析，标明缺口；不自动全仓重建或更新地图。
3. 从当前 Skill 位置解析 `{CM_WORKFLOW_ROOT}`，逐项传参数，禁止拼接用户文本为 shell 命令：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-security.mjs" --project "{项目根}" {已解析的可选参数}
```

4. 将扫描 JSON 原样保存在项目外本次私有目录的普通文件中，保留范围、digest、工具状态、遗漏和 findings。退出码 1 表示发现候选问题，3 表示检查仍不完整，均需继续上下文复核；2 表示阻断，只汇报阻断原因。0 可能是 NO_CHANGES，不是安全认证。
5. 对 selected 中每个路径做轻量 AI 复核。先看改动及调用链，再看扫描候选；只加载相关代码，禁止默认加载整套外部审计 Skill。命中或触及鉴权、支付、跨租户、命令/文件/网络边界时，沿该路径深入。
6. 逐项核验输入是否可控、现有防护是否有效、受影响业务及复现条件。分别检查工作区与不同的暂存版本；删除或改名必须结合基准版本和调用方，不能只看剩余文件。引用 `revision + 文件:行号`。
7. 对越权、注入、路径穿越、SSRF、敏感信息暴露、依赖漏洞给出有证据的判断。工具输出只算候选；没有测试或一般最佳实践不足以认定漏洞。无需主动执行 PoC、项目脚本、安装依赖或访问业务服务。
8. 按[复核 JSON 合同](references/scan-contract.md#finalize-报告门禁)生成逐路径复核结果，写入项目外普通文件；不得传入 result、coverage 或 aiReview。必须调用以下命令；它内部重跑 inventory 核对复核窗口漂移，保留扫描窗口证据，机械核对漏报与覆盖率：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-security.mjs" --project "{项目根}" --finalize --scan "{外部扫描报告.json}" --review "{外部复核结果.json}"
```

9. 以 `--finalize` 返回的 `result`、`coverage`、`gaps` 与 `reportPath` 输出简短结论，模型不再自行决定结论词。读取私有报告的 `checkSummary`，逐项展示已完成、已尝试但失败、未运行及原因，再列 `nextSteps`；OSV 数据库新旧未知或生态未核验必须保留，不能把工具执行成功写成数据已更新。宿主在项目外创建私有报告目录；BLOCKED 时报告证据过期或输入错误，不替用户回滚。最终 JSON 原样保留校验通过的分析结论及未复核 reason，按路径列出未复核项；stdout 仅含六个摘要字段，不含自由描述。脱敏针对工具原始 stdout/stderr、密钥原文与源码片段；模型不得把这些内容粘进复核字段，JS 无法验证这项语义义务。默认扫描不自动修复、不安装、不提交、不上传给额外服务；需要修复时将证据交给用户决定。

范围、业务地图与安全边界确认后按 `runtime/logging.md` 写 `run_start`；`--finalize` 返回终态后写 `run_done`，只记录扫描范围、结论词、发现数量、覆盖率与报告路径。本 Skill 通常在没有 specs 目录的项目上独立运行，保存首次写入器返回的 `run_id` 并在后续事件显式传回。工具原始 stdout/stderr、密钥原文、源码片段与 findings 正文不进日志；`BLOCKED` 同样写 `run_done`，detail 只写阻断原因。写日志不改变本 Skill 的只读边界。

## 报告

```text
安全检查：FINDINGS / REVIEWED_PARTIAL / NO_CHANGES / BLOCKED
范围：基准 → 当前分支 + 已跟踪暂存/工作区，或全部已跟踪文件
业务地图：已核验 / 部分核验 / 缺失 / 陈旧
发现：严重程度、文件:行号、受影响业务、证据与修复建议
已完成或尝试：工具、检查内容、版本、完成/失败及已有缺口
未运行：工具、原因（如未指定 Semgrep 规则、未提供 OSV 离线数据库）
需要补齐 / 下一步：逐项列规则、工具、离线数据或人工核验要求
AI 复核：completed、已复核路径、未复核路径及原因、分析结论与修复建议
源码一致性：扫描窗口、复核窗口分别列出；综合一致 / 变化
报告：绝对路径
```

存在候选问题时使用 FINDINGS，并分清已确认与待验证；源码漂移或范围不可信优先 BLOCKED。
无发现且有选中路径时一律使用 REVIEWED_PARTIAL，包括 coverage 为 FULL 的情况。
即使所选检查全完成，也只能说明本轮未发现问题，不能输出“没有漏洞”或替代独立 Review。
未跟踪文件只报告数量，不读取；需要包含时由用户明确选择并另行确认范围，不自动 git add。
