---
name: b0
description: |
  Delegate tasks to AI agents via Box0. Use when the user asks to
  review code, check security, run tests, compare tools, get multiple
  perspectives, research a topic, analyze data, write docs, or any
  task that could benefit from specialized or parallel execution.
  Also use when the user mentions agent names or says "ask", "delegate",
  "get opinions from", or "have someone".
allowed-tools:
  - Bash
---

# Box0 (`b0`) Multi-Agent Platform

Run AI agents in parallel. Create agents with roles, trigger them on demand or on a schedule, and collect results.

## Setup

### Step 1: Check if Box0 is installed

```bash
b0 --version
```

If this succeeds, skip to Step 3.

### Step 2: Install

```bash
npm install -g @box0/cli@latest
```

If npm is not available, build from source:

```bash
git clone https://github.com/risingwavelabs/box0.git
cd box0 && cargo build --release
export PATH="$PWD/target/release:$PATH"
```

### Step 3: Check if server is running

```bash
b0 server status
```

If this shows "Server is running", skip to Step 5.

### Step 4: Start the server

```bash
b0 server
```

On first start, Box0 creates an admin account and auto-configures `~/.b0/config.toml`.

### Step 5: Install the skill

```bash
npx skills add risingwavelabs/skills --skill b0
```

### Step 6: Verify

```bash
b0 ls
```

This should run without errors. Setup is complete.

Tell the user: "Box0 is installed and ready. You can now delegate tasks to agents."

---

## When to use

When the user's request could benefit from specialized agents or parallel execution, delegate.

## Choosing an agent

**Always use `b0 run` with an existing agent or create one with `b0 add`.** Use `b0 ls` to see what is available.

**Use `b0 add` when:**
- No existing agent matches the task
- The user wants a named agent for future reuse

**Use `b0 run <name>` when:**
- `b0 ls` shows an existing agent that matches the task
- The user mentions an agent by name ("ask the reviewer")

## Commands

```bash
b0 ls                                                  # list available agents
b0 add <name> --instructions "..."                     # create a named agent
b0 add <name> --instructions "..." --every 1h --task "..." # create scheduled agent
b0 add <name> --instructions "..." --webhook           # create agent with trigger URL
b0 add <name> --instructions "..." --webhook-secret s  # create agent with HMAC secret
b0 rm <name>                                           # delete an agent
b0 run <agent> "<detailed task prompt>"                # trigger agent and wait for result
b0 run <agent> "<task>" --timeout 600                  # trigger with custom timeout
b0 info <name>                                         # show agent info including trigger URL
b0 logs <name>                                         # show recent agent logs
b0 update <name> --instructions "..."                  # update agent instructions
```

## How to write task prompts

This is critical. Do NOT forward the user's words. Compose a complete, actionable prompt.

Bad:
```
b0 run reviewer "review this PR"
```

Good:
```
b0 run reviewer "Review the changes on branch feature-timeout in this repo.
The PR adds timeout handling to src/handler.rs.
Focus on correctness, edge cases, and error handling.
Cite line numbers for any issues found."
```

Steps:
1. **Gather context first** - read relevant files, run `git diff`, check the branch
2. **Include specifics** - file paths, line numbers, branch names, what changed and why
3. **State the deliverable** - what the agent should produce (a list of issues, a summary, a fix)

For large content (diffs, file contents), pipe via stdin:
```
git diff main..HEAD | b0 run reviewer "Review the following diff. Focus on correctness."
```

## Concurrent tasks

Run multiple agents in parallel:

```bash
b0 run reviewer "Review the changes on branch feature-timeout..." &
b0 run security "Check src/handler.rs for OWASP top 10 vulnerabilities..." &
b0 run doc-writer "Update README to reflect the new timeout config option..." &
wait
```

Each `b0 run` call blocks until its agent completes. Run them in the background with `&` to parallelize.

## Scheduled agents

Create an agent that runs automatically on a schedule:

```bash
b0 add monitor --instructions "Check logs for errors." --every 1h --task "scan logs"
```

Intervals: `30s`, `5m`, `1h`, `6h`, `1d`.

## Webhook triggers

Every agent with `--webhook` has a trigger URL. Any HTTP POST to that URL runs the agent.

```bash
b0 add notifier --instructions "Process incoming alerts." --webhook
```

This prints the trigger URL: `<server>/trigger/<workspace>/<agent-name>`.

To see the trigger URL for an existing agent:

```bash
b0 info notifier
```

To add HMAC signature verification:

```bash
b0 add notifier --instructions "Process alerts." --webhook --webhook-secret mysecret
```

Then sign requests with `X-Hub-Signature-256: sha256=<hmac-sha256-of-body>`.

## Error handling

If an agent fails, `b0 run` reports the error. Decide whether to:
- Retry with a clearer prompt
- Try a different agent
- Handle the task yourself
- Report the failure to the user

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `b0: command not found` | Run `npm install -g @box0/cli@latest` |
| `b0 server status` shows not running | Run `b0 server` |
| `b0 run` times out | Increase timeout with `--timeout 600` |
| Agent returns empty result | Check agent instructions with `b0 info <name>` |
