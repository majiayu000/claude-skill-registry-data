---
name: aps-doc-hist-union
description: Expert documentation generation for hist-union workflows. Documents historical and incremental table combination strategies, schema validation, time-based partitioning, and backfill processes. Use when documenting hist-union layers.
---

# APS Hist-Union Documentation Expert

Specialized skill for generating comprehensive documentation for hist-union workflows that combine historical and incremental table data.

## When to Use This Skill

Use this skill when:
- Documenting hist-union workflows
- Creating documentation for historical data combination logic
- Documenting backfill processes
- Generating documentation for table merging strategies
- Documenting schema validation and consistency checks

**Example requests:**
```
"Document the hist-union workflow for events table"
"Create documentation for historical data combination"
"Document the backfill process for customer data"
"Generate hist-union documentation following this template: [Confluence URL]"
```

---

## 🚨 MANDATORY: Codebase Access Required

**WITHOUT codebase access = NO documentation. Period.**

**If no codebase access provided:**
```
I cannot create technical documentation without codebase access.

Required:
- Directory path to hist-union workflows
- Access to .dig, .sql, .yml files

Without access, I cannot extract real table names, union logic, or configurations.
Provide path: "Code is in /path/to/histunion/"
```

**Before proceeding:**
1. Ask for codebase path if not provided
2. Use Glob to verify files exist
3. STOP if cannot read files

**Documentation MUST contain:**
- Real table names from actual configs
- Actual SQL UNION logic from codebase
- Real file paths and line numbers
- Working examples from actual code

**NO generic placeholders. Only real, extracted data.**

## REQUIRED Documentation Template

**Follow this EXACT structure (analyzed from production examples):**

```markdown
# Hist_Union Project Documentation

## Overview
{Brief description of hist-union purpose}

**Key Features:**
- {Feature from actual workflow}
- {Feature from actual workflow}

---

## Architecture

### Project Structure
{Actual directory tree from codebase}

### Configuration
**Databases:**
{Table with database names and purposes}

**Watermark Table:**
{inc_log table structure and purpose}

---

## Processing Patterns

### Pattern 1: Incremental Load (Watermark-Based)
{Explain watermark tracking using inc_log}

**SQL Pattern:**
{Real SQL showing UNION ALL with watermark logic}

### Pattern 2: Full Load (Complete Reload)
{Explain full reload pattern}

**SQL Pattern:**
{Real SQL showing full reload}

---

## Watermark Management

**inc_log Table:**
{Schema and purpose}

**Watermark Update Logic:**
{Explain how watermarks are updated}

---

## Main Workflow Configuration

**Workflow File:** {hist_union_runner.dig}

**Key Features:**
- {Feature from actual .dig file}
- {Feature from actual .dig file}

**Parallel Execution:**
{Explain _parallel settings}

---

## SQL Query Examples

### Example 1: Incremental Load Pattern
{Real SQL from codebase}

### Example 2: Full Load Pattern
{Real SQL from codebase}

### Example 3: Complex Schema
{Real SQL from codebase if applicable}

---

## Tables Processed

{Table organized by data source listing all tables}

---

## Execution Flow

{Step-by-step workflow execution}

**Execution Commands:**
{Real commands from codebase}

---

## Best Practices

{List from actual implementation}

---

## Troubleshooting

**Common Issues:**
{Real issues and solutions}

**Monitoring Queries:**
{Real SQL for checking status}

---

## Maintenance

{Maintenance tasks and schedules}

---

## Summary

{Brief recap of capabilities}
```

---

**Template Usage Notes:**
- Read actual workflows (.dig), SQL files, inc_log table schema
- Extract REAL watermark logic and UNION patterns
- Document REAL table names and processing patterns
- Use actual directory structure from codebase
- Include working SQL examples
- NO placeholders - only real extracted data

## Summary

This skill generates production-ready hist-union documentation by:
- Reading actual .dig workflows and .sql files from codebase
- Following the exact template structure shown above
- Extracting real watermark logic, UNION patterns, and table configurations
- Creating comprehensive documentation with working SQL examples

**Key capability:** Transforms hist-union codebase into professional Confluence documentation with all processing patterns documented.
