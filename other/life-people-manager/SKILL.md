---
name: life-people-manager
description: Manage relationships in the vault — track contacts, log interactions, analyze relationship health and staleness, personality profiling, network analysis. Use when the user says "add a person", "who haven't I talked to lately", "relationship check", "profile X", or after meeting someone new. NOT for drafting the actual outreach message (use life-communication-written — a user-global skill that lives in ~/.claude/skills, not in this repo).
---

# People Manager

Comprehensive relationship management skill - beyond contact notes to understanding and nurturing relationships.

## Bilingual Search

Notes and logs may be in Chinese or English. When searching:
- 朋友/friend, 友谊/friendship, 关系/relationship
- 疗愈日志/healing log, 会议/meeting, 冲突/conflict
- 信任/trust, 联系/contact, 网络/network

Always search both languages when looking for people-related content.

## Location & Conventions

- **Folder**: `30_Resources/People/`
- **Naming**: `@FirstName LastName.md` (e.g., `@Jun Ma.md`, `@田海亭.md`)
- **MOC**: `[[_300 people MOC]]`

---

## Reference files (read on demand)

`SKILL_DIR` = `{home}/.claude/skills/life-people-manager/`. The harness loads only this file; read a sibling with the Read tool when you reach the step that needs it.

| File | Priority | Read when |
|---|---|---|
| `<SKILL_DIR>/templates.md` | Required | Creating a person note — Extended Frontmatter yaml + Person Note Template live here |
| `<SKILL_DIR>/examples.md` | Reference | You want the expected shape of a workflow's output (create-contact dialogue, health report, network map/gaps, intro chains, networking strategy) |
| `<SKILL_DIR>/cli-reference.md` | Reference | You need the Obsidian CLI (`obs.sh`) lookup snippets + grep fallbacks, or the Analysis Questions lookup tables |

## Templates

Extended Frontmatter yaml + Person Note Template: `<SKILL_DIR>/templates.md`.

## Workflows

### Create New Contact

When user says "add contact" or "new person note":

1. Ask for: Name, Relationship type, Location (optional), Company (optional)
2. Generate filename: `@FirstName LastName.md`
3. Create in `30_Resources/People/`
4. Fill frontmatter with provided info
5. Add template structure
6. Link back to `[[_300 people MOC]]`
7. Offer to add to People MOC under appropriate group

Example dialogue: `<SKILL_DIR>/examples.md` §Create New Contact.

### Find Contacts

Search contacts by various criteria:

```bash
# By company
grep -r "company: Google" "30_Resources/People/" --include="*.md"

# By location
grep -r "location: Sydney" "30_Resources/People/" --include="*.md"

# By relationship
grep -r "people/professional" "30_Resources/People/" --include="*.md"

# By name (partial match)
ls "30_Resources/People/" | grep -i "smith"
```

### Find Stale Contacts

Contacts you haven't interacted with recently:

```bash
# Find all last_contact dates and check which are > 3 months old
grep -r "last_contact:" "30_Resources/People/" --include="*.md" -A0
```

**When user asks "who should I catch up with?":**
1. Scan all people notes for `last_contact` field
2. Identify contacts where last_contact > 3 months ago
3. Prioritize by relationship type (friends > professional > service)
4. Suggest 3-5 people to reach out to

### Log Interaction

**Quick interaction (chat, message, call):**
1. Open person's note
2. Add entry to `## Quick Log` section:
   ```
   - 2025-01-03: Had coffee, discussed job market
   ```
3. Update `last_contact` in frontmatter

**Significant meeting:**
1. Create meeting note in `Timestamps/Meetings/YYYY-MM-DD Meeting with @Person.md`
2. Link to person with `[[@FirstName LastName]]`
3. The Dataview query in person note will auto-show it
4. Update `last_contact` in frontmatter

**Daily journal mention:**
- Just use `[[@Person]]` in daily note
- Dataview will pick it up

### Update People MOC

The MOC should be organized by groups:

```markdown
# People

## Family
- [[@Mom]]
- [[@Dad]]

## Friends - Australia
- [[@Friend Name]]

## Friends - China
- [[@朋友名]]

## Professional Contacts
- [[@Colleague Name]] - Company, Role

## Service Providers
- [[@Doctor Name]] - Specialty
- [[@Accountant Name]]
```

**When adding new contact to MOC:**
1. Determine appropriate group from relationship/location
2. Add link in correct section
3. Optionally add brief description

## Contact Logging Decision Tree

```
New interaction with @Person?
    │
    ├── Quick (< 5 min, casual)
    │   └── Add to Quick Log section in @Person note
    │
    ├── Significant (meeting, important call, event)
    │   └── Create separate note in Timestamps/Meetings/
    │       └── Link to @Person in that note
    │
    └── Just mentioning in daily reflection
        └── Use [[@Person]] in daily journal
```

---

## Relationship Analysis Workflows

### 1. Relationship Health Check

**User asks**: "How are my relationships doing?" / "Relationship health report"

**Claude workflow**:
1. Scan all people notes for `last_contact`, `trust_level`, `energy`, `reciprocity`
2. Categorize relationships:
   - **Neglected gems**: High trust (7+) + last_contact > 3 months + positive energy
   - **Energy drains**: energy=drains + contact in last month
   - **One-sided**: reciprocity=low + you initiated last 3 contacts
   - **Thriving**: Regular contact + high trust + gives energy
3. Generate report with actionable suggestions

Example output: `<SKILL_DIR>/examples.md` §Relationship Health Check.

### 2. Person Deep Dive

**User asks**: "Tell me about @Jun Ma" / "Analyze my relationship with @Person"

