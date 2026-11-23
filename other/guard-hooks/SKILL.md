---
name: guard-hooks
description: >
  Install, check or remove the playbook guard hooks: deterministic guards that stop a coding
  agent from skipping git hooks, committing secrets, adding attribution lines or non-Conventional
  commit subjects, loosening lint config, or committing straight to the default branch, plus a
  typecheck when the agent stops. Use on request only: "install the guard hooks", "set up the
  guards", "why was my commit blocked by a playbook guard", "turn off a guard", "remove the guard
  hooks". Works in Claude Code and Codex.
license: MIT
compatibility: Needs Node 20 or later and git, on macOS or Linux. Not tested on Windows. Hooks run in Claude Code and Codex; Cursor imports the Claude Code entries.
---

# Guard hooks

A skill tells an agent what to do. A hook is a script the agent's harness runs before an action, and it can refuse. These guards cover rules a script can check. They block, ask, or stay silent; they never log and never give advice.

## The guards

| Id | Fires on | What it stops | Result |
| --- | --- | --- | --- |
| `no-verify` | `git commit`, `push`, `merge`, `rebase`, `cherry-pick`, `am`, `pull`, `revert` | `--no-verify` and its abbreviations, `-n` on a commit, `-c core.hooksPath=`, `HUSKY=0`, `GIT_CONFIG_*` on the command | blocked |
| `staged-secrets` | `git commit` | A change that adds an AWS, GitHub, npm, Slack, Anthropic or OpenAI key or a private key, or includes a local env file (`.env`, `.env.local`, `.env.*.local`), a key store or an SSH private key. It reads what is staged, plus what `-a` or a `git add` earlier in the same line is about to stage | blocked |
| `commit-message` | `git commit`, `gh pr create`, `gh pr edit` | `Co-authored-by:` and "Generated with" lines in a commit message or pull request body, and a commit subject that is not a Conventional Commit | blocked |
| `config-protection` | editing a file | Changes to existing lint, format, commitlint, lint-staged, lefthook or husky config and agent hook config. Other new files pass. `playbook-guards.json` is covered even before it exists | asks first |
| `protected-branch` | `git commit`, `git push` | A commit on, or a push to, the remote's default branch or a branch you list | asks first |
| `verify-on-stop` | the agent stopping, in Claude Code | Finishing with type errors, in a project that has a `typecheck` script and whose branch changed TypeScript | sent back once |

"Asks first" is a permission prompt in Claude Code. Codex has no such prompt, so there the action is blocked and the message says how to proceed.

## Install

The installer edits the user's own agent config, so show the change and get a yes before applying it.

1. Find this skill's directory: the one holding this `SKILL.md`. Installed with `npx skills` it is `~/.agents/skills/guard-hooks` (or the same path under the project for a project install). Installed as a plugin it is `skills/guard-hooks` inside the plugin's own folder, which the agent names when it loads this skill. Run the installer from there with no flags. It prints what it would write and changes nothing:

   ```bash
   node scripts/install.mjs
   ```

2. Show the user that output. Tell them what changes: the guard scripts are copied to `~/.playbook/guard-hooks/scripts`, and hook entries pointing at that copy are written to `~/.claude/settings.json` for Claude Code, and to `~/.codex/hooks.json` for Codex when Codex is installed. Other settings and other hooks in those files are kept, and each file is backed up beside itself first.
3. Only after the user agrees, apply it:

   ```bash
   node scripts/install.mjs --apply
   ```

4. Tell the user what is left for them:
   - **Claude Code**: start a new session. Hooks load when a session starts.
   - **Codex**: open Codex and run `/hooks` to review and trust the new hooks. Codex skips a hook until it is trusted, and asks again when an entry changes.
   - **Cursor**: nothing to install. Cursor imports hooks from `~/.claude/settings.json` when its third-party import setting is on. This is from Cursor's documentation and has not been tested with this pack. The stop check runs only when the agent reports a first stop the way Claude Code does, so it cannot loop there.

