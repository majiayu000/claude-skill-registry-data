---
name: project-search
description: Search across all project artifacts including meetings, sprints, milestones, documentation, and decisions. Use when user mentions "find", "search", "where is", "locate", "show me", or asks questions about project content. Multi-strategy search using README indexes, pattern matching, and full-text search.
---

# Project Search Skill

## When to use this Skill

Activate when the user:
- Asks to find or locate project content
- Uses keywords: "find", "search", "where is", "locate", "show me"
- Asks questions about project history or decisions
- Needs to find meetings, sprints, or documentation
- Wants to search by person, date, topic, or milestone
- References specific content they can't locate

## Workflow

### Phase 1: Query Analysis

**Objective**: Understand what the user is searching for and determine search strategy.

**Steps**:

1. **Parse search query** from user message:
   - Extract search terms
   - Identify search type (content, person, date, milestone, etc.)
   - Detect filters (date range, file type, status)

2. **Categorize search intent**:
   - **Content search**: "Find decisions about database"
   - **Person search**: "What has @alice worked on"
   - **Date search**: "Meetings from last week"
   - **Milestone search**: "What's in beta release milestone"
   - **Sprint search**: "Show sprint 5 stories"
   - **Topic search**: "Anything about authentication"
   - **Status search**: "Show blocked items"

3. **Extract search parameters**:
   - **Keywords**: Main search terms
   - **Person**: @mentions or names
   - **Date range**: "last week", "Q1", "after Jan 1", specific dates
   - **Content type**: meetings, sprints, docs, decisions, all
   - **Status**: completed, in-progress, blocked, planned
   - **Milestone/Sprint**: Specific milestone or sprint number

4. **Determine search scope**:
   - Project root only
   - Specific subdirectory (meetings/, sprints/, etc.)
   - Across entire workspace

**Example Analysis**:
```
User: "Find all meetings where we discussed the API design"

Parsed:
- Intent: Content search
- Keywords: ["API design"]
- Content type: meetings
- Date range: all time
- Search scope: meetings/

Strategy: README index → Content search in meetings/
```

### Phase 2: Strategy Selection

**Objective**: Choose optimal search strategy based on query type.

**Search strategies (in order of preference)**:

#### Strategy 1: README.md Index Search (Fastest)

**Use when**:
- Searching by file name, title, or general topic
- Need list of files in category
- Recent content (README indexes are up-to-date)

**Process**:
1. Read appropriate README.md file:
   - `meetings/README.md` for meeting search
   - `sprints/README.md` for sprint search
   - Project `README.md` for overview
2. Parse index entries
3. Filter by search criteria
4. Return matching entries with descriptions

**Example**:
```
Search: "Find sprint 5"
→ Read sprints/README.md
→ Find entry: "Sprint 5: Authentication Features"
→ Return: sprints/sprint-05/sprint-plan.md
```

#### Strategy 2: YAML/Structured Data Search (Fast)

**Use when**:
- Searching milestones (milestones.yaml)
- Searching by metadata (dates, owners, status)
- Need exact matches on structured fields

**Process**:
1. Read relevant YAML file (milestones.yaml)
2. Parse structure
3. Filter by criteria
4. Return matching entries

**Example**:
```
Search: "Show milestones owned by @alice"
→ Read milestones.yaml
→ Filter: owner == "@alice"
→ Return: List of alice's milestones
```

#### Strategy 3: Pattern Matching (Fast)

**Use when**:
- Searching by filename patterns
- Date-based filename search
- Type-based search (all *.md in sprints/)

**Process**:
1. Use `Glob` tool with pattern:
   - `meetings/**/*2025-11*.md` for November meetings
   - `sprints/*/sprint-plan.md` for all sprint plans
   - `docs/**/*.md` for all documentation
2. Filter results by additional criteria
3. Return matching files

**Example**:
```
Search: "Meetings from November"
→ Glob: meetings/**/*2025-11*.md
→ Return: List of November meeting files
```

#### Strategy 4: Full-Text Content Search (Slower)

