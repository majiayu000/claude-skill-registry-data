---
name: close
description: Commit the session to durable vault memory and prepare a clean resume point
trigger: /close
status: DEPRECATED by the two-verb lifecycle — see skills/context-capsule/SKILL.md. /context-capsule absorbs /close; there is no separate close ceremony. Kept for manual invocation during the transition; not deleted.
---

# Session Close

> **Deprecated.** This skill is superseded by [[skills/context-capsule/SKILL.md|/context-capsule]] (docs/two-verb-lifecycle.md). New installs should reach for `/context-capsule`; this file stays for anyone still invoking `/close` by habit during the transition.

Run the aigent-OS end-of-session memory commit inline. The close must be idempotent: rerunning it after a partial failure must not duplicate ledger entries, capsules, or session summaries.

All operator-owned durable state lives under `vault/`. Framework indexes such as `memory/SKILL_LEDGER.md` remain outside the vault and are not session memory.

## Hardened compatibility contract

The active two-verb lifecycle does not run a second close ceremony, but manual
`/close` keeps the same shared postconditions as nightly:

- exact already-authored decision outcomes append only through
  `daemons/nightly-decision-outcome.mjs`, with a unique decision/interval match
  and compare-and-swap;
- bounded Session Log or Active Priorities trimming runs only through
  `skills/context-hygiene/SKILL.md`, archives before removal, and must end in
  `CONTEXT_HYGIENE PASS`;
- Dream synthesis follows `skills/dream/SKILL.md` and must end in
  `DREAM_CONTRACT PASS`;
- cognitive changes follow `skills/cognitive-update/SKILL.md` and must end in
  `COGNITIVE_CONTRACT PASS`;
- missing canonical input is failure, not "nothing to do";
- judgment-bearing measurement entries are staged through
  `skills/nightly-ledger-capture/SKILL.md`.

These helpers use local memory, Git, stderr, and the SessionStart surface. No
external coordination service is required.

## Step 0: discipline audit

Run these checks before writing the daily note.

### Gate A: honesty ledger

If the session included non-trivial work, completed-task claims, multi-file edits, or consequential decisions and `vault/memory/HONESTY_LEDGER.md` was not updated:

1. Run `/honesty-check` on the most consequential work block.
2. Append one structured entry covering verified, inferred, guessed, tradeoffs, stopped short, cost implications, self-rating, and resolution.
3. Continue only after the entry is durable.

### Gate B: trust-decay capture

If consequential work was described as fixed, verified, tested, deployed, complete, shipped, ready, running, merged, or passing and `vault/memory/TRUST_DECAY.md` was not updated, append one to three open Phase 1 claims. Do not convert confident language into evidence after the fact.

### Gate C: failure corpus

If `/diagnose` established a verified cause, append it to `vault/memory/FAILURE_MODES.md` unless an equivalent entry already exists.

### Gate D: decision outcomes

If the operator answered a decision-aging prompt, use the dedicated writer
before closing:

```text
node daemons/nightly-decision-outcome.mjs --root "$AIGENT_ROOT" \
  --as-of <YYYY-MM-DD> --decision-date <YYYY-MM-DD> \
  --decision-title "<exact heading>" --interval <30|60|90> \
  --outcome "<enum>" --operator-text "<exact enum>" \
  --operator-source "<durable direct operator ref>" \
  --expected-file-sha "<pre-read sha256>"
```

Ambiguous, not-yet-due, already-recorded, or raced correspondence is staged
instead of guessed.

### Gate E: weekly measurement

On Friday, include one line summarizing honesty entries, trust-decay captures, failure modes, and decision outcomes for the week. Zero activity after a non-trivial week is a signal that the measurement loop did not fire.

## Step 0.5: somatic integrations

### Review staged memory

Read `vault/memory/MEMORY_CANDIDATES.md`. If staged candidates exist, run `/digest`. Promotion remains human-gated; a close may record deferral but must not silently promote candidates.

### Create a context capsule when needed

Create `vault/memory/capsules/<capsule_id>.md` when any of these are true:

- Context pressure is medium or higher.
- More than five delegations remain open.
- A non-trivial task shipped.
- The operator explicitly requested a capsule.

Use the context-capsule schema, set `status: active`, and connect resumed sessions with `parent_capsule_id`. If a previous capsule is still active, demote it to `resumed` before making the new one active.

Update `vault/memory/BODY_STATE.json` at `state.last_capsule` only after the capsule file is durable.

Skip capsule creation when there is no meaningful state to preserve.

## Step 1: identify durable changes

Update only files whose owned state changed. Typical sessions touch two to six notes.

| Location | Update when |
|---|---|
| `vault/memory/SESSION_LOG.md` | Always, with one idempotent entry per session |
| `vault/memory/DECISION_LOG.md` | A lasting, non-obvious decision was made |
| `vault/memory/ACTIVE_PRIORITIES.md` | Priority, mode, blocker, or completion changed |
| `vault/memory/DELEGATION_TRACKER.md` | A delegation opened, moved, blocked, or closed |
| `vault/projects/*.md` | Project state materially changed |
| `vault/agents/*.md` | Agent scope or capability changed |
| `vault/people/*.md` | A person or role changed |
| `vault/concepts/*.md` | Durable doctrine or a reusable technique changed |
| `vault/memory/PRODUCT_STATE.md` | Its map-of-content links changed |
| `vault/memory/BUSINESS_CONTEXT.md` | Material business context changed |
| `vault/memory/PEOPLE_AND_ROLES.md` | Its map-of-content links changed |
| `vault/memory/BOTTLENECK_PATTERNS.md` | A repeated bottleneck appeared or resolved |
| `vault/memory/IDEA_QUEUE.md` | A useful idea should survive the session |

