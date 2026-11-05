---
name: fluttairbar
description: Check the AI command-line tools on this device (Claude Code, Codex, OpenCode, Pi, Cursor Agent, Grok Build, fx, Ori, ZCode) for their installed and newest versions and safe updates, and how much of the Claude, Codex and Cursor subscriptions signed in here is used, which agent skills, hooks and instructions file each coding agent has, and whether conversation history is kept on two devices, with fluttAIrbar's command line `fluttairbar-cli`. Use when asked whether AI tools are up to date, how much usage or limit is left, when a limit resets, before updating an AI command-line tool, or which skills an agent has.
---

# fluttAIrbar

`fluttairbar-cli` reads what is installed and signed in on this device. It
never prints tokens, emails or account ids and never rewrites a credentials
file.

## AI command-line tools

```bash
fluttairbar-cli harnesses --json            # every tool it knows
fluttairbar-cli harnesses --json --only codex,claude
```

One object per tool: `id`, `name`, `installed`, `currentVersion`,
`latestVersion`, `updateAvailable`, `ageGateSatisfied`, `updateSource`
(`npm`, `githubRelease` or `officialChannel`), `checkError`, and `configs`
(each tool's config files, sensitive ones shown as present only).

- `updateAvailable` with `ageGateSatisfied: false` means the release is
  newer than 14 days: fluttAIrbar holds npm and GitHub releases back until
  then. Say so; do not install it another way.
- `officialChannel` tools (Claude Code's native install, Grok Build) update
  through their own updater.

## Usage limits

```bash
fluttairbar-cli usage --json
```

`{"schema":"fluttairbar.usage.v1","providers":[...]}`, one provider each for
`codex`, `claude` and `cursor`: `state` (`ok`, `signed-out`, `expired`,
`stale`, `paused`, `error`), `detail` (what to do, in a sentence), `plan`, and
`windows`, each with `label` ("5 hours", "7 days"), `used_percent` and
`resets_at` (ISO 8601, UTC). Report the percentages and when they reset in
the user's local time. `stale` or `expired` means the user should run that
tool once to renew its session; never renew it yourself.

## Updating (ask first)

```bash
fluttairbar-cli harnesses --update --only codex   # one tool
fluttairbar-cli harnesses --update                # every verified update
fluttairbar-cli harnesses --sync-codex-daemon     # Codex CLI to its daemon's version
```

These install software: ask the user before running them, and run them
only for tools the scan showed as ready. Exit 1 means an update failed; the
output says which.

## Agent skills, hooks, shared instructions, quiz, conversation history

```bash
fluttairbar-cli skills --json               # skills per agent, and their instructions file
fluttairbar-cli skills install --all -n     # what linking would do; nothing changes
fluttairbar-cli hooks --json                # hooks per agent: installed, missing, different, no hooks
fluttairbar-cli hooks install --all -n      # what adding them would do; nothing changes
fluttairbar-cli conversations --json        # history kept here, last copies, `behind`
```

`skills` lists per skill and agent `linked`, `via DIR`, `copy`, `off` or
`missing`, and for each agent whether its instructions file is `linked` to
the shared one. `conversations` shows `behind`: directions of the copy that
keep failing, with days. `hooks` lists each declared hook's `state` for
its agent; an agent without hook settings is `no hooks`, never guessed.
`install`, `add`, `remove`, `on`, `off` (skills and hooks) and
`conversations copy` change files: run them with `-n` first, show the plan,
and add `-y` only when the user said so. Conversation history is never
deleted or pruned; `quiz` uses the agents' subscriptions, so run it only when
asked.

## Not installed?

From a checkout of https://github.com/mmdmcy/fluttAIrbar on Linux:
`tool/install_linux.sh` (the tray app and `fluttairbar-cli`), or only the
command line with `flutter pub get` and then `dart compile exe
tool/fluttairbar_cli.dart -o ~/.local/bin/fluttairbar-cli`. Both need the
Flutter SDK; the compiled `fluttairbar-cli` does not, so it can be copied to
a machine without it.
