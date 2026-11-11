---
name: list-contracts
description: "Show every concept contract under .claude/concepts/ grouped by project and status. Highlights contracts needing user action (drafts with unresolved Open Questions, approved contracts not yet implemented). Use when: user says /list-contracts, 'show my contracts', 'what's pending', or after finishing a feature to see what's next."
user_invocable: true
---

# /list-contracts -- Concept Contract Inventory

When invoked, run the `list_contracts.py` script and present its output to the user.

## Step 1: Run the inventory script

```bash
py -3 ".claude/scripts/list_contracts.py"
```

Accepts these optional flags the user may pass after `/list-contracts`:
- `--project <name>` — filter to one project. The name for this repository is the `project.name` slot of `.claude/project-profile.md`.
- `--status <name>` — filter to one status (`draft`, `approved`, `stub`, `implemented`, `archived`, `superseded`, `rejected`)
- `--json` — emit structured JSON instead of the human report

Examples:
```bash
# All contracts
py -3 ".claude/scripts/list_contracts.py"

# Drafts that need user input
py -3 ".claude/scripts/list_contracts.py" --status draft

# Everything in one project (the name comes from the project.name slot)
py -3 ".claude/scripts/list_contracts.py" --project <project.name>
```

## Step 2: Show the report to the user

The script output is a formatted table. Pass it through verbatim (do not reformat) so the user can scan it.

## Step 3: If drafts exist, prompt for next action

If the report lists any **draft** contracts with unresolved Open Questions, ask the user whether they want to continue resolving them now. If yes, open the first draft file with Read, show the Open Questions section, and walk through each question with `AskUserQuestion`.

If the report lists any **approved** contracts, point out that they are ready for implementer agent handoff and name the first one in the list.

## Step 4: If nothing is pending, say so

If every contract is `implemented`, `archived`, `superseded`, or `rejected`, tell the user everything is in a stable state and offer to run `/design-first` for the next feature.

## Status meanings (for the user if they ask)

- **draft** — data-architect has drafted the contract; user still has Open Questions to resolve. Hook BLOCKS edits.
- **approved** — all Open Questions answered; implementer agents can run. Hook ALLOWS edits on `Files to touch`.
- **stub** — a follow-up stub at `.claude/concepts/followups/*.followup.md`, created by `data-architect` Step 4.5 when an Adjacent Areas row was decided as `follow-up handle`. Cheap durable handle for deferred cross-area improvements. Hook does NOT honor stubs as approved — they are NOT permission to edit code. Promote by running `/design-first` against the stub's `What was noticed` paragraph.
- **implemented** — code is live, reviewer has audited. Kept as historical record.
- **archived** — obsolete or deprioritized. Hook SKIPS this contract entirely.
- **superseded** — replaced by another contract (see `Supersedes:` pointer). Hook SKIPS.
- **rejected** — user declined after reviewing the draft. Hook SKIPS.

## Follow-up stubs section

Stubs surface under their parent project's group with a `[STUB]` icon, followed by the stub's `**Issue:**` value (`#<n>`) so the register points at the tracker. A stub whose issue is `pending` or missing is flagged `[NO ISSUE: open one via /design-first Step 3.4]`. The action column shows:
- `[follow-up stub, Nd old]` when fresh (< 7 days)
- `[NEEDS TRIAGE: Nd old; promote via /design-first or let archive_stale_stubs.py reap]` when >= 7 days

Stubs older than 30 days are auto-archived by `.claude/scripts/archive_stale_stubs.py` (invoked by `/validate-registries`) — renamed to `<slug>.followup.archived.md` and no longer surfaced as actionable.
