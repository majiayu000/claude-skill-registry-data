---
name: skill-customizer
description: Customize existing skills through iterative improvement based on user feedback and preferences. Use when users want to personalize a skill to match their specific workflow, output preferences, domain requirements, or company standards by forking and iteratively refining an existing skill.
---

# Skill Customizer

Enable users to transform existing skills into personalized versions that perfectly match their unique needs through forking, testing, gathering feedback, and iterative improvement.

## When to Use This Skill

Use skill-customizer when:
- User finds an existing skill useful but wants specific modifications
- User has personal preferences about output format, verbosity, or style
- User needs to adapt a skill to company-specific requirements or workflows
- User wants to add domain-specific knowledge to an existing skill
- User discovers gaps after trying a skill on real tasks

**Do NOT use when:**
- User wants to create a completely new skill from scratch (use skill-creator instead)
- User only needs a one-time modification without creating a reusable skill
- The customization is so extensive that starting fresh would be simpler

## Proactive Suggestion Trigger

**When to proactively suggest using skill-customizer:**

When a user is actively using a skill and has provided modification requests, preferences, or guidance during the session, watch for satisfaction signals such as:
- User expresses satisfaction with the customized behavior ("That's perfect!", "Exactly what I needed", "Much better")
- User has given multiple consistent preferences or modifications
- User has requested specific output format changes or workflow adjustments
- The session shows iterative refinement that stabilized to user's preference

**In these scenarios, proactively offer:**

"I notice you've been refining how [skill-name] works to match your preferences. Would you like to save these customizations as your own personalized version of this skill? I can help you create a customized skill that automatically applies these preferences in future sessions."

This transforms one-time adjustments into reusable, persistent customizations that improve the user's long-term workflow.

## Customization Workflow

Follow this iterative process to customize a skill effectively:

### Phase 1: Fork the Base Skill

**Identify the base skill**

Ask the user:
- Which skill to customize?
- Where is the skill located?
- What name for the customized version?

**Create the fork**

Run from the skill-customizer directory:
```bash
cd skill-customizer
python3 scripts/fork_skill.py <source-skill-path> <new-skill-name> --path <output-directory>
```

Or from parent directory with full path:
```bash
python3 skill-customizer/scripts/fork_skill.py <source-skill-path> <new-skill-name> --path <output-directory>
```

This creates:
- Complete copy of the original skill
- Updated metadata with customization tracking
- CUSTOMIZATION_LOG.md for documenting changes

**Understand the base skill**

Review the forked skill:
- SKILL.md content and structure
- Scripts in `scripts/` directory
- Reference documents in `references/` directory
- Assets in `assets/` directory

### Phase 2: Test and Gather Feedback

**Use the skill on real tasks**

Have the user try the forked skill to identify:
- What works well as-is
- What doesn't match expectations
- Specific pain points or inefficiencies
- Missing features or capabilities

**Collect structured feedback**

Use the feedback tracking script:
```bash
python3 scripts/track_feedback.py <skill-directory>
```

Or collect through conversation:
1. "What task were you trying to accomplish?"
2. "What aspects worked well?"
3. "What didn't match your expectations?"
4. "What are your specific preferences?"
5. "What improvements would help most?"

This creates/updates FEEDBACK.md with timestamped entries.

### Phase 3: Plan and Apply Improvements

**Analyze feedback and plan changes**

Categorize modifications by target:

**SKILL.md modifications:**
- Change default behavior or workflows
- Adjust output format preferences
- Update examples with user-specific scenarios
- Add user's domain context
- Modify tone or verbosity

**Script modifications:**
- Adjust default parameters
- Add preprocessing or postprocessing steps
- Customize output formatting
- Add validation logic specific to user's needs

**Reference additions:**
- Add company guidelines or policies
- Include domain-specific schemas
- Document user's preferred workflows

**Asset additions:**
- Add company templates
- Include brand assets
- Add domain-specific boilerplate

**Apply targeted modifications**

