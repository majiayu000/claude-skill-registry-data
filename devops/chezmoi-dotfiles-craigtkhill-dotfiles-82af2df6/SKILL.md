---
name: chezmoi-dotfiles
description: Manage dotfiles using chezmoi. Use when creating, modifying, or deploying dotfiles, shell functions, or configuration files in this repository.
---

# Chezmoi Dotfiles Management

This skill helps manage dotfiles using chezmoi in this repository.

## Repository Location

All dotfiles are managed in `~/.local/share/chezmoi` which is a git repository synced to GitHub at `https://github.com/craigtkhill/dotfiles.git`.

## Critical Workflow

When creating or modifying dotfiles, you MUST follow this exact order:

1. **Navigate to chezmoi source directory**
   ```bash
   cd ~/.local/share/chezmoi
   ```

2. **Create or edit files using chezmoi naming conventions**
   - Use `dot_` prefix for dotfiles (e.g., `dot_gitconfig` → `~/.gitconfig`)
   - Preserve directory structure (e.g., `dot_config/fish/functions/` → `~/.config/fish/functions/`)
   - You can edit directly in `~/.local/share/chezmoi` or use `chezmoi edit <target-path>`

3. **Apply changes to home directory**
   ```bash
   chezmoi apply
   # or for specific file:
   chezmoi apply ~/.config/fish/functions/myfile.fish
   ```

4. **Commit and push to GitHub**
   ```bash
   cd ~/.local/share/chezmoi
   git add .
   git commit -m "your message"
   git push origin main
   ```

5. **Verify it's managed**
   ```bash
   chezmoi managed | grep myfile
   ```

## Common Commands

- `chezmoi status` - Show what has changed
- `chezmoi diff` - Show detailed differences
- `chezmoi managed` - List all managed files
- `chezmoi apply` - Apply changes from dotfiles to home directory
- `chezmoi apply --force` - Force apply, overriding conflicts
- `chezmoi add <file>` - Add a file to chezmoi tracking
- `chezmoi re-add <file>` - Re-add a tracked file

## Fish Shell Specifics

Fish automatically loads functions from `~/.config/fish/functions/`. Each function must be in its own file named `functionname.fish`.

After adding new fish functions:
1. Copy to `~/.config/fish/functions/`
2. Functions are immediately available (fish auto-loads them)
3. No need to source or reload

## Adding Existing Files to Chezmoi

If you want to add an existing file from your home directory to chezmoi:

```bash
chezmoi add ~/.config/fish/functions/myfile.fish
```

This will copy the file to `~/.local/share/chezmoi` with proper naming and make it managed.

## Common Mistakes

❌ **DON'T**: Edit files directly in `~/.config/fish/` without updating chezmoi
- Changes will be lost when chezmoi applies source files

❌ **DON'T**: Forget to commit and push changes to GitHub
- Your dotfiles won't be backed up or available on other machines

✅ **DO**: Edit in `~/.local/share/chezmoi` → Apply → Commit → Push
