---
name: make-skill
description: >
  Turn a project, tool, API, workflow, SOP, documentation set, or library into
  an installable Codex Skill. Use when the user asks to create, update, package,
  scaffold, or evaluate a Skill from a GitHub repo, package, CLI, REST or GraphQL
  API, MCP server, internal process, template, methodology, or existing docs.
  Also use when deciding whether something is worth turning into a Skill.
---

# Make Skill

Turn reusable procedural knowledge into a small, installable Skill. Optimize for
modern Codex: assume the model is capable, keep instructions lean, and bundle
deterministic scripts or references only where they reduce repeated work.

## Core Judgment

A good Skill does one or more of these:

- Preserves domain knowledge the model cannot reliably know.
- Provides a repeatable workflow with fragile sequencing.
- Bundles scripts, templates, or assets that avoid rewriting boilerplate.
- Documents project-specific APIs, schemas, commands, or constraints.
- Improves trigger reliability for a recurring class of user requests.

Do not create a Skill for generic advice that a mature model already performs
well without extra context.

## Pipeline

1. Research the source.
2. Decide convertibility.
3. Choose Skill type and structure.
4. Generate or update `SKILL.md` and resources.
5. Generate `agents/openai.yaml`.
6. Validate and forward-test when risk justifies it.
7. Package as `.skill` when requested.
8. Present install path and usage examples.

If the user only asks whether something can be a Skill, stop after the
convertibility verdict.

## Phase 1: Research

Prefer local files over web search when the source is already in the workspace.
Browse current official docs or repositories when the source is external or may
have changed.

| Source | Minimum research |
|---|---|
| GitHub repo | README, docs/ or examples/, install command, license, activity |
| CLI tool | install command, top commands/flags, examples, common errors |
| Library/package | install command, core API, I/O formats, version constraints |
| REST/GraphQL API | auth, base URL, key endpoints, rate limits, examples |
| MCP server | startup command, transport, tool list, required env vars |
| Internal workflow/SOP | trigger, inputs, decision points, outputs, failure modes |
| Methodology/docs | core process, edge cases, output format, when not to use |

Research limits:

- Start with at most three high-value documents or pages.
- Extract facts before fetching more.
- Put large reference material in `references/` rather than `SKILL.md`.
- Ask the user only for missing private details that cannot be discovered.

Minimum evidence before building:

- What task the Skill enables.
- At least two realistic trigger prompts.
- Inputs, outputs, and required tools/dependencies.
- Known credentials, costs, or destructive operations.

For a local project, run the bundled inspector before making the convertibility
decision:

```bash
python scripts/inspect_project.py path/to/project --output project-analysis.json
```

The inspector detects the ecosystem and likely Skill type, extracts package
metadata and environment-variable names, and checks installed Skill directories
for likely duplicates. For Markdown READMEs it also records installation commands
and ranks up to three source-backed usage examples with section and line evidence.
Sensitive-looking example values are redacted. Treat the conversion score as a
transparent heuristic, not as the final decision. Inspector output omits absolute
local paths by default; use `--include-local-paths` only for private diagnostics.

For a high-value local project with no strong duplicate, generate a concrete
review-required draft:

```bash
python scripts/bootstrap_from_project.py path/to/project --output ./skill-src
```

The bootstrapper creates a source-informed `SKILL.md`, `agents/openai.yaml`,
`evals/evals.json`, and `references/project-analysis.json`. Extracted README setup
commands and two or three high-confidence examples are inserted into the draft;
package metadata is used only as a clearly labeled setup fallback. It stops on
high-similarity duplicate Skills unless `--allow-duplicate` is explicitly used.
Extraction is not execution verification, so run every retained example before
release and add examples manually when the README provides none.

## Phase 2: Convertibility Verdict

Read `references/blockers.md` when the source may need a GUI, daemon, hardware,
root access, OAuth/browser login, or large dependencies.

Use this verdict format:

```markdown
Can be converted: yes/no/partial
Type: [CLI/library/API/MCP/knowledge/workflow/template]
Value: [high/medium/low]
Reason: [one paragraph]
Planned files: [SKILL.md, scripts/x.py, references/y.md, assets/...]
Risks: [credentials, cost, fragility, current docs needed, etc.]
```

High value means the Skill adds durable knowledge, scripts, templates, or a
fragile procedure. Low value means the content is mostly generic prompting.

If `inspect_project.py` reports a duplicate candidate, inspect that Skill before
creating anything. Prefer extending a compatible existing Skill over publishing
a second Skill with overlapping triggers.

## Phase 3: Choose Structure

Use the smallest structure that works.

