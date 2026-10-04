---
name: skill-md-adoption
description: >-
  SKILL.md is an open specification released by Anthropic in 2025 that
  standardizes how tools discover and auto-invoke procedural knowledge (skills,
  patterns, guides, rules). Instead of each tool (Claude, Cursor, VSCode, CLI)
  maintaining isolated skill registries, SKILL.md enables a single skill to be
  published once and auto-invoked across any tool that speaks the spec.
---

# SKILL.md Adoption: Vendor-Neutral Skill Discovery

SKILL.md is an open specification released by Anthropic in 2025 that standardizes how tools discover and auto-invoke procedural knowledge (skills, patterns, guides, rules). Instead of each tool (Claude, Cursor, VSCode, CLI) maintaining isolated skill registries, SKILL.md enables a single skill to be published once and auto-invoked across any tool that speaks the spec.

> _Analog: npm packages aren't Node-specific—they work in browsers, Deno, and serverless runtimes. SKILL.md does for procedural knowledge what package specs do for code: decouple the artifact from the runtime._

## Why SKILL.md matters

**Before**: Skills were vendor silos. A "deployment checklist" skill lived in Claude's `.claude/skills/`, and Cursor had its own copy in `.cursor/skills/`. Updates didn't sync. Different formats. No discovery API.

**After**: One SKILL.md published to a shared registry. Claude, Cursor, VSCode, and CLI tools discover it via `forge-kit install`, call it with the same trigger phrase, and get identical behavior.

## The SKILL.md format

A SKILL is a Markdown file with frontmatter + structured sections. Minimal viable example:

```markdown
---
name: validate-commit-msg
description: Check commit messages against team conventions.
triggers:
  - "validate commit"
  - "check message"
  - "commit lint"
version: "1.0.0"
---

# Validate Commit Message

Ensures commits follow the [Conventional Commits](https://conventionalcommits.org) standard.

## Purpose

Catch malformed commit messages before they land in the repo. Saves code review friction and maintains a searchable git log.

## Invocation

- **Claude**: `validate commit`
- **Cursor**: Trigger inline, or use Command Palette
- **CLI**: `forge-kit invoke validate-commit-msg <message>`

## Example

\`\`\`bash
# Bad message (triggers validation failure)
$ git commit -m "fixed bug"

# Good message (passes validation)
$ git commit -m "fix(auth): prevent session hijack on refresh"
\`\`\`

## When NOT to use

- Manual pre-commit hooks already exist and are working well.
- The team doesn't use Conventional Commits.
- Messages are freeform and policy is unclear.

## Implementation

The skill body describes the logic (pseudocode, links to external validators, or shell commands). Tools that consume the skill translate the `triggers` into their native hotkey/command system.

\`\`\`bash
# Pseudocode
if message matches /^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?:/
  return "PASS"
else
  return "FAIL: Use Conventional Commits format"
\`\`\`
```

### Frontmatter fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | slug | ✅ | Unique identifier, no spaces. Used in URLs and CLI. |
| `description` | string | ✅ | One-liner. Shown in registries and search results. |
| `triggers` | array | ✅ | Natural-language phrases. Tools bind these to hotkeys. Min 1. |
| `version` | semver | optional | Defaults to `1.0.0`. Update on any change. |
| `deprecated` | date | optional | Format `YYYY-MM-DD`. Signals EOL; tools show warning. |
| `author` | string | optional | Name or handle of original author. |
| `tags` | array | optional | `[orchestration, security, testing, cli]` etc. for filtering. |
| `applies_to` | array | optional | `[claude, cursor, cli, vscode]`—which tools support this skill. |
| `migration_target` | string | optional | If deprecated, link to replacement skill `name`. |

### Body structure (recommended sections)

1. **Purpose** — Why this skill exists. What problem does it solve?
2. **Invocation** — How tools trigger it. Show all platforms if multi-tool.
3. **Example** — Real usage. Input → Output.
4. **When NOT to use** — Anti-patterns or edge cases where the skill fails.
5. **Implementation** — Pseudocode, links to validators, or shell commands.
6. **Troubleshooting** — Common errors and fixes (optional but helpful).

Keep the body **under 300 lines** for readability. Link to external docs rather than paste long reference material.

---

## Registry discovery models

No central authority. Instead, tools discover skills via convention:

### Per-tool directories (fastest)