For each modification:
1. Edit the relevant file
2. Test the change on the same task that revealed the gap
3. Document in CUSTOMIZATION_LOG.md with version, what changed, why, and how to verify

### Phase 4: Iterate Until Satisfied

**Test the improved version**

After applying changes:
1. Run the skill on the same task again
2. Compare results with previous version
3. Verify the changes addressed the feedback

**Gather new feedback**

Ask the user:
- "Does this better match your expectations?"
- "Are there any new issues or additional preferences?"
- "What else would you like to adjust?"

**Repeat or finalize**

If more improvements needed: return to Phase 3
If satisfied: proceed to Phase 5

### Phase 5: Packaging the Skill

Once the skill is ready, package it into a distributable zip file. The packaging process automatically validates the skill first to ensure it meets all requirements.

```bash
python3 scripts/finalize_skill.py <skill-directory>
```

Optional output directory specification:

```bash
python3 scripts/finalize_skill.py <skill-directory> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality

2. **Package** the skill if validation passes, creating a timestamped zip file: `{skill-name}-{YYYYMMDD-HHMMSS}.zip`

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

## Best Practices

**Iterative Improvement**
- Make small, focused changes rather than large overhauls
- Test each change before moving to the next
- Document each iteration in CUSTOMIZATION_LOG.md
- Keep feedback organized and prioritized

**Maintain Skill Quality**
- Follow the same quality standards as the original skill
- Use imperative/infinitive form in SKILL.md (not second person)
- Keep SKILL.md concise; move details to `references/`
- Ensure scripts are well-documented and reusable

**Preserve Original Structure**
- Keep the same directory organization as the base skill
- Maintain compatibility with skill tooling
- Don't break existing functionality unless intentionally removing it

**Document Customizations**
- Always update CUSTOMIZATION_LOG.md with each change
- Include rationale for changes (why, not just what)
- Provide testing steps to verify improvements
- Track version numbers for major iterations

**Balance Specificity and Reusability**
- Don't over-customize to a single task
- Keep the skill useful for related tasks
- Consider whether changes should be configurable vs. hardcoded

## Resources

### scripts/fork_skill.py
Creates a customized copy of an existing skill with updated metadata and customization tracking.

**Usage:**
```bash
scripts/fork_skill.py <source-skill-path> <new-skill-name> --path <output-directory>
```

**What it does:**
- Copies entire skill directory structure
- Updates SKILL.md frontmatter with new name
- Adds customization metadata (source skill, date)
- Creates CUSTOMIZATION_LOG.md for tracking changes

### scripts/track_feedback.py
Interactively collects and organizes user feedback for systematic improvement.

**Usage:**
```bash
scripts/track_feedback.py <skill-directory>
```

**What it does:**
- Prompts for structured feedback (task, preferences, improvements)
- Creates/updates FEEDBACK.md with timestamped entries
- Analyzes feedback patterns across multiple entries
- Helps prioritize customization efforts

### scripts/finalize_skill.py
Validates and packages a customized skill with timestamp for distribution.

**Usage:**
```bash
scripts/finalize_skill.py <skill-directory> [output-directory]
```

**What it does:**
- Validates skill structure and frontmatter automatically
- Creates timestamped zip file: `{skill-name}-{YYYYMMDD-HHMMSS}.zip`

The timestamp allows tracking different versions and iterations of the customized skill.

### scripts/quick_validate.py
Standalone validation script for checking skill structure without packaging.

**Usage:**
```bash
scripts/quick_validate.py <skill-directory>
```

**What it does:**
- Checks YAML frontmatter format
- Validates required fields (name, description)
- Verifies naming conventions

Use this during development to validate changes before packaging.

### references/customization_patterns.md
Comprehensive guide to common customization patterns, detailed examples, and best practices.

Load this reference when:
- Facing complex customization decisions
- Unsure how to implement a specific type of change
- Looking for examples of successful customizations
- Planning extensive modifications

Includes:
- Detailed modification examples with before/after code
- Troubleshooting common customization challenges
- Advanced techniques for skill enhancement
- Patterns for maintaining customized skills over time
