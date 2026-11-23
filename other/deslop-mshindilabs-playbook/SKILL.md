---
name: deslop
description: >
  Remove AI-generated slop from code and clean up code style. Trigger on "deslop this",
  "remove the AI slop", "clean up the AI-looking code in this branch", "strip the
  unnecessary comments and defensive checks", or "this diff looks machine-written". For
  prose use the `unslop` skill. For comments alone use the `no-comments` skill.
license: MIT
metadata:
  upstream: cursor/plugins@d42aff08 cursor-team-kit/skills/deslop
---

# Remove AI code slop

Check the diff against the repo's default branch and remove AI-generated slop introduced in the branch.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep any comment the repo's own written rules require.
- Keep the final summary concise (1-3 sentences).
