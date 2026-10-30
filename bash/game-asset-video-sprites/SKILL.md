---
name: game-asset-video-sprites
description: 将角色参考图和动作视频制作成循环像素精灵，处理首尾衔接、高清色键、共享裁切和全局调色板。适用于视频帧路线，不负责骨骼绑定。
---

# 视频转游戏精灵

先确认角色参考、动作和循环/一次性类型、最终像素高度、帧率及引擎导入格式。输出 RGBA 帧、精灵表、帧时长和循环区间；保留高清中间帧用于返修。

## 路线与执行

1. 先比较现成方案：[FFmpeg](https://ffmpeg.org/ffmpeg-filters.html) 抽帧/色键，[Aseprite CLI](https://www.aseprite.org/docs/cli/) 拼表/调色板，及本包后处理脚本。沿用已有工具，不先重写像素化器。
2. 先批准待机 A 与跑步 R 等中枢姿势。生成器若支持首尾帧，循环用 A→A、R→R，转场用 A→R；多参考输入不等于首尾约束。先做短片确认动作量，首尾相同可能只产生微动。
3. 背景选择角色中未出现的色相。绿幕路线在高清阶段去背景与溢色，再以 BOX 缩小，最后全局锁色。不要先缩小再按绿像素删除，也不要每帧重新提取调色板。
4. 从全片前景并集确定共同裁切框、人物尺度、地面和画布；逐帧居中会抹掉动作位移并引入抖动。
5. 找循环要同时比较首尾姿势、运动方向与接地；只取低像素差可能选中两张静止帧。只在末帧确实重复首帧时删除它。一次性动作保留起止。
6. 先预览原始帧，再比较高清透明帧和最终目标尺寸，输出锁色前后指标。调色板稳定不代表轮廓稳定。

## 可运行工具

进入本技能的 `assets/workspace/`；Python 需 numpy、Pillow、OpenCV，FFmpeg 在 PATH。例如已准备 `ref.png` 和 `frames/`：

```sh
python scripts/sprite-postprocess.py palette ref.png palette.json -k 24 --chroma
python scripts/sprite-postprocess.py pixelize "frames/*.png" palette.json pixels --height 64 --crop auto --chroma --mode box
python scripts/sprite-postprocess.py metrics "pixels/*.png" --palette palette.json --out metrics.json
python scripts/sprite-postprocess.py sheet "pixels/*.png" sheet.png --gif preview.gif --fps 12
```

高度、色数和帧率是示例，按游戏实际要求选择。生成阶段的 ComfyUI 模板名称是旧项目本地接口，不能当公开模型 ID；使用部署现场现有的图像编辑/视频节点。

## 已知边界与验收

- 历史实测：首尾帧路线优于同批多参考路线的衔接；只对当时角色/模型成立。17 帧循环是一次试验结果，不是通用长度。
- 透明蒙版的三帧中值只在慢动作中有益，跑步会抹掉脚；快速运动不默认启用。
- 原画姿态迁移的剪影提示在试验中失败，深度/OpenPose 更可靠；仍须确认角色身份和肢体。
- 检查可见像素的调色板外颜色数、二值 alpha、循环边界相对普通帧差、轮廓/落脚漂移和目标尺寸的可读性。骨骼渲染再像素化、引擎内像素导入等尚需独立验证。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
