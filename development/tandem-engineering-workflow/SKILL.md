---
name: tandem-engineering-workflow
description: "Engineering discipline for development work orchestrated through Tandem, regardless of whether the worker is Claude, Codex, or another supported engine. Trigger for implementation, debugging, review, test, or architecture work. Begin the first response with 📋📋📋📋📋 when active."
---

# Tandem engineering workflow

📋📋📋📋📋 The engineering workflow is active.

This skill defines how an MCP-capable director should plan, delegate, verify, and report engineering work performed through Tandem. It is engine-neutral. Engine-specific features, such as Claude model controls or the Claude-only relay, are optional special cases.

## Roles

- Human: sets the goal, grants authority, makes consequential product decisions.
- Director: clarifies the outcome, selects devices and engines, assigns bounded work, and owns the final answer.
- Worker session: implements or investigates one defined part of the goal.
- Reviewer session: independently checks the result when the risk or scope warrants it.

One session may hold several roles on a small task. Keep ownership explicit on larger work.

## Workflow

### Understand

1. Restate the concrete outcome and definition of done.
2. Inspect the repository, current branch, local instructions, and existing changes before editing.
3. Identify what is unknown and research only what affects the decision.
4. Push back on unsafe, contradictory, or needlessly broad requests with concrete reasons.

### Plan

5. Break work into phases with clear file ownership and tests.
6. Decide which assignments are independent and which depend on earlier output.
7. Select a device and engine based on advertised capability and data locality. Do not route by guesswork.
8. Use a planning mode when the chosen engine provides one and the work is non-trivial. Otherwise ask the worker for a written plan before implementation.
9. Review the plan before authorizing broad writes. Correct scope drift before code is changed.

### Build

10. Give each worker a bounded assignment, the relevant context, and a measurable completion condition.
11. Preserve user changes and avoid unrelated refactors.
12. Keep security controls explicit: narrow cwd allowlists, opt-in engines, no secret output, and no permission bypass unless authorized.
13. Poll a running turn instead of resending its prompt.
14. Read the worker's actual result. A completion claim is not verification.

### Verify

15. Inspect the diff or resulting artifact directly.
16. Run focused tests first, then the full relevant suite.
17. Check failure paths, boundaries, cleanup, and compatibility, not only the happy path.
18. Use an independent reviewer for high-risk changes involving authentication, remote execution, networking, secrets, or destructive operations.
19. Fix findings and repeat verification until no required work remains.

### Report

20. Lead with the outcome.
21. State what changed, what was verified, and what remains limited.
22. Do not claim deployment, merge, commit, publication, or external delivery unless it actually happened.
23. Do not expose tokens, personal device identity, private URLs, paths, or raw session output in the report.

## Multi-device rules

- Call `list_devices` before choosing a remote target.
- Preserve global names such as `studio:review` exactly.
- A disconnected device is a recoverable operational state, not evidence that its work failed or succeeded.
- Re-run selection only for new sessions. Existing global names remain pinned.
- Integrate cross-device work in one explicitly owned place.

## Quality gate

The work is ready only when:

- the requested behavior exists;
- tests pass in proportion to risk;
- security and privacy boundaries still hold;
- documentation matches actual behavior;
- the diff contains no unexplained unrelated changes;
- the director can explain remaining limitations without relying on a worker's unsupported claim.
