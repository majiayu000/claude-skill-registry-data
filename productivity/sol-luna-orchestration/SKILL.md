---
name: sol-luna-orchestration
description: Coordinate substantive software work with a configurable Astra or Sol root and verified advanced and Luna executors. Covers durable assignments, isolated writer worktrees, candidate review, validated delivery, and human-confirmed Ultra takeovers. Invoke it before planning, delegating, coordinating, or validating independent work.
---

# Astra-Luna orchestration

The technical skill name, launchers, managed markers, and state namespaces retain their historical identifiers. The advanced capacity key `sol` counts Astra and Sol runs in the same four-slot pool. Astra is the default, and Sol is an explicit operator choice, never a fallback.

Read `models` in `$CODEX_HOME/sol-luna-orchestration/config.json`. `advanced` defaults to `astra@latest` and also accepts `sol@latest`; `economy` defaults to `luna@latest`. An exact stable model id pins a release. Optional `efforts` entries override named roles; takeover remains `ultra`. The launcher resolves project-owned aliases through the runtime catalog, picks the newest visible stable numeric release in that family, and checks capabilities. Missing effort or Fast support blocks execution rather than selecting an older or different model. Unknown naming conventions need an explicit code update; do not guess their release order.

Run `npm run models` for read-only route discovery, or `npm run root -- --cwd <repository>` to start a configured root. Neither JSON edits nor installation change a running session. Native Codex and desktop sessions use their selected settings or the last installed global defaults; confirm actual metadata. Do not send project aliases directly to Codex.

New assignments persist their resolved `model_route`. Queued work and retries retain that route, but every attempt must produce fresh verification evidence. A legacy assignment without a pinned route cannot resume automatically: retain its evidence and explicitly create replacement work. Never edit stored assignments to upgrade models.

Use this workflow once, before the first substantive request in a root task. Do not run it inside a session whose developer instructions contain `CODEX_ORCHESTRATION_ROLE=executor`. A session marked `CODEX_ORCHESTRATION_ROLE=ultra-orchestrator` already owns the takeover workflow and must not acquire another lock.

## Workflow

1. Confirm that the root uses the configured advanced model and effort, the Standard service tier, and `model_verbosity = "low"`. The defaults are `astra@latest` and `high`.
2. Define the outcome, acceptance criteria, risks, ownership boundaries, and final verification.
3. Keep planning, integration, tightly coupled work, and sensitive decisions in the root.
4. Delegate only independent scopes when parallelism or lower context cost materially helps. Capacity is not a fan-out target.
5. Select exactly one verified profile and create a bounded assignment contract: base revision, allowed and forbidden write roots, required checks, artifacts, review policy, operator approval gate, and a resolved `manual`, `commit`, or `push` delivery policy.
6. Send the briefing through the canonical Node launcher. Writer profiles require at least one `--write-root` and run inside an isolated worktree while retaining `workspace-write` sandbox enforcement.
7. Use durable assignment state and the residual planner to resume queued work. Never overlap active write roots.
8. Accept a result only when App Server settings and rollout turn metadata agree, `routing_verified` is true, and the reported changed files match the candidate Git tree.
9. Claim and review the exact immutable candidate, obtain required approvals, integrate it into the root checkout, complete its declared delivery, acknowledge it, and clean its worktree.

## Fast path for Git operations

Rebases, merges, cherry-picks, reverts, and conflict resolution stay with the root. Loading this skill does not mean they must be delegated. Before changing history, the root checks the current checkout, working tree, linked worktrees, upstream, and refs. It then fetches the latest remote refs and runs the Git operation in a state that can still be aborted or recovered. Only the conflicts Git actually reports should drive the resolution.

Do not send `explore` off to scan the commit history and guess what might conflict. If Git stops on a real conflict, the root may ask `explore` one focused question about the intent behind those specific files. The root still makes the edit. If that run stalls or fails, do not repeat the same request; work from the conflict Git has already exposed.

Stop and ask the operator when the checkout is dirty, another Git operation is already in progress, or the target branch is checked out in another worktree. This does not change who may push or force-push.

