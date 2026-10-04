---
name: team-management
description: Create and manage teams in the POS. Use when creating a new team, adding engineers to a team, or when user mentions "new team", "create team", "add team", or "team setup".
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Team Management Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Manage teams in the POS. Teams are organizational units led by TPMs.

## Commands

- `/team create {name}` - Create a new team with full setup
- `/team list` - List all teams
- `/team status {name}` - Show team status
- `/team add-engineer {team} {specialty}` - Add engineer to team

## `/team create {name}` - Full Setup

**Required Information:** Team name (kebab-case), description, focus areas, tech stack, port range, engineer specialties.

### Steps

1. **Create directory structure**
   ```bash
   mkdir -p {teams_dir}/{team-name}/{repos,plans/sprints,logs,projects,docs}
   ```

2. **Create team.yaml** at `{teams_dir}/{team}/team.yaml`:
   ```yaml
   name: "{team-name}"
   tpm: tpm-{team-name}
   description: "{description}"
   client:
     name: "{Client or Internal}"
     type: internal_product
   focus_areas: [...]
   tech_stack:
     backend: {framework}
     frontend: {framework}
     database: {db}
   engineers: [eng-backend, eng-frontend, eng-testing, eng-devops]
   active_projects: []
   ports:
     range: "8X00-8X99 (backend), 3X00-3X99 (frontend)"
   created: "{today}"
   ```

3. **Create status.yaml** at `{teams_dir}/{team}/status.yaml` with `session_active: false`, empty task/blockers/sprints.

4. **Create QUICK-START.md** with team name, TPM, focus, quick commands, key file paths, tech stack.

5. **Add to platform registry** - Edit `pos.yaml` with team entry under `teams:`.

6. **Create TPM agent** at `.ai/agents/tpm-{team-name}.md` with responsibilities (planning, coordination, quality, communication), available engineers, and workflow (receive assignment, create plan, execute after approval, report).

7. **Run agent linking**:
   ```bash
   ./scripts/link-team-agents.sh
   ```
   Restart Claude Code after linking.

## Team-Specific Engineers

Create in `.ai/agents/teams/{team-name}/` then run `./scripts/link-team-agents.sh`.

## Available Engineer Specialties

| Specialty | Use For |
|-----------|---------|
| eng-backend | APIs, services, databases, business logic |
| eng-frontend | UI, components, state management, UX |
| eng-testing | Tests, coverage, quality assurance |
| eng-devops | CI/CD, deployment, infrastructure |
| eng-security | Audits, vulnerability fixes, compliance |

## Status Flow

```
new -> planning -> active -> review -> complete
         |
       on_hold
```

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
