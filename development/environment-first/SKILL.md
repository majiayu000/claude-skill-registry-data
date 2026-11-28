---
name: environment-first
description: When something that should work doesn't, suspect the environment before rewriting the code — wrong directory, stale build, missing env var, version mismatch, dirty state. Use when a command fails unexpectedly, tests fail that "can't" fail, behavior contradicts the code you're reading, or the error is command-not-found, module-not-found, connection refused, permission denied, "works in CI", or "works on my machine".
---

# environment-first

Weak debugging assumes the code is wrong and starts editing. Often the code is fine and the world is misconfigured — and code edits made while the environment lies are wrong edits that then need reverting.

Heuristic: if the failure message doesn't mention your code's names at all (import errors, command-not-found, connection refused, permission denied), it's environment until proven otherwise.

## Before editing any code

1. **Prove you're running the source you're reading.** When behavior contradicts the code, you probably aren't executing that code: stale build artifact, cached bytecode, an installed copy shadowing the checkout, the wrong virtualenv/node_modules, a server started before the change. Test it directly: add a deliberate marker (a distinctive log line or a throw) to the file, rerun, and confirm the marker appears. No marker → rebuild/restart/reinstall until it does. Only then reason about the logic.
2. **Run the boring five and paste the outputs** (under a minute, in order): `pwd` plus current branch — right repo, right checkout? `git status` — unexpected local modifications or untracked files? runtime version (`node -v`, `python --version`, etc.) vs what the manifest or `.nvmrc`/`.tool-versions` expects? env vars and config files the code reads — set, and set to the value you assume? dependency install current — lockfile newer than the last install?
3. **Run the exact failing command, not your paraphrase of it.** Same cwd, same shell, same flags, same script name as CI or the user used. A different invocation that passes proves nothing about the one that fails.
4. **"Works on the other machine / in CI" is an environment diff by definition.** Diff versions, env vars, OS, and filesystem assumptions (case sensitivity, path separators, line endings) before diffing the code.
5. **Flaky ≠ mysterious.** Intermittent failure usually means shared state, port collisions, timing, or leftover files from a previous run. Clean state (kill stray processes, delete temp output, fresh clone if cheap) and rerun before blaming the test's logic.

## After the environment is fixed

6. **Re-run the original failing command and paste the output.** If the failure vanishes, say so plainly: nothing was wrong with the code, and no code change ships. Revert any edits made while the environment was lying (see workmanship).
7. **Record the setup fix** where the project keeps such things (README, setup script, project CLAUDE.md) so the next session doesn't rediscover it.
