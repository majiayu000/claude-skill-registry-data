---
name: recall
description: This skill should be used when the user asks to "recall related knowledge", "search previous solutions", "check what we learned before", "look up past decisions", or when starting a new task and wanting to surface prior context. Searches .claude/knowledge/ for solutions, patterns, and ADRs related to the current task before spending tokens on fresh exploration.
---

# Skill: recall

Searches the project knowledge base (`.claude/knowledge/`) to surface relevant prior learning before starting a new task. Recall results reduce redundant exploration and prevent repeating solved problems.

## Knowledge base structure

```
.claude/knowledge/
├── solutions/    bug-fix captures: what broke, why, how fixed
├── adrs/         architectural decision records (MADR format)
└── patterns/     reusable implementation patterns with code examples
```

## Search procedure

### 1. Extract search terms from the issue

Read the issue title and body. Extract:
- Domain keywords (e.g., "booking", "appointment", "payment")
- Technical keywords (e.g., "Flyway", "Server Component", "Tailwind")
- Error messages or symptoms (if it's a bug fix)

### 2. Search each knowledge directory

```bash
# Semantic search via grep across all knowledge files
grep -ril "<keyword>" .claude/knowledge/solutions/ 2>/dev/null
grep -ril "<keyword>" .claude/knowledge/patterns/ 2>/dev/null
grep -ril "<keyword>" .claude/knowledge/adrs/ 2>/dev/null
```

Read the full content of any file that matches.

### 3. Produce recall summary

Write a "Prior Knowledge" section at the top of `exploration.md` (or as a standalone note if exploration hasn't started yet):

```markdown
## Prior Knowledge (from recall)

### Related ADRs
- [ADR-0003](docs/adr/0003-...) — relevant decision + brief summary

### Related Patterns
- `patterns/filename.md` — one-line description of relevance

### Related Solutions
- `solutions/bug-slug.md` — one-line description of relevance

### How this affects the task
<!-- Brief note on how prior knowledge should shape exploration or design -->
```

## Graceful degradation

If `.claude/knowledge/` does not exist or is empty, log "Knowledge base empty — proceeding without recall" and continue. Do not block the workflow.

## When recall is sufficient to skip exploration

After recall, assess whether the retrieved knowledge fully covers the task scope. If yes, note in `state.yaml`:

```yaml
config_used:
  skipped_phases: [explore]
  recall_was_sufficient: true
```

And proceed directly to clarification/design with the recalled knowledge as context.