\`\`\`
~/.claude/skills/<name>/SKILL.md          # Claude
.cursor/skills/<name>/SKILL.md            # Cursor
.codex/skills/<name>/SKILL.md             # Codex (VSCode)
~/.local/share/forge-kit/skills/<name>.md # CLI (Linux/macOS)
\`\`\`

Tools scan their home directory on startup or on-demand with \`skills find\` or \`Cmd+K skills\`.

### Registry API (forward-looking)

When the ecosystem matures, tools will query a central HTTP registry (model: npm registry, but read-only and signed). Anthropic hosts the reference implementation.

\`\`\`bash
# Future CLI usage
$ forge-kit install validate-commit-msg
# Fetches from registry, verifies signature, caches locally.

$ skills find orchestration
# Searches descriptions + tags across installed + registry.
\`\`\`

### Cross-tool sync (chezmoi/dotfiles pattern)

For teams: Keep skills in a git repo (e.g., \`dotfiles/\`) with chezmoi:

\`\`\`bash
# In dotfiles repo
mkdir -p dot_claude/skills/validate-commit-msg
echo "---\nname: validate-commit-msg\n---\n..." > dot_claude/skills/validate-commit-msg/SKILL.md

# In .chezmoi.toml.tmpl
[copy]
  glob = true

# chezmoi apply syncs all skills to ~/.claude/skills/
\`\`\`

Teams can now version-control, review, and release skills as a group.

---

## Versioning and deprecation

### Version semantics

Use semantic versioning. Increment \`version\` in frontmatter:

- **Patch** (1.0.1): Typo fixes, clarification in description.
- **Minor** (1.1.0): New trigger phrase, new section in body, new example.
- **Major** (2.0.0): Breaking change in trigger names, invocation, or output format.

Tools that auto-update can respect \`^1.0.0\` constraints (npm-style).

### Soft deprecation

Instead of deleting a skill, mark it deprecated:

\`\`\`yaml
---
name: old-validator
deprecated: "2025-05-01"
migration_target: "validate-commit-msg"
---
\`\`\`

Tools show a warning: **"This skill is deprecated (since May 1, 2025). Use 'validate-commit-msg' instead."** The skill still works but signals to users it's end-of-life.

---

## Security review for skills

Skills are executable by definition. Before installing or publishing, consider:

### Trigger-phrase injection

If a skill's trigger is \`"run command"\` or \`"execute"\`, malicious data could trigger it unintentionally. **Fix**: Use specific, multi-word triggers. \`"validate commit message"\` is better than \`"validate"\`.

\`\`\`yaml
# Bad: Too broad
triggers:
  - "do it"
  - "run"

# Good: Specific and multi-word
triggers:
  - "validate commit message"
  - "check conventional format"
\`\`\`

### Auth scope leakage

If a skill uses environment variables or config files, document what it accesses:

\`\`\`yaml
---
name: deploy-to-prod
requires:
  - "AWS_ACCESS_KEY_ID"
  - "GITHUB_TOKEN"
---
\`\`\`

Tools can warn users: **"This skill needs access to AWS and GitHub credentials. Allow (Y/n)?"**

### Registry signing (forward-looking)

When a central registry launches, skills will be signed with Ed25519 keys. Tools verify signatures before auto-invocation, preventing supply-chain attacks (SBOM model).

\`\`\`bash
# Future: Tool verifies signature
$ forge-kit install validate-commit-msg
Fetching from registry...
✓ Signature valid (author: anthropic)
✓ Installed: ~/.claude/skills/validate-commit-msg/SKILL.md
\`\`\`

For now, distribute skills via signed git commits or signed releases on GitHub.

---

## Anti-patterns to avoid

### 1. One skill doing too much

Bad: A single "development workflow" skill that validates, deploys, tests, and commits.

Good: Five focused skills—one per task. Chain them in a \`workflow\` (separate artifact type) if coordination is needed.

### 2. Overlapping triggers

Bad: Two skills both triggered by \`"test"\`.

\`\`\`yaml
# skill1.md
triggers: ["test", "run tests", "validate"]

# skill2.md
triggers: ["test", "run validation"]
\`\`\`

Tools won't know which to invoke. **Fix**: Make triggers specific and non-overlapping.

\`\`\`yaml
# skill1.md
triggers: ["run unit tests", "test coverage"]

# skill2.md
triggers: ["validate types", "check lint"]
\`\`\`

### 3. Hard-coded personal paths

Bad: A skill body references \`/Users/yourname/projects/\`.

\`\`\`markdown
## Example

# Run tests in /Users/jdoe/projects/api
$ cd /Users/jdoe/projects/api && npm test
\`\`\`

This skill is not portable. **Fix**: Use relative paths, environment variables, or ask the user for input.

\`\`\`markdown
## Example

# Run tests in the current project
$ npm test

# Or specify a different path
$ npm test --dir ./api
\`\`\`

### 4. Missing implementation details

Bad: A skill says "Validate code" but the body just links to an external tool.

Good: Include pseudocode or a shell command snippet so users understand what happens.

### 5. No deprecation plan

If you rename a skill or realize it's a mistake, mark it deprecated and point to a replacement. Don't ghost users.

---

## Links

- [OWASP LLM Top 10: Prompt Injection](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — Understanding injection risks in skill triggers and bodies.
- [packages/core/patterns/prompt-injection-defense.md](prompt-injection-defense.md) — Layered strategies for securing skill execution.
- [packages/core/best-practices/ai-skill-stewardship.md](../packages/core/best-practices/ai-skill-stewardship.md) — Governance, versioning, and team workflows for shared skill repos.

---

## Checklist: Before publishing a skill

- [ ] Frontmatter complete: \`name\`, \`description\`, \`triggers\` (min 1), \`version\`.
- [ ] Body has: Purpose, Invocation, Example, When NOT to use, Implementation.
- [ ] Triggers are specific and non-overlapping with existing skills.
- [ ] No hard-coded personal paths; uses relative paths or env vars.
- [ ] Implementation is clear (pseudocode or real commands, not just links).
- [ ] If it requires auth, \`requires\` field lists env vars or files.
- [ ] Linted: no broken links, valid YAML frontmatter.
- [ ] Tested: tried from at least one tool (Claude, Cursor, or CLI).
- [ ] Published to all 4 locations (EN toolkit, PT mirror, \`~/.claude/skills/\`, dotfiles).
