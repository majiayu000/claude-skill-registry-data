---
name: gaia-steward-lane
description: >-
  Pick up one bounded Gaia Steward maintenance dispatch, do exactly it, and hand
  the result back for independent verification. Use when the user says "check the
  steward lane", "pick up maintenance work", "is there anything for me to fix",
  "run the steward lane", "/gaia-steward-lane", or when a scheduled routine wakes
  you with no other instruction. Also use before starting speculative repository
  cleanup: if Steward has not found the work, the work probably does not exist.
version: 1.0.0
---

# gaia-steward-lane

The pickup point for Gaia Steward's bounded Class B lane.

Steward decides *what* maintenance exists and *how much authority* it carries.
This skill is how you take one item of that work, stay inside its envelope, and
hand it back in a shape that can be verified rather than trusted.

## The one thing to understand first

You are not being asked to maintain this repository. You are being asked to
resolve **one finding**, inside **one envelope**, and to stop.

Almost every failure mode of this skill is the same mistake: noticing something
else worth fixing and fixing it. Don't. Note it in your report — Steward will
observe it on its own next scan, and it will arrive with its own authority.

## Getting work

```bash
gaia steward lane next --prompt
```

Three possible outcomes, all normal:

| Output | Meaning | What you do |
|---|---|---|
| A full prompt beginning `# Tree Keeper dispatch` | There is work | Follow that prompt. It is the contract; this file is only how you got it. |
| `Nothing to dispatch: no queued Class B debt` | Steward found nothing | **Stop. Report that and end.** A quiet lane is a healthy lane. |
| `Nothing to dispatch: … maxInFlight ceiling` | Work is already outstanding | **Stop.** Someone else's dispatch is unverified. Do not start a second one. |

Exit code `0` in all three cases. Idle is not failure.

If you want to see the state before asking for work:

```bash
gaia steward lane status
```

## Doing the work

The rendered prompt carries everything that binds you: allowed paths, allowed
commands, forbidden paths, stop conditions, and a proof contract. Read all of it
before your first edit.

Two rules the prompt states and this file repeats because they are the ones most
often broken:

1. **The allowed commands are your only mutation interface.** If the envelope
   grants you no command for something, you *describe* the change — you do not
   reach around the missing command and do it by hand. This repository routes
   changes through tools for reasons those tools enforce and you cannot see:
   audit trails, validation, provenance.
2. **You may not widen your own authority.** Needing a path, command, or decision
   you were not granted is a *finding to report*, not a permission to assume. Say
   so and stop; that is a successful dispatch.

A dispatch that concludes "the finding does not reproduce" is also successful.
Do not manufacture a change to justify the run.

## Handing it back

Capture two things: the diff, and a record of the commands that prove it.

```bash
git diff > candidate.diff
```

Write the proof transcript as `steward-proof-transcript-v1`, one or more entries
per item in the packet's proof contract, numbered from 1 in the order the packet
lists them:

```json
{
  "schemaVersion": "steward-proof-transcript-v1",
  "entries": [
    {"contractIndex": 1, "command": "python scripts/validate.py", "exitCode": 0, "output": "…"}
  ]
}
```

Then verify:

```bash
gaia steward verify <debt-id> --diff candidate.diff --proof proof.json
```

**Do not skip this and do not summarize the diff instead.** Most of what a
reviewer would check by eye is mechanical, and Steward checks it for free: scope
against the envelope, proof coverage and exit codes, whether guards were
weakened, whether unrelated debt appeared while you worked.

Exit codes: `1` reject, `3` escalate, `0` pending. **`0` does not mean accepted.**
Steward has no authority to accept — it can only fail to object. If you get `0`,
say so plainly and hand the work to a human or a second reader; a run of
`--prompt` will render the independent verifier's prompt for exactly that.

If you get `1` or `3`, read the reasons. They are specific, and they are usually
right. A reject on scope means you edited something you were not granted; fix
that before anything else.

## What you must never do here

- Merge, push to `main`, tag, or release.
- Widen `founder/steward/POLICY.yaml`, or edit anything under `.gaia/steward/`.
  The policy defines your authority and the receipts are the audit trail; an
  agent editing either is the failure this whole system exists to prevent.
- Record an `accept` verdict for your own work. `gaia steward lane record
  --verdict accept` exists for a *second reader*, and its `--note` records who
  said so.
- Take a second dispatch before the first is verified.

## Optional External Operator Advisory (Outside Runtime Only)

Gaia Steward maintenance dispatches run with a strict zero-model budget. Model execution is strictly forbidden inside the automated Class A/B dispatch loop. However, an external operator inspecting maintenance debt outside the runtime may optionally run the read-only advisory runner ([docs/agents/jev.md](../../../docs/agents/jev.md)):

```bash
# Offline dry-run by default ($0 spend); add --live to query TypeSafe API
gaia steward scan --json > /tmp/debt.json
python scripts/jev_advisory.py --mode steward --input /tmp/debt.json
```

This inspection provides non-binding hints only, never reorders maintenance debt, never expands the dispatch envelope, and hands off to `worker-luna` when uncertain or offline.

## When there is genuinely nothing

Say so in one line and stop. Steward is measured on its no-op rate as much as its
closure rate — a system that always finds something to do is a system that
manufactures work.

## Where the rest of this lives

- `founder/steward/README.md` — the policy in prose, and what each bound is for.
- `founder/steward/routines/` — the human contract for each routine, and cadences.
- `founder/STEWARD.md` — why any of this is shaped the way it is.
