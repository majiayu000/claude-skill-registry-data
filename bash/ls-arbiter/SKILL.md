---
name: ls-arbiter
description: "Push decisions to Arbiter Zebu for async human review. Use when you need human input on plans, architectural choices, or approval before proceeding."
metadata:
  version: "1.3"
compatibility: "Python 3.12+, python-frontmatter, and an Arbiter Zebu queue at ~/.arbiter/queue. The bundled CLI manages queue files; an Arbiter Zebu bot or human reviewer must still complete decisions."
---

# Arbiter Skill

Use this skill when work is blocked on a human decision: plan review, architecture tradeoffs, release approvals, or a batch of related choices that should be answered asynchronously.

Do not use it for simple questions you can answer from the repository, urgent real-time decisions, or approvals that require direct user confirmation in the current chat.

## Active Contract

This skill ships a Python queue helper:

```bash
python3 scripts/arbiter_cli.py push '<plan-json>'
python3 scripts/arbiter_cli.py status <plan-id>
python3 scripts/arbiter_cli.py get <plan-id>
python3 scripts/arbiter_cli.py await <plan-id> --timeout 3600
```

The helper writes and reads markdown plans in `~/.arbiter/queue/`:

| Directory | Purpose |
|---|---|
| `pending/` | Plans waiting for review |
| `completed/` | Plans marked complete with answers |
| `notify/` | Optional notification files for agent heartbeat checks |

The helper does not run the Arbiter Zebu bot, contact Telegram, or replace the reviewer. It only manages the filesystem queue contract that Arbiter Zebu consumes.

## Prerequisites

1. Install framework Python dependencies:

```bash
uv sync --locked --no-dev
```

2. Ensure an Arbiter Zebu bot or compatible reviewer watches `~/.arbiter/queue/`.
3. Keep `~/.arbiter/queue/pending`, `completed`, and `notify` readable by the agent process.

If you intentionally installed the upstream Arbiter CLI, you may use it directly, but this skill documents and tests the bundled Python helper as the local supported surface.

## Push A Plan

Create one JSON object with a title and a non-empty `decisions` array:

```bash
python3 scripts/arbiter_cli.py push '{
  "title": "API Design Decisions",
  "tag": "nft-marketplace",
  "context": "Implementation is blocked until these choices are made.",
  "priority": "normal",
  "notify": "agent:swe2:main",
  "decisions": [
    {
      "id": "auth-strategy",
      "title": "Auth Strategy",
      "context": "How should admin users authenticate?",
      "options": [
        {"key": "jwt", "label": "JWT tokens", "note": "Stateless"},
        {"key": "session", "label": "Server sessions", "note": "Central revocation"}
      ],
      "default": "session"
    },
    {
      "id": "database",
      "title": "Primary Datastore",
      "options": [
        {"key": "postgresql", "label": "PostgreSQL"},
        {"key": "mongodb", "label": "MongoDB"}
      ],
      "allowCustom": true
    }
  ]
}'
```

Successful output:

```json
{
  "planId": "abc123",
  "file": "/home/user/.arbiter/queue/pending/agent-nft-marketplace-abc123.md",
  "total": 2,
  "status": "pending"
}
```

## JSON Fields

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Plan title |
| `decisions` | Yes | Non-empty list of decision objects |
| `tag` | No | Project or topic filter; defaults to `general` |
| `context` | No | Background for the reviewer |
| `priority` | No | `low`, `normal`, `high`, or `urgent`; defaults to `normal` |
| `notify` | No | Session key for heartbeat notification |
| `agent` | No | Agent ID; defaults from `ARBITER_AGENT`, `AGENT_ID`, or `USER` |
| `session` | No | Session ID; defaults from `ARBITER_SESSION` or `AGENT_SESSION` |

Decision objects require `id`, `title`, and a non-empty `options` array. Each option requires `key` and `label`; `note` is optional. Set `allowCustom: true` if the reviewer may answer with free text. `push` rejects plan or decision completion fields and always writes each new decision as `status: pending` with null `answer` and `answered_at` values.

## Check Status

Use a plan ID or the newest plan with a tag:

```bash
python3 scripts/arbiter_cli.py status abc123
python3 scripts/arbiter_cli.py status --tag nft-marketplace
```

Output includes `status`, `total`, `answered`, `remaining`, and per-decision answer state derived from the frontmatter `decisions` list. A decision is answered only when its answer is a non-empty string matching an option key, unless that decision has `allowCustom: true`.

## Get Answers

After the reviewer records a valid answer in frontmatter for every decision:

```bash
python3 scripts/arbiter_cli.py get abc123
python3 scripts/arbiter_cli.py get --tag nft-marketplace
```

If any answer is missing or invalid, the command exits non-zero and reports the remaining decision count. A file location or plan-level `status: completed` value does not override answer validation.

## Await Completion

For blocking workflows, poll until completion or timeout:

```bash
python3 scripts/arbiter_cli.py await abc123 --timeout 3600 --interval 30
```

Use `await` only when the current workflow can safely block. For routine agent loops, prefer heartbeat polling.

## Heartbeat Integration

Add a heartbeat or session-resume check that:

1. Looks for files in `~/.arbiter/queue/notify/` for the current session.
2. Runs `python3 scripts/arbiter_cli.py get <plan-id>` or `get --tag <tag>`.
3. Resumes blocked work when answers are complete.
4. Archives or removes handled notification files according to the local Arbiter policy.

## Troubleshooting

| Issue | Check |
|---|---|
| `python-frontmatter is required` | Run `uv sync --locked --no-dev` from the LocalSetup source checkout |
| Plan not visible to Arbiter | Confirm the generated file is under `~/.arbiter/queue/pending/` and has YAML frontmatter |
| `get` reports pending | Check for missing or invalid per-decision answers in frontmatter; moving the plan to `completed/` does not determine completion |
| Tag finds the wrong plan | Use the explicit `planId`; tag lookup returns the newest matching plan |

## Reference

See [references/overview.md](references/overview.md) for the filesystem lifecycle and generated file shape. The template in [templates/decision.md](templates/decision.md) mirrors the bundled CLI output.
