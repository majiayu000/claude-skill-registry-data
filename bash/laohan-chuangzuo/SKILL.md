---
name: laohan-chuangzuo
description: 统一创作引擎，负责创作口播初稿（不含封面提示词，封面由 laohan-fengmianqiuzhi 独立产出；不含选题搜索，选题由工作流①前置用 laohan-xuanti/laohan-douyinsousuo 出大纲后以大纲模式喂入）。支持录屏视频(音频提取→转录)、URL队列(抓取→整理)、结构化大纲、原始文本、自由主题五种输入。其他 skill 的写作环节统一调用本 skill。Use when 用户说"写口播稿""帮我写""录屏转口播""视频转口播稿""写一篇""根据链接改写""改写文档"。
version: "3.6.1"
---

# 统一创作引擎

所有涉及口播稿写作统一调用本 skill。一份方法论，一个入口。

## 核心理念

一份方法论、一个入口——所有写作走同一个管线，避免不同入口产出质量参差不齐。素材先整理（Layer A/B）再写稿，确保口播稿建立在结构化理解之上，而非对原始素材的直接改写。

内容长度由独立内容单位决定，不由预设字数或分钟数决定。内容重复与人味废话是两条不同的审计线：同一判断换词复述必须合并；结巴、语气词、自嘲、反问和停顿继续按风格保留，不能因去重被误删，也不能冒充内容增量。

## 不适用场景

- 纯文本摘要/总结 → 用 summarize skill，不走创作流程
- 翻译 → 直接翻译，不需要口播稿格式
- 学术论文/技术文档写作 → 输出格式是口播稿，不适合正式文档

## 知识来源（唯一正本，symlink 到 OpenClaw workspace）

- **写作规则**：`references/style.md`（恢复 2026-07-11 前实战版本）。其中开场、转场、修辞、标题公式、场景密度、节奏、口头禅和模板均为已验证的默认方法；允许按本题增删或扩充，但不得以“防模板化”为由整体降级成可有可无的抽象建议
- **整理方法**：`references/skill.md` → `~/.openclaw/workspace-reviewer/knowledge/skill.md`（进宝 skill.md v3.5）
- **转录方法**：`references/transcription.md`（音频提取 + 语音转文字三级降级）
- **转译选题法**：`references/yuanchuang-method.md`（转译选题法 + 角度库 + 标题公式 + 数据基准）。本 skill 不再自带热点搜索；此方法供工作流①前置阶段复用——①用 laohan-xuanti/laohan-douyinsousuo 出选题后，按本文件规则生成大纲再喂入本 skill 大纲模式
- **写作风格目录**：`references/styles/`（每份 .md 是一种写作结构框架，Step -1 强制选择）
- **创作机械合同**：`references/creation-contract.md`（Episode schema 4的选题/表达池绑定、内容单位、逐段审计、人味、自然时长、TTS与validator；独立模式兼容schema 3，历史采访合同仅对旧schema 3选题生效）
- **方法论真源**：项目`docs/老韩创作六步法.md`（定结构→选钩子三变体读选→铺内容含爆点分布/节奏锚点/情绪弧线→造记忆点含金句/评论区预设→HKRR自检→人味定稿+机械验收）；五波调研依据见`script-pool/口播稿方法论调研-2026-09-17.md`

GitHub 上是实体文件（拷贝），本地用 symlink 自动同步。

## 输入模式

| 模式 | 输入 | 触发场景 | 内部处理 |
|------|------|----------|---------|
| 大纲模式 | 结构化大纲文件 | 工作流①前置产出 / 外部传入 | 跳过整理，从 Step 2 开始 |
| 素材模式 | 原始文本/转录稿 | 录屏转录后、URL抓取后 | 先 Layer A/B 整理，再写稿 |
| 自由模式 | 主题关键词 或 无输入 | 用户直接调用 | 先生成大纲→确认→写稿 |

## 前置处理（将各种输入转化为三种模式）

### Pre-A：录屏预处理

触发：用户提供了视频文件（mp4/mov 等）或说"录屏转口播""视频转口播稿"。

1. **提取音频**：`ffmpeg -i "<视频路径>" -vn -acodec libmp3lame -q:a 2 "/tmp/录屏音频_$(date +%s).mp3" -y`
2. **语音转文字**：三级降级（详见 `references/transcription.md`）
   - 硅基流动 API（免费，秒级）→ whisper-cli（本地快）→ Python whisper（最准）
3. 独立写作时转录结果保存为 `output/transcript-YYYY-MM-DD.md`；Episode 模式保存为 `episodes/<slug>/02-创作工作稿/transcript.md`，自动进入**素材模式**。

### Pre-B：URL 队列预处理

触发：用户说"根据链接改写""链接内容改写""改写文档"。

1. **读取队列**：独立写作检查 `<cwd>/url.md`；Episode 模式只检查 `episodes/<slug>/02-创作工作稿/url.md`，找第一个 `- [ ]` 且后面有 URL 的行
   - 没有待处理 → 告诉用户"队列为空"，结束
2. **抓取内容**：根据平台自动选择方法（参考 laohan-xiazai 路由）
   - 抖音：移动端 UA → iesdouyin.com
   - B站：opencli bilibili
   - 其他：Jina Reader / agent-reach
