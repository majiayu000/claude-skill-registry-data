---
name: visual-comedy-director
description: "把无对白动画故事拆成可生成、可剪辑的连续镜头表，控制喜剧节奏、空间关系与时间轴。"
---

# 视觉喜剧分镜

## 输入与交付
读取story.md和characters.json；输出shots.json，其顶层为episode_id、fps、target_duration_s、shots。
每镜记录shot_id、start_s、duration_s、cast、scene、shot_type、composition、camera、action、start_state、end_state、gag、sound_cues、image_path、video_path、source_in_s、source_out_s、freeze_s、status、image_status、video_status。暂未生成的路径和取用区间为null；初建时三个状态均为pending。image_status和video_status分别由关键帧与视频环节维护，取值为pending、generating、needs_review、approved、retry_needed。文字分镜通过不代表媒体通过；两种媒体状态均approved且文件与取用区间有效，才将status设为approved。
## 导演规则
普通镜头约3—5秒，动作约2—3秒；70秒通常15—20镜，但以动作可读和总时长为准。优先从以下选择，不必每集用满：L1双人中近景、L2表情特写、L3前景小角色与背景威胁、L4第三方反应、L5草地一排探头、L6仰拍、L7包围、L8追逐全景。
保留系列双人惊讶开场，同时在3秒内展示异常。主要爆点可安排约10/30/55秒；适当预留0.5秒期待停顿及0.2—0.3秒反应定格，不机械给每个动作插停顿。末帧约0.5秒定格纳入总时长。
仰拍增强气势，俯拍突出弱小；紧张时可推近，但追逐路线和包围关系需要全景。写清轴线、视线目标、运动方向、道具持有者、姿态和损伤状态；切镜后保持连续，跨轴需有可读过渡。
一个短镜头只承担可执行的主要动作；复杂连续事件拆镜。参考图需能支持起始姿态，不能只用表情图要求复杂全身动作。
## 时间语义与验收
start_s和duration_s是最终成片区间，duration_s包含定格；默认硬切，转场额外记录transition及overlap_s并纳入总长，不能重复加时。各镜区间完整覆盖目标时长，无意外空隙或重复。画面可生成性不足时回改分镜，不能靠后期长时间静帧凑数。
交付scene-generator、animation-prompt和sound-designer同一份分镜；改动时通知受影响下游并更新入点。

## 项目约定
本技能服务双主角反差、无对白视觉喜剧系列；默认约70秒、9:16竖屏，结尾留钩子。用户的新要求优先。保持已确认角色与画风，不把示例角色强加给其他项目。
每集在用户项目目录保存产物；镜号采用S001等稳定编号，修改内容不随意改号。沿用episode.json清单：episode_id、theme、target_duration_s、character_version、story_path、shots_path、audio_path、output_path、status。首次单独调用时只建立实际需要的文件，不要求先完成全部流程。
路径必须指向真实文件；未完成用null或“待生成”，不用虚构链接。提示词、生成素材、审核通过、导出成片是不同状态。已获授权内继续工作，不重复确认；付费工具遵循实际工具报价与授权流程。
