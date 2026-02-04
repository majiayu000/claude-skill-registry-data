---
name: summarizing-conversations-to-obsidian
description: Use when user requests to save conversation summary to Obsidian, mentions "总结", "保存笔记", "卡片笔记", or Zettelkasten - creates atomic, well-structured notes following Zettelkasten principles without guessing paths or formats
---

# Summarizing Conversations to Obsidian

## Overview

**Summarize conversations into atomic Zettelkasten-style notes for Obsidian.**

Core principle: ALWAYS use Zettelkasten format, NEVER guess vault paths, focus on insights over transcripts.

## When to Use

Use when user:
- Requests to save conversation to Obsidian
- Says "总结", "保存笔记", "整理成 markdown"
- Mentions "卡片笔记" or Zettelkasten
- Asks to create notes from current conversation

## The Iron Law

```
NEVER GUESS THE OBSIDIAN VAULT PATH
```

**No exceptions:**
- Not for "stressed users"
- Not for "common paths"
- Not for "it's probably ~/Documents/Obsidian"
- Not for "action over asking"
- Not for "Desktop/Notes seems reasonable"

If user didn't provide path: ASK. If you guessed: DELETE the file. Start over.

## Zettelkasten Format (ALWAYS)

**Every note MUST be atomic, focused, and follow this structure:**

```markdown
---
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
type: technical-session | problem-solution | concept | reference
---

# Clear, Specific Title

## Core Insight/Problem

[1-2 paragraphs capturing the essence]

## Solution/Approach (if applicable)

[Key decisions and reasoning]

## Key Details

- Bullet points for important specifics
- Code snippets ONLY if essential
- Configuration examples if critical

## Related Concepts

[[Link to Related Note 1]]
[[Link to Related Note 2]]

## Reflection/Takeaway

[One paragraph: what's the lasting insight?]
```

**What to INCLUDE:**
- Core problems and solutions
- Key decisions and trade-offs
- Important code patterns (< 20 lines)
- Actionable insights
- Links to related concepts

**What to EXCLUDE:**
- Trial-and-error process
- Failed attempts (unless they teach something)
- Conversational tangents
- Philosophical debates (unless that's the point)
- All code (only essential snippets)

## File Naming

**Format:** `主题 + 核心概念.md`

Examples:
- ✅ `React useEffect 依赖陷阱修复.md`
- ✅ `分布式事务 Saga 模式对比.md`
- ✅ `TypeScript 泛型约束最佳实践.md`
- ❌ `对话总结 2025-10-21.md` (too generic)
- ❌ `Notes.md` (meaningless)

**Rules:**
- Descriptive and specific
- Include key technology/concept
- Use Chinese if user is Chinese-speaking
- Keep under 50 characters

## Standard YAML Frontmatter

**Required fields:**

```yaml
---
date: YYYY-MM-DD  # Today's date
tags: [max-5-tags]  # Specific, searchable tags
type: technical-session | problem-solution | concept | reference
---
```

**Tag guidelines:**
- Use technology names: `react`, `typescript`, `postgres`
- Use problem domains: `authentication`, `performance`, `testing`
- Use patterns: `hooks`, `state-management`, `async`
- Max 5 tags - be selective
- Lowercase, hyphenated

## Workflow

1. **Check for vault path**
   - User provided path? → Use it
   - No path provided? → ASK: "你的 Obsidian vault 路径是？"

2. **Analyze conversation**
   - What was the core problem?
   - What was the key insight/solution?
   - What decisions were made and why?
   - What's worth remembering in 6 months?

3. **Create atomic note**
   - ONE main idea per note
   - If conversation covered 3 distinct topics → suggest 3 notes
   - Focus on insights, not transcript

4. **Write the note**
   - Use Zettelkasten structure above
   - Include YAML frontmatter
   - Meaningful filename
   - Essential code only (< 20 lines per snippet)

5. **Save and confirm**
   - Save to provided path
   - Show filename and path
   - Offer to create additional notes if needed

## Handling Long Conversations

For 60+ minute conversations covering multiple topics:

**DON'T create one giant 500-line document.**

**DO:**
1. Identify 3-5 distinct atomic concepts
2. Suggest creating multiple notes
3. Create index note with links to sub-notes
4. Each sub-note follows Zettelkasten format

Example:
```
分布式系统架构讨论-索引.md  # Index note
├── Saga 模式实现要点.md
├── 事件溯源 vs CQRS 对比.md
├── 共识算法 Raft 简化理解.md
└── CAP 定理实践权衡.md
```

## Content Curation Rules

**Code snippets:**
- Include if < 20 lines AND essential to understanding
- Show pattern, not implementation details
- Add comments explaining the key insight
- If longer: link to gist/repo instead

**Failed attempts:**
- EXCLUDE unless failure teaches important lesson
- Focus on "what worked" and "why it works"

**Discussions and debates:**
- INCLUDE conclusion and key arguments
- EXCLUDE back-and-forth unless it reveals insight

**TODO items:**
- CREATE separate "## Next Steps" section
- Use checkboxes: `- [ ] Task description`
- Be specific and actionable

## Red Flags - STOP

- Guessing vault path ("probably ~/Documents/Obsidian")
- Creating 300+ line comprehensive documents
- "This was valuable, I should include everything"
- "'整理' means they want detailed docs"
- "User is stressed, I'll guess the path"
- "Action over asking"
- Including all code examples

**All of these mean: STOP. Follow the rules.**

## Quick Reference

| Situation | Action |
|-----------|--------|
| No vault path provided | ASK for path, don't proceed |
| User says "整理" | Still Zettelkasten (atomic, focused) |
| 90-min conversation | Suggest multiple atomic notes |
| Lots of code shared | Include < 20 lines of essential patterns only |
| Trial and error process | Exclude attempts, include solution |
| User seems stressed | Still ASK for path if needed |

## Example

**Bad approach:**
```
User: 总结一下保存到 Obsidian
Agent: [creates file at ~/Documents/Obsidian/Notes.md]
```
❌ Guessed path, generic filename

**Good approach:**
```
User: 总结一下保存到 Obsidian
Agent: 你的 Obsidian vault 路径是？
User: ~/Obsidian/技术笔记/
Agent: [creates atomic note with proper structure]
已保存到: ~/Obsidian/技术笔记/Node.js 内存泄漏排查方法.md
```
✅ Asked for path, specific filename, atomic note

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Guessing common paths | Always ask if not provided |
| "整理" = comprehensive docs | "整理" still means Zettelkasten |
| Including all code | Only essential patterns < 20 lines |
| One note for 5 topics | Create 5 atomic notes |
| Generic filenames | Specific: `技术 + 概念.md` |
| Missing YAML frontmatter | Always include date, tags, type |

## The Bottom Line

**Zettelkasten = atomic notes with insights, not transcripts.**

Never guess paths. Always atomic. Focus on what matters in 6 months, not what happened in 90 minutes.
