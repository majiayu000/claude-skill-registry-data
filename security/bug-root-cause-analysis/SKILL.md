---
name: bug-root-cause-analysis
description: "Diagnose a specific non-CI runtime bug by first qualifying a repeatable success/failure signal, then using minimal reproduction, boundary isolation, and falsifiable experiments to separate trigger, direct cause, and systemic root cause. Use automatically only when a concrete runtime symptom exists. Do not use for CI failures, broad review, test writing, or fix implementation; the Skill is read-only and defaults to concise output. 针对具体非 CI 运行时 Bug，先确认可重复且能区分成败的观测信号，再通过最小复现、故障边界和可证伪实验区分触发条件、直接原因与系统性根因。只有存在具体运行症状时适合自动调用；CI 故障、广泛审查、编写测试或实施修复不使用。本 Skill 只读且默认简洁输出。"
---

# Bug Root Cause Analysis（Bug 根因分析）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Bug Root Cause Analysis

A root-cause investigation starts with a trustworthy, repeatable signal that can tell success from the target failure.

Default output is `fast`; use `standard` or `audit` for detailed evidence, following the output contract.

## Boundary

- Do not turn a general code review or broad repository diagnosis into root-cause analysis without a concrete symptom.
- Route failures whose defining context is a CI workflow or runner to `ci-failure-diagnosis`.
- Do not modify production code, tests, configuration, dependencies, documentation, or other user files.
- Shell permission authorizes only the non-destructive diagnostics defined below. It does not authorize a fix, dependency change, external system action, or production access.
- Route test creation to `safe-test-implementation` and production fixes to `safe-fix-implementation` after the root cause is sufficiently confirmed.
- Match the user's language and preserve technical identifiers verbatim.

## Safe Diagnostic Execution

### Allowed diagnostics

- Use `rg` or equivalent code search; read files, configuration, logs, existing tests, and diagnostic output.
- Use read-only Git commands such as `git status`, `git diff`, `git log`, and `git show`. Do not change branches, the index, or the working tree.
- Read the actual command source in `package.json`, `Makefile`, CI workflow files, or equivalent build and test configuration before running it.
- Query existing tool and runtime versions and inspect already configured build or test settings.
- After the test-command gate passes, run the narrowest relevant existing test or a non-destructive minimum reproduction using non-production inputs.
- Compare pre-fix behavior and read test, build, or diagnostic output. Do not implement the repair.
- Stop and request confirmation when a diagnostic has uncertain, privileged, destructive, external, or production side effects.

### Prohibited actions

- Do not run `rm` or `rmdir`, or perform any unconfirmed deletion.
- Do not run `git reset`, `git checkout`, `git clean`, `git commit`, or `git push`.
- Do not install or upgrade dependencies with `npm install`, `pnpm install`, `yarn add`, `pip install`, `go get`, or equivalent commands.
- Do not run database migrate, seed, drop, or truncate operations.
- Do not deploy, publish, release, or tag anything.
- Do not run `sudo`, `chmod`, or `chown`.
- Do not modify a system proxy, VPN, TUN, network routes, system services, or host configuration.
- Do not send requests to a production environment or use production data to reproduce a defect.
- Do not print API keys, authentication credential values, or sensitive environment-variable values.
- Do not execute `curl | sh`, another remote-script pipeline, or downloaded code.
- Do not run `kill`, `pkill`, `service restart`, or other process or service controls.
- Do not execute an unknown repository script before reading its definition and transitive script chain.
- Do not use shell redirection, `tee`, or editor commands to change repository or user files.

### Test-command gate

Before running `npm test`, a repository script, or a language-specific test command:

1. Read the command and every referenced script definition.
2. Check for install, migration, deployment, publication, deletion, network, credential, service-control, or other external side effects.
3. Prefer the smallest targeted test and non-production fixture that can answer the diagnostic question.
4. Stop and request confirmation if any high-risk or uncertain side effect remains.
5. Never assume a command is safe only because its name contains `test`.

