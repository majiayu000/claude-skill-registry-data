---
name: firmware-report-writer
description: Use when producing human-readable reverse-engineering or firmware static-analysis reports, especially reports that need executive summaries, firmware layout, rootfs summary, route tables, function maps, confirmed findings, hypotheses, risk-ranked areas, recommended manual validation steps, and appendices with commands and offsets.
metadata:
  short-description: Write conservative firmware RE reports
---

# Firmware Report Writer

Use this skill when turning reverse-engineering notes into a conservative, auditable report.

Companion references are available in `references/`: `WORKFLOW.md` for the end-to-end checklist, `CASE_LAYOUT.md` for case organization, `REPORT_TEMPLATE.md` for a starting report, and `TOOLS.md` for external dependencies.

## Report Structure

Prefer this structure unless the user asks otherwise:

1. Executive summary
2. Firmware layout summary
3. Extracted rootfs summary
4. Web UI route summary
5. CGI endpoint table
6. Function map
7. Confirmed findings
8. Hypotheses / items needing manual validation
9. Risk-ranked interesting areas
10. Recommended next manual steps
11. Appendix with useful commands, offsets, hashes, and artifact notes
12. Skill/workflow self-evaluation when the user asks to test or improve the analysis workflow

## Evidence Standards

Use clear labels:

- `Confirmed`: directly supported by source, symbols, disassembly, relocation records, strings with table linkage, or rootfs references.
- `Candidate`: suspicious and worth auditing, but missing part of reachability or data flow.
- `Hypothesis`: plausible interpretation needing manual validation.
- `Unknown`: not enough evidence.

## Style Rules

- Be conservative. Do not claim exploitability without source-to-sink evidence.
- Separate source-tree findings from extracted-rootfs findings when artifacts differ.
- Include exact filenames and offsets/addresses where practical.
- Avoid burying uncertainty in prose; put confidence in the table or finding label.
- Keep commands reproducible and avoid destructive operations.
- When producing an addendum, state what changed from the prior report and what remains unchanged.

## Table Templates

Endpoint table:

```markdown
| Endpoint | Artifact | Handler/function | Visible references | Confidence | Notes |
|---|---|---|---|---|---|
```

Function map:

```markdown
| Function | Artifact | Role | Key calls/sinks | Confidence | Notes |
|---|---|---|---|---|---|
```

Risk table:

```markdown
| Rank | Area | Evidence | Why interesting | Validation needed |
|---|---|---|---|---|
```

## Closing Guidance

End with concrete manual next steps: targeted dynamic tests, emulator/instrumentation ideas, debugger breakpoints, route probes, file-system observation, and hash/firmware-version checks. If the user asked to evaluate the workflow, include concise skill gaps and proposed skill updates.
