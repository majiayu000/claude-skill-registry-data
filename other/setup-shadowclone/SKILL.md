---
name: setup-shadowclone
description: Install and configure shadowclone for the user from start to finish. Use it when the user asks to "set up", install, configure, or start shadowclone with Claude Code, Codex, Cursor, Pi, Antigravity, OpenCode, or another agent.
license: MIT
---

# Set Up shadowclone

Do the whole setup for the user. The user only answers questions in chat and picks skills in the browser. Finish in less than 5 minutes.

Do the steps in order. Run long commands in the background, and do the next step while they run. Do not explain a step that works.

## 1. Check the CLI (10 seconds)

1. If this skill is on disk, run `node <this-skill-directory>/scripts/check-cli.mjs`. It runs only `shadowclone --version` and prints a status.
2. If this skill is not on disk, run `shadowclone --version`. Version 0.0.13 or newer is `ready`. A missing command is `unavailable`.
3. If the status is `ready`, run `shadowclone init --status --json`. If it prints `{"initialized":true}`, setup exists. Keep its consent choices, and go to step 4.
4. If the status is `unavailable` or `outdated`, tell the user that you will install the shadowclone CLI. Start `npm install -g @shadowclone/cli@latest` in the background. Never use `sudo`.
5. If npm cannot write to its global folder, show the exact error. Help the user choose a user-owned npm prefix, and run the install again.

## 2. Ask three questions (30 seconds)

Ask these questions in one message while the install runs. Use your question tool if you have one. Record an explicit yes or no for each answer.

1. **Learn from past sessions?** shadowclone reads the coding-agent sessions on this machine, redacts them, and learns your rules with your own agent CLI. The first pass takes up to 2 minutes.
2. **Keep skills in sync?** shadowclone keeps your skills up to date across your agents.
3. **Keep learning in the background?** This needs a yes to question 1.

If the answer to question 1 is no, the answer to question 3 is no. Do not infer an answer from the install, from the use of an agent, or from another answer.

## 3. Install and initialize (in the background)

1. Wait for the CLI install, and check the CLI again as in step 1.
2. Install the plugin for the agent that you run in, if it is not installed. The plugin adds this skill and the shadowclone MCP server.
   - Claude Code: `claude plugin install shadowclone --marketplace theonly1me/shadowclone`
   - Codex: `codex plugin marketplace add theonly1me/shadowclone`, then `codex plugin add shadowclone@shadowclone`
   - Cursor, Pi, Antigravity, and OpenCode have no plugin step.
3. If a plugin command asks for input or fails, give the user the command, and continue the setup.
4. Start one `shadowclone init` command in the background. Pass exactly one flag from each pair, from the answers:
   - `--learn` or `--no-learn`
   - `--skill-maintenance` or `--no-skill-maintenance`
   - `--background-learning` or `--no-background-learning`

The command detects Claude Code, Codex, Cursor, Pi, Antigravity, and OpenCode, and installs their native guidance. With `--learn`, it also runs the first learning pass.

## 4. Open the skill wizard (while init runs)

1. Start `shadowclone wizard` as a background process. It opens the skill wizard in the browser and prints a loopback URL.
2. Give the user the URL. Tell the user to pick skills, select **Equip**, and tell you when it is done.
3. Do not operate the browser for the user.
4. If the wizard says that another update is running, tell the user to wait a few seconds and equip again.

## 5. Verify and report (30 seconds)

When the user equipped a build and `init` is done:

1. Stop the wizard process.
2. Run `shadowclone sync`.
3. Run `shadowclone doctor`. Fix each local failure that you can act on.
4. Run `shadowclone context --explain` in the current repository.
5. Tell the user the number of rules learned, the skills that are active, and each step that failed or that you skipped.
6. If learning stopped at its setup budget and background learning is off, tell the user that `shadowclone learn --deep` continues it for up to 5 minutes.
7. Tell the user to restart each open coding-agent session. This loads the plugin, the MCP server, and the native guidance.

Do not turn on a source, call a model, read sessions, or publish files without the matching consent. Keep command output that holds local paths or user content out of shared artifacts.
