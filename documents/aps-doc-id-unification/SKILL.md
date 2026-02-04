---
name: aps-doc-id-unification
description: Expert documentation generation for ID unification layers. Documents identity resolution algorithms, merge strategies, match rules, entity graphs, and multi-workflow orchestration. Use when documenting ID unification processes.
---

# APS ID Unification Documentation Expert

Specialized skill for generating comprehensive documentation for ID unification layers with multiple workflow components.

## When to Use This Skill

Use this skill when:
- Documenting ID unification workflows
- Creating documentation for identity resolution logic
- Documenting merge strategies and match rules
- Generating documentation for prep table creation
- Documenting enrichment workflows
- Creating multi-workflow documentation (prep + unification + enrichment)

**Example requests:**
```
"Document the ID unification layer with all workflows"
"Create documentation for identity resolution logic"
"Document merge strategies and match rules"
"Generate ID unification documentation following this template: [Confluence URL]"
```

---

## 🚨 MANDATORY: Codebase Access Required

**WITHOUT codebase access = NO documentation. Period.**

**If no codebase access provided:**
```
I cannot create technical documentation without codebase access.

Required:
- Directory path to ID unification workflows
- Access to .dig, .yml, unify.yml files

Without access, I cannot extract match rules, merge keys, or workflow configs.
Provide path: "Code is in /path/to/id_unification/"
```

**Before proceeding:**
1. Ask for codebase path if not provided
2. Use Glob to verify files exist
3. STOP if cannot read files

**Documentation MUST contain:**
- Real match keys from unify.yml
- Actual workflow names from .dig files
- Real table names and prep configs
- Working examples from actual code

**NO generic placeholders. Only real, extracted data.**

## REQUIRED Documentation Template

**Follow this EXACT structure (analyzed from production examples):**

### For Parent ID Unification Page:

```markdown
# ID Unification

## Overview
{Brief description of the layer}

{Links to child workflow pages}
```

### For Individual Workflow Pages (Child Pages):

**1. Main Orchestration Workflow (unif_runner.dig)**

```markdown
# Main Orchestration Workflow (unif_runner.dig)

## Overview
{Purpose and business value}

## Workflow Configuration
- Timezone & Scheduling
- Configuration Files Loaded

## Workflow Execution Steps

### Step 1: Prep Creation
{What it does, business meaning, what gets created, processing time}

### Step 2: ID Unification
{What it does, business meaning, what gets created, processing time}

### Step 3: Enrichment
{What it does, business meaning, what gets created, processing time}

## Error Handling
{_error workflow, alert configuration}

## Complete Workflow Flow
{Text-based flow diagram showing all steps}

## Usage Scenarios
- Manual Execution (First Time Setup)
- Scheduled Execution (Production)
- Troubleshooting a Failed Run

## Monitoring & Troubleshooting
- Success Indicators
- Common Issues
- Useful Monitoring Queries

## Summary
{Quick reference commands and next steps}
```

**2. Prep Table Creation Workflow (dynamic_prep_creation.dig)**

```markdown
# Prep Table Creation Workflow (dynamic_prep_creation.dig)

## Overview
{Purpose and business value}

## Workflow Configuration
- Timezone & Scheduling
- Configuration Files Loaded

## Workflow Execution Steps

### Step 1: Initialize Schema
{Create tables: unif_input, unif_input_tmp_td, exclusion_list}

### Step 2: Reset Configuration Table
{Empty unif_prep_config}

### Step 3: Parse Configuration & Process Tables
- Step 3a: Store Generated SQL
- Step 3b: Create/Update Prep Tables (4 SQL operations explained)
- Step 3c: Populate Unified Input Table

### Step 4: Finalize Unified Input Table
{Detailed breakdown: Drop/Recreate, Get Latest Data, Apply Exclusion List, Filter All-Null Records}
{Complete data flow example with exclusion list}

## Data Flow Diagram
{Text diagram showing source → prep → unified input}

## Configuration Example
{src_prep_params.yml structure with real examples}

## Key Benefits
{6 key benefits listed}

## Monitoring & Troubleshooting
- Success Indicators
- Common Issues
- Useful Queries

## Summary
{Next steps and technical details}
```

**3. ID Unification Workflow (id_unification.dig)**

```markdown
# ID Unification Workflow (id_unification.dig)

## Overview
{Purpose and business value}

## Workflow Configuration
- Timezone & Scheduling
- Configuration Files
- Key Parameters

## Workflow Execution Steps
{Step-by-step breakdown of TD API call, merge logic, master table creation}

## unify.yml Configuration
{Real structure with keys, tables, persistent_ids/canonical_ids}

## Match Rules and Merge Iterations
{Explain merge_by_keys and merge_iterations}

## Master Tables Created
{List all output tables: persistent_ids_master, lookup, mapping tables}

## Monitoring & Troubleshooting
- Success Indicators
- Common Issues
- Useful Queries

## Summary
```

**4. Enrichment Workflow (enrich_runner.dig)**

```markdown
# Enrichment Workflow (enrich_runner.dig)

## Overview
{Purpose and business value}

## Workflow Configuration
- Configuration Files
- Enrichment Table List

## Workflow Execution Steps
{Step-by-step: Loop through tables, generate JOIN SQL, create enriched tables}

## Enrichment Logic
{SQL pattern for joining with unified IDs}

## Enriched Tables Created
{List all tables with unified ID columns}

## Monitoring & Troubleshooting
- Success Indicators
- Enrichment Coverage Queries
- Common Issues

## Summary
```

---

**Template Usage Notes:**
- Read actual .dig workflows, unify.yml, src_prep_params.yml
- Extract REAL match keys, merge iterations, table configurations
- Document REAL prep table logic, exclusion list usage
- Use actual workflow file names and paths
- Include working SQL/YAML examples from codebase
- Document all 4 workflows as child pages under parent
- NO placeholders - only real extracted data

## Summary

This skill generates production-ready ID unification documentation by:
- Reading actual .dig workflows, unify.yml, and config files from codebase
- Following the exact parent/child template structure shown above
- Extracting real match rules, merge strategies, and workflow configurations
- Creating comprehensive multi-workflow documentation with working examples

**Key capability:** Transforms complex ID unification codebase into professional Confluence documentation with parent page and 4 detailed child workflow pages.
