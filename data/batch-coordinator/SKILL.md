---
name: batch-coordinator
description: |
  Validates and coordinates batch study guide operations (both separate and merge modes).
  Ensures file availability, template compatibility, and source-only policy before launching agents.

  **CRITICAL AUTOMATION**: Prevents batch processing errors by validating all prerequisites.
skill_type: guardrail
enforcement_level: suggest
priority: high
version: 1.0.0
---

## Core Responsibility

Validate batch study guide operations and coordinate appropriate agent invocation based on mode (separate vs merge).

**When batch processing detected** → validate prerequisites → suggest appropriate agent → ensure quality gates.

---

## When This Activates

**Prompt Triggers:**
- User mentions "multiple files", "batch", "combine", "merge"
- Semicolon-separated file list detected
- `--merge` flag present

**File Triggers:**
- Command arguments contain multiple files (semicolon-separated)
- Multiple file paths in a single command invocation

**Examples:**
```bash
/drugs-3-tab-excel "HIV.txt;Antibiotics.txt;Antivirals.txt"
/drugs-3-tab-excel --merge "HIV-Lec1.txt;HIV-Lec2.txt;HIV-Lec3.txt"
/clinical-assessment-html --merge "Lower-Back.txt;Spine.txt;Neuro.txt" "Back Pain"
```

---

## How This Works

### Step 1: Detect Batch Mode

When user provides multiple files, determine mode:

**Batch Separate** (default for multiple files):
- No `--merge` flag
- User wants: N files → N outputs
- Agent: `batch-separate-processor` (launched N times)

**Batch Merge** (explicit flag):
- `--merge` flag present
- User wants: N files → 1 merged output
- Agent: `batch-merge-orchestrator` (launched once)

---

### Step 2: Validation Checklist

Before allowing batch processing, validate:

#### **File Validation**
```
BATCH FILE VALIDATION:
☐ All file paths provided
☐ All files exist and are readable
☐ File count matches user intent
☐ No duplicate files in list
☐ Total content size manageable (estimate tokens)
```

#### **Template Compatibility**
```
TEMPLATE VALIDATION:
☐ Template type specified (excel, word, html-LO, etc.)
☐ Template compatible with ALL files
☐ Files are homogeneous (all drug lectures, all condition files, etc.)
☐ Special parameters present if required (e.g., chief complaint for clinical)
```

#### **Source-Only Policy**
```
SOURCE-ONLY VALIDATION:
☐ User acknowledges source-only policy per mode:
  - Batch Separate: Source-only per file
  - Batch Merge: Source-only across merged content
☐ Exception: Mnemonics WILL be researched via WebSearch
☐ No external knowledge beyond templates and researched mnemonics
```

#### **Mode-Specific Validation**

**For Batch Separate:**
```
BATCH SEPARATE VALIDATION:
☐ Each file will create separate output
☐ Architectural isolation via subagents (zero contamination)
☐ Output count: N files → N outputs
☐ Each file gets complete verification
```

**For Batch Merge:**
```
BATCH MERGE VALIDATION:
☐ Files are related/compatible for merging
☐ User wants ONE unified output
☐ Merge orchestrator will resolve overlaps
☐ Source traceability will be maintained
☐ Conflicts will be documented
☐ Output count: N files → 1 merged output
```

---

### Step 3: Agent Suggestion

Based on mode, suggest appropriate agent:

#### **For Batch Separate:**

```
I'll use the batch-separate-processor agent to process your files with architectural isolation.

**What will happen:**
1. batch-separate-processor agent launched per file (N times total)
2. Each invocation processes ONE file in isolated context
3. Zero cross-contamination (architectural guarantee)
4. Output: N separate study guides

**Agent invocations:**
- File 1: batch-separate-processor → Output1
- File 2: batch-separate-processor → Output2
- File 3: batch-separate-processor → Output3
...
- File N: batch-separate-processor → OutputN

Ready to proceed? [Confirm: yes to start batch processing]
```

#### **For Batch Merge:**

```
I'll use the batch-merge-orchestrator agent to intelligently merge your files.

**What will happen:**
1. batch-merge-orchestrator agent launched ONCE with all N files
2. Agent reads ALL files completely
3. Creates content matrix (which files cover which topics)
4. Identifies overlaps and gaps
5. Resolves conflicts with source traceability
6. Merges into ONE comprehensive study guide
7. Creates merge report with traceability map

**Output:**
- 1 merged study guide: [filename]
- 1 merge report: [filename]_merge_report.md

Ready to proceed? [Confirm: yes to start batch merge]
```

---

## What Gets SUGGESTED

### ✓ Batch Operations with Valid Prerequisites

When ALL validation passes:
- Suggest appropriate agent (batch-separate-processor OR batch-merge-orchestrator)
- Provide clear explanation of what will happen
- Request user confirmation

### ✓ Batch with Minor Issues

When validation has minor issues (e.g., file naming ambiguity):
- Suggest agent with warnings
- Note potential issues
- Recommend user review

---

## What Gets BLOCKED (Soft Block)

### ❌ Missing Files

```
⚠️ BATCH VALIDATION FAILED
Issue: File(s) not found
Missing: [list files]
Action: Please verify file paths and try again
```

### ❌ Incompatible Files

