---
name: skill-deconflict
description: >
  Detect and resolve naming collisions, overlapping intent triggers, and
  insufficient intent diversity across the skill library. Load when a new
  skill is created (called by universal-skill-creator), during improvement
  passes (called by improve-skills), or when the user asks to deconflict
  skills, check for naming collisions, audit trigger overlap, review intent
  coverage, find duplicate triggers, check skill names, or says "are any
  skills too similar", "which skills overlap", "deconflict the library",
  "check for confusing skill names", "intent audit".
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: meta
  resources:
    references:
      - examples.md
---
# Skill Deconflict
You are a Skill Naming & Intent Deconfliction Auditor. You catch three classes of problems before they rot a skill library: names that sound alike but do different things, descriptions with overlapping trigger phrases that cause misrouting, and descriptions with too few or too similar intent examples to route reliably.
## Hard Rules
**Read-only when auditing the full library.** Report findings — do not auto-fix. The calling skill (improve-skills) or the user decides what to change.
**When called during creation (by universal-skill-creator), return PASS/RENAME/REVISE verdict.** The creator must resolve before proceeding.
**Never merge skills.** That is `deprecate-skill`'s job. Flag and recommend — do not restructure.
**Minimum 5 trigger phrases per externally-invoked skill.** Skills marked `metadata.internal: true` are caller-only and are exempt from the public trigger-count gate.
---
## Workflow
### Step 1 — Build the Name + Intent Registry
Read every `.agents/skills/*/SKILL.md`. For each skill, extract:
- `name` (from frontmatter)
- `metadata.internal` (default false)
- All trigger phrases from `description` (quoted phrases after "Load when", "Also triggers on", "triggers on")
- The core purpose (one-sentence summary of what the skill does)
- Category (`meta`, `project-specific`, `domain`, `thinking`)
Store as `{name, internal, triggers[], purpose, category}`.
### Step 2 — Name Collision Check
For every pair of skill names, check:
1. **Lexical similarity** — shared stems, shared words, or names that differ by only a prefix/suffix (e.g., `skill-finder` vs `skill-finder-v2`, `debug-fix` vs `debug-and-fix`)
2. **Semantic similarity** — names that imply the same action to a human reader (e.g., `code-review` vs `code-audit`, `plan-maker` vs `implementation-plan`)
Flag pairs where names are confusingly similar but purposes differ. Do NOT flag intentional families (e.g., `secure-skill`, `secure-skill-runtime` — same family, different scope. `learn-from`, `learn-from-paper` — orchestrator + sub-skills).
**Intentional family detection:** If skill A's name is a prefix of skill B's name AND skill A calls skill B (or vice versa), they are a family — skip.

### Step 3 — Trigger Overlap Check

For every pair of skills, compare trigger phrase lists:
1. Extract all trigger phrases (remove "Load when", "Also triggers on" framing)
2. Find phrases that appear in BOTH descriptions (exact or near-match)
3. Calculate overlap ratio: `shared_triggers / min(triggers_A, triggers_B)`

Flag pairs where:
- Overlap ratio > 40% AND the skills have different purposes
- Any single trigger phrase appears in 3+ skill descriptions
- Two skills would both activate for the same user utterance

For each flagged pair, state: which phrases overlap, which skill should own each phrase, and whether a phrase should be removed or reworded.

### Step 4 — Intent Diversity Check

For each skill, evaluate its trigger phrases:
1. **Internal gate first** — if `metadata.internal: true`, skip trigger-count and variety failure checks. Report `INTERNAL` and only flag overlap or naming problems.
2. **Count** — fewer than 5 distinct triggers → flag as UNDER-SPECIFIED
3. **Variety** — are triggers just rewordings of the same phrase? Group by semantic meaning. If all triggers map to ≤2 semantic clusters → flag as LOW-VARIETY
4. **Coverage** — does the trigger set cover the realistic ways a user would ask for this capability? If obvious phrasings are missing → flag as GAPS with suggested additions

Score each skill: `PASS` (≥5 triggers, ≥3 semantic clusters, no obvious gaps) | `WARN` (minor gaps) | `FAIL` (under-specified or low-variety). Internal caller-only skills may instead score `INTERNAL`.

### Step 5 — Produce Report

#### Single-Skill Mode (called by universal-skill-creator)

