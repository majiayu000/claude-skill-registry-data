---
name: codex-ai
description: 通过 Codex CLI 进行代码审查、算法设计、架构分析和性能优化。适用于复杂技术任务、系统级设计、性能瓶颈分析。触发词：代码审查、review、算法设计、架构分析、性能优化。
---

# Codex-AI 协作技能

通过 Bash 直接调用 Codex CLI，处理复杂技术任务。

## 何时使用

触发此技能当用户提到：
- 代码审查、review、code review
- 算法设计、复杂逻辑
- 架构分析、架构评审
- 性能优化、瓶颈分析

## 快速开始

### 代码审查
```bash
codex review --uncommitted -m gpt-5.1-codex-max -c 'model_reasoning_effort="xhigh"'
```

### 算法设计和架构分析
```bash
# 简单任务
codex exec -m gpt-5.1-codex-max -c 'model_reasoning_effort="high"' "<任务描述>"

# 复杂任务（多约束、系统级设计）
codex exec -m gpt-5.2 -c 'model_reasoning_effort="xhigh"' "<任务描述>"
```

## 模型选择

**简单任务** → `gpt-5.1-codex-max`：代码审查、简单重构、文档生成

**复杂任务** → `gpt-5.2`：复杂算法、架构评审、性能优化、多约束问题

**判断标准**：
- 单一目标、局部修改 → 简单
- 多约束、系统级设计 → 复杂

## 工作流程

### 代码审查工作流

1. **确定审查范围**：
   - 未提交变更：`--uncommitted`
   - PR 分支：`--base main`
   - 特定提交：`--commit <SHA>`

2. **选择模型**：
   - 常规审查 → `gpt-5.1-codex-max`
   - 深度分析（安全、性能）→ `gpt-5.2`

3. **执行审查**：
   ```bash
   codex review --uncommitted -m gpt-5.1-codex-max -c 'model_reasoning_effort="xhigh"'
   ```

4. **审查输出并采取行动**

### 算法设计工作流

1. **明确需求**：
   - 列出所有约束条件
   - 定义性能目标
   - 说明边界情况

2. **选择模型**：
   - 单一目标 → `gpt-5.1-codex-max`
   - 多约束 → `gpt-5.2`

3. **执行设计**：
   ```bash
   codex exec -m gpt-5.2 -c 'model_reasoning_effort="xhigh"' "设计任务描述"
   ```

4. **验证建议**：
   - 理解设计原理
   - 评估可行性
   - 测试验证

5. **逐步实施**

## 常用参数

| 参数 | 说明 |
|------|------|
| `-m <MODEL>` | 模型选择 |
| `-c 'model_reasoning_effort="xhigh"'` | 推理强度（推荐） |
| `-C <DIR>` | 工作目录 |
| `-o <FILE>` | 输出到文件 |
| `--uncommitted` | 审查未提交变更 |
| `--base <BRANCH>` | 对比基准分支 |

## 详细文档

- **使用场景和示例**：查看 [README.md](README.md)
- **完整命令参考**：查看 [REFERENCE.md](REFERENCE.md)
