---
name: project-creation
description: Create new project YAML files for the POS. Use when creating a new project, initializing project tracking, or when user mentions "new project", "start project", or "create project".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Project Creation Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Create and initialize new projects with full setup.

## Commands

- `/project create {team} {name}` - Create a new project
- `/project list {team}` - List team projects
- `/project status {team} {project}` - Show project status

## `/project create {team} {name}`

**Required:** Team name, project name (kebab-case), description, type (internal/client), tech stack, priority, git remote.

### Steps

1. **Validate team:** `ls {teams_dir}/{team}/team.yaml`
2. **Clone or init repo** in `{teams_dir}/{team}/repos/`
3. **Create project directory:** `mkdir -p {teams_dir}/{team}/projects/{name}/{plans,reviews,logs}`
4. **Create project YAML** at `{teams_dir}/{team}/projects/{name}.yaml`:
   ```yaml
   name: "{name}"
   description: "{description}"
   type: internal | client
   team: "{team}"
   workspace: "{teams_dir}/{team}/repos/{name}"
   status: new  # new | planning | active | review | complete | on_hold
   priority: medium
   created: "{today}"
   repository:
     host: gitlab.example.com
     path: "{gitlab_path}"
     active_branch: main
   deployment:
     platform: ""  # e.g., dokploy, vercel, railway
     project_id: ""
     services: []
   requirements: []
   acceptance_criteria: []
   history:
     - date: "{today}"
       action: "Project created"
       by: cto
   ```
5. **Add to platform registry** - Edit `pos.yaml` under `teams.{team}.repos`
6. **Update team config** - Add to `active_projects` in `team.yaml`, assign port
7. **Generate PROJECT_INDEX.yaml:** `./scripts/generate-project-index.sh {name} {team}`
8. **Optional:** Create initial sprint in `plans/sprints/`

### Status Flow

```
new -> planning -> active -> review -> complete
         |
       on_hold
```

## Output

Report: project file path, repo location, GitLab URL, files created, next steps (clone repo, create sprint, start session).

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
