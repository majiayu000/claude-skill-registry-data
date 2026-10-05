---
id: legal-academic-writing
name: 法学论文撰写与引注核查
version: 3.0
language: zh-CN
description: 面向中文法学论文的完整工作流：撰写与修改、引注核查、真脚注。覆盖从选题定位、命题构建、规范与案例核读、论证展开、引注台账，到按《法学引注手册》逐条核查脚注格式、制作真正 Word 页下脚注（footnote）并成稿。用于撰写/修改/扩充法学论文、开题报告、文献综述、研究报告，以及核查论文脚注引注格式（Track Changes 修订模式修正）。
---

# 法学论文撰写、引注核查与真脚注 Skill

## 0. 这个 Skill 解决什么问题

覆盖三类任务：

1. **撰写**：用户给出选题或命题，从零撰写法学论文/开题报告/文献综述/研究报告成稿。
2. **修改/扩充**：用户给出已有论文草稿（可能带脚注体系），完善结构、表述、补充引用、保留真脚注。
3. **引注核查**：用户给出论文 .docx，按《法学引注手册》（2025版）逐条核查脚注引注格式，以 Word 修订模式（Track Changes）修正格式错误并加蓝色批注。

核心要求贯穿三者：

- 直接产出成稿，而不是只给提纲或建议；
- 涉及规范、案例、学术观点时核读文献后引用；
- 使用中文法学论文常见的**页下脚注式引注**；
- 生成 Word 时制作**真正的 Word 页下注（footnote）**；
- 避免把脚注错误做成尾注（endnote）、页脚（footer）或手工上标；
- 引注格式符合《法学引注手册》，可核查、可修订；
- 降低模板化、对仗化、空泛化的 AI 表达；
- 对现行法、历史法、学者主张、经验事实作规范层级区分；
- 最终输出可直接继续编辑、投稿或提交的 DOCX。

---

# 1. 任务识别

收到任务后，先判断属于哪类：

- 用户给出**选题/命题/方向** → 撰写模式（第一节流程）
- 用户给出**已有论文草稿**（附档或路径），要求完善/修改/扩充 → 修改模式（第一节流程，从"读取原稿"开始）
- 用户给出**论文 .docx**，要求核查/检查/修正引注格式 → 引注核查模式（第二节流程）

撰写/修改模式与引注核查模式可衔接：先撰写/修改成稿，再对成稿做引注核查。

---

# 一、撰写与修改工作流

强制顺序：先构思，再调研，再写作，再引注，再改 Word，最后核查。

## 第一步：定位与构思

先明确论文要解决什么，写下一段"写作说明"（不进入正文）：

- **核心问题**：要解决的法学真问题（制度漏洞、裁判分歧、规范冲突、学理争议）。
- **法律载体**：问题落在哪部法律、哪条规范、哪个司法解释、哪类案例上。
- **中心论题**：全文要证明的一个可争论命题。
- **论证框架**：分几部分、每部分承担什么论证功能、彼此如何衔接。
- **标题**：先写工作标题，成稿后打磨。

构思不清晰时，先停下来，不要用大段文字掩盖未构思。

## 第二步：调研与核读文献

动笔前，凡涉及以下内容必须调研核实，不得凭记忆书写：

- 法律条文：现行有效版本、施行时间、是否被修正案修改。
- 司法解释、规范性文件：文号、发布机关、现行效力。
- 案例：完整案号、法院、裁判日期、裁判要旨。
- 学术观点：作者、文献、期刊、年份、页码。

来源优先级：
1. 本地知识库（`knowledge_search` / `knowledge_auto_retrieve` / `knowledge_read_file`）。
2. IMA 知识库（`research_ima` 自动路由选库，或 `search_ima_catalog`）——补充学术文献、内部材料、法规库与案例库。
3. 北大法宝 / 元典等法律数据库（法规与案例主检索来源）。
4. 国家法律法规数据库（仅当用户指定、商业库无结果或效力冲突时）。

对每个准备写入正文的外部观点，至少完成：找到原文具体页、确认该页支持命题、判断用途（支持/限制/反驳/方法借鉴）、记录页码与出版信息。核读细则见 `references/source_review_and_evidence.md`，为拟写命题建立 `templates/evidence_matrix.md` 命题—证据矩阵。

写法律规范与案例相关段落前先检索取得依据；拿不到原文时标 `[待补引文位]`。

