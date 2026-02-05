---
name: capture-new-idea
description: Capture user ideas verbatim in .wrangler/ideas/ directory using the MCP issues_create tool with type='idea'. Preserves exact user wording without interpretation or enhancement.
---

# Capture New Idea

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: capture-new-idea | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: capture-new-idea | Capturing user's feature suggestion
```

This creates an audit trail showing which skills were applied during the session.

## Purpose

This skill captures user ideas exactly as stated, without interpretation, enhancement, or reformulation. Ideas are stored in `.wrangler/ideas/` directory for future consideration and refinement.

## Core Principle

**PRESERVE USER'S EXACT WORDING** - Do not:
- Rephrase or enhance the idea
- Add technical details
- Interpret what the user "meant to say"
- Convert to requirements or specifications
- Add implementation suggestions

The idea artifact type exists to capture raw thoughts before they undergo refinement into specifications or issues.

## When to Use This Skill

Use this skill when the user:
- Suggests a feature or improvement casually
- Mentions "it would be nice if..."
- Says "I've been thinking about..."
- Proposes something without concrete details
- Shares a rough concept or vision
- Wants to "capture this for later"

**DO NOT use for**:
- Detailed feature requests (use `writing-specifications` skill)
- Bugs or issues (use `create-new-issue` skill)
- Concrete implementation tasks (use `writing-plans` skill)
- Ideas that are already refined into specs

## Process

### 1. Extract User's Exact Words

Identify the core idea from the user's message. Use their exact phrasing where possible.

**Example:**
- User says: "It would be cool if users could export their data as PDF"
- Title: "Export data as PDF"
- Description: "It would be cool if users could export their data as PDF"

### 2. Create Idea Using MCP Tool

Call the `issues_create` MCP tool with:

```javascript
issues_create({
  title: "Short, clear title from user's words",
  description: "User's idea in their own words (verbatim or lightly formatted)",
  type: "idea",
  status: "open",
  priority: "medium",  // Default unless user indicates urgency
  labels: [],  // Add contextual labels if obvious (e.g., ["ui", "export"])
  // Leave assignee, project, wranglerContext empty unless specified
})
```

### 3. Field Guidelines

**title** (required):
- Extract core concept from user's statement
- Keep concise (under 50 characters ideal)
- Use user's terminology, not technical jargon
- Example: "Dark mode option" not "Implement theme switching system"

**description** (required):
- Use user's exact words when possible
- If user provided multiple sentences, keep them all
- Add minimal formatting (line breaks, bullets) for readability only
- NO interpretation, NO enhancement, NO technical details
- Template: See [IDEA_TEMPLATE.md](templates/IDEA_TEMPLATE.md)

**type**: Always `"idea"`

**status**: Always `"open"` (ideas start as open until reviewed)

**priority**:
- `"low"` - Nice to have someday
- `"medium"` - Default for most ideas
- `"high"` - User explicitly emphasizes importance
- `"critical"` - Rarely used for ideas (only if user says "we really need this")

**labels** (optional):
- Add only obvious, non-interpretive labels
- Examples: `["ui"]`, `["mobile"]`, `["export"]`, `["performance"]`
- Avoid speculative labels like `["backend"]` unless user mentioned it

**assignee, project, wranglerContext**: Leave empty unless user explicitly specifies

## Examples

### Example 1: Simple Feature Idea

**User says:**
"I think we should add keyboard shortcuts for common actions"

**Create idea:**
```javascript
issues_create({
  title: "Keyboard shortcuts for common actions",
  description: "I think we should add keyboard shortcuts for common actions",
  type: "idea",
  status: "open",
  priority: "medium",
  labels: ["ui", "accessibility"]
})
```

### Example 2: Performance Concern

**User says:**
"The app feels slow when loading large datasets. Maybe we could add pagination or lazy loading?"

**Create idea:**
```javascript
issues_create({
  title: "Improve performance with large datasets",
  description: `The app feels slow when loading large datasets. Maybe we could add pagination or lazy loading?`,
  type: "idea",
  status: "open",
  priority: "medium",
  labels: ["performance"]
})
```

### Example 3: High Priority Idea

**User says:**
"We really need offline support - customers keep asking for it and it's affecting sales"

**Create idea:**
```javascript
issues_create({
  title: "Offline support",
  description: "We really need offline support - customers keep asking for it and it's affecting sales",
  type: "idea",
  status: "open",
  priority: "high",
  labels: ["feature"]
})
```

### Example 4: Vague Concept

**User says:**
"What if we made the UI more playful?"

**Create idea:**
```javascript
issues_create({
  title: "Make UI more playful",
  description: "What if we made the UI more playful?",
  type: "idea",
  status: "open",
  priority: "low",
  labels: ["ui", "design"]
})
```

## What Happens to Ideas

Ideas stored in `.wrangler/ideas/` can later be:
1. **Refined into specifications** - Use `writing-specifications` skill to develop the idea
2. **Converted to issues** - Use `issues_update` to change `type: "idea"` to `type: "issue"`
3. **Archived** - Close or delete ideas that are no longer relevant
4. **Grouped** - Add `project` field to group related ideas

## Anti-Patterns

**DON'T enhance the user's idea:**
```javascript
// ❌ WRONG - Adding details not mentioned by user
issues_create({
  title: "Implement OAuth2 authentication with JWT tokens",
  description: "Add OAuth2 authentication using industry-standard JWT tokens with refresh token rotation...",
  type: "idea"
})

// ✅ CORRECT - User's actual words
issues_create({
  title: "Better login system",
  description: "Users are complaining about having to log in too often",
  type: "idea"
})
```

**DON'T convert to requirements:**
```javascript
// ❌ WRONG - Turning idea into requirements
issues_create({
  title: "Search functionality",
  description: `Requirements:
- Full-text search across all fields
- Real-time results
- Autocomplete suggestions
- Filter by date range`,
  type: "idea"
})

// ✅ CORRECT - Keeping it as an idea
issues_create({
  title: "Better search",
  description: "It's hard to find things - we need better search",
  type: "idea"
})
```

## Template Reference

See [IDEA_TEMPLATE.md](templates/IDEA_TEMPLATE.md) for the structure of idea descriptions.

## Verification

After creating the idea:
1. Confirm the idea was created successfully
2. Note the ID assigned (e.g., "000042")
3. Inform user: "Captured your idea as #000042 in .wrangler/ideas/"
4. DO NOT start implementing or planning - ideas are for capture only

## Transition to Implementation

When an idea is ready for implementation:
1. User decides to pursue the idea
2. Use `writing-specifications` skill to create a detailed spec (new artifact)
3. OR use `issues_update` to convert idea to issue
4. OR use `writing-plans` skill to break into implementation tasks

Ideas remain raw capture until deliberately refined.
