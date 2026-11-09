---
name: jyr-roughcut
description: 口播粗剪——把一条口播原片自动剪掉气口停顿、口癖、结巴、说错重来的半句，输出剪映草稿（A-roll 切碎在一条轨上 + 重新对齐的字幕）。规则先剪一遍，再由 Agent 读句子做语义取舍。当用户说"粗剪 / 口播粗剪 / 剪气口 / 去口癖 / 把这条口播剪干净放进剪映"时使用。
---

# 口播粗剪

两步，Agent 在中间做判断：

```bash
# 1) 规则粗剪 + 生成审阅单
jyr roughcut /abs/raw.mp4 --plan /abs/work/rc.plan.json
#    -> rc.plan.review.json：编号句子 + 自动删除项（filler/repeat/false-start）
```
2) **读 review.json 的句子**，找出规则看不出的：同一句说了两遍（保留后一遍）、说错重来、跑题。写 edits：
```json
{"drop_sentences": [6, 13, 14], "keep": [{"sentence": 3, "word": 2}], "drop_words": [[20, 4]]}
```
```bash
jyr roughcut /abs/raw.mp4 --plan /abs/work/rc.plan.json --edits edits.json --out /abs/work/rc --publish --name 名字
```
- `--pause 0.5`：超过 0.5 秒的停顿剪掉（两侧各留 0.12 秒呼吸）。Whisper 常把"嗯/呃"直接略掉不写出来，这些口癖会落在停顿里被一起剪掉。
- 默认带字幕；`--no-subtitles` 关掉。
- 实测（316.6 秒真实口播原片，对照人工粗剪 232.4 秒）：只用规则 → 250.0 秒，人工保留的内容我们保留 99%（90.4% / 天花板 91.0%）；加 Agent 删 3 句 → 241.7 秒。剩下的差距是人工更细的字词级取舍。