## Profiles

| Profile | Model | Effort | Tier | Sandbox | Workspace | Purpose |
|---|---|---|---|---|---|---|
| `explore` | Luna | `max` | Fast | `read-only` | Shared checkout | Broad discovery and contract tracing |
| `implement-lite` | Luna | `max` | Fast | `workspace-write` | Isolated worktree | Small, explicit, low-risk edits |
| `playwright` | Luna | `max` | Standard | `read-only` | Shared checkout | Browser inspection and authorized test interaction through Playwright MCP |
| `implement` | Advanced | `medium` | Standard | `workspace-write` | Isolated worktree | Bounded implementation requiring stronger judgment |
| `review` | Advanced | `high` | Standard | `read-only` | Exact candidate worktree when `--candidate-id` is used | Independent plan or Git-change review |

The table shows default efforts. All roles use low output verbosity. Fast profiles force `features.fast_mode = true`; Standard roles force it to `false`. Model and effort come from the operator's configuration; tier and sandbox remain fixed by the profile. Executors cannot override them through CLI flags.

Root and planner default to Astra/high. Implementation defaults to medium; independent review defaults to high and does not acquire root planning or approval authority. Choosing Sol does not imply equivalent quality at the same effort. Escalation returns to the root rather than silently increasing effort or starting another session. Ultra requires explicit human authorization and runtime-advertised support.

Once `turn/start` succeeds, `explore` gets 120 seconds to report `item/*` progress for the active thread. Matching events reset this idle timer without extending the overall timeout. All profiles default to a 900-second overall timeout, configurable through `--timeout-seconds`; only `explore` has the additional idle timer.

The launcher requires Codex CLI 0.147.0 or a later compatible version and uses the experimental Codex App Server over local stdio JSON-RPC. It deliberately has no fallback to the legacy execution path. App Server protocol `priority` maps to public `fast`, and protocol `default` maps to public `standard`.

## Platform verification

Windows uses a junction for the global skill. Linux and macOS use directory symlinks. Treat portability as two separate gates:

```text
npm run verify:platform
npm run verify:live
```

`verify:platform` is the required authentication-free gate on Windows, Linux, and macOS. It verifies Codex CLI compatibility, strict configuration, generated App Server schemas, the current process fingerprint, an idempotent isolated global installation, the native link type and canonical target, temporary cleanup, and unchanged Git state.

`verify:live` is a manual authenticated gate. It verifies root, every executor profile, Playwright, Ultra, locks, recovery, isolation, capacity, and unchanged repository state. Mark a platform as live verified only after its self-hosted `codex-live` artifact succeeds. A sandbox failure keeps the platform pending and never justifies a bypass or weaker sandbox.

Root acceptance reads effective global defaults through `config/read` without model or effort overrides in a temporary repository before negotiating a turn. All writer probes explicitly use manual delivery. Keep evidence outside the repository and preserve its implementation diff. Pause consumers and finish existing assignments before installing a model migration; never convert pending work or restore old durable state to roll back defaults.

## Launcher

The canonical interface reads the briefing from stdin. Replace the placeholders with the chosen profile, repository, sandbox, and assignment options:

```text
node .agents/skills/sol-luna-orchestration/scripts/invoke-profile-executor.mjs --profile <profile> --cwd <repository> --sandbox <mode> --timeout-seconds 900 [assignment options]
```

For example, this read-only briefing works in PowerShell and Bash from the repository checkout:

```text
echo "Find where executor profiles are defined. Report paths without changing files." | node .agents/skills/sol-luna-orchestration/scripts/invoke-profile-executor.mjs --profile explore --cwd . --sandbox read-only
```

Use the profile table above to select the route. Writers must explicitly pass `--sandbox workspace-write` and at least one `--write-root`; read-only profiles must not request workspace write.

`npm run executor` remains a convenience entry point. Use the direct command for exact option forwarding and exit codes. Code `0` means completed with verified routing, `1` means blocked or failed, and `2` means invocation, capacity, timeout, configuration, contract, MCP, or routing verification failed.

