---
name: incident-response
description: This skill should be used when the user mentions "postmortem", "incident", "root cause analysis", "blameless", "severity", "SEV1", "on-call", "RCA", or "outage", or is writing up an incident. It provides a blameless postmortem methodology, a severity model, and reliability metric definitions.
---

# Incident Response and Blameless Postmortems

## Purpose
A consistent, blameless methodology for writing incident postmortems and classifying severity, so writeups drive systemic fixes instead of finger-pointing. This is incident-management domain knowledge (structure, blameless framing, severity, metrics), applied uniformly every time.

## The blameless principle
Analyze **systems and processes, never individuals**. People act rationally given the information and tools they had; if a human error caused harm, the real finding is the missing guardrail that let it. This is not about avoiding accountability, it's that blame suppresses the honest disclosure you need to actually fix the system.

**Reframe every human-error statement:**
| Blameful (reject) | Blameless (use) |
|-------------------|-----------------|
| "X pushed a bad config" | "the change reached prod because no test covered this path" |
| "on-call was slow" | "the alert didn't page; ack took N minutes" |
| "someone ran the wrong command" | "the safe and destructive commands were indistinguishable" |

## Postmortem structure (standard sections)
1. **Summary**: 2-3 sentences: what broke, blast radius, duration.
2. **Impact**: users affected, duration, severity, SLO/error-budget burn.
3. **Timeline (UTC)**: detection → mitigation → resolution, each entry evidence-cited.
4. **Root Cause / Contributing Factors**: multiple systemic factors, not one scapegoat.
5. **What went well / what went poorly**: specific and honest.
6. **Action items**: owner + due date + type (preventive / detective).
7. **Lessons learned**: durable takeaways.

## Timeline discipline
- Normalize **all** timestamps to UTC; note any timezone assumption.
- Mark the phase transitions explicitly: incident begin, **detection**, escalation, **mitigation**, **resolution**.
- Cite a source for every entry (alert, log line, chat timestamp, deploy record). Never invent a time, mark gaps `[unknown, needs follow-up]`.

## Action item quality
Each item: maps to a contributing factor, has an **owner** (role/team) and a **due date**, and is classified:
- **Preventive**: removes the failure mode (test, guardrail, config default).
- **Detective**: catches it faster next time (alert, dashboard, probe).
Avoid vague items ("be more careful"); every item must be verifiable as done.

## Additional Resources
### Reference Files
For the full template and a worked example, consult:
- **`references/postmortem-template.md`**: the complete fill-in template plus a fully worked example incident writeup.

For the severity model and metrics, consult:
- **`references/severity-levels.md`**: SEV1-SEV4 definitions, escalation paths, on-call communication norms, and the MTTR/MTTD/MTBF metric definitions.