3. 独立写作时内容保存为 `output/content-YYYY-MM-DD.md`；Episode 模式保存为 `episodes/<slug>/02-创作工作稿/content.md`，进入**素材模式**。
4. **完成后更新队列**：将 url.md 中对应行改为 `- [x] URL 关键词 ✅ YYYY-MM-DD`

## 环境检测

```
STYLE_FILE = 检测顺序：
  1. <当前工作目录>/templates/style.md      ← 用户定制版（优先）
  2. <skill安装目录>/references/style.md    ← 标准版（symlink 到 OpenClaw）

ACTIVE_STYLE_FILE = 通用风格时为 STYLE_FILE；教程型/其他风格时为 <skill安装目录>/references/styles/<选择>.md

ORGANIZE_FILE = <skill安装目录>/references/skill.md  ← 标准版（symlink 到 OpenClaw）

OUTPUT_DIR = 普通独立写作时 <当前工作目录>/output/；已验证系列单期资料包的独立草稿写入 <项目>/script-pool/<series-id>/；Episode 模式时 episodes/<slug>/02-创作工作稿/
```

## Episode 模式

当参数含 `--episode episodes/<slug>` 时，先读取 `00-选题.md` 和 `00-选题.json`，不得重新选择另一主题。2026-09-17起按五步法合同执行：直接从选题、`script-pool/Jeffrey个人表达池.md`（真实场景、亲历细节、固定表达素材）和系列研究摘录取材，写`02-创作工作稿/大纲.md`后直接写全文；不产生反向采访或大纲确认（历史episode的schema 3选题继续按其原采访合同验证）。最终定稿只能写 `episodes/<slug>/01-口播稿.md`，同时写 schema 4 `02-创作工作稿/创作决策.json`（绑定选题SHA、`expression_pool_usage`取材记录，钩子兑现①packaging_assessment承诺）。共享 `output/` 只允许用于非 workflow 的独立写作，不能作为 episode 输入或真值。

Episode schema 4 在原schema 3全部内容之外，至少增加：

- `topic_sha256`、`interview_sha256`、`outline_sha256`、`outline_approval_sha256`；
- 方向研究型选题必须读取`02-创作工作稿/系列研究摘录.json`，并在`research_source_contract`把全部内容单位映射到资料包claim或Jeffrey原创依据；
- `hook_contract.designed_after_outline_acceptance=true`并绑定确认时间；
- `contract_version=content-units-v2`。普通独立模式仍使用schema 3 / `content-units-v1`；已验证系列单期资料包使用`series-draft-v1`草稿合同，只能标记`DRAFT / NOT_STAGE_2_COMPLETE`。

原内容合同继续包含：

- 与①一致的 `topic_thesis`、`hypothesis_id`、`content_form`、`audience`、`expected_audience_effect`；
- `contract_version=content-units-v1`、`input_mode`、`active_style_file`、`active_style_sha256`、`structure_tool`、`structure_rationale`；
- 非空数组 `fact_boundary`、`alternative_structures`、`unproven_assumptions`；
- Step 3 的 `argument_plan`：`opening_contract`、`reasoning_path`、`material_tradeoffs`、`shootable_expression`、`originality_and_citations`；
- 至少一项 `original_contributions`，每项写清新增判断及其观众价值；只有一项时必须登记 `single_contribution_rationale`，证明没有为了数量硬凑第二个观点；
- `opening_contract` 登记 `mode: DEFAULT_SIGNATURE|TOPIC_SPECIFIC_HOOK`。默认使用“嘿，你有没有这种感觉，”，只有题目存在明显更强的具体结果、数字、动作、冲突或直问时才允许题目专属开场，并记录 `exception_reason`；两种模式的 `anchor_text` 都必须绑定第一段5秒内真实锚点；
- `visual_anchors` 至少一项，每项绑定一个内容单位，写清观众理解任务与可视化表达；它只给后续导演可拍依据，不规定动画技术；同时保留 `content_sufficiency`、唯一 `content_units`、覆盖全部口播段落SHA的 `paragraph_audit`、两遍 `semantic_redundancy_review`；
- `01-口播稿.md`正文只允许Jeffrey真正口播的文字，禁止B-Roll、字幕、镜头、转场、特效或Remotion执行提示；正文承诺模板、清单、提示词、命令或其他可复制资源时，必须独立写入`12-发布/观众资源/`，完整填写推荐值，并由`audience_resource_contract`绑定文件SHA及四平台交付方式；
- `human_voice_contract` 必须登记至少4种真实出现在稿件中的人味设备；`structure_contract` 在分层时绑定连续的 `1、2、3……`；
- `duration_contract.mode=CONTENT_DETERMINED`、`padding_for_duration=PROHIBITED`，并绑定本机 `say` 生成的TTS机械试读音频、SHA和 `ffprobe` 实测时长；TTS只用于检查5秒锚点、拗口句和自然时长，是可重建的内部QA代理，不是正式口播音轨，不进入视频或Remotion，也不能替代Jeffrey真人试拍后的节奏判断；
- `execution_steps` 逐项记录 `step_minus_1`、`step_0`、`step_2`—`step_7` 与新增`step_5_5`为 `COMPLETED`，不适用的 Pre-A/B、Step 1/1.5 写 `SKIPPED` 及理由；
- `quality_checks` 在原六关之外增加 `semantic_redundancy`、`human_voice`、`humanizer_zh`、`dynamic_duration`、`structure_clarity`，全部为 `PASS`，另有非空 `read_aloud_note`；
- 最终 `script_title`、`script_hash`、合法 `completed_at`。
- `publish_copy_contract` 必须绑定3个标题候选、唯一主推标题、选择理由、标题与介绍证据、视频介绍结构与SHA，以及每次必带的 `#AI新星计划`。
- Episode 模式还必须读取 `references/multi-platform-publish-contract.md`，在同一轮创作中输出 `12-发布/多平台发布内容.md`。抖音、视频号、小红书、哔哩哔哩的标题、介绍/正文和话题必须按平台受众分别创作，不能复制口播稿或复用一份文案；视频号独立短标题不超过16字；抖音、视频号、小红书话题固定包含 `#老韩AI`，哔哩哔哩标签固定包含 `老韩AI`。

