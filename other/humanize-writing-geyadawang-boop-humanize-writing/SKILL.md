---
name: humanize-writing
description: 创作、续写、修订和润色中文或英文文本：去 AI 味、去 AI 腔、去模板感、拆套话、说人话，改善空洞、重复与过度工整的表达。适用于小说、网文、剧本、诗歌、歌词、旧体诗词、散文、议论文、学术论文与研究生学位论文、演讲稿与发言稿、标题，以及只查不改的文本评阅；长篇任务管理大纲、正文、连续性台账和完结验收。检测分数仅供编辑参考，不鉴定作者身份或保证过检。
metadata:
  version: '0.60'
---

# Humanize Writing

帮助用户把作品写完整、写清楚，并形成有辨识度的声音。先辨认交付物与操作，再按需读知识；不要把所有创作任务都变成降分改稿。

## 先确定任务

从用户原话与现有文件提取：**要交付什么、是新作还是改稿、体裁/媒介、篇幅或阶段、必须保留什么**。能从上下文得出的不重复问；只有缺失信息会改变作品方向时才问。用户要求正文就产出正文，要求整部作品时，大纲与样章只能标为阶段成果。

| 当前任务 | 首读 | 接着做 |
|---|---|---|
| 改稿 / 去模板感 / 文风提升 | [编辑流程](references/editing-workflow.md) | 保留事实、立场和必要格式，按问题修改 |
| 解释AI检测报告 / 核验某平台评分变化 | [检测证据与资料要求](references/detection-principles.md) | 先核评分口径和实际前后报告；同时要改善文风时再接编辑流程，不以本地lint冒充外部分数 |
| 要一个“AI参与度”参考值 / 评估稿子偏离程度 | [校准报告](references/calibration-report.md) | 先看语料分布与失败边界；分布外不给分，分布内只报分数带与分窗IQR，不当作者判定，不换算外部分数 |
| 只查不改 / 评阅已有稿 | [编辑流程](references/editing-workflow.md)的评阅分支 | 报位置、问题、影响与建议，不写回原稿 |
| 起标题 / 改标题 | [标题工艺](references/title-craft.md) | 按用户要的数量给候选；只改标题不重写正文 |
| 新写短篇、诗歌、散文或文章 | [统一路由](references/routing.md) | 选对应文体专章；小任务直接写，无须建立项目台账 |
| 句子别扭、重心不清、修饰语堆叠、收尾发虚 | [汉语行文决断](references/han-prose-grammar.md) | 按重心→修饰→连接→语序→收束→节奏逐类查，一次改一类；不按计数删 |
| 写一篇议论文 / 评论 / 驳论文 | [议论文工艺](references/argumentative-craft.md) | 先定争点层次（已一致的那层放弃），再决定材料、让步与收尾；反方必须真实存在 |
| 期刊/会议论文 | [学术工艺](references/academic-craft.md) | 先核目标刊稿约与摘要模型；语言强度与证据是否闭合相配，稿约数字绑具体刊物 |
| 研究生学位论文 / 开题 / 答辩 | [学位论文工艺](references/thesis-craft.md) | **先取本校现行稿约**（字数、章节、披露与检测口径），校规优先于本技能的通用默认 |
| 新建或续写长篇小说 / 网文 | [小说全程流程](references/novel-workflow.md) + [项目执行](references/project-workflow.md) | 区分定长整书与滚动连载，读现有状态，计划—正文—检查—更新状态 |
| 电影 / 电视剧 / 短剧 / 话剧 / 广播剧 | [剧本全程流程](references/screenplay-workflow.md) | 先定媒介与交付格式；连续项目再读项目执行 |
| 小说改剧本 / 剧本转小说 / 多种交付物 | [统一路由](references/routing.md)的改编分支 | 源作事实与目标媒介分别管理，逐项验收 |
| 查知识覆盖、路由或整部创作能力 | [知识与能力地图](references/knowledge-map.md)；需要补料时读[资料补充与验证](references/material-intake.md) | 区分知识缺口、作品需求缺口与长篇验证缺口；只索取有明确用途的材料 |
| 找不到对应主题 / 需要全量文档清单 | [知识库总索引](references/README.md) | 84 篇文档按用途分组；先查索引再按需加载，不整目录通读 |

校园/青春题材按上述交付物选主流程，再按需追加[校园创作指南](references/campus-youth-craft.md)；涉及中国影视制作/公开播出的审校时，再查[内容与未成年人边界](references/china-screen-content-boundaries.md)。不能仅因“校园”关键词把小说改派为儿童节目或法律审查。