Use `--agent claude` or `--agent codex` to install for one agent. Running the installer again is safe: it replaces its own hooks and never duplicates them.

The hooks run the copy, not the skill. Updating or removing the skill therefore leaves the guards as they were. After the skill updates, run the installer with `--apply` again to refresh the copy.

## Check

```bash
node scripts/install.mjs --check
```

This lists each installed hook and whether its script exists, and says when the copy is older than the skill. It exits 1 when a hook points at a script that is not there. That state matters because it is silent: a hook whose script is missing fails, the agent treats the failure as harmless and runs the tool, and nothing says a guard is off. Run the check when the user asks whether the guards are working.

The hooks run `node` from the `PATH` the agent starts with. If the agent reports that `node` was not found, start it from a shell where `node --version` works.

Codex gets the pre-tool guards only. `verify-on-stop` relies on the agent saying when it is already continuing after a stop hook, which is confirmed for Claude Code and not for Codex, so it is left out there to rule out a loop.

## Remove

```bash
node scripts/install.mjs --remove --apply
```

This deletes exactly the entries the installer added, and the copy of the scripts once no agent uses it. Nothing else is touched.

Remove the hooks before removing the skill. If the skill is already gone, the copy can remove itself:

```bash
node ~/.playbook/guard-hooks/scripts/install.mjs --remove --apply
```

## Switch a guard off

- **For a session or a machine**: set `PLAYBOOK_GUARDS_DISABLED` in the environment the agent starts in, to a comma-separated list of ids, or `all`. Setting it inside a command the agent runs has no effect.
- **For a project**: add `playbook-guards.json` at the project root.

  ```json
  {
    "disabled": ["verify-on-stop"],
    "protectedBranches": ["release"],
    "conventionalCommits": true,
    "secretScanIgnore": ["test/fixtures/", "docs/**/*.example.md"]
  }
  ```

  `protectedBranches` adds to the remote's default branch. Set `conventionalCommits` to `false` to keep the attribution check and drop the subject check. `secretScanIgnore` lists paths `staged-secrets` skips, for test fixtures that hold fake keys: a file or directory prefix, or a pattern where `*` spans anything. The file is covered by `config-protection`, so an agent cannot quietly change it.

Never switch a guard off to get past a block. A block means the action breaks a rule: fix the action. Switch a guard off only when the user says the rule does not apply to their project.

## When a guard blocks you

The message starts with `[playbook guard: <id>]` and says what to change. Do that. Do not look for another way to run the same thing: no wrapper script, no alias, no editing the hook config. If you believe the block is wrong, stop and tell the user what you ran and what the guard said.

## What the guards do not catch

They stop the common case and say so plainly. They are not a security boundary.

- The command reader follows quotes, heredocs, `cd`, `export`, prefix words such as `sudo` and `timeout`, and `sh -c` wrappers. It does not follow variables, command substitution, aliases, functions or encoded strings. Where it cannot tell what a command will do, it lets the command through.
- `staged-secrets` matches known key shapes. It does not measure entropy and will miss a credential in a format it does not know. Shared env files such as `.env.production` are judged by their content, not their name.
- `commit-message` reads `-m`, `-F` and heredocs. A message typed into an editor, built from a variable, or written to a file by the same command line is not seen.
- `protected-branch` follows `git checkout` and `git switch` earlier in the same line. After a `cd` it cannot follow, it does not ask.
- `config-protection` sees edits made with the agent's edit tools. A config rewritten by a shell command is not seen.

Keep real git hooks and CI as the backstop: commitlint for messages, a secret scanner for secrets, branch protection on the remote. The `setup-commit-hooks-and-release` skill sets up the first of those.

## How it behaves

- A guard that fails internally lets the action through and writes one line to stderr. It never blocks because of its own error.
- Input over 1 MiB is not read, and input is never echoed back.
- A guard writes nothing to disk. Only the installer does: the copy of the scripts and the hook entries.
- A command with no `git` or `gh` in it returns before anything is parsed.
