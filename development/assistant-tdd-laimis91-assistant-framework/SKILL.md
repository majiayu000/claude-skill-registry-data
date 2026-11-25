---
name: assistant-tdd
description: "Use for tests-first TDD requests, project TDD rules, or workflow-selected TDD checks."
---

# Test-Driven Development

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Use TDD only when requested, required by project policy, or activated for selected
checks by the carried verification decision. Scope, technique, and TDD are
independent; inactive TDD never needs a fabricated RED.

## Cycle

1. **RED.** The writer adds or extends a meaningful behavior assertion. Run it
   and observe the intended missing-behavior failure before production edits.
   Syntax, imports, environment, and flaky failures do not authorize production.
   If it passes, inspect existing behavior and the oracle; do not remove working
   code or invent failure evidence. When TDD is active and a test is being
   authored or corrected, load [test craft](references/test-craft.md) for worked
   examples of tests whose RED fails for the intended reason.
2. **GREEN.** Make the smallest production change that passes. Verify the target,
   selected relevant regressions, and applicable binding checks. Repair failures
   before moving on; do not infer an unselected full suite. Classify failures
   against accepted behavior before repair; incidental assertions do not justify
   production changes. Keep carried reduced-testing scope and one shared semantic progress
   guard across tests, checks, workers and sessions.
3. **REFACTOR.** After current GREEN, improve names or remove duplication only
   when useful; `none needed` is valid. Record actual changes. After edits, run affected checks. No edits after
   GREEN and nothing changed since means no rerun: record v3 `reuse_green`
   with `green.reuse_digest` (`contracts/output.yaml` recipe) from that passing
   GREEN run. Reuse creates zero new invocation, result or test count.
   Failed GREEN, an unknown digest, or a changed one reruns. Only persisted
   packets opting into `reuse_identity_mode: detailed` add the seven-category
   identity. Historical v2 cycle entries stay readable, without `invocation_ref` or reuse.

Keep actual test identity, commands/argv, cwd, observed outcomes, and why RED
failed for the right reason. Partial cycles remain partial; an exception needs
its recorded approval/reason and cannot be called TDD completion. Reused checks
need no fabricated test edits.

## Workflow ownership

For workflow/producer boundaries, load `contracts/index.yaml`: `entry`, active
`current_phase`, and `completion` preserve the existing canonical cycle log and
gates. Missing/invalid selectors load the full named file. Workflow owns dispatch.
Load workflow's `references/build-worker-protocol.md` only when that execution
path is selected.

- `bounded_executor`: one owner authors tests, observes RED, implements, and
  verifies GREEN and REFACTOR.
- `separated_workers`: the SAME selected writer authors tests (`test_authoring`),
  implements after current RED (`production`), and refactors after current GREEN
  (`refactor`). Builder/Tester executes checks only. Test-authoring DONE is
  stage-only and cannot complete Build or permit Review.

Preserve the unchanged decision, task-wide `tdd_mode`, and selected IDs. Workflow
activation is their intersection with `tdd_choice.applicable_check_ids`; split
active packets until exactly one ID intersects. Authorizing RED must match that
CheckSpec's exact ID, test file/name, argv/cwd, and meaningful-failure oracle.
Changed authorizing inputs require fresh RED without erasing history. Standalone
TDD without a decision invents no CheckSpec ID.

For a carried Architecture Decision Pack, test its semantic conversions,
validation, compatibility, design-pressure behavior, and stated quality scenarios.
Do not invent a Pack, benchmark, or quality claim. Unknown-cause bugs go through
assistant-debugging before selecting the regression oracle.

## Result and stop rules

Return the cycle evidence, changed test/production files, relevant verification,
exceptions, and blockers; preserve the canonical log for actual consumers.
Missing or invalid required RED blocks production (`NEEDS_CONTEXT` for delegated
writers). Wrong-reason RED requires a test/environment repair; failed GREEN or
REFACTOR blocks the next behavior. Ask only about unresolved material behavior
or oracle choices, with no numeric question quota.
