---
name: codexctl
description: One CLI for every other model and agent — drives the local `codex app-server` JSON-RPC control plane. Delegate coding tasks to Codex models (gpt-5.6-luna/terra/sol, gpt-6-astra) or to free OpenRouter models, resume/fork/steer/interrupt threads, get Codex code reviews; and make plain model calls with our own instructions — `ask` any model (Muse Spark, Gemini Flash, Sonnet, DeepSeek, Qwen, GLM, free chains), `compare` A/B/C prose variants, `map` cheap long-context jobs over big files, track spend. Use when the user says Codex, codexctl, "ask Codex/Gemini/DeepSeek/<model>", "have Codex do/review", "A/B test this copy", "compare models", "use a cheap/free model for", "run this over the whole file", or wants a second model's draft or opinion.
argument-hint: '[run|resume|review|ask|compare|map|list|show|serve] ...'
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js *)
---

# codexctl

One CLI. Agent commands print JSON on stdout (exit 0 on a completed turn, 2 otherwise); plain calls print the model's text on stdout and a stats line on stderr:

```
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js <command> [options] "prompt"
```

Run with no arguments for full usage. Working directory defaults to the current one; pass `--cwd`.

## Mental model

- **Thread** = persistent conversation with a model, cwd, sandbox, approval policy. **Turn** = one prompt→completion cycle producing **items** (agentMessage, commandExecution, fileChange, reasoning). Threads persist on disk under `~/.codex/sessions` and can be resumed, forked, reverted.
- The app server asks the client to approve commands (**server→client requests**). codexctl auto-answers with `--decide` (default `accept`). Safety comes from the **sandbox**, not from the approval answer: `workspace-write` (default, writes only inside cwd, no network), `read-only`, `danger-full-access`.
- Each invocation normally spawns a private app-server. Run `codexctl serve` once to get a shared WebSocket server; then invocations attach to it, and `steer`/`interrupt` can reach turns started by earlier invocations.
- **Two kinds of call.** *Agent* commands (`run`, `resume`, `fork`, `review`) use Codex's own agent prompt and tools in a workspace. *Plain* commands (`ask`, `compare`, `map`) replace that prompt with ours (`assets/plain.md`, or `--system`/`--instructions`), strip skills, plugins and connectors, run read-only in an ephemeral thread, and cost ~7 KB per request. Any model works for either kind.

## Common invocations

```bash
# delegate a task (Luna, low effort, writes inside cwd, no prompts)
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --cwd . "Add unit tests for src/parser.ts and run them"

# stronger model / more effort, read-only investigation
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --model gpt-5.6-sol --effort high --sandbox read-only "Explain how auth works in this repo"

# continue a thread, fork it into another model, just the text
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js resume THREAD_ID "Now handle the edge case for empty input" --text
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js fork THREAD_ID --model gpt-5.6-terra "Second opinion: is the previous fix correct?"

# Codex code review of uncommitted changes (or --base main / --commit SHA / --custom "...")
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js review --cwd .

# structured answer
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --schema schema.json --text "Classify each file in src/ as core or util"

# free OpenRouter models as the agent ($0; chain falls through on 429/provider error; lean prompt is automatic)
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --model free --cwd . "Add a --dry-run flag to bin/cleanup.py and run its tests"
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --model "deepseek,nemotron-free" --cwd . "..."

# plain calls: one model, our instructions, no agent prompt
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js ask "Rewrite this paragraph in plain English: ..."          # default: flash (Gemini 3.8 Flash)
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js ask free --file notes.md "Reformat as a markdown table"       # $0 chain, fallback on 429
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js ask deepseek --file big.log "List every error class with counts"   # cheap 1M-context model
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js ask --system "You are a copy editor." sonnet --prompt-file brief.md

# A/B/C prose variants for the user to pick from (spark = Muse Spark, flash = Gemini Flash, sonnet); --blind, --judge default
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js compare "Write a launch tweet for ... Plain, no hashtags."
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js compare --models spark,flash --n 2 --blind --judge default "..."
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js reveal latest

# per-section output over a huge file, chunks in parallel, cheap model with a free floor
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js map --model cheap-chain --chunk 150000 --label --file transcript.txt "Extract every decision made, as bullets" --out decisions.md

# long task in the background: returns {pid, journal, resultFile}; poll resultFile
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js serve
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js run --detach --model gpt-5.6-sol --effort medium "Port the build to pnpm workspaces"
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js steer THREAD_ID "Also update the CI workflow"
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js interrupt THREAD_ID

# inventory / housekeeping
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js models        # Codex models
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js aliases       # alias -> OpenRouter id, chains, groups
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js usage         # spend of plain calls, last 30 days
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js limits
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js list --cwd . --limit 10
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js show THREAD_ID
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js delete THREAD_ID ...
node ${CLAUDE_SKILL_DIR}/scripts/codexctl.js exec --cwd . -- python -m pytest -q
```

