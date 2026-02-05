---
name: Craft CMS Skills
description: Complete skill suite for managing Craft CMS content including sections, entry types, fields, entries, drafts, field layouts, and sites.
---

## Important: Use this plugin, Not YAML Files

**CRITICAL**: Always use this HTTP API to manage Craft CMS content. Never directly modify YAML configuration files in the `config/project/` directory. The API ensures proper validation, maintains data integrity, and handles all necessary relationships automatically. Direct YAML edits can corrupt your Craft installation.

**CRITICAL**: The `skills` plugin must be installed to Craft. You can verify installation by running `php craft plugin/list` and install it with `php craft plugin/install skills`

## Base URL Configuration

All API routes require a base URL and API prefix. The standard Craft CMS configuration uses the `PRIMARY_SITE_URL` environment variable and a configurable API prefix:

- **Environment Variable**: Check for `PRIMARY_SITE_URL` in ENV or `.env` file
- **If Not Set**: Ask the user for the base URL to use
- **API Prefix**: Configurable prefix that defaults to `/api`
  - **Check Order**:
    1. First check `config/skills.php` for `apiPrefix` in the PHP array
    2. If not found, try the default `/api`
    3. If requests fail, ask the user for the configured API prefix
- **Route Format**: `{PRIMARY_SITE_URL}/{apiPrefix}/{endpoint}`
- **Default Example**: `https://craft-site.com/api/sections`
- **Custom Prefix Example**: `https://craft-site.com/custom-api/sections`

## Request/Response Format

All API endpoints:
- **Return JSON**: All responses are in JSON format with structured data
- **Accept Header**: Include `Accept: application/json` header in requests to ensure errors are also formatted as JSON for better error handling and debugging
- **Content-Type**: Use `Content-Type: application/json` for POST/PUT requests with JSON body data

## Content
- [create_entry](create_entry.md) - `POST /api/entries` - Create entries with section/entry type IDs and field data
- [get_entry](get_entry.md) - `GET /api/entries/<id>` - Retrieve entry by ID with all fields and metadata
- [update_entry](update_entry.md) - `PUT /api/entries/<id>` - Update entry (prefers draft workflow)
- [delete_entry](delete_entry.md) - `DELETE /api/entries/<id>` - Delete entry (soft/permanent)
- [search_content](search_content.md) - `GET /api/entries/search` - Search/filter entries by section/status/query

## Drafts
- [create_draft](create_draft.md) - `POST /api/drafts` - Create draft from scratch or existing entry
- [update_draft](update_draft.md) - `PUT /api/drafts/<id>` - Update draft content/metadata (PATCH semantics)
- [apply_draft](apply_draft.md) - `POST /api/drafts/<id>/apply` - Publish draft to canonical entry

## Sections
- [create_section](create_section.md) - `POST /api/sections` - Create section with types/versioning/sites
- [get_sections](get_sections.md) - `GET /api/sections` - List all or filter by IDs
- [update_section](update_section.md) - `PUT /api/sections/<id>` - Update properties/settings
- [delete_section](delete_section.md) - `DELETE /api/sections/<id>` - Permanently delete (removes all entries)

## Entry Types
- [create_entry_type](create_entry_type.md) - `POST /api/entry-types` - Create with handle/name/layout
- [get_entry_types](get_entry_types.md) - `GET /api/entry-types` - List with fields/usage/URLs
- [update_entry_type](update_entry_type.md) - `PUT /api/entry-types/<id>` - Update properties/layout
- [delete_entry_type](delete_entry_type.md) - `DELETE /api/entry-types/<id>` - Delete if not in use

## Fields
- [create_field](create_field.md) - `POST /api/fields` - Create with type and settings
- [get_fields](get_fields.md) - `GET /api/fields` - List global or layout-specific
- [get_field_types](get_field_types.md) - `GET /api/fields/types` - List available types
- [update_field](update_field.md) - `PUT /api/fields/<id>` - Update properties/settings
- [delete_field](delete_field.md) - `DELETE /api/fields/<id>` - Permanently delete (removes data)

## Field Layouts
- [create_field_layout](create_field_layout.md) - `POST /api/field-layouts` - Create empty field layout for entry types
- [get_field_layout](get_field_layout.md) - `GET /api/field-layouts` - Get field layout structure by entry type/layout/element ID
- [add_tab_to_field_layout](add_tab_to_field_layout.md) - `POST /api/field-layouts/<id>/tabs` - Add tab to field layout with flexible positioning (prepend/append/before/after)
- [add_field_to_field_layout](add_field_to_field_layout.md) - `POST /api/field-layouts/<id>/fields` - Add custom field to tab with positioning, width, required, and display options
- [add_ui_element_to_field_layout](add_ui_element_to_field_layout.md) - `POST /api/field-layouts/<id>/ui-elements` - Add UI elements (heading, tip, horizontal rule, markdown, template) to layouts
- [move_element_in_field_layout](move_element_in_field_layout.md) - `PUT /api/field-layouts/<id>/elements` - Move fields/UI elements within or between tabs with precise positioning
- [remove_element_from_field_layout](remove_element_from_field_layout.md) - `DELETE /api/field-layouts/<id>/elements` - Remove fields or UI elements from field layout

## Sites
- [get_sites](get_sites.md) - `GET /api/sites` - List all sites with IDs/handles/URLs

## Assets
- [create_asset](create_asset.md) - `POST /api/assets` - Upload file from local/remote URL to volume
- [update_asset](update_asset.md) - `PUT /api/assets/<id>` - Update metadata or replace file
- [delete_asset](delete_asset.md) - `DELETE /api/assets/<id>` - Delete asset and file
- [get_volumes](get_volumes.md) - `GET /api/volumes` - List asset volumes with IDs/URLs

## System
- [health](health.md) - `GET /api/health` - Health check endpoint to verify plugin installation and API availability
