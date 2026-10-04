---
name: save-github
description: >
  Upload a local Codex skill to a new GitHub repository.
  Trigger when user says: upload skill to GitHub, publish skill,
  push skill to GitHub, or similar. Creates the repo,
  uploads all files, and generates a README.
---

# Save to GitHub (Skill Publisher)

## Overview

Upload a Codex skill directory to a new public GitHub repository.

## Trigger

User says something like:
- `\u628a\u67d0\u67d0\u6280\u80fd\u4e0a\u4f20\u5230github`
- `upload the xxx skill to github`
- `publish my xxx skill`
- `push xxx skill to github`

Extract the skill name and run the workflow.

## Workflow

1. Resolve the skill directory (check CODEX_HOME/skills/<name>)
2. Get GitHub token (env var GITHUB_TOKEN or ask user)
3. Run the bundled script:

```
python scripts/publish_skill_to_github.py <skill-path> [--token <token>]
```

4. Report the GitHub URL to the user

## Notes

- Requires `requests` Python package (pip install requests)
- Uses GitHub Contents API, no git CLI needed
- Creates a PUBLIC repository
- A README.md is auto-generated