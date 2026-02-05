---
name: query-schema
description: Query game configuration table schemas and analyze table relationships using HTTP API and CFG syntax. This skill should be used when Claude needs to understand table structures for game development, query configuration data, or analyze foreign key relationships between tables.
---

# Query Schema Skill

## Overview

Query game configuration table schemas through HTTP API endpoints to understand table structures, field definitions, and foreign key relationships. Parse CFG syntax to analyze table dependencies and provide comprehensive schema understanding.

## Quick Start

Query a table schema by:
1. Identifying target table name from user request
2. Calling API endpoint: `http://localhost/cfgserver/query_table?table_name=$tablename`
3. Extracting `schema` field from JSON response
4. Interpreting CFG syntax to understand table structure

## Core Capabilities

### Table Schema Query
- Query individual table schemas to understand structure and field definitions
- Identify primary keys and field constraints
- Analyze foreign key relationships and table dependencies

### Multi-Table Analysis
- Query multiple tables simultaneously to map cross-table relationships
- Understand dependency chains and schema consistency
- Provide comprehensive view of interconnected table structures

### CFG Syntax Interpretation
- Parse table, struct, and interface definitions in CFG syntax
- Understand field types including containers like `list<type>`
- Analyze foreign key relationships using `->foreign_table` syntax
- Interpret comments and documentation for field usage

## Trigger Scenarios

Activate this skill when encountering:
- User requests about table structures ("请告诉我道具表的结构")
- Game development tasks requiring configuration understanding
- Feature implementation needing table relationship analysis
- Configuration data queries requiring schema comprehension
- Table operation requests ("帮我配置一个新道具")

## Workflow

### Single Table Query
1. Identify target table name from user request or context
2. Construct API URL: `http://localhost/cfgserver/query_table?table_name=$tablename`
3. Send GET request to API endpoint
4. Validate response by checking `result` field
5. Extract and interpret CFG syntax from `schema` field
6. Provide analysis of table structure, fields, and relationships

### Multi-Table Query
1. Identify related tables with dependencies
2. Construct API URL with comma-separated table names
3. Send GET request to multi-table endpoint
4. Map foreign key dependencies between tables
5. Provide comprehensive view of interconnected structures

## Error Handling

- Handle table not found by checking name spelling and existence
- Verify host connectivity and service availability for network issues
- Ensure proper URL construction and parameter format
- Refer to CFG syntax guide for parse errors

## Resources

### references/
- **api_guide.md**: API endpoints, parameters, and usage examples
- **cfg_syntax.md**: CFG syntax parsing and relationship analysis

Load references when:
- Requiring detailed API specifications
- Needing in-depth CFG syntax understanding
- Analyzing complex table relationships
- Troubleshooting query issues
