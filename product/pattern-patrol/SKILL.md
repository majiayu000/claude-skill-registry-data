---
name: pattern-patrol
description: "Pattern Patrols system of recurring, certified sweeps. Use when you are a patrol run or an assignment names a P# id, you spot a registered-pattern violation off-mission (log a sighting), a mistake class keeps recurring, or you touch PATROL_REGISTRY or PATROL_SIGHTINGS. NOT for one-off bug fixes."
---

# pattern-patrol — keep eradicated problems dead

**Canonical system (read first):**
`../common-docs/systems/intelligence/pattern-patrols/FEATURE.md`
**Arman's target:** `.../pattern-patrols/VISION.md`
**The patrol list + status:** `.../pattern-patrols/PATROL_REGISTRY.md`
This skill is the matrx-frontend mechanics. Never duplicate the registry here.

## The one-paragraph model

A _patrol_ is a named pattern Arman wants permanently eliminated (or a good
pattern he wants present everywhere), backed by doctrine, a durable queue, a
skill teaching the fix, a scheduled recurring run, and adversarial
certification of every fix batch. The registry owns the current count. A patrol
stays in **ERADICATION** until an independent full pass proves zero actionable
backlog; only then may it enter **MAINTENANCE**. Detection is never the terminal
job while actionable work exists.

## Duty 1 — running a patrol (you were launched as one)

Follow the per-run template in `CODEX_OPERATOR.md` (same directory as the
system doc). The repo-specific facts it needs:

- **Ledger:** `.matrx/PATROL_SIGHTINGS.md`. **Permanent run history:**
  `.matrx/patrol-runs/<P#>/<run-id>.json` (append only through
  `pnpm patrol:run`; `latest.json` is only a projection). **Reports:** `.matrx/patrol-reports/<id>.md`
  (create the directory on first use; one file per patrol, overwritten each run
  — it carries your scan baseline).
- **Resume before discovering:** inspect `latest.json` and its permanent record
  before a new scan. An unfinished approval, fix, certification,
  infrastructure retry, or delivery resumes with its exact candidate first.
  Never strand it, overwrite its report, or ask Arman to repeat a decision.
- **Modes, not reporting tiers:** ERADICATION consumes the ranked ready queue
  before broad discovery, uses every available parallel-agent slot (never more
  than ten workers), and runs multiple independently certified batches until
  verified zero or one hard blocker stops every remaining ready item.
  MAINTENANCE is allowed only after independent zero proof; its first finding
  switches the same run back to ERADICATION and starts repair immediately.
- **Per-item routing:** every verified item is `repair-now`,
  `genuine-human-decision`, or `hard-blocked`. Repair-now executes now. A
  decision or blocker stays open while the patrol takes the next independent
  repair-now item. A detector, ranked list, chip, or machinery improvement is
  never a completed patrol outcome while ready product work remains.
- **Professional improvement standing authority:** automatically fix a
  verified defect or weakness when one remedy is clearly superior, reuses a
  canonical primitive or demonstrated industry standard, preserves product
  behavior/contracts, and fits a bounded certified batch. The skill need not
  enumerate the exact callsite. Known bugs and established quality upgrades do
  not wait for permission.
- **Decision routing:** ask Arman only when legitimate alternatives materially
  change product behavior, policy, workflow, permissions, data meaning,
  destructive impact, or visual intent. Missing evidence/machinery creates a
  focused task or infrastructure state. If the core repair is clear and an
  optional enhancement is debatable, ship the core and ask only about the
  enhancement. Implementation uncertainty never turns into a pointless
  approval request.
- **Human decisions are item-scoped:** when Arman chooses among legitimate
  alternatives, apply only that decision. The resulting repair still uses a
  bounded Tier-M batch with normal gates and adversarial certification. Reports
  separate standing-authority fixes, genuine human decisions, unresolved
  evidence/machinery, and the batch verification/certifier verdict. It never
  repeats a known defect inventory as a substitute for execution.
- **Hard rules, non-negotiable:** never disable a check, add a suppression,
  touch generated files, or change how a component enters a chunk (THE
  FRAGMENTATION LAW — `code-splitting` skill before ANY such change); fixing
  one side must not move the other (mobile↔desktop, dark↔light);
  `pnpm type-check` before any done-claim. Commit every coherent batch
  immediately and push it to a remote ref within 15 minutes. After independent
  certification names the exact candidate SHA, integrate it through the normal
  fast `origin/main` workflow within 45 minutes. Only deployment/release stays
  serialized.
- **Shared-checkout ownership:** scheduled patrols run in the canonical shared
  checkout; worktrees are forbidden. Capture exact base SHA, dirty paths, and
  baseline diagnostics before editing. Unrelated dirty files belong to other
  owners: never stage, rewrite, revert, stash, or clean them. Claim disjoint
  repair units, re-read an owned file before editing, use path-scoped Git, and
  commit only owned files. Concurrent unrelated work is not patrol evidence.
