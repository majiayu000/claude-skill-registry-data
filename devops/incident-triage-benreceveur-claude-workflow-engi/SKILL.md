---
name: incident-triage
description: Faster on-call handoffs and better postmortems with triage SOPs
version: 1.0.0
tags: [incidents, triage, on-call, postmortem]
---

# Incident Triage Skill

## Purpose
Streamline incident response with SOPs, indicator extraction, and memory-backed timelines.

## Process
1. Apply triage SOP from SKILL.md
2. Extract indicators from logs (via extract_indicators.py)
3. Escalate per matrix in references/escalation_matrix.md
4. Write timeline to memory with TTL (30 days)
5. Generate postmortem template

## Scripts
- `extract_indicators.py`: Pull signals from logs
- `generate_timeline.py`: Create incident timeline

## Memory Integration
Incidents auto-expire after 30 days via TTL.

*Incident Triage v1.0.0*
