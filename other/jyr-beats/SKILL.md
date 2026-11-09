---
name: jyr-beats
description: 卡点——识别音乐节拍（本地，纯 numpy），把一组视频/图片按拍切成剪映草稿，并在音乐上打好剪映原生"踩点"标记。当用户说"卡点 / 踩点 / 按节奏剪 / 音乐卡点视频"时使用。
---

# 卡点

```bash
jyr beats /abs/music.mp3                         # 只看 BPM 和节拍时间
jyr beats /abs/music.mp3 --clips /abs/素材文件夹 --every 2 --max-len 15 --canvas 9:16 \
          --plan /abs/work/beats.plan.json --out /abs/work/beats --publish --name 卡点
```
- `--every N`：每 N 拍切一次（快歌用 2 或 4）。素材按文件名顺序循环使用；同一视频连续取不同片段。
- 音乐轨上会写入剪映"踩点"标记，打开草稿能看到黄点，可在剪映里继续手调。
- 精度（合成节拍器实测 90–150 BPM）：速度误差 ≤1.5%，节拍位置中位误差 2 ms、最大 5 ms（< 1 帧）。真实歌曲有"半拍/倍速"歧义，听感不对就换 `--every`。