字段和命令以 `references/creation-contract.md` 为准。Step 7 必须实际运行validator；Episode未出现 `PASS chuangzuo script contract schema=4` 时不得声称②完成。

任一改动改变 `01-口播稿.md` hash，都使②立即失效。错字或标点之外的实质改稿必须回 Step 3，重做规划、质量检查和试读，再写新的 schema 4 决策记录；不得只替换 hash。

## 执行清单（每步完成后打勾）

- [ ] Step -1: **风格选择（强制，不可跳过）**
- [ ] Pre-A/B: 前置处理（如需；Pre-C 热点转译已移除，搜索归工作流①）
- [ ] Step 0: 判断输入模式（大纲/素材/自由）
- [ ] Step 1: [素材模式] Layer A/B 整理
- [ ] Step 1.5: [Episode] 从选题+表达池取材生成大纲；[独立自由模式] 生成大纲→用户确认
- [ ] Step 2: 选题确认（模式A/B选择+主题锁定）
- [ ] Step 3: 规划（原版12项 + 内容单位/自然稿长/分层合同，不可跳过）
- [ ] Step 4: 写口播稿
- [ ] Step 5: 质量检查（6关）
- [ ] Step 5.5: humanizer-zh最终语言定稿与主张零增删改审计
- [ ] Step 6: 通过/重试
- [ ] Step 7: 输出口播初稿（封面提示词不在本 skill 范围，由独立 skill laohan-fengmianqiuzhi 在后续流程产出）
- [ ] Post-A: [可选] NotebookLM 幻灯片

---

## Step -1：风格选择（强制，不可跳过）

独立写作时在执行任何创作动作之前，必须让用户选择写作风格。不选择不执行。**Episode mode 例外**：先依据 `00-选题.md`/JSON 的受众、论点、干预和预期效果判断教程型或观点型，锁定 `ACTIVE_STYLE_FILE`，再用该文件选择结构工具；在 gate 真源 `02-创作工作稿/创作决策.json` 记录风格文件、选择理由、替代方案和待验证假设。Step 2 只复核该选择与大纲一致，不得重新选择。可同时写同名 `.md` 人类摘要，但它不代替 JSON。不得因等待风格选择而阻断已授权的 AUTONOMOUS_RUN。

执行方式：
1. 读取 `references/styles/` 目录下所有 `.md` 文件
2. 列出所有可用风格，格式如下：

```
请选择本次口播稿的写作风格：

1. 通用 — 观点型/热点评论/行业分析，使用 style.md 默认规则
2. 教程型（五层模型）— 工具教程/操作指南，使用完整五层结构、六要素、品牌层、结尾层和自检清单

请输入编号或名称。
```

3. **独立写作等待用户选择**。Episode mode 按上面的可追溯自主选择执行。
4. 用户选择后：
   - **通用**：直接使用 style.md 作为唯一规则，不加载额外风格文件
   - **教程型或其他**：读取对应的 `references/styles/<选择>.md` 作为自包含完整规则；不得只摘取其中的抽象结构而跳过语言、场景、节奏、品牌和自检方法
5. **默认不选**：没有"默认选项"，每次触发都必须选择。防止风格混用

**新增风格**：往 `references/styles/` 目录添加新 `.md` 文件即可，自动被发现。不需要修改本文件。

---

## Step 0：判断输入模式

检查输入参数：
- **大纲模式**：输入是 Markdown 文件，含 `## 核心论点` 或 `## 论证路径` 等大纲结构 → 跳到 Step 2
- **素材模式**：输入是长文本（转录稿/网页抓取内容），无大纲结构 → 执行 Step 1
- **自由模式**：无输入文件 或 只有主题关键词 → 执行 Step 1.5

## Step 1：素材模式 — Layer A/B 整理

读 `references/skill.md`（进宝 Layer A/B v3.5），对原始素材执行：

**Layer A（无损事实层）**：
1. 素材信息表（来源/标题/作者/日期/时长）
2. 黄金开局钩子（痛点场景+渴望结果+核心冲突）
3. 结构化模块（按逻辑拆分为独立模块，编号标注）
4. 断言台账（每个可验证的事实单独列出）

