---
name: generate-bruno-files
description: Create Bruno .bru request files for API endpoints found in the project source code. Use when the user asks to generate Bruno API files from source code, mentions the Bruno API client, or wants to scaffold .bru files for HTTP requests.
user-invocable: true
allowed-tools: Bash(ls *), Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "source file path or description of which API calls to generate .bru files for"
---

Create Bruno .bru request files for API endpoints found in the project source code.

Input: $ARGUMENTS (a source file path or description of which API calls to generate .bru files for)

# Context

This project uses Bruno (open-source API client) with a collection in `.bruno/`.
The collection config is `.bruno/bruno.json` and shared variables live in `.bruno/collection.bru` (gitignored; template at `.bruno/collection.example.bru`).

# Instructions

## Step 1: Identify API calls

Read the source file specified in $ARGUMENTS. Extract every HTTP request:
- Method (GET, POST, PUT, PATCH, DELETE)
- URL / endpoint path
- Headers (auth, content-type, custom headers)
- Query parameters
- Request body (if any)

If $ARGUMENTS is empty or unclear, use AskUserQuestion to ask which file or endpoints to generate .bru files for.

## Step 2: Check existing .bru files

List existing request files in `.bruno/` to avoid duplicates:

```bash
ls .bruno/*.bru
```

If a .bru file already covers the same endpoint, skip it and inform the user.

## Step 3: Review collection variables

Read `.bruno/collection.example.bru` to see which variables are already defined. If the new requests need variables not yet in the collection, note them for Step 5.

## Step 4: Create .bru files

For each unique API endpoint, create a `.bru` file in `.bruno/` following these conventions:

### Naming
- Use kebab-case: `verb-resource.bru` (e.g., `list-users.bru`, `create-order.bru`, `get-item-by-id.bru`)
- Name should reflect the action, not the URL path

### File format

```bru
meta {
  name: <kebab-case-name>
  type: http
  seq: <next-available-sequence-number>
}

<method> {
  url: <url-with-{{variables}}-for-dynamic-segments>
  body: <none|json|form|xml>
  auth: <none|bearer|basic>
}

auth:bearer {
  token: {{token_variable}}
}

headers {
  X-Custom-Header: value
}

body:json {
  {
    "field": "value"
  }
}
```

### Rules
- Use `{{variable_name}}` for dynamic URL segments, tokens, IDs — never hardcode secrets or IDs
- Include `auth:bearer` block when the API uses bearer token auth
- Include `headers` block only for non-standard headers (not Content-Type for JSON — Bruno handles that)
- Include `body:json` block for POST/PUT/PATCH with a realistic example body matching the source code's payload structure
- Set `seq` to continue from the highest existing sequence number

## Step 5: Update collection variables (if needed)

If new variables are required (e.g., a new `api_key`, `user_id`, etc.):

1. Read the current `.bruno/collection.example.bru`
2. Add the new variables with empty values to the `vars:pre-request` block
3. Inform the user to also update their local `.bruno/collection.bru` with the new variables

## Step 6: Summary

Display a table of created files:

| File | Method | Endpoint | Source |
|------|--------|----------|--------|
| `name.bru` | GET | `/path` | `file.py:line` |

If any variables were added, list them and remind the user to fill values in `collection.bru`.
