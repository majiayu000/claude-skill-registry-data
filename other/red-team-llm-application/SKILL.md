---
name: red-team-llm-application
description: Design, execute, and report authorized adversarial security tests for complete LLM applications, including model interfaces, prompts, retrieval, tools, output consumers, identities, and monitoring. Use for pre-release red teams, security regression campaigns, control validation, incident reproduction, or risk-driven testing that spans multiple AI attack classes rather than a prompt-injection-only review.
---

# Red Team an LLM Application

Run a bounded, hypothesis-led campaign against the application as deployed. Measure security consequences, control performance, and benign utility with reproducible evidence.

Read [methodology](references/methodology.md) before writing a campaign charter or test matrix.

## Safety boundaries

- Require explicit authorization naming the target, environment, identities, dates, permitted techniques, data rules, rate limits, and emergency contacts.
- Refuse active testing when ownership or authorization remains ambiguous.
- Prefer isolated test tenants, synthetic data, sandboxed tools, no-op destinations, and reversible state.
- Exclude denial of service, uncontrolled cost generation, real credential collection, real data exfiltration, malware deployment, social engineering of uninvolved people, and third-party testing unless separately authorized.
- Define automatic stop conditions for sensitive-data exposure, unexpected external effects, instability, budget limits, and monitoring loss.
- Preserve evidence and notify the named contact immediately after a stop condition; do not continue to improve the exploit.

## Workflow

1. **Write the charter.** Record objectives, threat actors, target and exclusions, environment, authorization, allowed techniques, data handling, communications, rate and cost limits, stop conditions, and evidence retention.
2. **Fingerprint the application.** Pin code revision, model and snapshot, prompt hashes, decoding settings, retrieval corpus or snapshot, tool and guardrail versions, identity, infrastructure, and test date.
3. **Model the attack surface.** Trace all inputs, prompt layers, retrieval paths, output consumers, tool calls, state and memory, identities, integrations, and monitoring controls.
4. **Select hypotheses.** Derive security hypotheses from the threat model and observed architecture. Cover applicable instruction manipulation, data disclosure, unsafe output handling, poisoning or dependency trust, authorization and agency, cross-tenant isolation, resource abuse, and detection or recovery failure.
5. **Design paired cases.** Give every adversarial case a clear precondition, harmless payload intent, expected secure result, measurable failure condition, benign control, cleanup step, and evidence plan.
6. **Run in stages.** Start with dry runs and stubs, then single-component tests, then approved end-to-end chains. Stop at the first sufficient proof of impact.
7. **Capture all trials.** Record exact inputs, outputs, retrieval context, tool traces, state changes, alerts, latency, token or cost use, timestamps, and cleanup results. Preserve successes and failures.
8. **Triage and reproduce.** Remove duplicates, distinguish model behavior from application vulnerability, repeat nondeterministic results, minimize the reproduction, and assign severity and confidence using declared criteria.
9. **Verify treatment.** Recommend defense-in-depth changes and convert confirmed cases plus benign controls into release-blocking regression tests.

## Evidence rules

- Use immutable case IDs and evidence IDs.
- Hash or version every mutable target component and test corpus.
- Preserve raw artifacts only within authorized handling rules; redact secrets and sensitive content in reports.
- Record every comparable trial before calculating a success rate.
- Separate `confirmed`, `partially confirmed`, `inconclusive`, `not reproduced`, `not tested`, and `not applicable`.
- Require an observed security consequence or materially failed control for a finding.
- Record cleanup evidence for every test that changes state.

## Output contract

Return:

1. Signed-off scope and rules-of-engagement summary.
2. Target fingerprint and attack-surface diagram.
3. Risk-to-test coverage matrix.
4. Case ledger with hypotheses, paired benign controls, results, all trials, evidence, and cleanup.
5. Findings with minimal reproduction, attack chain, affected asset, severity, confidence, and detection outcome.
6. Control scorecard covering prevention, authorization, containment, detection, response, and benign utility.
7. Prioritized remediation and machine-readable regression cases.
8. Limitations, unknowns, untested paths, and residual risk.

Write each finding as: `ID | hypothesis | preconditions | attack chain | security consequence | affected asset | trials and reproduction rate | evidence | severity | confidence | detection | cleanup | remediation | regression | framework mapping`.

## Quality gate

Do not finalize until:

- The authorization and stop conditions cover every executed technique.
- The target fingerprint makes results reproducible and comparable.
- Every finding shows application-level impact, not merely surprising model text.
- Every test has a benign control, expected result, and cleanup status.
- Every executed trial is represented in the evidence ledger.
- High-risk chains stop at sufficient proof and avoid unnecessary impact.
- Coverage gaps and nondeterministic behavior remain visible.
- Retesting verifies both security improvement and intended-function preservation.
