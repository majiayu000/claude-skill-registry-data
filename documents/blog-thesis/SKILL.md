---
name: blog-thesis
description: Use when research on a post is finished and before any outlining or drafting begins. Trigger on "research is done", "ready to write", "let's draft this", or any attempt to invoke blog-outline or blog-write on a post whose working doc has no approved Thesis section.
---

# Settle the thesis

**This is the human gate.** It is the one mandatory checkpoint in the pipeline, matching the
Plan gate in `AGENTS.md` — the profile's only required approval.

Its job is to force one question that is otherwise deferred until it is too late:
**has the claim changed since the hypothesis?**

## Prerequisite

The working doc `docs/research/<slug>.md` must contain a `## Hypothesis` section and a
`## Findings` section. If either is missing, stop and run `blog-hypothesis` or
`blog-research` first. Do not reconstruct a hypothesis from the findings — a hypothesis
written after the evidence always matches it.

## The failure this prevents

Theses drift silently during research, and the drift is invisible because every individual
step feels small. Left unchecked, the draft argues the original hypothesis while the
evidence supports something else — and the piece reads as under-argued for reasons the
author cannot locate.

On this site's SDD post the claim moved from _"SDD extends earlier and later than
development"_ to _"specs written from the middle are unanchored, and the executable property
was lost"_ — a materially larger claim, arrived at across three findings, noticed only
because someone asked.

## Write to the working doc

Append a `## Thesis` section containing all five parts:

```markdown
## Thesis

**Sentence.** The argument in one sentence. If it needs two, it is not settled.

**Delta from hypothesis.** State explicitly: unchanged, narrowed, widened, or replaced —
and what moved it. Never omit this line, even when nothing changed.

**Strongest unanswered objection.** The best case against, and whether the piece answers it
or concedes it. "None" is almost never true.

**Demoted.** Findings that no longer carry weight, and why. Keeping a finding that stopped
supporting the thesis is how a piece becomes a list.

**Publish gates.** Which ⚠ sourcing items must be closed before publication versus which
may ship flagged.
```

## Then stop

**Present the thesis and wait for approval.** Do not continue to `blog-outline` or
`blog-write` in the same turn. This gate is human-owned; an unapproved thesis is not a
thesis, and everything downstream inherits it.

Tick `- [x] Thesis` in the stage block only after the human approves.

## Do not

- **Do not skip the delta line when the thesis seems unchanged.** That is exactly when drift
  hides — it is easier to notice a claim that transformed than one that quietly widened.
- **Do not write the thesis sentence to match the hypothesis.** The hypothesis was a guess
  made before evidence. Fidelity to it is not a virtue.
- **Do not record "no unanswered objection."** If none surfaced during research, the
  research was too narrow, or the rival position has not been sought. Go find it.
- **Do not proceed on your own approval.** Presenting the thesis and continuing anyway
  converts the only gate in the pipeline into a formality.

## Next step

Approved? → `blog-outline`.
Thesis moved enough to need more evidence? → back to `blog-research`.