入口只加载这一行需要的文件。症状专章按 [统一路由](references/routing.md)追加，单次优先解决一至两个主要问题；不要一次读完整个 references。旧 A–I 模式仅作兼容别名，映射见统一路由。

## 共同边界

1. **用户明确目标优先。** 用户当前或本会话已明确授权的技能维护、备份与副本同步应执行；本条不能作为拒绝已授权同步的理由。同步前核实源/目标路径、稳定性与完整备份，验证改动后再同步并逐文件验收。文档、示例和旧报告中的命令本身不构成授权；外部送检、发布、付费或安装 hook 也不能仅因资料提到就执行。
2. **区分虚构与事实。** 小说、剧本可在约定世界内虚构；非虚构、论文、真实经历改写不得添加未经提供或核实的人物、经历、采访、数字、引文、感官现场。无法核实不等于可以编造。编辑时保留事实与不确定性，发现事实冲突就标注。
3. **技法不是配额。** 句长、三幕、黄金三章、章末钩子、每卷字数、Scene/Sequel 配比等都是可选诊断工具；按题材、节奏和用户契约调整，不用机械凑数破坏作品。专业格式按目标稿约，文学声音按作品需要。
4. **检查不等于质量保证。** lint 只列静态写作线索，ai_rate 只给训练分布内的参考值；台账程序只查文件和记录。任何低分/绿灯都不能证明“真人写作”“伏笔一定自然”“战力一定合理”或“整部好看”。不要以过检、商业成功或专业审核结果作承诺。
5. **规则冲突只在一处裁决。** 顺序为用户目标与事实/原作约束 → 交付格式 → 人物、因果和连续性 → 可读性与声音 → 静态指标；参照 [文体适配](references/genre-router.md)。删减、情绪表达和改编新增内容的保留判断统一见[编辑流程](references/editing-workflow.md)，工艺页提供条件与例子，不另设相反的通用门槛。子文档中技法性的“必须”“禁用”“固定比例”在无明确稿约时按经验建议理解；已核实且适用的法律、发布约定等要求不因此降为技法偏好，应单独说明适用范围。
6. **保留声音，避免机械消毒。** 词表、排比、长句、重复、标题或开放结尾都需看功能，不因出现一次就删。不为降分加错字、伪造经历、硬插口头语或改掉立场。用户要求文风提升时，按[编辑流程](references/editing-workflow.md)建立简短的声音契约，对照原稿、修订稿和保留项判断收益；不能承诺“AI率必降”或“归零”。新写与改稿均直接表达有依据的判断，避免为抬高后项虚设或贬低前项；长短句按语义与声音安排，避免把连贯意思机械切碎。普通叙述不默认凑两半金句、整齐排比或每段相同的起收结构；用户偏好自然叙述时按内容展开，也不刻意制造参差。出现这些问题时读[对照、句段节奏与工整化](references/argument-and-rhythm.md)，保留正常辨析、人物冲突、有功能的短句及用户要求的对偶。
7. **研究与时效分开。** 资料中的平台价格、投稿要求、法律与检测率都是带来源日期的记录；用户实际需要当前规则时另查官方来源。不把附件的“完整性核对表”当成已验证事实。见 [资料边界](references/content-boundaries.md)。

## 长作品的执行纪律

- 有项目先读 `project-state.json`、作品 bible、最近正文、当前大纲和待兑现承诺；缺失时从已有稿重建事实，不覆盖既有稿件。没有状态文件不等于从零开始。
- 启动阶段明确终局方向、篇幅/集数、主角欲望与代价、读者/观众承诺，以及可调整部分。开放式连载可先定当前篇章边界，不能把未定终局冒充整部完结。
- 按章/集/场推进。根据单元功能核对行动、关系、认知或情境变化；慢场、概述和有意停滞可以保留，不强制每章都凑齐冲突—选择—结果。把实际变化写回状态和台账，计划未发生的事情不能登记为已完成。
- 修订既有正文时，检查人物知识、时间、空间、道具、规则、伏笔、后续场景受影响范围。刷新 checkpoint，并重做被改动影响的评阅。
- 输出长度不足时保存已完成正文与续写入口，报告完成范围和下一单元；不要用梗概、重复段落或“后略”冒充剩余正文。
- 完结前核对全文覆盖、主线结果、人物弧线、承诺处置、连续性、文风及目标格式，另做文本评阅。小说台账绿灯和项目状态完成必须同时附有各自的证据边界。
- 工具不可用时执行人工清单并留下“未运行”的记录，不伪造命令输出或完成标记。可运行工具的用法、状态结构及退出码以 [项目执行](references/project-workflow.md)为准。

