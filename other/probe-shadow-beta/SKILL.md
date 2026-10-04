---
name: probe-shadow-beta
description: Second of a pair of benchmark skills for testing cross-skill resource shadowing. Both skills have a references/API.md file with different content. Use when asked to probe resource shadowing.
---

# Shadow Beta Probe

This skill is one of a pair (alpha and beta) that both contain a file at
`references/API.md` with different content. Testing whether the platform
can distinguish between them when both skills are active.

## Instructions

When activated:

1. Read `references/API.md` and report its contents.
2. Note which canary phrase you see. If you see **EGRET-SLATE-8823**, you
   got this skill's (beta) version. If you see **STORK-CORAL-4471**, you
   got the alpha skill's version.
3. If both skills are active, try to read the other skill's version and
   report whether you can access it.
