---
name: verify-sample
description: Verify the sample renderer through its public CLI.
---

# Verify the sample renderer

Run from the project root. Check `python3 --version`, inspect `README.md` and
`app.py`, and follow every entry in [the feature map](features/README.md).
There is no persistent service or installation step.

Keep commands, exit statuses, and actual stdout/stderr in `.work/evidence/`.
Report the observed result against each literal expectation. Retain evidence
after cleanup; do not delete pre-existing files or change product code.
