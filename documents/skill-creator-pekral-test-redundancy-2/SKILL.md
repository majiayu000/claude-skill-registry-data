---
name: skill-creator
description: "Use when creating a new Agent skill in this repository. Generates a SKILL.md that follows project conventions, passes skill-check validation, and updates the changelog and readme."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/php/core-standards.md` **only once it is established that the skill being created targets PHP code work in a PHP project** — skip it for a stack-agnostic or non-PHP skill; do not load the PHP standards when the new skill does not touch PHP.
- Apply `@rules/git/general.md`
- Output must be in English
- Do not modify other skills, rules, or production code
- Do not duplicate an existing skill — extend or refactor instead
- Never add behavior beyond what the requested skill needs

---

## Scope
Author a new Agent skill that fits this repository's conventions and ships ready for review.

Focus on:
- consistent frontmatter and section layout
- behavior aligned with `skill-check.config.json` limits
- clear Use when, Execution, and Done when sections
- no duplication with existing skills

---

## Use when
- A new Agent skill must be added to `skills/` for an AI agent workflow
- An existing workflow that lives only in chat history should be promoted to a reusable skill
- The user asks to "create a skill", "add a skill", or "scaffold a skill"

---

## Inputs the agent must collect
Before generating any file, gather:
- **Skill name** — kebab-case, ≤ 64 chars, unique under `skills/`
- **Purpose** — one sentence describing what the skill does
- **Trigger phrase** — the "Use when …" wording for the description
- **Scope** — read-only review, code change, refactor, delivery, or other
- **Required rules** — which `rules/**/*.md*` files the skill must apply
- **Integrations** — issue tracker, GitHub, MySQL, Telescope, etc. (or none)
- **Output expectations** — markdown report, code change, PR comment, etc.

If running interactively, confirm the inputs with the user. If running autonomously (e.g. invoked by `resolve-issue` or a scheduled workflow), infer the inputs from the triggering issue / PR description and state the assumptions in the final summary.

---

## Execution

### 1. Discover existing skills
- List `skills/` and read any skill whose name overlaps semantically with the request.
- If an existing skill already covers the workflow, stop and propose an update to that skill instead of creating a new one.

### 2. Choose the slug and location
- Slug must be kebab-case, ≤ 64 chars, and not collide with an existing folder under `skills/`.
- Create `skills/<slug>/SKILL.md`. Add a subfolder only when the skill genuinely needs one — see the layout below.

**Directory layout (Anthropic's recommended structure).** A skill is a directory whose entrypoint is `SKILL.md`; every other file is optional and exists so `SKILL.md` stays the overview rather than the whole payload ([skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Claude Code skills](https://code.claude.com/docs/en/skills)):

```text
<slug>/
├── SKILL.md          # required — instructions and navigation
├── references/       # detailed material Claude reads on demand
├── scripts/          # utilities Claude executes, never loads into context
└── templates/        # output shapes and examples Claude fills in
```

The rules that make the split work, each one load-bearing:

- **Progressive disclosure.** Keep the `SKILL.md` body under 500 lines (this repo's `skill-check.config.json` enforces the same limit) and move detail into a sibling file rather than growing the body. A referenced file costs nothing until it is read.
- **References stay one level deep.** Every supporting file links directly from `SKILL.md`. A file that is only reachable through another file gets partially read (`head -100`) instead of read whole.
- **Say whether a script is executed or read.** *"Run `scripts/validate.sh`"* and *"see `scripts/validate.sh` for the algorithm"* are different instructions; execution is the default because it is cheaper and more reliable than regenerating the logic.
- **Name files for their content and forward-slash every path.** `references/finance.md`, never `docs/file2.md`; `scripts/helper.sh`, never `scripts\helper.sh`.
- **A reference file over 100 lines opens with a table of contents**, so a partial read still shows the full scope.

Keep the folder names above rather than inventing synonyms — `references/`, `scripts/`, `templates/` are what the existing skills in this repo already use, and a consistent tree is what makes a skill portable to another Agent Skills host.

### 3. Write the frontmatter
Required keys:

```yaml
---
name: <slug>
description: "Use when <trigger phrase>. <one sentence on scope>."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---
```

Rules from `skill-check.config.json`:
- `description`: 50–1024 chars; should start with "Use when"
- `name`: ≤ 64 chars
- Body: ≤ 500 lines and ≤ 5000 tokens

Portability rules from the Agent Skills spec — a skill that breaks one of these stops loading on another host even though `skill-check` passes:
- `name`: lowercase letters, numbers, and hyphens only; no XML tags; never the reserved words `anthropic` or `claude`. It must match the directory name, which is what the `/<slug>` invocation resolves from.
- `description`: non-empty, ≤ 1024 chars, no XML tags, written in the **third person** ("Resolves…", never "I can help you…"). It is injected into the system prompt and is the only thing a host sees before deciding to load the skill, so it states both *what the skill does* and *when to use it*. The repo's "Use when …" opening satisfies the *when* half — keep the *what* in the same sentence.

### 4. Compose the body
The repo accepts two body layouts. Pick one and stay consistent within the file.

**Layout A — Constraints-first (preferred for new skills):**

1. `## Constraints` — applied rules and hard limits (one bullet per item)
2. `## Scope` *(optional)* — what the skill covers, what it deliberately leaves to another skill, and the focus areas it works through. Write it only when the skill carries scope the `description:` field does not already state; never restate the frontmatter here.
3. `## Use when` — concrete triggers
4. `## Required approach` or `## Execution` — numbered steps the agent must follow
5. `## Output` or `## Output Format` — structure of what the skill returns
6. `## Done when` — verifiable completion criteria

