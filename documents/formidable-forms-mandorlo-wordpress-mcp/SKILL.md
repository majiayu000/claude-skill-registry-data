---
name: formidable-forms
description: Manage Formidable Forms via REST API and WP-CLI. List forms, get form details and fields, retrieve entries. Use when working with Formidable Forms or Formidable Forms Pro WordPress plugin.
---

# Formidable Forms

This skill enables management of Formidable Forms on WordPress sites.

## Overview

Formidable Forms is a popular WordPress form builder plugin. This skill provides capabilities to:

- List all forms on a site
- Get detailed form information including all fields
- Retrieve form entries/submissions
- Analyze form structure

## Prerequisites

The target WordPress site must have:

1. **Formidable Forms plugin** (free version or Pro)
2. **For REST API scripts**: Formidable API add-on (paid) with an API key configured

## Available Scripts

### list-forms

List all forms on the WordPress site.

**Method**: Uses `wp eval` to query Formidable's PHP API directly (no API add-on required).

**Output**: JSON array of forms with id, form_key, name, description, and status.

### get-form

Get detailed information about a specific form including all its fields.

**Parameters**:
- `formId` (required): The form ID or form key

**Output**: Form details plus array of all fields with their configuration.

### get-entries

Retrieve entries/submissions for a form.

**Parameters**:
- `formId` (required): The form ID
- `limit` (optional): Number of entries to retrieve (default: 25)
- `page` (optional): Page number for pagination (default: 1)

**Output**: Array of form entries with field values.

## How It Works

These scripts use `wp eval` to execute PHP code directly on the WordPress server via WP-CLI. This approach:

- Works without the paid Formidable API add-on
- Accesses Formidable's internal PHP classes (`FrmForm`, `FrmField`, `FrmEntry`)
- Returns JSON-formatted data

## Common Workflows

### Analyze form structure

1. Call `list-forms` to see all forms on the site
2. Call `get-form` with the desired form ID to see all fields and their configuration
3. Use field information to understand form structure

### Export form data

1. Call `get-entries` to retrieve submissions
2. Use pagination parameters for large datasets
3. Process the JSON response as needed

### Troubleshoot form issues

1. Call `get-form` to inspect field settings
2. Check field types, required status, and validation rules
3. Review conditional logic if configured

## API Reference

For detailed REST API documentation (if using the paid API add-on):
https://strategy11.github.io/formidable-forms-rest-api-docs/

## Field Types

Common Formidable Forms field types you may encounter:

| Type | Description |
|------|-------------|
| `text` | Single line text input |
| `textarea` | Multi-line text area |
| `email` | Email address field |
| `phone` | Phone number field |
| `select` | Dropdown select |
| `radio` | Radio buttons |
| `checkbox` | Checkboxes |
| `number` | Number input |
| `date` | Date picker |
| `time` | Time picker |
| `file` | File upload |
| `hidden` | Hidden field |
| `html` | HTML content block |
| `divider` | Section divider |
