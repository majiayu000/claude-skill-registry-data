---
name: docs-review
description: Audit or improve general repository documentation against implemented behavior. Use for deliberate README or documentation-quality work not owned by a more specific documentation skill.
---

# Documentation Review

Own general repository-document quality in an explicit audit-only or authorized edit mode.

## Workflow

1. Confirm audience, document set, desired outcome, and whether the task authorizes edits.
2. Route current-change drift to `docs-drift-review`, `docs/context/` structure to `repo-context-document`, semantic contracts to `spec-update`, journeys to `critical-journey-document`, and persuasive claims to `marketing-claims-review`.
3. Verify content against implementation, commands, configuration, examples, tests, metadata, and canonical documents. Run documented commands and examples when they are read-only or can run in a scratch directory, because an example that does not run is the defect readers hit first. Read the code for the rest, and say which claims you ran and which you only read.
4. Classify evidence-backed findings as `keep`, `update`, `merge`, `split`, `move`, `archive`, or `remove`.
5. In audit-only mode, return prioritized findings without edits.
6. In edit mode, change only the confirmed document set and preserve repository structure and voice unless that structure is the requested defect.
7. Use `text-improve` on changed prose without changing verified facts, required terminology, or intentional voice.
8. Require explicit authority before archiving, removing, or materially expanding the document set.

Do not invent features, commands, architecture, benchmarks, screenshots, promises, or roadmap items; impose a generic template; or broaden a focused request.

Finish with an evidence-backed audit or verified scoped edits, plus unresolved facts that need an owner.
