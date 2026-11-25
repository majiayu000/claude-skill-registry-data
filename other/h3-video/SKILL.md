---
name: h3-video
description: 在 DSH 对话中用 MiniMax H3 生成带声音的视频，按用户指定的清晰度、Turbo 或质量档和秒数调用，按任务 ID 取回 MP4。
whenToUse: 用户提到 H3 生视频、480p Turbo 预览、768p 质量档、指定镜头时长、查询视频任务或需要生成单个分镜时使用。
---

## 从对话到镜头

调用 `h3_generate_video`，将档位填入 `preset`，将用户要求的秒数作为数值填入 `duration_seconds`。每次生成一个有声镜头。创作页和工具共用参数。用户要指定画幅时传 aspect（landscape / portrait / square）；质量档 steps 可设 4–50，Turbo 省略 steps；seed 填 0–2147483647 的整数。没要求覆盖时使用工作流默认值。

| 用户说法 | preset |
| --- | --- |
| 480p Turbo、快速预览 | turbo480 |
| 768p Turbo | turbo768 |
| 480p 质量档 | quality480 |
| 768p 质量档、768p 高质量 | quality768 |

例如「用 480p Turbo 预览，拍 8 秒雨打窗户」传 `preset="turbo480", duration_seconds=8`。「换成 768p 质量档，同样时长」沿用原提示词和 8 秒，传 `preset="quality768"`。需要复用随机输入时带回上一镜的 seed。未指定档位和时长时，纯文字使用 480p Turbo、5 秒，带参考图使用 480p 质量档、5 秒。

把主体、动作、镜头和现场声音写入 prompt。每镜可请求 1–15 秒（1–4 秒属于较短实验范围），24 fps，帧数向上对齐至 17k+5。回传实际帧数及实际画面时长。queued 或 running 时使用同一 ID 调 h3_video_status，完成后把回执中的 playback_markdown 原样贴在最终回复的独立行，让 DSH 会话显示原位播放器。保留相对路径和任务 ID，本地文件路径可另附。unknown 时核实该任务。队列完成且需要释放显卡时调用 h3_release_gpu。

## 几分钟的成片

整片优先使用 h3-long-film 技能和 h3_film_create 项目流程。先把总时长拆成带时间码的镜头表，为每镜记录目标秒数、主体、连续动作、机位和声音。举例，两分钟可先排 12 个 10 秒镜头。先用 480p Turbo 验证节奏和构图，选定镜头再按目标质量重生成。单卡逐镜执行并记录任务 ID、seed 和 MP4 路径，以便中断后继续。跨镜写明需要延续的人物、服装、场景与运动方向。

将镜头交给可用的剪辑流程，在时间线上逐镜裁齐目标时长，统一对白、环境声和音乐，最后导出并核对成片时长。只有取得剪辑后的最终文件才报告整片完成。此插件提供镜头生成、取回与显卡释放工具。

## 人物与参考图
用户发图并要求保持人物或物体一致时，调用 h3_generate_video，按 <Picture 1> 起的顺序传入 reference_images 数组，元素是对话图片的 sha256: 附件 ID。支持 1–9 张。选择 quality480 或 quality768，省略档位时带图默认 quality480。使用 MiniMaxH3ReferenceToVideo 和专用 Ref2VA 权重。查看回执中的 mode 和 reference_images。长片使用本机人物库和长片技能锁定每镜出场角色。
