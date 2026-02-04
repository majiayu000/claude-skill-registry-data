---
name: handbook-updater
description: Expert knowledge on how to properly maintain and update the central Amplify Gen 2 handbook
---

# Handbook Updater Skill

## Purpose

This skill teaches Claude how to properly maintain and update the central Amplify Gen 2 handbook located at `~/.claude/AmplifyHandbook/`.

When you discover new patterns, create documentation, or update existing guides, this skill ensures everything is done correctly and shared with the team.

---

## Core Responsibilities

When this skill is activated, you know how to:
1. Determine the correct location for new documentation
2. Follow handbook formatting conventions
3. Update navigation tables and decision trees
4. Maintain consistency across the handbook
5. Commit and push changes to GitHub for team collaboration

---

## The Source of Truth

**Central Location:** `~/.claude/AmplifyHandbook/`

This directory is cloned from: `https://github.com/ChinchillaEnterprises/AmplifyHandbook`

**All handbook updates happen here**, NOT in individual project folders.

---

## Handbook Structure & Where Things Go

### 1. Top-Level Guides

**Location:** `~/.claude/AmplifyHandbook/`

**When to create here:**
- Fundamental concepts that span multiple features
- Critical rules and guidelines
- Cross-cutting patterns

**Examples:**
- `AI-DEVELOPMENT-GUIDELINES.md` - Core rules (No CDK, etc.)
- `ASYNC_PATTERNS.md` - Timeout solutions
- `BACKEND_ENV_CONFIG.md` - Environment detection
- `ENVIRONMENT_VARIABLES.md` - Env var patterns
- `NO-API-GATEWAY.md` - Backend endpoint pattern

### 2. Feature-Specific Folders

