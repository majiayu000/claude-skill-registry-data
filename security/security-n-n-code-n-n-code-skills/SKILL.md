---
name: security
description: Evidence-grounded threat modeling, vulnerability review, and secure implementation. Use for explicit security audits or primary risks involving authorization, untrusted input, external requests, parsers/uploads, secrets, sensitive data, isolation, or release integrity. Not for routine implementation or non-security red-teaming. Add `security-identity-access` for identity and tenant authorization.
---

# Security

Find and reduce realistic abuse paths while keeping evidence, authority, and
side effects explicit.

Compose with `security-identity-access` when identity or tenant-authorization
boundaries are central. That companion owns identity-specific checks; this
skill owns the shared investigation, safety, evidence, and reporting contract.

## Choose The Mode And Authority

| Mode | Use when | Authority |
|---|---|---|
| `security review` | Determine whether concrete code, configuration, or a change creates security-relevant weaknesses or unsafe exposures | Read-only: do not edit source or configuration or change external state |
| `threat model` | Map assets, boundaries, attacker goals, abuse paths, and mitigations | Read-only: do not edit the system or present scenarios as confirmed vulnerabilities |
| `secure implementation` | Design, implement, or remediate security-sensitive behavior | Mutate only the files or systems explicitly authorized by the request |

Writing an explicitly requested report does not authorize remediation. If a
request combines analysis and implementation, keep the initial investigation
read-only and make the transition to changes visible.

## Shared Workflow

1. **Set scope and assumptions.** Identify the mode, target paths and
   environments, protected assets, plausible attacker capabilities, deployment
   shape, and relevant authorization assumptions. Inspect discoverable context
   before asking questions; ask only when an answer would materially change
   scope, authority, or ranking.
2. **Map the system.** Trace entrypoints, data flows, trust boundaries,
   authoritative controls, storage, external integrations, and observable
   effects. Follow a path across all participating components rather than
   stopping at a frontend, handler, or risky-looking call.
3. **Choose high-value hypotheses.** Derive a small set of abuse paths from the
   actual architecture and attacker goals. Prioritize paths involving authority,
   isolation, code or query execution, external resource access, dangerous
   parsing, sensitive data, or resource exhaustion when those surfaces exist.
4. **Trace each hypothesis.** Establish input provenance, transformations,
   guards, reachability, attacker prerequisites, sink behavior, and concrete
   impact. Check middleware order, authorization placement, schemas,
   parameterization, encoding, and configuration already in effect. A risky API,
   scanner alert, or pattern match is a lead, not a finding.
5. **Verify material protections.** When a conclusion depends on a framework,
   runtime, or library default, identify the resolved dependency and effective
   configuration, then verify the behavior using matching authoritative
   documentation, source, or a minimal safe reproduction. If that evidence is
   unavailable, classify the path as needing validation rather than assuming
   either safety or vulnerability.
6. **Classify, act, and report.** Use the evidence outcomes below, stay within
   the selected mode, and produce its required output.

Separate runtime, development, test, build, and pipeline risk. Include
dependencies, build scripts, generated artifacts, provenance, or CI only when
the user scopes them in or concrete repository evidence places that surface on
the relevant abuse path or trust boundary. Rank it by control of shipped
artifacts, deployment credentials, or release integrity. Verify an advisory
against the resolved dependency and applicable capability before treating it
as a finding.

## Safe Validation Boundary

A security request authorizes inspection of the supplied or otherwise in-scope
materials. It does not by itself authorize probing deployed services, accounts,
networks, or third parties.

Run repository-supported local checks and non-destructive synthetic regression
cases in an authorized isolated harness. Crafted requests, endpoint scanning,
fuzzing, exploit proofs, or other active validation against a shared or
deployed target require authorization for the exact target and method and must
remain non-destructive.

Prefer isolated local or test targets, synthetic data, least-privileged test
accounts, bounded requests, and reversible observations. Do not access or
disclose real data, capture credentials, establish persistence, send real
messages, incur material cost, impair availability, or cross the authorized
boundary. Access or credentials alone are not authorization. If adequate proof
would exceed this boundary, stop at the strongest safe evidence and record the
exact missing fact or next authorized test.

## Evidence Outcomes

Use these outcomes for review conclusions:

