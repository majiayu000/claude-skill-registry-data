---
name: educoder-cli
description: Guide Codex through solving or writing code for an EduCoder homework task with educoder-cli. Use when the user asks to solve a Touge/EduCoder task, write an Educoder answer, fetch a homework problem statement, download remote starter code, submit local code for evaluation, or debug an EduCoder evaluation failure using this CLI.
---

# EduCoder CLI

## Overview

Use `educoder-cli` as the source of truth for task context. Work from real task data, keep credentials and submitted source out of logs, and treat submission as a remote state-changing action.

Read `references/educoder-cli.md` for installation commands, selector rules, JSON fields, and the verified real path.

## Setup

1. Confirm `uv` is available.
2. Install the CLI when the `educoder` command is missing:

   ```bash
   uv tool install git+https://github.com/lihaoze123/educoder-cli
   ```

3. In a clone of this repository, use `uv run educoder ...` instead of the tool command.
4. Log in through the CLI:

   ```bash
   educoder login --login <account>
   ```

   Let the CLI prompt for the password. Do not ask the user to paste passwords, cookies, `zzud`, `autologin`, or `_educoder_session` in chat.

## Workflow

1. Verify the CLI and credentials:

   ```bash
   educoder status --json
   ```

   If running from this repo, use `uv run educoder status --json`.

2. Select the task target.

   If the user did not specify a target, discover candidates:

   ```bash
   educoder courses --json
   educoder homeworks --course <course> --json
   ```

   Prefer exact course/homework identifiers when available. If several plausible targets exist, ask the user to choose before editing or submitting.

3. Read the real problem context:

   ```bash
   educoder task --course <course> --homework <homework> --json
   educoder task --course <course> --homework <homework>
   ```

   Extract the challenge path, statement, test sets, prior compile output, pass/fail status, time limit, and next/previous game identifiers. Use the text rendering when it is easier to read Markdown/HTML problem statements.

4. Fetch the current remote code into a local working file:

   ```bash
   educoder code --course <course> --homework <homework> --output <path> --force --json
   ```

   Use the returned `path` as the remote answer path. Keep downloaded source in a normal working file, not in chat logs or Trellis/research artifacts.

5. Solve locally.

   Inspect the statement and tests first. Preserve the expected remote file type and path, such as `main.py` or a `.circ` file. Use local language/tooling checks when available. For non-code artifacts such as Logisim circuits, avoid rewriting opaque file formats unless you understand the structure.

6. Submit only when safe:

   ```bash
   educoder submit --course <course> --homework <homework> --file <path> --timeout 60 --json
   ```

   `submit` saves code remotely and triggers evaluation. Do not run it unless the user selected the course/homework or the current task target is unambiguous. For exploratory work, stop after preparing the local file and explain the exact submit command.

   For command-line/WebSSH tasks where `submit` only saves files and does not run terminal commands, run the required remote command and trigger evaluation with:

   ```bash
   educoder exec --course <course> --homework <homework> --command "<shell-command>" --evaluate --timeout 60 --json
   ```

   Use `--command -` to read a longer shell script from stdin. Keep WebSSH connection details and secrets out of chat logs.

7. Iterate from feedback.

   On failure or timeout, read the JSON/text submission output and the task detail again. Use `last_compile_output`, test-set `output` versus `actual_output`, and `compile_success` to decide the next edit. Avoid pasting full submitted source or raw payloads into the conversation.

## Safety Rules

- Never print or persist `zzud`, `autologin`, `_educoder_session`, cookies, headers, request bodies, or full raw API payloads.
- Do not store downloaded or submitted source in skill references, Trellis research files, or final answers.
- Treat `code --output` as local file creation and `submit` as remote mutation.
- If the CLI reports ambiguous course/homework matches, show the candidate names/IDs and ask for one target.
- If a task has not been started and no `game_identifier` can be resolved, tell the user to open the experiment in the EduCoder web UI first.

## Completion Checklist

- CLI installed or installation blocker reported.
- Credentials checked or missing-login blocker reported.
- Course and homework target recorded by identifier or ID.
- Problem statement, challenge path, tests, and prior compile output inspected.
- Local answer file created or updated.
- Submission run only when target and remote mutation are appropriate.
- Final answer summarizes pass/fail status, changed local files, and any next command needed.
