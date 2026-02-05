---
name: sync-dotfiles
description: Sync dotfiles from private chezmoi repository to public dotfiles repository. Use when the user requests to update their public dotfiles repo, sync dotfiles, or copy dotfiles from chezmoi to the public repository. This skill renders chezmoi templates and applies safety filtering to prevent accidentally exposing sensitive files.
---

# Sync Dotfiles

Sync dotfiles from the private chezmoi repository (`~/.local/share/chezmoi`) to the public dotfiles repository (`~/Developer/misc/dot`). This skill processes chezmoi templates and applies safety filtering to prevent accidentally syncing sensitive data.

## Workflow

### 1. Run the sync script

Execute the sync script to copy files from chezmoi to the public repo:

```bash
python scripts/sync_dotfiles.py
```

The script will:
- Get all files managed by chezmoi
- Filter out sensitive patterns (`.ssh/`, `.gnupg/`, `*secret*`, `*token*`, `*password*`, etc.)
- Render chezmoi templates to get final file content
- Copy rendered files to the public repo
- Leave all changes **unstaged** for manual review

**Options:**
- `--dry-run`: Preview what would be synced without copying files
- `--chezmoi-dir <path>`: Override chezmoi source directory (default: `~/.local/share/chezmoi`)
- `--public-repo <path>`: Override public repo directory (default: `~/Developer/misc/dot`)

**Example with dry run:**
```bash
python scripts/sync_dotfiles.py --dry-run
```

### 2. Review changes

After syncing, review the unstaged changes in the public repo:

```bash
cd ~/Developer/misc/dot
git status
git diff
```

Check carefully for:
- Sensitive information (API keys, tokens, passwords)
- Private paths or system details
- Anything you're not ready to share publicly

### 3. Selectively stage changes

Stage only the files you want to make public:

```bash
# Stage specific files
git add .zshrc .vimrc

# Or stage all changes if everything looks good
git add -A

# Or discard changes you don't want
git restore <file>
```

### 4. Commit and push when ready

```bash
git commit -m "Update dotfiles"
git push
```

## Safety Blocklist

The script automatically skips these sensitive patterns:

- **SSH/GPG**: `.ssh/*`, `.gnupg/*`, `*.pem`, `*.key`, `*_rsa`, `*_ed25519`
- **Credentials**: `*secret*`, `*password*`, `*token*`, `*credential*`, `*.env`, `*api_key*`
- **Cloud**: `.aws/credentials`, `.aws/config`, `.azure/*`, `.gcloud/*`
- **Other**: `.netrc`, `.docker/config.json`, `*_history`, shell histories

These patterns provide a safety net, but **always manually review** the diff before committing.

## Template Processing

The skill uses `chezmoi cat` to render templates, which means:
- Template variables are resolved to their actual values
- Conditional sections are processed
- The public repo gets the final rendered output, not the `.tmpl` files

This ensures your public dotfiles show what users would actually use, not chezmoi's internal template syntax.
