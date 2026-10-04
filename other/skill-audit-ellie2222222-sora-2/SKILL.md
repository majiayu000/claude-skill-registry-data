---
name: skill-audit
description: >-
  Inventories every skill available in the current session (project, user, and plugin scope) and audits
  each one for defects specific to skill files -- frozen references to a file layout that has since moved,
  trigger descriptions that overlap or collide with a bundled built-in, missing scope/verify/report phases,
  instructions that contradict this repo's own conventions doc, restated bloat, and advice with no
  observable check. Fixes what is safely fixable in project-scope skills and proposes the rest. Use when
  asked to "view all skills", "list the skills", "audit/improve the skills", "check my skills", or after
  renaming anything a skill might point at -- distinct from `double-check` (audits the codebase, not the
  instructions that drive it) and `restructure` (where files live, not what the skill files say).
---

# Skill Audit

Two halves, one pass: **show what exists** (the inventory), then **improve it** (the audit). A run that
only lists skills has done half the job; a run that edits without first showing the inventory gives the
user no way to tell whether the right set was even considered.

Read this repo's contributor-facing conventions doc — `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, or a
README section on conventions — **fresh, every run**. It is the authority a skill can contradict, and it
changes; an audit against a remembered copy is an audit against nothing. If no such doc exists, skip the
contradiction checks (category 4) and say so rather than inventing a house style to enforce.

Every pattern below is described generically. Do **not** quote a current skill's text into this file as an
example: this file would then go stale the moment that skill is fixed, which is the very defect
category 10 exists to catch. Find the live instances each run.

## Non-negotiable constraints

- **Project scope is editable; user and plugin scope is not.** Skills under this repo's own
  `.claude/skills/` are committed, shared content — fix them. Skills from the user's home directory or from
  an installed plugin belong to a wider context than this repo: report findings and propose diffs, but do
  not edit them unless the user says to. A silent edit there changes behavior in every other project they
  work on.
- **Never change what a skill is *for* on your own judgment.** Fixing a stale path, a contradiction, or
  duplicated prose is maintenance. Narrowing its trigger, widening its scope, merging it into another, or
  deleting it is a product decision — propose it and stop.
- **A skill edited mid-run does not take effect this run.** The version that was loaded is the version
  driving the current turn. Say so when reporting, so the user doesn't test the fix expecting it to be live.
