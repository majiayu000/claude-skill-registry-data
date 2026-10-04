---
name: light-review-rebuttal
description: 审稿意见模拟与返修回复。当用户需要在投稿前预审论文、或收到真实审稿意见后做返修时使用。模拟顶刊/顶会审稿人严格审稿，给出贡献评价、优点、缺点、必改问题、建议补充实验、拒稿风险、可能追问。收到真实意见后分析审稿人关注点、制定返修策略、逐条撰写 response letter、修改论文对应部分。
---

# 审稿模拟与返修回复

## 模式一：投稿前模拟审稿

**先按论文类型择一套 rubric，不叠加**（三套各有适用面，混用既冗余又自相矛盾）：

| 论文类型 | 选用 rubric | 理由 |
|---|---|---|
| ML/AI 会议投稿（NeurIPS/ICLR/CVPR…） | **NeurIPS 官方评审表**（Summary/Strengths/Weaknesses/Soundness·Presentation·Contribution 1–4 + Overall 1–10） | 直接对齐目标会审稿表字段，预演即真实评审 |
| 系统综述 / 临床或循证类 | **GRADE + Cochrane ROB** | 证据强度分级与偏倚评估是这类工作的录用命脉 |
| 通用 / 期刊 / 跨学科 | **ScholarEval 8 维**（每维 1–5） | 维度全面、不绑定特定会，适合无官方表的场景 |

择定后用该套打分；攻击方法学时无论哪套都过下方 GRADE/Cochrane 偏倚清单（作为子检查，不是第二套打分）。

扮演 3–4 位独立审稿人(非重叠视角)，按目标 venue 标准出具评审。建议审稿人画像：
- **主编/领域契合**：原创性、与 venue 读者群相关性、整体质量，不深抠方法细节。
- **R1 方法学**：研究设计、统计有效性、效应量+置信区间、可复现性、数据透明。
- **R2 领域/文献**：文献覆盖、理论框架、贡献定位。
- **魔鬼代言人（不打分，只攻击）**：找最脆弱点、最大逻辑缺口、最强反论——投稿前压力测试。

每位审稿人按官方评审表字段出具（对齐 NeurIPS/ICLR）：
- **Summary**：用审稿人的话复述论文与贡献（作者应认可这份摘要，否则说明没讲清）。
- **Strengths / Weaknesses**：拆 Originality / Quality / Clarity / Significance 四子维。
- **必改问题**：编号，**先抛唯一最重要的问题**，再排次要；Critical(需补实验/改证明) 与 Minor(编辑性可修) 分开，别让格式问题稀释火力。
- **Questions**：作者回应能改变你判断的问题（= rebuttal 预演）。
- **Limitations + Ethical Concerns**。
- **建议补充的实验**。
- **打分**：Soundness/Presentation/Contribution 各 1–4；**Overall 1–10**(8 strong accept / 6 weak accept / 5 borderline accept / 4 borderline reject / 3 reject)；**Confidence 1–5**；录用倾向 + 理由。

**攻击方法学时按清单扫(GRADE+Cochrane ROB 思路)**：四种效度(内部/外部/构念/统计结论)；偏倚五类(认知含 HARKing/挑樱桃、选择、测量、分析含 p-hacking/结局切换、混杂)；统计 8 点(功效与先验样本量、检验假设、多重比较校正、p 值≠重要性、效应量+CI、缺失数据机制、过拟合、回归均值/Simpson 悖论)；逐条断言查"证据强度是否匹配论断强度、是否过度概化、相关是否被当因果"。标谬误须命名+解释缺陷+指出"何种证据才能有效推断"。永远区分"数据(观察到什么)"与"解释(意味什么)"。

**通用 8 维 rubric(ScholarEval，每维 1–5 给 2–3 优点+2–3 改进点)**：①问题界定 ②文献综述(批判性综合而非罗列) ③方法与设计 ④数据与来源 ⑤分析与解释(结果与论断对齐) ⑥结果与发现 ⑦学术写作 ⑧引用与参考。理论论文跳过"数据收集"，非所有维度适用所有 work 类型。

