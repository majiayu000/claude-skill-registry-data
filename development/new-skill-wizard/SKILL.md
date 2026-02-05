---
name: new-skill-wizard
description: Creates a new skill in the Powerhouse Lab skills library with proper git workflow. Use when the user wants to create a new skill, add a skill, build a skill, or says "new skill called X".
allowed-tools: Read, Write, Bash, Glob, Grep
---

# New Skill Wizard

You help users create new skills in the Powerhouse Lab skills library. You handle all the git workflow, file creation, and wiring automatically.

## WHEN TO ACTIVATE

Trigger on phrases like:
- "Create a new skill"
- "I want to make a skill for..."
- "New skill called..."
- "Add a skill"
- "Build a skill"

## THE PROCESS

### Step 1: Get the Basics

If the user hasn't provided these, ask ONE question at a time:

1. **Skill name** (kebab-case like `brand-voice` or `client-intake`)
2. **What it does** (one sentence)
3. **When to use it** (trigger phrases)

If they give you everything upfront, skip the questions.

### Step 2: Set Up Git (Do This Automatically)

```bash
cd ~/Documents/GitHub/powerhouse-lab
git checkout main
git pull origin main
git checkout -b skill/<name>
```

Tell them: "Created branch `skill/<name>` from latest main."

### Step 3: Create the Skill Files (Do This Automatically)

```bash
# Create skill folder with all optional subdirectories
mkdir -p skills/<name>/{scripts,references,resources,assets}

# Add .gitkeep files so empty folders are tracked
touch skills/<name>/scripts/.gitkeep
touch skills/<name>/references/.gitkeep
touch skills/<name>/resources/.gitkeep
touch skills/<name>/assets/.gitkeep
```

Create `skills/<name>/SKILL.md`:

```yaml
---
name: <name>
description: <their description>. Use when <their trigger phrases>.
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# <Name in Title Case>

## What This Does
<Their one-sentence description>

## Instructions

[We'll develop this together]

## Examples

[To be added after testing]

## Guidelines

- [To be defined]
```

**YAML Frontmatter Rules (Anthropic Spec):**

Only 4 fields are supported:

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | kebab-case, match directory name |
| `description` | Yes | What it does + when to use (max 1024 chars) |
| `allowed-tools` | No | **Tool names only** - not other skills |
| `model` | No | Specific Claude model if needed |

**`allowed-tools` contains ONLY actual tools:**
- Valid: `Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch`
- Valid patterns: `Bash(python:*)`, `WebFetch(domain:github.com)`
- **NOT valid**: Other skill names like `ai-slop-detector`

**Skill chaining:** If a skill says "run through ai-slop-detector" in the instructions,
Claude will invoke that skill automatically. Do NOT put other skills in `allowed-tools`.

**Keep SKILL.md under 500 lines.** Use progressive disclosure: essential instructions
in SKILL.md, detailed docs in `references/` folder.

**Folder structure created:**
```
skills/<name>/
├── SKILL.md        # The skill instructions
├── scripts/        # Executable Python/Bash (runs without loading into context)
├── references/     # Docs Claude loads when needed
├── resources/      # Templates and data files
└── assets/         # Binary files, images, logos
```

### Step 4: Wire It Up (Do This Automatically)

**4a: Create symlinks for all platforms:**
```bash
./scripts/setup-skills.sh
```

**4b: Register with Claude Code (CRITICAL):**
Add `"Skill(<name>)"` to `.claude/settings.local.json` in the `permissions.allow` array.

```bash
# Example: For a skill called "brand-voice"
# Add this line to settings.local.json:
"Skill(brand-voice)"
```

**Why this matters:** The symlinks make the skill *visible*, but Claude Code won't *use* it
unless it's registered in settings.local.json. This is the step that was missing and caused
inbox-triage to fail.

Tell them: "Skill is now wired up. You'll need to start a new terminal session for Claude Code to recognize it."

### Step 5: Develop the Content Together

Ask:
> Now let's build out what this skill actually does.
>
> When someone triggers this skill, what should I do step-by-step?

Work with them to fill in:
- Instructions (the core logic)
- Examples (what good output looks like)
- Guidelines (rules to follow)

Update the SKILL.md as you go.

### Step 6: Create Testing Plan

Before testing, create a testing plan the user (or an agent) can execute:

```markdown
## Testing Plan for <skill-name>

### Pre-flight Checks
- [ ] Skill appears in `.claude/skills/` symlinks
- [ ] Skill registered in `settings.local.json`
- [ ] New terminal session started (settings refresh)

### Skill Discovery Test
- [ ] Run: "What skills are available?"
- [ ] Expected: <skill-name> appears in list with correct description

### Basic Invocation Test
- [ ] Run: "<trigger phrase>"
- [ ] Expected: Skill activates, follows instructions

### Happy Path Test
- [ ] Input: <typical input scenario>
- [ ] Expected output: <what should happen>

### Edge Case Tests
- [ ] Empty input: <what should happen>
- [ ] Missing data: <what should happen>

### Integration Test (if skill uses other skills/tools)
- [ ] Verify dependent skills are also registered
- [ ] Test full workflow end-to-end
```

Save this plan to `skills/<name>/references/TESTING.md` so it persists.

**Lesson learned:** Always test the skill ALONE before testing it inside an agent.
If the skill doesn't work standalone, adding it to an agent won't fix it.

### Step 7: Execute Tests

Tell them:
> Ready to test! Start a fresh terminal session, then run through the testing plan.
> Come back and tell me what needs adjusting.

### Step 8: Publish (When They're Happy)

```bash
git add skills/<name>/
git commit -m "feat: Add <name> skill"
git push -u origin skill/<name>
git checkout main
git pull origin main
git merge skill/<name>
git push origin main
```

Tell them: "`<name>` is now live on main and available everywhere."

### Step 9: Claude.ai Upload (Ask First)

Ask: "Want me to package this skill for Claude.ai?"

If yes:
```bash
./scripts/package-skill.sh <name>
```

Tell them: "ZIP ready at `dist/<name>.zip`. Upload to Claude.ai → Settings → Features → toggle it ON."

**Note:** Claude.ai requires individual skill uploads (one ZIP per skill). Use `./scripts/package-all-skills.sh` to create ZIPs for all skills at once.

## IMPORTANT RULES

1. **Do the git and file setup automatically** - don't make them run commands
2. **Ask questions one at a time** - don't overwhelm
3. **Show them what you created** - paste the SKILL.md content so they can see it
4. **Keep iterating** - update the file as they refine the instructions
5. **Celebrate when done** - this is a big deal, they just shipped a skill!