**Use when**:
- Searching for specific terms in content
- Need to find mentions of topics, names, or concepts
- Other strategies insufficient

**Process**:
1. Use `Grep` tool with search terms
2. Specify scope (meetings/, sprints/, all project)
3. Extract context around matches
4. Rank results by relevance
5. Return matches with snippets

**Example**:
```
Search: "Find discussions about OAuth implementation"
→ Grep: pattern="OAuth" path=meetings/
→ Find matches in 3 meeting files
→ Return: Files with context snippets
```

#### Strategy 5: Cross-Reference Search (Comprehensive)

**Use when**:
- Need to find all related content
- Following links and references
- Building complete picture

**Process**:
1. Start with initial search (using above strategies)
2. Read found documents
3. Extract cross-references (links, mentions, related items)
4. Follow links recursively (limited depth)
5. Build relationship map
6. Return full result set with connections

**Example**:
```
Search: "Everything about beta release milestone"
→ Find milestone in milestones.yaml
→ Follow related_sprints links
→ Find meetings mentioning beta release
→ Find docs created for beta
→ Return: Complete set with relationships
```

### Phase 3: Execute Search

**Objective**: Run selected search strategy and gather results.

**Steps**:

1. **Execute primary search strategy**

2. **Collect results**:
   - File paths
   - Titles/descriptions
   - Relevant metadata (dates, owners, status)
   - Content snippets (for full-text search)

3. **Apply filters**:
   - Date range filter
   - Person filter (@mentions)
   - Status filter
   - Content type filter

4. **Check governance** (if applicable):
   - Read RULE.md for access restrictions
   - Filter out restricted content

5. **Rank results** by:
   - **Relevance**: Match quality to query
   - **Recency**: Newer content ranked higher
   - **Location**: Closer to project root ranked higher
   - **Completeness**: Fully completed items vs drafts

6. **If no results from primary strategy**:
   - Fall back to next strategy
   - Broaden search criteria
   - Suggest related searches

### Phase 4: Format and Present Results

**Objective**: Present search results in clear, actionable format.

**Steps**:

1. **Group results** by category:
   - Meetings
   - Sprints/Iterations
   - Milestones
   - Documentation
   - Decisions

2. **Format result entries**:
   ```
   📄 [Category] Title
      Path: path/to/file.md
      Date: YYYY-MM-DD
      [Relevant metadata: Owner, Status, etc.]
      [If content search: Context snippet with highlights]
   ```

3. **Include result count and search details**:
   ```
   🔍 Search Results for "{query}"

   Found {count} results in {categories}
   Search scope: {scope}
   Filters applied: {filters if any}
   ```

4. **Present results**:

   **Format**:
   ```
   🔍 Search Results: "{query}"

   Found {total} results across {categories}

   📋 Meetings ({count})
   - [2025-11-13: Sprint 5 Planning](meetings/sprint-planning/2025-11-13_sprint-5-planning.md)
     "Discussed API design for authentication endpoints..."

   - [2025-11-06: Architecture Review](meetings/general/2025-11-06_api-architecture.md)
     "@alice presented OAuth 2.0 implementation options..."

   🏃 Sprints ({count})
   - [Sprint 5: Authentication Features](sprints/sprint-05/sprint-plan.md)
     Status: Active | Stories: 8 | Owner: @bob

   🎯 Milestones ({count})
   - [Beta Release](milestones.yaml#beta-release)
     Target: 2025-03-31 | Status: In Progress | Progress: 75%

   📚 Documentation ({count})
   - [API Design Document](docs/api-design.md)
     Owner: @alice | Updated: 2025-11-10

   🔗 Cross-References ({count})
   [If cross-reference search performed]
   - Sprint 5 → Beta Release Milestone
   - API Design Doc → Sprint 5 Stories
   - Sprint Planning → Architecture Review Meeting
   ```

5. **Offer refinement options**:
   ```
   💡 Refine your search:
   - "Show only completed"
   - "Find from last month"
   - "Search only in sprints"
   - "Show details for [specific result]"
   ```

