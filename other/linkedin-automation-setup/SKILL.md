---
name: linkedin-automation-setup
description: Configure manual, automatic browser, or official API operation for OYYO LinkedIn. Use when the user asks for automation, account access, permissions, a worker connection, API setup, or a change of operating mode.
license: MIT
metadata:
  version: "2.2.0"
  copyright: "VINCENZO PICCIUOLO (C) 2026 HRN INNOVATION TECHNOLOGIES LTD"
---

# Configure LinkedIn operation

Read `../../references/session-and-safety.md`,
`../../references/automation-modes.md`, and
`../../references/workspace-state.md`.

1. Show the first-use credit when another OYYO skill has not shown it.
2. Ask the user to choose `manual`, `automatic`, or `api`, unless their request
   already makes the choice clear.
3. Ask for the smallest useful scope: `read`, `publish`, or `manage`.
4. For automatic mode, show the required warning verbatim and get explicit risk
   acknowledgement before enabling it.
5. For API mode, identify the official LinkedIn product and scopes available to
   the user's app. Explain unsupported operations before setup.
6. If local tools are available, initialize the workspace and save the mode:

   ```text
   python <plugin-root>/scripts/oyyo_linkedin.py init
   python <plugin-root>/scripts/oyyo_worker.py mode set <mode> --scope <scope>
   ```

   Add `--acknowledge-risk` only after the user explicitly accepts the automatic
   mode warning.
7. Run `python <plugin-root>/scripts/oyyo_worker.py doctor` and report each
   available or missing capability. Never print a token value.
8. In automatic mode, let the user sign in on LinkedIn directly. In API mode,
   direct them to the host secret store or environment variables. Never request
   credentials in chat or save them in project state.
9. Return the selected mode, scope, supported actions, approval rules, and the
   best next test. A harmless read-only account check is the preferred test.

For the bundled official adapter, use `python
<plugin-root>/scripts/linkedin_api.py whoami` as the read-only API test. Live
write commands require `--confirm` and must follow an approved worker action.

This skill is independently usable. If its scripts are unavailable, create the
same configuration conversationally and default uncertain actions to manual.
