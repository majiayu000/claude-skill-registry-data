---
name: pdlc-implement
description: 按设计文档和已有测试用例实现代码（带前置守卫、自检、handoff）
argument-hint: <功能描述或功能ID>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: impl
produces:
  # 跟随项目既有源码布局，不限定固定目录
  - <实现代码 · 项目既有布局>
requires:
  # 只依赖设计文档；测试的位置由 test-location.md 的规则动态定位，不硬编码路径
  - docs/02_design/
next_step: pdlc-review
terminal_state: impl_done
recommended_model: sonnet
recommended_effort: medium
---

# 按设计文档实现代码

严格按照设计文档和已有的测试用例实现功能代码。

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

## PDLC 前置守卫（不可跳过）

1. 从用户输入提取功能名称关键词
2. 按下面的规则搜索与该功能相关的**测试代码**：

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

3. **按上述四步走完仍未找到测试代码** → 输出以下后立即中止：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的测试代码。
   实现代码前必须先编写测试（TDD）。请先运行：
   👉 /pdlc-tdd <功能描述>
   ```
4. **找到测试** → 运行测试，确认**红灯**（失败）。若已全绿：
   - 交互模式：提示"测试已全部通过，可能代码已实现，请确认是否需要继续。"
   - `--autonomous` 模式：视为流程性确认，默认**跳过实现直接收尾**（写 `auto_decisions[]` 留痕），`current_stage` 推进为 `impl`、`next_step=pdlc-review`、`last_phase_result.advanced_to=review`（下一阶段短名，非命令名）
5. 提取功能ID（从设计文档或 PRD），继续
6. **任务状态关联**（如 `docs/06_tasks/` 存在任务文件）：
   - 匹配含功能ID的任务文件
   - ⬜ 未开始 / 🔄 进行中的任务，标为 🔄，追加 `<!-- 开始时间: <今日日期> -->`

## 段一：实现代码

1. **阅读设计文档**：`docs/02_design/` 对应子目录下的文档，逐字理解
2. **阅读测试用例**：对应服务/应用下的测试代码，理解每条意图
3. **阅读编码规范**：`docs/00_standards/coding/`（未命中 → 提示 `consider /pdlc-standard add coding/<topic>`）
4. **最少量实现**：使所有测试通过的最小代码
5. **运行测试**：确认绿灯
6. **重构优化**：测试通过前提下优化代码结构
7. **更新服务 CHANGELOG**
8. **任务完结**：匹配任务由 🔄 改 ✅，追加 `<!-- 完成时间: <今日日期> -->`

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

### 实现自检清单（必须全部检查）

1. **设计偏离检查**：重读设计文档，确认没有遗漏接口或功能点
   - 遗漏 → 补充实现并确认测试通过
   - 偏离 → 修正代码或补充设计说明
2. **编码规范快检**：运行项目 lint 工具
   - 可自动修复 → 直接修复
   - 修复后重跑测试确认不破坏功能
   - lint fix 导致失败 → 回滚并记录人工处理
3. **覆盖率验证**：覆盖率达标线**以项目配置为准**：优先取 `docs/00_standards/test-commands.yml` 的 coverage 命令阈值参数（那才是强制点，退出码即判定），其次 `quality-targets.yml`；两者都没有时按 >= 80% 兜底。
   - 不达标 → 补测试用例并确认通过

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

## 段四：更新状态机 + 交接

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `impl`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-review`（写进 `next_step`，交接时提示）。
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
- `current_stage`: `impl`、`next_step`: `pdlc-review` —— **仅当本阶段成功时才这样写**
  （所有 `checks` 通过且未命中 `blocked_reason`）。
- **失败/受阻时不得推进**：`ok=false`（含 blocked）→ 按 `state-update.md` 规则 5，
  `current_stage` **保持原值不变**、`advanced_to=null`、`blocked_reason` 写明原因。
  > ⚠️ 失败也照写 `current_stage: impl` 是常见错误：那会让 `current_stage` 不再表示
  > 「最后一个真正完成的阶段」，外层循环的 stuck-stop 因此失效。
- **写 `last_phase_result`**：`checks.tests_pass` / `coverage_pass` / `lint_clean` 取自真跑 `unit` / `coverage` / `lint` 的退出码，**不得用自检结果冒充**。退出码语义与"跑不了"的处理见下（该文件不存在则回退项目既有约定，并提示 `consider 建立 docs/00_standards/test-commands.yml`）。

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
✅ 实现完成，自检通过
  - 设计一致性：<✅/部分>
  - lint 检查：<✅/X 项已自动修复/X 项待人工>
  - 测试覆盖率：<XX>%
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-review <feature-id>
```

---

**实现目标**: $ARGUMENTS