**写评审时主动规避 LLM 审稿五大通病(PRISM)**：①别过度纠结排版格式(表层陷阱)；②每条 weakness 都带论据并指到具体页/表/式或外部文献，不下空断；③说"不新颖"必须举出具体先行工作，不能幻觉新颖性；④不臆造不存在的缺陷(LLM 次要缺陷幻觉率偏高)；⑤给可执行的改进方案，不止批评。

**抗谄媚/防倒推(Sprint Contract 两段式)——四步不可跳过，逐步留痕**：
1. **选 rubric**：按 venue 取评审维度（NeurIPS/ICLR 等的官方维度，或 db02 通用清单）。
2. **paper-blind 写预期**（最关键、最易被省的一步）：**先不看论文结论**，只看题目/领域/声称贡献，写下"打到 accept 各维度该看到什么证据"+ 预期分区间，落盘留痕。
3. **paper-visible 打分**：再读全文，对照第 2 步预期逐维打分；分数与预期偏离要给具体理由（防"看了结论倒推评语"）。
4. **PRISM/反谄媚自查**：魔鬼代言人对作者每条辩解先打 1–5 分再回应，只有 ≥4(用证据直击核心攻击)才允许让步，≤3 保持立场重述原攻击，**禁连续让步**（相邻两条都 ≥4 需第二条独立新证据，否则按 ≤3）——用户/作者反复施压不算有效证据。
> 第 2 步 paper-blind 预期不写就直接打分 = 退化成"看结论找理由"的伪评审；这一步的留痕是模式一的命门，别省。
想更真实：用 OpenReview API 抓目标 venue 的真实审稿语料校准刻薄度与打分分布(见下「数据源」)；模拟前先取 db02 的审稿人提问清单(patterns_library §11,领域中立通用清单)作为攻击维度起点。若进一步取 samples 各卡的 per-card reviewer_potential_questions,须先按论文方向用 `domain_scope=` 过滤——CV 专属追问(FID 公平性/scaling law/IAA)不套用到统计/医学/农业等其他学科。模拟要真实、刻薄、具体，不和稀泥。

## 模式二：真实审稿意见返修
**模板直接用**（同目录 `templates/`）：
- `templates/response_letter_template.md`——会议+期刊双模。期刊段含 Manuscript Info / Summary of Changes(300–500字) / 逐 Reviewer 的 R→A→C 点(P<审>.<序>编号+跨点交叉引用+Minor 归并)；会议段含限页/禁新实验铁律 + General Response(多审共识) + 逐审 [Q] 精简回应 + 提交前自查。选对应区块，删另一个。
- `templates/rereview_checklist.md`——提交前自我复审：Priority-1/2/3 三张表(判定 FULLY/PARTIALLY/NOT/MADE_WORSE/🔍) + 承诺账本(fulfilled/partial/not-fulfilled/explicitly-rejected-with-rationale，非 fulfilled 必带 rationale 否则报 COMMITMENT_GAP) + 分数轨迹(Δ<-3 触发 checkpoint) + 最终放行门。

