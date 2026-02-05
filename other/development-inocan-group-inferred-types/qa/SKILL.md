---
name: qa
description: Generate QA steps for Jira tickets in German/English technical writing style
---

# QA Steps Generator

Generate comprehensive QA steps for the Jira ticket we've been working on, following my technical writing style.

## Instructions

**Context:** Use the ticket description, branch name, and implementation details from our conversation to create comprehensive QA steps. Output as markdown ready for copy-paste into Jira.

**Core rules (quick reference):**
- Language: German infinitives + English tech terms
- Structure: **Steps:** → actions → **Nach QA:** → close
- Grammar: Use infinitive forms (wechseln, öffnen, mergen, deployen)
- Code: Wrap in backticks (`branch-name`, `main`, `production`)
- Emojis: 🔍 verify, ↪️ merge, 🚀 deploy, 📕 close, 🌟 review
- Always end: "Ticket schließen. 📕"

**For complex cases or full details, read:** `~/.claude/skills/qa/QA_STYLE_GUIDE_FOR_AGENTS.md`.
