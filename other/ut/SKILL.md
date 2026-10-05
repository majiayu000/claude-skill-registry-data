---
name: ut
description: Show UltraThink system status, available skills, hooks, and configuration
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# UltraThink Status

Show the current UltraThink system status. Run these checks and present a summary:

## 1. Skill Count

Count skills in `~/.claude/skills/`:

```bash
ls -d ~/.claude/skills/*/SKILL.md 2>/dev/null | wc -l
```

## 2. Registry Status

Check the registry:

```bash
node -e "const r=JSON.parse(require('fs').readFileSync(require('os').homedir()+'/.claude/skills/_registry.json'));const l={};r.skills.forEach(s=>{l[s.layer]=(l[s.layer]||0)+1});console.log('Total:',r.skills.length);console.log(JSON.stringify(l))" 2>/dev/null
```

## 3. References (behavioral rules)

```bash
ls ~/.claude/references/*.md 2>/dev/null
```

## 4. Agents

```bash
ls ~/.claude/agents/*.md 2>/dev/null
```

## 5. Hooks

```bash
ls ~/.claude/hooks/ 2>/dev/null
```

## 6. Dashboard Status

```bash
lsof -i :3333 2>/dev/null | head -2
```

## 7. Database Connection

Check if DATABASE_URL is set and reachable (don't print the actual URL):

```bash
if [ -f ~/Documents/GitHub/InuVerse/ai-agents/ultrathink/.env ]; then echo ".env file: exists"; else echo ".env file: missing"; fi
```

## Output Format

Present results as a status dashboard:

```
UltraThink Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Skills:     X total (Y orchestrators, Z hubs, ...)
Rules:      X loaded
Agents:     X defined
Hooks:      X active
Dashboard:  running / stopped
Database:   configured / not configured

Available commands:
  /dashboard    Start the web dashboard
  /ut           This status view
  /ut-skills    Search/browse skills
  /ut-hooks     View hook event log
  /ut-memory    Browse memory entries
  /ut-init      Init UltraThink in current project
```
