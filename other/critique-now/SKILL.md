---
name: critique-now
description: "Manually run contract-critic against an already-approved (or skipped) contract. Use when: user says /critique-now <path>, 'run critic anyway', 'audit this contract', 'I want a second opinion on this approved design', or wants to verify the accuracy-skip system was right to skip a previous contract."
user_invocable: true
---

# /critique-now — Force contract-critic Against an Approved or Skipped Contract

This skill spawns `contract-critic` against a contract whose `Status:` is `approved`, `implemented`, OR has a `Verdict: skipped` stub from the accuracy-skip system. It is the ONLY user-facing path to retroactively audit a contract that bypassed Step 2.5 of `/design-first`.

## When to use it

- Accuracy-skip engaged on a contract and the user wants to verify the skip was justified.
- A contract was approved months ago and a follow-on issue suggests the design was flawed.
- Random spot-checks for confidence that the area-mapping.json buckets aren't trusting the wrong things.

## When NOT to use it

- Contract is still `Status: draft` — the regular `/design-first` Step 2.5 flow handles this.
- The user just wants to see accuracy state — use `/contract-accuracy` (read-only).
- The user wants to mark a contract as rejected — use `/contract-reject`.

## Step 1: Validate the input

The skill argument is the path to a contract under `.claude/concepts/`. Read the file and confirm `Status:` is one of `approved` / `implemented`, OR the file contains a `## Critique` section with `**Verdict:** skipped`. If neither, refuse:

> "Contract status is `<status>`. /critique-now only runs against approved, implemented, or accuracy-skipped contracts. For drafts, use /design-first; for an inspection without spawning the critic, use /contract-accuracy."

## Step 2: Stage a draft copy

The `contract-critic` agent refuses to run against non-draft contracts (see `.claude/agents/contract-critic.md`). Stage a draft copy:

1. Create `~/.claude/state/critique-now-tmp.md` as a verbatim copy of the original.
2. In the copy ONLY, replace the `Status:` line value with `draft`.
3. If the copy contains a prior `## Critique` section (skip-stub or earlier critic output), strip it from the copy — the critic must operate on the pre-critique body. Preserve the deletion in a comment at the top of the copy: `<!-- /critique-now: original critique section removed for re-evaluation -->`.

## Step 3: Spawn contract-critic

Launch the `contract-critic` Agent (via the `Agent` tool, `subagent_type: agentic-auto-improve:contract-critic`; use the bare `subagent_type: contract-critic` only when the project carries its own `.claude/agents/contract-critic.md`) with:

```
TASK: critique the draft contract (manual /critique-now invocation)
PRIOR_FINDINGS:
  contract_path: ~/.claude/state/critique-now-tmp.md
  contract_status: draft
  origin_contract_path: <real path>
  invocation: critique-now
```

The critic will append `## Critique` to the TMP file. Read the result.

## Step 4: Apply the verdict to the original

Extract the `## Critique` section from the TMP file. Append it to the ORIGINAL contract under a separator. If the original already had a prior `## Critique` section (skip-stub OR earlier critic output), preserve it as an HTML comment block named `<!-- prior-critique YYYY-MM-DD ... -->` ABOVE the new Critique section so the history is auditable.

## Step 5: Update accuracy state if verdict != clean

Parse the new `**Verdict:**` line from the appended section.

- `clean` — accuracy state DOES NOT change. `/critique-now` confirming a previous skip is the most valuable outcome and the existing automated tracker (`critic-verdict-tracker.py`) will pick up the Edit and record a clean run automatically. (Both the manual confirmation and the auto-tracker observation collapse to one increment via the sha-cache.)
- `warnings-only` or `blockers-found` — the accuracy-skip system trusted this area incorrectly. Run:

  ```bash
  py -3 .claude/scripts/accuracy_update.py record-from-contract "<real-path>" critique-now-blocker --failure
  ```

  This derives every area for the real contract and resets each one's `clean_streak` to 0 with `last_verdict: failed:critique-now-blocker`.

- `skipped` — should never occur (the critic doesn't emit this verdict; only the accuracy system does, and we stripped the stub in Step 2). If it appears, log a warning and treat as `warnings-only`.

## Step 6: Clean up the TMP copy

Delete `~/.claude/state/critique-now-tmp.md`. The original contract now carries the new `## Critique` section as the audit trail.

## Step 7: Report to the user

Print:

- The new `**Verdict:**`
- BLOCKER / WARN / NIT counts (extract from the findings)
- Whether accuracy state was reset (and for which areas)
- Suggested next action: if `blockers-found`, suggest `/design-first` on a follow-up contract that addresses them; if `clean`, confirm the original design holds.

## What this skill does NOT do

- Does NOT modify any production code or move the contract through the lifecycle (the contract's `Status:` stays approved/implemented).
- Does NOT delete or move the original contract.
- Does NOT silently override existing Critique sections — they are preserved as comments.

## Hard refusals

If the user invokes `/critique-now` without an argument, refuse with:

> "/critique-now requires a contract path. Run `/list-contracts` to see candidates, or invoke as `/critique-now .claude/concepts/<slug>.md`."

If the contract file does not exist:

> "Contract not found at `<path>`. Check the path or run `/list-contracts`."
