---
name: forge-skill-testing
description: "Standard test protocol for a new/changed Forge skill: activation-test (trigger vs near-miss phrases, target >=95%) + opt-in fresh-session A/B benchmark. Use when creating or editing any skill."
---

# forge-skill-testing — activation + A/B test protocol

**Self-improvement substrate (wp-skill-evals):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction, append it to `learnings.md` with a date and real evidence — never invent a lesson
that didn't happen.

**Origin (wp-disclosure-ab, backlog item 8, YT-SWEEP-2026-07-31, 4 source videos:
7s9Fnorg3eI, O_z9vDLgvoY, UtGszoiwrsQ, wQ0duoTeAAU):** complementary to the description-length budget
work — a short, well-formed description is step 1 (discovery), but nobody was measuring whether
a skill actually **activates** on real phrasing, or whether it genuinely helps once it does. Community
data cited in the sweep: activation drops to ~20% with vague descriptions, and this is essentially
never measured in practice.

**This is the CHECKLIST/PROTOCOL, not an automated runner.** No script executes these steps — they are
a human/agent-in-the-loop procedure, the same way `forge-code-review`'s severity scale is a method, not
a linter. Step 2 after `forge-skill-evals.cjs`'s binary evals (see that tool's own header comment for the
"step 1 -> step 2" pointer).

## When to use
- A skill's `SKILL.md` frontmatter `description` was just written or rewritten.
- A skill's body changed enough that its trigger conditions may have shifted.
- Skill Boss or Head Chef wants real evidence a skill is actually discoverable/useful, not just present.
- NOT required for every trivial doc tweak (a typo fix, a one-line clarification) — use judgment; this
  protocol costs real runs (see part 2) and is opt-in per skill change, never a merge/ship gate.

## Part 1 — Activation test (cheap, do this for every meaningfully-changed skill)

1. Write **6+ trigger phrases** — realistic things an owner/agent would actually type that SHOULD cause
   this skill to be selected/loaded. Use the skill's own "When to use" bullets and description as the
   source, but phrase them the way a real request sounds, not a copy of the description.
2. Write **4+ near-miss phrases** — realistic requests that sound adjacent but should NOT activate this
   specific skill (they belong to a sibling skill, or a different domain entirely). A near-miss that
   accidentally activates the skill is a real precision problem, not a pass.
3. Run each phrase in a fresh session (or ask "would this skill fire on X?" against the current
   frontmatter honestly) and record activation Y/N per phrase.
4. **Target: >= 95% correct** (trigger phrases activate AND near-miss phrases don't, combined). Below
   that, the description likely needs sharper "when to use" language — rewrite and re-test, don't just
   accept a low score.
5. **Log the result in `.claude/FORGE_SKILL_REGISTRY.md`** — that table has no dedicated activation-test
   column (see its own legend), so append a compact, dated note to the skill's existing **Safety notes**
   cell in the exact shape `activation <correct>/<total> (<YYYY-MM-DD>)` (see the template below for a
   worked example). Never touch any other skill's row while doing this.

Template with the exact phrase-count/scoring/logging worksheet: `references/activation-test-template.md`.

## Part 2 — Fresh-session A/B benchmark (OPT-IN, costs real runs, never a gate)

This is the more expensive, complementary measurement: does the skill actually help, net of the tokens
it costs to load?

1. **Designer/tester split, no context bias.** One session (Claude A) designs or edits the skill.
   A SEPARATE, genuinely fresh session (Claude B, no shared conversation history with A) is the one that
   attempts the target task — never the same session that just wrote the skill grading its own work.
2. **3 runs with the skill, 3 without.** Same representative task, run 3 times with the skill available
   and 3 times with it unavailable (temporarily moved aside, or a throwaway project copy without it).
3. **Measure pass-rate, wall-clock time, and approximate token usage** (via `/context` or session stats)
   for each of the 6 runs.
4. **Record the real numbers** in the skill's own `learnings.md`, dated — a hypothetical/expected result
   standing in for a run that didn't happen is a fabrication, not a benchmark.
5. **This is genuinely optional and never a merge/ship gate.** It costs real session time and tokens;
   run it when a skill is new, when its net value is genuinely in doubt, or when the owner asks for
   evidence a skill is worth its context cost — not as a checkbox on every routine skill edit.

Full worked table (runs, pass/fail, time, tokens, verdict): `references/activation-test-template.md`.

## Relationship to forge-skill-evals.cjs

`forge-skill-evals.cjs` (`evals.json` + binary assertions) answers "is the skill's file/config/content
structurally correct?" — a cheap, deterministic, always-safe-to-run check. This protocol answers a
different, harder question — "does the skill actually get selected on real phrasing, and does it help
once selected?" — which needs judgment and, for Part 2, real spend. Run evals first (fast, free,
mechanical); run this protocol when a description/body genuinely changed and the answer to those two
harder questions actually matters.

## Honesty
Never report an activation score, an A/B pass-rate, a time, or a token count that wasn't actually
measured in a real run. "Not yet executed" is a valid, honest status for a skill whose protocol hasn't
been run — it is never silently upgraded to a fabricated passing number.
