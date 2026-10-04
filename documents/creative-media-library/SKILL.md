---
name: creative-media-library
description: Manage books, movies, music, papers, podcasts in the vault — track consumption, analyze patterns, organize media notes (bilingual 书籍/电影/音乐). Use when the user says "log this book/movie", "what have I been reading", "rate this", or "add to want-to-watch". NOT for fetching paper PDFs (use tool-academic-search) or digesting a source into the KB (use vault-source-digest).
---

# Media Library

Comprehensive media and content management skill for tracking and analyzing consumption across multiple formats.

## Bilingual Search

Notes may be in Chinese or English. When searching:
- 书籍/book, 电影/movie, 音乐/music, 论文/paper
- 已读/read, 已看/watched, 想看/want-to-watch
- 评分/rating, 推荐/recommendation

Always search both languages when looking for media content.

## Location & Conventions

| Type | Folder | Naming |
|------|--------|--------|
| Books | `30_Resources/Books/` | `Title - Author.md` |
| Movies/TV | `30_Resources/Entertainment/` | `Title (Year).md` |
| Music | `30_Resources/Entertainment/Music/` | `Album - Artist.md` |
| Papers | `30_Resources/Electrical-Engineering/Papers/` | `Topic or Title.md` |
| Podcasts/Videos | `30_Resources/Entertainment/Podcasts-Videos/` | `Title.md` |

### MOC Pages (Maps of Content)
- `[[_books MOC]]` - Books navigation hub
- `[[_entertainment MOC]]` - Movies, Music, Podcasts navigation hub
- `[[_papers MOC]]` - Academic papers navigation hub

---

## Frontmatter Templates

### Books

```yaml
---
type: book
title: "Book Title"
author: "Author Name"
tags: [book, genre/fiction, topic/psychology]
# Reading Status
status: reading | completed | want-to-read | abandoned
date_started: YYYY-MM-DD
date_finished: YYYY-MM-DD
# Rating
rating: 1-10
# Metadata
publisher:
year:
pages:
isbn:
language: zh | en
# Source
source: kindle | physical | audible | pdf
---
```

### Movies/TV

```yaml
---
type: movie | tv-series
title: "Title"
original_title: "Original Title"
tags: [movie, genre/drama, director/name]
# Watch Status
status: watched | watching | want-to-watch
date_watched: YYYY-MM-DD
# Rating
rating: 1-10
imdb_rating:
# Metadata
director:
year:
runtime:
country:
language:
# Source
source: theater | streaming/netflix | download
---
```

### Music

```yaml
---
type: album | song | playlist
title: "Album Name"
artist: "Artist"
tags: [music, genre/jazz, mood/relaxing]
# Status
status: listening | favorite | archived
date_discovered: YYYY-MM-DD
# Rating
rating: 1-10
# Metadata
year:
label:
tracks:
# Source
source: spotify | apple-music | vinyl | cd
spotify_link:
---
```

### Papers/Academic

```yaml
---
type: paper | technical-doc | standard
title: "Paper Title"
authors: ["Author 1", "Author 2"]
tags: [paper, field/electrical, topic/cable-rating]
# Reading Status
status: read | reading | to-read | reference-only
date_read: YYYY-MM-DD
# Importance
importance: high | medium | low
cited_by_me: true | false
# Metadata
journal:
year:
doi:
conference:
# Related
related_project: "[[Project Name]]"
---
```

### Podcasts/Videos

```yaml
---
type: podcast | youtube | video-course
title: "Title"
creator: "Creator/Channel"
tags: [podcast, topic/productivity]
# Status
status: listened | watching | subscribed
date_consumed: YYYY-MM-DD
# Rating
rating: 1-10
# Metadata
duration:
episode:
series: "Series Name"
# Link
url:
---
```

---

## Note Templates

### Book Note Structure

```markdown
[[_books MOC]]

---

## Basic Info
- Author:
- Year:
- Pages:

## Why I Read This
-

## Core Ideas (3-5 bullet points)
1.
2.
3.

## My Notes
### Chapter X: Title
-

## Key Quotes
> "Quote" (p.XX)

## Action Items / Applications
- [ ]

## Related Reading
- [[Other Book]]
```

### Movie Note Structure

```markdown
[[_entertainment MOC]]

---

## Synopsis
Brief plot summary

## Why I Watched / Why Bookmark
-

## What I Liked
-

## What I Didn't Like
-

## Key Scenes / Quotes
-

## Connections
- Similar films:
- Related themes:
```

### Paper Note Structure

```markdown
[[_papers MOC]]

---

## Abstract
One-sentence summary

## Research Question
-

## Methodology
-

## Key Findings
1.
2.

## Value to Me
- Can apply to:
- Need to explore:

## Citation
Standard citation format
```

---

## Workflows

### Create New Media Note

**User says**: "记录一本书" / "Add a book" / "记录一部电影"

**Claude workflow**:
1. Ask for: Title, Author/Director, Status (reading/watched/etc.)
2. Generate appropriate filename
3. Create in correct folder
4. Fill frontmatter with provided info
5. Add template structure
6. Link back to MOC page

