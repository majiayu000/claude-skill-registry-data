---
name: marketing-sync
description: Sync ClaudeKit Marketing with Engineer updates using natural language. Handles the two-step sync process, reports what changed, and helps review updates.
activationKeywords:
  - sync marketing
  - update marketing
  - marketing sync
  - sync engineer to marketing
  - check marketing updates
  - review marketing updates
---

# ClaudeKit Marketing Sync Skill

Sync ClaudeKit Marketing with ClaudeKit Engineer updates using natural language commands.

---

## 🎯 Purpose

This skill automates syncing ClaudeKit Marketing with Engineer updates while protecting Marketing customizations. It handles:
- Checking for Engineer updates
- Running the two-step sync process
- Reporting what was synced
- Listing files that need review
- Helping with update decisions

---

## 🚀 Capabilities

### 1. Check for Updates
**User says:** "Check if there are ClaudeKit Engineer updates"

**You do:**
```bash
cd /Users/sam/claudekit-engineer
git fetch origin
git log HEAD..origin/main --oneline
```

**Report:**
- If updates available: List commits since last pull
- If up to date: Confirm already current
- Suggest syncing if updates found

---

### 2. Sync Marketing with Engineer
**User says:** "Sync Marketing with Engineer updates" or "Update ClaudeKit Marketing"

**You do:**

**Step 1: Update Engineer Template**
```bash
cd /Users/sam/claudekit-engineer
git pull
```

**Step 2: Run Sync Script**
```bash
./sync-to-marketing.sh
```

**Step 3: Parse and Report Results**
- Skills synced (count)
- Hooks synced (count)
- Framework files synced
- Agents added (list)
- Agents updated (list with .new files)
- Commands new (categorized)
- Commands updated (list with .new files)

**Step 4: Provide Next Steps**
- How to review .new files
- How to copy new commands
- How to test Marketing

---

### 3. Review Updates
**User says:** "Review Marketing updates" or "Show me what changed"

**You do:**

**List all .new files:**
```bash
cd /Users/sam/claudekit-marketing
find .marketing/ -name "*.new" -type f
```

**For each .new file:**
- Show file path
- Offer to compare versions
- Explain options: keep/replace/merge

**Example interaction:**
```
Found 2 files to review:
1. .marketing/agents/brainstormer.md.new
2. .marketing/commands/ideate.md.new

Would you like to:
- Compare versions (shows diff)
- See what changed (summary)
- Get merge recommendations
```

---

### 4. Compare Versions
**User says:** "Compare brainstormer updates" or "What changed in ideate?"

**You do:**
```bash
diff .marketing/agents/brainstormer.md .marketing/agents/brainstormer.md.new
```

**Report:**
- What changed (summary)
- New features added
- Improvements made
- Your customizations (if any)
- Recommendation: keep/replace/merge

---

### 5. Apply Updates
**User says:** "Use new version of brainstormer" or "Keep my ideate customization"

**You do:**

**Use new version:**
```bash
mv .marketing/agents/brainstormer.md.new .marketing/agents/brainstormer.md
```

**Keep current version:**
```bash
rm .marketing/agents/brainstormer.md.new
```

**Confirm action and explain what was done.**

---

### 6. Copy New Commands
**User says:** "Copy content commands" or "Add recommended commands"

**You do:**

**For specific category:**
```bash
cp -r /Users/sam/claudekit-engineer/.claude/commands/content \
     /Users/sam/claudekit-marketing/.marketing/commands/
```

**For specific command:**
```bash
cp /Users/sam/claudekit-engineer/.claude/commands/brainstorm.md \
   /Users/sam/claudekit-marketing/.marketing/commands/
```

**Report:**
- What was copied
- Where it was copied to
- Suggest testing it

---

### 7. Merge Assistance
**User says:** "Help me merge brainstormer updates"

**You do:**
1. Read both versions (current and .new)
2. Identify differences
3. Provide merge strategy:
   - What to keep from yours
   - What to add from new
   - How to combine them
4. Offer to create merged version

---

### 8. Test Marketing Setup
**User says:** "Test Marketing" or "Verify Marketing works"

**You suggest:**
```bash
cd /Users/sam/claudekit-marketing
claude

# Test commands
/content/good test
/design/fast test

# Test agents
> "Use copywriter to write landing page headline"
```

**Report test status and any issues.**

---

