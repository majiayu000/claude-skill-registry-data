---
name: grist-reference
description: Grist API reference documentation for the grist-mcp-server project. Use when implementing or modifying Grist MCP tools, working with Grist cell values, UserActions, column types, widget options, database schema, or pages/widgets. This skill provides authoritative API specifications.
---

# Grist API Reference

This skill provides comprehensive Grist API documentation for developing the grist-mcp-server.

## Quick Reference

| Task | Reference File |
|------|----------------|
| REST API endpoints | `grist-api.yml` |
| TypeScript types, CellValue encoding | `grist-api.d.ts` |
| Metadata tables, column definitions | `grist-database-schema.md` |
| Pages, widgets, layouts, linking | `grist-pages-widgets.md` |
| Apply endpoint, response verification | `grist-apply-endpoint.md` |

## Reference Files

### grist-api.yml (~2100 lines)
OpenAPI 3.0 specification for the Grist REST API.

**Grep patterns:**
- `paths:` - API endpoints
- `components/schemas` - Data schemas
- `CellValue` - Cell value encoding
- `UserAction` - User action format

**Use for:** Endpoint parameters, request/response schemas, authentication

### grist-api.d.ts (~2030 lines)
Complete TypeScript type definitions for Grist API.

**Grep patterns:**
- `type.*Value` - Cell value types (RefValue, DateValue, etc.)
- `interface.*Options` - Widget options interfaces
- `UserAction` - UserAction type definitions
- `GristObjCode` - Encoding codes (L, D, R, etc.)
- `PERMISSION` - Permission system reference

**Use for:** Type definitions, cell value encoding, widget options format

### grist-database-schema.md (~573 lines)
Grist metadata tables and database structure.

**Key sections:**
- `_grist_Tables` - Table definitions
- `_grist_Tables_column` - Column schema
- `_grist_Views_section` - Widget definitions
- `_grist_ACLRules` - Access control

**Use for:** Understanding metadata structure, foreign key relationships

### grist-pages-widgets.md (~658 lines)
Practical guide for pages (views) and widgets (view sections).

**Key sections:**
- `CreateViewSection` - Widget creation action
- `Layout Structure` - layoutSpec JSON format
- `Widget Linking` - linkSrcSectionRef, linkSrcColRef
- `Sorting` - sortColRefs format
- `Filtering` - _grist_Filters table

**Use for:** Page/widget creation, layout configuration, widget linking

### grist-apply-endpoint.md (~490 lines)
Guide for verifying actions via `/apply` endpoint.

**Key sections:**
- `ApplyUAResult` - Response structure
- `retValues` - Return value verification
- `Error Handling` - Error response formats
- `Best Practices` - Safe access patterns

**Use for:** Validating action results, error handling patterns

## Common Tasks

**Implementing a new tool:**
1. Load `grist-api.yml` for endpoint schema
2. Load `grist-api.d.ts` for TypeScript types

**Working with cell values:**
1. Load `grist-api.d.ts` - search for `GristObjCode` and `CellValue`

**Creating pages/widgets:**
1. Load `grist-pages-widgets.md` for CreateViewSection and layout format

**Understanding metadata tables:**
1. Load `grist-database-schema.md` for table schemas

**Handling apply endpoint responses:**
1. Load `grist-apply-endpoint.md` for response verification