**Layer B（衍生加工层）**：
5. 可操作步骤提取（教程型素材必填，非教程型标注"不适用"）
6. 痛点映射（观众的真实痛点→素材能解决哪个）
7. 延伸思考（反常识发现、跨域连接、可执行收获）
8. 核心选题提炼（一句话主题+标题底子+裁剪建议）
9. 教程型质量预评分（模式A时执行，6维度打分）

独立写作时整理结果输出到 `output/organize-YYYY-MM-DD.md`；Episode 模式输出到 `episodes/<slug>/02-创作工作稿/organize.md`，进入 Step 2。

### Step 1 改写分支（对标爆款素材专用，2026-09-17生效）

素材是对标爆款视频的转录全文时（①已产出），Layer A/B 整理之后按改写管线执行，方法真源为项目`docs/老韩创作六步法.md`改写模式节（原创题不走改写分支，直接走标准六步法）：

1. **organize 是唯一内容来源**：Layer A 模块覆盖≥80%，信息密集型素材（经验指南/盘点/路径讲解）允许按源顺序展开；
2. **亲历内化**（Jeffrey 2026-09-17授权）：正文、介绍、四平台文案零第三方指代——不提原作者名/账号，不出现"博主/作者/视频里说/up主/那条视频"；对标素材全部内化为老韩第一人称亲历（晒单是自己的单、群是自己的群、学费是自己掏的），细节落地要很像；机械检查第三方指代词表零命中；
3. **增量是增补**：老韩自有判断≥2处作为增补，不替换源骨架主体；
4. **指纹脱敏**：与源稿指纹级相同的既定事实（人数×单价×工期组合、案例行业+痛点、行业清单、源稿独有措辞）换成相似但不同的值；并排比对不可通过事实组合锁定同源；正文/介绍/四平台同步并做机械残留检查；
5. **直读测试**（humanizer 后置）：逐句三问——指代能否在前句找到同类别对象、拟物动词（叫/响/漏/爬/断）有无本体铺垫、术语首现有无当句解释；无铺垫隐喻必须改为字面直白表述，词内误报人工判读保留；
6. 决策 JSON `rewrite_record` 登记 organize 绑定、覆盖率、亲历内化声明（含授权）、直读测试结果、指纹脱敏记录与被否版本演进链。

## Step 1.5：取材与大纲

Episode模式从三处取材后直接写`大纲.md`：①当前选题（thesis、tension、audience、packaging_assessment）；②`script-pool/Jeffrey个人表达池.md`中与题目相关的真实场景、亲历细节和固定表达（在决策JSON的`expression_pool_usage[]`登记`used/where`）；③`USER_DIRECTION_RESEARCH`时的系列研究摘录。反向采访与大纲确认门槛已于2026-09-17砍除；Jeffrey的修改意见在④—⑤或成稿反馈时吸收。

大纲成立后按`docs/老韩创作六步法.md`写全文，机械要求：
1. **定结构**：决策JSON登记`structure_type: TUTORIAL|EXPOSITION|STORY`（教程=问题-方案-演示-总结；科普=现象-原理-案例-升华；故事=问题-低谷-转折-结果-方法，留存最高的格式，亲历题优先）。
2. **钩子三变体**：先出3个不同方向的开头钩子登记`hook_variants[]`（各含text+direction），TTS读出声后选最自然的（登记`selected_hook_index`与`tts_selected: true`）；选中钩子必须兑现①`packaging_assessment.title_direction`的标题承诺（`hook_contract.fulfills_packaging_promise=true`）。
3. **铺内容**：内容单位制照旧；另登记`beat_distribution`（预计时长等分格子每格至少一个点的检查结论）、`rhythm_anchors[]`（每15—30秒一个正文级锚点：悬念/转折/提问/数字，供⑨导演，不进口播正文；`position`必须用「第N段」指到正文真实段落——段号越界或只写模糊位置会被合同判红，见 3.6.1 内容层交叉判据）、`emotion_arc`（开头痛点焦虑→中段认知释放→收尾踏实感三节点）。
4. **造记忆点**：登记`quote_anchor`（一句可被观众二创引用的金句，必须承载本期判断非鸡汤，放情绪高点或收尾前；**且必须是正文里真实出现的原句**——字幕/剪辑要按它取原文，validator 自 2026-09-30 起机械核对"逐字出现在口播段落里"，忽略标点与空白）与`comment_hook`（开头可埋问题悬念、真引导放情绪最高点、预期观众最想说什么；有上期评论素材时引用被问最多的问题做跨期钩子）。
5. **HKRR自检**：登记`hkrr_check`（快乐/知识/共鸣至少一项为true，rhythm必须true，附rationale）；不达标重排再写。

独立自由模式无素材时生成大纲：

无素材时，基于用户提供的主题（或交互询问）生成大纲：

```markdown
# [两句话标题，＜30字]

## 核心论点（一句话）
[全篇围绕这一个论点]

## 论证路径
1. [切入点]
2. [递进]
3. [收束]

## 关键素材/数据/场景
- [素材点1]
- [素材点2]

## 内容模式
[模式A 教程型 / 模式B 观点型]
```

