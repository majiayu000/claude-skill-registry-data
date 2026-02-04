---
name: skill-contributor
description: Guides contributors through adding new skills to the claude-code-skills repository via Pull Request with proper validation and documentation
---

# Skill Contributor

Helps contributors add new skills to the claude-code-skills repository following the proper workflow with validation and documentation updates.

## When to Use

Use this skill when:
- User wants to contribute a new skill to the claude-code-skills repository
- User asks to submit a skill via PR or pull request
- User requests help adding their skill to the repository
- User mentions contributing to the skill collection

## Prerequisites Check

Before starting, verify:

1. **Current working directory**: Must be the claude-code-skills repository root
   - Run: `pwd` to confirm
   - Should see: `/path/to/claude-code-skills`

2. **Git repository status**: Check if fork or main repo
   - Run: `git remote -v`
   - If user's fork: ready to proceed
   - If main repo: guide user to fork first

3. **New skill exists**: The skill to contribute must already be created
   - Ask user for the skill directory path
   - Verify SKILL.md exists in that directory

## Contribution Workflow

Follow these steps to guide the contributor:

### Step 1: Fork Verification

Check if the user has forked the repository:

```bash
git remote -v
```

**If pointing to WomenDefiningAI/claude-code-skills**:
- Guide user to fork the repository at https://github.com/WomenDefiningAI/claude-code-skills
- Ask them to clone their fork and work from there

**If pointing to user's fork**: Proceed to next step

### Step 2: Copy Skill to Repository

If the skill is not already in the repository:

1. Ask user for the skill directory location
2. Verify the skill structure:
   ```bash
   ls -la /path/to/their/skill/
   ```
3. Copy skill to the skills/ directory:
   ```bash
   cp -r /path/to/their/skill/ ./skills/skill-name/
   ```

### Step 3: Run Validation

Validate the skill structure using the validation script:

```bash
python3 skills/skill-builder/scripts/validate-skill.py skills/skill-name/
```

**If validation fails**:
- Show the user the errors
- Offer to help fix issues
- Re-run validation after fixes

**If validation passes**: Proceed to next step

### Step 4: Update README.md

The skill must be added to the README.md in the "Available Skills" section.

1. Read the current README.md to find the insertion point
2. Ask the user for:
   - Skill name (display name)
   - One-line description
   - Key features (3-5 bullet points)

3. Add the skill entry after the existing skills, following this format:

```markdown
### 🎯 Skill Display Name

**Status**: ✅ Available
**Directory**: `skills/skill-name/`
**Purpose**: One-line description of the skill

**Features**:
- Feature 1
- Feature 2
- Feature 3

[**View Documentation →**](skills/skill-name/README.md)

**Quick Install**:
```bash
git clone https://github.com/WomenDefiningAI/claude-code-skills.git
cp -r claude-code-skills/skills/skill-name ~/.claude/skills/
```

---
```

4. Insert in the "## Available Skills" section (after existing skills)

### Step 5: Create README.md for the Skill

If the skill doesn't have a README.md, create one:

1. Ask user for:
   - What the skill does
   - Installation instructions (already standardized)
   - Usage examples
   - Requirements/dependencies

2. Create README.md based on skills/skill-builder/README.md template

### Step 6: Git Operations

Create a new branch and commit the changes:

```bash
# Create feature branch
git checkout -b add-skill-name

# Add the new skill
git add skills/skill-name/

# Add updated README
git add README.md

# Create commit
git commit -m "Add [skill-name] skill

- Adds new skill: [brief description]
- Includes validation
- Updates README.md with skill documentation

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to user's fork
git push -u origin add-skill-name
```

### Step 7: Create Pull Request

Use GitHub CLI to create the PR:

```bash
gh pr create --title "Add [skill-name] skill" --body "$(cat <<'EOF'
## Summary

This PR adds a new skill: **[skill-name]**

### What This Skill Does

[Brief description of what the skill does and when to use it]

### Changes Included

- ✅ New skill directory: `skills/skill-name/`
- ✅ SKILL.md with valid frontmatter
- ✅ README.md with installation and usage instructions
- ✅ Updated main README.md to list the skill
- ✅ Passed validation: `python3 skills/skill-builder/scripts/validate-skill.py skills/skill-name/`

### Validation Output

```
[Paste validation output showing ✅ VALIDATION PASSED]
```

### Testing

Tested by:
- [ ] Installing to `~/.claude/skills/` directory
- [ ] Verifying Claude recognizes the skill
- [ ] Testing the skill with example use cases

### Additional Notes

[Any additional context, dependencies, or notes for reviewers]

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**If gh CLI not available**:
- Provide the PR URL manually: https://github.com/WomenDefiningAI/claude-code-skills/compare
- Give the user the formatted PR title and description to copy

### Step 8: Post-PR Checklist

After creating the PR, remind the user:

1. ✅ Validation passed
2. ✅ README.md updated
3. ✅ PR created with detailed description
4. ⏳ Wait for maintainer review
5. 📝 Be ready to address feedback

## Common Issues & Solutions

### Issue: Validation Fails

**Error**: "Invalid YAML frontmatter"
- **Fix**: Check SKILL.md starts with `---` and has valid YAML

**Error**: "name contains invalid characters"
- **Fix**: Name must be lowercase, alphanumeric, hyphens only

**Error**: "Referenced file does not exist"
- **Fix**: Ensure all files mentioned in SKILL.md exist

### Issue: User Hasn't Forked

**Solution**:
1. Direct to https://github.com/WomenDefiningAI/claude-code-skills
2. Click "Fork" button
3. Clone their fork
4. Restart contribution workflow

### Issue: Skill Not Created Yet

**Solution**:
- Use the skill-builder skill to create the skill first
- Come back to skill-contributor after skill is built

## Validation Checklist

Before creating the PR, verify:

- [ ] Skill has SKILL.md with valid YAML frontmatter
- [ ] Skill name follows naming rules (lowercase, hyphens, alphanumeric)
- [ ] Description is clear and under 1024 characters
- [ ] Validation script passes: `python3 skills/skill-builder/scripts/validate-skill.py skills/skill-name/`
- [ ] README.md is updated with skill entry
- [ ] Skill directory is in the skills/ directory
- [ ] All referenced files exist
- [ ] Skill has been tested locally

## Examples

### Example 1: Contributing a Code Review Skill

```
User: I've created a code review skill and want to contribute it to the repo
Assistant: I'll help you contribute your code review skill to the repository. Let me start by checking the current directory and repository status.

1. Check working directory and git remote
2. Locate the code-review skill files
3. Run validation
4. Update README.md
5. Create PR with proper description
```

### Example 2: Quick Contribution

```
User: Add my test-generator skill via PR
Assistant: I'll guide you through the contribution workflow:
1. Verify fork status
2. Validate test-generator skill
3. Update README.md
4. Create and push branch
5. Submit PR

Let me start by checking your repository setup.
```

## Notes

- Always run validation before creating PR
- Fork the repository if you haven't already
- Update README.md to list the new skill
- Provide clear PR description with validation output
- Be responsive to maintainer feedback
- Test the skill locally before submitting