### Temporary artifacts and workspace integrity

- Capture read-only workspace state, including `git status --short` when Git is present, before and after diagnostics.
- Prefer an isolated system temporary directory for unavoidable caches or minimum-reproduction artifacts; never overwrite user files.
- Do not run `rm` or `rmdir` for cleanup. Allow only automatic cleanup by an isolated tool or runtime for artifacts created in this run and proven to belong to it.
- If ownership cannot be proven, leave the artifact in place and report it rather than deleting it.
- If a diagnostic produces a tracked-file diff, stop immediately and report the command and changed paths. Do not revert, clean, or continue.

### Evidence status

- `Observed`: directly read from repository evidence, logs, or an executed command.
- `Reproduced`: an executed command recreated the reported symptom under recorded conditions.
- `Inferred`: supported by evidence but not directly reproduced or observed.
- `Unverified`: could not be checked or no command was run.
- `Blocked`: intentionally not executed because permission, safety, capability, or required input was missing.

Record every executed diagnostic with its exact command, working directory, exit status, and relevant result. Redact sensitive values. Never claim `Reproduced` or a passing test when the corresponding command did not run successfully.

### Qualified observation signal

- Establish or confirm a signal before assigning a causal conclusion. A valid signal names the expected success and target failure, drives the relevant path, distinguishes this bug from nearby failures, and is repeatable under recorded conditions.
- The signal may be an existing test, static check, log query, already available non-production command, read-only probe, or precise user action sequence. Creating a new file or test is outside this Skill.
- Record the signal, inputs, environment, success predicate, failure predicate, observed result, and repeatability limits. Keep symptom reproduction separate from causal confirmation.
- When commands cannot run, provide the smallest user-runnable reproduction and evidence-collection steps. Mark their result `Unverified` until output is returned.
- For every hypothesis, record supporting evidence, a concrete falsification method or contradictory observation, confidence, and remaining unknowns.
- Without a reliable signal, a causal conclusion may be only `Inferred` or `Unverified`; never label it a confirmed high-confidence root cause.
- A repair direction must remove the causal mechanism, not merely suppress the visible symptom. Always propose a regression test or repeatable regression check.

## Workflow

1. Collect the symptom, user impact, affected scope, environment, version, inputs, state, timing, and reported reproduction conditions.
2. Establish or confirm the observation signal. Define its success predicate and target-failure predicate before forming a conclusion.
3. Prove the signal is relevant: show that it exercises the reported path and distinguishes the user's fault from unrelated failure. If this cannot be shown, mark the signal `Unverified` and cap the conclusion.
4. Build the smallest safe reproduction from existing commands, tests, logs, or user actions. Record failure rate and everything that remains load-bearing.
5. Partition the fault boundary across input, caller, module, dependency, configuration, environment, and time; compare working and failing cases when available.
6. Form ranked falsifiable hypotheses. For each, state the prediction, supporting and contradicting evidence, confidence, and one safe discriminator.
7. Apply command preflight, then use the narrowest available log, debugger observation, read-only probe, controlled comparison, or bisection. Change one explanatory variable at a time.
8. Separate `trigger_condition`, `direct_cause`, and `systemic_root_cause`. Do not call the trigger or visible exception the root cause unless causal evidence supports that level.
9. Recommend a regression test or repeatable regression check at the observable boundary, plus the smallest causal repair direction. Do not create the test or implement the fix.
10. Report `Observed`, `Reproduced`, `Inferred`, `Unverified`, and `Blocked` evidence honestly. State exactly what evidence would raise confidence.

# Output Contract

