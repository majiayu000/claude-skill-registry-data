---
name: select-llm-model
description: >-
  Recommend which LLM to use for a task. Use when asked which model or best LLM
  for X, to pick a model, or for a shortlist ranked on live leaderboard evidence
  (coding, reasoning, agentic, tool-use, price, speed). Fetches leaderboards and
  cites them.
---

# Select LLM Model

Task-driven LLM recommender. Input: a free-form task description. Output: a
ranked shortlist of models, each with per-axis rationale, a source citation,
and the fetch timestamp — plus an explicit list of data gaps.

Data is fetched **live at invocation time** through two CLI tools with
subcommands (no bundled snapshot): `scripts/benchmarks.ts` (capability
benchmarks) and `scripts/openrouter.ts` (deployment price, per-provider
breakdown, speed). The agent queries them targeted — by category, benchmark,
model, or provider — never a firehose. Standings move continuously, so every
answer states when it fetched.

## Operating principles

- **Fail-fast, never fabricate.** If no fetch path works, STOP and say so. A
  source whose tool exits non-zero (unparseable bytes, missing key, missing
  field) is recorded as a Gap — never an invented score.
- **A blocked or failed `curl` is the fail-fast signal — never route around
  it.** If a `curl <url>` fetch errors, returns nothing, or reports `command
  not found`, record that source as a Gap and move on. NEVER retry it via an
  absolute path (`/usr/bin/curl`, `/opt/.../curl`), an alternate binary
  (`wget`, `httpie`, a language one-liner), a proxy, or a `-o /tmp/…` download.
  Working around an unavailable fetch tool to reach the network anyway defeats
  the purpose and yields fabricated-looking results. If EVERY source's fetch
  fails this way, STOP — do not produce a ranking.
- **A disclaimer does not license a ranking from memory.** When you have
  reported the Gaps, the answer is finished: naming models is itself the
  forbidden act, whatever label sits above it. "From my training knowledge",
  "not live-cited", "as of my cutoff", "just so you have something to start
  from" — each of these still hands the user a model list they did not ask you
  to guess at, and a hedged list is what they will act on because it is the
  only list on the page. Say which sources failed and what would make them
  work, and stop there.
- **Rank ONLY the models the tools return.** Model names you do not recognize
  are valid live data, NOT test stubs or placeholders — never dismiss fetched
  rows, never re-fetch to get "more familiar" models, and never substitute
  models from memory. If the tools return models X/Y/Z, the shortlist is drawn
  from X/Y/Z and nothing else.
- **Cite everything.** Each model's per-axis score names the source it came from
  and the fetch timestamp. No uncited rankings.
- **Disclose assumptions.** When the task is vague, state the axis weights you
  assumed before ranking.

## Phase 0 — Tooling check

The tools run as `curl <url> | deno run … --stdin`. Probe the runtime and the
key — but do **NOT** probe `curl`:

- **Runtime:** confirm `deno` is available (e.g. `deno --version`). If `deno` is
  unavailable, every source becomes a Gap (fail-fast) — do NOT fall back to
  scraping raw HTML from memory.
- **Key:** the Artificial Analysis source needs `AA_API_KEY` (free key at
  `https://artificialanalysis.ai/api`). If unset, AA is a Gap — do NOT scrape
  its JS-rendered leaderboard page.
