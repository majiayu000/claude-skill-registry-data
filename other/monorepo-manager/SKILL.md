---
name: monorepo-manager
description: Use when Nour says manager, manage the repo, run the backlog, continue the job, stay on it or get it all done, asks what is going on with the jobs or sessions that are running, when a job touches more than one lane (nickstire server or client, statenour, worker, platform, research), when several sessions or lane agents run at once and their results must be checked before Nour hears them, or before an overnight or unattended run. Splits and dispatches the work, pre-clears protected steps, checks every return and every relayed claim, integrates, merges through the gate and keeps the job ledger. Not for a one-area task even when phrased "get it all done" (do it directly, under nour-command), one PR's merge or CI state (merge-gate.mjs and answer-first), whether a merged PR is live (deploy-not-live, production-health-report), a stranded branch or stale worktrees (stranded-branch-rescue), deep research (Perplexity in Chrome), or reviewing a finished session (session-observer).
triggers: manager, manage the repo, run the backlog, continue the job, stay on it, get it all done, more than one lane, dispatch lanes, sessions, relay, overnight, before I wake, job ledger, heartbeat jobs, integrate lanes, verify every diff
---

# Monorepo manager (v4, 2026-10-30)

You coordinate so Nour does less: lane agents and sessions edit; you write only the job's ledger row (step 17). One area needs
no manager (a multi-agent run costs about 15 times a chat: [benchmark](references/benchmark-2026-10-22.md) B5); `nour-command`
sets how hard to work, this skill who does what. Defects behind the steps: [references/replay-2026-10-15.md](references/replay-2026-10-15.md),
[references/replay-2026-10-22.md](references/replay-2026-10-22.md), `evals/baseline.md` (v4). Skills per step: [references/skill-map.md](references/skill-map.md);
subagent rules: [references/subagent-policy.md](references/subagent-policy.md). Each rule names its enforcer or says advisory.

## Job start: know Nour, the shop and the money (first turn of a job or after a compaction; advisory)

Read in order: `.agents/core/USER.md` (who he is, the four protected classes, shop data meanings), `.agents/core/SOUL.md`,
`apps/nickstire/docs/SHOP-SOUL.md`, `apps/nickstire/shared/business.ts` (facts, never copied), `docs/agent-os/NOUR-RUNTIME-KERNEL.md`
(the money list), then the memory index and the area's RESUME HERE file. Write the job's money frame in one line: what it
moves (cars, calls, tire and repair sales, recovered declined work, repeat customers, reviews, hours back to Nour) and the read
that will show it. Why and what each file gives: [references/know-nour-and-the-shop.md](references/know-nour-and-the-shop.md).

## Every turn (the turn contract; details and the relay check: [references/relay.md](references/relay.md))

1. A SessionStart `[health] ... FIX FIRST:` line is the first task: run the fix, or end with `Health: not fixed, because ...`.
2. Skill calls in the first batch; the `Skills:` line names only skills called THIS turn (earlier ones: `used earlier:`).
3. CI state = the `gh pr checks <n>` tally read this turn; "live" = a production read this turn. Merge is not deploy.
4. Nothing a session or lane said reaches Nour unchecked: run the relay check (step 8) or label it as their claim.
5. Ask Nour only about the four protected classes in USER.md (and `AGENTS.md` protected operations); a step inside his order is done, then reported.
6. A decision he defers ("leave it for later", "remind me") goes to the takeover file's parked register (format in the pipeline reference).
Rows 1-3: Stop hooks `scripts/agent-os/health-first.mjs` and `scripts/agent-os/skills-check.mjs` (sent back once). Rows 4-6: advisory.

## Modes (say which one you are in)

| Mode | Use when | Allowed effects |
|---|---|---|
| Observe | heartbeat follow-up, "what's going on" | reads only; findings become proposals |
| Plan | new job | reads; a plan in chat with two alternatives, the 10x option and kill criteria (step 2); no ledger row yet |
| Execute | Nour authorized the job | lane worktrees or sessions, one integration branch and PR, a ledger row |
| Recover | "continue", interrupted job, after a reboot or compaction | reads first; reconcile, then Execute |
| Dry run | testing the manager | chat output only; never the real ledger, never a PR |
| Cancel | "stop" / "cancel" | stop dispatching, mark the row CANCELLED, ignore late results for that job |

## Workers

