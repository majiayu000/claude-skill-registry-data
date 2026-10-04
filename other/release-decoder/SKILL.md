---
name: release-decoder
description: This skill should be used when the user pastes Claude Code release notes, changelogs, or version updates and wants to understand what changed in plain English. Triggers on phrases like "what's new", "explain this update", "process this release", "what does this changelog mean", "decode this", or when text contains version numbers like v2.0.70, the word "Released", "Changes:", "Bug fixes", or "New features". The skill translates technical jargon, assesses relevance to the user's specific CLAUDE.md setup, executes actions with approval, and saves insights to Memory MCP.
---

# Release Decoder

Transform Claude Code release notes from developer jargon into personalized, actionable insights.

## When This Skill Activates

- User pastes release notes or changelog
- User asks "what's new in Claude Code?"
- User asks "what does this update mean?"
- User says "decode this" or "explain this release"
- Text contains version patterns like "v2.0.70" or "Released!"

## The Translation Pipeline

For every release note, apply this 8-step pipeline:

```
Raw Update → Category → Plain English → Relevance Check → DETECT INTEGRATIONS → Action → VERIFY TEST → Memory Save
```

**CRITICAL:** Steps 3.5 (Detect Integrations) and 4.5 (Verify Test) are MANDATORY. Never skip them.

## Step 1: Parse and Categorize

Extract each changelog item and assign ONE category:

| Category | Icon | Meaning | Typical Action |
|----------|------|---------|----------------|
| Bug Fix | 🐛 | Something broken is now fixed | Usually awareness only |
| New Feature | ✨ | New capability added | Learn it, try it |
| Performance | ⚡ | Faster/smoother operation | Good to know |
| Settings | ⚙️ | New configuration option | May update CLAUDE.md |
| UX | 💅 | Better interface experience | Learn new interaction |
| Breaking | ⚠️ | Change that requires action | MUST address |

## Step 2: Translate to Plain English

Reference `references/tech-glossary.md` for term translations.

**Translation Template:**
```
**What changed:** [One sentence a non-coder would understand]
**In plain terms:** [Analogy or real-world comparison if helpful]
```

**Examples:**

| Technical | Plain English |
|-----------|---------------|
| "Added wildcard syntax mcp__server__*" | "You can now allow all tools from a service with one line instead of listing each separately" |
| "Fixed IME composition window positioning" | "Typing in Chinese, Japanese, or Korean now works better" |
| "Improved memory usage by 3x" | "Claude Code uses less of your computer's resources during long conversations" |
| "Added plan_mode_required spawn parameter" | "When using helper tasks, you can now require approval before they make changes" |

## Step 3: Assess Relevance to User

Read the user's CLAUDE.md (both global and project-specific) to determine relevance.

**Check for:**
1. **Skills they use** - Does update affect frontend-design, dev-browser, memory, etc.?
2. **Workflows mentioned** - PRD-driven, session protocols, 40% context rule, etc.
3. **Platform** - macOS/Windows/Linux (user is on macOS)
4. **Language** - English typing means CJK/IME updates are low priority
5. **MCP tools** - Which servers do they have configured?

## Step 3.5: Detect User Integrations (MANDATORY)

**BEFORE saying "no action needed", search for user integrations that might use the new feature.**

For each HIGH/MEDIUM relevance update, run these checks:

| Feature Type | Search For | Commands |
|--------------|------------|----------|
| Status line changes | Custom status line scripts | `ls ~/.claude/*status* ~/.claude/commands/*status*` |
| MCP/permissions | Custom settings.json | `cat ~/.claude/settings.json \| jq '.permissions'` |
| Context tracking | Scripts using context data | `grep -r "context_window\|current_usage" ~/.claude/` |
| Hooks | Custom hooks | `ls ~/.claude/hooks/` |
| Plugins | Plugin configs | `ls ~/.claude/plugins/` |

**If integration found:**
1. READ the integration file
2. CHECK if it uses the new feature's data/API
3. TEST if it's working correctly with actual output
4. ONLY THEN decide if action is needed

**Example - Status Line Update:**
```bash
# 1. Check for custom status line
ls ~/.claude/*status*

# 2. If found, read it
cat ~/.claude/statusline-command.sh

# 3. Check if it uses the new field
grep "current_usage" ~/.claude/statusline-command.sh

# 4. Test actual output - compare debug data to /context
cat /tmp/statusline-debug.json

# 5. If mismatch → action IS needed (update the script)
```

**NEVER skip this step.** "Version matches" is NOT proof that features work.

**Relevance Scores:**

| Score | Icon | Criteria | Action Required |
|-------|------|----------|-----------------|
| HIGH | 🔴 | Directly affects their workflow, fixes bug they might hit | Yes - offer to execute |
| MEDIUM | 🟡 | New capability they could adopt | Optional - explain benefits |
| LOW | 🟢 | Doesn't affect current setup | Mention briefly |
| N/A | ⚪ | For platforms/features they don't use | Skip entirely |

## Step 4: Generate Actions

For HIGH and MEDIUM relevance items, determine specific actions:

### Action Types

| Type | When | Format |
|------|------|--------|
| **Update Claude** | New version available | Offer to run `claude update` |
| **Update CLAUDE.md** | New setting/permission relevant | Show exact text to add |
| **Try Feature** | New capability useful to them | Provide copy-paste prompt |
| **No Action** | Bug fix, awareness only | Just explain what changed |

### Execution Workflow

For executable actions:

1. **Explain** what will happen in plain English
2. **Ask permission** using AskUserQuestion tool with clear options
3. **Execute** the action (run command, edit file)
4. **Verify with REAL TEST** (see Step 4.5 below)
5. **Report** result with proof

