---
name: game-asset-tts-narration
description: 为游戏美术演示、教程或普通角色对白设计虚构音色、批量生成 TTS 并筛选候选，处理识别质检、韵律、分段接缝和配音交付。
---

# TTS 讲解与普通对白

先确认语言、讲解/对白、语速、声线、句子 ID、试听方式和输出采样率。方法来自用户指定的 voice-drama 技术实现及游戏美术视频；这里只保留普通语音流程，不带原项目台本、音频或场景配置。

## 模型与参考

1. 先用公开上游的标准能力：Qwen3-TTS VoiceDesign 造虚构音色，Fish S2 的参考音频/文本与行内标签，Breeze 的整段声音指令。各模型控制参数和标签不同，先读所选版本文档，不把一套标签或 cfg 迁移到全部模型。
2. 描述声音的音区、音色、语速与说话方式，用中性完整句生成参考。Qwen 候选跨段可能不像同一个说话人，先筛一个稳定参考后固定，不每句重新造音色。
3. 参考音频与逐字文本配对，分别保留采样率、模型版本、种子和描述。参考语气会影响后续输出；需要自然讲解就不要使用与目标情绪冲突的参考。声纹相似和韵律相似分开判断。

## 批量与质检

- 文字中的数字、单位、缩写先写成期望读音，屏幕字幕保留正常排版；原脚本关闭 normalize，迁移时应明确自行负责规范化。
- 给每句稳定 ID，每句有限数量候选，记录 manifest；断点续跑按文件存在跳过，因此文本/模型/参考改了要用新输出目录，避免误用旧音频。
- `qc.py` 读取同名 `.lab` 或 `manifest.jsonl`，检查时长、识别文本、中文 CER、基频及语速。它的 CER 只统计汉字，数字和拉丁词需另外核对；不能用 CER=0 保证整句正确。
- 识别模型的同音字误差、标点忽略和气声无基频应分开解释。`prosody.py` 的半音跨度/能量波动只是代理，不能据此声称自然、好听或听过。
- 同一参考、不同种子仍可能声线漂移；试听普通长句、疑问/陈述与相邻段衔接，必要时测说话人相似度。分句方便重抽，却可能在未收尾处断开；交叉淡化不能补缺音节。
- 成片配音保留句首/句尾余量，必要时 FFmpeg `atempo` 保持音高加速。响度、真峰值、BGM ducking 与是否截断需在最终混音里复核。

## 附带代码

进入 `assets/workspace/`，按上游安装模型环境和本地 Fish API 服务；先看 implementation 的依赖分组与环境变量：

```sh
python src/voice_design.py qwen -n 2
python src/tts_batch.py --named config/narration-example.json:voice --ref assets/voice/candidates/qwen-a-s1.wav --takes 2 --temperature 0.7 --top-p 0.7 -o work/takes
python src/qc.py work/takes -o work/qc.json
python src/prosody.py work/takes -o work/prosody.json
```

示例需自行取得权重；不自动下载或启动服务。Fish API 适配器复用本地 MessagePack 协议，版本变更要检查请求字段。VoiceDesign 示例已换成普通教程台词与中性音色描述。

## 交付与边界

输出选中音频、可编辑讲稿、句子 ID/时长、候选/质检记录及试听结论。原项目讲解视频用过 1.15 倍速与每句两遍，但这些不是所有语言/声线的默认值。源项目中的表演情绪比较不推广为普通讲解的模型排名。

本次只验证代码、输入输出与不加载权重的离线小样；没有重新进行模型推理、音色试听或 GPU 性能评测。资源获取见 [sources.md](references/sources.md)，代码适配见 [implementation.md](references/implementation.md)。
