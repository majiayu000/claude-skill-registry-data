---
name: planners-proposal
description: 消化 Brief 与多源调研材料，与人多轮探讨策略判断，形成可校验、可在实时文字工作台持续修改与拖拽排序的 Storyline（storyline.md），并轻量登记主要来源与盲区，确认后交给 planners-bypage 展开逐页正文。
---

# Planners Proposal

> 由阿祖不看 TVC 创建与维护。个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。来源信息不默认写入客户交付物。

## 目标（OKR）

**不抢先代写长篇正文或画 PPT，而是通过多轮高质量讨论与实时工作台共创，把零散资料收敛为一套逻辑推进成立、每页一句完整主张、主要判断均标明出处的 `storyline.md`。**

- **产物目录（`<Project>/.planners/`）**：
  - `storyline.md`：按 `planners-doc/2` 写的唯一主线工作稿（`#` 章节、`##` 页、首段 `主张：` + 支撑要点 + 末尾 `>` 轻量出处）。
  - `project-memory.md`：已确认判断、取舍边界、采用的 Method Wiki 方法 `lens_id`。
  - `source-index.json`：遵循 `source-index/2.1.0` 的轻量台账（记路径、覆盖状态、未读盲区 `blind_spots` 与来源可信度 `provenance: primary|secondary|derived|unverified`）；Proposal 阶段**不必逐份抽取耗时的细粒度 `audit_companion`**（留待 Bypage 全面核查前补全）。
- **核心协作分工**：
  - 深入研讨卡点 → 调用 `sparkling`（不凑轮次，方向已明且依据在场时直接推进）。
  - 寻找专业分析角度 → 查 `planners-method-wiki`（读 `<Wiki>/index.md` / 运行 `query-wiki.mjs` / 读 `lenses/<id>.md` Markdown 真源）。
  - 塑造递进张力与章节推进 → 调用 `storytelling`（高管决策汇报保留结论先行，不用悬念藏建议）。
  - 锤炼每页 `主张：` 与标题链 → 调用 `slide-copy`。
  - 涉及核心数据口径调整或结论变更时 → 按需调用 `planners-fact-check` 局部核对（完整终稿核查由 Bypage 负责）。

## 工具

`<P>` 为本 Skill 根目录，`<K>` 为 `planners-review-core` 根目录，`<D>` 为 `<Project>/.planners/storyline.md`。

| 动作 | 命令 |
|---|---|
| 校验 Storyline 结构与「一页一主张+支撑」 | `node "<P>/scripts/validate-storyline-doc.mjs" "<D>"` |
| DSH 侧栏：生成 surface 后调 `review_open` 打开工作台 | `node "<K>/scripts/doc-surface.mjs" "<D>"` |
| DSH 侧栏：模型读取任务 / 加锁 / 回写 patch / 完成 / 看冲突 | `node "<K>/scripts/doc-command.mjs" "<Project>/.planners/.doc-workbench/review-surface.json" <tasks\|claim\|patch\|complete\|conflicts>` |
| 本地独立宿主：启动并打开文字工作台 | `node "<K>/scripts/doc-workbench.mjs" "<D>" --open` |
| 本地独立宿主：查看/接手批注收件箱 | `node "<K>/scripts/doc-inbox.mjs" <list\|take> "<D>"` |

详细契约与块级回写规则见 [工作台操作](references/workbench.md) 与 [职责与接口](references/architecture.md)。

## 剧本（Playbook）

1. **读懂资料与轻量建账**：读完项目 Brief 与核心研究材料后，生成或更新 `.planners/source-index.json`（`source-index/2.1.0`），标注每个核心来源的 `provenance`（原始一手 `primary` / 转述二手 `secondary` / 模型推演 `derived` / 未核实 `unverified`）和未读盲区，先向用户对齐事实边界再给策略判断。
2. **高摩擦讨论与方法启发**：当存在多个竞争方向或认知卡点时，用 `sparkling` 和 `planners-method-wiki` 拆解问题；若方向与事实已明确，不为了走形式强行发散，直接巩固证明链。把确认的边界、取舍和采用的 `lens_id` 记入 `.planners/project-memory.md`。
3. **撰写与校验 `storyline.md`**：参照 [`templates/storyline.md`](templates/storyline.md) 与 [`contracts/storyline.md`](contracts/storyline.md)，运用 `storytelling` 组织章节推进、用 `slide-copy` 锤炼每页 `主张：` 与支撑，每页末尾用 `>` 引用块注明主要观点来自哪些来源（如 `> 消费者访谈汇总 §3 / source-index: src-interview-01`）。生成后立即运行 `validate-storyline-doc.mjs`。
4. **交付实时工作台多轮打磨**：
   - 先通过校验再打开工作台；工作台内支持直接改字、回车拆块、拖曳调序、自动保存（无手动保存按钮）和历史版本恢复。
   - 接到批注任务时：先看 `task.diff`（若用户在工作台里手动新增、删减或重排了页/章节，`task.diff` 会明确列出结构变动），再按块指纹加锁并仅提交局部 `patch`，不重写整份文档。遇到 `deferred_blocks` / 待核对冲突时交由用户在工作台选定，不擅自覆盖用户手稿。
   - **区分自动保存与继续下游**：工作台自动保存不代表用户批准交接。只有当用户明确确认主线定稿，或请求交给 Bypage 展开逐页内容时，才整理交接。
5. **交接下游**：把 `<Project>/.planners/` 下的 `storyline.md`、`project-memory.md`、`source-index.json` 原样交给 `planners-bypage`，不代写逐页完整可见正文或 `by-page.md`。

## 兼容与边界

- **旧主稿兼容**：旧 `.proposal-work/page-architecture.json` 不再作为新项目入口；旧项目文件在工作台以**只读**方式打开。
- **不造新解析器**：任何文档结构、工作台与块级反馈都复用 `planners-review-core`（`planners-doc/2`），本 Skill 只扩展 `validate-storyline-doc.mjs` 的提案规则。