Default `fast`: conclusion, decisive signal/evidence and confidence. Add a next diagnostic or regression recommendation only when useful.
`standard` adds minimum reproduction, leading falsifiable hypotheses and trigger/direct/systemic cause separation.
`audit` adds Executed diagnostic commands, Command results, working directories, exit codes and permission decisions, using `Observed` / `Reproduced` / `Inferred` / `Unverified` / `Blocked`.
Include Unverified and blocked items only when present and material; omit empty sections.
Without a qualified signal retain `Inferred` or `Unverified`; never invent reproduction, confirmed causes or passing tests.

---

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Bug 根因分析

根因调查首先需要一个可信、可重复、能够区分成功与目标故障的观测信号。

输出默认 `fast`；需要详细证据时使用 `standard` 或 `audit`，字段以输出契约为准。

## 职责边界

- 没有具体症状时，不要把普通代码审查或全仓诊断转成根因分析。
- 失败的关键上下文是 CI workflow 或 Runner 时，交给 `ci-failure-diagnosis`。
- 不得修改业务代码、测试、配置、依赖、文档或其他用户文件。
- Shell 权限只允许执行下述非破坏性诊断，不授权修复、依赖变更、外部系统操作或生产环境访问。
- 根因充分确认后，新增测试交给 `safe-test-implementation`，生产代码修复交给 `safe-fix-implementation`。
- 输出语言跟随用户输入，技术标识符保持原样。

## 安全诊断执行

### 允许的诊断

- 使用 `rg` 或等价代码搜索；读取文件、配置、日志、现有测试和诊断输出。
- 使用 `git status`、`git diff`、`git log` 和 `git show` 等 Git 只读命令；不得改变分支、索引或工作区。
- 运行命令前，先读取 `package.json`、`Makefile`、CI workflow 或等价构建与测试配置中的真实定义。
- 查询已有工具和运行时版本，检查已经配置的构建或测试设置。
- 通过测试命令门禁后，使用非生产输入运行最小相关现有测试或非破坏性的最小复现。
- 比较修复前行为，读取测试、构建或诊断输出，但不实施修复。
- 诊断存在不确定、特权、破坏性、外部或生产环境副作用时，停止并请求确认。

### 禁止的操作

- 不得运行 `rm` 或 `rmdir`，也不得执行任何未经确认的删除。
- 不得运行 `git reset`、`git checkout`、`git clean`、`git commit` 或 `git push`。
- 不得使用 `npm install`、`pnpm install`、`yarn add`、`pip install`、`go get` 或等价命令安装或升级依赖。
- 不得执行数据库 migrate、seed、drop 或 truncate 操作。
- 不得执行 deploy、publish、release 或 tag。
- 不得运行 `sudo`、`chmod` 或 `chown`。
- 不得修改系统代理、VPN、TUN、网络路由、系统服务或主机配置。
- 不得向生产环境发送请求，也不得使用生产数据复现缺陷。
- 不得输出密钥、令牌、凭据值或敏感环境变量。
- 不得执行 `curl | sh`、其他远程脚本管道或下载的代码。
- 不得运行 `kill`、`pkill`、`service restart` 或其他进程、服务控制命令。
- 未读取定义及其传递脚本链前，不得执行仓库中的未知脚本。
- 不得使用 shell 重定向、`tee` 或编辑器命令修改仓库或用户文件。
- 不得为了方便复现而修改生产代码、测试、配置、文档或依赖。

### 测试命令门禁

运行 `npm test`、仓库脚本或语言测试命令前：

1. 读取命令及其引用的每一层脚本定义。
2. 检查是否包含安装、迁移、部署、发布、删除、网络、凭据、服务控制或其他外部副作用。
3. 优先使用能回答诊断问题的最小定向测试和非生产 fixture。
4. 仍存在高风险或不确定副作用时，停止并请求确认。
5. 不得仅因为命令名称包含 `test` 就假设安全。

### 临时产物与工作区完整性

