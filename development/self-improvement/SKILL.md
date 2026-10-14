---
name: self-improvement
description: Enables agent self-reflection and learning from mistakes through systematic skill updates. Prioritizes updating existing skills over creating new ones - always searches existing skills first, creates new skills only when justified. Includes upstream source sync workflow for tracking and updating skills from databricks/databricks-agent-skills. Use after encountering errors, completing complex tasks, or when asked to reflect, learn, or document a mistake. Triggers on "learn from this", "don't repeat", "remember this pattern", "what went wrong", "update skills", "capture this learning", "document mistake", "prevent this error", "databricks-agent-skills updated", "upstream changed", "sync with databricks-agent-skills".
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Self-reflection meta-skill — updates/creates `SKILL.md` files in the repo skill tree; no deployed resource and no deploy verb. Client-agnostic. On Genie Code, the repo skill tree lives under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`); write skill edits there, not a bare relative path — relative paths resolve against the page CWD (see `skills/genie-code-environment` §8)."
coverage: full
metadata:
  version: "1.4.0"
  author: prashanth subrahmanyam
  domain: admin
  role: utility
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal workflow
---

# Agent Self-Improvement

A systematic framework for self-reflection, learning from mistakes, and continuous improvement through skill creation.

## Core Principle

**Every error is a learning opportunity. Every learning becomes a skill.**

The virtuous loop: **Reflect → Capture → Generalize → Create/Update Skill → Apply**

---

## When to Trigger Self-Reflection

### Automatic Triggers (Agent-Initiated)

Initiate self-reflection when ANY of these occur:

| Trigger | Signal | Action |
|---------|--------|--------|
| **Error repetition** | Same error type 2+ times in session | Search existing skills → Update or create |
| **Debugging spiral** | 3+ attempts to fix same issue | Search existing skills → Update or create |
| **Silent failure** | Code ran but produced wrong results | Search existing skills → Update or create |
| **Assumption failure** | Assumed X, reality was Y | Search existing skills → Update or create |
| **Documentation gap** | Official docs contradicted expectation | Search existing skills → Update or create |
| **Overengineering** | Complex solution replaced by simple one | Search existing skills → Update or create |

**Key principle:** The action is ALWAYS "search existing skills first" before any skill modification.

### Proactive Triggers (Freshness & Platform Awareness)

These triggers are **proactive** — they don't require an error to fire. They keep skills current.

| Trigger | Signal | Action |
|---------|--------|--------|
| **Periodic review** | User says "audit skills" or "check freshness" | Run `admin/skill-freshness-audit` skill |
| **Platform release** | User says "Databricks released X" or "new MLflow version" | Find affected skills by domain → fetch verification_sources → flag drift |
| **Upstream updated** | User says "databricks-agent-skills updated" or "upstream changed" | Find skills with `upstream_sources` referencing databricks-agent-skills → fetch upstream → compare → flag drift |
| **Documentation change** | WebFetch returns different API pattern than skill documents | Flag skill for update, log drift details in drift report |
| **Pre-task verification** | Loading a high-volatility skill for implementation | Check `last_verified` age; if stale (>30 days for high), suggest quick verification |
| **Post-implementation review** | Completed a task using a skill | If skill patterns needed adjustment, update the skill and `last_verified` |

**Cross-reference:** For the full audit workflow, see `admin/skill-freshness-audit/SKILL.md`.

### User-Initiated Triggers

Respond to phrases like:
- "Learn from this mistake"
- "Don't do this again"
- "Remember this for next time"
- "Document what went wrong"
- "Add this to your learnings"
- "Create a skill from this"
- "Audit skills" / "Check freshness" (→ delegates to `skill-freshness-audit`)
- "Databricks released X" / "New MLflow version" (→ platform release audit)
- "databricks-agent-skills updated" / "Upstream changed" / "Sync with databricks-agent-skills" (→ upstream sync workflow)

---

## Self-Reflection Workflow

### Step 1: Recognize the Learning Moment

Ask yourself these questions:
```
1. What went wrong? (or what almost went wrong?)
2. What was the root cause?
3. What assumption was incorrect?
4. How did I discover the issue?
5. What would have prevented this?
```

### Step 2: Search Existing Skills First (MANDATORY)

**Before considering a new skill, ALWAYS search existing skills thoroughly.**

```bash
# Step 2a: List all existing skills
find data_product_accelerator/skills -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {}

