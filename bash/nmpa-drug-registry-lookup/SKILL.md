---
name: nmpa-drug-registry-lookup
description: 中国药品权威数据库查询 — NMPA(国家药监局) + CDE(药品审评中心) + DrugBank(英文名/ATC) + PubChem(化学结构) 多源融合,提供(通用名 ↔ 商品名 ↔ 英文名 ↔ 适应症 ↔ NMPA 批文号 ↔ 上市日期)精确映射。Make sure to use this skill whenever the user mentions 药品名 / 通用名 / 商品名 / NMPA / 国药准字 / 药监局 / CDE / drug brand name / generic name / drug registry / pharmaceutical lookup / drug verification / 药物核验 / 商品名对应 / drug cross-check / drug authority lookup. 在任何 medical / market-sizing / clinical / disease-research 报告生成阶段,**所有药品提及必须先调 lookup_drug() 验证**,严禁 LLM 凭训练记忆拼凑通用名↔商品名↔英文名对应关系。LLM 训练截止后药企会更换商品名、新药持续上市,记忆完全不可信。Iron Law:lookup 返回 None → 调用方必须 raise UnverifiedDrugError,不允许 fallback 到记忆。免费公开数据源,跨平台:Claude Code / Codex / Gemini CLI 三端均可 auto-trigger,实现仅依赖 httpx + beautifulsoup4 标准生态,不绑定任何厂商 SDK。
license: MIT
---

# nmpa-drug-registry-lookup · 中国药品权威 Registry

## 一句话定义

中国市场所有报告里的药品提及,都从此 skill 拿权威记录(NMPA + CDE + DrugBank + PubChem 多源融合);**LLM 不允许凭记忆改写药品名**。

---

## Iron Law(违反此条 = 报告作废)

**任何写入报告的药品名(通用名 / 商品名 / 英文名),必须通过 `lookup_drug()` 验证。**

LLM 不允许凭训练记忆拼凑通用名↔商品名↔英文名对应关系 — 因为:

1. 药企会更换商品名(如同一通用名在不同厂家有多个商品名)
2. 新药持续上市,LLM 训练截止日期之后的数据**完全不可信**
3. 中国市场命名经常与全球市场不同(如:Lorlatinib 中国商品名"博瑞纳",国外"Lorbrena")
4. 一个药名错位 = 整份报告地基塌方(治疗推荐错 / GRADE 错 / LP 错 / 市场份额测算错)

**唯一允许的姿势**:

```python
from nmpa_drug_registry_lookup.scripts.registry import lookup_drug, UnverifiedDrugError

rec = lookup_drug("洛拉替尼")
if rec is None:
    raise UnverifiedDrugError("洛拉替尼 not in NMPA registry — refuse to write to report")

# 报告里写药名时,通用名和商品名都从 record 取,不要手输
generic_zh = rec.generic_name_zh   # "洛拉替尼"
generic_en = rec.generic_name_en   # "Lorlatinib"
brand_zh   = rec.brand_names_zh[0] # "博瑞纳"
```

**绝不允许**:

```python
# 错误!LLM 凭记忆
report_html += "<p>洛拉替尼(商品名:赛可瑞)...</p>"   # 赛可瑞实际是克唑替尼!
report_html += "<p>布加替尼(商品名:博瑞纳)...</p>"   # 博瑞纳实际是洛拉替尼!
```

---

## 何时调用

- 任何**报告生成阶段**(market-sizing / 治疗方案 / 决策树 / 市场份额测算)涉及具体药品名
- 用户问"X 药的通用名是什么?"、"Y 药什么时候在中国上市?"、"Z 药 NMPA 批文号是多少?"
- `medical-evidence-grading` / `disease-market-sizing-orchestration` 调用方需要药名锚定
- 报告生成完毕,跑 `cross_check_drug_mentions()` 全文扫描,catch LLM 偷偷凭记忆改写的药名

## 何时不调用

- 文献检索本身(给 PubMed query 时)— 不需要,query 自由文本即可
- 询问药物机制 / 靶点(用 `pubtator-entity-search` 抓基因/通路)
- 询问临床试验状态(用 `clinical-trials-v2`)

---

## 与其他 skill 的协作关系

```
                        ┌─ pubmed-eutils(召回主力)
召回层 ───┬─────────────┤
          │             └─ europepmc-search
          │
          │             ┌─ cn-clinical-guidelines-fetch(指南权威)
权威层 ───┼─────────────┤
          │             └─ ★ nmpa-drug-registry-lookup(本 skill · 药品权威)
          │
          ▼
报告生成层 ───  所有药品名引用 → lookup_drug() / cross_check_drug_mentions()
```