6. **If too many results**:
   ```
   ℹ️ Showing top {limit} results. {remaining} more found.

   Narrow your search:
   - Add date range: "from last week"
   - Specify type: "only meetings"
   - Add filters: "owned by @name"
   ```

7. **If no results**:
   ```
   🔍 No results found for "{query}"

   Suggestions:
   - Check spelling
   - Try broader terms
   - Search related terms: "{suggestions}"
   - Search in different location

   Recent content:
   [Show recently added/updated files as alternatives]
   ```

### Phase 5: Detailed View (Optional)

**Objective**: If user wants details on specific result, provide full context.

**Steps**:

1. **If user selects specific result**:
   ```
   User: "Show me the sprint 5 details"
   ```

2. **Read full document**:
   ```
   Read sprints/sprint-05/sprint-plan.md
   ```

3. **Present complete information**:
   ```
   📄 Sprint 5: Authentication Features

   **Status**: Active (Day 8 of 14)
   **Goal**: Complete user authentication and profile management
   **Dates**: 2025-11-01 to 2025-11-14

   **Progress**:
   - Completed: 3/8 stories (18/45 points) - 40%
   - In Progress: 2 stories
   - Blocked: 1 story (OAuth config)

   **Team**:
   - @alice: 2 stories
   - @bob: 3 stories
   - @carol: 2 stories
   - @david: 1 story

   **Related**:
   - Milestone: Beta Release (contributes to)
   - Meetings: [Sprint 5 Planning](link), [Daily Standups](link)
   - Docs: [Auth Design](link)

   📄 Full document: sprints/sprint-05/sprint-plan.md

   💡 Actions:
   - "Update sprint 5 progress"
   - "Show sprint 5 meetings"
   - "Mark story complete in sprint 5"
   ```

## Special Cases

### Case 1: Person-specific search

```
User: "What has @alice been working on?"

Process:
1. Search all content for @alice mentions
2. Filter by recency (last sprint/month)
3. Categorize:
   - Assigned stories/tasks
   - Meeting attendances
   - Owned milestones
   - Created documents

Result:
📊 @alice's Recent Activity

**Current Work** (Sprint 5):
- Story: OAuth Integration (8sp) - In Progress
- Story: Profile Edit Page (3sp) - Completed ✅

**Meetings** (Last 2 weeks):
- Sprint 5 Planning (2025-11-01)
- Architecture Review (2025-11-06)
- Daily Standups (10 attendances)

**Milestones**:
- Owner: Security Audit (Target: 2025-03-20)

**Documents**:
- Created: API Design Doc (2025-11-10)
- Updated: Auth Spec (2025-11-08)
```

### Case 2: Timeline/Date-based search

```
User: "What happened in the project last week?"

Process:
1. Calculate date range (last week)
2. Search all content within range
3. Sort chronologically
4. Group by day

Result:
📅 Project Activity: Nov 6 - Nov 13, 2025

**Monday, Nov 6**
- Meeting: Sprint 4 Retrospective
- Sprint 4 completed (38/40 points)
- Milestone updated: Beta Release (60% → 75%)

**Tuesday, Nov 7**
- Sprint 5 started
- Stories assigned to team

**Wednesday, Nov 8**
- Daily standup recorded
- Decision: Use PostgreSQL for auth

**[Continue for each day]**

📊 Week Summary:
- Meetings: 8
- Stories completed: 5
- Documents updated: 3
- Milestones progressed: 1
```

### Case 3: Topic/Theme search

```
User: "Find everything about database decisions"

Process:
1. Full-text search for "database"
2. Focus on decisions/ directory
3. Also search meetings and docs
4. Cross-reference related content

Result:
🔍 Search: "database"

📋 Decisions (3):
- [001: Database Selection](decisions/001-database-choice.md)
  PostgreSQL chosen for auth system (2025-10-15)

- [005: Caching Strategy](decisions/005-caching.md)
  Redis for session caching (2025-10-20)

- [012: Migration Approach](decisions/012-database-migration.md)
  Flyway for schema versioning (2025-11-01)

📋 Meetings discussing database (4):
- Architecture Review (2025-10-15)
- Sprint 3 Planning (2025-10-16)
- Tech Spike Results (2025-10-19)
- Database Design Session (2025-10-22)

📚 Related Documentation (2):
- Database Schema (docs/database-schema.md)
- Migration Guide (docs/migration-guide.md)

🏃 Related Sprints:
- Sprint 3: Database setup and migration

🔗 Cross-references:
All database decisions link to Sprint 3 and Beta Release milestone
```

