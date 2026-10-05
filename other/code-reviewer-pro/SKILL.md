---
version: "2.0.0"
name: code-reviewer-pro
description: "代码审查、重构建议、安全漏洞检查、命名规范、复杂度分析、注释文档生成. Use when you need code reviewer pro capabilities. Triggers on: code reviewer pro."
author: BytesAgain
---

# Code Reviewer

代码审查助手。提供审查检查清单、重构建议、安全漏洞检查、命名规范、复杂度分析、注释文档生成。

## 使用方式

根据用户需求调用对应脚本命令：

### 命令列表

| 命令 | 说明 | 用法 |
|------|------|------|
| `review` | 代码审查检查清单 | `bash scripts/review.sh review <language>` |
| `refactor` | 重构建议与模式 | `bash scripts/review.sh refactor <pattern>` |
| `security` | 安全漏洞检查清单 | `bash scripts/review.sh security <language>` |
| `naming` | 命名规范速查 | `bash scripts/review.sh naming <language>` |
| `complexity` | 复杂度分析指标 | `bash scripts/review.sh complexity` |
| `document` | 注释文档模板 | `bash scripts/review.sh document <language>` |

### 工作流

1. 用户要做代码审查 → 调用 `review`
2. 用户想重构代码 → 调用 `refactor`
3. 安全审查 → 调用 `security`
4. 查命名规范 → 调用 `naming`
5. 分析复杂度 → 调用 `complexity`
6. 生成文档模板 → 调用 `document`

脚本路径: `skills/code-reviewer/scripts/review.sh`
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com

## Examples

```bash
# Show help
code-reviewer-pro help

# Run
code-reviewer-pro run
```

## Commands

Run `code-reviewer-pro help` to see all available commands.
