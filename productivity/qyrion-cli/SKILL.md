---
name: qyrion-cli
description: Starts, monitors, replies to, downloads artifacts from, and cancels Qyrus AI mobile and web sessions through the qyrion CLI. Use for explicit qyrion commands, direct session operations (start/stream/send/question/result/cancel), email-report/email-status for existing History reports without rerunning, artifact/screenshot download, app upload, device or test listing, and troubleshooting qyrion CLI errors or exit codes. Do not use for deciding what to test (use qyrus-device-testing) or for git-diff test impact analysis (use qyrus-change-impact).
---

<!-- Distilled from: shared/session-workflows.md, shared/private-execution.md, shared/test-preservation.md, shared/execution-routing.md, shared/local-state.md, shared/prerequisites.md, shared/cli-contract.md, shared/event-contract.md, shared/safety-policy.md, apps/qyrion/docs/getting-started.md. -->

# Qyrion CLI operations

For project variables, `@` references, Default capture, test-owned datasets,
rerun preflight or replacement confirmation, read
`references/test-data-workflows.md` and check its capability gates first.

Direct session operations against the Qyrus device and browser cloud through the
`qyrion` CLI. Use structured modes only (`--json` / `--jsonl`); never scrape
human-formatted output.

For credential-bearing objectives or session history, use the private
input/output wrapper in `references/private-execution.md`, including on
later reads. Plain `qyrus_env.py`/stdin does not redact returned objectives.

For web/mobile objectives, this CLI is the default execution surface, not the
host's browser/Playwright/CUA. Apply `references/execution-routing.md` before
testing or searching saved tests: preserve explicit new/reuse intent and
reuse known ticket inputs. Several independent objectives may use multiple
CLI processes; follow `references/parallel-orchestration.md`, with subagents
optional. Do not parallelize shared-account/state dependencies by assumption.

Read before the first call in a task:

- `references/cli-contract.md` — resolution order, full command catalog, flags
- `references/event-contract.md` — JSONL frames, statuses, park semantics
- `references/safety-policy.md` — binding safety rules

Use the scenario's authorized test username/password in the private objective
or session answer per `references/private-execution.md`. Do not omit the
password or demand manual login merely because it is a password; actual host
restrictions still apply. Discard unrelated credentials from SDK Memory.
Use `references/session-workflows.md` for meaningful session names, scoped
project/test discovery, and platform-correct saved-test reruns. Preserve explicit
user names; otherwise use a short scenario label for multi-scenario runs.
For any requested save/export, read `references/test-preservation.md`: one
resolved project/module, all step pages, full coverage mapping and read-back.
`sessions save-test` saves a Qyrion test into a Qyrion project. "Save it to
(my) Web Testing" means a Web Testing script in one of the person's Qyrus
teams, made through the Qyrus MCP (`qyrus-mcp` skill), never a Qyrion
project named "Web Testing" (`references/execution-routing.md`, Qyrus
product names).

## Preflight (mandatory, in order)

1. Resolve the CLI: `QYRION_CLI` env override → `qyrion` on `PATH`. If missing,
   own setup using `references/prerequisites.md`: announce and install from
   a verified source, then continue. No separate prerequisite prompt is needed.
2. Handshake: `qyrion capabilities --json`.
   - If the command is unknown or fails with a usage error, the CLI is too
     old for this plugin. Offer an update using `references/update-checks.md`;
     after acceptance upgrade through its trusted installation source and
     repeat the handshake once. Preserve explicit source installs/pins.
     Report a remaining blocker; do not improvise against an old CLI.
   - Check the `features` flags before using gated commands (artifact
     download, `sessions question`, `--after-sequence`); see the CLI
     contract's gating table.
3. Resolve credentials and team through `references/credentials.md`: use
   Qyrus MCP's guide and `qyrus_teams_get_by_api_key`, preserving the returned
   team UUID. Do not require the CLI's separate gateway `auth teams` call;
   its failure does not invalidate successful MCP authentication.
4. Confirm team selection: if multiple teams are listed and no team is
   configured, show their names and ask which to use — never guess — then
   persist with `qyrion auth use-team <team-id>` or `QYRION_TEAM_ID` in the
   private file. A single team may be auto-selected; say so. Verify Qyrion
   authorization with helper-wrapped `qyrion sessions list --json`.
   Honor `--profile <name>` if the user works with multiple environments and
   pass the same profile to every subsequent command.

Use the throttled update check at task entry via `references/update-checks.md`.
The version command is `qyrion version --json`; no automatic replacement or
background scheduler is implied.

## Web sessions

For a website, require `features.web_sessions`, then use `--platform web`
and `--start-url <website-url>` without mobile device/app flags. See the
browser commands in `references/cli-contract.md`. Use `qyrus-web-testing`
for exploration and export to durable Aegis tests. Shared credentials are
loaded with `references/credentials.md`; wrap every CLI invocation.

## Core operations

Capture and keep the `run_id`: the first `--jsonl` line of `run` /
`sessions create` is a `snapshot` frame with `run.run_id`. Every later
operation takes that id, from any process.

One-shot verification (terminates on objective completion, meaningful exit
code):