# Step 2b: Search skill descriptions for related terms
grep -ri "keyword1\|keyword2\|keyword3" data_product_accelerator/skills/*/SKILL.md

# Step 2c: Read potentially related skills in full
cat data_product_accelerator/skills/{potential-match}/SKILL.md
```

**Analysis checklist before proposing ANY new skill:**

- [ ] Listed all existing skills in the repository
- [ ] Searched descriptions for related keywords (error type, technology, pattern)
- [ ] Read at least 3 potentially related skills in full
- [ ] Confirmed no existing skill covers this pattern (even partially)
- [ ] Confirmed this isn't a sub-case of an existing skill

**Decision matrix:**

| Finding | Action |
|---------|--------|
| Existing skill covers this exactly | No action needed - apply the skill |
| Existing skill covers this partially | **Update existing skill** with new case |
| Existing skill covers related pattern | **Update existing skill** with new section |
| Multiple skills could be extended | **Update the most relevant one** |
| No existing skill is even remotely related | Consider new skill (proceed to Step 3) |

### Step 3: Generalize the Learning

Transform specific errors into universal, reusable patterns:

| Specific Error | Generalized Skill |
|----------------|-------------------|
| "Metric view `name` field not supported in v1.1" | `api-version-validation` - Always verify API fields against current docs |
| "Module imports fail in Asset Bundle notebooks" | `isolated-execution-patterns` - Inline dependencies in isolated environments |
| "`argparse` fails in notebook_task" | `platform-parameter-passing` - Verify platform-specific parameter mechanisms |

### Step 4: Update Existing Skill (Strongly Preferred)

**Default action: UPDATE an existing skill. New skills are the exception, not the rule.**

```
After completing Step 2 search, decide:

Can ANY existing skill be reasonably extended?
│
├── YES (90% of cases) → UPDATE the existing skill
│   ├── Add new example to "Common Symptoms" or examples
│   ├── Add new trigger to "When to Use" section
│   ├── Add new item to "Prevention Checklist"
│   ├── Add new subsection under "The Solution" if needed
│   └── Update description to include new trigger keywords
│
└── NO (only after thorough search) → CREATE new skill
    ├── Must pass "New Skill Justification" checklist below
    ├── Use skill template
    ├── Name: kebab-case, descriptive
    └── Location: skills/{skill-name}/SKILL.md
```

**New Skill Justification Checklist (ALL must be true):**

- [ ] Searched ALL existing skills (listed them, searched keywords)
- [ ] Read at least 3 potentially related skills in full
- [ ] This pattern is fundamentally different from all existing skills
- [ ] Cannot reasonably be added as a section to any existing skill
- [ ] The new skill would have distinct trigger keywords
- [ ] The new skill covers a pattern likely to recur (not one-off)

### Step 5: Apply Proactively

Before starting similar tasks:

1. **Scan relevant skills** in `data_product_accelerator/skills/`
2. **Apply prevention patterns** from skill instructions
3. **Reference skill** during implementation

---

## Skill Creation Template

When creating a new skill from a learning, use this structure:

```markdown
---
name: {kebab-case-name}
description: {What it does}. {When to use it}. Use when {trigger scenarios}.
---

# {Skill Title}

{One-line overview of what this skill prevents or enables.}

## When to Use

- {Trigger scenario 1}
- {Trigger scenario 2}
- {Trigger scenario 3}

## The Problem

{Brief description of the error/issue this skill addresses.}

### Root Cause
{Why this happens - the underlying technical reason.}

### Common Symptoms
- {Error message or behavior 1}
- {Error message or behavior 2}

## The Solution

{Clear instructions for the correct approach.}

### Correct Pattern
\`\`\`python
# Example of the right way
\`\`\`

### Incorrect Pattern (Avoid)
\`\`\`python
# Example of what NOT to do
\`\`\`

## Prevention Checklist

- [ ] {Actionable check 1}
- [ ] {Actionable check 2}
- [ ] {Actionable check 3}

## Generalized Principle

> **Key Insight:** {One-sentence universal takeaway}

{Broader lesson that applies beyond this specific case.}
```

---

## Skill Categories

Skills fall into three main categories. See [assets/skill-template.md](assets/skill-template.md) for full template.

### Error Prevention Skills
Prevent recurring technical errors. Include specific error messages, clear correct/incorrect patterns, and actionable checklists.

**Example:** `notebook-import-patterns` - Prevents import failures from Databricks notebook headers. Key insight: Platform-specific file formats may break standard language features.

### Assumption Correction Skills
Correct common misconceptions. Emphasize expectation vs reality, include verification commands.

**Example:** `databricks-naming-conventions` - Prevents table name errors. Key insight: Naming conventions vary by layer and project - always verify with `SHOW TABLES`.

### Simplification Skills
Document simpler approaches discovered after complex workarounds failed.

**Example:** `avoid-sys-path-manipulation` - Recognizes when 3+ workaround attempts signal misunderstanding. Key insight: Complex workarounds signal misunderstanding - find the simple solution.

---

## Reflection Prompts

Use these prompts to guide self-reflection:

### After Errors
```
I just encountered an error. Let me reflect:
- What was the error message?
- What did I try that didn't work?
- What finally worked?
- What assumption was wrong?
- Should I create a skill to prevent this?
```

### After Successful Complex Tasks
```
This task is complete. Let me capture learnings:
- What was harder than expected?
- What would I do differently next time?
- Did I discover any new patterns?
- Should this become a new skill or update an existing one?
```

### After Long Debugging Sessions
```
I spent significant time debugging. Let me document:
- What was the root cause?
- What led me astray?
- What was the breakthrough insight?
- What skill would have prevented this?
```

### After Platform Updates
```
A new version of Databricks/MLflow was released. Let me check:
- Which skills reference the updated product? (check volatility-classification.md)
- Are there API signature changes? (fetch verification_sources URLs)
- Do any code patterns need updating?
- Should I run the skill-freshness-audit?
- Which high-volatility skills are now potentially stale?
```

### Before Using a High-Volatility Skill
```
I'm about to use a high-volatility skill. Quick freshness check:
- When was this skill last_verified? (check frontmatter)
- Is it older than 30 days? If so, suggest verification first.
- Are there verification_sources I can quickly fetch?
- Does the skill's version history show recent updates?
```

### After a Databricks Agent Skills Update
```
The databricks-agent-skills upstream has been updated. Let me sync:
- Which skills have upstream_sources pointing to databricks-agent-skills? (check lineage map)
- What changed in the upstream files? (WebFetch raw GitHub URLs)
- Do any of our skills need updating based on upstream changes?
- For derived/extended skills: are there new patterns we should adopt?
- For reference skills: have any API signatures changed?
- Update last_synced and sync_commit after syncing each skill
```

---

## Upstream Source Sync Workflow

Skills in this repository track their lineage to `databricks/databricks-agent-skills` via `upstream_sources` metadata in their frontmatter. This workflow describes how to sync skills when the upstream changes.

**Lineage Map:** See `admin/skill-freshness-audit/references/databricks-agent-skills-lineage-map.md` for the complete mapping.

### When to Sync

- User says "databricks-agent-skills updated", "sync with databricks-agent-skills", or "upstream changed"
- After a known databricks-agent-skills release or major commit
- During periodic freshness audits (check `last_synced` staleness)
- When a skill with upstream sources produces incorrect patterns

### Sync Workflow

```
1. IDENTIFY affected skills:
   a. Read the lineage map (admin/skill-freshness-audit/references/databricks-agent-skills-lineage-map.md)
   b. OR: Glob all SKILL.md files and read upstream_sources from frontmatter
   c. Filter to skills where upstream_sources is non-empty

2. FETCH upstream content:
   a. For each upstream path, construct the raw GitHub URL:
      https://raw.githubusercontent.com/{repo}/main/{path}
   b. WebFetch each URL to get the current upstream content
   c. Note the latest commit hash for sync_commit tracking

3. COMPARE upstream against our skill:
   a. Check for new patterns, sections, or capabilities in upstream
   b. Check for deprecated approaches still present in our skill
   c. Check for API signature changes (function names, parameters)
   d. Check for new best practices or warnings

4. REPORT differences:
   a. Use the Upstream Drift Report format from skill-freshness-audit
   b. Classify each difference by impact (high/medium/low)
   c. Prioritize derived > extended > reference relationships

5. APPLY updates (with human approval):
   a. Update skill content to incorporate upstream changes
   b. Preserve our custom extensions and additions
   c. Update frontmatter: last_synced date and sync_commit hash
   d. Update last_verified date
   e. Bump version if substantive changes were made
```

### Priority Order for Syncing

| Relationship | Priority | How to Sync |
|---|---|---|
| `derived` | High | Our skill directly draws from upstream. Align closely with upstream patterns. |
| `extended` | Medium | Our skill extends upstream. Adopt new base patterns, keep our extensions. |
| `inspired` | Low | Heavily customized. Only check for major direction changes. |
| `reference` | Low | Original content. Only verify API/pattern accuracy. |

### After Syncing a Skill

Update the skill's frontmatter:

```yaml
metadata:
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-agent-bricks/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"    # ← Update to today's date
      sync_commit: "ca92a6c"       # ← Update to latest upstream commit
```

### Key Principles

- **Never blindly copy upstream.** Our skills are extended/customized. Upstream is a source of truth for base patterns, not a replacement for our content.
- **Preserve our extensions.** When upstream adds new patterns, merge them alongside our existing additions.
- **Human approval required.** Always report differences and wait for approval before modifying skill content.
- **Update metadata even if no content changes.** If upstream hasn't changed since last sync, still update `last_synced` to prove it was checked.

---

## Skill Update vs New Skill

**Philosophy: Fewer, richer skills are better than many thin skills.**

A repository with 5 comprehensive skills is more valuable than 20 narrow ones. Each new skill adds discovery overhead. Prefer depth over breadth.

### Update Existing Skill (Default - 90% of cases)

Update when ANY of these are true:
- Same technology or domain (even if different error)
- Related pattern (even if different symptom)
- Could be a subsection of existing skill
- Shares trigger keywords with existing skill
- User would reasonably look for this in an existing skill

**How to update:**
```markdown
## The Solution

[Existing content stays...]

### Additional Pattern: {New Pattern Name}

**Discovered:** YYYY-MM-DD

{Description of new pattern}

#### Symptoms
- {New symptom 1}
- {New symptom 2}

#### Fix
{How to resolve}
```

### Create New Skill (Exception - Only After Thorough Search)

Create new ONLY when ALL of these are true:
- [ ] Fundamentally different domain/technology
- [ ] No existing skill shares trigger keywords
- [ ] Cannot logically fit as a section in any existing skill
- [ ] Pattern is significant and will recur
- [ ] Completed "New Skill Justification Checklist" (see Step 4)

---

## Virtuous Loop Checklist

After each significant task or error, run through this checklist:

```
Self-Improvement Checkpoint:

1. RECOGNIZE: Did something noteworthy happen?
   - [ ] Encountered an error (repeated or significant)
   - [ ] An assumption failed
   - [ ] Overcomplicated something
   - [ ] Docs/examples misled me

2. SEARCH EXISTING SKILLS (mandatory before any skill changes):
   - [ ] Listed all skills: find data_product_accelerator/skills -name "SKILL.md"
   - [ ] Searched for related keywords in skill descriptions
   - [ ] Read potentially related skills in full

3. DECIDE (update is the default):
   - [ ] Can this be added to an existing skill? → UPDATE IT
   - [ ] Only if no existing skill fits → Consider new skill
   - [ ] Completed New Skill Justification Checklist? → Create it
```

---

## Quick Skill Creation

### Create New Skill Directory
```bash
SKILL_NAME="your-skill-name"
mkdir -p "data_product_accelerator/skills/${SKILL_NAME}"
cat > "data_product_accelerator/skills/${SKILL_NAME}/SKILL.md" << 'EOF'
---
name: your-skill-name
description: What this skill does. When to use it. Trigger phrases.
---

# Skill Title

Overview of what this skill prevents or enables.

## When to Use

- Trigger scenario 1
- Trigger scenario 2

## The Problem

Description of the error/issue.

## The Solution

Clear instructions for the correct approach.

## Prevention Checklist

- [ ] Check 1
- [ ] Check 2

## Generalized Principle

> **Key Insight:** One-sentence takeaway.
EOF
echo "Created: data_product_accelerator/skills/${SKILL_NAME}/SKILL.md"
```

### List Existing Skills
```bash
# List all skills in project
find data_product_accelerator/skills -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {}
```

### Search Skills by Description
```bash
# Find skills related to "import"
grep -l "import" data_product_accelerator/skills/*/SKILL.md 2>/dev/null
```

---

## Additional Resources

- [Skill Template](assets/skill-template.md) - Copy-paste skill template
- [Create Skill Script](scripts/create-skill.sh) - Interactive skill creation
- [Learning Format Reference](references/LEARNING-FORMAT.md) - Standardized learning capture format

---

## Reference Files

This skill includes the following reference files:

- **assets/skill-template.md** - Complete skill template for creating new skills
- **scripts/create-skill.sh** - Interactive bash script for skill creation
- **references/LEARNING-FORMAT.md** - Standardized format for capturing learnings

---

## Summary

**The core loop:**
1. **Reflect** - Recognize learning moments (errors, surprises, simplifications)
2. **Search** - Thoroughly search existing skills for related patterns
3. **Generalize** - Extract universal principles
4. **Update (preferred) or Create** - Extend existing skills; new skills only when justified
5. **Apply** - Use skills proactively in future work

**Key principles:**

- **Search before create:** Always search existing skills before proposing a new one
- **Update is the default:** 90% of learnings should update existing skills
- **Fewer, richer skills:** 5 comprehensive skills > 20 narrow skills
- **Justify new skills:** New skills require completing the justification checklist

**Remember:** A learning captured in the right skill prevents the same mistake forever. An uncaptured learning guarantees repetition. But skill sprawl creates discovery problems—keep skills consolidated.
