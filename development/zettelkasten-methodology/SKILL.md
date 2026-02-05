---
name: zettelkasten-methodology
description: Complete guide to Zettelkasten note-taking methodology. Use when creating notes, establishing connections, or building knowledge management systems in Obsidian. Covers atomic notes, literature notes, MOCs, and linking strategies.
---

# Zettelkasten Methodology

The Zettelkasten (German for "slip box") is a personal knowledge management system developed by German sociologist Niklas Luhmann, who used it to produce over 70 books and 400 scholarly articles.

## Core Principles

### 1. Atomicity

Each note contains exactly **one idea**. This is the most important principle.

**Why atomicity matters**:
- Makes notes reusable in different contexts
- Enables precise linking
- Prevents notes from becoming outdated
- Allows ideas to be combined in new ways

**Test for atomicity**:
- Can this note be split without losing meaning?
- Does this note make one clear point?
- Would I link to this entire note or just part of it?

### 2. Autonomy

Notes must be **self-contained** and understandable without reading other notes.

**Requirements**:
- Complete sentences, not fragments
- Sufficient context included
- No pronouns referring to external content
- Could be understood in 5 years

### 3. Connectivity

Notes gain value through **connections** to other notes.

**Types of connections**:
- **Support**: This note strengthens another idea
- **Contrast**: This note contradicts or nuances another
- **Extension**: This note builds upon another
- **Application**: This note applies another concept
- **Association**: This note reminds me of another

### 4. Personal Expression

Always write in **your own words**.

**Never**:
- Copy-paste quotes as notes
- Paraphrase without understanding
- Import highlights without processing

**Always**:
- Transform ideas through your understanding
- Add your interpretation and context
- Connect to your existing knowledge

## Note Types

### Fleeting Notes

**Purpose**: Quick capture of ideas before they're lost

**Characteristics**:
- Temporary (24-48 hour lifespan)
- Minimal formatting
- Just enough context to remember
- Gateway to permanent notes

**Workflow**:
1. Capture immediately when idea strikes
2. Review daily
3. Either: Transform to permanent note OR discard
4. Never let them accumulate

### Literature Notes

**Purpose**: Process and capture ideas from sources

**Characteristics**:
- One note per source (book, article, video)
- Ideas in your own words
- Clear source attribution
- Bridges to permanent notes

**Workflow**:
1. Consume the source
2. Capture key ideas (in your words)
3. Note page/timestamp references
4. Identify potential permanent notes
5. Create permanent notes from best ideas

### Permanent Notes (Zettel)

**Purpose**: The core of your knowledge base

**Characteristics**:
- Atomic (one idea)
- Autonomous (self-contained)
- Connected (linked to others)
- Personal (your understanding)
- Evergreen (timeless value)

**Workflow**:
1. Write the idea clearly
2. Provide sufficient context
3. Create meaningful links
4. Add to relevant MOC
5. Tag appropriately

### Structure Notes / MOCs

**Purpose**: Navigation and organization

**Characteristics**:
- Overview of a topic cluster
- Entry points for exploration
- Contextual organization (not alphabetical)
- Links with brief descriptions

**Workflow**:
1. Identify theme/topic cluster
2. Gather related permanent notes
3. Organize by subtopic or progression
4. Add brief context for each link
5. Include entry points for newcomers

## Linking Strategy

### When to Link

Link when you can answer **why** the notes connect:
- "This supports X because..."
- "This contradicts Y in that..."
- "This extends Z by..."
- "This applies to W when..."

### How to Link

**Good link**: `See [[compound-effect]] for why small daily improvements matter`

**Bad link**: `Related: [[compound-effect]]` (no context)

### Link Discovery Questions

Ask yourself:
1. What does this remind me of?
2. What would this contradict?
3. Where might I use this?
4. What is this similar to?
5. What would this combine with?

## Note Lifecycle

```
Idea → Fleeting Note → Literature Note* → Permanent Note → MOC Integration
                           ↓
                    (*if from source)
```

### Seedling → Budding → Evergreen

**Seedling**: New note, rough, few connections
**Budding**: Refined, some connections, needs work
**Evergreen**: Polished, well-connected, complete

## Obsidian Implementation

### Folder Structure

```
vault/
├── 0-inbox/          # Fleeting notes land here
├── 1-literature/     # Literature notes
├── 2-permanent/      # Permanent notes (Zettel)
├── 3-moc/            # Maps of Content
├── templates/        # Note templates
└── attachments/      # Images, PDFs
```

### Naming Convention

**Timestamp + kebab-case**:
```
202312150930-compound-effect-habits.md
YYYYMMDDHHmm-descriptive-title.md
```

**Benefits**:
- Unique forever
- Sortable by creation
- Works as citation ID

### Tags vs Links

**Use tags for**:
- Status (#seedling, #evergreen)
- Type (#fleeting, #literature)
- Source type (#book, #article)
- Projects (#project/thesis)

**Use links for**:
- Conceptual connections
- Related ideas
- MOC inclusion
- Cross-references

### Essential Plugins

- **Dataview**: Query and display notes
- **Templater**: Dynamic templates
- **Graph Analysis**: Visualize connections
- **Backlinks**: See incoming links
- **Outgoing Links**: See outgoing links

## Common Mistakes

### 1. Collector's Fallacy
**Problem**: Saving without processing
**Solution**: Process or discard within 48h

### 2. Over-linking
**Problem**: Linking everything to everything
**Solution**: Only link with clear reason

### 3. Folder Obsession
**Problem**: Organizing by topic folders
**Solution**: Let links create structure

### 4. Quote Hoarding
**Problem**: Notes full of quotes
**Solution**: Transform to your words

### 5. Perfectionism
**Problem**: Waiting for "perfect" note
**Solution**: Start messy, refine over time

## Daily Practice

### Morning Review (5 min)
1. Review inbox/fleeting notes
2. Process or schedule for processing
3. Check for orphan notes

### During Work
1. Capture ideas immediately
2. Don't interrupt flow to process
3. Trust your future self

### Evening Processing (15-30 min)
1. Transform fleeting to permanent
2. Create links for new notes
3. Update relevant MOCs
4. Clean inbox

### Weekly Review (30 min)
1. Review orphan notes
2. Strengthen weak connections
3. Update growing MOCs
4. Archive stale fleeting notes

## Reference Files

- **Linking Strategies**: See [references/linking-strategies.md](references/linking-strategies.md)
- **Note Templates**: See [references/note-templates.md](references/note-templates.md)
- **Obsidian Setup**: See [references/obsidian-setup.md](references/obsidian-setup.md)
