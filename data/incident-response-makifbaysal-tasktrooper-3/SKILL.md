---
name: incident-response
category: operations
description: How to work a production incident remediation task. Use when the task title starts with "Incident:" or its description carries an incident id and a suggest/auto_fix policy.
---
# Incident response

A task titled `Incident: …` is a live production problem, assigned to you by the system. Its description carries an **incident id** and a first-pass hypothesis produced by the rules engine, plus the policy in force (`suggest` or `auto_fix`). That hypothesis is a starting point, not a verdict.

## Order of work

1. **Read the incident first.** `get_incident` with the id from the task description: raw alert payload, timeline, occurrence count, current remedy hypothesis.
2. **Correlate with the tools you hold.** `get_environment` for the affected environment (provider, health URL, binding status), then `list_deployments` — "what changed?" answers most incidents. `list_runtime_errors` with `new: true` tells you whether the error group started with the most recent deploy. `query_runtime_logs` with `text:` set to the error reads what the running service actually did.
3. **Classify.** Config/credentials, dependency, capacity, or code defect. The classes need different fixes, and guessing the class wrong wastes the whole investigation.
4. **Write the remedy.** `propose_incident_remedy` with a summary (root cause + fix), concrete steps — each as *command → expected output → if it fails: …* — the evidence you relied on, and an honest confidence. Set `rollback: true` when "redeploy the last good release" is the fix: you hold no rollback tool yourself, so under `suggest` the human decides from this proposal and under `auto_fix` the release engineer acts on it. If you are not sure, say so with a low confidence and name what you would need to check next — an honest "here is what I would check" is useful; a confident guess is not.
5. **Act per policy.**
   - **suggest** (default): do NOT change production code. The proposal is the deliverable — move the task to `human_uat` with no code change and say in your closing message that the remedy awaits a human decision.
   - **auto_fix**: implement the remedy and take it through the normal pipeline — TDD, the standing acceptance criteria, all of it. A hotfix that skips them causes the next incident.
6. **Resolve only after verifying recovery.** `resolve_incident` only after `get_environment` / `list_runtime_errors` show the environment is actually healthy again, with the note naming that evidence. Never mark an incident resolved because you shipped a fix — shipping and recovering are different facts.

## Rules

- A recurring incident (occurrences > 1, or a prior resolved incident with the same fingerprint) means the previous fix did not hold: fix the cause, not the symptom, and say explicitly why this time is different.
- Never write a remedy you cannot execute step by step. "Investigate the database" is not a remedy; "connection pool is capped at 10 while the new worker opens 25 — raise `DB_MAX_CONNS` to 40 in the prod config" is.
- If the incident payload is not enough to conclude anything, say what specific log, metric or access you need. Do not invent a cause to have something to write.
