---
name: codex
description: >
  This skill should be used ONLY when the user explicitly mentions "codex" by name.
  Trigger phrases: "use codex", "ask codex", "let codex review", "compare with codex",
  "delegate to codex", "codex review my code", "have codex check this",
  "用 codex", "让 codex 看看", "codex 审查", "codex 帮我看", "用 codex 分析",
  "让 codex 帮忙", "交给 codex", "codex 看一下", "换 codex 看看".
  Do NOT trigger on generic phrases like "get a second opinion", "review my code",
  "cross-model verification", "帮我看看代码", "再检查一下" unless the user explicitly mentions "codex".
---

# Codex Bridge

Route user requests to the appropriate Codex command. Commands handle context collection, prompt composition, and result analysis autonomously.

## Safety

- Default sandbox: `read-only`. Only use `workspace-write` on explicit user request.
- Forbidden flags: `--dangerously-bypass-approvals-and-sandbox` (and its alias `--yolo`), `--full-auto`, `--sandbox danger-full-access`
- Never pass secrets (API keys, tokens, passwords) in Codex prompts.

## Intent Classification & Routing

Classify the user's request and invoke the matching command. When the intent is ambiguous (e.g., "codex check this"), look at conversation context — if the user was just editing code and has uncommitted changes, lean toward review; otherwise default to general task.

### Review Intent → `/codex-bridge:codex-review`

Trigger when the request is about reviewing code changes, diffs, commits, or PRs.

Keywords: review, 审查, check changes, 看看改动, code review, PR review, diff review, check my code, 看看代码

Examples:
- "让 codex review 我的改动" → `/codex-bridge:codex-review`
- "codex 审查一下这个 PR" → `/codex-bridge:codex-review`
- "ask codex to review changes against main" → `/codex-bridge:codex-review main`
- "codex check my latest commit" → `/codex-bridge:codex-review HEAD`

Pass any branch name, commit SHA, or review instructions as arguments.

### General Task → `/codex-bridge:codex`

Trigger for all other requests: analysis, verification, second opinion, document review, task delegation.

Keywords: analyze, verify, explain, compare, delegate, check, 分析, 验证, 看看, 帮忙看

Examples:
- "让 codex 分析这个函数的错误处理" → `/codex-bridge:codex "分析...的错误处理"`
- "ask codex about the auth implementation" → `/codex-bridge:codex "analyze the auth implementation"`
- "codex 帮我看看这个插件的安全性" → `/codex-bridge:codex "review the security of this plugin"`

Pass the user's full request as the argument. The command will resolve context and compose the prompt.

### Ambiguous Cases

When the user's intent could match either command:
- If the user mentions "changes", "diff", "commit", or "PR" → review
- If the user mentions a specific file or function to analyze → general task
- If still unclear, ask the user: "Would you like Codex to review your recent changes, or analyze something specific?"

## Additional Resources

- **`references/usage-patterns.md`** — Detailed prompt templates for each usage pattern
- **`scripts/codex-exec.sh`** — Standalone wrapper for direct terminal use outside of Claude Code (commands invoke Codex CLI directly)