独立写作时输出到 `output/outline-YYYY-MM-DD.md`；Episode 模式输出到 `episodes/<slug>/02-创作工作稿/outline.md`。展示确认后再进入 Step 2。

## Step 2：选题确认（动笔前必须完成，不可跳过）

1. **复核内容模式**：按下列信号确认 Step -1 已锁定的模式 A（教程型）或模式 B（观点型）及 `ACTIVE_STYLE_FILE`；若与①证据冲突，回 Step -1 重选并在决策 JSON 留痕
   - 选 A 信号：涉及具体工具/操作/配置/流程/对比测试
   - 选 B 信号：行业观点/新闻/深度思考/人物故事
2. **锁定主题**：大纲/整理结果中的一句话主题 = 全篇锚点，不准自换
3. **判断素材类型**：对照 `ACTIVE_STYLE_FILE` 内的素材适配规则；该文件没有专用表时，按 Step 1 的 Layer A/B 证据类型记录，不另外加载 style.md
4. **大纲自检**：Episode模式确认大纲覆盖选题thesis与tension，且钩子设计兑现packaging承诺
5. **（教程型专用）可操作步骤清单**：模式 A 时从素材中提取观众能跟着做的步骤

## Step 3：规划（不写稿，不可跳过）

以 Step 2 锁定的论点为锚，恢复原版12项规划。它们是经过实战验证的默认模板，可以在本题上增加，但无具体理由不得删除：

1. **一句话论点**
2. **内容模式 + 素材类型**
3. **教程型操作步骤规划**：步骤骨架，标注每步使用的真实素材或来源
4. **核心主题贯穿规划**：标题关键词和核心概念在正文中的落点
5. **精华筛选**：必须包含、选择性包含、跳过的内容与理由
   - 方向研究型选题先按单期资料包的claim和事实边界筛选；来源只提供事实与公共需求，不复制竞品标题、结构或整段表达
6. **场景规划**：至少1个核心生活场景、动作链和代入式互动点
7. **改写策略**：comprehensive（默认）/ angle / structure / depth
8. **目标读者、预期效果与待验证假设**：与①及 `创作决策.json` 一致
9. **技法选配**：骨架 #1—#4、反常识钩子、#15/#18/#19、横向对比及动态技法；若删去原版默认技法，记录具体原因
10. **结构错位方案**：原序与叙述序，避免照搬素材结构
11. **金句/比喻处理**：保留引用或替换；替换不得弱于原版冲击力
12. **增量点与事实边界**：通常规划2处以上独立判断；题目只有1个足够强且完整的原创判断时允许保留1处，但必须说明不硬凑第二项的理由。同时标清来源、待⑤核验主张和不能伪装成亲测的内容

原版12项完成后必须再产出三份硬结果，不能直接进入Step 4：

1. **内容充足度**：把热点或素材能支持的独立内容单位全部列出。每个单位必须包含新判断、支撑和观众价值；只有措辞不同的不算新单位。
2. **自然稿长决策**：热点短小但已经能形成完整判断时写 `KEEP_NATURAL_LENGTH`，允许短稿；只有找到新的机制、案例、反例、操作或边界才能写 `EXPANDED_WITH_NEW_UNITS`。禁止为了 `expected_duration_seconds`、`typical_duration_seconds` 或字数补同义段落。
3. **结构合同**：确有多个并列层级时，规划连续的 `1、2、3……`；没有真实层级时保持自然叙述，不为了形式拆段。
4. **发布文案策略**：从正文核心冲突中生成3个标题候选，登记标题公式和至少两条正文证据，再按明确理由只选1个主推标题。观点型/产品回归介绍按“观众问题 → 可信证据 → 核心内容 → 下一步 → 互动”规划；教程型按“观众问题 → 核心内容 → 实测或步骤证据 → 下一步 → 互动”规划，不能临时拼接与正文无关的卖点。
5. **可视化锚点**：至少选择1个最需要画面帮助理解的内容单位，写清观众要看懂什么，以及适合用对比、过程、因果、证据、真实场景或产品画面中的哪种表达；不在②指定Remotion技术。
6. **观众资源规划**：正文若承诺模板、清单、提示词、命令或其他可复制资源，规划一份独立完整资源。所有字段用可直接复制的推荐值填满，允许观众按自己的项目修改，但不得留下`[填写]`、`[粘贴]`、TODO、TBD或空字段；同时规划四平台实际交付位置。

## Step 4：写口播稿

按规划写稿。硬性要求：

