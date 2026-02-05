---
name: headless-cli
description: "无头模式 AI CLI 调用技能：支持 Gemini/Claude/Codex CLI 的无交互批量调用，包含 YOLO 模式和安全模式。用于批量翻译、代码审查、多模型编排等场景。"
---

# Headless CLI 技能

无交互批量调用 AI CLI 工具，支持 stdin/stdout 管道，实现自动化工作流。

## When to Use This Skill

触发条件：
- 需要批量处理文件（翻译、审查、格式化）
- 需要在脚本中调用 AI 模型
- 需要多模型串联/并联处理
- 需要无人值守的 AI 任务执行

## Not For / Boundaries

不适用于：
- 需要交互式对话的场景
- 需要实时反馈的任务
- 敏感操作（YOLO 模式需谨慎）

必需输入：
- 已安装对应 CLI 工具
- 已完成身份认证
- 网络代理配置（如需）

## Quick Reference

### 🔴 YOLO 模式（全权限，跳过确认）

**Codex CLI**
```bash
# --yolo 是 --dangerously-bypass-approvals-and-sandbox 的别名
alias c='codex --enable web_search_request -m gpt-5.1-codex-max -c model_reasoning_effort="high" --yolo'
```

**Claude Code**
```bash
alias cc='claude --dangerously-skip-permissions'
```

**Gemini CLI**
```bash
# --yolo 或 --approval-mode yolo
alias g='gemini --yolo'
```

### 🟡 Full-Auto 模式（推荐的自动化方式）

**Codex CLI**
```bash
# workspace-write 沙箱 + 失败时才审批
codex --full-auto "Your prompt"
```

**Gemini CLI**
```bash
# 自动批准编辑工具
gemini --approval-mode auto_edit "Your prompt"
```

### 🟢 安全模式（无头但有限制）

**Gemini CLI（禁用工具调用）**
```bash
cat input.md | gemini -p "prompt" --output-format text --allowed-tools '' > output.md
```

**Claude Code（Print 模式）**
```bash
cat input.md | claude -p "prompt" --output-format text > output.md
```

**Codex CLI（非交互执行）**
```bash
codex exec "prompt" --json -o result.txt
```

### 📋 常用命令模板

**批量翻译**
```bash
# 设置代理（如需）
export http_proxy=http://127.0.0.1:9910
export https_proxy=http://127.0.0.1:9910

# Gemini 翻译
cat zh.md | gemini -p "Translate to English. Keep code/links unchanged." \
  --output-format text --allowed-tools '' > en.md
```

**代码审查**
```bash
cat code.py | claude --dangerously-skip-permissions -p \
  "Review this code for bugs and security issues. Output markdown." > review.md
```

**多模型编排**
```bash
# 模型 A 生成 → 模型 B 审查
cat spec.md | gemini -p "Generate code" --output-format text | \
  claude -p "Review and improve this code" --output-format text > result.md
```

### ⚙️ 关键参数对照表

| 功能 | Gemini CLI | Claude Code | Codex CLI |
|:---|:---|:---|:---|
| YOLO 模式 | `--yolo` | `--dangerously-skip-permissions` | `--yolo` |
| 指定模型 | `-m <model>` | `--model <model>` | `-m <model>` |
| 非交互 | `-p "prompt"` | `-p "prompt"` | `exec "prompt"` |
| 输出格式 | `--output-format text` | `--output-format text` | `--json` |
| 禁用工具 | `--allowed-tools ''` | `--disallowedTools` | N/A |
| 继续对话 | N/A | `-c` / `--continue` | `resume --last` |

## Examples

### Example 1: 批量翻译文档

**输入**: 中文 Markdown 文件
**步骤**:
```bash
export http_proxy=http://127.0.0.1:9910
export https_proxy=http://127.0.0.1:9910

for f in docs/*.md; do
  cat "$f" | timeout 120 gemini -p \
    "Translate to English. Keep code fences unchanged." \
    --output-format text --allowed-tools '' 2>/dev/null > "en_$(basename $f)"
done
```
**预期输出**: 翻译后的英文文件

### Example 2: 代码审查流水线

**输入**: Python 代码文件
**步骤**:
```bash
cat src/*.py | claude --dangerously-skip-permissions -p \
  "Review for: 1) Bugs 2) Security 3) Performance. Output markdown table." > review.md
```
**预期输出**: Markdown 格式的审查报告

### Example 3: 多模型对比验证

**输入**: 技术问题
**步骤**:
```bash
question="How to implement rate limiting in Python?"

echo "$question" | gemini -p "$question" --output-format text > gemini_answer.md
echo "$question" | claude -p "$question" --output-format text > claude_answer.md

# 对比两个答案
diff gemini_answer.md claude_answer.md
```
**预期输出**: 两个模型答案的对比

## References

- `references/gemini-cli.md` - Gemini CLI 完整参数
- `references/claude-cli.md` - Claude Code CLI 参数
- `references/codex-cli.md` - Codex CLI 参数
- [Gemini CLI 官方文档](https://geminicli.com/docs/)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code/)
- [Codex CLI 官方文档](https://developers.openai.com/codex/cli/reference)

## Maintenance

- 来源: 各 CLI 官方文档
- 更新: 2025-12-19
- 限制: 需要网络连接和有效认证；YOLO 模式有安全风险
