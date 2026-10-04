---
description: Use when delegating coding work to the local pi agent to cut cost, or when you are about to hand-write source or test files yourself instead of specifying them, or when a small-model agent reads files endlessly without ever writing, times out having produced nothing, or keeps reasoning forever even though thinking was turned off.
---

# Delegating to pi

**You are the tech lead, not the typist. All source code is written by pi — implementation and tests alike.**

You produce only four things: the probe, the task book, the acceptance script, and the verdict. Every other character gets dispatched.

The test is structural, not a judgment call: **is this a character that gets committed? Then dispatch it.**

## The four-way split (the one decision that must be right)

| What this really is | Who does it | The test |
|---|---|---|
| **Writing any source code**: implementation, tests, patches | pi | "Is this a character that gets committed?" |
| **A lookup, decidable without reading context** | a script | "Does this transformation require understanding context?" |
| **Comparing two lists item by item** | pi | Extract and normalize with a script, hand the comparison to pi |
| **Deciding the contract, judging success/failure** | you | probe, task book, acceptance script, verdict |

**The "a lookup, decidable" branch is the most expensive misjudgment**, and no hook can catch it.
Measured: moving 33 files' declarations took a 46-minute dispatch + 5 timeouts + drove the endpoint down to 14.6 tok/s (normally 50),
while a deterministic script finished in seconds at zero load. **It needs no context understanding, so it should never pass through a model at all.**

**"pi can't handle this" is not a reason to do it yourself.** Sometimes it means split the work — but reach for that
far less often than feels natural, because splitting has a measured cost of its own (see below).
The one place the 700-line rule genuinely applies is **editing a single existing file**: past roughly 700 lines pi
spends its budget re-reading. Extract the part that needs changing into a new file and hand pi the whole new file.
That is a rule about *one file's size*, not about how much work a dispatch may carry.

## Size the task like a subagent's, not like a slice

**Give pi a whole coherent unit of work.** Multiple files, implementation and tests together, the whole feature.
Do not pre-slice it into pieces small enough to feel safe.

This is measured, and the result went the opposite way to the intuition it replaced. The same job — a two-module
matcher plus tests, against a fixed written contract — dispatched two ways:

| | Whole task (3 files) | Sliced to one 30-line file |
|---|---|---|
| Outcome | ran out the clock | ran out the clock |
| Writes | **2**, exactly as asked | **22** — the same scratch file 21 times |
| Input tokens | **5,070** | **59,776** (12x) |
| Scope | clean | wrote a file the task book forbade |
| Correctness | **passed all 9 acceptance tests** | parser correct, nothing else produced |

Slicing did not make it faster, safer, or cheaper. **A task far below what pi can do does not finish early — it
spends the remaining budget on self-doubt**, writing and re-running scratch files, which is exactly the roaming
and token burn the "keep it small" instinct was trying to prevent. The big dispatch's only shortfall was the
clock; its code was correct.

So: a dispatch that takes 15 minutes and returns working code is a success, not a problem to engineer away.
Raise `timeout_s` before you shrink a task.

**Two-stage dispatch (tests first, then implementation) is an option, not the default.** It doubles the context
build-up and doubles the wall clock. Reach for it when you specifically need the tests to be written blind to the
implementation — a subtle algorithm where a self-marked test would be worthless. For ordinary work, one dispatch
carrying the contract, the implementation and the tests is both cheaper and, measured above, correct.

## How to dispatch

Use the MCP tools; don't assemble CLI commands by hand:

| Tool | When to use it |
|---|---|
| `pi_dispatch` | Dispatch a task book. Defaults to `mode=async` — dispatch, keep working, collect later. `mode=sync` blocks, for when your next step depends on the result |
| `pi_status` | Where it stands: elapsed and remaining time, writes, reads, tokens — plus `phase: "thinking"` while the model is mid-reasoning and a `stream_events` count that rises whenever the stream moves, and a `spinning` warning when it is rewriting one file over and over. Compact by default so it is cheap to poll; pass `verbose` when a poll looks wrong |
| `pi_steer` | Interject mid-run when you notice it's heading the wrong way |
| `pi_abort` | Abort. **Re-dispatch an aborted task unchanged; only rewrite the task book after a real failure** |
| `pi_result` | Collect the verdict of an async dispatch |
| `pi_transcript` | Drill in only when the verdict isn't enough |
| `pi_stats` | Check token usage |