**调用顺序**:
1. orchestration 解析疾病 → fetch_chinese_guidelines() 拿指南治疗推荐表
2. 用指南里提到的药品 → lookup_drugs_batch() 建立本疾病 drug_registry.json
3. 报告生成时所有药品名引用从 drug_registry.json 取(LLM 禁止改写)
4. 报告草稿出来 → cross_check_drug_mentions(html) 全文扫描,critical 严重性 → raise

---

## 核心函数签名

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DrugRecord:
    """中国药品权威记录。frozen 防止 LLM 修改。"""
    generic_name_zh: str         # 通用名(中文,首选 NMPA 命名)
    generic_name_en: str         # 通用名(英文,DrugBank/INN)
    brand_names_zh: tuple[str, ...]    # 商品名列表(中国市场,可能多个生产厂家)
    brand_names_en: tuple[str, ...]    # 商品名列表(全球)
    nmpa_approval_no: str        # NMPA 批准文号(如 国药准字 H20180123 / 进 J20180012)
    first_approval_date_cn: str  # 中国首次上市日期 ISO yyyy-mm-dd
    indications_cn: tuple[str, ...]    # 适应症(中文)
    atc_code: str                # ATC 分类(如 L01ED05 = 抗肿瘤 ALK 抑制剂)
    target: str                  # 靶点(对靶向药,如 "ALK")
    drug_class: str              # 类别(如 "三代 ALK-TKI")
    sources: tuple[str, ...]     # 来源 URL,可追溯


class UnverifiedDrugError(Exception):
    """lookup 失败时调用方应 raise — 拒绝写入报告。"""


def lookup_drug(
    name: str,                   # 任意名称(通用/商品/英文,模糊匹配)
    market: str = "CN",
    cache_dir: Path | None = None,
) -> DrugRecord | None:
    """单药查询。匹配优先级:
    1. 已知 fallback dict 精确命中(NMPA 网站抓不到时的兜底)
    2. NMPA 精确通用名
    3. NMPA 商品名
    4. DrugBank generic_name
    5. PubChem 化学名 fallback

    None = 该药不在权威数据库 → 调用方必须 raise UnverifiedDrugError。
    """


def lookup_drugs_batch(
    names: list[str],
    market: str = "CN",
    cache_dir: Path | None = None,
) -> dict[str, DrugRecord | None]:
    """批量查询。返回 {name: DrugRecord or None}。"""


def cross_check_drug_mentions(
    text: str,                   # 报告 HTML / Markdown 草稿
    market: str = "CN",
    cache_dir: Path | None = None,
) -> dict:
    """扫描文本里所有疑似药品名,逐个 lookup,返回错误清单。

    Returns:
        {
            "ok": bool,
            "verified_drugs": [...],       # 命中权威数据库的药名
            "unverified_drugs": [...],     # 在数据库找不到 → 必须修
            "name_mismatches": [           # 通用名/商品名混用错位(critical)
                {"text_uses": "赛可瑞", "claimed_as": "洛拉替尼",
                 "actual_generic": "克唑替尼", "evidence_source": "NMPA"},
                ...
            ],
            "violation_severity": "none" | "warning" | "critical",
        }

    严重性规则:
    - 任何 name_mismatches 非空 → critical(LLM 把 A 药写成 B 药商品名)
    - 仅 unverified_drugs 非空 → warning(可能是新药 / 仿制名)
    - 全部 verified → none
    """
