---
name: threat-model
description: Produces a threat model — purpose, deployment, trusted inputs, untrusted inputs — for a new feature or component before it's implemented. Use when writing an implementation plan for a new API endpoint, data pipeline, agent loop, or system component. Also invoke when a plan introduces new trust boundaries, handles user-supplied data, adds authentication flows, or integrates external services.
---

# Threat Model (A06:2025)

## What this checks

This skill produces the threat-model context a developer needs
before writing the code: what is this thing, where will it run, what
inputs do we trust, what inputs do we not. It does **not** emit
findings or apply a checklist of "missing controls" — that's the
developer's job once they have the context.

Single source of truth: this skill delegates to the
`threat-modeling` subagent in `.claude/agents/threat-modeling.md`. The
subagent's JSON output is the canonical threat-model shape.

## Vulnerable patterns

This is an orchestrator skill. The agent it dispatches has no
vulnerable-pattern catalog of its own — it produces context, and
later auditors (`vulnerability-audit`, `design-review`,
`contract-audit`) use that context to find code-level issues.

## Procedure

Use the **Agent** tool to dispatch one `threat-modeling` subagent.
Pass it the plan, spec, or codebase under discussion. The subagent
returns a JSON object describing purpose, deployment, trusted
inputs, and untrusted inputs.

**Render that JSON as a Markdown report for the developer.** Do
not show the raw JSON. The report shape:

```
## Threat Model — <one-line summary derived from purpose>

**Purpose.** <purpose>

**Deployment.** <deployment>

**Trusted inputs** (the maintainer controls these; auditors should
not flag content originating here):

- <category 1>
- <category 2>
- ...

**Untrusted inputs** (cross a trust boundary; every one needs an
explicit handling step in the plan — validation, rate limit,
authentication, etc.):

- <category 1>
- <category 2>
- ...

---

*Use this as the design checklist for what your plan must address.
The skill produced context; deciding which controls to add is
yours.*
```

The closing line is intentional — this skill does not enforce
specific controls or emit findings. It surfaces the trust-boundary
picture; the developer decides what to add (auth on new endpoints,
rate limits on user-facing surface, validation on external-service
responses, …).

## Verification

- [ ] Output is a Markdown report (not raw JSON) with a `## Threat
      Model` heading
- [ ] **Purpose**, **Deployment**, **Trusted inputs**, and
      **Untrusted inputs** are each present as labeled sections
- [ ] Trusted-input and untrusted-input categories are listed
      explicitly (one bullet per category)
- [ ] The report describes the system; it does NOT list "missing
      controls", recommend specific mitigations, or emit findings —
      that work belongs to `design-review` or to the developer's
      own follow-up

## References

- CWE-693 ([Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html))
- CWE-657 ([Violation of Secure Design Principles](https://cwe.mitre.org/data/definitions/657.html))
- [OWASP A06:2025 Insecure Design](https://owasp.org/Top10/A06_2021-Insecure_Design/)
