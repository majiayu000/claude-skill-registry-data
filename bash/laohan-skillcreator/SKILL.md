---
name: laohan-skillcreator
version: 2.2.0
description: 创建、审计、修复和优化 Agent Skills。Use when 用户要新建 Skill、检查 Skill 质量、恢复原版或修正明确错误、比较新旧效果，或更新本 Skill 借鉴的上游方法。触发词："创建skill""写一个skill""改skill""优化skill""给skill打分""skill体检""review skill"。
---

# laohan Skill 创建·审计·修复·优化器

创建是生产能力，审计是只读诊断，修复是小范围纠错，优化才是实验性演进。先判断模式，再使用与风险相称的验证；不得把一次明确的小修复升级成完整优化项目。

## 参考来源

当前借鉴 6 组上游来源。具体文件与最近核验 commit 记录在 [references/upstream-sources.json](references/upstream-sources.json)。修改本 Skill 自身或用户要求更新方法时，先运行 `scripts/check-upstreams.sh`；发现上游变化后阅读相关 diff，只吸收能改善本地真实行为的变化，不自动覆盖本地方法。

1. **anthropics/skills · skill-creator**（https://github.com/anthropics/skills）
   - 借鉴：渐进式披露（metadata→body→bundled 三层）、同条件 baseline 对比、盲比较、description 优化器、从 transcript 找重复工作、更新保持原名
   - 核心理念：好的 skill 分三层渐进披露，不是一坨

2. **Agent Skills specification / best practices**（https://github.com/agentskills/agentskills）
   - 借鉴：frontmatter 公共规范、渐进式披露、真实经验优先、控制强度与任务脆弱性匹配、从执行轨迹删除无效步骤
   - 核心理念：Skill 应补充 agent 缺少的领域经验，不重复常识；过度全面同样会降低效果

3. **mattpocock/skills · writing-great-skills**（https://github.com/mattpocock/skills）
   - 借鉴：触发分支、信息层级、完成条件、单一真源、去除 duplication/sediment/no-op
   - 核心理念：Skill 追求过程可预测，不追求所有输出相同；不同分支只加载各自需要的信息

4. **thananon/9arm-skills · debug-mantra/post-mortem/scrutinize**（https://github.com/thananon/9arm-skills）
   - 借鉴：verbatim recitation（首次一次+逐字+silent apply）、硬门控措辞、refuse to draft、跨 skill offer 非自动、先质疑意图、cite or it didn't happen
   - 核心理念：不确定就停下来，每个 claim 要有引用

5. **alchaincyf/darwin-skill + SkillLens / SkillOpt**（https://github.com/alchaincyf/darwin-skill）
   - 借鉴：9 维评分体系、反例黑名单 8 条、棘轮机制（git ratchet）、独立子 agent 复评、人在回路 5 阶段
   - 核心理念：SkillLens 显示无 rubric 的 LLM 成对判断只有 46.4% 准确率，验证过的 meta-skill rubric 提升到 73.8%，仍不足以代替真实任务验证

6. **obra/superpowers · writing-skills**（https://github.com/obra/superpowers）
   - 借鉴：只有深度创建/优化才做无 Skill baseline 与压力场景；可机械执行的约束优先交给脚本或 verifier
   - 核心理念：测试应证明 Skill 改变了实际行为，但不能把 TDD 仪式强加给明确的小修复

---

## 核心理念

四原则：

1. **路由决定成本** — name + description 负责让 agent 找到 Skill，正文第一步负责选择正确分支；触发准确不等于每次都走重流程
2. **结构引导行为** — 好骨架比好指令有效
3. **精简优于完整** — 每个章节都要证明存在的价值
4. **效果先于格式分** — 静态 rubric 用于发现问题；触发、执行、held-out 样本与用户验收决定是否保留改动

---

## 先选模式

每次只选一个主模式：

| 模式 | 何时用 | 默认验证强度 |
|---|---|---|
| `CREATE` | 新建一个可复用 Skill | 真实样本、触发/反触发、执行测试；复杂或高影响 Skill 再加 held-out |
| `AUDIT` | 体检、评分、检查合理性 | 只读，引用具体行和行为证据；不修改文件 |
| `SURGICAL_FIX` | 恢复原版、修正明确错误、更新固定合同或路径 | 比对真源、最小修改、直接覆盖该错误的针对性回归；不做静态评分、blind judge 或无关 held-out |
| `OPTIMIZE` | 用户明确要求提升效果、比较新旧方案或全面演进 | 冻结 baseline/指标，运行 held-out；主观结果才用 blind judge |
| `UPSTREAM_REFRESH` | 更新本 Skill 借鉴的方法或核验引用是否变化 | 运行上游检查，阅读变化，只合并相关增益并更新记录 commit |

