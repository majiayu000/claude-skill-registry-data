---
name: rulai-distill
description: |
  蒸馏工厂：把书籍/长视频/播客/访谈/人物素材蒸馏成可执行、可验证、可追溯的 Agent Skills。
  融合 RIA-TV++ 七阶段管线（cangjie）+ FIDELITY 独立双 Agent 出厂质检（nuwa）+ 认知植入结构（yeadon）
  + 跨模型异族复评（DeepSeek：8/8 一致、重申 A、无编造，组织独立台账 docs/independent-recheck/ 可查）。
  出厂质检是**机器强制**的：validate / verify-quotes / anchor / lint-quotes / gate 五道门禁，不过不发版；
  83 个自身缺陷公开登记在 CONSTRAINTS.md，台账行数/分布/回归项数由测试强制相等（写错即 CI 红）。
  触发词：「蒸馏」「拆书」「拆解这本书」「做成 skill」「提取方法论」「提取思维方式」「人物思维 Skill」「book to skill」「distill」「extract methodology」。
  English triggers: "distill this book", "turn this into skills", "extract methodology", "persona skill", "cognitive implant".
  不做：书摘、读后感、单纯摘要、作者语气模仿。
license: MIT
compatibility: >-
  Needs Python >= 3.10 and git. Optional extras (auto-degrades when absent):
  PyYAML, tiktoken, jsonschema, yt-dlp (only fetch-subtitle touches the network).
  Runs fully offline otherwise. Follows the open Agent Skills spec, so it loads in
  Claude Code, Codex CLI, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Hermes, WorkBuddy.
metadata:
  version: "1.11.1"
  lineage: "cangjie-skill(2.5.0) 全套工程能力 + nuwa-skill FIDELITY/字幕/六路调研 + yeadon 认知植入/prompt 编译"
  license: MIT
---

# rulai-distill · 蒸馏工厂

> 输入是内容，输出是**可执行 + 可验证 + 可追溯**的技能资产。

## 核心承诺

大多数蒸馏技能只解决"生成"，不解决"证明"。本技能把**出厂质检**写进流水线：
**不双 Agent 测过就不发版，不由自己给自己打分。**

方法论骨架来自 cangjie（七阶段 / 三重验证 / 晋级门 / 原子发布），
出厂质检来自 nuwa（FIDELITY 五维百分制 + 盲测），
人物分支来自 yeadon（认知植入结构 + 禁用显式步骤），
音视频与调研管线同样来自 nuwa。细节分工见 `README.md` 第二节。

---

## 何时用、何时不用

**适用**：
- 「把《XX》蒸馏成可调用的方法论技能」
- 「这个长视频的核心方法论做成 skill」
- 「蒸馏某人的思维方式，生成思维顾问」
- 「我读了很多书但用不出来，想变成能触发的技能」

**不适用**：
- 书摘 / 读后感 / 内容摘要 → 直接让模型总结即可
- 作者语气模仿 / 角色扮演 → 用 nuwa-skill
- 单个知识点查询 → 直接问模型

**边界自检**：如果你的需求是"知道这本书讲了什么"，本技能是过度设计；如果是"让 Agent 在具体场景里能用上其中的判断方法"，本技能才对口。

---

## 执行流程（七阶段）

### 阶段 0 · 整内容理解（Adler 分析）

**素材预处理（超过 5 万字或素材是音视频时必做）**

```bash
# 长文 / 书籍
python3 scripts/td.py chunk book.md --max-chars 4000     # 结构分块 + 索引 + 缓存
python3 scripts/td.py index book.md.td --grep "关键词"    # 只取相关块，别整本灌入

# 视频 / 播客 / 访谈
python3 scripts/td.py fetch-subtitle <URL> --out subs/          # 默认 dry-run，加 --execute 才联网
python3 scripts/td.py transcript subs/<id>.srt                  # → 逐字稿
python3 scripts/td.py chunk <逐字稿>.md --source-id transcript
```

> 字幕获取是本包**唯一联网**的命令，默认只打印不执行。已有本地字幕 / ffmpeg 转写 /
> ASR 工具的，见 `references/media-pipeline.md` 3.1。

读全内容，产出 `BOOK_OVERVIEW.md`：作者身份与立场、结构骨架、核心论点、隐含假设、适用边界。

**为什么必须先做**：跳过这一步直接提取，产出的是"看起来像方法论的书摘"。先建立全局认知图，才能判断某个片段是"方法论"还是"作者在某情境下的临时表述"。

