---
name: planner-output-format
description: YAML frontmatter + markdown output format for planner agent. Defines structure, rules, and examples for plan generation.
user-invocable: false
references: references/REFERENCE.md
scripts: scripts/validate-plan.sh
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when

- Generating a plan as a planner agent
- Structuring output that will be parsed by the pipeline orchestrator
- Deciding how to organize todos, verify_steps, and implementation detail sections

## Do not use this skill when

- You are a coder, reviewer, or debugger — this format is for planners only
- The task requires informal conversation rather than a structured plan

## Purpose

Defines the mandatory output format for planner agents: YAML frontmatter containing machine-parseable todos, followed by a markdown body containing all human-readable investigation results, diagrams, implementation steps, and risk analysis. Separates the progress checklist (YAML) from the detailed instructions (markdown).

## Capabilities

### Format Rules

The response is a YAML frontmatter block between `---` delimiters followed by a markdown body.

Critical: the very first character of the response must be `---`. No text before the first delimiter — no "I'll output...", no summary, no investigation results. These all go in the markdown body after the second `---`.

The planner describes WHAT to do and WHY, but never writes code. Implementation Steps sections specify the file, function or method, what behavior should change, and constraints. They do not include code blocks showing current code replaced with new code — the coder decides HOW to implement.

### YAML Frontmatter Structure

Fields: `name` (3–7 word plan name), `overview` (1–2 sentences on what and why), `todos` (array of step objects), `isProject` (boolean).

Each todo object has: `id` (unique kebab-case identifier), `content` (short 1-line checkpoint, max 100 chars — what to verify, not how to do it), `verify_steps` (list of 1–3 concrete testable assertions for the verifier), `status` (always `pending`).

Do not include code snippets, detailed instructions, or file paths inside todos. Todos are a progress checklist, not detailed task descriptions.

If there are questions for the client, add `has_questions: true` and a `questions` array to the frontmatter.

### Markdown Body Sections

After the second `---`, the body contains all detail in this order:

Architecture — Mermaid diagrams and interaction schemas.

Investigation Results — what was found in the codebase: relevant symbols, patterns, dependencies, call sites.

Approach Selection — a table of considered approaches with pros and cons, the selected variant, and trade-off rationale.

Implementation Steps — detailed steps referencing specific files, functions or methods, what behavioral change is needed, and why. No code snippets showing before/after. The coder reads this and decides how to implement.

Files Summary — a table listing each file with action (NEW/MOD) and approximate line count change.

Risks and Rollback — identified risks and the rollback plan for each.

Agents and Review — who implements each step and in what order.

Validation — what build command, tests, and criteria confirm the plan is complete.

### Verify Steps

Each verify_step is a single testable assertion. Examples: "Function X exported from module Y", "TypeScript compiles without errors", "Build command passes", "API endpoint returns 200", "New component visible in the UI". Avoid vague assertions like "works correctly".

## Behavioral Traits

- Outputs `---` as the absolute first character — no preamble whatsoever
- Keeps todo content to one line, max 100 characters
- Puts all investigative reasoning and code analysis in the markdown body
- Never inserts before/after code blocks in Implementation Steps
- Writes 1–3 verify_steps per todo, each a single testable assertion

## Important Constraints

- FIRST character must be `---` — no exceptions, no leading text
- NEVER write code in todos or verify_steps
- NEVER show "current code → replace with" blocks — coder decides HOW
- ALWAYS set `status: pending` for all todos
- ALWAYS include at least one final `verify` todo that checks build and tests pass

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
