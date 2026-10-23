---
name: verify-work
description: "Prove a change works with real checks before calling it done. Use before saying work is done, or when the user says \"check it works\" or \"run the checks\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: quality
  cover: "3 tiers"
---

# Verify work

Evidence before claims. Never report "done" from memory: run the commands, read the output.
Validation scales with what the change can break, never with how many lines it is.

## Tier 1: always (seconds, terminal only)

Run the project's own checks. Find them in `package.json`, a `Makefile` or the README; typically:

- lint
- typecheck
- unit tests

All must pass. Report real numbers ("212/212 tests"), not "tests pass". A failure means fix,
re-run, and only then report.

## Tier 2: only if the UI changed

Skip it for pure logic, data or migration changes.

1. Start the dev server if it isn't running.
2. Open only the screens you changed. No crawling.
3. Take two screenshots: desktop (1440 wide) and phone (390 wide).
4. Look at them: overflow, clipped text, broken alignment, missing states, focus you can't see.
5. If you need to log in and don't have test credentials, ask. Never guess or hard-code them.

## Tier 3: only when asked

End-to-end suites and anything slow, costly or touching live data. If you think it's needed, say
so and let the user decide.

## Close out

- Report each tier: what ran and the real result, plus the screenshots if you took them.
- List the files you changed. Don't commit or push unless the user asked you to.

## Red flags: you're about to skip verification

- "It's a tiny change." Tiny changes break builds. Tier 1 takes seconds.
- "Tests passed earlier." Earlier isn't after your last edit. Run them again.
- "The UI change is obviously fine." Look at it in the browser before you say so.

## Credits

The "evidence before claims" principle and the red-flags format come from
[superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT).
