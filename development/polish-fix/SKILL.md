---
name: polish-fix
description: Land one small UI papercut as a tiny, easy-to-approve PR, the low-ceremony path for fixes too small to warrant a full session. Use when the user spots a minor visual or interaction nit (spacing, alignment, colour, hover, copy, a slightly-off radius) and wants it fixed and shipped without ceremony, or says "quick fix", "polish this", "tiny PR for X". Makes the minimal change, captures a before/after, and opens a small PR. Does NOT do feature work, refactors, or anything that needs review discussion; escalate those to a normal session.
---

# Polish Fix

A polish fix is **one tiny, obvious UI improvement shipped with as little ceremony
as possible**. The whole value is volume without overhead: dozens of small craft
fixes that would never each justify a dedicated session.

Keep each one genuinely small. If it grows past a few lines or needs a design
decision, it isn't a polish fix; stop and treat it as real work.

## Workflow

1. **Pin the papercut.** State the single concrete change in one sentence ("tighten
   the gap between the avatar and name", "fix the sticky hover on the nav links").
   One papercut per fix.
2. **Make the minimal change.** Touch the fewest lines that resolve it. Match the
   surrounding code and tokens: no new abstractions, no drive-by edits, no scope
   creep into nearby nits (those are *separate* polish fixes).
3. **Capture before/after.** Screenshot the element or page in both states, so
   the PR is reviewable at a glance without anyone running it. Use whatever browser
   automation the harness provides (e.g. a Playwright or browser MCP); if none is
   available, say so in the PR and describe the change textually instead of blocking.
4. **Open a small PR.** Branch, commit (end the message with the project's
   `Co-Authored-By` line if one is configured), and open a PR whose body is just the
   one-line description plus the before/after images. Upload the screenshots
   wherever your workflow can host them (a gist, an image host) and link them in
   the body; if nothing is available, leave a placeholder and ask the user to
   attach them. Title it so a reviewer can approve on sight.

## Keep it cheap

- **One papercut per PR.** Don't batch unrelated fixes; small, single-purpose PRs
  are the thing that makes them approvable on sight. (If a pile accumulates, the
  user can ask to squash them later.)
- **No tests, no refactors, no behaviour change** beyond the visual/interaction nit.
- **Respect the project's checks.** Run whatever build/lint the repo defines before
  pushing; a polish fix that breaks CI defeats the purpose.
- **Escalate honestly.** The moment a "quick fix" reveals a real problem, say so and
  stop; don't quietly expand the PR.
