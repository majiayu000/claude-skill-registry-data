---
name: capture-evidence
description: Hand off verification to the Cursor worker sai-verifier and return criterion-level results, screenshots, and a real screen recording of at most 30 seconds.
---

# Capture evidence

The coding agent implements and prepares the environment. Cursor Auto verifies on `sai-verifier` without editing application code. The coding agent records the worker desktop, but does not drive the browser.

## Prepare and hand off

1. Commit the change and record the exact SHA. Use `devdock-development` to prepare changed services and the required UI. Confirm the served or synchronized code matches the revision under test.
2. For new job classes, run the job explicitly in-pod when necessary: development SQS queues are shared with UAT workers.
3. Keep credentials in the worker's `~/.secrets/test-accounts.env`. Load only required values through the configured secret mechanism. Never print them or include literal secrets in prompt files or artifacts.
4. Write a handoff containing the task, repo, branch, SHA, URLs, numbered acceptance criteria with exact steps, relevant environment checks and task helpers, and artifact destinations. Instruct the verifier to verify only and never edit live-synced application checkouts.

The existing helpers are under `/srv/Code/agent/verification`. Inspect them before use: `cursor-run.py` currently has a task-specific repository, and the environment scripts have task-specific defaults. Confirm the target repository, revision, worker, and helper paths match this task. If they do not, report the setup blocker instead of verifying the wrong project.

For a matching setup:

```bash
python3 bin/cursor-run.py create handoff/<task>.prompt.md --name 'verify <task> <sha>' --ref <sha> --model auto
python3 bin/cursor-run.py watch <agent-id> <run-id>
python3 bin/cursor-run.py followup <agent-id> <prompt-file>
python3 bin/cursor-run.py artifacts <agent-id> --download <dir>
```

Keep follow-ups in the same conversation. Explicitly select `auto`; do not silently use a different model or revision.

## Browser instructions for the verifier

- Launch the configured `chromium` wrapper so VPN PAC routing applies.
- On transient tunnel errors, 403s, or unexpected UAT-US redirects, wait 10 seconds and reload, at most six times. Persistent failure is BLOCKED.
- Load the required credentials immediately before login. Use one login attempt; report BLOCKED on failure without exposing the values.
- On Google or Microsoft human verification, leave the page open, report “waiting for human verification”, and poll every 30 seconds for at most 20 minutes. Sai completes it through Show desktop.

## Record and assess

Record the actual worker desktop with FFmpeg `x11grab` while the verifier performs the key steps. Confirm the display and resolution first. Trim login, waiting, and retries from the delivered video. Keep it at most 30 seconds, check duration with `ffprobe`, and inspect playback and screenshots. A screenshot slideshow is not a recording.

Report each criterion as PASS, FAIL, or BLOCKED, with reproduction steps, tested SHA, and artifact paths. Prove changed code handled the flow through pod logs or runtime evidence. Rule out competing explanations such as an existing webhook or scheduled pull before accepting a PASS.

FAIL goes back to implementation, then verification against the new SHA. BLOCKED identifies the missing prerequisite. Attach screenshots and the video to the task conversation with a concise criterion report. Keep the PR description focused on problem, change, configuration, and tests.