- **开场默认与例外**：默认以“嘿，你有没有这种感觉，”开头。只有题目专属的具体结果、数字、动作、冲突或直问明显更强、更自然时，才可直接使用该钩子，并在 `opening_contract.exception_reason` 说明为什么；两种模式都必须在5秒内给真实锚点，不能用例外制造空泛标题党
- **停更/回归/产品开发题**：第一段强制使用 `ACTIVE_STYLE_FILE` 的“问题先行四问开场”，依次回答观众问题、停更动机、可信行动、产物定义；“做了一个”却不说明产品类别、目标用户和使用结果，Step 4 不通过
- 第一行 `# 标题`（≤30字，模式A「动词+工具/场景+结果」，模式B「主题句+情绪句」）
- 正文只写Jeffrey真正要说的话。禁止插入`[B-Roll]`、`[字幕]`、`[画面]`、镜头、转场、特效、Remotion包名、时长、位置或其他导演/实现提示；这些只能在`创作决策.json.visual_anchors`中保留抽象理解任务，并由后续导演阶段决定表达。
- 正文承诺观众资源时，只口播资源用途和取得位置；资源本体独立写入`12-发布/观众资源/<资源名>.md`，不能附在口播稿末尾。资源必须完整填写推荐值并提示“这是推荐起点，请按自己的项目判断并修改”。
- **抖音发布信息**：口播正文后固定追加 `## 抖音发布信息`，下设 `### 主推标题` 和 `### 视频介绍`。视频介绍末尾附与本题相关的标签，并且每次必须包含抖音活动标签 `#AI新星计划`；这一区域不进入口播、TTS、内容单位或段落审计
- **视频介绍SEO/GEO规则（2026-09-17）**：核心搜索词前置在前55字折叠线内（题材词+动作词）；介绍必须总结整篇骨架（案例/方法/增量/资源）不能只抓一点；关键词在标题/介绍前段/话题标签三处命中；实体词+一个真实互动问号（GEO利于AI搜索引用）；120—200字，只保留一个问号
- 严格执行 `ACTIVE_STYLE_FILE` 的完整方法；原版模板是默认基线，不因重复使用就自动判坏

**写稿时同步自检：**
- 关键节奏点尽量≤15字，短句比例以原版60%为默认目标；复杂事实边界允许长句
- 转场优先使用原版转场句式库，禁“首先/其次/最后”式说明书结构
- 标点：冒号→逗号，双引号→「」，「---」做句末停顿
- #19“是不是有点意思”按原版3—5次目标自然融入；若本题语气不适合可减少并记录原因
- 至少4种原版“废话感”元素，保持真人口播呼吸感
- 人味废话单独登记为 `VOICE_ONLY` 或具体人味设备；内容审计时排除它们，不能因为不增加事实就删除
- 每个内容段必须绑定至少一个内容单位并写清新增信息；同一判断只换词、没有新增支撑/例子/推论/操作/边界时直接合并
- 节奏按原版快慢交替：开头拉满→缓冲→加速→缓冲→结尾加速→减速

## Step 5：质量检查

**E. 内容底线（命中 = 不通过）：**
- 核心论点、关键证据和必要边界均已覆盖；素材覆盖度以原版≥80%为默认目标
- 有明确反常识论点或足够强的结果演示
- 结尾行动号召源自素材中的可执行精华
- 标题核心词在开场和关键结论自然出现；不设出现次数，不为记忆点复述同一内容
- 核心主题贯穿全文，无偏离段落
- 至少1个核心生活场景，并有代入式互动或动作链
- 全文至少有一句离开本期经历、判断或边界就不能成立的具体表达；纯中性说明书不通过
- 至少有一个内容单位被转成明确可视化锚点，说明画面承担的理解任务；只有“放大文字、变颜色”而没有内容关系的不算
- 字数与时长没有默认下限或为凑时长设置的目标；完稿后仅用本机TTS机械试读估算自然时长，不把它称为真人实测或正式音轨
- 两遍内容重复审计都必须通过：第一遍逐段检查新增内容单位，第二遍排除人味设备后检查同义判断；未解决的重复一律不通过

**E2. 教程型专用（模式 A 时执行）：**
- 有 ≥1 个明确操作步骤
- 有操作前后对比
- 标题含工具名+动作词
- 结尾恢复资源钩子、收藏引导、互动引导和行动式结尾；资源必须真实存在，不能虚构

**D. 原创性检查（命中 = 不通过）：**
- 老韩增量通常 ≥2 处；只有1处时必须是足够强且完整的原创判断，并登记不硬凑第二项的理由；无空泛总结
- 引用原话 ≤2 处，伪装成自己的 → 不通过
- 「我实测」类声明可溯源到素材

**A. 正则检查（命中 = 不通过）：**
- 模板连接词：首先/其次/总而言之/综上所述
- AI 填充：值得注意的是/毋庸置疑/显而易见
- 空洞大词：至关重要/开创性的/赋能/抓手/赛道（非比喻）
- 禁词：意味着什么|本质上|换句话说|不可否认|不难发现|作为一个|让我们|不妨|试想一下|值得一提的是

**B. 禁区检查**（禁用词+禁用标点+禁用结构，按 `ACTIVE_STYLE_FILE` 的自检规则）

**B2. AI味检查（命中 = 不通过）：**
- 体制化开头：不可否认/众所周知/在当今的时代/随着...的发展
- 空心强化：真正地/不得不说/坦率地说
- 三连排比：连续 3+ 相同句式
- 冒号堆砌：一段内 >3 个「：」后接列表
- 过度总结：由此可见/这充分说明/这告诉我们
- 假设复数："我们都知道"/"每个人都会"（应用"你"单数）

**C. 技法检查：**
- 骨架 #1—#4 全部体现
- 反常识钩子或结果演示构成全文核心吸引力
- #15 回环呼应：结尾照应开头
- #18 框架命名：使用时形成可复述名称
- #19 签名互动：“是不是有点意思”按3—5次目标检查
- 横向对比至少1次
- 技法总计以原版≥7条为默认目标
- 废话感以原版≥4种为默认目标
- 任何删减都写入 `创作决策.json`，说明为什么删后效果更好；没有证据时保留原版