## 第三步：撰写论证

推荐段落结构：

> 本段命题 → 问题/争议 → 理由 → 文献或规范证据 → 对文献的限缩或评价 → 本文结论

论证规则硬性注意（详见 `references/argumentation_and_ai_style.md`）：

- **不把政策当构成要件**：刑事政策可解释、导向、协调，不能突破罪刑法定创造犯罪或法外加重。
- **不把"总体从严"写成"个案普遍从重"**：总体治理重心与个案罪责判断是两个层次。
- **不从"危害严重"直接跳到"扩大犯罪圈"**：补足既有规制不足、风险可识别、提前干预适合、更温和手段不足、刑罚介入合比例。
- **不按罪名预设"严罪/宽罪"**：围绕客观不法、行为危险、主观责任、控制能力、获利、持续性、再犯风险、犯罪后表现、刑罚必要性。
- **学者观点必须保持身份**：不把"有学者建议增设资格刑"改写为"我国应当增设资格刑"，除非本文完成自己的规范论证。
- **区分命题类型**：事实命题、规范命题、评价命题、推论分清，不把事实前提直接当规范结论。

## 第四步：生成引注文本

先决定"为什么引"，再决定"怎么引"。每条脚注进入 `templates/citation_ledger.md`，记录：锚点句、类型（直接引/间接引/规范/案例/数据/方法借鉴）、来源、具体页码、最终脚注文本。

### 必须引注

他人的理论观点；他人提出的概念/模型/分类；具体统计数据；具体案件事实；历史事实；对立法/司法解释制定背景的说明；非常识性事实；直接引语；借来的论证框架；本文批评/限缩的原观点。

### 通常不引

纯粹由本文完成的逻辑推导；众所周知无争议的常识；论文结构安排；对前文已充分引证材料的简短回扣。

### 脚注位置

脚注号**紧贴其支持的命题之后**，不统一放段末。一引一注，不把多个来源塞一个脚注让读者猜。

## 第五步：撰写成稿 + 写入真正 Word 脚注

**用户要求"脚注"时，只允许 `word/footnotes.xml` + `w:footnoteReference`。**

禁止：尾注、文末注释、页脚手写来源、手工"①②③"、Unicode 上标模拟、括号 `[1]` 冒充。

### 路径 A（推荐）：from-markdown 内联 GFM 脚注

LegalWork 的 `document_skill_execute`（kind=docx, operation=from-markdown）原生支持 GFM 脚注：正文 `[^1]` + 文末 `[^1]: 参见……`，worker 自动生成真脚注。适用于从零撰写。

### 路径 B（已有 DOCX 补脚注/精细控制）：独立脚本

当原稿是已有 DOCX、需在不重建整篇的前提下补脚注，或需审计时：

1. 正文已有占位标记（`[[FN001]]`）。
2. `python scripts/insert_true_legal_footnotes.py input.docx notes.json output.docx` 插入真脚注。
3. `python scripts/audit_notes.py output.docx` 审计脚注/尾注结构。
4. `python scripts/assert_true_footnotes.py output.docx` 硬性验收。

**脚本解释器**：必须用 LegalWork 自带的 office-runtime Python（含 lxml、python-docx），不要用系统 python3。优先读 `LEGALWORK_OFFICE_PYTHON`；为空则探测 `resources/office-runtime/python/bin/python3`（dev）→ `<app>/Contents/Resources/office-runtime/python/bin/python3`（打包）。

### 读取已有 DOCX 脚注（修改模式必读）

- `read` 工具读 docx 只能得到正文（mammoth 提取），**读不到脚注**。
- 看脚注/尾注结构：`python scripts/audit_notes.py <docx>`。
- 提取脚注**文本**：bash + office-runtime Python 解包 `word/footnotes.xml`。
- 禁止用 read 读 `<docx>/word/footnotes.xml` 这类"docx 内部部件路径"（会报 ENOTDIR）。
- 原稿已有脚注时：复制原脚注格式、新 ID 用 `max(positive IDs)+1`、不重建整篇、不动原脚注。

## 第六步：结构验收

```bash
python scripts/audit_notes.py output.docx
python scripts/assert_true_footnotes.py output.docx
```

硬性验收：新增引注均为 `w:footnoteReference`；`word/footnotes.xml` 存在；引用 ID 与定义一一对应；未新增 `w:endnoteReference`；脚注数 = 引注台账数；脚注文字非空。

