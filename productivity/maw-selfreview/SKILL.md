---
name: maw-selfreview
description: |
  One-stage adversarial review of your own uncommitted diff, run by a different vendor than the one that wrote it. Use before committing work you produced in an ordinary session — no task folder, no pipeline, no branch handling.
  Costs one spawn and about a minute, against nine stages for the full pipeline. Reviews the diff only; it never edits code.
  Normally fires automatically from the pre-commit gate rather than being called by hand — the moment you would think to ask for it is the moment you are least likely to.
---

# Self-review — the judge must not be the author

In an ordinary session you are both the author and the only reviewer of what you wrote. That is not a review, it is a re-reading, and it fails in a specific direction: you skip exactly the places you feel sure about, and you feel sure precisely where you cannot see the defect.

This skill spends one spawn to break that. A reviewer on a **different vendor** receives the diff and the task it was meant to accomplish, reads the repository itself, and reports. It cannot edit anything.

Different vendor is not decoration. Measured on this project: a codex reviewer caught that a DSN test dropped production tables; a claude fixer working on that same finding caught a second leak path codex had missed; elsewhere codex found five tools leaking a key while claude caught that codex's own Helm recommendation would break minikube and its `2001::/16` rule would kill half of IPv6 egress including Google. Same-vendor review shares blind spots with the author by construction.

## When it runs

**Automatically, from the pre-commit gate** (`hooks/maw-selfreview-gate.sh`), when the staged diff either exceeds the size threshold or touches a path listed as invariant-bearing. A review you have to remember to request is a review that will not happen at the moment it matters.

**Bypass exists and must stay cheap.** A gate that cannot be skipped gets disabled wholesale; the practical failure mode reported across the industry is `--no-verify` becoming permanent muscle memory the first time a hook is slow or wrong. So: the bypass is one flag, it is logged, and it is never silent. Speed is part of the contract — if this takes longer than about a minute, it will be routed around, and then it protects nothing.

**Manually** with `/maw-selfreview` when you want it outside those triggers.

## What the reviewer gets

- the staged diff, and **only** that plus one hop of directly touched dependencies — the scope constraint is what stops the review radius from growing into the rest of the codebase
- the task or intent the change was supposed to serve
- read access to the repository, so claims can be checked against the real thing
- no write access anywhere

## What the reviewer must produce

Every finding carries a severity, and severity decides what happens next:

| severity | meaning | effect |
|---|---|---|
| `BLOCKER` | the change is wrong or unsafe as written | commit is blocked |
| `MAJOR` | a real defect, not hypothetical | commit is blocked |
| `MINOR` | worth knowing, does not have to be fixed now | reported, does **not** block |
| `TRACKED` | real but out of this diff's scope | reported, does **not** block |

**Convergence is defined by the absence of BLOCKER and MAJOR, not by an empty report.** A review that must reach zero findings never terminates: an adversarial reviewer always finds something, and on the fifth pass it will be inventing. Minor items and polish may remain outstanding forever, and that is the correct end state, not a failure.

Every `BLOCKER` and `MAJOR` needs **material evidence** — a `file:line`, the output of a command actually run, a concrete counter-case. "This looks risky", "this may not handle edge cases", "consider whether" are not findings. If the reviewer cannot say what breaks and under what input, it is at most `MINOR`.

The honest empty verdict is `NO_BLOCKING_FINDINGS`, and it is the expected outcome for most diffs. Say it plainly. Manufacturing a blocker to justify the spawn is the failure this contract exists to prevent — and it is measurable: on this project's own benchmark, an adversarial checker degraded 13% of already-correct answers by objecting to them.

## What it does not see

Anything visual, anything about feel, anything that only appears at runtime. It reads a diff. If the change is about how something looks or behaves under load, this review is not evidence about that, and it should say so rather than inventing a textual proxy.

## Cost

One spawn, roughly a minute. That is the entire point: the full pipeline is nine stages and hours, and it is not proportionate to a commit. On small, well-understood changes even this may be more than needed — the gate's thresholds exist so it does not fire on every three-line edit.
