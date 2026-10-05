---
name: eng-runbook
description: |
  Engineering runbook / incident response guide with step-by-step procedures,
  code snippets, and severity indicators. Use for "runbook", "incident response",
  "SOP", "playbook".
triggers:
  - "runbook"
  - "incident response"
  - "sop"
  - "playbook"
  - "procedure"
  - "troubleshooting"
df:
  mode: document
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Engineering Runbook Skill

Produce an engineering runbook page.

## Structure
1. **Header**: runbook title, last updated, owner, severity level badge.
2. **Overview**: when to use this runbook, expected outcome, time estimate.
3. **Prerequisites**: tools, permissions, access required.
4. **Steps**: numbered list. Each step:
   - Action description.
   - Code block or command (copyable).
   - Expected output / validation.
   - Rollback command if applicable.
5. **Escalation**: who to contact if steps fail.
6. **Appendix**: related runbooks, logs locations, dashboards.

## Rules
- Severity badges: P1=red, P2=orange, P3=yellow, P4=gray.
- Code blocks: dark background, syntax highlight via CSS classes.
- Steps are numbered, never bulleted.
- `data-df-id` on each step.

## Output
Single `index.html`, inline CSS.
