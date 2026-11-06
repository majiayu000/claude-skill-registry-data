---
name: science-reporting-standards
description: Use when preparing a submission, when a reviewer asks for CONSORT/PRISMA/STROBE/ARRIVE/TRIPOD items, when the journal demands data/code availability statements, or when an audit reports blocking findings; covers which standard applies to which design and what each one actually requires.
---

# 报告规范：审稿人手里的核对表

## 先选对规范（选错等于白写）

| 你的研究 | 规范 | 关键条目（缺了必被要求补） |
|---|---|---|
| 随机对照试验 | **CONSORT** | 注册号、随机化方法与分配隐藏、盲法、主要结局、受试者流程、样本量估算、ITT、不良事件 |
| 系统综述 / meta | **PRISMA** | 方案预注册（PROSPERO）、数据库与检索式、筛选流程、偏倚风险、异质性、发表偏倚 |
| 队列 / 病例对照 / 横断面 | **STROBE** | 设计类型、纳排标准、混杂处理、缺失数据、敏感性分析 |
| 动物实验 | **ARRIVE 2.0** | 物种品系、饲养条件、人道终点、随机分组（含笼效应）、评估设盲 |
| 预测模型 | **TRIPOD** | 预测因子定义、区分度**与**校准、内部/外部验证、EPV 或最小样本量 |
| 质性研究 | COREQ / SRQR | 研究者立场、抽样策略、资料饱和、编码与可信度 |

## 任何投稿都要有的四段声明

这四段缺失是编辑部最常见的"退回补材料"，与学术质量无关但会拖两周：

1. **Data availability** —— 数据在哪、登记号、受控访问条件。不要写"合理请求可提供"。
2. **Code availability** —— 仓库链接 + 版本 tag + 环境文件。
3. **Competing interests** —— 没有也要显式写 `The authors declare no competing interests`。
4. **Author contributions** —— 用 CRediT 逐人写；通讯作者之外的实质贡献必须列全。

再加三段按情形：**Ethics**（人/动物必须有批号）、**Funding**（含资助号）、**Acknowledgements**。

## 统计报告：审稿人最先查的五件事

1. **精确 n**：每组多少、每个图多少。不是"若干"、不是"n≈"。
2. **效应量 + 95% CI**：只给 p 值等于没给结果大小。p 值与效应量必须同时出现。
3. **多重比较**：做了几次比较、如何校正（Bonferroni / FDR）、哪些是预设哪些是事后。
4. **缺失数据**：缺失比例、机制假设、插补方法与完整病例分析的对比。
5. **软件与版本**：R/Python 版本、包版本、随机种子。

`science_paper_audit` 的 GEN-05/06/07 就是查前三项。它只能查"有没有"，查不出"对不对"——数值合理性要你自己看。

## TOP Guidelines 8 项（透明度分级，多数刊已采纳）

1. 引用数据/代码　2. 数据可得（含等级）　3. 代码可得　4. 材料可得
5. 研究设计预注册　6. 分析计划预注册　7. 分析计划偏离说明　8. 可复现性信息

关键：**没有就明说"未预注册"**。沉默会被当作隐瞒；明确声明是合规的。

## 用工具的顺序

```
science_paper_audit(profiles=["general", <你的设计对应的规范>])
  → 先消 blocking（审稿人必然要求补）
  → 再看 warning（影响送审概率）
  → manual 项自己判断（工具不替你做语义判定）
  → skipped 项不等于通过：补上对应章节再跑一次
```

绑了 `manuscriptId` 时会额外检查证据链：**孤儿断言**（结论没有证据挂接）与被自己的证据反驳的断言。这两类是审稿人最容易击穿的点。

## 硬规矩

- 不要用"我们遵循了 CONSORT 指南"代替逐项报告。审稿人按条目核对，不看声明。
- 规范文件本身要放进补充材料（尤其 PRISMA 检索式、CONSORT 流程图）。
- 报告规范管的是"有没有报"，不是"做得对不对"。设计缺陷补不回来，但漏报可以补。
