---
name: pdlc-prd
description: 创建 PRD 文档（自动化生成 + 自检 + handoff）
argument-hint: <功能描述 | 已有需求文档路径>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: requirements
produces:
  - docs/01_requirements/prd/<feature-id>-<feature-name>-prd.md
requires: []
next_step: pdlc-design
terminal_state: prd_done
---

# 创建 PRD 文档

根据用户提供的需求描述或已有需求文档，在 `docs/01_requirements/prd/` 目录下创建一份完整的 PRD（产品需求文档）。

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

## 段一：生成 PRD

### 1.1 输入解析（必须执行）

从本命令的参数中判断输入类型：

1. **检测是否为文件路径**：匹配以下模式之一即视为文件输入：
   - 以 `/`、`./`、`../`、`~` 开头
   - 以 `.md`、`.txt`、`.docx`、`.pdf`、`.doc` 结尾
   - 包含 `docs/` 或 `requirements/` 路径片段
   - 是一个实际存在的文件路径

2. **文件输入处理**：
   - 读取文件内容（支持 Markdown、纯文本、PDF）
   - 若为飞书文档链接，通过飞书 API 获取
   - 从内容提取：功能名称、范围、用户故事、验收标准
   - **保留原文档核心内容**，仅补充和结构化，不重写
   - 在 PRD 中添加：`<!-- 来源文档: <原始路径> -->`

3. **文本输入处理**：按描述推断功能需求

> **核心原则**：文件输入是「基于已有内容结构化」，文本输入是「从零生成」。

### 1.2 功能ID分配

<!-- @include templates/prompts/feature-id.md（已内联于下方，无需另读） -->
## 功能ID分配（必须执行）

1. 获取当前日期与时分秒：`date +%Y%m%d`（如 `20260717`）、`date +%H%M%S`（如 `122801`）
2. 生成功能ID：`F<YYYYMMDD>-<HHMMSS>`（示例形如 `F20260717-122801`；用执行时的真实日期与时分秒）
3. **本地防撞**：若该 ID 已被占用（`docs/` 或 `docs/.pdlc-state/` 下已有同名前缀），重新读取 `date +%H%M%S` 重取（生成本身有耗时、通常已跨秒；若仍同秒则 `sleep 1` 后再读一次，**不手算时分秒**，天然处理跨天边界）
4. 从用户描述中提取功能名关键词（英文小写+连字符，如 `user-auth`）

**为什么用时分秒而非序号**：多人 / 多 AI 并行开发时，各自独立取「当日序号 max+1」会分到相同编号，合并时状态机文件同名冲突、只能手工重编号。改用创建时刻的 `HHMMSS`：各副本零协调也几乎不撞（仅同一秒创建才可能），合并时文件名互异、git 自动合并。旧的 `F<日期>-<NN>`（2 位序号）ID 仍然有效、可解析。

**注意**：日期与时分秒使用执行时的实际值，**严禁**复制示例值。
<!-- @include-end templates/prompts/feature-id.md -->

### 1.3 生成 PRD 文档

1. 阅读 本 skill 目录下的 `assets/prd-template.md` 获取模板格式
2. 阅读 `docs/00_standards/coding/` 获取编码规范（若存在；**查找未命中 → 在报告里提示 `consider /pdlc-standard add coding/<topic>`**）
3. 文件名格式：`<功能ID>-<功能名>-prd.md`
4. 文档顶部加 PDLC 追溯头：

<!-- @include templates/prompts/pdlc-trace.md（已内联于下方，无需另读） -->
## PDLC 追溯头（文档顶部必须包含）

每个带编号的文档必须以下列注释开头：

```
<!-- PDLC-TRACE -->
<!-- 功能ID: <F/B 开头的 ID> -->
<!-- 功能名称: <kebab-case 名> -->
<!-- 阶段: <requirements | design | tdd | impl | review | e2e | ship | deploy | retro> -->
<!-- 前置文档: <上一阶段文档路径 | 无> -->
<!-- 创建时间: <执行时的实际 ISO 8601 时间戳> -->
<!-- 关系: <type=id; ... | 整行省略> -->
```

