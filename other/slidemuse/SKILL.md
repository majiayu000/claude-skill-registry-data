---
name: slidemuse
description: 将书籍、PDF、论文、报告或文字制作成视觉统一的图片版 PPT，适用于竞赛、答辩、路演、课程展示和读书分享；按需还原可编辑 PPTX，也支持直接还原已有图片、PDF 或图片版 PPTX。不用于普通修改已有可编辑 PPTX。
---

# SlideMuse · 2.23.0

新材料按 **内容提炼 → 图片 PPT → 按需可编辑还原** 制作。已有页面要求还原时直接进入重建。内容与视觉应准确、清楚、统一；检查服务于这几个结果。

## 开始任务

先检查用户已给的材料和上下文，必要时阅读材料来判断篇幅与用途。只询问会实质改变结果、又无法合理推断的信息，并一次问完；不要为了填满五个字段阻止阅读。

- 源材料不可访问、受众/任务存在相互冲突的解释、关键事实缺失时询问。
- 未指定风格：按无参考处理；未指定页数：根据材料推荐并随内容稿展示；未指定交付：先做图片版；默认 16:9、沿用材料语言。使用场景可从上下文判断，无法判断且影响内容取舍时再问。把采用的默认值简要告诉用户，不额外等待确认默认值。
- 用户已要求可编辑版，即已授权最后的重建阶段，不在图片版完成后重复询问。
- 默认只在**内容方案**和**风格选择**处请用户决策。已有“你来定”“按这个做”“其余由你决定”等对应授权时继续执行，记录授权范围即可。明确修改也是该范围的授权。
- 状态码、哈希、日志与检查文件由 Agent 管理，不要求用户理解或填写。进度只说明当前成果、需要选择的内容和实际阻塞项。

任务文件放到独立工作目录。用 `deck-spec.md` 保存内容稿、采用的需求、用户授权和当前进度；[规格模板](references/deck-spec-template.md)可按任务规模选用，保留实际信息，不机械填满无关栏目。恢复旧任务或修改已有交付时再读[变更与恢复](references/workflow-updates.md)。

## 1. 内容方案

读取 [Prompt 1A](references/prompts.md)、[内容深度](references/content-outline.md)与[密度规则](references/content-density.md)。论文、政策或长报告再按需读[材料审阅](references/material-reading.md)。

先明确受众需要理解的问题和整套回答，再写逐页内容：页面作用、结论、实际展示文案、证据/数据及必要解释。内容页按其用途安排信息密度；图表能表达的关系不重复堆正文。封面和过渡页按作用简化。

核对材料事实、推断、计算和建议，修正无支撑结论、错误口径、缺失关键解释及篇幅问题。来源不够时缩小结论或询问必要事实，不编造数据。地图、实验截图等证据按[证据素材](references/evidence-assets.md)决定保留原图或可靠数据重绘。

向用户展示整套叙事和逐页实际内容；长稿可分段呈现，不能只给标题表或文件链接。没有内容授权时在这里等待；已有对应授权时展示后继续。内容确定后再创建 Page Spec、风格图片和成品，不提前消耗生图调用。

## 2. 风格和图片版

读取 [Prompt 1B / 2](references/prompts.md)与[风格总览](references/style-options.md)。默认给四套使用相同内容的独立缩略图总览，让用户选择。沿用用户明确指定的模板，或按其明确的跳过/代选授权执行；已有选择不再询问。代选时仍生成四套并记录选择理由，跳过预览时记录 `skipped`。

总览使用任务指定页面比例；最多八页时展示全部，更多页时选同一组六至八个代表页。每套一次生图，保留方案编号。纯尺寸、网格或边距问题用 `build_style_overview.py` 修正；内容或视觉问题才重试生图。实际生成四套时运行 `validate_style_options.py` 并看图核对，只展示每套最新有效候选。

内容与风格确定后，按 [Page Spec](references/page-spec.md) 创建 `page-spec.json`，保留准确文案、数据、来源、稳定 ID、风格和授权。已有用户授权可直接记录为内容确认，不另索要固定口令。

```sh
python "<skill-dir>/slidemuse.py" validate "<work>/page-spec.json" --strict
```

按 [Prompt 2](references/prompts.md)逐页生成。用 [`produce`](references/page-production.md)归档原图、合成精确证据并记录逐页审阅；需要完整生成后端时再读[生成后端](references/generate-backend.md)。未记录在 Page Spec 的数据视觉不得装饰性添加。每页检查文字、数字、图表关系、可读性与整体风格，只返修有问题的页面。

