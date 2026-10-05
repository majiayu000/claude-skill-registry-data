---
name: second-opinion
description: Get external AI opinions on a problem or question. Use when you want diverse perspectives from the agent CLIs you are not running (Claude, Codex, Pi, OpenCode).
compatibility: Requires at least one of claude, codex, pi or opencode on PATH besides the one you are running as. Pi and OpenCode advisors need an OpenRouter key.
argument-hint: '[--quick] [--timeout=300] [--words=500] <question or context>'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Second Opinion Command

Get input from three independent advisors on the current problem or question. Consult the advisor CLIs you are *not* — from `claude`, `codex`, `pi` and `opencode`, skip whichever one you are running as, and query the rest. By default, iterates if responses lack confidence.

## Usage

```
/second-opinion <question or context>
/second-opinion --quick <question>        # Single pass, no iteration
/second-opinion --words=300 <question>    # Limit response to 300 words
/second-opinion --timeout=120 <question>  # Set timeout to 120s
/second-opinion                           # Uses current conversation context
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--quick` | off | Single pass, no iteration |
| `--timeout` | `300` | Timeout per advisor in seconds |
| `--words` | `500` | Max words per advisor response |

## Gotchas
- `.second-opinion.md` is written to the project directory and is NOT gitignored by default. If cleanup is skipped (error, timeout), it can be accidentally committed.
- The advisor CLIs must be installed. If one is missing or fails, the command continues with the others and that advisor's input is simply absent from the synthesis.
- **The advisors are meant to read the code** — that's the point. All advisors run in *read-only* mode so they can read/explore the repo but cannot modify it. Point them at the relevant files in the prompt; reading them stays fast (~15–25s). Always close stdin with `</dev/null` on advisor commands.
- **Claude** runs non-interactively in print mode (`claude -p`). Give it the read-only built-ins (`--tools "Read,Grep,Glob"`) so it can explore but not edit, and `--disable-slash-commands` so it can't recurse into skills.
- **Codex** blocks on "Reading additional input from stdin..." unless stdin is closed (`</dev/null`), and prompts for confirmation outside a git repo unless given `--skip-git-repo-check`.
- **The advisor's identity is the model, not the CLI.** Pi and OpenCode use the explicit models in the commands below, from two different labs, so their opinions stay independent of each other.
- **Pi** needs `-p` for non-interactive mode and `--no-session` so the consultation does not land in the session list. Restrict it with `--tools read,grep,find,ls`; the allowlist excludes write and delegation tools. A model newer than Pi's cached catalog warns `Model "…" not found for provider "openrouter". Using custom model id.` and then works normally — that warning is not a failure.
- **OpenCode** bills through OpenRouter — models must use the `openrouter/` prefix (`opencode/*` is OpenCode Zen, which has no payment method and errors out). Use `--agent plan` with the per-run task denial below. Plan mode alone can delegate to other agents.
- **Headless gotcha:** OpenCode evaluates each part of a compound (`;`/`&&`/`|`) bash command separately and takes the least-permitted verdict; with stdin closed there's no TTY to answer an `ask` prompt, so the whole call is auto-rejected and the run terminates before producing any prose. The classic trigger is a benign `echo ---` separator inside an otherwise-allowed read chain. The prompt template already tells the advisor to avoid chaining; if a run still dies with no output, suspect a chained command hitting an un-allowlisted token.

## How It Works

### Default Flow (Iterative)

1. Summarize the current problem/question from the conversation (or use what the user provides)
2. Query advisors in parallel for their perspectives
3. Evaluate confidence in all responses
4. If confidence is LOW for any advisor, re-query with additional context (up to 2 iterations)
5. Present final results with your synthesis

### Quick Mode (`--quick`)

1. Query all advisors once
2. Present results immediately without iteration
3. Useful when you just want fast input without refinement

## Execution

### Step 1: Prepare the Context

Extract or use the user's question/problem. If not explicitly provided, summarize:
- What is the current task or problem?
- What approaches are being considered?
- **The relevant file paths** — list them so the advisors know where to look. This is what makes the opinion code-aware rather than generic; spend effort here.

Write the prompt to `.second-opinion.md` in the current working directory (dotfile so it stays out of the way; in the project directory so the advisors can read both it and the code it points to). Use this exact filename for all subsequent steps:

```markdown
Read-only consultation. Do not modify any files — but DO read the relevant code in this project before answering.

Do not dispatch subagents or launch other agent CLIs; answer this consultation yourself.

Shell use: prefer your built-in file-reading tool. If you do run shell commands, run ONE simple command at a time — do NOT chain with `;`, `&&`, or `|` and do NOT add `echo` separators. This is a headless session, so any command that would need confirmation is auto-declined, and a single declined command ends the run before you can answer. A chain is only as permitted as its least-permitted part.

I need a second opinion: {problem_summary}

Relevant files/areas to look at: {file_paths}

Read those (and anything else in the project you need) and give your perspective in {words} words or less. Reference specific functions/files so I know what you looked at. Focus on:
- Key considerations I might be missing
- Potential issues with the current approach
- Alternative approaches worth considering

If you need more context to give a confident answer, say so clearly.
```

