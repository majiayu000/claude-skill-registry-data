---
name: learnings-log
description: |
  Historical record of expert tips and learnings that have been integrated into the plugin skills.
  Consult this when patterns emerge or to understand the evolution of knowledge.
---

# Learnings Log

This skill tracks all successful expert tips that have been integrated into the plugin's knowledge base. Each entry records what was learned and which skills were updated.

## Purpose

- **Historical record**: See what tips have been provided
- **Pattern detection**: Identify common issues or knowledge gaps
- **Validation**: Verify learnings are being properly integrated
- **Evolution tracking**: Understand how the plugin's knowledge grows

## Log Format

Each learning entry should include:
- **Date**: When the tip was provided
- **Context**: What was stuck or going wrong
- **Tip**: The expert guidance provided
- **Skills Updated**: Which skill files were modified
- **Key Learning**: Summary of what was learned

## Learning Entries

### 2026-01-06: Rollups Should Operate on Relations, Not Whole Tables

**Context**: Attempting to add rollup columns to a CRM app to show insights like count of contacts per company and sum of deal amounts. Was about to create rollups that would operate directly on entire tables, which would have shown global totals instead of per-company totals.

**Tip Provided**:
> "Rollups should mainly be used in coordination with a relation or query column and rarely the whole table. For example using a rollup and selecting a table and a column in that table will count the number of rows in that table. If you did that against a relation it would count the number of related items it found which is much more useful in many cases. Ex Orders > Order items. If i related from the order to order items, i could then count the number of order items in that order versus counting all order items in the table."

**Skills Updated**:
- `computed-columns/SKILL.md` - Section: "Rollup Columns"
  - Added: "CRITICAL CONCEPT" callout that rollups should operate on Relation columns
  - Added: Explanation of why (rollups on relations auto-filter to related rows)
  - Added: "Why Use Relations with Rollups" section with pattern diagram
  - Added: Example showing WRONG vs RIGHT approach for Order Items counting
  - Added: Complete CRM example matching the user's actual use case (Companies → Contacts/Deals)
  - Added: "When to Use Rollup on Whole Table" section (rare cases like dashboards)
  - Updated: Setup steps to emphasize creating Relation first
  - Added: Common Rollup Patterns table with real-world examples
- `data-modeling/SKILL.md` - Section: "Relation & Lookup Pattern"
  - Added: IMPORTANT note that rollups should operate on relations, not tables
  - Added: Cross-reference to computed-columns skill for detailed guidance

**Key Learning**: Rollups should almost always operate on a Relation column, not directly on a table. Rollups on relations automatically filter to only related rows, while rollups on entire tables aggregate ALL rows (rarely useful).

**Impact**: Prevents a critical common mistake that would cause rollups to show meaningless global totals instead of per-row aggregations. This is especially important in CRM apps, order systems, and any app with one-to-many relationships. Makes the Relation → Rollup pattern explicit and teachable.

---

### 2025-12-31: Action Button Ordering and Multiple Actions

**Context**: Task required adding an email button to send location information. The Edit button was appearing as the primary (leftmost) button, and the new Email Info button was secondary. Needed to understand how action ordering works in Glide.

**Tip Provided**:
> "In 'Actions' anywhere in Glide the top 'action' is the left most button. So in the current app we have Edit at the top and edit is the main thing seen. If we don't need to be able to edit that page, we should just remove this button. Alternatively, you can move edit below another action to get the other action to appear first."

**Skills Updated**:
- `layout/SKILL.md` - Section: "Actions"
  - Created: New "Action Button Ordering" subsection at top of Actions section
  - Added: Core rule - top action in list = leftmost button in UI
  - Added: Visual example showing list order vs UI display order
  - Added: Step-by-step instructions for reordering actions via drag-and-drop
  - Added: Guidance on making an action primary (move to top or remove others)
  - Added: Common use case about removing/reordering default Edit action

**Key Learning**: In Glide's actions list, the top action appears as the leftmost button in the UI. To control button prominence, drag actions to reorder them or remove unwanted actions.

**Impact**: Prevents confusion about why buttons appear in unexpected order. Makes it clear how to prioritize custom actions over default actions like Edit. Essential for creating intuitive UIs with multiple action buttons.

---

### 2025-12-31: Send Email Action - Recipient Field Configuration

