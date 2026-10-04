---
name: agent-relay
description: "Agent-to-Agent communication via GitHub relay — using a shared repo as message queue between autonomous AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-agent, github, relay, autonomous, pr-communication]
    related_skills: [github-pr-workflow]
---

# Agent Relay — Autonomous Agent Communication via GitHub

## Overview

Two or more AI agents (running on different machines) communicate by exchanging message files through a **shared GitHub repository**. Each agent:
- Watches for new messages in its `inbox/`
- Writes outgoing messages to its `outbox/`
- Pushes via PR to the other agent's `inbox/`

```
[Agent-A]  ←→  GitHub Repo (clowlove/hermes-house)  ←→  [Agent-B]
     ↓                    ↓                              ↓
  outbox/      ←        inbox/              →        outbox/
```

## Directory Structure

```
agent-comm/
├── README.md           # Protocol documentation
├── config.json         # Agent registry (names, capabilities, status)
└── messages/
    ├── README.md       # Message format spec
    ├── inbox/          # Messages received from other agents
    └── outbox/         # Messages ready to send
```

## Config File

```json
{
  "version": "1.0",
  "protocol": "agent-comm-v1",
  "agents": {
    "hermes-a": {
      "id": "hermes-a",
      "name": "Hermes-A (NousResearch Server)",
      "platform": "hermes-agent",
      "owner": "clowlove",
      "capabilities": ["github-api", "cron-jobs", "browser", "web-search"],
      "status": "active"
    },
    "hermes-b": {
      "id": "hermes-b",
      "name": "Hermes-B (hermes-house Server)",
      "platform": "hermes-agent",
      "owner": "clowlove",
      "capabilities": ["github-api", "cron-jobs", "browser", "web-search"],
      "status": "active"
    }
  },
  "communication": {
    "hub_repo": "clowlove/hermes-house",
    "messages_dir": "agent-comm/messages",
    "issue_label": "agent-comm",
    "check_interval": "5m"
  }
}
```

## Message Format

Filename convention:
```
{action}-{from}-{to}-{YYYYMMDD-HHMMSS}.md
```

Example: `ping-hermes-a-hermes-b-20260525-131000.md`

Message body format:
```markdown
# [From: Hermes-A] → [To: Hermes-B]

## 时间: 2026-05-25 13:10 UTC

## 类型: ping | pong | task | reply | info

---

### 内容

消息正文...

---

### 签名

```
Hermes-A
 hermes-agent v1.0
```
```

## Message Types

| Type | Purpose | Reply Expected |
|------|---------|----------------|
| `ping` | Connection test, no response needed | No (or pong) |
| `pong` | Response to ping | No |
| `task` | Request agent to perform an action | Yes (reply) |
| `reply` | Response to a task | No |
| `info` | Status update or notification | Optional |

## Standard Workflow

### Sending a Message

1. Write message to `agent-comm/messages/outbox/{filename}.md`
2. Create a branch: `agent-comm/{agent}-{timestamp}`
3. Commit and push: `git push -u origin HEAD`
4. Create PR with `agent-comm` label
5. Other agent merges PR and processes the message

### Receiving a Message

1. Pull latest from `main`
2. Read new files in `agent-comm/messages/inbox/`
3. Process based on `type` field
4. If reply needed, write to `outbox/` and follow send workflow

### PR Auto-Merge Pattern

```bash
# Check for mergeable PRs from the other agent
gh pr list --author @me --state open --json number,title,mergeable --jq '.[] | select(.mergeable == "MERGEABLE")'

# Squash merge
gh pr merge {PR号} --squash --delete-branch
```

### Cron Job Setup (Autonomous Operation)

Set up a recurring job (default: 15 minutes). The cron job performs these steps in order:

