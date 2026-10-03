---
name: thermo-nuclear-code-quality-review
description: Mandatory post-change coherence check with two distinct passes on the final candidate. Use proactively after source-code edits and before claiming a task is done, pushing, or opening a PR. Pass A audits ownership and boundaries; pass B attacks the design with counterfactual simplification and hidden-coupling questions.
---

# Thermo-Nuclear Code Quality Review

Review the exact candidate being shipped, not a remembered diff. Be demanding
about correctness and maintainability without turning a minor patch into an
unrelated architecture program.

## Applicability

Run this skill when source code changed and the task is approaching completion,
push, or PR. Skip pure documentation, comment, issue-text, and mechanical rename
changes with no executable effect; state the skip.

Resolve the task's real base from the active request or PR. Do not default to
`main`. Record the base SHA, HEAD SHA, dirty state, changed files, and candidate
fingerprint. Read the full changed files and the narrow owning context needed to
judge them.

This skill requires two named passes on the final diff. The passes must ask
different questions; repeating the same rubric twice is correlated ceremony.

## Pass A — Ownership and boundary coherence

Ask whether the change is correct in the architecture that exists:

- Does the implementation satisfy the user contract without changing another
  contract field?
- Is the logic in the layer that owns the state, money, authorization, unit, or
  lifecycle rule?
- Do types, serialization, database/API boundaries, error behavior, and state
  transitions preserve the real invariant?
- Does the canonical impact graph cover the changed roots and applicable
  consumers?
- Does the patch reuse an existing canonical helper when semantics truly match?
- Did it add a fallback, cast, optional branch, or dual rail that hides an
  unresolved contract?
- Do focused tests exercise the behavioral boundary rather than only a copied
  expression or helper?

Fix blocking findings in one coherent batch. Then refreeze the candidate and
run Pass A again if the edit invalidated it. When Pass A is clean on the current
fingerprint, emit this exact completion token on its own line:

```text
<thermo-review-complete>
```

## Pass B — Counterfactual simplification and hidden coupling

Keep the candidate fingerprint fixed. Now assume the implementation works and
try to find a materially simpler or safer shape:

- What concepts, branches, wrappers, modes, or duplicated calculations did the
  patch introduce?
- Can one existing ownership boundary absorb the behavior directly?
- Would deleting an abstraction or special case make the invariant more
  explicit?
- Did the change couple surfaces that have different owners, units, lifecycle,
  authority, or change cadence?
- Did it duplicate a rule that should change atomically, or centralize rules
  that should remain separate?
- Does a large file or function now conceal a separable responsibility?
- Is there a smaller counterexample that shows the chosen abstraction is wrong?

A line-count threshold is a smell, not an oracle. Decompose only when the new
boundary removes concepts or coupling and remains inside the authorized task.
Do not create helpers, modules, policy objects, state machines, or generic
dispatchers merely because they sound cleaner.

When Pass B is clean on the same current fingerprint, emit the completion token
again:

```text
<thermo-review-complete>
```

## Scope and ambition

Use this precedence order:

1. user contract and authority;
2. canonical state, money, unit, time, and permission semantics;
3. material evidence gaps;
4. smallest correct behavioral change;
5. simplification that deletes meaningful complexity without expanding blast
   radius;
6. follow-up refactors;
7. style.

Be ambitious in thought and bounded in mutation. If a better architecture
requires changing unrelated owners, public contracts, or many untouched files,
record it as follow-up unless the current implementation would otherwise be
unsafe or fundamentally wrong.

## Findings bar

Prioritize:

1. correctness or contract violations;
2. ownership and boundary leaks;
3. hidden state, unit, authorization, or lifecycle coupling;
4. complexity that the candidate introduced and can delete safely;
5. branch-local slop that obscures the invariant.

Do not flood the review with preferences. A blocking finding must name the
candidate location, violated contract, reachable harm, and smallest acceptable
remedy. A simplification finding must name the measurable concept, branch,
wrapper, dependency, or coupling it deletes.

## Invalidation and convergence

Any source-code edit after a thermo credit changes the fingerprint and resets
the two pass credits. Batch accepted edits before rerunning. Do not restart
unrelated discovery or runtime checks unless their stated assumptions changed.

If two passes keep producing the same concern without new evidence, do not add
another pass. Create an executable counterexample, inspect a new authoritative
boundary, narrow the claim to `partial`, or ask for the authority needed to
expand scope.

## Compact result

```markdown
## Thermo
**Candidate:** <base/head/fingerprint>
**Pass A — ownership/boundaries:** clean | <blocking finding>
**Pass B — counterfactual simplification:** clean | <blocking finding>
**Accepted changes:** <only decision-relevant items>
**Follow-up, outside contract:** <none or bounded item>
**Coverage:** verified | partial — <gap>
```
