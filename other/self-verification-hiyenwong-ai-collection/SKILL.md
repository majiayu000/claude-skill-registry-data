---
name: self-verification
description: 自我验证技能，基于 ReVeal 论文实现多轮生成-验证迭代，支持代码和推理任务的可靠自我验证。触发词：自我验证、self-verification、verify、验证代码、验证推理。
---

# Self-Verification Skill

可靠的自我验证能力，支持代码和推理任务的多轮迭代改进。

## 核心理念

基于 **ReVeal (arXiv:2506.11442)** 论文：
- 验证-生成不对称性优化
- 多轮生成-验证迭代
- TAPO (Turn-level Adaptive Policy Optimization) 信用分配
- 工具反馈驱动的持续进化

## 工作流程

### 1. 生成阶段
```
Input: 任务描述
Output: 初始方案/代码

步骤：
1. 分析任务需求
2. 生成初步解决方案
3. 识别潜在问题点
```

### 2. 验证阶段
```
Input: 生成的方案/代码
Output: 验证结果 + 问题列表

验证维度：
- 语法正确性
- 逻辑一致性
- 边界条件处理
- 错误处理完整性
- 性能考量
```

### 3. 迭代改进
```
Loop (max_iterations: 5):
1. 根据验证结果识别问题
2. 针对性修复
3. 重新验证
4. 如果通过 → 结束
5. 如果未通过 → 继续迭代
```

## 使用示例

### 代码验证
```python
# 生成初始代码
code = generate_code(task)

# 自我验证
verification = self_verify(code, test_cases)

# 迭代改进
while not verification.passed and iterations < max_iterations:
    code = improve_code(code, verification.issues)
    verification = self_verify(code, test_cases)
    iterations += 1
```

### 推理验证
```python
# 生成推理链
reasoning = generate_reasoning(question)

# 验证推理步骤
validation = validate_reasoning(reasoning)

# 修正逻辑错误
if not validation.valid:
    reasoning = correct_reasoning(reasoning, validation.errors)
```

## 验证检查清单

### 代码验证
- [ ] 语法正确
- [ ] 无明显 bug
- [ ] 边界条件处理
- [ ] 错误处理
- [ ] 代码风格一致
- [ ] 注释清晰

### 推理验证
- [ ] 前提正确
- [ ] 推理步骤合理
- [ ] 结论与前提一致
- [ ] 无逻辑跳跃
- [ ] 无矛盾

## 工具使用

- `exec` - 运行测试命令
- `read` - 读取生成的代码/文件
- `write` - 保存改进后的版本
- `edit` - 精确修复问题

## TAPO 信用分配

每次迭代后评估：
1. 哪些修改有效 (+信用)
2. 哪些修改无效 (-信用)
3. 调整后续策略

## 最佳实践

1. **不要急于求成** - 允许多轮迭代
2. **记录每次改进** - 便于回溯和学习
3. **使用工具验证** - 不要仅依赖语言模型判断
4. **设置合理上限** - 避免无限循环

## 与其他 Skills 协同

- `ice-review` - 任务后回顾验证过程
- `self-challenge` - 生成验证测试用例
- `memory-retrieval` - 检索历史验证经验
## Activation Keywords

- `self-verification`
- `self-verification`
- `self verification`

## Tools Used

- `exec`
- `read`
- `write`
- `edit`

## Instructions for Agents

1. Read the task description carefully
2. Follow the step-by-step process
3. Use the appropriate tools
4. Verify the results

## Examples

### Example 1: Basic Usage

**User:** <example user request>

**Agent:** <example agent response>

### Example 2: Advanced Usage

**User:** <example user request>

**Agent:** <example agent response>
