---
name: clink-brainstorm
description: Fan out a question to multiple independent AI agents (Gemini/Antigravity, OpenAI/Codex, Cursor, and optionally a further model of your choice) through PAL's clink tool, then synthesize their answers into one recommendation. Use for multi-agent brainstorming, getting a second/third opinion on a design or plan, sanity-checking a decision across model families, or when the user says "ask the other AIs", "brainstorm with multiple models", or "get other perspectives".
---

# clink-brainstorm

> **Requires [PAL MCP server](https://github.com/BeehiveInnovations/pal-mcp-server)** connected as an MCP server, with its `clink` tool configured for at least two independent CLI agents. This skill is a prompting/orchestration layer on top of `clink` — it does nothing standalone without PAL installed and reachable. See Prerequisites below.

Drive 3+ independent AI agents on the **same well-specified question**, then synthesize the answers yourself into one recommendation. This is "manual consensus" — PAL's native `consensus` tool cannot mix clink CLI agents with its own model provider roster, so the orchestration is done by hand, here.

## What this skill is, and what the other one is

Two skills sit on `clink`. They are not variants of each other, and the distinction decides every routing choice below.

| | What it is | What comes back |
|---|---|---|
| **`clink-brainstorm`** — this file | **an engineering committee.** Several senior agents put on the *same* codebase review or the *same* plan, then you synthesize | **judgment** — what is wrong, what to build, which approach wins |
| [**`clink-subagents`**](../clink-subagents/SKILL.md) | **`clink` used as your subagents.** You hand out chunks of the work and they come back done | **finished work** — an implementation, a refactor, a bulk transform, a first draft, a focused lookup |

**The consequence for routing, which is where this gets confused:** a panel's deliverable is reasoning, so **it takes the reasoning model every time** — `gpt-5.6-sol` at `medium`/`high`, and the small model that `clink-subagents` leans on has no place here. There you are buying throughput on verifiable leaves, which is a different purchase. **Do not carry a model or effort setting from one skill into the other.**

> **Cost figures below are AA cost-per-task in USD, written without a currency sign — do not add one back.** Loading a skill as a slash command with arguments performs shell-style positional substitution: a dollar sign followed by a digit is replaced by the corresponding word of those arguments, so an amount written the natural way renders as garbage precisely when an agent is reading it.

Want a design judged or a codebase reviewed by a panel → here. Want a subtask executed → `clink-subagents`.

## Prerequisites

This skill assumes [PAL MCP server](https://github.com/BeehiveInnovations/pal-mcp-server) is installed and connected as an MCP server, with its `clink` tool configured for at least two independent CLI agents. Out of the box, upstream PAL ships `gemini`, `claude`, and `codex` presets in `conf/cli_clients/`.

If you want the extra agents referenced below:
- **`cursor`** (Cursor's headless `cursor-agent`) needs no new code at all — `BaseCLIAgent` already pipes the prompt over stdin and appends `--model`, which is exactly its interface. It is a `constants.py` entry plus a config file, both shipped in the fork below. Fixed args are `-p --trust --output-format text`: `--trust` is mandatory or a non-interactive run in an unseen directory aborts with *"Workspace Trust Required"*, and its JSON shape is not Claude Code's so `claude_json` cannot parse it.
- **`antigravity`** (Google's Gemini-CLI successor, `agy`) needs a small platform-specific fix — plain piped subprocesses get empty output from `agy` unless it's driven through a real pseudo-console. A ready-made fix (Windows, via `pywinpty`) lives in [this PAL fork](https://github.com/xenodeve/pal-mcp-server) — see its `CHANGES-FORK.md`.
- **A third model behind an alternate gateway** (this doc uses `claude-9arm` as a running example — Claude Code CLI pointed at a non-Anthropic OpenAI-compatible backend via `--settings`/`--model`) is just a config file, no code — see the same fork's `conf/cli_clients/claude-9arm.json.example`. Swap in whatever gateway you actually use; the pattern is generic.

None of this is required to use the skill — two or three agents from any mix of `clink` CLIs (or PAL's own `chat`/`consensus` for a non-agentic angle) is enough for a brainstorm round. Adjust the example `cli_name`s below to whatever you actually have configured.

## Available agents (example roster — adjust to your setup)

| Call | Backend model | Cognitive lens | Mechanism | Typical latency |
|---|---|---|---|---|
| `mcp__pal__clink(cli_name="antigravity")` | Gemini via Google's `agy`. Roster: Gemini 3.6 / 3.5 Flash (High\|Medium\|Low), **Gemini 3.1 Pro (High\|Low)**, plus Claude Sonnet/Opus 4.6 (Thinking) and GPT-OSS 120B | **System-centric** — big-picture integration, cross-file deps, directory structure | ConPTY-driven subprocess (see fork) | ~20-25s |
| `mcp__pal__clink(cli_name="codex")` | OpenAI Codex — **`gpt-5.6-sol` only here**, at `medium`/`high` | **Code-centric** — syntax correctness, implementation details, edge cases | subprocess, `--json` | ~10-15s for a trivial prompt, but **400-530s for a read-heavy round** against a real repo (measured 2026-07-31, recorded in `xeno-skills` issue #55) — budget minutes, not seconds |
| `mcp__pal__clink(cli_name="cursor")` | Cursor's `cursor-agent` — the widest roster of any client: **Grok 4.5** (xAI), **Composer 2.5**, **Kimi K3 / K2.7 Code** (Moonshot), **GLM 5.2** (Zhipu), plus Opus/Sonnet/Fable, the GPT-5.x line, and Gemini | **Breadth-centric** — the only route to the xAI / Moonshot / Zhipu families | subprocess, `-p` + prompt over stdin; on Windows genuinely agentic **only if its config overrides `env.SHELL`** — a bash `SHELL` inherited from the caller makes its tools fail silently and it degrades to a text-only responder (see `clink-subagents` gotchas) | ~25-30s even for a trivial prompt |
| `mcp__pal__clink(cli_name="claude-9arm")` (example name — use your own gateway config) | any model your gateway exposes | **Logic-centric** — reasoning soundness, efficiency, logical consistency | subprocess, real `claude` CLI routed through `--settings`/`--model` | ~8-10s |
| `mcp__pal__chat(model=<your-provider-model>, ...)` | same model as above, direct PAL route — no clink | **Conceptual-centric** — broad ideas, theory, alternative approaches (non-agentic) | PAL's own provider call | usually faster, no CLI bootstrap overhead |
| `mcp__pal__clink(cli_name="claude")` | Anthropic Claude | general | subprocess | upstream default preset |
| `mcp__pal__clink(cli_name="gemini")` | — | — | **dead as of mid-2026** — Gemini CLI binary was retired in favor of `agy`/Antigravity. Re-confirmed 2026-07-30: the preset still loads, but the call fails with `Executable 'gemini' not found in PATH` | n/a |

The **cognitive lens** column matters most during adversarial rounds (see below) — when you need to challenge a consensus, tailor each agent's probe to its natural strength rather than sending the same generic "find flaws" prompt to everyone.

If a clink agent and `chat` hit the **same underlying model**, they are NOT interchangeable — `chat` has no file/tool access at all (a single-shot text completion via PAL's provider routing), while a `clink` CLI agent is a full agent loop that can genuinely read real files (verified: a real repo file was correctly read and quoted back, with `num_turns: 2` in the response confirming an actual Read-tool round-trip, not a guess). **This changes which one belongs in a brainstorm round:**
- **Question is about the actual codebase** (review an implementation, verify a claim against real code, anything where "read this file" would help) → use the agentic `clink` agent, not `chat`. `chat` literally cannot check anything against the real repo — asking it a codebase question makes it guess from whatever text you pasted, with no verification.
- **Question is purely conceptual/architectural** (answerable without touching a file) → `chat` is fine and faster (no CLI bootstrap tax).
- If unsure, default to the agentic `clink` call — it can still answer conceptual questions fine, just costs a bit more latency; the reverse (using `chat` when the question needed real files) silently produces a worse-grounded answer with no error to signal it.

**The third state, and it is worse than either: an agentic agent told not to read files is `chat` with worse latency.** Picking the agentic client satisfies the rule above and then `"Do NOT read files; everything you need is below"` undoes it — you pay the CLI bootstrap and get `chat`'s blindness, having followed the rule.

**Measured, one round, same question, same models, 2026-08-11.** Blind, all three designed a transport-neutral authorization platform and a pre-publication claim checker — **neither can exist in this repository**. One agent then ignored the instruction, read eleven files (351 s, 426k input tokens), **withdrew its own enforcement phase** citing that fact, and produced the cost ranking that replaced the plan. The difference was file access and nothing else.

**When the feasibility ceiling and the codebase rule conflict, the codebase rule wins.** *"A read-heavy delegation takes 400–530 s against a real repo; under a 60–120 s transport ceiling that is infeasibility, not latency"* is the reason suppressing reads looks sensible — and the 351 s round above **exceeded the ceiling, was backgrounded, completed anyway, and was the only round worth having.** So handle a long round by **expecting** it, not by blinding the agent: fire it, let it background, take other work.

**If reads genuinely must be suppressed — a purely conceptual question with no repository in it — say so in the prompt as a decision**, with the reason. A later reader can then tell a deliberate choice from an unexamined default, which could not be told here.

## Why you can't just call `consensus` with all of them

`mcp__pal__consensus`'s `models[]` roster only accepts PAL-configured provider models — it has no concept of a clink CLI agent (they live in a completely separate registry: `clink/registry.py` + `conf/cli_clients/*.json`). There is no single tool call that spans both. Orchestrate manually instead (see below).

## The delegation contract — build the request before you call (#215)

Every `clink` delegation carries a **`BrainstormRequest v1`** and comes back as a
**`BrainstormResponse v1`**. The shapes are in
[`references/request-v1.md`](references/request-v1.md) and
[`references/response-v1.md`](references/response-v1.md), with worked examples under
[`references/examples/`](references/examples/). They are not inline because this file is
already large and the master pays for its size on every load.

**Required going out:** `protocol`, `version`, `problem`, `objective`, `scope.exclude`,
`questions`. **Required coming back:** `decision_status`, `confidence`, and the sections
`Summary`, `Findings`, `Recommendation`, `Evidence boundary`.

**Two of those are the point.** `decision_status: needs_user_input` **stops implementation** —
without it a recommendation about product behaviour reads exactly like one about an
implementation detail. And `Evidence boundary` states what the worker did *not* check:
omitting a risk that does not exist is honest, and omitting what was never checked is
indistinguishable from having checked it.

**`permissions.execute_commands` defaults to `false` for a measured reason** — antigravity
cannot run shell through this transport and returns the permission error *instead of* its
output with `return_code: 0`.

## How to run a brainstorm round

1. **Write one precise question/proposal** — the same exact prompt goes to every agent. Vague or drifting prompts make answers incomparable. State the question, relevant constraints, and what kind of answer you want (recommendation, critique, risk list, etc.) — these agents have **zero context from your conversation**, so include everything they need to answer standalone (paths, prior decisions, what's already been tried).
   **Audit the prompt before it is sent — convergence measured on a leading question is worthless.** Four questions, answerable in seconds, and a *yes* to any of the first three is a defect in the prompt rather than a risk to note:

   - **Does it supply one of the candidate answers as a phrase?** On 2026-08-11 a prompt asked whether a change was *"the right next move, or displacement activity while the mechanism has four known bypasses"*. Three agents on three model families converged on displacement. Under the adversarial round all three reversed, and one wrote back `"self_critique": "I walked into the offered displacement slot"`.
   - **Does it label one option?** That prompt attached *Major/security* to the competing option before anyone read it. The panellist who named the cause: *"three panellists under that frame 'independently' choosing B is not triangulation."*
   - **Does it state your own position, or which answer you expect?** Including the order the options are listed in.
   - **Would a reader who saw only this prompt know which answer you wanted?** If yes, the round measures your framing.

   **When the audit fails: rewrite and re-fire** — the round has not cost anything yet. If rewriting is genuinely not possible, **fire it anyway and mark the result `convergence unverified`**, so the synthesis carries the caveat instead of the reader inheriting an unmarked one.

   **Both checks run before the call, which is the half the forced adversarial round cannot supply** — see *When agents converge*.
   **Then scope the terms the answer turns on.** The audit above catches a prompt that supplies an answer; this catches one that supplies none and leaves a word to be filled in. **A neutral prompt can still be under-specified, and that produces convergence just as reliably.**

   **For each term the answer depends on: would two competent readers scope it the same way?** Where they would not, add a sentence saying which reading applies.

   **Measured, 2026-08-13.** A round judged a plan for a review agent whose job was described as *"asks whether the invoked skills' **rules were followed**"*. Three agents on different model families **all resolved that toward outcome** — is the code good — concluded that session history cannot establish outcome, and two refused to build parts of the design. The developer rejected it in one sentence: the reviewer checks **whether the prescribed workflow was followed**; code quality is CI's job. **The panel was not wrong about the question it answered. It answered a different one.**

   **The tell is that there is no tell.** That prompt carried measured constraints, file paths, three named options and a word count — **one noun with two readings inside an otherwise precise brief**, and unanimous agreement on the wrong reading looks exactly like unanimous agreement. So the check is on the **terms**, not on the prompt's overall quality — precision was never the thing missing.
## Dialing model + effort per call (this PAL fork)

2. **Fire agents in parallel** — put multiple tool calls in a single message (independent calls, no shared state) rather than sequentially. Sequential stacks latencies; parallel is bounded by the slowest single agent. **And a round past two minutes is moved to a background task, at which point it is not a reason to wait** — start synthesising what has already returned, or take other work; the notification will find you. A panel fired in one message pays that block once for the whole round.
   - **Codebase question** (needs real file access — see the `chat` vs agentic split above) — use your agentic clink agents, not `chat`:
     ```
     mcp__pal__clink(prompt=Q, cli_name="antigravity")
     mcp__pal__clink(prompt=Q, cli_name="codex")
     mcp__pal__clink(prompt=Q, cli_name="claude-9arm")
     ```
   - **Purely conceptual question** (no file grounding needed) — `chat` is fine and adds a free extra angle since it usually returns fastest:
     ```
     mcp__pal__clink(prompt=Q, cli_name="antigravity")
     mcp__pal__clink(prompt=Q, cli_name="codex")
     mcp__pal__clink(prompt=Q, cli_name="claude-9arm")
     mcp__pal__chat(prompt=Q, model=<your-provider-model>, working_directory_absolute_path=<project root>)
     ```
   Either way, if a clink agent and a `chat` call are the same underlying model, treat that pair as one vote when weighing convergence, not two independent ones.
3. **Read each response for what it actually says**, not just whether it returned 200. Note where they agree (signal — independent agents converging is real validation), where they diverge (the interesting part — dig into *why* before picking a side), and any agent that clearly misread the question (these may be smaller/different models than your main one; treat their output as input to your judgment, not a vote to average blindly).
4. **Synthesize and present your own recommendation** — don't just paste the raw responses at the user. State what the agents converged on, what they disagreed about, and your own read on which is right and why (you have the full session context they don't).
5. **Use `continuation_id`** (returned in each clink/chat response) to follow up with the *same* agent in the *same* thread if you want to push back or ask a clarifying question — it preserves that agent's prior context, so you don't have to re-explain the whole question from scratch.


The [xenodeve PAL fork](https://github.com/xenodeve/pal-mcp-server) adds two **optional per-call** `clink` params — `model` and `reasoning_effort` — so you can tune each agent's capability *per round* without editing config (which is cached at server start). For brainstorming this is a real lever: match depth to the question, and widen cognitive diversity by routing an agent to a different backend family.

`mcp__pal__clink(prompt, cli_name, model?, reasoning_effort?, role?, continuation_id?)`

| Back-end | `model` (per call) | `reasoning_effort` (per call) |
|---|---|---|
| `codex` | ✅ `-m` — **`gpt-5.6-sol` for every brainstorm round** (the panel's output is reasoning; the small model is a `clink-subagents` instrument) (validated; invalid → 400) | ✅ `low\|medium\|high\|xhigh\|max` — **`medium` by default, `high` for the round that matters; `xhigh` and `max` are past the value cliff** |
| `antigravity` | ✅ `--model "<label>"` — the label exactly as `agy` lists it, e.g. `Gemini 3.1 Pro (High)`, `Claude Opus 4.6 (Thinking)` | ✅ `--effort low|medium|high` — real, but **mutually exclusive** with `--model`; agy refuses the pair for every model it serves, and the tiered label (`(Low/Medium/High)`, `(Thinking)`) is the other way to say it. PAL refuses the pair before spawn (`pal-mcp-server#43`). |
| `cursor` | ✅ `--model` — id form, e.g. `cursor-grok-4.5-high`, `kimi-k3-max`, `composer-2.5`, `gpt-5.6-sol-xhigh` | ➖ baked into the model id, **ladder differs per model** — derive it with [`references/cursor-params.py`](references/cursor-params.py) rather than assuming a suffix exists |
| `claude-9arm` | ✅ `--model` — limited to what the gateway serves | ❌ no-op (this gateway has only thinking on/off) |

Omit both → the CLI's config default. (`mcp__pal__chat` takes its own `model` param directly.)

**Four scales are in play and none converts into another.** Ranking a number from one against a number from another produces a false ordering, so every figure here states its scale.

| Scale | Where it appears | Can you act on it directly? |
|---|---|---|
| **Coding / Agentic sub-index** (older) | `clink-subagents`' routing rubric | no — comparative, and a different population |
| **AA Intelligence Index v4.1** | the `Index` column below | no — comparative only |
| **Coding Agent Index v1.3** | harness x model pairs, in [`clink-masteragent`](../clink-masteragent/SKILL.md) | no — a third population again |
| **Subscription credits** | what a round actually costs your weekly cap | **yes — this is the only one you spend** |

<!-- figures:start source=docs/research/data/aa-models-augmented.csv -->

The rungs this skill routes to, and the two it refuses. `Index` is AA Intelligence
Index v4.1; `Burn` is AA cost-per-task in USD, a proxy for quota burn since codex is
subscription-flat; `Cost/pt` is the suite cost divided by the index, **lower is better
value**. The source lives in the `xeno-skills` repo and is **not shipped with the
installed skill**. The full ladder including the small model is in
[`clink-subagents`](../clink-subagents/SKILL.md) — this table is the panel seat only.

| Rung | Index | Burn | Cost/pt | Used here |
|---|---|---|---|---|
| `gpt-5.6-sol` `medium` | 53.6 | 0.514 | 13.01 | yes — to surface positions |
| `gpt-5.6-sol` `high` | 55.9 | 0.771 | 20.75 | yes — the round that matters |
| `gpt-5.6-sol` `xhigh` | 57.7 | 1.167 | 32.31 | no — past the value cliff |
| `gpt-5.6-sol` `max` | 58.9 | 1.862 | 58.46 | no — past the value cliff |

<!-- figures:end -->

**Brainstorm-specific use:**
- **Codex here is `gpt-5.6-sol` at `medium`, escalating to `high` for the round that matters. Nothing below, nothing above.** The two rungs and the two refusals are in the table above; this bullet does not restate their values.

  **Why there is no small-model option here.** This skill convenes a panel of engineers to review a codebase or judge a plan — **the deliverable is reasoning**, so it takes the reasoning model. `gpt-5.6-luna` is a `clink-subagents` instrument, for when clink is doing *work*; a round whose entire output is judgment has nothing to gain from it.

  **Why the range stops at `high`.** Read it off the `Cost/pt` column above, where lower is better: 13.01 at `medium`, 20.75 at `high`, then 32.31 and 58.46. **Value halves twice over the two rungs the cap refuses** — `max` costs about 4.5× as much per index point as `medium` and buys 5.3 points. Over a 3-round loop that is nine calls, and moving *the codex seat alone* from `medium` to `max` multiplies **its** burn by 3.6× — the other seats are unaffected, so this is a codex-lane cost, not a loop-wide one.
- **Widen the *model* spread, not just the CLI spread.** Real cognitive diversity comes from *different backend families*, not the same model three times. A strong cheap round: `codex` → `gpt-5.6-sol` at `medium`, `antigravity` → `Gemini 3.1 Pro (High)`, `cursor` → `cursor-grok-4.5-high`, gateway model via `claude-9arm` — four genuinely different lineages in one fan-out. Pick the client by **whose quota it spends**, not merely by whether it carries the model — see *Quota routing* below.
- **Steep diminishing returns on effort.** The four rungs in the table span 5.3 index points while the burn rises more than threefold, and the last rung alone costs about 60% more than the one below it for roughly a point. That is why `medium`/`high` is the whole usable range and `xhigh`/`max` are capped out. Blanket-`max` on a 3-agent × 3-round loop is a multi-minute, quota-heavy operation for almost no marginal signal.
- **Don't assume a higher tier buys accuracy — measure it on your own tasks.** A same-prompt A/B on `cursor-grok-4.5-low` vs `-high` (two probes: a 6-step modular-arithmetic chain, and "list every defect a caller could hit" on a function that sorts its argument in place) produced **no observable difference**: both tiers got the arithmetic right, both led their defect list with the in-place mutation, and latency overlapped (46–55s either way). Note the ceiling that test was working against — Grok 4.5's ladder stops at `high`, so it was the shortest ladder available. Treat the result as scoped: *no difference on mid-difficulty work at the top of a 3-rung ladder*, not evidence the knob is inert. The house-lane models are exactly the ones with short ladders, so a test that would actually separate the tiers costs the foreign lane.
- These per-call params are the **only** way to vary model/effort without restarting PAL — reach for them instead of editing `conf/cli_clients/*.json` mid-session.

## Quota routing — pick the client by whose allowance it spends

Most models are now reachable from **more than one client**. Choosing on availability alone quietly drains the scarcest pool first.

**`antigravity` and `cursor` meter the same way: a cheap in-house lane and a faster-draining foreign lane, billed as two independent pools.**

| Client | House lane (cheap) | Foreign lane (drains faster) |
|---|---|---|
| `antigravity` | Google — every Gemini model | non-Google — Claude Sonnet/Opus 4.6, GPT-OSS 120B |
| `cursor` | Cursor Models — *only* `cursor-grok-4.5-*` and `composer-2.5` | Other Models — Opus/Sonnet/Fable, GPT-5.x, Gemini, Kimi, GLM |

Because the lanes are metered separately on **both**, spending a house lane costs its foreign lane nothing. So Gemini on `agy` and Grok 4.5 on `cursor` are **two independent cheap lanes**, and with `codex` on its own subscription you have three before touching anything scarce. (On Cursor the separation is one-way rather than a wall: usage past the Cursor Models limit spills into the Other Models pool or on-demand spend.)

**Refill cadence matters as much as pool size.** Cursor meters **monthly**, with no 5-hour or weekly rolling window — so a burst cannot trip a short-window wall mid-round, and its practical headroom exceeds a rolling-window client's even when the bars look comparably full. Its house lane (Cursor Models) is also allocated the larger share of its two. Clients on rolling windows have to be paced across a long loop; Cursor does not.

**Cursor's Max Mode is persisted state that `clink` can neither set nor see.** Max Mode raises the context ceiling to the model's maximum (up to ~1M tokens) and bills at token rates. There is **no CLI flag** for it: it is toggled by `/max-mode` inside an *interactive* `cursor-agent` session and stored in `~/.cursor/cli-config.json` (`maxMode`, mirrored at `model.maxMode`), so every headless `-p` run — every clink call included — silently inherits whatever that file last said. Left on, ordinary rounds become token-billed ones against the foreign lane, and nothing in the call or its response reveals why. Check it before a long session:

```
(Get-Content ~/.cursor/cli-config.json | ConvertFrom-Json).maxMode    # want: False
```

Brainstorm prompts are a few KB, so the context ceiling almost never earns its cost here — leave it off, and reach for it only if a single probe is genuinely context-bound. Note this is a **different axis** from the `-max` suffix in a model id (`…-low` / `-medium` / `-high` / `-xhigh` / `-max`), which is the effort tier and is safe to select per call.

The rule that falls out: **prefer each client's house lane, treat both foreign lanes as scarce** — never route a model through a client that carries it only in the foreign lane when another client has it in-house. And when a round is *bursty* — a wide fan-out, or a loop-until-dry that could run many rounds — lean the volume onto Cursor, which cannot wall mid-loop, and spend the rolling-window clients on the calls that most need them.

| Family you want | Ask | Why |
|---|---|---|
| Gemini | `antigravity` | agy carries Gemini in-house; `cursor` carries the same models only in its foreign lane. |
| Grok 4.5 · Composer 2.5 | `cursor` | Their own Cursor Models pool — the cheapest agentic lane you have. |
| Kimi K3 · GLM 5.2 | `cursor` (sole source) | Costs Other Models quota. Spend deliberately — one targeted probe, not a whole round. |
| GPT-5.x | `codex` | Its own subscription, with a real `reasoning_effort` knob. Both other clients carry GPT only in a foreign lane, so routing it there is a worse-controlled call *and* a scarcer spend. |
| Claude | usually neither | You are already Claude. Paying quota for a same-family echo yields the least new information of any option available. |

**One client fills several seats — a panel's width is bounded by models, not by clients.** `cli_name` names the **client**, not the model. Several `clink` calls with the *same* `cli_name` and different `model` values, in one message, run in parallel. `cursor` alone reaches Grok 4.5, Composer 2.5, Kimi K3, GLM 5.2, the GPT-5.x line, Gemini and the Claude family; `antigravity` reaches every Gemini plus Claude Sonnet/Opus 4.6 and GPT-OSS 120B. **Grok 4.5 + Kimi K3 + GLM 5.2 is one message and three genuinely different lineages, all through `cursor`.**

It compounds with the pool split above: `cursor`→Grok spends the house lane while `cursor`→Kimi K3 spends the foreign one, so **a single client draws on two independent pools in the same round.** The house-lane preference is unchanged — it still decides *which* client a given model should be reached through.

**The caution that rides with it:** Kimi K3 and GLM 5.2 share the **same** foreign pool, so calling both in one round drains it twice rather than once from each of two. Spend a foreign lane when a different vendor's prior is the actual point, never to pad a seat count.

**Default cheap round:** `codex` + `antigravity`(Gemini) + `cursor`(Grok 4.5) — three lineages across three independent billing lanes, none of them touching an expensive pool. Add `claude-9arm` if your gateway is flat-rate.

**Escalate to Kimi K3 / GLM 5.2 only when a round has already converged** and you need a genuinely foreign prior to break the agreement. That is exactly the forced-adversarial situation below, and it is the one time the Other Models pool is worth spending.

## Round 2+: bounded judge-led challenge loop

A single round (independent parallel answers) is the default. For a genuinely consequential decision where round 1 produced real disagreement, run a **bounded challenge loop** instead of accepting round 1 as final — but **you (the orchestrating agent) are the judge and the stop condition**, not the sub-agents:

1. **Round 1** as above — same question to all agents, in parallel.
2. **You synthesize**: convergence (agents agreeing independently = signal), divergence (the interesting part), anything one agent caught that the others missed.
3. **Round 2 — write one challenge prompt per agent**, reusing that agent's own `continuation_id` (separate thread per agent, do NOT mix). The challenge must:
   - **Quote the other agents' actual claims and reasoning, not a vague "others disagreed."** Specific quotes ("Reviewer B recommended X because Y") is what makes the next round sharpen instead of restate. Generic "what do you think now?" gets a generic non-answer.
   - **Ask explicitly whether they revise or stand firm, and why** — give them room to concede with new reasoning, not just cave to majority.
   - **Surface what the OTHER agents caught that this agent didn't mention**, and ask them to react to it specifically.
4. **You synthesize again** — check whether round 2 produced genuinely new information (positions moved, reasoning sharpened) or was dry (just repeated round 1). Real convergence looks like: agents narrowing from "3-way disagreement" to "agree on the bookends, one narrow wrinkle left" — that's a sign the loop is working, not stalling.
5. **Default cap: 2 rounds of challenge (3 rounds total including round 1).** This is not a cost-driven limit if your backends are flat-rate subscriptions — it's there because **dry rounds are the actual stop signal, and a cap is just the safety valve for when a loop fails to self-terminate.** Stop *before* the cap whenever either hits: (a) positions have converged enough that you're confident making the final call, or (b) a round comes back dry (no new reasoning, just restated positions). If a round is still producing real movement, it's fine to go a round further; raise the cap explicitly with the user rather than silently looping past it. Looping past *dry* is the actual waste, not looping past some fixed round count.

## When agents converge — forced adversarial round

**The prompt audit in step 1 is this section's other half, and it runs first.** This one treats convergence as a property of the agents and applies pressure after the fact — which works, and cost a full extra round on 2026-08-11. The audit asks the same question before the call, when a rewrite is still free.

**Convergence is not automatically a validation signal.** Agents trained on similar data, given the same prompt framing, or that are inherently agreeable can all arrive at the same answer for the wrong reasons. When round 1 shows all or most agents agreeing, run one **forced adversarial round** before treating it as confirmed — the goal is to find out if the consensus survives targeted pressure, not just to generate dissent for its own sake.

### How to run it

1. **Detect convergence** — round 1 responses all agree on the same core recommendation (or all agree "this is fine, no issues"). Note: partial convergence (2 of 3 agree, 1 diverges) should go to the challenge loop instead; the adversarial round is for when disagreement didn't surface naturally at all.

2. **Send one adversarial probe per agent via their `continuation_id`** — each agent already has the question context, so you only need to add the adversarial task. **Tailor the probe to each agent's cognitive lens:**

   - **Codex (Code-centric):** *"All agents agreed on [X]. Your task is NOT to defend this. Find implementation-level flaws: syntax traps, missed edge cases, off-by-one errors, race conditions, anything the code would actually do wrong at runtime that the consensus didn't address."*
   - **Antigravity (System-centric):** *"All agents agreed on [X]. Your task is NOT to defend this. Find system integration problems: dependency conflicts, cross-file side effects, infrastructure assumptions that don't hold, or directory/import issues that only show up in a real deployment context."*
   - **Claude-9arm (Logic-centric):** *"All agents agreed on [X]. Your task is NOT to defend this. Find logical inconsistencies: places where the reasoning doesn't hold, efficiency problems, hidden assumptions that break under pressure, or scenarios where the approach fails even if the code is syntactically correct."*
   - **Qwen via chat (Conceptual-centric):** *"All agents agreed on [X]. Your task is NOT to defend this. Propose the strongest alternative approach that the consensus didn't consider — a different conceptual frame, a competing design, or a fundamentally different way to solve the problem that might be better."*
   - **Cursor → Kimi K3 or GLM 5.2 (Foreign-prior):** *"All agents agreed on [X]. Your task is NOT to defend this. State plainly where you would have answered differently and why, then name the strongest concrete objection the group appears to have no way of seeing."* Reach for this only when the other lenses come back dry — a model trained on a different corpus is the one probe that can break an agreement rooted in shared priors rather than in evidence. It also costs the Other Models pool, so it is a deliberate escalation, not a default fourth probe.

   Fire all four in parallel (same as round 1 — independent calls, separate `continuation_id`s, one message).

3. **Read for real dissent vs. surface dissent** — after an adversarial prompt, every agent *will* find something to say. The question is whether it's a real flaw or a manufactured one:
   - **Real dissent:** concrete, specific (names a line, a scenario, a condition), and would actually matter if the consensus were acted on
   - **Surface dissent:** vague ("there might be edge cases"), hedged ("could potentially have issues"), or generic ("always consider testing") — this is agents being compliant with the "find flaws" instruction, not genuinely surfacing a problem
   - A dry adversarial round (all surface dissent, nothing concrete) confirms the consensus. A round with at least one concrete flaw feeds into the challenge loop as new disagreement to resolve.

4. **Stop condition:** if the adversarial round comes back dry (all surface dissent), accept the consensus and say so explicitly. If it finds real dissent, run one normal challenge loop round (step 3 of the challenge loop above) to resolve it — the adversarial round is one pass, not a new loop of its own.

**The synthesis states which loop steps ran.** One line — *round 1 · adversarial round · resolving round · synthesis* — each marked ran or skipped-with-reason. **The resolving round is the only step whose absence looks identical to its completion**: its output would have been folded into the same synthesis, and every other step leaves something behind.

**Reversal on different axes is not dissent against a consensus, and it is the case most likely to leave a contradiction standing** — it reads as agreement that round 1 was wrong and is agreement about nothing else. On 2026-08-11 all three reversed, on architecture, sequencing and cost, and two ended in direct contradiction — *"pre-execution interception is the wrong layer"* against *"the matcher change is the cheap, correct fix and should be done first"* — never made to meet.

**When the orchestrator holds verified evidence the panel could not reach, the resolving round may be waived — on condition the waiver and the evidence are named in the synthesis.** Above, the contradiction was settled by a fact neither panellist had: a merge through `mcp__github__merge_pull_request` produces no local `git push`, so a pre-push hook can never observe it. **The resolution was probably right. It was still a documented step replaced by private judgment, undisclosed** — and naming it costs one sentence.

**A synthesis that skipped a step and did not say so is what `clink-debug` already refuses** — *"'Fixed' after a hunt that never falsified anything is a hypothesis wearing a verdict's clothes."*

### Why this matters

The cognitive diversity of the agents means their *blind spots are also different* — Codex that agreed on an architecture might have missed the system integration problem that Antigravity would have caught, but didn't catch because it was also going through the same prompt lens as the others in round 1. The adversarial round exploits this by forcing each agent to search specifically in its own strongest domain, rather than a generic "find problems" sweep that any agent might answer generically.

## Latency is usually the real constraint, not cost

If your backends ride flat-rate subscriptions you're already paying for (rather than metered per-token billing), the `total_cost_usd` figure some tools report in responses is just internal accounting against a configured rate — it doesn't reflect money actually charged. Check your own setup before assuming either way.

**What's usually real is latency**:
- A CLI-driven agent's own session bootstrap (reading project context, system prompt injection) adds real tokens/time before it even starts on your question — larger real questions take proportionally longer.
- Agents that explore their working directory before answering (common for agentic CLIs) add tens of seconds per call.
- A 3-round, 3-agent challenge loop is a multi-minute wall-clock operation. That's the thing to budget for.

**Reach for this when the decision is worth the wait** — architecture calls, "am I missing something obvious", cross-checking a plan before a big/risky change. Don't use it for things a single careful pass already answers confidently — not necessarily because it costs money, but because burning minutes of wall-clock on a low-stakes question is its own waste.

## Giving a clink agent one of your skills

You can make a clink agent follow one of your own skill's rules for a task — useful when you want it held to the same discipline (a style guide, a refuse-gate, a checklist) rather than answering freely.

**If the round's question is *why is this broken*, stop and read [`clink-debug`](../clink-debug/SKILL.md) first.** It owns every rule about hunting a bug across these skills — which seats may sit in a falsification round, what evidence must reach them, and when a panel is the wrong instrument entirely. Convening one from here without it is how a panel returns a confident cause nobody reproduced.

**Self-discovery is unreliable — don't rely on it.** Telling an agent "use the Skill tool to invoke X" produces inconsistent results because most clink agents have no skill system of their own that maps to yours:
- Some agentic CLIs with full filesystem access may go find and read your skill file on their own initiative if asked to.
- CLIs with their own separate skill/plugin system typically check that system, don't find your skill there, and give up without trying to read the raw file.
- Routing the *same* underlying model through a full agent loop (`clink`) vs. directly can behave inconsistently for this specific ask — don't assume they behave identically.

**The reliable method: paste the skill's content directly into the prompt.** Read the skill file yourself (full or a distilled excerpt, either works) and include it verbatim in the `prompt` you send, with a short framing line like *"Follow this skill for the rest of this conversation (full content sent directly, no file to find): ---\n<skill content>\n---"*. This works regardless of the target agent's own tooling and doesn't depend on filesystem access. It reliably works for both simple rule-following (an agent correctly cites specific rule names and applies them to a scenario, not just parrots the text back) and conditional gates (an agent correctly refuses a request that's missing required inputs per the pasted rules, quoting exactly which items are unmet — a harder test, since the natural instinct is to be helpful and act anyway despite the constraint).

**Data handling — decide your own policy before sending project content to a third-party model.** Whether sending your project's source/architecture/skills to a clink agent needs case-by-case gating is a call only you can make based on what's actually in your repo and who's authorizing it. If nothing in your codebase is confidential beyond literal secret values (API keys, tokens in `.env` or config files), it's reasonable to send ordinary project/skill content without asking each time — just never paste literal credential values into a clink prompt.

**One hard constraint that some coding-agent platforms won't let you waive by consent:** Claude Code's own auto-mode permission classifier hard-blocks the `absolute_file_paths` parameter on `clink` when it points into a repo's source, even with explicit user consent, and blocks attempts to write a skill policy that tries to pre-waive it. If you hit this, don't try to route around the classifier — treat it as a genuine constraint, not a negotiation.

**The working alternative for giving a clink agent real file access:** put the file path in the prompt *text* and ask the agent to read it with its own tools, instead of using a dedicated file-path parameter — e.g. *"Read this file directly using your own file-reading tools: /path/to/file.py, then answer: ..."*. This works because it's the agent's own initiative/tooling reading the file, not the orchestrator handing over a flagged parameter. Prefer this over paraphrasing when accuracy matters — a paraphrase risks losing detail you didn't think to include; direct file reads don't have that gap. Note that some agentic CLIs (ones with standing filesystem access via a bypass-approvals flag) will go read the real file on their own initiative regardless of what you send them — don't assume a careful paraphrase keeps them from seeing the real file.

## Known gotchas

- **A retired/replaced CLI binary stays dead** — if a vendor swaps CLI tools (e.g. Gemini CLI → Antigravity's `agy`), the old `cli_name` won't come back; route to the successor instead and update your config.
- **Clink CLI-client config is typically cached at MCP-server process start, not read per-call.** If you edit `conf/cli_clients/*.json` or the agent registry, the running server won't see the edit until it's restarted. Don't conclude a fix didn't work until you've restarted and retested.
- **A clink CLI agent only resolves if its `command` field is reachable from the *server's* process environment, not just your interactive shell.** A CLI that works fine in your terminal isn't automatically visible to a long-running or freshly-spawned server process — if a clink call fails with "not found in PATH", swap the config's bare command name for a full absolute path to the executable.
