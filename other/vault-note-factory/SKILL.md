---
name: vault-note-factory
description: Unified note-creation router — detects what kind of note the content wants, runs pre-checks (duplicates, location, naming), and routes to the right skill or template. Use when the user says "create a note", "save this as a note", "new person/book/project note", or content needs filing and the type is unclear. NOT for digesting sources (use vault-source-digest for PDFs, vault-ai-conversation-digest for chat transcripts) or KB clause work (use eos-kb-atomize).
---

# Note Factory

Unified entry point for creating any type of note in the vault. Handles detection, pre-checks, and routing.

## Quick Reference

| User Says | Note Type | Routes To |
|-----------|-----------|-----------|
| "create note for X" | Auto-detect | (this skill decides) |
| "new person X" | Person | → people-manager |
| "new book X" | Book | → media-library |
| "new movie X" | Movie | → media-library |
| "new place X" | Place | → (this skill) |
| "new project X" | Project | → project-builder |
| "journal today" | Daily | → daily-journal |
| "save / file / digest this conversation" + pasted AI chat | AI transcript | → ai-conversation-digest |
| "I'll paste conversations and you note them properly" | AI transcript | → ai-conversation-digest |

---

## Pre-Creation Checklist

**ALWAYS run before creating any note:**

### 1. Search First (必须先搜索)

```
Before creating, search:
1. Exact name match
2. Partial/fuzzy match
3. Chinese/English equivalent
4. Related notes that might contain this info
```

**If found:**
- Existing note → Ask: "已有 [[X]]，要打开还是新建？"
- Related note → Ask: "在 [[Y]] 中有相关内容，要扩展还是新建？"

### 2. Determine Note Type

| Clues | Type |
|-------|------|
| Name of person, "met", "talked to" | Person |
| "went to", "visited", address, venue | Place |
| "reading", "book by", author mention | Book |
| "watched", "movie", "show", "series" | Movie/TV |
| "listening to", "album", "song" | Music |
| Goal + deadline, actionable | Project |
| Ongoing responsibility | Area note |
| Reference material, how-to | Resource |

### 3. Ask for Minimum Info

| Type | Required | Optional |
|------|----------|----------|
| Person | Name, Relationship | Location, Company |
| Place | Name, Type | Address, Why I go |
| Book | Title, Author | Status, Rating |
| Movie | Title | Year, Status |
| Project | Name, Goal | Deadline |

### 4. Create with Template

Route to appropriate skill:
- Person → `people-manager`
- Book/Movie/Music → `media-library`
- Daily/Weekly/Monthly → `daily-journal`
- Project → `project-builder`
- Place → (create directly, template below)

### 5. Link Strategy (必须执行)

**重要**：创建笔记后 **立即** 执行 Post-Creation Auto-Linking。

详细流程参考 `CLAUDE.md` 中的 "**4. Post-Creation Auto-Linking**" 部分。

**快速检查清单：**

```
✅ Step 0: 搜索是否已存在 (Obsidian CLI 优先)
   - bash obs.sh search "query=NoteName" limit=5
   - FALLBACK: Grep for 'NoteName' across *.md

✅ Step 1: 查找相关 MOC
   - 参考 CLAUDE.md 中的 MOC 路由表
   - 或用 Glob 搜索: _*MOC*.md

✅ Step 2: 更新 MOC
   - MOC 中添加新笔记链接
   - 新笔记 frontmatter 后添加 [[MOC名]] 回链

✅ Step 3: 建立双向链接
   - bash obs.sh backlinks file="Related Note"  (查找相关笔记)
   - FALLBACK: Grep for '\[\[Related Note' across *.md
   - 在相关笔记中添加链接到新笔记
   - 在新笔记中添加链接到相关笔记

✅ Step 4: 报告
   - 告诉用户完成了哪些链接操作
```

**不要跳过这一步！** 链接是笔记价值的核心。

---

## Note Type Templates

### Place Template

```yaml
---
tags:
  - place/<type>  # library, cafe, restaurant, park, etc.
  - place/<city>  # sydney, adelaide, etc.
type: place
location: City, State
address:
website:
hours:
---
```

