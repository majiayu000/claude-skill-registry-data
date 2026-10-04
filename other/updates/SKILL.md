---
name: updates
description: Send project-manager-style progress updates during long Codex goals or long-running tasks using Gmail when connected. Use when the user asks for updates, PM updates, progress notifications, email updates, status reports during /goals, or non-final updates during long work.
---

# Updates

Send concise user-visible status updates during long-running work, especially `/goals`, without ending the current turn.

Use updates for:

- Reporting major, meaningful progress.
- Completing a major phase.
- Needing user input.
- Hitting a blocker.
- Risky, expensive, or long-running work.
- During active long work when useful, while avoiding routine updates more often than every 30 minutes.

When using this skill for a long task:

- Keep track of the task start time.
- Keep track of the last update time.
- Before sending the first routine email, wait for the requested update interval to elapse; do not email as soon as the task starts.
- When Codex regains control after a substantial step or tool call, check elapsed time before deciding whether to send a routine update.

Choose the update channel:

1. If Gmail is available, send updates by Gmail to the authenticated account itself.
2. Otherwise, tell the user they need to connect Gmail in Codex to receive updates.

For Gmail:

- Use `gmail._get_profile` to get the connected account email.
- Send only to that same email address.
- Use only `gmail._send_email`.
- Do not use Gmail search, read, archive, delete, label, forward, attachment, or mailbox-management tools.
- Do not attach files.
- Do not include secrets, raw logs, file contents, or large command output.
- Keep the email short: subject under 80 characters and body under 1,500 characters.
- Use the current project name in the subject. Prefer the git repository name from `git remote get-url origin` when available; otherwise use the basename of `git rev-parse --show-toplevel`; otherwise use the current workspace folder name.
- Include the exact current thread name at the top of the body. In Codex Desktop, resolve it from `CODEX_THREAD_ID` and `$CODEX_HOME/session_index.jsonl` or `~/.codex/session_index.jsonl` when needed.
- If the exact project name cannot be resolved, do not invent one; use `Codex update` without a suffix.
- If the exact thread name cannot be resolved, omit the `Thread:` line.

Suggested subject format:

`Codex update: <exact project name>`

Suggested body format:

```text
Thread: <exact thread name>
Status: <info | blocked | input needed | done>

<2-5 short plain-language sentences. Split longer updates across multiple lines, roughly one line every 1-2 sentences. Use single line breaks inside this update text, not blank lines between sentences.>

Next: <what Codex is doing next or what is needed from the user>
```

Avoid routine update spam. Do not send more than one routine update every 30 minutes unless the user specifically requested it, but send blocker or input-needed updates immediately.
