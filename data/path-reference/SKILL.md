---
name: path-reference
description: Create properly formatted references to paths (files or folders) in a git repository. Use when writing docs that need to link to any path in the repo.
---

# path-reference

Create clickable links to paths in a git repository.

## Commands

**Get web URL** (always use `-b default` for stable links):
```bash
uvx --from git-web-url==1.0.1 gwu url -p $path -b default
```

**Get relative path** (for display text):
```bash
uvx --from git-web-url==1.0.1 gwu relpath -p $path
```

## Link Formats

**Markdown:**
```markdown
[relative/path/to/file.py](https://github.com/user/repo/blob/main/relative/path/to/file.py)
```

**reStructuredText:**
```rst
`relative/path/to/file.py <https://github.com/user/repo/blob/main/relative/path/to/file.py>`_
```

## Supported Platforms

GitHub, GitLab, Bitbucket, AWS CodeCommit (including enterprise variants)