```

---

## 数据源(免费公开)

| 来源 | 提供 | 抓取方式 |
|-----|------|---------|
| **NMPA 国家药监局** (`nmpa.gov.cn`) | 通用名 / 批文号 / 适应症 / 上市时间 (权威 I 级) | REST + WebFetch + bs4 |
| **CDE 药品审评中心** (`cde.org.cn`) | 临床试验阶段 / 适应症详情 | WebFetch |
| **DrugBank**(免费学术) | 英文名 / ATC code / mechanism | API / scrape |
| **PubChem**(NIH) | 化学结构 / IUPAC / 同义词 | REST(`pug.ncbi.nlm.nih.gov/rest/pug`) |
| **NCBI Gene** | 靶点基因(已通过 pubtator-entity-search 间接) | 复用 |

**fallback 兜底**:NMPA 网站反爬严重时,`scripts/_known_drugs_fallback.py` 含一份手工核验的常用药字典,每条都有 NMPA 公开页 URL 引用作来源。

---

## 失败模式(8 条)

| # | 症状 | 原因 | 修复 |
|---|------|------|------|
| 1 | lookup 返回 None | 药品不在 NMPA(可能仿制名 / 进口未上市 / 拼写错)| 让用户确认是否仍写入,标 unverified;不允许 LLM 凭记忆补 |
| 2 | 同一通用名多个商品名 | 多厂家(如阿仑膦酸钠) | brand_names_zh 列出全部,不要任选一个 |
| 3 | 通用名↔商品名错位(LLM 偷偷脑补) | LLM 训练截止后数据老化 | `cross_check_drug_mentions` 全文扫描,critical 级 raise |
| 4 | NMPA 网站抓取失败(反爬) | nmpa.gov.cn 改版 / 验证码 | 降级:cache → fallback dict → 报错 |
| 5 | 同一英文名对应多个中文音译 | 早期未规范化 | NMPA 通用名为唯一权威,其他作 alias |
| 6 | DrugBank 拒绝学术抓取 | 反爬升级 | 该字段标 None,不阻塞主流程(NMPA 字段是必需) |
| 7 | LLM 在 prompt 里"脑补"通用名 | 训练数据过时 | 任何 grade_evidence / LP 阶段都强制 lookup,不接受 LLM 直出 |
| 8 | 进口药批文号格式 vs 国产不同 | NMPA 编号规则:H/J/Z/S 前缀 | 不要自行拆解,作为 opaque string 存储 |

---

## 跨平台

- **Python**: 3.10+(用 PEP 604 `X | None` 类型注解)
- **依赖**: `httpx`, `beautifulsoup4`, 可选 `pypdf`(适应症附件解析)
- **测试**: `python -m pytest`(Windows 用 `C:\Python3\python.exe -m pytest`,不要用 `python3` stub)
- **Windows GBK 终端兼容**: 测试入口加 `sys.stdout.reconfigure(encoding="utf-8")`
- **Cache**: JSON 文件 `<cache_dir>/drug_registry.json`,TTL 7 天;SQLite 是 future work
- **不联网测试**: 测试用 `tests/fixtures/nmpa_responses/*.html` 预录制响应,绝不在 CI 里直连 NMPA

---

## 调用方典型用法

### A. 单药 lookup

```python
from nmpa_drug_registry_lookup.scripts.registry import lookup_drug, UnverifiedDrugError

rec = lookup_drug("洛拉替尼")
if rec is None:
    raise UnverifiedDrugError("洛拉替尼 not in NMPA registry — refuse to write to report")

print(rec.generic_name_en)    # "Lorlatinib"
print(rec.brand_names_zh)     # ("博瑞纳",)
print(rec.atc_code)           # "L01ED05"
print(rec.first_approval_date_cn)  # "2022-04-29"
```

### B. 批量预热(orchestration 在 Step 0b 调)

```python
from nmpa_drug_registry_lookup.scripts.registry import lookup_drugs_batch

key_drugs = ["克唑替尼", "阿来替尼", "塞瑞替尼", "恩沙替尼",
             "布加替尼", "洛拉替尼", "伊鲁阿克", "依奉阿克"]
results = lookup_drugs_batch(key_drugs)

missing = [d for d, r in results.items() if r is None]
if missing:
    raise UnverifiedDrugError(f"NMPA registry missing: {missing}")

# 写入 .cache/<slug>/drug_registry.json,后续报告生成阶段 LLM 必须从此取
```

### C. 报告生成完毕全文扫描

```python
from nmpa_drug_registry_lookup.scripts.registry import cross_check_drug_mentions

result = cross_check_drug_mentions(report_html)
if result["violation_severity"] == "critical":
    # LLM 把 A 药写成 B 药商品名 — 必须重生成
    raise OrchestrationError(f"drug name mismatches: {result['name_mismatches']}")
elif result["violation_severity"] == "warning":
    # 仅有 unverified(可能是新药)— §0 加红色警告
    add_section_zero_warning(result["unverified_drugs"])
```

---

## 引用与下游

- 上游: `cn-clinical-guidelines-fetch`(指南先告诉本 skill 该疾病有哪些药)
- 下游: `disease-market-sizing-orchestration`(在内容生成阶段强制锚定)、`content-verification-layer`(report-level cross-check 的事实审计层)
- 同层互补: `pubtator-entity-search`(基因靶点)、`pubmed-eutils`(文献召回)

参考文档:
- `references/nmpa-fetch-api.md` — NMPA 网站结构 + 抓取策略
- `references/drugbank-integration.md` — DrugBank 学术免费用法
- `references/failure-modes.md` — 8 失败模式详解