The default control plane and result format are both v2. Use `--enqueue-only` to persist work without starting it, then resume the stored contract with `--assignment-id <id>`. Repeat `--write-root`, `--forbid-root`, `--check-json`, and `--artifact-json` as needed. Add `--review-policy independent`, `--require-operator-approval`, or `--candidate-id <id>` only when the assignment needs those gates.

New writer assignments read their automatic-delivery default from `$CODEX_HOME/sol-luna-orchestration/config.json`. Set `automatic_delivery` to `false` to opt out globally. When enabled, the controller commits the validated candidate and also selects push if the checked-out branch has a matching configured upstream.

For one new assignment, override the configuration with `--delivery manual`, `--delivery commit --commit-message <message>`, or `--delivery push --commit-message <message> --push-remote <configured-name> --push-branch <existing-branch>`. Read-only profiles and resumed assignments do not resolve the setting again.

The launcher writes a colored route banner to stderr when the terminal supports color and reserves stdout for one JSON result. It respects `NO_COLOR`, `TERM=dumb`, and `FORCE_COLOR`.

Read [the assignment schema](references/assignment-request.schema.json) when constructing a durable contract, [the executor task schema](references/executor-result.schema.json) when changing model-facing output, and [the v2 envelope schema](references/executor-result-v2.schema.json) when consuming controller results.

## Durable assignments and candidates

Assignment records and sanitized action events live outside the repository under Codex state. Every mutation carries an action id, expected state revision, and authority. Replays with the same action are idempotent; stale revisions, reused action ids with changed content, stale Ultra generations, and overlapping writer leases fail closed.

Writer worktrees complement the sandbox; they do not replace it. Keep repository edits within the assigned paths in the isolated worktree. The controller checks those paths, symlink and submodule capabilities, required checks, and artifact boundaries before creating an immutable candidate commit. The executor never stages or commits, and only root or Ultra may integrate the candidate.

Manual delivery leaves the integration unstaged. Commit delivery uses a temporary index containing only the candidate paths and preserves unrelated staged and working changes. Push delivery uses the remote and branch stored in the assignment, requires the delivery parent to exist remotely, verifies ancestry, and performs a normal noninteractive push without force. It never publishes unrelated local parent commits. There is no fallback to a shared writable checkout.

Controller commits use deterministic Git plumbing and do not run commit hooks or create signed commits. Express mandatory validation as required checks, and use manual delivery when repository policy requires hooks or signing.

Use the control CLI to inspect residual work and perform explicit transitions:

```text
npm run control -- status --cwd <repository>
npm run control -- next --cwd <repository>
npm run control -- reconcile --cwd <repository>
npm run control -- claim --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- request-review --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- approve --cwd <repository> --assignment-id <id> --revision <n> --kind root
npm run control -- integrate --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- commit-delivery --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- push-delivery --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- retry-delivery --cwd <repository> --assignment-id <id> --revision <n>
npm run control -- ack --cwd <repository> --assignment-id <id> --revision <n>
```

Mutations require the exact current revision. `reconcile` resumes pending commit, push, acknowledgment, and cleanup steps under the stored delivery policy. A Git delivery failure records a sanitized error and enters `delivery_blocked`. It waits for an explicit `retry-delivery` rather than retrying the failing push in a loop.

Independent review runs `review` against `--candidate-id <id>` and publishes a verdict bound to that candidate revision. Operator questions, approvals, and delivery retries remain explicit dashboard or CLI actions. The controller never invents an answer.

The optional dashboard binds only to loopback, uses a one-time URL token, an HttpOnly session cookie, origin and CSRF checks, and exposes only the redacted status projection plus operator answer/approval actions:

```text
npm run dashboard -- --cwd <repository>
npm run simulate -- --iterations 1000 --seed 73
```

The simulator is pure and deterministic: it mutates neither Git nor durable state and exercises successful, blocked/retry, recovery, review, approval, stale-action, stale-candidate, and unauthorized-action paths.