**If those tools are not available in this session**, the plugin was installed or reloaded
mid-session: Claude Code registers MCP servers at session start, so `/reload-plugins`
restores the skills and hooks but not the tools, and nothing announces it. Restarting the
session is the real fix. Until then use the CLI, which calls the same function behind
`pi_dispatch` — do NOT hand-roll a runner around `src/dispatch.mjs`:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-dispatch" <task-book> --cwd <dir> --timeout 900
```

Writing your own runner looks easy and is not. `dispatch()` returns `{ handle, done }`, so
awaiting just the outer call hands back an empty shell indistinguishable from a hung run;
and counting what pi did means re-deriving `verdict.mjs` — a write is a
`tool_execution_start` with the path in `args.path`, and one tool call fires 3-4 events
that must be deduped by `toolCallId` or four writes read as twelve.

**Two-stage dispatch**, when you have decided you need it: dispatch the tests first (with the contract), confirm they
genuinely fail and fail where expected; then dispatch the implementation (with that failing test set, plus "do not
touch the tests"). The risk it buys off is real — tests written alongside an implementation tend to pass whatever
was written. Weigh that against the doubled cost, and note the cheaper guard that covers most cases: **write the
acceptance test yourself** and run it against whatever comes back. That is your job either way, and it does not
need a second dispatch.

**While it runs**: poll `pi_status`. It is deliberately compact — counts, not lists — because every reply stays in
your context for the rest of the session. If it reports `spinning`, pi is rewriting the same file: `pi_steer` it, and
size the next task larger.

**A poll where nothing moved is not a stalled dispatch.** A long reasoning turn produces no tool calls and no
finished message, so writes, reads, tokens and `current_tool` all legitimately sit still for minutes — measured:
identical replies at 40s and 137s on a run that finished correctly at 290s. Two fields settle it without
touching the transcript: `phase: "thinking"` says the model is mid-reasoning right now, and `stream_events`
rises whenever the stream moves, so comparing it across two polls is a liveness test. Reach for `pi_transcript`
to find out what pi is *doing*, never to find out *whether it is alive*.

**Model choice**: leave it unspecified to use the user's own pi default model (`~/.pi/agent/settings.json`) —
that is the right choice almost every time. Only switch it deliberately, via `pi_dispatch`'s `provider` / `model` parameters,
and always supply both together (pi only honours a paired override). See `references/choosing-models.md` for the selection criteria:
editing an existing file always calls for dense; only writing a brand-new file from scratch is worth trading to a MoE for speed.

**`pi_dispatch`'s other flags have measured defaults**: `thinking=off`, `tools=read,write,edit`,
`no_context_files=true`. Override them deliberately — every one of these defaults exists because of a measured
"without this it times out with zero output" run (the reasoning is in the tool descriptions).

## Modes

`/pi-delegate:mode strict` makes the hook block your own edits to existing product code outright.
Use `/pi-delegate:probe` to get a one-time bypass for a probe.

## Further reading (load on demand, not all at once)

| File | When to read it |
|---|---|
| `references/delegating-implementation.md` | Dispatching implementation — how to write the contract, two-stage dispatch, how to split work down to what pi can handle |
| `references/task-books.md` | Writing a task book, when the output followed it exactly but is still wrong, or when the brief was written through a shell heredoc |
| `references/verifying.md` | Acceptance review, or a second layer of review |
| `references/choosing-models.md` | Timeouts with zero output, choosing a model, or reading the Arena.ai advisory in the SessionStart report |
| `references/small-model-field-guide.md` | Shortlisting a new model, sizing hardware, or choosing a quantization — published guidance, to be verified rather than trusted |
| `references/orchestration.md` | Fan-out, deciding concurrency width |
| `references/diagnosing.md` | Wrong output and you're not sure what to adjust — a symptom lookup table |

## Symptoms don't point to causes

Failure symptoms (timeout, no output) all look the same. **Measure the thinking/tool ratio before touching anything.**
Use `pi_transcript`'s `filter=tools` to see what it's actually reading — a file that was never named is roaming.

## Upgrading pi-delegate

`/plugin update` then `/reload-plugins` is enough. The reload restarts the MCP server and
re-reads the skills and hooks, and the completion monitor restarts too — but only because
its `name` in `monitors/monitors.json` changed in 0.6.2.

That is worth knowing, because a monitor's `name` is exactly what Claude Code uses to avoid
starting a duplicate on reload: **an already-running monitor with an unchanged name is never
replaced, however much its command changed.** It stops when the session ends, and not
before. So a release that changes what the monitor *does* has to change its `name` as well,
or every existing session keeps running the old command in silence.

That silence is the real hazard here rather than the staleness: 0.6.1 moved the completion
log to a per-session path while every running monitor was still tailing the old shared one.
Async dispatches completed and wrote their line correctly; nothing was watching where they
wrote it. `tail -F` on a path nobody writes to reports nothing at all, so the only symptom
was a notification that never came.

**Poll; do not wait on the notification.** `pi_status` is the mechanism — the MCP server
talks to pi over RPC and knows the outcome the moment it happens. The notification is a
convenience that only exists when a watcher is attached, and an async dispatch's reply now
says outright whether one is. When none is (every headless run, and any session whose
monitor has died), nothing will arrive on its own.

A notification that never comes looks exactly like a task still working — the same
"symptoms don't point to causes" shape this skill warns about for pi itself. Polling costs
almost nothing; believing a notification that is not coming costs the entire wait. The
verdict is never lost either way, only the nudge.
