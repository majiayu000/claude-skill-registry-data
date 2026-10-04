---
name: publish-insights
description: This skill should be used when the user wants to publish their Claude Code /insights report to GitHub Pages. It automates creating a git repo, setting up GitHub, enabling Pages, and monitoring the deployment. Triggers on "publish insights", "share my insights report", "put insights on GitHub Pages", or after generating an /insights report.
---

# Publish Insights

Publish a Claude Code `/insights` report to GitHub Pages for easy sharing and access.

## Prerequisites

- **GitHub CLI (`gh`)** - Must be installed and authenticated. Verify with `gh auth status`.
- **Git** - Must be installed.

If `gh` is not authenticated, prompt user to run `gh auth login` first.

## Example Session

**User:** "Publish my insights report"

**Claude:**
1. Found report at `~/.claude/usage-data/report.html`
2. Detected GitHub user: `jtsternberg`
3. Confirmed settings: repo `claude-insights`, public visibility
4. Created repo and enabled Pages
5. Published to: https://jtsternberg.github.io/claude-usage-data/

## Workflow

> Placeholders like `{username}` and `{repo}` should be replaced with actual values gathered during pre-flight.

Copy this checklist and track progress:

```
Publishing Progress:
- [ ] Verify prerequisites
- [ ] Locate report file
- [ ] Pre-flight confirmation
- [ ] Initialize git repo (if needed)
- [ ] Copy report and create README
- [ ] Validate files
- [ ] Commit changes
- [ ] Create GitHub repo
- [ ] Push to GitHub
- [ ] Enable GitHub Pages
- [ ] Monitor deployment
- [ ] Verify and report success
```

### Step 1: Verify Prerequisites

```bash
gh auth status
```

**If not authenticated:** Stop and ask user to run `gh auth login` first.

### Step 2: Locate Report File

Check for the report file:

```bash
[ -f ./report.html ] && echo "Found: ./report.html" || \
[ -f ~/.claude/usage-data/report.html ] && echo "Found: ~/.claude/usage-data/report.html" || \
echo "Not found"
```

- **Found in current directory:** Use `./report.html`
- **Found in default location:** Use `~/.claude/usage-data/report.html`
- **Not found:** Ask user for the path, or suggest running `/insights` to generate one

### Step 3: Pre-Flight Confirmation

Gather all inputs upfront. Get the GitHub username:

```bash
gh api user --jq '.login'
```

Present a confirmation checklist with defaults:

```
Publish to GitHub Pages:
- Report: {detected-path}
- GitHub user: {username}
- Repo name: claude-insights (default)
- Visibility: public

Confirm to proceed, or specify changes.
```

User confirms once; no per-step prompts after this.

### Step 4: Initialize Git Repository

Check if already in a git repo:

```bash
git rev-parse --git-dir 2>/dev/null && echo "In git repo" || echo "Not in git repo"
```

- **Not in a repo:** Create a new directory and initialize:
  ```bash
  mkdir -p {repo} && cd {repo}
  git init && git branch -M main
  ```
- **In an existing repo:** Ask user if they want to use this repo or create a new directory

### Step 5: Copy Report and Create README

Copy the report as `index.html`:

```bash
cp {report-path} ./index.html
```

Create a minimal README.md:

```markdown
# Claude Code Usage Insights

Interactive dashboard of Claude Code usage patterns, generated with `/insights`.

**View the report:** https://{username}.github.io/{repo}/

## Generate Your Own

Run `/insights` in any Claude Code session, then use `/publish-insights` to publish it.
```

### Step 6: Validate Files

Verify the report file is valid HTML:

```bash
head -5 index.html | grep -q "<!DOCTYPE html\|<html" && echo "Valid HTML" || echo "Warning: May not be valid HTML"
```

**If invalid:** Warn user and confirm whether to proceed.

### Step 7: Commit Changes

```bash
git add index.html README.md
git commit -m "$(cat <<'EOF'
Add Claude Code usage insights report

Generated with Claude Code /insights command.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Step 8: Create GitHub Repository

```bash
gh repo create {username}/{repo} --public --description "Claude Code usage insights report" --source=. --remote=origin
```

**If repo already exists:** Ask user to choose a different name or confirm using the existing repo. To use existing:
```bash
git remote add origin https://github.com/{username}/{repo}.git
```

### Step 9: Push to GitHub

```bash
git push -u origin main
```

**If push fails (non-empty repo):** May need to pull first or force push. Ask user preference.

### Step 10: Enable GitHub Pages

```bash
gh api repos/{username}/{repo}/pages -X POST --input - <<'EOF'
{
  "build_type": "legacy",
  "source": {
    "branch": "main",
    "path": "/"
  }
}
EOF
```

**If Pages already enabled:** This will error; that's fine, continue to monitoring.

### Step 11: Monitor Deployment

Inform user: "Deployment started. You can watch progress at: https://github.com/{username}/{repo}/actions"

Then poll for completion:

```bash
# Poll every 10 seconds - Pages builds typically complete in 30-60 seconds
# Shorter intervals waste API calls; longer delays feel unresponsive
while true; do
  STATUS=$(gh api repos/{username}/{repo}/pages/builds --jq '.[0].status')
  if [ "$STATUS" = "built" ]; then
    echo "Build complete!"
    break
  elif [ "$STATUS" = "errored" ]; then
    echo "Build failed!"
    gh api repos/{username}/{repo}/pages/builds --jq '.[0].error'
    break
  fi
  sleep 10
done
```

### Step 12: Verify and Report Success

Verify the page loads (may take 1-2 minutes to propagate):

```bash
curl -s -o /dev/null -w "%{http_code}" https://{username}.github.io/{repo}/
```

**If not 200:** Wait 30 seconds and retry up to 3 times.

Report to user:

- **Live URL:** `https://{username}.github.io/{repo}/`
- **Repository:** `https://github.com/{username}/{repo}`
- Confirmation that page returns HTTP 200

## Rollback

If the process fails after creating the repo, clean up:

```bash
# Delete the remote repo (requires confirmation)
gh repo delete {username}/{repo} --yes

# Remove local git artifacts if desired
rm -rf .git index.html README.md
```
