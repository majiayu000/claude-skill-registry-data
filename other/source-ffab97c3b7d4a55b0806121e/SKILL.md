---
name: domino-projects
description: Work with Domino Projects including Git integration, DFS vs Git-based projects, collaboration, and version control. Covers project creation, Git provider setup (GitHub, GitLab, Bitbucket), branch management, collaborator permissions, and project settings. Use when creating projects, setting up Git repos, or managing team collaboration.
---

# Domino Projects and Git Skill

## Description
This skill helps users work with Domino Projects - including project creation, Git integration, version control, and collaboration features.

## Activation
Activate this skill when users want to:
- Create or configure a Domino project
- Set up Git integration
- Understand DFS vs Git-based projects
- Collaborate with team members
- Manage project settings and permissions

## Project Types

### Git-Based Projects
- Code stored in external Git provider (GitHub, GitLab, Bitbucket)
- Full Git workflow support
- Better for teams familiar with Git
- Access to Git provider features (PRs, issues)

### Domino File System (DFS) Projects
- Code stored in Domino's internal file system
- Automatic versioning (Git under the hood)
- Simpler for users unfamiliar with Git
- Good for research and experimentation

## Creating a Project

### Via Domino UI
1. Click **New Project**
2. Enter project name
3. Select project type:
   - **Git-based**: Connect to Git repository
   - **DFS**: Use Domino File System
4. Configure settings
5. Click **Create**

### Via Python SDK
```python
from domino import Domino

domino = Domino()

# Create DFS project
project = domino.project_create(
    project_name="my-project",
    owner_name="your-username"
)

print(f"Project ID: {project['id']}")
```

## Git-Based Projects

### Connecting to Git Repository
1. Create project as Git-based
2. Enter repository URL
3. Configure authentication:
   - **SSH Key**: Add SSH public key to Git provider
   - **HTTPS**: Use personal access token

### Git Credentials
```bash
# Add SSH key to Domino account
# Go to Account Settings > Git Credentials

# Or use HTTPS with token
https://username:token@github.com/org/repo.git
```

### Working with Git in Workspaces

#### Sync Changes
Click **Sync** in workspace to push changes:
1. Domino commits changes
2. Pushes to configured branch
3. Updates project state

#### Manual Git Commands
```bash
# Check status
git status

# Add and commit
git add .
git commit -m "Update model training"

# Push to remote
git push origin main

# Pull latest
git pull origin main
```

#### IDE Git Integration
- VS Code: Use Source Control panel
- JupyterLab: Use Git extension
- RStudio: Use Git pane

### Branch Management
```bash
# Create feature branch
git checkout -b feature/new-model

# Work on branch
git add .
git commit -m "Add new model"
git push origin feature/new-model

# Switch branches
git checkout main
```

### Multi-Repository Support
Domino supports multiple Git repositories per project:

1. Go to Project Settings > **Repositories**
2. Add additional repositories
3. Configure mount paths
4. Enable/disable per execution

```python
# Access code from multiple repos
# Repo 1: /mnt/code/main-repo/
# Repo 2: /mnt/code/shared-lib/
from shared_lib import utils
```

## DFS Projects

### How DFS Works
- Files stored in Domino-managed Git
- Automatic commits on sync
- Version history tracked
- Simplified workflow

### Sync Files
1. Work in workspace
2. Click **Sync** when ready
3. Enter commit message
4. Files pushed to Domino

### View History
1. Go to **Files** in project
2. Click **History**
3. View all commits
4. Restore previous versions

## Project Structure

### Recommended Structure
```
project/
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── data/               # Local data (small files)
├── src/                # Source code
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
├── notebooks/          # Jupyter notebooks
│   └── exploration.ipynb
└── tests/              # Unit tests
    └── test_model.py
```

### Special Paths
- `/mnt/code/`: Project files
- `/mnt/data/`: Domino Datasets
- `/mnt/artifacts/`: Output artifacts
- `/mnt/imported/`: Imported project files

## Collaboration

### Project Roles

| Role | Permissions |
|------|-------------|
| **Owner** | Full control, delete project |
| **Admin** | Manage members, settings |
| **Contributor** | Edit files, run executions |
| **Launcher User** | Run launchers only |
| **Results Consumer** | View results only |

### Adding Collaborators
1. Go to Project Settings > **Access**
2. Click **Add Collaborator**
3. Search for user
4. Assign role
5. Click **Add**

### Sharing Projects
- **Private**: Only invited users
- **Organization**: All org members can view
- **Public**: Anyone in Domino instance

## Project Settings

### Environment
Set default compute environment:
1. Go to Project Settings > **Environment**
2. Select default environment
3. Optionally allow overrides

### Hardware Tier
Set default resources:
1. Go to Project Settings > **Hardware Tier**
2. Select default tier
3. Set GPU preferences

### Environment Variables
Add project-level variables:
```
API_KEY=your-api-key
MODEL_VERSION=v2.0
DEBUG=false
```

Access in code:
```python
import os
api_key = os.environ.get('API_KEY')
```

## Importing/Exporting Projects

### Import Project
1. Click **New Project**
2. Select **Import**
3. Choose source:
   - Git repository
   - ZIP file
   - Another Domino project

### Export Project
```bash
# Download project files
domino download project-owner/project-name
```

### Fork Project
1. Go to project page
2. Click **Fork**
3. Creates copy in your account

## Reproducibility

### Execution Records
Every execution tracked:
- Exact code version
- Environment used
- Hardware tier
- Inputs/outputs
- Start/end times

### Reproduce Past Execution
1. Go to Jobs or Workspaces
2. Find execution to reproduce
3. Click **Reproduce**
4. Creates workspace with same settings

### Environment Locking
Lock environment to specific revision:
```python
# In project settings or via SDK
domino.project_update(
    project_name="my-project",
    environment_id="env-specific-revision"
)
```

## Best Practices

### 1. Use Git for Code
Keep code in version control for:
- Change tracking
- Code reviews
- Collaboration
- Rollback capability

### 2. Separate Code and Data
- Code: Git repository
- Large data: Domino Datasets
- Artifacts: `/mnt/artifacts/`

### 3. Document Projects
Include README with:
- Project purpose
- Setup instructions
- How to run
- Dependencies

### 4. Use Environments
Don't install packages ad-hoc; use:
- Dockerfile instructions
- requirements.txt
- Environment configuration

### 5. Regular Commits
```bash
# Commit frequently with meaningful messages
git commit -m "Add data preprocessing step"
git commit -m "Fix model evaluation bug"
```

## Troubleshooting

### Git Authentication Failed
- Verify credentials in Domino account settings
- Check token hasn't expired
- Ensure repository access permissions

### Sync Conflicts
```bash
# Pull latest first
git pull origin main

# Resolve conflicts
git status
# Edit conflicting files
git add .
git commit -m "Resolve conflicts"
```

### Files Not Appearing
- Check file is in correct path
- Verify sync completed
- Refresh browser

## Documentation Reference
- [Version control and Git](https://docs.dominodatalab.com/en/latest/user_guide/bd26e2/version-control-and-git/)
- [Git-based Projects](https://docs.dominodatalab.com/en/latest/user_guide/910370/git-based-projects/)
- [Use Git in your Workspace](https://docs.dominodatalab.com/en/cloud/user_guide/0d2247/use-git-in-your-workspace/)
- [Projects overview](https://docs.dominodatalab.com/en/cloud/user_guide/5b332c/projects-overview/)