- **Exclusive preview lease:** `pnpm preview:start` uses only the canonical
  checkout's managed server. Never stop it while another task is actively
  verifying. `pnpm preview:status` reports ownership. Read the machine-profile RSS cap from launcher status;
  the five-minute startup-progress cap remains fixed. The launcher never
  restarts automatically.
- **Certification (Tier M):** a second adversarial agent ("assume this batch
  broke something; find it") compares pre-edit and post-edit type/gate
  diagnostics. New batch-caused failures reject; unchanged baseline debt is
  loud but cannot reject. Apply `FEATURE.md`'s risk-based visual proof: every
  changed file gets scoped static coverage, repeated mechanical edits get one
  representative surface per distinct risk class, and shared primitive/layout/
  interaction/theme changes get the full relevant matrix. CERTIFIED ships;
  REJECTED requires a concrete batch defect and is fixed/reverted;
  INFRASTRUCTURE BLOCKED preserves the approved diff for retry. A broken preview
  is never proof that product code broke. Only one managed preview runs
  machine-wide; concurrent patrols queue instead of starting a second build.
  No independent verdict → invalid run.
- **Fast integration, serialized release:** push the candidate immediately.
  After an independent certifier records `CERTIFIED` for the exact candidate
  SHA, integrate it into `origin/main` through the normal shared workflow;
  preserve that commit as an ancestor. The machine-wide lease applies only to
  `./scripts/release.sh`. If a newer release already contains the candidate,
  record that version instead of creating another bump.
- **Scoping:** structural novelty (new `app/**/page.tsx` leaves, new
  `features/*` dirs, new files matching the patrol's surface signature) + the
  ledger + a full pass every Nth run. NEVER scope by raw git churn.
- **Loud degradation:** if a patrol cannot execute its ready queue, or a
  required read, scan, fix, certification, gate, release, report, or memory
  update does not happen, follow `FEATURE.md`'s exact Loud Degradation
  Contract. Begin with `AUTOMATION DEGRADED — ACTION REQUIRED`; when Arman must
  act, end with `ARMAN, WE NEED YOU: <one specific next action>.` Counts alone
  are never an adequate warning.
- **Human-owned exceptions:** agents may propose an exception but never clear,
  suppress, allowlist, or approve one. Every proposal stays an open finding,
  includes a production review URL, and ends with `EXCEPTION APPROVAL REQUIRED`
  plus `ARMAN, WE NEED YOU`. After explicit approval, record a durable approval
  id/reason/reference in the patrol's typed allowlist and beside the source;
  detectors report approved exceptions separately instead of hiding them.

## Duty 2 — logging a sighting (you're on another mission)

You spot a live violation of a registered patrol. **Do not fix it** (unless it
is literally inside the lines you're already changing — boy-scout rule). Add
one line to `.matrx/PATROL_SIGHTINGS.md`:

```
- [ ] P4 | features/foo/Bar.tsx:120 | bg-white with no dark: pair on the modal shell | 2026-08-08
```

…and continue your mission. The patrol verifies sightings itself; yours is a
hint, not a promise, so thirty seconds is the right amount of effort.

## Duty 3 — nominating a new patrol (the list must grow)

When a mistake you're fixing looks like a PATTERN — same class in a third
place, something Arman has ranted about, a check you wish existed — **stop and
tell him**: the pattern in one sentence, grep-level evidence with real counts
(run the greps; no vibes), proposed tier + cadence. On approval: add the
registry row (or Candidate-bench line), dispatch the sweep to a subagent with a
named lane (law 7 — never a `spawn_task` chip), and note which of
the five parts already exist. Promotion patterns (presence of something good —
copy-for-AI, assists, admin-map rows) qualify exactly like elimination
patterns.

## Anti-patterns

- Fixing sightings off-mission (derails sessions — the ledger exists so you don't).
- A patrol "improving" style beyond its registered pattern.
- Reporting a clean run as wasted effort — zero findings is the system working.
- Marking a registry status ✅ that isn't (the registry must never lie).
- Giving a polished normal-looking summary for a degraded or incomplete run.
- Rejecting or reverting valid work because an unrelated baseline gate or the
  preview harness failed.
- Using a noncanonical preview, leaving owned work uncommitted or
  unpushed, or delaying certified work behind a fictitious integration gate.
- Treating a Markdown report or automation memory as more authoritative than
  the permanent run record, or rewriting an earlier lifecycle event.
- Stopping after detection while any actionable repair remains, or
  asking Arman to approve an obvious professional improvement.
- Assigning parallel agents to summarize or rank defects instead of giving
  each one a disjoint repair unit with required verification.
- Treating “looks intentional” or “false positive” as approval to suppress it.
- Growing this skill with per-patrol content — that belongs in the registry row
  or the pattern's own skill.
