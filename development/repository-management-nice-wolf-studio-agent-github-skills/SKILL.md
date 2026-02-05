---
name: repository-management
description: Manage GitHub repositories - create, fork, branch, and file operations using gh CLI
---
# GitHub Repository Management Skill

This skill provides comprehensive repository management operations including creating repositories, managing branches, and working with files.

## Available Operations

### 1. Create Repository
Create a new GitHub repository in your account or organization.

### 2. Fork Repository
Fork an existing repository to your account or specified organization.

### 3. Create Branch
Create a new branch in a repository from an existing branch.

### 4. Search Repositories
Search for GitHub repositories using GitHub's search syntax.

### 5. Get File Contents
Retrieve the contents of a file or directory from a repository.

### 6. Create or Update File
Create a new file or update an existing file in a repository.

### 7. Push Multiple Files
Push multiple files to a repository in a single commit.

## Usage Examples

### Create a New Repository

**Public repository:**
```bash
gh repo create my-awesome-project --public --description "My awesome project" --clone
```

**Private repository:**
```bash
gh repo create my-private-repo --private --description "Private project" --clone
```

**With README initialization:**
```bash
gh repo create my-project --public --add-readme
```

### Fork a Repository

**Fork to your personal account:**
```bash
gh repo fork owner/repo-name --clone
```

**Fork to an organization:**
```bash
gh repo fork owner/repo-name --org my-org --clone
```

**Fork without cloning:**
```bash
gh repo fork owner/repo-name
```

### Create a Branch

**Create from default branch:**
```bash
gh api repos/owner/repo-name/git/refs -f ref=refs/heads/new-feature -f sha=$(gh api repos/owner/repo-name/git/refs/heads/main --jq '.object.sha')
```

**Using Git directly (if repo is cloned):**
```bash
cd repo-name
git checkout -b new-feature
git push -u origin new-feature
```

### Search Repositories

**Search by keyword:**
```bash
gh search repos "machine learning" --limit 20
```

**Search with filters:**
```bash
gh search repos "web framework" --language python --stars ">1000" --limit 10
```

**Search in organization:**
```bash
gh search repos "org:myorg" --limit 50
```

**Search by topic:**
```bash
gh search repos "topic:docker" --stars ">100"
```

### Get File Contents

**View file contents:**
```bash
gh api repos/owner/repo-name/contents/path/to/file.txt --jq '.content' | base64 -d
```

**List directory contents:**
```bash
gh api repos/owner/repo-name/contents/path/to/directory
```

**Get file from specific branch:**
```bash
gh api repos/owner/repo-name/contents/README.md?ref=develop --jq '.content' | base64 -d
```

### Create or Update File

**Create a new file:**
```bash
echo "file content" | gh api repos/owner/repo-name/contents/path/to/newfile.txt \
  -X PUT \
  -f message="Add new file" \
  -f content=$(echo "file content" | base64) \
  -f branch=main
```

**Update an existing file (requires SHA):**
```bash
# First, get the file SHA
SHA=$(gh api repos/owner/repo-name/contents/path/to/file.txt --jq '.sha')

# Then update
echo "updated content" | gh api repos/owner/repo-name/contents/path/to/file.txt \
  -X PUT \
  -f message="Update file" \
  -f content=$(echo "updated content" | base64) \
  -f sha="$SHA" \
  -f branch=main
```

### Push Multiple Files

For pushing multiple files, it's recommended to clone the repository and use Git:

```bash
# Clone the repository
gh repo clone owner/repo-name
cd repo-name

# Create/modify multiple files
echo "content1" > file1.txt
echo "content2" > file2.txt
mkdir -p src
echo "code" > src/main.py

# Commit and push
git add .
git commit -m "Add multiple files"
git push
```

**Alternative: Using GitHub API for multiple files (requires tree/commit API):**
```bash
# This is more complex and typically requires a script
# Recommended to use Git directly for multiple files
```

## Common Patterns

### Create Repository and Push Initial Code

```bash
# Create repository
gh repo create my-project --public --clone
cd my-project

# Add initial files
echo "# My Project" > README.md
echo "print('Hello')" > main.py

# Commit and push
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Fork, Branch, and Push Changes

```bash
# Fork the repository
gh repo fork upstream/repo-name --clone
cd repo-name

# Create feature branch
git checkout -b my-feature

# Make changes
echo "new feature" > feature.txt
git add feature.txt
git commit -m "Add new feature"

# Push branch
git push -u origin my-feature

# Create PR (using pull-request-management skill)
gh pr create --title "Add new feature" --body "Description of changes"
```

### Clone Private Repository

```bash
# Ensure you're authenticated
gh auth status

# Clone
gh repo clone owner/private-repo
```

## Error Handling

### Repository Already Exists
```bash
# Check if repo exists first
gh repo view owner/repo-name 2>/dev/null && echo "Exists" || echo "Does not exist"
```

### Insufficient Permissions
```bash
# Verify authentication and permissions
gh auth status

# Try refreshing credentials
gh auth refresh
```

### File Not Found
```bash
# Verify the file path exists
gh api repos/owner/repo-name/contents/path/to/file.txt 2>&1 | grep -q "Not Found" && echo "File does not exist"
```

## Best Practices

1. **Always specify owner/repo format**: Use `owner/repo-name` not just `repo-name`
2. **Check authentication first**: Run `gh auth status` before operations
3. **Use descriptive commit messages**: Include context about what changed and why
4. **Branch protection**: Set up branch protection rules for important branches
5. **Clone for multiple changes**: Use Git directly when making multiple file changes
6. **Handle errors gracefully**: Check command exit codes and handle failures

## Related Skills

- `issue-management` - Create and manage issues
- `pull-request-management` - Work with pull requests
- `commit-operations` - View commit history

## References

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Git Documentation](https://git-scm.com/doc)