| Outcome | Meaning |
|---|---|
| `confirmed finding` | Evidence supports an attacker-reachable or attacker-influenceable condition, a realistic abuse path, and security-relevant impact after existing protections are considered |
| `needs validation` | A credible, material path remains but reachability, configuration, deployment, or protection evidence is missing |
| `not supported` | Examined evidence refutes the suspected path in the effective configuration |
| `coverage gap` | A material surface could not be examined, but no specific vulnerability is established |

Code, configuration, or runtime evidence can confirm a path without a working
exploit when it establishes the condition, reachability, prerequisites, and
impact. Do not make an exploit proof a universal reporting gate.

Do not suppress a credible concern merely because it is not yet a confirmed
finding. Preserve it under `needs validation` with the missing evidence and
safest discriminating probe.

Report severity and confidence independently. Severity reflects impact,
exploit prerequisites, and affected scope if the path is real; confidence
reflects the strength and completeness of the evidence. For an unresolved path,
label potential severity rather than lowering severity to compensate for weak
confidence. Do not assign CVSS or another numeric score unless requested and
the required deployment evidence is available.

If no findings are confirmed, say **No confirmed findings in the examined
scope** and state coverage, limitations, and residual checks. Do not translate
limited review evidence into “secure” or “no vulnerabilities.”

Threat-model abuse paths are scenarios rather than findings. Rank them by
impact and likelihood under explicit assumptions, and say what evidence would
confirm or reduce each risk.

## Implementation Decisions

Tie each security change to an evidenced abuse path or explicit security
requirement. Fix the problem at the authoritative boundary and prefer
server-enforced access decisions, structured or parameterized APIs,
context-correct encoding, explicit resource bounds, least privilege, and
fail-closed behavior where a security decision cannot be made safely.

Preserve intended behavior deliberately. State any compatibility, usability,
operational, or performance tradeoff instead of hiding it behind “hardening.”
Do not add generic defenses or dependencies without a concrete ownership and
maintenance reason.

Treat suspected secrets carefully:

- do not reproduce secret values in findings, logs, commands, patches, or test
  fixtures
- distinguish credentials and private key material from public identifiers and
  non-secret configuration
- keep plaintext secrets out of source, history, artifacts, process arguments,
  logs, and user-facing errors
- use the deployment's approved secret store or injection mechanism with
  appropriate access control and rotation; environment variables are one
  delivery mechanism, not a universal secret store or safety guarantee
- when exposure is plausible, recommend revocation or rotation as appropriate;
  deleting a value from the current file does not invalidate it or remove
  earlier copies
- treat revocation or rotation as primary containment; rewriting shared history
  requires separate authorization and coordination

## Output By Mode

For a `security review`, report:

1. confirmed findings first, ordered by severity
2. needs-validation items, ordered by potential impact
3. meaningful not-supported dispositions when they resolve a likely false
   positive
4. examined scope, coverage gaps, validation performed, and residual risk

Each confirmed finding or needs-validation item includes:

- outcome, severity or potential severity, and confidence
- impacted asset or trust boundary
- required attacker capability and prerequisites
- evidence trace with concrete source references
- impact
- fix direction or discriminating validation step, including behavior
  tradeoffs

For a `threat model`, report:

- scope, system assumptions, assets, actors, and trust boundaries
- a small ranked set of abuse paths with prerequisites, impact, relevant
  existing controls, and current disposition when one has been decided
- mitigations tied to owning components or boundaries
- residual risks, open questions, and assumptions that would change ranking

For `secure implementation`, report:

- the abuse path or requirement addressed and changed scope
- the control added or revised and relevant behavior tradeoffs
- exact validation evidence
- unresolved risks, unrun checks, and rollback or follow-up needs when relevant

## Validate Fixes Proportionally

Validate the changed boundary, the closest safe abuse case, and the legitimate
behavior that must continue to work. Add or update a focused regression when it
materially protects the boundary and lies within the requested scope, then run
the narrowest relevant repository checks.

Broaden validation when the change affects shared authorization, parsers,
security primitives, framework configuration, dependencies, or multiple trust
boundaries. Keep active checks within the safe-validation contract. Record exact
commands or fixtures, observed outcomes, and anything not run. Do not claim a
finding is fixed solely because the patch appears correct.
