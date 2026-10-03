---
name: ki-memory-write
description: 写入 ki-search 记忆的 SSOT：封装写 ki 的公共动作（可用性检测、scope 确定、格式硬约束、查重、降级、删除），按记忆类型分发到专题、接口、数据流、强关联、决策、错误库、待生效变更各写入策略。触发："写专题记忆"、"写 ki 记忆"、"记录决策"、"记录这个报错"、"登记/结账待生效变更"、"ki memory write"。
---

# ki 记忆写入（SSOT）

## 概述

**目的**：把"往 ki-search 写记忆"这个**公共动作**收敛为一处，消除 expert-team（专题记忆/接口信息/数据流/决策记忆）与 strong-relation（强关联）、debug / solution-capture（错误库）、code-review（待生效变更）各自重复声明的格式硬约束、ki 可用性检测、scope 确定、查重、降级策略，避免双源漂移。

**功能**：统一的 ki 写入公共动作层，按记忆类型分发到不同策略（各策略独立一个 reference），策略方只调用本 skill，不再内嵌 ki 写入细节。

**使用场景**：
- expert-team 专家/专题落盘后写"专题记忆"（模块内部知识路标）
- expert-team 识别专家模块暴露接口后写"接口信息"（按子功能聚合的可检索原子）
- expert-team 识别专家模块数据实体后写"数据流"（数据实体流向）
- expert-team 识别模块关键决策后写"决策记忆"（当初为什么这么定、砍了什么备选）
- strong-relation 识别强关联后写"强关联"（跨模块耦合）
- debug 定位成功 / solution-capture 沉淀后写"错误库"（报错原文 → 根因/解法，语义去重）
- code-review 发现本次改动会让既有知识资产失效、但变更尚未合入（PR / 需求未合并）→ 写"待生效变更"（登记待合入的资产变更，纯 KB 不向量化）
- 变更合入后按台账「合并后应为」落地正式变更（ki 记忆 / 专家资产 / wiki / 项目文档），再删除台账条目
- 任何需要往 ki 写入"路标型 / 接口型 / 数据流型 / 决策型 / 错误型 / 关联型 / 待生效变更型"记忆的场景

## 定位

```
expert-team 落盘 → 提炼专题记忆（路标）→ ki-memory-write（专题记忆策略）→ ki_bulk_sync_relation
expert-team 落盘 → 识别暴露接口 → ki-memory-write（接口信息策略）→ ki_bulk_sync_relation
expert-team 落盘 → 识别数据实体 → ki-memory-write（数据流策略）→ ki_bulk_sync_relation
expert-team 落盘 → 识别关键决策 → ki-memory-write（决策记忆策略）→ ki_bulk_sync_relation
strong-relation 识别关联 → 判定方向强度 → ki-memory-write（强关联策略）→ ki_bulk_sync_relation
debug 定位成功 / solution-capture 沉淀 → ki-memory-write（错误库策略）→ ki_bulk_sync_relation
code-review 发现资产将失效 → 登记待生效变更 → ki-memory-write（待生效变更策略，vector=false）→ ki_bulk_sync_relation
变更合入后结账 → 按「合并后应为」落地正式变更（ki 记忆 → ki_sync_relation / 专家资产·wiki·项目文档 → 改文件）→ ki_delete_relation 删台账条目
```

**七类记忆统一走 `ki_sync_relation` / `ki_bulk_sync_relation`，group 均为「父目录/{功能模块名}」结构**（父目录区分记忆类型，子目录按功能模块动态创建）：

