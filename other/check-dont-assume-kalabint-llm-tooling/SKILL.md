---
name: check-dont-assume
description: Verify every load-bearing claim by reading the code or running the check; never assert from memory or dismiss something as too obvious to confirm.
---

# Check, do not assume

Before stating a fact a decision will rest on, look: read the file, run the query, probe the endpoint. "It obviously does X" is the phrasing that precedes being wrong.

**Why:** the cost of a wrong asserted fact is paid downstream by whoever trusted it; the cost of checking is seconds.

**How to apply:** when you catch yourself about to write "this should", "presumably", or "it must", convert it into an observation with a command behind it. Keep what you verified separate from what you inferred, and label the inferences as inferences.
