---
name: forsetti-compliance
description: Review MCOS phase work for Forsetti/CLU compliance.
disable-model-invocation: true
---

# Forsetti Compliance Skill

Checklist:

- Vendored Forsetti code untouched.
- Module manifests updated only when needed.
- CLU bundle behavior documented and tested.
- Windows governance bundle included.
- macOS/iOS governance bundle paths included if applicable.
- Compliance script updated to match current architecture.
- No provider-era authorization assumptions remain in AI-client gateway path.
- Mutating operations still pass through governance decision flow where required.

Output a pass/fail checklist and exact remediation items.