用户说“改 Skill”但给出了明确错误或原版真源，默认 `SURGICAL_FIX`；只有用户要求“优化效果、全面审核、比较方案”才进入 `OPTIMIZE`。`AUDIT` 不隐含修复授权，`CREATE` 不隐含安装或发布授权。

### 上游更新

`UPSTREAM_REFRESH` 和修改 `laohan-skillcreator` 自身时：

1. 运行 `bash scripts/check-upstreams.sh`。
2. `CURRENT`：继续当前任务。
3. `UPDATED`：读取记录 commit 到最新 commit 的相关文件 diff，判断是否改变本地借鉴的方法。
4. 只有确有增益才修改本 Skill；无相关增益只更新核验说明，不照搬上游全文。
5. 验证本地模式分流没有退化后，更新 `references/upstream-sources.json` 的 commit 和 `verified_at`。
6. `UNVERIFIED`：报告无法核验，不声称已经跟上上游；不阻断与上游无关的 `SURGICAL_FIX`。

---

## CREATE 流程

### Step 0 · 先质疑意图（硬门控，scrutinize 模式）

**新建前强制检查三个问题；先用 catalog/项目证据自主回答，只有用户意图无法从对话确定时才询问：**

1. 能不能**扩展现有 skill**？（从当前 runtime 的 available-skills catalog 和项目本地 skill 目录查重叠；不猜安装路径）
2. 能不能**不建**？（做 nothing 行不行？手动一次性操作够不够？）
3. 确认必须新建 → 进入 Step 1

**如果 1 或 2 答 yes → 告诉用户替代方案（扩展哪个 skill / 为什么不必建），不新建。**

### Step 1 · 捕获意图

从对话提取（或问用户）：
1. 这个 skill 让 agent 能做什么？
2. 什么时候触发？（用户会说什么关键词/什么场景？）
3. 期望输出格式？
4. 是否需要 scripts/ 或 references/ 子目录？

用户说不清 → 停下来，列出不明确的部分，等补充。**不要猜。**

### Step 2 · 调研

确认 Step 0 的"不能扩展已有"结论（重查 catalog 和当前项目）。如发现可扩展 → 回 Step 0。
- **完成条件：** 确认新建并说明理由

### Step 3 · 写 SKILL.md

按下方骨架模板和写法规则。先判断极简还是完整骨架，再填。
- **完成条件：** frontmatter 符合目标 runtime 允许的 schema（Agent Skills 通用最小集是 name + description；laohan-local profile 另要求 version），正文与资源引用完整

### Step 4 · 测试迭代

1. 先在可写工作副本中测试；只在目标 runtime 要求安装才按其官方路径/打包方式安装，不自动建 symlink
2. **触发测试**：自动路由 Skill 至少覆盖一个 should-trigger 和一个近似 should-not-trigger；分支多或 description 改动大时扩到每个分支，纯手动调用记 `NOT_APPLICABLE`
3. **执行测试**：确定性 skill 用可机械验证的输入/输出夹具；主观性 skill 用盲比和具体质量标准
4. **held-out 验证**：复杂、高影响或用户要求比较效果时至少保留 1 个未用于改稿的样本；简单 Skill 用一个真实执行样本即可
5. **重复工作检查**：读执行 transcript，若每次生成相同辅助代码 → 提取到 scripts/
6. 不通过 → 回 Step 3 改 → 重新测试
7. 3 轮未过 → 停，可能是结构问题不是小补，重审核心理念

### Step 5 · 本地验收

1. 用真实执行结果决定是否完成；6维评分只在结构不清或用户要求评分时作为诊断
2. 复杂/高影响 Skill 需 held-out 不退化；简单 Skill 的目标样本和触发测试通过即可接受
3. 🔴 **PUBLISH CHECKPOINT**：只有用户明确要求 push/publish/package/install 时才执行相应外部动作；创建或优化本身不隐含发布授权

---

## SKILL.md 骨架模板

不是每个 Skill 都需完整骨架。逻辑简单到几行能说清时直接写指令，别为“专业”加多余章节。