**F. 发布文案检查：**
- 主推标题有3个候选、至少2条正文证据和非空选择理由，最终稿只保留选中的1个
- 标题承诺能被正文兑现；观点型突出可信证据与反常结果，教程型突出搜索词、动作和具体结果
- 视频介绍按当前内容类型完成五段信息结构，数字、功能和结果不超出正文事实边界
- 视频介绍只保留1个互动问题，并且标签原样包含 `#AI新星计划`

## Step 5.5：humanizer-zh 最终语言定稿（含通用直读测试）

humanizer-zh 十类模式扫描后，执行**直读测试**（所有稿通用，改写与原创都执行）：逐句三问——指代能否在前句找到同类别对象、拟物动词（叫/响/漏/爬/断）有无本体铺垫、术语首现有无当句解释；无铺垫隐喻和悬空指代改成字面直白表述，词内误报人工判读保留。humanizer测的是AI腔，直读测试补"人话但看不懂"的缺口。

内容、事实、结构、资源承诺和Step 5全部成立后，才执行本步骤。必须完整读取本机`~/.agents/skills/humanizer-zh/SKILL.md`，并先把尚未humanize的完整稿件保存为输入快照：Episode固定为`02-创作工作稿/humanizer-input.md`；普通独立正式稿使用同basename的`.humanizer-input.md`。系列资料包`series-draft-v1`仍是草稿，不执行本门。

本步骤只允许删除AI腔、调整口语、停顿、句长和节奏。禁止新增、删除或改变事实主张、个人经历、数字、日期、来源边界、产品能力、资源承诺、Jeffrey固定表达和内容单位。处理后必须：

1. 逐项对照全部`content_units[].id`，记录`audited_content_unit_ids`；
2. 确认`added_claims=[]`、`removed_claims=[]`、`changed_claims=[]`，任何非空都回Step 3处理，不能由humanizer直接决定；
3. 按`humanizer-zh`的直接性、节奏、信任度、真实感、精简度五项各10分评分，总分至少45；
4. 在`humanizer_contract`绑定Skill路径/SHA、输入快照路径/SHA、最终有效口播SHA、主张审计、评分和执行时间；
5. 从头朗读最终正文。后续任何实质改稿都必须重新保存输入快照、重跑本步骤，并重新生成TTS、稿件SHA、决策JSON和发布文案绑定。

`USER_PROVIDED_FINAL_SCRIPT_AND_RAW`是Jeffrey已确认并已录制的输入，不自动执行改写；只走其独立的recorded-input guard。

## Step 6：通过/重试

- ✅ 全部通过 → Step 7
- ❌ 不通过 → 第1次重试换角度，第2次重试换结构，仍不通过回 Step 3 重新规划（最多2轮）

## Step 7：输出口播初稿

1. 普通独立写作时口播稿写入 `output/script-YYYY-MM-DD.md`，并保留同basename`.humanizer-input.md`；传入已验证系列单期资料包时，口播草稿与同basename `.decision.json` 写入 `script-pool/<series-id>/`，不伪造humanizer正式门；Episode 模式写入 `episodes/<slug>/01-口播稿.md`并保留`02-创作工作稿/humanizer-input.md`。Episode正文承诺观众资源时，资源独立写入`episodes/<slug>/12-发布/观众资源/`，不得塞回口播稿。
2. 普通独立写作也必须写同basename的 `.decision.json` 和 `.tts.aiff`；系列资料包草稿不得伪造TTS或正式完成证据，使用`series-draft-v1`并绑定packet SHA；Episode 模式写 `02-创作工作稿/创作决策.json` 与 `tts-read-aloud.aiff`。
3. 用本机 `say` 完整机械试读并用 `ffprobe` 记录TTS音频时长；TTS音频、正文有效口播文本和决策JSON必须互相绑定SHA，但该时长只能作为口播时长估算，不能称为真人实测。
4. 在正文后写入非口播的抖音发布信息，主推标题和视频介绍都必须非空，视频介绍必须带 `#AI新星计划`。
5. Episode 模式按 `references/multi-platform-publish-contract.md` 同步写 `12-发布/多平台发布内容.md`；四个平台分别选择切入点、标题、介绍/正文和话题，视频号独立短标题不超过16字，所有事实仍受当前口播稿与审核边界约束；三端话题必须带 `#老韩AI`，B站标签必须带 `老韩AI`。存在观众资源时，四个平台还必须绑定同一资源并登记实际交付位置。
6. 按 `references/creation-contract.md` 运行 `scripts/check-script-contract.mjs`。系列资料包草稿使用`--series-draft <packet.json>`；没有对应机械PASS不得交付，即使PASS也只算草稿，不算②完成。

❌ 差：用户否掉旧稿后直接重写 `01-口播稿.md`，沿用旧决策和旧质量结论。

✅ 好：实质改稿回到 Step 3，重新说明论证、取舍、可拍表达和原创增量，跑完六关与试读，再用新 hash 封口。

