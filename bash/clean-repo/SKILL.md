---
name: clean-repo
description: "Removes every template-managed artifact across all domains by running each domain's clean-workspace skill after one combined dry run and prompt. Use when the user wants a full pre-push reset; for one domain or one mod, use that domain's cleanup skill instead."
argument-hint: "[--yes] [--dry-run] [--keep-server] [--plan <ID>] [--other-project]"
disable-model-invocation: true
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\<other>\`.

# /clean-repo

Remove everything the template's skills created, across all domains, so the repo is ready to push.

This is a thin orchestrator. It finds every `skills/<domain>-clean-workspace/` skill and runs its `clean.py`. Each domain owns its own cleanup logic. Today that is only `/dayz-clean-workspace` (DayZ scaffolds, junctions, deploy dirs and server staging).

## How to run

```cmd
python "<skill-dir>\clean.py" [--yes] [--dry-run] [--keep-server] [--plan <ID>] [--other-project]
```

| Argument | Notes |
|---|---|
| `--yes` | Skip the confirmation prompt. Required when stdin isn't a TTY. |
| `--dry-run` | Show the combined plan and its plan ID, then stop without removing anything. |
| `--keep-server` | Keep `.server/` (test-server configs, missions, logs). Children run without `--include-server`. |
| `--plan <ID>` | The plan ID from an earlier `--dry-run`. Refuses (exit 3) if the current plan differs, so nothing the user did not see is removed. Use the same `--keep-server` choice as the dry run. Not valid with `--dry-run` (exit 2). |
| `--other-project` | Allow cleaning the project cached by `/dayz-init` when it is not this checkout. Without it, that case is refused (exit 2). |

### From an agent shell

The agent's shell is not a TTY, so the script cannot prompt there. Ask in chat instead:

1. Run `python "<skill-dir>\clean.py" --dry-run` (add `--keep-server` if the user wants to keep their server configs and missions).
2. Show the user the combined plan it printed, including the project folder from its `Project:` line, any `[WARN]` lines and the `Plan ID:` line.
3. Ask in chat whether to remove everything listed from that project. Stop if they do not clearly say yes. If a `[WARN]` line says the cached project is not this checkout, say so in the question.
4. On a yes, run the command the dry run printed after `To remove exactly this plan, run:`. It already carries `--yes --plan <ID>` plus `--keep-server` and `--other-project` when they apply. If it exits 3, the plan changed: show the new plan and ask again.

## What it does

Each child cleans the project cached by `/dayz-init` (shown as `Project:` in the plan), which may not be this checkout; run `/dayz-init` in the checkout you mean to clean first.

- **Plan first.** Every run starts with each child's dry run, printed under a `=== /<skill> (--dry-run) ===` header. That is the combined plan. If any child's dry run fails, nothing is removed (exit 1).
- **Versioned server files.** Unless `--keep-server` is passed, it asks git which files under the project's `.server/` are tracked or kept trackable by the project's `.gitignore` (the template ignores all of `.server/`, but a clone may add exceptions for `serverDZ.cfg` or `mission/` edits) and warns with up to five of their paths. If git cannot be run there or fails (for example the project is not a git repository), a dry run warns and prints no removal command, and a removal run refuses with exit 1. Pass `--keep-server` to clean without touching `.server/`.
- **Plan ID.** `Plan ID: <ID>` is a 12-character hash of the server choice, every child's dry-run output and the path, size and modification time of each versioned `.server/` file. Anything added or edited after the dry run, including a mission file or `serverDZ.cfg`, changes it. `--plan <ID>` refuses (exit 3) when the ID no longer matches.
- **Confirmation.** Without `--yes` it asks `Remove everything listed above from <project>? [y/N]`. Any answer other than `y` or `yes`, or end of input, aborts with exit 0. After a yes it repeats the check silently and refuses (exit 3) if the plan changed while the prompt was open.
- **Other checkout.** When the cached project is not this checkout (a git worktree or second clone), it prints a `[WARN]`, and a removal run refuses (exit 2) unless `--other-project` is passed.
- **Removal.** Runs each child with `--include-server --yes` (just `--yes` with `--keep-server`) under a `=== /<skill> (--yes) ===` header.

Each child still decides what to remove from its own state when it runs; the plan check narrows the gap to the moment between the last dry run and the removal.

It does not gate on `/dayz-preflight`, because it is domain-agnostic. Each child gates on its own preflight.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Completed, dry run completed, user aborted, or no cleanup skills found |
| 1 | A child's dry run or cleanup failed, the `/dayz-init` project cache could not be read, or git could not list the versioned `.server/` files and `--keep-server` was not passed |
| 2 | `--plan` combined with `--dry-run`, not a TTY and `--yes` not passed, or the cached project is not this checkout and `--other-project` not passed |
| 3 | The plan changed since it was shown or approved (`--plan` mismatch, or a change while the prompt was open); nothing was removed |

## Discovery

Any folder in `skills/` whose name ends in `-clean-workspace` and contains `clean.py` is picked up. Folders starting with `_` are skipped. A new domain plugs in by shipping a `<domain>-clean-workspace` skill that accepts `--include-server`, `--dry-run` and `--yes`, keeps server staging unless `--include-server` is passed, and prints the same dry-run output (stdout and stderr) for the same state (the plan ID hashes it).

## When to use this vs. a single domain cleanup

| Goal | Use |
|---|---|
| Remove one mod's DayZ artifacts | `/dayz-clean-workspace --mod <Name>` |
| Remove all DayZ artifacts (mods and server staging) | `/dayz-clean-workspace --include-server` |
| Remove everything across every domain before a push | `/clean-repo` |
| Same, but keep `.server/` configs and missions | `/clean-repo --keep-server` |