## 第七步：引注格式核查（可选但推荐）

成稿后，按第二节的引注核查工作流，对全文脚注逐条核查格式是否符合《法学引注手册》。新增脚注和原有脚注都核查。

---

# 二、引注核查工作流

用于核查 .docx 文件脚注引注格式是否符合《法学引注手册》（2025版），以修订模式修正格式错误、加蓝色批注。**只修改格式，不修改内容。**

支持中文引注、英文引注；不支持日文、法文、德文等其他语言。

## 工具依赖

```bash
pip install python-docx lxml
```

## 工作流程

### 第一步：提取脚注

```bash
python citation/scripts/docx_parser.py <论文.docx> -o footnotes.json
```

### 第二步：逐条核查

读 `footnotes.json`，对每条脚注：

#### 2a. 判断是否为引注

脚注分"引注类"（含文献出处，需核查）和"说明类"（纯解释，跳过）。引注脚注中混有说明文字时，**先分割**，只核查引注部分。

#### 2b. 判定语言

含 CJK 字符 → 中文引注；不含 CJK 且英文字母开头 → 英文引注；其他语言提示"暂不支持核查"。

#### 2c. 判定类型

中文：网络文献 → 再次引用 → 司法案例 → 法律文件 → 古籍 → 学位论文 → 报纸 → 文集 → 期刊 → 图书 → 未知。
英文：网络 → 再次引用 → 案例 → 期刊 → 图书。
判定依据见 `citation/references/reference-index.md` 与 `citation/scripts/citation_checker.py`。

#### 2d. 查找对应规则

| 类型 | 规则文件 |
|------|---------|
| 通用 | `citation/references/rules-general.md` |
| 中文图书 | `citation/references/rules-chinese-books.md` |
| 中文期刊/报纸/文集 | `citation/references/rules-chinese-articles.md` |
| 中文网络 | `citation/references/rules-chinese-internet.md` |
| 中文未发表 | `citation/references/rules-chinese-unpublished.md` |
| 中文法律 | `citation/references/rules-chinese-legal.md` |
| 中文案例 | `citation/references/rules-chinese-cases.md` |
| 英文 | `citation/references/rules-english.md` |
| 再次引用 | `citation/references/rules-repeated-citation.md` |

#### 2e. 逐条核查格式

重点检查（详见 `reference-index.md` 反查表）：作者后缺冒号、书名未用《》、缺"载"字、缺年份、页码缺"第/页"、译作缺国籍译者、国籍括号应 [ ]、网络文献缺日期、文号年份应〔〕、案号年份应（）、中英标点混用、英文斜体/卷号/See 等。

**核查原则**：只报告格式错误，不质疑内容；手册未规定不强求；同一引注多错全列；标注条款编号。

### 第三步：生成修正数据

格式见 `citation/CORRECTIONS_SCHEMA.md`。核心字段：`footnote_id`、`rule`、`error_type`、`old_text`（必须是脚注中实际存在的文本）、`new_text`、`reason`。只替换格式相关，不改文献内容。

### 第四步：报告核查结果

应用修改前，先向用户报告摘要：脚注总数、引注脚注数、说明脚注数（跳过）、发现错误数、涉及脚注数、错误类型分布。列出每条错误，询问确认。

### 第五步：备份并应用修订

**安全原则：任何时候不修改用户原始文件。始终在副本上工作。**

1. 备份：`copy <论文.docx> <论文_备份.docx>`
2. 用户确认后：`python citation/scripts/docx_revisor.py <论文.docx> -c corrections.json -o <论文_已修订.docx>`
3. 交付两个文件：备份 + 已修订（含修订模式 + 蓝色批注）。

### 第六步：输出结果

告知输出路径、修订数量、批注数量，提示在 Word 打开查看修订模式与批注。

## 注意事项

1. 只改格式（标点、连接词、括号、格式标记），不改文献名称、作者、出版社等实质内容。
2. 说明性文字不核查。
3. 一条脚注多个引用的逐个核查。
4. 外文文献优先中译本（手册第95条）。
5. 类型模糊时标"建议人工复核"。
6. 同一错误重复出现，逐条列出不合并。

---

# 3. 引注格式：默认 house style

除非用户/学校/期刊另有要求，默认中文法学论文页下注释制。完整模板见 `references/legal_citation_style.md`（撰写用）与 `citation/references/`（核查用）。

