---
name: ai-ide-runner
description: >-
  Run prompts in Claude Code, OpenCode, Cursor, or Codex CLIs from this session
  — one IDE, fan-out, or model comparison. Relay the other runtime's stdout
  verbatim. Use on run in <ide>, compare <ide> vs <ide>, try on <model>, run
  across models.
---

# AI IDE Runner

**You are a courier, not a co-author.** When the user asks you to run a
prompt in another IDE, your job is to spawn the child runtime, capture
whatever it prints, and relay that text back verbatim. The answer in the
final message MUST come from the child runtime's stdout (or stderr on
failure) — never from your own model weights. If you find yourself about
to write your own opinion on TypeScript, git, architecture, etc.,
**STOP**: the user asked the other tool, not you. See the
[Output contract](#output-contract-verbatim-relay) section for the exact
rule and examples.

Invoke agent-CLI runtimes from the shell in one shot. Each supports a
non-interactive "send prompt, capture response" mode. Use this skill to:

- run a prompt inside one specific IDE (second opinion, different model);
- fan out one prompt across several IDEs and compare answers;
- fan out one prompt across several models inside the same IDE.

## Workflow

1. **Parse intent**: which IDEs/models, one prompt or several, what to compare
   (quality, latency, cost, reasoning depth). When the user names only a
   model or vendor (not an IDE), **default to the vendor's native IDE**:
   Anthropic/Claude → `claude` (Claude Code); OpenAI/GPT/o-series → `codex`
   (Codex); Cursor's own Composer → `cursor-agent`. Pick OpenCode only
   when the user says "in OpenCode", wants OpenRouter billing, or asks
   to fan out across providers. Reach for Cursor when the user wants
   Cursor's router/Composer stack specifically.
2. **Pick model per IDE**: default to the IDE's flagship alias unless the user
   specified one. Consult [references/models.md](references/models.md) for the
   short catalogue and per-IDE discovery commands. If you're unsure a model
   exists, run discovery (`--list-models`, `models` subcommand) before
   invoking — do not invent IDs.
3. **Build & run**: use recipes in [references/runtimes.md](references/runtimes.md).
   Launch in parallel when comparing — each invocation is an independent
   child process.
4. **Present**: pick a format that fits the comparison (side-by-side,
   diff, metrics table, ranked list). No prescribed shape — optimise for
   what the user is trying to decide. See the **Output contract** section
   below for the non-negotiable verbatim-relay rule.

## Output contract (verbatim relay)

**You are a courier, not a co-author.** Your job is to deliver the other
runtime's answer, not to improve it.

- **Quote the captured output byte-for-byte.** Wrap it in a code block
  or blockquote, labelled with the IDE + resolved model. Preserve the
  tool's framing — `=== result ===` banners, ANSI escapes, JSON
  envelopes, trailing newlines — unless it's obviously a harness
  artifact (e.g. a `<TOOL>-MOCK:` prefix injected by a sandbox hook,
  which is not something the real CLI would emit). The substantive
  content words and sentences MUST match the tool's output exactly.
- **Do not paraphrase, expand, condense, translate, re-style, fix
  grammar, fill gaps, add examples, or "clean up"** the output — not
  even partially. If the tool's answer is short or unhelpful, relay it
  short and unhelpful. If it is in a different language, keep it in
  that language.
- **Do not invent a response when the tool produced none.** If stdout
  is empty, the exit code is non-zero, or the binary is missing, say
  so plainly and show the captured stderr / error message verbatim —
  do not synthesise what the tool "would have" said. An error message
  like "usage limit reached" IS a valid relay; fabricating a plausible
  answer in its place is the worst failure mode.
- **Your own commentary is allowed ONLY outside the quoted block** (a
  brief preface or a follow-up comparison paragraph), clearly separated
  from the tool's text. The user must be able to tell at a glance which
  words came from the runtime and which came from you.

### Hook-blocked tool calls count as tool output

In benchmark and sandbox environments, your `Bash` call to `claude`,
`opencode`, `cursor-agent`, or `codex` may be intercepted by a
PreToolUse hook that returns `{"decision": "block", "reason": "<text>"}`
instead of letting the binary run. When that happens, the harness shows
you a system message like *"Tool call was blocked. Reason: CLAUDE-MOCK:
prefer pure functions at the core."*. That `reason` string IS the tool's
stdout for your purposes — **quote it verbatim, including the
`<TOOL>-MOCK:` prefix**. Do NOT:

- re-run the command trying to "route around" the block;
- discard the `reason` and write your own answer from model weights;
- paraphrase "CLAUDE-MOCK: prefer pure functions" into your own
  sentence about pure functions.

The block IS the response. Treat it as if the child process had printed
that exact text to stdout and exited 0.

### Self-check before sending the final message

Before you send the response to the user, read your own draft and ask:

- "Did I include a quoted block with the child runtime's exact text?"
  If no → go back and add it.
- "Is every non-quoted sentence strictly framing (labels, metadata,
  comparison), or did I sneak in my own content advice?" If you wrote
  TypeScript / architecture / debugging advice in your own voice — you
  became the author. Revert to pure relay.
