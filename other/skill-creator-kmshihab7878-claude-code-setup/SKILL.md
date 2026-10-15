---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

Create, evaluate, improve, package, and maintain Claude skills. Use this skill
when the user wants a new skill, an existing skill changed, skill performance
measured, evals run, or a skill description optimized for triggering accuracy.

## Core Loop

1. Determine where the user is: new skill, draft review, eval run, improvement,
   description optimization, packaging, or troubleshooting.
2. Capture intent and confirm the required input contract before writing.
3. Draft or edit the skill folder.
4. Create realistic test prompts when testing is useful.
5. Run skill-vs-baseline evals when tooling supports it; otherwise run a
   smaller qualitative review.
6. Grade outputs, gather user feedback, and improve the skill.
7. Repeat until the user is satisfied, objective checks pass, or progress stalls.
8. Package or present the final skill when requested and supported.

## Required Input Contract

Before writing a new skill, identify:

- what the skill enables Claude to do
- when it should trigger, including user phrases and contexts
- expected output format or artifacts
- dependencies, tools, scripts, reference docs, or assets
- safety boundaries and prohibited behavior
- whether evals are useful for the task type

If the conversation already contains the workflow to turn into a skill, extract
the sequence, tools, corrections, input/output formats, and success criteria
from the conversation before asking follow-up questions.

## Skill Folder Contract

Use this structure unless the existing skill already has a compatible layout:

```text
skill-name/
  SKILL.md
  scripts/
  references/
  assets/
  evals/evals.json
```

- `SKILL.md` is required and holds frontmatter plus concise operating guidance.
- `scripts/` holds deterministic or repetitive executable helpers.
- `references/` holds lazy-loaded detailed docs.
- `assets/` holds templates, icons, examples, or output resources.
- `evals/evals.json` holds skill test prompts when evals are used.

Keep `SKILL.md` concise. Move bulky examples, schemas, deep explanations,
templates, troubleshooting detail, and long playbooks into `references/`.

## Frontmatter Requirements

Every `SKILL.md` must include YAML frontmatter with:

- `name`: stable skill identifier, usually matching the folder name.
- `description`: the primary trigger mechanism. Include what the skill does and
  when to use it.

Descriptions should be specific and slightly trigger-forward. Include likely
user intents and contexts, not only a generic capability label. Do not hide
triggering rules only in the body.

## Safety and Security Constraints

- Do not create misleading skills.
- Do not add malware, exploit code, credential harvesting, data exfiltration, or
  unauthorized-access workflows.
- Do not include secrets, credentials, private context, local user paths, session
  records, memory exports, personal identifiers, or real tokens in skill files.
- Do not overfit instructions to one example when the skill should generalize.
- Preserve existing skill `name` and frontmatter identity when improving an
  installed skill unless the user explicitly asks for a rename.
- Treat bundled scripts as code: keep them scoped, inspectable, and testable.

## Creation Workflow

1. **Capture intent:** confirm capability, trigger contexts, output format,
   dependencies, success criteria, and safety limits.
2. **Research:** inspect existing files, examples, tools, references, and related
   skills. Ask only the missing questions that affect the skill design.
3. **Draft structure:** create `SKILL.md`; add `scripts/`, `references/`,
   `assets/`, and `evals/` only when they carry real value.
4. **Write instructions:** use imperative, general, reusable guidance. Explain
   why important rules matter.
5. **Add minimal examples:** include only examples needed for correct invocation
   or output shape; move longer examples to references.
6. **Validate:** check frontmatter, links, file layout, safety constraints, and
   eval schema when present.
7. **Evaluate:** run test prompts when meaningful; compare against baseline for
   measurable skills.
8. **Iterate:** improve based on transcript evidence, grader output, benchmarks,
   and user feedback.

Full phase detail: `references/workflow-deep-dive.md`.

## Validation Rules

- Do not claim eval success without evidence.
- Do not use `/skill-test` or another testing skill for the skill-creator eval
  loop.
- For eval runs, create a sibling workspace named `<skill-name>-workspace/` and
  organize by `iteration-N/eval-N/`.
- For new skills, baseline is `without_skill`.
- For improving existing skills, snapshot or otherwise preserve the old version
  before comparing.
- Capture timing from completion notifications immediately when available.
- Use `eval-viewer/generate_review.py` for human review when browser/static
  output is available; do not invent custom review HTML.
- Use `agents/grader.md`, `agents/analyzer.md`, and `agents/comparator.md` only
  for their documented roles.

Detailed eval, grading, viewer, failure-mode, and security guidance:
`references/validation-and-safety.md`, `references/eval-workflow.md`, and
`references/schemas.md`.

## Minimal Eval Example

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Full schemas: `references/schemas.md`.

## Output Expectations

When creating or modifying a skill, report:

- skill folder and files created or changed
- trigger behavior and output contract
- safety constraints included
- validation performed and results
- evals run, if any, with evidence
- known limitations and recommended next iteration

If packaging is requested and supported, use `scripts/package_skill.py` and point
to the created package artifact.

## Environment Variants

- Claude Code/Codex with subagents: run parallel skill-vs-baseline evals when
  useful.
- Claude.ai without subagents: run qualitative tests one at a time and ask for
  user review inline.
- Headless/Cowork-like environments: generate a static review artifact instead
  of a browser server.

Variant details and packaging notes: `references/workflow-deep-dive.md`.

## Reference Map

- `references/workflow-deep-dive.md` - full creation workflow, eval phase
  details, environment variants, packaging, and advanced decisions.
- `references/frontmatter-and-structure.md` - frontmatter examples, folder
  layout, naming, output contracts, and resource placement.
- `references/authoring-patterns.md` - writing patterns, long templates,
  description guidance, progressive disclosure, and reusable instruction forms.
- `references/validation-and-safety.md` - extended validation checks, failure
  modes, eval mechanics, security caveats, and troubleshooting.
- `references/examples.md` - end-to-end skill creation and improvement examples.
- `references/eval-workflow.md` - existing detailed eval-and-review procedure.
- `references/description-optimization.md` - existing trigger-description
  optimization procedure.
- `references/schemas.md` - JSON schemas for eval, grading, timing, and metrics.
- `references/skill-template-reference.md` - existing anatomy diagram and
  progressive-disclosure reference.

Specialized agents:

- `agents/grader.md` - evaluate assertions against outputs.
- `agents/comparator.md` - blind A/B comparison.
- `agents/analyzer.md` - analyze why one version beat another.
