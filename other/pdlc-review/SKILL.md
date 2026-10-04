---
name: pdlc-review
description: 代码评审 + 文档评审
argument-hint: <功能ID | PR 描述>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: review
produces:
  - docs/07_reviews/**
requires: []
next_step: pdlc-ship
terminal_state: review_done
recommended_model: sonnet
recommended_effort: medium
---

# 代码评审

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

对指定的服务或应用进行全面的代码评审。

## PDLC 前置检查（必须执行，不可跳过）

1. 从用户输入中提取功能 ID 或功能名称关键词。输入是缺陷 ID（`B` 开头，`/pdlc-fix` 的下一跳）时，
   读 `docs/.pdlc-state/<缺陷ID>.json` 与 `docs/04_testing/defects/` 下对应的缺陷报告，评审对象是这次修复改动的代码
2. **检查实现代码是否存在**：在项目的源码目录下搜索与该功能相关的源代码文件（非测试文件）。源码目录按项目实际布局确定
   （如 `src/`、`app/`、`lib/`、`backend/`、`frontend/`、`packages/*/` 等），不要只看某一种布局；
   已有状态机时，优先看其 history 里 `impl` / `fix` 阶段记下的 `produced` 路径
3. **检查测试是否通过**：找到对应的测试代码并运行，确认测试处于**绿灯状态**（全部通过）
4. **未找到实现代码** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的实现代码。
   评审必须基于已有的代码实现。请先运行：
   👉 /pdlc-implement <目标>
   ```