基础形式：

- 期刊论文：`参见张三：《论××》，载《法学研究》2025年第3期，第45—47页。`
- 专著：`参见张三：《刑法总论》，法律出版社2024年版，第128—130页。`
- 译著：`参见〔德〕克劳斯·罗克辛：《德国刑法学总论》第1卷，王世洲译，法律出版社2005年版，第88页。`
- 学位论文：`参见张三：《××研究》，中国政法大学2023年博士学位论文，第56—58页。`
- 案例：`参见××人民法院（2024）×刑终×号刑事判决书。`
- 网络资料：`参见最高人民法院：《××》，载最高人民法院网站，2026年3月1日发布，最后访问日期2026年8月11日。`
- 再次引用：`参见张三，前引文，第52页。` 不自动用 ibid./op. cit.。

---

# 4. AI 写作风格硬规则

详见 `references/argumentation_and_ai_style.md`。

避免：过度对仗；每个标题"××性与××需求"；"首先其次再次最后"机械连用；"由此可见/不难发现"代替理由；每段结尾"提升治理现代化水平"；无依据的"显著/普遍/日益/必然"；把简单判断拆成同义反复；每段"有学者指出"。

优先：短标题；一段解决一个问题；文献进入论证而非堆砌；能说"尚不足以证明"不说"充分说明"；能说"可能构成"不说"必然导致"。

---

# 5. 交付前硬性清单

## 学术内容

- [ ] 中心论题明确、可争论；
- [ ] 新增命题有来源或明确属于本文分析；
- [ ] 引用页码真正支持相邻命题；
- [ ] 直接引语与转述区分；
- [ ] 旧文献未被误写成现行法；
- [ ] 学者建议未伪装成法律规定；
- [ ] 经验性结论没超出样本范围；
- [ ] 没有"危害严重→当然犯罪化"跳跃；
- [ ] 没有"总体从严→普遍重判"跳跃；
- [ ] 标题没有刻意对仗和 AI 套路。

## 引注

- [ ] 该引的都引了；
- [ ] 不需要引的没乱加脚注；
- [ ] 每条脚注有明确锚点；
- [ ] 页码为具体支持页；
- [ ] 期刊/书籍/论文/案例/规范格式统一；
- [ ] 二手转引注明"转引自"；
- [ ] 引注格式符合《法学引注手册》；
- [ ] 引注核查已通过或已列出待修正项。

## Word 技术

- [ ] `word/footnotes.xml` 存在（有脚注时）；
- [ ] 正文使用 `w:footnoteReference`；
- [ ] 未误生成 `w:endnoteReference`；
- [ ] 脚注未写入页脚；
- [ ] 无手工 Unicode 上标假脚注；
- [ ] footnote IDs 引用↔定义一一对应；
- [ ] separator / continuationSeparator 完整；
- [ ] relationships / content types 正确；
- [ ] 脚注显示在当页页底。

---

# 6. 附带文件

## 撰写/修改

- `references/legal_citation_style.md`：中文法学引注格式细则（撰写用）；
- `references/docx_true_footnotes.md`：真脚注 OOXML 从零实现；
- `references/source_review_and_evidence.md`：文献阅读与证据矩阵；
- `references/argumentation_and_ai_style.md`：论证和 AI 表达审查；
- `references/word_revision_workflow.md`：在 DOCX 上安全修改；
- `templates/evidence_matrix.md`：命题—来源—页码矩阵；
- `templates/citation_ledger.md`：脚注台账；
- `scripts/audit_notes.py`：检查脚注/尾注结构；
- `scripts/insert_true_legal_footnotes.py`：从零创建真脚注；
- `scripts/assert_true_footnotes.py`：硬性验收；
- `scripts/test_true_footnotes.py`：自测脚本。

## 引注核查（整合自 chinese-legal-citation）

- `citation/citation-skill-SKILL.md`：原核查 skill 完整说明；
- `citation/CORRECTIONS_SCHEMA.md`：修正数据格式规范；
- `citation/references/`：10 个《法学引注手册》规则库（通用/图书/文章/网络/未发表/法律/案例/英文/再次引用/索引）；
- `citation/scripts/docx_parser.py`：脚注提取；
- `citation/scripts/docx_revisor.py`：修订模式修改；
- `citation/scripts/citation_checker.py`：引注分类辅助。
