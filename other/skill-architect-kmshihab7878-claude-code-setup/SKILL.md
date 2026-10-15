---
name: skill-architect
description: >
  Build, validate, and improve Claude Code skills. Design-first workflow with
  YAML frontmatter validation, progressive disclosure, and quality assessment.
  Use when creating new skills, improving existing ones, auditing skill quality,
  or troubleshooting skill triggering issues.
version: 1.0.0
keywords: skill, meta, builder, validation, quality, architecture
---

# skill-architect

Build, validate, and improve Claude Code skills using a design-first methodology.

## how to use

- `/skill-architect` — apply skill architecture principles to the current conversation.
- `/skill-architect build <name>` — create a new skill from scratch following the full build workflow.
- `/skill-architect review <path>` — review an existing skill and produce a scored quality report.
- `/skill-architect validate <path>` — run the validator and report structural/frontmatter/content issues.

## when to apply

- Creating a new Claude Code skill from scratch.
- Improving or refactoring an existing skill.
- Auditing skill quality across a skill library.
- Troubleshooting why a skill is not triggering correctly.
- Reviewing a skill before publishing or sharing.
- Converting a one-off workflow into a reusable skill.

## when NOT to apply

- General coding tasks — use `coding-workflow` instead.
- "Improve my skills" meaning career or personal development.
- Prompt engineering for chat conversations (skills are file-based, not chat-based).
- Writing one-off documentation or READMEs.
- Configuring MCP servers (that is infrastructure, not skill authoring).
- Iterative skill improvement with eval benchmarks — use `skill-creator` instead;
  it provides subagent testing, programmatic grading, eval-viewer, and
  description optimization with eval queries.

## rule priorities

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Design-first thinking | Critical |
| 2 | YAML frontmatter | Critical |
| 3 | Folder structure | Critical |
| 4 | Instruction quality | High |
| 5 | Progressive disclosure | High |
| 6 | Composability | Medium |
| 7 | Testing | Medium |
| 8 | Iteration | Low |

Full per-category rules: `references/skill-system-patterns.md`.

## critical constraints

### Design-first (priority 1)

- MUST define 3+ trigger prompts before writing.
- MUST identify the skill category (document/asset, workflow automation, MCP enhancement).
- MUST check existing skills for overlap.
- MUST define explicit scope boundaries — what the skill does NOT cover.
- NEVER start writing SKILL.md without completing the design phase.

### YAML frontmatter (priority 2)

- MUST start with `---` on line 1.
- MUST include `name` in kebab-case matching the folder name exactly.
- MUST include `description` under 1024 characters with no angle brackets.
- MUST NOT use forbidden terms in `name`: `claude`, `anthropic`, `plugin`, `extension`.
- The description's first sentence determines triggering.
- Use `>` folded scalar for multi-line descriptions.

Full field spec: `references/yaml-reference.md`.

### Folder structure (priority 3)

```text
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional — stdlib only
└── references/       # Optional — supplementary docs
```

- Folder name MUST be kebab-case and MUST match the `name` field.
- MUST NOT have both `README.md` and `SKILL.md`.
- Scripts MUST use Python stdlib only — no pip dependencies.
- Keep SKILL.md under 5000 words; spill into `references/`.

## core workflow

### Build (creating a new skill)

1. **Design** — define triggers, category, scope, and name.
2. **Structure** — create folder layout.
3. **Content** — write scripts → references → SKILL.md.
4. **Validate** — run `scripts/validate_skill.py` (13 checks must pass).
5. **Test** — Tier 1 triggering, Tier 2 functional.
6. **Refine** — register, iterate on real usage.

Full procedure with templates: `references/architecture-workflow.md`.

### Review (auditing an existing skill)

1. **Read** SKILL.md, references/, scripts/.
2. **Validate** with `validate_skill.py --verbose`.
3. **Score** 8 dimensions (0-5 each, 40 max).
4. **Output** validator results, scorecard, top 3 issues, fixes.

Full scoring rubric and review procedure: `references/evaluation-and-validation.md`.

## skill categories

| Category | Description | Examples |
|----------|-------------|----------|
| Document/Asset | Static references, lookup tables, specs | `api-design-patterns` |
| Workflow Automation | Multi-step processes, checklists, pipelines | `coding-workflow`, `git-workflows` |
| MCP Enhancement | MCP server wrappers with domain rules | `aster-trading` |

Per-category patterns: `references/skill-system-patterns.md`.

## validation gates

Structural validation — all 13 checks must pass before shipping:

```bash
python3 ~/.claude/skills/skill-architect/scripts/validate_skill.py <skill-path>
```

Testing tiers — full methodology in `references/testing-guide.md`:

| Tier | What | How |
|------|------|-----|
| 0 | Structural validity | `validate_skill.py` |
| 1 | Triggering accuracy | 3+ positive / 3+ negative prompts |
| 2 | Functional correctness | Happy path + error path + boundary |
| 3 | Performance delta | With-skill vs without |

## safety constraints

- Do not create misleading skills.
- Do not include malware, exploit code, credential harvesting, or data exfiltration patterns.
- Do not bundle secrets, credentials, tokens, private context, personal identifiers, or local user paths in skill files.
- Preserve existing `name` and frontmatter identity when improving an installed skill unless the user explicitly asks for a rename.
- Treat bundled scripts as code: keep them scoped, inspectable, testable, and stdlib-only.

## output expectations

When creating or modifying a skill, report:

- Skill folder and files created or changed.
- Trigger behavior (positive + negative scope).
- Safety constraints included.
- Validator results (which of 13 checks passed/failed).
- Tests performed and results.
- Known limitations and recommended next iteration.

## minimal frontmatter example

```yaml
---
name: example-skill
description: >
  One-sentence trigger statement. Use when <specific user intent A> or
  <specific user intent B>.
version: 1.0.0
keywords: domain, capability, target
---
```

Full templates and patterns: `references/yaml-reference.md`,
`references/workflow-patterns.md`.

## Reference map

| Need | Read |
|---|---|
| Full build + review workflow with templates | `references/architecture-workflow.md` |
| 8 rule categories detailed, skill category patterns | `references/skill-system-patterns.md` |
| Testing tiers, scoring rubric, validator details | `references/evaluation-and-validation.md` |
| Anti-patterns and diagnostics | `references/troubleshooting.md` |
| End-to-end skill construction walkthroughs | `references/examples.md` |
| YAML frontmatter field specification | `references/yaml-reference.md` |
| 5 reusable workflow patterns | `references/workflow-patterns.md` |
| 3-tier testing methodology | `references/testing-guide.md` |
| Pre/during/post development checklists | `references/checklist.md` |
| Automated validator (13 checks) | `scripts/validate_skill.py` |
