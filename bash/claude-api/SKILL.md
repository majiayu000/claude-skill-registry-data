---
name: claude-api
description: Anthropic Claude API patterns for Python and TypeScript. Covers Messages API, streaming, tool use, vision, extended thinking, batches, prompt caching, and Claude Agent SDK. Use when building applications with the Claude API or Anthropic SDKs. Do NOT use for Claude Code CLI/harness configuration (claude-code-guide agent) or for authoring MCP servers (mcp-server-patterns skill).
origin: ECC
---

# Claude API

Build applications with the Anthropic Claude API and SDKs.

## When to use

- Building applications that call the Claude API
- Code imports `anthropic` (Python) or `@anthropic-ai/sdk` (TypeScript)
- User asks about Claude API patterns, tool use, streaming, or vision
- Implementing agent workflows with Claude Agent SDK
- Optimizing API costs, token usage, or latency

**When NOT to use:**

- Claude Code CLI features, hooks, settings, or slash commands — that is the `claude-code-guide` agent, not an API integration task
- Authoring MCP servers — use `mcp-server-patterns`
- OpenAI/Gemini image or render pipelines (`scripts/oai_render/`) — different vendor, different SDK

## Inputs

Required before starting — absent any of these, **stop; never proceed** with a placeholder:

1. `ANTHROPIC_API_KEY` present in the environment (`.env` / secret manager — never hardcoded, never committed). Missing key = stop and ask where the secret lives; do **not** fall back to a stub client (fail-open, bug-230 pattern).
2. The SDK installed in the target runtime: `pip show anthropic` or `npm ls @anthropic-ai/sdk` returns a version. Missing = install it; do not vendor or hand-roll HTTP calls.
3. A target model ID that exists on the account — verify against `client.models.list()` (`GET /v1/models`) rather than trusting a remembered ID; the roster changes.
4. In this repo: any call that generates completions costs money → STOP-AND-SHOW manifest + explicit `y` first (CLAUDE.md §1). `count_tokens` and `models.list` generate no completion and need no gate.

## Model Selection

| Model | ID | Best For |
|-------|-----|----------|
| Opus 5 | `claude-opus-5` | Complex reasoning, architecture, research |
| Sonnet 5 | `claude-sonnet-5` | Balanced coding, most development tasks |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast responses, high-volume, cost-sensitive |

Default to Sonnet 5 unless the task requires deep reasoning (Opus) or speed/cost optimization (Haiku).
The roster changes — before hardcoding an ID, verify it exists via `client.models.list()`
(`GET /v1/models`); a retired or mistyped ID returns a 404 `not_found_error` at request time.

## Python SDK

### Installation

```bash
pip install anthropic
```

### Basic Message

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain async/await in Python"}
    ]
)
print(message.content[0].text)
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku about coding"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are a senior Python developer. Be concise.",
    messages=[{"role": "user", "content": "Review this function"}]
)
```

## TypeScript SDK

### Installation

```bash
npm install @anthropic-ai/sdk
```

### Basic Message

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

const message = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Explain async/await in TypeScript" }
  ],
});
console.log(message.content[0].text);
```

### Streaming

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a haiku" }],
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

## Tool Use

Define tools and let Claude call them:

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
)

# Handle tool use response
for block in message.content:
    if block.type == "tool_use":
        # Execute the tool with block.input
        result = get_weather(**block.input)
        # Send result back
        follow_up = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": "What's the weather in SF?"},
                {"role": "assistant", "content": message.content},
                {"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
                ]}
            ]
        )
```

## Vision

Send images for analysis:

```python
import base64

with open("diagram.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "Describe this diagram"}
        ]
    }]
)
```

## Extended Thinking

For complex reasoning tasks:

```python
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{"role": "user", "content": "Solve this math problem step by step..."}]
)

for block in message.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Answer: {block.text}")
```

## Prompt Caching

Cache large system prompts or context to reduce costs:

```python
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=[
        {"type": "text", "text": large_system_prompt, "cache_control": {"type": "ephemeral"}}
    ],
    messages=[{"role": "user", "content": "Question about the cached context"}]
)
# Check cache usage
print(f"Cache read: {message.usage.cache_read_input_tokens}")
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
```

## Batches API

Process large volumes asynchronously at 50% cost reduction:

```python
import time

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"request-{i}",
            "params": {
                "model": "claude-sonnet-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        }
        for i, prompt in enumerate(prompts)
    ]
)

# Poll for completion
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    time.sleep(30)

# Get results
for result in client.messages.batches.results(batch.id):
    print(result.result.message.content[0].text)
```

## Claude Agent SDK

Build multi-step agents:

```python
# Note: Agent SDK API surface may change — check official docs
import anthropic

# Define tools as functions
tools = [{
    "name": "search_codebase",
    "description": "Search the codebase for relevant code",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}]

