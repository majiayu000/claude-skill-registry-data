---
name: skill-evals-creator
description: |
  Create or update behavior evals (evals.json) for a skill. Invoked by skill-creator. Mode 1 (TDD):
  creates evals from a skill intent description before the SKILL.md is written. Mode 2 (post-skill):
  creates or updates evals based on an existing SKILL.md. Output: evals/evals.json ready for
  skill-evals to run.
license: MIT
metadata:
  version: "1.1.2"
---

# Skill Evals Creator

Creates behavior evals (evals.json) for a skill — from intent before the skill is written (Mode 1), or from an existing skill (Mode 2).

---

## Detect the mode

**Mode 1 — From intent (TDD):** skill-creator passes an explicit intent description. SKILL.md does not exist yet. Design evals from the intent description.

**Mode 2 — From existing SKILL.md:** skill-creator passes the skill path. SKILL.md already exists. Read it and create or update evals based on what the skill actually does.

skill-creator always passes the mode explicitly when invoking this skill.

---

## Mode 1 — From intent

### Step 1 — Fill gaps

You receive the skill intent description from skill-creator. Check if it answers:
1. What should this skill enable Claude to do?
2. When should it trigger? (phrases, contexts)
3. What's the expected output format?
4. What edge cases should it handle?
5. What should it NOT do? (near-miss cases for negative evals)

Ask only about gaps. Don't re-ask what's already in the intent description.

### Step 2 — Design eval cases

Design 3–5 test cases:

| Type | Count | Focus |
|---|---|---|
| Happy path | 2–3 | Clear trigger, core behavior |
| Edge case | 1 | Ambiguous input or unusual phrasing |
| Negative | 0–1 | Near-miss that should NOT activate this skill |

For each case:
- **`prompt`**: A realistic user message — casual, specific, not "test my skill"
- **`assertions`**: 2–3 grading criteria

**Default tier: `structural`.** Before marking any assertion `nuanced`: check whether it can be captured by a text pattern, count, or named entity check. If you think no — check one more time. Only if you still conclude it genuinely requires judgment: mark it `nuanced`.

- `structural` — binary: phrase present/absent, file exists, valid JSON, named entity in output, count ≥ N
- `nuanced` — requires judgment: quality, tone, semantic correctness that no text pattern can approximate

**Nuanced assertions must be justified:** When an assertion is marked `nuanced`, it must include a justification explaining why structural tier was considered and rejected — either in a sibling field (e.g. `nuanced_justification`) or embedded in the `description` field itself.

**Think Red before Green:** assertions must fail without the skill. Before finalizing each assertion, ask: would a capable Claude without this skill satisfy this assertion naturally? The assumed baseline is a *capable* model responding normally — not a degraded or corner-case baseline. If a capable model would satisfy the assertion on any well-formed input, the assertion is generic and must be restructured or removed. Canonical examples of assertions that always fail this test: "criteria are testable" (any capable model writes testable acceptance criteria) and "coverage breadth" (any capable model covers multiple cases). If yes, the assertion is not testing skill value — restructure or remove it.

If you find yourself writing more than one nuanced assertion per case, stop and try harder to make them structural.

**For happy-path cases:** When a happy-path case uses a clear, complete user story with unambiguous intent, include an assertion that the target skill generates output WITHOUT asking a clarifying question first — testing that the skill does not over-ask.

**Assertion precision rules:**

