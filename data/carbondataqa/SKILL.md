---
name: carbon.data.qa
description: Answer analytical questions about carbon accounting data using internal datasets, APIs, and emission factor calculations.
---

# carbon.data.qa

## Purpose

This skill enables Claude to answer factual, analytical questions about carbon accounting data by querying Carbon ACX's internal datasets (CSV files in `data/` directory), derived artifacts, and the local API when running. It encodes domain knowledge about:

- Carbon accounting terminology and units (tCO2e, kWh, pkm, etc.)
- Emission factor structures and relationships
- Activity-to-emissions calculations
- Temporal data queries (Q1 2024, monthly totals, etc.)
- Layer, sector, and profile hierarchies

## When to Use

**Trigger Patterns:**
- User asks about emissions data: "What were total CO2 emissions for Q1 2024?"
- Queries about specific activities: "What's the emission factor for streaming video?"
- Comparative questions: "Compare emissions from cloud storage vs local storage"
- Data exploration: "Show me all activities in the professional services layer"
- Unit conversions: "Convert 500 kWh to tCO2e"
- Source/provenance queries: "Where does the video streaming data come from?"

**Do NOT Use When:**
- User wants to generate reports (use `carbon.report.gen` instead)
- User wants to write code (use `acx.code.assistant` instead)
- Questions about repo structure or development setup
- Non-carbon-accounting questions

## Allowed Tools

- `read_file` - Read CSV data files, JSON artifacts, schemas
- `python` - Process data, perform calculations, query APIs
- `grep` - Search for specific activities or emission factors
- `bash` - Run simple data queries via command line (read-only)

**Access Level:** 1 (Local Execution - read-only, no file writes, no external network)

**Tool Rationale:**
- `read_file`: Required to access canonical CSV data in `data/` directory
- `python`: Needed for parsing CSVs, JSON artifacts, performing unit conversions and emission calculations
- `grep`: Efficient searching through data files for specific patterns
- `bash`: Helpful for quick file inspection and data exploration

**Explicitly Denied:**
- `write_file`, `edit_file` - This is a read-only analytical skill
- `web_fetch` with external URLs - Only internal localhost API endpoints allowed

## Expected I/O

**Input:**
- Type: Natural language question (string)
- Format: Free-form query about carbon data
- Constraints: Must relate to carbon accounting, emissions, or activities in the dataset
- Examples:
  - "What is the emission factor for coffee?"
  - "Total emissions from video streaming in 2024"
  - "List all military operations activities"
  - "What units are used for grid intensity?"

**Output:**
- Type: Structured answer with data, units, and citations
- Format: Markdown with tables, bullet lists, and inline values
- Requirements:
  - **MUST include units** (tCO2e, kWh, etc.) with all numeric answers
  - **MUST cite data sources** - reference `source_id` from `data/sources.csv`
  - **MUST include timestamp** - data vintage or "as of" date
  - Handle ambiguity by asking clarifying questions
- Example:
  ```markdown
  **Emission Factor for HD Video Streaming:**

  - Activity: `MEDIA.STREAM.HD.HOUR` (HD video streaming per hour)
  - Emission Factor: 0.055 kgCO2e/hour
  - Unit: kgCO2e per hour of streaming
  - Source: [SOURCE_ID_123] - "Streaming Energy Report 2023"
  - Vintage: 2023
  - Notes: Includes device playback + network delivery
  ```

**Validation:**
- Every numeric value has explicit units
- Sources are referenced by `source_id`
- "Unknown" or "Data not available" for missing data (never guess)
- Calculations show methodology

## Dependencies

**Required:**
- Access to Carbon ACX data directory (`data/`)
- Python 3.11+ with pandas, PyYAML
- Understanding of data schema (see `reference/data_schema.md`)
- Carbon accounting units glossary (see `reference/units_glossary.md`)

**Data Files:**
- `data/activities.csv` - Activity catalog
- `data/emission_factors.csv` - Emission factors
- `data/layers.csv` - Layer definitions
- `data/sectors.csv` - Sector taxonomy
- `data/units.csv` - Unit definitions and conversions
- `data/sources.csv` - Data provenance
- `data/profiles.csv` - Activity profiles
- `calc/outputs/` - Derived artifacts (if available)

**Optional:**
- Local API at `http://localhost:8787/api` (when Worker is running)
- Derived JSON manifests in `dist/artifacts/`

## Examples

### Example 1: Basic Emission Factor Query

**User:** "What's the emission factor for a cup of coffee?"

**Claude Process:**
1. Recognize this is a carbon data query → invoke `carbon.data.qa` skill
2. Search `data/activities.csv` for coffee-related activities
3. Find matching emission factor in `data/emission_factors.csv`
4. Look up source details in `data/sources.csv`
5. Format answer with units and citation

**Output:**
```markdown
**Coffee Emission Factor:**

- Activity: `FOOD.COFFEE.CUP.HOT` (12 oz hot coffee cup)
- Emission Factor: 0.021 kgCO2e/cup
- Source: [SRC_FOOD_2023] Coffee supply chain LCA
- Vintage: 2023
- Scope: Includes bean production, roasting, brewing, waste
```

### Example 2: Aggregation Query

**User:** "Show me total emissions from all social media activities"

**Claude Process:**
1. Query `data/activities.csv` for activities with `category=social`
2. Load corresponding emission factors
3. Aggregate by activity type
4. Present as table with sources

