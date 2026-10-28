---
name: retro
description: Look back over AI-coding sessions (this one, or recent session logs) and propose improvements to the agent's environment.
disable-model-invocation: true
argument-hint: "'this' for the current session, or how many recent session logs to mine (default 50)"
---

# Retro

Turn sessions into a ranked list of concrete improvements to the agent's **environment**, not the code. Read-only analysis; **never modify the log files**. Output a numbered proposal list with one verbatim (redacted) evidence line per finding, then let the user pick which to apply.

**Scope.** `this`, or a run straight after a build or a bug fix: the current session. Its conversation is already in context, so skip steps 1–3 and apply the lenses in step 4 to it. After the context was cleared, find that session's log in step 1 and mine only it. Otherwise: the N most recent sessions, steps 1–6.

## Where the logs live

- **Claude Code:** `~/.claude/projects/<slug>/*.jsonl` (top-level sessions). Per-session subagent transcripts are under `<uuid>/subagents/agent-*.jsonl`: **skip these** when counting "sessions"; they're part of a parent.
- **Codex:** `~/.codex/sessions/<year>/<month>/<day>/rollout-*.jsonl` and `rollout-*.jsonl.zst`. Child-agent rollouts belong to their parent session.
- **Grok:** `~/.grok/sessions/<url-encoded cwd>/<id>/chat_history.jsonl`. A cwd under `/private/tmp` is usually a headless `panel` run.
- **agy (Antigravity CLI):** every user prompt is in `~/.gemini/antigravity-cli/history.jsonl` (`display`, `workspace`, `conversationId`); the rest of the conversation is `~/.gemini/antigravity-cli/conversations/<conversationId>.db`, SQLite with protobuf payloads.

The first three are JSONL, one event per line. Stream `.jsonl.zst` through `zstd -dc -- FILE`; keep archives intact. If no Zstandard reader is available, report the excluded archives and the incomplete coverage. Open every log read-only.

## 1. Pick the N most recent sessions

Default N = 50 **parent sessions** unless the user gives a number. Follow
[session selection](references/session-selection.md): discover plain and compressed logs,
group children under their parents, distinguish human sessions from automated runs,
then select N. Report parent counts by harness, child logs inspected, exclusions, and
unreadable files. Selection is complete when each selected parent has a source path
and its available child paths; children never consume another session slot.

## 2. Extract signal (use jq: do NOT cat whole files)

Files are large and full of tool-output noise. `jq` is the right tool. Four formats:
For a compressed Codex file, replace `jq FILTER FILE` below with
`zstd -dc -- FILE | jq FILTER`. Preserve the archive path and decompressed line number
in evidence. A user-role message is not proof of human authorship: exclude preambles,
agent briefs, relayed messages, and quoted earlier corrections from human counts.

**Claude Code**
```bash
# human-typed messages (string form)
jq -rc 'select(.type=="user" and (.message.content|type=="string")) | .message.content' FILE
# human messages (array form; skip <command-name>/system-reminder noise by eye)
jq -rc 'select(.type=="user" and (.message.content|type=="array")) | .message.content[]? | select(.type=="text") | .text' FILE
# messages the user queued while a turn ran (excluding subagent <task-notification> blobs): many corrections live only here
jq -rc 'select(.type=="queue-operation" and .operation=="enqueue") | .content | select(type=="string" and (startswith("<task-notification>") | not))' FILE
# bash commands the assistant ran
jq -rc 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Bash") | .input.command' FILE
# tool errors
jq -rc 'select(.type=="user") | .message.content[]? | select(.type=="tool_result" and .is_error==true) | (.content|if type=="array" then (map(.text//"")|join(" ")) else tostring end)' FILE
```

