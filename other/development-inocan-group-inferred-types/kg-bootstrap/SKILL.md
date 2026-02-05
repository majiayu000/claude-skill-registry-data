---
name: kg-bootstrap
description: Creates and bootstraps Knowledge Graph projects from video transcripts. Extracts entities (people, organizations, concepts) and relationships into searchable graphs. Use when users want to build a knowledge graph, extract entities, analyze connections between people/organizations, or select Option 5 after transcription.
---

# Knowledge Graph Bootstrap

## Step-by-Step Workflow

### Step 1: Check Existing Projects
Use `list_kg_projects` first:
- If projects exist → Ask: "Would you like to add to an existing project or create a new one?"
- If no projects → Proceed to Step 2

### Step 2: Create New Project (if needed)
Ask for a project name describing the research domain:
> "What would you like to call this Knowledge Graph project?"
> Examples: 'Tech Industry Interviews', 'Climate Research', 'Company History'

Use `create_kg_project` and report the project ID.

### Step 3: Bootstrap Domain Profile
**This is where the magic happens:**

Explain: "I'll analyze your transcript to discover entity types (people, organizations, concepts) and relationships."

Use `bootstrap_kg_project` with:
- `project_id`: The newly created ID
- `transcript`: Full transcript text (use `get_transcript` if needed)
- `title`: Video/source title

### Step 4: Present Bootstrap Results
Format results conversationally:

```
## Knowledge Graph Schema Discovered!

**Project:** [Name]
**Confidence:** [X]%

### Entity Types Discovered ([N])
- **Person**: Individuals mentioned
- **Company**: Organizations, startups
- [etc.]

### Relationship Types ([N])
- **works_at**: Employment relationships
- **founded**: Company founding
- [etc.]

### Example Entities Identified ([N])
- [Entity Name] ([Type])
- [etc.]

Now extracting entities into the graph...
```

### Step 4.5: CRITICAL — Extract from Bootstrap Transcript

**IMMEDIATELY after bootstrap**, call `extract_to_kg` with the SAME transcript:

```
extract_to_kg(
    project_id="...",
    transcript="...",        ← Same transcript used for bootstrap
    title="...",             ← Same title
    transcript_id="..."      ← REQUIRED for evidence linking
)
```

This populates the actual graph with entities. Bootstrap only creates the schema (types and patterns); extraction adds the nodes and edges.

After extraction completes, present:
```
## Knowledge Graph Complete!

**Entities Added:** [N]
**Relationships Found:** [N]

Would you like me to:
1. Extract entities from another transcript
2. View current graph statistics
3. Explore key players and connections
```

### Step 5: Continue Building
For subsequent transcripts on a bootstrapped project:
- Use `extract_to_kg` directly (no re-bootstrap needed)
- **IMPORTANT**: Always pass `transcript_id` to enable evidence linking
- Show what was added vs. what already existed
- Offer to continue with more transcripts

## Tool Parameters

### `extract_to_kg` (CRITICAL)
When calling `extract_to_kg`, always include:
- `project_id`: Target KG project ID
- `transcript`: Full transcript text
- `title`: Video/source title
- `transcript_id`: **Required for evidence** — Use the ID returned by `save_transcript`

```
extract_to_kg(
    project_id="abc123",
    transcript="...",
    title="Interview with CEO",
    transcript_id="5da6b612"  ← from save_transcript result
)
```

Without `transcript_id`, the graph inspector won't be able to show supporting evidence for entities.

## Critical Rules

- A project MUST be bootstrapped before extraction
- Bootstrap happens ONCE per project (first transcript only)
- **Bootstrap creates schema ONLY** — you MUST call `extract_to_kg` afterward to populate the graph
- **ALWAYS extract from the bootstrap transcript** — don't skip to "another transcript"
- **Always pass `transcript_id`** when using `extract_to_kg`
- Always show progress in chat — user shouldn't need to check sidebar
- The sidebar syncs automatically, but chat is the primary interface

## Common Mistake to Avoid

❌ WRONG:
```
bootstrap_kg_project(transcript)
→ "Your KG is ready! Extract from ANOTHER transcript?"
```

✅ CORRECT:
```
bootstrap_kg_project(transcript)
→ "Schema discovered! Now extracting entities..."
extract_to_kg(same_transcript)
→ "X entities and Y relationships added!"
```