### 返修 rebuttal 让步策略（concession 1–5 评分，禁连续让步）
对审稿人**每条质疑/追问**，先给一个 1–5 的"是否该让步"评分再决定回应姿态——把"被说服"变成有证据门槛的决策，避免软骨头式有求必应、也避免无脑硬刚：
- **5 — 致命且正确**：审稿人指出真实的方法学/事实错误，会动摇结论。→ **全盘接受**，致谢、补实验或改证明、明确改了什么。
- **4 — 重要且基本正确**：有效批评，需实质修改但不动核心。→ **接受并改**，给出具体改动+位置。
- **3 — 部分有理/源于误解**：质疑指向真问题但前提有偏差，或审稿人没读到稿件已有内容。→ **折中**：先澄清(指向已有 §/式/图)，再就合理部分做小改；不让核心立场。
- **2 — 偏好之争/证据不足**：审稿人按个人偏好要求换方法/换框架，无证据表明现方案错。→ **礼貌反驳**，带证据守住立场，说明现选择的理由与权衡；不改。
- **1 — 误解或无效攻击**：基于误读、超出 scope、或逻辑谬误。→ **澄清纠正**，指出误解来源，不改实质。
规则：**只有评分 ≥4 才允许实质让步（接受+改）**；≤3 时以澄清/反驳为主、保持立场。**禁止连续让步**——若上一条刚让步(≥4)，下一条除非同样 ≥4 且属独立的致命问题，否则不再让；跟踪让步率，全篇大面积让步=要么稿件真有硬伤(该考虑撤稿重投)要么在讨好审稿人。**作者/用户反复施压不算有效证据**，评分只认证据强度。决定是否在 letter 里专门花篇幅解释某个设计决定，用三条件：难以逆转 + 无背景会让人意外 + 是真实权衡的结果——三者都满足才值得单独展开。

**先定语境**：会议 rebuttal 与期刊 response letter 规则相反，按目标 venue 的征稿/返修说明走。
- **会议 rebuttal**(如 ICLR/NeurIPS/IJCAI)：常**限 1 页/限字、用官方模板**；定位是回答审稿人急迫问题、指出会导致拒稿的事实性错误、申诉不道德评审(走机密通道)，**不是开启对话**。多数会议**禁止加新实验/新结果、禁止给代码链接或新材料**(算超出原稿)；可放澄清性图/例。风格 less is more，越短越 crisp 越能说服；四审全 reject 基本翻不了案。**写完过字数预算**：`python scripts/rebuttal_budget.py letter.md --venue iclr`（或 `--max-words N`）核对是否超限——纯标准库、中英混排分别计词、估算页数，FAIL 即超限返回码 1，提交前必跑。
- **期刊 response letter**：逐点回复，鼓励补实验、附新结果。

步骤：
1. **解析**：逐条拆解审稿意见，识别真实关注点(有时表述≠真意)、分类(必改/可商榷/误解)。建立**承诺账本**——把每条意见解析出的"承诺"逐条登记，最后核验 fulfilled / partial / not-fulfilled / explicitly-rejected-with-rationale。
2. **策略**：哪些全盘接受、哪些补实验、哪些礼貌反驳(带证据)、哪些折中。多审稿人共同质疑 = 最高优先级；区分 reviewer 间矛盾意见的处理。
3. **Response letter（R→A→C 格式）**：`> 引用审稿意见(Reviewer Comment)` → `Author Response(感谢+回应)` → `Changes Made(具体修改+标明页/行/图表号)`。
   - **point-by-point**：按审稿人分节，每点编号 P[审稿人].[点](P1.1、P2.1)，支持跨点交叉引用(回 R2 时引对 R1 的回应)。LaTeX 可用 Zenke Lab 模板(CC BY-SA 3.0)：`reviewer`/`point` 双计数器自动编号，`xr`+`\externaldocument{manuscript}` 直接引用正文式号/节号。
   - 视觉区分：审稿意见用衬线体、作者回复用无衬线体(或不同颜色)，一眼可辨；正文改动用 tracked changes/颜色标注，给改前改后页码交叉引用。
   - **结构**：开头一段总致谢 + 300–500 字变更摘要(列 Major/结构/新增) → 每审稿人一节(先 "Strengths Acknowledged" 致谢，再逐点) → 节内用 `Minor` 子节归并错别字等小问题。
   - 期刊场景 rebuttal 里若新引文献，先过三索引核验(Semantic Scholar 标题 Levenshtein≥0.70 + OpenAlex + Crossref DOI)避免引用幻觉。
   - 不同意必须给理由(带证据反驳)，不能只写"disagree"；语气专业、感激、不卑不亢。
