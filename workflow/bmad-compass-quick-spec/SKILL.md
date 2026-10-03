---
name: bmad-compass-quick-spec
description: 'Create implementation-ready quick tech specs for small changes or features. Use when the user says "quick spec"'
---

## Spec status lifecycle

Specs produced by this skill flow through a shared lifecycle consumed by `bmad-quick-dev`:

`draft → ready-for-dev → in-progress → in-review → done`

- **draft** — initialized by `steps/step-01-understand.md` when the spec file is first created; retained while `step-03-generate.md` assembles the plan.
- **ready-for-dev** — set by `steps/step-04-review.md` after the user approves the final spec.
- **in-progress** — flipped by `bmad-quick-dev` when implementation begins.
- **in-review** — held by `bmad-quick-dev` while the adversarial-review loop runs.
- **done** — written by `bmad-quick-dev`'s `step-07-spec-trace.md` (standard pipeline) OR `step-oneshot.md` (one-shot route). **Never** touched by `bmad-quick-dev/step-06-resolve-findings.md` — that step's single responsibility is resolving findings, not frontmatter write-back.

See `docs/development/bmad/quick-spec-quick-dev.md` § "Spec File Naming and Lifecycle" for the full contract and the slug-derivation rules that produce spec filenames.

Follow the instructions in ./workflow.md.