### Case 4: Status-based search

```
User: "Show me all blocked items"

Process:
1. Search sprints for status: blocked
2. Search milestones for status: delayed
3. Search meetings for blocker discussions

Result:
⚠️ Blocked Items

🏃 Sprints:
- Sprint 5, Story: OAuth Integration
  Blocked: Waiting for third-party API credentials
  Owner: @alice
  Blocked since: 2025-11-10

📋 Meetings mentioning blockers:
- Daily Standup (2025-11-10)
- Daily Standup (2025-11-11)
- Daily Standup (2025-11-13)

💡 Action needed:
- @alice: Follow up on API credentials
- Consider workaround or mock implementation
```

## Error Handling

### Error: No RULE.md found

```
⚠️ No RULE.md found.

Search will proceed with default project structure.

Note: For best results, initialize project governance:
"Initialize project"
```

Proceed with search using standard directories.

### Error: No results found

```
🔍 No results found for "{query}"

Checked:
- ✓ Meetings
- ✓ Sprints
- ✓ Milestones
- ✓ Documentation
- ✓ Decisions

Suggestions:
- Check spelling: "{query}"
- Try broader terms
- Try related searches:
  * "{suggestion 1}"
  * "{suggestion 2}"

📋 Recent project activity:
[Show last 5 updates as alternatives]
```

### Error: Search too broad

```
ℹ️ Your search "{query}" returned {count} results.

This may be too many to review effectively.

Suggestions to narrow:
1. Add date range: "from last month"
2. Specify type: "only in meetings"
3. Add person filter: "by @name"
4. Add status: "completed only"

Or continue with:
"Show top 10 results"
```

### Error: Invalid date range

```
⚠️ Could not parse date: "{date_input}"

Supported formats:
- Specific: "2025-11-13" or "November 13, 2025"
- Relative: "last week", "last month", "yesterday"
- Range: "from Nov 1 to Nov 15"
- Quarter: "Q1", "Q2 2025"

Please rephrase your date filter.
```

## Integration with Other Skills

### With AkashicRecords search-content

Both Skills can search same project:
- AkashicRecords: Knowledge base, articles, general content
- ProjectMaster: Project-specific content (meetings, sprints, milestones)

If both exist, search both and merge results.

### With track-meeting Skill

Found meetings can be:
- Viewed in detail
- Updated
- Linked to other content

### With manage-sprint Skill

Found sprints can be:
- Updated with progress
- Viewed in detail
- Cross-referenced with milestones

### With track-milestone Skill

Found milestones can be:
- Updated with status
- Viewed with full dependencies
- Linked to contributing sprints

## Best Practices

### 1. Start with README indexes

Fastest search method. Always try first.

### 2. Use specific search terms

Specific terms yield better results than generic ones.

### 3. Add filters to narrow results

Date ranges, content types, and person filters improve relevance.

### 4. Follow cross-references

Related content often provides fuller picture.

### 5. Search by person for team insights

Find what specific team members are working on or have created.

### 6. Use date-based search for retrospectives

"What did we do last sprint?" captures recent history.

### 7. Search by milestone for big picture

See all content contributing to major goals.

### 8. Combine search strategies

If one strategy fails, automatically try next.

## Notes

- Multi-strategy search ensures comprehensive results.
- README index search is fast and accurate for well-maintained projects.
- Full-text search is powerful but slower - use as fallback.
- Cross-reference search builds complete context around topics.
- Search results link to Skills that can act on found content.
- Person-based and date-based searches provide valuable team insights.

---

Effective search transforms project content into accessible knowledge. This Skill makes finding information fast and intuitive.
