---
name: memory-management
label: 记忆管理
description: 两级记忆系统，让 aily 成为真正的工作协作者。解码速记、缩写、昵称和内部用语，让 aily 像同事一样理解请求。aily.md 用于工作记忆，memory/ 目录用于完整知识库。
---

# Memory Management

Memory makes aily your workplace collaborator - someone who speaks your internal language.

## The Goal

Transform shorthand into understanding:

```
User: "ask todd to do the PSR for oracle"
              ↓ aily decodes
"Ask Todd Martinez (Finance lead) to prepare the Pipeline Status Report
 for the Oracle Systems deal ($2.3M, closing Q2)"
```

Without memory, that request is meaningless. With memory, aily knows:
- **todd** → Todd Martinez, Finance lead, prefers 飞书 IM
- **PSR** → Pipeline Status Report (weekly sales doc)
- **oracle** → Oracle Systems deal, not the company

## Architecture

```
aily.md            ← Hot cache (~30 people, common terms)
memory/
  glossary.md      ← Full decoder ring (everything)
  people/          ← Complete profiles
  projects/        ← Project details
  context/         ← Company, teams, tools
```

**aily.md (Hot Cache):**
- Top ~30 people you interact with most
- ~30 most common acronyms/terms
- Active projects (5-15)
- Your preferences
- **Goal: Cover 90% of daily decoding needs**

**memory/glossary.md (Full Glossary):**
- Complete decoder ring - everyone, every term
- Searched when something isn't in aily.md
- Can grow indefinitely

**memory/people/, projects/, context/:**
- Rich detail when needed for execution
- Full profiles, history, context

## Lookup Flow

```
User: "ask todd about the PSR for phoenix"

1. Check aily.md (hot cache)
   → Todd? ✓ Todd Martinez, Finance
   → PSR? ✓ Pipeline Status Report
   → Phoenix? ✓ DB migration project

2. If not found → search memory/glossary.md
   → Full glossary has everyone/everything

3. If still not found → ask user
   → "What does X mean? I'll remember it."
```

This tiered approach keeps aily.md lean (~100 lines) while supporting unlimited scale in memory/.

## File Locations

- **Working memory:** `aily.md` in current working directory
- **Deep memory:** `memory/` subdirectory

## Working Memory Format (aily.md)

Use tables for compactness. Target ~50-80 lines total.

```markdown
# Memory

## Me
[Name], [Role] on [Team]. [One sentence about what I do.]

## People
| Who | Role |
|-----|------|
| **Todd** | Todd Martinez, Finance lead |
| **Sarah** | Sarah Chen, Engineering (Platform) |
| **Greg** | Greg Wilson, Sales |
→ Full list: memory/glossary.md, profiles: memory/people/

## Terms
| Term | Meaning |
|------|---------|
| PSR | Pipeline Status Report |
| P0 | Drop everything priority |
| standup | Daily 9am sync |
→ Full glossary: memory/glossary.md

## Projects
| Name | What |
|------|------|
| **Phoenix** | DB migration, Q2 launch |
| **Horizon** | Mobile app redesign |
→ Details: memory/projects/

## Preferences
- 25-min meetings with buffers
- Async-first, 飞书 IM over email
- No meetings Friday afternoons
```

## Deep Memory Format (memory/)

**memory/glossary.md** - The decoder ring:
```markdown
# Glossary

Workplace shorthand, acronyms, and internal language.

## Acronyms
| Term | Meaning | Context |
|------|---------|---------|
| PSR | Pipeline Status Report | Weekly sales doc |
| OKR | Objectives & Key Results | Quarterly planning |
| P0/P1/P2 | Priority levels | P0 = drop everything |

## Internal Terms
| Term | Meaning |
|------|---------|
| standup | Daily 9am sync in #engineering |
| the migration | Project Phoenix database work |
| ship it | Deploy to production |
| escalate | Loop in leadership |

## Nicknames → Full Names
| Nickname | Person |
|----------|--------|
| Todd | Todd Martinez (Finance) |
| T | Also Todd Martinez |

## Project Codenames
| Codename | Project |
|----------|---------|
| Phoenix | Database migration |
| Horizon | New mobile app |
```

**memory/people/{name}.md:**
```markdown
# Todd Martinez

**Also known as:** Todd, T
**Role:** Finance Lead
**Team:** Finance
**Reports to:** CFO (Michael Chen)

## Communication
- Prefers 飞书 IM DM
- Quick responses, very direct
- Best time: mornings

## Context
- Handles all PSRs and financial reporting
- Key contact for deal approvals over $500k
- Works closely with Sales on forecasting

## Notes
- Cubs fan, likes talking baseball
```

