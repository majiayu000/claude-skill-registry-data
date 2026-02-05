---
name: strategic-planner
description: Design comprehensive technical specifications and strategic plans for data architecture and analytics projects. This skill should be used when planning major features, creating SPEC documents, assessing product requirements, breaking down complex projects into phases, or documenting architectural strategies like SPEC-1. Guides through requirements gathering, MoSCoW prioritization, phase planning, and open items tracking.
---

# Strategic Planner

Design and document comprehensive technical specifications for Fantasy Football Analytics following the SPEC document format used in the project.

## When to Use This Skill

Use this skill proactively when:

- User requests "create a spec for {feature}" or "plan {major initiative}"
- Planning greenfield architecture (like SPEC-1)
- Breaking down complex multi-phase projects
- Assessing product requirements or PRDs
- Creating strategic documents that will drive sprint planning
- Updating existing specs (versioning)

## Specification Purpose

Specs serve as **strategic blueprints** for major projects, capturing:

1. **Background** - Context and motivation
2. **Requirements (MoSCoW)** - Must/Should/Could/Won't prioritization
3. **Method** - Architecture, implementation phases, technical details
4. **Success Criteria** - Measurable outcomes
5. **ADR References** - Links to architectural decisions
6. **Open Items Tracking** - Unresolved questions and TODOs

**Benefits:**
- Align team on project scope and priorities
- Break complex work into manageable phases
- Document technical decisions with ADR links
- Track open items separately from main spec
- Enable sprint planning from phased tasks

## Specification Types

The FF Analytics project uses specs for:

1. **Data Architecture Specs** (e.g., SPEC-1: Fantasy Football Analytics Data Architecture)
2. **Feature Specifications** (smaller scope, focused features)
3. **PRD Assessments** (evaluate product requirements for feasibility)
4. **Migration Plans** (like prefect_dbt_sources_migration)

## Specification Creation Workflow

### Step 1: Gather Requirements

**Start with discovery questions:**

- What problem are we solving?
- Who are the stakeholders (data consumers, analysts, engineers)?
- What are the current limitations or pain points?
- What business/analytical goals does this support?
- What constraints exist (budget, time, technology)?

**Requirements Gathering Methods:**

1. **User Interviews** - Talk to data consumers (analysts, managers)
2. **Current State Analysis** - Review existing architecture, identify gaps
3. **Competitive Analysis** - Research similar solutions, best practices
4. **Constraint Mapping** - Identify technical, business, timeline constraints

**Output:** Raw list of requirements (unsorted, unfiltered)

### Step 2: Apply MoSCoW Prioritization

**MoSCoW Framework:** Categorize requirements into Must/Should/Could/Won't.

#### Must
**Critical, non-negotiable requirements** for MVP. Without these, the project fails.

**Examples (from SPEC-1):**
- Twice-daily automated schedule (08:00 and 16:00 UTC)
- Ingest commissioner Google Sheet (authoritative source)
- Preserve raw immutable snapshots for backfills
- Canonical entity resolution for Player/Team/Franchise

#### Should
**Important requirements** that add significant value but aren't blocking MVP.

**Examples (from SPEC-1):**
- Trade valuation marts (players + rookie picks)
- Incremental loads and backfills
- Data quality reports
- SCD snapshots for rosters/contracts

#### Could
**Nice-to-have features** if time/resources permit.

**Examples (from SPEC-1):**
- Mobile-friendly triggers
- Discord bot for triggers/summaries
- ML-readiness features

#### Won't (This Version)
**Explicitly out of scope** - prevents scope creep.

**Examples (from SPEC-1):**
- Real-time/streaming game-time mode
- Heavy microservices architecture
- Enterprise warehouse features

**Rule of thumb:**
- Must = 20-30% of requirements (absolute minimum for value)
- Should = 40-50% (makes it great, not just functional)
- Could = 20-30% (polish and convenience)
- Won't = Document to prevent re-litigation

### Step 3: Design Architecture & Break Into Phases

#### Design Architecture

**High-level components:**
- What are the major subsystems? (ingestion, transformation, serving)
- How do they interact? (data flows, APIs, events)
- What technologies? (DuckDB, dbt, GCS, etc.)
- What patterns? (Kimball dimensional modeling, 2×2 stat model)

**Reference existing ADRs:**
- ADR-009: 2×2 stat model (actuals vs projections, real-world vs fantasy)
- ADR-010: mfl_id canonical player identity
- Link to ADRs for all major architectural decisions

**Example (from SPEC-1):**
```text
Orchestration: GitHub Actions (schedule + workflow_dispatch)
Compute: Ephemeral GitHub runners (Python/SQL)
Storage: Google Cloud Storage (GCS) - Parquet lake
Engine: DuckDB with httpfs for gs:// access
Transforms: dbt-duckdb with External Parquet
Analytics: Google Colab notebooks
```

