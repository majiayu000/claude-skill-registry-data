---
name: review-prompt-injection
description: Review direct and indirect prompt-injection exposure in LLM, RAG, multimodal, copilot, and agentic applications through architecture inspection, code and configuration review, and authorized controlled probes. Use when assessing instruction hierarchy, untrusted-content channels, system-prompt or data leakage, unsafe tool influence, injection defenses, or a reported prompt-injection weakness.
---

# Review Prompt Injection

Trace whether untrusted content can alter privileged instructions or cause a security-relevant consequence. Prove complete paths rather than counting model refusals.

Read [methodology](references/methodology.md) before selecting channels, probes, or framework mappings.

## Safety boundaries

- Obtain explicit authorization before sending active probes to any deployed target.
- Use a local, staging, or isolated test environment whenever a tool, write, message, purchase, publication, deletion, or external request could occur.
- Use synthetic canaries and dummy records; never place real secrets in prompts to test whether they leak.
- Disable or stub side-effecting tools and cap requests, tokens, concurrency, and cost.
- Do not bypass access controls, access another tenant, persist poisoned content, or test a third party without separate authorization.
- Stop and preserve evidence if a probe causes an unexpected side effect or reveals real sensitive data.

## Workflow

1. **Define success and harm.** Record scope, authorization, environment, allowed channels, rate limits, stop conditions, expected instruction hierarchy, protected data, privileged actions, and security-relevant failure conditions.
2. **Fingerprint the target.** Record application revision, model and snapshot, prompts, decoding settings, retrieval state, tool manifests, guardrail versions, identity, and date. Do not compare runs with untracked changes.
3. **Map instruction channels.** Trace direct user input, uploaded files, images, retrieved documents, web or email content, tool results, memory, inter-agent messages, metadata, and downstream model output. Mark each channel's trust level and privilege.
4. **Review controls.** Inspect instruction separation, content provenance, data and action authorization, output validation, tool argument validation, least privilege, confirmation gates, egress controls, logging, and recovery paths.
5. **Build paired cases.** Pair each attack case with a benign task using the same channel and business intent. Use a synthetic canary or harmless no-op to identify instruction override, disclosure, unauthorized action, or persistence.
6. **Run controlled trials.** Preserve exact inputs, rendered prompts when available, retrieved chunks, outputs, tool traces, model settings, timestamps, and trial counts. Repeat nondeterministic cases and retain all outcomes.
7. **Confirm the consequence.** Distinguish jailbreak, prompt injection, disclosure, and unsafe action. Report a vulnerability only when the observed behavior crosses a defined security boundary or materially weakens a control.
8. **Recommend and regress.** Prefer authorization and isolation controls over prompt wording alone. Add a minimal failing case, a benign paired case, and an expected post-fix outcome.

## Evidence rules

- Store exact test-case IDs and immutable target fingerprints.
- Preserve raw request, response, retrieval, and tool artifacts when authorized; otherwise preserve a redacted hash-linked record.
- Record every trial, including refusals and inconsistent outcomes.
- Separate `confirmed`, `likely`, `inconclusive`, `not reproduced`, and `not tested`.
- Require a boundary, consequence, evidence reference, and reproduction rate for every finding.
- Do not expose system prompts, personal data, credentials, or working exploit details beyond the authorized audience.

## Output contract

Return:

1. Scope, authorization, target fingerprint, stop conditions, and limitations.
2. Instruction-channel and trust-boundary map.
3. Control review with source locations and effective privilege.
4. Test matrix with case ID, channel, precondition, payload intent, benign pair, expected result, trials, observed result, and evidence.
5. Findings with full attack path, consequence, reproducibility, severity, confidence, and minimal redacted reproduction.
6. Layered remediation plan and regression cases.
7. Explicit unknown, not-tested, and out-of-scope sections.

Write each finding as: `ID | injection class | affected channel | preconditions | violated boundary | security consequence | trials and success rate | evidence | severity | confidence | remediation | regression | framework mapping`.

## Quality gate

Do not finalize until:

- Every active probe is authorized and every side effect is isolated or stubbed.
- Every finding shows more than undesirable text; it shows a defined boundary or control failure.
- Exact target versions and every trial outcome are recorded.
- Benign paired cases verify that proposed controls preserve intended utility.
- Prompt-only mitigations are not presented as complete when authorization, isolation, or output controls are missing.
- Direct, indirect, stored, multimodal, retrieval, memory, and tool-output channels are marked tested, not tested, or not applicable.
- Sensitive evidence is redacted without destroying reproducibility.
