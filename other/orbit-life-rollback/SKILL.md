---
name: orbit-life-rollback
description: Audit downgrade / rollback safety — when a user reverts to an older plugin version (because the new one broke), does the older version handle data shaped for the newer version, do migration locks remain consistent, are tables / options forward-compatible. Use when the user says "rollback safety", "downgrade plugin", "rollback after broken release", or has a one-click rollback feature.
---

# 🪐 orbit-life-rollback — Plugin downgrade safety

Rollback is rarer than upgrade but critical when a release breaks. If your data structure is forward-only, the rollback bricks the customer's site.

---

## What this skill checks

### 1. Forward-compatible schema
**Whitepaper intent:** When v2.5 adds a column, v2.4 should still query the table without crashing. SQL is forgiving on extra columns; PHP code is the risk.

```php
// ❌ v2.4 code that fails on v2.5 data
$row = $wpdb->get_row( "SELECT * FROM ..." );
echo $row->old_field;  // OK
echo $row->new_field;  // OK (v2.5 added it; harmless if NULL)
$count = count( (array) $row );
if ( $count !== 5 ) wp_die();  // ❌ — fails because v2.5 added column = 6 fields

// ✅ Defensive
$row = $wpdb->get_row( "SELECT old_col, new_col_that_v25_might_have FROM ..." );
echo isset( $row->new_col_that_v25_might_have ) ? esc_html( $row->new_col_that_v25_might_have ) : '';
```

### 2. Data-shape forward-compatibility
v2.5 changes options storage format. v2.4 reads it back, crashes on unexpected shape.

```php
// v2.4 code
$settings = get_option( 'my_plugin_settings' );
foreach ( $settings as $key => $val ) {  // assumes flat array
  // ...
}

// v2.5 changes it to nested array. v2.4 now iterates inner arrays as scalars → fatal.

// ✅ Defensive
$settings = (array) get_option( 'my_plugin_settings', [] );
$settings = my_plugin_v24_normalize( $settings );
```

### 3. Migration version flag remains accurate
After downgrade, the migration version flag still says "2.5.0 done" even though we're on 2.4.0. v2.5 re-installed will skip migrations → corruption.

```php
// On activation, also re-run any migrations whose version is BELOW current
function my_plugin_init_migrations() {
  $installed = get_option( 'my_plugin_version', '0.0.0' );
  $current = MY_PLUGIN_VERSION;
  if ( version_compare( $installed, $current, '>' ) ) {
    // We just downgraded! v2.5's migrations may be incompatible with v2.4 code.
    // Best behaviour: warn the user via admin notice, suggest contacting support.
  }
}
```

### 4. Pin a "minimum_supported_version" option
On install of v2.5, write `min_supported_version = '2.5.0'` to mark the downgrade floor. v2.4 can read this and refuse to load:
```php
$min = get_option( 'my_plugin_min_supported_version', '0.0.0' );
if ( version_compare( MY_PLUGIN_VERSION, $min, '<' ) ) {
  add_action( 'admin_notices', function() {
    echo '<div class="notice notice-error"><p>This version is older than what your data was migrated for. Roll forward or restore a backup.</p></div>';
  });
  return;
}
```

### 5. Document the rollback path
Even with all the above, document for support: "How to roll back" — restore DB backup AND plugin files together.

### 6. WP_PLUGIN_AUTOMATIC_UPDATER awareness
WP's auto-update can trigger an upgrade without the user clicking. If it fails halfway, the half-upgraded state is bad. Use atomic operations where possible.

---

## Output

```markdown
# Rollback Safety — my-plugin

## Forward-compat checks
- ✓ Database queries select named columns (resilient to schema additions)
- ❌ includes/class-renderer.php iterates `(array) $settings` assuming flat shape
   → v2.4 will crash on v2.5 settings format
   → Add my_plugin_normalize_settings_v24() helper

## Migration tracking
- ⚠ No min_supported_version option — v2.4 can re-install and re-run migrations on top of v2.5 schema

## Documentation
- ⚠ readme.txt has no rollback instructions
   → Add "Rolling back" section to docs
```

---

## Pair with

- `/orbit-life-upgrade` — forward migrations
- `/orbit-life-activation` — what runs on plugin re-install
- `/orbit-version-compare` — show what changed between versions

---

## Sources & Evergreen References

### Canonical docs
- [Plugin Versioning](https://developer.wordpress.org/plugins/plugin-basics/header-requirements/) — version field
- [Atomic Updates](https://make.wordpress.org/core/2020/07/30/wordpress-5-5-feature-plugin-merge-proposal-auto-updates/) — WP core auto-update

### Last reviewed
- 2026-04-29
