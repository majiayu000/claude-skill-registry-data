---
name: acp-worker
description: Run or continue an operator-authorized external ACP worker through cwr-acp, using a configured default or an explicitly selected route. Use when the operator has selected ACP for this responsibility; native workers and merely discovering an ACP-capable CLI do not trigger it.
---

# Optional external ACP worker

Use the operator's current ACP default or explicit task selection. Defaults and
authorized fallbacks belong in the existing private route config, outside the plugin.
One route is sufficient; no worker catalog or subscription calendar is required.
Native Codex workers keep their existing collaboration tools;
do not wrap them in this CLI, switch the main model, or treat one route's failure as
authorization to launch another. An ACP worker is a separate agent session, not a
native Codex child or a new user-visible Codex task.

Use the same complete responsibility, minimal sufficient work order, engineering
constraints, same-worker rework, and coordinator acceptance rules as worker-routing.
An external worker may not delegate again. Inspect the real diff and evidence before
accepting its result; `runtime_status=completed` is not engineering acceptance.

## Availability and authorization

Use only an operator-registered canonical integration entrypoint and config path.
The executable is `integrations/acpx/src/cli.mjs` in the canonical source checkout,
or its locally installed `cwr-acp` bin. Do not infer this path from the plugin cache.
Read `docs/acp-integration.md` in that checkout for installation and limits.

The optional runtime must already be installed and its local ACP fixture tests must
have passed. Do not install packages, import private main-session instructions,
reuse personal agent profiles, copy credentials, change enabled routes, or authorize
new data transfer just to make this skill available. Report the specific missing
prerequisite and keep the existing native route available.

## Commands

Use the trusted, operator-supplied paths in place of ENTRY and CONFIG:

```sh
node ENTRY run --config CONFIG --cwd WORKSPACE --file ORDER --title TITLE --category implementation
node ENTRY continue --config CONFIG --session UUID --file INCREMENT
node ENTRY continue --config CONFIG --session UUID --file REWORK --revision-reason REASON
node ENTRY status --config CONFIG --session UUID
node ENTRY cancel --config CONFIG --session UUID
node ENTRY pending --config CONFIG
node ENTRY close --config CONFIG --session UUID
```

`run` creates an independent responsibility. Keep its returned integration UUID.
Omit `--route` when CONFIG has `routing.default`; the same call reads the current
default and optional `routing.fallbacks`. Add `--route NAME` only for an explicit
task/operator choice or an authorized recovery, not a remembered old default.
Legacy configs without routing still require that flag. An explicit route never
automatically falls back. Use `docs/acp-integration.md` for the small config example.
`continue` resumes that exact conversation; it cannot silently create a fresh one.
`--permissions` selects this integration's ACP permission-response policy, not a
filesystem boundary. The default `read` answers requests with approve-reads plus
non-interactive denial; `full` uses approve-all, which answers ACP permission
requests including execution and network requests. Both cover only requests that
actually reach the adapter's permission flow: an adapter can expose operations that
never raise one, so never claim `read` prevents writes or describe the policy as an
OS sandbox. Deterministic filesystem read-only behavior needs a host/OS sandbox or
a disposable read-only environment configured independently of this integration;
cwr-acp does not provide that boundary. `full` additionally requires a route that
permits full mode and current task authorization, and its authority still comes
from the work order and the current task.

Only the small work order is intentionally handed over. Registered environments,
agent homes and shared repository rules still require real input-boundary review.
Use a separate worktree or coordinate non-overlapping writers explicitly. The
integration's workspace lock cannot see native workers, other installations,
ports, databases, services, or external shared resources.

## Wait, cancel, continue, accept

Automatic fallback is limited to configured alternatives during preflight, before
any adapter launch, for a missing/unlaunchable entry or missing required environment
credential. It does not widen workspace or permissions, override a disabled route,
or retry dependency, initialization, prompt, stream or cleanup failures. Check the
returned selection evidence if a route was skipped; do not repeat the failed default
for another responsibility in the same task while the cause is unchanged. If no
alternative is authorized, use the main thread when the task allows direct work.

After startup, use the original receipt/status and cleanup evidence before recovery.
Only confirmed stopped work may move to a preauthorized alternative; inspect existing
artifacts and hand over the remainder, never replay an ambiguous write order. Do not
infer quota expiry, HTTP status or retry timing from generic runtime errors. A failed
test or missed requirement normally continues the same worker for correction.

