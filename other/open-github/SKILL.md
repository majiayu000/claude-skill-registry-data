---
name: open-github
description: Open GitHub pages in a browser — repo, issue, PR, secrets, or org/personal repos
argument-hint: "[repo|issue|pr|secrets|org|personal] [owner/repo] [#n]"
related:
  - list-github
  - all-github-repo

---

## Goal

Open GitHub pages in a browser with native OS commands, per the specified target — repo, issue, pull request, secrets settings, or repos of an org/personal account

## Scope

- `repo` (default): open the repo's `/tree/<current-branch>`
- `issue <n>` / `pr <n>`: open the specified issue or pull request
- `secrets`: open the repo's settings/secrets page
- `org` / `personal`: open repos in the org or personal account per context
- Never modify any repo

See also: /all-github-repo, /list-github-repo

## Execute

### 1. Resolve Target And Repo

> Goal: Get the correct owner, repo, target type, and number

1. Read the target from the first argument (`repo`, `issue`, `pr`, `secrets`, `org`, `personal`) — default `repo`
2. If `owner/repo` is given → use it
3. If not given → run `git remote get-url origin` and parse it into `owner/repo` (`https://` or `git@` form)
4. Run `git branch --show-current` for the repo target
5. If not in a git worktree and no argument → ask the user

### 2. Build URL

> Goal: Build the URL from the target type

- `repo` → `https://github.com/<owner>/<repo>/tree/<branch>`
- `issue` → `https://github.com/<owner>/<repo>/issues/<n>`
- `pr` → `https://github.com/<owner>/<repo>/pull/<n>`
- `secrets` → `https://github.com/<owner>/<repo>/settings/secrets/actions`
- `org` → `https://github.com/orgs/<org>/repositories` or the repo specified in the org context
- `personal` → `https://github.com/<owner>/<repo>` on the personal account
- URL-encode branches/params containing special characters

### 3. Open In Browser

> Goal: Open the URL with the OS default browser

1. Windows: `start <url>`; macOS: `open <url>`; Linux: `xdg-open <url>`
2. Report the opened URL in chat

## Rules

- Open only via OS native commands; do not substitute `webfetch`
- If the URL cannot be built → ask the user instead of guessing
- Always report the URL after opening

## Expected Outcome

- The requested GitHub page opens in the browser
