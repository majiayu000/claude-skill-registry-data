---
name: initialize-governance
description: Initialize complete governance framework in a project - creates constitution, roadmap, directory READMEs, and issue/spec templates with guided setup process
---

# Initialize Governance Framework

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: initialize-governance | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: initialize-governance | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



You are setting up a complete project governance framework to ensure perfect alignment between AI assistant and human partner on design principles, strategic direction, and tactical execution.

## Purpose

This skill creates the three-tier governance hierarchy:
1. **Constitution** (`CONSTITUTION.md`) - Immutable design principles
2. **Roadmap** (`ROADMAP.md` + `ROADMAP_NEXT_STEPS.md`) - Strategic + tactical plans
3. **Process Documentation** (README files, templates) - Operational guidance

## Initialization Process

### Phase 1: Discovery and Planning

**1. Detect Project Structure**

Use Bash to check current state:

```bash
# Check for git repository
git rev-parse --show-toplevel

# Check for existing wrangler workspace
ls -la .wrangler/ 2>/dev/null || echo "No .wrangler directory"

# Check for existing governance docs
[ -f .wrangler/CONSTITUTION.md ] && echo "Constitution exists" || echo "No constitution"
[ -f .wrangler/ROADMAP.md ] && echo "Roadmap exists" || echo "No roadmap"
```

**2. Ask User for Project Context**

Use AskUserQuestion to gather essential information:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "What is the core mission of this project in one sentence?",
      header: "Mission",
      options: [
        { label: "I'll type it myself", description: "Provide custom mission statement" }
      ],
      multiSelect: false
    },
    {
      question: "What stage is this project currently in?",
      header: "Stage",
      options: [
        { label: "Brand new", description: "Just starting, no code yet" },
        { label: "Early development", description: "Some code exists, still evolving" },
        { label: "Active development", description: "Established codebase, ongoing features" },
        { label: "Mature", description: "Stable codebase, maintenance mode" }
      ],
      multiSelect: false
    },
    {
      question: "Do you have existing design principles or guidelines?",
      header: "Principles",
      options: [
        { label: "Yes, documented", description: "Have written principles already" },
        { label: "Yes, informal", description: "Have ideas but not written down" },
        { label: "No, need help", description: "Want to create them now" }
      ],
      multiSelect: false
    }
  ]
})
```

**3. Create Directory Structure**

Ensure all required directories exist:

```bash
# Create directories if they don't exist
mkdir -p .wrangler
mkdir -p .wrangler/docs
mkdir -p .wrangler/plans

# Note: .wrangler/issues and .wrangler/specifications are created by session hooks
```

### Phase 2: Constitution Creation

**If user has existing principles**: Use the `constitution` skill (invoke with Skill tool) to help them refine and formalize.

**If user needs help creating principles**: Guide them through brainstorming process:

**1. Identify Core Values**

Ask these questions (one at a time, discussion-style):
- "What matters most to you in this project's design and architecture?"
- "What are the non-negotiables - things you'd refuse to compromise on?"
- "What mistakes have you seen in similar projects that you want to avoid?"
- "What does success look like for this project in 2 years?"

**2. Convert Values to Principles**

For each core value, help user formulate as concrete principle:

**Template**:
```markdown
### [Principle Number]: [Principle Name]

**Principle**: [One-sentence statement of the principle]

**In Practice**:
- [Specific application 1]
- [Specific application 2]
- [Specific application 3]

**Anti-patterns** (What NOT to do):
- ❌ [Anti-pattern 1 with explanation]
- ❌ [Anti-pattern 2 with explanation]

**Examples**:
- ✅ **Good**: [Concrete example showing principle in action]
- ❌ **Bad**: [Concrete example violating principle]
```

**3. Write Constitution File**

Use the template from `skills/constitution/templates/_CONSTITUTION.md`:

```bash
# Copy template (if not using the skill to generate it)
cp /path/to/wrangler/skills/constitution/templates/_CONSTITUTION.md .wrangler/CONSTITUTION.md
```

Then use Edit tool to fill in:
- Project name
- Current date for ratification
- North Star mission (from Phase 1)
- 5+ principles (from brainstorming)
- Decision framework (can use default)
- Amendment process (can use default)

### Phase 3: Roadmap Creation

**1. Gather Roadmap Information**

Ask user about phases and goals:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "How many major phases do you envision for this project?",
      header: "Phases",
      options: [
        { label: "1-2 phases", description: "Small project, focused scope" },
        { label: "3-4 phases", description: "Medium project, several major milestones" },
        { label: "5+ phases", description: "Large project, long-term vision" }
      ],
      multiSelect: false
    }
  ]
})
```

**2. For Each Phase, Gather Details**

For first phase (most important):
- "What's the main goal of Phase 1?"
- "What features are essential for Phase 1?"
- "What does success look like at the end of Phase 1?"
- "What's the timeline for Phase 1?"