| Lane | Agent | Owns | As a session (`start_session`) |
|---|---|---|---|
| nickstire server | `lane-nickstire-server` | `apps/nickstire/{server,drizzle,shared,scripts}/**` | branch `nickstire/<task>` |
| nickstire client | `lane-nickstire-client` | `apps/nickstire/client/**` | branch `nickstire/<task>` |
| statenour | `lane-statenour` | `apps/statenour/**` | branch `statenour/<task>` |
| worker | `lane-worker` | `apps/worker/**` | branch `chore/<task>` |
| platform | `lane-platform` | `.github`, `scripts`, `config`, `packages`, `.claude`, `.agents`, `docs/agent-os`, root configs, lockfile | branch `chore/<task>` or `docs/<task>` |
| research | `lane-research` | nothing: read-only answers, journey maps, Langfuse reads | read-only; `docs/<task>` if it writes a doc |

A lane agent suits a bounded diff you read back; a session suits work Nour may watch or steer, or that outlives this context.
When lane agents are missing (the harness says not available), dispatch the same brief with `start_session`. Same brief, same checks.
Writers at once: 2; heavy builds or full suites: 1, through `node scripts/agent-os/heavy.mjs run --` (enforced: 1,500 MB free).

## Session pipeline (every session you start, in order; detail: [references/session-pipeline.md](references/session-pipeline.md); example: [references/worked-example-2026-10-30.md](references/worked-example-2026-10-30.md))