- **Never weaken a safety rule.** If a skill repeats a constraint from the conventions doc (don't hit a
  rate-limited API, don't touch the database, never accept a credential), that repetition is deliberate
  redundancy — do not "de-duplicate" it away, even though category 6 otherwise targets restatement.

## Phase 0 — Scope

- **Named by the user** (one skill, or a subset) — audit only those, but still print the full inventory, so
  the shape of the whole set is visible.
- **Unscoped** ("audit the skills") — every skill in every scope. This is cheap; skill files are small and
  few.
- Check whether this repo records audit passes somewhere (a reports directory, or a convention its
  conventions doc describes) and skim the most recent skill-audit-flavored one. Don't re-flag what a prior
  pass deliberately kept, and carry its open items forward.

## Phase 1 — Inventory (always print this)

Discover skills; never work from a hardcoded list. Look in every scope that can supply one:

- **Project**: `.claude/skills/*/SKILL.md` under the repo root (and any directory-scoped equivalents, if
  this harness supports them — a skill listed with a path prefix is scoped to that directory).
- **User**: the same layout under the user's home config directory.
- **Plugin**: skills the session lists as `plugin:skill`.
- **Bundled/built-in**: the session's own available-skills listing names these. They can't be read as files,
  and they matter for exactly one reason — a name collision (see category 2).

For each, report one line: `name — scope — lines — last modified — the trigger phrase(s) its description
claims`. Then note anything structural: two skills claiming an overlapping trigger, a project skill whose
name matches a bundled one, a directory with no `SKILL.md`, or a `SKILL.md` whose `name` disagrees with its
directory.

Keep it a table or a list, not prose. The inventory is a map, not a review.

## Phase 2 — Audit each skill

1. **Frozen specifics.** The skill names a concrete path, module, symbol, command, or env var belonging to
   today's layout. Every such reference is a rot risk, and the ones that are *already* broken are bugs
   shipping right now. Grep each named path/symbol against the live repo: a reference that no longer
   resolves is a defect to fix; one that still resolves in a skill written to be layout-agnostic is a
   finding to flag. Distinguish the two — a skill that legitimately encodes a repo-specific rule (this
   repo's commit style, its report template) is allowed to name repo-specific things; a skill written as
   generic tooling is not.
2. **Trigger overlap and collision.** Two skills that would both fire on the same request, with nothing in
   either description saying which wins. Also: a skill whose name matches a bundled built-in, where the
   slash command silently resolves to the built-in instead. Both need an explicit "distinct from X because
   Y" clause in the description — that clause is the fix.
3. **Missing phase.** A skill that mutates anything needs, at minimum: how to scope itself when invoked
   bare, how to verify it didn't break what it touched, and where to record what it did (if this repo has
   that convention). A skill missing the scope phase guesses; missing the verify phase ships breakage;
   missing the record phase makes the next run redo the same discovery.
4. **Contradicts the conventions doc.** The highest-severity category, because a skill overrides default
   behavior by design and so wins the conflict. Check each imperative against the live conventions doc:
   commit/push permissions, attribution trailers, output format, safety rules, naming and style rules. A
   skill that says to do something the doc forbids is a defect regardless of how reasonable it reads.
5. **No observable check.** Advice that cannot be acted on or confirmed — "be thorough", "use good
   judgment", "consider performance". Either give it a concrete trigger and a check, or cut it. Prose that
   cannot fail is prose that does nothing.
6. **Restated bloat.** The same instruction in two sections, or a paragraph that says what its own heading
   already says. Condense. (Exception: the safety redundancy protected above.)
7. **Instructions the harness can't honor.** A named tool, flag, or file path that does not exist in this
   session; a step that assumes a capability the environment lacks (network access, a credential, an
   interactive prompt). Verify the tool/flag actually exists before trusting the instruction.
8. **Stale cross-reference to another skill.** "Distinct from `X`" where `X` was renamed or removed, or
   where `X`'s own description has since drifted so the stated distinction is no longer true. Check both
   directions — a rename fixes one file and orphans the sentence in three others.
9. **Frontmatter defects.** Missing or unparseable YAML; `name` disagreeing with the directory; a
   description that says what the skill *is* but never when to *use* it (the description is the only thing
   the model sees when deciding whether to invoke — a description with no trigger phrases means the skill
   effectively only fires when named explicitly).
10. **Anti-staleness self-discipline.** A skill that hardcodes an example quoting another file's current
    content, or a specific count ("the 6 checks below"), or a dated claim with no reference. Same defect
    class the audit itself must avoid.

Verify every candidate against the live file yourself before fixing. If the search is large enough to be
worth delegating to a read-only exploration agent, ask it for `file:line — the text — which category`
lines rather than full files.

**Calibrate.** A small, well-maintained skill set yields little from categories 5, 6 and 9. That is a real
outcome, not a shallow sweep. The signal usually sits in 1, 2, 4 and 8 — the ones that rot as the repo
moves underneath the skill. Don't manufacture findings against instructions that are simply terse.

## Phase 3 — Fix, propose, verify

- Fix in place: broken references, contradictions, missing "distinct from" clauses, condensable
  restatement, frontmatter defects — in project-scope skills only.
- Propose, don't apply: anything from the "never change what a skill is for" list, and every finding in
  user or plugin scope. Give the exact diff you would make, so accepting is one word.
- Verify mechanically, since skill files aren't executable:
  - The frontmatter parses as YAML and `name` matches the directory.
  - Every path, symbol, and command the skill names resolves in the live repo.
  - No two skills claim the same trigger phrase without a disambiguating clause.
  - If any non-skill file was touched (it shouldn't be), run this repo's real typecheck/test commands,
    discovered from its own config.
- Re-read each edited skill top to bottom once. It is an instruction another agent will follow literally;
  an edit that leaves two halves of a sentence disagreeing is worse than the defect it replaced.

## Phase 4 — Report

1. **The inventory**, per Phase 1 — always, even when nothing needed fixing.
2. **A written record**, following whatever convention this repo already uses for audit passes (same
   directory, same template, same date format, real date from the system). One entry per finding: which
   skill, which category, what it said, what was done — or why it was only proposed.
3. **The chat summary**, in whatever response format this repo expects for a change that touches files. One
   line per skill touched, plus the proposals awaiting a decision. Note explicitly that edits take effect
   from the next invocation, not this one.
