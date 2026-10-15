---
name: release-gating
description: Release gating rules and evaluation for BLOCKED, READY_FOR_REVIEW, and PASS release decisions.
---

# Release Gating Skill

## Gate Definitions
- **BLOCKED:**
  - Any confirmed CRITICAL security vulnerability.
  - Any hardcoded credential or exposed private key.
  - Any failing automated test in the regression suite.
  - Any compilation or build error.
- **READY_FOR_REVIEW:**
  - Zero blockers present.
  - One or more verified HIGH or MEDIUM risks require sign-off.
- **PASS:**
  - All mandatory gates satisfied.
  - Zero blockers, zero unresolved critical risks.