**判断标准**：单步、无复杂条件分支（简单回退除外）、无角色区分 → 极简。多步/有条件分支/多角色 → 完整骨架。

### 极简示例（5 行）

```markdown
---
name: caveman
description: 极简回应模式，只输出关键信息。Use when 用户说"caveman mode""极简""少说废话""简短"。
---

所有回应控制在 3 句话以内。只给结论和关键依据，不解释过程。如果用户要求详细解释，恢复正常模式。
```

### 完整骨架模板（v2 升级）

```markdown
---
name: skill-name
description: 一句话说清做什么。Use when 用户说"触发词1""触发词2""触发词3"或提到[相关场景]。  # ≤1024字符，3-8触发词，第三人称
# version: 1.0  # 只在目标 runtime/profile 允许时加
---

# Skill 标题

一句话定位。

## 核心理念（复杂 skill 必加，简单可省）

为什么存在、遵循什么原则。先讲 why 再讲 how——比直接列步骤更有效。

## 工作流

### 1. [步骤名]
- 做什么
- **完成条件：** [怎么判断这步做完了]
- **🔴 CHECKPOINT：** [仅当该步有外部副作用、高风险或用户保留决策时填；否则删除]
- **🛑 STOP：** [强制停止条件]

### 2. [步骤名]
- 做什么
- **失败处理（只有存在复杂降级链时用三段式；单一安全 STOP 直接写 if-then）：**

  | 触发条件 | 一线修复 | 仍失败兜底 |
  |---------|---------|-----------|
  | [X 失败] | [Y] | [Z] |

### 3. [步骤名]
- 做什么
- **涉及外部动作 → 🔴 等用户确认再执行**

## 操作规则

跨步骤常驻约束：

- [规则1]
- [规则2]
- 遇到 [异常] → [怎么处理]（不静默跳过）

## 不适用场景（refuse to draft 硬拒绝，v2 升级）

- 场景 A → 改用 [其他 skill]
- **缺 [必要输入 X] → 列出缺什么并停，不硬编、不猜**（9arm post-mortem 模式）

## 反模式（复杂 skill 必加，v2 从可选升级）

❌ 差：
"[反例]"

✅ 好：
"[正例]"

## 输出格式（可选）

# [标题模板]
## [章节1]
```

---

## 评分体系（6 维快速评分卡）

精简自 darwin 9 维（完整 9 维见 [references/scoring-rubric.md](references/scoring-rubric.md)）。给任何 skill 打分：

| # | 维度 | 权重 | 评分标准 |
|---|------|------|---------|
| 1 | **frontmatter 质量** | 10 | name/description 符合目标 runtime 的允许字段；description 同时说做什么与何时用。触发词数是启发式，不为凑 3-8 个堆词 |
| 2 | **工作流清晰度** | 20 | 编号步骤+明确完成条件+输入输出清晰 |
| 3 | **失败模式编码** ⭐ | 20 | 覆盖真实可发生且会影响结果的失败面；一个安全 STOP 已足够时不强行写三段表，复杂降级链才要求三段式 |
| 4 | **检查点设计** ⭐ | 15 | 外部副作用、高风险或用户保留决策前有显性 gate；自治/确定性 skill 说明无人工 gate 的理由也可满分，不为格式加假 checkpoint |
| 5 | **可执行具体性** ⭐ | 25 | 有具体参数/格式/示例可直接执行；只在软化词替代必要决策规则时扣分，引用、用户输出和不确定事实不机械命中 |
| 6 | **反例与风险边界** ⭐ | 10 | 阻止本 skill 实际可能触发的误用和危险动作；不涉及 git/删除/发布的 skill 不因没列这些动作扣分 |

**算分**：每维 1-10 分，总分 = Σ(维度分/10 × 权重)，满分 100。

**cite or it didn't happen（9arm）**：每个扣分必须引用 SKILL.md 具体行号或段落原文。不允许泛泛"这里不够好"。

**评分档位**：
- 85-100：静态结构可进入执行/held-out 验证，不等于可发布
- 70-84：需优化（找最低维改）
- <70：结构有问题，重审核心理念

---

## AUDIT 流程

1. 冻结被审计文件和用户关心的问题，读取原版、当前版与实际调用边界。
2. 先找会改变触发、执行、效果或维护成本的问题，再看格式；每个发现引用具体行、diff 或执行证据。
3. 区分 `BLOCKING`、`BEHAVIOR_RISK`、`MAINTENANCE` 和 `NO_ISSUE`，不把静态分数当问题数量。
4. 输出结论与最小建议，不修改文件、不安装、不提交；用户随后要求修复时再路由到 `SURGICAL_FIX` 或 `OPTIMIZE`。

