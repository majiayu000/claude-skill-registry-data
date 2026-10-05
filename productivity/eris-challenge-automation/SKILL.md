---
name: eris-challenge-automation
description: "Operate the reusable Project Eris challenge workflow when the user says Ready, Status, Status & Fix, Create X Task(s), supplies Shipd challenge/dataset link pairs to finish, asks to run or manage an Eris task batch, or wants the repeatable challenge-creation bot. Coordinates the bundled factory and submission skills, keeps a durable local ledger, distinguishes local records from fresh Shipd observations, and never bypasses dataset or challenge checks."
---

# Eris Challenge Automation

Use this skill as the command router and durable coordinator. This portable workspace bundles the companion factory and submission skills under the same `.codex/skills/` directory; those local copies are authoritative for this bot.

## Start

1. Run `validate-portable.ps1` from the bot root. Do not fall back to external workspace files if validation fails.
2. Read [references/commands.md](references/commands.md).
3. Read [references/lifecycle.md](references/lifecycle.md) for `Create X Task(s)` or any multi-task/status-repair operation.
4. Read [references/linked-drafts.md](references/linked-drafts.md) whenever the user supplies or promises Shipd challenge/dataset URL pairs.
5. Read [references/resilience.md](references/resilience.md) for multi-task runs, incomplete batches, rate limits, reconnects, or browser failures.
6. Read [references/visible-workers.md](references/visible-workers.md) for every multi-task batch or when the user asks for separate visible tasks/browsers.
7. Read `Config/workspace.json`; resolve every configured path relative to the bot root and use `eris_automation/run.ps1`.
8. Read the active batch with `eris_automation/run.ps1 status --json` before mutating the ledger.

## Route Exact Commands

- `Ready`: run the safe local ready operation. Never delete packages, registry files, evidence, or platform drafts.
- `Status`: perform a fresh authenticated read-only Shipd inspection for every bound active task, record the observation, and then report both live and local state with timestamps.
- `Status & Fix`: do `Status` first, then repair every genuine red or yellow finding, rerun the affected checks, and update the ledger. Do not suppress checks or weaken graders.
- `Create X Task` / `Create X Tasks`: create one batch whose completion target is exactly `X` successful challenge slots, then execute the gated lifecycle. A rejected dataset candidate is an attempt within its slot; immediately search for a replacement. By default a slot succeeds when all checks are green and Run Agents is visibly available; launch agents only when the current invocation explicitly requests it.
- `Finish X Linked Tasks`, `Submit X Linked Tasks`, or exact challenge/dataset URL pairs with a clear instruction to complete them: invoke the Linked Draft Finisher role. Bind the pairs in supplied order, overwrite disposable placeholder values, and carry every verified task through zero-warning checks. Launch agents only when explicitly requested.

When a `Create X Task(s)` request already includes exactly `X` challenge/dataset pairs, combine the modes: research and build each slot, bind the corresponding supplied pair, finish the platform workflow, launch agents once, and stop that slot.

Treat close natural-language equivalents the same way. A bare `Status` is read-only and does not authorize fixes or submissions.

## Required Boundaries

- For scouting, pilots, builds, revisions, source/license checks, baselines, leakage audits, and `Proceed` validation, read and follow `../eris-challenge-factory/SKILL.md`.
- A `Create X Task(s)` command explicitly authorizes X user-visible persistent Codex worker tasks, one per immutable slot. Create them at batch start with the exact fixed Shipd pair and bind them with `bind-worker`. A worker may perform Scout/Pilot and candidate replacement; it may enter full Build only for an evidence-backed `Proceed` idea.
- For a verified local package plus an exact Shipd dataset/problem pair, read and follow `../eris-submission-pool/SKILL.md` through rebuild, zero-warning validation, Mark as Ready, challenge checks, and Run Agents.
- Do not use `eris-submission-pool` to manufacture missing artifacts in the browser. If a slot lacks a supported dataset/problem draft route, stop it at `build_ready` and report the exact missing binding.
- Do not terminate a requested slot because a candidate fails source, license, novelty, scale, leakage, shortcut, metric, or runtime gates. Record the failed candidate with `replace-candidate`, return that same slot to Scout, and search broadly for another candidate. Preserve every quality gate.
- Fix every red failure and yellow warning substantively. Never tamper with an agent, validation check, grader, or evaluator merely to make it pass.
- Keep source URLs and licensing in dataset metadata. Apply the factory's platform-visible source-hiding rules where relevant, but do not misstate provenance.
- Supplying exact link pairs authorizes all ordinary draft edits, uploads/imports, rebuilds, validations, Mark as Ready, script/configuration changes, Prepare, and checks on those exact drafts. Do not ask whether placeholders may be replaced or whether checks may run. Launch agents only when the current invocation explicitly says through Run Agents. Browser-enforced always-confirm actions—especially deleting a cloud file—cannot be pre-authorized; workers must centralize and group them through the supervisor rather than asking separately.
- Stop the submission workflow immediately after confirmed agent launch, as required by `eris-submission-pool`.
- Treat model rate limits, reconnects, browser-control outages, and expired browser sessions as retryable runtime events, never candidate rejection. Checkpoint first, back off, reduce concurrency/context when useful, and resume the same slot. Browser authentication may require the user to restore the session, but the batch remains incomplete and resumable.
- Every platform worker must explicitly use the Codex in-app browser, make it visible, open separate exact dataset and challenge tabs, and preserve them for handoff. Do not use Chrome/extension profiles for this workflow unless the user explicitly changes the browser choice.

## Persistence

Use the local controller for batch IDs, task IDs, registry bindings, platform IDs, observations, revision counts, and terminal history. Save every durable artifact under `Workspace/output/` or `Working/`. Never claim acceptance or live readiness from local files alone. Record exact URLs/IDs and evidence timestamps after each live inspection.