```markdown
[[_places MOC]]

---

## About

Brief description.

## Why I Go Here

-

## Practical Info

| | |
|---|---|
| **Location** | |
| **Transport** | |
| **Cost** | |
| **WiFi** | |

## Visits

- YYYY-MM-DD: What I did

## Notes

-
```

---

## Type Detection Logic

When user says "create note for X" without specifying type:

```
1. Check context:
   - Recent conversation mentions (person? place? media?)
   - Nearby keywords ("met", "went to", "watched")

2. Check name patterns:
   - Capitalized words → likely Person or Place
   - "The X" → likely Movie/Show/Book
   - Contains "Library/Cafe/Park" → Place

3. If ambiguous, ask:
   "X 是什么类型？"
   1. 人物 (Person)
   2. 地点 (Place)
   3. 书籍 (Book)
   4. 电影/剧集 (Movie/TV)
   5. 其他 (Other)
```

---

## Workflows

### Universal Create

**User says**: "create note" / "new note" / "建立笔记"

**Workflow**:
1. Ask: "What/who is it?"
2. Detect type from response
3. If ambiguous, ask for type
4. Run pre-creation search
5. If no conflict, gather minimum info
6. Route to appropriate skill/template
7. Create note
8. Run post-creation linking

### Batch Create

**User says**: "create notes for A, B, C"

**Workflow**:
1. Parse entity list
2. Detect type for each
3. Group by type
4. Show summary: "将创建: 2个人物, 1个地点"
5. Confirm
6. Create all, show results

### Create from Journal

**Triggered by**: daily-journal entity detection

**Workflow**:
1. Receive entities from daily-journal
2. For each: run pre-creation check
3. Group new entities by type
4. Ask once for all
5. Create selected
6. Update journal with links

---

## Routing Table

| Type | Skill | Folder | Naming |
|------|-------|--------|--------|
| Person | people-manager | `30_Resources/People/` | `@Name.md` |
| Place | (direct) | `30_Resources/Places/` | `Name.md` |
| Book | media-library | `30_Resources/Books/` | `Title - Author.md` |
| Movie/TV | media-library | `30_Resources/Entertainment/` | `Title (Year).md` |
| Music | media-library | `30_Resources/Entertainment/Music/` | `Album - Artist.md` |
| Paper | media-library | `30_Resources/Electrical-Engineering/Papers/` | `Title.md` |
| Project | project-builder | `10_Projects/` | `Project Name.md` |
| Daily | daily-journal | `50_Journal/YYYY/` | `YYYY-MM-DD.md` |
| MOC | moc-manager | (varies) | `_name MOC.md` |

---

## Integration

This skill coordinates with:
- **obsidian-format**: Formatting rules (frontmatter, tags, links, dates) - **always follow**
- **daily-journal**: Receives detected entities, returns created notes
- **people-manager**: Delegates person creation
- **media-library**: Delegates book/movie/music creation
- **project-builder**: Delegates project creation
- **moc-manager**: Updates MOCs after creation

---

## Example Session

```
User: create note for Sarah

Claude: 搜索中... 未找到 "Sarah" 相关笔记。

Sarah 是什么类型？
1. 人物 (Person)
2. 其他

User: 1

Claude: 好的，创建人物笔记。

几个问题：
- 关系？(朋友/同事/家人)
- 在哪？(城市)

User: 朋友，Sydney

Claude: ✅ 已创建 30_Resources/People/@Sarah.md
- 已添加到 [[_300 people MOC]]
- 今天的日志已更新链接
```


## Verify after writing

After creating a note, confirm it landed correctly instead of assuming:

1. Re-read the created file. Frontmatter tags must be **block-style** (`tags:` then `  - person`), not inline `[a, b]`, and the type-defining tag must be present.
2. The note must sit in the folder its type implies, with the naming convention applied (`@Name.md` for people, `YYYY-MM-DD.md` for dailies).
3. If you added `[[wikilinks]]` (e.g. to a MOC or today's journal), run `python "80_Code/scripts/generate-link-index.py" --broken` and fix any link **you** introduced.

Report what you created with its path. If any check fails, fix it before reporting done.
