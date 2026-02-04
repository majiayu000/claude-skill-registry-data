---
name: logseq-db-knowledge
description: Essential knowledge about Logseq DB (database) graphs. Use this skill when working with Logseq DB to ensure accurate understanding of nodes, properties, tags, tasks, and queries. This corrects common misconceptions from file-based Logseq that do NOT apply to DB graphs.
---

# Logseq DB Knowledge Base

## Overview

This skill provides comprehensive knowledge about Logseq DB (database) graphs, which use a fundamentally different data model from the older file-based (markdown) version of Logseq.

**CRITICAL**: When the user is working with Logseq DB graphs, the traditional file-based Logseq knowledge does NOT apply. Always reference this skill to ensure accuracy.

**Keywords**: logseq database, logseq db, db graphs, nodes, new tags, supertags, classes, tag properties, logseq properties, datalog queries

## Core Concepts

### Nodes - The Foundation

In Logseq DB, **nodes** are the fundamental building block. Both pages and blocks are now called "nodes" because they behave similarly.

**Key Node Behaviors:**
- Nodes are referenced using `[[]]` syntax (same as before)
- All nodes can have properties, tags, and references
- Blocks can be converted to pages by tagging with `#Page`
- Nodes are collapsible with an arrow on the left (appears on hover)
- Nodes can be favorited, embedded, and have linked/unlinked references
- Nodes share the same keybindings for properties and editing

**Pages vs Blocks:**
- **Pages**: Have unique names by tag (e.g., `Apple #Company` and `Apple #Fruit` can coexist)
- **Blocks**: Created within pages; tagged blocks don't require unique names
- **Conversion**: Top-level blocks can become pages by adding `#Page` tag

**Example:**
```
Aug 29th, 2025
  My meeting notes #Page
```
This converts the block "My meeting notes" into a namespaced page under "Aug 29th, 2025"

### New Tags (Classes/Types/Supertags)

**CRITICAL DISTINCTION**: In Logseq DB, "new tags" are NOT the same as file-based tags!

**New tags** (also called classes, types, or supertags) are created with `#NAME` syntax and serve as templates for nodes.

**Creating New Tags:**
```
1. Open Search and type #Person
2. A dialog appears to configure tag properties
3. Add properties like "lastName" and "birthday"
4. Now any node tagged with #Person inherits these properties
```

**Tag Features:**
- Tags can have **parent tags** via the `Extends` property
- Tags inherit properties from all parent tags
- Tags can have their own properties on the tag page
- Tag properties automatically appear on all tagged nodes

**Parent Tag Example:**
```
#Book (has property: author)
  └─ #AudioBook (has property: narrator)
     └─ Inherits: author, narrator

#MediaObject (has property: duration)
  └─ #AudioBook
     └─ Inherits: author, narrator, duration
```

### Properties System

Properties in Logseq DB are powerful and type-safe.

**Property Types:**
1. **Text**: Default type, allows any text, behaves like a block
2. **Number**: Actual numbers (not strings), sorts correctly
3. **Date**: Date picker, links to journal pages, supports repetition
4. **DateTime**: Date + time picker, supports repetition
5. **Checkbox**: Boolean values (checked/unchecked)
6. **Url**: Only allows valid URLs
7. **Node**: Links to other nodes, can be restricted by tag

**Key Property Features:**
- **Default Values**: Properties can have defaults
- **Multiple Values**: Properties can hold multiple values (except checkbox/datetime)
- **Property Choices**: Limit property to specific choices (like enums)
- **UI Position**: Control where property displays (inline, below, beginning, end)
- **Hide by Default**: Hide properties unless zoomed in
- **Tag Properties**: Properties inherited by all nodes with that tag

**Property Shortcuts:**
- `Cmd-p` (or `Ctrl-Alt-p`): Add property to current node
- `Cmd-j`: Quick edit properties
- `p a`: Toggle display all properties
- `p t`: Add/remove tags
- `p i`: Set icon
- `p s`: Set Status (tasks)
- `p p`: Set Priority (tasks)
- `p d`: Set Deadline (tasks)

**Configuring Properties:**
- Click property name for dropdown menu
- `Cmd-click` to navigate to property page
- Configure: type, default value, choices, UI position, multiple values, hide settings