### Step 2: Query Advisors (in parallel)

Run the advisor commands in parallel — skipping the CLI you are running as — using
`{timeout}` as the Bash timeout. Each inlines the prompt via `$(cat .second-opinion.md)`
and closes stdin with `</dev/null`. All advisors run read-only and read the files the
prompt points them at, typically answering in ~15–25s; allow longer for a question that
spans many files.

Prefix the advisor commands with the `command` builtin where shown: in some shells
they are wrapper functions that depend on an interactive-shell variable not present
in the agent's environment; `command` bypasses the wrapper and runs the real binary,
which authenticates via its own on-disk credentials. If a bare binary instead exits
not-logged-in, its credential comes from the wrapper — drop the prefix for that one.

**Claude:** read-only built-ins, no slash commands, print mode. Leave `claude`
unprefixed — do **not** put `command` in front of it:
```bash
claude --tools "Read,Grep,Glob" --disable-slash-commands --no-session-persistence -p "$(cat .second-opinion.md)" </dev/null
```

**Codex:** read-only sandbox with both agent backends disabled; `--skip-git-repo-check` permits use outside a git repo:
```bash
command codex exec -s read-only --skip-git-repo-check --disable multi_agent --disable multi_agent_v2 -c agents.enabled=false "$(cat .second-opinion.md)" </dev/null
```

Use the Pi and OpenCode model ids and `max` reasoning settings below exactly,
including in `--quick` mode. Change them only when the user explicitly requests it.
If a selected model or reasoning level is unavailable, report that advisor as
unavailable and continue with the others.

**Pi:** `--tools` is the read-only guard (no `edit`/`write`/`bash`). Pi has no `-m` short flag — it is `--model`:
```bash
command pi -p --no-session --tools read,grep,find,ls --model openrouter/z-ai/glm-5.3 --thinking max "$(cat .second-opinion.md)" </dev/null
```

**OpenCode:** use plan mode and deny its task tool for this consultation. The inline config applies only to this process:
```bash
OPENCODE_CONFIG_CONTENT='{"agent":{"plan":{"permission":{"task":"deny"}}}}' command opencode run --agent plan -m openrouter/moonshotai/kimi-k3 --variant max "$(cat .second-opinion.md)" </dev/null
```

### Step 3: Evaluate Confidence

After receiving responses, evaluate each for confidence level:

**High Confidence Indicators:**
- Direct, specific recommendations
- References to specific code, files, or patterns
- Clear reasoning with concrete examples
- Definitive statements about approach

**Low Confidence Indicators:**
- Hedging language: "It depends", "possibly", "might", "could be"
- Requests for more context: "I'd need to see", "without more context"
- Very generic advice that could apply to any situation
- Uncertainty markers: "I'm not sure", "hard to say"
- Questions back to you about the problem

### Step 4: Iterate If Needed (Default Mode Only)

If confidence is LOW for any advisor:

1. Identify what context is missing based on their feedback
2. Gather additional context (read relevant files, clarify requirements)
3. Overwrite `.second-opinion.md` with enhanced context
4. Re-query the low-confidence advisor using the same command
5. Can iterate up to 2 times per advisor

Skip this step entirely if `--quick` flag was used.

### Step 5: Present Results

Format the responses for the user:

```markdown
## Second Opinions

### {advisor 1}
{advisor_1_response}

### {advisor 2}
{advisor_2_response}

### {advisor 3}
{advisor_3_response}

### My Take
{your brief synthesis - where they agree, disagree, and your recommendation}
```

Name each advisor heading after the CLI and the model it ran (e.g. `Codex`, `Pi (<model>)`).

If iteration occurred, note it:
```markdown
*Note: Re-queried {advisor} with additional context after initial response lacked confidence.*
```

### Step 6: Clean Up

Delete `.second-opinion.md` using the Bash tool:
```bash
rm .second-opinion.md
```

## Timeouts

Use the `{timeout}` value (default 300s) for each advisor's Bash timeout.

## Error Handling

- If one advisor fails, continue with the others
- If all fail, inform the user and offer to retry

## Key Differences from /debate

| Aspect | /second-opinion | /debate |
|--------|-----------------|---------|
| Rounds | 1-3 (with iteration) | 1-10 |
| Quick mode | Yes (`--quick`) | No |
| State files | None | Full state tracking |
| Session mgmt | No sessions | UUID tracking |
| Output files | None | rounds/, synthesis.md |
| Purpose | Quick check | Deep analysis |
| Speed | ~1-3 min | 5-30 min |
| Read-only | Yes (enforced) | Configurable |

## Examples

```
/second-opinion Should I use useCallback here or is it premature optimization?
/second-opinion Is this the right place to add error handling?
/second-opinion Review my approach to implementing this feature
/second-opinion --quick Just tell me if this pattern looks right
/second-opinion  # Uses current context from conversation
```

## Troubleshooting

### Advisor times out or fails to respond
**Solution:** Increase the timeout with `--timeout=600` or use `--quick` to skip iteration.