**严禁**把占位符（`<...>`）或示例日期原样写入实际文档。必须用真实值替换。

**关系行（RFC#6，可选）**：表达 feature 间关系链。无关系时**整行省略**（保持旧文档有效）。语法 `type=id` 对，多 id 用 `,` 分隔、多对用 `; ` 分隔，例：`<!-- 关系: extends=F20260510-100000; depends_on=F20260501-090000 -->`。6 种类型：`extends` / `depends_on` / `supersedes` / `resolves`（有向）与 `conflicts_with` / `relates_to`（对称）。
<!-- @include-end templates/prompts/pdlc-trace.md -->

5. 文档必须包含：背景与目标、目标用户、功能需求（含优先级）、非功能需求、验收标准
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
7. 用户故事使用标准格式："作为[角色]，我希望[功能]，以便[收益]"

### 1.4 关系检测（RFC#6）

从输入检测 feature 关系信号：

1. **关键词扫描**：输入含「基于 / 扩展 / 增强 / based on / extends / 依赖 / 替代 / 修复缺陷」等 → 存在关系
2. **扫描现有 feature**：读 `docs/.pdlc-state/*.json` 列已有 feature 名，判断本 PRD 是否 extends/depends_on 其一
3. **填 §6.1 关系表**：识别到的关系填入模板「6.1 关系」表（类型/目标ID/目标名/原因）。无则留空
4. 类型语义与方向性见本命令正文里的「Feature 关系链（6 种类型）」一节

> Phase 2：本步从"被动检测"升级为"主动提示用户确认关系"。

### 1.5 核心流程挂钩（若项目已启用质量闸门）

若存在 `docs/00_standards/quality-targets.yml`：本 PRD 里标为 **P0 / P1** 的流程，
逐条比对该文件的 `core_flows`，**在 handoff 里提示补齐**尚未收录的流程及其 E2E 映射。

> 为什么在这里提示：`core_flows` 清单若靠"事后有人记得改"来维护必然腐烂，
> 而腐烂的清单会让质量报告产出 **false-green**（新增核心流没进清单 → 覆盖矩阵照样全绿）。
> PRD 是这些流程的**上游真源**，在产出时就挂钩，比事后补救可靠。
> `/pdlc-quality` 每次运行还会再做一次强制对账兜底。

## 段二：自检（强制）

<!-- @include templates/prompts/self-audit.md（已内联于下方，无需另读） -->
## 段二：自检（强制）

重新阅读本次产出物，按质量关卡清单逐项检查。勾选已通过，标注未通过原因。

> **注意**：自检清单的具体内容由各命令自行定义，本片段只规定结构。

## 段三：修复（单次，不递归）

针对自检段标注为未通过的项：

- **可自动修复**：直接修复（如补缺字段、修正格式、补齐缺失段落）
- **修复后回验**：再次运行自检，确认被修复项现在通过
- **无法自动修复**：记录到自审报告，不再尝试，流程继续

⚠️ 单次修复原则：若一轮修复后仍有项未通过，**不再递归修复**，防止死循环。
<!-- @include-end templates/prompts/self-audit.md -->

### PRD 自检清单（必须全部检查）

**完整性**：
- [ ] 背景与目标：清晰说明为什么做、业务价值是什么
- [ ] 目标用户：至少一类用户角色定义明确
- [ ] 用户故事：≥ 3 条且符合标准格式
- [ ] 功能清单：每条有 P0/P1/P2 优先级标注
- [ ] 验收标准：可度量、可验证（有具体数值或明确通过/不通过条件）
- [ ] 非功能需求：至少覆盖性能、安全、可用性中的两项

**一致性**：
- [ ] PDLC 追溯头所有字段齐全且日期是今天实际日期
- [ ] 功能ID 格式正确（F<YYYYMMDD>-<HHMMSS>，兼容旧 F<日期>-<NN>）
- [ ] 文件路径符合规范

## 段三：修复（单次，不递归）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