## Tasks in Logseq DB

**CRITICAL**: Tasks work completely differently in Logseq DB!

### Old Way (File-based Logseq) - DOES NOT WORK IN DB:
```
- TODO This is a task
- DOING Working on this
- DONE Completed
```

### New Way (Logseq DB):
```
Tasks are blocks tagged with #Task
Status is a PROPERTY with these values:
- Backlog
- Todo
- Doing
- In Review
- Done
- Canceled
```

**Creating Tasks:**
1. Type `/todo` in a block (adds Status property + #Task tag)
2. Type text and end with `#Task`
3. Add `Deadline` or `Scheduled` property
4. Use `Cmd-Enter` to cycle through Todo → Doing → Done

**Task Properties:**
- **Status**: Property with choices (not a marker!)
- **Priority**: A, B, C priorities
- **Deadline**: Date property
- **Scheduled**: Date property

**Querying Tasks:**

❌ **WRONG (File-based approach):**
```clojure
[:find (pull ?b [*])
 :where [?b :block/marker "DOING"]]
```

✅ **CORRECT (DB approach):**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "Task"]
         [?b :logseq.property/status ?s]
         [?s :block/title "Doing"]]}
```

**Customizing Tasks:**
1. Customize `Status` property choices on the Status page
2. Add custom properties to `#Task` tag
3. Create custom task types by extending `#Task`:
   - Example: `#ProjectTask` extends `#Task` + adds "project" property

### Repeated Tasks

Repeated tasks work with `Deadline` or `Scheduled` properties:

1. Set Deadline/Scheduled on a task
2. In the popup, check "Repeat task"
3. Configure interval (Day, Week, Month, Year)
4. When Status changes to Done:
   - Status resets to Todo
   - Deadline/Scheduled advances by the interval

## Tag-Based Features

Logseq DB uses new tags to power core features. Each has a built-in table for management.

### Built-in Tags:
- **#Journal**: Daily journal pages
- **#Task**: Task management (see above)
- **#Query**: Simple and advanced queries
- **#Card**: Flashcards using spaced repetition
- **#Asset**: Files (images, PDFs, etc.)
- **#Template**: Reusable block templates
- **#Code**: Code blocks
- **#Quote**: Quote blocks
- **#Math**: LaTeX math blocks
- **#PDF Annotation**: PDF highlights and annotations

**All these tags can be extended** by adding custom properties on their tag pages!

### Journals (#Journal)

- Automatically created for current day
- Reference with natural language: `[[Today]]`, `[[Next Friday]]`, `[[Last Monday]]`
- Use `/Date picker` command for specific dates
- Navigate: `g n` (next day), `g p` (previous day)

### Queries (#Query)

- Create with `/Query` command (query builder)
- Advanced queries: `/Advanced Query` command
- All queries tagged with `#Query`
- View all queries on `#Query` page table

### Cards (#Card)

- Tag blocks with `#Card` to create flashcards
- Uses new spaced repetition algorithm
- Review in "Flashcards" section (left sidebar)
- 4 rating levels for scheduling
- `Due` property shows next review date

### Assets (#Asset)

- Drag and drop files onto blocks
- Batch upload from `#Asset` page
- Stored in graph's `assets/` directory
- Gallery View available for visual assets

### Templates (#Template)

- Create: Tag a block with `#Template`, add children
- Insert: Use `/Template` command
- **Auto-apply**: Use `Apply template to tags` property to auto-insert on tagged nodes
  - Example: Apply template to `#Journal` → appears on every journal page

## Querying Logseq DB

### Common DB Attributes

**IMPORTANT**: These are DB-specific attributes, different from file-based Logseq!

**Node Attributes:**
- `:block/title` - Node title (pages and named blocks)
- `:block/content` - Block text content
- `:block/properties` - Node properties (different structure than file-based)
- `:block/tags` - New tags assigned to node
- `:block/refs` - References to other nodes
- `:block/uuid` - Unique identifier
- `:block/created-at` - Creation timestamp
- `:block/updated-at` - Last update timestamp
- `:db/id` - Database entity ID
- `:db/ident` - Database identifier (e.g., `:logseq.class/Task`)

