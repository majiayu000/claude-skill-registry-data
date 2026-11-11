---
name: verify
description: Run the check and show its output before saying work is done, fixed or passing. Use before a commit, a PR or any claim of success.
---

# Verify

Say work is done only after you ran the check in this session and read its output.

- Run the repo's own check (`just check`, CI's command, or the test that covers the change). For a fix, run the original reproduction and show it now passing.
- Report what happened: the result, plus any failure with its output. A skipped step is reported as skipped.
- A check you couldn't run is "not verified", with why. Never "should work".
- Keep output short: run tests quietly and show failures only.
- Check that the change does what was asked, not just that the tests pass.
