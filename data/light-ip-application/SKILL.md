---
name: light-ip-application
description: 辅助软件著作权与专利申请。当用户需要做软著或专利材料时使用。软著：软件名称、功能说明、操作说明书、源代码整理、文档撰写、材料清单、流程、界面截图、功能模块说明、版本与完成日期。专利：判断是否可申发明/实用新型/外观，梳理技术问题、技术方案、有益效果、创新点、实施例、权利要求书与说明书草案、附图说明。最终文本须由专业代理人审核。
---

# 软著与专利申请辅助

## 重要声明（每次开头都提醒）
本技能产出为**草稿与辅助梳理**，不构成法律意见。软著/专利最终文本须由专业代理人或法律人员审核；材料不得虚构或夸大（联动 a10）。

## 软件著作权（登记机关：中国版权保护中心 CPCC，ccopyright.com）
软著只做**形式登记**，不审查代码质量/新颖性，确认权属与完成时间。
1. **软件命名**：全称+简称+版本号，规范可注册、体现功能；登记后不便更改，定稿前确认。
2. **功能说明**：软件用途、主要功能模块、运行环境、技术特点。
3. **操作说明书**：安装、配置、各功能操作步骤，配界面截图、功能模块说明。
4. **源代码整理**：前 30 页 + 后 30 页(连续、每页约 50 行;不足 60 页全交)、页眉含全称+版本、注释脱敏——**规则单一真相源见 db08 `databases/db08-ip-materials/resources_real.md` §2(带 last_checked + CPCC 指南 source_pointer),页数/行数口径提交前以 CPCC 当期指南核查**;脚本 `scripts/copyright_source_prep.py` 按此规则生成提交文本。
5. **文档**：用户手册或设计说明书，前 30 页+后 30 页规则同源码。
6. **材料清单核对**：登记申请表(系统生成)、源程序、文档、身份/营业执照、权属证明(合作/委托/职务开发需对应证明)。
7. **关键信息**：开发完成日期、首次发表日期(未发表可注明)、版本号、开发方式(独立/合作/委托/职务)、权利归属。
8. **流程与周期**：在线登记系统填报→提交→受理→审查(法定约 30 个工作日，可付费加急)→下发《计算机软件著作权登记证书》。
材料须真实对应、不得拼凑虚构。模板与审查重点见 db08。

## 专利
1. **可专利性初判**：是否属发明/实用新型/外观；新颖性、创造性、实用性初步判断；做查新检索（见下）。
2. **技术交底梳理**：要解决的技术问题 → 现有技术缺陷 → 本发明技术方案 → 有益效果 → 创新点。
3. **权利要求书草案**：
   - 独立权利要求记载解决问题的**全部必要技术特征**，构成最大保护范围。**两种撰写法二选一、别混用**（模板 claims_template.md 给了两个正确范式 + 常见错误警示）：①**单部分法**（方案整体新、无明确最接近现有技术）"一种…方法，包括：S1…S3"，**不写"其特征在于"**；②**两部分法**（改进型）"一种…方法，包括[前序：与现有技术共有特征]；其特征在于，[特征部分：仅区别特征]"。**最常见致命错误：把共有特征塞进"其特征在于"之后、或单部分法里硬加"其特征在于"——代理师直接打回。**
   - 从属权利要求用"根据权利要求 N 所述的…，其特征在于…"逐层附加限定；引用多项用"或"，不得引用编号更大的项。
   - 软件类常用组合布局：方法 + 装置/系统 + 计算机可读存储介质。
   - 须**以说明书为依据**；避免功能性/含糊措辞("约""左右")；术语前后一致；多项独立权利要求须属同一总发明构思(单一性)。
4. **说明书草案**(须**充分公开**，使本领域技术人员可实现)，按审查指南顺序：技术领域 → 背景技术(现状+对比文件+客观缺陷) → 发明内容(技术问题/技术方案/有益效果，效果尽量可量化或给机理) → 附图说明(逐图+标记清单) → 具体实施方式(≥1 个实施例，软件类给流程/模块交互/伪代码级描述使方案可重现)。每个权利要求特征都要在说明书找到支持。
5. **附图**：流程图/结构图/示意图，按专利制图规范交 m11 绘制——具体规范（图号编排、附图标记线不交叉、黑白线条图为原则不得着色、流程图/框图与权利要求术语对应）见 m11(light-figure-drawing) `references.md`「专利附图规范」节。专利附图走黑白矢量线条链路，不套论文数据图的配色/样式。**方法流程图/装置结构框图可用 Draw.io MCP** 出 diagram-as-code（`.drawio` 即 XML，黑白线条、可程序化生成、便于按代理人意见反复改稿、导出矢量），正合专利附图要求；输出后仍按上述规范核（标记线、术语与权利要求一致）。配置见 README 推荐 MCP 表。

### 查新检索（在先技术）实操
按数据范围选检索系统（**端点/字段码/认证/限流的逐条硬信息见 `references.md`，此处只给选用指引**）：

