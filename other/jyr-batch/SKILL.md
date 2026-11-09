---
name: jyr-batch
description: 批量出剪映草稿——一个模板计划 × 一张表（CSV/JSON），每行生成一个草稿（换标题/素材/颜色/时长）。当用户说"批量做草稿 / 批量剪映 / 一个模板套 N 条 / 系列视频统一包装"时使用。
---

# 批量

模板就是普通计划，把要变的地方写成 `{{字段}}`：
```json
{"name": "第{{期数}}期-{{标题}}", "canvas": "9:16",
 "tracks": [
  {"type": "video", "clips": [{"src": "{{视频}}", "duration": "{{秒数}}", "transition": "auto"}, {"src": "/abs/片尾.png", "duration": 2}]},
  {"type": "text", "clips": [{"text": "{{标题}}", "duration": "{{秒数}}", "style": {"font": "auto:title", "color": "{{颜色}}"}}]}]}
```
```csv
期数,标题,视频,秒数,颜色
1,开场,/abs/a.mp4,3,#FFD400
2,进阶,/abs/b.mp4,4.5,#00E5FF
```
```bash
jyr batch template.json rows.csv --out-dir /abs/work/batch --publish
```
- 整个值都是 `{{字段}}` 时保留数字类型（`"{{秒数}}"` → 4.5）。
- 表里缺字段会报错并指出位置。
