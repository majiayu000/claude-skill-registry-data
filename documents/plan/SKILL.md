---
name: plan
description: Gather all .plan files, evaluate them against the stated objective (if provided), and suggest missing plans — no implementation
disable-model-invocation: true
argument-hint: <describe the change>
---

# Scalpel Plan

Evaluate existing `.plan` files and identify gaps. This skill does not implement anything.

## Steps

### 1. Determine the Objective

Check whether `$ARGUMENTS` was provided.

| Arguments | Result |
|-----------|--------|
| provided  | Arguments are the objective. Evaluate plans against them. |
| absent    | No objective. Check existing plans for standards alignment only; skip alignment and gap detection. |

### 2. Load Project Standards

Look for standards and architecture documentation in this order and read every file found:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/ARCHITECTURE.md`, `docs/architecture.md`, or any file matching `docs/arch*`

These files define the project's conventions, patterns, and constraints. If none exist, note that no standards were
found and proceed without them.

Do not invent standards. Do not apply conventions from outside these files. Only enforce what is explicitly documented.

### 3. Gather and Normalize Plan Files

```bash
find . -name "*.plan" -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
```

Read every plan file found. Before evaluating, normalize each one silently to the expected format:

**Expected format:**
```markdown
---
file: <path to target file>
type: <add | modify | move | delete>
---

## Change

<description>
```

**Normalization rules — apply automatically, no prompt:**

- If the frontmatter is missing entirely, wrap the full file content in a `## Change` section and infer `file` from the plan's own path (same directory, same base name, `.plan` removed). Set `type: modify`.
- If `file` is missing from frontmatter, infer it from the plan's path as above.
- If `type` is missing from frontmatter, set `type: modify`.
- If the body has no `## Change` heading, treat the entire body as the change description and rewrite it under `## Change`.
- If the body has a `## Change Description` heading instead of `## Change`, rename it to `## Change`.

Write the normalized content back to the plan file before proceeding. Do not alter the meaning of the content — only fix the structure.

### 4. Evaluate Plans

Review each plan against the objective (if available) and the project standards (if available):

- Whether the plan's described change is sufficient, incomplete, or misaligned with the objective
- Whether the approach in the plan violates any standard or architectural constraint from step 2 — cite the specific
  rule when flagging a violation
- Whether any plans conflict with each other

Present findings as a concise list — one line per plan file. If no objective is available, summarize what each plan
intends to do.

### 5. Suggest Missing Plans

If an objective is available or the standards are being violated, identify files that will likely need to change to fulfill the requirements or standards but have no corresponding
`.plan` file. Use the scoped objective (arguments) when present, the standards documents, or use the broader objective. For each gap, name
the file and briefly explain why a plan is needed there.

When suggesting what a missing plan should contain, only recommend approaches that are consistent with the standards
loaded in step 2. Do not invent patterns.

Create the missing plan files — list them so the user can see what was added.

## Rules

- No implementation — do not modify any source files
- Never invent standards — only apply what is explicitly written in the standards files
- When citing a standard violation, quote or reference the specific rule from the source file
- Be specific, brevity is important to not overwhelm the plans with too much information such that a user cannot quickly understand the plan.
- Use Code examples when possible to illustrate the plan, but do not include full implementations.
- Be sure to use Markdown formatting for code snippets, file paths, and filenames to make the plan easy to read.
- When multiple steps are required to implement a plan, break them down into a ordered numbered list for clarity.