| 范围 | 系统 | 要点 |
|---|---|---|
| 中国专利（权威） | CNIPA 专利检索及分析 | 需登录免费、无公开 API，高级字段+法律状态筛选 |
| 全球免费 | Google Patents | URL 参数检索；大规模走 BigQuery 公开数据集 |
| PCT/跨语言 | WIPO PATENTSCOPE | 字段码 + CLIR，中文查外文在先技术 |
| 欧洲机读 | EPO OPS API | OAuth2 + CQL，红绿灯节流 |
| 专利↔论文 | The Lens API | 专利与学术一体，可免费授权 |
| 美国 | USPTO（data.uspto.gov） | PatentSearch API，端点已迁 ODP |
| 非专利文献 | OpenAlex | 补论文型在先技术（接入口径见 m01） |

> **脚本能力边界（诚实声明，避免读成"七源都能程序化查"）**：上表里 `scripts/patent_search.py` 真正能**程序化取数**的只有 **OpenAlex（论文型 NPL，非专利库）**；The Lens / EPO OPS / USPTO ODP 脚本只**构造请求体**（需你自带凭证才能发起，无凭证实测 401）；**CNIPA / Google Patents / WIPO PATENTSCOPE 无脚本，须人工登录网页或走 BigQuery 检索**。即专利库的真实在先技术检索仍以人工网页/机构账号为主，脚本是 NPL 补充 + 带凭证时的请求脚手架。

- 检索证据(命中文献号/日期/相关段落)随交底书留档；FTO/无效结论须代理师/律师定，本技能不下法律结论。

## 可运行资产（scripts/ 与 templates/，均已 python 跑通/curl 实测）
- `scripts/patent_search.py`：在先技术检索辅助。OpenAlex `/works` 做 **NPL（非专利文献）检索**（2026 起需免费 key，经 `--api-key`/环境变量 `OPENALEX_API_KEY` 透传，接入口径见 m01 真相源；`per_page` 上限 200），并为 The Lens / EPO OPS / USPTO ODP **构造请求体**（这三者需自带凭证，实测均 401=需鉴权）。**注：脚本本身不直接查专利库，专利库实查须人工网页或带凭证发起（见上"脚本能力边界"）。**
  - `python scripts/patent_search.py "关键词" --from-year 2015 --per-page 10 --mailto you@x.com --api-key $OPENALEX_API_KEY`
  - `python scripts/patent_search.py --print-adapters`（打印专利库请求模板）
  - **`python scripts/patent_search.py "关键词" --free-urls --cpc H01M --before 2020-01-01`**（无 API key 主力查新路径：生成 CNIPA pss-system / Google Patents / Lens / WIPO 的"点开即用"高级检索链接，Google Patents 带 before:priority 卡优先日、CPC 收敛——弥补无凭证拿不到专利库结果的空白）
  - `python scripts/patent_search.py --selftest`（离线自测，不联网）
- `scripts/copyright_source_prep.py`：软著源码材料整理。按"50 行/页、≤60 页全交否则前 30+后 30 页、页眉含全称+版本、注释脱敏"规则生成提交文本。**脱敏覆盖邮箱/手机/密钥赋值/PEM 私钥/IPv4/长 base64-hex 串，输出末尾报命中数 + 明示"仅正则粗筛不保证完备，须人工复核"**（不给"已彻底脱敏"错觉）；页数另报"有效代码行数"（排除 FILE 标记行/空行，避免虚增页数误判够不够 60 页）。
  - `python scripts/copyright_source_prep.py --src <代码目录> --name "全称" --version V1.0 --out submit_source.txt`
  - `python scripts/copyright_source_prep.py --selftest`
- `templates/disclosure_template.md`：技术交底书模板。
- `templates/claims_template.md`：权利要求书草案（方法+装置+介质组合布局）。
- `templates/specification_template.md`：说明书草案（按审查指南顺序）。
- `templates/copyright_checklist.md`：软著材料清单核对表。

## 产出
软著：全套草稿材料（套 `templates/copyright_checklist.md`）+ 源码整理（`copyright_source_prep.py`）+ 截图整理建议。
专利：可专利性分析 + 交底书（`disclosure_template.md`）+ 权利要求草案（`claims_template.md`）+ 说明书草案（`specification_template.md`）+ 检索证据（`patent_search.py`）+ 附图清单 + "需代理人审核"标注。

落盘工件名（CONVENTIONS §6.1，下游 orchestrator/a08 按名调度）：专利 `ip/disclosure_draft.md` + `ip/claims_draft.md` + `ip/specification_draft.md`；软著 `ip/copyright_package/`。

## 衔接
技术内容取自 m05/a03/a04/m07；软著功能说明与专利背景技术/发明内容可复用论文(m07)对应段落——专利的"要解决的技术问题/有益效果"与论文 Introduction/Results 高度同源，软著功能说明亦可借论文方法与结果段。附图交 m11（专利附图规范见 m11 references「专利附图规范」节，黑白线条+图号标记规范）；与论文/系统保持一致(a07)；材料入 db09。检索与权属风险上报 a10。交付前过 a08(light-self-review)自检闸门。

---
检索工具真实端点/参数、撰写规范要点与已知坑详见 references.md。
