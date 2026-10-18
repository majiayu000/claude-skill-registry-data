---
name: clink-subagents
description: Delegate a well-scoped chunk of WORK (implementation, refactor, bulk transform, focused research, first-draft) to Codex (GPT-5.6) or Antigravity (Gemini) as a subagent via PAL's clink tool — to offload effort, parallelize, or save your context. Use when you have a self-contained, verifiable subtask a cheaper agent can do while you orchestrate. NOT for gathering opinions/consensus (use clink-brainstorm) and NOT for orchestration/judgment (keep that yourself). Covers which agent fits which task (grounded in Artificial Analysis index data + a local benchmark), how to prompt them, and the mandatory verify-everything discipline.
---

# clink-subagents

> **Requires [PAL MCP server](https://github.com/BeehiveInnovations/pal-mcp-server)** connected, with `clink` configured for `codex` and `antigravity`, and optionally `cursor` (see `conf/cli_clients/*.json`; Antigravity needs the [xenodeve/pal-mcp-server](https://github.com/xenodeve/pal-mcp-server) fork for its ConPTY driver on Windows, and the same fork ships the `cursor` preset). This skill is an orchestration layer on top of `mcp__pal__clink` — it does nothing standalone.
>
## What this skill is, and what the other one is

Two skills sit on `clink`. They are not variants of each other, and the distinction decides every routing choice below.

| | What it is | What comes back |
|---|---|---|
| **`clink-subagents`** — this file | **`clink` used as your subagents.** You hand out chunks of the work and they come back done | **finished work** — an implementation, a refactor, a bulk transform, a first draft, a focused lookup |
| [**`clink-brainstorm`**](../clink-brainstorm/SKILL.md) | **an engineering committee.** Several senior agents put on the *same* codebase review or the *same* plan, then you synthesize | **judgment** — what is wrong, what to build, which approach wins |

**The consequence for routing, which is where this gets confused:** here you are buying **throughput on verifiable leaves**, so the small model at a cheap tier is usually the right answer and the difficulty table below is how you pick. There you are buying **reasoning**, so it is the reasoning model every time and the small model never appears. **Do not carry a model or effort setting from one skill into the other.**

Want a subtask executed → here. Want a design judged or a codebase reviewed by a panel → brainstorm.

## The core idea

You (the orchestrator) are the strongest **agentic** model in this setup — keep the decomposition, integration, judgment, and verification. Push the **leaves** of the work (self-contained, checkable subtasks) to a subagent, then verify and stitch. Delegate to *offload effort/context* or to *run independent chunks in parallel* — never to avoid thinking.

## When to delegate — and when not to

**The trigger: before the first edit of any task with more than one leaf, name each leaf and record delegate/keep with the reason.**

Not "delegate more" — that exhortation is already in this file and it already failed. On 2026-08-11 an orchestrator implemented a whole clink client — parser, agent, config, discovery, four doc files — and delegated **none** of it, in a repo whose `CLAUDE.md` opens with *"delegation is the default, not the optimisation"*. **The developer had invoked `/clink-subagents` and `/clink-masteragent` in the message immediately before.** Both were loaded and in context.

**So the gap is not knowledge.** The selection step did not run and conclude *keep*; it never ran. Both skills were reference material consulted by whoever remembered to consult them, and awareness was at its maximum. `t4-dev-workflow` had this exact shape and #105 fixed it by giving the change-site survey a moment; this is the same fix.

**The record is one line per leaf** — `leaf → delegate/keep → why`. It costs seconds, it is what makes a *keep* reviewable, and its absence is what made the 2026-08-11 miss invisible until someone read the diff.

**Delegate** a subtask that is:
- **Self-contained** — fully specifiable in one prompt (the agent has *zero* conversation context).
- **Verifiable** — you can prove it right afterward (run a test, read the diff, check against a spec). If you can't verify it, don't delegate it. **Verifiable means _observable behaviour_, not checkable-looking**, and the difference is not academic. Measured 2026-08-05: the same model at the same effort (`gpt-5.6-luna`, `high`), the same prompt shape, two leaves dispatched at the same moment. The **code** leaf returned a good test — it asserted on a returned value, so its failures were behavioural. The **prose** leaf (edit a skill document) returned assertions that were each a `grep` for a sentence the worker had made up. A code change has an output you can assert against; **a document's "behaviour" _is_ its prose, so a worker with nothing to observe falls back to inventing the prose and asserting on its own invention** — circular, and it looks exactly like a passing check. Before delegating, name the observation the work will be judged by. If you can't, it isn't a leaf.
- **Worth the latency** — each clink call is **~20–35s of CLI bootstrap** (a real agentic file-edit loop can be **~50s**). **This is a feasibility gate, not the cost function** — see *Token economics* below, which decides. It rules out a call that cannot complete in time, and it does not answer whether to make one. **Those are floor figures for a small task, not a budget for real work:** on read-heavy delegations against a live repo, `codex` took **401s and 529s**, `cursor` 108s, `antigravity` 55s — measured 2026-07-31 and recorded in `xeno-skills` issue #55, not derived from anything in this repo. Budget minutes for anything that has to read a repo. **Past two minutes Claude Code stops blocking on it: the call is moved to a background task, you are handed a task id, and the result arrives as a notification.** So the wait is bounded at ~2 minutes, not at the length of the call — see the rule below, which is about what you do with the rest of it.
- **Proven to have run** — *only for a delegation whose result depends on a command having executed*: a test run, a build, a lint, anything whose report is worthless if the tool silently no-opped. **Make the worker return a sentinel it can only produce by running the thing**, and check it came back:

  > *"Before anything else, run `<the command>` and paste its FIRST and LAST line verbatim, plus the exit code. If you cannot execute commands, reply exactly `TOOLCHAIN_DEAD` and stop."*

  **Why a sentinel rather than "check your setup".** A broken tool chain does not error — it returns **exit 0 with a plausible answer** the model produced by reasoning from the prompt instead. Nothing in the response distinguishes that from a real run, so **a plausible result is not evidence the tool ran.** Seen twice on this machine: a global instruction prefixing every shell command with a binary the harness had removed from `PATH` (every `codex` tool call failed, silently), and `codex`'s `rtk` wrapper failing to resolve `rg`, `grep`, `ls` and `gh` while its *file reads* kept working — so the same worker was half-blind, and only its shell half.

  **When the check fails, do the work yourself or change client — not retry.** Retrying re-runs the same broken chain and returns the same confident nothing; the fault is in the worker's environment, which another identical call cannot alter.

- Good fits: a well-specified function/module, a mechanical refactor across a known site, a bulk format/transform, a first-draft you'll review, focused external-doc research/summarization.

### Jobs a given client cannot do at all

Cheaper than discovering it with a call. **Every row carries the date it was last verified, because all of these have moved before** — treat an old date as a prompt to re-probe, not as a fact.

| Client | Cannot | Last verified |
|---|---|---|
| `antigravity` | **Run anything.** Its command tools are auto-denied headless, so it cannot execute a test, a build or a lint. *File reads and `--help`-style probes do work* — the limit is execution, not access, and forbidding shell commands in the prompt makes it reliable rather than flaky | 2026-08-04 |
| `cursor` (Windows) | **Touch a file at all**, if it inherits a bash `SHELL` — every tool call dies and it answers from the prompt text with exit 0. Fix the config first (see gotchas); do not delegate file work until you have | 2026-07-31 |
| `codex` | **Nothing inherently** — it holds through a write-run-self-correct loop. But on a machine where a wrapper intercepts its shell, its command tools fail while its file reads succeed, which is the half-blind case the precondition above exists to catch | 2026-08-04 |
| `claude-9arm` / qwen | **Run builds or tests.** It ignored an explicit working directory, wrote to the repo root, and produced no files across a multi-step run. Read, gather and format only | 2026-07-16 |

**Never delegate** (keep it yourself):
- Orchestration, decomposition, deciding *what* to build, integration across the whole change.
- **Final verification** — the buck stops with you.
- Security / auth / permission-sensitive changes, or anything needing full session context or taste.
- Anything you can't independently check.

## Which agent — routing rubric

Grounded in **[Artificial Analysis](https://artificialanalysis.ai/models)** indices (2026-07) + a local benchmark. Scores: **Coding Index / Agentic Index**.

> **Scale note — do not mix the two scales in this skill.** The `71–77` / `45–54` figures in the table below are the **Coding Index / Agentic Index**, an older sub-index. The `32–59` figures in the GPT-5.6 ladder further down are the **AA Intelligence Index v4.1**, a composite of nine evals where the frontier is ≈ 60. A number from one is not comparable to a number from the other, and averaging or ranking across them produces a false ordering. Higher is better on both — that is all they share. *(Source: `docs/research/2026-07-16-model-effort-capability-matrix.md`, scale note — in the `xeno-skills` repo. **Research is not shipped with the installed skill**, so the figures reproduced here are the reader's copy of record, not a link to follow.)*

| Agent (`cli_name`) | Backend | Coding | Agentic | Delegate to it… | Guardrail |
|---|---|---|---|---|---|
| **`codex`** | GPT-5.6 — **`sol` and `luna`**; **skip `terra` and `gpt-5.5`, they are dominated** (see the ladder below). Luna access is per-account and the research note says to verify it: an unavailable model hard-400s, so a failed `-m gpt-5.6-luna` call *is* the check | **71–77 (top tier)** | **45–54 (top tier)** | Harder self-contained coding, edge-case-y implementation, in-place edits of a known file. **Not reviews or design judgment — those are [`clink-brainstorm`](../clink-brainstorm/SKILL.md)** | Elite *model*, but its **agentic harness is the weaker link** — it can mishandle multi-step tool/state workflows. Give a tight spec; **verify the output**. **Model and effort are not free choices here** — there is a standing cap in the ladder section, and a read-heavy call runs **400–530s**, not the ~30s bootstrap figure above. |
| **`antigravity`** | Gemini 3.x (`agy`) | 68–70 (ok) | **21–37 (weak)** ⚠️ | ONLY simple, **single-shot**, single-file, trivially-verifiable **artifact** tasks — a pure function, boilerplate, one format/transform, a focused lookup | **Weak at multi-step agentic** — never give it work where a wrong early step compounds. **Headless it could once *write* files but not *run* anything** (command tools auto-denied) — re-verify before relying on that, it has moved: a headless file read now succeeds, and `role: codereviewer` returns a real severity-graded review rather than the permission error it used to. Still prefer **artifact mode** for anything you must trust, and verify yourself. Chatty: appends a `<SUMMARY>` block even when told "output only X" — strip it. **Fragile in a way unrelated to models:** every run does an eligibility check that fetches your Google profile picture, so a transient network failure to `googleusercontent.com` exits 1 mid-session with `Eligibility check failed` — retry rather than debug. |
| **`cursor`** | Widest roster of any client — Grok 4.5, Composer 2.5, Kimi K3 / K2.7 Code, GLM 5.2, Opus/Sonnet/Fable, GPT-5.x, Gemini | varies by model | **untested here** | Leaves where the *model family* is the point — a foreign-prior second opinion, or a lineage no other client carries (xAI / Moonshot / Zhipu) | **Not on the local ladder below** — treat any given model's agentic reliability as unknown until you test it yourself. **On Windows, confirm its config overrides `env.SHELL` before delegating anything that must touch a file** (see gotchas) — a bash `SHELL` inherited from the caller kills every tool silently and it degrades to a text-only responder. Floor latency ~25–30s even for a one-line prompt. Its quota splits in a way that changes routing — see economics. |
| **you (orchestrator)** | e.g. Claude Opus 4.8 | ~74 | ~47 | — | Decompose, integrate, verify. Delegate the leaves, own the tree. |

Rule of thumb: **Codex for the hard leaf, Antigravity for the trivial leaf, you for the tree.** If a task needs more than one dependent step of judgment, it isn't a leaf — don't delegate it (least of all to Antigravity).

**Two more channels the rubric doesn't table:**
- **`claude-9arm` / qwen via clink** (the free/unlimited local model — details in `qwen-agent`): fine for **read/gather/format** leaves, but its quality cracks earlier than the others (see the ladder) — at a moderate task it can return **correct output with a hidden side-effect** (e.g. mutating its input) that an output-only test passes. And **it ignores the working directory you specify** — an in-place write defaulted to the *repo root* despite an explicit scratch path, so its **write sandbox / allow-rules are not optional**; never give qwen unsandboxed write. Verify its writes by diff, and its returns by checking for side-effects, not just output equality.
- **In-harness Task/Explore subagents** (your own platform's subagent, not clink): a distinct lever for **read-only fan-out** — dispatch several in parallel over independent areas, each returning a terse structured verdict, so you ingest conclusions not file dumps. Best for *verify-before-you-act* sweeps (e.g. audit N issues' acceptance criteria against real code before a bulk close); it shrinks *your* context the same way clink does, with per-area parallelism clink lacks. Constrain output ("report only, not file contents") and they obey.

## Token economics — what "cheaper" actually means

Measured 2026-07-16 (same tasks, a live repo). The back-ends are **billed differently**, so "count total tokens" is the wrong lens:

- **You (the orchestrator)** are the only **metered, context-window-bound** token pool — the scarce one.
- **`codex` / `antigravity` are subscription** — flat, **rate-limited**, not per-token-billed.
- **A local model** (e.g. Qwen via `claude-9arm` — see the `qwen-agent` skill) is **unlimited and free**: its tokens cost only electricity + latency.

So **"cheaper" = fewer of *your* tokens**, and delegation wins whenever `(what you'd read + reason yourself) > (prompt + result you ingest + verification)`. Big-input / small-output / cheaply-verifiable → delegate. A 2-line edit in a file already in your context → do it yourself; the round-trip costs more of *your* tokens than the edit.

**Tokens are the cost function. Latency is a feasibility gate.** The two are not alternatives and this file used to state the second as the first — `clink-masteragent` already gets it right: *"Under a 60–120s transport ceiling that is **infeasibility, not latency**."*

**Worked, because a formula that is never computed is read as a sentiment.** Both from the 2026-08-11 change:

| leaf | what you'd read + reason | prompt + result you ingest + verify | verdict |
|---|---|---|---|
| **a 2-line edit in a file already in your context** | ~0 — the file is already loaded, the change is obvious | prompt + the returned diff + reading it to check | **keep** |
| **four documentation files, bulk mechanical** | every target file, their current wording, and the edit for each | one prompt, four short diffs, a skim | **delegate** |

**The second row is the case the old wording decided wrongly.** *"Never delegate something you'd finish correctly in less time"* answers **keep** — the writing is quick and each file is easy. The formula answers **delegate**: large input you would have to read, small output you ingest, and verification that is a skim. Those docs were the single largest mechanical leaf in the change, and the orchestrator wrote them itself and offered the latency argument afterwards.

**Read latency only to ask whether the call can complete at all**, then decide on tokens.

**The subagent's *returned* text is *your* tokens.** Constrain it hard ("return ONLY X"):
- `codex` obeys + is terse (5-bullet summary of an 8k-token file came back ~240 tok; a `NO BUGS FOUND` review, ~15).
- `antigravity` appends a `<SUMMARY>` block anyway (~+60% ingest) — strip it. **`cursor` does the same** (verified live: it appended one to a prompt that said "reply with exactly …"), so strip both.
- A read-heavy `codex` **review** once echoed its whole transcript back = **91k chars ≈ 23k of your tokens**. For read-heavy delegations, say "return findings only, not the files."

**Pick the back-end by latency × intelligence × subscription-quota you'll spend — never by its token count** (free or flat). Unlimited menial bulk you don't want to bill to a subscription → the local model (slower, less smart). Must be *right* → `codex` (top intelligence *and* tersest = also cheapest on your pool). The ~130k-token harness overhead a fresh local `claude-9arm -p` call reloads each time is **free compute** — it costs you only latency, nothing metered.

**Antigravity's quota is split by vendor — and the non-Google side drains fast.** Within `agy` there are **two shared subscription pools**:
- **Google pool** — `Gemini 3.5 Flash` + `Gemini 3.1 Pro` share this one.
- **non-Google pool** — `GPT-OSS 120B` + `Claude Sonnet 4.6` + `Claude Opus 4.6` share this one, and it **burns noticeably faster** than the Google side.

So routing `antigravity` to a Claude/GPT route (e.g. for a non-OpenAI second opinion) is fine *occasionally*, but it drains the non-Google allowance quickly; keep bulk/repeated antigravity work on the cheaper Gemini pool and spend the Claude/GPT route only when a different vendor's judgment is the point.

**Cursor splits the same way** — Cursor Pro shows the two as separate bars:
- **Cursor Models** — *only* `cursor-grok-4.5-*` and `composer-2.5`. Overflow beyond the limit spills into the Other Models quota or on-demand spend.
- **Other Models** — everything else it carries (Opus/Sonnet/Fable, GPT-5.x, Gemini, Kimi, GLM). Burns noticeably faster, and overflow goes straight to on-demand spend.

**Both clients follow one pattern: a cheap in-house lane (Google on `agy`, Grok/Composer on `cursor`) and a faster-draining foreign lane, metered as separate pools.** Spending a house lane therefore costs its foreign lane nothing, which gives you *two* independent cheap delegation lanes — bulk Gemini work on `agy` and bulk Grok/Composer work on `cursor` do not compete — plus `codex` on its own subscription as a third. Reserve both foreign lanes for the calls where a different vendor's judgment is the actual point.

**Cursor's allowance is monthly — no 5-hour or weekly rolling window.** That makes it the right home for *bursty* delegation: a wide parallel fan-out, or a long loop, cannot hit a short-window wall part-way through and strand the batch. Its house lane also carries the larger of its two allocations. Where a client meters on a rolling window you have to pace a long run; on Cursor you don't — so push repeated bulk volume there and save the rolling-window clients for the leaves that specifically need them.

**One client can run several workers at once, on both of its pools.** `cli_name` names the **client**, not the model: several `clink` calls with the *same* `cli_name` and different `model` values, in one message, run in parallel. So a fan-out is not capped at one worker per configured client — `cursor`→Grok draws the house lane while `cursor`→Kimi K3 draws the foreign one, and both run at the same time instead of queueing on a single allowance. **Kimi K3 and GLM 5.2 share the same foreign pool**, so running both drains it twice; that is a deliberate spend, not free breadth.

Net routing across all clients: **Gemini via `agy`** (in-house there) · **Grok / Composer via `cursor`** (in-house there) · **GPT-5.x via `codex`** (own subscription, plus a real effort knob) · **Kimi K3 / GLM 5.2 via `cursor`** only when a foreign prior is the actual point. Never pick a client merely because it carries the model — pick it by which allowance the call draws down, preferring whichever client carries that model in-house.

## How to delegate (the call)

`mcp__pal__clink(prompt, cli_name, role?, continuation_id?, images?)`

**A backgrounded call is not a reason to wait — this is the expensive half.** The two-minute block is fixed: the threshold lives in the harness and you have no control while a call is blocked. What follows it is entirely yours, and it is where the time actually goes. Measured, same host and same tool, opposite outcomes:

- A session on 2026-08-04 had a `codex` call backgrounded at 120s, picked up unrelated work, and took the result as a notification at **188s**. No idle time at all.
- Another showed **`Waiting for task`** with the call *already* in the background panel while the turn ran **3m 4s → 4m 17s**. The idle stretch was longer than the block that preceded it.

Nothing in the harness differed. **The moment a call is backgrounded, take the next piece of work — the notification will find you.**

**Waiting is sometimes correct, and this is not a discipline problem.** If the next step genuinely depends on the answer, filler work is worse than waiting — say so and wait. The observed variance tracks *whether independent work existed*, not effort: a brainstorm round idles least because firing N agents in parallel guarantees something else is in flight. **So the lever is the shape of the turn, not a reminder to be diligent** — which is what the two rules below are for.

Two consequences worth putting in the plan rather than discovering:

- **Fire the whole batch in one message.** N independent delegations sent together **pay that block once**, not N times, because they run concurrently and background together. Three sequential calls cost three blocks; three parallel calls cost one.
- **Order the turn so the block lands where it is free.** Do the local work first — reading files, grepping, checking git — and **fire the batch last**. Then the two minutes elapse when you had nothing pending anyway.

1. **Build the delegation contract, do not describe it.** The agent has **zero** context from your conversation, and "put everything in the prompt" is advice nobody can check. The shape is `BrainstormRequest v1` — `problem`, `objective`, `scope.exclude`, `questions`, and `context` split into facts / evidence / assumptions / unknowns so the worker cannot quietly promote your assumption into its conclusion. It is specified in [`clink-brainstorm/references/request-v1.md`](../clink-brainstorm/references/request-v1.md) and it applies to work delegations, not only panels. **`scope.exclude` is required**: a worker told what to look at still expands; one told what it may not touch has a boundary you can check afterwards.
2. **Pick a mode:**
   - **Artifact mode (safe default):** ask it to **return** the code/text; *you* review and integrate. Use for anything with any risk.
   - **In-place mode:** clink runs Codex/Antigravity with **bypass-approvals/sandbox** flags, so they *can* read and **mutate the repo directly**. Only let them edit files for **low-risk, well-scoped, verifiable** changes — then **diff + test**.
3. **Parallelize** independent delegations — multiple `clink` calls in one message (bounded by the slowest, not the sum).
4. **`role`** preset: `default` | `planner` | `codereviewer`. Use `codereviewer` when delegating a review; `planner` for a scoped plan you'll execute.
5. **`continuation_id`** (returned each call) — reuse it to follow up with the *same* agent in the *same* thread (≈49 turns) without re-sending context.
6. **File access:** prefer putting the absolute path *in the prompt text* and telling the agent to read it with its own tools. (Some orchestrators' permission classifiers block the `absolute_file_paths` parameter into repo source even with consent — don't fight it; use the prompt-text path instead.)
7. **Hand it the baseline skills. `karpathy-guidelines` on every call; `tdd` whenever the worker writes or changes code.** Both are procedural — they apply cleanly even to a small model, and they keep a worker on structure and honest about gaps where an unguided one drifts and fabricates. Add `simplify` or `post-mortem` when the task is a cleanup or a bug write-up. **If the task is diagnosing a failure, stop and read [`clink-debug`](../clink-debug/SKILL.md) first** — it owns every rule about delegating a bug hunt, including which skills the worker gets and what must be sent with them.

   **The split is not cosmetic, so do not collapse it back into one condition.** `karpathy-guidelines` governs *how to work at all* — the smallest thing that solves the problem, surgical diffs that trace to the request, no speculative surface, verifiable success criteria. A research summary, a bulk rename and a log condensation each earn it as much as a feature does, so gating it behind "coding" sends most of your delegations out without it. **`tdd` has a precondition: there has to be code to write.** Attached to *"summarize this log"* it hands the worker a red→green procedure with nothing to apply it to, and a literal model invents something to satisfy it rather than saying the skill does not apply. **[`clink-brainstorm`](../clink-brainstorm/SKILL.md) is outside the `tdd` half for the same reason** — a panel produces judgment, and there is no code there to test.

   **Do not tell the worker to *invoke* the skill; that only works in-harness.** `t4-dev-workflow`'s delegation reference says to name a skill and let the worker invoke it, which is correct for **your own platform's subagent** — it shares your skill catalog. **A clink back-end is a separate CLI with its own.** Measured 2026-07-31: `ls ~/.codex/skills/ | wc -l` → **120**, and `ls -d ~/.codex/skills/tdd` → *No such file or directory*. Asking `codex` to invoke `tdd` fails however clearly you ask, and it fails quietly — the worker just proceeds without it.

   **Use the path form instead: give the absolute path and let it read the file with its own tools.** Verified live the same day — a `codex` worker read `~/.agents/skills/code-review/SKILL.md` with PowerShell after the repo's own wrapper was unavailable, and followed it. Installed copies live at `~/.agents/skills/<name>/SKILL.md`. Cost: `tdd` is 3,249 bytes and `karpathy-guidelines` 2,585, so **5.8 KB of the worker's context and none of yours** — the cheapest part of any delegation you will make. The handoff mechanism itself is documented once, in [`clink-brainstorm` → *Giving a clink agent one of your skills*](../clink-brainstorm/SKILL.md) — including pasting the content inline, which is the more reliable of the two forms when the worker's file access is uncertain. Read it there rather than looking for a second copy here.

   **The specific failure this prevents, which is invisible while it happens.** A prompt that says *"write the function and its tests"* gets exactly that: implementation and test authored in one pass, so **no test in the change has ever been observed to fail.** The work looks finished, the suite is green, and nothing is yet known to test anything. **Ask for the RED first, and require the failing output back before the implementation is written.** Observed on `clone-space-mcp` PR #30 — two delegated tasks returned complete with `verify` exiting 0, and the missing evidence had to be reconstructed afterwards by mutation.
8. **Images:** the `images` parameter **does not work on any clink client** — no runner consumes it, and unlike a file path an image cannot be embedded into a text prompt, so it never reaches the CLI. Send the **absolute image path in the prompt text** and tell the agent to open it with its own tools; a vision-capable model then reads it correctly. Verified live: `cursor-grok-4.5-high` identified both the window and the selected radio option from a screenshot, against a prompt that told it to answer `NO_VISION` if it could not actually see the file. So this is a transport limit, not a model limit. (This fork now raises on `images` instead of dropping it; on stock PAL the call returns exit 0 with an answer written around a picture the model never saw.)

## Model & reasoning level — per call (this fork) or in config

This [PAL fork](https://github.com/xenodeve/pal-mcp-server) adds two **optional per-call** `clink` params — `model` and `reasoning_effort` — so you can dial capability per delegation without editing config. Support differs by back-end (all verified live 2026-07-16):

> **The codex effort rungs are per model — `not one ladder` — and the assumption is wrong in both directions.** Read from that client's own model cache on 2026-08-05:
> **Three models stop at `xhigh`** and never reach `max` — `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`. Asking those for `max` is a request the model cannot serve.
> **Four go one rung beyond it, to `ultra`** — `gpt-5.6-sol`, `gpt-5.6-sol-wm`, `codex-auto-review`, `gpt-5.6-terra`. But **`luna` does not have `ultra`**, and `luna` is the cheap tier this skill routes bulk work to, so its ceiling really is `max`.
> `gpt-5.6-sol-wm` appears in no other document here and what `wm` denotes is **not established** — do not route on it. Full table and method: `docs/research/2026-08-05-clink-model-inventory-refresh.md`.

| Back-end | `model` (per call) | `reasoning_effort` (per call) | Notes |
|---|---|---|---|
| **`codex`** | ✅ `-m <model>` — **validated** (invalid model → hard 400 error) | ✅ `-c model_reasoning_effort=` — but the rungs are **per model** (see the note above) | Read from `~/.codex/models_cache.json` 2026-08-05: **8 models**, every one served at a **272,000** context window regardless of what it supports — `gpt-5.4` declares a 1M `max_context_window` and still gets 272K, so a large-window delegation should not come here. |
| **`antigravity`** | ✅ `--model "<label>"` — **fail-closed** (invalid → exit 1 + catalog) | ✅ `--effort low|medium|high` — a real per-session flag, and **mutually exclusive** with `--model`: agy refuses the pair for every model it serves, so pass **one or the other, not both**. The tiered label (`(Low/Medium/High)`, `(Thinking)`) is the other way to say the same thing. **Honoured, not merely accepted** — same prompt, `low` → 0 thinking tokens, `high` → **446**; argv shape proves nothing on this client, whose history is a silently swallowed `--model`. PAL **refuses the pair before spawn** (pal#43). | agy's `--model` **must precede `--print`** (value-taking flag) or it's silently swallowed → default model; the fork's runner handles ordering. See gotchas. |
| **`cursor`** (Cursor's `cursor-agent`) | ✅ `--model <id>` — id form, e.g. `cursor-grok-4.5-high`, `kimi-k3-max`, `composer-2.5`, `gpt-5.6-sol-xhigh` | ➖ no separate flag — effort is **baked into the model id**, and **the ladder is per-model, not a fixed set** — do not assume a suffix exists (see below) | `-p` here is a **boolean** flag, so unlike `agy --print` it does **not** swallow `--model` — no ordering hazard. The `-max` suffix is the effort tier, **not** Cursor's Max Mode — that is separate persisted state, see gotchas. |
| **`claude-9arm`** (Claude Code → a gateway model, e.g. Qwen) | ✅ `--model` (last-wins) — **limited to what the gateway serves** | ❌ **no-op** — not a `claude`/gateway flag (this Qwen gateway has only thinking on/off, no graded effort) | Activate by copying `claude-9arm.json.example` → `.json` with your `claude.exe` + `--settings`/`--model`. |

Omit both to use the CLI's **config default** (Codex reads `~/.codex/config.toml`; others use their client `additional_args`).

### The GPT-5.6 ladder — and the cap on it

Effort is the knob most likely to be set wrongly, because the cost of setting it high is invisible at the call site.

**Four scales are in play and none converts into another.** Each figure below states which one it is on; ranking a number from one against a number from another produces a false ordering.

| Scale | Where it appears | Can you act on it directly? |
|---|---|---|
| **Coding / Agentic sub-index** (older) | the routing rubric above — the `71-77` / `45-54` pairs | no — comparative, and a different population |
| **AA Intelligence Index v4.1** | the `Index` column below; frontier is about 60 | no — comparative only |
| **Coding Agent Index v1.3** | harness x model pairs, quoted in [`clink-masteragent`](../clink-masteragent/SKILL.md) | no — a third population again |
| **Subscription credits** | the measured Sol-vs-Luna ratio below | **yes — this is the only one you spend** |

> **Every amount in this file is deliberately written without a currency sign — do not add one back.** Loading a skill as a slash command with arguments performs shell-style positional substitution: a dollar sign followed by a digit is replaced by the corresponding word of those arguments. Written the natural way, the entire ladder below rendered as `ตัว.20` / `skill.04` in a live invocation — a plausible-looking table carrying no cost information at all, with nothing to signal it.

<!-- figures:start source=docs/research/data/aa-models-augmented.csv -->

Every number between these markers comes from that file. `Index` is AA Intelligence
Index v4.1. `Burn` is AA cost-per-task in USD — codex is subscription-flat, so it
stands in for weekly quota burn rather than money. `Cost/pt` is what the whole Index
suite costs divided by the index: **lower is better value**, and it is the column the
skip rules are argued on. The source lives in the `xeno-skills` repo and is **not
shipped with the installed skill**; the figures are reproduced here so this file
still reads without it.

| Model | Effort | Index | Burn | Cost/pt |
|---|---|---|---|---|
| **`gpt-5.6-luna`** | low | 33.3 | 0.012 | 0.48 |
| **`gpt-5.6-luna`** | medium | 38.1 | 0.015 | 0.62 |
| **`gpt-5.6-luna`** | high | 46.1 | 0.029 | 1.33 |
| **`gpt-5.6-luna`** | xhigh | 49.1 | 0.043 | 2.16 |
| **`gpt-5.6-luna`** | max | 51.2 | 0.066 | 3.73 |
| **`gpt-5.6-sol`** | low | 49.4 | 0.307 | 8.10 |
| **`gpt-5.6-sol`** | medium | 53.6 | 0.514 | 13.01 |
| **`gpt-5.6-sol`** | high | 55.9 | 0.771 | 20.75 |
| **`gpt-5.6-sol`** | xhigh | 57.7 | 1.167 | 32.31 |
| **`gpt-5.6-sol`** | max | 58.9 | 1.862 | 58.46 |

The rungs the skip rule below excludes, with the figures that exclusion rests on:

| Model | Effort | Index | Burn | Cost/pt |
|---|---|---|---|---|
| `gpt-5.6-terra` | low | 40.5 | 0.132 | 3.83 |
| `gpt-5.6-terra` | medium | 45.6 | 0.160 | 4.89 |
| `gpt-5.6-terra` | high | 49.0 | 0.304 | 9.59 |
| `gpt-5.6-terra` | xhigh | 51.6 | 0.430 | 13.67 |
| `gpt-5.6-terra` | max | 55.0 | 0.733 | 29.26 |
| `gpt-5.5` | low | 43.5 | 0.260 | 8.63 |
| `gpt-5.5` | medium | 50.4 | 0.495 | 18.56 |
| `gpt-5.5` | high | 53.1 | 0.801 | 32.36 |
| `gpt-5.5` | xhigh | 54.8 | 1.175 | 50.66 |

### Pick by task difficulty — this table is the answer

Read down until a row describes your leaf, then stop. **Set both `model` and `reasoning_effort` explicitly on every codex call** — the config default is `sol` at `medium`, which is two rungs above where most work belongs.

| Your leaf | `model` | `reasoning_effort` | Index | Burn |
|---|---|---|---|---|
| **Trivial** — list, extract, reformat, restate, a one-line lookup | `gpt-5.6-luna` | `low` | 33.3 | 0.012 |
| **Simple** — boilerplate, a mechanical transform, a pure function with no trap | `gpt-5.6-luna` | `medium` | 38.1 | 0.015 |
| **Routine coding — the default when you are unsure** | `gpt-5.6-luna` | **`high`** | 46.1 | 0.029 |
| **Routine with a real edge case** — tricky input, an unfamiliar API, a draft you will edit | `gpt-5.6-luna` | `xhigh` | 49.1 | 0.043 |
| **Hard, cheap lane first** — a leaf Luna returned wrong at `xhigh`. Try this before changing lane; it costs an eighth of the row below | `gpt-5.6-luna` | `max` | 51.2 | 0.066 |
| **Hard** — subtle correctness, a leaf Luna returned wrong at **every** rung | `gpt-5.6-sol` | `medium` | 53.6 | 0.514 |
| **Hardest — the ceiling.** A leaf that already failed at `sol`/`medium` | `gpt-5.6-sol` | **`high`** | 55.9 | 0.771 |

<!-- figures:end -->

**The rungs outside the table, and why each is out.** Sol's `xhigh` and `max` are removed by the owner's cap below, not by the arithmetic. Sol `low` is out on the arithmetic, and the reason has changed since this rule was written: Luna `max` now scores **higher** (51.2 against 49.4) at a **fifth of the burn** (0.066 against 0.307) and roughly **half the cost per point** (3.73 against 8.10), so Sol `low` is now strictly dominated rather than merely a bad trade. Those exclusions plus the seven rows above are the complete set; there is no eighth option to reach for.

**Luna `max` was unlocked on 2026-08-04**, and the mechanism matters more than the row. The cap had been set from pre-cut prices; re-deriving it from current figures — which is what the cap is *for* — showed it no longer held on Luna's ladder, because the 80% cut of 2026-07-30 moved `max` from expensive to nearly free. The owner confirmed the unlock. **Sol's cap is unchanged and was re-derived the same way; it still holds.** This is the cap working as designed, not an exception to it.

**Reviews and judgment are not on this table at all.** Deciding whether code is correct, which design wins, or what is wrong with a plan is [`clink-brainstorm`](../clink-brainstorm/SKILL.md)'s job, and it uses `gpt-5.6-sol` for all of it. This table is for **work handed out to be done** — nothing on it is a substitute for a panel.

**The gap between the lanes is far wider than earlier versions of this table claimed.** The Luna rows burn **12× to 64× less** than the Sol rows (0.012–0.043 against 0.514–0.771), and on value per point Luna is **15× to 21× better than Sol at the same effort tier** (0.48 against 8.10 at `low`, 3.73 against 58.46 at `max`).

**That is corroborated by direct measurement, not only by the table.** Six `clink` calls with an identical prompt, plus the developer's own weekly-limit observation, put `gpt-5.6-sol @ medium` at **13–24× the subscription credits** of Luna for the same correct answer. Credits are the scale you actually spend, and the measured ratio and the sourced one now agree — the earlier documented figure of 3× to 11× was the outlier, and it was arguing from prices that had been cut.

**Pick the row by what the leaf *is*; escalate only after it actually failed.** Those are two separate steps and neither substitutes for the other. First selection is by description — stakes are not a row, and "this call really matters" moves you nowhere. Then, if that row came back wrong or thin, move down exactly one row and retry. Never open on a lower row because the leaf *feels* hard: that judgment is what put a documentation review on `sol`/`max` and burned four minutes for zero output.

**Never `gpt-5.6-terra` and never `gpt-5.5`.** Both are reachable — a real `codex exec -m gpt-5.6-terra` call returns normally, so absence from the table is a routing decision, not an availability fact. They are out because **intelligence per unit of cost is never worth it at any rung**, which is a weaker claim than the strict dominance this rule used to assert and is the one the current figures actually support:

- **`gpt-5.5` is strictly dominated at every rung.** `low` 43.5 @ 8.63 loses to Luna `high` 46.1 @ 1.33; `medium` 50.4 @ 18.56 loses to Luna `max` 51.2 @ 3.73; `high` 53.1 @ 32.36 loses to Sol `medium` 53.6 @ 13.01 — each time on **both** index and cost per point.
- **Terra is not dominated, and still never worth it.** Its best value is `low` at 3.83 per point, which is worse than *every* Luna rung (0.48 to 3.73). Where it edges anything, the edge is inside the noise: `xhigh` beats Luna `max` by **0.4 index points** for **6.5× the burn** (0.430 against 0.066), and `max` beats Sol `high` on value by 3.4% while scoring **lower** (55.0 against 55.9). Paying six times more for four tenths of a point is the trade this rule exists to refuse.

Why the cap removes Sol's top rungs, recomputed from the figures above rather than inherited: across Sol's ladder the index gains **+4.1, +2.3, +1.8, +1.2** while the burn goes 0.307 → 1.862, a sixfold rise. Per unit of cost that is **20, 8.9, 4.5, 1.8** index points — the fourth step returns under a tenth of the first. `high` is where the return collapses, and that is where the cap sits.

**Luna's ladder does not collapse that way, which is why its `max` is now a row.** Its whole range costs 0.012 to 0.066, so the step Sol charges 0.695 for costs Luna 0.023. Climbing to Luna `max` is cheaper than *not* climbing on Sol, and it is why the escalation path now exhausts the cheap lane before changing lane at all.

**The cap is still an owner's instruction and still not something to argue past.** It was loosened here by re-deriving it from current data — the procedure the cap itself prescribes — not by an agent judging a leaf hard enough to deserve a higher rung. That argument remains refused.

The cap is an owner's instruction (set 2026-07-31). **Do not reverse-engineer a rate, a deadline, or a difficulty estimate to argue your way past it** — it is deliberately tighter than the raw numbers alone would justify, so "but this leaf is hard enough to need `sol`/`max`" is the argument it was written to refuse, not a loophole in it.

Caveats. The index is a **composite** score, so a 1–2 point gap between two rungs is not a reliable difference — re-derive before routing on one. `Burn` is a single representative figure and the underlying measurement is noisy: the same prompt at the same model and effort has been measured at 20,344 and 62,742 input tokens, and AA publishes a 5th-to-95th-percentile cost spread of roughly fivefold. Stating those spreads in this table is [#89](https://github.com/xenodeve/xeno-skills/issues/89); until it lands, read `Burn` as an order of magnitude, not a price.

**Cursor's ladders are per-model — derive them, don't guess.** There is no fixed tier set and no structured catalog to query: `serverConfigCache` in `~/.cursor/cli-config.json` holds only backend URLs, and the real catalog is buried in a minified 3.7 MB bundle. The one machine-readable source is `cursor-agent --list-models`, where the knobs are encoded in the id suffixes. [`references/cursor-params.py`](../clink-brainstorm/references/cursor-params.py) peels the suffix vocabulary off each id and regroups; run it whenever Cursor ships new models. A measured run gave **193 ids → 31 base models**, and the ladders are genuinely irregular:

| base model | effort ladder | ctx | thinking | fast |
|---|---|---|---|---|
| `gpt-5.6-sol` · `gpt-5.6-terra` · `gpt-5.6-luna` | none < low < medium < high < xhigh < max | 1M | — | yes |
| `claude-opus-5` · `claude-opus-4-8` · `claude-opus-4-7` | low < medium < high < xhigh < max | 1M | yes | yes |
| `claude-fable-5` · `claude-sonnet-5` | low < medium < high < xhigh < max | 1M | yes | — |
| `gpt-5.5` | none < low < medium < high < **extra-high** | 1M | — | yes |
| `gpt-5.4-mini` · `gpt-5.4-nano` | none < low < medium < high < xhigh | — | — | — |
| `gpt-5.3-codex` · `gpt-5.2` | low < high < xhigh (**no medium**) | — | — | yes |
| `gemini-3.6-flash` | **minimal** < low < medium < high | — | — | — |
| `cursor-grok-4.5` | low < medium < high (**tops out at high**) | — | — | yes |
| `kimi-k3` | low < high < max (**skips medium and xhigh**) | — | — | — |
| `glm-5.2` | high < max (**starts at high**) | — | — | — |
| `composer-2.5` · `gemini-3.1-pro` · `gpt-5-mini` | none at all | — | — | varies |

The tier vocabulary is wider than it first looks — `none` and `minimal` are real rungs, and `extra-high` is a **two-token** rung distinct from `xhigh`. Both orderings of the suffixes occur: newer ids read `<base>-thinking-<tier>`, while 4.5/4.6-era ids read `<base>-<tier>-thinking`. Any parser has to handle both or it invents phantom base models — the first version of the script here reported 43 bases for exactly that reason.

**Cursor fails closed on an unknown model, which makes all of this cheap to verify.** An id it does not recognise exits `1` with `Cannot use this model: <id>` plus the full catalogue on stderr — verified live for a tier above a model's ceiling (`cursor-grok-4.5-xhigh`), a suffix on a model with no ladder (`composer-2.5-high`), and pure nonsense. **No silent fallback**, in pointed contrast to `agy`, which quietly ran its default model when `--model` was swallowed. So a wrong guess costs an error message, not a wasted call against the wrong model — and the error itself is a usable catalogue.

**Config-based selection (still valid):** pin `-m`/`--model`/`-c` in a client's `additional_args` (every call) or a role's `role_args`, or define multiple pinned clients (`codex-high.json`, `codex-fast.json`) selected via `cli_name`. **Restart PAL after any config edit** (cached at server start).

## The non-negotiable rule: verify everything they return

**A subagent's output is unverified until you prove it.** This is the whole discipline — a strong model behind a weaker agent harness still produces output you cannot trust on faith:
- Ran code? Run the test / execute it yourself.
- Edited files? Read the **diff**, then run the build/tests.
- Made a claim? Check it against the real code.
- **Check for side-effects, not just output equality.** A weaker agent (esp. qwen) can return *correct output* while mutating its input or leaving hidden state — an output-only test passes it. Diff, and assert the input is unchanged where it should be.
- **Run the real thing, not only the unit tests.** Unit tests pass a lot that a real build/boot rejects: a delegated (or your own) edit once passed `bun test` but broke `nest build` (an `import.meta` that the CommonJS build forbids) — only starting the server surfaced it. For anything that compiles/boots/serves, run the actual build + boot after verifying units.
- **A test you never saw fail is not evidence.** A green delegated change proves the suite passes, not that the suite would notice if the code were wrong — and when test and implementation are written in one pass, that is the default outcome. **Mutate the code the test covers and confirm it goes red**, then restore. Two mutations on `clone-space-mcp` PR #30 turned "27 tests pass" into actual evidence; without them the change would have merged with an assertion that passed while the file it checked was missing.

  **"Restore" needs a named mechanism, because the intuitive one deletes your work.** `git checkout <path>` and `git restore <path>` read from **the index**, not from the working tree — so on a file you have written and not yet staged they revert to the last commit and take the implementation with the mutation. Measured on `openclink` 2026-08-16: one revert silently removed **~60 lines** of new code, recoverable only because it was still in context. **Stage first (`git add`) so the revert restores your work**, or copy the file aside and copy it back. `git stash push --keep-index` also works. **The moment mutation testing is most useful is exactly the moment your work is not yet in the index**, so the rule steers you into the destructive case unless it says this.

  **And confirm the mutation applied.** A mutation the shell mangled produces the same zero-red as a mutation with no coverage gap, so a failed apply reads as a passing check. Assert the old text was found and the new text differs before you trust the result — the same session ran ~30 mutations and added that assertion after the first silent no-op.
- Antigravity especially: correct-*looking* but weaker — re-check the logic and **strip its `<SUMMARY>`** before using anything.

If your repo has agent operating rules (e.g. an `AGENTS.md`), a delegated subagent is bound by the same rules — and *you* are accountable for enforcing them on its output.

## Benchmark of record (re-run for your setup)

Snapshots that calibrated the rubric — **synthetic** plus **real tasks in a live repo** (T4-Fastwork as sandbox, 2026-07-16):

**Synthetic (coding):** `merge_intervals` + a `median` bug-fix (artifact) → 4/4 correct; Codex ~26–31s (clean), Antigravity ~21–30s (correct, always `<SUMMARY>`). In-place: Codex patched an `average()` empty-list guard, verified by running → ~50s.

**Real-repo (T4-Fastwork):**
- *Summarize a 30,696-char ledger → 5 bullets:* **Codex** 37s, input 50k (20k cached), result **~240 tok**, obeyed "only 5 bullets". **Antigravity** 38s, appended `<SUMMARY>`, ~375 tok. **Qwen/`claude-9arm`** (local) 64s, input **130k** (full CC harness, uncached) but free, ~464 tok, accurate + honest. Doing it myself ≈ **8.5k of *my* tokens**; delegating ≈ 240–464.
- *Adversarial review of a real regex fn (`tagForKey`); correct answer = no bug:* **Codex** (`codereviewer`) → `NO BUGS FOUND` in **19s**, 144 out — **correct** (no hallucinated false-positive), terse. **Antigravity** (`codereviewer`) → **failed at the time**: its harness tried a command tool that headless auto-denied → no review produced. **Re-tested 2026-07-30: it now works**, returning a severity-graded review with a refactor. Treat the whole ladder as a snapshot that ages — re-run it rather than quoting it.

**Difficulty ladder — the same task at all three, escalating, every artifact re-run to verify (2026-07-16).** This is the sharpest calibration: it finds *where each agent breaks*.
- **R0 trivial** (list a file's exports) → all three correct + terse (~19–36s). Floor.
- **R1 easy write** (a pure fn with a surrogate-pair trap) → all three correct (all knew the code-point idiom).
- **R2 moderate** (`mergeIntervals`, must merge touching + accept unsorted) → codex + antigravity correct **and side-effect-free**; **qwen correct output but MUTATED the caller's input** (aliasing) — the first crack, and an *invisible* one (output-only tests pass).
- **R3 hard, multi-step agentic** (write two files + run the test) → **codex ✅ full loop** (wrote, first run errored, **self-corrected**, verified); **antigravity ⚠️** wrote correct files but **couldn't run them** (headless command wall) → no self-verify; **qwen ❌ total failure** — ignored the given cwd, thrashed 13 turns writing to the repo root, sandbox-denied all, 0 files.
- **Breaking-point curve:** qwen cracks at R2 (subtle), shatters at R3 (agentic); antigravity is a solid *artifact* generator but breaks at "run it yourself"; **codex holds through R3** and sustained an ~11-min adversarial review that surfaced 3 real findings. Its ceiling is above this ladder.

**Takeaway:** Codex is the reliable default — top intelligence, follows tight output constraints, cheapest on *your* pool, no false-positive on a clean-code review. Antigravity is fine only for the trivial single-shot **`default`-role** leaf; its `codereviewer` role can no-op in headless. A local model is the free/unlimited option when you're offloading bulk, not chasing quality. **Snapshot — re-run if the CLIs/models change.**

## Gotchas

- **clink client config is cached at PAL server start.** Editing `conf/cli_clients/*.json` (e.g. changing a model or args) has no effect until PAL is restarted — don't conclude a change failed before restarting.
- **`command` must resolve from PAL's process env**, not just your shell. If a clink call errors "not found", use the absolute path to the exe in the config. The bare `gemini` CLI is **retired** → use `antigravity`. Note the env is snapshotted at process start: if an installer adds a directory to `PATH` *after* PAL (or your shell) launched, the running process still won't see it — check `PATH` at the User/Machine level before concluding the binary is missing, and restart rather than hardcoding a path.
- **On Windows, a bash `SHELL` inherited from the caller silently kills cursor's tools.** If the parent process exports `SHELL=…/bash.exe` — an MCP client may well do this — `cursor-agent` runs its internal commands through bash, they are Windows-shaped, and every tool call dies. `Read`, `Shell`, `Grep`, `Glob` and MCP access all fail, and **the agent answers from the prompt text alone with exit 0**, so the call looks successful while the client is effectively non-agentic. Fix per machine in `~/.pal/cli_clients/cursor.json` (a registry search path that survives `uv tool upgrade`) with `"env": {"SHELL": "C:/WINDOWS/system32/cmd.exe"}`. Established by A/B on one otherwise-identical command: bash fails, `cmd.exe` reads the file. **Windows-only, and cursor-only** — the same probe passed on `codex`, `antigravity`, `claude-9arm` and `claude` under the identical environment.
  Two traps sit on top of it. **`--auto-review` looks like the cure and isn't** — it is gated on account entitlement, and where unavailable it prints `Falling back to Allowlist` and changes nothing; it was briefly believed to be the fix because every validating run happened to have `SHELL` unset, so the bug could not occur. Do not validate a fix in conditions where the bug cannot reproduce. **And the agent misattributes the cause** — it blames a *"PreToolUse hook"* with a bash syntax error, repeatedly and convincingly, when no hooks file exists on the machine. The label is wrong; the mechanism it names (Windows commands under bash) is exactly right. A subagent's account of *why* it failed is a hypothesis like any other return value — dismiss the label, keep the lead.
- **Cursor's Max Mode is persisted, invisible to the caller, and expensive.** It raises the context ceiling to the model's maximum (up to ~1M tokens) and bills at token rates. There is **no CLI flag** — it is toggled by `/max-mode` in an *interactive* `cursor-agent` session and stored in `~/.cursor/cli-config.json` (`maxMode`, mirrored at `model.maxMode`), so every headless `-p` run inherits it, clink calls included. Left on after some unrelated interactive session, a routine delegation quietly becomes a token-billed one against the Other Models lane, with nothing in the clink response to explain the burn. Verify before a long run: `(Get-Content ~/.cursor/cli-config.json | ConvertFrom-Json).maxMode`. Worth turning on only when a delegation genuinely needs the larger window (a subagent reading a very large file set) — and turning back off afterwards. Distinct from the `-max` suffix in a model id, which is the effort tier and carries no such cost cliff.
- **A config `command` goes through POSIX-mode `shlex.split()`, which eats backslashes.** An absolute Windows path written the natural way (`"C:\\Users\\me\\tool\\x.cmd"` in JSON) is silently mangled to `C:Usersmetoolx.cmd` and fails as "not found in PATH" — the error names the mangled string, which is the tell. If you must hardcode a path, write it with **forward slashes**: `"C:/Users/me/tool/x.cmd"`. Applies to every clink client.
- **Harmless Codex noise:** its stderr often shows `rmcp … DELETE returned HTTP 404 session` — ignore it; check `return_code` and the content instead.
- **Antigravity's `codereviewer` role can no-op in headless.** It may invoke a command tool that headless mode auto-denies (`jetski: no output produced … required the "command" permission`) and return that error *instead of* a review — with `return_code: 0`, so check the **content**, not just the code. Safe fix: use `role: default` for Antigravity (its plain-Q&A path doesn't hit this), or grant that one tool a scoped allow-rule in the CLI's own settings. Codex's `codereviewer` role is unaffected.
- **Antigravity `--model` must come BEFORE `--print`.** `agy`'s `--print` is a **value-taking** flag (it consumes the next token as the prompt), so `agy --print --model "X" "<prompt>"` swallows `--model` as the prompt → agy runs with an empty model and **silently falls back to its default** (always reports *Gemini 3.5 Flash* regardless of what you asked). Correct order: `agy --model "X" --print "<prompt>"` (live-verified). This fork's Antigravity runner already emits that order and fails closed on a non-zero exit; if you hand-build an `agy` command, mind the order and check the exit code (an unsupported model exits `1` with a catalog).
- **Don't paste secrets** (`.env` values, tokens) into a clink prompt — you're sending to a third-party CLI/model. (During this work a GitHub PAT was found sitting in `~/.gemini/config/config.json` and echoed by an `agy` diagnostic log — audit those too.)
- **Latency is the real budget**, not (flat-rate) cost — a multi-delegation round is a multi-minute wall-clock operation. Parallelize, and don't delegate the trivial.

## See also

- **[`clink-brainstorm`](../clink-brainstorm/SKILL.md)** — the opinion/consensus counterpart (multi-agent fan-out + adversarial rounds).
- **[`karpathy-guidelines`](../../karpathy-guidelines/SKILL.md)** — the discipline to hold delegated work to (simplicity, surgical, verify).
