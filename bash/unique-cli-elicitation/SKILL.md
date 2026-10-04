---
name: unique-cli-elicitation
description: >-
  ALWAYS use this skill whenever you would otherwise ask the user a
  question in free-form chat -- for clarifications, confirmations
  (especially destructive actions), missing parameters, multiple-choice
  decisions, or structured form input. Elicitations are routed through
  the Unique AI Platform UI via `unique-cli elicit create` + `elicit wait`
  (the default polling pattern) or a single supervised `unique-cli elicit
  ask` call (only when your agent instructions say your environment
  supervises the wait) so the user gets a proper structured prompt and
  you get a structured answer back.
  Do NOT ask the user in plain chat when you can use this skill instead.
---

# Unique CLI -- Elicitation (Ask the User)

Use this skill **whenever you need input from the user** -- a clarifying question, a confirmation before a destructive action, a choice between options, or a structured form. Elicitations create a first-class UI prompt on the Unique AI Platform and return the answer as structured JSON.

> **Rule of thumb:** if you catch yourself about to write "Could you clarify…?" or "Do you want me to…?" or "Which one should I pick?" in chat, stop and use an elicitation instead (see "Two patterns" below for which command sequence to use).

!!! danger "`--visible` is currently MANDATORY"
    You **must always create elicitations with visibility on** (it is on by default for both `elicit create` and `elicit ask` — just don't pass `--no-visible`). Until the UN-19815 UI fix ships in your environment, an elicitation created without the visibility workaround is stored by the backend but **never rendered in the chat UI** — the user simply never sees the question and you will wait forever. There is no situation in which you should disable it today.

!!! danger "A non-terminal status is not an answer"
    This is the single rule that matters most, in **every** pattern below:
    `PENDING` is not `DECLINED`, is not an answer, and is never a reason to
    stop or proceed. Never treat a non-terminal status as a decline, never
    proceed on an unanswered form, and never fabricate what you think the
    user would say. If the last known status is `PENDING`, the only correct
    next action is to keep waiting -- either loop `elicit wait` again
    (Pattern A) or re-issue `elicit wait <id>` on the same elicitation
    (Pattern B) -- until you observe one of the terminal statuses in
    "Reading the response" below.

## Two patterns -- your agent instructions decide which one to use

There are two valid ways to wait for an elicitation's answer. **Which one you
use is decided by your agent instructions (system prompt / `AGENTS.md`), not
by this skill file guessing which harness you're running in:**

- **Your instructions are silent, or say nothing about your environment
  supervising long-running waits** -- use **Pattern A: `elicit create` +
  short polling loop with `elicit wait`** below. This is the default and is
  safe everywhere, including inside a harness whose Bash/shell tool has its
  own foreground-wait timeout (Claude Code, Codex, ~2 minutes commonly).
- **Your instructions explicitly say your environment supervises the wait**
  for a single long-running tool call (it will not silently background or
  kill the process before the human answers) -- use **Pattern B: a single
  supervised `elicit ask` call** below instead.

If in doubt, use Pattern A -- it is correct in every environment, whereas
Pattern B is only correct in one that actually supervises the wait. Neither
pattern is forbidden; pick the one your instructions call for.

## Pattern A: `elicit create` + short polling loop with `elicit wait` (default)

Do **not** call `elicit ask` from inside an agent harness (Claude Code, Codex,
or any environment where your Bash/shell tool has its own foreground-wait
timeout — commonly ~2 minutes) **unless your agent instructions explicitly
say your environment supervises the wait (see Pattern B below)**. `elicit
ask` blocks synchronously for up to `--timeout` seconds (default 2 hours)
waiting for the human to answer, but a human reading and answering a prompt
routinely takes longer than a typical Bash tool timeout. If that timeout
fires first and your instructions did not say otherwise, your harness will
silently detach the process to the background and hand you a "running in
background" stub instead of the real answer — you will not see the user's
response, and the chat may appear stuck to the user.

Instead, use `elicit create` (returns immediately) followed by a short
polling loop with `elicit wait`, where **every individual command finishes
comfortably under your harness's Bash foreground timeout** (90s is a safe
default — comfortably under Claude Code's ~120s):

1. **Create** the elicitation:

   ```bash
   create_output=$(unique-cli elicit create "<question>" \
     --mode FORM \
     --tool-name "<tool_name>" \
     --chat-id "$UNIQUE_CHAT_ID" \
     --expires-in 7200 \
     --schema '<json schema>')
   elicitation_id=$(echo "$create_output" | awk '/^Created elicitation/{print $3}')
   ```

2. **Poll in short bursts**, each well under your harness's Bash foreground
   timeout:

   **You MUST NOT stop after a single `PENDING` result.** If `elicit wait`
   returns `PENDING`, immediately call `elicit wait` again (same elicitation
   id) — as its own new tool call if you are not running the loop below —
   and keep doing so until you see a terminal status or the elicitation
   reaches its `--expires-in` deadline. Never tell the user you "stopped
   waiting" or "gave up" while `PENDING` is the last known status.

   ```bash
   status="PENDING"
   elapsed=0
   total_timeout=7200   # match --expires-in above
   chunk=90
   while [ "$elapsed" -lt "$total_timeout" ]; do
     result=$(unique-cli elicit wait "$elicitation_id" --timeout "$chunk" --poll-interval 3)
     status=$(echo "$result" | awk -F': *' '/^Status:/{print $2}')
     case "$status" in
       RESPONDED|ACCEPTED|DECLINED|CANCELLED|REJECTED|EXPIRED|COMPLETED) break ;;
     esac
     elapsed=$((elapsed + chunk))
   done
   ```

   Each `elicit wait ... --timeout 90` call is a normal, short-lived Bash
   invocation that always returns within ~90 seconds — either with a
   terminal status (done) or the current non-terminal status (loop again).
   Your harness never sees a single call run long enough to background it.

3. Parse `Response:` from the final `$result` exactly as you would with
   `elicit ask`'s output — the format is identical (see "Reading the
   response" below).

`elicit ask` remains the right choice for **non-agent, scripted, or
human-operated CLI usage** where a single blocking call is expected and
there is no surrounding tool-timeout concern (tests, ops scripts, manual CLI
use), and for **Pattern B below** when your instructions say your
environment supervises the wait. Do not reach for it from inside an agent
turn unless one of those two conditions applies.

```bash
unique-cli elicit ask "<question>" [options]
```

!!! danger "`--chat-id` is MANDATORY"
    You **must always pass** `--chat-id "$UNIQUE_CHAT_ID"` on every
    `elicit create`/`elicit ask` call. Omit `--message-id`: the CLI resolves
    the current turn's assistant message ID from `$UNIQUE_TURN_IDENTITY_FILE`
    (preferred) or `$UNIQUE_MESSAGE_ID`. Do **not** pass a stale
    `$UNIQUE_MESSAGE_ID` from a persistent process environment.

## Pattern B: a single supervised `elicit ask` call

Use this **only when your agent instructions explicitly say your
environment supervises the wait** for a single long-running tool call --
i.e. it will not silently background or kill the process before the human
answers. Do not use Pattern B just because it is simpler; use it only
because your instructions told you your environment can safely block for
the full wait.

```bash
unique-cli elicit ask "<question>" \
  --chat-id "$UNIQUE_CHAT_ID" \
  --expires-in 7200 \
  --timeout 1800
```

- **`--expires-in`** sets how long the request stays live on the platform
  (a human-scale deadline, e.g. `7200` = 2 hours) independently of
  **`--timeout`**, which is how long *this call* blocks. Set `--timeout` to
  match your supervisor's own wait budget; omit `--expires-in` only if you
  want it to default to `--timeout` (today's coupled behavior, unchanged).
- Immediately after creating the elicitation -- before it starts waiting --
  the CLI writes one line to **stderr** (never stdout):
  `UNIQUE_ELICITATION_CREATED id=<id> expires_at=<iso8601>`. A supervisor
  watching stderr can capture the elicitation id the instant it exists,
  without waiting for `ask` to return.
- While waiting, transient failures (connection errors, timeouts, 5xx) are
  retried automatically with bounded exponential backoff and logged to
  stderr -- you do not need your own retry loop around `ask` to survive a
  single dropped connection. 4xx errors are not retried.
- The result of the single call **is** the answer. Check `Status:` exactly
  as described in "Reading the response" below, and the same rule applies
  if `ask` still returns `PENDING` when `--timeout` elapses: that is **not**
  a decline and not a reason to stop -- the elicitation is still live on
  the platform (until `--expires-in`), so re-issue `elicit wait <id>` on the
  same id to keep waiting for the real answer.

## When to use

| Situation | Use elicitation? |
|-----------|------------------|
| Clarifying an ambiguous request | Yes |
| Confirming a destructive / irreversible action | Yes, always |
| Picking among 2+ concrete options | Yes |
| Gathering structured data (rating, date, options) | Yes |
| Quick status update / "I'll start now" message | No -- just talk |
| Purely informational output (results, summaries) | No |

## Examples

> The examples below use `elicit ask` for brevity to show the schema shapes.
> From an agent harness whose instructions are silent on supervision, use the
> same `--schema`/`--message`/`--tool-name` arguments with `elicit create`
> instead, then poll with `elicit wait` as shown in "Pattern A" above (or use
> `elicit ask` directly per "Pattern B" if your instructions say your
> environment supervises the wait).

### Minimal — free-text answer

```bash
unique-cli elicit ask "Which quarter should I report on?" \
  --chat-id "$UNIQUE_CHAT_ID"
```

Under the hood this creates a form with a single required string field `answer`. The reply you receive will look like:

```
ID:         elicit_abc123
Status:     RESPONDED
Mode:       FORM
...
Response:   {"answer": "Q1"}
Responded:  2026-04-16 14:22
```

Parse the JSON next to `Response:` to get the user's answer.

### Multiple-choice (recommended for picks / confirmations)

Provide an explicit JSON schema so the user sees proper UI controls instead of a free-text box. Use `enum` for finite choices.

```bash
unique-cli elicit ask "Which report format do you want?" \
  --chat-id "$UNIQUE_CHAT_ID" \
  --schema '{
    "type": "object",
    "properties": {
      "format": {
        "type": "string",
        "enum": ["PDF", "DOCX", "Markdown"],
        "description": "Output format"
      }
    },
    "required": ["format"]
  }'
```

### Confirmation (destructive action)

Always use this before `rm`, `rmdir -r`, mass uploads, or anything irreversible.

Use an **empty-properties schema** — the UI's Confirm/Cancel buttons ARE the
consent. Do **not** add a boolean `confirm` field: the button and the checkbox
are two separate signals, and a user who presses Confirm with the box unchecked
would show as **Accepted** in the UI while you would read `confirm: false` and
wrongly treat it as declined.

```bash
unique-cli elicit ask "Permanently delete /Archive/2024 and everything inside it? Confirming deletes it immediately — this cannot be undone." \
  --chat-id "$UNIQUE_CHAT_ID" \
  --schema '{"type": "object", "properties": {}}'
```

Proceed **only** if the `Status:` is `ACCEPTED`. Treat `DECLINED`, `REJECTED`, `CANCELLED`, or `EXPIRED` all as "do not proceed" -- tell the user you stopped and return control. Put everything the user needs to decide into the message text, since the form has no fields.

Confirm on a form with fields is the same consent. If you still need inputs
(e.g. which folder to delete), ask for them and state the consequence in the
same `elicit ask` message, then act on `ACCEPTED` -- do not add a checkbox for
the consent. Only split into a second, empty-schema confirmation when the
consequence depends on the answers and the user should see it before you act
(e.g. "Archive/2024 holds 1,234 files, 3 shared with other teams").

### Structured form (multiple fields)

```bash
unique-cli elicit ask "Please provide report settings" \
  --chat-id "$UNIQUE_CHAT_ID" \
  --schema '{
    "type": "object",
    "properties": {
      "quarter":   {"type": "string", "enum": ["Q1", "Q2", "Q3", "Q4"]},
      "year":      {"type": "integer", "minimum": 2000, "maximum": 2100},
      "recipients":{"type": "array", "items": {"type": "string", "format": "email"}},
      "include_appendix": {"type": "boolean", "title": "Include appendix"}
    },
    "required": ["quarter", "year"]
  }'
```

## Options

The table below documents `elicit ask`'s flags (used in both Pattern A's
"scripting" case and Pattern B). `elicit create` takes the same `--chat-id`,
`--message-id`, `--tool-name`, `--schema`, `--metadata`, and `--assistant-id`
flags, plus `--expires-in <seconds>` (`elicit create` has no `--timeout`/
`--poll-interval` -- those two apply only to `elicit wait`, which you call
separately in the Pattern A polling loop). `elicit create` also takes
`--mode FORM|URL` (default: `FORM` — you only need to pass it for URL
elicitations).

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--chat-id` | `-c` | none | **MANDATORY.** Chat to show the question in. Always pass `"$UNIQUE_CHAT_ID"`. Without it the visibility workaround cannot run and the user will not see the elicitation. |
| `--message-id` | `-m` | auto | Optional. Prefer omitting this flag — the CLI resolves the current turn's message ID from `$UNIQUE_TURN_IDENTITY_FILE` (preferred) or `$UNIQUE_MESSAGE_ID`. Do not pass a stale env value from a persistent process. |
| `--tool-name` | `-t` | `agent_question` | Short snake_case label shown to the user (e.g. `clarify`, `confirm_delete`, `choose_report`). |
| `--schema` | | single `answer` string | JSON Schema for the form body. |
| `--expires-in` | | `--timeout`'s value | Seconds before the platform auto-expires the request, decoupled from `--timeout`. This is the flag Pattern B uses to give the elicitation a human-scale deadline (e.g. `7200`) independent of the caller's own wait budget. Omit it to keep today's coupled behavior. |
| `--timeout` | | `7200` | Max seconds to block locally before giving up. Unless you pass `--expires-in`, this is also when the request expires on the platform, so the prompt expires exactly when you stop waiting and the chat UI can offer the user a way to continue. |
| `--poll-interval` | | `2.0` | Seconds between status polls. |
| `--metadata` | | none | `key=value` metadata (repeatable). |
| `--assistant-id` | | `$UNIQUE_ASSISTANT_ID`, else latest assistant in chat | Assistant id for the placeholder message created by the visibility workaround. Set this (or export `UNIQUE_ASSISTANT_ID`) only if the chat is brand-new with no prior assistant messages. |

!!! danger "Never pass `--no-visible`"
    The visibility workaround is on by default. **Do not pass `--no-visible`.** Without it the elicitation is invisible in the chat UI, the user never answers, and `elicit ask` blocks until `--timeout`. This is true in every environment today — there is no correct use of `--no-visible` from an agent.

## Reading the response

The command prints a key-value block terminated by:

```
Status:     <TERMINAL_STATUS>
...
Response:   <JSON or "(none)">
```

Terminal statuses:

| Status | Meaning | What to do |
|--------|---------|------------|
| `RESPONDED` / `ACCEPTED` / `COMPLETED` | User answered, or confirmed (accepted) an empty-schema confirmation | Parse `Response:` JSON and proceed. |
| `DECLINED` / `REJECTED` | User explicitly declined, or rejected (declined) an empty-schema confirmation | Do not proceed. Acknowledge and stop. |
| `CANCELLED` | Cancelled (by user or system) | Do not proceed. |
| `EXPIRED` | Timed out on the platform — the user did not answer before the request's expiry (`--timeout`, or `--expires-in` if you passed it) | Ask again only if the task still needs it; do not treat the expiry as approval. |

`ACCEPTED`/`REJECTED` and `RESPONDED`/`DECLINED` are functionally
equivalent terminal outcomes -- `ACCEPTED`/`REJECTED` are the accept/decline
synonyms produced by some response paths (e.g. the Codex approval-bridge
integration), while `RESPONDED`/`DECLINED` are produced by others. Treat
them the same way: `ACCEPTED` like `RESPONDED` (proceed), `REJECTED` like
`DECLINED` (stop).

Because `ask` derives the request's expiry from `--timeout` (unless you pass `--expires-in`), when the user does not answer in time the platform expires the request and `elicit ask` returns a clean `EXPIRED` status (rather than a local-only timeout). If you instead see `elicit: timed out after Ns ...` (Pattern B) or `elicit: still PENDING after Ns ...` (Pattern A's `elicit wait`), that is **not** `EXPIRED` -- see the danger box at the top of this file: keep waiting, do not treat it as a stopping condition. If this happens repeatedly, double-check that you passed `--chat-id` and did not pass `--no-visible` — an invisible elicitation is the most common cause of a local timeout.

### Repeat the answer back in chat

After a `RESPONDED` / `COMPLETED` elicitation, always repeat the user's answer back in the normal chat before you continue. This keeps the decision in the chat history and makes it clear what the user said.

Write this as a user-readable summary, not as raw JSON. Use the field descriptions and option labels from the schema to translate the response into plain language:

```markdown
Got it — you chose Markdown for the report format and asked me to include the appendix.
```

If the exact structured response is useful for auditing or debugging, put it behind a collapsed details block after the readable summary instead of leading with it:

````markdown
<details>
<summary>Structured elicitation response</summary>

```json
{"format":"Markdown","include_appendix":true}
```

</details>
````

Do not expose raw JSON by default when a natural-language confirmation would be clearer.

## Scripting pattern (non-agent-harness only)

This one-shot pattern is for **scripts, tests, or manual CLI use outside an
agent harness** — i.e. contexts with no Bash-tool foreground timeout to worry
about. From inside an agent harness whose instructions are silent on
supervision, use the `elicit create` + `elicit wait` polling pattern from
"Pattern A" above instead (or "Pattern B" if your instructions say your
environment supervises the wait); the output parsing below (pulling
`Response:` out of the text) is identical either way, only the command(s)
producing that output differ.

In a shell script or agent tool wrapper, capture the output and pull out the `Response:` line:

```bash
result=$(unique-cli elicit ask "Which region?" \
  --chat-id "$UNIQUE_CHAT_ID" \
  --schema '{
    "type":"object",
    "properties":{"region":{"type":"string","enum":["EU","US","APAC"]}},
    "required":["region"]
  }')

answer=$(echo "$result" | awk -F'Response:[[:space:]]*' '/^Response:/{print $2}')
region=$(echo "$answer" | jq -r '.region')

case "$region" in
  EU|US|APAC) echo "Proceeding with region=$region";;
  *)          echo "No valid answer ($region); aborting"; exit 1;;