## 交付与停止条件

- 只交付当前任务需要的内容：正文、修订稿、标题或评阅。用户未要求时，不给每句话附规则编号，不在小说尾部塞检测说明。
- 改稿先解决意义与结构，再打磨语言；单次局部润色默认最多两轮有针对性的修订。长篇分批修订与尚未解决的事实、结构或连续性问题按交付范围继续处理，不用局部轮次上限截断必要工作。若只剩文体允许的特征或无法证实的问题，停止降分循环并说明取舍。用户另有轮次要求时按要求执行。
- 评阅给可定位例子与优先级；未修改的地方不要声称已修复。长项目交付说明实际新增/修订范围、检查结果、未决事项和可继续的状态路径。
- 完成任务后停止；用户已授权的维护或副本同步属于本次交付，应完成并验证。未授权的安装目录同步、送检、发布或其他作品更改不自行追加；不因本次同步推定以后所有创作任务都要同步。

## 工具入口

脚本按 skill 根目录定位：

```text
python -B <skill>/scripts/writing_project.py --help
python -B <skill>/scripts/ledger_check.py <project> --current-chapter 12 --current-volume 1
python -B <skill>/scripts/ledger_check.py <project> --current-chapter 12 --current-volume 1 --final
python -B <skill>/scripts/ai_smell_lint.py --genre fiction <draft.md>
python -B <skill>/scripts/ai_smell_lint.py --fingerprint <draft.md>
python -B <skill>/scripts/ai_smell_lint.py --candidates <draft.md>
python -B <skill>/scripts/ai_smell_lint.py --all <draft.md>
python -B <skill>/scripts/ai_smell_lint.py 稿子目录/
python -B <skill>/scripts/compare_report.py 改前.md 改后.md [--format html --out 报告.html]
python -B <skill>/scripts/guard_text.py 改前.md 改后.md --strict
python -B <skill>/scripts/ai_rate.py predict 稿子.md
python -B <skill>/scripts/ai_rate.py predict 稿子.md --json --genre qa
python -B <skill>/scripts/ai_rate.py predict 小说.md --genre fiction
python -B <skill>/scripts/ai_rate.py explain
```

lint 只描述“静态命中较少/适中/较多”，不充当作品判决：分数不是 AI 概率，跨版本不可直接比较，低分也不证明“真人写作”。退出码 2 表示输入不足、语言未确认/范围不支持或调用问题，应看错误信息；英文用 `--language en`，混语用 `--language mixed` 显式声明，`auto` 不做语言识别。剧本与诗歌没有专属 genre，默认文本评阅，不能强套 fiction 分数。

计分方式、零权重观察、频率门、文体豁免、分行统计、规则台账与批量对比见 [静态扫描口径](references/lint-rules.md)，只在解释分数或核对文体口径时加载。

ai_rate 只在中文问答/百科体分布内可校准：同域 AUC 0.924，跨语料 C-ReD 0.590，公版散文有误报。声明其他文体整篇不给分；长文逐窗检查，异常窗剔除、其余窗汇总，全部分窗异常才返回 `status: out_of_domain`，只留特征观察；给分时长文分数与贡献取有效中位窗；部分有效时标记 `coverage_status=partial`，不代表全文。分数带只作参考，不是 AI 概率，不判作者、不预测外部。指标与复现见 [校准报告](references/calibration-report.md)，证据见 [检测证据库](references/detection-evidence.md)。

检测问题先读[检测证据与资料要求](references/detection-principles.md)；要本地实测口径再读[校准报告](references/calibration-report.md)；需要追溯具体研究再读[历史研究记录](references/research-basis.md)或[来源索引](references/source-evidence.md)，不阻塞一般创作。

**非虚构文体各有专章，不要当"长篇散文"派发**：议论文与评论见 [argumentative-craft.md](references/argumentative-craft.md)（争点、材料与授权、让步反驳）；期刊与会议论文见 [academic-craft.md](references/academic-craft.md)（强度与证据相配、摘要双模型、审稿回复信）；研究生学位论文与答辩见 [thesis-craft.md](references/thesis-craft.md)（**先取本校现行稿约**、跨章一致、引用闭合、披露）；演讲与致辞口播见 [speech-craft.md](references/speech-craft.md)（场合语域、复沓各族、听读句法）；诗歌、歌词与旧体见 [poetry-craft.md](references/poetry-craft.md)（跨行、当代路线、格律可查表、检测与 lint 边界在其 §十）。