For subsequent phases (can be less detailed):
- "What's the main goal of Phase N?"
- "What key features belong in Phase N?"

**3. Write Roadmap File**

Use template from `skills/validating-roadmap/templates/_ROADMAP.md`:

```bash
# Copy template (if not using the skill to generate it)
cp /path/to/wrangler/skills/validating-roadmap/templates/_ROADMAP.md .wrangler/ROADMAP.md
```

Fill in with Edit tool:
- Project name and overview
- Current state (what's already done)
- Each phase with timeline, goal, features, success metrics
- Link to constitution principles

**4. Write Next Steps File**

Use template from `skills/validating-roadmap/templates/_ROADMAP__NEXT_STEPS.md`:

```bash
# Copy template (if not using the skill to generate it)
cp /path/to/wrangler/skills/validating-roadmap/templates/_ROADMAP__NEXT_STEPS.md .wrangler/ROADMAP_NEXT_STEPS.md
```

Initial file should reflect current state:
- If brand new project: Everything in ❌ Not Implemented
- If existing project: Categorize features into ✅ / ⚠️ / ❌

### Phase 4: Process Documentation

**1. Create Issues README**

Create a minimal README with status metrics. No separate template file exists - create inline with essential content.

Use Edit tool to:
- Update "Status" section with current counts (run `issues_list` to get counts)
- Update "Metrics" section with actual data
- Keep rest of template as-is (it's generic guidance)

**2. Create Specifications README**

Create a minimal README with status metrics. No separate template file exists - create inline with essential content.

Use Edit tool to:
- Update "Status" section with current counts
- Update "Current Phase" section from roadmap
- Update "Metrics" section with actual data
- Keep rest as guidance

**3. Add Issue Template to .wrangler/templates/**

```bash
# Create templates directory
mkdir -p .wrangler/templates

# Copy issue template
cp /path/to/wrangler/skills/create-new-issue/templates/TASK_ISSUE_TEMPLATE.md .wrangler/templates/issue.md
```

**4. Add Specification Template to .wrangler/templates/**

```bash
# Copy spec template
cp /path/to/wrangler/skills/writing-specifications/templates/SPECIFICATION_TEMPLATE.md .wrangler/templates/specification.md
```

### Phase 5: Integration and Verification

**1. Update Project CLAUDE.md**

If `CLAUDE.md` exists in project root, add governance section:

```markdown
## Project Governance

This project uses a three-tier governance framework:

### Tier 1: Constitution (Immutable Principles)
**File**: `.wrangler/CONSTITUTION.md`

Supreme law of the project. All features and decisions must align with constitutional principles.

**Read this first** before working on any feature.

### Tier 2: Strategic Roadmap
**File**: `.wrangler/ROADMAP.md`

Multi-phase strategic plan showing project direction and feature phasing.

### Tier 3: Tactical Execution
**File**: `.wrangler/ROADMAP_NEXT_STEPS.md`

Granular tracking of implementation status with % completion metrics.

### Governance Workflow

Before implementing any feature:
1. Check constitutional alignment
2. Verify roadmap phase
3. Create/update specification
4. Break into tracked issues
5. Follow TDD implementation
6. Update progress in NEXT_STEPS

**Critical**: Use the `check-constitutional-alignment` skill before starting new features.
```

**2. Verify All Files Created**

Run verification:

```bash
# List all governance files
echo "=== Governance Files ==="
ls -lh .wrangler/CONSTITUTION.md
ls -lh .wrangler/ROADMAP.md
ls -lh .wrangler/ROADMAP_NEXT_STEPS.md
ls -lh .wrangler/specifications/README.md
ls -lh .wrangler/issues/README.md
ls -lh .wrangler/templates/issue.md
ls -lh .wrangler/templates/specification.md

echo ""
echo "=== Directory Structure ==="
tree -L 2 .wrangler/
```

**3. Create Welcome Issue**

Use `issues_create` to create first issue explaining governance:

```typescript
issues_create({
  title: "Welcome to Project Governance Framework",
  description: `## Governance Framework Initialized

This project now has a complete governance framework to ensure alignment between AI assistant and human partner.

### Key Documents

**Constitution** (\`.wrangler/CONSTITUTION.md\`)
- Immutable design principles
- Decision framework
- Amendment process

**Roadmap** (\`.wrangler/ROADMAP.md\`)
- Strategic multi-phase plan
- Feature phasing
- Success metrics

**Next Steps** (\`.wrangler/ROADMAP_NEXT_STEPS.md\`)
- Tactical execution tracker
- % completion metrics
- Prioritized work items

### Quick Start

1. Read the Constitution first
2. Review the Roadmap to understand phases
3. Check Next Steps for current priorities
4. Use MCP tools or skills to create issues/specs

### Next Actions

- [ ] Read CONSTITUTION.md thoroughly
- [ ] Review ROADMAP.md phases
- [ ] Identify first features to implement
- [ ] Create specifications for Phase 1 features
- [ ] Begin implementation following governance

### Skills Available

- \`check-constitutional-alignment\` - Verify feature alignment
- \`constitution\` - Refine principles and clarity
- \`verify-governance\` - Check governance integrity
- \`refresh-metrics\` - Update status metrics

Close this issue once you've reviewed all governance documents.
  `,
  type: "issue",
  status: "open",
  priority: "high",
  labels: ["governance", "onboarding"],
  project: "Governance Framework"
})
```

### Phase 6: User Handoff

**Provide Summary to User**

Create summary message:

```markdown
## Governance Framework Initialized

Your project now has a complete governance system ensuring we stay aligned on:
- Design principles (Constitution)
- Strategic direction (Roadmap)
- Tactical execution (Next Steps)

### Files Created

**Core Governance** (in `.wrangler/`):
- `CONSTITUTION.md` - [X] principles ratified
- `ROADMAP.md` - [Y] phases planned
- `ROADMAP_NEXT_STEPS.md` - Execution tracker

**Process Documentation** (in `.wrangler/`):
- `issues/README.md` - Issue management guide
- `specifications/README.md` - Specification guide
- `templates/issue.md` - Issue template
- `templates/specification.md` - Spec template

### Next Steps

1. **Review Constitution**: Read `.wrangler/CONSTITUTION.md`
   - Verify principles match your vision
   - Use `constitution` skill if refinement needed

2. **Review Roadmap**: Read `.wrangler/ROADMAP.md`
   - Confirm phases and timelines
   - Adjust priorities if needed

3. **Start Implementation**:
   - Create specifications for Phase 1 features
   - Use `writing-plans` skill to break into tasks
   - Follow governance workflow for all features

### Governance Workflow

```
Feature Request
    ↓
Constitutional Check (use check-constitutional-alignment skill)
    ↓ (if aligned)
Specification (create with constitutional alignment section)
    ↓
Implementation Plan (use writing-plans skill)
    ↓
Issue Tracking (auto-created by writing-plans)
    ↓
Implementation (follow TDD)
    ↓
Update NEXT_STEPS (mark features complete)
```

### Skills for Governance

- **check-constitutional-alignment** - Verify feature fits principles
- **constitution** - Refine and clarify principles
- **verify-governance** - Check framework integrity
- **refresh-metrics** - Update status counts

**You're all set!** We're now "of one mind" on project governance.
```

## Edge Cases

### If Governance Already Partially Exists

**Scenario**: Some governance files already exist

**Approach**:
1. Detect which files exist
2. Ask user: "I see you already have [files]. Would you like me to:"
   - "Enhance existing files (preserve your content)"
   - "Start fresh (backup old, create new)"
   - "Skip initialization"
3. If enhancing:
   - Read existing files
   - Identify gaps compared to templates
   - Propose additions (don't remove user content)

### If User is Unsure About Principles

**Scenario**: User says "I don't know" or "Not sure" when asked about principles

**Approach**:
1. Use researching-web-sources skill to find examples:
   - "software design principles"
   - "project constitution examples"
   - "engineering team values"
2. Present 3-4 common principles as starting point
3. Offer to use `constitution` skill for deep refinement

### If Project is Very Small

**Scenario**: Single-file project or very small scope

**Approach**:
1. Still create full governance (future-proofing)
2. Explain: "Even small projects benefit from clear principles"
3. Suggest simplified constitution (3 principles instead of 5+)
4. Suggest single-phase roadmap

## Success Criteria

Initialization is complete when:

- [ ] All 7 governance files exist and are populated
- [ ] Constitution has 3+ principles with examples
- [ ] Roadmap has at least 1 phase with goals
- [ ] README files have current metrics
- [ ] Templates are in place
- [ ] Welcome issue created
- [ ] User has reviewed all documents
- [ ] CLAUDE.md updated (if exists)

## Important Notes

**Template Paths**: Templates are in skill-specific directories:
- Constitution: `skills/constitution/templates/`
- Roadmap: `skills/validating-roadmap/templates/`
- Issues: `skills/create-new-issue/templates/`
- Specifications: `skills/writing-specifications/templates/`

**Use Copy, Not Move**: Always copy templates, never move them (templates stay in wrangler)

**Preserve User Content**: If enhancing existing files, never delete user content

**Constitutional First**: The constitution is most important - spend time here

**Roadmap Can Evolve**: Roadmap will change - it's okay to start simple

**Metrics Will Update**: Don't worry about exact metrics now - refresh-metrics skill handles this

## Related Skills

- **constitution** - For deep principle refinement and clarification
- **check-constitutional-alignment** - For verifying features align with principles
- **verify-governance** - For checking governance file integrity
- **refresh-metrics** - For updating status counts in READMEs and NEXT_STEPS

## Remember

You're establishing the foundation for perfect alignment between AI and human. Take time to make the constitution solid - everything else builds on this foundation.