```bash
qyrion run "Log in and verify the dashboard loads" \
  --device-ref <device-ref> --app <app-id> --mode ci --timeout 1800 --jsonl
```

In machine mode `run` never blocks on stdin: if the agent asks a mid-run
question, it exits `5` with a structured `input_required` error naming the
question (gate on the `run_input_required_exit` capability; older binaries
hang until `--timeout` and exit `1`). Answer with
`qyrion sessions send <run_id> "..." --follow`.

Interactive turn loop (live mode parks at `waiting_user_input` between
objectives, device stays allocated):

```bash
qyrion sessions create "Open the app and log in" \
  --device-ref <device-ref> --app <app-id> --mode live --jsonl
qyrion sessions stream <run_id> --jsonl --until input-required --max-seconds 900
qyrion sessions send <run_id> --message-file ./next.md --follow --jsonl
qyrion sessions result <run_id> --wait --json
qyrion sessions cancel <run_id>
```

Always pass `--max-seconds` on streams. Write long messages to a file and use
`--message-file`, not shell arguments.

To wait for a session, prefer `qyrion sessions result <run_id> --wait --timeout
240 --json --compact` over streaming or polling `sessions steps`: it returns when the
run is final or after the timeout (without `--timeout`, `--wait` waits 300
seconds; older binaries return at once, so pass it; 240 stays clear of hosts that
limit a call to about five minutes). A wait that ran out exits 0 with a status
that is not final: the session is still running. In a host that limits one
command, start the session with `qyrion sessions create ... --mode ci --json`
(it returns at once) and observe it with these waits; do not hold the command
with `qyrion run` (`references/cli-contract.md`, "Long sessions"). Check `run.status`; if it
is not final, run `qyrion sessions question <run_id> --json`, answer, and wait
again. `--compact` (feature `compact_session_output`) keeps `run.status`,
`run.step_count`, the newest `run.recent_events` entry, `run.pending_question`,
the summary and the report, and leaves out the artifacts, messages and events
that make a plain result hundreds of KB; read steps the same way with
`sessions steps <run_id> --json --compact --limit 500`, and fall back to the
plain form only when you need the bulk (`references/cli-contract.md`, "Read
compact, not whole"). A command that is killed (exit `-9`, for example when `run --jsonl`
output grows past the host's limit) does not stop the session: take the
`run_id` from the first output line or `qyrion sessions list --json` and
continue with `result --wait`.

To wait on several sessions you started (independent scenarios, see
`references/parallel-orchestration.md`), use one wait over all of them,
gated on `session_wait_any`: `qyrion sessions wait --any <run_a> <run_b>
--timeout 240 --json`. It returns on the first `question`, `finished` or
`failed_to_start` across them, or `timeout`, always with exit 0; handle that
session (answer, read its result, or report it), then wait again on the ids in
`watch_next`. Never block on one session while another may be asking.

## Park state: what a stopped stream means

`--until input-required` exiting 0 means the run parked at
`waiting_user_input`, not that it finished. Distinguish the two park reasons
by the preceding events:

- A `clarification_requested` frame precedes the park → the device agent
  asked a question (`payload.question`, or fetch with
  `qyrion sessions question <run_id> --json`). Answer it via
  `sessions send`, or apply the answer-qyrion-agent-questions policy if that
  skill is available.
- No clarification event → objective-complete park (live mode). Your next
  `sessions send` message becomes the next objective.

A parked session holds a real device. Never end a task with a session still
parked or running: send a final objective, let it complete, or cancel it.

## Artifact (screenshot) download flow

Gated by the `artifact_presign` capability. Screenshots ride on
`tool_result.payload.artifact_refs` (role `observe_raw` = raw device
screenshot).

```bash
qyrion sessions artifacts <run_id> --role observe_raw --json   # list handles
qyrion sessions download <run_id> <artifact_id> --output ./shot.png
```

Then read/view the local file. Prefer `download` over `presign`: local files
are reliable, and presigned URLs are short-lived secrets that must never be
logged, pasted, or committed.

## Exit codes

| Code | Meaning | First response |
|---:|---|---|
| 0 | Success / requested stop condition reached | proceed |
| 1 | Objective failed, blocked, cancelled, or timed out | inspect events + result; report verdict |
| 2 | Invalid usage or missing configuration | fix the command; check `--help` |
| 3 | Auth/authorization failure | see troubleshooting: verify key, tenant, and team |
| 4 | Backend availability failure | see troubleshooting |
| 5 | `qyrion run` parked on an agent question and cannot ask you (`input_required`) | read the question, answer with `qyrion sessions send <run_id> "..."` |
| 130 | Interrupted (SIGINT) | re-attach with `sessions stream <run_id>` |

## Troubleshooting

Read `references/troubleshooting.md` for the failure → remediation table
(auth exit 3, backend 404 `backend_route_missing`, missing capabilities,
device-slot waits, npm auth for the npx fallback).

## Output

Report: the commands run (at a safe level — no credentials, no presigned
URLs), run_id(s), final status and verdict, downloaded artifact paths, cited
event `sequence_no` values, and anything left running (there should be
nothing).
Retain scoped run/test IDs and outcomes per `references/local-state.md`;
never write raw objectives, questions, passwords or signed URLs to memory.
