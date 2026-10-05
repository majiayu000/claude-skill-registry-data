---
name: bug-echo
description: After a bug is fixed, characterize it as a code pattern and hunt the rest of the codebase for structural twins, ranked by confidence. Reports only — never fixes. Trigger on:- bug-echo, find the same bug elsewhere, where else does this happen, siblings of this bug, pattern-hunt after fix.
allowed-tools: Read, Grep, Glob, Bash
---

# Bug Echo

The bug you just fixed is rarely the only one of its kind. Ordinary review checks whether
code is wrong on its own terms — it has no reason to connect one file's defect to the
same mistake three files away. This skill does exactly that connection, and nothing else.

Off the linear pipeline (`.specify/memory/constitution.md`) — a reflex to run right after
a fix lands. It never edits; to fix what it finds, hand the list to `/resolve-review` or
just work it directly.

## When to use this

- Right after fixing a bug that could plausibly be a *class* — a missing guard, a wrong
  argument form, an absent platform affordance, a copy-paste that drifted.
- Skip for a genuinely one-off bug (a typo, a wrong constant used in exactly one place).
- Not a general audit — for that use `/code-review` or `/improve`.

## Procedure

1. **Characterize the fixed bug as a pattern.** Write one sentence naming the wrong
   *shape*, not the symptom: "a modal opened without a dismiss control", "a helper called
   with a positional arg that later became keyword-only", "a derived table read as
   evidence without a uniform-result check". If you can't state the shape, there's no
   pattern to echo — stop.

2. **Derive search terms for the shape.** The anti-pattern's tokens, the call that should
   be present but isn't, the construct that's misused. Plan several `Grep` queries — the
   bare name, the qualified form, the surrounding idiom — not one.

3. **Sweep the codebase in one parallel batch.** `Grep`/`Glob` for structurally similar
   sites. Cast wider than you think you need; step 4 is the filter.

4. **Read every hit.** A match is only a sibling if the *same defect* is actually present
   — local context (a guard one frame up, a different code path, a caller that can't hit
   it) often saves a look-alike. Grep counts are not findings.

5. **Rank what survives.** Per site: `file:line`, one line on why it's the same bug, and
   a tag:
   - `confirmed` — the defect is present, same mechanism, same consequence.
   - `likely` — same shape, couldn't fully rule the path in or out from reading.
   - `needs-eyes` — structurally similar, genuine doubt, worth a human glance.
   Note blast radius (user-facing? data? a hot path?) where it changes priority.

6. **Present the ranked list and stop.** Lead with the `confirmed` sites. If the sweep
   found nothing, say so plainly and say what you searched for — don't manufacture hits.

## Constraints

- Report only. No edits, no new tasks, no review artifact.
- One pattern per run. If fixing the bug revealed a second unrelated class, note it and
  run again — don't blur two sweeps.
- Don't downgrade "I couldn't tell" to `confirmed` to look decisive, or up to
  `needs-eyes` to look thorough.
- "No siblings" is a valid, useful result — state the searches that produced it.

## Done criteria

- The fixed bug is stated as a one-sentence pattern.
- Every structural match was read, not just counted.
- Output is a confidence-ranked `file:line` list (or a stated-empty result with the
  searches shown).
