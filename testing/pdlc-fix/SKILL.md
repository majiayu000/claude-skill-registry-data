---
name: pdlc-fix
description: 全自动 Bug 修复（定位→复现→修复→测试→文档）
argument-hint: <Bug 描述>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 1
stage: fix
produces:
  - docs/04_testing/defects/<defect-id>-defect.md
requires: []
next_step: pdlc-review
terminal_state: fix_done
---

# 全自动 Bug 修复

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

接收一句话 Bug 描述，全自动完成定位、复现、修复、测试、文档更新，中途不暂停、不询问用户。

## 执行规则

- **全程自动**：不在任何步骤暂停等待确认，遇到歧义自行做合理假设并在最终报告中说明
- **严格顺序**：必须按阶段一→二→三→四→五顺序执行，不得跳过
- **最小改动原则**：只修复 Bug 本身，不顺手重构或优化不相关代码
- **测试验证才结束**：全量测试通过后才输出最终报告

---

<!-- @include templates/prompts/defect-id.md（已内联于下方，无需另读） -->
## 缺陷ID分配（必须执行）

1. 获取当前日期与时分秒：`date +%Y%m%d`、`date +%H%M%S`
2. 生成缺陷ID：`B<YYYYMMDD>-<HHMMSS>`（示例形如 `B20260717-122801`；用执行时的真实日期与时分秒）
3. **本地防撞**：若该 ID 已被占用（`docs/` 或 `docs/.pdlc-state/` 下已有同名前缀），重新读取 `date +%H%M%S` 重取（生成本身有耗时、通常已跨秒；若仍同秒则 `sleep 1` 后再读一次，**不手算时分秒**，天然处理跨天边界）
4. 从 Bug 描述中提取功能名关键词（英文小写+连字符）

**为什么用时分秒而非序号**：多人 / 多 AI 并行时各自独立取「当日序号 max+1」会分到相同编号、合并冲突。改用创建时刻 `HHMMSS` 后各副本零协调也几乎不撞（仅同一秒才可能），文件名互异、git 自动合并。旧的 `B<日期>-<NN>` ID 仍有效、可解析。

**注意**：日期与时分秒使用执行时的实际值。
<!-- @include-end templates/prompts/defect-id.md -->

---

## 阶段一：问题定位

1. 根据 Bug 描述，搜索相关代码文件，阅读并理解涉及的逻辑
2. 查阅 `docs/02_design/` 对应子目录下的设计文档，确认**预期正确行为**
3. 明确根因：
   - 是代码逻辑错误、边界未处理、还是设计文档遗漏？
   - 影响范围：哪些模块/接口/数据受影响？
4. 若 Bug 描述不足以定位，根据描述做最合理推断，在报告中说明

## 阶段二：回归测试（红灯）

1. 编写一个**能精确复现该 Bug 的测试用例**，写到项目既有的测试布局里（定位规则见下）：

<!-- @include templates/prompts/test-location.md（已内联于下方，无需另读） -->
## 测试代码在哪（布局无关的定位规则）

> ⚠️ **这条规则的要害**：红灯守卫必须区分「**项目没有测试**」和「**测试不在我预期的位置**」。
> 前者才该拦；后者拦了就是误伤——真实项目的测试布局千差万别（单体 `backend/tests/`、
> 根级 `tests/`、Go 同包 `*_test.go`、Node 与源码同目录的 `*.test.tsx`…），
> 按一份写死的路径清单去找、找不到就拦，会让 pdlc 在大量正常项目上直接卡死。

**核心原则：优先问 runner，其次翻文件。** 测试框架自己最清楚有哪些测试——
让它报比我们去猜文件位置准得多，也和 pdlc「信退出码、不信目视检查」的哲学一致。
尤其**测试写在源文件里**的语言（见下），翻文件根本找不到。

按下列顺序定位，**命中即停**：

### 1. 项目自己的声明 + 向 runner 查询（最高优先级）

若存在 `docs/00_standards/test-commands.yml`，它的 `unit` / `e2e` 命令**就是权威**——
项目已经明确告诉你测试怎么跑。**用它去问 runner**，而不是去翻目录：

| runner | 列出全部测试 | 只查某功能相关 |
|---|---|---|
| cargo (Rust) | `cargo test -- --list` | `cargo test <关键词> -- --list` |
| pytest | `pytest --collect-only -q` | `pytest --collect-only -q -k <关键词>` |
| go test | `go test -list '.*' ./...` | `go test -list '<关键词>' ./...` |
| vitest / jest | `npx vitest list` / `--listTests` | `npx vitest list -t <关键词>` |
| gradle / maven | `--tests '*'` 干跑 | `--tests '*<关键词>*'` |

**查询结果为空 = 该功能没有测试**（这是行为证据，比"我没找到文件"可靠得多）。

### 2. 测试写在源文件里的语言（**必须靠内容匹配，文件名扫描无效**）⭐

这类语言没有独立测试文件，只能按**代码内标记**搜：

| 语言 / 框架 | in-source 测试标记 |
|---|---|
| **Rust** | `#[cfg(test)]`、`#[test]`、`mod tests` |
| **Vitest**（in-source testing） | `import.meta.vitest` |
| **Python** doctest | docstring 里的 `>>> ` |
| **Elixir** doctest | `@doc` 里的 `iex>` |
| **Go**（同包但独立文件） | `*_test.go` + `func Test` |

> ⚠️ **Rust 尤其要注意**：单元测试几乎总在源文件的 `#[cfg(test)] mod tests` 里，
> `tests/` 目录按 Cargo 约定只放**集成测试**。所以「`tests/` 目录不存在」在 Rust 项目里
> **完全不能推出「没有单元测试」**——照文件清单判红会稳定误伤所有 Rust 项目。