详见 `methodology/00-overview.md` 与 `references/media-pipeline.md`。

### 阶段 1 · 五路并行提取

五个提取器**并行**分发给不同 Agent，产出候选单元池：

| 提取器 | 产出 | 文件 |
|---|---|---|
| 框架 | 可复用的思维模型 / 分析框架 | `extractors/framework-extractor.md` |
| 原则 | 带条件的判断规则 | `extractors/principle-extractor.md` |
| 案例 | 具体到可类比的历史/业务案例 | `extractors/case-extractor.md` |
| 反例 | 失败模式、误用边界 | `extractors/counter-example-extractor.md` |
| 术语 | 专有名词与语境定义 | `extractors/glossary-extractor.md` |

**给每个子 Agent 的输入必须是最小相关的**：用 `td.py index <sidecar> --grep "<维度关键词>"`
拿到相关块的原文，而不是把整本材料塞进五个 Agent 的上下文——那是 5 倍浪费。

> 素材是**人物**时（书名换成人名），额外触发 `extractors/persona-extractor.md`，
> 并先跑六路调研：`td.py research init` → 填 6 个车道 → `td.py research merge`（去重 + 冲突标记 + 一手占比）。见 §人物蒸馏分支。

### 阶段 1.5 · 三重验证

每个候选单元过三关，详见 `methodology/02-triple-verify.md`：

1. **来源充分性**：原文是否有支撑？能否定位到具体段落？孤证 vs 反复论述
2. **可执行性**：能否转成"在什么场景下做什么"？纯观点不可执行
3. **任务效用**：真实场景会用得上吗？还是"听起来正确"的废话

**关键放宽规则**（来自 cangjie 的重要洞察）：一个**完整讲透一次**的流程或公式即可通过，**不要求作者反复论述**，也不要求是作者原创。这大幅降低了"必须找到 N 处佐证"的误杀率。

### 阶段 1.6 · 晋级门

判断这个能力是否值得成为**独立可触发技能**，还是只做卡片挂在路由入口下：

| 晋级条件 | 说明 |
|---|---|
| `independent_intent` | 有独立的用户意图，不是别的能力的附属 |
| `independent_contract` | 有自己的输入输出边界，能单独成立 |
| `independent_run` | 能独立执行，不依赖其他能力先跑 |
| `independent_reuse` | 会在多个不同场景反复用到 |
| `independent_eval` | 能构造出可机械判分的测试用例 |

五项全绿 → `promoted`（独立 Skill）；否则 → `router`（卡片 + 路由表）。

详见 `methodology/03-promotion-gate.md`。

### 阶段 2 · RIA++ 能力构造

每个通过验证的单元构造为能力卡，**六段结构**（RIA + Agent 扩展 E/B）：

```
R  Reading       原文/原始表述（带出处与定位）
I  Interpretation 方法论骨架：核心逻辑、适用前提
A1 Past          内容中的真实应用案例
A2 Future        用户会在什么情境下需要它 + 语言信号
E  Execution     可执行步骤（每步带完成标准与检查点）
B  Boundary      不适用情况 + 失败模式 + 易混淆辨析
```

**E 段是本技能与"书摘"的分界线**：必须写成"在什么场景 → 按什么步骤 → 做到什么算完成"。写不出完成标准的候选单元，说明还没想清楚，不予通过。

模板：`templates/CAPABILITY.md.template`

### 阶段 3 · Zettelkasten 链接

建立能力图谱，三种关系：

- `depends-on`：A 是 B 的前置（如"主要矛盾识别"依赖"矛盾分析法"）
- `composes-with`：A + B 组合解决完整问题（如"矛盾分析"+"矛盾转化" = 完整的"现在→未来"判断）
- `contrasts-with`：A 与 B 容易混，需显式辨析（如"矛盾分析法用于结构" vs "阶级分析法用于人"）

**易混淆辨析是最高价值的一段**。同一本书拆出 10+ 技能后，最大的真实故障是互相抢调用。显式写清"什么时候用 A 而不是 B"，比多写几百字方法论更能提升实际效果。

### 阶段 4 · 压力测试 + FIDELITY 出厂质检

**这是本技能与所有被合并对象的核心差异。**

#### 4a. 触发压力测试

