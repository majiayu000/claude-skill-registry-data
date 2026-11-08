---
name: background-task-tracking
description: Track accepted background runs and approval state without inventing execution or duplicating work.
---

# Background Task Tracking

1. Distinguish task proposal from confirmed backend acceptance. Claim 'started' only when the backend returns acceptance.
2. Retain only backend-provided task/run/approval identifiers necessary for a supported status lookup.
3. Recognize states: not submitted, running, awaiting approval, completed, failed, interrupted, cancelled, unknown. Neither elapsed time nor watch-screen dismissal proves a state change.
4. When asked 'is it finished?' use the integration's status endpoint where available. Otherwise say completion cannot be verified.
5. Never resubmit a potentially duplicate-sensitive task just because the watch timed out. Find the original run first if possible.
6. Background continuation requires an actual long-running backend. The prompt cannot create persistence or a notifier.
7. Give compact verified statuses: 'Still running; last confirmed step ...' or 'Waiting for your approval.' Expose failure and unknowns.
8. Do not promise completion alerts unless there is a configured, confirmed delivery path.