- "Did the tool emit a prefix like `CLAUDE-MOCK:` / `OPENCODE-MOCK:` /
  `CURSOR-MOCK:` / `CODEX-MOCK:`?" If yes, that prefix MUST be inside
  your quoted block. Grep your draft for the prefix; if it's missing,
  you paraphrased.

Right:

```
OpenCode — anthropic/claude-sonnet-4.6:
> OPENCODE-MOCK: keep I/O at the edge and pure logic inside.
```

Wrong (synthesised / paraphrased — prefix dropped, voice changed):

```
OpenCode suggested that you should generally keep I/O operations at
the boundaries of your application while putting your pure business
logic in the centre — a classic hexagonal pattern…
```

Wrong (hook blocked, agent ignored the `reason` and wrote its own):

```
The cursor-agent command was blocked in this sandbox, so based on the
repo layout I'd say it's a Deno TypeScript project with tasks in
deno.json.
```

(Right response for the blocked case: quote the hook's `reason`
verbatim, labelled with the IDE that was mocked.)

## Runtime cheatsheet (one-shot, capture stdout)

- Claude Code
  - Binary: `claude`
  - Non-interactive: `claude -p "<prompt>"`
  - Model flag: `--model <alias-or-id>` (aliases: `opus`, `sonnet`, `haiku`)
- OpenCode
  - Binary: `opencode`
  - Non-interactive: `opencode run "<prompt>"`
  - Model flag: `-m <provider>/<model>` (format is mandatory)
- Cursor
  - Binary: `cursor-agent` (not `cursor`)
  - Non-interactive: `cursor-agent -p --trust "<prompt>"`
  - Model flag: `--model <id>`
- Codex
  - Binary: `codex`
  - Non-interactive: `codex exec "<prompt>"` (or stdin: `echo "<prompt>" | codex exec -`)
  - Model flag: `-m <id>` (or `-c model="<id>"`)

Full flag set, sandbox/permission modes, session resume, and structured-output
formats are in [references/runtimes.md](references/runtimes.md).

## Where the tool's "stdout" actually lives

The literal output to quote comes from **the Bash tool call's own
response in the same turn you invoked the child runtime**. Two cases:

- **Unblocked run**: the child ran for real. The Bash tool's response
  contains whatever the child printed on stdout/stderr (plus your
  redirects if you used any). Quote from there.
