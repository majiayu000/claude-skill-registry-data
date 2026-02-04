---
name: byterover-notion-sync
description: Advanced memory and knowledge management workflows for Byterover MCP Server. Use when creating implementation reports with timelines, documenting features as PRDs, or syncing project documentation folders with automatic conflict resolution. Extends basic retrieve/store operations with structured workflows for documentation, analysis, and knowledge synthesis.
---

# Byterover Notion Sync

Bidirectional knowledge synchronization between Byterover memories and Notion documentation. Converts agent-readable memories into team-digestible documentation (reports, PRDs, architecture docs) and imports structured Notion content back into searchable memories.

## Core Capabilities

This skill provides two primary directions for knowledge flow:

### 1. Memories → Notion Documentation
Transform Byterover memories into structured, human-readable documentation in Notion:
- Implementation reports with timelines
- Product Requirements Documents (PRDs)
- Feature documentation
- Technical architecture documentation

### 2. Notion → Byterover Memories
Convert Notion pages into searchable, agent-optimized memories:
- Break down documentation into logical chunks
- Preserve structure and context
- Handle nested pages recursively
- Maintain traceability to source

---

## Workflow Decision Tree

**When user requests documentation creation**, use this decision tree:

```
Is the user asking to:

1. Create/Generate documentation in Notion FROM memories?
   → Go to: Memories to Notion Workflow

2. Import/Convert Notion pages TO memories?
   → Go to: Notion to Memories Workflow

3. Unclear which direction?
   → Ask: "Would you like to:
      A) Create Notion documentation from your Byterover memories
      B) Import Notion content into Byterover memories"
```

---

## Memories to Notion Workflow

Convert Byterover memories into structured Notion documentation.

### Step 1: Understand Request

**Extract from user query**:
- Topic/task name for memory search
- Timeline (if provided): e.g., "July 10-15" or "last week"
- Desired format: implementation report, PRD, feature docs, architecture docs
- Notion destination (if specified): page URL, database, or workspace-level

**If format not specified**, use the [Format Selection Guide](references/format-selection-guide.md) to determine appropriate format based on content characteristics.

### Step 2: Retrieve Relevant Memories

Call `Byterover:byterover-retrieve-knowledge` **multiple times** (3-5 calls) with variations:

```
Example for "authentication implementation July 10-15":
- Query 1: "authentication implementation July 2025"
- Query 2: "JWT token user login July"
- Query 3: "authentication security decisions"
- Query 4: "user authentication challenges errors"
- Query 5: "auth deployment July 15"
```

**Important**: Aggregate results from multiple queries to get comprehensive context.

### Step 3: Select Documentation Format

Based on content analysis and user request, choose format:

**Implementation Report** → [references/implementation-report-format.md](references/implementation-report-format.md)
- Use when: Describing completed work with timeline
- Indicators: Past tense, temporal progression, challenges & solutions

**PRD** → [references/prd-format.md](references/prd-format.md)
- Use when: Planning features, defining requirements
- Indicators: Future tense, user stories, acceptance criteria

**Feature Documentation** → [references/feature-documentation-format.md](references/feature-documentation-format.md)
- Use when: Explaining how to use something
- Indicators: Usage instructions, code examples, troubleshooting

**Technical Architecture** → [references/technical-architecture-format.md](references/technical-architecture-format.md)
- Use when: System design, component interactions
- Indicators: Architecture diagrams, design decisions, infrastructure

See [references/format-selection-guide.md](references/format-selection-guide.md) for detailed selection criteria.

### Step 4: Structure Content

Follow the selected format template:

1. **Extract information** from aggregated memories
2. **Organize chronologically** (for reports) or logically (for other formats)
3. **Fill template sections** with relevant content from memories
4. **Add context** where memories are sparse
5. **Create timeline** by identifying temporal markers in memories
6. **Note gaps** as open questions or areas for clarification

### Step 5: Determine Notion Destination

**User specified destination**:
- Page URL → Use `Notion:notion-create-pages` with `page_id` parent
- Database URL → First use `Notion:notion-fetch` to get data source, then use `data_source_id` parent
- Teamspace → Use `Notion:notion-create-pages` with `teamspace_id`

**User did not specify**:
- Ask: "Where would you like to save this in Notion?" with options:
  - Create as standalone page (can be organized later)
  - Specify a parent page or database
  - Save to a specific teamspace

**Default**: Create as standalone workspace-level page if user prefers not to specify.

### Step 6: Create Notion Page

Use `Notion:notion-create-pages`:

```javascript
{
  "parent": {
    "page_id": "..." // or data_source_id or omit for workspace-level
  },
  "pages": [{
    "properties": {
      "title": "[Document Title]",
      // Add other properties if creating in database
    },
    "content": "[Structured markdown content from template]"
  }]
}
```

