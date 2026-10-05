---
name: eris-submission-pool
description: Finish an existing build-ready Shipd Project Eris dataset and challenge draft through source upload/import, rebuild, zero-warning validation, Mark as Ready, challenge configuration, preparation, checks, and Run Agents; then stop. Use for a specific linked Eris dataset/problem pair backed by a verified local challenge package. Do not use to turn Pilot, Hold, or Reject candidates into submissions or to invent missing challenge artifacts in the browser.
---

# Eris Submission Pool

Run this as a one-shot state machine, not as a scheduled automation. The terminal success state is a visible confirmation that agent evaluation has started. Stop immediately after recording that state; do not monitor the runs unless the user separately asks.

The fixed phase order is: bind a verified Proceed package; populate dataset metadata and source data files; rebuild; set license and canonical source URL; reach zero-warning dataset validation; Mark as Ready; populate challenge configuration and canonical scripts; run Prepare; reach zero-warning challenge checks; then stop with Run Agents available by default. Click Run Agents exactly once only when the current invocation explicitly requests launch.

## Required companion workflows

Read `../eris-challenge-factory/SKILL.md` for source, novelty, leakage, baseline, grader, ownership, registry, and readiness policy. Use the installed computer-use capability for authenticated Shipd browser work and its confirmation requirements. Read [references/workflow.md](references/workflow.md) before changing either live draft. Store every downloaded or generated artifact beneath the portable bot root.

## Admission gate

Before the first website write, bind the exact user-supplied problem and dataset tabs and match them to one local challenge folder and registry entry. Require all of the following:

- the same machine/task owns the registry entry;
- `readiness.verdict` is `Proceed` with every required boolean true and no unresolved gates;
- the registry status permits building or review, never `pilot`, `hold`, `blocked`, `rejected`, or `abandoned`;
- canonical `prepare.py`, `grade.py`, synchronized paste files, both form-fill documents, source verification, acquisition instructions, raw upload/import plan, smoke tests, baselines, and leakage analysis exist;
- the source files, byte counts, checksums, license, source URL, extracted layout, and every scored native target have been verified;
- local preparation, grader robustness, perfect/sample/malformed submissions, lookup attacks, CPU/runtime limits, and current workspace checkpoints pass.

If the tabs are blank, stale, linked to missing storage objects, or cannot be matched uniquely to a Proceed package, do not populate them from a nearby folder or prior conversation. Record the observed IDs/state and stop for an exact package choice.

## Quality invariant

Resolve every red failure and every yellow warning by fixing the underlying dataset, code, documentation, metric, split, or source decision. Never weaken a check, disguise a warning, hard-code an expected result, alter score bounds dishonestly, or proceed because the platform allows it.

Platform checks are necessary but not sufficient. A green platform result cannot override a failed local novelty, source, independence, lookup, baseline, leakage, or grader gate. If a genuine fix changes the task materially, return to the Eris Scout/Build workflow and re-establish `Proceed` before resuming.

## Live-action boundaries

Treat draft edits, Mark as Ready, challenge submission, and Run Agents as external representational actions. Follow the current computer-use confirmation policy at the moment required. Treat uploads/imports under the upload and data-transmission rules. Never automate authentication, CAPTCHAs, permission changes, or safety bypasses.

When the current user invocation supplies the exact dataset/problem links and explicitly directs autonomous completion through Run Agents, that instruction authorizes these in-scope actions on those exact drafts. Do not ask again after each upload, field, rebuild, Mark as Ready, or check. If the browser-control capability itself requires a confirmation, surface it at that moment; this skill does not bypass tool-enforced controls.

Exact linked drafts always authorize ordinary title/description/tag/configuration/script edits, uploads/imports, rebuilds, validations, Mark as Ready, Prepare, and checks. Do not ask permission for those actions. Cloud deletion remains an always-confirm browser action: route the exact imminent deletion to the batch supervisor for one grouped action-time confirmation instead of asking independently.

## State and evidence

Before the first website write, copy [assets/pool-state-template.json](assets/pool-state-template.json) to `SUBMISSION_POOL_STATE.json` in the exact local challenge folder. Populate the exact problem and dataset IDs/URLs, current platform state, admission evidence, and blocker list. Update this checkpoint after every phase and before stopping so a later run can resume from verified state rather than browser memory.

After each phase, refresh the live page and verify the authoritative visible state. Record the platform version, imported/uploaded filenames and hashes, rebuild result, prepared outputs, check results, warning/failure text, substantive fixes, Mark as Ready state, Run Agents state, and timestamps in both `SUBMISSION_POOL_STATE.json` and the challenge registry or audit log. Keep allowed registry statuses unchanged; use `stage` for fine-grained states such as `blocked_admission_gate`, `dataset_ready`, `challenge_checks_passed`, and `agent_runs_started`.

The reusable pool is this skill plus its workflow and state template. Keep challenge-specific URLs, credentials, filenames, scores, and source facts out of the reusable skill; store them only in the challenge folder and registry.

Stop states:

- **Success:** by default, every check is green and Run Agents is visibly available without clicking it. When launch was explicitly requested, the page visibly reports a started/queued/running evaluation or a nonzero round state.
- **Needs confirmation:** the next live action requires action-time confirmation.
- **Blocked:** a reversible external condition prevents progress; preserve the exact evidence and keep the parent success slot pending. Browser authentication, reconnects, and rate limits are runtime blockers, never candidate rejection.
- **Rejected:** a measured source, novelty, truth, stability, leakage, or shortcut gate invalidates the formulation. Do not publish.

In an outcome-target automation batch, return a Rejected formulation to the controller's candidate-replacement loop. The same immutable task and Shipd pair must receive another independently scouted `Proceed` package; the rejection does not satisfy or terminate the requested success slot.
