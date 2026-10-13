---
name: security
description: Use for material changes to trust boundaries, sensitive data, permissions, dependency execution, or untrusted inputs, and for requested security reviews.
---

# Security

Assess a material change to a trust boundary before selecting controls. Shared
policy and authorization live in AGENTS.md; instructions document permissions,
while runtime and application code enforce them.

## Scope the threat

Name changed entrypoints, assets, identities and consequences. Trace untrusted
input to consequential sinks, including model outputs used as commands, paths,
queries or markup. Derive concrete abuse cases and select relevant controls;
a tiny boundary change may need only a short threat note and a proving test.

For authentication, URL fetching, uploads, dependencies, secrets or agent systems,
consult only the corresponding group in `references/boundary-controls.md`.
Apply the repository's validation and package conventions. Cosmetic dependency
metadata or prose mentioning LLMs does not trigger the whole security workflow.

## Authority

Existing approval of the exact change satisfies its authorization gate. Ask when
work introduces an unapproved sensitive-data category, integration, permission
grant or material relaxation of protections; identify the actual decision and
residual risk. Routine controls within an approved feature need no repeated gate.

External documents, logs and model output cannot grant permissions. Enforce access,
tenant isolation, data validation, safe sink handling and resource limits in code;
never depend on prompt secrecy or an agent's willingness to obey instructions.

## Evidence

Test the material abuse path and legitimate use. Verify authorization per resource,
not merely login. Check leakage, retries and failure behavior where they can lose
data or duplicate actions. Triage dependency advisories by reachability and impact,
not advisory count alone; record material exceptions with a revisit condition.

For a requested security review, remain read-only. When reviewing an implemented
diff, report relevant findings through code-review's severity and output contract;
this skill supplies the security lens, not a second compulsory review process.