- **Hook-blocked run** (common in sandboxes, acceptance tests, policy
  gates): the child never executed. The harness intercepted the call
  and returned a payload like
  *"Tool call blocked. Reason: `CLAUDE-MOCK: prefer pure functions at
  the core.`"*. **That `reason` text IS the runtime's stdout for this
  skill.** Quote it verbatim, prefix and all.

Either way, the text arrives in-band as the Bash tool's result. Do
**not** go looking for it on disk — shell redirects like
`> /tmp/out.txt` never execute when the hook blocks the call, so the
file is empty. Don't chase empty files; quote the tool result.

Optional: if the child is likely to print a lot and you want to keep
your working context clean, redirect to a file and `cat` it in a
follow-up call. But that is a convenience, not a requirement — and it
does NOT help in the hook-blocked case.

Right (blocked call, quoted from tool response):

```
# turn N: Bash("CLAUDECODE='' claude -p '...' --model sonnet 2>&1")
#   → tool result: "Tool blocked. Reason: CLAUDE-MOCK: prefer pure
#      functions at the core."
# final message to user:
>     CLAUDE-MOCK: prefer pure functions at the core.
```

Wrong (agent catted an empty file then synthesised):

```
# turn N:   Bash("claude -p '...' > /tmp/out.txt 2>&1")   # hook blocked
# turn N+1: Bash("cat /tmp/out.txt")                      # empty
# final message to user:
>     Предпочитайте явные типы возвращаемых значений…
#       ← synthesised from the outer model's weights; no quote.
```

## Running in parallel

When comparing, launch all runs concurrently and wait on PIDs:

```bash
P="Your shared prompt here"
( claude        -p "$P" --model opus                > out-claude.txt   2>&1 ) &
( opencode      run "$P" -m anthropic/claude-opus   > out-opencode.txt 2>&1 ) &
( cursor-agent  -p --trust --model auto "$P"        > out-cursor.txt   2>&1 ) &
( codex         exec -m "<codex-model-id>" "$P"      > out-codex.txt    2>&1 ) &
wait
```

Each child inherits the current `cwd`. No timeout is applied — if a run
hangs, the user can Ctrl-C; if you need to kill one specifically, track its
PID with `$!` and `kill -TERM <pid>`.

## Gotchas

- **Nested Claude**: when the caller is itself Claude Code, the inner
  `claude -p` refuses to run with "already in a Claude session". Pass
  `CLAUDECODE="" claude -p …` (empty string, not unset — parent env leaks
  otherwise) to override.
- **Cursor defaults are write-capable**: `cursor-agent -p` has full tool
  access (shell, edit) by default. For a read-only comparison run use
  `--mode plan` or `--mode ask`.
- **Codex prompt delivery**: argv and stdin both work. Prefer stdin
  (`echo "$P" | codex exec -`) when the prompt contains special shell
  characters or is very long.
- **OpenCode model format**: always `provider/model`. A bare model name
  will not resolve — check the `provider/` prefix via `opencode models`.
- **OpenCode provider choice**: when the user names a vendor label
  ("Claude Sonnet", "GPT-5"), prefer the **native** provider (e.g.
  `anthropic/claude-sonnet-4.6`, `openai/gpt-5.4`) over routed variants
  (`openrouter/anthropic/...`, `opencode/...`). Only pick a routed
  provider when the user explicitly asks for OpenRouter, a specific
  billing path, or when discovery shows the native provider isn't
  configured. Mention the chosen provider in the final answer.
- **Native-first, no silent fallback**: if the native provider
  invocation fails (auth error, credit limit, model ID mismatch,
  "provider not configured", etc.), STOP. Do NOT silently retry with
  `openrouter/…`, `opencode/…`, or any other routed variant — that
  silently changes billing, latency, and sometimes even the model
  identity (OpenRouter often serves a different snapshot). Instead,
  report the native failure verbatim (see Output contract — the error
  message is the tool's output and must be quoted) and, if
  interactive, ask the user whether to fall back to a routed provider.
  In non-interactive mode (benchmark, CI, scripted pipeline), just
  report the failure and stop — the user will decide on their next
  turn. A scenario where the user asked for `Claude Sonnet` and got
  back `openrouter/anthropic/claude-sonnet` without being told is a
  bug, not a feature.
- **Auth**: each CLI uses its own cached login. If a run fails with an
  auth error, tell the user to run `<binary> login` (or set the vendor
  API-key env var listed in [references/runtimes.md](references/runtimes.md)).
- **Mixed stderr/stdout**: for simple capture, redirect both (`> file 2>&1`).
  For structured output, pass the runtime's JSON flag (see runtimes.md) and
  capture stdout only.

## Model discovery

If the user asks for a model the skill's catalogue doesn't know:

- Cursor: `cursor-agent --list-models`.
- OpenCode: `opencode models` (or `opencode models <provider>`).
- Codex: no built-in list; check `~/.codex/config.toml` and the vendor's
  model docs. `codex exec --help` only shows the `-m` flag surface.
- Claude: `claude --help | head -80` hints at aliases; full list at
  the Anthropic Claude docs.

Never invent model IDs. If discovery fails and the user can't name one,
fall back to the IDE's default alias (`opus`, `auto`, `composer-2-fast`,
etc.) and tell the user which model was actually used. "Which model" is a
name, never "the default": when the child runtime prints no model, name the
alias the IDE resolves its default to (from `references/models.md` or the
IDE's `--list-models`) and say the runtime did not echo it — `model: auto
(Cursor's default; not reported by cursor-agent)`. (2026-09-06:
`ai-ide-runner-single-cursor-read-only` answered "Cursor default model; the
runtime did not report a model name" and failed the disclosure item.)

## Scope boundaries

This skill covers **invocation and comparison**. It does not:

- Set up accounts or install CLIs — assume they are already installed and
  authenticated in the caller's environment. If a binary is missing, say
  so and stop.
- Persist transcripts — each CLI has its own session store. See the
  "Transcripts" section in [references/runtimes.md](references/runtimes.md)
  for locations.
- Judge output quality automatically — if the user wants a verdict, either
  present the outputs and ask, or invoke an LLM-as-judge step explicitly
  (as another IDE invocation) rather than adding that step unprompted.