# Run an agentic loop with tool use
client = anthropic.Anthropic()
messages = [{"role": "user", "content": "Review the auth module for security issues"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )
    if response.stop_reason == "end_turn":
        break
    # Handle tool calls and continue the loop
    messages.append({"role": "assistant", "content": response.content})
    # ... execute tools and append tool_result messages
```

## Cost Optimization

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Prompt caching | Up to 90% on cached tokens | Repeated system prompts or context |
| Batches API | 50% | Non-time-sensitive bulk processing |
| Haiku instead of Sonnet | ~75% | Simple tasks, classification, extraction |
| Shorter max_tokens | Variable | When you know output will be short |
| Streaming | None (same cost) | Better UX, same price |

## Error Handling

```python
import time

from anthropic import APIError, RateLimitError, APIConnectionError

try:
    message = client.messages.create(...)
except RateLimitError:
    # Back off and retry
    time.sleep(60)
except APIConnectionError:
    # Network issue, retry with backoff
    pass
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Environment Setup

```bash
# Required
export ANTHROPIC_API_KEY="your-api-key-here"

# Optional: set default model
export ANTHROPIC_MODEL="claude-sonnet-5"
```

Never hardcode API keys. Always use environment variables.

## Procedure

1. Read the existing call sites first: `grep -rn "import anthropic\|@anthropic-ai/sdk" <project>` —
   reuse the project's client construction and retry/error conventions instead of adding a second style.
2. Verify the SDK is present in the target runtime (`pip show anthropic` / `npm ls @anthropic-ai/sdk`).
   Absent → install via the project's package manager; never vendor or hand-roll raw HTTP.
3. Resolve `ANTHROPIC_API_KEY` from the environment. Absent → **stop** (Inputs rule 1).
4. Pick the model from the table above and verify the ID via `client.models.list()`.
5. Pre-flight the request shape with `client.messages.count_tokens(...)`
   (`POST /v1/messages/count_tokens`) — it validates messages/system/tools and returns the input
   token count without generating a completion.
6. In this repo, present the STOP-AND-SHOW manifest (action, model, estimated tokens/cost) and wait
   for `y` before the first completion-generating call.
7. Implement using the patterns above (streaming for interactive UX, `tools` schema for tool use,
   `cache_control` for repeated large context, Batches for bulk).
8. Wrap every call with the Error Handling pattern; then run Verification below.

## Verification

Each check can return "no". A check that errors or times out is an artifact, not a pass —
re-run it by hand (standard rule 1). Fenced blocks below contain commands only: `#`-prefixed
lines inside them read as markdown headings to section parsers.

**Check 1 — SDK importable, version visible.** `[repro]`

```bash
python3 -c "import anthropic; print(anthropic.__version__)"
```

PASS: prints a version string (e.g. `0.83.0`) and exits 0.

**Check 2 — key present, without echoing the secret.** `[repro]`

```bash
python3 -c "import os,sys; sys.exit(0 if os.environ.get('ANTHROPIC_API_KEY') else 1)"
```

PASS: exits 0. Exit 1 = stop; do NOT proceed with a stub or placeholder key.

**Check 3 — auth and model ID valid; generates no completion.** `[live]`

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

PASS: prints `200`, and the JSON body (re-run without `-o /dev/null`) lists the target model
id in `data[]`. 401 = bad key. Target id absent from `data[]` = fix the model ID before any
paid call.

**Check 4 — request shape valid; free pre-flight, no completion generated.** `[live]`

```bash
python3 -c "
import anthropic
c = anthropic.Anthropic()
print(c.messages.count_tokens(model='claude-sonnet-5',
      messages=[{'role':'user','content':'ping'}]))"
```

PASS: prints a `MessageTokensCount` object with no exception. A 404 `not_found_error` here
means the model ID is wrong — cheaper to learn now than on `/v1/messages`.

Endpoint names, headers, and SDK methods above verified against the Anthropic Python SDK
docs (Context7 `/anthropics/anthropic-sdk-python`, 2026-07-29). `[docs]`

## Worked example

Run on this machine, 2026-07-29, from
`/Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon`:

```
$ python3 -c "import anthropic; print(anthropic.__version__)"
0.83.0

$ python3 -c "import os,sys; sys.exit(0 if os.environ.get('ANTHROPIC_API_KEY') else 1)"; echo "exit=$?"
exit=1
```

Check 1 passed (SDK 0.83.0 installed) `[repro]`; check 2 **failed** — no `ANTHROPIC_API_KEY` in that
shell — so the correct next action was to stop before any API call, not to continue with a placeholder.
`[repro]` A failing gate observed failing is also the proof the gate works (standard rule 3).

## Failure modes

- **Hardcoded or committed API key** — treat as exposed: rotate immediately, purge from history,
  then re-run Verification check 2. Prevention is Inputs rule 1.
- **Missing key silently swallowed** — a client factory that falls back to a mock/stub when
  `ANTHROPIC_API_KEY` is unset ships code that "passes" locally and 401s in production. Fail closed
  (bug-230, ×6: fail-open guards).
- **SIGSEGV on macOS in forked workers** — the Python SDK rides on httpx; darwin `fork()` after the
  proxy resolver initializes crashes the child. Pre-set `no_proxy='*'`/`NO_PROXY='*'` before any
  fork/multiprocessing that touches the client (bug-263, ×7).
- **Retired/mistyped model ID** — surfaces as 404 `not_found_error` only at request time; caught
  earlier by Verification checks 3–4.
- **Truncated output misread as complete** — when `stop_reason == "max_tokens"` the response was cut
  off, not finished. Branch on `stop_reason`; never parse a truncated JSON/tool payload as final.
- **Retry storms on 429** — a bare retry loop without exponential backoff amplifies rate-limit
  errors. Use the Error Handling pattern above; back off, then retry.
- **Cache misses that should be hits** — `cache_control` only pays off when the cached prefix is
  byte-identical across calls. Verify with `usage.cache_read_input_tokens > 0` on the second call;
  0 on every call means the prefix is drifting.