Create new notes with YAML frontmatter and relevant wikilinks. Do not manufacture notes merely to make the close look busy.

## Step 2: apply edits

For each file:

1. Read the current version.
2. Make the smallest accurate change.
3. Preserve user-authored material.
4. Add relevant wikilinks.
5. Avoid duplicate local entry keys, claim IDs, fact IDs, and capsule IDs.

## Step 3: daily note

Create or update `vault/daily/YYYY-MM-DD.md`:

```markdown
---
title: "YYYY-MM-DD"
tags:
  - daily
date: YYYY-MM-DD
---

# YYYY-MM-DD

## Session Work
- Work completed, linked to notes touched

## Decisions
- Lasting decisions

## Comms
- Material communication state

## Open Threads
- Unresolved work and owners

## Links
Previous: [[YYYY-MM-DD]]
```

Preserve an existing `## Session Captures` section written by hooks. Merge session prose around it rather than overwriting it.

## Step 4: session log

Add one entry near the top of `vault/memory/SESSION_LOG.md`:

```markdown
## YYYY-MM-DD - session topic

**Objective:** one line

**Completed:**
- completed work or None

**Decisions:**
- durable decision or None

**Open threads:**
- unresolved item or None

**Next action:** action and owner

See [[YYYY-MM-DD]].
```

Use the current session's stable local key for idempotency. If the same entry
already exists, update it instead of appending another block. Keep five
detailed recent entries and collapse older entries into the archive.

## Step 4.5: synthesis and bounded context hygiene

Run the shared Dream protocol in `skills/dream/SKILL.md`. Capture an
operating-system temp pre-write snapshot and require literal
`DREAM_CONTRACT PASS`; a caller-supplied candidate count is not evidence.

Then run:

```bash
node "$AIGENT_ROOT/daemons/nightly-context-hygiene.mjs" --root "$AIGENT_ROOT"
```

If it reports red, use `skills/context-hygiene/SKILL.md` to archive whole dated
blocks before trimming, then re-run the checker. Refuse unfamiliar shapes and
compare-and-swap races.

## Step 5: rebuild memory heat

Run:

```bash
node "$AIGENT_ROOT/daemons/memory-heat/compute-heat.js"
```

The output belongs at `vault/memory/HEAT_INDEX.json`. Surface failures; do not hide them behind unconditional `2>/dev/null`.

## Step 6: usage sync

Run, when present:

```bash
bash "$AIGENT_ROOT/daemons/sync-usage.sh"
```

A missing optional daemon is a skip, not a successful run.

## Step 6.5: temporal facts

Append concrete, verifiable state changes to `vault/memory/facts/facts.jsonl`. Facts need provenance, confidence, validity dates, and a stable ID. When a new fact contradicts an old one, close the old validity window and connect it with `superseded_by` before appending the replacement.

Skip this step when no verifiable fact changed.

## Step 7: optional integration validation

Only update an integration validation ledger when that integration was configured and used. Do not claim an optional MCP, plugin, or connector was validated merely because its documentation exists in the repo.

For remindb, use `vault/memory/REMINDB_VALIDATION.md` and record whether a memory tool ran and whether a defined failure occurred.

## Step 7.5: system check

Run:

```bash
bash "$AIGENT_ROOT/daemons/system-check.sh"
```

- PASS: include one concise line.
- FAIL: include the failure lines and continue closing.
- INFO: report the count and durable log location.

The audit does not block memory persistence, but failures must not be described as success.

## Step 7.75: conservative cognitive update

Execute `skills/cognitive-update/SKILL.md`. It may touch only the four files in
that skill's ownership fence. Require literal `COGNITIVE_CONTRACT PASS`. Zero
qualifying updates are valid when the skipped count and source scope are
recorded.

## Step 8: recompute runtime state

After all vault writes:

```bash
python3 "$AIGENT_ROOT/daemons/runtime/update-active-state.py"
```

Read `vault/memory/runtime/ACTIVE_STATE.json` and include active reflexes in the close summary when they require action.

## Step 9: output a brief commit summary

Report:

- Notes updated and why.
- Notes created.
- Checks that failed or were skipped.
- The single most important next-session pickup.

Do not list every file that was merely read.

## Step 10: stamp the close

Write the current UTC ISO timestamp to `.aigent/last-close` only after the durable memory writes complete:

```bash
mkdir -p .aigent
date -u +%Y-%m-%dT%H:%M:%SZ > .aigent/last-close
```

On PowerShell:

```powershell
New-Item -ItemType Directory -Force .aigent | Out-Null
(Get-Date -AsUTC).ToString('yyyy-MM-ddTHH:mm:ssZ') | Set-Content .aigent\last-close
```

If any required write failed, do not advance the close marker. State exactly which artifact remains incomplete so the next `/open` can recover it.