| 记忆类型 | group | relation | tags | 向量化 |
|----------|-------|----------|------|--------|
| 专题记忆 | `专题记忆/{功能模块名}` | 根据内容进行总结 | 无 | 是 |
| 接口信息 | `接口信息/{功能模块名}` | 子功能名（同一子功能的接口集合共用一条 relation） | `api` | 是 |
| 数据流 | `数据流/{功能模块名}` | 数据实体名（表/消息主题/缓存 key/数据结构） | `data` | 是 |
| 决策记忆 | `决策记录/{功能模块名}` | 决策主题（不含特殊字符） | `decision` | 是 |
| 错误库 | `错误库/{功能模块名}` | 错误特征（短短语，非报错原文） | `error` | 是 |
| 强关联 | `关联关系/{功能模块名}` | `{模块A}-{模块B}` | `relation` | 是 |
| 待生效变更 | `待生效变更/{功能模块名}` | `{变更主题}` | `pending` | **否**（`vector=false`） |

> **group 子目录七类统一按功能模块名**，技术栈/工具名写进正文与 keywords，不占 group 位；错误库中无明确归属模块的（Docker / Nginx / 工具链 / 语言级问题）归 `错误库/通用`；待生效变更中无明确归属模块的归 `待生效变更/通用`。
>
> **禁用 `ki_store` / `ki_bulk_store`**：二者只写向量层、不写本地 KB，会产出孤儿向量。写知识一律走 `ki_sync_relation` / `ki_bulk_sync_relation`（双写 KB + 向量）。
>
> **待生效变更的纯 KB 写入同样走这两个 API**，只需带 `vector=false`——**不需要改用 `ki_store`**。`vector` 是 `sync_relation` 系列的参数，控制的是"是否生成向量"，**KB 照常写入**，与 `ki_store` 的"只写向量不写 KB"是两回事。

- **输入**：记忆类型（专题记忆 / 接口信息 / 数据流 / 决策记忆 / 错误库 / 强关联 / 待生效变更）+ 已提炼/识别好的记忆内容
- **输出**：写入 ki-search 的记忆原子
- **边界**：本 skill **只负责"写 ki / 删 ki"这两个动作**（检测 → scope → 查重 → 格式约束 → 写入 → 删除），**不负责**内容的提炼/识别——专题记忆的"提炼路标"、接口信息的"识别暴露接口"、数据流的"识别数据实体"、决策记忆的"识别关键决策"是 expert-team 的事，强关联的"识别关联 + 判定方向"是 strong-relation 的事，错误库的"定位根因 + 给解法"是 debug / solution-capture 的事，待生效变更的"判断哪些资产会失效 + 写出合并后应改成什么"是 code-review 的事。策略内容（字段模板、分组/tags 约定）在各自 reference 中定义。

## 核心原则

1. **只写动作，不做认知**：本 skill 收敛"写 ki"的公共动作，不承担记忆内容的提炼/识别/判定——那是调用方（expert-team / strong-relation / debug / solution-capture / code-review）的职责
2. **格式硬约束 SSOT**：ki 记忆的格式硬约束（禁用 yaml、标题、表格）**只在本 skill 定义一次**，调用方不再各自声明
3. **策略分 reference**：专题记忆、接口信息、数据流、决策记忆、错误库、强关联、待生效变更的字段模板 / 分组 / tags / API 差异，分别在 `reference-topic-memory.md`、`reference-api.md`、`reference-data-flow.md`、`reference-decision.md`、`reference-error.md`、`reference-strong-relation.md`、`reference-pending-change.md` 中定义，SKILL.md 只放公共动作
4. **查重前置**：写入前一律先查同 group 是否已有同 relation 条目，命中则**更新**而非新建——重复条目堆积是知识库退化的头号路径（判定细则见 Step 3.6，错误库另有专门的判定表）
5. **降级不阻塞**：ki 不可用时跳过写入并告知调用方（对话内输出记忆内容清单），不阻塞调用方主流程
6. **scope 一致**：写入所用 scope = 项目标识，与各策略既有一致
7. **删除仅限结账**：`ki_delete_relation` 只用于待生效变更的结账清理（详见 Step 5），其余六类**不删除**——知识资产的演进靠覆盖更新，删除会丢失历史

## 执行流程

### Step 0：环境检测