## Capacity

- Luna profiles share a hard limit of 10 active executors per repository and 10 across the PC.
- Advanced profiles share a hard limit of 4 active executors per repository and 4 across the PC, across both Astra and Sol releases.
- The machine-wide aggregate limit is 14 executors.
- Playwright has an additional machine-wide limit of 2 and consumes Luna capacity.
- Root and Ultra processes do not consume executor slots. Executors delegated by Ultra do.
- Executor capacity acquisition is atomic and fails immediately. Durable assignments may remain queued until the residual planner can start them without an overlapping resource lease.
- Mutations may prune a dead lease only after revalidating every registered process identity and both capacity reservations. Pending finalization receipts keep their slots. Corrupt or unknown state fails closed.

Inspect repository and machine utilization with:

```text
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs status --cwd <repository>
```

`status` is a read-only snapshot, not a cleanup command. It reports the capture time, persisted capacity, potentially orphaned runs, and pending finalizations without initializing a namespace or changing metadata, leases, or history. Process inspection and history reads happen outside the coordination mutexes. Missing retained history makes the snapshot incomplete; it never authorizes a state change.

Executors save a hashed receipt before closing their leases. A coordination failure returns code `2` while preserving the verified routing metadata. Do not rerun the model, start a new assignment attempt, or archive its worktree to work around that failure. Recover explicitly:

```text
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs finalize --cwd <repository> --run-id <id>
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs finalize --cwd <repository> --run-id <id> --expected-revision <n>
```

The second form is required for assignments. Use the revision bound to the receipt, shown in `pending_finalizations`. Recovery checks receipt integrity, process-start fingerprints, ownership, fencing, the assignment attempt and revision, and writer content and artifacts. It stops after publishing the result; approval, integration, delivery, and acknowledgment remain separate. Live or unknown identities block recovery. Ultra receipts require the same active, authorized epoch; recovery-required and superseded epochs remain blocked. No model rerun, automatic finalization retry, or Ultra recovery occurs. Receipts and confirmations are retained without automatic deletion.

## Profile contracts

`explore` never changes files. It returns conclusions, `path:line` evidence, contracts, risks, and open questions. It blocks and escalates when the work requires architecture, security, concurrency, distributed-invariant, or contradictory-contract decisions.

`implement-lite` owns only a small, explicit, low-risk change. It blocks and recommends `implement` when the scope expands or judgment becomes cross-cutting.

`implement` owns only the assigned files or subsystem, makes the smallest complete change in its isolated worktree, and never self-approves, stages, commits, changes HEAD, or pushes. The controller runs declared checks, publishes the candidate, and alone performs the resolved delivery after all gates pass.

`review` returns `APPROVE` or `COMMENT` with completed status, or `REQUEST_CHANGES` with blocked status and at least one blocker. It never changes files.

`playwright` uses the private stdio server `sol_luna_playwright`, pinned to `@playwright/mcp@0.0.80`. No global Playwright entry is required. The installer preserves existing MCP configuration; a collision with the reserved internal name fails closed.

The launcher replaces the private server's complete runtime configuration and verifies it through `config/read`. It disables the user's `playwright` server only in this executor process, retains `default_tools_approval_mode="approve"` for authorized browser actions, and disables `browser_run_code_unsafe`. It removes inherited `PLAYWRIGHT_MCP_*` variables from the child environment and creates writable, isolated browser-temp and artifact directories with `--isolated` and `--output-dir`.

Before `turn/start`, effective configuration must pin package `0.0.80`, and thread-scoped MCP inventory must report its bundled runtime version `1.63.0-alpha-2026-08-31` and the required browser tools within 30 seconds and the overall timeout. Package and runtime versions are separate checks; either mismatch fails closed. Evidence must come from a successful, completed `mcpToolCall` on the private server in the active thread and turn. Mentions, started calls, and failed results do not count. Validate probe evidence before cleanup; report cleanup failures. Update both expected versions explicitly and pass offline and live checks, never use `@latest` or a fallback.

