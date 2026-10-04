---
name: orbit-rtc-compat
description: Audit a WordPress plugin for Real-Time Collaboration (RTC) compatibility — WP 7.0 ships RTC for the block editor; classic meta-boxes break it. Verifies plugin uses `register_post_meta()` + `PluginSidebar` instead of classic meta-boxes, declares sync-provider compatibility, doesn't write to post directly mid-edit. Use when the user says "RTC", "real-time collaboration", "WP 7.0 collab", "meta box collab", or has classic meta boxes that need to migrate.
---

# 🪐 orbit-rtc-compat — Real-Time Collaboration compat

WP 7.0's flagship feature is RTC — multiple editors editing the same post in real time. Classic meta-boxes don't work in RTC mode (they disable collab when present). Modern plugins migrate to `register_post_meta()` + Block Editor sidebar components.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://make.wordpress.org/core/ → search "Real-Time Collaboration" + "RTC" recent posts
   - https://developer.wordpress.org/block-editor/reference-guides/slotfills/plugin-sidebar/ → current PluginSidebar API
   - https://developer.wordpress.org/reference/functions/register_post_meta/ → meta registration reference
   - https://github.com/WordPress/gutenberg/discussions → RTC-related dev discussion

2. **Synthesize**: what's the current sync-provider filter name? Has anything moved since this skill was written?

3. **Audit the plugin** against the fetched rules.

---

## What this skill checks

### 1. Classic meta-boxes — flag, propose migration

```php
// ❌ Classic — disables RTC for any post that uses your meta-box
add_meta_box(
  'my_plugin_meta',
  __( 'My Plugin', 'my-plugin' ),
  'my_plugin_meta_callback',
  'post'
);

// ✅ Modern — RTC-compatible
register_post_meta( 'post', 'my_plugin_field', [
  'show_in_rest' => true,
  'single' => true,
  'type' => 'string',
  'auth_callback' => fn() => current_user_can( 'edit_posts' ),
] );

// + JS via @wordpress/edit-post:
import { PluginDocumentSettingPanel } from '@wordpress/edit-post';
import { useEntityProp } from '@wordpress/core-data';

const MyPanel = () => {
  const [meta, setMeta] = useEntityProp('postType', 'post', 'meta');
  return (
    <PluginDocumentSettingPanel name="my-plugin" title="My Plugin">
      <TextControl
        label="My Field"
        value={meta.my_plugin_field || ''}
        onChange={value => setMeta({ ...meta, my_plugin_field: value })}
      />
    </PluginDocumentSettingPanel>
  );
};
```

### 2. Don't write directly to post mid-edit

**Whitepaper intent:** RTC works by syncing edits across collaborators. A plugin that bypasses the block editor's data layer (e.g. directly `wp_update_post()` on save) writes that other collaborators don't see → conflicts.

```php
// ❌ Bypasses RTC sync — other editors don't see your changes
add_action( 'save_post', function( $post_id ) {
  wp_update_post( [ 'ID' => $post_id, 'post_excerpt' => 'auto-generated' ] );
});

// ✅ Hook into the editor's data flow
register_post_meta( 'post', '_my_excerpt_override', [ 'show_in_rest' => true ] );
// Generate the excerpt client-side via PluginSidebar, sync via meta
```

### 3. Sync provider compatibility (advanced)

WP 7.0 lets hosts plug in custom sync providers (default + Yjs + others). Plugins that hook into post saves should respect the active sync provider:

```php
$sync_provider = apply_filters( 'sync.providers', 'default' );
// Adjust behaviour if non-default sync is active
```

### 4. Color-coded selections + presence indicators

If your plugin renders a custom interactive UI inside the editor (canvas widget, custom list), it should expose selection / focus events to RTC's presence layer so other collaborators see "User A is editing the My Hero widget."

This is opt-in and rare — flag only if relevant.

### 5. Storage in `wp_options` / `transient` mid-edit

Plugins that store editor state in `wp_options` or transients (e.g. "last opened block") create RTC conflicts. Move to per-user state:

```php
// ❌ Global option — collaborators overwrite each other
update_option( 'my_plugin_last_opened_block', $block_id );

// ✅ Per-user
update_user_meta( get_current_user_id(), 'my_plugin_last_opened_block', $block_id );
```

---

## Output

```markdown
# RTC Compat — my-plugin · 2026-04-30

> Per make.wordpress.org/core (fetched 2026-04-30 14:32 UTC):
> WP 7.0 ships May 20; RTC is on by default for posts and pages.

## Classic meta-boxes detected: 3
- ❌ admin/meta-box-author.php — disables RTC when present
- ❌ admin/meta-box-source.php — disables RTC
- ⚠ admin/meta-box-debug.php — admin-only, less critical but still migrate

## Direct post writes mid-edit: 1
- ⚠ includes/class-excerpt.php:47 — wp_update_post on save_post
   → Migrate to client-side excerpt generation via PluginSidebar

## Sync provider awareness
- Plugin doesn't filter sync.providers — default is fine for now, but
  document if customer uses Yjs / custom provider

## Severity: HIGH — 3 classic meta-boxes will block RTC for any post they appear on
```

---

## Pair with

- `/orbit-abilities-api` — WP 7.0 readiness in general
- `/orbit-gutenberg-dev` — block editor patterns
- `/orbit-block-bindings` — modern data binding (RTC-friendly)

---

## Smoke test

Input: a plugin with 1 classic meta-box.
Expected:
- 1 ❌ HIGH finding for the meta-box
- Migration suggestion citing `register_post_meta` + PluginSidebar
- Cites make.wordpress.org/core fetched today

---

## Embedded fallback rules (offline)
- Classic meta-boxes disable RTC; migrate to `register_post_meta` + `PluginSidebar`
- Direct `wp_update_post()` mid-edit causes RTC conflicts
- Sync provider filter: `sync.providers`
- Per-user state via `update_user_meta`, not `update_option`

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Make WP Core](https://make.wordpress.org/core/) — RTC announcements
- [PluginSidebar API](https://developer.wordpress.org/block-editor/reference-guides/slotfills/plugin-sidebar/)
- [register_post_meta](https://developer.wordpress.org/reference/functions/register_post_meta/)
- [Gutenberg discussions](https://github.com/WordPress/gutenberg/discussions) — RTC integration thread

### Last reviewed
2026-04-30