**auth/** - Everything authentication-related
- Patterns, setup guides, OAuth, security
- Has its own README.md navigation hub

**data/** - Database schemas and DynamoDB patterns
- Schema examples (TypeScript files)
- Data modeling guides (TTL, indexes, etc.)

**functions/** - Lambda function patterns
- Access patterns (DynamoDB, S3, Cognito)
- Function types (scheduled, triggers, resolvers)
- Each function type has its own subdirectory

**webhooks/** - Webhook handling patterns
- Next.js API route pattern
- Authorization modes
- Complete working examples in `examples/`

**frontend/** - Client-side patterns
- Design system guides
- Data operations
- Component patterns

**troubleshooting/** - Debugging and fixes
- Common errors and solutions
- Deployment issues

### 3. Navigation READMEs

**Critical:** Every folder should have a README.md that serves as a navigation hub.

**README.md must contain:**
- "I Need To..." table with quick links
- Overview of what's in the folder
- Quick reference for common tasks
- Links to related documentation

**Folders with navigation READMEs:**
- `~/.claude/AmplifyHandbook/README.md` - Main hub
- `~/.claude/AmplifyHandbook/auth/README.md` - Auth hub
- `~/.claude/AmplifyHandbook/webhooks/README.md` - Webhook hub
- `~/.claude/AmplifyHandbook/frontend/README.md` - Frontend hub
- `~/.claude/AmplifyHandbook/troubleshooting/README.md` - Troubleshooting hub

---

## Update Workflow

### Step 1: Determine Location

Ask yourself:

**Is it a fundamental rule or cross-cutting pattern?**
→ Top-level guide (e.g., `ASYNC_PATTERNS.md`)

**Is it specific to a feature area?**
→ Feature folder (e.g., `auth/`, `functions/`, `webhooks/`)

**Is it a complete working example?**
→ Examples subfolder (e.g., `webhooks/examples/slack-events/`)

**Is it troubleshooting/debugging?**
→ `troubleshooting/` folder

### Step 2: Create or Update File in Central Handbook

**For new guides:**
```bash
# Create directly in central handbook
touch ~/.claude/AmplifyHandbook/path/to/NEW_GUIDE.md

# Follow the naming convention:
# - ALL_CAPS_WITH_UNDERSCORES.md for guides
# - lowercase-with-dashes.ts for code examples
# - README.md for navigation hubs
```

**For updates:**
```bash
# Update the file directly in central handbook
# Edit ~/.claude/AmplifyHandbook/path/to/EXISTING_GUIDE.md
```

**Formatting conventions:**
- Use clear hierarchical headers (H2, H3, H4)
- Include "What's Inside" or "Overview" section
- Provide decision trees when applicable
- Include complete code examples
- Add troubleshooting sections
- Use emojis sparingly (⭐ for NEW, ❌ for don'ts, ✅ for dos)

### Step 3: Update Navigation Tables

**Critical locations to update:**

1. **Main README.md** (`~/.claude/AmplifyHandbook/README.md`)
   - Add to "I Need To..." table
   - Update file structure diagram
   - Add to relevant learning path

2. **Folder README.md** (if applicable)
   - Add to folder's "I Need To..." table
   - Update "What's Inside" section

3. **Related guides** that reference this topic
   - Add cross-references
   - Update decision trees

### Step 4: Verify Changes

**Verify the file was created/updated:**
```bash
# Check that new/updated file exists in central handbook
ls -la ~/.claude/AmplifyHandbook/path/to/file.md

# Optionally view the file to confirm
cat ~/.claude/AmplifyHandbook/path/to/file.md
```

### Step 5: Commit and Push to GitHub

**CRITICAL: Share your changes with the team!**

After updating handbook files, commit and push to GitHub so all team members can access the updates:

```bash
cd ~/.claude/skills/

# Pull latest changes first (avoid conflicts)
git pull

# Stage all changes
git add handbook/

# Commit with descriptive message
git commit -m "docs: [Brief description of what was added/updated]"

# Push to GitHub
git push
```

**Commit message examples:**
- `"docs: Add AUTO_CONFIRM_SETUP guide for authentication"`
- `"docs: Update Lambda DynamoDB access patterns"`
- `"docs: Fix typo in webhooks guide"`

**Why this matters:**
- Your teammates need to pull to get your updates
- The handbook is a shared team resource
- Changes aren't available to others until pushed

### Step 6: Team Gets Updates

After you push, teammates should:

```bash
# Update their central handbook
cd ~/.claude/AmplifyHandbook/
git pull

# Then sync to their projects (optional)
# Use handbook-sync skill in their project
```

---

## Naming Conventions

### File Names

**Guides (markdown):**
- `ALL_CAPS_WITH_UNDERSCORES.md`
- Examples: `LAMBDA_DYNAMODB_ACCESS.md`, `AUTH_PATTERNS.md`

**Code Examples (TypeScript):**
- `lowercase-with-dashes.ts` or `descriptive-name.ts`
- Examples: `blog-schema.ts`, `simple-custom-operations.ts`

**Navigation Hubs:**
- Always `README.md`

**Folders:**
- `lowercase` (e.g., `auth/`, `functions/`, `webhooks/`)

### Section Headers

**Use consistent header patterns:**
```markdown
# Main Title (H1) - Only one per file

## Major Sections (H2)
### Subsections (H3)
#### Details (H4)
```

**Common section names:**
- "Overview" or "What's Inside"
- "The Problem" / "The Solution"
- "Quick Start" or "How to Use"
- "Common Use Cases"
- "Best Practices"
- "Troubleshooting"
- "Related Documentation"

---

## Content Guidelines

### 1. Decision Trees

When documenting patterns with multiple options, provide decision trees:

```markdown
**Need HTTP endpoint?**
```
Is it for internal operations?
  → YES: Use GraphQL custom mutation
  → NO: Is it for external webhooks?
      → YES: Use Next.js API route
      → NO: Consider Lambda Function URL
```
```

### 2. Code Examples

Always include complete, working examples:

```markdown
**Example:**
\`\`\`typescript
// Complete code that can be copy-pasted
export const myFunction = defineFunction({
  name: 'my-function',
  entry: './handler.ts',
  resourceGroupName: 'data',
});
\`\`\`
```

### 3. Cross-References

Link to related documentation:

```markdown
**See also:**
- [LAMBDA_DYNAMODB_ACCESS.md](./functions/LAMBDA_DYNAMODB_ACCESS.md)
- [AI-DEVELOPMENT-GUIDELINES.md](./AI-DEVELOPMENT-GUIDELINES.md)
```

### 4. Common Pitfalls

Include anti-patterns and mistakes to avoid:

```markdown
**Common Mistakes:**
❌ Importing from `aws-cdk-lib` directly
❌ Hardcoding DynamoDB table names
✅ Using `resourceGroupName: 'data'`
```

### 5. Progressive Disclosure

Structure content from simple to complex:
1. Quick summary at the top
2. Common use cases
3. Detailed explanation
4. Advanced patterns
5. Troubleshooting

---

## Maintenance Tasks

### When Adding New Pattern

1. Create guide in central handbook (`~/.claude/AmplifyHandbook/`)
2. Update all navigation READMEs in central handbook
3. Add cross-references to related guides
4. Update decision trees
5. Verify file was created successfully
6. **Commit and push to GitHub** (share with team)

### When Updating Existing Guide

1. Update the guide content in central handbook
2. Check if navigation tables need updating
3. Update "last updated" or version notes if applicable
4. Verify cross-references are still accurate
5. **Commit and push to GitHub** (share with team)

### When Removing/Deprecating

1. Mark as deprecated in the guide (don't delete immediately)
2. Update navigation tables to point to new pattern
3. Add migration guide if applicable
4. After grace period, remove from central handbook

---

## Quality Checklist

Before considering handbook update complete:

**Content:**
- [ ] Clear overview/introduction
- [ ] Complete code examples
- [ ] Decision trees for multiple options
- [ ] Troubleshooting section
- [ ] Cross-references to related docs

**Navigation:**
- [ ] Added to main README "I Need To..." table
- [ ] Added to folder README (if applicable)
- [ ] Updated file structure diagram
- [ ] Cross-references from related guides

**Formatting:**
- [ ] Follows naming conventions
- [ ] Consistent header hierarchy
- [ ] Proper code block formatting
- [ ] Links work correctly

**Verification:**
- [ ] File exists in `~/.claude/AmplifyHandbook/`
- [ ] Navigation updated in central handbook
- [ ] Changes verified with ls/cat commands
- [ ] Committed and pushed to GitHub

---

## Examples of Good Updates

### Example 1: Adding New Feature Guide

**Scenario:** Discovered a new pattern for scheduled Lambda functions

**Steps:**
1. Create `~/.claude/AmplifyHandbook/functions/SCHEDULED_LAMBDA_PATTERN.md`
2. Update `~/.claude/AmplifyHandbook/functions/README.md`
3. Add to main handbook README "I Need To..." table
4. Add cross-reference from `ASYNC_PATTERNS.md`
5. Verify file exists: `ls -la ~/.claude/AmplifyHandbook/functions/SCHEDULED_LAMBDA_PATTERN.md`
6. Commit and push:
   ```bash
   cd ~/.claude/skills/
   git pull
   git add handbook/
   git commit -m "docs: Add SCHEDULED_LAMBDA_PATTERN guide"
   git push
   ```

### Example 2: Adding Troubleshooting Guide

**Scenario:** Common error with OAuth callbacks

**Steps:**
1. Create `~/.claude/AmplifyHandbook/troubleshooting/OAUTH_CALLBACK_ERROR.md`
2. Update `~/.claude/AmplifyHandbook/troubleshooting/README.md`
3. Add cross-reference from `auth/CLIENT_SIDE_SETUP.md`
4. Add to main handbook troubleshooting section
5. Verify file exists
6. Commit and push:
   ```bash
   cd ~/.claude/skills/
   git pull
   git add handbook/
   git commit -m "docs: Add OAuth callback error troubleshooting guide"
   git push
   ```

### Example 3: Adding Complete Example

**Scenario:** Working Stripe webhook implementation

**Steps:**
1. Create directory `~/.claude/AmplifyHandbook/webhooks/examples/stripe-payments/`
2. Add `route.ts`, `README.md`, and supporting files
3. Update `webhooks/examples/README.md` to list new example
4. Update `webhooks/README.md` navigation table
5. Verify files exist
6. Commit and push:
   ```bash
   cd ~/.claude/skills/
   git pull
   git add handbook/
   git commit -m "docs: Add Stripe webhook example"
   git push
   ```

---

## Common Questions

**Q: Where do I update handbook files?**
A: Always in `~/.claude/AmplifyHandbook/`. This is the central, canonical source.

**Q: How do projects get the updates?**
A: Projects use the `handbook-sync` skill to copy from `~/.claude/AmplifyHandbook/` to their `resources/handbook/` folder.

**Q: What if I forget to push?**
A: Your changes stay local and teammates won't get them. Always remember: `git add`, `git commit`, `git push`!

**Q: Where do I document a new AWS service integration?**
A: In the central handbook. If it's Lambda-based, goes in `functions/`. If it's a client-side operation, goes in `frontend/`. Cross-cutting patterns go at top level.

**Q: Should I update the handbook for small fixes?**
A: Yes! Even typo fixes should be made in the central handbook and pushed.

---

## Remember

- **Central handbook is source of truth** - Always work with `~/.claude/AmplifyHandbook/`
- **Navigation tables** - Keep them up to date in central handbook
- **Complete examples** - Production-ready code only
- **Cross-references** - Link related documentation
- **Decision trees** - Help users choose the right pattern
- **Progressive disclosure** - Simple to complex
- **Quality over quantity** - Better to have fewer excellent guides
- **Always push to GitHub** - Share your knowledge with the team!

---

When this skill is active, follow these guidelines to maintain a consistent, well-organized, and useful handbook that serves the entire team from a single source of truth.