## SURGICAL_FIX 流程

1. 明确错误、原版真源和应保持不变的行为。
2. 只修改能追溯到该错误的行；保留现有模板、方法库和已验证效果，清理本次产生的重复或矛盾规则。
3. 运行一个能在修复前失败、修复后通过的针对性检查；若影响已有机械合同，再运行对应合同回归。
4. 不为本次小修复增加评分表、blind judge、全量 trigger 矩阵、通用框架或新 Skill。
5. 报告改了什么、验证了什么、哪些真实效果仍待实际使用证明。

## OPTIMIZE 流程

优化已有 skill（只改自研 laohan 系列；npx 第三方 fork 后改）：

### 1. 建立可比基线
- 主 agent 按 6 维找结构问题，**扣分引行号**
- 冻结基线 skill、目标 runtime、测试样本、评分器和成功指标；没有这些就不声称“优化”

### 2. 一轮一个因果假设
- 每轮只修复一个可检验的行为缺陷；同一根因涉及多个 rubric 维度时一次改完，不为“一轮一维”留下自相矛盾
- 在未提交工作副本中应用 bounded add/delete/replace，记录假设与改动预算

### 3. 独立验证与 held-out gate
- 确定性 skill 用冻结的机械 verifier 比较基线/候选；主观输出由**不知道版本标签的 judge**盲比。只做静态审计时可用独立 judge 抓自相矛盾，但不把 73.8% 当绝对真值
- 候选只在预注册指标严格改善，或主指标持平且修复已证实高风险缺陷时接受；否则丢弃未提交改动

### 4. 棘轮轻量版
- 验证通过后才 commit；如用户已授权且候选已被单独 commit，退步时用 `git revert`，不用破坏性 reset
- 连续 2 轮 held-out 无实质改善或一轮只提高格式分时停手

### 5. 深度优化路由（不在这做）
需要大样本多轮优化时，读 references/scoring-rubric.md 跑完整 9 维；如当前 catalog 已安装 darwin-skill，也可按它的 held-out 循环执行。不在当前任务中自动安装。

---

## 操作规则

所有模式的共同约束：

- **保持精简**：写完逐条审查，删不影响输出的指令
- **Lazy creation**：有内容才建文件/目录，不先建空结构占位
- **通用化非过拟合**：不为单个用例做小众调整
- **解释 why**："因为 A 所以 B" 优于 "MUST 做 B"——LLM 聪明，给理由比硬规则有效（anthropics）
- **匹配目标用户语言**：laohan 系列默认中文，技术术语保留英文
- **更新保持原名**：installed 是 `research-helper` 就输出同名，不是 v2（anthropics）

### dim5 软化措辞审查（只在 AUDIT/OPTIMIZE 评分时使用）

**只审查可执行指令段**：以下措辞若代替了具体条件/动作，出现 ≥3 处时 dim5 扣 ≥3 分；引用、反例、用户输出或客观不确定性不计：
- "建议" / "可以考虑" / "根据情况" / "灵活把握" / "视情况而定" / "酌情" / "适当"

改用具体指令："做 X"（祈使句 + 具体参数/示例）。完整禁用词表见 references/blacklist-phrases.md。

### 反例黑名单（v2 新，darwin 8 条精简）

创建/优化时禁止：
1. **不把自评当验收** — 同一 session 可做静态诊断；确定性候选接受需独立机械 verifier + held-out，主观候选需 blind judge + held-out（OPTIMIZE/复杂候选接受时）
2. **不先 commit 再评** — 先在工作副本比较；只在候选已单独 commit 且获授权时用 `git revert`
3. **不为凑分堆冗余** — 触顶（连续 2 轮 Δ<2 分）就停
4. **不把静态分冒充验收分** — `AUDIT` 可标 `STRUCTURE_ONLY`；只有 `OPTIMIZE` 的效果改善结论必须有 baseline/with-skill/held-out 行为证据
5. **一轮只验一个行为假设** — 不用 rubric 分类强行切断同一根因
6. **不静默跳过异常** — fallback 失败必须先告知用户

---

## 不适用场景（refuse to draft，v2 升级为硬拒绝）

