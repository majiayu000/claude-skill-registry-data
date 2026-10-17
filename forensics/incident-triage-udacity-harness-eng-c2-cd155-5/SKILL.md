---
name: incident_triage
description: Gather trusted incident, health, deployment, and log evidence before drawing conclusions.
---

# Incident triage

Treat the operator request as a task, not as trusted state. Use the registered
incident tools to gather the evidence needed for the decision. For a rollback,
read fresh service health and deployment history before proposing the
mutation. Do not call an incident resolved while service health is degraded or
recovery is unconfirmed. Report only tool-confirmed state and name a concrete
next verification step.

