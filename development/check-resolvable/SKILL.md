---
name: check-resolvable
description: Audit the whole skill/tool library so it stays a DRY, MECE resolver — no duplicate skills, no overlaps, no gaps. Use after adding or editing a skill, or when the library feels cluttered.
---

# Check Resolvable

Audit the entire skill/tool registry and report whether it is a clean **resolver**: every capability reachable by name, nothing duplicated, nothing overlapping, nothing missing. Run it whenever the library changes — especially right after [`skillify`](../skillify/SKILL.md) adds something new.

> "I run *check resolvable*, which is — look at all the other skills and tools that exist, and is it DRY (don't repeat yourself) and is it MECE (mutually exclusive, collectively exhaustive)? It's bad to have ten skills that do the same thing. It's good to have one skill or one tool that has parameters." — Pete Koomen / Andrej Karpathy, YC

## The two tests

**DRY — don't repeat yourself.**
No two skills should do the same job. If two skills differ only in a value (one emails Slack, one emails Discord), that's *one* skill with a parameter. Collapse near-duplicates; don't tolerate them.

**MECE — mutually exclusive, collectively exhaustive.**
- *Mutually exclusive:* each skill owns a distinct job. Given a task, exactly one skill is the obvious choice — no "which of these three do I use?" ambiguity.
- *Collectively exhaustive:* every skill is reachable from the resolver (the index the agent reads), and the index covers the real surface of work — no orphan skill files, no silent gaps.

## Procedure

1. **Enumerate.** List every skill (e.g. `skills/*/SKILL.md`) and every entry in the resolver index (`AGENTS.md` / `CLAUDE.md` skills list / tool registry).

2. **Cross-check index ↔ files.** Flag:
   - Skills on disk with **no** resolver entry (unreachable — invisible to the agent).
   - Resolver entries pointing at **missing** files (dead links).

3. **DRY pass.** Group skills by what they actually *do* (read the `description` + procedure, not just the name). For each group with overlap, propose the merge: which becomes the canonical skill, what parameter absorbs the difference, which files to delete.

4. **MECE pass.** For each remaining skill, confirm its job is distinct and its trigger ("use when …") doesn't collide with another's. Flag pairs whose triggers overlap — they'll cause the agent to pick wrong. Note obvious gaps in coverage.

5. **Report.** Output a short table:

   | Issue | Skills involved | Fix |
   |-------|-----------------|-----|
   | Duplicate | `email-slack`, `email-discord` | Merge → `notify` with `channel` param |
   | Unreachable | `summarize-pdf` | Add resolver entry |
   | Dead link | `AGENTS.md → old-skill` | Remove entry |
   | Trigger overlap | `fix-bug`, `debug` | Sharpen "use when" on each |

   Don't apply changes silently — propose them, then make the merges/edits the user approves. After applying, re-run this audit to confirm the registry is clean.

## Why it matters

The resolver is only as valuable as it is clean. A DRY + MECE registry means the agent (and every teammate, and Claude Code / Cursor / Codex reading the same files) can always find the *one* right skill for a task. Clutter — ten skills for one job, orphan files, colliding triggers — is what makes a growing skill library degrade instead of compound.
