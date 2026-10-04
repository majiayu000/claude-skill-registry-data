---
name: add-doctor-runbook
description: >
  Adds a new runbook to an existing doctor and registers it in the runbook
  index and mode config. Use when extending a doctor's audit coverage with a
  new check, without re-scaffolding the entire doctor.
---

# Add Doctor Runbook

Extends an existing doctor (scaffolded by `scaffold-doctor`) with one new
runbook — the internal markdown audit definition that drives a single health
check in the doctor's agentic loop.

---

## What you need before starting

- The doctor's project root (where `scaffold-doctor` deposited its output).
- A clear sense of what the new runbook should audit, what signals it reads,
  and what a violation looks like versus expected noise.

---

## Flow

### 1. Locate the doctor's runbook directory and registration files

Inside the scaffolded doctor, runbooks live in `skills/`. The two registration
files are:

| File | Purpose |
|---|---|
| `skills/index.ts` | Runbook index — imports every runbook and exports a `bundledSkills` record. |
| `config.ts` | Mode config — assigns each runbook to `runbooksDaily` or `runbooksWeekly`. |

Read both files before writing anything. Confirm the existing runbook names and
the mode lists so you can slot the new runbook in correctly.

### 2. Gather runbook requirements

Ask the user (or derive from context) three things:

1. **Purpose** — what aspect of app health does this runbook audit? One or two
   sentences.
2. **Signals and tools** — which data sources, queries, or MCP tools will the
   runbook call? (e.g., CloudWatch log groups, a Looker query, a DB table.)
3. **Healthy vs. violation** — what does a clean run look like, and what
   specific conditions should trigger `emit_finding`?

Do not proceed to authoring until all three are clear. If any is ambiguous,
ask a targeted question — a vague boundary between healthy and violation is
the most common source of miscalibrated runbooks.

### 3. Author the runbook markdown

Create `skills/<kebab-case-name>.md` following the structure in
[`../scaffold-doctor/references/writing-runbooks.md`](../scaffold-doctor/references/writing-runbooks.md).

Key requirements (enforced by the authoring checklist in that reference):

- **Pull live config first.** Step 1 of the Inspect section always reads
  thresholds from the app's config store. No hardcoded numbers anywhere.
- **Parameterize every check.** Time windows, count thresholds, feature-flag
  gates — all derived from the config you just read.
- **Healthy runs emit zero findings.** If the runbook would fire on a normal
  day, the threshold or classify logic is wrong.
- **Separate violations from visibility.** Informational observations (counts,
  rates, scorecards) go in the narrative; only actionable violations reach
  `emit_finding`.

For every `emit_finding` call, assign a **stable signature** using the format
for the finding's category, per
[`../scaffold-doctor/references/finding-contract.md`](../scaffold-doctor/references/finding-contract.md):

| Category | Signature format |
|---|---|
| Code bug with stack frame | `{ExceptionClass}:{relativeFilePath}:{lineNumber}` |
| Code bug without stack frame | `{ExceptionClass}:unknown:{md5_12chars_of_normalized_message}` |
| Audit finding | `{runbook}:{category}:{bucketDate}` (ISO week / date / month) |

Unstable signatures cause duplicate PRs and tickets. When in doubt, err toward
broader bucketing — false dedups are cheaper than duplicate work items.

### 4. Register the runbook

Two edits required — both must be made before the doctor is redeployed.

**`skills/index.ts`** — import the new file and add it to `bundledSkills`:

```typescript
import myRunbook from "./my-runbook.md";

export const bundledSkills: Record<RunbookName, string> = {
  // ... existing runbooks ...
  "my-runbook": myRunbook,
};
```

The key must exactly match the `name` field in the runbook's YAML frontmatter.

**`config.ts`** — assign the runbook to a mode:

```typescript
runbooksDaily: [
  "existing-runbook",
  "my-runbook",        // add here for daily checks
],
runbooksWeekly: [
  "aws-cost-analysis", // or here for weekly checks
],
```

**Choose the mode:**

- **`daily`** — checks that catch live regressions or fast-moving metrics
  (error rates, queue depth, send compliance, log anomalies).
- **`weekly`** — checks where daily noise would exceed signal (cost trends,
  coverage drift, long-horizon metrics).

A runbook not in the index never runs. A runbook not assigned to a mode is
imported but never scheduled.

### 5. Remind the user

Tell the user: **the runbook is inert until the doctor is redeployed.** Point
them to the doctor's deploy instructions (typically `sam deploy` or the
doctor's CI pipeline). The new runbook will not execute in the next scheduled
audit cycle until the updated build is live.

---

## Authoring checklist (condensed)

Full checklist is in
[`../scaffold-doctor/references/writing-runbooks.md`](../scaffold-doctor/references/writing-runbooks.md).

- [ ] Runbook file created at `skills/<kebab-case-name>.md`.
- [ ] YAML frontmatter includes `name` (matches filename) and `description`.
- [ ] Step 1 of Inspect reads live config — no hardcoded thresholds.
- [ ] Every `emit_finding` call has a stable `signature` per the finding
      contract.
- [ ] `emit_finding` is called only for actionable violations, not for PASS
      results or informational metrics.
- [ ] Runbook imported and keyed in `skills/index.ts`.
- [ ] Runbook added to `runbooksDaily` or `runbooksWeekly` in `config.ts`.
- [ ] User reminded that a redeploy is required before the runbook runs.