#### Break Into Implementation Phases

**Phase Design Principles:**

1. **Deliver value early** - Phase 1 should produce usable output
2. **Dependencies first** - Core infrastructure before features
3. **Iterative refinement** - Each phase builds on previous
4. **Milestone-based** - Clear completion criteria per phase

**Example Phase Breakdown (from SPEC-1):**

**Phase 1: Core Infrastructure (MVP)**
- GitHub Actions orchestration
- NFLverse ingestion
- Commissioner sheet sync
- Basic dimensional models (dim_player, fact_player_stats)

**Phase 2: Marts & Analytics**
- Trade valuation logic
- Fantasy scoring overlays
- Analytical marts
- Colab notebook templates

**Phase 3: Quality & Observability**
- Data quality tests
- Freshness monitoring
- Cost observability
- Error notifications

**Estimation Guidelines:**
- Phase duration: 1-4 weeks for most phases
- Tasks per phase: 5-15 discrete tasks
- Dependencies: Map cross-phase dependencies explicitly

### Step 4: Document Technical Details

**Be comprehensive and specific:**

#### Schemas
Show actual table structures with column names, types, and descriptions:

```sql
-- dim_player (SCD Type 2)
CREATE TABLE dim_player (
    player_id VARCHAR PRIMARY KEY,  -- mfl_id (canonical)
    player_name VARCHAR NOT NULL,
    position VARCHAR NOT NULL,
    nfl_team VARCHAR,
    valid_from DATE NOT NULL,
    valid_to DATE,  -- NULL = current
    is_current BOOLEAN NOT NULL
)
```

#### Data Flows
Describe how data moves through the system:

```text
Raw Layer (GCS) → dbt Staging → dbt Core (Facts/Dims) → dbt Marts → Notebooks
```

#### Configurations
Include sample configurations:

```yaml
# dbt model config for External Parquet
{{ config(
    materialized='table',
    external=true,
    partition_by=['season', 'week']
) }}
```

#### Algorithms
Explain complex logic (e.g., trade valuation, identity resolution):

```text
Trade Value Calculation:
1. Get KTC value for each asset (player or pick)
2. Apply league format multiplier (1QB vs SF)
3. Sum total value for each side
4. Calculate net value difference
5. Apply fairness threshold (±10%)
```

### Step 5: Define Success Criteria

**Make criteria measurable and testable:**

**Good success criteria:**
- ✅ "All 5 data sources ingesting successfully on twice-daily schedule"
- ✅ "dbt test suite passes with >95% success rate"
- ✅ "Notebooks load mart data in <5 seconds"
- ✅ "End-to-end data latency <2 hours from source update"

**Bad success criteria:**
- ❌ "System works well"
- ❌ "Users are happy"
- ❌ "Data is accurate"

**Format as checklist:**
```markdown
## Success Criteria

- [ ] All commissioner data synced within 12 hours
- [ ] NFLverse stats updated within 24 hours during season
- [ ] Trade valuation mart refreshed on each run
- [ ] Notebook examples demonstrating all marts
- [ ] <95% dbt test pass rate
```

### Step 6: Track Open Items

Create companion `{SPEC}_open_items.md` file to track unresolved questions.

**Use `assets/open_items_template.md`** for structure.

**Example open items (from SPEC-1):**

```markdown
## Phase 1: MVP

### High Priority
- [ ] **Identity Resolution**: Finalize canonical player ID (mfl_id vs gsis_id)
  - Decision needed: See ADR-010
  - Blockers: None

- [ ] **Scoring Config**: Which scoring format to prioritize? (PPR, Half-PPR, Standard)
  - Impact: Affects fantasy point calculations
  - Decision by: Week 1

### Medium Priority
- [ ] **Historical Backfill**: How far back to load NFLverse data?
  - Options: 2020 (3 seasons) vs 2015 (8 seasons)
  - Trade-off: Storage cost vs historical analysis depth

## Phase 2: Enhancements

### Low Priority
- [ ] **Mobile UI**: Determine if mobile-friendly dashboard is needed
  - Status: Deferred to post-MVP
```

**Benefits of separate tracking:**
- Keeps main spec clean and focused
- Enables prioritization and assignment
- Links to ADRs when decisions are made
- Clear status tracking (open, in progress, resolved, deferred)

## Best Practices

### Versioning Specs

Specs evolve - use version numbers:

- **v1.0** - Initial spec
- **v1.1** - Minor updates (clarifications, small scope changes)
- **v2.0** - Major updates (significant architecture changes)