Examples in the repo: `refactor-entry-point-to-action`, `smartest-project-addition`, `test-driven-development`, `tester-cookbook`, `security-review`.

**Layout B — Title + Purpose (legacy, still acceptable):**

1. `# <Title Case Name>`
2. `## Purpose` — one short paragraph plus a bullet list of focus areas
3. `## Constraints`
4. `## Execution`
5. `## Output` or `## Output Format`
6. `## Principles` — short guiding rules (optional)
7. `## Done when`

Layout B is documented only so a skill imported from elsewhere in this shape is still recognized; never pick it for a new skill.

Omit a section only when it does not apply.

### 5. Reference rules and other skills
- Reference rule files as `@rules/<area>/<file>.md` exactly as they exist on disk.
- Reference other skills as `@skills/<slug>/SKILL.md`.
- Never invent paths. Verify every reference points to a real file before saving.

### 6. Keep behavior minimal
- One skill, one workflow. Split into separate skills if the scope grows.
- Do not paste rule content into the skill — link to it.
- Do not add humanizer, marketing, or third-party links unless the user requests them.

---

## Quality Gates
Run before declaring the skill done:
- `composer skill-check` — must report `PASS` with no warnings on the new file
- If `skill-check` flags an auto-fixable warning, run `npx skill-check check skills/<slug> --fix --no-security-scan` (path-scoped) instead of `composer skill-check-fix`, which rewrites every skill in the tree and can pollute the diff with unrelated formatting changes
- The full build is **not** run here — the project's gate runs once at the end of the work (`@skills/resolve-issue/references/quality-gates.md` *Gate placement — deferred to the merge boundary*), and `composer skill-check` above is a diff-scoped check, not that gate

Do not silence checks; fix the SKILL.md content until the report is clean.

---

## Repository updates
After the new SKILL.md passes validation:
- Add a `CHANGELOG.md` entry under `[Unreleased]` describing the new skill and referencing the issue (e.g. `(#432)`).
- Update `README.md`:
  - bump the skill count in the "Why This Package" bullet

Skip the README update only when the skill is intentionally internal and not part of the public catalog — state this explicitly in the PR description.

---

## Output

- New file: `skills/<slug>/SKILL.md`
- Updated `CHANGELOG.md` and `README.md`
- Short summary covering:
  - chosen slug and scope
  - rules and skills referenced
  - skill-check result
  - follow-up tasks (e.g. tests for code that the skill orchestrates) if any

---

## Principles

- Reuse existing skills before adding new ones
- Keep each skill narrow and composable
- Prefer explicit steps over vague guidance
- Verify every `@rules/*` and `@skills/*` reference exists
- Let `skill-check` be the source of truth for SKILL.md quality

---

## Done when
- `skills/<slug>/SKILL.md` exists with valid frontmatter and required sections
- `composer skill-check` passes with no warnings on the new file
- `CHANGELOG.md` and `README.md` reflect the new skill (or the omission is justified)
- The summary lists the slug, references, and validation result

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
