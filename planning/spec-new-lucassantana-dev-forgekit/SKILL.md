---
name: spec-new
description: Create a committed per-feature spec under `docs/specs/YYYY-MM-DD-<slug>/{spec,tasks}.md` with frontmatter (status, created, owner, pr, tags). Promotes an ephemeral `.claude/plans/<name>.md` into a persistent, searchable artifact. Use when starting a feature that's larger than a one-shot PR.
type: skill
---

# spec-new

Agent-OS-style spec creation, adapted to our stack.

## When to use
- A plan in `~/.claude/plans/` is ready to execute AND will span multiple sessions or PRs.
- User asks "let's formalize this / make a spec for it".
- You're about to create a branch that will take more than one session.

## When NOT to use
- One-session quick fix → just commit, no spec.
- Research/brainstorm that may not ship → leave as plan.

## Usage
```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/specs.py new "<slug>" \
  --repo <path-to-repo> \
  [--from-plan ~/.claude/plans/<file>.md] \
  [--tags "rag,platform"]
```

Outputs a new folder `docs/specs/<date>-<slug>/` containing:
- `spec.md` — goal + context + approach + verification, with YAML frontmatter (`status: proposed` by default).
- `tasks.md` — checkbox list. If `--from-plan` was used, headers like `### Phase N` become tasks automatically.

## Typical flow
1. Draft plan in `~/.claude/plans/<name>.md` via `plan` skill.
2. `spec-new <slug> --from-plan ...` commits it to the repo.
3. Work through `tasks.md` across sessions. Tick boxes as they land.
4. When all tasks are ✓ and PR merged → use `spec-ship`.
5. Periodically regenerate `docs/roadmap.md` via `roadmap-refresh`.

## Integration with RAG
Specs index under `source_type=spec`, roadmaps under `source_type=roadmap`. Retrieve related past specs before drafting:
```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/query.py --scope spec "<new feature summary>"
```

## See also
- `spec-ship` — archive a shipped spec.
- `roadmap-refresh` — regenerate `docs/roadmap.md` from spec frontmatters.
- `plan` — ephemeral session planning.