> 封面提示词不在本 skill 范围。chuangzuo 的职责止于「确定来源 + 创作口播初稿」。封面由独立 skill `laohan-fengmianqiuzhi` 在后续流程（违规检查、校准评分通过、标题锁定后）单独产出。

---

## Post-A：NotebookLM 幻灯片（可选，用户要求时执行）

用户要求生成幻灯片时，基于 script.md 用 NotebookLM 生成 PNG 图片：

1. `mkdir -p <script.md所在目录>/slides`
2. `cp script.md <script.md所在目录>/slides/script.md`
3. `nlm notebook create "<标题>PPT"`
4. `nlm source add NOTEBOOK_ID --file <script.md所在目录>/slides/script.md`
5. `echo "y" | nlm slides create NOTEBOOK_ID --language zh-CN --length default`
6. 轮询等待 completed（30秒间隔，最多20轮）
7. `nlm download slide-deck --notebook NOTEBOOK_ID -o <script.md所在目录>/slides/<标题>.pdf`
8. `pdftoppm -png -r 200 <script.md所在目录>/slides/<标题>.pdf <script.md所在目录>/slides/slide`

输出到 `<script.md所在目录>/slides/slide-*.png`

依赖：nlm CLI v0.5.25 + poppler

## 输出路径

```
output/
├── transcript-YYYY-MM-DD.md    ← Pre-A 录屏转录结果
├── content-YYYY-MM-DD.md       ← Pre-B URL 抓取内容
├── organize-YYYY-MM-DD.md      ← Step 1 整理结果（素材模式）
├── outline-YYYY-MM-DD.md       ← Step 1.5 大纲（自由模式/热点模式）
├── script-YYYY-MM-DD.md        ← Step 7 口播初稿（本 skill 唯一终产物）
├── script-YYYY-MM-DD.decision.json ← schema 3创作执行证据
├── script-YYYY-MM-DD.tts.aiff  ← 本机实际试读证据
└── (cover-prompts 不在此产出，由 laohan-fengmianqiuzhi 独立 skill 后续生成)
```

如果 `output/` 不存在，自动创建。

Episode 模式的完整中间产物固定为：

```
episodes/<slug>/
├── 01-口播稿.md
├── 12-发布/
│   ├── 多平台发布内容.md
│   └── 观众资源/             ← 仅正文承诺资源时生成；完整推荐值，无空白占位
└── 02-创作工作稿/
　 ├── 创作决策.json
　 ├── 创作决策.md       ← 可选人类摘要
　 ├── humanizer-input.md ← 最终语言定稿前的完整稿件快照
　 ├── tts-read-aloud.aiff ← 本机实际试读证据
    ├── transcript.md
    ├── content.md
    ├── organize.md
    └── outline.md
```

Episode 模式禁止读取或写入共享 `output/`。

## 依赖

| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| ffmpeg | 音频提取（Pre-A） | `brew install ffmpeg` |
| 硅基流动 API Key | 语音转文字（Pre-A，优先） | 注册 siliconflow.cn |
| whisper.cpp | 本地语音转文字（Pre-A，备选） | `brew install whisper.cpp` |
| nlm CLI + poppler | NotebookLM 幻灯片（Post-A） | `pip install notebooklm-mcp-cli && brew install poppler` |

Pre-A/B 按需依赖，不使用对应模式时无需安装。

## 触发方式

```bash
# 录屏模式（传入视频文件）
/laohan-chuangzuo /path/to/recording.mp4
"把这个录屏视频转成口播稿"

# URL 队列模式
"根据链接改写""链接内容改写""改写文档"

# 大纲模式（传入大纲文件；选题搜索归工作流①）
/laohan-chuangzuo output/outline-YYYY-MM-DD.md

# Episode 模式（00-选题已锁定）
/laohan-chuangzuo --episode episodes/<slug>

# 素材模式（传入原始文本文件）
/laohan-chuangzuo output/transcript.md
/laohan-chuangzuo output/content.md

# 自由模式（直接触发或给主题）
/laohan-chuangzuo
/laohan-chuangzuo "Claude Code 配置技巧"
"帮我写""写口播稿"
```

## 注意事项

- style.md 和教程型风格文件是经过实战验证的默认方法论，不是仅供参考的候选摘要。Episode 合同只能增加真源、事实和落盘约束，不能覆盖或删除其创作方法
- **风格文件**（`references/styles/`）是完全自包含的写作规范，每次创作前必须选择一个风格。通用模式无额外文件，直接用 style.md；其他模式只读对应风格文件
- skill.md 是唯一的整理方法来源，Layer A/B 规则以该文件为准
- 转译选题法详见 `references/yuanchuang-method.md`（转译案例+角度库+标题公式+数据基准）。本 skill 不自带热点搜索；该文件供工作流①前置阶段复用
- 转录技术详见 `references/transcription.md`（音频提取+三级降级）
- 二创脱敏规则（style.md 第十节）：素材来自他人内容时执行；自由模式（原创主题）跳过
- 本 skill 不负责选题搜索（那是工作流①阶段的职责，用 laohan-xuanti + laohan-douyinsousuo 出大纲后喂入）
- 本 skill 不负责平台特定下载（那是 laohan-xiazai 的职责）