1. 确认 ki 可用（`ki_bulk_sync_relation` / `ki_manage_index_list` 可调用）
2. **ki 不可用** → 告知调用方，将记忆内容以对话内清单输出，**不阻塞**调用方主流程，本流程终止

### Step 1：确定记忆类型与策略

根据调用方传入的记忆类型，选择对应 reference 策略：

| 记忆类型 | 调用方 | 策略 reference | 写入 API |
|----------|--------|---------------|----------|
| 专题记忆 | expert-team（Step 8） | [reference-topic-memory.md](reference-topic-memory.md) | `ki_bulk_sync_relation` |
| 接口信息 | expert-team（Step 8.3） | [reference-api.md](reference-api.md) | `ki_bulk_sync_relation` |
| 数据流 | expert-team（Step 8.4） | [reference-data-flow.md](reference-data-flow.md) | `ki_bulk_sync_relation` |
| 决策记忆 | expert-team（Step 8.6） | [reference-decision.md](reference-decision.md) | `ki_bulk_sync_relation` |
| 错误库 | debug（Step 5.5）/ solution-capture（Step 7.5） | [reference-error.md](reference-error.md) | `ki_bulk_sync_relation` |
| 强关联 | strong-relation（Step 4） | [reference-strong-relation.md](reference-strong-relation.md) | `ki_bulk_sync_relation` |
| 待生效变更 | code-review（阶段 2.3） | [reference-pending-change.md](reference-pending-change.md) | `ki_bulk_sync_relation`（`vector=false`） |

### Step 2：按策略写入

加载对应策略 reference，按其字段模板 + 分组/tags/API 约定执行写入。

### Step 3：格式硬约束校验（写入前必做）

写入前校验记忆内容**不含**以下项（违反即先修正再写入）：

- yaml 元数据（`---` frontmatter）
- `##` / `###` 等 markdown 标题
- `|` 表格分隔符等 markdown 结构语法

统一为**纯文本描述 + `-` 列表**，保证 ki-search 向量化时语义纯净、检索准确。

> **为什么**：yaml 元数据和 md 标题会污染向量化，降低 ki-search 检索效率。

### Step 3.5：写入 API 硬约束（写入前必做）

- **禁用 `ki_store` / `ki_bulk_store`**——二者只写向量层、不写本地 KB，会产出孤儿向量；写知识一律走 `ki_sync_relation` / `ki_bulk_sync_relation`（双写 KB + 向量）
- **`vector` 参数**（`ki_sync_relation` / `ki_bulk_sync_relation` 通用）：
  - 默认 `true`（写入 KB + 生成向量），六类常规记忆保持默认
  - `vector=false` → **只写 KB、不生成向量**（纯 KB 模式）。**仅待生效变更使用**——台账是待办清单不是知识，进向量会污染语义检索（用户问"这个报错怎么解"却召回一条待办，是纯噪声）
  - ⚠️ `vector=false` **不等于不入库**：KB 照常写入，仍可用 `ki_query_group` 直查
- **建议带 `keywords`**（3-5 个）：必须是**自然语言词汇**（禁代码符号），且必须真实出现在 `module_info` 原文中。语义召回型记忆（决策记忆 / 错误库 / 专题记忆）收益最明显；**`vector=false` 的待生效变更无需 keywords**（不参与语义检索）

### Step 3.6：查重前置（写入前必做，七类通用）

写入前先查目标 group 下是否已存在同 relation 条目，**命中则更新，不新建**——重复条目堆积会让知识库越用越不敢信。

| 步骤 | 动作 |
|------|------|
| 1 | `ki_query_group(groups="{类型}/{模块名}", mode="full")` 列出该 group 全部条目 |
| 2 | 比对 relation 名：已存在 → **更新**（补充/修正内容）；不存在 → 新建 |

