---
name: laohan-yunying
version: "1.1.0"
description: 抖音数据与评论编排器。读取 Jeffrey 手动发布后登记的作品记录，回收作品数据和评论洞察，并把真实数据交给 cheat-on-content 复盘。Use when 用户说抓作品数据、复盘评论、登记手动发布结果、进入⑬数据或⑭评论。
---

# 抖音数据与评论编排器

本 skill 不发布、不准备发布文案、不代替 Jeffrey 点击平台。它只登记人工确认或本机Chrome适配器已经验证的发布事实，保存数据和评论证据；`cheat-on-content` 是预测与复盘引擎。

## 工作流

### 1. 发布事实登记

先运行 `bianpai check --require final`，再登记以下两种发布证据来源：

- `USER_CONFIRMED_MANUAL`：当前唯一人工发布 source，沿用`publish-record.json`。Jeffrey 在平台手动发布后提供平台身份、URL（抖音还须aweme_id）与平台显示的精确标题`platform_title`。历史`source: "user-confirmed"`仅允许schema <4 episode只读兼容；迁移或新登记必须写`USER_CONFIRMED_MANUAL`。
- `ADAPTER_VERIFIED_RECEIPT`：读取`12-发布/*-publish-results.jsonl`中与当前`final.mp4` SHA匹配的最后一个`PUBLISHED`记录；自动回执的 canonical source 固定为 source: ADAPTER_VERIFIED_RECEIPT，缺失或为其他值都不得登记。

归一化登记记录必须保留`platform`、`source`、`receipt_id|url`、`published_at`、`final_sha256`和`platform_title`。`ADAPTER_VERIFIED_RECEIPT`读取每个平台完整JSONL后，从后向前选择首条同时匹配该平台、当前final SHA、`publish_result: PUBLISHED`且`source`精确为`ADAPTER_VERIFIED_RECEIPT`的合法回执；后续FAILED或其他final记录不得遮蔽它。回执还必须绑定`authorized_by`、`authorized_at`、`authorization_note`和`bound_input_record_sha256`，并与本期`FULL_PIPELINE_TO_PUBLISH`授权完全一致；`published_at`与`recorded_at`必须是有效时间且不得早于授权。缺少任何绑定字段就停，不能编造。

⑫只消费上述归一化登记；原始JSONL行、浏览器页面或“点击过”都不是完成证据。

本Skill不得承担发布点击、上传、表单填写或浏览器控制；这些只属于release package与本机Chrome适配器。自动发布回执只证明对应平台已发布，不证明该平台运营数据已经接通。

### 2. 人工发布记录

`USER_CONFIRMED_MANUAL`只登记 Jeffrey 提供的作品 URL、aweme_id 与 platform_title；不调用 URL 解析、平台浏览器、发布 adapter 或任何替代发布工具。URL 必须包含同一 aweme_id；缺任一身份字段则停，不能编造。`ADAPTER_VERIFIED_RECEIPT`只读取既有回执，不调用或驱动发布 adapter。

写 `12-发布/publish-record.json`：

```json
{
  "platform": "douyin",
  "status": "PUBLISHED",
  "url": "https://www.douyin.com/video/<aweme_id>",
  "aweme_id": "<id>",
  "platform_title": "平台显示的精确作品标题",
  "published_at": "2026-07-10T20:00:00+08:00",
  "final_path": "07-剪辑/final.mp4",
  "final_sha256": "当前 final.mp4 的 SHA-256",
  "source": "USER_CONFIRMED_MANUAL"
}
```

然后调用上游 `cheat-publish` 登记同一 URL；只更新预测 metadata，绝不修改预测段。完成后运行 `node scripts/register-cheat-publish-evidence.mjs episodes/<slug>`，保存 publish 时点的 lane state 快照并验证 prediction header、URL、aweme_id、发布时间和不可变预测段；缺该证据时⑫不得完成。

发布后首屏截图或创作者中心导出是可选强证据，不能代替 Jeffrey 的发布事实，也不因缺失阻断⑫。若保存，证据文件必须在本期 `12-发布/`，并写 `platform-display-evidence.json`：`schema_version: 1`、evidence_path/SHA、aweme_id、platform_title、display_title、cover_asset/SHA、final_sha256、title/cover/video 三项 `MATCHED` 结论、reviewer、captured_at、reviewed_at。任一项与当前 publish-record、selected-cover 或 final 不一致时，⑫必须显示未完成，直到删去该可选证据或重做核对；不得自动修正或伪造截图。

### 3. 数据快照

人工提供的创作者中心数据来源写 `manual`。TzFilm SQLite adapter 只允许显式运行：`python3 scripts/tzfilm_douyin_adapter.py snapshot --db <douyin_stats.db> --episode episodes/<slug>`。它必须从本期 publish-record 读取 aweme_id/platform_title，按精确标题查询并拒绝歧义，不再接受命令行伪造作品 ID，也不得覆盖已有快照。它不运行 launchd、Telegram、预测追踪或任何发布动作。

