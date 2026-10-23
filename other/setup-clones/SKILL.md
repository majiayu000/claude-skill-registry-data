---
name: setup-clones
description: Configure shadowclone clones on this machine. A clone is Claude Code or Codex that works as the user, in Docker, toward a draft pull request. Use it when the user asks for clones, cloud sessions, or a background agent that works as them.
license: MIT
---

# Set Up Clones

Do the whole setup for the user. The user answers questions in chat, pastes tokens into a file, and approves the skill files. Run the steps in order. Do not explain a step that works.

A clone runs Claude Code or Codex as the user, on the user's own subscription or key, in Docker on this machine. The user starts it from the CLI or from an agent that has the shadowclone MCP tools.

## Rules

- Never ask for a token in chat, and never read the secrets file. The user pastes each token into the secrets file.
- Show the skill files to the user. Call the next step with `approve: true` only after the user agrees.
- If a step fails, show the exact error, fix what you can, and run the step again.

## 1. Check the machine (1 minute)

1. Run `shadowclone --version`. If the command is missing, install the CLI with `npm install -g @shadowclone/cli@latest`. Never use `sudo`.
2. Run `gh auth status`. If it reports no login, ask the user to run `gh auth login` in a terminal.
3. Run `docker info`. If Docker does not run, ask the user to start Docker Desktop, OrbStack, or Docker Engine.

## 2. Ask two questions (30 seconds)

Ask these in one message. Use your question tool if you have one. Put the recommended choice first.

1. **Which repository and which login?** The login choices are `claude-subscription` (default, from `claude setup-token`), `chatgpt-subscription` (never on a public repository), `anthropic`, `openai`, `openai-compatible`, `ollama`, or `foundry`.
2. **Keep the agent trailer?** Each commit gets `Co-authored-by` for the agent unless the user says no.

## 3. Run setup

1. Call the `shadowclone_clone_setup` tool with `operation: "setup"`, the repository, `provider`, and `baseUrl` or `model` when they apply.
2. If the skills repository is missing, call `operation: "skills"` in the repository checkout. Show the files, and call it again with `approve: true` after the user agrees. Then call setup again.

If the tool is not available, run `shadowclone clone setup --repo <owner/repository>` in a terminal instead.

## 4. The user adds the tokens

1. Give the user the secrets file path, the list of secrets from setup, and the `GH_TOKEN` link.
2. For `claude-subscription`, the user gets the token from `claude setup-token`.
3. For `chatgpt-subscription`, ask the user to run `shadowclone clone login --repo <owner/repository>` in a terminal.
4. Wait until the user says done.

## 5. Check and report

1. Call `shadowclone_clone_setup` with `operation: "status"` and the repository.
2. If a line says `fail`, give the user its detail, and check again after the user fixes it.
3. When every line says `pass`, tell the user how to start a clone: the `shadowclone_clone` tool with `operation: "start"`, or `shadowclone clone start --repo <owner/repository> "<task>"`.
4. Tell the user that `shadowclone_sessions` or `shadowclone clone list` shows each clone and its pull request.
