---
name: verify
description: Exercise the real app, API, CLI, or document artifact and collect observable evidence; unit tests alone do not count as end-to-end verification. Includes structural and delivery hygiene checks before handoff.
invocation: model+user
---

# verify — observable evidence and delivery verification

Prove that delivered work works through its actual interface, and verify document
or code artifacts before declaring a task finished. Unit tests and exit codes alone
are not proof of end-to-end behavior.

## When to use

- When validating finished features, CLI tools, web endpoints, or background processes.
- Before declaring task completion on user-facing deliverables, documents, or reports.
- To audit references, encoding, and markup integrity before committing.

## Non-goals

- Passing test suites alone do not substitute for exercising the live interface.
- Never fake success or claim passes for unexercised checks.
- Do not skip checks or weaken assertions to produce green output.

## Workflow

1. **Identify the real entrypoint**:
   - CLI binary, API endpoint, UI route, or delivered document file.
2. **Exercise with realistic inputs**:
   - Run the command, send real requests, or inspect the rendered viewport.
3. **Capture observable evidence**:
   - Collect actual stdout/stderr, HTTP status, DOM snapshots, logs, or metrics.
4. **Delivery hygiene & artifact integrity (merged from review-request)**:
   - Structure: clear purpose, logical headings, no orphan/empty sections.
   - References: all internal links, anchors, and file references resolve to existing paths.
   - Format: valid UTF-8 encoding, no stray byte-order marks (BOM), no accidental syntax errors.
   - Frontmatter: valid YAML with matching name and descriptive trigger where required.
5. **Report evidence and limits**:
   - State what was verified, how it was observed, and any remaining uncertainty honestly.