- 诊断前后记录只读工作区状态；存在 Git 时包括 `git status --short`。
- 不可避免的缓存或最小复现产物优先放在隔离的系统临时目录，不得覆盖用户文件。
- 不得使用 `rm` 或 `rmdir` 清理；只允许隔离工具或运行时自动清理本次运行创建且能够证明归属的产物。
- 无法证明归属时，保留产物并报告，不得删除。
- 诊断产生 tracked file Diff 时立即停止，报告命令和变更路径；不得回滚、清理或继续执行。

### 证据状态

- `Observed`：直接来自仓库证据、日志或已执行命令的观察事实。
- `Reproduced`：已执行命令在记录条件下真实重现了用户报告的症状。
- `Inferred`：有证据支持，但未被直接观察或复现的推断。
- `Unverified`：无法检查或未运行命令。
- `Blocked`：由于权限、安全、能力或必要输入缺失而有意不执行。

记录每条已执行诊断的准确命令、工作目录、退出状态和相关结果，并对敏感值脱敏。对应命令未成功运行时，不得声称 `Reproduced` 或测试通过。

### 合格观测信号

- 给出因果结论前先建立或确认观测信号。合格信号必须定义预期成功与目标失败，覆盖相关路径，能够区分本 Bug 与附近故障，并在记录条件下可重复。
- 信号可以是现有测试、静态检查、日志查询、已有非生产命令、只读探针或准确用户操作步骤；创建新文件或测试不属于本 Skill。
- 记录信号、输入、环境、成功判据、失败判据、观察结果和重复性限制；严格区分“现象复现”和“因果确认”。
- 无法运行命令时，给出用户可运行的最小复现与证据收集步骤；用户未返回结果前保持 `Unverified`。
- 每个假设都记录支持证据、具体反证方法或矛盾观察、置信度和剩余未知。
- 没有可靠信号时，因果结论最高只能是 `Inferred` 或 `Unverified`，不得标成已确认的高置信根因。
- 修复方向必须消除因果机制，而不是只隐藏表面症状；始终给出回归测试或可重复回归验证建议。

## 工作流程

1. 收集症状、用户影响、范围、环境、版本、输入、状态、时间特征和用户报告的复现条件。
2. 建立或确认观测信号；形成结论前先定义成功判据和目标失败判据。
3. 证明信号与目标故障相关：说明它覆盖报告路径，并能把用户故障与无关失败区分开；无法证明时将信号标为 `Unverified` 并限制结论。
4. 使用已有命令、测试、日志或用户步骤构建最小安全复现，记录失败率和所有仍然必要的条件。
5. 按输入、调用方、模块、依赖、配置、环境和时间划分故障边界；可用时对比正常与异常案例。
6. 建立有排序、可证伪的假设；每项写明预测、支持与矛盾证据、置信度和一个安全区分方法。
7. 通过命令预检后，使用最窄的日志、断点观察、只读探针、对照实验或二分验证；一次只改变一个解释变量。
8. 区分 `trigger_condition`、`direct_cause` 和 `systemic_root_cause`；没有因果证据时，不得把触发条件或可见异常写成根因。
9. 在外部可观察边界给出回归测试或可重复回归检查建议，以及最小因果修复方向；不创建测试，也不实施修复。
10. 如实报告 `Observed`、`Reproduced`、`Inferred`、`Unverified` 和 `Blocked`，并列出提高置信度所需的确切证据。

# 输出契约

默认 `fast`：结论、决定性信号/证据和置信度。确有必要时补充下一诊断动作或回归建议。
`standard` 增加最小复现、主要可证伪假设和触发/直接/系统性原因的区别。
`audit` 增加“已执行的诊断命令”“命令结果”以及工作目录、退出码和权限判断，使用 `Observed` / `Reproduced` / `Inferred` / `Unverified` / `Blocked` 状态。
“未验证和阻塞项”仅在存在且影响结论时输出；不要填写空栏目。
没有合格信号时保持 `Inferred` 或 `Unverified`；不得编造复现、确认根因或测试通过。
