---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 结构化决策：优缺点矩阵、加权评分、决策树、情景分析和艾森豪威尔矩阵。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="decide banner">

> **中文** — `decide` 官方中文版本。


# Decide — 结构化决策

> 通过结构化框架和评估方法做出理性的决策

---

## 何时使用？

- 在多个选项之间进行选择
- 需要优缺点列表
- 多标准决策
- 对重要决策感到不确定

**触发词：** decide, choose, compare, evaluate, weigh

---

## 框架

### 1. 优缺点矩阵（简单）

在 2 个选项之间做出快速决策。

```
PRO A:                    CON A:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

PRO B:                    CON B:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

Recommendation: [A/B] because [reasoning]
```

---

### 2. 加权评分（复杂）

带权重的多标准决策。

| 评估标准 | 权重 | 选项 A | 得分 A | 选项 B | 得分 B |
|-----------|--------|----------|---------|----------|---------|
| 标准 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| 标准 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| 总计 | 100% | - | X.XX | - | X.XX |

**流程：**
1. 收集标准
2. 分配权重（总和 = 100%）
3. 评估选项（1-10 评分）
4. 计算得分（评分 x 权重）
5. 比较并给出建议

---

### 3. 决策树（顺序）

具有明确 if-then 路径的决策：
1. 明确初始问题
2. 第一分支（最重要的标准）
3. 下一级别（第二重要的标准）
4. 延伸至最终选项

---

### 4. 情景分析（不确定性）

```
Best Case (X% probability):
  Outcome: +Y points -> Expected value: +Z

Realistic Case (X%):
  Outcome: +Y -> Expected value: +Z

Worst Case (X%):
  Outcome: -Y -> Expected value: -Z

Total expected value: [Sum]
```

---

### 5. 艾森豪威尔矩阵（优先级排序）

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

---

## 质量检查清单

在做出最终建议前检查：
- [ ] 是否已识别所有相关标准？
- [ ] 是否已考虑用户价值观？
- [ ] 是否已考虑长期影响？
- [ ] 是否已识别并评估风险？
- [ ] 是否已进行偏见检查？
- [ ] 是否已评估可逆性？

---

## 最佳实践

### 定义标准
- 具体且可衡量
- 数量不宜过多（理想为 3-7 个）
- 相互独立

### 权重分配
- 总和 = 100%
- 最重要的标准 >= 25%
- 无小于 5% 的权重

### 建议
- 明确且有理有据
- 提及替代方案
- 列出风险
- 考虑可逆性

---

## 工作流程与步骤

```
1. User request
2. Understand decision
3. Identify options (2-5)
4. Choose framework
5. Collect criteria
6. Apply framework
7. Bias check (optional)
8. Make recommendation
9. Document reasoning
```

---

## 变更日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*