**Codex** (current rollouts have no `user_message` events; that query only works on older logs)
```bash
# human messages (the FIRST one or two are the AGENTS.md / environment preamble: ignore them)
jq -rc 'select(.type=="response_item" and .payload.type=="message" and .payload.role=="user") | .payload.content[]?.text' FILE
# older logs only
jq -rc 'select(.type=="event_msg" and .payload.type=="user_message") | .payload.message' FILE
# tool calls (shell runs inside custom_tool_call "exec")
jq -rc 'select(.type=="response_item" and (.payload.type=="custom_tool_call" or .payload.type=="function_call")) | (.payload.input // .payload.arguments)' FILE
# tool outputs (grep for errors)
jq -rc 'select(.type=="response_item" and (.payload.type=="custom_tool_call_output" or .payload.type=="function_call_output")) | (.payload.output|tostring)' FILE | grep -iE 'error|not found|exception|fatal|denied' | head
```

**Grok**
```bash
# human messages (the first one or two carry the system-reminder preamble)
jq -rc 'select(.type=="user") | .content | if type=="array" then map(.text//"")|join(" ") else tostring end' FILE
jq -rc 'select(.type=="assistant") | .tool_calls[]? | tostring' FILE
# current logs use tool_result; older logs use tool
jq -rc 'select(.type=="tool_result" or .type=="tool") | .content|tostring' FILE | grep -iE 'error|not found|failed|denied' | head
```

**agy**
```bash
# human messages for one conversation (ID = the .db basename)
jq -rc --arg id ID 'select(.conversationId==$id) | .display' ~/.gemini/antigravity-cli/history.jsonl
# when that id is absent from history, the prompt is step 14 in the db
sqlite3 -readonly FILE "select step_payload from steps where step_type=14" | strings -n 8
# step types: 14 user prompt, 15 model text, 132 tool call + result, 101 message from another conversation
sqlite3 -readonly FILE "select step_payload from steps where step_type=132" | strings -n 8 | grep -iE 'error|not found|failed|denied' | head
```

Surface corrections fast by grepping extracted human messages:
`grep -iE "no,|actually|that.?s wrong|don.?t |stop |instead|you should have|i told you|revert|why did you|wrong"`

## 3. Fan out: one subagent per batch

50 sessions won't fit one context. Split the file list into ~7 round-robin batches (so big files spread out) and dispatch one subagent per batch **in parallel**, on a cheaper model where the harness lets you pick one (extraction, not judgement), each with the cheat-sheet above for the formats in its batch and an identical brief (in Claude Code with this plugin installed, `subagent_type=leek-skills:session-miner`: log-read-only, skips project CLAUDE.md, and remembers patterns from earlier retros so it can mark them recurring; elsewhere, any sub-agent the harness offers). Each subagent returns a structured findings list; the orchestrator dedupes across batches and synthesizes. Round-robin assignment:
```bash
awk '{ b=((NR-1)%7)+1; print > ("batch_" b ".jsonl") }' parents.jsonl
```

## 4. What to find

You are proposing improvements to the agent's **environment**, so that future runs go better. Each lens below names what to look for and the moment that triggers it.

**Evidence lenses**: what the transcript shows happening:

1. **Corrections**: the user pushed back ("no", "actually", "that's wrong", "don't do that", reverting/redoing). Highest value, capture every one.
2. **Repeated / errored commands**: a command or tool that errored, or was retried several times before working. Note what finally fixed it.
3. **Repeated setup steps**: the same setup/config/env/login/build/cache-clear rediscovered across more than one session.
4. **Content moments**: something worth an article, tweet, tutorial, diagram, prompt, product idea, or example.

**Environment lenses**: what should change so it stops happening:

