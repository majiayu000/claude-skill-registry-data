---
name: glab
type: reference
description: Reference for GitLab CLI (glab) - READ-ONLY operations only. ALWAYS read BEFORE using glab commands to ensure correct syntax and available flags.
---

## GitLab CLI Reference (glab)

**IMPORTANT**: This skill is for READ-ONLY operations only. DO NOT execute any commands that create, modify, or delete resources.

### Repository Identification

**Always be specific about which repository to use.**

| Method        | Command                            |
| ------------- | ---------------------------------- |
| Use `-R` flag | `glab <command> -R owner/repo`     |
| Use `--repo`  | `glab <command> --repo owner/repo` |

**Best Practice**: Use `-R owner/repo` explicitly instead of relying on the default repository to avoid ambiguity. The value can be `OWNER/REPO`, `GROUP/NAMESPACE/REPO`, a full URL, or a Git URL.

### Issues (Read-Only)

| Task        | Command                                  |
| ----------- | ---------------------------------------- |
| List issues | `glab issue list -R owner/repo`          |
| View issue  | `glab issue view <number> -R owner/repo` |

**List options**: `--all`, `--assignee <user>`, `--author <user>`, `--labels <label>`, `--milestone <n>`, `--search <text>`, `--state opened|closed|all`, `--per-page <n>`

### Merge Requests (Read-Only)

| Task         | Command                               |
| ------------ | ------------------------------------- |
| List MRs     | `glab mr list -R owner/repo`          |
| View MR      | `glab mr view <number> -R owner/repo` |
| View MR diff | `glab mr diff <number> -R owner/repo` |

**List options**: `--all`, `--assignee <user>`, `--author <user>`, `--labels <label>`, `--milestone <n>`, `--search <text>`, `--state opened|closed|merged|all`

### Repositories (Read-Only)

| Task            | Command                     |
| --------------- | --------------------------- |
| View repo info  | `glab repo view owner/repo` |
| List your repos | `glab repo list`            |
| List org repos  | `glab repo list -g <group>` |

### Releases (Read-Only)

| Task          | Command                                 |
| ------------- | --------------------------------------- |
| List releases | `glab release list -R owner/repo`       |
| View release  | `glab release view <tag> -R owner/repo` |

### CI/CD (Read-Only)

| Task              | Command                                   |
| ----------------- | ----------------------------------------- |
| List pipelines    | `glab ci list -R owner/repo`              |
| View pipeline     | `glab ci view [branch/tag] -R owner/repo` |
| Pipeline status   | `glab ci status -R owner/repo`            |
| Get pipeline JSON | `glab ci get -R owner/repo`               |
| Lint CI config    | `glab ci lint -R owner/repo`              |
| View job log      | `glab ci trace <job-id> -R owner/repo`    |

### Labels (Read-Only)

| Task        | Command                             |
| ----------- | ----------------------------------- |
| List labels | `glab label list -R owner/repo`     |
| Get label   | `glab label get <id> -R owner/repo` |

### Milestones (Read-Only)

| Task            | Command                                 |
| --------------- | --------------------------------------- |
| List milestones | `glab milestone list -R owner/repo`     |
| Get milestone   | `glab milestone get <id> -R owner/repo` |

### Schedules (Read-Only)

| Task           | Command                            |
| -------------- | ---------------------------------- |
| List schedules | `glab schedule list -R owner/repo` |

### Search (Read-Only)

| Task        | Command                              |
| ----------- | ------------------------------------ |
| Search code | `glab search semantic -R owner/repo` |

### API (Read-Only)

| Task        | Command                             |
| ----------- | ----------------------------------- |
| GET request | `glab api <endpoint> -R owner/repo` |

**IMPORTANT**: Never pass write flags to `glab api`. POST/PUT/DELETE methods (`-X`, `--request`, `--method`) and data flags (`-f`/`--field`, `-F`/`--raw-field`, `--input`) perform writes and are denied.
