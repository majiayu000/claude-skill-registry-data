---
name: conductor-max
description: Madmax conductor for pi — split a big goal into many tiny slices (up to ~50), run them as parallel pi-subagents workers in worktrees, and let TypeSafe Jev make every routing, review, QA and supervision decision. Use when a goal decomposes into many small, independently testable changes. Not for one-file fixes or prototypes.
---

# Conductor Max (pi)

**Large model plans. Jev decides. Workers execute. Verification checks.**

You (the main pi session) plan once and handle escalations. `jevo-worker*` subagents write code.
The `jevo` tool runs the shared decision CLI; its thresholds and vetoes live in code and fail closed.
Inside every `jevo-worker*` child, this package supervises it:

- **Finish gate:** when the worker ends a turn without tool calls, the package reruns the slice gate and
  asks Jev for QA and a staged review. If the slice isn't done, the reason is queued as a follow-up and
  the worker **keeps going** in the same run. After `JEVO_MAX_BLOCKS` (default 2) rounds, or on any
  error, the slice is marked `escalate`.
- **Health:** every `JEVO_HEALTH_EVERY` (default 8) tool calls, Jev checks for stuck or off-track work
  and steers the worker.

The workers are background children (`async: true`), because only background children load installed
extensions. Jev key: `TYPESAFE_API_KEY`, else `.env` in the project, else `~/.pi/agent/secrets/typesafe_api_key`.

## Tool: `jevo`

```
jevo(["slice","new","--id","S3","--goal","...","--acceptance","...","--allow","src/cart.py,tests/test_cart.py","--gate","pytest -q tests/test_cart.py"])
jevo(["triage","--slice","S3"])        # tier -> agent; exit 3 = human; wave serial|parallel
jevo(["slice","list"])                 # status: new / fixing / approved / escalate
jevo(["check","--slice","S3"])         # manual gate -> QA -> review (the finish gate runs it for you)
jevo(["report","--html",".jev-orchestrator/scoreboard.html"])
```

Exit codes in the JSON: 0 proceed/approve · 1 fix · 3 escalate · 2 error (treat as escalate).
`/jevo` in the TUI shows `slice list` (or any args you give it).

## Loop

1. **Scope + authority.** Restate the goal. Quote what the human authorizes. By default workers commit
   in their worktree only; no push, PR, deploy or ticket write without quoted authority.
2. **Plan once.** Build a slice DAG. A slice is one acceptance criterion, ≤ ~3 files, ≤ ~150 changed
   lines, and has its own fast gate command. `slice new` each. Commit your plan first: worktree isolation
   needs a clean checkout.
3. **Triage all slices.** Map tiers to agents: fast → `jevo-worker-fast`, balanced → `jevo-worker`,
   reasoning → `jevo-worker-reasoning`. Exit 3 goes to the human list. `wave: serial` slices run after the wave.
4. **Dispatch a wave** in one `subagent` call with worktree isolation (cap 12 in flight; raise toward 50
   only when slices touch disjoint files):

   ```js
   subagent({ isolation: "worktree", workflowScript: `
     const r = await runs.all([
       { key: "S1", agent: "jevo-worker-fast", task: "JEV-SLICE: S1\nGoal: ...\nAllowed: a.py, tests/test_a.py\nGate: pytest -q tests/test_a.py" },
       { key: "S2", agent: "jevo-worker", task: "JEV-SLICE: S2\n..." }
     ]);
     return r.map(x => x.output);
   ` })
   ```

   **Every task must start with `JEV-SLICE: <id>`.** That's how the supervisor finds the slice. Put the
   packet inline, because the slice file isn't visible inside the worktree.
5. **Collect.** `jevo(["slice","list"])`. `approved` → merge that worker's worktree branch in dependency
   order. `escalate` → run `jevo-reviewer` with the slice id, the ledger reason and the worktree path.
   `VERDICT: fix` → a **new** slice id and a fresh worker; `human` → the human list.
6. **Integration verify** after each wave merges: full test/lint/typecheck. Red → find the culprit merge,
   revert it, requeue it as a fix slice.
7. **Scoreboard:** `jevo(["report", ...])`. Report only numbers the ledger measured.

## Rules

- A worker's "done" is not evidence. The finish gate and your integration tests are.
- Never two workers in one checkout. Never let a worker delete files it didn't create.
- Jev reads its input literally and can be argued with. Code vetoes (allowlist, secrets, failure counts,
  exit codes) run first, and a Jev approval never pushes, merges to main or deploys.
- A high escalation rate means the slices are too big. Re-slice instead of loosening thresholds.
- Agent models are defaults. Override them with pi-subagents `subagents.agentOverrides.<name>.model`.
