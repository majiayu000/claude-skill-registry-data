---
name: neurosurgical-book-parser
description: Extract structured knowledge from neurosurgical and spine surgery textbooks. Identifies anatomical structures, surgical procedures, complications, and clinical relationships. Use when processing medical PDFs, building surgical knowledge graphs, or creating clinical decision support content. Applies kaizen continuous improvement from prior extractions.
allowed-tools: Read, Glob, Grep, Bash
---

# Neurosurgical Book Parser Skill

## What This Skill Does

Extracts structured medical knowledge from neurosurgical and spine surgery textbooks:
- Anatomical structures and their spatial relationships
- Surgical procedures with step-by-step sequences
- Clipping/fixation techniques and their applications
- Complications and contraindications
- Clinical outcomes and evidence

## When to Use This Skill

Activate when the user:
- Wants to process a neurosurgical or spine surgery textbook
- Asks to build a medical knowledge graph
- Needs to extract surgical procedures from PDFs
- Wants to create clinical decision support content
- Mentions "Seven Aneurysms", "spine surgery", "aneurysm clipping", or similar

## Critical Workflow: Direct Reading Over API

**ALWAYS read the book content directly rather than using API calls.**

See `docs/extraction-lessons-learned.md` for why:
- API extraction: $50-100 per book, 26+ hours, unreliable
- Direct reading: $0, ~1 hour, 100% reliable

## Extraction Workflow

### Step 1: Identify Book Structure

First, map the book's organization:

```bash
# Check for MinerU-processed content
ls mineru_output/*/auto/*.md

# Read table of contents or first pages
head -200 mineru_output/*/auto/*.md | grep -E "^#|Chapter|Section"
```

Create a chapter-to-page mapping like:
```python
CHAPTER_PAGES = {
    "Ch1_Introduction": (1, 15),
    "Ch2_Anatomy": (16, 45),
    # ... map all chapters
}
```

### Step 2: Define Entity Types

Use domain-specific types from ENTITY-TAXONOMY.md:

**Neurosurgical:**
- artery, vein, nerve, cistern, brain_region, bone_structure
- surgical_step, clipping_technique, surgical_approach
- aneurysm, complication, instrument

**Spine:**
- vertebra, disc, nerve_root, ligament, foramen
- decompression_technique, fusion_technique, fixation_approach
- stenosis, herniation, myelopathy, screw_type

### Step 3: Extract Entities by Chapter

Read each chapter and extract entities with context:

```bash
# Read a chapter section
# Note which chapter/section/page for context
```

For each entity, capture:
- `name`: Canonical name (lowercase, specific)
- `entity_type`: From ENTITY-TAXONOMY.md
- `page`: Source page number
- `chapter`: Chapter reference
- `description`: Brief context from text

### Step 4: Insert into Neo4j

Use batched insertions (20-30 at a time):

```bash
docker exec neurosurgery-neo4j cypher-shell -u neo4j -p "neo4j_dev_pass_2025" "
CREATE (:Anatomy {name: 'middle cerebral artery', book_entity_type: 'artery', page: 79, chapter: 'Ch15_MCA'})
CREATE (:Anatomy {name: 'm1 segment', book_entity_type: 'artery', page: 79, chapter: 'Ch15_MCA'})
// ... more entities
"
```

### Step 5: Build Relationships

Connect entities with surgical knowledge flow:

```bash
docker exec neurosurgery-neo4j cypher-shell -u neo4j -p "neo4j_dev_pass_2025" "
MATCH (a:Pathology {name: 'mca aneurysm'}), (c:Anatomy {name: 'sylvian cistern'})
CREATE (a)-[:LOCATED_IN {context: 'MCA aneurysms in sylvian cistern'}]->(c)
"
```

### Step 6: Log in KAIZEN.md

After each extraction, update KAIZEN.md with:
- Book processed
- Entity/relationship counts
- New patterns discovered
- Mistakes avoided

## Neo4j Label Mapping

| Entity Type | Neo4j Label |
|-------------|-------------|
| artery, vein, nerve, cistern, brain_region | Anatomy |
| surgical_step | Procedure |
| clipping_technique, fusion_technique | Technique |
| aneurysm, stenosis, complication | Pathology |
| instrument, screw_type | Instrument |
| figure, chapter, tenet | Reference |

## Relationship Types

**Anatomical:**
- LOCATED_AT, ADJACENT_TO, SUPPLIES, DRAINS_TO
- PASSES_THROUGH, BRANCHES_FROM

**Surgical:**
- REQUIRES_STEP, FOLLOWED_BY, USES_TECHNIQUE
- USES_INSTRUMENT, APPLIES_TO, TREATS, PROVIDES_ACCESS_TO

**Knowledge:**
- ILLUSTRATED_BY, DESCRIBED_IN, WARNS_ABOUT, REFERENCED_IN

**Clinical:**
- COMPLICATES, INDICATES, CONTRAINDICATES

## Supporting Files

- **ENTITY-TAXONOMY.md** - Complete entity type definitions
- **EXTRACTION-PATTERNS.md** - Proven extraction patterns
- **COMMON-MISTAKES.md** - Anti-patterns to avoid
- **KAIZEN.md** - Continuous improvement log
- **examples/** - Case studies from prior extractions

## Integration with Project

This skill integrates with:
- `neurosurgery_db/ingestion/parser.py` - MinerU JSON parsing
- `neurosurgery_db/ingestion/graph_loader.py` - Neo4j graph loading
- `docker-compose.yml` - Neo4j container configuration

## Quality Checklist

Before finishing an extraction:
- [ ] All chapters processed
- [ ] Entity names are canonical (lowercase, specific)
- [ ] Page references preserved
- [ ] Surgical steps are sequenced (FOLLOWED_BY)
- [ ] Aneurysms/pathologies linked to approaches
- [ ] Complications linked to procedures
- [ ] KAIZEN.md updated with learnings