## Choosing model and effort

| need | pick |
|---|---|
| quick edits, tests, scripts, throwaway probes | `gpt-5.6-luna --effort low` (default for `run`) |
| medium refactors, reviews | `gpt-5.6-terra --effort medium` |
| harder reasoning, second opinions | `gpt-5.6-sol --effort high` |
| the user's default heavy model | `gpt-6-astra` (efforts up to `ultra`; expensive) |
| $0 agent work on throwaway or public code, no ChatGPT quota | `run --model free` |
| menial text work: summaries, extraction, reformatting, classification, test data | `ask free` first, then `ask cheap-chain` (DeepSeek → Qwen → GLM → free) |
| prose the user will publish: tweets, copy, articles | `compare` (group `prose` = spark, flash, sonnet); show A/B/C, let the user pick |
| big inputs | whole-file `ask deepseek --file F` when it fits (cheap models take 1M tokens); `map` for per-section output |
| a quick general answer | `ask` (flash) |

On short tasks effort mostly adds latency, not quality. `aliases` lists every alias; any `org/model` OpenRouter id also works directly.

## Rules of thumb

- Report Codex's or the model's result to the user as that model's output, not yours; verify file changes Codex made before relying on them.
- Never send private or client material to `:free` or `-contributor` endpoints (the `free` chain, `spark-cheap`): their data policy allows logging. Paid endpoints only for that.
- Never start a second turn on a thread while one is running: it is silently merged into the active turn. Use `steer` for that.
- Compaction is lossy and emits no event; after long threads, restate the facts that matter.
- `--sandbox danger-full-access` and `--approval never` together give Codex unrestricted host access. Only with explicit user consent.
- Use `--ephemeral` for probes you do not want in the user's Codex history; otherwise clean up with `delete`. Plain calls are always ephemeral.
- Codex turns are billed against the user's ChatGPT plan (check `limits` before batch work); everything else goes through the OpenRouter key and shows in `usage`.

## Providers and prompt size

`--provider P` uses `[model_providers.P]` from `~/.codex/config.toml` (must be `wire_api = "responses"`; `openrouter` is configured and is implied by every alias and `org/model` id). `--model a,b` is a chain tried in order in fresh threads. `--provider` turns on `--lean`, which strips the connected ChatGPT-app tool schemas (~490 KB -> ~48 KB per request); `--instructions F` or `--system TEXT` replaces Codex's built-in prompt with ours (~15 KB); `--plain` adds the rest of what `ask` does (~7 KB). Details, measured sizes and the probed model table: [references/findings.md](references/findings.md).

## Supporting files (load on demand)

- [references/findings.md](references/findings.md) — verified behavior, gotchas, platform limits, timings (version-stamped).
- [references/protocol.md](references/protocol.md) — generated method/param reference for raw JSON-RPC work; regenerate with `codexctl schema` after `codex update`.
- [scripts/codexrpc.js](scripts/codexrpc.js) — the client library (`CodexClient`, `runTurn`) for custom orchestration beyond the CLI.
- [assets/plain.md](assets/plain.md) — the instructions plain calls use instead of Codex's agent prompt.