esac
```

## Schema tips

- Always set `"required"` for fields you actually need -- this guarantees the user cannot submit an empty form.
- Use `enum` for closed choices so the UI can render a selector.
- The Confirm button is the consent, on any form. Never add a boolean `confirm` or `acknowledge` field (the button and the checkbox are two separate signals that can disagree); put the consequence in the message text instead. When there is nothing else to ask, use an **empty-properties schema** (`{"type": "object", "properties": {}}`) and gate on `Status: ACCEPTED`. Reserve `"type": "boolean"` for genuine data fields where `false` is a valid answer the user can still submit with Confirm (e.g. `include_appendix`).
- `"required"` on a boolean means "must be answered", not "must be ticked". An unchecked box is a valid `false` and the form submits with it; there is no way to force a checkbox on.
- Always give booleans a `"title"`. The checkbox label and its required marker come from `title`; with only a `description` the box renders unlabelled.
- Add short `description` strings -- they are shown as help text next to each field.
- Keep schemas small. Ask at most 5 questions in a single elicitation; if you need more, split the flow so the user is not confused by an oversized form.

## Agent workflow rules

1. **Default to `elicit create` + `elicit wait` polling (Pattern A).** If you need an answer from the user, use this pattern, not a chat message -- unless your agent instructions explicitly say your environment supervises the wait, in which case use a single `elicit ask` call (Pattern B). See "Two patterns" above.
2. **Always pass `--chat-id "$UNIQUE_CHAT_ID"`.** Without it the elicitation is not attached to a chat and the user will not see it.
3. **Omit `--message-id`.** The CLI resolves the current turn's assistant message ID from `$UNIQUE_TURN_IDENTITY_FILE` (preferred) or `$UNIQUE_MESSAGE_ID`. Do not pass a stale `$UNIQUE_MESSAGE_ID` from a persistent process environment.
4. **Never pass `--no-visible`.** See the warning above. The visibility workaround is mandatory today.
5. **Never run destructive CLI commands without a confirmation elicitation.** This includes `rm`, `rmdir -r`, bulk renames, large uploads, schedule deletion, etc.
6. **Pick a meaningful `--tool-name`.** `confirm_delete`, `choose_region`, `pick_report` -- short snake_case describing the intent.
7. **Constrain answers with a schema** whenever the valid set is finite -- don't rely on parsing free text when `enum` is an option.
8. **Repeat answered elicitations back in chat.** Summarize what the user chose in natural language before acting on it; hide raw JSON in a collapsible details block only when it adds value.
9. **Handle non-`RESPONDED`/`ACCEPTED` outcomes explicitly.** If the status is `DECLINED` / `REJECTED` / `CANCELLED` / `EXPIRED`, tell the user you stopped and ask what they want to do next instead of silently proceeding. A non-terminal (`PENDING`) status is never one of these outcomes -- see the danger box at the top of this file.
10. **Don't spam elicitations.** One well-designed form with a few related fields is better than five sequential yes/no questions.
11. **Cap each elicitation at 5 questions.** If you need more than 5 answers, split them into multiple focused elicitations so the user can respond confidently.
12. **Never make a single blocking call longer than your harness's Bash foreground timeout, unless your instructions say your environment supervises the wait.** In Pattern A, use `--expires-in` on `elicit create` to set the real, human-scale deadline (e.g. 7200s / 2 hours), but keep each individual `elicit wait --timeout N` call short (≈90s) and loop until a terminal status or the overall deadline is reached. In Pattern B, `--expires-in` on `elicit ask` does the same job, decoupled from the (now safely long) `--timeout` your supervisor manages. Never call `elicit ask` with a multi-minute `--timeout` from an agent harness unless Pattern B applies.

## Prerequisites

Requires these environment variables:

```bash
UNIQUE_USER_ID    # User ID (required)
UNIQUE_COMPANY_ID # Company ID (required)
UNIQUE_API_KEY    # API key -- optional on localhost / secured cluster
UNIQUE_APP_ID     # App ID -- optional on localhost / secured cluster
UNIQUE_CHAT_ID    # Current chat ID -- always pass as --chat-id (required)
UNIQUE_TURN_IDENTITY_FILE # Per-turn identity JSON — CLI resolves message ID from here
UNIQUE_MESSAGE_ID # Fallback message ID when no turn-identity file is present
```

Install: `pip install unique-sdk`