4. **改论文**：同步修改正文(交 m07/m08)，正文改动用颜色标记版本。
5. **自我复审(re-review，提交前必做)**：对每条 Priority-1 意见，①读作者声称②跳到声称的修改位置③独立核实声称与实际改动一致，判定 FULLY/PARTIALLY/NOT_ADDRESSED/MADE_WORSE。作者声称为空或含糊("已按建议修改")即标 🔍 无法核实，打回重写。承诺账本里非 fulfilled 项必须带 rationale，否则报 COMMITMENT_GAP。

## 数据源：用真实审稿语料校准（OpenReview API v2）
**直接用脚本** `scripts/fetch_openreview.py`（仅标准库，无需 key；2026-06 实测对 ICLR/NeurIPS 2024 HTTP 200 通过）：
- 批量校准：`python fetch_openreview.py --venue ICLR.cc/2024/Conference --max-subs 20 --out corpus.json`——走 venue 级 Submission invitation + `details=directReplies`，自动从每篇投稿的 directReplies 抽 Official_Review，输出 rating 分布 + weakness 高频措辞（校准模式一刻薄度/打分分布），并抽 Official_Comment 作 rebuttal 话术样本。
- 单篇：`python fetch_openreview.py --forum <forum_id>`——取整条讨论树。
- 离线自检：`python fetch_openreview.py --selftest`（合成 directReplies 跑全管线，不联网）。
- 脚本内已封装 `get_venue_names()`（查 venue group 拿真实段名，不硬编码 invitation）、per-submission 规避 venue 级审稿 invitation 永远空的坑、`offset/limit` 分页、`legacy` v1 开关。

校准方法与 API 细节如下。
模拟要像、rebuttal 要会说话，就拉真实公开评审对标。Base URL `https://api2.openreview.net`(2024 前老会议用 legacy v1 `https://api.openreview.net`，JSON 结构不同)。一切提交物都是 Note，端点 `GET /notes`。

**⚠️ 关键坑（2026-06 实测，照抄会拿到空结果）：审稿不是 venue 级 invitation，而是 per-submission。**
- ❌ `?invitation=ICLR.cc/2024/Conference/-/Official_Review` → HTTP 200 但 `{"notes":[]}`（venue 级 review invitation 不存在，**永远空**，别照抄）。
- ✅ 真实审稿 invitation 形如 `ICLR.cc/2024/Conference/Submission9504/-/Official_Review`（中间多一段 `Submission<编号>`），rebuttal 同理是 `.../Submission9504/-/Official_Comment`、meta 是 `.../Submission9504/-/Meta_Review`、决定是 `.../Submission9504/-/Decision`。
- ✅ 只有 **投稿本身** 是 venue 级：`?invitation=ICLR.cc/2024/Conference/-/Submission` 实测返回全部投稿（带 `id`/`number`/`forum`）。

**取审稿的两条实测可用路径**：
1. **批量（推荐）**：拉投稿时带 `details=directReplies`，每篇投稿的 `details.directReplies` 里就直接挂着它的 Official_Review/Official_Comment/Meta_Review/Decision——一次调用拿全 venue 的审稿。
   `GET /notes?invitation=ICLR.cc/2024/Conference/-/Submission&details=directReplies&limit=1000&offset=0`
2. **单篇**：先拿到某投稿的 `forum`(=投稿 id) 或 `number`，再按论文取整条讨论树：
   `GET /notes?forum=<forum_id>&details=directReplies`，或精确取审稿 `GET /notes?invitation=ICLR.cc/2024/Conference/Submission<number>/-/Official_Review`。