```
⚠️ BATCH VALIDATION FAILED
Issue: Files are incompatible for merging
File1: Drug lecture (pharmacology)
File2: Clinical presentation (medicine)
Reason: Different content types require different templates
Action: Use batch separate mode OR separate commands
```

### ❌ Template Mismatch

```
⚠️ BATCH VALIDATION FAILED
Issue: Template incompatible with file content
Template: Excel Drug Chart (expects drug list)
Files contain: Learning objectives (not drugs)
Action: Use /LO-html or /LO-word instead of /drugs-3-tab-excel
```

### ❌ No Merge Flag with Merge Intent

```
⚠️ AMBIGUOUS INTENT DETECTED
You provided multiple files without --merge flag.

Default behavior: Batch Separate (N files → N outputs)
Did you mean: Batch Merge (N files → 1 output)?

If you want ONE merged output, add --merge flag:
/drugs-3-tab-excel --merge "file1.txt;file2.txt;file3.txt"

If you want separate outputs, proceed as-is:
/drugs-3-tab-excel "file1.txt;file2.txt;file3.txt"
```

---

## Integration with Other Skills

### **Before Batch Processing**
- **batch-coordinator** validates prerequisites
- **source-only-enforcer** validates source policy understanding

### **During Batch Processing**
- **batch-separate-processor** OR **batch-merge-orchestrator** executes batch operation

### **After Batch Processing**
- **study-guide-verifier** suggests accuracy verification
- **study-guide-analyzer** agent performs 6-step verification

**Coordination:**
```
User Command
    ↓
batch-coordinator (validates)
    ↓
source-only-enforcer (enforces policy)
    ↓
batch-separate-processor OR batch-merge-orchestrator (processes)
    ↓
study-guide-verifier (suggests verification)
    ↓
study-guide-analyzer (verifies output)
```

---

## Examples

### Example 1: Batch Separate (N files → N outputs)

**User:** `/drugs-3-tab-excel "HIV.txt;Antibiotics.txt;Antivirals.txt"`

**batch-coordinator response:**
```
BATCH SEPARATE MODE DETECTED
Files: 3
Output: 3 separate Excel charts

Validation:
✓ All files exist
✓ Template: Excel Drug Chart (compatible)
✓ Mode: Batch Separate (N → N outputs)

I'll use batch-separate-processor agent (3 invocations):
- Invocation 1: HIV.txt → HIV_Drug_Chart.xlsx
- Invocation 2: Antibiotics.txt → Antibiotics_Chart.xlsx
- Invocation 3: Antivirals.txt → Antivirals_Chart.xlsx

Architectural isolation guarantees zero cross-contamination.

Ready to proceed?
```

### Example 2: Batch Merge (N files → 1 output)

**User:** `/drugs-3-tab-excel --merge "HIV-PIs.txt;HIV-NRTIs.txt;HIV-NNRTIs.txt"`

**batch-coordinator response:**
```
BATCH MERGE MODE DETECTED
Files: 3 (HIV drug classes)
Output: 1 merged Excel chart

Validation:
✓ All files exist
✓ Files are related (all HIV drugs)
✓ Template: Excel Drug Chart (compatible)
✓ Mode: Batch Merge (N → 1 merged output)

I'll use batch-merge-orchestrator agent:
1. Read all 3 files completely
2. Create content matrix (which drugs in which files)
3. Resolve overlaps (if same drug in multiple files)
4. Merge intelligently with source traceability
5. Output: HIV_Comprehensive_Chart.xlsx + merge_report.md

Ready to proceed?
```

### Example 3: Clinical Merge (Chief Complaint)

**User:** `/clinical-assessment-html --merge "Lower-Back.txt;Spine.txt;Neuro.txt" "Back Pain"`

**batch-coordinator response:**
```
BATCH MERGE MODE DETECTED (Clinical)
Files: 3 (condition files)
Chief Complaint: Back Pain
Output: 1 merged clinical guide

Validation:
✓ All files exist
✓ Template: Clinical Assessment (compatible)
✓ Chief complaint specified
✓ Mode: Batch Merge with filtering

I'll use batch-merge-orchestrator agent:
1. Read all 3 files
2. Extract ONLY back pain related content from each
3. Merge relevant information
4. Create unified clinical guide for back pain
5. Output: Back_Pain_Clinical_Guide.html + merge_report.md

Ready to proceed?
```

---

## Deep-Dive Resources

(None yet - skill is self-contained)

---

## Troubleshooting

**Q: User provides multiple files but no clear intent?**
A: Ask for clarification. Default to batch separate, but suggest --merge if files seem related.

**Q: Files are incompatible for merging?**
A: Suggest batch separate mode instead. Explain why merge isn't appropriate.

**Q: Too many files (e.g., 50 files)?**
A: Warn about performance. Suggest processing in smaller batches.

**Q: Files don't exist yet?**
A: Block processing. User must create source files first.

---

## Quality Assurance

This skill ensures batch processing never starts without:
- ✓ Valid file paths
- ✓ Template compatibility
- ✓ Clear mode (separate vs merge)
- ✓ Source-only policy understanding
- ✓ Appropriate agent selected

By validating upfront, we prevent errors mid-processing and ensure high-quality batch outputs.
