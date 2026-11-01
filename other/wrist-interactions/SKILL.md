---
name: wrist-interactions
description: Handle smartwatch conversations, ambiguous voice transcripts, and recoverable background tasks within explicit permission boundaries.
---

1. Read the recognized question and current context. Resolve obvious transcription errors without changing the user's intent.
2. Answer quick questions directly, usually in one to three short sentences. Clarify only when ambiguity materially affects the result.
3. For longer work, verify backend acceptance before reporting it started. Preserve the exact run and approval identities supplied by the integration.
4. Recover authoritative state after reconnection. Distinguish running, completed, interrupted, failed, cancelled, and awaiting approval.
5. Use structured authorization when available. Denial, expiry, or missing permissions must fail closed.
6. Deliver text independently of speech. Treat engine callbacks as status; use a physical speaker check to investigate silence.
7. Store appropriate established preferences only in this profile's own memory.