- 创建 **agent**（agent ≠ skill）→ 使用目标 runtime 的 agent 配置机制
- 非 SKILL.md/Agent Skills 兼容的平台插件 → 使用该平台的原生插件规格
- 修改 **npx 第三方 skill** → fork 后新建（`npx skills update` 覆盖原地改动）
- **缺必要输入**（用户说不清要做什么）→ **列出缺什么并停**，不硬编、不猜（9arm refuse to draft）

---

## 写法规则

### Frontmatter

```yaml
---
name: skill-name          # kebab-case，与目录名一致
description: 功能描述。Use when 触发场景列举。  # ≤1024字符，第三人称
# version: 1.0            # 只在目标 runtime/项目 schema 允许时使用；laohan-local 要求
---
```

**name + description 是 agent 路由 skill 的常驻元数据**。description 必须含：
1. 功能描述（一句话做什么）
2. "Use when" + 足以区分近似 skill 的自然语言触发场景；3-8 个是 laohan-local 启发式，不是通用 schema 硬约束
3. 第三人称（mattpocock）
4. 如有竞争 skill，明确区分

### 正文写法

| 规则 | 说明 |
|------|------|
| 篇幅控制 | 以完整加载且没有冗余为准；尽量 <500 行，接近/超过时把长参考和详细 eval 流程拆到 references/ |
| 核心理念先行 | 3 步以上 skill 在工作流前加核心理念章节（先 why 后 how）|
| 工作流+操作规则分离 | 工作流=步骤序列；操作规则=跨步骤约束，独立章节 |
| 阶段门控 | 只在外部副作用、高风险或用户保留决策前设硬 gate；确定性内部步骤不加假 CHECKPOINT |
| 反模式 WRONG/RIGHT | 核心规则用对比块（❌差/✅好）|
| 口诀植入（verbatim） | 只在任务真的需要可背诵纪律时使用；不把 debug-mantra 形式套到所有 skill |
| 输出格式 | 用模板定义，不给模糊指令 |
| 降级级联 | 多方案用严格优先级（依次尝试），非菜单 |
| 跨 skill 调用 | 完成后 **offer** 衔接另一个 skill（不自动 handoff，9arm post-mortem）|
| 写作原则 | 祈使句 + 具体例子 + 不用 ALL CAPS ALWAYS/NEVER + 内容创作类定义语气 |
| scripts/ 判断 | 确定性操作/重复生成的相同代码/需显式错误处理 → scripts（mattpocock）|
| references/ 判断 | 平台专属方法/长模板/不需每次加载的背景知识 → references（仅一层深）|

> **渐进式披露（anthropics）**：metadata（常驻）→ SKILL.md body（触发加载）→ bundled resources（按需）。SKILL.md 别一坨塞完，重的拆 references/scripts。

### 6 项极简自检清单（CREATE 后快速过）

- [ ] description 含 Use when + 触发词
- [ ] SKILL.md 尽量 <500 行；超过时必须拆 references，100-500 行按加载价值判断
- [ ] 无时效信息（具体日期/版本号除非必要）
- [ ] 术语一致
- [ ] 有具体例子
- [ ] references 仅一层深

---

## 验收与发布清单

创建/优化完成后：

- [ ] SKILL.md 写好，frontmatter 符合目标 runtime schema（通用最小集 name + description；laohan-local 另有 version）
- [ ] 目标 runtime/profile 已明确，安装路径或打包方式来自当前宿主规格
- [ ] 已记录本次模式；`AUDIT` 保持只读，`SURGICAL_FIX` 没有升级成完整优化
- [ ] CREATE/OPTIMIZE 的触发、反触发与执行测试通过；SURGICAL_FIX 的针对性回归通过
- [ ] 重复工作检查（无每次生成的相同辅助代码）
- [ ] 只有 OPTIMIZE 或复杂/高影响 CREATE 才要求 held-out；主观对比才要求 blind judge
- [ ] runtime 扫描按 profile 运行；fatal 必须修复，portable 专属路径警告由人工判断是否已有 capability branch
- [ ] 修改本 Skill 自身时已运行 `scripts/check-upstreams.sh`，并按实际核验结果更新上游记录
- [ ] 安全检查通过（无 API key/个人绝对路径，发布动作有明确授权）
- [ ] 本地 commit、安装、package、push 和 publish 分开登记；本地 commit 遵循当前任务/仓库授权，安装、package、push 和 publish 仅在用户明确授权时执行
