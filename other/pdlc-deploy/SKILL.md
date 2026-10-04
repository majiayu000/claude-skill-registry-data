---
name: pdlc-deploy
description: 创建部署文档
argument-hint: <v<版本> | 功能ID | 服务名 | 应用名>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: deploy
produces:
  - docs/05_deployment/**
requires: []
next_step: null
terminal_state: deploy_done
---

# 创建部署文档

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->
<!-- @include templates/prompts/noninteractive.md（已内联于下方，无需另读） -->
## 非交互模式（`--autonomous`）

若本命令的参数含 `--autonomous`，本命令进入**无人值守**模式，按以下规则处理原本需要人应答的交互点。**参数是唯一真源**：不带 `--autonomous` 即为交互模式，一切照旧正常询问用户；绝不回读状态机 `run_mode` 兜底（「掉出 autonomous」是安全的失败方向）。

1. **流程性确认**（如「测试已绿是否继续」「是否覆盖已有文件」）→ **不询问**，按预设默认前进，并把决策追加到状态机 `history[].auto_decisions[]`：
   ```json
   { "point": "<确认点描述>", "chose": "<所选默认>", "at": "<ISO 8601>" }
   ```
2. **真需人判断**（PRD 关键取舍、评审「需人工确认」项、真实循环依赖等无法安全默认的点）→ **不猜**：
   - `current_stage` 保持不变（不推进）
   - 写 `last_phase_result.ok = false` 且 `blocked_reason = "<原因>"`
   - 末行输出哨兵：`<<<PDLC blocked reason="<原因>">>>`
   - 立即结束命令，交还人类
3. **破坏性操作**（发布 / 部署 / 打 tag / 触发 CI / DROP / force-push 等不可逆·外发操作）→ `--autonomous` **无效**，仍必须人工显式确认。
4. **顺手的 sidecar 产物**（如缺失时创建 `CHANGELOG.md`、补全文档 PDLC-TRACE 的创建时间等本阶段职责内、可安全默认的辅助改动）→ 视为流程性默认，**直接做并记入 `auto_decisions[]`**；这类改动不新增外部副作用，不属破坏性操作。

> 进入 autonomous 模式时，在状态机顶层写 `run_mode: "autonomous"` 仅供留痕（复盘区分人工 vs 循环产出）。
<!-- @include-end templates/prompts/noninteractive.md -->

> ⛔ **部署面向生产、不可逆·外发**：真实执行部署属破坏性范畴。**`--autonomous` 对涉及真实部署动作的环节无效**——仍必须人工显式确认。本命令默认只产出部署**文档**，不代表授权自动上线。

为一次发布、指定服务或应用创建部署手册。

## PDLC 前置检查（必须执行，不可跳过）

先按输入形态确定本次部署涉及的功能：

- **版本号**（`v1.2.0` / `1.2.0`，`/pdlc-ship` 交接时给的就是它）→ **发布级部署**：读 `CHANGELOG.md` 里 `## [<版本>]` 段，
  收集其中的功能 / 缺陷 ID（`F…` / `B…`）；这些就是本次部署涉及的功能。
  段落不存在 → 停止并提示先跑 `/pdlc-ship`。段落里一个 ID 都没有（如只发了文档 / 依赖升级）→ 照常出发布级文档，跳过下面的评审记录查找
- **功能ID**（`F…` / `B…`）→ 单个功能
- **服务名 / 应用名 / 关键词** → 按下面第 2 步搜评审记录

对上面确定的每个功能（或关键词）做评审记录检查：

1. 从用户输入中提取服务/功能名称关键词（输入已是版本号或功能ID时，用上面确定的功能ID）
2. 在 `docs/07_reviews/code/` 目录下搜索包含该功能ID或关键词的评审记录
   - 匹配新格式：`F<日期>-<编号>-*<关键词>*-review.md`
   - 匹配旧格式：`YYYYMMDD-*<关键词>*-review.md`
   - 同时检查文件内容中是否包含该关键词
3. **未找到评审记录** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的评审记录。
   部署文档必须基于已完成评审的代码。请先运行：
   👉 /pdlc-review <评审目标>
   ```
4. **找到** → 提取功能ID（如 `F20260326-090000`），读取评审记录内容，继续执行。
   发布级部署时逐个功能检查，缺评审记录的功能列在停止信息里一并指出

## 工作流程

1. 阅读目标服务/应用的 README.md 和技术栈信息
2. 阅读 `docs/02_design/architecture/` 下的架构设计文档（如有）
3. 阅读评审记录，确认功能状态
4. **【必须创建文件】** 在 `docs/05_deployment/guides/` 下创建部署手册
   - **使用模板**: 本 skill 目录下的 `assets/deploy-doc-template.md`（结构完整、章节齐全）
   - **文件名格式**：
     - 发布级部署：`v<版本>-deploy.md`（如 `v1.2.0-deploy.md`）——一份文档覆盖本次发布的全部功能，
       各功能涉及的配置 / 迁移 / 回滚要点在文档里分节写明
     - 单个功能：`<功能ID>-<功能名>-deploy.md`（如 `F20260326-090000-user-auth-deploy.md`）
     - 若无功能ID，则使用旧格式 `YYYYMMDD-<服务名>-deploy.md`
   - **文档顶部必须包含 PDLC 追溯头**（发布级部署的 `功能ID` 与 `前置文档` 列出全部，逗号分隔，并加一行 `版本`）：
     ```
     <!-- PDLC-TRACE -->
     <!-- 功能ID: F20260326-090000 -->
     <!-- 功能名称: user-auth -->
     <!-- 阶段: 部署 -->
     <!-- 前置文档: docs/07_reviews/code/F20260326-090000-user-auth-review.md -->
     ```
     发布级示例：`<!-- 功能ID: F20260326-090000, B20260328-140000 -->`、`<!-- 版本: v1.2.0 -->`

## 文档内容

- 前置条件（环境要求、依赖服务）
- 环境配置（环境变量、配置文件）
- 构建步骤
- 部署步骤
- 健康检查验证
- 回滚方案
- 常见问题排查

## 部署文档自审与自动修复（创建后立即执行，不可跳过）

重新阅读刚创建的部署文档，逐项检查以下质量门禁：

### 关键章节检查
- [ ] 前置条件：是否列出了所有运行时依赖（数据库版本、中间件版本、系统配置）
- [ ] 环境变量：是否列出了每个环境变量的名称、用途、示例值、是否必填
- [ ] 构建步骤：是否可直接复制执行，无需额外推断
- [ ] 部署步骤：是否区分了首次部署与升级部署
- [ ] 健康检查：是否定义了健康检查 URL、预期响应、超时时间
- [ ] 回滚方案：是否有明确的回滚步骤（不是简单写「回滚到上一版本」）
- [ ] 数据库迁移：如涉及 DB 变更，是否有迁移执行和回滚步骤
- [ ] 常见问题排查：是否有至少 3 个常见错误场景及解决方案

### 可执行性检查
- [ ] 所有命令是否完整可复制（无省略号 `...`、无占位符未说明）
- [ ] 端口号、域名、路径是否使用了变量或占位符并在前置条件中说明
- [ ] 步骤顺序是否合理（不会因顺序错误导致部署失败）

### 自动修复
- 缺失的健康检查：根据服务类型（HTTP/gRPC）自动补充标准健康检查配置
- 缺失的回滚方案：自动补充基于版本的回滚步骤模板
- 缺失的环境变量说明：从代码中扫描 `process.env`/`os.Getenv`/`System.getenv` 等，自动补充
- 模糊的操作步骤：改写为具体命令
- 缺失的常见问题：自动补充 3 个通用排查项（端口占用、权限不足、依赖不可达）
- 修复后在文档末尾追加审查记录：
  ```
  ## 自审记录
  - 审查时间：<ISO 8601>
  - 发现问题：X 项
  - 自动修复：X 项
  - 修复明细：
    - [已修复] <问题描述>
  ```

## 要求

<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- 步骤要具体可执行，不要模糊描述
- 包含回滚方案
- 如需 Docker 部署，同时生成 Dockerfile 和 docker-compose.yml

目标: $ARGUMENTS

## 段四：更新状态机 + 交接

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `deploy`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `null`（流程到此结束：`next_step` 写 `null`）。
<!-- pdlc:meta-end -->
<!-- @include templates/prompts/state-update.md（已内联于下方，无需另读） -->
## 状态机更新（段四必须执行）

本命令完成主产出后，必须更新状态机文件 `docs/.pdlc-state/<feature-id>.json`。

### 文件格式

```json
{
  "feature_id": "<F/B ID>",
  "feature_name": "<kebab-case>",
  "created_at": "<首次创建时间 ISO 8601>",
  "current_stage": "<当前阶段名>",
  "run_mode": "interactive | autonomous",
  "history": [
    {
      "stage": "<阶段名>",
      "done_at": "<ISO 8601>",
      "produced": ["<相对路径 1>", "<相对路径 2>"],
      "self_audit": { "passed": <N>, "failed": <N>, "manual": <N> },
      "auto_decisions": [
        { "point": "<autonomous 下自动前进的确认点>", "chose": "<所选默认>", "at": "<ISO 8601>" }
      ]
    }
  ],
  "last_phase_result": {
    "stage": "<本次阶段名>",
    "ok": true,
    "advanced_to": "<推进到的下一阶段 | null>",
    "checks": {},
    "self_audit": { "failed": 0 },
    "blocked_reason": null,
    "run_mode": "interactive | autonomous",
    "at": "<ISO 8601>"
  },
  "relations": {
    "extends": [],
    "depends_on": [],
    "supersedes": [],
    "resolves": [],
    "conflicts_with": [],
    "relates_to": [],
    "_updated_at": "<ISO 8601 | 省略>"
  },
  "next_step": "<下一跳命令名，如 pdlc-design；若流程结束则为 null>"
}
```

> ⛔ 示例里的 `"checks": {}` 是「本阶段没有命令可跑」的样子，**不是键名示范**——键名与取值见下方 §1。

> **`relations` 块（RFC#6，Phase 1 可选，Phase 2 推荐）**：6 个 key 对应 6 种关系类型，各为 ID 数组，存**出边**。其中 `conflicts_with` / `relates_to` 是对称类型，两端都要写；其余四种有向，只写在源 feature 上。拿不准时用 `/pdlc-relate set` 写入，它会按规则校验。旧状态文件无此块时视为全空，向后兼容。入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`，不在此块手维护。

> ⛔ **写状态机的四条硬约束**——读侧（`/pdlc-status`、`/pdlc-retro`、`/pdlc-relate`）会逐条体检，
> 违反的每一处都会出现在它们输出的最前面：
>
> 1. **实例里不写 `terminal_state`**。skill frontmatter 的 `terminal_state:` 是「这个命令走完后应到达的终态名」，
>    不是状态字段。判终态只看 `current_stage` 是否以 `_done` 结尾。
> 2. **`history[].stage` 写本命令的阶段短名**（见本命令正文里「本命令的状态机取值」）——`pdlc-implement` 写 `impl`，
>    不写 `implement` / `implementation`；`pdlc-prd` 写 `requirements`，不写 `prd`。
> 3. **时间戳必须带时刻**：`created_at` / `done_at` / `at` 一律写完整 ISO 8601（如 `2026-07-28T10:40:00+08:00`）。
>    只写日期，同一天内的阶段耗时就全部算成 0——读侧只能记「不可测」。
> 4. **`next_step` 只写命令名或 `null`**，不附说明文字（如「pdlc-ship（等评审通过）」）。
>    要说明原因，阻塞时写进 `last_phase_result.blocked_reason`。

> ⛔ **`_done` 的含义是「已发布」，只由 `/pdlc-ship`（写 `ship_done`）与 `/pdlc-deploy`（写 `deploy_done`）写入。**
> 其它命令的 `current_stage` 一律写本命令的阶段短名，走完整条链路的编排命令（`/pdlc-feature`）也一样——
> 它收尾时 `current_stage` 是最后一个阶段的短名，`next_step` 是 `pdlc-ship`。
>
> - 「评审通过、等待发布」就是 `current_stage` 为 `review`（或 `e2e` 等）且 `next_step` 为 `pdlc-ship`。
>   循环相关文档里说的 `review_done` 指的就是这个状态，**不是**要写进 `current_stage` 的值。
> - 为什么：读侧判「已抵达终态」只看 `current_stage` 是否以 `_done` 结尾。评审通过就写 `_done`，
>   `/pdlc-ship` 就分不清哪些功能已经发布过，发布说明会重复或漏收。
> - 旧版本写入的 `feature_done` / `fix_done` / `review_done` 分不清是否已发布，`/pdlc-ship` 会列出来请人确认。

### 更新流程

1. **文件不存在** → 创建文件，写入初始结构（`history` 为含当前阶段的数组）
2. **文件存在** → 读取 JSON，追加当前阶段到 `history`，更新 `current_stage` 和 `next_step`
3. **写回文件**：用 `jq` 或等效工具保持格式化

⚠️ 若更新失败（文件损坏/权限问题），必须中止命令并在最终报告中报错。状态机不可跳过。

### `last_phase_result`（机器可读阶段结果，每个 phase 收尾必写）

顶层 `last_phase_result` 是循环判停的**唯一真源**，外层只需 `jq '.last_phase_result.ok'` 即可决定 继续 / 停止 / 交还人类。规则：

1. **`checks` 必须客观、真跑得来**：只放**真跑命令的退出码**结果（命令取自 `docs/00_standards/test-commands.yml`，见 `test-commands-template.yml`），**绝不用模型自评、绝不填占位**。有测试的阶段用 `tests_pass` / `coverage_pass` / `lint_clean`（退出码 0 → `true`，非 0 → `false`）；stage 语义不同用对应键（如 tdd 段 `{ "red_verified": true }` 表示红灯已验证）。
   > ⛔ **键名与类型都是契约的一部分**：键名只能是 `tests_pass` / `coverage_pass` /
   > `lint_clean` / `e2e_pass`（tdd 段 `red_verified`），值只能是**布尔**。
   > 最常见的两种错法：① 照抄 `test-commands.yml` 的 `unit` / `coverage` / `lint` / `e2e`
   > ——那是**命令表**的字段名，不是状态机的（跑 `unit` 得到的结论写进 `tests_pass`）；
   > ② 写成 `"4 passed, 1 failed"` 这类字符串摘要。两种都会让 `jq '.checks.tests_pass'`
   > 读回 `null`，消费方（发布闸门、质量报告、自主循环）只看到「无法判定」——
   > **你诚实跑出来的结果等于没写**。三态怎么分见本命令正文里「跑 check 命令：退出码的三态语义」一节；正文里没有这一节的命令不跑 check 命令，`checks` 写 `{}`。
   >
   > ⚠️ **没有检查命令可跑的阶段（如 requirements/design 只产文档，或项目无 `test-commands.yml`）→ `checks: {}` 留空。绝不因为「本阶段成功」就把 `tests_pass`/`lint_clean` 等填 `true`——那是虚报，会污染跨工具共用的状态机、误导自主循环判停。** 上面 schema 示例里 `checks` 之所以是空的，正是这个原因——**空是"没跑"的意思，不是键名的示范**。
2. **`self_audit` 单列**：只放自检未通过数，**仅供参考，不作循环判停依据**。
3. **`ok` 的定义**：本阶段全部 `checks` 通过且未命中 `blocked_reason` → `true`；否则 `false`。
4. **命名空间**：`advanced_to` = **下一阶段的短名**，**不是命令名、也不是本阶段的 `current_stage`**。三者关系：`stage`=本阶段短名、`current_stage`=本阶段完成后的当前短名、`advanced_to`=下一阶段短名、`next_step`=下一跳命令名。

   ⛔ **短名不是「命令名去掉 `pdlc-` 前缀」**——`pdlc-implement` 的短名是 **`impl`**，不是 `implement`。别推导，查下表：

<!-- stage-map:start -->
   | `next_step`（下一跳命令名） | `advanced_to`（下一阶段短名） |
   |---|---|
   | `pdlc-tdd` | `tdd` |
   | `pdlc-implement` | `impl` |
   | `pdlc-review` | `review` |
   | `pdlc-design` | `design` |
   | `pdlc-ship` | `ship` |
   | `pdlc-deploy` | `deploy` |
<!-- stage-map:end -->

   `next_step` 为 `null`（终态或无后续）时 `advanced_to` 也是 `null`。

   > 📌 **本表是唯一真源，且是被断言钉住的**：每行的短名必须等于该 skill 自己 frontmatter
   > 里声明的 `stage:`，且任何 skill 的非 `null` `next_step` 都必须在表里有行——两个方向
   > 都由 `tests/frontmatter-check.sh` 检查，所以表不会和实现各自漂移。
   >
   > 写错短名的后果与键名写错同类：消费方按契约名匹配，认不出就当没这个阶段。
5. **推进一致**：`ok=true` 时本阶段必须真的推进了 `current_stage`（与第 6 条 IRON LAW 呼应）；到达终态或无后续时 `advanced_to=null`。`ok=false`（含 blocked）时 `current_stage` 不变、`advanced_to=null`、`blocked_reason` 写明原因。
6. **`run_mode`**：镜像本次调用是否带 `--autonomous`（带了写 `autonomous`，没带写 `interactive`）。
<!-- @include-end templates/prompts/state-update.md -->

**本阶段状态机更新**：只对本次部署涉及、且当前已是 `ship_done` 的功能，追加 `{ "stage": "deploy", ... }` 到其 history，`current_stage` 写 `deploy_done`，`next_step` 写 `null`。
- 涉及但还不是 `ship_done` 的功能（未发布，或旧版终态写法）→ 不改它的状态机，在交接里逐个列出，提示先走 `/pdlc-ship`
- 没有状态机文件的功能（按服务名部署的旧流程）→ 不新建状态机

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->
