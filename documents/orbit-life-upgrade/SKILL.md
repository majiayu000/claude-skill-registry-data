---
name: orbit-life-upgrade
description: Audit version-upgrade migration logic — detect plugins that change schema / option shape between versions, verify migration runs once + is idempotent, verify version-tracking option exists, verify migrations cover every n→n+1 path. Use when the user says "version upgrade", "data migration", "schema change", "v1 → v2 path".
---

# 🪐 orbit-life-upgrade — Version migration safety

When a plugin bumps version, often the data shape changes. Plugins that don't handle the migration path leave half-migrated installations.

---

## What this skill checks

### 1. Version-tracking option
```php
// On every load
$installed_version = get_option( 'my_plugin_version', '0.0.0' );
$current_version = MY_PLUGIN_VERSION;

if ( version_compare( $installed_version, $current_version, '<' ) ) {
  my_plugin_run_migrations( $installed_version, $current_version );
  update_option( 'my_plugin_version', $current_version );
}
```

### 2. Migration path coverage
Every n → n+1 must have a migration if anything changed:
```php
function my_plugin_run_migrations( $from, $to ) {
  if ( version_compare( $from, '2.0.0', '<' ) ) my_plugin_migrate_to_2_0();
  if ( version_compare( $from, '2.5.0', '<' ) ) my_plugin_migrate_to_2_5();
  // ...up to current version
}
```

**Whitepaper intent:** Migrations must be idempotent + ordered. A user upgrading from 1.5 → 2.5 runs both `migrate_to_2_0` and `migrate_to_2_5` in sequence. Skipping the 2.0 migration corrupts data.

### 3. Schema migrations via dbDelta
```php
function my_plugin_migrate_to_2_0() {
  global $wpdb;
  $sql = "CREATE TABLE {$wpdb->prefix}my_plugin_v2 ( ... )";
  require_once ABSPATH . 'wp-admin/includes/upgrade.php';
  dbDelta( $sql );
}
```

### 4. Data migrations (existing rows reshaped)
```php
function my_plugin_migrate_to_2_5() {
  global $wpdb;
  // Old: stored prices as cents (integer). New: stored as float dollars.
  $rows = $wpdb->get_results( "SELECT id, price_cents FROM {$wpdb->prefix}my_plugin_orders" );
  foreach ( $rows as $row ) {
    $wpdb->update(
      "{$wpdb->prefix}my_plugin_orders",
      [ 'price' => $row->price_cents / 100 ],
      [ 'id' => $row->id ]
    );
  }
}
```

For huge tables, batch:
```php
$batch_size = 500;
$offset = 0;
do {
  $rows = $wpdb->get_results( $wpdb->prepare(
    "SELECT id FROM {$wpdb->prefix}my_plugin_orders LIMIT %d, %d",
    $offset, $batch_size
  ));
  foreach ( $rows as $row ) { /* migrate */ }
  $offset += $batch_size;
} while ( count( $rows ) === $batch_size );
```

### 5. Test migration (every n → n+1 → n+2)
Set up a wp-env site with version N installed, manually populate data, upgrade plugin to N+1, verify data still works.

### 6. Roll-forward, not roll-back
Migrations are one-way. Never depend on being able to "downgrade" — that's `/orbit-life-rollback`'s problem.

### 7. Migration timeouts
A migration hitting a 30s execution-time limit corrupts state. Always batch + use cron for long migrations.

---

## Output

```markdown
# Version Migration — my-plugin

## Current version: 2.5.0
## Migration coverage:
- ✓ 1.0.0 → 2.0.0 (schema add)
- ✓ 2.0.0 → 2.5.0 (data reshape)
- ❌ 1.5.0 → 2.0.0 missing — users on 1.5 may corrupt going to 2.x

## Issues
- migrate_to_2_5 is not idempotent — running twice multiplies prices by 100 again
   → Add a "migration_done_2_5" option to skip on re-run
- migrate_to_2_5 runs synchronously, processes 50K rows — will timeout on busy sites
   → Batch via cron
```

---

## Pair with

- `/orbit-life-activation` — activation runs migrations on first install
- `/orbit-life-rollback` — what to do when upgrade goes wrong
- `/orbit-version-compare` — measure version-to-version diff

---

## Sources & Evergreen References

### Canonical docs
- [dbDelta](https://developer.wordpress.org/reference/functions/dbdelta/) — schema migrations
- [version_compare](https://www.php.net/manual/en/function.version-compare.php) — PHP function
- [WP Background Processing](https://github.com/A5hleyRich/wp-background-processing) — chunked migrations

### Last reviewed
- 2026-04-29