| Type | Use when | Typical files |
|---|---|---|
| CLI wrapper | Repeated shell commands, flags, conversions | `SKILL.md`, optional `scripts/` |
| Library | Repeated code imports/patterns | `SKILL.md`, helper scripts, examples |
| API | HTTP service with auth/endpoints | `SKILL.md`, `references/api.md`, scripts |
| MCP server | Skill teaches how to install/use MCP server | `SKILL.md`, `references/tools.md` |
| Knowledge | Domain framework or SOP | `SKILL.md`, optional references |
| Workflow | Multi-tool sequence | `SKILL.md`, scripts, references |
| Template | Reusable artifact format/assets | `SKILL.md`, `assets/`, references |

Scaffold when helpful:

```bash
python scripts/scaffold.py --name my-skill --type workflow --output ./skill-src
```

## Phase 4: Write The Skill

### Frontmatter

Use only:

```yaml
---
name: kebab-case-name
description: >
  Action-oriented trigger description. Include what the Skill does and the
  concrete situations where Codex should use it.
---
```

Name rules:

- Lowercase letters, digits, and hyphens only.
- Folder name must exactly match `name`.
- Keep under 64 characters.
- Avoid generic names like `helper`, `workflow`, or `analysis`.

Description rules:

- Include trigger phrasings the user might actually type.
- Keep it specific enough to avoid triggering on unrelated tasks.
- Avoid angle brackets and placeholder text.
- Keep under 1024 characters unless the local platform explicitly allows more.

### Body

Keep `SKILL.md` concise. Default target: under 250 lines unless the workflow is
genuinely complex.

Recommended sections:

1. Overview: what this Skill enables.
2. When to use / when not to use.
3. Workflow or core commands.
4. Resource routing: which references/scripts/assets to use and when.
5. Validation: how to know the work succeeded.
6. Edge cases and safety boundaries.

Move detailed docs to `references/`. Add scripts when the same code would be
rewritten repeatedly or deterministic behavior matters.

## Phase 5: Generate UI Metadata

Create or refresh `agents/openai.yaml` after writing `SKILL.md`:

```bash
python scripts/generate_openai_yaml.py path/to/skill
```

Override generated values when the default wording is too generic:

```bash
python scripts/generate_openai_yaml.py path/to/skill \
  --display-name "GitHub Check" \
  --short-description "Audit GitHub repo trust signals" \
  --default-prompt "Use $github-check to evaluate whether this GitHub repository is trustworthy."
```

The default prompt must mention `$skill-name`.

## Phase 6: Validate

Run the bundled validator:

```bash
python scripts/quick_validate.py path/to/skill
```

Before release, generate evals and run strict validation:

```bash
python scripts/generate_evals.py path/to/skill \
  --happy "[real common request]" \
  --edge "[real missing-input or auth case]" \
  --negative "[nearby request that should not trigger]"
python scripts/quick_validate.py path/to/skill --strict
```

Validation must pass before packaging. Then do a content review:

- Trigger description is specific and useful.
- `SKILL.md` references only files that exist.
- No unfinished placeholder markers, secrets, full tokens, cookies, or private data.
- Scripts have argument parsing and can be run from the command line.
- The Skill does not duplicate existing system/global instructions unless it adds
  a concrete workflow or asset.
- Large references have headings and are only loaded when needed.

## Phase 7: Forward-Test

Forward-test when the Skill is complex, newly created, likely to trigger often,
or changes behavior beyond formatting. Use fresh context if possible. Do not
pass your intended answer; pass the Skill path and a realistic user request.

Suggested prompts:

```text
Use $skill-name at path/to/skill-name to solve: [realistic task]
```

Test at least:

- Happy path: the most common request.
- Edge path: missing input, private docs, auth, rate limit, or unsupported source.
- Mis-trigger path: a nearby request where the Skill should not be used.

Record only concise results in the final delivery:

```text
Forward-test:
- happy path: pass/fail, key observation
- edge path: pass/fail, key observation
- mis-trigger path: pass/fail, key observation
```

Skip forward-testing only when the edit is trivial or no safe isolated test is
available. Explain the reason.

## Phase 8: Package

Package only the Skill folder itself, not a parent directory containing multiple
skills.

```bash
python scripts/package_skill.py path/to/skill ./dist
```

The output is `dist/<skill-name>.skill`.

## Phase 9: Deliver

Report:

- Skill name.
- What changed or what was generated.
- `.skill` output path.
- Two or three trigger examples.
- Any remaining risks, credentials, or manual install steps.

Do not tell the user to manually recreate files already present in the
workspace.

## Resources

- `references/convertible-patterns.md`: templates and examples by Skill type.
- `references/blockers.md`: hard and soft blockers.
- `references/skill-spec.md`: validation and packaging rules.
