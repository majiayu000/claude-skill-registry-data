---
name: jurisrank
description: >
  使用 JurisRank 进行阿根廷最高法院引用网络分析——一种经同行评审、
  带时间衰减的 PageRank 算法，用于衡量判例权威性。按引用影响力为先例
  排序、追踪学说演变并检测宪法漂移。
  已发表方法论：JCLLT（DOI: 10.47852/bonviewJCLLT62027951）。
  激活词：应引用哪些案例、先例排名、案例权威性、学说演变、阿根廷最高法院、
  CSJN 判例、引用网络、指导性案例、阿根廷法律检索。
command: /jurisrank <topic-or-case>
allowed-tools: Read, Write, WebFetch, Bash
when_to_use: >
  当您需要识别某个主题上最具权威性的阿根廷判例法、按引用影响力对竞争性
  先例排序、追踪阿根廷最高法院（CSJN）或联邦法院的学说如何演变，或验证
  对方律师引用的先例是否真正具有影响力或属于孤立案例时。
effort: medium
context: inline
metadata:
  author: "Adrián Lerer"
  license: "cc-by-4.0"
  version: "2026-05-13"
---

# JurisRank——阿根廷判例权威性分析

## JurisRank 是什么

JurisRank 是一种通过引用网络分析衡量阿根廷法院判决权威性的计算工具。其方法论**经同行评审**，发表于《计算法律与法律技术杂志》（Journal of Computational Law and Legal Technology）：

> Lerer, I.A. (2026). "Computational Detection of Constitutional Drift: Network Analysis and Semantic Measurement of Argentine Supreme Court Jurisprudence (1922–2025)."（宪法漂移的计算检测：阿根廷最高法院判例的网络分析与语义测量（1922-2025）。）*Journal of Computational Law and Legal Technology.* DOI: [10.47852/bonviewJCLLT62027951](https://doi.org/10.47852/bonviewJCLLT62027951)

**学术验证：** κ = 0.83 编码员间信度 · k 折交叉验证（k=5）· 73.2% 平均准确率 · 蒙特卡洛模拟（n=1,000）。

**许可：** 知识共享署名 4.0 国际版（CC BY 4.0）

---

## 三种算法

| 算法 | 用途 |
|-----------|---------|
| **JurisRank** | PageRank + 时间衰减——近期引用权重更高 |
| **RootFinder** | 祖源借用分析网络——追踪学说谱系 |
| **Legal-Memespace** | 主成分分析——映射多维学说 |

---

## 覆盖范围

- 阿根廷最高法院（CSJN）——1922 年至今
- 国家和联邦上诉法院（Cámaras nacionales y federales）
- 部分省级最高法院
- 阿根廷法院引用的相关国际先例

---

## 权威性分数解读

| 分数 | 含义 | 建议 |
|-------|---------|---------------|
| > 0.8 | 指导性案例——最高引用权威性 | 优先引用，附分数 |
| 0.6–0.8 | 广泛引用——先例权重强 | 引用并附分数 |
| 0.4–0.6 | 相关——中等权威性 | 引用并附说明 |
| < 0.4 | 有限权威性——孤立或异常案例 | 仅作参考 |
| 未找到 | 未检测到网络存在 | 声明无先例 |

---

## 用例

### 1. 为简报和备忘录选择判例
当多个案例涉及同一问题时，JurisRank 识别哪些在引用网络中承载最多权威性 → 按排序优先引用最有影响力的。

### 2. 学说演变分析
追踪 CSJN 或上诉法院在特定主题上的学说如何演变。识别最近判决是延续还是打破先前学说。

### 3. 对抗性判例尽职调查
验证对方律师引用的先例是真正具有权威性还是影响力低的孤立案例。

### 4. 宪法漂移检测
检测暗示学说侵蚀或重组的引用模式转变——JCLLT 论文的原始应用。

---

## 工作流

```
1. 识别要分析的主题或具体案例
2. 查询 JurisRank API：
   GET  https://api.jurisrank.com/v1/cases?query=<topic>
   POST https://api.jurisrank.com/v1/analyze-authority {"case_id": "..."}
3. 解读权威性分数和引用网络位置
4. 若需要学说演变，应用 RootFinder 进行谱系分析
5. 产出带引用建议的排序分析
```

---

## 反幻觉规则

JurisRank 按斯坦福法律 AI 基准（Magesh 等，2024）实施基于事实的验证：

**在将任何案例纳入分析之前：**
- 确认权威性分数 > 0.0（案例存在于网络中）
- 验证法域与事项的审理法院匹配
- 检查时间衰减：是否有被更多引用的后续判决取代了它？
- 验证案例确实支持该主张——而不仅是涉及该主题

**未经明确声明为未验证，绝不引用 JurisRank 网络中未找到的案例。**

---

## 输出格式

```
JURISRANK 分析 — [主题]
日期：[日期] | 工具：JurisRank（Lerer, 2026, JCLLT）

## 按权威性排序的先例
| 案例 | 法院 | 年份 | 权威性分数 | 网络位置 |
|------|-------|------|----------------|-----------------|
| ...  | CSJN  | ...  | 0.92           | 指导性案例    |

## 学说演变
[时间线：学说如何发展]

## 引用网络
[哪些案例互相引用；学说集群]

## 建议
[应引用哪些案例 · 以什么顺序 · 为什么]
```

---

## 关于作者

Ignacio Adrián Lerer 是阿根廷律师和独立研究者。JurisRank 是作为在同行评审期刊上发表的计算机法律分析研究的一部分而开发的。该工具已在阿根廷 DNDA（版权注册处）注册，并在阿根廷 INPI 有专利申请待审。

联系方式：[justitia.com.ar](https://justitia.com.ar)