同一文字或图表问题连续两次无效时停止同类生图重试，按 [Prompt 2A](references/prompts.md)或[图表可靠性](references/chart-reliability.md)使用允许的准确区域/文字兜底。程序改图遵守宿主工具的实际授权；未解决的问题不能自动标为通过。

合并图片版并实际渲染、查看结果：

```sh
python "<skill-dir>/scripts/build_image_ppt.py" "<work>/page-spec.json" "<work>/output/image-deck.pptx"
python "<skill-dir>/slidemuse.py" render "<work>/output/image-deck.pptx" "<work>/output/image-review" --page-spec "<work>/page-spec.json"
```

用户要求可编辑版时直接继续，否则交付。没有渲染器时说明仅完成结构验证，不声称视觉验收通过。

## 3. 按需还原可编辑版

读取 [Prompt 3](references/prompts.md)、[重建与分层](references/reconstruction.md)和 [Scene 协议](references/scene-format.md)。已有图片/PDF直接还原、复杂曲线/表格/公式、文字测量或逐页恢复需求，按需选择[完整重建后端](references/editable-backend.md)，保留其 Manifest，不混用 Scene 格式。

以 Page Spec 为语义来源、已批准页面为视觉基准。已知文字、数据、来源与稳定 ID 直接复用，不重新 OCR 或改写；只核验未确定项。用户已授权的差异记录后采用，不当作新冲突反复询问。

文字、简单形状、表格和有可靠数据的图表用原生对象；照片、人物及复杂插画用可独立移动的图片。从背景移除原生化文字和已拆主体，避免重影。整页截图不能充当可编辑底图。合并单元格和不等行高见[表格适配](references/upstream-editable.md)。

```sh
python "<skill-dir>/scripts/build_editable_ppt.py" "<work>/scene.json" "<work>/output/editable.pptx" --page-spec "<work>/page-spec.json"
python "<skill-dir>/slidemuse.py" audit "<work>/output/editable.pptx" --scene "<work>/scene.json" --output "<work>/output/editability.json"
python "<skill-dir>/slidemuse.py" render "<work>/output/editable.pptx" "<work>/output/editable-review" --page-spec "<work>/page-spec.json"
```

查看实际渲染，核对原生对象、文字、图表和背景；抽查用户需要的编辑操作。数据修改时同步相关占比、差额、结论和讲稿，[数据依赖](references/data-bindings.md)可辅助；依赖未声明时仍需实际核对。局部修改复用有效页面，保留原版与失败记录。讲稿需求见[演讲备注](references/speaker-notes.md)。

## 检查与交付

按任务范围验证，不把跨材料评测变成普通制作门槛：

- 普通制作：来源与内容核对、逐页看图、导出后真实渲染；可编辑版增加对象检查。
- 局部修改：核对受影响页、数据依赖和导出结果，复用仍有效的检查；不重新选风格或审查未变内容。
- 需要可复跑评分卡时才读[交付评测](references/evaluation.md)；跨材料质量比较时才读[多材料评测](references/benchmark.md)。保留原批次和首次/最终结果，不能把结构检查或样板复现称作生成质量提升。

自动保存已有工具产生的记录即可，不为每个小改动另造证据链或要求用户确认检查文件。完整新制作可用[制作日志](references/production-metrics.md)记录实际调用、返修与耗时；缺失历史标为未知。准备好规格后的自动编译/恢复见[流水线](references/pipeline.md)，集中人工查看见[审阅面板](references/review-panel.md)，溢出诊断见[文字布局](references/text-layout.md)。

交付时优先展示成品链接、一个有效预览和实际限制。图片版附有序图片及 Page Spec；Scene 重建附 Scene、素材和对象检查结果；完整后端附对应 Manifest、任务记录和预览。辅助文件保存在任务目录，无需逐项向用户解释。默认不重复嵌入工具已展示的图片、初稿或修复稿。保留原文件，写入失败时可恢复；不改旧封存记录来制造通过。

## 运行工具

统一入口为 `slidemuse.py`，详见[命令指南](docs/cli.md)。入口优先使用安装目录的 `.venv`；直接运行脚本时使用该环境或可用的 Python 3.10+。`doctor --json` 诊断环境，不能替代实际渲染。默认安装不携带 IRENA 演示，获取方式见[样板说明](docs/editable-sample.md)。

生图使用宿主实际提供的能力，[模型选择](references/models.md)按需读取；没有生图工具时报告阻塞，不用占位图冒充。基本 Scene 工具离线，外部 OCR/图像服务仅按用户所选后端和宿主规则使用，不寻找密钥或静默切换服务。复用已有风格库时读[风格库](references/style-library.md)。
