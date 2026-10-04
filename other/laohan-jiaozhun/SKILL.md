---
name: laohan-jiaozhun
version: "2.1.0"
description: 内容校准工作流适配器。为 episode 选择正确的 cheat-on-content 校准 lane，保存可追溯的校准入口；评分、盲预测、发布登记、复盘和 rubric 更新一律由上游 cheat-on-content 执行。Use when 用户说校准这期、给本期打分并预测、把 episode 接入 cheat、选择校准轨道、进入④校准。
---

# 内容校准适配器

## 合同地位（2026-09-20治理裁定）

本skill是**校准适配器辅助工具**，未登记executor-registry——④节点合同入口是上游`cheat-on-content`（registry node 4），⑤深扫合同入口是`dbs-content-review`+`laohan-shencha-content-claims`（node 5）。宿主按registry/whois执行④⑤，不因本skill目录可见而路由到它；本skill的lane路由、防污染与登记流程作为操作手册参考。

这里不是第二套 Cheat。`cheat-on-content` 是唯一校准引擎；本 skill 只把 episode 和它的校准 lane 接起来，避免本地 fork 公式、预测规则或迁移规则漂移。

## 不可跨越的边界

- 禁止在这里按固定教程型权重打分，禁止估算后把分数当预测，禁止另写 PREDICT / RETRO / BUMP。
- 禁止把 `tutorial-video` 的历史样本拿来评估 `opinion-video`；两种内容必须是独立 lane。
- 盲预测必须在拍摄、发布、查看本期实际数据之前，由上游 `cheat-on-content` 写入其 `predictions/`；预测段不可改写。
- 上游版本更新后若 state schema 不匹配，只能先执行 `cheat-migrate` dry-run。备份与用户确认前不得迁移历史 lane。

## 路由

评分前的 `verify-blind-rubric.mjs` 不得只核对 header：`blind-rubric.md` 必须逐字保留来源 rubric 当前完整维度定义与占位规则。维度语义有缩写、遗漏或改写时保持 PENDING，修复后换全新隔离上下文重评。

1. 先运行 `laohan-bianpai vendors`。Cheat 或 dbskill upstream 有更新时只记录待办；只在新 episode 前或独立维护窗口运行 `vendors --sync`。它报告 schema migration 时停止，不能绕过，也不能在本期中途切换规则。
2. 读取 `episodes/<slug>/01-口播稿.md` 与 `00-选题.md`，判断内容形态。
   - 教程、明确操作路径、资源交付 → `tutorial-video` lane。
   - 观点、评论、议题、个人判断 → `opinion-video` lane。
   - 无法判断时停止，不能默认为教程型。
3. 读取目标 lane 的 `.cheat-state.json`，确认 `content_form` 一致。观点视频固定使用工作流项目的 `calibration/opinion-video/`；无 lane 时先在该目录用上游 `cheat-init` 创建，不复用不匹配的旧目录。
4. 先运行 `node scripts/verify-blind-rubric.mjs calibration/<content_form>`。对当前 `01-口播稿.md` 运行上游 `cheat-score`：主评分器可用完整 `rubric_notes.md` 解析公式，但隔离子评分器只可读取已验证的 `blind-rubric.md` 与本期稿。任何 contamination warning 都必须丢弃并重启全新隔离评分。完整输出必须保留原始隔离 JSON（完整 script hash、rubric version、各维分数/理由、input_status、self_check、refusal）；登记脚本会复核它，不能只登记 Markdown 的 SHA。把无告警输出保存到 lane 内，再运行 `node scripts/register-cheat-score-evidence.mjs ...`。
   - lane 尚无真实发布样本时（`calibration_samples=0`），状态必须标为枚举值 `COLD_START_DIAGNOSTIC`，不是白话“冷启动诊断”；register/prepare 脚本与 bianpai gate 按该枚举值机械判别，不得声称已验证质量或流量，也不得为了提高 composite 覆盖原版模板、口头禅、场景、节奏或金句。评分建议只有指出具体理解/交付问题时才进入改稿候选。