**Context**: Send Email action wasn't working because the To, Cc, and Bcc fields weren't configured correctly for the use case of emailing location information to the logged-in user.

**Tip Provided**:
> "Send Email action isn't working because the to, cc, and bcc field aren't configured correctly. For this case, use the user's email address as the To field and clear the others"

**Skills Updated**:
- `layout/SKILL.md` - Section: "Email Actions"
  - Added: New "Configuring Send Email action" subsection
  - Added: Detailed guidance for each recipient field (To, Cc, Bcc)
  - Added: How to send to logged-in user (User / Email binding)
  - Added: How to send to specific person (email column from data)
  - Added: Guidance on when to clear optional fields (Cc/Bcc)
  - Added: Common mistake note about leaving fields configured unnecessarily
  - Added: Complete example for emailing to logged-in user with cleared Cc/Bcc

**Key Learning**: Send Email actions require careful configuration of recipient fields. For sending to the logged-in user, use `User / Email` for the To field and clear Cc/Bcc if not needed.

**Impact**: Prevents Send Email actions from failing due to misconfigured recipient fields. Clarifies the difference between required (To) and optional (Cc/Bcc) fields. Makes it clear how to bind to the logged-in user's email address.

---

### 2025-12-31: Reordering Actions via Drag-and-Drop

**Context**: Needed to make the Email Info action the primary button by moving it above the Edit action in the actions list. Initial attempt didn't work because the method wasn't clear.

**Tip Provided**:
> "You still haven't ordered the actions correctly. You need to drag Email Info action above the 'Add Action' piece"

**Skills Updated**:
- `layout/SKILL.md` - Section: "Action Button Ordering"
  - Added: Specific instruction to drag actions to reorder them
  - Added: Note that actions can be moved above or below each other
  - Added: Clarification that UI button order updates automatically

**Key Learning**: To reorder actions in Glide, click and drag the action in the actions list to move it above or below other actions.

**Impact**: Makes the reordering mechanism explicit. Prevents confusion about how to actually change action order once you understand the top-to-bottom = left-to-right rule.

---

### 2025-12-31: Using CMD+Z to Undo Mistakes

**Context**: Accidentally deleted the Email Info action while trying to reorder actions. Needed to quickly restore it without rebuilding.

**Tip Provided**:
> "Stop you just deleted the email action, quick CMD+Z to get it back"

**Skills Updated**:
- `glide/SKILL.md` - Section: "Browser Automation Tips > Keyboard shortcuts"
  - Added: CMD+Z / CTRL+Z to keyboard shortcuts list
  - Created: New "Undo mistakes" subsection
  - Added: Explanation of Glide's undo functionality
  - Added: Common scenarios where undo is useful (deleted action, removed component, changed setting)
  - Added: Important note about undo only working for recent actions in current session

**Key Learning**: Glide Builder supports standard undo functionality with CMD+Z (macOS) or CTRL+Z (Windows) to revert recent changes.

**Impact**: Prevents need to rebuild components/actions that are accidentally deleted. Provides a safety net during browser automation. Critical for recovering from automation errors without starting over.

---

### 2025-12-31: Send Email vs Compose Email Actions

**Context**: Task required adding a button to send an email with location information. Initially selected "Compose email" action, but this would open the user's email app rather than send programmatically.

**Tip Provided**:
> "Send email uses Glide's built in email service to send emails. Compose email opens the users default email app to send an email. For most cases we want to use the Send Email action unless the user specifically asks to open their email app."

