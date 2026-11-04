---
effort: medium
name: relay
description: |
  The ONLY way to call Codex, DeepSeek, MiMo, GLM, or Grok. Use whenever the user
  wants to ask, delegate to, or get a second opinion from Codex, DeepSeek,
  MiMo, GLM, or Grok. Do NOT run the codex, deepseek (ds), mimo (mm), glm, or grok
  CLI directly — from the main agent or a subagent; always use this skill's relay
  call command. Triggers on "ask/have/send to/get/delegate to codex" or the same with
  "deepseek"/"mimo"/"glm"/"grok", "second opinion", "relay".
allowed-tools: Read, Write, Bash(relay:*), Bash(find:*), Bash(printf:*)
user-invocable: true
---

# Relay

**Claude-only.** If `ANTHROPIC_BASE_URL` contains `deepseek`, `xiaomimimo`, or `z.ai`, this skill is unavailable — stop and tell the user: "relay is Claude-only; a non-Claude session cannot orchestrate other models." The relay script also refuses at the shell layer.

Call Codex, DeepSeek, MiMo, GLM, or Grok like a function: one command generates the request, invokes the peer, and prints the response.

> **The peer is a full agent in the Claude Code harness — not a stateless API call.** Relay invokes each peer through its registered transport (DeepSeek/MiMo/GLM via `claude -p` with the model weights swapped — V4-Pro, MiMo-V2.5-Pro, GLM-5.2; Codex via `codex exec`; Grok via its own `grok` CLI), so the peer has your core tools — Bash, file read/write, Grep/Glob, subagents, multi-step agentic loops. It can see this repo, run commands, and verify its own work; delegate file I/O and shell work directly. Do **not** treat it as a one-shot completion that "can't see the codebase." Web tools (WebFetch/WebSearch) are registered on every peer and broadly work — verified 2026-06-06: Codex and both Grok tiers do both; the only gaps are DeepSeek's WebFetch (400 `thinking options ... reasoning_effort` under its forced `max` effort) and MiMo's WebSearch (no live search), and each of those two still has the *other* web tool. So every peer can reach the web — treat browsing as available, not a per-call unknown to re-verify. The only constant difference from you is the model behind the harness.

```
relay call --name <slug> [--to <peer>] [--effort <level>] [--body-only] <<'BODY'
task
BODY
```

`relay` is in PATH. The caller is always Claude (this is a Claude-only skill); the peer defaults to Codex. Pass `--to deepseek`, `--to mimo`, `--to glm`, `--to grok-build`, or `--to grok-composer` to route elsewhere.

