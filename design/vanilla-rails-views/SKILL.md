---
name: vanilla-rails-views
description: Use when writing ERB templates, partials, view helpers, or Turbo Stream responses - covers partial organization, optional locals, CSS class patterns, collection rendering
---

# Views & Templates

ERB conventions for vanilla Rails applications.

## Partial Organization

**Lowest common ancestor** - place partials at the highest shared directory:

```
# Shared by cards/show and cards/index
app/views/cards/_card.html.erb

# Shared across controllers
app/views/application/_flash.html.erb

# Display variants of same model
app/views/cards/display/_compact.html.erb
app/views/cards/display/_full.html.erb
```

**Never** create deeply nested partials only used in one place.

## Optional Locals

Use `local_assigns.fetch` with explicit defaults:

```erb
<%# Good - explicit default, raises if required %>
<% pinned = local_assigns.fetch(:pinned, false) %>
<% card = local_assigns.fetch(:card) %>

<%# Bad - silent nil, ambiguous intent %>
<% pinned = local_assigns[:pinned] || false %>
```

## CSS Class Helper

Build classes with array + compact + join:

```erb
<%# Good %>
<div class="<%= [
  'card',
  ('card--pinned' if card.pinned?),
  ('card--closed' if card.closed?)
].compact.join(' ') %>">

<%# Bad - string interpolation %>
<div class="card <%= 'card--pinned' if card.pinned? %>">
```

For complex cases, use `token_list` helper:

```erb
<div class="<%= token_list('card', 'card--pinned': card.pinned?) %>">
```

## Collection Rendering

Always cache, always specify `as:`:

```erb
<%= render partial: 'cards/card',
           collection: @cards,
           as: :card,
           cached: true %>
```

## Turbo Streams

Prepend/append with update for empty states:

```erb
<%# Add item and update counter/empty state %>
<%= turbo_stream.before :cards, @card %>
<%= turbo_stream.update :cards_count, @cards.count %>

<%# Remove and handle empty %>
<%= turbo_stream.remove @card %>
<%= turbo_stream.update :cards_empty, partial: 'empty' if @cards.none? %>
```

## Stimulus Integration

Layer controllers on existing elements:

```erb
<%# Good - multiple controllers on body %>
<body data-controller="keyboard shortcuts dropdown">

<%# Bad - wrapper div just for controller %>
<div data-controller="card-actions">
  <%= render @card %>
</div>
```

Keyboard shortcuts via body controller:

```erb
<body data-controller="keyboard"
      data-action="keydown->keyboard#handle">
```

## Quick Reference

| Pattern | Use |
|---------|-----|
| `local_assigns.fetch(:x, default)` | Optional locals |
| `[...].compact.join(' ')` | Conditional CSS classes |
| `cached: true, as: :item` | Collection rendering |
| `turbo_stream.before` + `.update` | Add + refresh related |
| `data-controller="a b c"` | Multiple controllers |

## Common Mistakes

| Wrong | Right |
|-------|-------|
| `local_assigns[:x] \|\| default` | `local_assigns.fetch(:x, default)` |
| Wrapper div for Stimulus | Add controller to existing element |
| `render @cards` without cache | `render collection:, cached: true` |
| Partial in deep nested path | Lowest common ancestor |