**memory/projects/{name}.md:**
```markdown
# Project Phoenix

**Codename:** Phoenix
**Also called:** "the migration"
**Status:** Active, launching Q2

## What It Is
Database migration from legacy Oracle to PostgreSQL.

## Key People
- Sarah - tech lead
- Todd - budget owner
- Greg - stakeholder (sales impact)

## Context
$1.2M budget, 6-month timeline. Critical path for Horizon project.
```

**memory/context/company.md:**
```markdown
# Company Context

## Tools & Systems
| Tool | Used for | Internal name |
|------|----------|---------------|
| 飞书 IM | Communication | - |
| 飞书项目 | Engineering tasks | - |
| 飞书 CRM | CRM | "the CRM" |
| 飞书文档 | Docs/wiki | - |

## Teams
| Team | What they do | Key people |
|------|--------------|------------|
| Platform | Infrastructure | Sarah (lead) |
| Finance | Money stuff | Todd (lead) |
| Sales | Revenue | Greg |

## Processes
| Process | What it means |
|---------|---------------|
| Weekly sync | Monday 10am all-hands |
| Ship review | Thursday deploy approval |
```

## How to Interact

### Decoding User Input (Tiered Lookup)

**Always** decode shorthand before acting on requests:

```
1. aily.md (hot cache)        → Check first, covers 90% of cases
2. memory/glossary.md         → Full glossary if not in hot cache
3. memory/people/, projects/  → Rich detail when needed
4. Ask user                   → Unknown term? Learn it.
```

Example:
```
User: "ask todd to do the PSR for oracle"

aily.md lookup:
  "todd" → Todd Martinez, Finance ✓
  "PSR" → Pipeline Status Report ✓
  "oracle" → (not in hot cache)

memory/glossary.md lookup:
  "oracle" → Oracle Systems deal ($2.3M) ✓

Now aily can act with full context.
```

### Adding Memory

When user says "remember this" or "X means Y":

1. **Glossary items** (acronyms, terms, shorthand):
   - Add to memory/glossary.md
   - If frequently used, add to aily.md Quick Glossary

2. **People:**
   - Create/update memory/people/{name}.md
   - Add to aily.md Key People if important
   - **Capture nicknames** - critical for decoding

3. **Projects:**
   - Create/update memory/projects/{name}.md
   - Add to aily.md Active Projects if current
   - **Capture codenames** - "Phoenix", "the migration", etc.

4. **Preferences:** Add to aily.md Preferences section

### Recalling Memory

When user asks "who is X" or "what does X mean":

1. Check aily.md first
2. Check memory/ for full detail
3. If not found: "I don't know what X means yet. Can you tell me?"

### Progressive Disclosure

1. Load aily.md for quick parsing of any request
2. Dive into memory/ when you need full context for execution
3. Example: drafting an email to todd about the PSR
   - aily.md tells you Todd = Todd Martinez, PSR = Pipeline Status Report
   - memory/people/todd-martinez.md tells you he prefers 飞书 IM, is direct

## Bootstrapping

Use `/productivity:start` to initialize by scanning your chat, calendar, email, and documents. Extracts people, projects, and starts building the glossary.

## Conventions

- **Bold** terms in aily.md for scannability
- Keep aily.md under ~100 lines (the "hot 30" rule)
- Filenames: lowercase, hyphens (`todd-martinez.md`, `project-phoenix.md`)
- Always capture nicknames and alternate names
- Glossary tables for easy lookup
- When something's used frequently, promote it to aily.md
- When something goes stale, demote it to memory/ only

## What Goes Where

| Type | aily.md (Hot Cache) | memory/ (Full Storage) |
|------|----------------------|------------------------|
| Person | Top ~30 frequent contacts | glossary.md + people/{name}.md |
| Acronym/term | ~30 most common | glossary.md (complete list) |
| Project | Active projects only | glossary.md + projects/{name}.md |
| Nickname | In Key People if top 30 | glossary.md (all nicknames) |
| Company context | Quick reference only | context/company.md |
| Preferences | All preferences | - |
| Historical/stale | Remove | Keep in memory/ |

## Promotion / Demotion

**Promote to aily.md when:**
- You use a term/person frequently
- It's part of active work

**Demote to memory/ only when:**
- Project completed
- Person no longer frequent contact
- Term rarely used

This keeps aily.md fresh and relevant.
