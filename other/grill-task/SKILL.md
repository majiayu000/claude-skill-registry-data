---
name: grill-task
description: 需求澄清 + 字段对齐分析 — 反复提问拉齐用户意图,生成 TASK_CONFIRM 任务确认书与字段对齐分析报告。启动新需求、或需要与现有数据库表对齐字段名时调用本 skill。
disable-model-invocation: true
version: 4.0.0
requires: [context-pointer, no-field-guessing, no-self-invent, stage-gate]

---

# Grill-Task — 需求澄清 + 字段对齐

## Contract

- 输入: `TASK_CONFIRM_*.md`、`paths/knowledge-path.md`、用户需求笔记
- 输出: `REVIEW_需求确认书.md`、`REVIEW_字段对齐分析.md`
- 门控: `python3 scripts/task-confirm-check.py --strict TASK_CONFIRM_*.md REVIEW_需求确认书.md REVIEW_字段对齐分析.md` 通过;用户白名单话术签字
- Required rules: `stage-gate`, `no-field-guessing`, `context-pointer`, `goal-boundary`
- Required paths: `knowledge-path`, `doc-naming-path`
- 下一步: `/to-brd`

## 适用场景

- 用户提出新需求时
- 需求涉及现有表查询/维护类功能
- 团队对需求理解不一致时

## 流程步骤

### 1. 生成《需求确认表》

- 加载 `templates/TASK_CONFIRM.md`
- 替换项目名、日期,生成 `TASK_CONFIRM_{项目名}.md` 到工作目录
- 告知用户填写并保存

### 2. 用户填写后,生成《需求确认书》

- 读取用户填写的 `TASK_CONFIRM_*.md`
- 加载 `templates/REVIEW_需求确认书.md`
- 逐项标注 AI 助手的理解,列出待确认的设计假设
- 输出 `REVIEW_需求确认书.md`

### 3. 字段对齐分析(涉及现有表时强制)

- 提取需求中提到的所有表名和字段名
- 与 `knowledge-path.md` 引用的知识库核对
- 输出 `REVIEW_字段对齐分析.md`,分类标注:
  - ✅ 已对齐
  - ⚠️ 需 JOIN
  - ❓ 待确认(业务同义不同名)
  - 🔴 缺失

### 4. 阶段 2 出口门控(唯一脚本)

- 跑 `python3 scripts/task-confirm-check.py --strict TASK_CONFIRM_*.md REVIEW_需求确认书.md REVIEW_字段对齐分析.md`
- `task-confirm-check.py` 是阶段 2 唯一门控脚本
- `field-alignment-check.py` 不接 TASK_CONFIRM / REVIEW 文档,不得用于阶段 2 出口门控

## 关键纪律

- 用户填写完 TASK_CONFIRM 后,**严禁直接跳进设计**
- 必须先出确认书让用户审阅
- 用户确认通过 → 进入 `/to-brd`
- 字段对齐有 🔴 或 ❓ → `task-confirm-check.py --strict` 必须失败,严禁进入下一步

## 调用的 rule

- `rules/no-field-guessing` — 严禁猜测字段名
- `rules/no-self-invent` — 严禁自创字段
- `rules/context-pointer` — 三层知识库加载

## 关键纪律（2026-06-24 更新）

- ❌ 删除"4 章节"表述——实际为 5 章节（一~五）
- 阶段 2 只允许 `scripts/task-confirm-check.py` 作为出口门控脚本
- `field-alignment-check.py` 只校验 PRD/FSD/设计文档字段引用,不接 TASK_CONFIRM / REVIEW
- 🟡 删除：状态字段不再有 🟡 中间态，仅 ⬜/✅ 二态
- 🔒 HARD GATE：用户必须用白名单话术之一明确签字，LLM 不接受隐式同意

## 结束条件

- [ ] TASK_CONFIRM 状态字段 = ✅ 已确认（二态，无 🟡）
- [ ] TASK_CONFIRM 5 个必备章节（一~五）填完
- [ ] TASK_CONFIRM 无 12 词 TBD（见 `scripts/task-confirm-check.py` TBD_KEYWORDS）
- [ ] REVIEW_需求确认书 第八节"待明确事项"为空
- [ ] REVIEW_字段对齐分析 对齐结论表中 ❓=0 且 🔴=0（⚠️ 可保留，状态字段可为 ✅ 或 ⚠️）
- [ ] `python3 scripts/task-confirm-check.py --strict TASK_CONFIRM_*.md REVIEW_需求确认书.md REVIEW_字段对齐分析.md` exit 0
- [ ] 用户白名单话术签字（详见 `templates/TASK_CONFIRM.md` L48-55）

## 反模式

- ❌ TASK_CONFIRM 留 TBD 直接进 BRD — TBD 必须先闭环（确认/补资料/豁免）才能签字
- ❌ 把 `field-alignment-check.py` 当 2→3 门控 — 应是 `task-confirm-check.py`(同时校验 3 份产物)
- ❌ 接受 "OK/好/继续" 作为签字 — 必须 4 句白名单之一(我已全部确认,可以进入下一步 / 确认通过 / 全部完成,继续 / approved, proceed to next stage)
- ❌ 中间态(🟡)混入二态 — ⬜/✅ 二态,无 🟡;若需"进行中"用 ⬜(未完成)表达
- ❌ 一轮提问就停下 — 必须反复澄清到 5 节全填,无 TBD 才出"需求确认书"
- ❌ 字段对齐直接写"✅ 正确" — 必须给证据:字段路径 + 知识库章节 + 引用 URL
