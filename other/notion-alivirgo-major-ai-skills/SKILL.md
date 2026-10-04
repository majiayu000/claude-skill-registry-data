---
name: notion
description: "Create and update Notion pages, blocks, database entries, and property schemas through its API."
category: knowledge
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["notion", "notion-api", "databases", "blocks", "integrations", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Notion Workspace & API AI Skill Guide (Claude)

## Overview & Engine Architecture
Notion is a cloud workspace of **pages**, **databases**, and **blocks**. Programmatic control uses the **Notion API** (REST) with integration tokens, page parentage, and typed **database properties**. Claude operates as a Principal Knowledge Ops Engineer, specializing in **database schema design**, **idempotent upserts**, **block append pipelines**, and **permission-aware integrations**.

### Notion Object & API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Notion Architecture                         │
│                                                             │
│  Content Model                                              │
│  ├── Workspace / Pages / Child pages                        │
│  ├── Databases (properties + rows as pages)                 │
│  └── Blocks (paragraph, heading, list, code, ...)           │
│                                                             │
│  API Surface                                                │
│  ├── https://api.notion.com/v1                              │
│  ├── pages / databases / blocks / users / comments          │
│  └── Notion-Version header (pinned API version)             │
│                                                             │
│  Auth & Sharing                                             │
│  ├── Internal integration token                             │
│  ├── Page/database sharing to the integration               │
│  └── Capabilities (read/update/insert)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Share Before Query**: Integrations only see pages/databases explicitly shared with them.
2. **Pin API Version**: Always send `Notion-Version` (e.g. `2022-06-28` or newer pinned version).
3. **Property Types Matter**: Match property payloads to types (`title`, `rich_text`, `select`, `date`, `status`).
4. **Idempotent Writes**: Search by unique property before creating duplicate rows.
5. **Block Limits**: Respect payload size and rate limits; paginate with `start_cursor`.

---

## Production JavaScript: Create Database Row + Append Checklist

```javascript
// ==============================================================================
// Notion API: create a task row and append a to-do block
// npm i @notionhq/client
// ==============================================================================
import { Client } from "@notionhq/client";

const notion = new Client({ auth: process.env.NOTION_TOKEN });
const DATABASE_ID = process.env.NOTION_TASKS_DB;

async function createTask(title, dueISO) {
  const page = await notion.pages.create({
    parent: { database_id: DATABASE_ID },
    properties: {
      Name: {
        title: [{ text: { content: title } }],
      },
      Status: { status: { name: "Not started" } },
      Due: { date: { start: dueISO } },
    },
  });

  await notion.blocks.children.append({
    block_id: page.id,
    children: [
      {
        object: "block",
        type: "to_do",
        to_do: {
          rich_text: [{ type: "text", text: { content: "Define acceptance criteria" } }],
          checked: false,
        },
      },
      {
        object: "block",
        type: "paragraph",
        paragraph: {
          rich_text: [{ type: "text", text: { content: "Created by agent automation." } }],
        },
      },
    ],
  });

  return page.id;
}

createTask("Ship Notion skill docs", "2026-08-30")
  .then((id) => console.log("Created page", id))
  .catch((err) => console.error(err.body || err));
```

Query example:

```javascript
const res = await notion.databases.query({
  database_id: DATABASE_ID,
  filter: { property: "Status", status: { equals: "Not started" } },
  sorts: [{ property: "Due", direction: "ascending" }],
});
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **object_not_found** | DB/page not shared to integration. | Share resource → invite integration. |
| **validation_error on properties** | Wrong property name/type payload. | Fetch database schema; align keys/types. |
| **rate limited** | Burst writes. | Exponential backoff; batch thoughtfully. |
| **Empty title** | Title property not actually named "Name". | Inspect DB; use real title property id/name. |

---

## Best Practices

1. Store database IDs in env vars; never commit tokens.
2. Prefer `status`/`select` options that already exist in the schema.
3. Use rich_text arrays correctly (array of rich text objects, not bare strings).

### Essential References
- API base: `https://api.notion.com/v1`
- SDK: `@notionhq/client`
- Auth: My integrations → Internal integration secret

---

## Agent Operational Directive
> **MANDATORY**: Confirm the integration can access the target page/database before mutating. Pin `Notion-Version`. Match property types exactly; search before create to avoid duplicate rows.
