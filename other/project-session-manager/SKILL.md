---
name: project-session-manager
description: Worktree-first dev environment manager for issues, PRs, and features with optional tmux sessions
aliases: [psm]
level: 2
---

# Project Session Manager (PSM) Skill

`psm` is the compatibility alias for this canonical skill entrypoint.

> **Quick Start (worktree-first):** Start with `omc teleport` when you want an isolated issue/PR/feature worktree before adding any tmux/session orchestration:
> ```bash
> omc teleport #123          # Create worktree for issue/PR
> omc teleport my-feature    # Create worktree for feature
> omc teleport list          # List worktrees
> ```
> See [Teleport Command](#teleport-command) below for details.

Automate isolated development environments using git worktrees and tmux sessions with Claude Code. Enables parallel work across multiple tasks, projects, and repositories.

Canonical slash command: `/oh-my-copilot:project-session-manager` (alias: `/oh-my-copilot:psm`).

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `review <ref>` | PR review session | `/psm review omc#123` |
| `fix <ref>` | Issue fix session | `/psm fix omc#42` |
| `feature <proj> <name>` | Feature development | `/psm feature omc add-webhooks` |
| `list [project]` | List active sessions | `/psm list` |
| `attach <session>` | Attach to session | `/psm attach omc:pr-123` |
| `kill <session>` | Kill session | `/psm kill omc:pr-123` |
| `cleanup` | Clean merged/closed | `/psm cleanup` |
| `status` | Current session info | `/psm status` |

## Project References

Supported formats:
- **Alias**: `omc#123` (requires `~/.psm/projects.json`)
- **Full**: `owner/repo#123`
- **URL**: `https://github.com/owner/repo/pull/123`
- **Current**: `#123` (uses current directory's repo)

## Configuration

### Project Aliases (`~/.psm/projects.json`)

```json
{
  "aliases": {
    "omc": {
      "repo": "Yeachan-Heo/oh-my-copilot",
      "local": "~/Workspace/oh-my-copilot",
      "default_base": "main"
    }
  },
  "defaults": {
    "worktree_root": "~/.psm/worktrees",
    "cleanup_after_days": 14
  }
}
```

## Providers

PSM supports multiple issue tracking providers:

| Provider | CLI Required | Reference Formats | Commands |
|----------|--------------|-------------------|----------|
| GitHub (default) | `gh` | `owner/repo#123`, `alias#123`, GitHub URLs | review, fix, feature |
| Jira | `jira` | `PROJ-123` (if PROJ configured), `alias#123` | fix, feature |

### Jira Configuration

To use Jira, add an alias with `jira_project` and `provider: "jira"`:

```json
{
  "aliases": {
    "mywork": {
      "jira_project": "MYPROJ",
      "repo": "mycompany/my-project",
      "local": "~/Workspace/my-project",
      "default_base": "develop",
      "provider": "jira"
    }
  }
}
```

**Important:** The `repo` field is still required for cloning the git repository. Jira tracks issues, but you work in a git repo.

For non-GitHub repos, use `clone_url` instead:
```json
{
  "aliases": {
    "private": {
      "jira_project": "PRIV",
      "clone_url": "git@gitlab.internal:team/repo.git",
      "local": "~/Workspace/repo",
      "provider": "jira"
    }
  }
}
```

### Jira Reference Detection

PSM only recognizes `PROJ-123` format as Jira when `PROJ` is explicitly configured as a `jira_project` in your aliases. This prevents false positives from branch names like `FIX-123`.

### Jira Examples

```bash
# Fix a Jira issue (MYPROJ must be configured)
psm fix MYPROJ-123

# Fix using alias (recommended)
psm fix mywork#123

# Feature development (works same as GitHub)
psm feature mywork add-webhooks

# Note: 'psm review' is not supported for Jira (no PR concept)
# Use 'psm fix' for Jira issues
```

### Jira CLI Setup

Install the Jira CLI:
```bash
# macOS
brew install ankitpokhrel/jira-cli/jira-cli

# Linux
# See: https://github.com/ankitpokhrel/jira-cli#installation

# Configure (interactive)
jira init
```

The Jira CLI handles authentication separately from PSM.

## Directory Structure

```
~/.psm/
├── projects.json       # Project aliases
├── sessions.json       # Active session registry
└── worktrees/          # Worktree storage
    └── <project>/
        └── <type>-<id>/
```

## Session Naming

The **public session ID** (colon form, e.g. `omc:pr-123`) is the human-facing
identifier stored in `sessions.json` and used with `psm attach`/`psm kill`. tmux
reserves `:` and `.` for its `session:window.pane` target syntax and silently
rewrites them, so the **actual tmux session name** uses a tmux-safe form where
those characters become `_` (issue #3528). PSM translates the public ID to the
tmux-safe name at every tmux boundary; attach directly with the tmux-safe name.

| Type | Public ID (`psm attach`/`kill`) | Tmux Session (`tmux attach -t`) | Worktree Dir |
|------|---------------------------------|---------------------------------|--------------|
| PR Review | `omc:pr-123` | `psm_omc_pr-123` | `~/.psm/worktrees/omc/pr-123` |
| Issue Fix | `omc:issue-42` | `psm_omc_issue-42` | `~/.psm/worktrees/omc/issue-42` |
| Feature | `omc:feat-auth` | `psm_omc_feat-auth` | `~/.psm/worktrees/omc/feat-auth` |

---

## Implementation Protocol

When the user invokes a PSM command, follow this protocol:

### Parse Arguments

Parse `{{ARGUMENTS}}` to determine:
1. **Subcommand**: review, fix, feature, list, attach, kill, cleanup, status
2. **Reference**: project#number, URL, or session ID
3. **Options**: --branch, --base, --no-claude, --no-tmux, etc.

### Subcommand: `review <ref>`

**Purpose**: Create PR review session

**Steps**:

1. **Resolve reference**:
   ```bash
   node -e "const p=require('path'),f=require('fs');try{process.stdout.write(f.readFileSync(p.join(require('os').homedir(),'.psm','projects.json'),'utf8'))}catch{console.log('{\"aliases\":{}}')}"
   ```

   Then parse the ref format (`alias#num`, `owner/repo#num`, or a URL) and extract
   `project_alias`, `repo` (owner/repo), `pr_number`, and `local_path`.

2. **Fetch PR info**:
   ```bash
   gh pr view <pr_number> --repo <repo> --json number,title,author,headRefName,baseRefName,body,files,url
   ```

3. **Ensure local repo exists**:
   ```bash
   # If local path doesn't exist, clone
   if [[ ! -d "$local_path" ]]; then
     git clone "https://github.com/$repo.git" "$local_path"
   fi
   ```

4. **Create worktree**:
   ```bash
   worktree_path="$HOME/.psm/worktrees/$project_alias/pr-$pr_number"

   # Fetch PR branch
   cd "$local_path"
   git fetch origin "pull/$pr_number/head:pr-$pr_number-review"

   # Create worktree
   git worktree add "$worktree_path" "pr-$pr_number-review"
   ```

5. **Create session metadata**:
   ```bash
   cat > "$worktree_path/.psm-session.json" << EOF
   {
     "id": "$project_alias:pr-$pr_number",
     "type": "review",
     "project": "$project_alias",
     "ref": "pr-$pr_number",
     "branch": "<head_branch>",
     "base": "<base_branch>",
     "created_at": "$(date -Iseconds)",
     "tmux_session": "psm_${project_alias}_pr-$pr_number",
     "worktree_path": "$worktree_path",
     "source_repo": "$local_path",
     "github": {
       "pr_number": $pr_number,
       "pr_title": "<title>",
       "pr_author": "<author>",
       "pr_url": "<url>"
     },
     "state": "active"
   }
   EOF
   ```

6. **Update sessions registry**:
   ```bash
   # Add to ~/.psm/sessions.json
   ```

7. **Create tmux session** (tmux-safe name; `:`/`.` are translated to `_`):
   ```bash
   tmux new-session -d -s "psm_${project_alias}_pr-$pr_number" -c "$worktree_path"
   ```

8. **Launch Claude Code** (unless --no-claude):
   ```bash
   # --dangerously-skip-permissions prevents the "Do you trust this directory?" prompt
   # and repeated tool-approval prompts from stalling the session (issue #2508).
   tmux send-keys -t "psm_${project_alias}_pr-$pr_number" "claude --dangerously-skip-permissions" Enter

   # After claude boots (PSM_CLAUDE_STARTUP_DELAY, default 5s), deliver the task.
   # Use -l (literal) so special characters are not misinterpreted by tmux.
   sleep "${PSM_CLAUDE_STARTUP_DELAY:-5}"
   tmux send-keys -t "psm_${project_alias}_pr-$pr_number" -l \
     "Review PR #$pr_number: \"$pr_title\" by @$pr_author ($head_branch → $base_branch). URL: $pr_url." Enter
   ```

9. **Output session info**:
   ```
   Session ready!

     ID: omc:pr-123
     Worktree: ~/.psm/worktrees/omc/pr-123
     Tmux: psm_omc_pr-123

   To attach: tmux attach -t psm_omc_pr-123   (or: psm attach omc:pr-123)
   ```

### Subcommand: `fix <ref>`

**Purpose**: Create issue fix session

**Steps**:

1. **Resolve reference** (same as review)

2. **Fetch issue info**:
   ```bash
   gh issue view <issue_number> --repo <repo> --json number,title,body,labels,url
   ```

3. **Create feature branch**:
   ```bash
   cd "$local_path"
   git fetch origin main
   branch_name="fix/$issue_number-$(echo "$title" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 30)"
   git checkout -b "$branch_name" origin/main
   ```

4. **Create worktree**:
   ```bash
   worktree_path="$HOME/.psm/worktrees/$project_alias/issue-$issue_number"
   git worktree add "$worktree_path" "$branch_name"
   ```

5. **Create session metadata** (similar to review, type="fix")

6. **Update registry, create tmux, launch claude**:
   Same as review, but pass issue context as the initial task prompt:
   ```bash
   tmux send-keys -t "psm_${project_alias}_issue-$issue_number" "claude --dangerously-skip-permissions" Enter
   # After claude boots, deliver the task (see PSM_CLAUDE_STARTUP_DELAY):
   tmux send-keys -t "psm_${project_alias}_issue-$issue_number" -l \
     "Fix issue #$issue_number: \"$issue_title\". URL: $issue_url. Branch: $branch_name." Enter
   ```

### Subcommand: `feature <project> <name>`

**Purpose**: Start feature development

**Steps**:

1. **Resolve project** (from alias or path)

2. **Create feature branch**:
   ```bash
   cd "$local_path"
   git fetch origin main
   branch_name="feature/$feature_name"
   git checkout -b "$branch_name" origin/main
   ```

3. **Create worktree**:
   ```bash
   worktree_path="$HOME/.psm/worktrees/$project_alias/feat-$feature_name"
   git worktree add "$worktree_path" "$branch_name"
   ```

4. **Create session, tmux, launch claude** with feature context as initial prompt:
   ```bash
   tmux send-keys -t "psm_${project_alias}_feat-$feature_name" "claude --dangerously-skip-permissions" Enter
   tmux send-keys -t "psm_${project_alias}_feat-$feature_name" -l \
     "Implement feature \"$feature_name\" for project $project. Branch: $branch_name." Enter
   ```

### Subcommand: `list [project]`

**Purpose**: List active sessions

**Steps**:

1. **Read sessions registry**:
   ```bash
   node -e "const p=require('path'),f=require('fs');try{process.stdout.write(f.readFileSync(p.join(require('os').homedir(),'.psm','sessions.json'),'utf8'))}catch{console.log('{\"sessions\":{}}')}"
   ```

2. **Check tmux sessions** (prints nothing where tmux is not installed):
   ```bash
   node -e "const{execFileSync}=require('node:child_process');let o='';try{o=execFileSync('tmux',['list-sessions','-F','#{session_name}'],{encoding:'utf8'})}catch{o=''};for(const s of o.split(/\r?\n/).map(x=>x.trim()).filter(x=>x.startsWith('psm_')))console.log(s)"
   ```

3. **Check worktrees**:
   ```bash
   node -e "const p=require('path'),f=require('fs'),b=p.join(require('os').homedir(),'.psm','worktrees');try{for(const proj of f.readdirSync(b)){for(const w of f.readdirSync(p.join(b,proj)))console.log(p.join(b,proj,w))}}catch{console.log('(no worktrees)')}"
   ```

4. **Format output**:
   ```
   Active PSM Sessions:

   ID                 | Type    | Status   | Worktree
   -------------------|---------|----------|---------------------------
   omc:pr-123        | review  | active   | ~/.psm/worktrees/omc/pr-123
   omc:issue-42      | fix     | detached | ~/.psm/worktrees/omc/issue-42
   ```

### Subcommand: `attach <session>`

**Purpose**: Attach to existing session

**Steps**:

1. **Parse session ID**: `project:type-number`

2. **Verify session exists**. First translate the public id to a tmux-safe name by
   replacing every `.` and `:` with `_`, then check it (a non-zero exit means the
   session does not exist):
   ```bash
   tmux has-session -t "psm_<tmux-safe-id>"
   ```

3. **Attach**:
   ```bash
   tmux attach -t "psm_<tmux-safe-id>"
   ```

### Subcommand: `kill <session>`

**Purpose**: Kill session and cleanup

**Steps**:

1. **Kill tmux session** using the same tmux-safe name (`.` and `:` replaced with `_`).
   A non-zero exit just means the session was already gone:
   ```bash
   tmux kill-session -t "psm_<tmux-safe-id>"
   ```

2. **Remove worktree**. Read both paths out of the registry:
   ```bash
   node -e "const p=require('path'),f=require('fs'),id=process.argv[1];const s=JSON.parse(f.readFileSync(p.join(require('os').homedir(),'.psm','sessions.json'),'utf8')).sessions[id]||{};console.log(s.worktree||'');console.log(s.source_repo||'')" "<session_id>"
   ```

   Then, with `worktree_path` and `source_repo` from those two lines:
   ```bash
   git -C "<source_repo>" worktree remove "<worktree_path>" --force
   ```

3. **Update registry**:
   ```bash
   # Remove from sessions.json
   ```

### Subcommand: `cleanup`

**Purpose**: Clean up merged PRs and closed issues

**Steps**:

1. **Read all sessions**

2. **For each PR session, check if merged**:
   ```bash
   gh pr view <pr_number> --repo <repo> --json merged,state
   ```

3. **For each issue session, check if closed**:
   ```bash
   gh issue view <issue_number> --repo <repo> --json closed,state
   ```

4. **Clean up merged/closed sessions**:
   - Kill tmux session
   - Remove worktree
   - Update registry

5. **Report**:
   ```
   Cleanup complete:
     Removed: omc:pr-123 (merged)
     Removed: omc:issue-42 (closed)
     Kept: omc:feat-auth (active)
   ```

### Subcommand: `status`

**Purpose**: Show current session info

**Steps**:

1. **Detect current session** from tmux, or fall back to checking whether the cwd sits
   inside a worktree. This prints nothing when tmux is absent or no session is attached:
   ```bash
   node -e "const{execFileSync}=require('node:child_process');try{process.stdout.write(execFileSync('tmux',['display-message','-p','#{session_name}'],{encoding:'utf8'}))}catch{}"
   ```

2. **Read session metadata**:
   ```bash
   node -e "const f=require('fs');try{process.stdout.write(f.readFileSync('.psm-session.json','utf8'))}catch{console.log('(no .psm-session.json here)')}"
   ```

3. **Show status**:
   ```
   Current Session: omc:pr-123
   Type: review
   PR: #123 - Add webhook support
   Branch: feature/webhooks
   Created: 2 hours ago
   ```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Worktree exists | Offer: attach, recreate, or abort |
| PR not found | Verify URL/number, check permissions |
| No tmux | Warn and skip session creation |
| No gh CLI | Error with install instructions |

## Teleport Command

The `omc teleport` command provides a lightweight alternative to full PSM sessions. It creates git worktrees without tmux session management — ideal for quick, isolated development.

### Usage

```bash
# Create worktree for an issue or PR
omc teleport #123
omc teleport owner/repo#123
omc teleport https://github.com/owner/repo/issues/42

# Create worktree for a feature
omc teleport my-feature

# List existing worktrees
omc teleport list

# Remove a worktree
omc teleport remove issue/my-repo-123
omc teleport remove --force feat/my-repo-my-feature
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--worktree` | Create worktree (default, kept for compatibility) | `true` |
| `--path <path>` | Custom worktree root directory | `~/Workspace/omc-worktrees/` |
| `--base <branch>` | Base branch to create from | `main` |
| `--json` | Output as JSON | `false` |

### Worktree Layout

```
~/Workspace/omc-worktrees/
├── issue/
│   └── my-repo-123/        # Issue worktrees
├── pr/
│   └── my-repo-456/        # PR review worktrees
└── feat/
    └── my-repo-my-feature/ # Feature worktrees
```

### PSM vs Teleport

| Feature | PSM | Teleport |
|---------|-----|----------|
| Git worktree | Yes | Yes |
| Tmux session | Yes | No |
| Claude Code launch | Yes | No |
| Session registry | Yes | No |
| Auto-cleanup | Yes | No |
| Project aliases | Yes | No (uses current repo) |

Use **PSM** for full managed sessions. Use **teleport** for quick worktree creation.

---

## Requirements

Required:
- `git` - Version control (with worktree support v2.5+)
- `jq` - JSON parsing
- `tmux` - Session management (optional, but recommended)

Optional (per provider):
- `gh` - GitHub CLI (for GitHub workflows)
- `jira` - Jira CLI (for Jira workflows)

## Initialization

On first run, create default config:

This creates `~/.psm/worktrees` and `~/.psm/logs`, then seeds `projects.json` and
`sessions.json` only when they do not already exist:

```bash
node -e "const p=require('path'),f=require('fs'),h=require('os').homedir(),root=p.join(h,'.psm');f.mkdirSync(p.join(root,'worktrees'),{recursive:true});f.mkdirSync(p.join(root,'logs'),{recursive:true});const projects={aliases:{omc:{repo:'Yeachan-Heo/oh-my-copilot',local:'~/Workspace/oh-my-copilot',default_base:'main'}},defaults:{worktree_root:'~/.psm/worktrees',cleanup_after_days:14,auto_cleanup_merged:true}};const sessions={version:1,sessions:{},stats:{total_created:0,total_cleaned:0}};for(const[name,value]of [['projects.json',projects],['sessions.json',sessions]]){const t=p.join(root,name);if(f.existsSync(t)){console.log('Kept existing '+t)}else{f.writeFileSync(t,JSON.stringify(value,null,2));console.log('Created '+t)}}"
```
