---
name: craft-hook
description: How to create a new Reflex (Hook) for the OS.
---

# Skill: Craft Hook

> "The Subconscious. Automatic reactions."

## 0. Read The Docs First

https://code.claude.com/docs/en/hooks is the source of truth. This skill is what we learned
around it, and Anthropic adds events without asking us.

## 1. The Principles

- **Thin**: Hooks point to skills. They don't contain protocols.
- **Invisible**: A good hook is never noticed. It just *works*.
- **Non-Blocking**: Hooks complete quickly. Long tasks belong in agents.
- **Focused**: One hook, one job. Use matchers to target precisely.
- **Verified**: Test that Claude actually sees your output.

### The Thin Hook Rule

If you're writing more than 5 lines of protocol/criteria in a hook, it belongs in a skill.

```
HOOK RESPONSIBILITY              SKILL RESPONSIBILITY
├── WHEN to inject               ├── HOW to do it
├── WHAT to tell Claude          ├── WHY to do it
├── Formatting (emojis)          └── Decision criteria
└── Exit code / JSON output
```

**Anti-pattern**: Duplicating skill content in hooks.

## 2. Context Injection Rules

**Critical**: Not all hooks can inject to Claude's context. Know the rules:

| Event | stdout (exit 0) | stderr (exit 2) | JSON additionalContext |
|-------|-----------------|-----------------|------------------------|
| `SessionStart` | **→ Claude** | → User only | **→ Claude** |
| `UserPromptSubmit` | **→ Claude** | → User only | **→ Claude** |
| `Setup` | **→ Claude** | → User only | **→ Claude** |
| `PreToolUse` | → User verbose | **→ Claude** | **→ Claude** |
| `PostToolUse` | → User verbose | **→ Claude** | **→ Claude** |
| `Stop` | → User verbose | **→ Claude** | decision only |
| `SubagentStop` | → User verbose | **→ Claude** | decision only |
| `PreCompact` | → User verbose | → User only | **None** |
| `Notification` | → Debug only | → User only | None |
| `SessionEnd` | → Debug only | → User only | None |

### The Rules

1. **SessionStart/UserPromptSubmit/Setup**: Plain stdout goes to Claude. Just `echo`.
2. **PreToolUse/PostToolUse**: Must use JSON with `additionalContext` OR exit 2 with stderr.
3. **Stop/SubagentStop**: Use `decision: "block"` with `reason` to force continuation.
4. **PreCompact**: **Cannot inject to Claude at all.** Don't use for context preservation.

## 3. Implementation

- **Location**: `hooks/hooks.json`
- **Paths**: Use `${CLAUDE_PLUGIN_ROOT}` for portability
- **Testing**: Verify with `claude --debug` to see hook execution

## 4. Deeper

| | |
|---|---|
| [patterns](patterns.md) | the PostToolUse JSON shape, and the Stop hook |
| [template](template.md) | a thin hook, whole |
| [matchers](matchers.md) | what SessionStart matches, and when |
| `craft-plugin` | where a hook sits in a plugin |
| `craft-adr` | recording why a hook exists |
