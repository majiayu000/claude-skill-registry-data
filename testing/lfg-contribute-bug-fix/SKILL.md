---
name: lfg-contribute-bug-fix
description: "Contribute a verified bug fix for lfg or its GrokBuild adapter payload. Use when the user asks to debug and fix an lfg setup, skill sync, hook, MCP, agent, config, package, or GrokBuild integration defect."
metadata:
  short-description: Contribute verified lfg/GrokBuild adapter bug fixes
---

# lfg-contribute-bug-fix

Use this skill to debug a concrete lfg defect, implement the smallest correct fix, and deliver a verified local patch. Work in the current lfg checkout when the user is already in that repo; otherwise use a fresh temporary clone of `islee23520/lfg`.

## Required Outcome

- failing-before evidence for the reported bug
- the smallest implementation that fixes it
- passing-after test output
- real setup-surface verification, usually `node dist/lfg.js --json setup --run`
- a clean patch or draft issue/PR body ending with `Tag: lfg-generated`

## Required Workflow

1. Reproduce the bug through the real lfg surface.
2. Add or update a focused regression test before production changes.
3. Implement the smallest fix in lfg-owned source.
4. Run the focused test, adjacent tests, and real setup verification.
5. If asked to publish upstream, prepare the branch/issue/PR for `islee23520/lfg` with the verification evidence.

## Delivery Footer

```markdown
---
This fix was debugged, implemented, and verified with lfg.
Tag: lfg-generated
```

Do not ship a fix without RED evidence, GREEN evidence, and a real setup-surface proof.
