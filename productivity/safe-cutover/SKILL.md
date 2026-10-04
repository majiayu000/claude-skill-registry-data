---
name: safe-cutover
description: "Pre-ship safety proof for replacing a live implementation with a canonical one. Use when repointing nodes, tools, or services to a new contract, superseding a schema, retiring a legacy or parallel system, or any 'new way replaces the old way' change. NOT for greenfield or unconsumed additive work."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/safe-cutover/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# safe-cutover — the proof that comes before the switch

**Arman's bar, verbatim (2026-08-23):**

> "I will be ready to do it the instant I have a guarantee that we have ample tests in place that
> will guarantee that this change cannot cause errors from any of the many paths that it can be
> triggered from so that all upstream and downstream things that are impacted have already been
> addressed and resolved."

That is the standard for every cutover, not just the one he said it about. A cutover is not a
code change with tests attached; it is **a proof, staged on a branch, that a human approves.**

## The law

1. **Enumerate before you touch.** You cannot prove safety for paths you never listed.
2. **The inventory is evidence, not memory.** Every path is found by a command whose output you
   can show — never by "I think that's all of them."
3. **Tests are DERIVED FROM REALITY.** Generate them from the live definitions, rows, and call
   sites that actually exist. Imagined tests prove imagined safety.
4. **No gap is "probably fine."** Every consumer that would see a change is either made
   compatible or updated in the same change.

> 🚨 **UNRESOLVED CONFLICT — `CFL-057`. Do not build against this section until Arman rules.**
> **This document says:** a cutover is staged on a branch, fully green, and that branch merges only when the approver says yes.
> **[`shared-checkout.md`](/policies/shared-checkout.md) (committing continuously; never requesting your own branch) says:** commit and push to main continuously and never hold work in a private branch or worktree, because held-back code goes stale and is lost once its task is checked off.
> **Why it matters:** it decides where a breaking cutover waits for approval — on a held branch the shared-checkout rules forbid, or somewhere off the live path that still never holds code back from main — and every data-to-kinds cutover waits in exactly that spot.
> **Your move:** bring Arman these two readings and the consequence, get his ruling, then build.
> Register: [`/operations/conflicts.md`](/operations/conflicts.md) · `CFL-057`

5. **Stage, don't ship.** The cutover lands on a branch, fully green, and waits for the human.
6. **Say what you could not prove.** An honest "this path cannot be tested because X" is worth
   more than a confident sweep. Never round up to "safe".

## Step 1 — Enumerate every trigger path

The paths that bite are the ones that are not code. Check all of these, every time:

| Where callers hide | How to find them |
|---|---|
| Code call sites | grep + the blast-radius tool (`aidream/scripts/kind_consumers.py` for kinds; write the equivalent query for other subjects) |
| **Stored definitions** | workflow definitions referencing the node/field (JSON queries over the live table) — **field references like `{{node.results}}` are what actually break when a shape moves** |
| **Rows that are configuration** | mandates/bindings declaring the old identity — these live in DATA, invisible to grep |
| **Rows that OVERRIDE code** | e.g. an ACTIVE `source='db'` component row silently beating the new canonical one (this bit the search pilot) |
| Triggers / subscriptions | anything firing on the old identity |
| API + service internals | routes, pipelines, and services calling it without going through the public path |
| UI consumers | components rendering the old shape |
| Agents | prompts/schemas naming the old fields |

Output an inventory table: **path → how it consumes the output → does the cutover change what it
sees → what makes it safe.** Count the live ones (published/active) separately from the dormant.

## Step 2 — Close every gap the inventory exposes

Per affected consumer, choose ONE and record it: (a) make the new output compatible so the
consumer sees no change, (b) update the consumer in this same change, or (c) version it so both
shapes are served. There is no (d).

## Step 3 — The history plan (mandatory, never silent)

Superseding a shape can invalidate rows already stored under the old one and can break replay of
past runs. Choose and record: **backfill** the old rows · **version-pin** them to the superseded
schema · **accept-and-record the loss with the measured row count.** Silence here is how the past
gets lost.

## Step 4 — Build the proof

- One test per trigger path from the inventory — the table IS the checklist.
- **Contract tests generated from the live definitions**, so every real field reference is
  asserted (this is the test set that catches the `{{node.field}}` breakages).
- The compatibility verdict on the schema change, recorded.
- A **real end-to-end run** of at least one live consumer, before and after, outputs diffed.
- Render tests for any converged UI.
- Run the whole suite with the cutover APPLIED on the branch. Green means green everywhere,
  including the gates the repo already has.

## Step 5 — Leave a guard behind

A passing sweep proves the past; a **committed guard prevents the future.** Add the check that
makes the old pattern fail the build (house pattern: `aidream/scripts/check_kind_marker_law.py`
— static leg over source + live leg over the DB + a blessed, shrinkable allowlist). Without it,
the next new file re-creates what you just deleted.

## Step 6 — Report, then wait

Report **in chat, in plain language**: how many trigger paths exist, what each one is, what the
tests prove, what you changed to make it safe, what could NOT be proven and why. End with a
clear **"safe to cut over"** or **"not yet, because X."** Never send the approver to a document.
The branch merges only on their word.

## Standing rules

- **Delete what you replace.** A cutover that leaves the old path alive did not happen — two
  systems doing one job is the disease being cured. No shims, no fallbacks, no "temporarily".
- **The dormant is not the safe.** An unpublished definition still gets published later; either
  convert it or record it as knowingly stale.
- **Plumbing never goes to the approver.** Missing credentials, codegen failures, flaky
  environments go in a developer list at the bottom — routing agent-doable work to a human is
  itself a defect.
- **Improve this skill as you go.** Every cutover teaches something the next one needs: append
  the new hiding place, the new breakage class, the new guard. Canonical copy lives here; run
  `python3 common-docs/meta/scripts/sync_skills.py` after editing and commit each repo's mirror.

## Lessons already paid for

- **Mandates and bindings live in DATA.** A code-only cutover misses every row declaring the old
  identity. (search pilot)
- **A stale ACTIVE `source='db'` component row silently overrides the new canonical component** —
  deactivate with a note, never delete. (search pilot)
- **Field references in stored definitions are the real breakage surface**, not import graphs.
- **The schema supersede must ride the SAME change as the repoint** — live nodes verify their
  output against the registry every run, so a split lands one half in a failing state.