## Step 4.5: Verify with Real Test (MANDATORY)

**NEVER say "done" or "no action needed" without an actual test.**

| Verification Type | What to Test | How to Verify |
|-------------------|--------------|---------------|
| Version update | Feature actually works | Run the feature, check output |
| Status line change | Percentages match /context | Compare status line % to `/context` output |
| Permission change | Tools actually accessible | Try using the tool |
| Config change | Setting takes effect | Check behavior changed |

**Verification Template:**
```
## Verification
**Expected:** [What should happen]
**Actual test:** [Command/action run]
**Result:** [Actual output]
**Match?** ✅ Yes / ❌ No - needs fix
```

**Example - Status Line Verification:**
```bash
# What we expect: status line shows ~same % as /context

# Test 1: Check /context
/context  # Shows 82%

# Test 2: Check status line debug
cat /tmp/statusline-debug.log | tail -1
# Shows: total=74166 → 37%

# Result: ❌ MISMATCH - status line script needs update
# Action: Fix the script, not "no action needed"
```

**If test fails → fix it before saying done.**
**If test passes → show the proof.**

**Example Execution (CORRECT):**
```
"There's a new version with a memory fix. Let me update and verify.

Shall I update Claude Code for you?"

[User approves]

*Runs: claude update*
*Output: Updated to v2.0.70*

*Verification: Testing memory improvement...*
*Runs long task to check memory behavior*

"✅ Verified: Updated to v2.0.70 and tested - memory usage is lower."
```

## Step 5: Save to Memory MCP

After processing, save relevant insights:

**Entities to Create/Update:**

```
Entity: "Claude Code Version"
Type: "software"
Observations:
  - "Currently running v2.0.70 (updated [date])"
  - "v2.0.70 has 3x memory improvement"

Entity: "User Setup - Claude Code"
Type: "configuration"
Observations:
  - "Uses macOS (Darwin)"
  - "Types in English"
  - "Uses MCP: memory, playwright, context7"

Entity: "Release Notes History"
Type: "log"
Observations:
  - "[date]: Processed v2.0.70 release - 3 relevant updates"
```

**What to Save:**
- Version updates applied
- Features the user tried
- CLAUDE.md changes made
- User preferences discovered during processing

## Step 6: Format Output

Structure the final response:

```markdown
# Claude Code [VERSION] - What It Means for You

## Quick Summary
[2-3 sentences: How many updates matter? Any must-do actions?]
[Offer to run update if new version]

---

## 🔴 HIGH PRIORITY: [Title]

**What changed:** [Plain English]

**Why this matters to YOU:** [Reference their CLAUDE.md setup]

**Action:** [What to do]

> Shall I [specific action]? [Options if applicable]

---

## 🟡 NICE TO HAVE: [Title]

**What changed:** [Plain English]

**Why you might want this:** [Benefit explanation]

**To try it:** [Example prompt or steps]

---

## ⚪ Skipped (Not Relevant to You)

[One-line summaries of LOW/N/A items with brief reason why skipped]

---

## Saved to Memory

✓ [What was remembered for next time]
```

## Example Processing

**Input:**
```
Claude Code v2.0.70 Released!

Changes:
• Added wildcard syntax mcp__server__* for MCP tool permissions
• Improved memory usage by 3x for large conversations
• Fixed IME support for Chinese, Japanese, and Korean
```

**Output:**
```markdown
# Claude Code v2.0.70 - What It Means for You

## Quick Summary
2 updates matter to you. One improves your long conversations,
one simplifies your settings. Shall I update Claude Code now?

---

## 🔴 HIGH PRIORITY: Memory Improvement

**What changed:** Claude Code now uses 3x less computer memory
during long conversations.

**Why this matters to YOU:** Your CLAUDE.md mentions the 40% context
rule and session management. This fix means Claude will run smoother
during your long work sessions.

**Action:** I'll update Claude Code for you.

> Shall I run `claude update`? [Yes/No]

---

## 🟡 NICE TO HAVE: Simpler Permissions

**What changed:** Instead of listing every tool permission separately,
you can now use `mcp__memory__*` to allow ALL memory tools at once.

**Why you might want this:** Your CLAUDE.md has a long permissions list.
This could make it cleaner.

**Current (many lines):**
```
mcp__memory__create_entities
mcp__memory__search_nodes
mcp__memory__read_graph
```

**Simpler (one line):**
```
mcp__memory__*
```

> Want me to simplify your permissions? [Yes/No]

---

## ⚪ Skipped (Not Relevant to You)

- IME support for Chinese/Japanese/Korean → You type in English

---

## Saved to Memory

✓ Remembered: Processing v2.0.70 release on [date]
✓ Remembered: Wildcard permissions now available
```

## Handling Edge Cases

### Ambiguous Updates
If an update's impact isn't clear:
- Explain what it MIGHT mean
- Offer a test prompt to verify
- Note "This may or may not affect you"

### Related Updates
Group updates that work together:
```
### Related: [Theme]
These updates work together to [combined effect]
```

### No Relevant Updates
If all updates are N/A:
```
## Quick Summary
No updates in this release affect your setup.
You can skip this version unless you want the latest.

Here's what changed (for reference):
[Brief list]
```

## Resources

### references/tech-glossary.md
Comprehensive glossary of technical terms translated to plain English.
Reference this when encountering unfamiliar technical terms.

Categories covered:
- Core concepts (MCP, context, tokens)
- Interface terms (IME, status line, diff)
- Configuration terms (wildcards, permissions, hooks)
- Platform terms (macOS, Windows, Linux)
- Common phrases decoded