针对自检清单中未通过项：
- 可自动修复 → 直接补齐/修正
- 修复后再读一遍确认修复项现在通过
- 无法自动修复 → 记录到自审报告，继续段四

## 段四：更新状态机 + 交接

<!-- @include templates/prompts/relations.md（已内联于下方，无需另读） -->
## Feature 关系链（6 种类型）

PDLC 用扁平 feature ID 空间。关系链在 5 个位置冗余表达，本文件是类型与语法的**单一真相源**。

### 6 种关系类型

| 类型 | 语义 | 方向性 | 示例 |
|---|---|---|---|
| `extends` | A 是 B 的增量增强 | 有向（A→B） | `user-auth-otp` extends `user-auth-phone` |
| `depends_on` | A 需要 B 存在 | 有向（A→B） | `user-profile` depends_on `user-base` |
| `supersedes` | A 替代 B（B 进入废弃/待机） | 有向（A→B） | `auth-v2` supersedes `auth-v1` |
| `resolves` | A 修复缺陷 B | 有向（A→B） | `F20260603-090000` resolves `B20260520-110000` |
| `conflicts_with` | A 与 B 互斥 | 对称 | `payment-stripe` conflicts_with `payment-paypal` |
| `relates_to` | 弱耦合，应一起考虑 | 对称 | `password-policy` relates_to `otp-policy` |

**有向 vs 对称**：
- 有向类型（extends / depends_on / supersedes / resolves）只在源 feature 的关系块里存一条出边。
- 对称类型（conflicts_with / relates_to）写入时**两端都要镜像**（A.conflicts_with 含 B 时，B.conflicts_with 也必须含 A）。

### 表达位置 1：文档追溯头（pdlc-trace）

在 PDLC-TRACE 头加一行（无关系时整行省略）：

```
<!-- 关系: extends=F20260510-100000; depends_on=F20260501-090000,F20260415-110000; resolves=B20260520-110000 -->
```

语法：`type=id` 对，多 id 用 `,` 分隔，多对用 `; ` 分隔。

### 表达位置 2：状态机关系块（state JSON）

即状态机文件里的 `relations` 块（六键对象，每键一个 ID 数组）。存**出边**；入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`。

### 表达位置 3：反向索引 `_relations.json`（自动生成）

`/pdlc-relate rebuild` 扫描所有 `<id>.json` 关系块 + 文档头，生成正向 edges + 预计算 inbound/outbound index。

### 表达位置 4：全局图 `_graph.md`（自动生成）

mermaid 可视化。边样式按类型区分：`supersedes` 虚线、`conflicts_with` 粗线、其余实线。

### 表达位置 5：PRD §6.1 关系表

见 PRD 文档的 §6.1「关系」一节。

### 校验规则（`/pdlc-relate validate`）

- 悬空引用：关系指向的 ID 不存在
- 自引用：feature 关系到自己
- 循环：`extends` / `depends_on` 链不允许成环
- 矛盾对：同一目标同时 `supersedes` + `depends_on`
- 对称一致性：`conflicts_with` / `relates_to` 两端必须互含
<!-- @include-end templates/prompts/relations.md -->

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `requirements`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-design`（写进 `next_step`，交接时提示）。
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

**本阶段状态机更新**：
- `current_stage`: `requirements` —— **仅当本阶段成功时才这样写**。`ok=false`（含 blocked）时按
  `state-update.md` 规则 5：`current_stage` **保持原值不变**、`advanced_to=null`、写 `blocked_reason`。
- 追加 history：
  ```json
  { "stage": "requirements", "done_at": "<ISO8601>", "produced": ["docs/01_requirements/prd/<...>-prd.md"], "self_audit": { "passed": <N>, "failed": <N>, "manual": <N> } }
  ```
- `next_step`: `pdlc-design`

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

**本命令的 handoff 输出：**

```
✅ PRD 已创建：docs/01_requirements/prd/<feature-id>-<feature-name>-prd.md
📊 自检：<pass>/<total> 通过
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-design <feature-id>
```

---

**目标需求**: $ARGUMENTS