- **Cardinality guards:** If an assertion tests count or cardinality (e.g., "schema includes at least 2 entities with relationships"), add an inline guard for the degenerate case: `"A spec with only one entity passes automatically."` Without a guard, single-entity inputs produce false failures.
- **No "or equivalent" without examples:** If an assertion accepts alternative phrasings, list at least two concrete examples. Vague: `"N/A or equivalent note"`. Specific: `"N/A", "pure in-memory", or "serialisation out of scope"`. Vague alternatives produce inconsistent grading because different graders resolve them differently. This rule applies even without the words "or equivalent": any assertion that checks a semantic quality (e.g., "wins reflect genuine achievements") and defines only failure conditions without a passing example requires a concrete positive anchor — e.g., add `"e.g., 'surpassed the 1k user milestone' would pass"` after the failure description.
- **Behavioral restraint assertions:** If an assertion tests whether the skill withholds a behavior (e.g., "does not ask a clarifying question", "does not produce output for a near-miss input"), include an explicit note in its description that a capable baseline model may also satisfy this assertion for complete-intent inputs. Example: `"Note: this assertion may also pass without the skill for fully-specified inputs."`

### Step 3 — Show and confirm

Present the cases to the user: "Here are the eval cases I designed — anything to adjust?"

Wait for confirmation before saving.

### Step 4 — Save

Save to `<skill-dir>/evals/evals.json`:

```json
{
  "skill_name": "<skill-name>",
  "evals": [
    {
      "id": 1,
      "name": "case-name-kebab",
      "prompt": "realistic user message",
      "assertions": [
        {"name": "assertion-name", "description": "The response should X", "tier": "structural"}
      ]
    }
  ]
}
```

Confirm: "Evals saved to `<path>/evals/evals.json`."

---

## Mode 2 — From existing SKILL.md

### Step 1 — Read the skill

Read `<skill-dir>/SKILL.md`. Understand what the skill does, when it triggers, and what outputs it produces.

If `evals/evals.json` already exists: read it and present the current cases to the user.

If skill-creator also passed an improvement intent (the user is updating the skill): factor it in — the updated evals should reflect the intended new behavior, not only the current behavior.

### Step 2 — Present current state

If evals.json exists: "Here are the current eval cases — what should change?"

If evals.json doesn't exist: proceed to design from scratch based on the skill.

### Step 3 — Design or update eval cases

Follow the same case design rules as Mode 1 Step 2. For updates, keep cases that are still valid and propose additions or replacements for stale ones.

**Review existing nuanced assertions:** For each assertion in the existing evals.json with `tier='nuanced'`, run this structural conversion checklist against the assertion's description:

- Does the check verify the presence of a specific string, phrase, number, or percentage in the output? → **convert to structural**
- Does the check verify that a named condition, metric, or field appears in the output? → **convert to structural**
- Does the check count items or verify a cardinality condition? → **convert to structural**

If any criterion is met: convert to `tier='structural'` and rewrite the description as a mechanically verifiable pattern check. Only leave as `nuanced` if the assertion genuinely requires semantic judgment that no pattern can approximate — and add justification explaining what structural approach was tried and why it fails.

**Flag vacuous absence-checks:** For each existing assertion that only verifies the absence of a word or phrase (e.g. "output does not contain 'INCOMPLETE'", "output does not mention 'error'") without verifying any positive content: add a companion assertion that checks for the PRESENCE of the correct content that should appear. An absence-only check lets any output pass as long as the bad word is absent — even an empty output is "correct." Pair each absence-check with a check for what SHOULD be there.

The companion assertion must test for DOMAIN-LEVEL content — specific indicator names, metric values, or conditions that the skill evaluates — not just the skill's verdict or result label. An assertion that only checks for a pass verdict phrase (e.g. "Meets minimum standards", "VALID", "approved") is insufficient: it would pass even if the skill ignored the domain input entirely. The companion must reference the actual metric names, field names, or threshold values from the skill's evaluation logic. Example: for a thesis-validator skill, pair "output does not flag thesis as incomplete" with "output references RSI, SMA_20, or a specific percentage threshold" — not with "output contains 'Meets minimum standards'."

### Step 4 — Show and confirm

"Here are the eval cases — anything to adjust?" Wait for confirmation before saving.

### Step 5 — Save

Save to `<skill-dir>/evals/evals.json` (same schema as Mode 1). Confirm saved.
