---
name: token-efficiency
description: Token optimization — efficient reads, bash ops, model selection.
---

# Token Efficiency

This skill provides token optimization strategies for cost-effective agent runs across all projects and every supported CLI (Claude Code, opencode, Codex CLI). The strategies are CLI-independent — they are about how much text enters the context window, not about which tool reads it. Apply these guidelines by default unless the user explicitly requests verbose output or full file contents.

**Default assumption: users prefer efficient, cost-effective assistance.**

---

## Model Selection Strategy

Pick by model *class*, not by product name — every supported provider offers all three. The concrete model id per class and provider is resolved from `scripts/lib/tiers.json`; the Claude Code column below is one example mapping.

| Task type | Model class | Claude Code example |
|-----------|-------------|---------------------|
| Learning a new codebase, understanding architecture, deep analysis | **High-reasoning** | Opus |
| Writing code, debugging, testing, documentation, routine questions | **Balanced** (default) | Sonnet |
| Structured output, fast repetitive extraction | **Fast** | Haiku |

**Typical session pattern:**
1. **High-reasoning** — 10–15 min upfront to understand the codebase (one-time investment)
2. **Balanced** — all implementation, debugging, and routine work
3. **High-reasoning** — return only for deep architectural questions

Savings: ~50% token cost vs. running the whole session on the high-reasoning model.

---

## Core Optimization Rules

### 1. Use Quiet/Minimal Output Modes
Prefer `--quiet`, `-q`, `--silent` flags. Only use verbose when user explicitly asks.

### 2. Never Read Entire Log Files
Always filter before reading: `tail -100`, `grep -i "error"`, specific time ranges.

### 3. Check Lightweight Sources First
Check `git status --short`, `package.json`, `requirements.txt` before opening large files.

### 4. Use Grep Instead of Reading Files
Search for specific content with the Grep tool instead of reading entire files.

### 5. Read Files with Limits
Use `offset` and `limit` parameters. Check file size with `wc -l` first.

### 6. Use Bash Commands Instead of Reading Files

**Reading files costs tokens. Bash commands don't.**

| Operation | Wasteful | Efficient |
|-----------|----------|-----------|
| Copy file | Read + Write | `cp source dest` |
| Replace text | Read + Edit | `sed -i '' 's/old/new/g' file` |
| Append line | Read + Write | `echo "text" >> file` |
| Delete lines | Read + Write | `sed -i '' '/pattern/d' file` |
| Merge files | Read + Read + Write | `cat file1 file2 > combined` |
| Count lines | Read file | `wc -l file` |
| Check content | Read file | `grep -q "term" file` |

**Exception:** complex logic, code-aware changes, interactive review. See [strategies.md](strategies.md).

### 7. Filter Command Output
Limit scope: `head -50`, `find . -maxdepth 2`, `tree -L 2`.

### 8. Summarize, Don't Dump
Provide structured summaries of directory contents, code structure, and command output.

### 9. Use Head/Tail for Large Output
`head -100`, `tail -50`, or `head -500 | tail -100` for middle sections.

### 10. Use JSON/Data Tools Efficiently
Extract specific fields: `jq '.metadata'`, `jq 'keys'`. Don't read entire JSON files.

### 11. Optimize Code Reading
Get an overview first (find, grep for classes/functions), read structure only, then read only the relevant sections.

### 12. Use Subagents for Broad Exploration
Spawn an Explore subagent for broad codebase searches. Saves 70–80% tokens vs. direct multi-file exploration.

---

## Optional CLI Tools

The rules above assume `grep`, `find`, and manual JSON reading. Faster, lower-token alternatives exist for each — `rg` (ripgrep), `fd`, `jq`, `ast-grep` (structural code search/rewrite), `tokei` (instant repo stats), `delta` (readable diff review). None are required; run `/devteam:install list` to see what's missing, or `/devteam:install <tool>` to install one — see `skills/devops/tool-installers/SKILL.md` for the cross-OS knowledge base. `skills/shared/setup-health-check/references/checks-list.md` Category 13 only detects and points here.

## Decision Tree for File Operations

Before any file operation, ask:

1. **Creating a new file?** → Write tool directly
2. **Low-cost operation** (< 100 lines output)? → Use Claude context directly
3. **Modifying a code file** (.ts, .py, .js, .php…)? → Read + Edit (always)
4. **Modifying a small data file** (< 100 lines)? → Read + Edit is fine
5. **Modifying a large data or config file?** → `sed`/`awk` bash commands
6. **Copying or merging files?** → `cp`/`cat`, not Read/Write
7. **Can I check metadata first?** (line count, file size) → Do it
8. **Can I filter before reading?** (grep, head, tail) → Do it
9. **Can I summarize instead of showing raw output?** → Do it

---

## Cost Impact

| Approach | Tokens/Week | Notes |
|----------|-------------|-------|
| **Wasteful** — Read/Edit/Write everything | 500K | Reading files unnecessarily |
| **Moderate** — filtered reads only | 200K | Grep/head/tail usage |
| **Efficient** — bash commands + filters | 30–50K | cp/sed/awk instead of Read |

Applying these rules reduces costs by **90–95% on average**.

---

## When to Override These Guidelines

1. **User explicitly requests full output** ("Show me the entire file")
2. **Filtered output lacks necessary context** (error references missing line numbers)
3. **File is small** (< 200 lines)
4. **Learning mode** — when understanding new code, read 2–5 key files fully to establish context, then return to efficient mode for implementation

---

## Skills and Token Efficiency

Skills in `.claude/skills/` use **progressive disclosure** — Claude sees only the description (~40 tokens per skill) at session start. Full content loads only when activated. Having many skills available does not increase token usage.

---

## Quick Reference Card

**Model first:**
- Learning/understanding → Opus
- Development/execution → Sonnet (default)
- Structured output → Haiku

**File operations:**
- New file → Write tool
- < 100 lines output → Claude context directly
- Code file → Read + Edit
- Small data file → Read + Edit
- Large data/config file → bash (`sed`, `awk`, `grep`)
- Copy/merge → `cp`/`cat`

**Always:**
- Filter before reading (grep, head, tail)
- Read with limits when reading is required
- Summarize instead of dumping raw output
- Use quiet modes for commands

---

## Supporting Files

| File | Content | When to load |
|------|---------|-------------|
| [strategies.md](strategies.md) | Detailed bash patterns, sed/awk examples, macOS/Linux compatibility, file operation recipes | When implementing specific file operations or needing detailed bash patterns |