**When to version:**
- Update version in frontmatter: `**Version**: 2.2`
- Note changelog at bottom or in separate file
- Reference version in sprint tasks

### Linking ADRs

Every major architectural decision should link to an ADR:

```markdown
## Architecture Decision Records

- [ADR-009](docs/adr/ADR-009-2x2-stat-model.md) - 2×2 stat model structure
- [ADR-010](docs/adr/ADR-010-mfl-id-canonical.md) - mfl_id as canonical player ID
- [ADR-014](docs/adr/ADR-014-pick-identity.md) - Pick identity resolution
```

**Workflow:**
1. Draft spec with architectural decisions
2. Create ADRs for major decisions (use adr-creator skill)
3. Link ADRs in spec
4. Update ADRs as decisions evolve

### Include Code Samples

Don't just describe - show actual code:

**SQL snippets:**
```sql
-- Example query pattern from mart
SELECT
    player_name,
    position,
    SUM(fantasy_points) as season_total
FROM mart_fantasy_actuals_weekly
WHERE season = 2024
GROUP BY player_name, position
```

**dbt model configs:**
```sql
{{ config(
    materialized='table',
    external=true,
    partition_by=['season', 'week']
) }}
```

**Python ingestion patterns:**
```python
# NFLverse load pattern
df = load_player_stats(
    seasons=[2024],
    stat_type="weekly"
)
```

### Document Phases Granularly

Each phase should be atomic and standalone:

**Good phase definition:**
```markdown
**Phase 1.2: Core Facts (2 weeks)**

Tasks:
1. Create fact_player_stats (grain: player + game + stat)
2. Add grain uniqueness test (unique_combination_of_columns)
3. Create FK relationships to dim_player, dim_game
4. Validate stat_value measures (not_null, >= 0)
5. Test with 2024 season data
6. Document query patterns in notebook

Completion Criteria:
- fact_player_stats passing all dbt tests
- Sample queries working in notebook
- Performance <5s for single-season queries
```

**Bad phase definition:**
```markdown
**Phase 1: Build core models**
- Create facts and dimensions
- Add tests
```

## Integration with Other Skills

- **adr-creator**: Specs reference ADRs for architectural decisions
- **sprint-planner**: Specs inform sprint task creation
- **dbt-model-builder**: Specs define models to be built
- **notebook-creator**: Specs define notebook deliverables

**Project Workflow:**
1. **strategic-planner** creates SPEC (architecture & phases)
2. **adr-creator** documents key technical decisions
3. **sprint-planner** breaks phases into executable sprint tasks
4. Implementation uses **dbt-model-builder**, **data-quality-test-generator**, **notebook-creator**

## Resources

### assets/
- `spec_template.md` - Base specification template with MoSCoW structure
- `open_items_template.md` - Template for tracking unresolved questions
- `feature_track_template.md` - Template for feature-specific specs

### references/
- `example_spec.md` - SPEC-1 v2.2 (567 lines, comprehensive architecture spec)
- `example_open_items.md` - SPEC-1 open items tracking (393 lines)
- `example_prd_assessment.md` - PRD evaluation template

## Common Patterns

### Data Architecture Specs

**Pattern:** Comprehensive system design with multiple components

**Characteristics:**
- 300-600 lines (like SPEC-1)
- Multiple implementation phases (3-5 phases)
- Extensive technical details (schemas, configs, code)
- References 5-10 ADRs
- MoSCoW with 15-30 requirements

**Example:** SPEC-1 - Fantasy Football Analytics Data Architecture

**Structure:**
- Background (project context)
- Requirements (MoSCoW with Must/Should/Could/Won't)
- Method (Architecture, phases, technical details)
- Success Criteria (measurable outcomes)
- ADR References (design decisions)
- Open Items (link to separate file)

### Feature Specs

**Pattern:** Focused feature addition to existing architecture

**Characteristics:**
- 100-200 lines
- 1-2 implementation phases
- Targeted technical details
- References 1-3 ADRs
- MoSCoW with 5-10 requirements

**Example:** Adding injury data integration

**Structure:**
- Background (why injury data?)
- Requirements (MoSCoW focused on injury feature)
- Method (ingestion approach, schema additions)
- Success Criteria (injury data availability)
- ADR References (if needed for decisions)

### PRD Assessments

**Pattern:** Evaluate external product requirements for feasibility

**Characteristics:**
- Response to external PRD
- Feasibility analysis (technical, timeline, cost)
- Alternative approaches
- Risk assessment
- Implementation recommendation

**Example:** `example_prd_assessment.md`

**Structure:**
- PRD Summary (external request)
- Feasibility Analysis (can we build this?)
- Technical Approach (how would we build it?)
- Risks & Mitigation (what could go wrong?)
- Recommendation (build / defer / reject)