**Output:**
```markdown
**Social Media Activity Emissions (per hour):**

| Activity | Emission Factor | Source |
|----------|----------------|--------|
| YouTube streaming | 0.046 kgCO2e/hr | SRC_MEDIA_2024 |
| Facebook browsing | 0.038 kgCO2e/hr | SRC_SOCIAL_2024 |
| Instagram scrolling | 0.041 kgCO2e/hr | SRC_SOCIAL_2024 |
| TikTok watching | 0.043 kgCO2e/hr | SRC_SOCIAL_2024 |

*All values include device use + network transfer*
*Data vintage: 2024*
```

### Example 3: Ambiguous Query Handling

**User:** "What are the emissions for streaming?"

**Claude Process:**
1. Recognize ambiguity - multiple streaming types exist
2. Ask clarifying question before searching

**Output:**
```markdown
I found multiple streaming activities in the dataset:

1. **Video streaming:**
   - HD video (1080p)
   - UHD/4K video
   - SD video (mobile)

2. **Audio streaming:**
   - Standard quality music

3. **Platform-specific:**
   - YouTube
   - Social media video (TikTok, Instagram, etc.)

Which type of streaming would you like emission data for?
```

### Example 4: Unit Conversion Query

**User:** "How much CO2 does 500 kWh of Ontario grid electricity produce?"

**Claude Process:**
1. Look up Ontario grid emission factor in `data/emission_factors.csv`
2. Find activity `ENERGY.CA-ON.GRID.KWH`
3. Perform calculation: 500 kWh × emission factor
4. Show calculation with units

**Output:**
```markdown
**Ontario Grid Electricity Emissions:**

- Activity: `ENERGY.CA-ON.GRID.KWH`
- Consumption: 500 kWh
- Emission Factor: 0.025 kgCO2e/kWh (Ontario IESO grid average)
- **Total Emissions: 12.5 kgCO2e** (0.0125 tCO2e)

*Calculation: 500 kWh × 0.025 kgCO2e/kWh = 12.5 kgCO2e*
*Source: [SRC_GRID_ON_2024]*
*Vintage: 2024 annual average*
```

### Example 5: Edge Case - Missing Data

**User:** "What's the emission factor for blockchain mining?"

**Claude Process:**
1. Search `data/activities.csv` for blockchain/crypto activities
2. No matches found
3. Return graceful "not found" response

**Output:**
```markdown
**Data Not Available**

I could not find emission factors for blockchain or cryptocurrency mining in the current Carbon ACX dataset (v1.2).

The dataset currently focuses on:
- Professional services and food
- Digital infrastructure (streaming, cloud, AI)
- Industrial operations
- Transportation and logistics
- Military and defense operations
- Earth system feedbacks

You might be interested in related activities:
- Cloud server operations (`ONLINE.DC.CLOUD.SERVER.HOUR`)
- Data center rack usage (`ONLINE.DC.COLOCATION.RACK.MONTH`)

Would you like information on any of these instead?
```

## Limitations

**Known Edge Cases:**
- Cannot answer questions requiring data not in the CSV files
- Temporal queries limited to vintage years present in dataset
- Cannot perform predictive modeling or forecasting
- Regional data limited to what's explicitly coded (e.g., Ontario grid)
- Some activities have emission factors marked as "to be added"

**Performance Constraints:**
- Large aggregations across all activities may take 5-10 seconds
- Complex cross-layer queries require multiple file reads
- Derived artifacts may not always be up-to-date with source CSVs

**Security Boundaries:**
- Read-only access to data files
- No external API calls (except localhost Worker API)
- Cannot modify source data
- Cannot access files outside `data/` or `calc/outputs/` directories

**Scope Limitations:**
- Answers based solely on Carbon ACX dataset - no external knowledge
- Does not perform lifecycle assessments beyond what's in emission factors
- Does not provide regulatory compliance advice
- Does not make emission reduction recommendations (analytical only)

## Validation Criteria

**Success Metrics:**
- ✅ All numeric answers include explicit units (kgCO2e, tCO2e, etc.)
- ✅ Every emission factor cites `source_id` or notes if source missing
- ✅ Data vintage/timestamp included in responses
- ✅ Ambiguous queries prompt for clarification before answering
- ✅ Missing data returns graceful "not found" rather than guessing
- ✅ Calculations show methodology (formula with units)
- ✅ Responses match data files exactly (no hallucination)

**Failure Modes:**
- ❌ Returns emission values without units → REJECT
- ❌ Makes up data not in CSV files → REJECT
- ❌ Provides answers without source attribution → WARN
- ❌ Performs calculations with wrong units → REJECT
- ❌ Answers ambiguous questions without clarification → WARN

**Recovery:**
- If uncertain about data interpretation: Ask user for clarification
- If data missing: Explicitly state "Data not available" and suggest alternatives
- If calculation complex: Show step-by-step methodology
- If source missing: Note "Source not specified in dataset"

## Related Skills

**Dependencies:**
- None - this is a foundational skill

**Composes With:**
- `carbon.report.gen` - Use this skill to gather data, then generate reports
- `acx.code.assistant` - This skill informs what data structures exist for code generation

**Alternative Skills:**
- For report generation: `carbon.report.gen`
- For code generation: `acx.code.assistant`
- For schema validation: `schema.linter`

## Maintenance

**Owner:** ACX Team
**Review Cycle:** Monthly (align with dataset releases)
**Last Updated:** 2025-10-18
**Version:** 1.0.0

**Maintenance Notes:**
- Update when new CSV files added to `data/`
- Review when emission factor schema changes
- Validate examples against current dataset version
- Keep `reference/data_schema.md` synchronized with actual schema