**Claude workflow**:
1. Read person note thoroughly (frontmatter + all sections)
2. Search vault for all mentions:
   - Journal entries mentioning them
   - Meeting notes with their name
   - Tasks involving them
3. Synthesize:
   - **Relationship timeline**: How long, key milestones
   - **Interaction patterns**: Frequency, types of contact, who initiates
   - **Emotional patterns**: When do you feel good/drained after contact?
   - **What you've learned**: Personality insights, values, interests
4. Suggest next actions based on relationship_goal

### 3. Network Analysis

**User asks**: "Who can help me with X?" / "Who knows about Y?"

**Claude workflow**:
1. Parse query to identify need (skill, industry, location, etc.)
2. Scan people notes for:
   - `shared_interests` matching query
   - `company` or `title` relevant to query
   - Notes section mentioning relevant expertise
3. Filter by relationship quality:
   - Trust level 6+ (can ask for help)
   - Recent enough contact (or good reason to reconnect)
4. Suggest who to reach out to and how to frame the ask

Example: `<SKILL_DIR>/examples.md` §Network Analysis.

### 3b. Network Mapping

**User asks**: "Map my network" / "Show my network by industry" / "Network overview"

**Claude workflow**:
1. Scan all people notes
2. Group by:
   - **Industry/Sector**: company field, title field
   - **Location**: location field
   - **Relationship type**: tags (professional, friend, family)
   - **Strength**: trust_level + recency of contact
3. Generate visual map (text-based)

Example output: `<SKILL_DIR>/examples.md` §Network Mapping.

### 3c. Network Gaps Analysis

**User asks**: "Where are my network gaps?" / "What's missing in my network?"

**Claude workflow**:
1. Define target areas based on user's goals (career, industry, location)
2. Scan existing contacts by sector/purpose
3. Identify gaps:
   - Industries with 0-1 contacts
   - Missing "purpose" contacts (mentor, referral source, etc.)
   - Geographic gaps if relevant
4. Suggest how to fill gaps

Example output: `<SKILL_DIR>/examples.md` §Network Gaps Analysis.

### 3d. Introduction Chains

**User asks**: "How can I reach [person/company/role]?" / "Who can introduce me to X?"

**Claude workflow**:
1. Identify target (person, company, industry)
2. Search contacts for:
   - Direct connection to target
   - Works at target company
   - In same industry as target
3. Map introduction chain possibilities
4. Suggest approach and talking points

Example: `<SKILL_DIR>/examples.md` §Introduction Chains.

### 3e. Networking Strategy Advisor

**User asks**: "How should I approach networking for X goal?" / "Networking advice for [situation]"

**Claude workflow**:
1. Understand the goal (job search, industry switch, building presence)
2. Reference [[Networking]] note for strategies
3. Analyze current network against goal
4. Provide personalized advice

Example: `<SKILL_DIR>/examples.md` §Networking Strategy Advisor.

### 4. Relationship Retrospective

**User asks**: "How has my relationship with @Person evolved?" / "Retrospective on @Person"

**Claude workflow**:
1. Gather all data points:
   - Quick Log entries (chronological)
   - Meeting notes mentioning them
   - Journal entries
   - Relationship Health table scores
2. Analyze trends:
   - Contact frequency over time (increasing/decreasing?)
   - Trust level changes
   - Energy patterns
   - Key moments (positive and negative)
3. Present timeline and insights
4. Suggest: continue current pattern, invest more, or adjust expectations

### 5. Pre-Interaction Briefing

**User asks**: "I'm meeting @Person tomorrow" / "Prep me for seeing @Person"

**Claude workflow**:
1. Pull key info from person note:
   - Last interaction (what did you discuss?)
   - Things to remember (family names, sensitivities)
   - Current focus (what are they dealing with?)
   - Patterns (how do they prefer to communicate?)
2. Check for pending items:
   - Tasks related to them
   - Things you promised to do
   - `next_action` field
3. Generate briefing card

---

## Analysis Questions Claude Can Answer

Relationship Analysis + Network Analysis lookup tables: `<SKILL_DIR>/cli-reference.md` §Analysis Questions.

---

## Proactive Suggestions

Claude should proactively offer based on context:

| Trigger | Suggestion |
|---------|------------|
| Monthly review | "3 friends you haven't contacted in 3+ months" |
| After logging interaction | "Want to update their personality notes or trust level?" |
| Recurring patterns | "You've cancelled on @X twice recently - everything okay with that relationship?" |
| Before important dates | "@Jun's birthday is in 3 days" |
| After conflict logged | "Would a relationship retrospective help process this?" |
| Meeting scheduled | "Want a briefing card for your meeting with @Person?" |
| New person mentioned 3+ times | "You mention @NewPerson often - want to create a note for them?" |

---

## Obsidian CLI (Quick People Lookups) — with Fallbacks

Obsidian CLI (`obs.sh`) lookup snippets + grep fallbacks: `<SKILL_DIR>/cli-reference.md` §Obsidian CLI.

## Integration with Other Skills

- **knowledge-synthesis**: Find what you know about a person across all notes
- **task-aggregator**: Find tasks related to a person
- **cleanup-studio**: Identify stub person notes that need more info
- **obsidian-calendar-planner**: Birthday reminders, contact scheduling

---

## Verify after writing

After creating or updating a person note: re-read it to confirm frontmatter tags are block-style (`tags:` then `  - person`) and the expected sections exist. If you added `[[wikilinks]]`, run `python "80_Code/scripts/generate-link-index.py" --broken` and fix any broken link you introduced.
