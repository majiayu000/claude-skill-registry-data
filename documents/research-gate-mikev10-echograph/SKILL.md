---
name: research-gate
description: Gates expensive external research (perplexity deep_research) while allowing quick lookups. Enforces knowledge priority - local documentation and project patterns first, external research only when necessary. Permissive mode allows context7, local-rag, and quick perplexity searches. (project)
---

# Research Gate Skill

## Purpose

Enforce knowledge priority by gating expensive research while allowing quick lookups. **Context is king** - project documentation takes precedence over external sources.

## Permissive Mode (Default)

This skill operates in **permissive mode**:
- Quick searches allowed
- Library documentation allowed
- Only expensive deep research is gated

## What Gets Gated vs Allowed

### BLOCKED (Requires Explicit Request)

| Tool | Reason |
|------|--------|
| `mcp__perplexity__deep_research` | Expensive, slow, often unnecessary |

### ALWAYS ALLOWED

| Tool | Reason |
|------|--------|
| `mcp__context7__resolve-library-id` | Needed for accurate library lookups |
| `mcp__context7__get-library-docs` | Prevents API hallucination |
| `mcp__local-rag__query_documents` | Project knowledge |
| `mcp__local-rag__ingest_file` | Adding to project knowledge |
| `mcp__perplexity__search` | Quick lookups, low cost |
| `mcp__perplexity__reason` | Reasoning, moderate cost |
| `WebSearch` | Quick web lookups |
| `WebFetch` | Fetching user-provided URLs |

## Knowledge Priority (Enforced)

When researching any topic, follow this priority:

```
1. CLAUDE.md (project conventions) ← MANDATORY
2. .claude/PLANNING.md (architecture) ← MANDATORY
3. examples/ (working code patterns) ← MANDATORY
4. local-rag (indexed project docs) ← ALWAYS QUERY
5. PRPs/ai_docs/ (library guides) ← CHECK
6. context7 (library APIs) ← ALLOWED
7. perplexity search/reason ← ALLOWED
8. perplexity deep_research ← GATED
```

## When deep_research is Blocked

If `mcp__perplexity__deep_research` is called without explicit request:

```
Research gate: deep_research blocked

This operation is expensive and usually unnecessary.
Already checked:
- local-rag: [X results]
- context7: [available/not available]

To proceed, explicitly request deep research:
- "Do deep research on [topic]"
- "I need comprehensive research on [topic]"
- Use /maintenance:research command
```

## When deep_research is Allowed

The gate opens when:
- User explicitly says "deep research" or "comprehensive research"
- User runs `/maintenance:research` command
- User says "research this thoroughly"
- No relevant results from local-rag AND context7

## Pre-Research Checklist

Before ANY external research, verify:

- [ ] Checked CLAUDE.md for conventions?
- [ ] Checked PLANNING.md for architecture decisions?
- [ ] Queried local-rag for existing knowledge?
- [ ] Checked PRPs/ai_docs/ for library guides?
- [ ] Used context7 for library APIs?

Only proceed to perplexity if local sources insufficient.

## Research Flow

```
User asks about [topic]
        ↓
1. Check local-rag
   Found? → Use it
        ↓
2. Check PRPs/ai_docs/
   Found? → Use it
        ↓
3. Check context7 (if library-related)
   Found? → Use it
        ↓
4. Use perplexity search/reason (quick)
   Sufficient? → Use it
        ↓
5. deep_research ONLY if:
   - Explicitly requested, OR
   - All above sources insufficient
```

## Integration with Agents

### research-expert Agent
- Bypasses gate (designed for research)
- Still follows knowledge priority
- Documents findings in PRPs/ai_docs/

### implementation-guide Agent
- Uses local knowledge first
- Quick lookups allowed
- deep_research requires explicit request

### pattern-enforcer Agent
- Uses project docs only
- No external research needed
- context7 for library verification

## Output When Gated

```
research-gate: Checking local sources first...

Local results:
- local-rag: Found 3 relevant documents
- PRPs/ai_docs/: Found typer-patterns.md
- context7: Typer library docs available

Recommendation: Use local sources. Deep research not needed.

[If user still wants deep research, they must explicitly request it]
```

## Configuration

Projects can adjust gate strictness in CLAUDE.md:

```markdown
## Research Gate Settings

- deep_research: gated (default)
- perplexity_reason: allowed (default)
- perplexity_search: allowed (default)
- context7: always_allowed
- local_rag: always_first
```

## What This Skill Does NOT Do

- Does not block context7 (prevents hallucination)
- Does not block local-rag (project knowledge)
- Does not block quick perplexity searches
- Does not require flags for normal lookups

## Success Metrics

- 90%+ of queries answered from local sources
- deep_research used only when necessary
- No API hallucinations (context7 always available)
- Fast response times (local sources first)

---

**Core Principle**: Project documentation is the source of truth. External research supplements, never replaces, local knowledge.
