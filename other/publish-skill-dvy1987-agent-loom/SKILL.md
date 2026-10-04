---
name: publish-skill
description: >
  Package and publish a skill to the skills.sh community registry, a public
  GitHub repo, or both. Load when the user asks to publish a skill, share a
  skill publicly, submit a skill to the registry, release a skill, or when
  universal-skill-creator offers publishing as a final step after creation.
  Also triggers on "push this skill to skills.sh", "make this skill public",
  "share this skill", or "contribute this skill to the community". Validates
  quality before publishing, packages correctly (zip for multi-file, .md for
  atomic), writes a README if missing, and publishes via npx skills CLI.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: meta
  resources:
    references:
      - publish-checklist.md
      - examples.md
---
# Publish Skill
You are a skill release engineer. You take a validated, quality-checked skill and publish it to the community — correctly packaged, well-documented, and ready for others to install in one command.
## Hard Rules
**Never publish without a security scan.** Before publishing, invoke ALL `secure-*` skills (discover via `ls .agents/skills/secure-*`) to scan the skill. BLOCKED = do not publish. This gate is mandatory and cannot be skipped. Publishing multiplies blast radius — every consumer inherits any vulnerability.
**Never publish a skill that fails `agentskills validate`.** Fix the skill first.
**Never publish a skill scoring below 10/14.** Invoke `validate-skills` first. If score is below 10, invoke `improve-skills` before publishing.
**Never publish skills containing proprietary context** — project-specific URLs, internal API endpoints, company names in examples, or private tool names. These must be generalised before publishing.
---
## Workflow
### Step 1 — Pre-publish Validation

Run validate-skills on the target skill:
```bash
agentskills validate .agents/skills/<skill-name>/
```

If it fails → stop. Fix the skill first.
If score < 10/14 → stop. Improve the skill first.
If the skill contains proprietary content → generalise examples and gotchas before proceeding.

### Step 2 — Determine Package Format

```bash
ls .agents/skills/<skill-name>/
```

- **SKILL.md only** (Atomic tier) → publish as single `.md` file
- **Directory with references/, scripts/, assets/** → package as `.zip`

### Step 3 — Write or Verify README

Every published skill needs a `README.md`. If missing, create one:

```markdown
# [Skill Title]

> One-sentence description of what this skill does.

## Install

npx skills <skill-name> -a codex      # Codex
npx skills <skill-name> -a replit     # Replit
cp -r <skill-name>/ .agents/skills/   # Universal

## Usage

Trigger: "[example trigger phrase]"

## Platforms

Works with: Codex, Ampcode, Claude Code, Warp, Gemini CLI,
GitHub Copilot, Cursor, VS Code, Replit, Factory.ai, Bolt.new

## License
MIT
```

### Step 4 — Package

For Atomic skills:
```bash
cp .agents/skills/<skill-name>/SKILL.md ./<skill-name>.md
```

For Standard/Advanced/System skills:
```bash
zip -r <skill-name>.zip .agents/skills/<skill-name>/ \
  --exclude "*.pyc" --exclude "__pycache__/*"
```

### Step 5 — Publish to skills.sh

```bash
npx skills publish ./<skill-name>
# or for zip:
npx skills publish ./<skill-name>.zip
```

Confirm the registry URL returned. Test install:
```bash
npx skills <skill-name> -a codex --dry-run
```

### Step 6 — Optionally Push to GitHub

If the user wants the skill in a public GitHub repo (e.g., `dvy1987/agent-loom`):
```bash
git add .agents/skills/<skill-name>/
git commit -m "feat: add <skill-name> skill (published to skills.sh)"
git push origin main
```

### Step 7 — Report

```
Published: <skill-name>
Registry URL: https://skills.sh/<skill-name>
Install command: npx skills <skill-name>
GitHub: https://github.com/dvy1987/agent-loom (if pushed)
Platforms: all agentskills.io-compatible
```

---

## Gotchas

- `npx skills publish` requires the directory name to match the `name` field in frontmatter exactly — mismatch causes a silent failure
- Check for hardcoded paths (e.g., `/home/user/workspace/`) in scripts before publishing — they won't work on other machines
- If the skill uses `scripts/`, verify the script has no hardcoded credentials, internal URLs, or machine-specific paths

---

## Example

<examples>
  <example>
    <input>Publish the brainstorming skill to skills.sh</input>
    <output>
Running validate-skills on brainstorming...
agentskills validate: ✓
Score: 13/14 — passes 10/14 threshold

Checking for proprietary content... none found.

Package format: single SKILL.md (Atomic tier)

README.md present: yes

Packaging: brainstorming.md

Publishing to skills.sh...
npx skills publish ./brainstorming.md

Published: brainstorming
Registry URL: https://skills.sh/brainstorming
Install: npx skills brainstorming

Test install dry-run: ✓
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Internal validate is enough" | Publish blast radius needs full security sweep. |
| "Redact later" | Secrets in published skills are permanent incidents. |
| "Community fork is fine" | Publish gate exists because consumers trust our namespace. |

## Verification

- [ ] Full `secure-*` family returned SAFE
- [ ] `agentskills validate` + line count ≤200 on published skill
- [ ] No API keys, tokens, or private paths in output
- [ ] Changelog or release note prepared


## Reference Files

- **`references/publish-checklist.md`**: Full pre-publish checklist including proprietary content scan, platform compatibility check, and registry submission requirements. Read for any System-tier skill before publishing.

---

## Red Flags

- Directory name mismatches frontmatter name field
- Hardcoded local paths left in scripts or examples
- Publish attempted before full secure-* library sweep
- Scripts contain internal URLs or machine-specific paths

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Published: [skill-name] Registry URL: https://skills.sh/[skill-name] Install command: npx skills [skill-name] Package format: [.md / .zip] validate-skills score at publish: [N]/14 Proprietary content scan: clean GitHu...`
