---
name: gz-mx
persona: main-session
description: Use to open or exit the MX hangar or safe mode, or to check which mode is open.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-20
model: haiku
gz_command: mx
metadata:
  skill-version: "1.7.0"
---

# gz mx

## Overview

The MX Maintenance Hangar lets the operator repair governance surfaces that
the guards themselves protect. While the hangar is open, most governance
guards drop to advisory so repair work can proceed without the checked-in
surfaces blocking the repair itself. Two guards NEVER drop: `gate5_invariants`
and the PRIME DIRECTIVE (ownership — "fix what you know AND what you find").

The same marker carries a second mode. **Safe mode** is the toggle
(GHI #1244): OBPI initiation and brief ceremony are suspended under a written
contract, every guard outside the floor drops to advisory as in the hangar, and the banner names the contract each
turn. Gate 5, the ledger through `gz` verbs, operator PII and the PRIME DIRECTIVE bind
in both modes.

The operator operates this skill; the skill invokes `gz mx`; nobody shells
out to `gz mx enter` or `gz mx exit` directly. The operator never types the verb:
entry and exit are the skill's steps below, and an instruction that hands the
operator a raw `gz mx` command is a defect in the surface that gave it.

## When to Use

- **Entering the hangar** — governance repair session needs to begin; guards
  need to go advisory so you can fix the surfaces they protect
- **Checking hangar status** — confirming whether the hangar is currently
  open mid-session
- **Renewing the lease** — resuming a session whose lease ran out, with the work
  not done; the session stays open and no guard runs
- **Clean exit** — repair is complete; re-enforce all guards at full strength
- **Entering safe mode** — the operator has written a contract that says what the
  mode suspends, what still binds, what each act records and how the mode exits
- **Exiting safe mode** — the contract's exit legs are met; the skill reads them
  before the hard gate runs

## Workflow

1. **Open the hangar**
   ```bash
   uv run gz mx enter --reason "<why>" --attestor g0 [--scope ADR-X.Y.Z ...]
   ```
   Creates `.gzkit/mx.json` marker. Most governance guards drop to advisory. `--reason`
   and `--attestor` are required; the attestor is the operator, never an agent.

2. **Perform the repair**
   Work on the governance surfaces that needed fixing. Gate 5 invariants and
   the PRIME DIRECTIVE still bind — guards drop to advisory so you can repair
   governance itself, not so defects can be deferred.

3. **Close the hangar**
   ```bash
   uv run gz mx exit --attestor g0
   ```
   Removes `.gzkit/mx.json` marker. Every guard re-runs at full strength;
   exit is a hard gate (all guards must pass before exit succeeds).

## Workflow — safe mode (GHI #1244)

1. **Confirm the contract before anything is written.** The operator names the contract
   document, written from `.gzkit/templates/safe_mode_contract.md` under
   `docs/governance/safe-mode-doctrine.md` (first instance:
   `docs/governance/harbor-pilotage-candidate-2026-10-15.md`). The skill
   reads it and confirms it carries § Authority (whose word opened the mode), § Purpose,
   § The general arrangement (the target structure, drawn), § What is suspended and what
   is not, § Mandate, § Records (one commit per act with its trailer and its
   `gz arb red --commit` witness), § Repair orders (the register, each naming the band it
   serves) and § Exit (structural conditions, each with a witness). A contract missing any
   of these is reported and the mode is not entered.

2. **Enter safe mode**
   ```bash
   uv run gz mx enter --mode safe --contract <contract path> --reason "<why>" --attestor g0
   ```
   Same marker, `mode: safe`, bound to its `mx_session_opened` event. The verb refuses a
   missing or outside contract and refuses a contract under `--mode mx`. From this turn
   the banner names the contract; guards outside the floor are advisory until the exit.
   The entry event pins the contract: its SHA-256 and the bodies of § What is suspended
   and § Exit. Each commit that edits the contract while the session is open books
   `mx_contract_amended`, so the ledger always says which version is in force.

3. **Work the repair orders under the contract.** Each act is one commit with its
   `Task:` trailer naming its repair order, its commit-grain witness, and a passage-log
   row with the measurement before and after. The ledger is written only through `gz`
   verbs; no control is removed.

   **Renew the lease when a session resumes past it** (GHI #1261). The orientation
   announces an expired lease; renewal is the operator's call and one command:
   ```bash
   uv run gz mx renew --attestor g0
   ```
   Lease-only: no guard runs, the marker stays, debt keeps aging. Never exit and re-enter
   to renew; the exit is for the drydock's end.

4. **Read the exit before leaving.** The skill reads the contract's § Exit conditions
   and § Repair orders (the orientation's drydock block once GHI #1245 lands; until
   then each witness re-run) and names any condition not met or order still open. One
   unmet condition stops here: the exit is not attempted, and the operator decides
   whether it is waived by a recorded ruling or worked.

5. **Exit through the hard gate**
   ```bash
   uv run gz mx exit --attestor g0
   ```
   Every guard re-runs at full strength with the marker held (marked `exiting`), the
   enter-to-exit log is rendered for the operator, `mx_session_closed` is written, and
   the marker is removed. A red guard puts the marker back and refuses. A session past
   its lease is announced, booked as `mx_session_lease_expired`, and never blocks exit.

6. **Hand back.** The contract's handback amendment (every pilot commit listed, kept or
   reverted, the passage log carried, the suspended rules restored) is drafted by the
   session and ratified by the operator. Civil rule resumes on that ratification, not on
   the exit.

## Example

```bash
# Enter the hangar to repair a drifted OBPI brief
uv run gz mx enter --reason "repair a drifted OBPI brief" --attestor g0

# Perform repair work (briefs, rules, docs)
# ...

# Exit — guards re-enforce; exit fails if any guard is still red
uv run gz mx exit --attestor g0
```

Safe mode, as the skill runs it for the operator:

```bash
# Step 2 — enter under the pilotage contract
uv run gz mx enter --mode safe --contract docs/governance/harbor-pilotage-candidate-2026-10-15.md --reason "harbor pilotage" --attestor g0

# Steps 3 and 4 — repair orders under § Records; § Exit read before leaving

# Step 5 — exit through the hard gate
uv run gz mx exit --attestor g0
```

## Repairing a ledger row

The ledger is the one governance surface hangar mode can never make writable:
`AGENTS.md` § Behavior Rules forbids hand-writing it, and that prohibition is what makes
it trustworthy. A row recorded in error is therefore repaired *forward*, and
the repair is available inside or outside the hangar.

`gz ledger correct` appends one corrective action naming the prior row by its
`(event, id, ts)` triple — the ledger has no per-row id, because `id` carries
the artifact rather than the event. `gz ledger corrections` is the census of
what is currently in force.

```bash
# Review the exact target first; nothing is written
uv run gz ledger correct \
  --subject-event pipeline_launched \
  --subject-id OBPI-0.35.0-08-remember-post-append-advisory \
  --subject-ts 2026-08-23T13:12:21.832251+00:00 \
  --disposition void --cause agent-error \
  --reason "pipeline launched without operator initiation" \
  --attestor g0 --dry-run

# What is corrected right now
uv run gz ledger corrections
```

Three dispositions: `void` (the row records something that was not true — no
reader may count it), `discharged` (the row was true and its condition has
since been resolved — it leaves the liveness reading but stays evidence), and
`reinstated` (undo a prior correction). Operator-gated: `--attestor` and
`--reason` fail closed when empty, on the same terms as `gz obpi repudiate`.

## Constraints

- Operator operates the skill; the skill invokes `gz mx`; nobody shells out, and no
  surface hands the operator a raw `gz mx` command
- Safe mode is entered only under a contract that carries § Authority, § Purpose, § The
  general arrangement, § What is suspended, § Mandate, § Records, § Repair orders and
  § Exit; exit is attempted only after § Exit and the register are read
- `gate5_invariants` and the PRIME DIRECTIVE bind throughout the session
- Exit is a hard gate — do not attempt exit until all detectable defects are fixed
- See `.gzkit/rules/mx-mode.md` for the binding agent rule for hangar sessions
