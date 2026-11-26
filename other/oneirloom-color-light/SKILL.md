---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-color-light
description: 把色彩、明度、对比、光向、材质受光和空气感转成区域明确的图像提示词。用于修正偏灰、偏冷、过曝、光色错位或“鲜活梦幻”等抽象氛围。
triggers:
  - oneirloom-color-light
  - oneirloom
  - color
  - light

---

# Color and light

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

把色彩、明度、对比、光向、材质受光和空气感转成区域明确的提示词语言。本技能是判断规则库，不是时序流程：按下面的清单检查，反推场景的证据细则在 references。

## When to use

- 修正偏灰、偏冷、过曝、光色错位等具体光色问题
- 把“鲜活”“梦幻”等抽象氛围转成光色机制
- 反推或修正任务中的区域色彩对照、材质基色判定、人像光向推断（配合 `oneirloom-visual-analysis` 的 reconstruction workflow 使用）
- 透明/透光面料的色彩记录
- When material appearance is the unresolved decision, read [material response](references/material-response.md) for base color, reflected illumination, finish, transmission, and scale cues. Transparent-fabric evidence specifics remain in [evidence checks](references/evidence-checks.md).

## Regional color method

1. 分区域标注主体、背景、天空、云、暗部和高光。分别描述色相、明度、饱和度；整图一个“低饱和”标签会抹平冷暖关系。
2. 明确光源方向、软硬、环境补光、阴影深浅、色彩反射和材质响应。`柔光`控制边缘，`亮`控制明度，`发光`可来自局部晕染；三者不可互换。
3. 将氛围和色彩机制分开。“鲜活”可通过区域色相区分、暖色中间调、动作与表情建立；“梦幻”也可在深色场景中由发光体和空间层次产生。
4. 描述暗部支点与亮部过渡。例如黑发保持深色体积，皮肤中间调暖亮，云层亮处呈奶油杏桃色。避免全局调色命令与矛盾的明暗要求。

## Minimal correction

当天空、肤色一起偏青时，只改区域色彩句，固定人物、构图、服装与裁切；下一轮检验区域是否分开。

## Reconstruction evidence checks

反推与修正场景的三项证据检查。摘要如下，完整规则见 [references/evidence-checks.md](references/evidence-checks.md)：

- **区域对照**：按大面积视觉区域对比源图与结果；区分材质基色与受光下的表现色；整体冷暖印象不是全区域调色指令。
- **透明面料**：分开记录基色、透明度、透出底色与反光；亮区表现不足以判定基色；高透黑色保持黑色材质身份，不替换为白、裸色或不透明黑。
- **人像光向**：从受光面与投影推断主光方向与高度；保持观察到的主辅光关系；区分材质基色与照明色、大面有色照明与轮廓高光。

## Output and handoff

交付区域明确的光色句，融入主技能的完整提示词；控件与参考图输入不写进提示词正文。

区域色彩句连续两轮修正仍混色或偏色时，转入 `oneirloom-result-diagnosis` 检查模型、参考通道与画幅，不继续叠加同义色彩词。
