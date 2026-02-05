---
name: session-replay
description: Set up session replay for visual debugging. Use when implementing screen recording, replay features, or visual debugging tools.
triggers:
  - "record user sessions"
  - "replay user actions"
  - "screen recording"
  - "see what user did"
  - "set up session replay"
  - "visual debugging"
priority: 3
---

# Session Replay

Capture visual recordings of user sessions for debugging.

## When to Use

- Reproducing hard-to-debug issues
- Understanding user confusion
- QA and support investigations

## Privacy Requirements (Must Do)

Mask by default:
- All text input fields
- Passwords and sensitive data
- User-generated content
- Financial information
- User photos/documents

## Performance Budget

| Resource | Limit |
|----------|-------|
| CPU | <5% additional |
| Memory | <20MB additional |
| Network | Batch on WiFi |
| Battery | Pause when low |

## Capture Strategies

| Strategy | Fidelity | Overhead |
|----------|----------|----------|
| Screenshots (1-2 fps) | Lower | Lower |
| View hierarchy recording | Higher | Moderate |
| Hybrid (screenshots + events) | Best | Moderate |

## Best Practice

Don't record everything. Target:
- Error sessions only (rolling buffer)
- Key user journeys
- 1-10% sampling for general insights

## Implementation

See `references/session-replay.md` for:
- Platform-specific setup
- Privacy masking patterns
- Vendor configurations (Sentry, Datadog)
