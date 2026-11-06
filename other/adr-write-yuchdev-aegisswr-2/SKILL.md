---
name: adr-write
description: User-invoked as /adr-write <title>. Scaffolds a new Architecture Decision Record in docs/adr/ using the MADR template, pre-filling context from recent git log and open GitHub issues. Use when a design decision needs to be recorded before implementation.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
invocation: /adr-write <title>
# Ported from Claude (.claude/skills/adr-write/SKILL.md) on 2026-07-03
---

# ADR Write (MADR)

Scaffold a new ADR for the decision titled `$ARGUMENTS`.

## Steps

1. Determine the next ADR number: list `docs/adr/`, find the highest
   `NNNN-` prefix, increment (zero-padded to 4 digits). If none exist, start at
   `0001`. Filename: `docs/adr/NNNN-<kebab-title>.md`.
2. Seed **Context** from the repo: run `git log --oneline -10` and, if `gh` is
   authenticated, `gh issue list --state open --limit 10`. Summarise what is
   prompting this decision.
3. **Read the canonical template `docs/adr/template.md` and copy its structure
   verbatim** — do not invent your own headings. Fill `NNNN`, the title, today's
   date (from session context), and the seeded Context. Leave **Status:
   Proposed**. See the section spec in `.github/copilot/skills/adr-write/references/template-guide.md`
   for what each section must contain.
4. Add an index line to `docs/README.md`.

## Template

The single source of truth is **`docs/adr/template.md`** (read it at generation
time — do not paste a copy here that can drift). It uses the sections:
`Context`, `Decision`, `Alternatives Considered` (a table), `Consequences`
(Positive / Negative), `Validation / Rollout`, and `Links`.

## Output

Print the path of the created ADR and a one-line summary. Note that the
`app-architect` agent owns the decision content - this skill only scaffolds and
seeds it. Leave it `Proposed` for human/architect sign-off.

## Completion checklist

- [ ] File created at `docs/adr/NNNN-<kebab-title>.md` with correct zero-padded sequence number
- [ ] Structure matches `docs/adr/template.md` exactly
- [ ] Status is `Proposed`
- [ ] `Alternatives Considered` table has at least the chosen option + one rejected alternative
- [ ] `Links` section points at the driving roadmap task / issue
- [ ] `docs/README.md` has a new index line for the ADR
- [ ] `/link-check` passes on the new file