**Example**:
```
User: 记录一本书 - Atomic Habits

Claude: I'll create a book note for Atomic Habits.

Questions:
1. Author? (James Clear)
2. Status? (reading / completed / want-to-read)
3. Rating (if completed)? (1-10)

[Creates note with provided info]
```

### Update Status

**User says**: "我读完了 Atomic Habits" / "Finished reading X"

**Claude workflow**:
1. Find the book note
2. Update `status: completed`
3. Add `date_finished: [today]`
4. Ask for rating if not provided

### Find Media

**User says**: "有什么关于焦虑的书" / "Books about anxiety"

**Claude workflow**:
1. Search Books folder for keyword in tags, title, content
2. Also search Chinese equivalent (焦虑)
3. Return list sorted by rating

---

## Analysis Workflows

### 1. Annual Review / 年度统计

**User asks**: "我今年读了多少书？" / "How many books did I read this year?"

**Claude workflow**:
1. Scan all media notes for `date_finished` / `date_watched` in current year
2. Group by type (book, movie, music, etc.)
3. Generate report:

```markdown
## 2026 Media Consumption Report

### Books
- Total: 15 books
- Avg Rating: 7.2/10
- Top Rated: [[Book A]] (9/10), [[Book B]] (8/10)
- By Month: Jan(2), Feb(1), Mar(3)...

### Movies
- Total: 28 movies
- Avg Rating: 6.8/10
- Most Watched Genre: Drama (12), Sci-Fi (8)

### Papers
- Total: 8 papers read
- High Importance: 3
```

### 2. Genre Analysis / 类型分析

**User asks**: "我最常看什么类型的电影？"

**Claude workflow**:
1. Scan tags with `genre/*` pattern
2. Count frequency
3. Generate distribution:

```markdown
## Genre Distribution (Movies)

| Genre | Count | % |
|-------|-------|---|
| Drama | 12 | 43% |
| Sci-Fi | 8 | 29% |
| Comedy | 5 | 18% |
| Horror | 3 | 11% |
```

### 3. Consumption Trends / 消费趋势

**User asks**: "我的阅读习惯有什么变化？"

**Claude workflow**:
1. Analyze completion records over time
2. Identify patterns (seasonal? genre shifts?)
3. Compare with previous years

### 4. Topic Search / 主题搜索

**User asks**: "有什么关于焦虑的书？"

**Claude workflow**:
1. Search tags and content for keyword (焦虑, anxiety)
2. Return matching notes
3. Sort by rating/importance

### 5. Recommendation Tracking / 推荐追踪

**User asks**: "谁推荐的这本书？"

**Claude workflow**:
1. Check note's source or notes section
2. Cross-reference with People notes
3. Show recommendation chain

---

## Quick Actions Summary

| Command | Description |
|---------|-------------|
| "记录一本书" / "Add a book" | Create book note with guided prompts |
| "记录一部电影" / "Add a movie" | Create movie note |
| "我读完了 [书名]" | Update status=completed, add date_finished |
| "今年读了多少书" | Annual reading statistics |
| "推荐一本类似 [书名] 的书" | Find similar based on tags |
| "正在读什么" | List status=reading books |
| "想看清单" | List status=want-to-watch items |
| "评分最高的书" | Top rated books |
| "最近看的电影" | Recently watched movies |

---

## Analysis Questions Claude Can Answer

| Question | Data Source |
|----------|-------------|
| "今年读了几本书？" | date_finished in current year |
| "我最喜欢什么类型？" | tags with genre/* |
| "有什么高评分的电影推荐？" | rating >= 8 |
| "最近读完的书？" | date_finished, sorted DESC |
| "哪些书还没读完？" | status = reading |
| "关于 [主题] 的论文？" | tags and content search |
| "去年和今年的阅读量对比？" | Year-over-year analysis |

---

## Proactive Suggestions

| Trigger | Suggestion |
|---------|------------|
| Monthly review | "You haven't logged any books this month - anything you've read?" |
| Book finished | "Want to add a rating and key takeaways?" |
| Movie watched (via Quick Log) | "Want to create a full movie note for this?" |
| Year end | "Ready for your annual media consumption report?" |
| High-rated book | "This seems like a favorite - want to add it to a 'Best Of' list?" |

---

## Integration with Other Skills

- **moc-manager**: Use to create/update media MOCs
- **knowledge-synthesis**: Find insights across media notes
- **people-manager**: Track who recommended what
- **task-aggregator**: Find reading/watching tasks

---

## Status Values Reference

| Type | Status Options |
|------|----------------|
| Books | reading, completed, want-to-read, abandoned |
| Movies/TV | watched, watching, want-to-watch |
| Music | listening, favorite, archived |
| Papers | read, reading, to-read, reference-only |
| Podcasts | listened, watching, subscribed |


## Verify after writing

After adding or updating a media note:

1. Re-read it — frontmatter tags block-style, `status:` set to a valid value from the Status Values Reference above, and the type tag present so tag-queries find it.
2. Confirm it's filed in the folder its type implies (books / movies / music / papers / podcasts).
3. If you linked it to a MOC or another note, run `python "80_Code/scripts/generate-link-index.py" --broken` and fix any link you introduced.

Report the note path + its status. Don't report done on a note you haven't re-read.
