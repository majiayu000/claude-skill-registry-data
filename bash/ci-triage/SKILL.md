---
name: ci-triage
description: Use when a CI/GitHub-Actions failure is reported (by the user, an email summary, another tool, or a pasted "analysis") before proposing or applying any fix. Verifies the claim against real gh run logs, reproduces the root cause locally, fixes it, then re-verifies live post-push. Never trust a failure report at face value.
---

# CI Triage

Failure reports — pasted emails, another AI's "analysis," a teammate's summary — are frequently wrong in specific, plausible-sounding ways: fabricated commit hashes, stale timestamps presented as current, causes that sound technical but don't match the actual error. Treat every such report as a *lead*, not a fact. The only ground truth is `gh run view --log-failed` output.

## Process

### 1. Get the real failure, not the summary

For each claimed failure, resolve it to a concrete run ID and pull the actual log:

```bash
gh run list --repo <owner>/<repo> --limit 10
gh run view <run-id> --repo <owner>/<repo> --log-failed
```

If the report gives a commit hash or timestamp, cross-check it against `git log` / the run's actual metadata. A hash that's real but five days old, presented as "20 hours ago," is a red flag the whole report needs independent verification.

### 2. Diagnose from the log, not from the report's narrative

Read the actual error line (`##[error]...`, stack trace, non-zero exit). Common categories seen in practice:
- Dependency/tool version deprecation (e.g. `actions/upload-artifact@v3` auto-failing)
- Retired runner image (`runs-on: ubuntu-20.04` — job queues forever, never fails outright)
- Auth/secret expiry (`Invalid username or token`) — **not fixable by editing code**; flag for manual secret rotation, don't attempt a workaround
- Script bugs (wrong arg passed, reserved variable shadowed, overly broad regex/keyword match)

If the report's proposed root cause doesn't match what the log actually says, discard the report's diagnosis and follow the log.

### 3. Reproduce locally before calling anything "fixed"

Don't patch and push speculatively. Reproduce the exact failure condition first:
- PowerShell/shell bugs: run the same snippet locally with the same inputs
- SQL/migration bugs: spin up a throwaway container (`docker run --rm -d postgres:15 ...`) and run the real migration against it
- Workflow YAML logic: extract the `run:` block and execute it standalone

Only once you've reproduced the *exact* reported error should you apply a fix — then re-run the same repro to confirm it's resolved.

### 4. Push and re-verify live

After pushing, don't assume the fix landed clean:

```bash
gh run list --repo <owner>/<repo> --limit 5
gh run view <new-run-id> --repo <owner>/<repo> --log-failed   # only if it still fails
```

A fix for one failing step can surface a *different* pre-existing failure in a later step of the same job — that's not a regression you caused, but it does need the same treatment (verify → reproduce → fix → re-verify), not another guess.

### 5. Distinguish "not fixable by me" from "not fixed yet"

Some failures are legitimately outside code-fix scope — expired PATs, missing repo secrets, org-level permissions. Say so explicitly rather than proposing a workaround like `--no-verify` or disabling the check. Never bypass a hook or gate to make a report "look" fixed.

### 6. Scope check before generalizing a fix

If a bug looks structural (hardcoded path, deprecated action version, a footgun pattern), grep for the same pattern across all sibling repos before calling it done — but don't propagate a fix to a repo where the underlying feature/gate doesn't exist. Confirm applicability, don't assume uniformity.