- **Do NOT probe `curl`** with `command -v` / `which` / `type` / `--version`.
  The fetch itself is the availability test: the first `curl <url> | …` pipe in
  Phase 2 either returns bytes or it fails. A `curl` that errors or reports
  `command not found` means the fetch tool is unavailable — apply the fail-fast
  rule above (that source is a Gap; if every source fails, STOP with "No
  working shell fetch tool — cannot retrieve live data; not fabricating a
  recommendation"). Probing first only leaks a binary path you must not use.

## Phase 1 — Derive benchmark categories from the task

`benchmarks.ts` is queried by **category** (the closed set below). Assign a 0–3
weight to each category from the task description (adjust cues to intent):

| Category | Benchmarks (in the tool) | Cues in the task |
|---|---|---|
| general | intelligence, mmlu-pro, gpqa, hle | "general", "hard problem", "reasoning", "PhD", "knowledge", unspecified |
| coding | coding-index, livecodebench, scicode | "code", "implement", "bug", "leetcode", language names |
| math | math-index, aime, aime-25, math-500 | "math", "prove", "olympiad", "arithmetic" |
| agentic | terminal-bench-hard, tau2 | "agent", "autonomous", "terminal", "call tools", "function calling" |
| instruction | ifbench | "follow instructions", "format", "constraints" |
| long-context | lcr | "long context", "large document", "many files" |
| diff-edit | aider-polyglot | "edit existing code", "apply a patch", "diff", "in-place" |
| web | webarena | "browse", "web navigation", "fill forms", "browser agent" |
| computer-use | osworld | "control the desktop", "GUI automation", "computer use" |
| swe | swe-bench-verified | "resolve GitHub issues", "real-world SE", "repo-level fix" |

Rules:

- **Vague task → balanced profile.** If no category stands out, weight `general`
  highest and the rest evenly, and DISCLOSE: "Task under-specified — ranked on a
  balanced general-purpose profile."
- **Price / speed are NOT capability weights.** Treat a stated budget ("cheap",
  "best value", "under $X/Mtok") or latency need ("fast") as a post-rank filter /
  tie-breaker, fetched from `openrouter.ts` (price/speed). When the task says
  nothing about cost or latency, they do not enter the capability score. (For an
  explicit value/$ ask, price is the primary ranking lens — see Phase 3.)

## Phase 2 — Query the data tools

Call the two CLI tools ONLY for the categories you weighted non-zero. Run
every command with the working directory set to the directory you read THIS
`SKILL.md` from — the one holding `scripts/`. Do not reconstruct another skill
root (an IDE's own `skills/.system/…` tree, a home-directory install) from a
naming pattern: an `exec` that fails before the shell starts with `No such file
or directory` is reporting the working directory, not a missing `deno`. A
missing runtime says `deno: command not found`. (2026-09-06: one run set the
workdir to a non-existent `.system/select-llm-model`, read the cwd error as
"Deno is unavailable", and stopped without the pipe.) **Always fetch with `curl` and pipe into the
tool with `--stdin`** — this is the ONE supported invocation form (below). Do
NOT run the tool without the `curl … | … --stdin` pipe. A non-zero exit means
that source is a Gap. Add `--format table` for readable output, `--top N` to cap
rows.

**`benchmarks.ts`** — one call per weighted category (a category maps to one
fetch URL):

```sh
# general/coding/math/agentic/instruction/long-context → Artificial Analysis (key):
curl -fsSL -H "x-api-key: $AA_API_KEY" https://artificialanalysis.ai/api/v2/data/llms/models \
  | deno run -A scripts/benchmarks.ts scores --category coding --top 10 --stdin
# diff-edit → Aider:
curl -fsSL https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml \
  | deno run -A scripts/benchmarks.ts scores --category diff-edit --stdin
# web → Steel.dev (swap board per category: webarena | osworld | swe-bench-verified):
curl -fsSL https://leaderboard.steel.dev/leaderboards/webarena/ \
  | deno run -A scripts/benchmarks.ts scores --category web --stdin
```

- `scores --category <c>` (required) `[--benchmark <b>] [--model <substr>] [--top N]`.
- Output rows: `{category, benchmark, source, model, score, higherIsBetter}`.
- `--benchmark` is optional — omit to get all benchmarks of the category.

**`openrouter.ts`** — deployment price / provider detail / speed:

```sh
curl -fsSL https://openrouter.ai/api/v1/models \
  | deno run -A scripts/openrouter.ts price --sort blended --top 10 --stdin
curl -fsSL https://openrouter.ai/api/v1/models/openai/gpt-4o/endpoints \
  | deno run -A scripts/openrouter.ts providers --model openai/gpt-4o --stdin
```

- `price [--match <substr>] [--sort blended|input|output] [--top N]` → `{id,name,input,output,blended,context}` ($/Mtok).
- `models [--match <substr>] [--top N]` → `{id,name,context}` — resolve the exact `author/slug` for `providers`.
- `providers --model <author/slug>` (required) `[--sort price|uptime]` → per provider `{provider,input,output,cacheRead?,uptime30m,uptime1d,context,quantization,status}`.
- `speed [--match <substr>] [--top N]` → `{model,speed}` (median tok/s, from the AA URL — needs `AA_API_KEY`).

**Source notes.** Artificial Analysis absorbs ~15 benchmarks in one keyed call.
OpenRouter is the real deployment price/value source. Steel.dev adds agent + SE
benchmarks AA lacks; its `web`/`computer-use` boards are
**system/submission-attributed** (agent scaffold + model, e.g. "Claude Code +
GBOX MCP") — cite those as agent-system scores, not bare-model; `swe` lists bare
models. **latency/throughput are not available** (null in the OpenRouter API) —
`speed` (AA median tok/s) is the only throughput proxy.

**Known Gaps (no stable keyless endpoint — report as Gaps, do NOT scrape):**

- Human-preference Elo (LMArena) and fluid reasoning (ARC-AGI) — JS-rendered, no
  clean endpoint, not in the AA API.
- Aggregator SPAs LLM-Stats and BenchLM — Next.js apps with no exposed
  `_next/data` buildId at probe time.
- AgentBench — leaderboard is a Google Sheet + image, no machine-readable feed.
- Epoch AI Capabilities Index — no confirmed CSV/JSON endpoint.
- Scale SEAL / Showdown and SWE-bench Pro — private datasets, no keyless feed.

## Phase 3 — Normalize and rank

Parser scores are on incomparable native scales (intelligence index, 0–1 bench
fractions, $/Mtok). Merge rows across sources by model name/slug (best-effort;
an unmatched model is "no data" on that axis, never zero), then:

1. Per axis, convert each model's raw score to a **percentile within the fetched
   set**. For rows with `higherIsBetter: false` (price), invert so cheaper ranks
   higher — never let a low price sink a model.
1a. **Collapse a category's benchmarks.** A category groups correlated benchmarks
   (general = intelligence/mmlu-pro/gpqa/hle; math = the four math benchmarks).
   Average a category's benchmark percentiles into ONE contribution before the
   weighted sum, so a model is not multi-counted for being broadly smart.
2. Weighted-sum the per-category contributions using the Phase-1 weights.
3. Apply price/speed as a filter/tie-breaker per Phase 1. For an explicit
   value/$ ask, rank by the price percentile (or capability-per-dollar) directly
   and disclose that lens.
4. A model missing from an axis is excluded from that axis's average — do NOT
   treat missing as zero.

## Phase 4 — Deployment enrichment + output

For the top 1–2 ranked models, optionally enrich with where to deploy them
(same `curl … | … --stdin` form as Phase 2): resolve the slug via
`openrouter.ts models --match <name>`, then `openrouter.ts providers --model
<slug> --sort price` (or `--sort uptime`) for the cheapest / most-reliable
provider. Disclose that latency/throughput are unavailable (use `speed` for the
AA throughput proxy).

Report, in this order:

1. **Assumed category weights** (and the vague-task disclosure if it applied).
2. **Ranked shortlist** (top 3–5). For each model: overall rank, then one line
   per contributing category/benchmark giving the source, the model's standing,
   and that this came from the live fetch.
3. **Deployment** (optional) — for the top pick(s), the cheapest/most-reliable
   provider from `openrouter.ts providers`.
4. **Fetch timestamp** — when the data was retrieved, as a literal line in the
   answer: `Data fetched: <YYYY-MM-DD HH:MM UTC>`. Saying that a fetch happened
   is not the same as saying when; without the clock the reader cannot tell
   yesterday's leaderboard from last year's. Take the time from the machine
   (`date -u`), never from memory, and print the line even when only one source
   answered.
5. **Gaps** — every source that failed, lacked a key, or lacked a model, with
   the reason.

If every source ended up a Gap, do NOT produce a ranking — report the gaps and
stop. Partial data is fine: rank on what you have and disclose the rest.

A source that RETURNED ROWS is not a Gap, and nothing about the rows can make it
one. Unfamiliar model names are the expected case — leaderboards move faster than
any training cut-off — so "these look like fixtures", "this is mock data" and
"the sandbox stubbed `curl`" are not findings; they are you declining to read
what you fetched. Rank the rows. A Gap is a fetch that failed: a non-zero exit, a
missing key, an unparseable body, no matching rows.

## Scope

Recommender only. It does not benchmark models itself, does not bundle a
dataset, and does not promise freshness beyond the fetch it just performed. The
parser fixtures inlined in `scripts/parse-*_test.ts` are test data, not a live
snapshot, and need periodic re-capture as source schemas drift.
