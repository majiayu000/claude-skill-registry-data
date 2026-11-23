---
name: qyrus-device-testing
description: Run or create mobile app tests on real cloud devices from a build, ticket, story, bug, or objective through Qyrion Mobile Agent sessions. Use for Android/iOS smoke, E2E validation, new reusable mobile coverage, or test-this-app requests even without a Qyrion mention. Use qyrus-web-testing for websites, qyrus-change-impact for a specific diff, and qyrion-cli for command help.
---

<!-- Distilled from: shared/session-workflows.md, shared/private-execution.md, shared/test-preservation.md, shared/execution-routing.md, shared/cli-contract.md, shared/event-contract.md, shared/safety-policy.md, shared/parallel-orchestration.md, apps/qyrion/src/qyrion/cli/main.py. -->

# Test the app on real devices

**Use Qyrion mobile sessions for mobile objectives.** Reuse ticket/build and
permitted test-account details already provided. Do not substitute local
browser/CUA testing or turn a new-test request into a saved-script rerun.
Follow `references/execution-routing.md`: ask about new coverage versus reuse
only when genuinely unclear, in plain language without tool-selection menus.

Read the CLI, event and safety contracts before execution. Read
`references/parallel-orchestration.md` for multiple objectives and
`references/scenario-format.md` for scenario details. Consult other
references only when needed; do not read every reference up front.

Use the scenario's authorized test username/password in the private objective
or session answer per `references/private-execution.md`. Do not omit the
password or demand manual login merely because it is a password; actual host
restrictions still apply. Discard unrelated credentials from SDK Memory.
Use `references/session-workflows.md` for meaningful session names, scoped
project/test discovery, and platform-correct saved-test reruns. Preserve explicit
user names; otherwise use a short scenario label for multi-scenario runs.
For any requested save/export, read `references/test-preservation.md`: one
resolved project/module, all step pages, full coverage mapping and read-back.

## Prepare the target

1. Resolve/install missing CLI prerequisites via `references/prerequisites.md`;
   use `qyrion capabilities --json`. Offer incompatible-version updates via
   `references/update-checks.md`, install only after acceptance, then recheck.
2. Reuse shared setup and confirmed team via `references/credentials.md`;
   verify helper-wrapped `qyrion sessions list --json`. Ask only when multiple
   teams have no selection. Wrap ordinary calls with the installed credential
   helper; use `qyrus_private.py` for credential-bearing inputs/history per
   `references/private-execution.md`.
3. Read optional `qyrion.yml` for project, device and journey hints; use
   `references/qyrion-yml.md`. Account labels are not resolved credentials.
4. Use the user's `.apk`/`.aab`/`.ipa`, an explicitly selected uploaded app,
   or a verified relevant build output. Ask only if no suitable build is
   known; never guess a binary or silently switch environments.
5. Apply the safety policy for target environment, authorized test logins,
   stop-before points and resource limits.

## Define the scenarios

Start from the requested objective and its assertions. For broad discovery,
inspect relevant routes/screens, accessible labels, API clients, flags,
existing tests, requirements, and failure/empty/loading states. Rank by
business criticality, changed/untested surface, regression likelihood,
observability and setup risk; use `references/scenario-format.md`.

A known saved-test project can help dedup the save decision or satisfy a
reuse request. It does not replace an explicit fresh-session request. Do not
scan every MCP project before starting a known objective.

State the bounded scenarios and device choice, then proceed within existing
user authorization. Ask only for missing material scope or a larger test
matrix. Plan-only requests stop before execution. Independent objectives may
run concurrently once account/state dependencies are resolved; dependent
journeys stay sequential or in one session.

## Execute

Upload a local build when needed:

```bash
qyrion apps upload ./app-release.apk --platform android \
  --name "<app-name>" --skip-if-uploaded --json
```

Capture its app ID. `--skip-if-uploaded` deduplicates identical content; on
older CLI support, verify the intended build from `apps list` rather than
claiming a name/version match proves identical content. Select the requested
or suitable available device with `qyrion devices list --platform <p> --json`.

For one objective:

```bash
qyrion run --message-file ./scenario-01.md --platform mobile \
  --device-ref <ref> --app <app-id> --mode ci --timeout 1800 --jsonl
```

For an ongoing journey, use `sessions create ... --mode live --jsonl`, then
bounded `sessions stream <run_id> --until input-required --max-seconds 900
--jsonl` and `sessions send <run_id> --message-file ./next.md --follow --jsonl`.
Apply `references/private-execution.md` to credential-bearing input, all
subsequent history output, and temporary CLI logs; stdin alone is insufficient.
Objectives describe user intent and assertions, not invented account aliases.

Capture each run ID immediately. Inspect questions and artifacts, answer
known facts via `answer-qyrion-agent-questions`, and obtain terminal results
with `qyrion sessions result <run_id> --wait --timeout 240 --json --compact`
(read steps with `sessions steps <run_id> --json --compact --limit 500`; plain
`--json` is hundreds of KB on a long run, see `references/cli-contract.md`).
Multiple independent scenarios may use several CLI processes from one agent;
subagents are optional. Follow the parallel reference for concurrency caps,
monitoring all parked runs, and mandatory cleanup.

## Save and report

When saving was requested, inspect captured steps/login inputs and the live
save contract, then use supported `sessions save-test <run_id> --project <id>
--test-name <name> --json`. Resolve destination metadata at save time if
unknown. Saving was already authorized by "create and save"; avoid asking
again. Do not claim login values are redacted or that an account alias is a
secure reference. Read the asset back; report save and verified rerun separately.

Report each scenario's verdict, run ID, terminal status, assertion evidence,
local artifact paths/event sequence numbers, failure category, and unresolved
questions. A pass requires evidence, not just exit 0. Record scoped handles
and outcomes via `references/local-state.md`; no raw credentials or prompts.
Finish with a `sessions list --json` sweep and cancel only task-owned sessions
still active, including pending/running/parked sessions; report failed cleanup.
