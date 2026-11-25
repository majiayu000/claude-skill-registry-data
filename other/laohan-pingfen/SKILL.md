---
name: laohan-pingfen
metadata:
  version: "1.0.0"
description: 视频爆款评分与自校准闭环。发布前对成片发布包打预测分（双门模型 10 维 rubric），发布后用真实数据打实际分（账号分位基准），复盘时对比预测 vs 实际校准评分机制本身。Use when 用户说给视频评分、打分、爆款预测、评分校准、发布前自评、复盘评分准不准，或视频制作交付链要求出 score_report。
---

# laohan-pingfen — 视频爆款评分与自校准闭环

三个模式一个闭环：**PREDICT（发布前预测分）→ ACTUAL（发布后实际分）→ CALIBRATE（校准机制本身）**。评分不是打完就完——不看真实数据评判机制准确度、不持续修正权重的评分 = 占星，禁止。

## 触发 / 反触发

- 触发：视频制作完成交付发布包时（预评）；48h/7d 数据回收后（实评）；复盘任务中对比预测与实际（校准）；用户要求给已发布视频补评/全量评分。
- 反触发：稿子层 rubric 评分走 cheat-on-content（cheat-predict/cheat-score，评的是**稿件潜力**）；laohan-pingfen 只评**成片发布包与线上表现**，两层互补不互代。episode 接 cheat 校准 lane 的路由归 laohan-jiaozhun。

## 输入 / 数据链

- PREDICT 输入：发布包五文件（成片/三平台文案/封面）+ 标题候选 + 当期质量门回执（字幕/口型/weigui/封面审——引用结果，不重评）。
- ACTUAL 输入：平台真实数据。**不新建数据通道**——按项目合同走既有链路：amy-data-readback（CDP9333 创作者中心）/ laohan-yunying / opencli douyin；快照与登记点真源 = publish-record.json `data_pulls` + gap-analysis。13h 内读数无判定效力（EP08 判例），48h 起主判，7d 终判。
- baseline：账号已发布作品全量分布（`docs/ops/pingfen/baseline.json`，脚本重算）。

## 三模式

### 1. PREDICT — 发布前预测分

评分对象 = 发布包（标题+封面+成片+文案），rubric 真源 `references/scoring-rubric.md`（版本化，当前生效版本记录在项目 `docs/ops/pingfen/rubric.json`）。执行者按 rubric 逐维打 0-5 分并留一行理由，`scripts/pingfen.py score` 合成总分与档位。

产出 `docs/ops/pingfen/predictions/<EP>.json`：
- **immutable**：写入后预测段不可改（发现错只准在 notes 追加勘误，不得改分——防事后作弊，同 cheat-predict 预测段纪律）。
- 发布包接入：build-pubpk 带 score_report；飞书交付消息附评分行。

### 2. ACTUAL — 发布后实际分

`scripts/pingfen.py actual` 从快照/登记数据计算：主指标相对账号历史分位（播放 45% + 千播转发 25% + 千播评论 15% + 2s跳出反向 10% + 千播赞藏吸粉 5%），产出等级 S/A/B/C/D + 结构诊断（入口/裂变/互动哪层强弱）。产出 `actuals/<EP>.json`。

### 3. CALIBRATE — 校准机制本身

`scripts/pingfen.py calibrate` 对比预测档 vs 实际档：|差|=0 → CALIBRATED；≥1 档 → OVER/UNDER-ESTIMATED；≥2 档 → 强制归因。归因 = 找出被数据证伪的高分维度（例：F1 转发对象打了 4 分、实际千播转发垫底 → F1 的打分锚失准）。产出权重调整提案（±0.02 步长、单版本≤3 维）。

**生效路径**：提案写 `calibration-log.jsonl` → 按"10 分钟未回复自行确认"项目条款生效 → rubric 版本 +1 → **回测不退化才合入**（对全历史 backtest，已证爆款必须仍居最高档）。有效样本≥30 后可评估数据驱动权重拟合（当前小样本纯 rubric，参考 clipforge MIN_SAMPLES 门禁——样本不足不硬拟合）。

### 回溯校准（backtest）

机制新建或 rubric 改版时，用 rubric 给历史已发布视频的发布包打分，与真实数据对比验证区分度（例：17 倍差爆款应显著最高分、塌方期应低分）。backtest 不通过 = rubric 区分度不足，禁止定稿。

## 硬规则

1. 预测段 immutable；ACTUAL 数据必须来自真实回收链路，禁止编造/外推冒充实测。
2. 校准必须留下预测-实际对照与归因记录（`calibration-log.jsonl`），无记录不得宣称已校准。
3. rubric 权重只能经 CALIBRATE 流程变更（版本化+回测），禁止拍脑袋直接改权重。
4. 脚本负测：`pingfen.py` 对缺输入/非法档位/越界权重必须非 0 退出；预测文件已存在时 `score --write` 拒绝覆盖（FORCE 不存在）。
5. 评分与发布解耦：低分不自动拦截交付（交付门是各质量硬门），评分是预测与学习工具；高风险信号（如 D 档预测+关键维度 0 分）在交付消息中显著提示 Jeffrey。

## 失败与边界

- 数据缺（48h 未到/未回收）：ACTUAL 标 `PENDING(window)`，禁止用 13h 内读数出正式等级。
- 样本不足：baseline 分位在 N<8 时降级为秩参考并标注；等级判定附带样本量。
- 新账号冷启动：无历史基线 → 实际分只报绝对结构与外部基准（如有），等级标 `NO_BASELINE`。

## 完成证据

- PREDICT：predictions/<EP>.json 落盘 + 桌面发布包含 EPxx-评分.md（report 子命令）+ 飞书交付消息带评分行 + 窗口汇报含评分。
- ACTUAL：actuals/<EP>.json + 数据窗口与来源标注。
- CALIBRATE：calibration-log.jsonl 追加记录（含 backtest 区分度结论）。
