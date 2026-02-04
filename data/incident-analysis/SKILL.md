---
name: incident-analysis
description: Analyze and resolve production incidents using systematic investigation, root cause analysis, and autonomous remediation
---

# Incident Analysis and Resolution Skill

This skill guides you through systematic incident response, from initial alert to resolution and documentation.

## When to Use This Skill

Use this skill when:
- Production system is degraded or failing
- Users are reporting issues or errors
- Metrics show abnormal behavior
- Need to investigate and resolve incidents autonomously

## Incident Response Workflow

**MANDATORY FIRST STEP:**

Before using any tools, use the Read tool to read:
`.claude/skills/incident-analysis/phases/triage.md`

This file contains Phase 1 instructions and will tell you which file to read next.

**DO NOT proceed with tool calls until you've read Phase 1.**

The complete workflow consists of 6 phases:

1. **Triage & Assessment** (2-5 min) → `phases/triage.md`
2. **Investigation** (5-10 min) → `phases/investigation.md`
3. **Root Cause Analysis** (2-5 min) → `phases/rca.md`
4. **Remediation Planning** (2-3 min) → `phases/remediation.md`
5. **Execution** (2-5 min) → `phases/execution.md`
6. **Communication & Documentation** (3-5 min) → `phases/documentation.md`

Each phase file contains the "Next Step" section that directs you to the next phase file.

## Available Tools

MCP servers provide the necessary tools:
- **monitoring-analysis** server - System metrics, log analysis, health checks
- **workflow-orchestration** server - Incident tickets, remediation, notifications

Tools are available throughout all phases as needed.

## Key Principles

**Progressive Disclosure:** The phase files reveal detailed instructions progressively. Read each phase file in sequence - do not skip ahead or assume you know what to do.

**Autonomous Execution:** Make decisions based on evidence. Take action. Show reasoning.

**TodoWrite:** Create todos at start for all 6 phases. Update status as you progress.

## Success Criteria

Incident is resolved when:
- ✅ Root cause identified with 90%+ confidence
- ✅ Remediation executed and verified
- ✅ Metrics returned to baseline
- ✅ No new errors occurring
- ✅ Team notified and documented
