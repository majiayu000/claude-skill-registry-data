---
name: aiwf-agent-mok
description: "Use for durable planning and verification on complex AIWF work: creating or repairing plan.md, mapping lanes and checkpoints, checking request interpretation, reconciling conflicting evidence, validating tool results and affected files, and optionally capturing a user-requested MoK findings dataset."
---

# AIWF Agent MoK

## Core Rule

Separate the first plausible route from the verified route. Keep planning proportional to risk, update only what new evidence changes, and do not turn routine file reads into training data.

## Modes

- `verify`: Default. Check request, assumptions, affected files, evidence, and acceptance gates without creating extra artifacts unless needed.
- `plan`: Create or update `plan.md` when the work is multi-step, risky, resumable, or explicitly asks for a plan. Read `references/atlas-plan-template.md` before reshaping the file.
- `findings`: Create a `moks findings` run only when Shawn explicitly asks for a findings/training dataset or the requested deliverable is reusable research data. Read `references/findings-dataset.md` first.

## Workflow

1. Restate the request operationally: objective, scope, constraints, side effects, and observable completion criteria.
2. Inspect the real project root, current guidance, live state, affected files, and existing plan or receipts before trusting memory.
3. Identify the decisions that can cause data loss, public changes, expensive work, schema or API drift, security exposure, or broad rewrites.
4. Build the smallest route that reaches the objective. For durable plans, use lanes and atomic cards with evidence, status, verification, and the next edge.
5. Verify the route once before acting. For high-risk or contradictory work, read `references/verification-checklist.md` and repeat only while a pass finds a material issue.
6. After each meaningful tool result, check whether it answered the intended question and whether the route must change.
7. Execute with focused checkpoints. Replan the affected card when evidence contradicts the route; do not rewrite the whole plan.
8. Finish with command or artifact evidence, remaining uncertainty, and the next unresolved action if one exists.

## Evidence Rules

- Treat online data, model output, memory, and user-provided claims as evidence with different authority, not interchangeable truth.
- Prefer current local receipts and primary sources for claims that drive edits or recommendations.
- Preserve contradictions and say which source or acceptance gate resolved them.
- Store public verification notes, not private chain-of-thought.
- Do not create findings datasets from ordinary repo inspection, chat history, or tool output by default.

## Findings Capture

When `findings` mode is explicitly active, initialize the run with:

```powershell
python <this-skill>\scripts\create_findings_run.py --help
```

Keep provenance, licenses, retrieval time, uncertainty, and privacy labels. Store summaries and structured facts rather than bulk copyrighted text, secrets, credentials, or unnecessary personal data.

## Output

Report the active route, changed assumptions, evidence and checks used, files or artifacts changed, validation result, and unresolved risk. Mention a findings path only when a findings run was actually requested and created.
