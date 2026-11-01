---
name: debug-new-code
description: Procedure for debugging newly written rgmercs code that misbehaves in game. Use when a recent change produces wrong behavior, errors, or flaky results and the cause isn't obvious. Don't use for one-line typos or syntax errors.
---

Examine everything thoroughly before patching — fixing one symptom at a time wastes effort.

1. **Instrument first, hypothesize second.** Add debug output, read the full logs, then form a hypothesis — don't react to individual symptoms.
2. **Examine the entire flow including async boundaries** (actor messages, `mq.delay`, callbacks). Trace every state transition; don't stop at the first problem.
3. **Fix root causes comprehensively.** Address all identified issues together — one solid fix that handles all edge cases beats a chain of patches.
