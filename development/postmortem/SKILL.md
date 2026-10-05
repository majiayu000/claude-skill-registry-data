---
name: postmortem
description: Dissect a completed debugging session — reconstruct what broke, the real root cause, and what would have found it faster. Use after a long debugging session, or on 'postmortem' trigger phrases.
disable-model-invocation: true
argument-hint: "target: local | server (default: local)"
---

Reconstruct the debugging session that just happened. Work from what's in the conversation and the actual changes made — don't theorize past the evidence.

Pull out:
- The symptom, and what the real root cause turned out to be (not the first suspect).
- The dead ends: what looked guilty but wasn't, and why it was misleading.
- The signal that would have pointed here sooner — the log line, test, or check that was missing or ignored.
- What could have been done differently, and what made the better path non-obvious in the moment.

Close with one or two concrete changes that would catch this class of bug faster next time — a test, an assertion, a log, a habit. Prefer cheap and durable over thorough.

Keep it honest. If the fix was luck rather than understanding, say so.

## Target

- `local` (default) — pull evidence from this machine.
- `server` — pull evidence over SSH. Follow `/home/rahul/Documents/code/claude_settings/policies/ssh-policy.md`: read-only throughout.
  A postmortem reconstructs what happened, not remediates it — if a fix suggests itself,
  note it as a follow-up action item rather than performing it.