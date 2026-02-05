---
name: launchpad
description: Interact with Canonical's Launchpad platform via the Launchpad API (api.launchpad.net) using the lp-api CLI tool. Use when working with Ubuntu/Debian packages, bugs, builds, people, projects, or any Launchpad API resources. Triggered by mentions of Launchpad API, Ubuntu development, package builds, or bug tracking.
metadata:
  version: "1.2.8"
---

# Launchpad API

## Overview

This skill enables interaction with Canonical's Launchpad platform (https://launchpad.net) through direct API calls using the `lp-api` command-line tool. It provides full CRUD capabilities (Create, Read, Update, Delete) for querying and managing bugs, people, projects, builds, and other Launchpad resources via the official API at https://api.launchpad.net/devel.html.

**API-First Approach:** This skill focuses on direct API interaction using `lp-api`, not the web UI or Python launchpadlib. All operations are performed via HTTP requests to api.launchpad.net.

**Important Note:** All `lp-api` commands return JSON responses except using with ws.show==total_size, or using download and pipe subcommands. Parse these outputs to extract meaningful information.

## Installation & Troubleshooting

If `lp-api` is not found, use the GitHub API to find and download the correct binary for your system.

**1. Find download URL:**
```bash
# Get the browser_download_url for your OS (linux/darwin/windows) and Architecture (amd64/arm64)
# Example for Linux AMD64:
curl -s https://api.github.com/repos/fourdollars/lp-api/releases | \
  jq -r '.[0].assets[] | select(.name | endswith("linux-amd64.tar.gz")) | .browser_download_url'
```

**2. Download and Install:**
```bash
curl -L -o lp-api.tar.gz <URL>
tar -xzf lp-api.tar.gz
chmod +x lp-api
mkdir -p bin
mv lp-api bin/
export PATH=$PWD/bin:$PATH
```

## Authentication

The tool handles OAuth authentication automatically:

1. **Environment Variable** (preferred for CI/CD):
   ```bash
   export LAUNCHPAD_TOKEN="oauth_token:oauth_secret:consumer_key"
   ```

2. **Config File** (for interactive use):
   - Stored at `.lp-api.toml` in the current directory (recommended)
   - Use `-conf .lp-api.toml` to specify the location
   - Created automatically on first run via OAuth flow
   - User prompted to authorize at launchpad.net

## Resources

Refer to the documentation in `references/` for detailed usage, patterns, and workflows:

- **basics.md**: **START HERE**. CLI usage, core operations (GET/PATCH/POST), URL structure.
- **workflow.md**: Common workflows combining multiple operations (Bug triage, Batch updates, Build monitoring).
- **bugs.md**: Comprehensive guide to bug tracking, searching, and attachments.
- **git.md**: Guide to Git repositories, recipes, and merge proposal reviews.
- **livefs.md**: Guide to monitoring and managing LiveFS (ISO) builds.
- **archive.md**: Guide to working with archives (PPAs) and publishing.
- **package-sets.md**: Guide to managing package sets.
- **people.md**: Guide to managing people, teams, and memberships.
- **project.md**: Guide to managing projects, milestones, and releases.
- **series.md**: Guide to working with Launchpad series (distro releases).

## Quick Tips

### Search Bugs Across ALL Projects

To find bugs you're involved with across all projects and distributions, use `searchTasks` on the person resource:

```bash
# Get your person link
ME_LINK=$(lp-api get people/+me | jq -r '.self_link')

# All bugs assigned to you (across all projects)
lp-api get people/+me ws.op==searchTasks assignee==$ME_LINK

# Filter by status
lp-api get people/+me ws.op==searchTasks assignee==$ME_LINK status=="In Progress"

# Bugs you reported, subscribed to, or have activity on
lp-api get people/+me ws.op==searchTasks bug_reporter==$ME_LINK
lp-api get people/+me ws.op==searchTasks bug_subscriber==$ME_LINK
lp-api get people/+me ws.op==searchTasks bug_commenter==$ME_LINK  # includes any activity
lp-api get people/+me ws.op==searchTasks affected_user==$ME_LINK
```

**Note:** `bug_commenter` includes any bug activity (comments, status changes, field updates), not just message comments.

This is equivalent to the web UI at `https://launchpad.net/~username/+assignedbugs`.