TzFilm 的飞书同步仅作为外部看板；不读取飞书作为数据源，也不写 episode 以外的状态。发布后预测追踪完成并经本地验证后，可额外保存到 `13-数据/tzfilm-tracking.json`，标 `source: tzfilm-tracker` 与抓取时间；它只辅助观察，不得替代 Cheat 的发布前盲预测、retro 或 rubric。

发布后默认按① `00-选题.json.experiment.observation_window` 回收；不得在发布后改窗口。`metric_keys` 是预注册的指标键（`plays`、`likes`、`comments`、`shares`、`favorites`、`ctr5s`、`avg_duration_sec`）。当前只接受用户提供的创作者中心数据；不得把未验证的 opencli 或浏览器抓取写成默认链路。TzFilm adapter 验收完成后再更新这一段的自动化优先级和降级链。

当前⑬/⑭默认数据与评论真值仍限抖音；其他平台写`UNSUPPORTED_SOURCE`或`NOT_COLLECTED`，不写`0`。每次追加一行到 `13-数据/snapshots.jsonl`：

```json
{"platform":"douyin","aweme_id":"<id>","observed_at":"ISO-8601","observation_window":"T+3","measurement_role":"TARGET|CONTEXT","metric_dictionary_version":1,"source":"creator-center|manual","metrics":{"plays":0,"likes":0,"comments":0,"shares":0,"favorites":0}}
```

只有窗口精确匹配①、`plays` 和全部 metric_keys 非空的记录可标 `TARGET`；提前、额外或指标缺失的记录必须标 `CONTEXT`，可保存趋势但不能完成⑬、支持或反驳假设。数据自动抓取失败必须保留失败原因和数据来源，降级为 manual；不得把空值写成 0。

### 4. 评论与复盘交接

TzFilm 的评论导出只允许 export，不允许 reply。显式导入：`python3 scripts/tzfilm_douyin_adapter.py comments --input <unreplied-comments.json> --episode episodes/<slug>`。adapter 必须验证 selectedWork 精确标题与 publish-record 一致，过滤空文本并去重；禁止调用 `auto_reply.py reply` 或保存回复计划到 episode。

首选 `douyin-session` 抓取高赞评论；Cookie 失效时引导用户重新登录，失败后让用户粘贴高赞评论。评论可用时写 `14-评论/comments.jsonl`，每行固定为 `{"platform":"douyin","aweme_id":"<id>","captured_at":"ISO-8601","source":"douyin-session|manual","text":"评论正文","likes":0}`；不可用时仍写洞察文件并说明原因。

写 `14-评论/insights.md`，首行必须为 `评论数据状态: AVAILABLE` 或 `评论数据状态: UNAVAILABLE`。UNAVAILABLE 时第二行必须是 `失败原因: <具体原因>`；之后记录抓取时间、来源、代表评论、3—5 个主题、选题信号与待验证假设。

T+N 数据和评论齐备后，调用上游 `cheat-retro`。它写 prediction 的 `## 复盘` 段、`rubric-memo.md` 和经用户确认的 `script_patterns.md`；本 skill 不修改 rubric。完成后写 `14-评论/retro-handoff.json`：`status: "COMPLETE"`、episode、aweme_id、prediction_file、prediction_after_retro_sha256、rubric_memo_sha256、snapshots_sha256、insights_sha256、comments_sha256（无评论时为 null）和 ISO `completed_at` 都必填；还必须写非空 `feedback_hypotheses` 数组，每项有唯一 hypothesis_id、intervention、expected_metric、`T+N` observation_window、`OPEN|SUPPORTED|REJECTED|INCONCLUSIVE` status 与目标 `feedback_target: "①"|"④"`。结论为 `UPGRADE_EVIDENCE` 时，额外要求至少两期 evidence_episode_ids 和 comparison_note；单期结论只准 OBSERVATION 或 HYPOTHESIS。没有这些证据不得把⑭标完成。

## 降级链

| 环节 | 首选 | 失败后 | 最终兜底 |
|---|---|---|---|
| aweme_id | Jeffrey 提供 ID | — | BLOCKED |
| 数据 | 用户提供创作者中心数据 | TzFilm adapter 独立验收（不覆盖真值） | BLOCKED |
| 评论 | 用户提供导出的高赞评论 | TzFilm export-only 导入独立验收 | 标记 UNAVAILABLE |

## 反模式

❌ 看到 `final.mp4` 就自动发布，或拿播放数据反改盲预测。  
✅ 用户发布后登记 URL；数据只进入快照和 upstream retro。

❌ 把 `laohan-xiazai` 的临时抓取输出当运营真源。  
✅ 统一写入 episode 的发布、快照和评论产物，再由 bianpai 路由。
