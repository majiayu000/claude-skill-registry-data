---
name: push-github
description: Push current project to GitHub with professional structure and branding. Use when Rick says push, commit, or put on GitHub.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit
---

# Push to GitHub

## Steps
1. Ensure README.md has RJ Business Solutions branding and logo
2. Ensure .gitignore excludes .env, node_modules, .wrangler
3. Ensure .env.example exists with all required variables (no values)
4. Initialize git if needed: `git init`
5. Configure: `git config user.name "Rick Jefferson"` and `git config user.email "rjbizsolution23@gmail.com"`
6. Add all: `git add .`
7. Commit: `git commit -m "feat: $ARGUMENTS"`
8. Create repo if needed: `gh repo create rjbizsolution23-wq/<repo-name> --public --source=. --remote=origin`
9. Push: `git branch -M main && git push -u origin main`

## README Template
Always include:
- Company logo: `![RJ Business Solutions](https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg)`
- Company name and address
- Tech stack
- Setup instructions
- Contact info: rjbizsolution23@gmail.com, rickjeffersonsolutions.com
- (c) 2025 RJ Business Solutions. All rights reserved.
