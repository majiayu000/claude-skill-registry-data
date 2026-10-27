---
name: drush-webmaster
version: 1.0.0
description: |
  Manage Drupal content, entities, views, menus, fields, and site structure
  using drush webmaster (wm:*) commands. Use when asked to "list content types",
  "find articles by author", "create a new page", "edit node 42", "add a field",
  "build a view", "add a menu link", "translate this
  content", "publish this node", "what content types
  exist", "show me the site schema", "search for
  content", "clone this entity", "moderate content",
  or any Drupal entity/content management task.
  Proactively invoke this skill (do NOT attempt raw
  SQL, drush eval, or direct Drupal API calls) when
  the user wants to query, create, edit, inspect, or
  manage Drupal content, entities, views, menus,
  blocks, vocabularies, media, translations, or site
  configuration.
---

## Preamble (run first)

```bash
# Site context discovery — runs automatically when skill is invoked
echo "=== SITE CONTEXT ==="
drush wm:site:info 2>/dev/null || \
  echo "SITE_INFO: unavailable (no drush/bootstrap)"

echo ""
echo "=== CONTENT TYPES ==="
drush wm:content-type:list 2>/dev/null || echo "CONTENT_TYPES: unavailable"

echo ""
echo "=== OPTIONAL MODULES ==="
_PM="drush pm:list --status=enabled"
_PM="$_PM --type=module --format=list"
_HAS_LANG=$($_PM 2>/dev/null \
  | grep -c "^language$" || true)
_HAS_MOD=$($_PM 2>/dev/null \
  | grep -c "^content_moderation$" || true)
_HAS_SEARCH=$($_PM 2>/dev/null \
  | grep -c "^search$" || true)
echo "TRANSLATION_ENABLED: $([ "$_HAS_LANG" -gt 0 ] && echo 'yes' || echo 'no')"
echo "MODERATION_ENABLED: $([ "$_HAS_MOD" -gt 0 ] && echo 'yes' || echo 'no')"
echo "SEARCH_ENABLED: $([ "$_HAS_SEARCH" -gt 0 ] && echo 'yes' || echo 'no')"

# Show configured languages if translation is enabled
if [ "$_HAS_LANG" -gt 0 ]; then
  echo ""
  echo "=== LANGUAGES ==="
  drush wm:translation:languages 2>/dev/null || true
fi

# Site learnings — persistent knowledge across sessions
_SITE_UUID=$(drush config:get system.site uuid \
  --format=string 2>/dev/null || echo "unknown")
_SITE_HASH=$(echo -n "$_SITE_UUID" \
  | (shasum -a 256 2>/dev/null || sha256sum) \
  | cut -c1-12)
_LEARN_DIR="$HOME/.drush-wm/sites/$_SITE_HASH"
_LEARN_FILE="$_LEARN_DIR/learnings.jsonl"
echo ""
echo "=== LEARNINGS ==="
echo "SITE_HASH: $_SITE_HASH"
if [ -f "$_LEARN_FILE" ]; then
  _LEARN_COUNT=$(wc -l < "$_LEARN_FILE" | tr -d ' ')
  echo "LEARNINGS_COUNT: $_LEARN_COUNT"
  tail -50 "$_LEARN_FILE"
else
  echo "LEARNINGS_COUNT: 0"
fi
```

**After reading preamble output:**

- If `TRANSLATION_ENABLED` is `no`: do not suggest
  translation commands (`wm:translation:*`,
  `wm:entity:translation:*`)
- If `MODERATION_ENABLED` is `no`: do not suggest
  moderation commands (`wm:entity:transitions`,
  `wm:entity:moderate`)
- If `SEARCH_ENABLED` is `no`: do not suggest
  `wm:search`, use `wm:entity:query` instead
- If `SITE_INFO` is `unavailable`: alert the user
  that drush is not available or the site cannot be
  bootstrapped
- Use the content type list to validate bundle names
  before running entity queries or create operations

# Drush Webmaster Commands

The `wm:*` command suite provides YAML-based Drupal
site management. All output is structured YAML. Run
`drush wm:<command> --help` for full documentation
on any command before using it.

## Discovery (Full Schema)

