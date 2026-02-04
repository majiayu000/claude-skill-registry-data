---
name: data-analytics-foundations
description: Core data analytics concepts, Excel/Google Sheets fundamentals, and data collection techniques
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 01-data-analytics-foundations
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  skill_level:
    type: string
    required: true
    enum: [beginner, intermediate, advanced]
    default: beginner
  focus_area:
    type: string
    required: false
    enum: [excel, sheets, data_quality, collection, all]
    default: all

# Observability
observability:
  logging_level: info
  metrics: [usage_count, success_rate, completion_time]
---

# Data Analytics Foundations Skill

## Overview
Master the foundational concepts of data analytics including data types, collection methods, spreadsheet fundamentals, and basic data manipulation techniques.

## Core Topics

### Data Fundamentals
- Understanding data types (quantitative, qualitative, structured, unstructured)
- Data sources and collection methods
- Data quality dimensions (accuracy, completeness, consistency, timeliness)

### Spreadsheet Proficiency
- Excel fundamentals and advanced formulas
- Google Sheets collaboration features
- Data cleaning and transformation in spreadsheets
- Pivot tables and data summarization

### Data Collection
- Survey design and implementation
- Web scraping basics
- API data extraction
- Database querying fundamentals

## Learning Objectives
- Understand core data analytics terminology and concepts
- Master Excel and Google Sheets for data analysis
- Implement effective data collection strategies
- Apply data quality assessment techniques

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Formula error | Invalid syntax | Validate formula structure |
| Data type mismatch | Wrong input format | Convert data types explicitly |
| Missing data | Incomplete dataset | Apply imputation or filtering |
| Performance issue | Large dataset | Use data sampling or optimization |

## Related Skills
- databases-sql (for advanced data querying)
- statistics (for data analysis techniques)
- visualization (for presenting insights)
