---
name: dxb
version: 1.0.0
description: |
  Build and manage DXPR Builder pages via drush dxb:* commands.
  Write Bootstrap 5 HTML — the builder parses it into drag-and-drop
  editable elements. Use when asked to "create a page", "build a
  landing page", "edit page markup", "list templates", "update page
  layout", "create a reusable section", "scaffold content from a
  template", or any DXPR Builder content/layout task. Proactively
  invoke this skill instead of writing raw drush eval or direct
  Drupal API calls for page building tasks.
---

## Preamble (run first)

```bash
echo "=== DXPR BUILDER CONTEXT ==="

echo ""
echo "=== PAGE TEMPLATES ==="
drush dxb:template:list 2>/dev/null || echo "TEMPLATES: unavailable"

echo ""
echo "=== CONTENT TYPES WITH DXPR BUILDER FIELDS ==="
DXPR_TYPES=$(drush php:eval '
  $etm = \Drupal::entityTypeManager();
  $displays = $etm->getStorage("entity_view_display")->loadMultiple();
  $types = [];
  foreach ($displays as $display) {
    foreach ($display->getComponents() as $name => $component) {
      if (isset($component["type"]) && $component["type"] === "dxpr_builder_text") {
        $types[] = $display->getTargetEntityTypeId() . "." . $display->getTargetBundle() . " (field: " . $name . ")";
      }
    }
  }
  echo implode("\n", array_unique($types)) ?: "None found";
' 2>/dev/null) || DXPR_TYPES="FIELD_DETECTION: unavailable"
echo "$DXPR_TYPES"

echo ""
echo "=== CONTENT TYPE DETAILS (fields, settings) ==="
# Use wm:content-type:get if available for each builder-enabled bundle.
if command -v drush &>/dev/null && drush wm:content-type:list &>/dev/null 2>&1; then
  echo "$DXPR_TYPES" | grep "^node\." | sed 's/node\.\([^ ]*\).*/\1/' | sort -u | while read -r bundle; do
    echo "--- $bundle ---"
    drush wm:content-type:get "$bundle" 2>/dev/null || echo "  unavailable"
  done
else
  echo "wm:content-type:get unavailable (drush_webmaster not installed)"
fi

echo ""
echo "=== USER TEMPLATES ==="
drush dxb:user-template:list 2>/dev/null || echo "USER_TEMPLATES: unavailable"
```

**After reading preamble output:**

- Use content type details to understand fields, required settings, and descriptions
- Before `page:create`, pass the correct `type` argument (the content type machine name)
- Use the content type + field list to know which bundles support DXPR Builder and which field to target
- Use template list to suggest available templates when creating pages
- If multiple builder fields exist on a bundle, always specify `--field`

# DXPR Builder Drush Commands

<!-- PROMPT_RULES_START (auto-generated from prompt.js — do not edit manually) -->
## HTML Content Rules

DXPR Builder parses standard Bootstrap 5 HTML into drag-and-drop
editable elements. You write BS5 markup, the builder handles the
rest. However, you MUST follow these rules:

### Layout

- Use Bootstrap grid system and responsive design patterns
- Row columns must total exactly 12 (e.g. col-6 + col-6, col-4 + col-4 + col-4). Do NOT use col-auto or col without a size — each column must have an explicit number (col-1 through col-12)
- Avoid nested containers
- Sections contain content directly - no empty wrapper divs:
- But only use a container-fluid when appropriate for the type of content
- CRITICAL: NEVER use Bootstrap flexbox utility classes (d-flex, d-inline-flex, gap-*, flex-row, flex-column, flex-wrap, justify-content-*, align-items-*) for layouts. These classes are FORBIDDEN.
- For ANY horizontal arrangement of elements (buttons, links, cards, icons, etc.), you MUST use the Bootstrap grid: wrap elements in div.row containing div.col-N children that total 12

### Styling

- The content will be part of a custom themed Bootstrap 5 page
- Use Bootstrap classes for their intended purpose, e.g. do not use .warning or .success just for styling
- DO NOT use CSS background colors or gradients unless the user explicitly requests them
- DO NOT include style tags

### Images

- Every IMG tag needs src and alt attributes
- Place images between content blocks, not inline with text
- Format src as: https://promptahuman.com/600x400@2x?bg_color=[HEX]&text_color=[HEX+333333]&title=[file_name.png]&prompt=[Creative Brief in plain text, emoji allowed.]
- bg_color: Use 444444 or contextually appropriate color
- text_color: Must be subtle - use bg_color value + 333333 (e.g., bg_color=444444 → text_color=777777)
- Alt text must double as the image creative brief: a standalone description (10-20 words) that an image creator (AI or human) could use to produce the picture without any other context
- Use the same text for both the alt attribute and the URL prompt parameter
- File name respects picture type, image=jpg, animation=gif, video=mp4, etc
- Section bg image can be on container never on row or col

### General

- Output only valid HTML that can be directly inserted into a webpage
- DO NOT include DOCTYPE, html, head, or body tags
- DO NOT use markdown formatting (no \`\`\` or \`\`\`html tags)
- Return ONLY the raw HTML with no wrapping or formatting
- Never include explanations, meta-commentary, word counts, character counts, or generation statistics
- No explanations or meta-commentary in output
<!-- PROMPT_RULES_END -->

## Commands

### Discovery

```bash
# List available elements (blocks, views)
drush dxb:element:list
drush dxb:element:list --type=block
drush dxb:element:list --type=view

# List page templates
drush dxb:template:list
drush dxb:template:list --category=Landing

# List user templates (reusable components)
drush dxb:user-template:list
drush dxb:user-template:list --global
```

### Creating Pages

```bash
# Create from template (type is required)
drush dxb:page:create drag_and_drop_page my_template \
  --title="Page Title"

# Dry run
drush dxb:page:create page my_template \
  --title="Test" --dry-run
```

### Reading & Updating Markup

`page:update` preserves the entity's existing text format (e.g. `dxpr_builder_html`). Never set the text format manually when updating -- the command handles it.

```bash
# Get current markup
drush dxb:page:get 42
drush dxb:page:get 5 --entity-type=block_content

# Update with Bootstrap 5 HTML
drush dxb:page:update 42 \
  --markup='<section class="py-5"><div class="container">...</div></section>'

# Update from file
drush dxb:page:update 42 --markup=@/tmp/page.html

# Dry run
drush dxb:page:update 42 --markup="<div>new</div>" --dry-run
```

### Saving Reusable Templates

```bash
# Create user template
drush dxb:user-template:create "Hero Section" \
  --markup='<section class="py-5">...</section>'

# Create global template (available to all users)
drush dxb:user-template:create "CTA Block" \
  --markup='<div class="container">...</div>' --global
```

## Workflow

1. **Discover** — `template:list`, `element:list`
2. **Create** — `page:create` from template, or create entity then `page:update` with BS5 markup
3. **Edit** — `page:get` to read current markup, modify, `page:update` to save
4. **Reuse** — `user-template:create` to save sections for reuse

Always write Bootstrap 5 HTML following the content rules above.
The builder parses it into visual drag-and-drop components automatically.