### `wm:schema:dump` — Full site schema for AI context

Use for deeper exploration beyond what the preamble provides.

```bash
# Full schema (all sections)
drush wm:schema:dump

# Single section (faster, focused)
drush wm:schema:dump --section=content-types
drush wm:schema:dump --section=views
drush wm:schema:dump --section=vocabularies

# Multiple sections
drush wm:schema:dump --section=content-types --section=vocabularies
```

Available sections: `content-types`,
`vocabularies`, `views`, `menus`, `blocks`,
`media-types`, `entity-types`, `site`

Use `drush wm:schema:sections` to list all available sections.

### `wm:site:info` — Site name, slogan, email, paths

```bash
drush wm:site:info
```

## Before Modifying (Discover First)

Before running any create, edit, or delete operation, run the
appropriate discovery command if you haven't already in this
conversation. This prevents validation errors and wasted retries.

| Operation | Run first |
|---|---|
| Create entity | `wm:content-type:get` — fields |
| Edit fields | `wm:entity:get` — current values |
| Delete entity | `wm:entity:get` — confirm target |
| Add field | `wm:field:list` + `wm:field:types` |
| Create/edit view | `wm:view:tables` + `available:fields` |
| Translate | `wm:translation:languages` |
| Moderate | `wm:entity:transitions` — states |
| Bulk create | `wm:content-type:get` — structure |
| Bulk delete | `wm:entity:query` — confirm scope |

Skip discovery when the context is already known from earlier in the
conversation or the user explicitly asks to proceed directly.

## Querying & Inspecting Entities

### `wm:entity:query` — Find entities by field conditions

Powerful query with operators, sorting, pagination. No search index needed.

```bash
# Published articles by author
drush wm:entity:query node article \
  --where="status=1" --where="uid=5" \
  --sort=created:DESC

# Count drafts
drush wm:entity:query node --where="status=0" --count

# Content without images
drush wm:entity:query node article --where="field_image=NULL" --fields=id,title

# Paginate
drush wm:entity:query node blog --limit=50 --offset=50
```

Where operators: `=`, `!=`, `>`, `<`, `>=`, `<=`,
`=NULL`, `!=NULL`, `=a,b,c` (IN list)

Options: `--where`, `--sort=field:ASC|DESC`,
`--limit`, `--offset`, `--fields`, `--count`

### `wm:entity:get` — Get single entity with field values

```bash
drush wm:entity:get node 1
drush wm:entity:get node 1 --fields=title,body
drush wm:entity:get node 1 --exclude=revision_*,created
drush wm:entity:get user 1
```

### `wm:entity:field:get` — Get a single field value

```bash
drush wm:entity:field:get node 1 title
drush wm:entity:field:get node 1 body
drush wm:entity:field:get user 1 mail
```

### `wm:entity:field:set` — Set a single field value

```bash
drush wm:entity:field:set node 1 title "New Title"
drush wm:entity:field:set node 1 body \
  '{"value":"<p>HTML</p>","format":"full_html"}'
drush wm:entity:field:set node 1 status 1
drush wm:entity:field:set node 1 status 1 --dry-run
```

Value is a plain string for simple fields, or JSON
for structured fields (body, entity references,
links, images).

### `wm:entity:list` — Simple entity listing

```bash
drush wm:entity:list node article
```

### `wm:search` — Full-text search (requires Search module + index)

```bash
drush wm:search "contact form"
drush wm:search "DXPR" --limit=50
drush wm:search "admin" --type=user_search
```

Returns: nid, bundle, title, url, snippet. Use
`wm:entity:get` to get full content after finding
results.

## Creating & Editing Entities (YAML Workflow)

The edit/apply workflow: export to YAML, modify, apply with validation.

### `wm:entity:edit` + `wm:entity:apply` — Edit existing entity

```bash
# Step 1: Export to versioned YAML file
drush wm:entity:edit node 5089

# Step 2: Edit the YAML file at ~/.drush-wm/entities/
# Step 3: Validate and save
drush wm:entity:apply node 5089

# Preview changes without saving
drush wm:entity:apply node 5089 --dry-run
```

### `wm:entity:new` + `wm:entity:apply` — Create new entity

