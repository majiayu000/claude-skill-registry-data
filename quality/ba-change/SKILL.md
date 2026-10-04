---
name: ba-change
description: Use when approved project truth may need to change, a business rule has changed, the user is refining a pending change, or an existing change needs to be resumed.
argument-hint: "[สิ่งที่ต้องการเปลี่ยน หรือ change ที่ต้องการทำต่อ]"
disable-model-invocation: true
---

# BA Change

Use this as the **Single Front Door** for evolving approved BA truth. BA Discovery is **Single User Only**: clarification, impact confirmation, and final confirmation stay with the same interactive user.

Before reasoning or writing, read:

- `${CLAUDE_PLUGIN_ROOT}/shared/contract-core.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/contract-records.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/contract-changes.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/question-contract.md`
- [references/change-workflow.md](references/change-workflow.md)

## Start / resume

When new intent must be compared against existing OPEN changes, run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ba_context.py" \
  --project "${CLAUDE_PROJECT_DIR}" \
  --identity-review
```

When a focused `CHG-*` is already known:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ba_context.py" \
  --project "${CLAUDE_PROJECT_DIR}" \
  --focus-change CHG-0001
```

**Read before relating.** Compare new intent against the actual OPEN change content before creating another `CHG-*`.

## Working contract

1. Stage proposed meaning in `.ba/changes/`; do not mutate canonical truth.
2. Re-read relevant current truth and use **Focused Evidence Traversal**: follow causal evidence, not keywords or memory.
3. Explain the Impact Frontier in language the single user can evaluate.
4. Obtain impact confirmation before revalidation.
5. Show a short **Minimum Revalidation** plan and revisit only `NEEDS_UPDATE` / `NEEDS_RECONFIRMATION` knowledge.
6. Preserve still-valid confirmed understanding and revalidate only new delta.
7. Show the **Final Before → After** and obtain FINAL confirmation.
8. Build prospective canonical files under `.ba/changes/.candidate/<CHG-ID>/`, outside current canonical state.
9. Validate with `${CLAUDE_PLUGIN_ROOT}/scripts/ba_lint.py`, then use `${CLAUDE_PLUGIN_ROOT}/scripts/ba_change_commit.py` for prospective validation and apply/readback.
10. Do not claim `APPLIED` until post-commit readback and lint succeed.

If Python is unavailable, state that **deterministic validation/commit tooling was not run**. Conversational analysis may continue, but do not claim structural integrity or verified `APPLIED` state without command evidence.

Never require the user to switch to another BA phase command. Phase semantics may guide internal reasoning, but `/ba-change` remains the user's front door.
