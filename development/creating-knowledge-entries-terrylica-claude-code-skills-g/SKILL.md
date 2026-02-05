---
name: creating-knowledge-entries
description: Create structured GitHub Issue knowledge entries with one-shot input. Handles auto-formatting, AI labeling, title extraction, and publishing. Use when user wants to share tips, document solutions, create how-tos, or add any knowledge to the base.
---

# Creating Knowledge Entries

One-shot knowledge capture with full automation.

## Trigger Detection

Activate this skill when user says:

- "I want to share knowledge"
- "Let me document this"
- "Add to knowledge base"
- "Share a tip"
- "Document this solution"
- "Create how-to"

## Workflow

### Step 1: Minimal Prompt

```
Just paste what you want to share (any format is fine):
```

**Critical:** Do NOT ask user about types, categories, or labels. User shares freely, AI decides everything autonomously.

### Step 2: Autonomous Processing

Process user input completely autonomously:

1. **Analyze existing labels** in repo (understand current taxonomy)
2. **Detect content type** via AI (tip, how-to, troubleshooting, reference, example, question)
3. **Extract title** via AI
4. **Format content** with appropriate template
5. **Suggest labels** based on existing taxonomy (or create new if empty)
6. **Link to related knowledge** via automated search
7. **Create GitHub Issue** with all decisions made

See [REFERENCE.md](REFERENCE.md) for complete automation pipeline.

### Step 3: Confirmation (What Was Decided)

```
✅ Created Issue #{number}!

📋 What I decided:
─────────────────────────────────────────
Title:    "{AI-extracted-title}"

Type:     {type-emoji} {type-name}

Labels:   {label1, label2, label3}
          (based on existing repo labels)

Format:   Structured with sections
          {auto-generated-sections}

Related:  Linked to #{n1}, #{n2}
─────────────────────────────────────────
🔗 {issue-url}

Search: gh search issues "{keywords}" --label={primary-label}
```

## Quick Example

**Input:**

```
tmux is great for persistent sessions. ctrl-b d to detach and
tmux attach to reattach. Useful when ssh connections drop.
```

**Output:**
Formatted GitHub Issue:

- **Title:** "Terminal: Using tmux for Persistent SSH Sessions"
- **Labels:** terminal, tips, workflow
- **Content:** Structured with "What It Does", "When to Use It", "Key Commands" sections
- **Related:** Auto-linked to similar terminal tips

## Dependencies

- `gh` CLI (issue creation)
- `gh-models` extension (AI labeling, title extraction)
- `jq` (JSON processing)

## Error Handling

Content too short (< 20 chars):

```
I need more content to create a useful knowledge entry.
Could you provide at least a sentence or two?
```

API fails:

```
⚠️  Couldn't create issue automatically. Here's the formatted content:
[formatted markdown shown]

Create manually: gh issue create --title "..." --body-file content.md
```

## Complete Reference

For detailed automation pipeline, templates, and examples, see [REFERENCE.md](REFERENCE.md).

---

**Repository:** https://github.com/terrylica/claude-code-skills-github-issues