```bash
# Step 1: Create template with all fields
drush wm:entity:new node article

# Step 2: Edit the template (fill required fields)
# Step 3: Create the entity
drush wm:entity:apply node new
```

### Bulk Operations

```bash
drush wm:entity:bulk-create   # YAML input
drush wm:entity:bulk-update   # YAML input
drush wm:entity:bulk-delete   # YAML input
```

### Other Entity Operations

```bash
drush wm:entity:clone node 42         # Clone entity
drush wm:entity:deep-clone node 42    # Clone with references
drush wm:entity:diff node 42 43       # Compare entities
drush wm:entity:history node 42       # YAML version history
drush wm:entity:revert node 42        # Revert to previous version
drush wm:entity:fields node article   # List fields for a bundle
drush wm:entity:types                 # List entity types
```

## Content Types & Fields

```bash
drush wm:content-type:list            # List all content types
drush wm:content-type:get article     # Full details + fields
drush wm:content-type:stats           # Content counts
drush wm:content-type:create          # Create content type
drush wm:content-type:update article  # Update settings
drush wm:content-type:delete article  # Delete (must be empty)

drush wm:field:list node article      # List fields on bundle
drush wm:field:get node article title # Field details
drush wm:field:add                    # Add field to bundle
drush wm:field:update                 # Update field settings
drush wm:field:delete                 # Delete field + data
drush wm:field:types                  # Available field types
```

## Views

Same YAML edit/apply workflow as entities.

```bash
drush wm:view:list                    # List all views
drush wm:view:get content             # Full view config
drush wm:view:create                  # Create view
drush wm:view:clone content           # Clone existing view
drush wm:view:edit blog               # Export to YAML
drush wm:view:apply blog              # Apply changes
drush wm:view:apply blog --dry-run    # Validate only
drush wm:view:preview content         # Render view output
drush wm:view:delete content          # Delete view
drush wm:view:enable/disable content  # Toggle view

# Discovery helpers for building views
drush wm:view:tables                  # Available base tables
drush wm:view:available:fields node_field_data
drush wm:view:available:filters node_field_data
drush wm:view:available:sorts node_field_data
drush wm:view:available:arguments node_field_data
drush wm:view:available:relationships node_field_data
drush wm:view:available:areas node_field_data
```

## Menus

```bash
drush wm:menu:list                    # All menus with link counts
drush wm:menu:get main               # Menu details + all links
drush wm:menu:create                  # Create menu
drush wm:menu:delete main             # Delete (must be empty)
drush wm:menu:link:list main          # Links with hierarchy
drush wm:menu:link:add                # Add link
drush wm:menu:link:update             # Update link
drush wm:menu:link:delete             # Delete link
```

## Vocabularies & Taxonomy

```bash
drush wm:vocabulary:list              # All vocabularies + counts
drush wm:vocabulary:get tags          # Vocabulary details + fields
drush wm:vocabulary:create            # Create vocabulary
drush wm:vocabulary:update tags       # Update settings
drush wm:vocabulary:delete tags       # Delete (must be empty)
```

Use `wm:entity:query taxonomy_term tags` to query
terms, and `wm:entity:new taxonomy_term tags` to
create terms.

## Blocks & Media

```bash
drush wm:block:list                   # All placed blocks by region
drush wm:block:get block_id           # Block placement details
drush wm:block:place                  # Place block in region
drush wm:block:update                 # Update placement
drush wm:block:remove                 # Remove from region
drush wm:block:types                  # Available block plugins

drush wm:media-type:list              # Media types + counts
drush wm:media-type:get image         # Media type details
```

## Getting Full Help

Always run `--help` on any command before first use
to see full argument/option details:

```bash
drush wm:entity:query --help
drush wm:view:create --help
drush wm:field:add --help
```

## Translation Management

Requires the Language and Content Translation
Drupal modules (optional — commands return clear
errors if not installed).

### `wm:translation:languages` — List configured languages

```bash
drush wm:translation:languages
```

### `wm:entity:translations` — List translations for an entity

```bash
drush wm:entity:translations node 1
drush wm:entity:translations taxonomy_term 5
```

### `wm:entity:translation:get` — Get a specific translation

