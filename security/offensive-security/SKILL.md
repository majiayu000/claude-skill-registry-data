---
name: offensive-security
description: Authorized offensive security skill for ethical penetration testing, red-team planning, vulnerability validation, reconnaissance of owned assets, web/API/mobile/cloud assessment, report writing, remediation guidance, and lab-based security testing. Use only for systems the user owns or is authorized to test; focus on safe, scoped, legal assessment and defensive improvement.
---

# Offensive Security

## Authorization Boundary

- Confirm scope, authorization, target ownership, allowed techniques, test window, and reporting requirements before active testing guidance.
- Do not provide instructions for unauthorized access, persistence, stealth, evasion, credential theft, destructive actions, or real-world exploitation against third parties.
- Prefer lab-safe proof, vulnerability explanation, detection, and remediation when the request is dual-use.

## Assessment Workflow

1. Define scope: targets, exclusions, credentials, rate limits, legal constraints, and success criteria.
2. Build a test plan aligned to the asset type: web, API, network, cloud, mobile, identity, or source code.
3. Collect evidence safely with minimal impact and clear timestamps.
4. Validate findings enough to prove risk without expanding access unnecessarily.
5. Report business impact, reproduction summary, affected assets, severity rationale, and remediation.

## Quality Bar

- Keep commands scoped to authorized assets and non-destructive options.
- Avoid noisy scans unless the user confirms timing and rate limits.
- Include cleanup and rollback steps for any test artifact.
- Provide defensive detection and hardening guidance with every confirmed issue.