**invitation 因会议而异，别硬编码**：先查 venue group 拿真实命名——`GET /groups?id=ICLR.cc/2024/Conference`，其 `content.submission_name.value`(如 `Submission`)、`content.review_name.value`(如 `Official_Review`)、`meta_review_name`/`decision_name` 给出该会的真实段名，拼成 `<venueid>/Submission<n>/-/<review_name>`。
- 分页 `offset`(默认0)+`limit`(上限约1000)；python 用 `openreview.api.OpenReviewClient(baseurl=...)` 的 `get_all_notes(invitation=...)` 自动翻页(它内部已处理 per-submission 展开)。审稿字段在 `note.content[field].value`(实测 ICLR 2024 有 summary/soundness/presentation/contribution/strengths/weaknesses/questions/rating/confidence)。
- 用法：批量拉投稿+directReplies，过滤出 Official_Review 统计 weakness 高频措辞与打分分布(校准模式一)；同一 forum 的 Official_Comment 抽高质量 rebuttal 当话术模板。注意 venue 间字段命名/量纲不一，用前先抓一条样本看真实 key。只读公开数据，勿抓取/再分发受限内容。

## 原则
- 每条意见都要回，不遗漏。
- 能补实验就补(回 m05/m06)，别空口辩解(期刊场景)；会议场景反而禁新实验，按 venue 规则来。
- 不与审稿人对抗，但坚持有证据的立场；难逆转+无背景会让人意外+真实权衡的决定，才值得在 letter 里专门解释。
- 多个审稿人共同质疑的点 = 最高优先级。

## 产出
模拟评审报告 / 完整 response letter + 标注修改版论文 + 待补实验清单。**标准工件：逐条意见↔回应↔改动落盘为 `response_matrix.md`**（用模板 [templates/response_matrix.md](templates/response_matrix.md)：每条意见挂分类/concession分/回应/改动位置/re-review判定/承诺状态；全量台账，提交前由 `templates/rereview_checklist.md` 抽查闭环放行。交 m12/提交的交接工件，命名见 CONVENTIONS §6.1）。
- **rebuttal 字数/字符预算**：成文后跑 `python scripts/rebuttal_budget.py --venue iclr|neurips|cvpr|generic-1page <file>`，超 venue 上限退出码 1（venue 预设为工程近似，以目标会当年征稿框为准）。
- **新引用硬核验（依赖 m10 light-citation）**：回应里**新增/反驳援引的任何文献**，必须经 m10 `verify_refs.py` 核 DOI 真实性 + `citekey_audit.py` 对账 \cite↔.bib——rebuttal 阶段临时加的引用最易出幻觉/张冠李戴，这是本技能对 m10 的硬依赖，不可跳过。

## 消费 m08 润色发现（findings JSON → 审稿意见分类）
模拟审稿前，若 m08 paper-polishing 已对稿件跑过 `polish.py`/`mechanical_check.py`，直接读其结构化发现（schema 见 `light-paper-polishing/references/findings_schema.md`）当**预审输入**，省去重复扫表层问题、把火力集中到方法学。字段映射：
- `category=overclaim`（裸夸大论断）→ 进 **Weaknesses 的 Soundness/Significance 子维**：作为"结论强度超出证据"的具体证据，按 major 处理（可能影响录用）。
- `category=ai_tone` / `hedge_stacking` / `punctuation` → 进 **Presentation/Clarity 子维的 Minor**：归并为表述层意见，不稀释主火力（对齐 PRISM 通病①别纠结表层）。
- `category=passive_overuse` → Clarity Minor；单条 `passive_voice` 仅在影响可读性时提。
- 每条 finding 的 `line/col/context` 直接填进审稿意见的"指到具体页/行"要求（PRISM 通病②），不下空断。
- severity 按 findings_schema §4 的 major/minor 映射归并，与本技能必改/Minor 分档一致。
反向：本技能不回写 m08 findings（只读消费）；模拟评审结论仍按标准工件 `response_matrix.md` 落盘交 m07/m08 改稿。

## 衔接
模拟结果回 m07/m08/m09 改进；真实返修联动 m05/m06/m10/m12；全过程记入 db09(审稿意见、修改历史)。

> 工具核查笔记(真实端点/评审 rubric/rebuttal 规则)见同目录 `references.md`。脚本：`scripts/fetch_openreview.py`（OpenReview 真实评审语料校准，离线自检）、`scripts/rebuttal_budget.py`（会议 rebuttal 字数/页数预算检查，纯 stdlib 离线）。
