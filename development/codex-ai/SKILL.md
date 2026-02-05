---
name: codex-ai
description: 通过 Codex MCP 工具进行代码审查、算法设计、架构分析和性能优化。适用于复杂技术任务（>10行核心逻辑）、系统级设计、多约束权衡、性能瓶颈分析。触发词：review、code review、代码审查、算法设计、复杂算法、架构分析、架构评审、系统设计、性能优化、瓶颈分析、性能调优。
allowed-tools:
  - mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex
  - mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex-reply
  - Bash
---

# Codex-AI 协作技能

通过 MCP 工具调用 Codex CLI,处理复杂技术任务。

## 使用场景

触发此技能当用户提到:
- **代码审查**: review、code review、审查代码
- **算法设计**: 复杂算法（>10行核心逻辑）
- **架构分析**: 架构评审、系统设计、扩展性分析
- **性能优化**: 瓶颈分析、性能调优

## 何时不使用

- 简单任务（<10行代码、基本语法）
- 文档查询（使用 Context7）
- 简单调试（日志分析）
- 代码生成（直接生成即可）

## 工作流程

1. **识别任务类型**: 代码审查/算法设计/架构分析/性能优化
2. **选择模型**: 简单任务 → gpt-5.2-codex, 复杂任务 → gpt-5.2
3. **准备上下文**: 收集 git diff、代码片段、约束条件
4. **调用 Codex**: 使用 `mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex`
5. **格式化输出**: 展示分析结果和下一步行动

**输出格式**:
```
📊 分析结果
- 任务类型: <类型>
- 使用模型: <模型>

📝 Codex 建议
<分析结果>

💡 下一步行动
<实施建议>
```

## MCP 工具调用

使用 `mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex` 发起新会话:

```json
{
  "name": "mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex",
  "parameters": {
    "prompt": "<任务描述>",
    "model": "gpt-5.2-codex",
    "config": {"model_reasoning_effort": "xhigh"}
  }
}
```

使用 `mcp__plugin_codex-mcp-tool_codex-mcp-tool__codex-reply` 继续会话。

**完整参数说明和示例**: 查看 [REFERENCE.md#MCP工具完整参考](REFERENCE.md#mcp-工具完整参考)

## 模型选择

- **gpt-5.2-codex**: 简单任务（代码审查、简单重构、单一目标算法）
- **gpt-5.2**: 复杂任务（复杂算法、架构评审、性能优化、多约束权衡）

**详细决策标准**: 查看 [REFERENCE.md#模型选择详解](REFERENCE.md#模型选择详解)

## 错误处理

常见问题：
- **工具调用失败**: 检查 Codex CLI 安装和配置
- **输出不符合预期**: 使用 `AskUserQuestion` 补充信息
- **模型选择不当**: 重新评估任务复杂度

**完整故障排查指南**: 查看 [REFERENCE.md#错误处理完整指南](REFERENCE.md#错误处理完整指南)

## 详细文档

- **使用场景和示例**: 查看 [README.md](README.md)
- **完整命令参考**: 查看 [REFERENCE.md](REFERENCE.md)
