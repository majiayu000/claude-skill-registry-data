---
name: forgejo-cli
type: reference
description: Reference for Forgejo CLI (fj) - READ-ONLY operations only. ALWAYS read BEFORE using fj commands to ensure correct syntax and available flags.
---

## Forgejo CLI Reference (fj)

**IMPORTANT**: This skill is for READ-ONLY operations only. DO NOT execute any commands that create, modify, or delete resources.

The `forgejo-cli` package provides the `fj` binary.

### Repository Identification

By default, `fj` operates on the repository detected from the current directory.

| Method                 | Command                      |
| ---------------------- | ---------------------------- |
| Use `-R <remote>`      | `fj <command> -R origin`     |
| Use `-r/--repo <repo>` | `fj <command> -r owner/repo` |
| Use `-H <host>`        | `fj <command> -H <host>`     |

`-R/--remote` selects a **local git remote** by name (e.g. `origin`). `-r/--repo` takes an `owner/repo` and is accepted by `release` and `tag` subcommands. `-H/--host` overrides the host.

### Current User (Read-Only)

| Task   | Command     |
| ------ | ----------- |
| Whoami | `fj whoami` |

### Issues (Read-Only)

| Task           | Command              |
| -------------- | -------------------- |
| Search issues  | `fj issue search`    |
| View issue     | `fj issue view <id>` |
| List templates | `fj issue templates` |

**Search options**: `--state open|closed|all`, `--author <user>`, `--label <label>`, `--limit <n>`, `--keyword <text>`

### Pull Requests (Read-Only)

| Task       | Command                 |
| ---------- | ----------------------- |
| Search PRs | `fj pr search`          |
| View PR    | `fj pr view <number>`   |
| PR status  | `fj pr status <number>` |

### Repositories (Read-Only)

| Task           | Command                       |
| -------------- | ----------------------------- |
| View repo info | `fj repo view [repo]`         |
| View README    | `fj repo readme [repo]`       |
| View labels    | `fj repo labels view [repo]`  |
| Star status    | `fj repo star-status [repo]`  |
| Watch status   | `fj repo watch-status [repo]` |

### Releases (Read-Only)

| Task          | Command                 |
| ------------- | ----------------------- |
| List releases | `fj release list`       |
| View release  | `fj release view <tag>` |

### Tags (Read-Only)

| Task      | Command             |
| --------- | ------------------- |
| List tags | `fj tag list`       |
| View tag  | `fj tag view <tag>` |

### Organizations (Read-Only)

| Task         | Command                 |
| ------------ | ----------------------- |
| List orgs    | `fj org list`           |
| View org     | `fj org view <name>`    |
| List members | `fj org members <name>` |

### Users (Read-Only)

| Task | Command |
| --- | --- |
| Search users | `fj user search <q>` |
| View user | `fj user view <name>` |
| User repos | `fj user repos <name>` |
| User orgs | `fj user orgs <name>` |
| Followers/Following | `fj user followers <name>` / `fj user following <name>` |

### Actions (Read-Only)

| Task           | Command                     |
| -------------- | --------------------------- |
| List tasks     | `fj actions tasks`          |
| List secrets   | `fj actions secrets list`   |
| List variables | `fj actions variables list` |
