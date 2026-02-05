---
name: gist-management
description: Manage GitHub gists - create, edit, list, and share code snippets using gh CLI
---
# GitHub Gist Management Skill

This skill provides operations for managing GitHub Gists - simple way to share code snippets, notes, and small files.

## Available Operations

### 1. Create Gist
Create new gists (public or secret).

### 2. List Gists
View your gists or public gists.

### 3. View Gist
Display gist content.

### 4. Edit Gist
Update gist files and description.

### 5. Delete Gist
Remove a gist.

### 6. Clone Gist
Clone gist as a Git repository.

### 7. Star/Unstar Gist
Star gists to save them.

### 8. Fork Gist
Fork someone else's gist.

## Usage Examples

### Create Gist

**Create from file:**
```bash
gh gist create myfile.js --desc "Useful JavaScript function"
```

**Create public gist:**
```bash
gh gist create myfile.py --public --desc "Python script"
```

**Create secret gist:**
```bash
gh gist create config.yaml --desc "Configuration file"
```

**Create from multiple files:**
```bash
gh gist create file1.js file2.js file3.js --desc "Project files"
```

**Create from stdin:**
```bash
echo "console.log('Hello')" | gh gist create --filename hello.js --desc "Hello world"
```

**Create in browser:**
```bash
gh gist create myfile.txt --web
```

### List Gists

**List your gists:**
```bash
gh gist list
```

**Limit results:**
```bash
gh gist list --limit 50
```

**List public gists only:**
```bash
gh gist list --public
```

**List secret gists only:**
```bash
gh gist list --secret
```

### View Gist

**View gist content:**
```bash
gh gist view abc123def456
```

**View specific file:**
```bash
gh gist view abc123def456 --filename myfile.js
```

**View in browser:**
```bash
gh gist view abc123def456 --web
```

**View raw content:**
```bash
gh gist view abc123def456 --raw
```

### Edit Gist

**Edit gist file:**
```bash
gh gist edit abc123def456 --filename myfile.js
```

**Add file to gist:**
```bash
gh gist edit abc123def456 --add newfile.js
```

**Update description:**
```bash
# Use API
gh api gists/abc123def456 -X PATCH -f description="Updated description"
```

### Delete Gist

**Delete gist:**
```bash
gh gist delete abc123def456
```

**Delete with confirmation:**
```bash
gh gist delete abc123def456 --confirm
```

### Clone Gist

**Clone gist as Git repo:**
```bash
gh gist clone abc123def456
```

**Clone to specific directory:**
```bash
gh gist clone abc123def456 my-gist-folder
```

### Star Gist

**Using API to star:**
```bash
gh api gists/abc123def456/star -X PUT
```

**Unstar:**
```bash
gh api gists/abc123def456/star -X DELETE
```

**Check if starred:**
```bash
gh api gists/abc123def456/star
```

**List starred gists:**
```bash
gh api gists/starred --jq '.[] | {id, description, files: .files | keys}'
```

### Fork Gist

**Fork using API:**
```bash
gh api gists/abc123def456/forks -X POST --jq '{id, url: .html_url}'
```

## Common Patterns

### Quick Code Sharing

```bash
# Share a code snippet
cat script.sh | gh gist create --filename script.sh --desc "Deployment script" --public

# Get the URL
gh gist list --limit 1
```

### Backup Configuration

```bash
# Backup dotfiles
gh gist create ~/.bashrc ~/.vimrc --desc "My dotfiles backup"
```

### Collaborative Gist

```bash
# Create gist
gh gist create notes.md --public --desc "Meeting notes"

# Others can fork and modify
# gh gist fork abc123def456
```

## Best Practices

1. **Use descriptive names**: Make filenames and descriptions clear
2. **Public vs Secret**: Use secret for sensitive (not private!) content
3. **Version control**: Gists are Git repos, commit history is preserved
4. **Organize**: Use consistent naming and descriptions
5. **Clean up**: Delete unused gists periodically

## Integration with Other Skills

- Use `repository-management` for full projects
- Share code snippets from `code-review` discussions
- Quick prototypes before creating full repos

## References

- [GitHub CLI Gist Documentation](https://cli.github.com/manual/gh_gist)
- [GitHub Gists Guide](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists)
- [Gists API](https://docs.github.com/en/rest/gists)
