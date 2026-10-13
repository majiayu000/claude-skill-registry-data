---
name: social-eng-methodology
description: >
  Plan and run an AUTHORIZED social-engineering assessment safely — the load-first guardrails for
  any human-factor test. Load before any phishing, vishing, pretext, or physical work. Signals:
  "social engineering", "phishing assessment", "test our employees", "security awareness",
  a human-factor objective in a pentest SoW. Establishes authorization, safety, tracking, and the
  awareness-focused report.
domain: social-eng
type: methodology
stability: locked
modes: [pentest]
severity: info
mitre: [T1566, T1598]
schema_version: 1
---

# Social-engineering engagement methodology

## When this governs
Load this **first**, before any phishing/vishing/pretext/physical skill. Social engineering targets
*people*, so it carries authorization and duty-of-care requirements beyond a normal technical test.
This is `pentest`-only: it is never run against a bug-bounty target, and never against individuals
or organizations that have not authorized it in writing.

## Authorization — stricter than technical scope
On top of `tradecraft-scope-roe`, an SE engagement requires, in writing, before anything:
- **Explicit sign-off from someone empowered to consent for the employees being tested** (not just
  IT) — SE tests real staff, so leadership/HR/legal must have approved the human-factor testing.
- **The pretext boundaries**: which themes are allowed and which are off-limits (no fake layoffs,
  bonuses, medical/family emergencies, or anything that causes real distress or coerces protected
  decisions).
- **Target boundaries**: which people/roles/sites are in scope; who is explicitly excluded.
- **A "no-harm" line**: no real financial transactions, no exfiltration of real personal data, no
  actions that damage systems, and no impersonation of real named individuals without consent.
- **A get-out-of-jail letter** carried during any physical work, plus a live emergency contact who
  can confirm authorization to anyone who challenges the tester.

If any of that is missing or unclear, **stop and get it** — do not "just send a test phish".

## The lifecycle
1. **Objective** — what the client wants to learn (click rate, credential submission, report rate,
   physical access, callback rate). It's a measurement, not a "gotcha".
2. **Recon** — only OSINT needed for a credible pretext (`recon-osint`), scoped to in-scope targets.
3. **Pretext design** — believable, within the allowed themes, proportionate to the objective.
4. **Execute with tracking** — instrument so every step is measured and attributable to the test
   (unique tokens/links), and so results can't be confused with a real attack.
5. **Measure & clean up** — collect metrics, disable pretext infra, and delete any personal data
   captured beyond what the metric needs.
6. **Report for awareness** — outcomes and root causes, framed to improve defenses and training,
   never to name-and-shame individuals.

## Guardrails (always)
- **Minimize harm and data.** Prove the human-factor risk with the least intrusion; capture the
  metric, not people's real secrets. A credential-harvest page records "a credential was submitted",
  it does not store or reuse real passwords.
- **Stay attributable and reversible.** Every artifact is tagged as the assessment; nothing is left
  running; a challenged tester can prove authorization immediately.
- **Protect the humans.** No lasting distress, no targeting of individuals' personal/home life, no
  themes the client excluded. If a target escalates emotionally, de-escalate and disclose.
- **Report defensively.** Findings drive controls (MFA, reporting culture, physical procedures) and
  training — individuals are aggregated, not singled out.

## Verify
Written authorization (incl. consent for testing staff), agreed pretext/target boundaries, a
no-harm line, and a tracking + cleanup plan all exist before execution; the deliverable is an
awareness-oriented report with metrics and remediation.

## References
MITRE ATT&CK T1566 (Phishing), T1598 (Phishing for Information); disclose.io-style safe-harbor
framing; standard pentest SE rules of engagement.
