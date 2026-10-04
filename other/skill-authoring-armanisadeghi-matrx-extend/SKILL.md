---
name: skill-authoring
type: Skill
title: "skill-authoring — skills that fire, fit, and are proven"
description: "Rules for SKILL.md files that trigger, fit, and are proven. Use when creating a SKILL.md, rewriting its description, splitting an oversized SKILL.md, or editing one because an agent ignored, misread, or never fired it."
tags: [meta, skills, agents, docs-system]
timestamp: 2026-09-12T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/skill-authoring/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# skill-authoring — skills that fire, fit, and are proven

A skill is a **guard on agent behavior**, so fix-the-class applies: a skill you never watched
fail-then-pass is not a guard. These rules sit on top of the `docs` skill (whole-document review, never lose a rule) — read
that too.

## 1. The description is the trigger — and the listing is capped

How Claude Code loads skills ([official docs](https://code.claude.com/docs/en/skills), checked 2026-09-10):
- The model sees only each skill's `name` + `description` (+ `when_to_use`) until it invokes the skill.
  That combined text is **truncated at 1,536 chars** per skill in the listing (`skillListingMaxDescChars`
  changes the cap).
- The **whole listing is budget-capped** at 1% of the context window (`skillListingBudgetFraction`, or
  `SLASH_COMMAND_TOOL_CHAR_BUDGET` as a fixed char count, raises it). The listing **always keeps every
  skill name**; on overflow Claude Code **drops descriptions starting with the skills invoked least**, and
  a `skillOverrides` entry of `"name-only"` drops one on purpose. A skill without its description can
  still be invoked but is rarely chosen on its own — every character you add can push another skill's
  trigger out.
- Measured in the Claude Code 2.1.263 source, beyond the docs: 4 chars/token (8,000 chars at 200k,
  ~40,000 at 1M); **every entry still costs its name + 2 chars**; descriptions are admitted greedily by
  **usage score** (use count, 7-day half-life). So every duplicate entry (a synced copy listed as
  `aidream:x`) burns budget even with no description.
- Skills in `.claude/skills` of subdirectories below the launch dir load **lazily**, the first time a
  file there is read or edited. That is why repo-scoped duplicates (`aidream:x`, `matrx-frontend:x`)
  appear mid-session, each one another listing entry.
- `disable-model-invocation: true` removes the description from context entirely: the skill becomes
  user-invoked only (`/name`), and subagents cannot preload it either.

Rules:
- **Recipe:** `<what it is — one noun phrase>. Use when <trigger>, <trigger>, … .` Primary use case
  first. Target **≤300 chars**, hard **500** — our rule, stricter than the docs, which set only the
  1,536 cap and say to put the key use case first.
- **Triggers are what the agent will actually see:** situations, symptoms, file paths/globs, error
  strings, the user's words.
- **Never the procedure.** No "Covers / Encodes / Enforces / pipeline", no step lists — an agent handed
  the procedure in the description executes the summary and skips the body.
- **No dates, rulings, approvals, or keyword dumps** — those live in the body. Cutting a dump is a
  MOVE, not a deletion: **every trigger you drop from the description gets a row in a relocation
  table in the body — old trigger → its new home** — an index a repo grep still finds. That table is
  what "don't lose a trigger" actually asks for, and it is what you show the owner.
- **At most one `NOT for X (use Y)`**, only when a sibling skill is a real near-miss.
- **Slash-only skill** (reached by `/name` and by nothing else) → `disable-model-invocation: true`.
  First `grep -r "<name>"` across all skills and agent definitions — no other skill or subagent can
  reach it afterwards.
- **The lint enforces it:** `python3 common-docs/meta/scripts/skill_descriptions.py lint`
  (`--repo <dir>`, `--workspace`) fails a description over 500 chars unless allowlisted and over
  1,024 always; `skill-description-allowlist.txt` only shrinks. **1,024 is a hard ceiling, never a
  target** — the house target is ≤300, and every proven-good rewrite on record landed at 276–300.
  Writing up to a cap is the failure this rule exists to stop. Wired into `okf_lint.py`, aidream
  `scripts/check_skill_descriptions.py`, and matrx-frontend `pnpm check:skill-descriptions`.
- **A trigger that keeps missing** in a footgun area → run the `skill-creator` plugin's description
  optimization loop (should-fire + near-miss queries), never lengthen by hand.

## 2. Size — the body routes over branches

- **SKILL.md body ≤500 lines** — the file itself, not the directory. Over budget is fixed by
  relocating, not by squeezing prose.
- **Branch test:** inline what every run needs; move what only some runs reach (one stage, one
  provider, one variant, a long API reference) into a sibling file named for the branch, with a
  pointer that says **when** to read it: `Stage V only → read stage-v.md.`
- **A routing list is read as complete.** A "read only the branch your run reaches" list names
  **every** companion, pre-existing ones included; an unlisted file is never opened (matrx-frontend
  `surface-authoring` evals E1: 0/3 reps opened the one reference the list omitted and lost its completion gate). Never end
  a route with "nothing else": pointers inside a branch file (e.g. "run the `safe-cutover` skill first")
  still bind, and 2/3 common-docs `data-to-kinds` reps skipped one citing those words.
- **One level deep.** SKILL.md → file, never file → file. A reference file over 100 lines opens with a
  contents list.
- **Point at `--help` or a script** instead of restating flags or deterministic steps.
- **Splitting relocates; every rule survives.** Canonical SKILL.md companion files ship with
  `sync_skills.py` automatically (in common-docs they carry OKF frontmatter).
- **Every step ends on a checkable completion criterion** — "every touched table returns
  `canonical_certify_ok`", never "understanding reached".

## 3. Match the form to the failure

| Observed failure | Write | Never write |
|---|---|---|
| Knows the rule, skips it under pressure | Prohibition + named replacement + §4 counters | Soft advice ("prefer", "consider") |
| Complies, but output has the wrong shape | A recipe: what the output IS, its parts, in order | A list of don'ts — they get negotiated |
| Omits a required element | A REQUIRED slot in the template it fills | A prose reminder near the template |
| Behavior depends on a condition | A conditional on an observable predicate | A rule plus an exemption clause |

**No nuance clauses** ("unless it matters") — they reopen the negotiation. A real exception is its own
conditional.

## 4. Discipline skills — close the loopholes you saw

A discipline skill guards a rule that costs the agent time and that it already knows (verify live,
never revert a gate, never silence a type error).
- **`## Rationalizations`** — a two-column table, `Excuse (verbatim) | Reality (one line)`. **Rows only
  from observed transcripts or real incidents**; an imagined row is bloat.
- **`## Red flags`** — 3–7 thoughts that precede the violation ("this case is different", "the gate is
  blocking my release").
- Put the about-to-violate symptom in the description: `Use when … or when tempted to …`.

## 5. Prove it

Required for a new skill, an edit made because an agent misbehaved, any discipline skill, and any
description rewrite. Exempt: typo, path, and pointer fixes.

1. **Scenario from reality.** Use the prompt or transcript that actually failed (incident, feedback
   item, review-queue row). Only with no incident, synthesize one with real repo paths, ≥2 real
   pressures (time, sunk cost, "the user said skip it", a blocking gate), and a forced choice.
2. **RED — baseline.** Dispatch fresh subagents (lane named; `standard` unless the consuming lane is
   known) with the scenario and **without** the new text (for an edit: the current skill). **3 reps.**
   Record choices and rationalizations verbatim. **No failure → nothing to fix; do not write the guidance.**
3. **GREEN.** Write the minimum that answers the recorded failures. Same scenario, lane, 3 reps,
   **with** the skill. Pass = all 3 comply and cite the skill.
4. **REFACTOR.** A new rationalization → a §4 row + red flag → rerun. Reps that disagree with each
   other mean the wording is not binding — change the form (§3) before adding words.
5. **Trigger check** (description changed): 3 should-fire and 3 near-miss prompts to fresh subagents
   with the skill installed; record fire / no-fire.
6. **Record the proof** in `<skill>/evals.md`: scenario, lane, date, RED result, GREEN result,
   rationalizations harvested. It is the regression test — the next editor reruns it. The author never
   grades a run it performed itself. **Every recorded rep cites its agent id or transcript path** —
   a verdict nobody can re-check against the transcript is a claim, not proof; when a rep's transcript
   genuinely cannot be recovered, its row says "transcript not recoverable" rather than looking
   auditable. (Two records shipped without ids on 2026-09-10 and had to be reconstructed from runner
   transcripts two days later.)

## Before you save — checklist

- [ ] Description follows §1: noun phrase + `Use when`, ≤300 chars (500 hard), no procedure, no dates;
  `skill_descriptions.py lint` passes.
- [ ] Slash-only? `disable-model-invocation: true` after the cross-skill grep.
- [ ] Body ≤500 lines; branch-only material disclosed one level deep with when-to-read pointers; any
  routing list names every companion file.
- [ ] Every rep in `evals.md` cites an agent id / transcript path, or says it is not recoverable.
- [ ] Split a SKILL.md? Every original line survives somewhere in the directory (re-grep or an oracle), an
  agent that did not split it verifies routing, and a §5 scenario run proves no behavior was lost.
- [ ] Guidance form matches the observed failure (§3).
- [ ] Discipline skill: rationalization rows and red flags come from observed failures.
- [ ] §5 run done (or exempt) and `evals.md` updated.
- [ ] `docs` skill §2 and §8 passed. Canonical SKILL.md? Edit the one under `common-docs/skills/` — never a synced copy — run
  `sync_skills.py`, commit every touched repo.
