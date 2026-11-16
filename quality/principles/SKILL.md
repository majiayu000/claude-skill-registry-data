---
name: principles
description: "Engineering principles index; read the leaf file before citing a principle."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "cursor/plugins pstack 0.15.25 skills/principle-* (all 24, copied to references/ with frontmatter stripped and links rewritten)"
---

# Principles

Each row is one engineering principle. The gist is a pointer, not the principle: the leaf file holds the rule, its limits and its tells.

Cite a principle only if you read its file this session. A citation from the gist alone borrows the name without the content, and the leaf's caveats ("skip it when…", "distinct from…") are usually what decides the case.

## Use

1. Match the situation to a row by its gist. Done when: you have one to three candidate rows, or none fits.
2. Read each candidate's file in `references/`. Done when: every principle you will cite has been read this session.
3. Apply it, and when you cite it, name the file and the line that decided the call, e.g. "per `references/fix-root-causes.md`: a guard is a fix only when the state it handles is legitimate".

## Index

| Principle | Gist | File |
|---|---|---|
| Attack the premise | Two fixes on one premise failed the same gate: test the premise before a third fix | `references/attack-the-premise.md` |
| Boundary discipline | Validate at system edges (CLI, config, network, APIs); trust internal types; keep logic pure | `references/boundary-discipline.md` |
| Build the lever | Non-trivial work gets a codemod, script or generator a reviewer can rerun | `references/build-the-lever.md` |
| Encode lessons in structure | A repeated instruction or correction becomes a lint, flag, check or script | `references/encode-lessons-in-structure.md` |
| Exhaust the design space | No precedent for a UI or architecture call: prototype two or three, compare side by side | `references/exhaust-the-design-space.md` |
| Experience first | Choose user delight over implementation convenience; fewer polished features | `references/experience-first.md` |
| Explain the number | Before trusting a measured number, find what limits it and what else it might measure | `references/explain-the-number.md` |
| Fix root causes | Trace the symptom to where the system first went wrong and fix it there | `references/fix-root-causes.md` |
| Foundational thinking | Get core types and data structures right before logic | `references/foundational-thinking.md` |
| Guard the context window | Route bulk output to subagents; keep summaries in the main thread | `references/guard-the-context-window.md` |
| Laziness protocol | Bias toward deletion and the smallest change that solves it | `references/laziness-protocol.md` |
| Make operations idempotent | Steps converge to the same end state after crashes, restarts and retries | `references/make-operations-idempotent.md` |
| Migrate callers, then delete legacy APIs | Move every caller and delete the old API in one wave; no compat layer | `references/migrate-callers-then-delete-legacy-apis.md` |
| Minimize reader load | Count layers to trace and state to hold; collapse one-caller wrappers | `references/minimize-reader-load.md` |
| Model the domain | Encode the domain in a data structure instead of scattered conditionals | `references/model-the-domain.md` |
| Never block on the human | Reversible work: decide and keep going instead of asking | `references/never-block-on-the-human.md` |
| Outcome-oriented execution | In phased rewrites, converge on the target; no throwaway intermediate compat | `references/outcome-oriented-execution.md` |
| Prove it works | Verify against the real artifact, not a proxy or a self-report | `references/prove-it-works.md` |
| Redesign from first principles | A new requirement reshapes the design instead of being bolted on | `references/redesign-from-first-principles.md` |
| Separate before serializing shared state | Concurrent writers: remove the sharing first, lock only for a real invariant | `references/separate-before-serializing-shared-state.md` |
| Sequence verifiable units | Small units that each end verified, checked before the next | `references/sequence-verifiable-units.md` |
| Subtract before you add | Remove dead code and redundant layers first, then build on the simpler base | `references/subtract-before-you-add.md` |
| Test behavior, not implementation | Assert what users observe; tests survive internal refactors | `references/test-behavior-not-implementation.md` |
| Type-system discipline | Illegal states unrepresentable, branded primitives, parse at boundaries, exhaust variants | `references/type-system-discipline.md` |
