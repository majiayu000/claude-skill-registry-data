---
name: options-analysis
description: Use when making structured decisions between multiple options - creates weighted scoring spreadsheet with systematic evaluation across considerations grouped by area
---

# Options Analysis

## Overview

Guide users through creating structured multi-criteria decision analysis (MCDA) spreadsheets using Google Sheets.

**Core principle:** Systematic evaluation with weighted scoring, resumable workflow, and state-driven navigation.

**Announce at start:** "I'm using the options-analysis skill to help you systematically evaluate your options."

**When to use:**
- Comparing multiple options (cloud providers, vendors, architectural approaches)
- Need structured, auditable decision framework
- Want weighted scoring across multiple criteria
- Require justifications for each score

**Output:** Google Spreadsheet with:
- Analysis sheet: Options × Considerations with scores (0-5) and justifications
- Summary sheet: Weighted scores and ranking
- Metadata sheet: Area weights and workflow state

## Prerequisites

This skill requires a Google Sheets MCP server. If not already configured, see Setup Guide below.

## Table of Contents

1. [Setup Guide](#setup-guide) - Install Google Sheets MCP server
2. [Quick Reference](#quick-reference) - State detection and phase mapping
3. [The Workflow](#the-workflow) - Main checklist and phases
4. [Phase Details](#phase-details) - Detailed instructions per phase
5. [State Detection Logic](#state-detection-logic) - How to infer current state
6. [Google Sheets Operations](#google-sheets-operations) - MCP patterns and formulas
7. [Common Mistakes](#common-mistakes) - Anti-patterns and troubleshooting

---

## Setup Guide

### Installing Google Sheets MCP Server

**Check if already configured:**

```bash
# Check for google-sheets MCP server in available tools
# (MCP servers show up as mcp__google-sheets__* tools)
```

If you see `mcp__google-sheets__*` tools available, skip to [The Workflow](#the-workflow).

**Install Google Sheets MCP Server:**

Option 1: Using npx (Node.js required):
```bash
npx -y google-sheets-mcp
```

Option 2: Using uvx (Python, recommended):
```bash
uvx mcp-google-sheets@latest
```

**Configure in Claude Code:**

Add to your Claude Code MCP configuration file:

For npx version:
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "google-sheets-mcp"]
    }
  }
}
```

For uvx version:
```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "uvx",
      "args": ["mcp-google-sheets@latest"]
    }
  }
}
```

### Authentication Setup

**Recommended: Service Account**

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account credentials
5. Download JSON key file
6. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```
7. Share spreadsheets with service account email (found in JSON key)

**Alternative: OAuth 2.0**

Follow MCP server's OAuth setup instructions (more complex, better for personal use).

### Verification

Test the connection:

1. List available MCP tools - should see `mcp__google-sheets__*` functions
2. Try reading a test spreadsheet
3. If errors occur, check:
   - MCP server is running
   - Authentication credentials are valid
   - Service account has access to spreadsheet

---

## Quick Reference

| Current State | Detected By | Next Phase |
|---------------|-------------|------------|
| No spreadsheet | User hasn't provided URL | Create new spreadsheet |
| Empty spreadsheet | No sheets named "Analysis", "Summary", "Metadata" | Define options |
| Has Metadata sheet | Read workflow checklist from Metadata | Jump to incomplete phase |
| `options_defined: false` | Metadata.B8 = FALSE | Define Options (Phase 2) |
| `areas_defined: false` | Metadata.B9 = FALSE | Define Areas & Weights (Phase 3) |
| `considerations_defined: false` | Metadata.B10 = FALSE | Define Considerations (Phase 4) |
| `scoring_complete: false` | Metadata.B11 = FALSE | Scoring (Phase 5) |
| `summary_created: false` | Metadata.B12 = FALSE | Summary Generation (Phase 6) |
| All checklist items TRUE | All Metadata workflow flags = TRUE | Maintenance Mode (Phase 7) |

---

## State Detection Logic

When the skill is invoked, follow this sequence:

### Step 1: Get Spreadsheet Reference

Ask user: "Do you have an existing options analysis spreadsheet, or should I create a new one?"

**If new:**
- Prompt for analysis name/title
- Create new spreadsheet with that title
- Proceed to Phase 2 (Define Options)

**If existing:**
- Prompt for spreadsheet URL or ID
- Extract spreadsheet ID from URL (format: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`)
- Proceed to Step 2

### Step 2: Read Spreadsheet Structure

Use MCP tool to list sheets in spreadsheet.

**Check for key sheets:**
- "Analysis" sheet exists?
- "Summary" sheet exists?
- "Metadata" sheet exists?

**If no sheets exist:** Fresh spreadsheet, go to Phase 2 (Define Options)

**If Metadata sheet exists:** Read workflow state (Step 3)

**If only Analysis exists, no Metadata:** Corrupted state - offer to create Metadata sheet and infer state from Analysis structure

### Step 3: Read Metadata Sheet Workflow State

Metadata sheet structure:
```
     A                     B
7  Workflow State
8  options_defined       TRUE/FALSE
9  areas_defined         TRUE/FALSE
10 considerations_defined TRUE/FALSE
11 scoring_complete      TRUE/FALSE
12 summary_created       TRUE/FALSE
```

Read cells B8:B12 to determine which phases are complete.

### Step 4: Display Current State and Menu

Example output:
```
Options Analysis Status:
✓ Options defined (3 options: AWS, Azure, GCP)
✓ Areas defined (4 areas with weights)
✓ Considerations defined (18 considerations across areas)
○ Scoring in progress (42 of 54 cells scored - 78%)
○ Summary not yet created

What would you like to do?
1. Continue scoring (12 cells remaining)
2. Add new option
3. Add new consideration or area
4. Modify area weights
5. Review current scores
6. Generate summary (requires all scoring complete)
7. Start fresh analysis (will archive current work)
```

Use AskUserQuestion tool to present menu with options.

### Step 5: Route to Appropriate Phase

Based on user selection and current state, jump to the relevant phase section below.

---

## The Workflow

When starting this skill, create a TodoWrite checklist to track progress:

```markdown
Options Analysis Workflow:
- [ ] Phase 1: State Detection & Orientation
- [ ] Phase 2: Define Options
- [ ] Phase 3: Define Areas & Weights
- [ ] Phase 4: Define Considerations
- [ ] Phase 5: Scoring
- [ ] Phase 6: Summary Generation
- [ ] Phase 7: Maintenance (ongoing)
```

Copy this checklist to TodoWrite at the start of each session. Update task status as you progress through phases.

### Phase Overview

| Phase | Goal | Output |
|-------|------|--------|
| 1. State Detection | Determine current analysis state | Navigation menu |
| 2. Define Options | Set up options being evaluated | Analysis sheet with option columns |
| 3. Define Areas & Weights | Create decision areas with importance weights | Metadata sheet with normalized weights |
| 4. Define Considerations | Add specific criteria under each area | Analysis sheet with colored, grouped rows |
| 5. Scoring | Collect scores and justifications for each cell | Populated Analysis sheet |
| 6. Summary Generation | Calculate weighted scores and ranking | Summary sheet with formulas |
| 7. Maintenance | Add options/considerations, modify weights | Updated analysis |

Phases 2-6 can be partially completed and resumed. Phase 7 is entered after initial analysis is complete.

---
## Phase Details

### Phase 2: Define Options

**Goal:** Establish the options being evaluated (e.g., AWS, Azure, GCP).

**Prerequisites:** Spreadsheet created (empty or has ID)

**Steps:**

#### Step 1: Prompt for options

Ask user: "What options are you evaluating? Please list them separated by commas."

Example user response: "AWS, Azure, Google Cloud Platform"

Parse response into array: `["AWS", "Azure", "Google Cloud Platform"]`

#### Step 2: Create/update Analysis sheet

**If Analysis sheet doesn't exist:**

Use MCP tool to create sheet named "Analysis"

**Set up header row (Row 1):**

| A | B | C | D |
|---|---|---|---|
| Consideration | AWS | Azure | Google Cloud Platform |

Write to cells:
- A1: "Consideration"
- B1: First option name
- C1: Second option name
- ... (one column per option)

**Formatting:**
- Row 1: Bold, freeze row (so it stays visible when scrolling)
- Font size: 11pt
- Background: Light gray (#F3F3F3)

#### Step 3: Create Metadata sheet

Create sheet named "Metadata"

**Write initial structure:**

```
     A                     B        C          D
1  Options Analysis Metadata
2
3  Options:
4  [List options here]
5
6  Areas & Weights:
7  (To be defined in Phase 3)
8
9  Workflow State:
10 options_defined       TRUE
11 areas_defined         FALSE
12 considerations_defined FALSE
13 scoring_complete      FALSE
14 summary_created       FALSE
```

Write cells:
- A1: "Options Analysis Metadata" (Bold, size 14)
- A3: "Options:"
- A4: Join options with ", " (e.g., "AWS, Azure, Google Cloud Platform")
- A6: "Areas & Weights:"
- A9: "Workflow State:"
- A10: "options_defined", B10: "TRUE"
- A11: "areas_defined", B11: "FALSE"
- A12: "considerations_defined", B12: "FALSE"
- A13: "scoring_complete", B13: "FALSE"
- A14: "summary_created", B14: "FALSE"

#### Step 4: Update TodoWrite and report

Mark Phase 2 as complete in TodoWrite.

Report to user:
```
✓ Phase 2 Complete: Options defined

Analysis sheet created with [N] options: [option names]
Metadata sheet initialized with workflow state.

Next: Define decision areas and their weights (Phase 3)
```

Proceed to Phase 3 or return to menu based on user preference.

---
### Phase 3: Define Areas & Weights

**Goal:** Create conceptual decision areas (e.g., Reliability, Cost) and assign importance weights.

**Prerequisites:** Phase 2 complete (options defined)

**Steps:**

#### Step 1: Prompt for areas

Ask user: "What are the key decision areas you want to evaluate? These group related considerations together."

Examples to suggest:
- Technical: "Reliability, Performance, Security, Scalability"
- Business: "Cost, Vendor Support, Ecosystem, Compliance"
- User Experience: "Usability, Documentation, Community, Tooling"

Parse response into array of area names.

#### Step 2: Prompt for weights

For each area, ask: "On a scale of relative importance, how would you weight [Area Name]? You can use percentages (e.g., 30%) or relative numbers (e.g., 3). I'll normalize them afterward."

Collect weights for all areas.

**Normalization:**

Example inputs: Reliability: 40, Cost: 30, Security: 20, Usability: 10

Sum: 100 (already normalized)

If sum ≠ 100, normalize:
- Reliability: 40/100 * 100 = 40%
- Cost: 30/100 * 100 = 30%
- Security: 20/100 * 100 = 20%
- Usability: 10/100 * 100 = 10%

#### Step 3: Write areas to Metadata sheet

Update Metadata sheet starting at row 7:

```
     A              B
6  Areas & Weights:
7  Reliability     40
8  Cost            30
9  Security        20
10 Usability       10
```

For each area:
- Column A: Area name
- Column B: Normalized weight (as number, e.g., 40 not 40%)

#### Step 4: Choose colors for areas

Assign distinct, pleasant background colors to each area for visual grouping:

| Area Index | Color Name | Hex Code |
|------------|------------|----------|
| 1 | Light Blue | #CFE2F3 |
| 2 | Light Green | #D9EAD3 |
| 3 | Light Yellow | #FFF2CC |
| 4 | Light Orange | #F4CCCC |
| 5 | Light Purple | #D9D2E9 |
| 6 | Light Teal | #D0E0E3 |

Cycle through colors if more than 6 areas.

Store color mapping in memory for Phase 4.

#### Step 5: Update workflow state

Update Metadata!B11 to "TRUE" (areas_defined)

#### Step 6: Report and proceed

Mark Phase 3 complete in TodoWrite.

Report:
```
✓ Phase 3 Complete: Areas & Weights defined

4 decision areas created:
- Reliability (40%)
- Cost (30%)
- Security (20%)
- Usability (10%)

Weights normalized to sum to 100%.

Next: Define specific considerations within each area (Phase 4)
```

Proceed to Phase 4 or return to menu.

---
### Phase 4: Define Considerations

**Goal:** Add specific evaluation criteria under each decision area, with visual grouping.

**Prerequisites:** Phase 3 complete (areas and weights defined)

**Steps:**

#### Step 1: Read areas from Metadata

Read Metadata sheet rows 7+ to get list of areas and their assigned colors.

#### Step 2: For each area, prompt for considerations

For each area, ask: "What specific considerations fall under [Area Name]? List them separated by commas."

Example for "Reliability" area:
User response: "Multi-region support, Disaster recovery options, SLA guarantees, Monitoring capabilities"

Parse into array: `["Multi-region support", "Disaster recovery options", "SLA guarantees", "Monitoring capabilities"]`

Repeat for all areas.

#### Step 3: Build Analysis sheet structure

Start writing to Analysis sheet at row 3 (row 1 is header, row 2 blank for spacing).

Current row tracker: `current_row = 3`

**For each area:**

1. **Write area header row:**
   - A[current_row]: Area name + weight, e.g., "Reliability (40%)"
   - Format:
     - Bold font
     - Font size: 12pt
     - Background color: Area's assigned color (from Phase 3)
     - Merge cells A[current_row]:[last_option_column][current_row]
   - Increment: `current_row += 1`

2. **Write consideration rows:**
   - For each consideration in this area:
     - A[current_row]: "  ├─ " + consideration name (e.g., "  ├─ Multi-region support")
     - Use "  └─ " for the last consideration in the area
     - Format:
       - Normal font (not bold)
       - Background color: Lighter shade of area color (add 30% white overlay)
     - For score columns (B through last option):
       - Leave cell empty (for scoring in Phase 5)
       - Set data validation: Whole number between 0 and 5
       - Set conditional formatting:
         - 0-1: Red background (#F4CCCC)
         - 2-3: Yellow background (#FFF2CC)
         - 4-5: Green background (#D9EAD3)
     - Increment: `current_row += 1`

3. **Add blank row for spacing:**
   - Increment: `current_row += 1`

#### Step 4: Example structure

After this phase, Analysis sheet should look like:

```
     A                          B      C       D
1  Consideration              AWS   Azure   GCP
2
3  Reliability (40%)          [merged across all columns, light blue bg]
4    ├─ Multi-region support  [empty] [empty] [empty]
5    ├─ Disaster recovery     [empty] [empty] [empty]
6    ├─ SLA guarantees        [empty] [empty] [empty]
7    └─ Monitoring            [empty] [empty] [empty]
8
9  Cost (30%)                 [merged across all columns, light green bg]
10   ├─ Total cost of ownership [empty] [empty] [empty]
11   └─ Licensing model       [empty] [empty] [empty]
12
...
```

All empty cells have data validation (0-5) and conditional formatting.

#### Step 5: Update Metadata workflow state

Update Metadata!B12 to "TRUE" (considerations_defined)

#### Step 6: Calculate total scoring cells

Count total empty score cells: `num_options * num_considerations`

Store this in memory for progress tracking in Phase 5.

#### Step 7: Report and proceed

Mark Phase 4 complete in TodoWrite.

Report:
```
✓ Phase 4 Complete: Considerations defined

18 considerations added across 4 areas:
- Reliability: 4 considerations
- Cost: 2 considerations
- Security: 8 considerations
- Usability: 4 considerations

Total scoring cells to complete: 54 (18 considerations × 3 options)

Data validation and conditional formatting applied to all score cells.

Next: Score each option for each consideration (Phase 5)
```

Proceed to Phase 5 or return to menu.

---
### Phase 5: Scoring

**Goal:** Collect scores (0-5) and justifications for each option-consideration pair.

**Prerequisites:** Phase 4 complete (considerations defined)

**Steps:**

#### Step 1: Identify unscored cells

Scan Analysis sheet for empty cells in score columns (columns B onward, excluding area header rows).

Build list of unscored cells with their coordinates and labels:
- Cell: B4
- Option: "AWS" (from column B header)
- Consideration: "Multi-region support" (from column A, removing tree chars)
- Area: "Reliability" (from nearest area header above)

#### Step 2: Display progress

Calculate and display progress:
```
Scoring Progress: 42 of 54 cells scored (78%)

Remaining cells by area:
- Reliability: 3 cells
- Cost: 5 cells
- Security: 2 cells
- Usability: 2 cells
```

#### Step 3: Prompt for scores

**For each unscored cell:**

Use AskUserQuestion or direct prompt:

"Score [Option] for [Consideration] (under [Area]):

Scale:
0 = Poor/Not supported
1 = Minimal/Barely adequate
2 = Below average
3 = Average/Acceptable
4 = Good/Above average
5 = Excellent/Best in class

Score (0-5): "

Wait for user input (validate it's a number 0-5).

**Then prompt for justification:**

"Provide a brief justification for this score (this will be saved as a cell comment): "

Wait for user input (1-2 sentences recommended).

#### Step 4: Write score and comment

- Write the numeric score to the cell
- Add the justification as a cell comment/note using Google Sheets MCP

Example MCP call (pseudocode):
```
mcp__google-sheets__write_cell(
  spreadsheet_id=current_spreadsheet,
  sheet="Analysis",
  cell="B4",
  value=4
)

mcp__google-sheets__add_comment(
  spreadsheet_id=current_spreadsheet,
  sheet="Analysis",
  cell="B4",
  comment="Strong multi-region support with automated failover. Tested in production."
)
```

#### Step 5: Update progress

After each score, recalculate and display progress:
```
✓ Scored AWS for Multi-region support: 4/5

Progress: 43 of 54 cells scored (80%)
Remaining: 11 cells
```

#### Step 6: Handle interruptions

User can pause anytime. Skill should:
- Save all scores entered so far
- Return to menu
- When resumed, detect which cells are still empty and continue from there

#### Step 7: Completion detection

When all cells are scored (no empty score cells remain):

Update Metadata!B13 to "TRUE" (scoring_complete)

Mark Phase 5 complete in TodoWrite.

Report:
```
✓ Phase 5 Complete: All scoring finished

54 of 54 cells scored (100%)

All options have been evaluated across all considerations.
Justifications saved as cell comments.

Next: Generate summary with weighted scoring (Phase 6)
```

Proceed to Phase 6 or return to menu.

---
### Phase 6: Summary Generation

**Goal:** Create Summary sheet with weighted scoring formulas and ranking.

**Prerequisites:** Phase 5 complete (all cells scored)

**Steps:**

#### Step 1: Create Summary sheet

Use MCP tool to create sheet named "Summary"

#### Step 2: Set up Summary sheet structure

**Row 1 - Headers:**

| A | B | C | D |
|---|---|---|---|
| Option | Raw Score | Weighted Score | Rank |

Format: Bold, background #F3F3F3, freeze row

#### Step 3: Write option names

For each option (from Analysis!B1, C1, D1...):

Write to Summary column A, starting row 2:
- A2: First option name (e.g., "AWS")
- A3: Second option name
- ... etc

#### Step 4: Calculate Raw Score (simple average)

For each option row in Summary:

**Formula for Raw Score (column B):**

Example for AWS (Summary!B2):
```
=AVERAGE(Analysis!B:B)
```

BUT we need to exclude:
- Header row (row 1)
- Area header rows (merged cells)
- Empty cells

**Better formula using AVERAGEIF:**

```
=AVERAGEIF(Analysis!B:B, ">-1", Analysis!B:B)
```

This averages all numeric values in column B of Analysis sheet.

Write this formula to Summary!B2 (for first option).

Adjust column reference for each option (B for first, C for second, etc.).

#### Step 5: Calculate Weighted Score

**This is the critical formula to avoid consideration-count bias.**

Read areas and weights from Metadata sheet (rows 7+).

For each area:
1. Identify which rows in Analysis belong to this area
2. Calculate AVERAGE of scores for this option in those rows
3. Multiply by area weight
4. Sum across all areas

**Formula structure for AWS (Summary!C2):**

```excel
=SUMPRODUCT(
  Metadata!B7:B10,  // Area weights (40, 30, 20, 10)
  {
    AVERAGE(Analysis!B4:B7),   // Reliability scores (rows 4-7)
    AVERAGE(Analysis!B10:B11), // Cost scores (rows 10-11)
    AVERAGE(Analysis!B14:B21), // Security scores (rows 14-21)
    AVERAGE(Analysis!B24:B27)  // Usability scores (rows 24-27)
  }
) / 100
```

**Dynamic formula generation:**

Since row ranges depend on how many considerations per area, we need to:

1. Read Analysis sheet to determine area row ranges
2. Build the array formula dynamically
3. Write formula to cell

**Pseudocode:**
```
areas = read_metadata_areas()  // [(name, weight, color), ...]
area_ranges = []

for area in areas:
  start_row = find_area_header_row(area.name) + 1
  end_row = start_row + count_considerations_in_area(area) - 1
  area_ranges.append(f"AVERAGE(Analysis!B{start_row}:B{end_row})")

formula = f"=SUMPRODUCT(Metadata!B7:B{6+len(areas)}, {{{','.join(area_ranges)}}})/100"

write_cell(Summary!C2, formula)
```

Repeat for each option, adjusting column (B→C→D...).

#### Step 6: Add Rank formula

For each option in Summary:

**Formula for Rank (column D):**

```
=RANK(C2, $C$2:$C$[last_row], 0)
```

This ranks based on Weighted Score (column C), descending order (0 = highest is rank 1).

Example for AWS (Summary!D2):
```
=RANK(C2, $C$2:$C$4, 0)
```

Assuming 3 options (rows 2-4).

#### Step 7: Apply conditional formatting to Rank

Format Rank column with colors:
- Rank 1: Green background (#D9EAD3), bold
- Rank 2: Yellow background (#FFF2CC)
- Rank 3+: Light red background (#F4CCCC)

#### Step 8: Format numbers

- Raw Score: 2 decimal places (e.g., 3.45)
- Weighted Score: 2 decimal places (e.g., 72.30)
- Rank: Whole number (e.g., 1)

#### Step 9: Update Metadata workflow state

Update Metadata!B14 to "TRUE" (summary_created)

All workflow states now TRUE - analysis complete!

#### Step 10: Report results

Mark Phase 6 complete in TodoWrite.

Display summary results:
```
✓ Phase 6 Complete: Summary generated

Final Rankings:
1. AWS - Weighted Score: 78.50 (Raw: 4.20)
2. Azure - Weighted Score: 71.20 (Raw: 3.85)
3. Google Cloud Platform - Weighted Score: 65.80 (Raw: 3.50)

Summary sheet created with:
- Raw scores (simple average across all considerations)
- Weighted scores (area-weighted average)
- Automatic ranking

Formulas will update automatically if scores change.

Analysis complete! You can now:
- Review the Summary sheet for final rankings
- Add more options or considerations (Phase 7 - Maintenance)
- Share the spreadsheet with stakeholders
```

Proceed to Phase 7 (Maintenance Mode) or end session.

---
### Phase 7: Maintenance Mode

**Goal:** Extend or modify completed analysis.

**Prerequisites:** Phase 6 complete (summary generated) OR any phase complete and user wants to make changes

**Available Operations:**

#### Operation A: Add New Option

**When:** User wants to evaluate an additional alternative.

**Steps:**

1. Prompt for new option name
2. Insert new column in Analysis sheet:
   - Insert after last existing option column
   - Header (row 1): New option name
   - Copy data validation and conditional formatting from existing option column
3. Update Summary sheet:
   - Add new row with option name
   - Copy formulas from existing rows, adjust column references
4. Mark scoring as incomplete:
   - Update Metadata!B13 to "FALSE" (scoring_complete)
5. Return to Phase 5 to score new option across all considerations

**Important:** Formulas in Summary sheet must be updated to include new column.

#### Operation B: Add New Consideration

**When:** User realizes an important criterion was missed.

**Steps:**

1. Prompt: "Which area does this consideration belong to?"
2. Display list of existing areas for selection
3. Prompt for consideration name
4. Find the area's section in Analysis sheet
5. Insert new row:
   - After last consideration in that area, before blank row
   - Column A: "  ├─ " + consideration name (or "  └─ " if now last in area)
   - Update previous last consideration from "  └─ " to "  ├─ "
   - Score columns: Empty with data validation (0-5) and conditional formatting
6. Update Summary sheet formulas:
   - Adjust AVERAGE range for that area to include new row
7. Mark scoring as incomplete:
   - Update Metadata!B13 to "FALSE"
8. Return to Phase 5 to score new consideration for all options

#### Operation C: Add New Area

**When:** User wants to add entirely new decision category.

**Steps:**

1. Prompt for area name and weight
2. Recalculate and normalize all weights (including new area)
3. Update Metadata sheet with new area and normalized weights
4. Assign color to new area (next in rotation)
5. Insert area header row in Analysis sheet:
   - Append at bottom (after last area)
   - Format with assigned color
6. Prompt for considerations under this area
7. Add consideration rows (same as Operation B)
8. Update Summary sheet formulas to include new area in SUMPRODUCT
9. Mark areas_defined, considerations_defined, and scoring_complete as FALSE
10. Return to Phase 5 for scoring

#### Operation D: Modify Area Weights

**When:** User wants to change importance of decision areas.

**Steps:**

1. Display current weights from Metadata sheet
2. Prompt for new weights (can modify one or all)
3. Normalize new weights to sum to 100%
4. Update Metadata sheet weights (column B, rows 7+)
5. Summary sheet formulas automatically recalculate (they reference Metadata)
6. Display updated rankings

**Note:** This doesn't require re-scoring; formulas update automatically.

#### Operation E: Re-score Specific Cells

**When:** User wants to revise a previous score.

**Steps:**

1. Prompt: "Which option and consideration would you like to re-score?"
2. Display current score and justification (from cell and comment)
3. Prompt for new score and justification
4. Update cell value and comment
5. Summary formulas automatically recalculate

#### Operation F: Review and Export

**When:** Analysis is complete and user wants to share.

**Steps:**

1. Display Summary sheet rankings
2. Offer to:
   - Generate shareable link
   - Adjust sharing permissions
   - Export to PDF (if MCP server supports)
   - Create presentation slides (future enhancement)

#### Maintenance Menu

When in Maintenance Mode, present this menu:

```
Analysis Complete - Maintenance Mode

Current rankings (as of last update):
1. AWS (78.50)
2. Azure (71.20)
3. GCP (65.80)

What would you like to do?
1. Add new option
2. Add new consideration
3. Add new decision area
4. Modify area weights
5. Re-score specific cells
6. Review and share
7. Return to main menu
8. End session
```

Use AskUserQuestion tool to present menu.

---

## Google Sheets Operations Reference

This section documents common MCP operations used throughout the skill.

### Creating Sheets

**Create new spreadsheet:**
```
Use: mcp__google-sheets__create_spreadsheet
Parameters:
  - title: "Options Analysis - [Project Name]"
Result: spreadsheet_id
```

**Create new sheet within spreadsheet:**
```
Use: mcp__google-sheets__create_sheet
Parameters:
  - spreadsheet_id: [id from above]
  - title: "Analysis" | "Summary" | "Metadata"
```

### Reading Data

**Read single cell:**
```
Use: mcp__google-sheets__read_cell
Parameters:
  - spreadsheet_id
  - sheet: "Metadata"
  - cell: "B10"  # e.g., options_defined status
Result: cell value
```

**Read range:**
```
Use: mcp__google-sheets__read_range
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "A1:Z100"  # or specific range like "B4:D7"
Result: 2D array of values
```

**List sheets:**
```
Use: mcp__google-sheets__list_sheets
Parameters:
  - spreadsheet_id
Result: Array of sheet names
```

### Writing Data

**Write single cell:**
```
Use: mcp__google-sheets__write_cell
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - cell: "B4"
  - value: 4  # or "AWS" for text
```

**Write range (batch write):**
```
Use: mcp__google-sheets__write_range
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "A1:D1"
  - values: [["Consideration", "AWS", "Azure", "GCP"]]
```

**Write formula:**
```
Use: mcp__google-sheets__write_cell
Parameters:
  - spreadsheet_id
  - sheet: "Summary"
  - cell: "C2"
  - value: "=SUMPRODUCT(Metadata!B7:B10, {AVERAGE(Analysis!B4:B7), AVERAGE(Analysis!B10:B11)})/100"
  - is_formula: true  # Important: treat as formula, not string
```

### Formatting

**Set cell background color:**
```
Use: mcp__google-sheets__format_cells
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "A3:D3"  # Area header row
  - format:
      backgroundColor: "#CFE2F3"  # Light blue
```

**Set font formatting:**
```
Use: mcp__google-sheets__format_cells
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "A1:D1"  # Header row
  - format:
      bold: true
      fontSize: 11
```

**Merge cells:**
```
Use: mcp__google-sheets__merge_cells
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "A3:D3"  # Area header spans all option columns
```

**Freeze rows:**
```
Use: mcp__google-sheets__freeze_rows
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - rows: 1  # Freeze first row (headers)
```

### Data Validation

**Set dropdown or numeric constraints:**
```
Use: mcp__google-sheets__set_data_validation
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "B4:D50"  # All score cells
  - validation:
      type: "NUMBER_BETWEEN"
      min: 0
      max: 5
      strict: true  # Reject invalid input
```

### Conditional Formatting

**Color scale based on value:**
```
Use: mcp__google-sheets__set_conditional_formatting
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - range: "B4:D50"
  - rules:
    - condition: "NUMBER_BETWEEN"
      min: 0
      max: 1
      format: {backgroundColor: "#F4CCCC"}  # Red
    - condition: "NUMBER_BETWEEN"
      min: 2
      max: 3
      format: {backgroundColor: "#FFF2CC"}  # Yellow
    - condition: "NUMBER_BETWEEN"
      min: 4
      max: 5
      format: {backgroundColor: "#D9EAD3"}  # Green
```

### Comments

**Add comment to cell:**
```
Use: mcp__google-sheets__add_comment
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - cell: "B4"
  - comment: "Strong multi-region support with automated failover."
```

**Read comment from cell:**
```
Use: mcp__google-sheets__read_comment
Parameters:
  - spreadsheet_id
  - sheet: "Analysis"
  - cell: "B4"
Result: comment text
```

### Common Patterns

**Pattern 1: Write header row with formatting**
```
1. Write values: write_range(A1:D1, [["Consideration", "AWS", "Azure", "GCP"]])
2. Format bold: format_cells(A1:D1, {bold: true})
3. Format background: format_cells(A1:D1, {backgroundColor: "#F3F3F3"})
4. Freeze row: freeze_rows(1)
```

**Pattern 2: Insert area header with color**
```
1. Write area name with weight: write_cell(A3, "Reliability (40%)")
2. Merge across columns: merge_cells(A3:D3)
3. Format bold: format_cells(A3:D3, {bold: true, fontSize: 12})
4. Set background color: format_cells(A3:D3, {backgroundColor: "#CFE2F3"})
```

**Pattern 3: Add consideration row with validation**
```
1. Write consideration name: write_cell(A4, "  ├─ Multi-region support")
2. Set row background: format_cells(A4:D4, {backgroundColor: "#E8F0FE"})  # Lighter blue
3. Set data validation: set_data_validation(B4:D4, {type: "NUMBER_BETWEEN", min: 0, max: 5})
4. Set conditional formatting: set_conditional_formatting(B4:D4, [...color rules...])
```

---

## Common Mistakes

### 1. Not Normalizing Area Weights

**Symptom:** Weighted scores don't make sense, rankings seem arbitrary.

**Cause:** Area weights don't sum to 100%, so formula produces incorrect results.

**Fix:** Always normalize weights after collecting them:
```
total = sum(all_weights)
normalized_weight = (weight / total) * 100
```

### 2. Incorrect SUMPRODUCT Formula

**Symptom:** All options get the same weighted score, or scores are way off.

**Cause:** Using simple AVERAGE across all considerations instead of area-weighted average.

**Wrong:**
```
=AVERAGE(Analysis!B:B) * 100
```

**Correct:**
```
=SUMPRODUCT(Metadata!B7:B10, {AVERAGE(Analysis!B4:B7), AVERAGE(Analysis!B10:B11), ...})/100
```

**Why:** Each area must be averaged separately first, then multiplied by its weight.

### 3. Hardcoding Row Numbers in Formulas

**Symptom:** Formulas break when adding new considerations or areas.

**Cause:** Using fixed ranges like `B4:B7` that don't adjust when rows are inserted.

**Fix:** When adding considerations, regenerate Summary formulas with updated ranges. OR use named ranges that expand automatically.

### 4. Forgetting to Update Workflow State

**Symptom:** Skill resumes in wrong phase, menu shows incorrect options.

**Cause:** Not updating Metadata workflow cells (B10:B14) after completing phases.

**Fix:** Always update Metadata!B[row] to "TRUE" when completing a phase.

### 5. Not Setting Data Validation

**Symptom:** Users enter invalid scores (e.g., 10, -1, "good"), breaking formulas.

**Cause:** Forgot to set data validation on score cells.

**Fix:** Apply data validation (0-5, whole numbers, strict) to all score cells immediately when creating consideration rows.

### 6. Skipping Cell Comments

**Symptom:** Scores exist but no one remembers why they were assigned.

**Cause:** Not collecting justifications or not saving them as comments.

**Fix:** Always prompt for justification after each score, save as cell comment.

### 7. Manually Editing Metadata Sheet

**Symptom:** Skill loses track of state, formulas break, areas disappear.

**Cause:** User or skill directly edited Metadata structure without following format.

**Fix:** Only modify Metadata through skill operations. If corrupted, offer to rebuild from Analysis sheet structure.

## Anti-Patterns

### Don't: Mix Phase Orders Without State Updates

Jumping between phases (e.g., adding options in Phase 7 but not marking scoring_complete as FALSE) creates inconsistent state.

**Do:** Update ALL relevant workflow flags when making structural changes.

### Don't: Use Row Numbers in Menu Display

Telling user "row 23 needs scoring" is cryptic.

**Do:** Always display human-readable labels: "AWS - Multi-region support" not "cell B23"

### Don't: Require All Scoring Before Summary

While recommended, forcing 100% scoring before allowing summary generation is too rigid.

**Do:** Allow summary generation at any point, but warn if incomplete: "Warning: Only 42 of 54 cells scored. Rankings may be inaccurate."

### Don't: Overwrite Existing Scores Without Confirmation

Re-scoring should show current value and ask for confirmation.

**Do:** Display current score and justification, ask "Update this score? (Y/N)"

### Don't: Use Generic Error Messages

"Error writing to sheet" doesn't help debug.

**Do:** Specific errors: "Error: Cannot write to cell B4. Spreadsheet may be read-only. Check sharing permissions."

---

## Example Workflow

This example walks through a complete options analysis from start to finish.

**Scenario:** Choosing a cloud provider for a new application.

### Session Start

**User:** "I need to choose between AWS, Azure, and Google Cloud for my app."

**Claude (with skill):** "I'm using the options-analysis skill to help you systematically evaluate your options."

[Skill checks for Google Sheets MCP server - found]

**Claude:** "Do you have an existing options analysis spreadsheet, or should I create a new one?"

**User:** "Create a new one."

### Phase 2: Define Options

**Claude:** "What options are you evaluating? Please list them separated by commas."

**User:** "AWS, Azure, Google Cloud"

[Skill creates spreadsheet "Options Analysis - Cloud Provider Selection"]
[Skill creates Analysis sheet with header row]
[Skill creates Metadata sheet with workflow state]

**Claude:** "✓ Phase 2 Complete: Options defined. Analysis sheet created with 3 options: AWS, Azure, Google Cloud. Next: Define decision areas and their weights (Phase 3)"

### Phase 3: Define Areas & Weights

**Claude:** "What are the key decision areas you want to evaluate? These group related considerations together."

**User:** "Reliability, Cost, Performance, Developer Experience"

**Claude:** "On a scale of relative importance, how would you weight Reliability?"

**User:** "40%"

**Claude:** "How would you weight Cost?"

**User:** "30%"

**Claude:** "How would you weight Performance?"

**User:** "20%"

**Claude:** "How would you weight Developer Experience?"

**User:** "10%"

[Skill normalizes weights - already sum to 100%]
[Skill writes to Metadata sheet]
[Skill assigns colors: Reliability=Blue, Cost=Green, Performance=Yellow, DevEx=Orange]

**Claude:** "✓ Phase 3 Complete: Areas & Weights defined. 4 decision areas created with normalized weights. Next: Define specific considerations within each area (Phase 4)"

### Phase 4: Define Considerations

**Claude:** "What specific considerations fall under Reliability? List them separated by commas."

**User:** "SLA guarantees, multi-region support, disaster recovery, monitoring tools"

[Skill records 4 considerations for Reliability]

**Claude:** "What specific considerations fall under Cost?"

**User:** "Pricing model, free tier, cost optimization tools"

[Skill records 3 considerations for Cost]

**Claude:** "What specific considerations fall under Performance?"

**User:** "Latency, throughput, global CDN, caching options"

[Skill records 4 considerations for Performance]

**Claude:** "What specific considerations fall under Developer Experience?"

**User:** "Documentation quality, community support, ease of setup"

[Skill records 3 considerations for Developer Experience]

[Skill builds Analysis sheet structure with colored areas and tree-formatted considerations]
[Skill applies data validation (0-5) and conditional formatting to all score cells]

**Claude:** "✓ Phase 4 Complete: Considerations defined. 14 considerations added across 4 areas. Total scoring cells to complete: 42 (14 considerations × 3 options). Next: Score each option for each consideration (Phase 5)"

### Phase 5: Scoring

**Claude:** "Scoring Progress: 0 of 42 cells scored (0%). Let's start scoring. Score AWS for SLA guarantees (under Reliability). Scale: 0=Poor, 5=Excellent. Score (0-5):"

**User:** "4"

**Claude:** "Provide a brief justification for this score:"

**User:** "99.99% uptime SLA, proven track record, clear escalation process"

[Skill writes 4 to Analysis!B4, adds comment]

**Claude:** "✓ Scored AWS for SLA guarantees: 4/5. Progress: 1 of 42 cells scored (2%). Remaining: 41 cells. Score AWS for Multi-region support?"

**User:** "5"

**Claude:** "Justification?"

**User:** "Mature multi-region architecture, automatic failover, extensive global presence"

[Process continues for all 42 cells...]

[After 30 minutes and 42 scores...]

**Claude:** "✓ Phase 5 Complete: All scoring finished. 42 of 42 cells scored (100%). All options have been evaluated across all considerations. Justifications saved as cell comments. Next: Generate summary with weighted scoring (Phase 6)"

### Phase 6: Summary Generation

[Skill creates Summary sheet]
[Skill writes headers: Option, Raw Score, Weighted Score, Rank]
[Skill writes option names in column A]
[Skill calculates raw scores using AVERAGE]
[Skill builds SUMPRODUCT formulas for weighted scores based on area ranges]
[Skill adds RANK formulas]
[Skill applies conditional formatting to Rank column]

**Claude:** "✓ Phase 6 Complete: Summary generated.

Final Rankings:
1. AWS - Weighted Score: 76.20 (Raw: 4.14)
2. Google Cloud - Weighted Score: 71.50 (Raw: 3.93)
3. Azure - Weighted Score: 68.30 (Raw: 3.79)

Summary sheet created with raw scores, weighted scores, and automatic ranking. Formulas will update automatically if scores change. Analysis complete! You can now review the Summary sheet, add more options or considerations, or share the spreadsheet."

### Phase 7: Maintenance (Later Session)

[User returns to spreadsheet next week]

**User:** "I want to add Oracle Cloud as a fourth option."

**Claude (with skill):** [Detects existing spreadsheet, reads Metadata]

**Claude:** "Options Analysis Status:
✓ Options defined (3 options: AWS, Azure, Google Cloud)
✓ Areas defined (4 areas with weights)
✓ Considerations defined (14 considerations)
✓ Scoring complete (42 of 42 cells scored)
✓ Summary created

You're in Maintenance Mode. What would you like to do?"

**User:** "Add new option"

**Claude:** "What is the name of the new option?"

**User:** "Oracle Cloud"

[Skill inserts new column E in Analysis sheet]
[Skill updates Summary sheet with new row and formulas]
[Skill marks scoring_complete as FALSE]

**Claude:** "✓ New option added: Oracle Cloud. Analysis sheet updated with new column. Summary formulas updated. 14 cells need scoring for Oracle Cloud. Returning to scoring phase..."

[Skill resumes scoring for just the Oracle Cloud column]

---