- 3 条 `should_trigger` + 2~3 条 `should_not_trigger`（诱饵）
- **跨技能混淆测试（硬性）**：诱饵中至少 1 条必须是"应该触发另一个技能"的场景
- 测试时把**整包所有技能的 name + description 列表**给被测 Agent，让它做"该激活哪一个"的选择题，而非"要不要激活这一个"的判断题
- 诱饵容错为 0

详见 `methodology/04-pressure-test.md`。

#### 4b. FIDELITY 出厂质检

**铁律：答题 Agent 与评分 Agent 必须是两个独立 Agent，绝不自评自证。**

依据：SkillLens 论文（arXiv 2605.23899）实证 LLM 自评 skill 质量准确率仅 46.4%，接近随机。

五个维度（总分 100）：

| # | 维度 | 分值 | 测什么 |
|---|---|---|---|
| 1 | 立场/结论一致性 | 30 | 对内容明确表达过的判断，回答方向是否一致（3 题 × 10 分） |
| 2 | 风格辨识度 | 20 | 不看名字能否认出是这套方法论，还是通用 AI 腔（盲读） |
| 3 | 边缘诚实度 | 20 | 遇到内容没讲过的问题，是标注推断还是斩钉截铁编造（1 题） |
| 4 | 来源透明度 | 15 | 底稿是否可溯源，一手占比、关键引语有无出处 |
| 5 | 结构完整度 | 15 | 六段是否齐全、E 步有无完成标准、B 有无失败模式 |

等级：A ≥85 / B 70-84 / C 55-69 / D <55。**B 是进入 registry 的准入门槛。**

**反作弊规则**（必须遵守，否则分数无效）：
- 答题 Agent 不知道自己在被测什么维度
- 评分 Agent 不参与答题，只对照原始内容判定
- 出题避开 skill 内已有示例（防背答案）
- 重要结论建议 2 个评分 Agent 独立跑，分差 >10 分人工复核
- **禁止自评自证**——这是本机制的存在的唯一理由

模板：`templates/FIDELITY.md.template`

### 阶段 5 · 形态决策、确定性编译与发布

**先决策形态**：`python3 scripts/td.py strategy <bundle>` —— 默认 `single-first`，
晋级能力 ≥3 **且**触发验证已就绪才推 pack，避免一拆多就互相抢调用。

**再编译发布**（脚本只做确定性操作，语义推理全部交给 Agent）：

```bash
td.py validate <dir>                       # 静态校验：死链 / 结构 / 来源占比
td.py gate <FIDELITY.md> --min B           # 门槛；非双 Agent 评测默认不放行
td.py compile <bundle> --out <dir>         # staging → 快照 → 锁 → rename 原子替换
td.py snapshot <dir> / td.py rollback <dir> --to <id>
td.py upstream list                        # 内置上游（cangjie）能力与依赖状态
```

发布会比对 `BUILD_MANIFEST.json` 的 `published_hashes` 检测本地手改，**拒绝静默覆盖**，
并用 `WriterLock`（O_EXCL 锁文件）防并发写同一目标。

**上游优先原则**：分块、词法索引、token 计量、形态决策、增量维护等能力**优先走上游**
（`scripts/vendor/cangjie/`，MIT 原样内置），本包自研层负责零依赖统一入口与上游没有的部分
（FIDELITY 门槛、字幕管线、六路调研、冲突标记、prompt 编译）。详见 `scripts/vendor/PROVENANCE.md`。

### 阶段 6 · 持续演进

产物登记到 `registry/<slug>/`，含 `fidelity_score` 与 `eval_mode`。

```bash
td.py diff <A> <B> / td.py impact <dir> <slug>     # 改了什么、会波及谁
td.py repair <dir> / td.py patch <card> <p.json>   # 机械修复（默认 dry-run）
td.py update <bundle> --out <dir>                  # 重新校验 + 重编译
td.py count <dir>                                  # token 计量
```

**写操作默认 dry-run**，落盘需显式 `--apply`。本技能不做自动进化，只保证产物
**可被 darwin 安全处理**（有 manifest、有快照、有回滚）。

> 完整命令清单与参数：`references/command-cheatsheet.md`

---

## 人物蒸馏分支

素材是**人**（书名/访谈/演讲换成人物名）时，阶段 2 的能力卡换成**认知植入结构**：

### 入口分流：模糊需求诊断（可选，补自 nuwa）

