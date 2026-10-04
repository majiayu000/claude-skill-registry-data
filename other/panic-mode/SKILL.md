---
name: panic-mode
description: Triages a live incident — stop the bleeding first, smallest safe fix next, post-mortem once stable; invoke via /panic-mode when something is on fire in production and you need to restore service before understanding everything.
---

# Panic Mode

Something is on fire and users are watching. This mode does not start with root-cause philosophy — it stops the bleeding, restores service with the smallest safe move, and saves the post-mortem for after the building is no longer burning.

## When to use
- A live incident: prod is down, degraded, or actively harming users.
- You need to restore service first and understand it fully later.

## Behavior
1. Assess blast radius immediately: what's broken, who's affected, how bad, and is it getting worse.
2. Stop the bleeding first — roll back, disable the feature, flip the flag, or throttle, whichever restores service fastest and safest.
3. Prefer mitigation over root-cause heroics while users are impacted; a clean fix can wait until things are stable.
4. Apply the smallest reversible change that restores service; avoid risky compound fixes mid-incident.
5. Communicate status crisply: what's happening, what you did, current state, next step.
6. Once stable, capture the timeline while it's fresh.
7. Only then move to true root cause and a durable fix, plus a prevention note.

## Output
Service restored via the safest mitigation, a crisp status line, an incident timeline, and a follow-up root-cause + prevention plan for once things are calm.
