---
name: go-deploy
version: "1.0.0"
user-invocable: true
description: Open the project's deployment platform link. Triggers when user says 「去部署」「部署平台」「准备部署」 (go deploy / deploy platform / prepare to deploy) — even without explicitly saying "open link", as long as the intent is to access a deployment console or release platform. The skill reads docs/deploy.md for deployment links; if absent, scans project docs to extract and generate config; if nothing found, prompts user to provide. Supports multiple deployment links per project.
---

# Go Deploy — Open Deployment Links

## Triggers

- 「去部署」 (go deploy)
- 「部署平台」 (deploy platform)
- 「准备部署」 (prepare to deploy)

On trigger, execute one action: **open the deployment platform link**. No deployment execution, no status queries, no build operations.

---

## Phase 1: Read docs/deploy.md

1. Look for `docs/deploy.md` in the project root
2. **Exists** → proceed to Phase 3 (parse links)
3. **Does not exist** → proceed to Phase 2 (scan project)

---

## Phase 2: Scan Project

`docs/deploy.md` doesn't exist — the project hasn't configured deployment info yet. Scan existing docs to auto-extract and generate config, reducing manual input burden.

Scan these sources in priority order (higher-priority sources are typically maintained by project owners and more reliable):

| Priority | Source | Scan Logic |
|----------|--------|------------|
| 1 | `AGENTS.md` | Find sections with 「部署」「deploy」「发布」 keywords, extract URLs |
| 2 | `README.md` | Same as above |
| 3 | `scripts/` directory | Find scripts with `deploy`/`open`/`publish` in filename, read URL variables |
| 4 | CI/CD config | `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile` |
| 5 | `package.json` | `scripts` field with `deploy`/`publish`/`release` commands |

**Link filtering**: Project docs often contain many irrelevant URLs (dependency sites, reference docs, etc.). Only extract URLs that look like deployment consoles (containing `deploy`/`console`/`cluster`/`release` keywords, or known platform domains). Deduplicate and annotate each with its source.

### Scan Result Handling

- **Candidate links found** → list all candidates (with source files), ask user to confirm which are actual deployment links (keyword matching has false positives — user confirmation avoids writing wrong info) → after confirmation, generate `docs/deploy.md` (see format below) → proceed to Phase 3
- **No candidate links found** → output this prompt:

```
No deployment-related information found in the project.

Please provide the following and I'll create docs/deploy.md:
1. Deployment link URL (required)
2. Deployment platform name (optional, e.g. "Vercel", "Internal Deploy Platform")
3. Brief description (optional)

If the project has multiple deployment links, list them separately.
```

After user provides info, generate `docs/deploy.md` and proceed to Phase 3.

---

## Phase 3: Parse Links

Extract deployment links from `docs/deploy.md`:

1. Find all `##` level-2 headings (each heading = one deployment target)
2. Under each heading, find lines starting with `**Link**:` or `**链接**:` or `**URL**:` and extract the URL
3. Optionally read `**Platform**:` / `**平台**:` and `**Description**:` / `**说明**:` lines
4. Aggregate into a link list

**Error handling**: `docs/deploy.md` exists but no link line found → prompt that format doesn't match convention, proceed to Phase 2 (scan). URL not starting with `http://` or `https://` → skip and warn.

---

## Phase 4: Select Link

- **Only 1 link** → proceed directly to Phase 5
- **Multiple links** → list all, ask user to select (ask every time, don't remember previous choice):

```
Detected the following deployment links:

1. <first ## heading>
2. <second ## heading>

Enter the number of the link to open:
```

---

## Phase 5: Open Link

Execute the OS-appropriate command:

```bash
# macOS
open "<URL>"
# Linux
xdg-open "<URL>"
# Windows (Git Bash / MSYS2 / Cygwin)
cmd.exe /c start "" "<URL>"
```

**Fallback**: If browser can't open or command fails → output the URL directly, prompt user to copy manually. After opening, state: "Opened: \<link name\>".

---

## docs/deploy.md Format Convention

Each deployment target is a `##` level-2 heading. Under it, a list with `**Link**:` line for URL (required); `**Platform**:` and `**Description**:` are optional. Create the `docs/` directory if it doesn't exist when generating.

**Example**:

```markdown
# Deployment

## Production

- **Platform**: Internal Deploy Platform
- **Link**: https://deploy.example.com/console/my-project
- **Description**: Main deployment entry — view cluster status, release new versions

## Staging

- **Link**: https://pre-deploy.example.com/my-project
```
