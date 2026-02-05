---
name: dual-folder-workflow
description: "Workflow for private repos + Colab training. Trigger when: (1) training on Colab with private repo, (2) separating dev from production, (3) avoiding untested code in production."
author: Claude Code
date: 2025-12-18
---

# Dual-Folder Workflow - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-18 |
| **Goal** | Separate development from production when using private repo with Colab training |
| **Environment** | Windows, Git, Google Colab, Private GitHub repo |
| **Status** | Success |

## Context
When a repository is private, Google Colab cannot directly `git clone` it. The typical workflow involves:
1. Zip the local repo
2. Upload to Google Drive
3. Unzip in Colab and train

The problem: If you're actively developing new features, you risk accidentally uploading untested code for production training. Models trained with buggy code could then be used for live trading.

## Verified Workflow

### Folder Structure
```
C:\users\smith\
├── Alpaca_trading/           # stable branch - PRODUCTION
│   └── Zip this for Colab training
│   └── Run live/paper trading from here
│
└── Alpaca_trading_dev/       # develop branch - TESTING
    └── Test new features here
    └── Never use for production
```

### One-Time Setup
```bash
# Ensure main folder is on stable
cd C:\users\smith\Alpaca_trading
git checkout stable
git pull origin stable

# Clone second copy for development
cd C:\users\smith
git clone https://github.com/<user>/<repo>.git Alpaca_trading_dev
cd Alpaca_trading_dev
git checkout develop
```

### Daily Workflow

| Task | Folder | Branch |
|------|--------|--------|
| Production training (zip for Colab) | `Alpaca_trading/` | stable |
| Live/paper trading | `Alpaca_trading/` | stable |
| Testing new features | `Alpaca_trading_dev/` | develop |
| Feature ready for production | Merge develop → stable |

### Promoting Features to Production
```bash
# In Alpaca_trading_dev - push your changes
git add .
git commit -m "feat: My new feature"
git push origin develop

# In Alpaca_trading - pull and merge
cd ../Alpaca_trading
git checkout stable
git fetch origin
git merge origin/develop -m "Merge develop: My new feature"
git push origin stable
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Single folder, branch switching | Easy to forget which branch you're on | Use separate folders for physical separation |
| Relying on git status before zip | Human error - forgot to check | Dedicated production folder eliminates risk |
| develop as default branch | Accidentally trained with untested code | Always use stable for production |
| No folder naming convention | Confusion about which is which | Clear naming: `_dev` suffix for development |

## Final Parameters
```yaml
# Folder structure
production_folder: Alpaca_trading
development_folder: Alpaca_trading_dev

# Branch assignments (never change these)
production_branch: stable
development_branch: develop

# Workflow rules
- Never zip Alpaca_trading_dev for Colab
- Never run live_trader.py from Alpaca_trading_dev
- Always merge develop → stable (never the reverse for features)
```

## Key Insights
- **Physical separation > branch discipline** - Two folders eliminates "which branch am I on?" errors
- **Naming matters** - `_dev` suffix makes it obvious which folder is for testing
- **Stable = production** - Both training AND trading use stable branch
- **develop = testing only** - Never use develop for production workloads
- **Merge direction** - Features flow: develop → stable (never backwards)

## References
- CONTRIBUTING.md: Full branch strategy documentation
- CLAUDE.md: Project workflow section
