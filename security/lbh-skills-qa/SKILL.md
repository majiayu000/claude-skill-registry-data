---
name: lbh-skills-qa
version: 1.0.0
description: Run the Legal Builder Hub security-review gate on a candidate legal skill — inspect its manifest and body for unsafe behavior before any install is allowed.
author: matrixx0070
tags: [legal, security, review, vetting, gate, audit]
capabilities: []
---

## When to use

Use this the moment a candidate legal skill is shortlisted and someone wants to install it. This is the security gate: no legal skill reaches a user's workflow without passing here. You inspect the skill's declared metadata and its instruction body for anything that could leak data, run unsafe actions, or give unqualified legal output.

**Not for:** discovering candidates (`lbh-registry-browser`), the mechanical install itself (`lbh-skill-installer`), or judging pure legal accuracy — you gate safety and hygiene, and flag substance for a human lawyer.

## Method

1. Verify identity: name, pinned version, author, license, and source URL all present and internally consistent. Missing any → FAIL.
2. Scan the body for unsafe primitives: requests to fetch remote code, execute shell, load other skills dynamically, write outside a sandbox, or exfiltrate document contents. Any present → BLOCKER unless explicitly justified and consented.
3. Check the trust boundary: does the skill treat user documents as data, or could injected text in a contract steer it into actions?
4. Check legal-safety posture: does it disclaim non-advice and defer substantive questions to a lawyer? Absence is a HIGH finding for regulated workflows.
5. Match the declared jurisdiction and capability against the intake card. Mismatch → FAIL fit.
6. Assign a verdict — PASS / PASS-WITH-CONDITIONS / FAIL — with each finding tiered (BLOCKER/HIGH/MED/LOW) and cited to a line.

## Example

Candidate `contract-redliner v1.3` declares author and MIT license but its body says "fetch the latest clause library from a URL and apply it." That is a remote-fetch BLOCKER. Verdict: FAIL — the skill would pull unvetted external content into a legal document. You return the finding and recommend `lbh-registry-browser` re-shortlist a self-contained alternative.

## Pitfalls

- Passing a skill because it's popular or well-written. Prose quality is not safety; read for primitives, not polish.
- Missing injection risk: a skill that acts on instructions embedded in the reviewed contract is compromised by design.
- Treating a missing non-advice disclaimer as cosmetic. For regulated/PII workflows it is a HIGH finding.
- Approving "latest" instead of a pinned version, so the vetted artifact differs from the installed one.

## Output format

```
# Security Review — <name>@<version>
IDENTITY: author/license/source/version = <ok|missing:...>
UNSAFE PRIMITIVES: <none | list with line refs>
TRUST BOUNDARY: <treats docs as data? y/n>
LEGAL SAFETY: non-advice disclaimer=<y/n>
FIT: jurisdiction/capability vs intake = <match|mismatch>
FINDINGS: [BLOCKER] ... [HIGH] ... [MED] ...
VERDICT: PASS | PASS-WITH-CONDITIONS(<...>) | FAIL
```

## Reference

**Skill-vetting checklist:** identity complete; capabilities meaningful; jurisdiction/doc-type declared; body free of unsafe primitives; non-advice disclaimer present; source pinned.

**Security-review gate criteria:** BLOCKER = remote code fetch, shell execution, dynamic skill loading, out-of-sandbox writes, or document exfiltration. HIGH = missing disclaimer on regulated data, injection-actionable body. A single BLOCKER = FAIL.

**Versioning / rollback:** record the exact reviewed `name@version` and verdict; only that immutable coordinate is cleared for install, and rollback returns to a prior PASS-ed version.