If a bare `relay` ever returns "command not found" (a sandboxed/non-zsh/reset-env shell that didn't inherit the PATH entry), re-run the **identical** command with the absolute install path — `~/.claude/skills/relay/scripts/relay call …`. That is the whole recovery; do not reconstruct the call by hand.

**All Codex, DeepSeek, MiMo, GLM, and Grok interactions go through `relay call`.** Do not invoke `codex exec`, the `grok` CLI, or the `ds`/`mm`/`glm` aliases directly, do not spawn agents to run the codex, grok, or claude CLI for these purposes, and do not pass model flags (`-m`, `--model`) — the model and invocation method come from the peer registry (`peers.json`), not the call.

## Peer selection

| Peer | When to pick | How to invoke |
|---|---|---|
| **Codex** (default) | Code review, security review, refactoring, agentic coding. GPT-6.1-Sol (the local Codex default; `gpt-5.5` is not available on a ChatGPT-account login). Two effort tiers (`medium`/`xhigh`). | `relay call --name ...` (no `--to` needed) |
| **DeepSeek** | Independent model family for true cross-vendor diversity, frontier reasoning, multi-step analysis. Open-weight V4-Pro (1.6T MoE). Always runs at `max` (DeepThink). Text-only (no image input via relay). | `relay call --to deepseek --name ...` |
| **MiMo** | Another independent open-weight lineage (Xiaomi MiMo-V2.5-Pro, 1.02T MoE / 42B active, 1M context). Use for a third cross-vendor perspective. No effort knob. Text-only (no image input via relay). | `relay call --to mimo --name ...` |
| **GLM** | A fourth independent lineage (Zhipu/z.ai GLM-5.2), reached through z.ai's Anthropic-compatible endpoint. Use for another cross-vendor perspective. Pinned to `max` reasoning via the registry (like DeepSeek); ignores `--effort`. Text-only (no image input via relay). | `relay call --to glm --name ...` |
| **Grok Build** | An independent xAI lineage (`grok-build`), xAI's agentic coding model. Runs via grok's own CLI in headless mode (not Anthropic-compatible). Effort `medium`/`high` (default `medium`). | `relay call --to grok-build --name ...` |
| **Grok Composer** | xAI's fast model (`grok-composer-2.5-fast`) — same lineage as Grok Build, lighter/cheaper. Use as a faster xAI option (not a distinct cross-vendor perspective). No effort knob. | `relay call --to grok-composer --name ...` |

Pick Codex by default — it's the strongest general-purpose coding agent and integrates cleanly with the relay protocol. Pick DeepSeek, MiMo, GLM, or Grok Build for a perspective from a model trained outside both the Anthropic and OpenAI lineages, or when running `/prism` Parallax (Grok Composer is a faster xAI variant, not a distinct lineage from Grok Build). Of these, only Grok Build has an effort knob (`medium`/`high`); DeepSeek, MiMo, GLM, and Grok Composer ignore `--effort`, so omit it for them. DeepSeek requires `DEEPSEEK_API_KEY`, MiMo requires `MIMO_API_KEY`, and GLM requires `GLM_API_KEY` in the environment; Grok uses its own cached login (no key var).

### Peer registry

Every model-family fact — transport (`codex` CLI vs a generic `claude-env` Anthropic-compatible envelope), endpoint, key variable, model id, effort knob, per-peer extras, and launcher template style — lives once in `peers.json` next to the script. `relay` and `prism-launch` both read it, so **adding a peer that reuses an existing transport is one stanza** there, not edits across the script, the prism launcher, and the docs. The `claude-env` peers share one code path that differs only by registry data; Codex and Grok each have their own transport. Two deliberate exceptions stay in code, not data: a brand-new *transport* needs its own script branch (this is how `grok` was added — its own headless-CLI invocation), and a new `claude-env` peer should also get its endpoint added to the inbound Claude-only refusal at the top of the script (a one-line safety guard that must run before the registry is loaded). Grok needs no refusal entry — it sets no `ANTHROPIC_BASE_URL`, and the transport-agnostic `RELAY_PEER` guard already blocks a dispatched grok peer from recursing. The interactive `ds`/`mm`/`glm` launchers in `shell/.functions` are a separate consumer and still carry their own copy — keep them in sync.

### Common Mistakes
- **Premature failure diagnosis**: If a relay call was launched with `run_in_background: true`, do not inspect `.relay` files or enter the failure flow until the background task's completion notification arrives. No notification means the peer is still running.
- **Wrapping relay in a subagent**: Do not spawn an Agent that then calls `relay` inside. When the subagent completes, the platform kills its child processes — including the still-running peer CLI. Call `relay` directly from the main conversation with `run_in_background: true` instead.
- **Empty heredoc body**: The `<<'BODY'` ... `BODY` block must contain text — an empty body causes an immediate error.
- **Missing `--name`**: Every call requires `--name` — omitting it is a script error, not a peer failure.

## Example

```bash
relay call --name auth-review --effort medium <<'BODY'
Review src/auth.py for security issues. Run pytest to verify.
BODY
```

## Effort Levels

`--effort` applies to Codex and Grok Build. Codex accepts `medium`/`xhigh`; Grok Build accepts `medium`/`high` (default `medium`). DeepSeek and GLM always run at `max` reasoning (DeepSeek via DeepThink; GLM via `reasoning_effort: max`, pinned in the registry), and MiMo and Grok Composer have no effort knob — the flag is silently ignored or omitted on those calls.

| Level | When to use |
|-------|-------------|
| `medium` | **Default for Codex and Grok Build.** Balanced starting point for code review, tests, bug fixes, and most refactoring. |
| `xhigh` | Codex only. Hard architecture work, deep security review, or eval-bound tasks worth the extra latency. |
| `high` | Grok Build only — its deeper reasoning tier. Use for hard analysis where the extra latency is worth it. |

Before raising effort, improve the prompt first — add outcome-first success criteria, stop rules, verification steps, and completeness criteria.

## Prompting Codex

**Before composing the prompt body, read the prompt-engineer references** — `~/.claude/skills/prompt-engineer/references/gpt.md` for cross-cutting GPT-5.5 prompt patterns and `~/.claude/skills/prompt-engineer/references/codex.md` for Codex coding agent patterns. If those symlinks are unavailable, use the repo copies at `agents/extensions/skills/prompt-engineer/references/`. This is not optional — the guides contain model-specific patterns that materially affect output quality.

Lead with the outcome, not the procedure. GPT-5.5 responds best to outcome-first prompts — state the goal, success criteria, and stop rules, then let Codex pick the path. Use XML scaffolding only when a specific failure mode needs it:

- `<output_contract>` — when format precision matters
- `<completeness_contract>` — when the task has discrete items that must all be covered
- `<verification_loop>` — when post-change validation is required

**Example:**

```bash
relay call --name pool-refactor --effort medium <<'BODY'
Add connection timeouts and stale-connection recovery to src/db/pool.py.

Success criteria:
- ConnectionPool accepts a timeout_seconds parameter at construction
- stale connections are auto-reconnected on use
- a reclaim_stale() method exists for explicit cleanup
- existing callers keep working without changes

<verification_loop>
Run pytest tests/test_pool.py — all tests must pass. No new lint errors.
</verification_loop>

<output_contract>
Summary of changes, one per line, with file path and description.
</output_contract>
BODY
```

## Prompting DeepSeek, MiMo, GLM, and Grok

These are all independent (non-Anthropic/OpenAI) models that respond well to XML-scaffolded, structured prompts. **Before composing a DeepSeek prompt body, read `~/.claude/skills/relay/references/deepseek.md`** (symlinked to the prompt-engineer reference) — it covers the CO-STAR framework, XML scaffolding conventions, thinking-mode quirks, and DeepThink failure modes. This is not optional — the guide contains model-specific patterns that materially affect output quality. MiMo-V2.5-Pro, GLM-5.2, and Grok (both models) have no dedicated reference; treat them like DeepSeek.

Default to XML scaffolding (DeepSeek V4 was trained heavily on XML-tagged data; MiMo, GLM, and Grok behave similarly). The CO-STAR sections — `<context>`, `<objective>`, `<style>`, `<tone>`, `<audience>`, `<response_format>` — give the cleanest results for non-trivial tasks. Use positive framing ("include X") over negative constraints ("don't omit X"). Aside from Grok Build's `--effort` flag, their thinking is always on — so keep system-style meta-instructions out of the prompt body; they degrade under long system prompts. Lead with the outcome and success criteria, then let the model pick the path.

**Example** (swap `--to deepseek` for `--to mimo`, `--to glm`, `--to grok-build`, or `--to grok-composer` to route elsewhere — the prompt shape is identical):

```bash
relay call --to deepseek --name pool-design <<'BODY'
<context>
We're hardening src/db/pool.py before a SOC 2 audit. Codebase is Python 3.12 +
FastAPI. Tests live in tests/test_pool.py and run under pytest.
</context>

<objective>
Add connection timeouts and stale-connection recovery to src/db/pool.py.
</objective>

<success_criteria>
- ConnectionPool accepts a timeout_seconds parameter at construction
- stale connections are auto-reconnected on use
- a reclaim_stale() method exists for explicit cleanup
- existing callers keep working without changes
- pytest tests/test_pool.py passes; no new lint errors
</success_criteria>

<response_format>
Summary of changes first (one line per change: file path + description),
then the diffs grouped by file. Cap at 400 words excluding diffs.
</response_format>
BODY
```

## Calibration handoff

For **judgment tasks** — analysis, review, design, research, second opinions — ask the peer to end its answer with a reasons-based calibration block, then act on it when the response returns. **Skip it for mechanical or code-changing calls** (run-a-command, apply-a-defined-change): there the trust signal is tests, diffs, and the `verify:` frontmatter, not a self-report. Don't ask for a number — verbalized confidence from these models is poorly calibrated (clusters at round numbers, skews overconfident), so a `%` or `High/Med/Low` manufactures false precision the orchestrator can't discount.

Add to the prompt body — inside `<output_contract>` for Codex, `<response_format>` for DeepSeek/MiMo/GLM/Grok:

```text
End with a ## Calibration block:
- Key assumptions: 1-3 the answer rests on ("none material" only if true)
- Most likely wrong because: the strongest failure mode, missing info, or counterargument
- Would change my conclusion: the specific fact, test, or counterexample that would flip it
- Verify before acting: specific current/high-stakes claims to check ("none" for pure reasoning)

No numeric %, probability, or High/Medium/Low label — this block is for routing and verification, not a calibrated probability.
```

**On return, use it — otherwise it is decoration.** Verify the listed claims before passing the answer up; re-query with corrected context if a Key assumption conflicts with what you know; seek a tie-breaker (another peer or `/prism`) if "Most likely wrong because" attacks the core conclusion. Ignore any self-confidence score a peer volunteers anyway — the assumptions and failure mode are the signal, not a self-graded number.

## Output

The script prints the response file content to stdout. The response has YAML frontmatter followed by free-form markdown:

- **Frontmatter**: `relay`, `re`, `from`, `to`, `status` (`done` | `error`), `verify` (`pass` | `fail` | `skip`)
- **Body**: findings, changes, reasoning — free-form markdown below the frontmatter fence

Use `--body-only` to strip the frontmatter and get just the markdown body.

Request and response files are saved in `.relay/` (auto-gitignored). Peer stderr is logged to a `.log` sidecar file alongside the request. **Never read the `.log` file** — it contains the peer's full stderr output, which is extremely long and token-heavy. Only inspect the `.res.md` response file.

### When a relay call fails

**You must diagnose and retry — do not report failure to the user without attempting a fix first.**

**Background-task guard:** If the relay call was launched with `run_in_background: true`, this diagnosis flow applies only after the background task's completion notification has arrived. Relay calls take significantly longer than subagents — this is normal, not a failure. Until the completion notification arrives, the call is in progress and healthy. Do not read logs or check for the response file.

When a completed relay call reports a missing response file, the peer failed before producing output. Each call generates a new request ID, so retrying does not re-execute previous attempts.

1. **Check the Bash output.** The relay script prints diagnostic information (exit code, error summary) to stdout/stderr. Use this — visible in the Bash tool result — to identify the cause. **Do not read the `.log` sidecar file** — full stderr, token-heavy.
2. **Diagnose.** Common causes and fixes:
   - *Peer binary not found* → verify the peer CLI is installed and in PATH
   - *Empty body / malformed heredoc* → verify the heredoc has content and a matching terminator
   - *Peer exited non-zero but response file exists* → not a failure; read the response file
3. **Fix and retry once.** Correct the invocation based on the diagnosis and re-run the relay call.
4. **If the retry also fails**, report the failure to the user with the diagnosed cause from the Bash output.

The first failure is information, not a stop signal.

## Async / Parallel

When you have independent subagent work alongside a relay call, **never block on relay while subagents wait (or vice versa)**. Run everything concurrently:

**Background the Bash call**: Use `run_in_background: true` on the Bash tool so the relay call runs concurrently with your subagents. The platform sends a completion notification when the background task finishes — do not poll, do not inspect `.relay` files, and do not enter the failure diagnosis flow before that notification arrives.

**Give it a generous timeout.** Relay peers are full agents and can run long (Codex `xhigh`, DeepSeek/MiMo DeepThink, GLM at `max`, Grok at `high` routinely take many minutes). A Bash-tool `timeout` that fires mid-run kills the peer and wastes every token it already spent — favor completion over a tight bound. Set `timeout: 3600000` (60 min) on the backgrounded Bash call; relay has no internal per-call cap, so this outer timeout is the only bound.

**Rule: Launch relay calls and subagents concurrently. Never serialize independent work.**

**Never wrap relay in a subagent.** If an Agent task calls `relay` with `run_in_background: true`, the subagent will complete before the peer (Codex, DeepSeek, MiMo, GLM, or Grok) finishes, and the platform will kill the orphaned peer process. Always call `relay` from the main conversation. If a subagent must call relay (e.g., the skill was invoked before you could prevent it), the Bash call must run in foreground — omit `run_in_background` so the subagent blocks until the peer replies.

## Prism / Parallax

When Relay is used as the Parallax transport inside Prism, the relay call receives the **same full question and same context** as every local reviewer — only the lens (weighing posture) differs. Do not narrow the prompt for the Parallax agent. Prism dispatches each parallax tier independently — the relay calls run concurrently as separate Bash invocations.

Launch each relay Bash call with `run_in_background: true` in the same parallel dispatch step as the local reviewer subagents. Do not wrap Relay itself in another subagent layer.

If a Parallax relay call fails (after its background completion notification has arrived), treat it as a recoverable transport problem. Check the relay script's Bash output for the diagnosed cause, fix the invocation, and retry once before declaring that peer unavailable — never read the `.log` sidecar (full stderr, token-heavy). A failure of one peer (e.g., Codex) does not affect the others.

## Utility Commands

`relay --help` and `relay --version` print usage and version info.

`--to` accepts `codex` (default), `deepseek`, `mimo`, `glm`, `grok-build`, or `grok-composer`. There is no relay-to-Claude direction — Claude is the sole caller in this protocol.
