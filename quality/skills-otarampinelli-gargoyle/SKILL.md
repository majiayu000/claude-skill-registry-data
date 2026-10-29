---
name: gargoyle
description: Reviews local changes with gargoyle checks before pushing, then helps fix what it finds. Use when the user says "/gargoyle", "run gargoyle", or asks to review their changes before pushing.
---

# Gargoyle

Run `gargoyle guide` and follow it. It walks you through reviewing the user's changes and triaging what the review finds.

If the user named checks, like `/gargoyle security-review code-quality`, pass them on with `--checks` as the guide says.

If the `gargoyle` command isn't installed, tell the user to install it from https://github.com/otarampinelli/gargoyle and stop.
