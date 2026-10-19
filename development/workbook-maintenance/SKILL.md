---
name: workbook-maintenance
description: Maintain the metisa MCU-port project workbook with traceable facts, test evidence, status, and safe next steps.
---

# Workbook Maintenance

## Use when

A new source finding, test/build result, board decision, safety issue, license finding, or porting milestone occurs.

## Procedure

1. Read the existing status, relevant work package, and evidence before editing.
2. Label statements as confirmed source fact, static analysis, compile result, simulation, or physical measurement.
3. Add exact commands, target/profile, relevant versions, result, and known limitations to the session log.
4. Update the finding/status register and the relevant gate/task without promoting untested work.
5. Check relative Markdown links and editor diagnostics after changes.

## Constraints

- Do not mark hardware or worst-case tests passed without raw measurements and identified hardware.
- Do not erase earlier evidence; append corrections and explain status changes.
- Preserve unresolved blockers, license caveats, and missing Git provenance.

## Done when

The workbook makes the next safe step obvious and lets another agent reproduce the reported evidence.