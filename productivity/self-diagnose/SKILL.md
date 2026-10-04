---
name: self-diagnose
description: "Explain bounded local trace diagnosis reports and suggest explicit next commands."
intents: [meta, task]
allowed-tools:
  - self_diagnose
---

# Self Diagnose

Use this skill when the operator asks Allbert to inspect its own recent local behavior, explain a failure, or decide what to check next.

## Safety Contract

- Use only the `self_diagnose` tool for trace diagnosis.
- Do not read trace files directly.
- Do not infer private state from paths, manifests, or trace filenames.
- Do not start remediation from natural-language intent.
- When a fix is appropriate, tell the operator the exact `allbert-cli diagnose run --remediate <code|skill|memory> --reason <text>` command to run.

## Report Handling

- Call `self_diagnose` with an explicit `session_id` only when the operator names a session.
- Otherwise call it without `session_id` so the kernel uses the active session plus bounded recent sessions.
- Summarize the classification, confidence, report path, and one or two evidence points.
- Mention skipped or truncated data when the report summary says truncation happened.
- Keep recommended next actions concrete and review-first.

## Boundaries

The diagnosis report is an explanation artifact. Any code patch, skill draft, or memory update must go through the existing reviewed approval, quarantine, or staging surfaces.