**For databases**, include appropriate properties based on format:
- Implementation Report: Type, Status, Start Date, End Date, Team, Tags
- PRD: Type, Status, Owner, Priority, Target Release, Tags
- Feature Documentation: Type, Status, Category, Tags, Last Updated
- Technical Architecture: Type, Status, System, Owner, Version

### Step 7: Confirm and Provide Link

Return to user:
- Link to created Notion page
- Summary of what was documented
- Note any gaps or areas that need manual review
- Suggest follow-up actions if relevant

**Example response**:
```
Created Implementation Report: "User Authentication Implementation"

📄 Notion page: https://notion.so/...

Summary:
- Documented 5-day implementation timeline (July 10-15)
- Captured 3 major technical decisions
- Included challenges and resolutions
- Added 8 code examples from memories

Note: Timeline dates were approximate based on memory context. You may want to verify exact dates.
```

---

## Notion to Memories Workflow

Convert Notion pages into Byterover memories while preserving structure.

### Step 1: Understand Request

**Extract from user query**:
- Notion page URL or search query
- Topic/area (if searching rather than direct URL)
- Scope: single page or include nested pages
- Any special focus areas

### Step 2: Locate Notion Content

**If user provided URL**:
- Use `Notion:notion-fetch` with the page URL/ID

**If user provided topic/search query**:
- Use `Notion:notion-search` to find relevant pages
- Present results to user for confirmation
- Fetch confirmed pages

### Step 3: Analyze Page Structure

