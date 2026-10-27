---
name: github-pages-deploy
description: Deploy a static HTML file or static site directory to GitHub Pages. Use when the user wants a durable GitHub-hosted URL for a static page, diagram, report, or generated site, and can provide GitHub authentication via GITHUB_TOKEN or GH_TOKEN.
metadata:
  version: "0.1.0"
  author: arisng
---

# GitHub Pages Deploy

Deploy static content to GitHub Pages using a dedicated Pages branch in a GitHub repository.

This skill is similar in spirit to zero-config preview deploy skills, but GitHub Pages has different constraints:

- Authentication is required. Use `GITHUB_TOKEN` or `GH_TOKEN`.
- The deployment is tied to a GitHub repository you control.
- Publish latency is usually slower than Vercel. Expect build time.
- The skill manages a dedicated branch, `gh-pages` by default.

## Use when

- The user wants a durable static URL under `github.io`
- The content is plain HTML, CSS, JS, or a prebuilt static directory
- The user wants repository-backed hosting instead of a claimable preview deployment

## Requirements

- `pwsh`
- `git`
- `GITHUB_TOKEN` or `GH_TOKEN`

Token requirements:

- Classic PAT: `repo`
- Fine-grained PAT: repository `Contents: write`, `Administration: write`, `Pages: write`

## Usage

```powershell
pwsh {{skill_dir}}/scripts/deploy.ps1 -Path ./site -Repo owner/repo
```

```powershell
pwsh {{skill_dir}}/scripts/deploy.ps1 -Path ./diagram.html -Repo my-diagram
```

## Arguments

- `-Path` Required. A static site directory or a single `.html` file.
- `-Repo` Required. Either `owner/repo` or just `repo`. If only `repo` is provided, the authenticated user becomes the owner.
- `-Owner` Optional override when `-Repo` is only a repository name.
- `-Branch` Optional. Defaults to `gh-pages`.
- `-CName` Optional custom domain. The script also writes a `CNAME` file.
- `-NoWait` Optional. Return immediately after push and Pages configuration.

## Behavior

1. Resolves GitHub auth from `GITHUB_TOKEN` or `GH_TOKEN`
2. Stages the input into a temp directory
3. If the input is a single HTML file, renames it to `index.html`
4. Ensures `.nojekyll` exists so GitHub Pages serves assets literally
5. Creates the target repository if it does not exist
6. Updates the dedicated Pages branch without touching the caller's working tree
7. Configures GitHub Pages to serve from that branch root
8. Waits for the latest Pages build unless `-NoWait` is set
9. Prints a human-readable summary and one JSON object on stdout

## Output

The script prints progress to stderr and emits a JSON object to stdout:

```json
{"siteUrl":"https://owner.github.io/repo/","repoUrl":"https://github.com/owner/repo","owner":"owner","repo":"repo","branch":"gh-pages","createdRepo":true,"pagesStatus":"built","buildStatus":"built","commitSha":"abc123..."}
```

## Operational Notes

- This skill is not anonymous. There is no claimable deploy model.
- The target branch is deployment-managed content. Do not point it at a branch you edit manually unless that is intentional.
- Existing Pages configuration on the same repository will be updated to the selected branch and root path.
- A repository named `owner.github.io` publishes at the user or org root domain. Other repositories publish under `/repo/`.

## Failure Modes

- Missing token: export `GITHUB_TOKEN` or `GH_TOKEN`
- Missing permissions: ensure the token can create repos and manage Pages
- Private Pages limitations: use a public repository unless your plan supports private Pages
- Build delay: use `-NoWait` if you only need the target URL and will verify later