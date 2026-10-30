---
name: game-asset-spine-portrait
description: 将正面立绘拆成完整 RGBA 部件并制作带网格转头、视线、表情和二次运动的 Spine 角色，适用于桌面角色、对话头像与立绘演出。
---

# 正面立绘 Spine

输入全身或半身正面图、所需表情/手势和实际显示尺寸。输出完整分层、Spine 4.2 JSON、图集和运行时演示。正面视差转头不等于任意角度三维转头。

## 执行

1. 先比较 See-through 语义拆层、同画布逐部件编辑和现成 Spine 工具。该项目最终采用 See-through；早期像素差分切层已被否定，不要因旧脚本还在就当默认路线。
2. 基础图双手与衣身分开；尾巴、翅膀、发饰逐一描述位置与形状。表情同画布只改局部，核对画布一致、头部偏移和前景 IoU。历史目标偏移 <0.5px、IoU >0.99，应按实际显示尺寸确认。
3. See-through 先检层完整性再绑骨。分辨率越高不保证部件越全；缺裙子/头饰时尝试另一种子或较低分辨率，再以整层替换。不同次推理的深度标尺不直接互比。
4. 需要高分辨率头部时使用附带节点补丁，先 `git apply --check` 确认上游版本兼容。头部结果通过 `latest.txt` 另存时，串行运行并核对本次记录；背面无脸可能不更新记录，不能复制上一张脸。
5. 把层按原始 pad/resize 变换还原到同一画布；以预乘 alpha 缩放，按逐像素深度合并。保留模型生成的完整轮廓，不把可见部分替换回原图像素。虹膜/嘴等局部使用完整 RGBA。
6. 先查重合成再生成网格与权重。头部转动必须有连续形变网格；手势更换使用独立附件/骨骼，表情用插槽切换，眼白裁剪虹膜。头发/衣摆优先用 Spine 4.2 原生物理。

## 配套工具

进入 `assets/workspace/`，配置 `COMFYUI_DIR`，按 sources 安装节点、模型与超分权重。准备本次 `front.png`、See-through 导出和 DWPose：

```sh
python scripts/seethrough-to-layers.py front.png seethrough poses.json layers
python scripts/front-rig.py layers rig --name character
python scripts/spine-pack.py rig --name character
node scripts/spine-verify.mjs rig character
```

同画布编辑提示词与节点 API 工作流附在 config。ComfyUI API 图须用现场 `/object_info` 校对节点输入，旧模板不是跨版本契约。

## 验收与失败经验

重合成误差超过历史参考约 12/255 或 `alpha_miss` 超过 1% 时先定位缺层。检查原尺寸头部、手腕、肩颈和发际线，再查转头/眨眼/张嘴/手势过渡。导入实际 app 后才可声称在 app 跑通。

爆炸图曾在中间保留整人且漏部件；Qwen-Image-Layered 曾按色彩/阴影拆层而非人体语义；通用矢量化破坏渐变、睫毛和虹膜。超分只能改善清晰度，不能补缺失部件或错误轮廓。8GB 显卡可行性当时仅从较大显卡的峰值推测，不能当真实 8GB 实测。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
