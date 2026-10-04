---
name: orbit-abilities-api
description: Audit a WordPress plugin for the new Abilities API + AI Client & Connectors API (WP 7.0, ships May 20, 2026). Verifies `register_ability()` calls, `@wordpress/abilities` JS package usage, AI Client provider abstraction, browser-agent + WebMCP integration patterns. Use when the user says "Abilities API", "WP 7 AI", "register_ability", "AI Client API", or builds plugins that integrate with WP's native AI framework.
---

# 🪐 orbit-abilities-api — WP 7.0 Abilities API audit

WP 7.0 ships the Abilities API + AI Client & Connectors API — WordPress's native framework for plugins to expose actions to AI agents and consume AI services with a standardised interface.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel** (these are source-of-truth — embedded rules below are offline fallback only):
   - https://make.wordpress.org/core/ → search for "Abilities API" and "AI Client" recent posts
   - https://developer.wordpress.org/news/ → latest "What's new for developers" entry (current month)
   - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/abilities.php → canonical source for `register_ability()` (will exist post-7.0)
   - https://www.npmjs.com/package/@wordpress/abilities → JS package latest version + current API
   - https://github.com/WordPress/gutenberg/tree/trunk/packages/abilities → JS package source

2. **Synthesize current state**:
   - "Has WP 7.0 actually shipped yet?" (check `https://wordpress.org/download/releases/`)
   - "What's the current Abilities API signature as of the canonical source today?"
   - "Have any rules been deprecated since this skill was last run?"

3. **Audit the plugin** against the synthesized current rules.

4. **Cite, in every finding**: source URL + fetch timestamp.

---

## What this skill checks (under the live-fetched rules)

### 1. Abilities are registered, not actions
**Whitepaper intent (per WP 7.0 announcement):** Plugins that expose AI-callable actions should use `register_ability()` — gives AI agents a typed, discoverable interface. Plain `add_action()` works too, but Abilities are the canonical path for AI-integration in WP 7.0+.

```php
// ✅ WP 7.0+ pattern
register_ability( 'my-plugin/save-settings', [
  'label'       => __( 'Save plugin settings', 'my-plugin' ),
  'description' => __( 'Persists user settings to the database.', 'my-plugin' ),
  'permission_callback' => fn() => current_user_can( 'manage_options' ),
  'args'        => [
    'api_key' => [ 'type' => 'string', 'required' => true ],
  ],
  'execute_callback' => 'my_plugin_save_settings',
] );
```

### 2. AI Client API for outbound AI calls
```php
// Use WP's AI Client instead of bundling your own SDK
$client = wp_get_ai_client();  // post-WP 7.0
$response = $client->generate_text( [
  'prompt' => 'Summarise this post: ' . $post_content,
  'max_tokens' => 100,
] );
```

This abstracts over OpenAI / Anthropic / Google / local models. Plugins become AI-provider agnostic.

### 3. Client-side `@wordpress/abilities`
```js
import { registerAbility } from '@wordpress/abilities';

registerAbility( 'my-plugin/preview-render', {
  // browser-side ability — useful for editor previews etc.
} );
```

### 4. WebMCP integration (where applicable)
WP 7.0's Client-Side Abilities API hooks into WebMCP — plugins can be controlled by external AI agents over MCP without writing a custom MCP server.

### 5. Permission callbacks (NEVER skip)
Every ability must have a `permission_callback`. Without it, anyone with browser access to the WP-Admin can call the ability. Treat the same as REST endpoint permission_callback.

### 6. Deprecation of `state.navigation` in Interactivity API
WP 7.0 deprecates `state.navigation` in the Interactivity API. Use the new `watch()` function and `state.url` instead.

```js
// ❌ Deprecated in 7.0
const route = store.state.navigation.path;

// ✅ Post-7.0
import { watch } from '@wordpress/interactivity';
watch( () => state.url );
```

---

## Output

```markdown
# Abilities API Audit — my-plugin · 2026-04-30

> Per WP make.wordpress.org/core (fetched 2026-04-30 14:32 UTC):
> WP 7.0 RC4 expected May 14; release May 20.

## Abilities registered: 0
- ⚠ Plugin exposes 4 admin-AJAX actions but no `register_ability()` calls
- Recommendation: migrate the 4 user-facing actions to Abilities post-7.0
   - my-plugin/save-settings
   - my-plugin/import-data
   - my-plugin/export-data
   - my-plugin/reset

## AI Client API
- ⚠ Plugin bundles its own OpenAI SDK (vendor/openai-php-client)
- Recommendation post-7.0: use `wp_get_ai_client()` for provider abstraction.
  Drop the bundled SDK to save ~600KB.

## Interactivity API
- ✓ No `state.navigation` references (clean for 7.0)

## WebMCP exposure
- 0 abilities currently MCP-discoverable. Consider opt-in for plugins
  that want to be controllable by external AI agents.
```

---

## Pair with

- `/orbit-wp-playground` — WP core agent skills, complementary to Abilities
- `/orbit-rtc-compat` — WP 7.0's Real-Time Collaboration affects meta-boxes
- `/orbit-rest-fuzzer` — abilities, like REST endpoints, must have permission_callback

---

## Smoke test

Input: a plugin that registers 1 admin AJAX action.
Expected output:
- 0 abilities registered
- 1 recommendation to migrate to `register_ability()` post-WP 7.0
- Cites `make.wordpress.org/core` (or current canonical source) with today's date

---

## Embedded fallback rules (used only if WebFetch fails)

- WP 7.0 ships May 20, 2026; Abilities API + AI Client API native
- `register_ability()` is the canonical PHP function
- `@wordpress/abilities` is the JS package
- Every ability needs `permission_callback`
- Interactivity API: `state.navigation` → `watch()` + `state.url`

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Make WP Core](https://make.wordpress.org/core/) — release announcements
- [Developer Blog](https://developer.wordpress.org/news/) — monthly developer changes
- [@wordpress/abilities npm](https://www.npmjs.com/package/@wordpress/abilities) — JS package version + API
- [WP Develop trunk](https://github.com/WordPress/wordpress-develop/) — canonical source

### Last reviewed
2026-04-30 — re-fetch on every run; WP 7.0 release date is volatile (extended once already)