> ⚠️ **`mode="full"` 必带**：默认 `mode="hot"` 只返回最热 5 条，且 `auto_fallback` 静默兜底不报错——漏掉的恰恰是最该查重的冷条目。
>
> **批量写入时整个 group 只查一次**：`ki_bulk_sync_relation` 一次写 N 条时，先对该 group 执行一次 `ki_query_group(mode="full")` 拿到全部既有 relation 清单，再在清单内逐条比对——**不要每条写入各查一次**（N 次查询无收益，且 expert-team 建专家时单批可达数十条）。

**错误库额外适用专门的判定表**（它的 relation 是"错误特征"，不天然唯一，同一报错换个路径就是"新错误"），见 [reference-error.md](reference-error.md)「查重前置」节——包括"判定存疑按同一条处理"的从严规则。

**待生效变更的查重**：同一 PR / 需求对同一资产的变更只登记一条，重复触发时更新「合并后应为」而非新增条目。

### Step 4：刷新缓存与校验落盘

写入后执行两步：

1. **刷新缓存**（必须）：`ki_query_group`（`mode="full"`）——ki 写入后需刷新索引缓存，否则低频写入的记忆（决策记忆、错误库）可能检索不到
2. **校验归档**：用 `ki_query_group`（group = 对应根分组，如 `专题记忆` / `接口信息` / `数据流` / `决策记录` / `错误库` / `关联关系/{功能模块名}` / `待生效变更`）确认记忆原子已归入正确分组，抽查 1-2 条确认已可检索，失败则修正后重写

> **`vector=false` 的待生效变更**：第 1 步刷新照做（刷的是 KB 索引缓存），第 2 步校验用 `ki_query_group` 直查确认，**不可用 `ki_search` 校验**——它不进向量，`ki_search` 必然查不到，查不到不等于写入失败。

### Step 5：删除（仅待生效变更结账用）

**触发条件**：待生效变更条目对应的变更已合入，且正式变更已按「合并后应为」落地完成。

**API**：`ki_delete_relation`——**双侧删除**（KB + 向量）且 **wiki 同步删除**（指 ki 导出的 wiki 中该台账条目本身，**不删**「影响资产」指向的项目 wiki 文件——那是项目里的独立文件）。

**执行顺序**（顺序不能颠倒）：

1. 按台账条目的「合并后应为」落地正式变更——**按资产类型分叉**：ki 记忆走本流程 Step 1~4（group 为**目标资产**的真实 group，如 `错误库/{模块}`）；专家资产 / wiki / 项目文档则按「影响资产」坐标**直接修改对应文件**，不走 ki 写入
2. 确认变更已落盘（记忆可检索 / 文件已保存）
3. `ki_delete_relation` 删除台账条目（`待生效变更/{模块}` 下的对应 relation）
4. 同步删除 `AGENTS.md` 中的指针行

> **为什么先写后删**：反序会在"正式记忆写入失败、台账已删"时丢失这条待办。先写后删保证任何中断点都能从台账重新恢复。
>
> **其余六类不执行本 Step**：知识资产演进靠覆盖更新，删除会丢失历史。

## 更多资源

- 专题记忆策略（8 字段路标模板 + 维护规则），参见 [reference-topic-memory.md](reference-topic-memory.md)
- 接口信息策略（子功能聚合模板 + tag=`api`），参见 [reference-api.md](reference-api.md)
- 数据流策略（数据实体流向模板 + tag=`data`），参见 [reference-data-flow.md](reference-data-flow.md)
- 决策记忆策略（决策/被否决方案/触发条件/证据门 + tag=`decision`），参见 [reference-decision.md](reference-decision.md)
- 错误库策略（报错原文→根因/解法 + 查重判定表 + 非平凡门槛 + tag=`error`），参见 [reference-error.md](reference-error.md)
- 强关联策略（三元组/双向影响线模板 + 分组/tags 约定），参见 [reference-strong-relation.md](reference-strong-relation.md)
- 待生效变更策略（知识资产待合入变更台账 + `vector=false` + 结账删除 + tag=`pending`），参见 [reference-pending-change.md](reference-pending-change.md)
- 记忆的**查询**（SSOT），调用 `use_skill("ki-memory-lookup")`