```bash
drush wm:entity:translation:get node 1 fr
drush wm:entity:translation:get node 1 en
```

### `wm:entity:translation:set` — Add or update a translation

```bash
# Add French translation
drush wm:entity:translation:set node 1 fr '{"title":"Bonjour"}'

# Add full translation with body
drush wm:entity:translation:set node 1 fr \
  '{"title":"Bonjour","body":{"value":"<p>Contenu</p>","format":"full_html"}}'

# Preview without saving
drush wm:entity:translation:set node 1 fr '{"title":"Test"}' --dry-run
```

### `wm:entity:translation:delete` — Remove a translation

```bash
drush wm:entity:translation:delete node 1 fr
drush wm:entity:translation:delete node 1 fr --dry-run
```

## Content Moderation

Requires the Content Moderation Drupal module
(optional — commands return clear errors if not
installed).

### `wm:entity:transitions` — Show current state and available transitions

```bash
drush wm:entity:transitions node 1
drush wm:entity:transitions media 5
```

### `wm:entity:moderate` — Transition entity to a new moderation state

```bash
# Publish a draft
drush wm:entity:moderate node 1 published

# Send to review
drush wm:entity:moderate node 1 review

# Archive content
drush wm:entity:moderate node 1 archived

# Preview without saving
drush wm:entity:moderate node 1 published --dry-run
```

Always use `wm:entity:transitions` first to discover
available states and valid transitions for an entity.

## Learnings (Site Memory)

Save site-specific knowledge that would be useful in future sessions.
The preamble loads these automatically so Claude starts each session
already knowing this site's quirks.

**To save a learning** (self-contained — derives site hash inline):

```bash
_SU=$(drush config:get system.site uuid \
  --format=string 2>/dev/null || echo "unknown")
_SH=$(echo -n "$_SU" \
  | (shasum -a 256 2>/dev/null || sha256sum) \
  | cut -c1-12)
mkdir -p "$HOME/.drush-wm/sites/$_SH"
printf \
  '{"ts":"%s","cat":"%s","key":"%s","val":"%s"}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  "<category>" "<key>" "<description>" \
  >> "$HOME/.drush-wm/sites/$_SH/learnings.jsonl"
```

**Categories:** `content_type`, `field`, `view`, `vocabulary`,
`menu`, `moderation`, `translation`, `gotcha`

**When to save:**
- User corrects a wrong assumption (e.g., "it's `blog_post` not `article`")
- You discover a non-obvious field requirement or naming convention
- A command fails and you determine the correct approach
- The site has unusual configuration worth remembering

**Before saving**, check if a learning with the same `key` already
exists in the file. If so, skip or update the existing entry rather
than appending a duplicate.

**Do NOT save:**
- Information that `wm:schema:dump` already provides (always current)
- Temporary state (draft counts, specific entity IDs being worked on)
- Sensitive data (passwords, API keys, user emails)

**Housekeeping:** If `LEARNINGS_COUNT` exceeds 100, trim the oldest
entries before adding new ones:

```bash
_SU=$(drush config:get system.site uuid \
  --format=string 2>/dev/null || echo "unknown")
_SH=$(echo -n "$_SU" \
  | (shasum -a 256 2>/dev/null || sha256sum) \
  | cut -c1-12)
_LF="$HOME/.drush-wm/sites/$_SH/learnings.jsonl"
_TMP=$(mktemp) \
  && tail -80 "$_LF" > "$_TMP" \
  && mv "$_TMP" "$_LF"
```

## Key Workflow Pattern

Default to Discover → Inspect → Modify. Skip discovery only when
context is already known from earlier in the conversation or the
user explicitly requests direct execution.

1. **Discover**: `wm:schema:dump`,
   `wm:content-type:get`, `wm:entity:query`,
   `wm:search`
2. **Inspect**: `wm:entity:get`, `wm:view:get`,
   `wm:field:list`, `wm:entity:transitions`
3. **Edit**: `wm:entity:edit` then modify YAML then
   `wm:entity:apply --dry-run` then
   `wm:entity:apply`
4. **Create**: `wm:entity:new` → fill template → `wm:entity:apply node new`
