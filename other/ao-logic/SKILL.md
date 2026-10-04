---
name: "ao-logic"
description: "通用逻辑抽象接口。当定义逻辑推理、演绎归纳、逻辑运算时调用此技能。"
---

# 通用逻辑接口

## 核心概念

- **逻辑推理**：基于逻辑规则的推理过程
- **演绎归纳**：从一般到特殊和从特殊到一般的推理
- **逻辑运算**：逻辑符号的运算和操作
- **逻辑分析**：分析和评估逻辑论证

## 主要功能

- **逻辑规则**：定义和应用逻辑规则
- **推理过程**：执行逻辑推理和证明
- **逻辑运算**：进行逻辑符号的运算
- **逻辑分析**：分析和评估逻辑论证

## 能力定义

### 逻辑推理 (logicalReasoning)
- **描述**：基于逻辑规则的推理过程
- **方法**：
  - deductiveReasoning：演绎推理
  - inductiveReasoning：归纳推理
  - abductiveReasoning：溯因推理

### 逻辑运算 (logicalOperations)
- **描述**：逻辑符号的运算和操作
- **方法**：
  - andOperation：与运算
  - orOperation：或运算
  - notOperation：非运算
  - implicationOperation：蕴含运算
  - equivalenceOperation：等价运算

### 逻辑分析 (logicalAnalysis)
- **描述**：分析和评估逻辑论证
- **方法**：
  - argumentAnalysis：论证分析
  - fallacyDetection：谬误检测
  - validityCheck：有效性检查
  - soundnessCheck：可靠性检查

### 逻辑规则 (logicalRules)
- **描述**：定义和应用逻辑规则
- **方法**：
  - ruleDefinition：规则定义
  - ruleApplication：规则应用
  - ruleValidation：规则验证

## 详细定义

完整的接口定义、属性和方法请参考 <mcfile name="skills.json" path="./skills.json"></mcfile>。