用户来的时候**只有模糊需求、没有目标人物**（「我想提升决策质量」「有没有一种思维方式能帮我看透商业本质」）时，先走 `references/persona-need-diagnosis.md` 的**模糊需求诊断分支**：需求定位（≤2 轮追问）→ 候选推荐（人物 vs 主题）→ 用户选择 → 再进入下方蒸馏。这把 nuwa 的「从需求反推蒸馏对象」补回，避免维度错配与无谓的重调研。用户已给明确人名则跳过，直接六路调研。

> **本版本已补回的 nuwa 人物资产**：① 六路调研骨架（`td.py research init` 的 01-writings…06-timeline，含 03-expression-dna 车道，合并时带**车道覆盖审计**——比 nuwa 多一层缺失车道告警）；② 表达 DNA 六维结构化（`extractors/persona-extractor.md` 第 6 类 + `templates/PERSONA.md.template`「我说话的方式」）；③ 模糊需求诊断（本小节 + `references/persona-need-diagnosis.md`）；④ **心智模型三重验证**（`extractors/persona-extractor.md`：跨域复现 ≥2 车道 / 生成力留出题 / 排他性对照 no-skill 基线，附降级规则——区别于 cangjie 阶段 1.5 的候选单元三重验证）；⑤ **人物版 eval-kit 题型预设**（`references/persona-eval-preset.md`：3 已知立场 + 1 超范围 + 1 盲读，含出题纪律与完整示例）。五者在 rulai 下均按**离线优先**改造。

```
我是谁              身份锚定（不是"模仿他"，是"带着他的经历思考"）
我的认知上下文
  ├─ 信念及其来源     5-7 条，每条必须讲清"因为什么经历形成"
  ├─ 我做过的关键决策  3-5 个，必须有事后反思
  ├─ 我栽过的跟头     2-3 个真实失败
  ├─ 我的内在矛盾     ≥2 对真实矛盾
  └─ 我明确不懂的     ≥3 条认知边界
我看问题的方式        3-9 个思维习惯，**禁止写显式 Step 1/2/3**
我绝不会做的事        4-6 条红线
我说话的方式          偏好 / 禁忌 / 不确定时的处理
素材来源              ≥2 条可溯源
```

**为什么禁用显式步骤**：`scripts/td.py validate` 会机械检测 `Step 1/2/3`、`第一步：`、`1.` 模式并报 error。

首句必须写明认知植入而非角色扮演：

> "你不是在模仿语气；你带着以下经历、判断、失败和边界来思考。"

结构模板：`templates/PERSONA.md.template`

---

## 目录结构

完整目录结构见 `README.md` 第五节。加载本文件约 5.5K tokens，全部文档约 39K，
细节按需从 `methodology/` 与 `references/` 加载——不要一次性全读。

---

## 边界与诚实声明

1. **本技能不声称能从原始书籍一键蒸馏**。语义提取必须由 Agent 完成，脚本只做确定性操作。
2. **字幕获取是唯一联网命令，且默认 dry-run**。`td.py fetch-subtitle` 不加 `--execute`
   只打印命令；本地已有字幕时完全不需要联网。
3. **FIDELITY 分数不是自证**。`gate` 对 `fallback-self` 默认**拒绝**（需 `--allow-fallback`），
   且自测模式下维度 1/3 按 80% 折算、维度 2 作废。
4. **上游代码原样内置、不改**。`scripts/vendor/cangjie/` 是 MIT 原件；要改逻辑请在其仓库
   提 PR，本包只在 `tdlib/` 做适配。
5. **五项晋级门是建议不是定律**。宁可少晋级几个独立技能，也不要制造互相抢调用的技能包。
6. **一手来源不足时必须降级**。素材标注为"推测"的维度，要在认知边界里明确写出。
7. **触发评测不由脚本调用模型**。本包零网络：Agent 作答、脚本判分、容错 0。

---

## 资源依赖

- 必需：Python 3.10+
- 可选：`PyYAML`（严格 frontmatter）、`tiktoken`（精确 token 计量）、`jsonschema`
- **无网络调用**：所有脚本纯本地，不访问任何外部 API
- 自检：`python3 scripts/td.py doctor`
- 回归：`python3 tests/e2e.py`（130 项，零依赖与完整依赖两种解释器各跑一遍）
- CI：`.github/workflows/pipeline-check.yml`（双版本矩阵 + 红线扫描 + Schema 校验）

## 许可

MIT。本技能融合三个 MIT 项目的公开方法论，署名见 `metadata.lineage`。
