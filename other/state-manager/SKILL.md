---
name: epci:state-manager
description: >-
  Manages feature state persistence across sessions for EPCI v6.0 workflows.
  Tracks implementation progress, phases, checkpoints, history, and resumption context.
  Maintains central index of all features and supports temporary sessions for brainstorm/debug.
  Use when: starting new feature (/implement), resuming paused work, saving checkpoints,
  tracking multi-session implementations, or managing brainstorm/debug sessions.
  Internal component for EPCI v6.0.
user-invocable: false
allowed-tools: Read, Write, Glob
---

# State Manager

Internal component for feature state persistence across sessions.

## Overview

Enable resumable workflows by persisting:
- Feature lifecycle (status, phase, timestamps)
- Task execution progress
- File modifications and artifacts
- Checkpoints for resume
- History of actions
- Temporary sessions (brainstorm, debug)

## Storage Structure

```
.claude/state/
├── config.json                    # Global EPCI configuration
├── features/
│   ├── index.json                 # Central feature registry
│   └── {feature-slug}/
│       ├── state.json             # Feature state machine
│       ├── history.json           # Action history log
│       └── checkpoints/
│           └── {phase}-{timestamp}.json
└── sessions/
    └── {session-id}.json          # Temporary sessions
```

## API

### Feature Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `createFeature(slug, spec)` | Initialize new feature state | slug, SpecOutput | FeatureState |
| `loadFeature(slug)` | Load existing feature state | slug: string | FeatureState \| null |
| `updateFeature(slug, updates)` | Partial update feature state | slug, Partial<State> | void |
| `listFeatures(filter?)` | List features by status | filter?: {status} | FeatureSummary[] |

### Checkpoint Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `createCheckpoint(slug, phase)` | Save resumption point | slug, phase | Checkpoint |
| `listCheckpoints(slug)` | Get all checkpoints for feature | slug: string | Checkpoint[] |
| `restoreCheckpoint(checkpointId)` | Resume from checkpoint | checkpointId: string | FeatureState |

### History Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `appendHistory(slug, entry)` | Log action to history | slug, HistoryEntry | void |
| `getHistory(slug)` | Get feature action history | slug: string | HistoryEntry[] |

### Session Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `saveSession(sessionId, data)` | Persist temporary session | sessionId, SessionData | void |
| `loadSession(sessionId)` | Load temporary session | sessionId: string | SessionData \| null |
| `cleanupSessions(maxAge?)` | Remove stale sessions | maxAge?: number | number (deleted) |

## State Schema (v6)

See [references/state-schema.md](references/state-schema.md) for full schema.

```json
{
  "feature_id": "auth-oauth-google",
  "version": 1,

  "lifecycle": {
    "status": "in_progress",
    "current_phase": "code",
    "completed_phases": ["explore", "plan"],
    "created_at": "2026-01-22T10:00:00Z",
    "last_update": "2026-01-22T14:30:00Z",
    "created_by": "/implement",
    "last_updated_by": "/implement"
  },

  "spec": {
    "prd_json": "docs/specs/auth-oauth-google.prd.json",
    "prd_md": "docs/specs/auth-oauth-google.md",
    "complexity": "STANDARD",
    "total_tasks": 6,
    "estimated_minutes": 180
  },

  "execution": {
    "tasks": {
      "completed": ["US-001", "US-002"],
      "current": "US-003",
      "pending": ["US-004", "US-005", "US-006"],
      "failed": []
    },
    "iterations": 12,
    "last_error": null
  },

  "artifacts": {
    "feature_doc": "docs/features/auth-oauth-google-20260122-100000.md",
    "test_files": ["tests/integration/oauth.test.ts"],
    "modified_files": ["src/auth/oauth.ts", "src/auth/types.ts"]
  },

  "checkpoints": [...],
  "improvements": []
}
```

**Note**: `artifacts.feature_doc` is set by `/implement` step-00-init when creating the Feature Document.
Path format: `docs/features/{feature-slug}-{YYYYMMDD-HHmmss}.md`

## Index Schema

Central registry of all features (`.claude/state/features/index.json`):

```json
{
  "version": "1.0",
  "last_update": "2026-01-22T15:00:00Z",
  "features": [
    {
      "id": "auth-oauth-google",
      "status": "in_progress",
      "current_phase": "code",
      "complexity": "STANDARD",
      "branch": "feature/auth-oauth-google",
      "created_at": "2026-01-20T10:00:00Z"
    }
  ]
}
```

## Usage

Invoked automatically by skills:

| Skill | Action | Function Called |
|-------|--------|-----------------|
| `/implement` | Start new feature + Feature Document | `createFeature()` + set `artifacts.feature_doc` |
| `/implement --continue` | Resume feature | `loadFeature()`, `restoreCheckpoint()` |
| `/quick` | Optional lightweight tracking | `createFeature()` (minimal) |
| `/brainstorm` | Save exploration session | `saveSession()` |
| `/debug` | Save investigation session | `saveSession()` |

## Implementation

```
// Starting a new feature
state_manager.createFeature("auth-oauth", specOutput)
  → Creates .claude/state/features/auth-oauth/state.json
  → Updates .claude/state/features/index.json
  → Returns initial FeatureState

// Updating phase
state_manager.updateFeature("auth-oauth", {
  lifecycle: { current_phase: "implementation" }
})
  → Updates state.json
  → Appends to history.json

// Creating checkpoint
state_manager.createCheckpoint("auth-oauth", "plan")
  → Saves to checkpoints/plan-20260122-100523.json
  → Returns Checkpoint { id, phase, timestamp, git_ref, resumable }

// Temporary session (brainstorm)
state_manager.saveSession("brainstorm-20260122-143052", sessionData)
  → Saves to sessions/brainstorm-20260122-143052.json
```

## Reference Files

- [api-reference.md](references/api-reference.md) — Detailed function signatures
- [state-schema.md](references/state-schema.md) — Complete JSON schemas
- [examples.md](references/examples.md) — Integration examples

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `STATE_NOT_FOUND` | Feature doesn't exist | Call `createFeature()` first |
| `STATE_CORRUPTED` | JSON parse error | Restore from checkpoint |
| `INDEX_CORRUPTED` | Index file invalid | Rebuild from feature dirs |
| `CONCURRENT_MODIFY` | Race condition | Retry operation |

## Limitations

This component does NOT:
- Handle cross-project state sharing
- Provide real-time sync (file-based)
- Manage database connections
- Support distributed locking