### 3. 常见布局约定（按项目实际技术栈挑，不要全试）

| 生态 | 常见测试位置 |
|---|---|
| Python | `tests/`、`backend/tests/`、`test/`、与源码同目录的 `test_*.py` |
| Node / TS | `tests/`、`__tests__/`、`src/**/__tests__/`、与源码同目录的 `*.test.ts(x)` / `*.spec.ts(x)` |
| Rust | 源文件内 `#[cfg(test)]`（单测）+ `tests/`（集成测试） |
| Go | 与源码同包的 `*_test.go` |
| JVM | `src/test/java/`、`src/test/kotlin/` |
| Ruby | `spec/`、`test/` |
| 微服务 / 单体仓 | 上述任一可能出现在 `backend/`、`backend/services/<名>/`、`frontend/<应用>/` 之下 |

### 4. 文件名兜底扫描

前三步都没命中时，按文件名模式全仓搜（`*test*` / `*spec*`，排除 `node_modules`、
`.venv`、`vendor`、`dist`、`build`、`target`、`.git`），再按功能关键词筛。

### 5. 判定

- **任一步找到相关测试** → 通过，进入下一步（`pdlc-implement` 还需确认红灯）
- **四步走完确实找不到任何测试** → 这才是真红灯，按各命令的守卫规则中止
- **找到测试但与本功能无关** → 按「本功能无测试」处理（同样是真红灯），但报告里要说明
  「项目有测试，只是没覆盖本功能」，别让用户以为项目裸奔
- **无法判定**（如 runner 装不上、语言不认识）→ **不要默认放行，也不要假装找到了**：
  如实报「无法确认本功能是否有测试」并交还人类。**「我判断不了」绝不等于「没问题」。**

> 写测试时（`pdlc-tdd`）同样按本规则决定**写到哪**：跟随项目既有布局与惯例——
> Rust 单测就写进源文件的 `#[cfg(test)] mod tests`，**不要**为了迎合某种预设结构
> 新造一套平行的测试目录。
<!-- @include-end templates/prompts/test-location.md -->

2. 测试命名格式：`应该_当<触发条件>时_<预期行为>`
3. 运行该测试，**确认测试失败（红灯）**，记录失败输出
4. 若已有相关测试但未覆盖该场景，在原测试文件中追加用例

## 阶段三：代码修复（绿灯）

1. 用**最小改动**修复 Bug，不改动与 Bug 无关的代码
2. 运行步骤二编写的回归测试，**确认通过（绿灯）**
3. 若修复过程中发现设计文档有遗漏或错误，同步更新对应设计文档

## 阶段四：全量测试验证

1. 运行该服务/应用的**完整测试套件**，确认没有引入新的失败
2. 若有 E2E 测试，运行相关 E2E 用例验证端到端行为正常
3. 如有测试因本次修复而需要更新（如快照测试、预期值变更），同步更新

## 阶段五：文档更新与最终报告

> ⚠️ **必须创建文件，不可仅在对话中输出。** 以下每份文档都必须作为实际文件写入磁盘。

1. 更新对应服务的 `CHANGELOG.md`，在 `[未发布]` 下新增 fix 条目：
   - 格式：`- 修复 <简要描述>（<触发条件>）`
2. 若涉及设计文档变更，同步更新 `docs/02_design/` 下对应文档
3. **【必须创建文件】** 在 `docs/04_testing/defects/` 下创建缺陷记录：`<缺陷ID>-<功能名>-defect.md`
   - **文档顶部必须包含 PDLC 追溯头**（格式见下方片段）：

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

   - 记录：根因分析、影响范围、修复方案、回归测试覆盖情况
   - **创建后验证**：确认文件已存在于 `docs/04_testing/defects/` 目录
4. 输出最终报告（同时在对话中显示，**但报告内容必须已落盘到上述文件中**）：

```
## Bug 修复报告：<简要描述>（<缺陷ID>）

### 根因分析
<一段话描述根本原因>

### 影响范围
- 涉及文件：
- 涉及接口/功能：

### 修复方案
<描述做了什么改动，为什么这样改>

### 测试结果
- 回归测试：通过
- 全量测试：X 个通过 / 0 个失败

### 文档变更
- CHANGELOG.md：已更新
- 设计文档：已更新 / 无需更新

### 假设与说明
（记录执行过程中自行做出的关键假设）

### 上线前待办
（如有需要人工处理的事项，如数据修复脚本、缓存清理等）
```

---

## 产出物清单（每项必须作为文件创建）

| 产出物 | 路径 | 必须 |
|--------|------|------|
| 缺陷记录 | `docs/04_testing/defects/<缺陷ID>-<功能名>-defect.md` | ✅ 必须 |
| 回归测试 | 对应服务测试目录 | ✅ 必须 |
| CHANGELOG | 对应服务 `CHANGELOG.md` | ✅ 必须 |
| 设计文档更新 | `docs/02_design/` 下对应文档 | 按需 |

> **文件落盘规则**：所有带编号（缺陷ID）的文档必须作为实际文件写入，不可仅在对话中显示。最终报告完成前，必须确认上述文件均已创建。

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
- 只修复 Bug，不做额外优化或重构
- 回归测试用例必须保留在代码库中，不得删除
- 日期使用执行当天实际日期，格式 YYYYMMDD

Bug 描述: $ARGUMENTS

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `fix`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-review`（写进 `next_step`，交接时提示）。
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
