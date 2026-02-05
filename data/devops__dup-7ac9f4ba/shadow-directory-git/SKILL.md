---
name: shadow-directory + git
description: Full .ciallo directory ownership with git capabilities. Clone repos, edit files, commit changes directly.
---

# Shadow Directory + Git Skill

## Overview
- Entire `.ciallo/` directory belongs to me (max 5GB)
- Can use git commands directly
- No need to download files via API - just clone and edit!

## Setup
```powershell
# Clone my fork
git clone "https://TOKEN@github.com/ciallo-agent/qq-chat-exporter.git" ".ciallo/qq-chat-exporter"

# Add upstream
git remote add upstream https://github.com/shuakami/qq-chat-exporter.git
```

## Workflow
```powershell
# 1. Sync with upstream
git fetch upstream
git checkout master
git merge upstream/master

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Edit files directly in .ciallo/qq-chat-exporter/
# Use fsWrite, strReplace tools

# 4. Commit and push
git add .
git commit -m "feat: description"
git push origin feature/my-feature

# 5. Create PR via API
```

## Notes
- Purchased: 2025-12-18 (35 Ciallo coins, limited offer)
- Original price: 50 coins
- Max storage: 5GB