---
name: hadriansecurity--openhack
description: "Whitebox security review agent — checkpointed pentest workflow: recon → scenario routing → expert agents (12 OWASP families) → triage → findings. Runs inside Claude Code, Codex, or Cursor."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Whitebox pentest workflow from Hadrian Security. Checkpointed, file-based state.

## Quick start

```bash
# Install
pip install openhack

# Run against a repo
openhack init-run <target> <git-url>
```

Or simply ask the agent:
```
Initiate a whitebox pentest on https://github.com/example/app.git
```

## Flow (10 phases, human approves each)

1. `openhack init-run` — clone target, init run state
2. Select experts (12 OWASP families or subset)
3. `openhack run-recon` — surface discovery, writes routing-units.jsonl
4. `openhack create-scenarios` — router agent generates scenario backlog
5. Run scenario backlog — each scenario gets its own expert agent + evidence
6. `openhack record-scenario-result` — records finding candidates
7. `openhack render-finding-triage-prompt` — triage prompt per candidate
8. `openhack record-finding-triage` — accepted/downgraded → final findings
9. `openhack validate-run` — integrity check

## Key principle

Recon is scouting only. Do NOT begin vulnerability analysis from recon alone.
Each phase requires human approval before proceeding.

## Source

https://github.com/hadriansecurity/openhack
