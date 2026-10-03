---
name: new-feature
description: Start a feature or change through the orchestrated, architecture-aware pipeline. Manual command.
argument-hint: "<what the system should do> [autopilot]"
disable-model-invocation: true
---
Act as orchestrator using skill `orchestration`. The text after the command is the request.
1. Read `.ai/architecture/profile.yml`; run `pwsh scripts/Set-AiState.ps1 -Init -Task "<request>" -Tool <copilot|claude-code>`.
2. Classify, run the pipeline for the class. Stop at G1 unless the request contains `autopilot`.
Output only gate lines, questions (numbered, with defaults) and the final report.
