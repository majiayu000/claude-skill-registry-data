---
name: wally-static-asset-designer
description: Use only when the user explicitly requests wally-static-asset-designer or $wally-static-asset-designer by name. Plan, generate through ChatGPT Web in the in-app Browser, revise, archive, and review reusable static visual assets. Use for asset lists, regional_anchor, style_aesthetic, person-led Preview, Cxx, Cxx-Lxx, Gxx, CSxx, Pxx, Pxx-state, Sxx, multi-angle nine-grid and 2x2 four-grid references, or returned-asset review. Generate multiple distinct prompt-and-image candidates for user selection in named project chats; keep screenplay, storyboard, performance, dialogue, audio, and final video prompts outside this skill.
---

# Wally Static Asset Designer

规划静态资产，先用 Preview 选择全局视觉效果，再生成各项资产的候选版本，由用户逐项选择并归档。

Version: `wally-static-asset-designer@2026-09-29-v2.16-character-reference-sheets`

## 共用边界

- 接受剧本、文字、表格、图像、故事板、参考板、已有资产、部分材料和混合输入。只处理会影响当前产物的缺失与矛盾，不要求用户从固定起点重做。
- 保留剧本事实、整体调性与用户已确认的视觉约束。故事板只作为状态、构图、空间与道具的证据，不修改镜头序列。
- 有参考图时先看图，以图中可见事实为依据；缺少的必要依据明确指出，不凭空补齐。具体生产依赖由所选类型文件维护。
- 只交付用户点名的产品。完整流程仅在用户要求建立整套资产系统或完成全流程时运行；已有选定的 Preview 或基础资产直接继承。
- Preview 与自然效果图使用“整体风格＋构图描述”：保留图片类型与文化锚点；有视觉风格参考图时直接引用图片，省略风格词，没有参考图时才写关键视觉定义。先从剧本提炼要验证的表现目标，再选覆盖这些目标的一组代表画面；同轮各风格复用这一组。每张独立剧照简写前景、主体、背景。选帧与比较见 [preview.md](references/preview.md)，风格引用规则见 [style-aesthetic.md](references/style-aesthetic.md)，正文边界见 [craft.md](references/craft.md)。正式资产板式仍遵循对应类型合同；无风格参考图的单帧写法见[纪实摄影示例](examples/preview-documentary.md)。
- 不创作剧本、分镜、表演、对白、时序或声音，不编写视频提示词。

## 候选版本与选择

本节统一维护每轮候选包的最低数量，适用于提示词准备与对应图像生成：

| 产品 | 不同完整生成输入（正文与所需参考） | 独立图像版本 | 变化范围 |
| --- | --- | --- | --- |
| Preview 完整方向探索 | 至少 8 个风格方向，每个方向为同一组代表画面分别写完整输入 | 每个方向的每个代表画面至少 1 版 | 符合剧本整体调性的不同全局视觉风格方向。 |
| 每项静态资产，包括九宫格、四宫格 | 至少 4 套 | 至少 4 版 | 按类型合同继承已选图片类型与所需参考，在当前资产允许的范围内形成不同候选。 |

- Preview 分别记录风格方向与代表画面；同一风格的多张画面共同验证该方向，不能充作多个风格方向。正式资产的一套完整生成输入对应一个候选版本。各方向或版本须有可见、可解释的设计差异；采用不同风格参考时可以共用正文，但须记录并实际接入各自参考。重复输入、只改编号或依赖随机结果不构成不同方案。
- 用户看完整候选包后自行选择。Agent 负责说明差异、剧本调性适配和技术问题，不替用户选定，不把 `usable` 当成批准。
- 用户选定后记录版本与原图，依赖它的生产才能继续。批量执行授权只覆盖生成候选，不替代选图；用户明确指定采用已有版本时直接记录，不重复询问。
- 只做审查、解释或归档时不自动补生成候选包。用户针对一个候选要求技术修正时，只修该候选；新一轮方向探索才重新形成候选包。
- 用户限定单一风格、某个模型或某项表现验证时，按限定范围执行并记录为专项测试；完成该测试不等于完成全局风格选型。

## 默认执行方式

- 图片产物默认内部起草提示词，通过内置 Browser 操控 ChatGPT Web，生成、检查、下载并交付候选图，不要求用户搬运提示词。
- 用户要求提示词、查看或修改提示词时，仅交付相应文本；要求制作或生成图片时执行网页生成。
- 建立新一轮制作项目、项目与聊天命名、逐版提交、原图验收、重试和归档统一遵循 [browser-execution.md](references/browser-execution.md)。每项资产独立聊天，各版本在该资产聊天内依次生成。

## 按任务读取

只读当前任务对应文件；历史版本记录留在仓库 Changelog，不默认加载。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 资产规划与视觉边界 | [planning.md](references/planning.md)、[regional-anchor.md](references/regional-anchor.md)、[style-aesthetic.md](references/style-aesthetic.md)，使用 [方案模板](templates/visual-direction-proposal.md)；确认资产范围、剧本调性和不可变事实，风格方向留待 Preview 看图选择。 |
| Preview 候选与选定 | [preview.md](references/preview.md)、[craft.md](references/craft.md) 与 [Preview 模板](templates/preview-prompt.md)；要图时再读浏览器流程。 |
| 单项正式资产候选 | [contracts.md](references/contracts.md) 与所选 `types/<asset>.md`；类型对应关系见 planning，字段、几何和呈现按类型合同保留；要图时再读浏览器流程。 |
| 九宫格 / 四宫格候选 | 默认使用 [multi-angle.md](types/multi-angle.md)；用户直接要求或选择 fallback 时使用 [multi-angle-2x2.md](types/multi-angle-2x2.md)。基础地点须已选定；审查九宫格时不擅自追加或执行四宫格。 |
| 已有资产或候选审查 | [review-protocol.md](references/review-protocol.md) 和相关类型清单；Preview 还使用 preview 的调性与方向检查。 |

完整流程：资产范围与剧本调性 → Preview 候选 → 用户选择全局效果 → 各资产候选 → 用户逐项选择 → 按需制作依赖资产或多角度参考。一次产物是一项资产的一组可比较候选，不附重复设计报告。
