---
name: remotion-delivery-qa
description: Run reproducible delivery QA on Remotion MP4 exports, covering transition frame extraction, full-frame technical and text-edge checks, audio track verification, and dual-directory archiving of deliverables and project files. Only for Remotion export acceptance; not for general code review or ordinary web testing.
version: 1.0.2
---

# Remotion 导出与交付 QA

把“渲染成功”“全帧技术检查”“代表帧视觉检查”和“完整播放听审”分开记录。只报告真正完成的检查范围。

## 按需要进入

- 选 composition、导出与定位旧文件：读 [导出身份](references/export-identity.md)。
- 检查正文/注释排版和转场：读 [文字与抽帧](references/text-and-frames.md)。
- 检查 MP4、帧数、音轨与分轨：读 [媒体验证](references/media-checks.md)。
- 整理用户给出的两个目录：读 [交付归档](references/delivery.md)。

## 不可混淆的结果

- 脚本逐帧检查边界、透明度或解码，不能证明每帧美观。
- 抽查清晰关键帧，不能证明转场没有一帧重叠、裁切或闪白。
- 原 WAV 存在，不能证明 MP4 内有正确音轨；静音 MP4 也能正常渲染成功。
- 旧版和本次版使用不同 composition 或文件名时，不能凭“目录里有 MP4”认定成功。

在确有导出任务时沿用当前依赖版本与已验证渲染入口；先修具体问题，再做针对性复检。不要每次都重跑与本次改动无关的完整审计。

## Example

A delivery report that separates what was actually checked:

```
渲染        Remotion render 成功，composition=main，1920x1080，30fps
全帧技术    抽帧 900 帧，全部检查，无黑帧无撕裂
文字边界    逐帧检查字幕安全区，第 412 帧右侧超出 3px（已记录）
音轨        ffprobe：2 轨（aac 48kHz），时长 30.00s，与合成一致
完整播放    人工听审通过
归档        成片入 deliverables/，工程入 project/
```

"渲染成功" is never reported as "质量已验收".
