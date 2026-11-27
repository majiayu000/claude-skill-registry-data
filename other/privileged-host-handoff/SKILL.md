---
name: privileged-host-handoff
description: >-
  Drive a human operator through commands on a host you cannot reach (secure admin workstation, jump
  server, bastion, air-gapped box) and verify the evidence they paste back. Use when a command must
  run on such a host or its pasted output needs checking. Not for wizard scripts or steps you can
  run yourself.
metadata:
  revision: "2"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "probe the host, pin what runs, hand over self-contained gated blocks, dry run before execute, read the paste as evidence"
  summary_zh: "人工代跑特权主机：先探测能力、钉住要跑的文件、交付自包含带闸门的命令块、先 dry run 再执行、把贴回的输出当证据核对"
  kind: "entry"
---

# Privileged host handoff

You plan and verify; a human runs each step on a host only they can reach, then pastes the output
back. Every round trip costs the operator minutes inside a privileged session, so the loop is judged
by two things: no step is ever run twice by accident, and every pasted output either proves the
expected state or yields a precise next block.

**Done when** the remote change reached its intended state and you verified it from pasted
evidence (a readback, not the write's own response), or the work stopped at a named blocker with a
read-only diagnosis block ready.

## 1. Map the hosts, then probe before building a route

Write a small host table before the first block: for each host, the identity and tenant it signs in
as, what it can reach (control plane, repositories, registries), its shell and language mode, and
which steps run there. A step that must read something a host's identity cannot reach goes to
another host; name the host in every block heading.

If the developer tenant and the privileged host's production or admin tenant are isolated, do
all developer-tenant control-plane, repository, registry, and CI metadata and artifact reads on
the dev workstation first. Prepare the pinned bundle there and transfer it by the approved route.
Keep privileged-host blocks on local checks and APIs reachable by the verified privileged identity;
never put developer-tenant API calls in those blocks.

Prove every capability the route depends on with one read-only probe block per host: tool presence
and versions, language mode, a GET against each API assigned to that host, and per-target capabilities.
Build the route only on probed facts. Locked-down hosts routinely block binaries, ship patched CLIs,
log command text, or restrict the language. Mark anything derived from docs or source as unverified
until a probe confirms it.

When the host is a locked-down Windows/PowerShell machine, or a block fails there in a way your own
machine does not reproduce, read [references/restricted-shells.md](references/restricted-shells.md).

## 2. Pin what runs

Anything copied to the host (scripts, plans, guard files) comes from a reviewed, merged revision.
Compute each file's SHA-256 from that revision yourself after the merge, and make the block refuse
to run on a mismatch. A script that runs there records its own hash, its inputs' hashes, the
language mode, and start/finish time in an evidence file, so a pasted result can be tied to the
exact bytes that produced it. After every fix-and-merge, re-derive the hashes before handing out
the next block.

## 3. Write each block to the contract

Batch all probes, preflight checks, or cohesive steps for the same host and phase into one
self-contained script block. One paste completes the phase and prints its results; do not send
one command per turn.

Every block is pasted into a fresh or long-lived console by a tired human. It must:

- be self-contained: one scope (`& { ... }` in PowerShell, `( ... )` or `set -euo pipefail` in a
  subshell for bash) so a failing guard stops the whole block, and assign every variable it uses;
- have every value filled in: no `<placeholder>`, no interactive prompt (`Read-Host`, `read -p`
  read the next pasted line), no reliance on a previous window's variables;
- open with gates that throw on mismatch: signed-in identity and tenant/subscription, target
  context (cluster, account, workspace), and each pinned file hash;
- write evidence to a fresh timestamped directory and print a compact, structured summary in a
  `finally`, even on failure: phase result and per-check outcomes; use tight queries, not JSON dumps;
- label itself read-only or mutating, and state above it the expected outcome with counts and
  order, plus the stop rule for anything else.

Skeletons for PowerShell and bash: [references/block-templates.md](references/block-templates.md).

## 4. Run in phases

Split handoffs only at a phase gate or host boundary, not between checks in the same phase.
Review is a human gate, not a script step; never combine dry run and execute in one paste.

1. **Inventory / probe** (read-only).
2. **Dry run**: the mutating script in plan mode. State the expected plan before the operator runs
   it (for example "18 present, 6 would-create, in this order").
3. **Review** the pasted plan against the expectation, item by item.
4. **Execute**: a block that differs from the dry run only by the execute switch and the evidence
   directory name. Ask for the operator's go-ahead immediately before an irreversible step.
5. **Acceptance**: independent readbacks and behavioral probes. Probe guards both ways: one
   request that must be denied and one that must be allowed (a server-side dry run proves admission
   behavior without writing).

## 5. Read the paste as evidence

- Check identity, hashes, language mode, and the result field first; then compare counts and items
  with what you predicted. A zero exit code is not proof: shells report stale exit codes after a
  thrown error or a pipeline.
- When a run stops, say whether your own guard stopped it (the guard worked; adjust inputs or the
  code) or the platform refused (a fact about the host you had not probed).
- An `unknown` or partially applied outcome is never rerun. The next block is read-only: read the
  live state of every touched resource, then decide between a fix and a resume.
- Ship the smallest verified fix quickly while the operator still holds the session; defer extra
  hardening rounds to after the step lands.
- Explain each operation once in plain words (what it does, why, how to read its result) and give
  the runbook path; expand jargon and acronyms the operator may not share.

## 6. Mutate shared resources defensively

- Guard each write on the current value (compare-and-set): read, check it equals what you
  expected, then write; refuse on drift.
- Read back with an independent GET; the platform may normalize fields, so compare the fields you
  own and allow documented defaults explicitly.
- Before deleting and recreating a shared object (a service connection, an identity binding),
  capture its full configuration including attached checks and permissions, get explicit approval,
  recreate, restore each attachment, read each back, then chase every place that embeds the old
  identifier (federated subjects, docs, script parameters).
- Prefer the platform's own refusal over a missing lock: if a protection cannot be applied to a
  resource type, replace it with least privilege plus an alert on the destructive operation.

## Additional resources

- [references/restricted-shells.md](references/restricted-shells.md): read when the host runs a
  restricted shell or a block fails there but not on your machine.
- [references/block-templates.md](references/block-templates.md): read when writing the first block
  for a host.
