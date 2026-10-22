---
name: rules-distill
description: "Distill principles from the installed skills into the always-loaded rules layer."
license: MIT
user-invocable: true
origin: shimo4228
disable-model-invocation: true
---

# rules-distill — promote environment-specific facts to rules

Scan installed skills, find principles that belong in the **always-loaded rules layer**, and distill
them into rules — appending to, revising, or creating rule files. The skill produces
candidates and verdicts; it **never edits rules without your approval**.

## When to Use

- Periodic rules maintenance (monthly, or after installing new skills)
- After a `skill-stocktake` reveals patterns that should be rules
- When rules feel incomplete relative to the skills in use

## Phase 1 — Inventory (Glob, exhaustive)

Enumerate with Glob (no script):

- Skills: `~/.claude/skills/*/SKILL.md`
- Rules: read every `~/.claude/rules/**/*.md` in full — the corpus is small, so no grep pre-filter is needed

> Glob targets only skill definition files, so dependency markdown under `.venv` /
> `.pytest_cache` is excluded structurally.

Present the counts (skills scanned, rule files, headings) before analysis.

## Phase 2 — Cross-read & Verdict (inline, holistic)

Read every skill body and every rule into one context and analyze them together —
extraction and matching are a single pass. Seeing all skills at once is what makes the
recurrence count exact and the "not already in rules" test reliable.

**A principle is a candidate only if ALL of these hold:**

1. **Environment-specific** — a fact, a wiring, or a trap particular to *this* machine,
   harness, or set of accounts. A general engineering principle is not a candidate no
   matter how many skills repeat it.
2. **Substrate does not already do it** — if the current model handles it natively, a
   written rule does not add behaviour; it freezes an older default and competes with
   the newer one.
3. **Not a procedure** — steps and workflows belong in a skill. Residency is for facts
   and wiring, which have to be true before any particular task starts.
4. **Actionable behavior change** — expressible as "do X" / "don't do Y", not "X is important"
5. **Clear violation risk** — what goes wrong if ignored, in one sentence
6. **Not already in rules** — check the full rules text, including the same idea in different words

> Tests 1–3 are `rules/README.md`'s admission criterion ("facts, wiring, and traps specific to this environment.
> Procedures for thinking and work belong to skills, checks that need a firing time belong to hooks, and general judgment belongs to the substrate"),
> established by
> [ADR-0018](https://github.com/shimo4228/claude-harness/blob/main/docs/adr/0018-rules-rightsize-for-claude5.md) and
> [ADR-0035](https://github.com/shimo4228/claude-harness/blob/main/docs/adr/0035-commit-review-hook-and-rules-rightsize.md).
>
> **Recurrence is evidence, not a gate** — report the count, do not filter on it.
> Frequency and residency-worthiness diverge often enough to matter: a general principle
> repeated in ten skills fails tests 1–3 (substrate has it — ADR-0018 cut residency 60%
> removing exactly that class), while a one-off environment trap passes them.

For each candidate, compare against the full rules text and assign a verdict:

| Verdict | Meaning | Present to user |
|---------|---------|-----------------|
| **Append** | Add to an existing section of an existing rule file | Target + draft |
| **Revise** | Existing rule content is inaccurate/insufficient | Target + reason + before/after |
| **New Section** | Add a new section to an existing rule file | Target + draft |
| **New File** | Create a new rule file | Filename + full draft |
| **Already Covered** | Sufficiently covered (even if worded differently) | Reason (1 line) |
| **Too Specific** | Should stay at the skill level | Link to the relevant skill |

Exclude: principles already in rules, language/framework-specific knowledge (belongs
in language-specific rules or skills), and code examples / commands (belong in skills).

### Verdict quality

Each verdict must be self-contained — target, evidence, and rationale on its own.
Draft text links back to the detailed How with the pointer form the rules corpus uses:
``skill: `name` ``.

```
# Bad
Append to security.md: Add LLM security principle
```

Good example (the evidence is why it passes tests 1–3, not an occurrence count. Cite references **by section heading** —
line numbers shift every time the referenced file grows):

```
# Good
New Section in rules/common/debugging.md:
"If rate limits fire repeatedly during bulk writes to an external platform, treat them as a
policy signal, not a transient error, and stop the burst. Do not push through with backoff; report to a human."

Test 1 (environment-specific): an event that actually happened on this author's account. On 2026-07-16,
  continuing with backoff resulted in an indefinite account block + deletion of all created content. Not general
  HTTP 429 etiquette, but a stop condition specific to this operation
Test 2 (not substrate-native): the substrate's default retries 429 as transient.
  The rule is needed to override that default
Test 3 (not a procedure): not a procedure but a declaration of fact: "repeated rate limits = policy signal"
Violation risk: pushing through loses the whole account (proven, unrecoverable)
Recurrence: 1 skill (evidence, not a gate)
```

Note that it **passes even with a Recurrence of 1**.

## Phase 3 — User Review & Execution

Present a summary table (`# | Principle | Verdict | Target | Confidence`) as the
overview, then **confirm one by one**: walk the
candidates sequentially — for each, show its evidence, violation risk, and draft text,
then ask `[y/n/skip]`. The user can modify the draft before approving, and can stop at
any point. Never batch the approval ("apply all 5? [y/n]" defeats the design — one
candidate, one decision); skipped candidates go to the ledger with `status: skipped`.

**Never modify rules automatically. Always require user approval.** This is the one
hard gate — rules load every session, so a bad rule has outsized blast radius.

> Paths below start at `${CLAUDE_SKILL_DIR}`, the directory holding this SKILL.md; an agent that does not substitute the variable reads it as that directory.

Then update the ledger `${CLAUDE_SKILL_DIR}/results.json` inline (Read → merge → Write):

```json
{
  "distilled_at": "2026-03-18T10:30:42Z",
  "candidates": {
    "llm-output-trust-boundary": {
      "principle": "Treat LLM output as untrusted when stored or re-injected",
      "verdict": "Append",
      "target": "rules/common/security.md",
      "evidence": ["llm-memory-trust-boundary", "llm-social-agent-anti-pattern"],
      "status": "applied"
    }
  }
}
```

`distilled_at` is real UTC (`date -u +%Y-%m-%dT%H:%M:%SZ`); candidate IDs are
kebab-case derived from the principle.

## Related

- `skill-stocktake` — audits skill *quality*; rules-distill promotes recurring *principles* to rules. Run stocktake first, then distill what survives.
- `rules-stocktake` — audits the rules this skill produces (residency cost, staleness, absorption) and demotes back what stopped earning its always-loaded slot; the inverse direction over the same boundary.
- `learn-eval` — extracts per-session patterns into skills/memory; rules-distill later promotes the cross-cutting ones to rules.
