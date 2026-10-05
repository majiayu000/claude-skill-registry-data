---
type: Skill
name: gws-meet
version: 1.0.0
description: Google Meet skill for creating meeting spaces, reviewing conference records, and managing participants and recordings via the gws CLI.
license: Apache-2.0
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Google Meet (gws-meet)

> **PREREQUISITE:** Read the `gws-shared` skill for auth, global flags, and security rules.

Manage Google Meet conferences using the `gws` CLI.

```bash
gws meet <resource> <method> [flags]
```

## Quick Examples

```bash
# Create a new meeting space
gws meet spaces create \
  --json '{"config": {"accessType": "TRUSTED", "entryPointAccess": "ALL"}}'

# Get meeting space details (includes join URL)
gws meet spaces get \
  --params '{"name": "spaces/SPACE_ID"}'

# Update a meeting space
gws meet spaces patch \
  --params '{"name": "spaces/SPACE_ID", "updateMask": "config"}' \
  --json '{"config": {"accessType": "RESTRICTED"}}'

# End an active conference
gws meet spaces endActiveConference \
  --params '{"name": "spaces/SPACE_ID"}' \
  --json '{}'

# List recent conference records
gws meet conferenceRecords list \
  --params '{"pageSize": 10}'

# Get a specific conference record
gws meet conferenceRecords get \
  --params '{"name": "conferenceRecords/CONFERENCE_ID"}'

# List participants in a conference
gws meet conferenceRecords participants list \
  --params '{"parent": "conferenceRecords/CONFERENCE_ID"}'

# List recordings for a conference
gws meet conferenceRecords recordings list \
  --params '{"parent": "conferenceRecords/CONFERENCE_ID"}'

# List transcripts for a conference
gws meet conferenceRecords transcripts list \
  --params '{"parent": "conferenceRecords/CONFERENCE_ID"}'
```

## Meeting Space Config Options

```json
{
  "config": {
    "accessType": "TRUSTED",       // OPEN, TRUSTED, RESTRICTED
    "entryPointAccess": "ALL"      // ALL, CREATOR_APP_ONLY
  }
}
```

## Common Workflows

### Create and share a meeting link

```bash
# 1. Create space
SPACE=$(gws meet spaces create --json '{}')

# 2. Extract the meeting URI
echo $SPACE | jq -r '.meetingUri'
# → https://meet.google.com/abc-defg-hij

# 3. Share via Gmail (see gws-gmail skill)
```

### Review who attended a meeting

```bash
# Get conference record
gws meet conferenceRecords list --params '{"pageSize": 5}'

# List participants with duration
gws meet conferenceRecords participants list \
  --params '{"parent": "conferenceRecords/CONFERENCE_ID"}'
```

## Key API Resources

### spaces
`create`, `get`, `patch`, `endActiveConference`

### conferenceRecords
`list`, `get`

### conferenceRecords.participants
`list`, `get`

### conferenceRecords.recordings
`list`, `get`

### conferenceRecords.transcripts
`list`, `get`

## Discovering More

```bash
gws meet --help
gws schema meet.spaces.create
gws schema meet.conferenceRecords.list
```