### 9. Commit Changes
**User says:** "Commit Marketing sync" or "Save Marketing updates"

**You do:**
```bash
cd /Users/sam/claudekit-marketing
git status
git add .marketing/
git commit -m "chore: sync with ClaudeKit Engineer vX.XX.X

- Synced skills, hooks, framework
- Added [list new agents]
- Reviewed [list .new files]
- Copied [list new commands]"
git push
```

**Confirm commit and push completed.**

---

## 🔍 Smart Detection

### Auto-detect Context

**If user is in Marketing directory:**
```bash
pwd
# /Users/sam/claudekit-marketing
```
You know they want to work with Marketing.

**If user is in Engineer directory:**
```bash
pwd
# /Users/sam/claudekit-engineer
```
Clarify: "Do you want to sync updates TO Marketing?"

---

## 📋 Workflow Patterns

### Pattern 1: Complete Sync
```
User: "Sync Marketing with latest Engineer"

You:
1. Check if Engineer has updates (git fetch)
2. Pull Engineer updates (git pull)
3. Run sync script
4. Parse and report results
5. List .new files to review
6. Suggest next steps
```

---

### Pattern 2: Review and Apply
```
User: "Review Marketing updates"

You:
1. Find all .new files
2. For each, show summary of changes
3. Ask which to review in detail
4. Provide recommendations
5. Apply user's choices
6. Confirm actions taken
```

---

### Pattern 3: Selective Copy
```
User: "Copy content and design commands"

You:
1. Verify commands exist in Engineer
2. Check if already in Marketing
3. Copy directories
4. Report what was copied
5. Suggest testing
```

---

## 🎯 Response Format

### For Sync Operations

**Template:**
```markdown
## ClaudeKit Marketing Sync Report

**Date:** YYYY-MM-DD
**Engineer Version:** vX.XX.X

### ✅ Synced Automatically
- Skills: XX skills (replaced)
- Hooks: X hooks (replaced)
- Framework: metadata, settings, statusline (replaced)

### 🆕 New Components
**Agents Added:**
- [list agents]

**New Commands Available:**
- ⭐ content/good.md (recommended)
- ⭐ design/fast.md (recommended)
- ✓ brainstorm.md (useful)

### ⚠️ Review Required
**Agents Updated (X):**
- brainstormer.md.new

**Commands Updated (X):**
- ideate.md.new

### 📋 Next Steps
1. Review .new files: `find .marketing/ -name "*.new"`
2. Copy recommended commands: `cp -r ~/claudekit-engineer/.claude/commands/content .marketing/commands/`
3. Test Marketing: `cd ~/claudekit-marketing && claude`

Would you like to review the updates now?
```

---

### For Review Operations

**Template:**
```markdown
## Review: [filename]

**File:** .marketing/agents/brainstormer.md
**Status:** Updated version available

### What Changed
[Summary of changes]

### Your Version Has
- [Your customizations]

### New Version Has
- [Improvements from Engineer]

### Recommendation
[Keep yours / Use new / Merge] because [reason]

### Options
1. **Keep yours:** `rm .marketing/agents/brainstormer.md.new`
2. **Use new:** `mv .marketing/agents/brainstormer.md.new .marketing/agents/brainstormer.md`
3. **Merge:** I can help combine the best of both

What would you like to do?
```

---

## 💡 Smart Recommendations

### When to Use New Version
- Minor customizations only
- New version has significant improvements
- Your version outdated

### When to Keep Yours
- Significant brand-specific customizations
- Company-specific workflows
- New version doesn't add much value

### When to Merge
- Both have valuable elements
- Your customizations + new improvements
- Worth the extra effort

---

## 🛡️ Safety Checks

### Before Syncing
1. ✅ Check if Marketing has uncommitted changes
2. ✅ Warn if sync will affect work in progress
3. ✅ Confirm user wants to proceed

### After Syncing
1. ✅ Verify backup was created
2. ✅ Check for errors in sync output
3. ✅ Confirm Marketing directory still valid

### Before Overwriting
1. ✅ Confirm user wants to replace file
2. ✅ Show what will be lost
3. ✅ Suggest backup if needed

---

## 📁 Key Paths

**Engineer:**
- Directory: `/Users/sam/claudekit-engineer`
- Commands: `.claude/commands/`
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- Hooks: `.claude/hooks/`

