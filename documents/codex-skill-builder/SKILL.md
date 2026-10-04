---
name: codex-skill-builder
description: Build, improve, package, and review Codex skills from rough ideas, workflows, scripts, README/API/CLI docs, or existing skill folders. Use when the user wants to create a new Codex skill, convert a repeatable workflow into a reusable skill, scaffold SKILL.md plus references/scripts/assets, validate a skill, or prepare a skill for sharing on GitHub.
---

# Codex Skill Builder

Use this skill to turn a rough workflow, tool guide, script, README, API/CLI document, or existing skill folder into a Codex-ready skill.

Default stance: be proactive and concrete, but do not create files until the user explicitly asks to generate or edit. Prefer a preview copy in the current workspace before touching global skill directories.

## Operating Rules

- Do not use `AskUserQuestion`; ask concise plain-language questions only when needed.
- For new skill ideas, use the three-step rhythm:
  1. Ask the Need Snapshot questions and stop.
  2. After the user answers, summarize knowns/missing details, give two technical options, outline the workflow, and stop.
  3. Only create files after the user explicitly says to generate/build/create/write the skill.
- If editing an installed skill outside the writable workspace, first copy it into the workspace unless the user explicitly approves editing the original.
- Use Codex terminology, not Claude-specific terms.
- Keep `SKILL.md` focused and under 500 lines when possible.
- Put long guidance in `references/`; put deterministic repeated operations in `scripts/`; put templates or reusable output files in `assets/`.
- Add safety boundaries for skills that download, scrape, upload, delete, call paid APIs, handle credentials, or process private data.
- Validate the final skill with `scripts/quick_validate.py` when available.

## Need Snapshot

When the user describes a new skill idea and has not already provided enough detail, ask 5-8 high-signal questions in one block and stop. Generate the questions from the domain instead of using a fixed questionnaire.

Use this structure:

```markdown
## Need Snapshot

To design this skill well, I need a quick picture of the workflow:

1. What should trigger this skill?
   Example: "When I paste a Douyin link", "When I ask to review a PR", "When I upload a PDF".

2. What input will the user usually provide?
   Example: links, files, screenshots, repo paths, API docs, rough notes.

3. What output should the skill produce?
   Example: a report, edited files, a plan, a package, code changes.

4. What steps do you already repeat manually?
   Example: fetch data, inspect files, ask questions, run scripts, validate results.

5. What must the skill never do without confirmation?
   Example: delete files, publish online, spend API credits, scrape private data.

6. What does a successful result look like?
   Example: passes validation, produces a clean summary, saves 30 minutes, creates a ready-to-install skill.

You can answer briefly. Write "not sure" for anything unclear.
```

After asking the Need Snapshot, stop.

## After The User Answers

Summarize and recommend before building. Do not create files yet.

Use this structure:

```markdown
I understand the skill like this:

- Known:
  - ...
- Still missing:
  - ...
- Default assumptions:
  - ...

The core workflow should be:
1. ...
2. ...
3. ...

I see two implementation options:

Option A: Simple version
- Pros:
- Cons:
- Best for:

Option B: Stronger version
- Pros:
- Cons:
- Best for:

Recommendation: start with Option <A/B> because <reason>.

Next step: if you say "generate", I will create a workspace preview copy first, without installing it globally.
```

## Architecture Assessment

Decide internally how much structure the skill needs:

- Simple: one `SKILL.md`, no scripts, minimal references.
- Medium: `SKILL.md` plus one or more `references/` files and optional examples.
- Complex: `SKILL.md`, `references/`, `scripts/`, maybe `assets/`, plus validation and safety boundaries.

Use scripts when:

- the same code would be rewritten repeatedly,
- a command must be deterministic,
- validation is useful,
- packaging, parsing, or filesystem operations are error-prone.

Use references when:

- the instructions are long,
- there are multiple modes or variants,
- examples would clutter `SKILL.md`,
- the domain has detailed rules Codex should load only when needed.

Use assets when:

- the skill needs templates, boilerplate, sample files, brand assets, or reusable output material.

## Build Requirements

Every generated skill must include:

- a folder name matching the skill `name`;
- `SKILL.md`;
- YAML frontmatter containing only `name` and `description`;
- a lowercase hyphen-case `name`;
- a third-person `description` that says what the skill does and when to use it;
- concrete workflow instructions in the body;
- links to one-level reference files when more detail is needed;
- safety boundaries when relevant.

Recommended additions:

- `agents/openai.yaml` for Codex App display metadata;
- `scripts/quick_validate.py` for local validation;
- `references/` for detailed playbooks;
- `examples/prompts.md` for realistic trigger examples.

## Creating A Skill

When the user explicitly asks to generate a skill:

1. Create a workspace preview folder by default.
2. Scaffold the minimal structure needed for the assessed complexity.
3. Write `SKILL.md` first, with concise body instructions.
4. Add `references/`, `scripts/`, `assets/`, or `examples/` only when they materially improve repeatability.
5. Add `agents/openai.yaml` when the skill is user-facing.
6. Add or reuse `scripts/quick_validate.py`.
7. Run validation and fix issues before reporting completion.

Default scope:

```markdown
I will treat this as a workspace preview:
- Tool: Codex
- Install behavior: do not install globally yet
- Target: current workspace
- Later: move or copy to the global skills directory after review
```

## Reviewing Existing Skills

When reviewing an existing skill, check:

1. Structure: `SKILL.md` is at the actual skill root; no accidental nested duplicate folder.
2. Frontmatter: valid YAML, hyphen-case name, description under 1024 characters.
3. Trigger quality: description includes clear use cases and keywords.
4. Codex fit: no stale instructions for unavailable tools or another assistant environment.
5. Context hygiene: `SKILL.md` is concise; long content lives in references.
6. Tooling: scripts run with available dependencies or document requirements clearly.
7. Safety: risky actions require confirmation and boundaries.
8. Metadata: `agents/openai.yaml` exists if the skill is meant to be user-facing.
9. Validation: `scripts/quick_validate.py` or equivalent catches basic structural issues.

Lead with the verdict:

```markdown
Verdict: suitable / suitable after changes / not suitable yet

Main issues:
1. ...

Recommended fixes:
1. ...
```

## Converting Docs Into A Skill

When converting README/API/CLI documentation:

1. Identify the source type: CLI, API, library, file processor, data processor, scraper/downloader, AI model/tool, or workflow.
2. Extract user-facing tasks instead of every documentation detail.
3. Define the user's likely inputs, expected outputs, runtime environment, and success criteria.
4. Put the shortest reliable workflow in `SKILL.md`.
5. Put detailed commands, parameters, errors, and examples in `references/`.
6. Add safety boundaries based on risk:
   - download/scrape/crawl: platform limits, copyright, private data;
   - tokens/keys/secrets: credential handling;
   - delete/write/upload/database: confirmation before destructive or external writes;
   - paid APIs/rate limits: cost and rate-limit warnings.
7. Generate 3-5 realistic prompt examples.
8. Validate the resulting skill folder.

## Validation

Run validation after creating or modifying a skill:

```bash
python scripts/quick_validate.py <skill-folder>
```

If the bundled validator cannot run, fix it to use only the Python standard library or explain the limitation clearly.

## References

- Skill quality checklist: `references/best-practices.md`
- Workflow design patterns: `references/workflows.md`
- Output patterns: `references/output-patterns.md`
- Codex-style interaction guidance: `references/interaction-guide.md`