**Property Attributes:**
- `:logseq.property/status` - Status property
- `:logseq.property/priority` - Priority property
- `:logseq.property/deadline` - Deadline property
- Custom properties: `:logseq.property/YOUR-PROPERTY-NAME`

**Tag Attributes:**
- `:logseq.class/Task` - Task tag (built-in)
- `:logseq.class/Journal` - Journal tag (built-in)
- `:logseq.class/Query` - Query tag (built-in)
- `:logseq.class/Card` - Card tag (built-in)

### Tag Matching: Built-in vs Custom Tags

**CRITICAL: This is the most common source of query errors!**

There are TWO ways to match tags in queries, and choosing the wrong one will cause your query to fail:

#### Method 1: Using `:db/ident` (Built-in tags ONLY)
```clojure
[?b :block/tags ?t]
[?t :db/ident :logseq.class/Task]
```

**Only works for built-in Logseq tags:**
- `:logseq.class/Task`
- `:logseq.class/Journal`
- `:logseq.class/Query`
- `:logseq.class/Card`
- `:logseq.class/Asset`
- `:logseq.class/Template`
- `:logseq.class/Page`

#### Method 2: Using `:block/title` (UNIVERSAL - works for ALL tags)
```clojure
[?b :block/tags ?t]
[?t :block/title "Task"]
```

**Works for both built-in AND custom user-created tags:**
- Built-in: `"Task"`, `"Journal"`, `"Query"`, `"Card"`, etc.
- Custom: `"zotero"`, `"Person"`, `"Project"`, `"Meeting"`, etc.

#### Best Practice: Use `:block/title` by default

**RECOMMENDATION**: Always use `:block/title` unless you have a specific reason to use `:db/ident`.

Why?
- ✅ Works universally for all tags (built-in and custom)
- ✅ More intuitive (matches the visible tag name)
- ✅ Easier to remember
- ✅ Prevents common query errors

#### Example: Mixing Built-in and Custom Tags

```clojure
{:query [:find (pull ?b [*])
         :where
         ;; Find tasks (built-in tag)
         [?b :block/tags ?task-tag]
         [?task-tag :block/title "Task"]
         [?b :logseq.property/status ?status]
         [?status :block/title "Done"]

         ;; That reference pages with custom tag
         [?b :block/refs ?ref]
         [?ref :block/tags ?custom-tag]
         [?custom-tag :block/title "zotero"]]}
```

This query finds all Done tasks that reference pages tagged with `#zotero`.

### Query Examples

**CRITICAL: ALL queries in Logseq DB blocks MUST use this exact format:**

**Find all nodes with a specific tag:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "Task"]]}
```

**Find tasks with specific status:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "Task"]
         [?b :logseq.property/status ?s]
         [?s :block/title "Doing"]]}
```

**Find nodes by property value:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :logseq.property/author ?author]
         [?author :block/title "John Doe"]]}
```

**Find all journals:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "Journal"]]}
```

**Find nodes by text content:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/content ?content]
         [(clojure.string/includes? ?content "history")]]}
```

### Query Syntax in Logseq DB

**CRITICAL FORMAT RULE:**

Every advanced query in Logseq DB MUST start with `{:query` and end with `}`.

**Correct format:**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "Task"]
         [?b :logseq.property/status ?s]
         [?s :block/title "Doing"]]}
```

**Common mistakes - DON'T DO THESE:**
```clojure
; ❌ WRONG - Extra {{query}} wrapper (this is old syntax)
{{query
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]]}
}}

; ❌ WRONG - Missing {:query ...} wrapper entirely
[:find (pull ?b [*])
 :where
 [?b :block/tags ?t]
 [?t :block/title "Task"]]

; ❌ WRONG - Using :db/ident for custom user tags
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :db/ident :logseq.class/zotero]]}  ; zotero is a custom tag!

; ✅ CORRECT - Use :block/title for custom tags
{:query [:find (pull ?b [*])
         :where
         [?b :block/tags ?t]
         [?t :block/title "zotero"]]}
```

