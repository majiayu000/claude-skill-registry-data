---
name: debug-incident
description: "Investigate a defect or production incident with hypotheses, tracing, safe reproduction and regression tests."
---

# Incident/defect playbook
- Determine actual user impact, onset, environment, change timeline, identifiers and reproducibility without collecting secrets.
- Form falsifiable hypotheses; read logs/traces/metrics, reproduce in safe environment and narrow causal code path.
- For urgent production incidents prioritize containment/reversible rollback; do not execute prod commands without approval.
- Fix root cause with smallest change and new regression test; review side effects, consistency and potential historical data repair.
- Finish with symptom→root cause→evidence→fix→tests→deployment monitoring→follow-up prevention.
