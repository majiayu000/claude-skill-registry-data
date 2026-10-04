---
name: remy-gate
description: Remy Inclusion Gate. Auto-fires during feature builds. Ensures every feature has Remy write parity, approval tiers, and real-time UI sync.
---

# Remy Inclusion Gate

**Auto-fires during:** `/builder`, `/feature-closeout`, any feature implementation.
**Purpose:** No feature ships without Remy integration planned.

## The Check (8 Questions)

For every feature being built, answer:

1. **Can Remy perform this action conversationally?**
   - If yes: verify the command exists in `command-orchestrator.ts`
   - If no: what write command is needed? Document it.

2. **What write command is needed?**
   - Check if a server action already exists in `lib/*/actions.ts`
   - If it does: create a Remy wrapper in `lib/ai/remy-write-commands.ts`
   - If not: the server action needs to be built first

3. **What approval tier?**
   - Tier 1 (auto): drafts, notes, memories, reversible changes
   - Tier 2 (confirm): client updates, menu changes, task creation
   - Tier 3 (explicit): emails, payments, state transitions, financial mutations

4. **What context does Remy need?**
   - Check `remy-context.ts` - is the data Remy needs already loaded?
   - If not: add it to the context loader

5. **What defaults reduce repeated questions?**
   - Can this action use chef defaults instead of asking every time?
   - If a pattern repeats 3+ times, it should become a default

6. **Does the UI update in real time when Remy acts?**
   - Write commands must call `broadcast()` after mutation
   - Verify `useSSE()` hook exists on the relevant page

7. **Can the user undo what Remy did?**
   - Reversible actions: log in `remy_action_log` (when built)
   - Irreversible actions: must be Tier 3

8. **Does this work without AI?**
   - Every feature must have a manual path
   - AI accelerates, never gates

## Output Format

After running the check, append to the build's verification:

```
## Remy Gate
- [ ] Remy command: `{command_name}` (exists / needs building)
- [ ] Approval tier: {1|2|3}
- [ ] Context loaded: {yes / needs addition to remy-context.ts}
- [ ] Real-time UI: {broadcast wired / needs wiring}
- [ ] Manual path: {works without AI}
- [ ] Notes: {any gaps or future work}
```

## When to Skip

- Pure styling/CSS changes
- Documentation-only changes
- Build tooling / dev infrastructure
- Test files

## Reference Files

- Write commands: `lib/ai/remy-write-commands.ts`
- Command orchestrator: `lib/ai/command-orchestrator.ts`
- Command types: `lib/ai/command-types.ts`
- Context loader: `lib/ai/remy-context.ts`
- Classifier: `lib/ai/remy-classifier.ts`
- Vision doc: `docs/specs/remy-operating-layer-vision.md`