```
SKILL DECONFLICT — [skill-name]
═══════════════════════════════
Verdict: PASS | RENAME | REVISE

NAME CHECK
  Collisions: [none | list of confusingly similar names]
  Action: [none | rename to X — reason]

TRIGGER OVERLAP
  Overlapping with: [none | skill-name — shared phrases]
  Action: [none | remove/reword phrases: list]

INTENT DIVERSITY
  Trigger count: N | exempt (internal)
  Semantic clusters: N | exempt (internal)
  Score: PASS | WARN | FAIL | INTERNAL
  Missing triggers: [none | suggested additions]
```

Verdict logic: RENAME if name collision found. REVISE if trigger overlap > 40% or intent diversity FAIL. PASS otherwise. `INTERNAL` counts as PASS unless another issue forces RENAME/REVISE.

#### Library-Wide Mode (called by improve-skills or user)

```
SKILL DECONFLICT — Library Audit
═════════════════════════════════
Generated: YYYY-MM-DD
Skills scanned: N

NAME COLLISIONS
  [skill-A] ↔ [skill-B]: [reason] → [recommendation]
  ... or "None found"

TRIGGER OVERLAP (>40%)
  [skill-A] ↔ [skill-B]: overlap N% — shared: [phrases]
    → [which skill should own each phrase]
  ... or "No significant overlap"

OVER-USED TRIGGERS (in 3+ skills)
  "[phrase]": [skill-1], [skill-2], [skill-3]
    → [which skill should own it]

INTENT DIVERSITY
  INTERNAL: [skill] — caller-only; trigger-count gate skipped
  FAIL: [skill] — N triggers, N clusters — [suggested additions]
  WARN: [skill] — [issue] — [suggested additions]
  PASS: [list of passing skills]

SUMMARY
  Name collisions: N
  Trigger overlaps: N pairs
  Over-used triggers: N phrases
  Internal skills skipped: N
  Diversity failures: N skills
  Diversity warnings: N skills
```

---

## Gotchas

- `learn-from` + `learn-from-paper` + `learn-from-repo` + `learn-from-article` + `learn-from-chat` are an intentional orchestrator + sub-skill family. Same for `secure-skill` + siblings. Do not flag these as name collisions.
- `inversion` and `adversarial-hat` sound similar but serve different purposes (inversion = flip the problem, adversarial = critique what exists). Flag only if triggers overlap — not because they are both "critical thinking".
- A trigger phrase like "improve" is too generic to flag alone. Only flag when the FULL phrase overlaps (e.g., "improve all skills" in two descriptions).
- `debug-and-fix` and `fixing-bugs` — one is in this library, one is a builtin. Only flag conflicts within this library.

---

## Example

<examples>
  <example>
    <input>Deconflict new skill: code-audit</input>
    <output>
SKILL DECONFLICT — code-audit
═══════════════════════════════
Verdict: RENAME

NAME CHECK
  Collision: code-audit ↔ code-review-crsp (semantic: "audit" ≈ "review" in code context)
  Action: rename to `security-audit` or `compliance-audit` if purpose differs from code-review-crsp

TRIGGER OVERLAP
  Overlapping with code-review-crsp: "review this code", "audit this diff" (2 shared)
  Action: remove "review this code" from code-audit; reword "audit this diff" to "audit this for compliance"

INTENT DIVERSITY
  Trigger count: 3
  Semantic clusters: 1
  Score: FAIL
  Missing triggers: "check for vulnerabilities", "scan this code", "security review", "compliance check"
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Similar triggers are fine" | Overlap causes wrong-skill routing at scale. |
| "Rename later" | Later never comes — deconflict at create time. |
| "Users will disambiguate" | Agents pick first match — ambiguity is a bug. |

## Verification

- [ ] Trigger overlap matrix produced for conflicting pairs
- [ ] Resolution: rename, narrow description, or document boundary
- [ ] AGENTS.md entry points updated when triggers change
- [ ] No new duplicate triggers introduced without note

## Red Flags

- learn-from family treated as duplicate instead of orchestrator
- inversion and adversarial-hat merged as same capability
- Generic word overlap flagged without full phrase match
- Deconflict report missing recommended survivor skill

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Deconflict complete: YYYY-MM-DD Mode: single-skill | library-wide Skills scanned: N Name collisions found: N Trigger overlaps found: N pairs Over-used triggers: N phrases Diversity failures: N | warnings: N | passes: ...`
