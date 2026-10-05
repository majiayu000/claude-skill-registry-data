---
slug: shadows-context-optimizer
version: 1.1.1
displayName: 上下文优化器（Shadows Context Optimizer）
summary: 优化令牌和上下文窗口，压缩提示，减少冗余，优先考虑关键上下文，适用于达到上下文限制或提高代理效率时。
tags: clawhub
---

# Context Optimizer — Token Economy Protocol

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Context window approaching capacity (>70% usage)
- Agent responses becoming slower or less coherent
- User says "optimize context", "compact", "reduce tokens"
- Working with very large codebases
- Multi-file operations causing context bloat

## WHEN NOT TO TRIGGER

- Short conversations with plenty of context remaining
- Simple single-file operations

---

## PREREQUISITES

No binaries required. This is a pure reasoning skill about optimizing context window usage. It provides strategies and patterns — it does not execute commands or access external systems.

---

## PRINCIPLES

### 1. Reference Over Inline

Instead of reading entire files into context, reference them:
- "The auth module at `src/auth/index.ts` handles..." instead of pasting 500 lines
- Read only the specific functions/sections needed
- Use line ranges: `Read file.py lines 45-80` instead of the whole file

### 2. DRY Prompts — Zero Duplication

- Never repeat information already in system context
- Don't re-describe tools you already know about
- Don't re-state project conventions that are in CLAUDE.md/SOUL.md
- If a fact was established earlier, reference it, don't restate it

### 3. Lazy-Load Strategy

- Load detailed context only when needed for the current task
- Use subagents/sub-tasks for exploration (protects main context)
- Delegate research to agents, keep main context for execution

### 4. Smart File Reading

```
WRONG: Read the entire 2000-line file
RIGHT: Read lines 150-200 where the function is defined

WRONG: Read all 15 config files
RIGHT: Read only the config relevant to current task

WRONG: Grep the entire codebase for "import"
RIGHT: Grep specific directories for specific patterns
```

### 5. Output Compression

When reporting results:
- Lead with the answer, not the reasoning
- Skip filler words and unnecessary transitions
- Use tables for comparative data
- Use bullet points for lists, not paragraphs

---

## TECHNIQUES

### Technique 1 — Context Audit

Assess current context usage:
1. Count how many files have been read in this session
2. Identify which file contents are still relevant to the current task
3. Determine what information can be summarized instead of kept verbatim
4. Flag redundant tool results that repeat already-known information

### Technique 2 — Compaction

When context is high:
1. Summarize completed work (keep outcomes, drop process details)
2. Drop file contents that are no longer needed for the active task
3. Keep only active task context in working memory
4. Preserve critical state: decisions made, errors encountered, current objectives

### Technique 3 — Subagent Delegation

For research-heavy tasks:
1. Spawn a subagent for codebase exploration
2. Subagent returns only findings (not raw file contents)
3. Main context stays clean for implementation
4. Multiple subagents can run in parallel for independent queries

### Technique 4 — Structured Responses

```
WRONG (100 tokens):
"I've looked at the file and after careful analysis I believe that
the issue is related to the authentication middleware where the
token validation function doesn't properly handle expired tokens."

RIGHT (30 tokens):
"Bug: `validateToken()` in auth middleware doesn't handle expired
tokens. Fix: add expiry check at line 45."
```

---

## ANTI-PATTERNS TO AVOID

| Anti-Pattern | Fix |
|-------------|-----|
| Reading whole files when you need 10 lines | Use offset + limit |
| Listing all MCP servers | Agent already knows them |
| Repeating deny rules | Already in settings |
| Describing the OS/environment | Already in system context |
| Re-reading files read earlier | Summarize and reference |
| Multiple searches for one query | One well-crafted search |
| Verbose status updates | Concise milestone updates |

---

## RULES

1. **Minimum viable context** — load only what's needed NOW
2. **Summarize, don't accumulate** — compress completed work
3. **Delegate exploration** — use subagents for research
4. **Direct answers** — skip preamble, lead with the point
5. **3-search maximum** — never use more than 3 search tools for one query

---

## SECURITY CONSIDERATIONS

This skill is purely advisory — it provides strategies for token optimization. It does not execute commands, read files, make network calls, modify configuration, or store data. Zero risk profile.

- **Commands executed**: None
- **Data read**: None (advisory reasoning only)
- **Network access**: None
- **Persistence**: None
- **Credentials**: None required
- **File modification**: None

---

## OUTPUT FORMAT

Apply the techniques above inline during agent operation. No separate report is generated — the skill manifests as improved efficiency in the agent's behavior: shorter responses, fewer tool calls, targeted file reads, and minimal context consumption.

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
