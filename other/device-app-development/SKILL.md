---
name: device-app-development
description: Develop a request-specific app with the mounted device SDK, inspect relevant API documentation, exercise interactions, and export a checked artifact.
---

# Device app development

1. Understand the complete text/transcript/visual request and read `/workspace/authoring.txt` once. That brief contains the syntax and measured requirements needed to start. Use the SDK index, relevant example or canonical source only to answer an unresolved question; there is no mandatory documentation checklist.
2. Create a runnable request-specific draft early in `/workspace/out/app.json` and execute `python3 /workspace/trusted_check.py`. Use raw JSON and a quoted heredoc, never a Python dictionary literal. Combine primitives freely; examples are not app categories or replacement answers.
3. Exercise the intended workflow and review the result against the input. Batch independent targeted reads when needed, then repair actual defects. Model-authored scenarios are useful checks, not independent proof of intent. The manifest describes source APIs and the selected model/budget; it does not attest installed firmware.
4. Run the checker again after changes. Preserve canonical sources and finish after the real `VALIDATED_APP` or `UNSUPPORTED_REQUEST` hash marker. Do not spend the whole job reading implementation files before attempting execution.

Use short targeted reads/searches instead of full schema/source dumps. No package installation, shell networking, provider credentials or firmware flashing is available inside this job. Public research may use only the enabled managed tools, following `/workspace/agent-sdk/tools-and-assets.md`. This SDK currently exposes the implemented AppSpec runtime; it does not pretend that arbitrary script/native application execution is already available.