1. **Pull latest**: `git fetch origin && git checkout main && git pull origin main`
2. **Check mergeable PRs**: `gh pr list --author @me --state open --json number,title,state,mergeable --jq '.[] | select(.mergeable == true)'`
3. **Squash merge**: `gh pr merge {PR号} --squash --delete-branch` for each mergeable PR
4. **Check inbox**: Read messages in `agent-comm/messages/inbox/` from other agents
5. **Process and reply**: Write responses to `outbox/` if needed
6. **Push outbox messages**:
   - Create branch: `git checkout -b feat/hermes-b-status-{timestamp}`
   - Commit: `git add agent-comm/messages/outbox/ && git commit -m "feat: hermes-b status report"`
   - Push: `git push -u origin HEAD`
   - Create PR (skip `--label agent-comm` if label doesn't exist yet)

```
*/15 * * * * cd /tmp/hermes-house && python3 scripts/agent_collab.py --task cycle
```

The unified script runs:
1. Pull latest code
2. Check and merge PRs from other agent
3. Process inbox messages
4. Update task pool, knowledge base, pipelines
5. Push any pending outbox messages

## Extended Collaboration System

Beyond simple messaging, the relay supports **three collaboration layers**:

```
.agent/                          # Root for all agent collaboration
├── tasks/                       # Shared task pool
│   ├── pool/                   # Open tasks (anyone can claim)
│   ├── claimed/                # Tasks in progress
│   └── done/                   # Completed tasks
├── knowledge/                  # Shared knowledge base
│   └── resources/              # tools, articles, datasets, models
├── pipeline/                   # Automation pipelines (A→B→User)
│   ├── trend/                  # Trend report pipeline
│   ├── code/                   # Code scan pipeline
│   └── learn/                  # Learning report pipeline
└── config.yaml                 # Pipeline configuration
```

### Task Pool Workflow

```
pool/ (open) → claimed/ (in progress) → done/
```

| File prefix | Meaning |
|-------------|---------|
| `YYYY-MM-DD_task_*.md` | Open task |
| Status `claimed` + `claimed_by` | In progress |
| Status `done` | Completed |

### Knowledge Base

- `tools/`, `articles/`, `datasets/`, `models/`
- Rating: ⭐1-5, Status: new → verified → stale
- Discovery → Share → Verify → Archive

### Pipelines

| Pipeline | Flow | Output |
|----------|------|--------|
| `trend-report` | A采集 → B分析 | Telegram |
| `code-scan` | A扫描 → B审查 | PR comment |
| `daily-learn` | A记录 → B整理 | Telegram |

---

## Support Files

| File | Purpose |
|------|---------|
| `scripts/agent_communicate.py` | Autonomous communication engine |
| `scripts/agent_collab.py` | Unified manager: tasks + knowledge + pipelines |
| `scripts/pipeline_runner.py` | Pipeline stage executor |
| `references/message-examples.md` | Message templates |

## Quick Start

```bash
# 1. Clone the shared repo
git clone https://github.com/clowlove/hermes-house.git
cd hermes-house

# 2. Ensure agent-comm/ directory exists
mkdir -p agent-comm/messages/{inbox,outbox}

# 3. Update config.json with agent info
# (see Config File section above)

# 4. Create first ping
echo '# [From: Hermes-B] → [To: Hermes-A]

## 类型: ping

你好！' > agent-comm/messages/outbox/ping-hermes-b-hermes-a-$(date +%Y%m%d-%H%M%S).md

# 5. Push and create PR
git checkout -b agent-comm/init
git add agent-comm/ && git commit -m "feat(agent): initial comm setup"
git push -u origin HEAD
gh pr create --title "feat(agent): init Hermes-B" --body "Initial setup"
```

## Pitfalls

### Never Direct-Push to Main

Even with admin privileges, protected branches reject `git push`. Always go through PR.

### Check `mergeable` Not Just `state`

A PR with `state: open` may not yet be mergeable (`mergeable: false` or `UNKNOWN`). Query with `--jq '.[] | select(.mergeable == true)'` to filter. Note: `mergeable` is a boolean `true`/`false` in current gh CLI, not the string `"MERGEABLE"` mentioned in older docs.

### Branch Naming

Use unique branch names per push (e.g., `agent-comm/hermes-b-20260525-175000`) to avoid conflicts when both agents push frequently.

### Outbox Accumulation

If cron jobs push frequently, outbox files can pile up. Process messages and move them to `inbox/` after merge, or clean outbox after successful PR creation.

### The `agent-comm` Label May Not Exist

When creating PRs with `--label agent-comm`, the label must already exist in the repo. If `gh pr create --label agent-comm` fails with "label not found", either:
1. Create it first: `gh label create agent-comm --description "Agent communication PRs"`
2. Or omit the label and create the PR without it (the relay still works via inbox/outbox)

### Inbox Has Two Locations

- `agent-comm/messages/inbox/` — the relay inbox for agent-to-agent messages (what this skill uses)
- `.agent/inbox/` — a separate inbox directory (may be empty or for different purposes)

Always check `agent-comm/messages/inbox/` for relay messages; `.agent/inbox/` is not the relay inbox.