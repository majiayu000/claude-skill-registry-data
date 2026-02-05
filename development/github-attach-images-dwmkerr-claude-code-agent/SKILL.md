---
name: GitHub Attach Images
description: Attach images to GitHub PRs and issues via a scratch repo
---

# GitHub Attach Images

Attach images to GitHub PRs or issues by hosting them in a scratch repo.

## When to use

- Adding screenshots to PR comments
- Attaching images to issue comments
- Any GitHub comment needing embedded images

## Setup scratch repo

1. **Clone or create scratch repo**
   ```bash
   git clone git@github.com:<USERNAME>/scratch.git /tmp/scratch
   ```
   If it doesn't exist, create a public repo called `scratch` first.

2. **Folder structure**
   ```
   scratch/
   └── github-attachments/
       └── <org>_<repo>_<pr-or-issue>/
           ├── 01-screenshot.png
           └── 02-screenshot.png
   ```

## Add images

1. **Copy images to scratch repo**
   ```bash
   mkdir -p /tmp/scratch/github-attachments/<org>_<repo>_<number>
   cp /path/to/screenshots/*.png /tmp/scratch/github-attachments/<org>_<repo>_<number>/
   ```

2. **Push to GitHub**
   ```bash
   cd /tmp/scratch
   git add .
   git commit -m "chore: images for <org>/<repo>#<number>"
   git push
   ```

## Attach to PR or issue

**Comment on PR:**
```bash
gh pr comment <NUMBER> --repo <org>/<repo> --body "$(cat <<'EOF'
## Screenshots

![Description of screenshot](https://raw.githubusercontent.com/<USERNAME>/scratch/main/github-attachments/<org>_<repo>_<number>/01-screenshot.png)

This shows...
EOF
)"
```

**Comment on issue:**
```bash
gh issue comment <NUMBER> --repo <org>/<repo> --body "$(cat <<'EOF'
![Description](https://raw.githubusercontent.com/<USERNAME>/scratch/main/github-attachments/<org>_<repo>_<number>/image.png)
EOF
)"
```

## Image URL format

```
https://raw.githubusercontent.com/<USERNAME>/scratch/main/github-attachments/<org>_<repo>_<number>/<filename>
```