**Skills Updated**:
- `layout/SKILL.md` - Section: "Actions"
  - Created: New "Email Actions" section separating Send Email and Compose Email
  - Added: Detailed explanation of Send Email (Glide's built-in service, recommended default)
  - Added: Detailed explanation of Compose Email (opens user's email app, use only when explicitly requested)
  - Added: Use cases and examples for each action type
  - Added: Clear guidance on default choice (Send Email unless user specifically asks for email app)
  - Updated: "Other Actions" section to remove combined "Compose Email/SMS" entry, added separate "Send SMS" entry

**Key Learning**: "Send Email" and "Compose Email" are two distinct actions with different behaviors - Send Email uses Glide's service to send programmatically (recommended default), while Compose Email opens the user's email app (use only when explicitly requested).

**Impact**: Prevents confusion about which email action to use. Ensures automated email features work correctly without requiring user interaction. Makes the distinction clear between programmatic sending and manual composition.

---

### 2025-01-01: Initial Log Created

This learnings log was created as part of the self-learning `/tip` command feature.

**Purpose**: Enable the plugin to learn from expert feedback and continuously improve its knowledge base.

---

<!-- New learnings will be added below this line in reverse chronological order -->

### 2025-12-31: Keyboard Shortcut for Adding Columns

**Context**: Builder agent needed to add a 'created date' column to the locations table. Manual column creation via UI clicks can be slow and less reliable.

**Tip Provided**:
> "Whenever you need to add a column it will always need done via browser automation. You can navigate to a table and then use the keyboard shortcut CMD+SHIFT+ENTER to create a new column. This is much faster"

**Skills Updated**:
- `data-modeling/SKILL.md` - Section: "Creating Columns via UI"
  - Added: Keyboard shortcut method as the recommended approach (CMD+SHIFT+ENTER)
  - Added: Step-by-step workflow for keyboard shortcut method
  - Added: Explanation of why this method is preferred (faster, more reliable)
  - Reorganized: Manual UI method as alternative approach
- `glide/SKILL.md` - Section: "Data Editor > Adding Columns"
  - Added: Note that all column creation requires browser automation (API doesn't support it)
  - Added: Keyboard shortcut method as recommended approach
  - Updated: Emphasized that keyboard shortcut is significantly faster
- `glide/SKILL.md` - Section: "Browser Automation Tips > Keyboard shortcuts"
  - Added: CMD+SHIFT+ENTER shortcut to the keyboard shortcuts reference list

**Key Learning**: CMD+SHIFT+ENTER is the fastest and most reliable way to add columns in Glide when using browser automation.

**Impact**: Significantly speeds up column creation workflows. Makes automation more efficient and reduces reliance on fragile UI click sequences. This is especially valuable when adding multiple columns or when building apps with complex data models.

---

## Usage Notes

### For the skill-learner agent:

When you update skills based on a tip, also add an entry to this log:

```markdown
### YYYY-MM-DD: [Brief Title]

**Context**: [What was stuck or going wrong]

**Tip Provided**:
> [The user's tip in their own words]

**Skills Updated**:
- `skill-name/SKILL.md` - Section: [section name]
  - Added: [brief description of what was added]

**Key Learning**: [One-sentence summary of the core insight]

**Impact**: [Why this matters / what problem this prevents]

---
```

### For reviewing patterns:

Periodically review this log to identify:
- **Recurring themes**: Are similar tips being provided? Might indicate a gap in the main skills
- **Complex areas**: Which topics generate the most tips? May need better documentation
- **Success patterns**: What types of tips integrate most successfully?

### Example Entry

```markdown
### 2025-01-15: Emoji Picker Navigation

**Context**: Builder agent was stuck trying to select an app icon, kept failing to click the right emoji from the category view.

**Tip Provided**:
> "Don't browse the emoji categories. Always use the search box - type the emoji name like 'rocket' or 'checkmark' and click the result. It's much faster and more reliable."

**Skills Updated**:
- `glide/SKILL.md` - Section: "Creating New App"
  - Added: Detailed guidance on emoji picker search workflow
  - Added: Note about avoiding category browsing
- `layout/SKILL.md` - Section: "UI Navigation Patterns"
  - Added: General emoji picker usage pattern

**Key Learning**: Glide's emoji picker is optimized for search, not browsing - category navigation is unreliable for automation.

**Impact**: Prevents future failures when setting app icons or using emoji fields. Makes icon selection deterministic.

---
```

## Statistics

As tips accumulate, track:
- Total tips integrated: [number]
- Most frequently updated skills: [list]
- Common categories: [UI navigation, API usage, workflows, etc.]

## Integration with /tip Command

The `/tip` command automatically:
1. Calls skill-learner agent to update relevant skills
2. skill-learner agent adds entry to this log
3. User can review both skill updates and log entry

## Future Enhancements

Consider adding:
- Searchable index of learnings by topic
- Links from log entries to specific skill sections
- Rollback capability (revert a learning if it was incorrect)
- Export functionality to share learnings with other users
- Automatic pattern detection (analyze log for recurring themes)