Changing `routing.default` or its fallback order does not migrate an existing session.
To revoke a channel, set its existing route's `enabled` to false under the user's
authorization as well as selecting the new default; subsequent runs and continuations
on that channel are denied. Status/cancel/close remain available for safe recovery.
Do not disable a still-authorized old route merely because a new default was selected.

The CLI blocks until its turn result and owned-connection cleanup. Use the host's
normal shell execution/wait semantics. Do not short-poll a healthy worker, restart
it because the shell tool yielded, or promise an automatic background wakeup.

`cancel` only acknowledges a cancellation request. Wait for the running command's
terminal result and cleanup before taking over. A lost reply is ambiguous: use
`status` and the recorded receipt before considering a retry. Keep unconfirmed
cleanup/stale locks for explicit reconciliation; never auto-delete them.

The CLI prints a bounded output excerpt plus an evidence pointer. Detailed tool
and conversation state stays in the private local acpx store. Missing usage stays
unknown. Advertised model/usage fields are adapter reports, not billing evidence or
proof of provider identity. Continue the same session for authorized implementation
and rework. Close the responsibility after acceptance; closing does not delete history.

## Natural collaboration records

Dispatch statistics are LIGHT and OBSERVATIONAL. The runtime facts (turns, receipts,
runtime status, usage) are derived automatically; do NORMAL `run`/`continue`/`close`
without any bookkeeping. Ordinary completion or close needs no annotation and is not an
outstanding review obligation. Do not add a `submitted`/`accepted`/`record`/`pending`
step after every worker, and do not fill in history for completeness. Give a new
responsibility a short task title and one category on the original `run`
(investigation, implementation, review, other); that is metadata, not a reporting step.

Two optional, genuinely useful moments:

- **A real correction worth recording**: when you actually send rework, you may pass the
  reason with the continuation itself:
  `node ENTRY continue --config CONFIG --session UUID --file REWORK --revision-reason
  REASON` (one of requirement_missed, validation_failed, scope_changed,
  constraint_added, environment_blocked, uncertain). This is a shortcut, not required
  for ordinary continuation, and a plain `continue` never records a revision. If the
  annotation cannot be written, the authorized task still runs exactly once and the
  interruption is reported through the existing additive warning; never rerun the
  worker to repair telemetry.
- **A specific task that needs retained review evidence**: use
  `node ENTRY record --config CONFIG --session UUID --file EVENT_JSON` deliberately for
  a submission for review, an explicit acceptance or takeover, or a note you want kept.
  This is optional and not part of the ordinary flow. Do not infer acceptance from
  runtime completion, classify provider text automatically, or backfill old decisions
  from memory. A plain `note` records an observation and never invents a review.

The projection derives one `review_state` per responsibility and a `summary.review`
count per state (accepted, taken_over, awaiting_review, changes_requested,
needs_attention, no_receipt, not_requested, legacy_untracked). `not_requested` is the
ordinary default; `awaiting_review` requires an explicit `submitted` event; legacy
bindings with no tracking and no explicit review event stay `legacy_untracked`, quietly
historical and never pending work. When you actually want to check what still needs a
look, run `node ENTRY pending --config CONFIG`: it is read-only, loads no adapter,
excludes legacy history and ordinary work with no explicit outstanding request, and prints safe ids, state, status and
title only. It is an on-demand view, not a backlog you must clear.

The `record` input uses schema `cwr.dispatch.event/1`, a new UUID `event_id` per action,
the existing `session_id`, and `kind`: submitted, revision_requested, accepted,
taken_over, or note. Keep this small JSON outside Git; do not put raw work orders or
transcripts in it. `summary` is optional. Revision/takeover requires one reason:
requirement_missed, validation_failed, scope_changed, constraint_added,
environment_blocked, uncertain. Only claim checks actually performed. Optional evidence
entries are `{source: coordinator|worker, kind: diff|test|manual|other, summary: text}`;
worker claims keep their own source. An optional request_id must name an existing
receipt.

Keep the same event_id when retrying an uncertain write. Correct a mistaken label with a
new event_id and `supersedes` pointing to the latest event in its chain; never rewrite
the original file. When retained review evidence matters, a real coordinator takeover
can be recorded explicitly. Read `docs/dispatch-data.md` in the canonical checkout for
the full contract.

Use `stats --config CONFIG --since 7d` for local totals, `pending --config CONFIG` only
when you want to check for actionable review records, and `dashboard --config CONFIG`
when asked for the visual overview. None invokes a model or reads account quota. Only
the dashboard's aggregate export is prepared for sharing; stats JSON, pending and detail
contain local identifiers and task information. No automatic upload, A/B workload or
quota-savings percentage is part of this flow.
