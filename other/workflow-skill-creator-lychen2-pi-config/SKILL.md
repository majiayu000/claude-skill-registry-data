---
name: workflow-skill-creator
description: Distill a completed user workflow into a reusable skill when asked to capture, package, or create a skill from worked examples.
---

# Workflow-to-Skill Distiller

Capture a workflow that actually worked, with enough flexibility for a new task.
Use the conversation and existing artifacts as the starting evidence.

## Define the useful part

Identify the trigger, inputs, expected artifact, reusable steps, and task-specific
choices. Resolve these from the completed work before asking questions. Ask only
for missing scope or behavior that changes the skill; there is no required interview,
round count, or approval cycle for already authorized creation.

Reuse installed skills and existing tools where they fit. A workflow that calls tools
or processes files does not automatically need a new CLI. Add code when it removes
repeated error-prone work or provides a capability the existing tools lack.

## Write the skill

- Use a concise `SKILL.md` with YAML `name` and `description`. Describe the task and
  trigger clearly; keep the name lowercase with hyphens and within 64 characters,
  and the description within 1024 characters.
- Keep the entrypoint focused on decisions and a usable workflow. Put long examples,
  reference material, and optional procedures in referenced files loaded when needed.
- Separate working instructions from the output specification. Checklists guide
  execution; they are not sections to copy into the deliverable.
- Specify the requested artifact directly, including its audience and format. Route
  subject matter to the artifact, actionable editorial issues to native comments
  or a brief handoff, and routine process residue nowhere. Footnotes, captions,
  speaker notes, bibliography `note` fields, tooltips, and collapsed panels are
  audience-facing content, not substitutes for comments.
- State scope as concrete methods, parameters, and applicability beside the affected
  claim. Preserve meaningful uncertainty, safety information, and required
  disclosures. Do not generate standalone disclaimer or verification-status
  sections by default; include comparisons and assessments when requested.
- Audit the examples and templates as well as the prose rules. Do not preserve an
  earlier interaction's apology, correction history, or self-defense as a reusable
  output pattern. Include a reader-view check without requiring its checklist or
  completion claim to appear in the output.
- Validate external inputs where they enter the system and handle side-effecting
  boundaries explicitly. Internal calls should rely on established contracts, not
  repeat external-input checks, permission prompts, or generic fallback machinery.
- Preserve meaningful failure handling: identify an actionable cause, recover when a
  known alternative fits, or report a concrete blocker. Avoid defensive scaffolding
  for hypothetical cases unsupported by the workflow.

A small instruction-only skill can use:

```markdown
## Workflow
1. Identify the required inputs from the task.
2. Perform the reusable steps using existing tools or skills.
3. Check the result against the task's acceptance criteria.

## Delivery
Return the requested artifact for its intended reader. State necessary assumptions
and limitations as concrete facts where they affect interpretation. Keep actionable
editorial issues in native comments or the handoff; omit routine process residue.
Inspect all reader-facing surfaces, not just the body. Do not print this check.
```

## Add helpers when useful

Use the project's existing runtime and conventions. Prefer standard-library code
when adequate; add dependencies for a demonstrated need. A single-purpose script
is sufficient unless separate operations genuinely benefit from subcommands.

For API helpers, consult the service's rate limits and honor `Retry-After`. Use bounded
retries for transient, safely retryable requests, and report errors with useful
context without credentials or sensitive response bodies. Coordinate rate limiting
across processes only when concurrent use requires it. Inspect and adapt
`references/cli_script_template.py` when its structure fits; it is an example, not a
mandatory implementation.

Use stdout for small structured results and files for large payloads or requested
artifacts. Make truncation/pagination explicit in machine-readable results when
relevant. Use safe defaults rather than requiring every optional argument.

## Verify and deliver

Check frontmatter, referenced paths, and the workflow's representative success and
failure cases. Run helpers that changed and test a sample task when available.
Separate structural checks from an actual agent behavior test; report only checks
performed. Deliver the skill files and a concise invocation example. Do not add
compliance claims, an interview transcript, or unrequested design paperwork.