5. **测试未通过** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：「<功能名>」的测试未全部通过，无法进行评审。
   请先确保所有测试通过后再提交评审：
   👉 /pdlc-implement <目标>（修复失败的测试）
   ```
6. **检查通过** → 确定功能ID（输入即 ID 时直接用；否则从相关设计文档或 PRD 中提取；缺陷修复用缺陷ID），继续执行

## 评审流程

1. **阅读设计文档**: 先阅读 `docs/02_design/` 对应子目录下的相关设计文档
2. **阅读编码规范**: 阅读 `docs/00_standards/coding/` 目录了解编码规范（未命中 → 报告里提示 `consider /pdlc-standard add coding/<topic>`）
3. **检查代码实现**: 对照设计文档逐一检查实现是否符合
4. **检查测试覆盖**: 确认测试是否充分覆盖
5. **代码质量自动检查与修复**（必须执行）：
   - 按 `/pdlc-lint check` 逻辑运行项目 lint 工具
   - 若存在可自动修复的问题，按 `/pdlc-lint fix` 逻辑自动修复
   - 记录修复前后的问题数变化

## 评审检查项（逐项检查，发现问题立即修复）

**先判断适用性**：下面的清单按 Web 服务写成，不是每个项目都有接口、数据库或页面。
开始前按项目类型（Web 服务 / CLI 工具 / 库 / 桌面应用 / 数据脚本等）与本次改动范围，逐项判断是否适用：

- 适用 → 正常检查，勾选 `[x]` 或记为问题
- 不适用 → 标 `[—] 不适用：<一句话理由>`（如「无 HTTP 接口」「本次改动不涉及数据库」）。不适用项**不算未通过**，也不进自动修复
- 拿不准是否适用 → 按适用检查

### 设计一致性（对照设计文档）
- [ ] 每个 API 接口的 URL、方法、参数是否与设计文档一致
- [ ] 数据库表结构、字段名、类型是否与 DB 设计一致
- [ ] 响应格式是否符合项目约定的统一格式（以设计文档 / 编码规范为准，如 `{ code, message, data }`）

### 代码质量
- [ ] 命名是否规范（变量/函数/类遵循项目命名约定）
- [ ] 是否有重复代码可提取为公共方法
- [ ] 错误处理是否合理（不吞异常、不用空 catch、有意义的错误信息）
- [ ] 日志是否充分（关键操作有日志、不打印敏感信息）

### 安全检查
- [ ] SQL 注入：是否使用参数化查询/ORM，无字符串拼接 SQL
- [ ] XSS：用户输入是否转义后再输出
- [ ] 权限控制：接口是否有鉴权，敏感操作是否有权限校验
- [ ] 敏感数据：密码是否加密存储、Token 是否有过期机制、日志不含敏感字段

### 性能检查
- [ ] 数据库查询是否有 N+1 问题
- [ ] 列表接口是否有分页
- [ ] 是否有不必要的全表扫描（缺失索引）
- [ ] 大数据量操作是否有批处理

### 测试完备性
- [ ] 单元测试覆盖率是否达标（覆盖率达标线**以项目配置为准**：优先取 `docs/00_standards/test-commands.yml` 的 coverage 命令阈值参数（那才是强制点，退出码即判定），其次 `quality-targets.yml`；两者都没有时按 >= 80% 兜底。）
- [ ] 核心业务路径是否有完整的测试
- [ ] CHANGELOG 是否已更新

## 自动修复（评审中发现的问题，能修则修）

对以下类型的问题**直接修复代码，不仅仅记录**（只修适用项里发现的问题——标为不适用的检查项，一律不据此改代码；
例如项目没有列表接口，就不会去「补分页」）：

1. **lint 问题**：运行 lint fix 自动修复格式、规范问题
2. **命名不规范**：自动重命名为符合项目约定的名称
3. **缺失错误处理**：自动补充 try-catch / 错误码返回
4. **缺失日志**：在关键操作处自动添加日志语句
5. **SQL 注入风险**：自动改写为参数化查询
6. **XSS 风险**：自动添加输出转义
7. **缺失分页**：自动为列表接口补充分页逻辑
8. **缺失 CHANGELOG**：自动追加变更条目

**不可自动修复的问题**（记录到评审报告，标记为需人工处理）：
- 架构层面的设计问题
- 业务逻辑的正确性争议
- 需要重大重构的性能问题

## 评审报告生成

> ⚠️ **必须创建文件，不可仅在对话中输出。**

**【必须创建文件】** 在 `docs/07_reviews/code/` 下创建评审记录：
- **文件名格式**: `<功能ID>-<功能名>-review.md`（如 `F20260326-090000-user-auth-review.md`）
- **文档顶部必须包含 PDLC 追溯头**：
  ```
  <!-- PDLC-TRACE -->
  <!-- 功能ID: F20260326-090000 -->
  <!-- 功能名称: user-auth -->
  <!-- 阶段: 评审 -->
  <!-- 前置文档: docs/02_design/api/F20260326-090000-user-auth-api.md -->
  <!-- 创建时间: 2026-03-26T10:30:00 -->
  ```
- **报告内容格式**：
  ```markdown
  ## 评审总结
  - 评审时间：<ISO 8601>
  - 评审范围：<涉及的文件数和代码行数>
  - 问题总数：X 项（阻塞: X / 严重: X / 一般: X / 建议: X）
  - 自动修复：X 项
  - 需人工处理：X 项

  ## 自动修复记录
  | # | 问题类型 | 文件 | 修复内容 |
  |---|---------|------|---------|
  | 1 | lint | src/xxx.ts | 修复 XX 规则违规 |

  ## 需人工处理
  | # | 严重程度 | 问题描述 | 建议方案 |
  |---|---------|---------|---------|
  | 1 | 阻塞 | XXX | 建议 XXX |

  ## 评审检查项结论
  - [x] 设计一致性：通过
  - [x] 代码质量：通过（X 项已自动修复）
  - [ ] 安全检查：X 项需人工确认
  - [—] 性能检查：不适用（<理由>）
  ```

6. **修复后验证**：自动修复完成后，重新运行全部测试（命令取自 `docs/00_standards/test-commands.yml`），确认修复未引入新问题
   - 测试通过 → 评审完成
   - 测试失败 → 回滚修复，将问题标记为需人工处理
   - **写 `last_phase_result`**：`checks` 取自真跑 test-commands 的 `unit`/`coverage`/`lint` 退出码，不用自检冒充；
     退出码三态语义与「命令跑不了 = yml 过期信号」见下方 check 命令规则
7. **`--autonomous` 下的收尾判定**（呼应非交互契约）：
   - 「需人工处理/需人工确认」表中存在**阻塞级**项 → 不推进：`last_phase_result.ok=false` + `blocked_reason="评审存在阻塞级待人工项"` + 输出 blocked 哨兵，交还人类
   - 仅有非阻塞级人工项 → 记录在案并正常推进：`current_stage` 写 `review`，`next_step` 写 `pdlc-ship`（评审通过即此状态，不写任何 `_done`）

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
- 问题按严重程度分级：阻塞 / 严重 / 一般 / 建议
- **能修的问题直接修复**，不仅仅指出问题
- 修复后必须验证测试仍然通过

评审目标: $ARGUMENTS

---

## 文档评审

对指定的文档进行质量评审，检查完整性、一致性和可操作性。**发现问题直接修复，而非仅列出建议。**

### 文档评审检查项

#### 完整性
- [ ] 是否覆盖了所有必要章节（对照下方「加载对照物」里对应类型的模板检查）
- [ ] 是否有遗漏的功能点或接口
- [ ] 非功能需求是否有说明
- [ ] 是否有明确的验收标准
- [ ] PDLC 追溯头是否完整（功能ID、功能名称、阶段、前置文档、创建时间）

#### 一致性
- [ ] 术语命名是否前后一致（同一概念不用不同名称）
- [ ] 数据模型是否与 API 设计一致（字段名、类型）
- [ ] 接口参数是否与 PRD 需求对应
- [ ] 版本号和日期是否准确
- [ ] 文档间交叉引用路径是否正确

#### 可操作性
- [ ] 操作步骤是否具体可执行（无模糊表述如「适当配置」「按需调整」）
- [ ] 是否有示例代码或示例数据
- [ ] 错误码是否有清晰的处理建议
- [ ] 部署步骤是否可复现

#### 规范性
- [ ] 是否符合对应模板格式
- [ ] 表格是否完整（无空列、无缺失表头）
- [ ] Markdown 语法是否正确（标题层级、列表缩进、代码块语言标注）
- [ ] 输出语言是否符合用户对话语言（或用户显式指定的语言）

### 文档自动修复规则（发现即修，不仅记录）

1. **缺失章节**：对照模板自动补充，内容根据文档已有信息合理推断
2. **PDLC 追溯头缺失或不完整**：自动补全缺失字段
3. **术语不一致**：统一为文档中首次出现的术语，全文替换
4. **模糊表述**：自动改写为具体、可度量的描述
5. **表格格式问题**：自动修复空列、对齐问题
6. **Markdown 语法错误**：自动修复标题层级、列表缩进
7. **交叉引用路径错误**：检查引用的文件是否存在，不存在则标注警告
8. **缺失示例**：为 API 接口自动补充请求/响应示例

**不可自动修复的问题**（记录到评审报告）：
- 业务逻辑的正确性争议
- 需要与产品确认的需求歧义
- 涉及跨文档架构调整的问题

### 文档评审工作流程

1. **识别文档类型**：判断文档属于 PRD / API 设计 / DB 设计 / 架构设计 / 测试计划 / 部署手册
2. **加载对照物**：
   - 加载对应类型的模板（均在本 skill 目录下）：PRD → `assets/prd-template.md`、API 设计 → `assets/api-design-template.md`、DB 设计 → `assets/db-design-template.md`、架构设计 → `assets/arch-design-template.md`、测试计划 → `assets/test-plan-template.md`、部署手册 → `assets/deploy-doc-template.md`
   - 加载前置文档（从 PDLC-TRACE 中获取路径）
   - 如是设计文档，同时加载 PRD 进行交叉比对
3. **逐项检查**：按上方检查项逐一执行
4. **自动修复**：发现问题直接修改原文档
5. **【必须创建文件】生成评审记录**：在 `docs/07_reviews/doc/` 下创建评审记录
   - **文件名格式**: `<功能ID>-<功能名>-<文档类型>-doc-review.md`
   - **报告格式**：
     ```markdown
     ## 文档评审报告
     - 评审时间：<ISO 8601>
     - 目标文档：<文档路径>
     - 文档类型：<PRD/API设计/DB设计/...>
     - 问题总数：X 项（必须修改: X / 建议修改: X / 可选: X）
     - 自动修复：X 项
     - 需人工确认：X 项

     ## 自动修复记录
     | # | 问题类型 | 修复内容 |
     |---|---------|---------|
     | 1 | 缺失章节 | 补充了「非功能需求」章节 |

     ## 需人工确认
     | # | 严重程度 | 问题描述 | 建议 |
     |---|---------|---------|------|
     | 1 | 必须修改 | XXX 需求存在歧义 | 建议与产品确认 |

     ## 检查项结论
     - [x] 完整性：通过
     - [x] 一致性：通过（X 项已修复）
     - [x] 可操作性：通过
     - [x] 规范性：通过
     ```
- 修复后仅复查一次（确认修复未引入新问题），**不再递归修复**。若复查仍发现问题，记录到评审报告的「需人工确认」中

<!-- @include templates/prompts/check-commands.md（已内联于下方，无需另读） -->
## 跑 check 命令：退出码的三态语义

命令取自 `docs/00_standards/test-commands.yml`（唯一真源）。逐条真跑，**按退出码分三态**——
不是两态。这是 IRON LAW「checks 只认客观事实」在执行层的落法：

| 观察到的 | 含义 | 写进 `checks` |
|---|---|---|
| 退出码 `0` | 通过 | 对应键 = `true` |
| 退出码非 0（命令**跑起来了**，只是没过） | 未通过 | 对应键 = `false` |
| 退出码 `127` / `command not found` / 脚本文件不存在 / 该项为空字符串 | **无法判定** | **省略该键，或写 `null`**——**绝不能是 `false`** |

> ⛔ **唯一的红线是不许写 `false`**：那是**会误导人的虚报**——它说的是"检查失败了"，
> 于是有人去查代码，但真正的问题是**配置过期**，代码可能完全没毛病。
>
> **省略键与 `null` 等价，两种都可以**：对消费方而言无法区分（`jq '.checks.lint_clean'`
> 在两种情况下都返回 `null`）。`null` 甚至更明确——省略是歧义的（"没看"还是"看了判不出"），
> `null` 明说"看了，判不出"。**别在这上面纠结，力气花在不写 `false` 上。**
>
> 这与「没有检查命令可跑的阶段 → `checks: {}`」同源。

## 「跑不了」＝ `test-commands.yml` 过期信号（顺带检测，零额外成本）

命令跑不起来，几乎总意味着**这份 yml 已经跟不上项目了**——脚本改名、runner 换了、
工具从依赖里移除、子项目路径调整。真实项目里这类漂移是常态（例如某前端框架升级后
移除了内置 lint 子命令，而 yml 里那条命令还在）。

由于**各阶段本来就在跑这些命令**，这个信号是白捡的。检测到时：

1. 在本阶段的报告里单列一条：**「`test-commands.yml` 疑似过期」**，写明是哪一项、
   观察到什么（退出码 / 报错原文）、以及为什么判定为"跑不了"而非"没通过"。
2. 提示补救：`/pdlc-test-setup --refresh`（重新探测并给出 diff）。
3. **不要自作主张改 yml**——本阶段的职责是干活，不是改配置；只报告，不动手。

## 变更方向决定自动化程度（`--refresh` 时适用）

更新这份 yml 等于**改变"通过"的定义**，所以按**方向**区别对待：

| 方向 | 例子 | 处理 |
|---|---|---|
| **让闸门变严** | 空着的 `e2e` 现在能跑了、覆盖率阈值上调 | **可自动应用**，报告留痕 |
| **平移替换** | 命令改名但语义相同，且新命令**已验证能跑** | **可自动应用**，报告留痕 |
| **让闸门变松** | 删掉某条 check、把命令改成空、下调阈值 | **必须人确认**，绝不自动 |

> ⚠️ 这条方向规则是防「自动修复把闸门修没了」：lint 命令坏掉时，**把它留空**是最省事的
> "修法"，结果闸门悄悄松了、报告还是绿的——比不更新更危险。
> **变严可以自动，变松必须由人签字。**
<!-- @include-end templates/prompts/check-commands.md -->
<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `review`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-ship`（写进 `next_step`，交接时提示）。
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
