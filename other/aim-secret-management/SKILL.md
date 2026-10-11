---
name: aim-secret-management
description: Use credentials such as API keys, tokens and passwords without ever seeing them, and ask the user to store one without pasting it into the chat. Use when a task needs a key, token or password that is not set up yet, when the user pastes or offers a credential, wants to store one, and before putting a secret into a command, config file or .env.
allowed-tools: Bash
compatibility: Requires aim-secret, which AI Maestro installs
user-invocable: true
metadata:
  author: 23blocks
  version: 1.0.0
---

# Credentials without seeing them

Secrets live in a local vault, by name. You use them by name and never receive the value, so it stays out of the model, the transcript and your memory.

## Ask for one

```bash
aim-secret has OPENAI_API_KEY || aim-secret request OPENAI_API_KEY --note "for the embedding job"
```

`request` returns at once. The user gets a card in the AI Maestro chat with the name filled in and a masked field (in Claude Code with the secrets mod, the `request_secret` tool opens a form in the terminal instead). End your turn after calling it: you get a message when the value is stored or declined. If it is declined, carry on without it and do not ask again unless you cannot go on.

## Use it

```bash
aim-secret exec --use OPENAI_API_KEY -- python embed.py
aim-secret exec --use AWS_ACCESS_KEY_ID --use AWS_SECRET_ACCESS_KEY -- aws s3 ls
aim-secret exec --use MY_KEY_NAME=OPENAI_API_KEY -- node job.js
```

The value is placed in that one command's environment. Anything the command prints has it replaced by `[secret:NAME]`, which is correct. The last form maps the secret `OPENAI_API_KEY` to the environment variable `MY_KEY_NAME`.

## Names

Capital letters, digits and underscores, starting with a letter, using the provider's usual variable name (`OPENAI_API_KEY`, `GITHUB_TOKEN`). `aim-secret list` prints names only. Reuse an existing name rather than adding a second one for the same credential.

## If a value shows up in the conversation

The user pasted a key or password, or a command printed one. Do not repeat it, copy it into a file or command, or act on it from the chat. Tell the user it is now in the transcript, so it is worth rotating, and run `aim-secret request` so they can store it properly.

## What you do not do

- Read the vault, Keychain entries or `~/.aimaestro/vault`, or print the environment of the command you ran through `exec`.
- Write a secret into a file, a commit, a log or a message. Put `--use NAME` on the command that needs it.
- Run `aim-secret set`. It is for the person, at a terminal.

## When `request` fails

Exit 4 means it could not tell which agent this is or reach AI Maestro: tell the user, and set `AIM_AGENT_ID` if you know your agent id. Exit 2 is a bad name. Exit 5 is a refusal, and the message says why.