Review fetched content for:
- Main sections (## headings)
- Nested/child pages (<page> tags)
- Content types: concepts, procedures, code, decisions, APIs
- Total length and complexity

### Step 4: Plan Memory Chunks

Follow [references/notion-to-memory-guide.md](references/notion-to-memory-guide.md) chunking strategy:

**Create separate memories for**:
- Each major section with substantial content (>100 words)
- Distinct concepts or topics
- Code examples with explanations
- Procedures or workflows
- Decision records
- API endpoints or methods

**Memory size guidelines**:
- Ideal: 200-800 words
- Minimum: 100 words (combine smaller sections)
- Maximum: 1500 words (split larger sections)

### Step 5: Extract and Format Memories

For each planned chunk:

1. **Extract content** with surrounding context
2. **Format based on content type**:
   - Concept/Definition
   - Procedure/How-To
   - Code Example
   - Decision/ADR
   - API/Reference
   - Architectural Component

   See [references/notion-to-memory-guide.md](references/notion-to-memory-guide.md) for templates.

3. **Add metadata**:
   ```markdown
   **Source**: [Page Title] - [Section Name]
   **Topic**: [Main topic]
   [Content formatted according to type]
   **Notion Source**: [Page URL]
   ```

4. **Store memory** using `Byterover:byterover-store-knowledge`

### Step 6: Handle Nested Pages

For each child page found in <page> tags:

1. **Fetch child page** using `Notion:notion-fetch`
2. **Add parent context** to memories from child page
3. **Repeat conversion process** (Steps 3-5)
4. **Create relationship memory** linking parent and child topics if needed

### Step 7: Verify and Summarize

**Quality checks** before finalizing:
- [ ] All major sections converted to memories
- [ ] Code examples are complete and formatted
- [ ] Source URLs are included
- [ ] Context is preserved
- [ ] Memory sizes are reasonable

**Return to user**:
- Count of memories created
- Summary of topics covered
- Any sections skipped or combined
- Confirmation of nested page processing

**Example response**:
```
Converted Notion page to memories: "API Authentication Guide"

✅ Created 8 memories:
   - 1 overview memory
   - 3 procedure memories (getting token, using token, refreshing)
   - 2 code example memories
   - 1 troubleshooting memory
   - 1 API reference memory

Processed 2 nested pages:
   - "JWT Token Implementation"
   - "OAuth2 Integration"

Total: 8 parent page memories + 12 nested page memories = 20 memories

All memories include source URLs for traceability.
```

---

## Best Practices

### For Memories → Notion

1. **Cast wide net**: Use multiple memory queries with variations
2. **Aggregate first**: Collect all relevant memories before structuring
3. **Choose format carefully**: Use format selection guide
4. **Preserve technical accuracy**: Don't paraphrase code or technical terms
5. **Note gaps**: Mark unclear areas as open questions
6. **Add timeline context**: Extract dates and temporal markers from memories
7. **Link related docs**: Cross-reference other relevant Notion pages

### For Notion → Memories

1. **Chunk logically**: Keep related information together
2. **Preserve structure**: Maintain headings, lists, code formatting
3. **Add context**: Include source page and section information
4. **Handle nesting**: Process child pages recursively
5. **Don't over-split**: Avoid creating too many tiny memories
6. **Test retrieval**: Consider what queries would find these memories
7. **Maintain traceability**: Always include source URLs

### General Guidelines

1. **Bidirectional traceability**: Always link between Notion and memories
2. **Preserve technical detail**: Don't lose code, configurations, or specifics
3. **Structure consistently**: Use templates for reproducibility
4. **Focus on reusability**: Format for future discovery and use
5. **Handle conflicts**: If memory conflicts detected, show resolution URL to user
6. **Iterate**: Ask for user feedback and refine as needed

---

## Common Patterns

### Pattern 1: Implementation Post-Mortem
```
User: "Document the auth implementation from last week"

Workflow:
1. Retrieve memories: "authentication", "auth implementation", "JWT", "user login"
2. Format: Implementation Report with Timeline
3. Structure: Timeline, challenges, solutions, outcomes
4. Create in Notion with properties: Type=Implementation Report, Status=Completed
```

### Pattern 2: Feature Planning
```
User: "Create PRD for notification system based on our discussions"

Workflow:
1. Retrieve memories: "notification system", "push notifications", "notification requirements"
2. Format: PRD
3. Structure: User stories, requirements, technical approach
4. Create in Notion with properties: Type=PRD, Status=Draft, Priority=P0
```

### Pattern 3: Documentation Import
```
User: "Import our API docs from Notion into memories"

Workflow:
1. Search Notion: "API documentation"
2. Fetch confirmed page
3. Chunk by endpoint/section
4. Format as API Reference memories
5. Store with source URL and context
```

### Pattern 4: Architecture Documentation
```
User: "Document our microservices architecture"

Workflow:
1. Retrieve memories: "microservices", "architecture", "service design", "infrastructure"
2. Format: Technical Architecture
3. Structure: Components, interactions, design decisions
4. Create in Notion with diagrams (using mermaid syntax)
```

---

## Troubleshooting

### Issue: Insufficient Memories Retrieved

**Solution**:
- Try broader query terms
- Use multiple variations of query
- Adjust time range if applicable
- Ask user to provide more specific topic details

### Issue: Can't Determine Format

**Solution**:
- Ask user directly: "Would you like this as an implementation report, PRD, feature documentation, or architecture document?"
- If still unclear, default to Implementation Report (most general)

### Issue: Timeline Information Missing

**Solution**:
- Note in document: "Timeline approximate based on memory context"
- Use relative markers: "early phase", "later", "final stages"
- Leave specific dates as [TBD] and note for user to fill in

### Issue: Memory Conflicts Detected

**Solution**:
- **CRITICAL**: Always display conflict resolution URL to user
- Explain conflict briefly
- Provide link for resolution
- Wait for user to resolve before continuing

### Issue: Large Notion Page (>5000 words)

**Solution**:
- Break into multiple memories strategically
- Use nested sections as natural boundaries
- Create index memory linking to sub-memories
- Process in batches if needed

---

## References

All reference materials are available in the `references/` directory:

- **[format-selection-guide.md](references/format-selection-guide.md)** - Determine which format to use for memory → Notion conversion
- **[implementation-report-format.md](references/implementation-report-format.md)** - Template for implementation reports with timelines
- **[prd-format.md](references/prd-format.md)** - Template for Product Requirements Documents
- **[feature-documentation-format.md](references/feature-documentation-format.md)** - Template for feature/API documentation
- **[technical-architecture-format.md](references/technical-architecture-format.md)** - Template for architecture documentation
- **[notion-to-memory-guide.md](references/notion-to-memory-guide.md)** - Comprehensive guide for Notion → Memory conversion

---

## Examples

### Example 1: Create Implementation Report

**User**: "Create a report on the payment system implementation we did from Oct 10-15"

**Process**:
1. Query memories: "payment system implementation October", "payment integration", "payment challenges October"
2. Select format: Implementation Report (completed work with timeline)
3. Structure content with timeline, decisions, challenges, outcomes
4. Create Notion page with properties
5. Return link and summary

### Example 2: Create PRD from Memories

**User**: "Turn our notification system discussions into a PRD"

**Process**:
1. Query memories: "notification system", "push notifications", "notification requirements", "notification design"
2. Select format: PRD (feature planning)
3. Structure: User stories, requirements, technical approach, success metrics
4. Create in product database with proper properties
5. Return link and note any missing requirement details

### Example 3: Import Documentation

**User**: "Import the authentication guide from Notion into memories"

**Process**:
1. Search Notion: "authentication guide"
2. Fetch page and analyze structure
3. Plan chunks: overview, procedures (3), code examples (2), troubleshooting
4. Extract and format each chunk with proper memory template
5. Store all memories with source URLs
6. Return summary of memories created

### Example 4: Document Architecture

**User**: "Create architecture doc for our microservices setup"

**Process**:
1. Query memories: "microservices architecture", "service design", "API gateway", "service communication"
2. Select format: Technical Architecture
3. Structure: Components, interactions, design decisions, infrastructure
4. Add mermaid diagrams for visual representation
5. Create in architecture database
6. Return link with component summary
