---
name: drush-webmaster
description: |
  Manage Drupal content, entities, views, menus, fields, and site structure
  using drush webmaster (wm:*) commands. Use when asked to "list content types",
  "find articles by author", "create a new page", "edit node 42", "add a field",
  "build a view", "add a menu link", "translate this",
  "publish this node", "site schema", "search for content",
  "clone this entity", "moderate content", or any Drupal
  entity/content management task.
  Proactively invoke this skill (do NOT attempt raw SQL, drush eval, or direct
  Drupal API calls) when the user wants to query, create, edit, inspect, or
  manage Drupal content, entities, views, menus, blocks, vocabularies, media,
  translations, or site configuration.
---

# Drush Webmaster Commands

The `wm:*` command suite provides YAML-based Drupal site management.
All output is structured YAML. Run `drush wm:<command> --help` for
full documentation on any command before using it.

## Discovery (Start Here)

### `wm:schema:dump`: Full site schema for AI context

**Run this first** when working with an unfamiliar site or section.

```
drush wm:schema:dump
drush wm:schema:dump --section=content-types
drush wm:schema:dump --section=content-types --section=vocabularies
```

Available sections: `content-types`, `vocabularies`, `views`, `menus`,
`blocks`, `media-types`, `entity-types`, `site`

### `wm:site:info`: Site name, slogan, email, paths

```
drush wm:site:info
```

## Before Modifying (Discover First)

Before running any create, edit, or delete operation, run the
appropriate discovery command. This prevents validation errors.

| Operation | Run first |
|-----------|-----------|
| Create entity | `wm:content-type:get <bundle>`: required fields |
| Edit entity | `wm:entity:get <type> <id>`: current values |
| Delete entity | `wm:entity:get <type> <id>`: confirm correct entity |
| Add field to bundle | `wm:field:list <type> <bundle>` then `wm:field:types` |
| Create/edit view | `wm:view:tables` then `wm:view:available:fields` |
| Translate entity | `wm:translation:languages`: see configured languages |
| Moderate entity | `wm:entity:transitions <type> <id>`: transitions |
| Bulk operations | `wm:content-type:get` or `wm:entity:query`: scope |

Skip discovery when context is already known or the user
asks to proceed directly.

## Querying & Inspecting Entities

### `wm:entity:query`: Find entities by field conditions

```
drush wm:entity:query node article \
  --where="status=1" --where="uid=5" \
  --sort=created:DESC
drush wm:entity:query node --where="status=0" --count
drush wm:entity:query node article --where="field_image=NULL" --fields=id,title
drush wm:entity:query node blog --limit=50 --offset=50
```

Where operators: `=`, `!=`, `>`, `<`, `>=`, `<=`,
`=NULL`, `!=NULL`, `=a,b,c` (IN list)

### `wm:entity:get`: Get single entity with field values

```
drush wm:entity:get node 1
drush wm:entity:get node 1 --fields=title,body
```

### `wm:entity:field:get` / `wm:entity:field:set`: Get/set single field value

```
drush wm:entity:field:get node 1 title
drush wm:entity:field:set node 1 title "New Title"
drush wm:entity:field:set node 1 body \
  '{"value":"<p>HTML</p>","format":"full_html"}'
```

### `wm:search`: Full-text search (requires Search module)

```
drush wm:search "contact form"
```

## Creating & Editing Entities (YAML Workflow)

```
drush wm:entity:edit node 5089        # Export to YAML
drush wm:entity:apply node 5089 --dry-run  # Preview changes
drush wm:entity:apply node 5089       # Apply changes

drush wm:entity:new node article      # Create template
drush wm:entity:apply node new        # Create entity

drush wm:entity:bulk-create           # Bulk operations
drush wm:entity:bulk-update
drush wm:entity:bulk-delete

drush wm:entity:clone node 42
drush wm:entity:deep-clone node 42
drush wm:entity:diff node 42 43
drush wm:entity:history node 42
drush wm:entity:revert node 42
```

## Content Types & Fields

```
drush wm:content-type:list
drush wm:content-type:get article
drush wm:content-type:stats
drush wm:content-type:create
drush wm:content-type:update article
drush wm:content-type:delete article

drush wm:field:list node article
drush wm:field:get node article title
drush wm:field:add
drush wm:field:update
drush wm:field:delete
drush wm:field:types
```

## Views

```
drush wm:view:list
drush wm:view:get content
drush wm:view:create
drush wm:view:clone content
drush wm:view:edit blog
drush wm:view:apply blog --dry-run
drush wm:view:apply blog
drush wm:view:preview content
drush wm:view:delete content

drush wm:view:tables
drush wm:view:available:fields node_field_data
drush wm:view:available:filters node_field_data
drush wm:view:available:sorts node_field_data
```

## Menus, Vocabularies, Blocks & Media

```
drush wm:menu:list
drush wm:menu:get main
drush wm:menu:create
drush wm:menu:link:add
drush wm:menu:link:update

drush wm:vocabulary:list
drush wm:vocabulary:get tags
drush wm:vocabulary:create

drush wm:block:list
drush wm:block:place
drush wm:block:types

drush wm:media-type:list
drush wm:media-type:get image
```

## Translation Management

Requires the Language and Content Translation Drupal modules.

```
drush wm:translation:languages
drush wm:entity:translations node 1
drush wm:entity:translation:get node 1 fr
drush wm:entity:translation:set node 1 fr '{"title":"Bonjour"}'
drush wm:entity:translation:delete node 1 fr
```

## Content Moderation

Requires the Content Moderation Drupal module.

```
drush wm:entity:transitions node 1
drush wm:entity:moderate node 1 published
drush wm:entity:moderate node 1 published --dry-run
```

Always run `wm:entity:transitions` first to discover valid state transitions.

## Key Workflow Pattern

Default to Discover, then Inspect, then Modify.

1. **Discover**: `wm:schema:dump`,
   `wm:content-type:get`, `wm:entity:query`
2. **Inspect**: `wm:entity:get`, `wm:view:get`,
   `wm:field:list`, `wm:entity:transitions`
3. **Edit**: `wm:entity:edit` then modify YAML then
   `wm:entity:apply --dry-run` then `wm:entity:apply`
4. **Create**: `wm:entity:new` then fill template
   then `wm:entity:apply node new`