Executor turns use App Server approval policy `never`. Command and file approvals, permission grants, and MCP elicitations fail closed with protocol-valid responses. Non-blocking user-input requests receive an empty answer. Blocking, non-sensitive questions become durable operator requests whose acknowledged answers are carried into a retry; sensitive answers are never persisted.

Full interaction is allowed only on localhost and explicitly named development or test environments. External sites are observation-only unless the briefing authorizes a named state-changing action and destination. Purchases, deletion, publishing, messaging, account or security changes, production mutation, and `browser_run_code_unsafe` are prohibited.

## Exclusive Ultra takeover

Use the configured advanced model at `ultra` on Standard only when a named architecture, security, concurrency, distributed-invariant, or contradictory-contract decision cannot be resolved responsibly by the root. The human must provide a reason and `--confirm-exclusive-takeover`.

```text
node .agents/skills/sol-luna-orchestration/scripts/invoke-sol-ultra.mjs --cwd <repository> --reason <reason> --confirm-exclusive-takeover --sandbox read-only
```

Send the authorized briefing through stdin. Workspace writing requires an explicit `--sandbox workspace-write`. Ultra temporarily replaces the root, disables native multi-agent execution, and delegates only through verified profiles. Its executors inherit the exact `CODEX_ORCHESTRATION_LOCK_ID` and monotonic `CODEX_ORCHESTRATION_GENERATION`. They consume the normal capacity pools and never overlap write roots.

New Ultra-owned writer assignments inherit the operator-controlled automatic-delivery setting. An explicit user boundary against commits or pushes takes precedence and requires `--delivery manual`. Durable executor output uses the v2 envelope; the Ultra result includes its integer `generation`.

A verified terminal result releases the lock. Timeout, interruption, process failure, invalid output, or routing failure leaves it in `recovery-required`. State v2 registers the Ultra launcher and App Server, plus every executor launcher and App Server, with a portable process-start fingerprint.

Recover only with the exact lock id and only after every registered identity is confirmed `dead` or `reused`. A live or `unknown` identity fails closed, and recovery never kills it:

```text
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs status --cwd <repository>
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs history --cwd <repository> --limit 50
node .agents/skills/sol-luna-orchestration/scripts/orchestration-gate.mjs recover --cwd <repository> --lock-id <exact-lock-id>
```

Active version 1 state remains `legacy-unfenced` and is never converted silently. After its owners stop, recovery also requires `--confirm-legacy-recovery`; a v1-only repository then starts v2 at generation 1. History is immutable and sanitized. Retention targets 1,000 events while protecting the active generation, but history does not determine lock ownership.

## Guardrails

- Do not use native `spawn_agent` or custom agent TOML for profile routing.
- Do not alter approval policy, request `danger-full-access`, or use bypasses.
- Do not let executors re-delegate, alter orchestration policy, stage, commit, change HEAD, push, or own overlapping files concurrently.
- Keep `explore`, `playwright`, and `review` read-only. Require explicit workspace write for both implementation profiles.
- Do not infer model, effort, or tier from configuration or executor prose. Require matching `thread/settings/updated` model, effort, and tier plus rollout `turn_context` model and effort.
- Do not manually edit or delete orchestration state.
- Treat hooks as defense in depth, not complete enforcement across every tool path.
- Do not add TTLs, heartbeats, automatic recovery, shared-checkout write fallbacks, dependency fallbacks, or `shell: true`.
- Disclose that unregistered descendants cannot be identified portably and that fencing cannot atomically cancel an arbitrary workspace mutation already in progress.

## Completion criteria

A root task is complete only when every applicable condition below is met:

- Every used profile has verified routing.
- Every accepted candidate has the required review and approvals.
- Integration is conflict-free and the declared delivery is complete.
- Relevant checks and platform verification pass.
- Durable assignments are acknowledged and their worktrees are cleaned or explicitly archived.
- Playwright use is verified when requested.
- Every Ultra generation is released or reported as `recovery-required`.
- Any unresolved portability, descendant-registration, or sandbox limitation is disclosed.
