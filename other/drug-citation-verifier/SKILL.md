---
name: drug-citation-verifier
description: Cite-or-Block 架构下的药名 cross-check 原子 skill。给定报告文本与 .cache/<slug>/sources/,扫描每个药品提及 → 找最近 citation 锚点 → 核对锚点指向的源里是否真的提到了此药(通用名 + 商品名)。无字典、无 fallback、源里没 = critical。
---

# drug-citation-verifier (A5')

> **替代作废的 `nmpa-drug-registry-lookup`(commit `e7cfb83`,违反 P0)。**

Cite-or-Block 架构下的**药名 cross-check 原子 skill**。本 skill 是 A11
`citation-anchor-resolver` 之上的薄包装,专注一件事:

> 报告里写了药名 X + 引用了锚点 Y → 锚点 Y 指向的源里,真的有 X 吗?

源里有 = 通过。源里没 = critical violation,无论 X 是 2018 年的老药、
2026 年新批的药、还是 LLM 编造的药。

---

## Iron Law (P0 守护)

**绝不维护药品字典。**

本 skill **不知道**也**不需要知道**"哪些药存在"。它只做一件事:
**报告里的药名 X + 引用锚点 Y** → 验证 Y 指向的源里是否真的提到了 X。

源里没 → fail。无论 X 是 2018 年的老药、2026 年新批的药、或编造的药。

### 唯一允许的"内置规则"

- **中文药名后缀**(`替尼/单抗/阿克/沙星/霉素/康唑/芬净/他汀/...`)— 用于**抽取**疑似药名
- **英文药名后缀**(`-tinib/-mab/-statin/...`)
- **上下文关键词**(`商品名/剂量/I 级推荐/...`)— 用于关联药名与上下文

这些是"中文医药命名学",**不是**"已知药品列表"。任何符合后缀的字符串都
视为药提及,然后**必须核对源**才能判定真伪。

完整后缀规则表见 [`references/extraction-heuristics.md`](references/extraction-heuristics.md)。

### 反例(违反 P0)

```python
# WRONG — 任何具体药名出现在 .py 源代码 = P0 violation
KNOWN_DRUGS = {"洛拉替尼": "Lorlatinib", "克唑替尼": "Crizotinib", ...}
DRUG_REGISTRY = [...]
_known_drugs_fallback = {...}
```

这类代码 = 立刻停下来重设计。本 skill 的 watchdog 测试
(`tests/test_drug_citation_verifier.py::test_no_hardcoded_drug_dict_in_source`)
会扫描 `scripts/*.py` 拒绝任何具体药名出现。

---

## 何时使用

| 场景 | 使用本 skill 吗? |
|------|-------------------|
| 报告内容生成完毕,需要 cross-check 药名是否真有出处 | ✅ |
| Step 8 审计阶段,逐段 scan critical violation | ✅ |
| 不知道某药是否存在,想"查一下" | ❌(本 skill 不查表) |
| 抓指南后想入药品库 | ❌(本架构不入库,只存原文) |

---

## 核心 API

### `verify_drug_mentions_in_text(text, sources_dir) -> dict`

```python
from pathlib import Path
import sys

# 1) 加载 A11(citation-anchor-resolver)
A11 = Path.home() / ".claude" / "skills" / "citation-anchor-resolver" / "scripts"
sys.path.insert(0, str(A11))

# 2) 加载本 skill
A5 = Path.home() / ".claude" / "skills" / "drug-citation-verifier" / "scripts"
sys.path.insert(0, str(A5))

from verifier import verify_drug_mentions_in_text

text = """
ALK 阳性 NSCLC 一线推荐洛拉替尼(商品名:博瑞纳)。
[guideline:CSCO-2024-NSCLC:§5.5.2]
"""
sources_dir = Path(".cache/lung-cancer-alk-2026/sources")

result = verify_drug_mentions_in_text(text, sources_dir)

# {
#   "ok": True / False,
#   "drug_mentions": [{
#       "text": "洛拉替尼",
#       "brand_in_context": "商品名:博瑞纳",
#       "citation": "[guideline:CSCO-2024-NSCLC:§5.5.2]",
#       "verified": True,
#       "missing_in_source": [],
#       "reason": "all keywords matched",
#       "severity": "none",
#   }, ...],
#   "violation_severity": "none" | "warning" | "critical",
# }
```

### 工作流

1. `_drug_extract.extract_drug_mentions_with_context(text)` —
   命名学规则抽取所有"疑似药提及"(含括号内的商品名/英文名)
2. `parse_citations_in_text(text)`(A11)— 找文中所有 citation 锚点
3. `_citation_match.find_nearest_citation(mention, citations, text)` —
   就近匹配:同句最优,同段次之,跨段则视为 missing
4. 对每个 mention:
   - 没找到 citation → `critical`(无来源)
   - 有 citation → A11.`verify_claim_against_source(name+brand, citation, sources_dir)`
   - `verified=False` → `critical`(出处不支持)
5. 计算 `violation_severity`:any critical → critical;all verified → none

---

## 严重级别

| Severity | 含义 | 报告生成行为 |
|----------|------|--------------|
| `none`   | 所有药提及都核对通过 | 通过 |
| `warning`| 有非关键问题(本版暂未启用,预留) | 警告 |
| `critical` | 任一药提及无 citation 或源不支持 | **阻断**,LLM 重写 |

---

## 设计取舍

### 为什么不用 LLM 抽取?

- LLM 抽取需要联网 + 推理时间,在审计 hot path 上昂贵
- 命名学规则 100% deterministic,易测试
- 即便有"漏抽"(如未在后缀表中的特殊命名),
  下游的 A1 / 内容生成层会再做语义级校验

### 为什么不允许"已知药 → 商品名"映射?

- 一旦允许,就会演化成全药品库(P0 violation)
- 商品名是国家/年代依赖的(如同药在中美商品名不同)
- 正确做法:商品名应该**写在指南/审批文件里**,从源里学,不预存

---

## 依赖

- ✅ A11 `citation-anchor-resolver`(commit `c2c97b3`)— 必须先安装
- ❌ **不**依赖 `nmpa-drug-registry-lookup`(违反 P0,作废)

---

## 故障模式

详见 [`references/failure-modes.md`](references/failure-modes.md)。

常见 4 种:

1. **报告写药名但无 citation** → critical(无来源)
2. **citation 解析不到源**(锚点格式坏 / 文件丢失) → critical
3. **源里只有通用名没商品名,但报告写了商品名** → critical(missing_in_source)
4. **LLM 编造的药名(符合命名学但源里没)** → critical

---

## 相关 Skill

| Skill | 关系 |
|-------|------|
| `citation-anchor-resolver` (A11) | 本 skill 的依赖,提供锚点解析 |
| `content-verification-layer` (A6') | 本 skill 的下游协调层,统管全报告 cross-check |
| `nmpa-drug-registry-lookup` | **作废**(违反 P0,保 git 历史作反例) |
