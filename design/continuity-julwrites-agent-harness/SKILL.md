---
name: continuity
description: Manage session continuity (Ledgers and Handoffs). Use this to save state before clearing context or ending a session.
---

# Continuity System

Use this skill to manage long-term memory artifacts.

### Create a Ledger (In-Session State)
Save the current state of your work before clearing context.
```bash
python3 scripts/continuity.py ledger create "Title of work" "Description of current state, working files, and next steps"
```

### Create a Handoff (Between-Session State)
Create a summary for the next session/agent.
```bash
python3 scripts/continuity.py handoff create "Title of handoff" "Summary of what was done, what is left, and key decisions"
```

### Read Latest
Retrieve the most recent context.
```bash
python3 scripts/continuity.py ledger read-latest
python3 scripts/continuity.py handoff read-latest
```
