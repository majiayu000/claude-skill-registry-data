---
name: pdlc-feature
description: 全自动 PDLC 新功能开发（串联 PRD→设计→TDD→实现→评审→发布）
argument-hint: <功能描述 | 已有 PRD 路径>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
layer: 1
stage: feature
produces:
  - docs/01_requirements/prd/<feature-id>-<feature-name>-prd.md
  - docs/02_design/**
  # 跟随项目既有布局，不限定固定目录
  - <实现与测试代码 · 项目既有布局>
requires: []
next_step: pdlc-ship
terminal_state: feature_done
---

# 全自动 PDLC 新功能开发

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

接收功能描述或已有需求文档，全自动走完 PDLC 所有阶段，直到产出可上线状态，中途不暂停、不询问用户。

## 输入解析（阶段一之前执行）

从本命令的参数中判断输入类型：

1. **检测是否为文件路径**：如果输入匹配以下模式之一，视为文件输入：
   - 以 `/`、`./`、`../`、`~` 开头的路径
   - 以 `.md`、`.txt`、`.docx`、`.pdf`、`.doc` 结尾
   - 包含 `docs/` 或 `requirements/` 路径片段
   - 是一个实际存在的文件路径

2. **文件输入**：读取文件内容，从中提取功能描述、用户故事、验收标准。阶段一基于文件内容结构化生成 PRD（保留原始意图，补充缺失部分），而非从零推断。在 PRD 中标注：`<!-- 来源文档: <原始文件路径> -->`

3. **文本输入**：按原有逻辑，从一句话描述自动推断

4. **已有 PRD 路径**：如果输入指向 `docs/01_requirements/prd/` 下已有的 PRD 文件，则**跳过阶段一**，直接从阶段一-B（任务拆解）或阶段二（技术设计）开始

## 执行规则

- **全程自动**：不在任何阶段暂停等待确认，遇到歧义自行做合理假设并在最终报告中说明
- **严格顺序**：必须按阶段一→二→三→四→五→六顺序执行，不得跳过
- **文档先行**：每阶段先产出文档，再进入下一阶段
- **TDD 强制**：代码实现前测试必须已存在且处于失败状态
- **自查通过才结束**：所有测试通过、评审记录完成后才输出最终报告
- **功能ID贯穿全程**：阶段一分配功能ID后，所有后续文档和产出物统一使用该ID

---

## 功能ID分配（阶段一开始前执行）

1. 获取当前日期与时分秒：`date +%Y%m%d`、`date +%H%M%S`
2. 生成功能ID：`F<YYYYMMDD>-<HHMMSS>`（示例形如 `F20260717-122801`；用执行时的真实值）
3. **本地防撞**：若该 ID 已被占用（`docs/` 或 `docs/.pdlc-state/` 下已有同名前缀），重新读取 `date +%H%M%S` 重取（生成本身有耗时、通常已跨秒；若仍同秒则 `sleep 1` 后再读一次，**不手算时分秒**，天然处理跨天边界）
4. 从用户描述中提取功能名关键词（英文小写+连字符，如 `user-auth`）

> 用时分秒而非当日序号，是为了多人 / 多 AI 并行时零协调也不撞号、合并零冲突。旧 `F<日期>-<NN>` ID 仍可解析。

### 关系建议（RFC#6）

分配 ID 后，扫描 `docs/.pdlc-state/*.json` 列出已有 feature 名，结合用户描述判断本功能与既有 feature 的关系：

- 描述含「基于 / 扩展 / 增强 X」→ 建议 `extends X`
- 描述含「需要 / 依赖 X」→ 建议 `depends_on X`
- 描述含「替代 / 重做 X」→ 建议 `supersedes X`
- 命中后填入 PRD §6.1 关系表，并在阶段四状态机的 `relations` 块写入。类型语义与方向性见本命令正文里的「Feature 关系链（6 种类型）」一节
- 无明显关系则跳过

---

## 阶段一：需求分析（PRD）

1. 根据功能描述，自动推断：功能范围、目标用户、核心用户故事（至少 3 条）、验收标准
2. 在 `docs/01_requirements/prd/` 下创建文件，命名格式：`<功能ID>-<功能名>-prd.md`
3. 使用 本 skill 目录下的 `assets/prd-template.md` 作为模板
4. **文档顶部必须包含 PDLC 追溯头**：
   ```
   <!-- PDLC-TRACE -->
   <!-- 功能ID: F20260326-090000 -->
   <!-- 功能名称: user-auth -->
   <!-- 阶段: 需求 -->
   <!-- 前置文档: 无 -->
   <!-- 创建时间: 2026-03-26T10:30:00 -->
   ```
5. 文档须包含：背景、目标、用户故事、功能清单、验收标准、非功能要求、不在范围内的事项

### 🔍 阶段一质量关卡（PRD 自审，必须执行）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

PRD 创建后、任务拆解前，立即执行自审：
- **完整性**：检查背景、目标用户、用户故事（≥3条）、功能清单（有优先级）、验收标准（可度量）、非功能需求、不在范围内 — 缺失的章节自动补充
- **一致性**：用户故事与功能清单一一对应，验收标准覆盖所有 P0 功能
- **可操作性**：验收标准无模糊表述，均可转化为测试用例 — 模糊的自动改写为量化指标
- 修复后在 PRD 末尾追加「自审记录」（含审查时间、问题数、修复明细）
- **自审通过才进入阶段一-B**

## 阶段一-B：任务拆解（紧接 PRD 之后自动执行）

1. 扫描 `docs/06_tasks/` 目录，查找是否已存在该功能的任务文件
2. **若不存在**，立即按 `pdlc-task plan` 的逻辑自动执行任务拆解：
   - 读取刚创建的 PRD，提取功能清单与验收标准
   - 为每条功能清单项生成任务条目，分配任务ID（格式：`T<功能ID的日期-时分秒>-<NN>-<type>`，前缀嵌入本功能ID的时分秒段，`NN` 为**本功能内**递增序号）
   - 创建任务文件：`docs/06_tasks/<功能ID>-<功能名>-tasks.md`
   - 格式参考 `pdlc-task plan` 的输出规范（每条任务含 ID、标题、类型、状态 `⬜`、前置依赖）
3. 在阶段报告中输出任务文件路径和任务总数

## 阶段一-C：PRD 文档评审（紧接任务拆解后自动执行）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

1. 按 `/pdlc-review` 的文档评审段落逻辑，对 PRD 执行正式文档评审（聚焦**格式规范性、模板符合度、交叉引用**）
2. 对照 本 skill 目录下的 `assets/prd-template.md` 检查格式规范性
3. 发现问题直接修复原 PRD 文档，修复后仅复查一次，不递归
4. 在 `docs/07_reviews/doc/` 下创建评审记录：`<功能ID>-<功能名>-prd-doc-review.md`
5. 评审通过后进入阶段二

---

## 阶段二：技术设计

根据 PRD 自动判断需要哪些设计文档，按需创建（不需要的跳过）：

**API 设计**（如涉及接口变更）：
- 路径：`docs/02_design/api/<功能ID>-<功能名>-api.md`
- 模板：本 skill 目录下的 `assets/api-design-template.md`
- 必须包含：接口列表、请求/响应结构、错误码

**数据库设计**（如涉及数据存储）：
- 路径：`docs/02_design/database/<功能ID>-<功能名>-db.md`
- 模板：本 skill 目录下的 `assets/db-design-template.md`
- 必须包含：ER 图、表结构、索引设计、迁移 DDL

**架构设计**（如涉及新服务或重大架构变更）：
- 路径：`docs/02_design/architecture/<功能ID>-<功能名>-arch.md`
- 模板：本 skill 目录下的 `assets/arch-design-template.md`

**所有设计文档顶部必须包含 PDLC 追溯头**：
```
<!-- PDLC-TRACE -->
<!-- 功能ID: F20260326-090000 -->
<!-- 功能名称: user-auth -->
<!-- 阶段: 设计 -->
<!-- 前置文档: docs/01_requirements/prd/F20260326-090000-user-auth-prd.md -->
```

### 🔍 阶段二质量关卡（设计文档自审，必须执行）

每份设计文档创建后立即执行自审：
- **PRD 一致性**：PRD 中每条 P0/P1 功能是否有对应设计覆盖 — 遗漏的自动补充
- **API 检查**：URL 规范、请求/响应完整、统一响应格式、分页参数、鉴权说明
- **DB 检查**：主键、索引、审计字段（created_at/updated_at）、迁移 DDL
- **跨文档一致性**：API 响应字段与 DB 字段对应，查询参数有索引支撑
- 修复后在设计文档末尾追加「自审记录」
- 在 `docs/07_reviews/doc/` 下创建设计评审记录：`<功能ID>-<功能名>-design-doc-review.md`
- 修复后仅复查一次，不递归；复查仍有问题则记录到评审报告
- **自审通过才进入阶段三**

---

## 阶段三：测试先行（TDD 红灯）

1. 在 `docs/04_testing/unit-tests/` 下创建测试计划：`<功能ID>-<功能名>-test-plan.md`
   - **文档顶部包含 PDLC 追溯头**（阶段: 测试，前置文档指向设计文档）
2. 写到项目**既有的**测试布局里（定位规则见下），不新造平行目录：

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

3. 测试必须覆盖：正常流程、边界条件、异常场景
4. 单元测试覆盖率：覆盖率达标线**以项目配置为准**：优先取 `docs/00_standards/test-commands.yml` 的 coverage 命令阈值参数（那才是强制点，退出码即判定），其次 `quality-targets.yml`；两者都没有时按 >= 80% 兜底。
5. 运行测试，**确认测试处于失败状态（红灯）**，记录失败输出
6. 同步编写 E2E 测试骨架（可暂时 skip，实现阶段补全）：
   - 路径：`docs/04_testing/e2e-tests/<功能ID>-<功能名>-e2e.md`

### 🔍 阶段三质量关卡（测试计划自审，必须执行）

测试代码编写完成、运行前执行自审：
- **验收标准覆盖度**：PRD 每条验收标准至少有一个对应测试用例 — 缺失的自动补充
- **场景完备性**：边界条件（空值/最大值/零值）、异常场景（401/403/404/409）、幂等性
- **测试质量**：方法命名是否描述场景、是否单一断言、测试数据是否有意义
- 修复后在测试计划末尾追加「自审记录」（含验收标准覆盖数、API 接口覆盖数）
- **自审通过才运行测试确认红灯**

---

## 阶段四：编码实现（绿灯）

1. 阅读 `docs/00_standards/coding/` 目录确认编码规范
2. 编写最少量的实现代码使所有单元测试通过
3. 实现过程中不偏离设计文档；若发现设计遗漏，自行补充设计文档后继续
4. 运行测试，**确认全部通过（绿灯）**
5. 在测试通过前提下，重构优化代码结构（不改变行为）
6. 补全 E2E 测试代码并运行验证

### 🔍 阶段四质量关卡（实现自检，必须执行）

代码实现完成、测试全部通过后，执行快速自检：
- **设计偏离检查**：对照设计文档，确认没有遗漏的接口或功能点
- **测试覆盖验证**：按上述口径确认覆盖率达标，不达标则补充测试
- **编码规范快检**：快速运行 lint check，有问题立即 lint fix
- 自检通过才进入阶段五正式评审

---

## 阶段五：自查评审（代码评审 + 自动修复）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

按 `/pdlc-review` 增强版逻辑执行全面评审，**发现问题直接修复**：

1. **设计一致性检查**：对照设计文档逐项确认实现完整性
   - API URL/方法/参数是否与设计一致
   - DB 表结构/字段是否与设计一致
   - 响应格式是否统一 — 不一致的直接修复代码
2. **验收标准验证**：对照 PRD 逐条确认验收标准是否满足，未满足的补充实现
3. **代码质量检查与修复**：
   - 按 `pdlc-lint check` 运行 lint 工具，存在问题则 `pdlc-lint fix` 自动修复
   - 检查命名规范 — 不规范的直接重命名
   - 检查错误处理 — 缺失的直接补充
   - 检查日志 — 关键操作缺日志的直接添加
4. **安全检查与修复**：
   - SQL 注入：字符串拼接 SQL → 自动改写为参数化查询
   - XSS：未转义输出 → 自动添加转义
   - 权限控制：缺鉴权的接口 → 标记为需人工处理
   - 敏感数据：日志中打印敏感字段 → 自动脱敏
5. **性能检查**：N+1 查询、缺失分页、缺失索引 — 能修的直接修复
6. **修复后验证**：重新运行全部测试，确认修复未引入新问题
   - 测试失败 → 回滚修复，标记为需人工处理
7. **生成评审报告**：在 `docs/07_reviews/code/` 下创建评审记录：`<功能ID>-<功能名>-review.md`
   - 包含 PDLC 追溯头（阶段: 评审，含创建时间）
   - 包含：评审总结（问题总数/自动修复数/需人工处理数）、自动修复记录表、需人工处理表、检查项结论
8. 更新对应服务的 `CHANGELOG.md`，在 `[未发布]` 下新增 feat 条目

## 阶段六：最终报告

> ⚠️ **文件落盘验证**：输出最终报告前，必须逐一确认以下文件均已作为实际文件创建到磁盘（不可仅在对话中显示）：

| 产出物 | 路径 | 验证方式 |
|--------|------|---------|
| PRD 文档 | `docs/01_requirements/prd/<功能ID>-*-prd.md` | 确认文件存在 |
| 任务清单 | `docs/06_tasks/<功能ID>-*-tasks.md` | 确认文件存在 |
| PRD 评审记录 | `docs/07_reviews/doc/<功能ID>-*-prd-doc-review.md` | 确认文件存在 |
| 设计文档 | `docs/02_design/` 下对应目录 | 确认文件存在 |
| 设计评审记录 | `docs/07_reviews/doc/<功能ID>-*-design-doc-review.md` | 确认文件存在 |
| 测试计划 | `docs/04_testing/unit-tests/<功能ID>-*-test-plan.md` | 确认文件存在 |
| 测试代码 | 对应服务测试目录 | 确认文件存在 |
| 代码评审记录 | `docs/07_reviews/code/<功能ID>-*-review.md` | 确认文件存在 |

**如有文件缺失，立即补创建，不可跳过。**

所有文件确认到位后，输出一份结构化的完成报告，格式如下：

```
## PDLC 完成报告：<功能名>（<功能ID>）

### 产出物清单
| 类型 | 文件路径 |
|------|----------|
| PRD | docs/01_requirements/prd/<功能ID>-... |
| API 设计 | docs/02_design/api/<功能ID>-... |
| 数据库设计 | docs/02_design/database/<功能ID>-... |
| 测试计划 | docs/04_testing/unit-tests/<功能ID>-... |
| 评审记录 | docs/07_reviews/code/<功能ID>-... |

### 测试结果
- 单元测试：X 个通过 / 0 个失败
- E2E 测试：X 个通过 / 0 个失败
- 覆盖率：XX%

### 任务完成情况
- 任务文件：`docs/06_tasks/<功能ID>-<功能名>-tasks.md`
- 总任务数：X  完成：X  进行中：X  未开始：X

### 验收标准确认
- [x] 验收标准 1
- [x] 验收标准 2

### 假设与决策说明
（记录执行过程中自行做出的关键假设）

### 上线前待办
（如有需要人工处理的事项，如数据库迁移、环境变量配置等）
```

---

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
- 文件名中的功能名使用英文小写+连字符，如 `user-login`
- 日期使用执行当天的实际日期，格式 YYYYMMDD
- 不引入不必要的依赖
- 不过度设计，实现够用即可

功能描述: $ARGUMENTS

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
> **本命令的状态机取值**：阶段短名 `feature`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-ship`（写进 `next_step`，交接时提示）。
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
