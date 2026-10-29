---
name: quality-control
description: Design-smell review of a diff — matches the changes since a fixed point (commit, branch, tag, or merge-base) against a fixed baseline of Fowler code smells (Refactoring, ch.3) and reports judgement-call findings. Complements /code-review (bugs, documented standards) and /validate_plan (spec conformance); use for the design-quality lens neither covers, or when the user asks for a "smell review".
---

Review the diff between `HEAD` and a fixed point against the smell baseline below. This skill covers design smells only — bug hunting and documented-standards compliance belong to `/code-review`; spec conformance belongs to `/validate_plan`.

## Process

### 1. Pin the fixed point

Whatever the user (or calling command) supplies — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If unspecified, ask.

Capture: `git diff <fixed-point>...HEAD` (three-dot, merge-base comparison) and `git log <fixed-point>..HEAD --oneline`. Confirm the ref resolves (`git rev-parse`) and the diff is non-empty before spawning the sub-agent.

### 2. The smell baseline

A fixed set of Fowler code smells (_Refactoring_, ch.3). Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the work doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 3. Spawn the review sub-agent

One `general-purpose` Agent call. Include in the prompt:

- The diff command and commit list.
- The smell baseline from step 2 pasted in full — the sub-agent has no other access to it.
- The brief: "Report any baseline smell you spot in the diff — per file/hunk where relevant: name the smell and quote the hunk. Every finding is a judgement call; a documented repo standard overrides the baseline. Skip anything tooling enforces, and skip bug/spec findings — other reviews own those. Under 400 words."

### 4. Report

Present the sub-agent's findings under `## Design smells (judgement calls)`, verbatim or lightly cleaned. End with a one-line count and the worst finding (if any).