**Marketing:**
- Directory: `/Users/sam/claudekit-marketing`
- Commands: `.marketing/commands/`
- Agents: `.marketing/agents/`
- Skills: `.marketing/skills/`
- Hooks: `.marketing/hooks/`

**Sync Script:**
- Location: `/Users/sam/claudekit-engineer/sync-to-marketing.sh`

**Documentation:**
- Obsidian: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault-4/Claude Code/CK-Marketing/`

---

## 🎨 Example Interactions

### Example 1: Basic Sync
```
User: "Sync Marketing with Engineer"User: "Sync Marketing with Engineer"

You:
1. Checking for Engineer updates...
   Found 3 new commits since last sync
2. Pulling Engineer updates... Done
3. Running sync script...

## Sync Report
✅ Synced: 19 skills, 3 hooks, 3 framework files
🆕 New: 2 commands available (content/cro.md, design/3d.md)
⚠️ Review: 1 agent updated (brainstormer.md.new)

Would you like to review the updated files now?
```

### Example 2: Review Updates
```
User: "Review the updates"

You:
Found 1 file to review:

**brainstormer.md.new**
- Added improved brainstorming process structure
- Added Phase 2: Divergent Thinking details
- Your version has marketing-specific expert perspectives

Recommendation: Merge - combine your marketing focus with new structure

Would you like me to:
1. Show detailed diff
2. Help merge them
3. Just use the new version
4. Keep your current version
```

### Example 3: Copy Commands
```
User: "Copy the content commands"

You:
Copying content commands from Engineer to Marketing...

✅ Copied:
- content/good.md → .marketing/commands/content/
- content/fast.md → .marketing/commands/content/
- content/cro.md → .marketing/commands/content/
- content/enhance.md → .marketing/commands/content/

These commands are now available in Marketing!

Test them: `cd ~/claudekit-marketing && claude`
```

### Example 4: Check for Updates
```
User: "Check if there are Engineer updates"

You:
Checking ClaudeKit Engineer for updates...

✅ Engineer is 2 commits ahead:
- feat: add content/cro command for conversion optimization
- fix: improve brainstormer categorization logic

Updates are available. Would you like to sync Marketing now?
```

### Example 5: Compare Specific File
```
User: "Compare the brainstormer changes"

You:
Comparing brainstormer.md versions...

**Your Version (Marketing):**
- Has marketing-specific expert perspectives
- Focuses on campaign ideation
- Includes brand alignment checks

**New Version (Engineer):**
- Improved brainstorming process structure
- Better phase organization
- Enhanced examples

**Key Differences:**
- New adds structured phases (Discovery, Divergent, Convergent)
- Your version has marketing-specific focus areas
- Both have value

**Recommendation:** Merge
Keep your marketing perspectives, add the new process structure.

Would you like me to help merge them?
```

---

## 🔧 Helper Functions

### Parse Sync Output
```bash
# Extract counts and lists from sync script output
# Return structured data for reporting
```

### Find .new Files
```bash
find /Users/sam/claudekit-marketing/.marketing/ -name "*.new" -type f
```

### Compare Files
```bash
diff file1 file2
# Parse and summarize differences
```

### Get File Type
```bash
# Determine if agent, command, skill, hook
# Return category for appropriate handling
```

---

## 📚 Documentation References

**Decision Framework:**
`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault-4/Claude Code/CK-Marketing/DECISION-FRAMEWORK.md`

**Sync Guide:**
`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault-4/Claude Code/CK-Marketing/SYNC-FROM-ENGINEER.md`

**Review Guide:**
`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault-4/Claude Code/CK-Marketing/REVIEWING-UPDATES.md`

---

## ⚠️ Important Notes

1. **Two-Step Process:** Always `git pull` Engineer before running sync script
2. **Safe Sync:** Commands and agents use safe sync (never overwrite)
3. **Customizations Protected:** .new files created instead of overwriting
4. **User Decides:** Skill helps decide, doesn't auto-apply updates
5. **Test Before Commit:** Always test Marketing after syncing

---

## ✅ Success Criteria

**Skill succeeds when:**
- ✅ User can sync with simple natural language
- ✅ Clear reports of what changed
- ✅ Easy to review updates
- ✅ Simple to apply decisions
- ✅ Customizations always protected
- ✅ Marketing stays current with Engineer

---

Your goal: Make syncing ClaudeKit Marketing effortless while protecting customizations and giving users full control.