**Example: Find blocks referencing "Alice":**
```clojure
{:query [:find (pull ?b [*])
         :where
         [?person :block/title "Alice"]
         [?b :block/refs ?person]]}
```

### Query Builder (Recommended)

Instead of writing raw queries, use Logseq DB's Query Builder:
1. Type `/Query` command in a block
2. Use the visual interface to build queries
3. Select tag (e.g., #Task)
4. Add property filters (e.g., Status = "Doing")
5. Logseq generates the correct query syntax automatically

See `references/query-examples.md` for more examples.

## Views and Tables

Logseq DB provides powerful table views for managing tagged nodes.

**Table Features:**
- Built-in tables on all tag pages
- Sortable columns (by any property)
- Filterable rows
- Create new nodes directly in table
- Bulk actions on selected rows
- Multiple view types: Table, Gallery (for assets)

**Accessing Tables:**
1. Navigate to any tag page (e.g., `#Task`, `#Journal`)
2. See "Tagged Nodes" section with table
3. Click `+` to create new tagged node
4. Select multiple rows for bulk actions

## Common Misconceptions

When working with Logseq DB, avoid these file-based assumptions:

❌ **WRONG**: Tasks use TODO/DOING/DONE markers
✅ **CORRECT**: Tasks use #Task tag + Status property

❌ **WRONG**: Query tasks with `:block/marker`
✅ **CORRECT**: Query tasks with tag matching and `:logseq.property/status`

❌ **WRONG**: Use `:db/ident` for custom user tags
✅ **CORRECT**: Use `:block/title` for all tags (works for both built-in and custom)

❌ **WRONG**: Tags are just hashtags for organization
✅ **CORRECT**: New tags are classes that define properties and behavior

❌ **WRONG**: Properties are frontmatter in markdown files
✅ **CORRECT**: Properties are structured, typed data in the database

❌ **WRONG**: Pages and blocks are fundamentally different
✅ **CORRECT**: Pages and blocks are both nodes with similar behavior

❌ **WRONG**: Can't have duplicate page names
✅ **CORRECT**: Pages are unique by tag: `Apple #Company` ≠ `Apple #Fruit`

## Best Practices

### 1. Use New Tags for Structure
Create tags for your domain (e.g., `#Person`, `#Project`, `#Meeting`) and define their properties once. All tagged nodes inherit the structure.

### 2. Leverage Property Types
Use the right property type:
- `Number` for quantities (sorts correctly)
- `Date` for dates (links to journals, enables repetition)
- `Node` for relationships (type-safe references)

### 3. Extend Built-in Tags
Add custom properties to `#Task`, `#Journal`, etc. to customize for your workflow.

### 4. Use Templates for Automation
Set templates to auto-apply to tags for consistent structure.

### 5. Query by Tag First
Always start queries by filtering to a tag, then add property filters:
```clojure
[?b :block/tags ?t]
[?t :block/title "YourTagName"]
```

Use `:block/title` for universal compatibility with both built-in and custom tags.

### 6. Use Tables for Bulk Management
Navigate to tag pages and use tables for sorting, filtering, and bulk operations.

## Migration from File-based Logseq

If converting from file-based Logseq:

1. **Tasks**: Use DB Graph Importer in Logseq to convert TODO markers to #Task tags
2. **Tags**: File-based `#tags` become inline tags; evaluate if they should be new tags
3. **Properties**: Markdown frontmatter converts to database properties
4. **Queries**: Rewrite queries using DB attributes (see query examples)

**Important**: Test the importer on a copy of your graph first!

## Additional Resources

For comprehensive information, refer to:
- `references/data-model.md` - Detailed DB schema and data model
- `references/query-examples.md` - Complete query cookbook
- `references/db-vs-file.md` - Side-by-side comparison guide
- Official docs: https://docs.logseq.com (DB graph sections)

## When to Use This Skill

Invoke this skill whenever:
- User mentions Logseq DB or database graphs
- Working with Logseq queries and results don't match expectations
- User asks about tasks, properties, or tags in Logseq
- Debugging Logseq CLI or API queries
- Converting from file-based to DB graphs
- Creating custom workflows with new tags

**Proactive Use**: If you notice file-based Logseq assumptions in your responses, automatically reference this skill to correct them.