5. **Navigation**: how easily did the agent find the right files? Hidden dependencies between files? Would a context pointer help? _Use when_ the session spent a long time hunting for one piece of information.
6. **Automated checks**: could a linter, type check, test, or filesystem check have caught this? Read the repo's own check commands first (`composer.json` / `package.json` scripts, Pint/PHPStan/Larastan config, the CI workflow), so a check that exists but is unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint, static analysis, or tests) is itself a finding. _Use when_ the agent made a mistake a machine could have caught, or the repo has no guardrail at all.
7. **Coding standards**: should the **reviewer** get a new rule, or an existing one clarified or removed? Classify the violation first. A **mechanical** one (a fixed syntactic pattern, a banned function or facade, an import shape, a file-location rule) gets a deterministic check instead of a prose rule: a custom PHPStan/Larastan or ESLint rule, a Pest arch test, a pre-commit hook, or a CI job, whichever the repo's existing guardrail makes cheapest. Reserve the standards doc for **judgement calls** (cross-file consistency, "matches the surrounding style", anything no check could replace). _Use when_ review failed to catch a mistake.
8. **Steering files**: are there instructions in `CLAUDE.md` / `AGENTS.md` (repo or global) that belong in coding standards or an automated check instead? _Use when_ a steering file is large and unwieldy.
9. **Tool economy**: expensive or chatty tool calls that could be streamlined; custom CLIs or MCP servers that are token-inefficient. _Use when_ one call burned a visible share of the context.
10. **No-ops**: instructions in steering files that don't change the agent's behaviour versus the default. _Use when_ the steering files have grown without pruning.
11. **Information access**: could the agent have been *given* the missing fact? Teed dev-server logs, read-only access to a third-party service, a status endpoint. _Use when_ a crucial piece of information simply wasn't reachable.

## 5. Redaction (mandatory)

In every quoted evidence line, replace emails, API keys, tokens, secrets, passwords, and bearer strings with `[REDACTED]`. Keep quotes short.

## 6. Output: a numbered proposal list

Before proposing a change, read the current destination and compare the observed behavior with its instructions. Recover the loaded skill version/path from the transcript when possible (including plugin cache versions); otherwise record **version unknown**. Compare the session date/version with the relevant fix's history. Classify each candidate as **missing guidance**, **existing guidance ignored**, **already fixed**, or **outside this skill's control**. Repeated evidence from an old version is not a current regression. Already-fixed and out-of-scope items belong in a brief exclusions note; ignored guidance needs an enforcement or clarity improvement, not a duplicate rule.

For each finding, give: the proposal, **the one verbatim (redacted) evidence line it came from** (source path and line, or SQLite step index), the loaded version or **version unknown**, its disposition above, the current destination passage, and a one-sentence why. Label assistant diagnoses and summaries as such rather than human corrections. Destinations:

- a content idea to draft / add to the idea library
- a line to add to `CLAUDE.md` / `AGENTS.md` (name the file)
- a slash command or skill to add or update (name it)
- a hook that should run automatically
- a tool or CLI that should be fixed
- a config or settings change
- **or nothing**, if it was a genuine one-off

**Do not change anything.** Present the list and let the user choose which to apply (`AskUserQuestion` where available: one `multiSelect: true` question per destination, up to 4 questions per call and 4 options each, further rounds for the rest; otherwise the user picks by number in chat). Lead with the cross-cutting themes (patterns that recurred across 3+ sessions are the highest-value to act on).

## Reference: where a fix belongs

All work goes through two stages, and they carry very different context pressure. The **implementation** agent bears the most: it explores, writes code, and debugs failures. The **reviewer** bears the least, it receives a diff, so it needs no exploration and usually writes no code.

So **standards belong to the reviewer, not the implementer.** A proposal of the form "tell the agent to always do X while coding" is nearly always better placed as a review rule, where it costs nothing until there is a diff to check.

The destinations, ranked by what they cost:

- `CLAUDE.md` / `AGENTS.md` sit in every agent's context in this repo. Spend lines here incredibly sparingly, and mostly on **context pointers** to other files.
- A coding standards doc is read at review time, not implementation time, cheap, and the right home for most rules.
- Reference docs are free until a pointer reaches them. Look for an existing doc before writing a new one.
- A skill costs its description in context if model-invoked, nothing if user-invoked. Follow `writing-for-agents`.
