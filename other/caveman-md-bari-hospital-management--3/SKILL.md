---
name: caveman
description: Cut ~75% of output tokens by talking like caveman. Full technical accuracy. Lite, full, ultra, and 文言文 intensity levels. Works on Claude Code, Cursor, Copilot, Gemini CLI, and 40+ agents.
externalRepo: JuliusBrussee/caveman
---

# Caveman

> **Community skill** — source and full install at [github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)

Ultra-compressed communication mode. Cuts token usage ~65–75% by having the agent talk like caveman — dropping articles, filler, and pleasantries — while keeping every bit of technical accuracy.

## Install

```bash
# Any agent (auto-detect)
npx skills add JuliusBrussee/caveman

# Claude Code
claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman

# Cursor
npx skills add JuliusBrussee/caveman -a cursor

# Windsurf
npx skills add JuliusBrussee/caveman -a windsurf

# Gemini CLI
gemini extensions install https://github.com/JuliusBrussee/caveman
```

## Usage

```
/caveman          — activate (default: full)
/caveman lite     — drop filler, keep grammar
/caveman full     — classic caveman (fragments OK, drop articles)
/caveman ultra    — maximum compression, arrows for causality
/caveman wenyan   — classical Chinese 文言文 mode
stop caveman      — back to normal
```

## Companion Skills

- `caveman-commit` — terse commit messages, ≤50 char subject
- `caveman-review` — one-line PR comments
- `/caveman:compress` — compress CLAUDE.md / memory files (~46% input token savings)

---

## Good to Know

Advanced reference for Caveman. Background, edge cases, and patterns worth understanding.

### Output tokens vs. input tokens

Caveman cuts **output tokens** — what the model writes back to you. It does **not** affect input tokens (what you send or what gets loaded from CLAUDE.md, memory files, etc.).

For input token savings, use **`caveman-compress`**: it rewrites your CLAUDE.md and memory files into caveman-speak so Claude reads less at session start (~46% savings per file). Both together give you the full picture.

| What it saves | Tool |
|---|---|
| Output tokens (responses) | `caveman` |
| Input tokens (CLAUDE.md, memory) | `caveman-compress` |

### Technical accuracy is not compressed

The skill explicitly preserves:

- Technical terms and proper nouns
- Error messages (quoted exactly)
- Code blocks, file paths, URLs
- Version numbers and flags
- Warnings and caveats

Only prose fluff is removed. A March 2026 paper found that brevity constraints on LLMs can **improve accuracy by 26 percentage points** on some benchmarks — less rambling, more precise answer.

### Auto-clarity for dangerous operations

Caveman automatically suspends compression for:

- **Destructive operations** — `DROP TABLE`, `rm -rf`, irreversible actions
- **Security warnings** — anything that could cause data loss or exposure
- **Multi-step sequences** — where fragment ordering risks misread

After the clear part is done, caveman mode resumes automatically. You don't need to toggle it.

### Intensity levels

| Level | Command | What it does | Best for |
|---|---|---|---|
| **lite** | `/caveman lite` | Drop filler, keep grammar | Readability-sensitive outputs |
| **full** | `/caveman full` | Fragments OK, drop articles | Default daily use |
| **ultra** | `/caveman ultra` | Max compression, `→` for causality | Long sessions, heavy context |
| **wenyan** | `/caveman wenyan` | Classical Chinese 文言文 | Extreme compression experiment |

Start with `full`. Drop to `lite` if teammates read your AI output. Use `ultra` only when context is tight.

### Works across all agents

Caveman is agent-agnostic. It works via system prompt injection, so any agent that accepts a system prompt or rules file is compatible:

Claude Code · Cursor · Windsurf · Gemini CLI · GitHub Copilot · Aider · Continue · Cline · and 40+ more

### Claude Code: auto-activate every session

Add this to your `CLAUDE.md` so caveman activates at session start without a manual `/caveman` command:

```markdown
<!-- CLAUDE.md -->
/caveman full
```

Or for project-specific intensity:

```markdown
/caveman ultra
```

This fires at the top of every session. Pair with `caveman-compress` on the same file to cut both input and output costs.

### The benchmark numbers are real

The **65–75% output token reduction** is measured, not estimated. Numbers come from real sessions across coding, debugging, and explanation tasks. Variation depends on:

- **Task type** — explanations compress more than code generation
- **Intensity level** — `ultra` saves more than `lite`
- **Model verbosity baseline** — Claude 3.x tends to be more verbose than GPT-4o, so savings are higher

> The 26% accuracy improvement cited above is from external research on brevity constraints, not a caveman-specific benchmark. But the directional finding holds: tighter output ≠ worse answers.
