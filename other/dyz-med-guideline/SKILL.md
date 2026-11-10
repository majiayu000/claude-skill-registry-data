---
name: dyz-med-guideline
description: >-
  按当前适用的医学研究报告规范逐条核对稿件，标记 COVERED、PARTIAL、MISSING、NOT_APPLICABLE，并给出
  可定位的修改建议。当用户明确要检查 CONSORT、STROBE、PRISMA、STARD、CARE、TRIPOD、ARRIVE、SPIRIT
  等规范符合性时使用；笼统稿件诊断、论断证据核查和模拟审稿分别交给相应技能，本技能不出具合规认证。
  Use to check applicable medical reporting guidelines including STROBE, CONSORT and PRISMA.
---

# 医学报告规范逐条核查

## 核心原则

- 先确认研究设计、稿件类型、规范版本和适用扩展，再开始计数。
- 使用官方完整核对表，不凭记忆重建条目。
- 只在稿件中找到可定位证据时标为 `COVERED`。
- `NOT_APPLICABLE` 必须写明理由，不能用于隐藏缺失。
- 报告规范检查评价透明度，不证明研究设计正确、证据可靠或稿件必然可发表。

## 工作流程

### 1. 确认规范

从研究设计、稿件类型和目标期刊要求确定：

- 主规范；
- 版本；
- 适用扩展；
- 期刊自有清单。

优先通过 EQUATOR、规范官网或目标期刊作者指南核实当前版本。当前随机试验结果应使用 CONSORT 2025，试验方案应使用 SPIRIT 2025；不要继续把 CONSORT 2010 或 SPIRIT 2013 当成默认现行版本。

若无法访问当前官方核对表：

1. 使用用户提供的正式清单；或
2. 明确标记为“版本未核实的有限检查”；
3. 不把本地旧版模板的通过结果描述为当前规范完全合规。

### 2. 准备稿件

确认：

- 全文或待检查分节；
- 表格、图、补充材料、方案和注册记录是否纳入检查；
- 稿件版本；
- 目标输出是完整逐条表，还是只列缺失项。

没有全文时，只检查已提供部分，并明确未检查范围。

### 3. 逐条核对

对官方清单的每个条目记录：

| 字段 | 要求 |
|---|---|
| Item ID | 官方条目号 |
| Requirement | 条目要求的简要转述 |
| Status | COVERED / PARTIAL / MISSING / NOT_APPLICABLE |
| Evidence | 稿件章节、段落、页码、表图或补充材料 |
| Comment | 缺口、冲突或不适用理由 |
| Suggested fix | 需要补什么、放在哪里 |

状态规则：

- `COVERED`：要求被清楚、完整地报告；
- `PARTIAL`：有相关文字，但缺少条目要求的重要组成；
- `MISSING`：在已检查材料中没有找到；
- `NOT_APPLICABLE`：确实不适用，并有研究设计理由。

不要因为稿件“看起来提过”就标为完整覆盖。

### 4. 做一致性检查

必要时读取 `templates/data/cross-reference-map.yaml`。该文件只是示例骨架，只有项目中存在对应风险项、GRADE 记录或偏倚工具结果时才交叉核对。

检查：

- 注册记录与稿件结局是否一致；
- 方案、统计分析计划和结果报告是否一致；
- 文中称已完成的偏倚评估、GRADE 或敏感性分析是否有实际产物；
- 表图、补充材料和正文是否互相支持；
- 清单标为 `COVERED` 的条目是否与其他风险记录冲突。

不存在对应项目记录时标为 `UNVERIFIED`，不要编造交叉引用。

### 5. 汇总

分别报告四类数量。计算百分比时明确分母：

- 总条目分布：以全部条目为分母；
- 适用条目覆盖率：以 `COVERED + PARTIAL + MISSING` 为分母；
- 不把 `NOT_APPLICABLE` 计入适用条目覆盖率。

将 `MISSING` 和 `PARTIAL` 按以下优先级排列：

1. 会影响读者理解、复现或主要结论解释；
2. 目标期刊明确要求；
3. 重要但不影响核心解释；
4. 编辑性改进。

### 6. 提出修改建议

每条建议说明：

- 要补充的事实或说明；
- 建议章节；
- 需要哪个原始材料核实；
- 若信息不存在，应如何如实披露。

不得为满足清单而虚构随机化、盲法、注册、伦理、样本量计算、分析或数据共享信息。

## 标准输出

```markdown
## 报告规范核查

- 主规范及版本：
- 适用扩展：
- 稿件版本：
- 已检查范围：

### 汇总
- COVERED：
- PARTIAL：
- MISSING：
- NOT_APPLICABLE：
- 适用条目覆盖率：

### 逐条核对
| Item | Requirement | Status | Evidence | Comment | Suggested fix |
|---|---|---|---|---|---|

### 优先修复
1.
2.

### 未核实范围
- 
```

## 完成检查

- 研究设计、规范版本和扩展已核实；
- 使用官方完整清单或明确披露有限检查；
- 每个条目只有一个状态；
- `COVERED` 有可定位的稿件证据；
- `NOT_APPLICABLE` 有明确理由；
- 百分比分母已说明；
- 所有缺失项有可执行且不虚构事实的建议；
- 结果没有被描述为合规认证或录用保证。

## 版本记录

按[版本索引](references/versioned-guidelines.md)定位官方来源并保存实际取得的版本、日期、文件哈希和扩展适用性；索引不能代替完整官方清单。

## 配套资源

- `templates/checklists/consort-2010-legacy.md`：历史版 CONSORT 2010 骨架，仅用于旧版对照，不用于当前 RCT 默认检查。
- `templates/data/cross-reference-map.yaml`：项目交叉核对示例骨架。
- `examples/worked-example-consort.md`：基于历史版清单的虚构教学示例。
- `references/references.md`：报告规范版本与官方来源。
