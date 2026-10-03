---
name: wm
description: Working Memory for AI coding assistants. Captures tacit knowledge from sessions and surfaces relevant context. Use "wm show" to review state, "wm compress" to synthesize.
license: Apache 2.0
---

# wm — Working Memory for AI Coding Assistants

wm automatically captures tacit knowledge from your coding sessions and surfaces relevant context for each new task. It's the memory layer that helps AI assistants learn how *you* work.

## Commands

### wm show [what]

Review current working memory state.

```bash
wm show           # Show state.md (default)
wm show state     # Show .wm/state.md
wm show working   # Show compiled working set
wm show sessions  # List available sessions
```

**Use this to:** Check what wm has captured before starting work.

### wm compress

Compress and synthesize working memory state.

```bash
wm compress
```

Abstracts accumulated knowledge to higher-level patterns, reducing size while preserving critical insights.

**Use this when:** State.md is getting too large or redundant.

### wm distill

Batch extract tacit knowledge from all sessions in this project.

```bash
wm distill
```

Processes all sessions and extracts:
- Metis (wisdom patterns)
- Guardrails (constraints discovered)

**Use this when:** Setting up a new project or after many sessions.

### wm pause [extract|compile|both]

Pause or resume wm operations.

```bash
wm pause extract    # Pause extraction only
wm pause compile    # Pause compilation only
wm pause both       # Pause all operations
wm resume           # Resume operations
```

**Use this when:** You want to work without wm capturing/injecting context.

### wm init

Initialize wm in a project.

```bash
wm init
```

Creates `.wm/` directory structure:
- `state.md` - Current session state
- `distill/` - Extracted patterns
- `sessions/` - Session archives

**Use this when:** Starting a new project.

## Dive Prep (Agent-based)

For complex context gathering, use the dive-prep agent:

```
/wm:dive-prep [intent or context]
```

This spawns an agent that:
1. Detects OH connection and suggests linking endeavors
2. Gathers local context (CLAUDE.md, git state, etc.)
3. Fetches OH context if available
4. Writes `.wm/dive_context.md` with curated grounding

## What Gets Captured

**Tacit knowledge** is the unspoken wisdom in how someone works:

- Rationale behind decisions (WHY this approach)
- Paths rejected and why (judgment in pruning options)
- Constraints discovered through friction
- Preferences revealed by corrections
- Patterns followed without stating

**Not captured:**
- What happened ("Fixed X", "Updated Y")
- Explicit requests or questions
- Tool outputs or code snippets

## Storage

Working memory stored in `.wm/`:
```
.wm/
├── state.md          # Current session state
├── dive_context.md   # Prepared dive context
├── distill/
│   ├── metis.md      # Wisdom patterns
│   └── guardrails.md # Constraints
└── sessions/         # Archived sessions
```

## Quick Reference

```text
wm show               # Review current state
wm compress           # Synthesize state
wm distill            # Extract from all sessions
wm pause extract      # Pause extraction
wm resume             # Resume operations
wm init               # Initialize in project
```
