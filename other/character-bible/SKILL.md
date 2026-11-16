---
name: character-bible
description: "为无对白双主角喜剧建立角色设定、参考图和版本，适用于首次角色定稿或有明确范围的角色调整。"
---

# 动画角色资产

## 输入与交付
输入角色描述、反差关系、已有参考图；缺少角色描述时先提出一组可审阅方案，不自行锁定。输出characters.json和角色参考图目录，确认前标为draft。
characters.json包含version、status、style，以及characters数组；每个角色记录id、name、species、colors、body_ratio、limbs、locomotion、prop_handling、signature_features、personality、reference_images、expressions。双主体型比例和关系写在pair字段。
## 制作
1. 建立体型/性格/身份至少一种反差；每角固定3—5个识别特征和两个主要性格标签。默认可用绿色胖青蛙与红棕短粗蛇，但名称和造型以用户确认结果为准。
2. 首次明确蛇有无手脚、如何持物与移动，不一边定义无肢一边要求叉腰跑步。用参考图固定比例，数值是设计目标，不声称模型能精确遵守。
3. 固定圆润、鲜亮、温暖的3D卡通材质与色彩；场景光照另行控制。建立正面、侧面、背面与同框比例参考，以及害怕、开心、生气、惊讶、得意、倒霉六种表情；已有合格素材优先复用。
4. 调用当前可用图像工具前读取对应生成技能。遵循用户image2.5偏好；无法选择或验证时明确说明，不声称使用过。不通过隐式换模型掩盖缺口。
5. 实际查看参考图，核对颜色、肢体、轮廓和双主体型；不合格图不进入锁定资产。用户确认后status=approved，后续更改另建版本并列出受影响镜头。
## 交接
纯文字策划可向story-writer交付draft状态的characters.json，reference_images为空数组；不把文字确认当作完整角色资产approved。媒体制作仍需完成参考图审核与确认。向story-writer交付characters.json；向scene-generator交付相同版本和真实参考图路径。未生成图片时明确只完成文字设定，不称为完整角色资产包。

## 项目约定
本技能服务双主角反差、无对白视觉喜剧系列；默认约70秒、9:16竖屏，结尾留钩子。用户的新要求优先。保持已确认角色与画风，不把示例角色强加给其他项目。
每集在用户项目目录保存产物；镜号采用S001等稳定编号，修改内容不随意改号。沿用episode.json清单：episode_id、theme、target_duration_s、character_version、story_path、shots_path、audio_path、output_path、status。首次单独调用时只建立实际需要的文件，不要求先完成全部流程。
路径必须指向真实文件；未完成用null或“待生成”，不用虚构链接。提示词、生成素材、审核通过、导出成片是不同状态。已获授权内继续工作，不重复确认；付费工具遵循实际工具报价与授权流程。