1. Brief: step 6, and every brief carries the lines LOOP RULE, STANDARD and SIBLINGS from the reference. Rule `session-dispatch-brief` (advisory for the three lines).
2. RAM gate, read `node scripts/agent-os/heavy.mjs status` before every start (a session is budgeted 1,500 MB over a 500 MB floor):
   under 2,000 MB start nothing (under 500 MB also stop this job's least important idle session); 2,000 to 2,999 MB docs-only or read-only sessions only; 3,000 MB and up a writer session may start too.
   Machine-wide cap: 10 running sessions, other managers' included (`list_sessions` unfiltered). Advisory; `heavy.mjs` gates runs only.
3. Queue: a brief the gate blocks is written now and listed as QUEUED in the takeover file; start it the moment a slot frees.
4. Start: `start_session` with `model`, `effort` and `permission_mode` set, the brief file in `prompt`, tier named in your intro
   line. It caps both at YOUR level, so run the manager at the highest tier the job needs. Rule `session-dispatch-brief`.
5. Sweep: under your own `/loop`, sweep every 600 to 900 s: free RAM, `gh pr checks` per open PR, per session minutes since its last commit,
   dirty count and last events (`list_events`). 45 minutes without a commit: one check-in; third silent sweep: replace (B9). Advisory.
6. Digest: every ruling from Nour goes to every running session of the job in the same tick, verbatim, with what it changes;
   every finished doc becomes a 3-5 line digest for the still-running sessions (verdict, numbers to reuse, file to cite). Advisory.
7. Check: step 7. A thin doc, an unlabelled number, a placeholder or a "not found" with no search receipt:
   send it back once with the exact gap; a second miss on the same gap gets a higher tier or a replacement. Lanes: `subagent-receipt-check.mjs`; sessions: advisory.
8. Close out, in order, after merge (steps 12-17): takeover memory, `archive_session`, one line per finished piece to Nour;
   never while its PR is open or its worktree holds uncommitted work. Advisory (the tool wants his agreement: his 2026-10-30 order covers his jobs).

## Procedure (Execute)

1. **Recover state.** Read EVERY ledger row whose status is not MERGED/CANCELLED, plus the last 5:
   `node scripts/agent-os/ledger-render.mjs --open --tail 5`; run `node scripts/agent-os/ledger-check.mjs`, `gh pr list --state open`, `node scripts/agent-os/repo-status.mjs`,
   `list_sessions`, the takeover file and its parked register. A MERGED PR under an open row is stale: fix it in your PR. A matching open job resumes; never a duplicate. Pasted plan? `plan-gate` first.
2. **Spec.** Fill `.agents/core/templates/task-spec.md` with the base SHA; KNOWN lists facts and guesses apart (B8). One area = no
   manager; most jobs 1-3 workers (B2). A design choice gets two alternatives that differ in kind, the 10x option, kill criteria,
   the money frame and the benchmarked mechanism ([references/sessions-and-plans.md](references/sessions-and-plans.md)).
3. **Pre-clear.** Before an unattended stretch, ask in one message for a go on each SPECIFIC protected action the job can hit; you perform a cleared
   action yourself (a session never acts on a relayed go); each yes verbatim in the takeover file; the uncleared park with a one-liner (B11).
4. **Split.** Name each lane and its exact paths. Overlapping paths or a shared contract (endpoint, type, env var,
   `packages/*`) means ORDER: the contract owner lands first, consumers get the agreed version in their brief.
5. **Claim.** `node scripts/agent-os/agent-start.mjs --branch <integration-branch> --claimed-by "<job id>"`; only a line starting
   `[agent-start] leased` is a receipt (it exits 0 without one). No receipt = no writers; read-only work continues; tell Nour. Check open PRs and sibling worktrees first.
6. **Dispatch.** One brief file ending `brief.md` per worker from `.agents/core/templates/subagent-brief.md`, every field filled,
   Nour's verbatim words and memory files by path, `SHOP DATA:` if it reads shop data, sibling files to cite. Run `node scripts/agent-os/skill-recall.mjs --file <brief>` and put its matches in SKILLS TO INVOKE FIRST.
   `model` and `effort` from MODEL / EFFORT on every lane and session (rules `lane-dispatch-brief`, `session-dispatch-brief`, `brief-shop-data` deny a miss); background, no polling; one decision per message; dispatch time (UTC) in your notes ([references/job-lessons.md](references/job-lessons.md)).
7. **Check every return.** Read the real diff; `node <your checkout>/scripts/agent-os/check-lane-paths.mjs --lane <lane> --base <sha>`
   (exit 1 reject, exit 2 not checked); re-run one receipt yourself; every RETURN fact labelled FACT, INFERRED or NOT CHECKED.
   A failed or BLOCKED worker is re-dispatched only with a change: more context, a higher tier, a smaller task or a ruling (B18).
8. **Relay.** Before Nour hears a worker's claim, classify it (shop or money, an absolute, a state, a plan), check it against
   USER.md's shop data meanings, memory and the source, forward the receipt verbatim with its source, label what you could not
   check ([references/relay.md](references/relay.md)); a wrong shop fact: correct the worker and fix the brief gap in the same turn.
9. **Probe it yourself.** Any guard, gate, hook, validator or parser: your OWN probes against the REAL binary, every numeric cap at
   cap-1, cap, cap+1 and bad-item-last, plus `guard-red-team`; send each bypass back as the exact input ([references/verify.md](references/verify.md)).
10. **Check the names.** Any list a rule relies on (tool names, permission rules, env vars, rule ids, file or skill names) is
    resolved entry by entry against the live source, never by its author: tool names via your own `ToolSearch select:`.
11. **Read the primary source.** A decision-critical external fact gets a short quote YOU read on the primary page, with URL and
    date, labelled FACT, STRONG INFERENCE or CLAIM. An agent's "not documented" is a CLAIM until you search the page.
12. **Review before the PR opens.** Lenses find, skeptics refute (`.claude/workflows/adversarial-review.js` with Nour's opt-in, else `lane-research` 2 at a time);
    `receiving-code-review` per Codex round; `differential-review` for auth, payments, guards, customer data; two red rounds on one finding: one tier up (B20) ([references/review-and-merge.md](references/review-and-merge.md)).
13. **Integrate.** One integration branch and PR per coherent job, lane commits cherry-picked onto current origin/main; gates run ON THE COMBINED TREE. A skill job runs `skill-forge`'s
    `check <dir> --git` (`--existing --git` for an existing skill). Push from the tip's checkout or a hook-free clone, never
    `--no-verify`. Protected operations not pre-cleared stop here with the exact one-liner.
14. **Consumer check.** Anything that enforces: prove the real consumer applies it in a FRESH session (`assert-the-consumer`).
    Hooks load from the PRIMARY: fast-forward it, then test (dirty for line endings only: `eol-restore.mjs`). Not reached: `tested, not live`.
15. **Merge.** Authorized: a change Nour asked for in words (his policy, guard and skill edits too), a pasted-report job, a docs-only PR;
    on green: `node scripts/agent-os/merge-gate.mjs <pr> --sha <head you verified> --merge`, no second question.
16. **Report.** `.agents/core/templates/completion-report.md`: one plain line per finished piece, labels kept, the highest evidence rung, live apart from
    merge (`deploy-not-live` when it lags), what each session did well and what went back, then the parked register. No "done" while scoped work is actionable.
17. **Log and learn.** Add `docs/agent-os/ledger/<job-id>.md` in the SAME PR (row `MERGED`, PR cell `this PR`, metrics row), `node scripts/agent-os/ledger-check.mjs`
    first; each reversible decision made without Nour is one `Ruling: <what> - <why> - <cost if wrong>` line in the PR body (B19). Repeated lesson:
    `session-observer`. Never edit evaluators or guards to make a job pass ([references/ledger-and-metrics.md](references/ledger-and-metrics.md)).
