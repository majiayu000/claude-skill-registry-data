---
name: audit-against
description: "Grade a piece of work against the rubric of a book-to-skill knowledge skill (e.g. /metzify, /decomplexify) using a parallel mixture-of-experts council. Use when the user runs `/audit-against <knowledge-skill> [target]`, or asks to 'audit this against <skill>', 'grade my approach against <book skill>', 'how does this hold up against Metz/McConnell', or 'run the council on this against <skill>'. Selects the glossary/pattern/chapter criteria relevant to the target, fans out one expert per criterion, adversarially verifies each weakness, and returns a graded scorecard plus severity-ranked weaknesses. Distinct from /audit (generic PASS/FAIL against ad-hoc criteria): this derives its rubric from a book-to-skill output's actual frameworks."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Agent
argument-hint: <knowledge-skill> [file|dir|--repo|--plan "..."]
---

# Audit Against a Knowledge Skill

Grade a target against the frameworks of a book-to-skill knowledge skill, using a mixture-of-experts council: **select relevant criteria (gating) → one expert per criterion (experts) → adversarially verify → synthesize a scorecard (combine)**.

Invocation: `/audit-against <knowledge-skill> [target]`

- Arg 1 — the knowledge skill slug (e.g. `metzify`, `/metzify`, `decomplexify`). Required.
- Arg 2 — the target (optional; defaults to the working-tree diff).

## Step 1 — Resolve the knowledge skill

Strip any leading `/`. Find its directory (first hit wins): `~/.claude/skills/<slug>/`, `.agents/skills/<slug>/`, `~/.config/agents/skills/<slug>/`, `~/.config/amp/skills/<slug>/`.

A book-to-skill output has `SKILL.md` plus some of `glossary.md`, `patterns.md`, `cheatsheet.md`, and a `chapters/` dir. Confirm `SKILL.md` exists.

- **Not a book-to-skill output** (no glossary/patterns/chapters): degrade — treat the `## ` sections of `SKILL.md` (and any `references/*.md`) as the criteria source, then continue. Tell the user you're running in degraded mode.
- **Not found at all**: stop and list the slugs available under `~/.claude/skills/`.

## Step 2 — Resolve the target

Auto-detect from arg 2. Read the **content** in full now — subagents cannot see your context, so every grader prompt must carry the target text inline.

| Arg 2 | Target | How to read |
|-------|--------|-------------|
| *(absent)* | Working-tree diff (default) | `git diff HEAD` (staged+unstaged). If empty, fall back to `git diff` then last commit `git show HEAD`. State which you used. |
| a path to a file | that file | Read it. |
| a path to a dir | that subtree | `git ls-files <dir>` or Glob; read the source files (skip vendored/build dirs). Cap at ~15 files; log any omitted. |
| `--repo` | whole repo | Warn this is the most expensive mode. Read the primary source files; cap and log omissions. |
| `--plan "..."`, or pasted prose / a quoted approach | inline approach | Use the text verbatim as the target. |

Record a `target_kind` of `diff | file | dir | repo | plan` — it sets how a finding's **location** is expressed (file:line for code; "step N" or a quote for a plan).

## Step 3 — Gate: select the relevant criteria (do this inline)

This is the heart of the skill — "clock which contents are relevant." A book-to-skill output is small; read it directly rather than dispatching a scout.

Read from the resolved skill (anchored to its known structure):

- `SKILL.md` → the `## Core Frameworks & Mental Models` section (each bold `**Name**` lead-in is a candidate criterion) and the `## Topic Index` / `## Chapter Index` tables (for routing).
- `patterns.md` → each `## <Pattern>` header is a candidate criterion (with its When/How/Trade-offs).
- `glossary.md` → each `**Term** — definition (Ch N)` line is a candidate concept.
- `cheatsheet.md` → condensed rules and decision tables (use as supporting detail).

Build a candidate list, then **score each candidate's relevance to the target's domain** (does the target actually touch what this criterion governs?). Keep those clearly relevant; **cap at 8–12 criteria.** For anything dropped, note it briefly so coverage is honest (silent truncation reads as "covered everything").

For each kept criterion, read the chapter file it points to (via the Chapter/Topic Index) only if you need the full rule statement — otherwise the SKILL.md/patterns.md text is enough. Produce the **rubric**: a numbered list, each entry = `{name, rule statement, source (file + section / Ch N)}`.

If after scoring fewer than 3 criteria are relevant, tell the user the skill is a poor fit for this target and ask whether to proceed anyway.

## Step 4 — Council: one expert per criterion (parallel)

Read `references/rubric.md` for the grade scale, lens definitions, severity tiers, and the exact grader/verifier prompt templates. **Dispatch all experts in a single message** (multiple `Agent` calls, `subagent_type: general-purpose`, `model: sonnet`) so they run concurrently — this is the parallel swarm.

Each expert gets ONE criterion plus the full target content, and applies the three fixed lenses internally (Adherence, Severity, Applicability). It returns a structured grade + evidence + a draft weakness if the grade is C or worse. Fill the grader template from `references/rubric.md` for each criterion; do not improvise the schema.

## Step 5 — Verify: refute each weakness (parallel)

Collect every draft weakness from Step 4. **Dispatch one skeptic per weakness in a single message**, using the verifier template in `references/rubric.md`. Each skeptic tries to *refute* the weakness (wrong criterion? misread code? not actually a violation?) and returns `upheld | refuted` with reasoning. **Drop refuted weaknesses.** If there are no draft weaknesses, skip this step.

## Step 6 — Synthesize the scorecard

Render the output using the **scorecard template** in `references/rubric.md`: the graded per-criterion table, the severity-ranked (verified) weaknesses with location + fix + the criterion each violates, what the target does well, the criteria judged not applicable, and an overall weighted verdict. Keep prose tight; the table and the ranked list carry the value.

## Notes

- Scope is book-to-skill knowledge skills. Don't build robust handling for arbitrary skills beyond the one-line degraded mode in Step 1.
- Subagent prompts must be self-contained: the criterion text + the target text both go in. Graders cannot read your files or context.
- Match the council size to the ask: a quick check can use single-vote verification; "thoroughly audit" / "be comprehensive" warrants more criteria and 3-vote skeptic panels (see `references/rubric.md`).
