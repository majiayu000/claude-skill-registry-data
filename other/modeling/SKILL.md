---
name: superpowers-sage:modeling
description: >
  Content modeling for Sage/Bedrock — classify as CPT ACF fields Blade component
  Livewire component or Options Page, Poet CPT configuration, ACF Composer fields
  vs GUI, relational content, static vs dynamic, content architecture decisions,
  config/poet.php, modeling before building, content classification matrix
user-invocable: true
---

# Modeling — Content Architecture Analysis

Classify content within blocks and components to determine the right data modeling approach: static ACF fields, dynamic CPTs, Options Pages, or relationship fields.

## When to use
- Planning a new block or component that displays content
- Deciding whether content should be hardcoded, editable per-page, or managed as a collection
- Before implementing blocks to prevent "static content that should be dynamic" mistakes
- Automatically invoked by `/building` when content classification is needed

## Content Classification Matrix

| Classification | When to Use | Implementation |
|---|---|---|
| **Static** | Fixed text that rarely changes, part of page identity | ACF field in block `fields()` |
| **Dynamic Collection** | Growing list of items (portfolio, team, testimonials) | CPT via Poet + taxonomy |
| **Dynamic Global** | Shared across pages (site info, social links, CTA) | ACF Options Page |
| **Dynamic Relation** | References other content (featured posts, related projects) | ACF Relationship field |
| **Fixed Repeater** | 3-5 items, rarely change, no detail pages | ACF Repeater field in block |

## Decision Checklist

For each piece of content in a block, ask:

1. **Does this content appear in more than one place?**
   - YES → Dynamic Global (Options Page) or Dynamic Relation
   - NO → Continue...

2. **Will the client add/remove items over time?**
   - YES → Dynamic Collection (CPT)
   - NO → Continue...

3. **Does the list have categories or filters?**
   - YES → Dynamic Collection (CPT + taxonomy)
   - NO → Continue...

4. **Is it a fixed set of 3-6 items that rarely changes?**
   - YES → Fixed Repeater (ACF Repeater in block)
   - NO → Continue...

5. **Does this content have its own detail page?**
   - YES → Dynamic Collection (CPT) — even if the list is short
   - NO → Continue...

6. **Should this content be searchable or filterable on the frontend?**
   - YES → Dynamic Collection (CPT)
   - NO → Static (ACF field)

## Output Format

For each analyzed component, output:

```markdown
### Content Model: {Component Name}

| Content Element | Classification | Implementation |
|---|---|---|
| {element} | {static/dynamic-collection/etc.} | {ACF field type / CPT name} |

**Poet Config** (if CPTs needed):
```php
// config/poet.php
'post' => [
    'project' => [
        'route' => 'projects',
        'supports' => ['title', 'editor', 'thumbnail'],
    ],
],
'taxonomy' => [
    'project_type' => [
        'links' => ['project'],
        'meta_box' => 'radio',
    ],
],
```

**ACF Fields** (key fields):
```php
$this->addText('headline', ['label' => 'Headline']);
$this->addRepeater('items', ['label' => 'Items'])
    ->addText('title')
    ->addTextarea('description')
    ->endRepeater();
```

**Query Example** (if dynamic):
```php
$projects = get_posts([
    'post_type' => 'project',
    'posts_per_page' => 6,
    'orderby' => 'menu_order',
    'order' => 'ASC',
]);
```
```

## Key Principles
- **Ask the checklist** — don't guess, systematically evaluate each content element
- **Default to static** — only use CPTs when the checklist clearly indicates dynamic content
- **YAGNI** — a repeater is simpler than a CPT; use the simpler option when both work
- **Poet for CPTs** — never `register_post_type()` directly
- **Future-proof wisely** — if content will "probably" grow, use a CPT; if "maybe someday", use a repeater

## Query First — MCP Integration

Before proposing CPTs or ACF field groups, query what already exists:

```
execute-ability posts/list-types
execute-ability acf/field-groups
```

See [`sageing/references/mcp-query-patterns.md`](../sageing/references/mcp-query-patterns.md).