5. 进入⑤：固定调用 `dbs-script-flow`、`dbs-resonate`、`dbs-ai-check` 和 `laohan-shencha CONTENT_CLAIMS`；只有首 5 秒被判弱时调用 `dbs-hook`。dbs-ai-check 只诊断具体命中句，不自动改写；dbs-hook 一旦触发，完整使用上游三种方法，每种3—5条、总计10—15条差异候选。严禁补造作者经历、采访人数、数据、结果或案例，缺证据必须写 `[需真实证据]`。报告完成后运行 `node scripts/stamp-episode-script-hash.mjs episodes/<slug> 04-深扫报告.md 04-事实核验.md`，两份⑤报告才会写入同一个 script_hash。仅 hash 匹配不足：③必须没有明确未解决高风险；⑤深扫必须 `review_status: CLEAR` 与 `unresolved_issue_count: 0`，事实核验必须 `fact_check_status: CLEAR`、`contradicted_count: 0`、`unverifiable_count: 0`，否则不得 prepare 或登记最终盲预测。⑤还必须输出 `04-事实主张.json`：任何 PROOF beat 都必须引用当前稿/事实报告绑定的 `SUPPORTED claim_id` 与同源 evidence，`INFERRED`（即使带 `inference_note`）不得进入 PROOF beat，来源链接本身不构成事实证明。注意：当前 stamp 脚本只绑定两份⑤报告 hash，`04-事实主张.json` 的 PROOF beat 边界属描述层约束，本次不改脚本。
6. ⑤报告与当前稿 hash 一致后，先运行 `node scripts/prepare-cheat-prediction-input.mjs episodes/<slug> calibration/<content_form>`。把输出的 lane snapshot 作为上游 `cheat-predict` 的唯一输入，并在预测 metadata 写 `**Script**: <snapshot path>` 与 `**Script Hash**: <sha256>`。然后运行 `node scripts/register-cheat-prediction.mjs episodes/<slug> calibration/<content_form> predictions/<file>.md v1`。它验证预测晚于快照、metadata 与快照一致，才写 `03-预测证据.json` 并标 `RECORDED`。任何改稿都会使 hash 失效；必须重跑⑤、prepare 新快照并登记新的 prediction revision，不能改写旧预测。
7. `03-校准报告.md` 的开头必须是：

```yaml
---
calibration_engine: cheat-on-content
content_form: opinion-video # 或 tutorial-video
calibration_root: <相对于本报告的 lane 路径>
script_hash: <01-口播稿.md 的 sha256>
score_status: COMPLETE
prediction_status: PENDING # ⑤完成后才改为 RECORDED
prediction_file: null # RECORDED 时必须是 predictions/...md
---
```

随后只摘要本期分数、关键修改点与上游预测文件路径；不复制一套 rubric。运行 `laohan-bianpai status`；缺上游 state、hash 或最终预测即为 BLOCKED。

## 历史兼容

`~/.openclaw/workspace-shared/content-ops` 是旧的 `tutorial-video` 校准数据，不是所有 episode 的默认源。它升级到上游 schema 前保持只读；FDE 这类观点视频不得使用它的旧教程型 composite 作为放行依据。

## 何时回到这里

- 发布后：`laohan-yunying` 只归档真实发布/数据/评论，再交给上游 `cheat-publish` 与 `cheat-retro`。
- 样本足够时：只由上游 `cheat-bump` 进行全量重打与独立审核。
- ⑭ retro-handoff 必须有 `feedback_hypotheses`：每条绑定唯一 `hypothesis_id`、干预、预期指标、T+N 窗口、状态和反馈目标（①或④）；缺字段 bianpai 必须拒绝 full workflow。该字段由上游 `cheat-retro` 产出，本 skill 作为④到⑭的路由入口，登记盲预测后必须提示⑭需补齐该字段（单期只可 `OBSERVATION`/`HYPOTHESIS`，至少两期同干预固定窗口且明确对照才可标 `UPGRADE_EVIDENCE`）。
