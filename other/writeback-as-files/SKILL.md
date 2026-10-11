---
name: writeback-as-files
description: Use when an agent needs to write back to a provider through a relayfile mount (Linear comments, GitHub issues, Slack messages, Notion pages, etc.). Covers the file-creation writeback contract (drop JSON at the canonical path → provider mutation), discovering paths and schemas via .schema.json siblings, idempotency keys, writeback status with relayfile writeback list and relayfile status, and recovering from dead-lettered writes under .relay/dead-letter/. NOT for read operations or for direct API calls — relayfile mediates the writeback so you can ignore provider auth, retries, and rate limits.
---

# Writebacks Are Files

## Overview

In a relayfile mount, the agent does not call a provider API to mutate state. It **writes a file**. The mount daemon picks up the change, validates the payload against the canonical schema, signs and delivers the request to the provider, and records the result. Auth, retries, idempotency, dead-lettering, and the audit trail are handled on the other side.

## When to use this skill

- The user asks the agent to take an action against a provider (comment, message, create, update, close, react, …).
- You see a writable path under `<mount>/<provider>/…` and want to know what shape the file should be.
- A previous write didn't seem to take effect and you need to find out why.
- You're about to call a provider SDK directly — stop and check if relayfile already exposes a writeback for that mutation.

## The contract in one sentence

> Drop a JSON file at the canonical writeback path; the provider receives the corresponding mutation within ~30 seconds.

## Find the canonical path

Writeback directories are discoverable in the mount. They sit next to the read-side data and carry a sibling `.schema.json` describing the expected payload.

```bash
# What can I do under a Linear issue?
$ ls $MOUNT/linear/issues/AGE-16__87389837-62b1-4e1a-a237-59218bab2974/
content.md
comments/                # writeback dir — drop JSON files here
comments/.schema.json    # schema for individual comment writebacks
state-transitions/       # writeback dir — drop JSON to move issue state
state-transitions/.schema.json
```

```bash
# What's the schema for a Linear comment?
$ cat $MOUNT/linear/issues/AGE-16__.../comments/.schema.json
{
  "type": "object",
  "required": ["body"],
  "properties": {
    "body": { "type": "string", "minLength": 1, "maxLength": 65535 },
    "asUserId": { "type": "string" }
  }
}
```

Schemas are the source of truth. Read them before guessing payload shape.

## Examples

### Post a Linear comment

```bash
cat > $MOUNT/linear/issues/AGE-16__.../comments/wb-$(date +%s).json <<'EOF'
{
  "body": "Picking this up — design clarified the blocker."
}
EOF
```

### Open a GitHub issue

```bash
cat > $MOUNT/github/repos/AgentWorkforce/relay/issues/wb-$(date +%s).json <<'EOF'
{
  "title": "Race condition in writeback retry loop",
  "body": "Repro: …\n\nExpected: …\n\nActual: …",
  "labels": ["bug", "writeback"]
}
EOF
```

### Send a Slack message

```bash
cat > $MOUNT/slack/channels/C0ADE9B71CN__gtm-prospects/messages/wb-$(date +%s).json <<'EOF'
{
  "text": "ACME signed — moving them to the activation channel."
}
EOF
```

### Update a Notion page body

```bash
# Notion content.md is a *write-through* file — overwriting it queues an update.
echo "# Onboarding\n\nUpdated …" > $MOUNT/notion/pages/<id>/content.md
```

## Filename conventions

- **Use a unique suffix** (timestamp + short random) so retries don't collide. The mount daemon also derives an idempotency key from the file path, so two writes to the same path inside the dedup window are coalesced.
- **`wb-<timestamp>.json`** is the conventional prefix for agent-authored writebacks. It makes them easy to spot in dead-letter forensics.
- Do **not** name files `.tmp` or use rsync-style `.partial` — the daemon picks up files atomically on rename close; partial-suffix files are ignored.

## Watching status

```bash
# Pending writebacks (queued but not delivered yet)
relayfile writeback list --state pending

# Failed writebacks (dead-lettered after exhausting retries)
relayfile writeback list --state dead

# Quick health check
relayfile status
# workspace rw_xxxxxxxx (my-agent)   mode: poll   lag: 4s
# linear   ready    214 files    last event 2s ago
# pending writebacks: 0    dead-lettered: 0
```

`dead-lettered: 0` is the field to watch. If it goes non-zero, your writes are not landing.

## Dead-letter recovery

Failed writebacks land in `<mount>/.relay/dead-letter/` with the original payload plus a `.error.json` sibling explaining the failure:

```bash
$ ls $MOUNT/.relay/dead-letter/
wb-1715608327.json
wb-1715608327.error.json

$ cat $MOUNT/.relay/dead-letter/wb-1715608327.error.json
{
  "code": "schema_violation",
  "message": "body: must be at least 1 character",
  "attempts": 1,
  "lastAttemptAt": "2026-05-13T14:32:07Z"
}
```

Typical causes:

- `schema_violation` — your payload didn't match `.schema.json`. Fix and re-drop.
- `provider_4xx` — provider rejected (auth scope, missing parent, etc.). The error body contains the provider's response.
- `provider_5xx_exhausted` — provider repeatedly failed after backoff. Usually transient; re-drop with a fresh filename.

To replay: read the original payload, fix what's wrong, write to a fresh path with a new suffix.

## What NOT to do

- **Don't call the provider SDK directly** from within the agent if a writeback path exists. You lose the retry, idempotency, dead-letter, and audit story.
- **Don't write to read-only paths.** The mount enforces read-only at the OS level on canonical record files (e.g. `*.json` payloads). If your write returns `EACCES`, find the writeback subdirectory instead.
- **Don't poll for completion in a tight loop.** Subscribe to the change stream for `writeback.succeeded` and `writeback.failed` events.
