---
name: wp-database
description: "Use when a WordPress plugin needs a custom database table — creating with dbDelta (strict SQL format: two spaces before PRIMARY KEY, no trailing comma), writing versioned upgrade routines with version_compare and register_activation_hook, querying with $wpdb prepared statements (prepare, insert, update, delete, get_row, get_results, get_var), debugging with $wpdb->last_error or SAVEQUERIES, schema migrations between plugin versions, uninstall cleanup, multisite table handling with switch_to_blog / get_sites, or seeding test/preview data into custom tables. Triggers: \"create a custom table\", \"dbDelta not working\", \"dbDelta not creating my table\", \"write a migration\", \"wpdb query\", \"wpdb prepare\", \"slow query on my custom table\", \"upgrade my database schema\", \"add a column to my table\", \"seed test data\", \"how do I store this in a custom table\", \"database upgrade routine\", \"table not being created on activation\", \"prepare placeholder wrong\", \"last_error is empty after query\", \"SAVEQUERIES debug\", \"version_compare for db upgrade\", \"register_activation_hook table\", \"wpdb prefix table name\", \"uninstall drops table\", \"multisite per-site table\", \"charset_collate missing\". Not for: WordPress options API or post meta — use those when a custom table is not needed."
---

# WordPress Custom Database Tables

> **Model note:** `dbDelta` schema and CRUD patterns are mechanical (`haiku`). Query optimisation and multi-version data migrations require cross-file reasoning — use `sonnet` for those sub-tasks.

Create and manage custom database tables in WordPress plugins: `dbDelta()` for schema definition, versioned upgrade routines, `$wpdb` CRUD with prepared statements, and data migration strategies.

## When to use

- "Create a custom DB table for my plugin", "set up plugin schema with dbDelta".
- "Write a migration for plugin upgrade", "run schema changes on update".
- "Query a custom table", "insert/update/delete with $wpdb".
- "Optimise a slow custom query", "add an index to a plugin table".
- "Migrate data from post meta to a custom table".

**Not for:** WooCommerce order table operations — use `wp-woocommerce`. General $wpdb query optimisation in core WP tables — use `wp-performance` (official skill).

## Method

### 1. Create table with dbDelta

`dbDelta()` is the only WP-safe way to create and alter tables — it diffs the current schema against the SQL and applies only the necessary changes.

```php
function my_plugin_create_tables() {
    global $wpdb;
    $charset_collate = $wpdb->get_charset_collate(); // e.g. DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci

    // $wpdb->prefix respects multisite site prefix automatically
    $table_log  = $wpdb->prefix . 'my_plugin_log';
    $table_meta = $wpdb->prefix . 'my_plugin_item_meta';

    // IMPORTANT: two spaces before PRIMARY KEY, one space before each KEY
    // IMPORTANT: no trailing comma on last field before closing paren
    $sql = "CREATE TABLE {$table_log} (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  item_id bigint(20) unsigned NOT NULL,
  action varchar(100) NOT NULL DEFAULT '',
  message longtext NOT NULL,
  user_id bigint(20) unsigned NOT NULL DEFAULT 0,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY  (id),
  KEY item_id (item_id),
  KEY created_at (created_at)
) {$charset_collate};

CREATE TABLE {$table_meta} (
  meta_id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  item_id bigint(20) unsigned NOT NULL,
  meta_key varchar(255) NOT NULL DEFAULT '',
  meta_value longtext,
  PRIMARY KEY  (meta_id),
  KEY item_id (item_id),
  KEY meta_key (meta_key(191))
) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
```

**Critical dbDelta formatting rules** (violations cause silent failures):
- Two spaces after `PRIMARY KEY` (e.g. `PRIMARY KEY  (id)`)
- Field definitions must end with a comma except the last field before the closing paren
- `KEY` lines go after all field definitions, before the closing paren
- Only `CREATE TABLE` statements — no `ALTER TABLE` (dbDelta handles column additions, not removals)
- Always include `{$charset_collate}` at the end

### 2. Versioned upgrade routine

Track schema version in an option; only re-run dbDelta when the version changes:

```php
define( 'MY_PLUGIN_DB_VERSION', '1.3.0' );

function my_plugin_maybe_upgrade_db() {
    $installed = get_option( 'my_plugin_db_version', '0' );
    if ( version_compare( $installed, MY_PLUGIN_DB_VERSION, '>=' ) ) {
        return; // already up to date
    }

    my_plugin_create_tables(); // always safe to re-run dbDelta

    // Version-specific data migrations
    if ( version_compare( $installed, '1.2.0', '<' ) ) {
        my_plugin_migrate_to_1_2_0();
    }
    if ( version_compare( $installed, '1.3.0', '<' ) ) {
        my_plugin_migrate_to_1_3_0();
    }

    update_option( 'my_plugin_db_version', MY_PLUGIN_DB_VERSION );
}
add_action( 'plugins_loaded', 'my_plugin_maybe_upgrade_db' );
```

Run on `plugins_loaded` (every request until updated), not just on activation — catches updates after auto-update or version switch.

### 3. $wpdb CRUD

Always use `$wpdb->prepare()` for any value from user input or untrusted source.

**Insert:**
```php
$result = $wpdb->insert(
    $wpdb->prefix . 'my_plugin_log',
    [
        'item_id'    => $item_id,
        'action'     => 'view',
        'message'    => $message,
        'user_id'    => get_current_user_id(),
        'created_at' => current_time( 'mysql' ),
    ],
    [ '%d', '%s', '%s', '%d', '%s' ] // format for each value: %d int, %s string, %f float
);
$inserted_id = $wpdb->insert_id;
```

**Update:**
```php
$wpdb->update(
    $wpdb->prefix . 'my_plugin_log',
    [ 'message' => $new_message ],          // data
    [ 'id'      => $log_id ],               // where
    [ '%s' ],                               // data format
    [ '%d' ]                                // where format
);
```

**Delete:**
```php
$wpdb->delete(
    $wpdb->prefix . 'my_plugin_log',
    [ 'item_id' => $item_id ],
    [ '%d' ]
);
```

**Select — single row:**
```php
$row = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_plugin_log WHERE id = %d",
        $log_id
    )
); // returns stdClass or null
```

**Select — multiple rows:**
```php
$rows = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_plugin_log WHERE item_id = %d ORDER BY created_at DESC LIMIT %d",
        $item_id,
        50
    )
); // returns array of stdClass
```

**Select — single value:**
```php
$count = (int) $wpdb->get_var(
    $wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->prefix}my_plugin_log WHERE action = %s",
        'view'
    )
);
```

**Raw query (DDL / no-result):**
```php
// phpcs:ignore WordPress.DB.DirectDatabaseQuery
$wpdb->query(
    $wpdb->prepare(
        "DELETE FROM {$wpdb->prefix}my_plugin_log WHERE created_at < %s",
        gmdate( 'Y-m-d H:i:s', strtotime( '-30 days' ) )
    )
);
```

### 4. Error handling

```php
$result = $wpdb->insert( ... );
if ( false === $result ) {
    // $wpdb->last_error contains the MySQL error
    error_log( 'my-plugin DB error: ' . $wpdb->last_error );
    return new WP_Error( 'db_insert_error', $wpdb->last_error );
}
```

Enable query logging during development:
```php
define( 'SAVEQUERIES', true );
// Then: print_r( $wpdb->queries )
```

### 5. Schema migrations (data migrations)

For migrating existing data (not just schema changes):

```php
function my_plugin_migrate_to_1_2_0() {
    global $wpdb;

    // Example: move post meta to custom table
    $meta_rows = $wpdb->get_results(
        "SELECT post_id, meta_value FROM {$wpdb->postmeta} WHERE meta_key = '_my_plugin_data'"
    );

    if ( ! $meta_rows ) return;

    $table = $wpdb->prefix . 'my_plugin_log';
    foreach ( $meta_rows as $row ) {
        $wpdb->insert( $table, [
            'item_id' => $row->post_id,
            'message' => $row->meta_value,
            'action'  => 'migrated',
        ], [ '%d', '%s', '%s' ] );
    }

    // Remove the old meta after successful migration
    $wpdb->delete( $wpdb->postmeta, [ 'meta_key' => '_my_plugin_data' ], [ '%s' ] );
}
```

For large datasets, use batches (via `wp-background-processing`):
```php
function my_plugin_migrate_batch( $offset = 0 ) {
    global $wpdb;
    $batch = $wpdb->get_results( $wpdb->prepare(
        "SELECT * FROM {$wpdb->postmeta} WHERE meta_key = '_old_key' LIMIT 100 OFFSET %d",
        $offset
    ) );
    // ... process batch ...
    if ( count( $batch ) === 100 ) {
        // More to process — schedule next batch
        as_enqueue_async_action( 'my_plugin_migrate_batch', [ 'offset' => $offset + 100 ], 'my-plugin' );
    } else {
        update_option( 'my_plugin_migration_complete', true );
    }
}
```

### 6. Table removal on uninstall

Use `register_uninstall_hook` (not `deactivation_hook`) for destructive cleanup:

```php
// uninstall.php (registered via register_uninstall_hook(__FILE__, ...) or placed at plugin root)
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) exit;

global $wpdb;

// Drop per-site tables on multisite
if ( is_multisite() ) {
    $sites = get_sites( [ 'number' => 0, 'fields' => 'ids' ] );
    foreach ( $sites as $site_id ) {
        switch_to_blog( $site_id );
        $wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_log" );
        delete_option( 'my_plugin_db_version' );
        restore_current_blog();
    }
} else {
    $wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_log" );
    delete_option( 'my_plugin_db_version' );
}
```

### 7. Seeding sample / preview data (dev only)

To populate custom tables with realistic data for local preview, write a standalone script run via WP-CLI's `wp eval-file` — never auto-loaded by the plugin. Keep it in a `tools/` dir and document it in `tools/README.md`.

```php
<?php
// tools/seed-dev-data.php — run: wp eval-file tools/seed-dev-data.php [--fresh]
if ( ! defined( 'WP_CLI' ) || ! WP_CLI ) { exit( "Run via: wp eval-file <this file>\n" ); }
global $wpdb;
$table = $wpdb->prefix . 'my_plugin_log';

// --fresh truncates first. TRUNCATE is destructive — gate it, and expect the
// agent permission classifier to block it unless tables are already empty.
if ( in_array( '--fresh', (array) ( $args ?? [] ), true ) ) {
    $wpdb->query( "TRUNCATE TABLE {$table}" ); // phpcs:ignore
}

foreach ( $rows as $row ) {
    $wpdb->insert( $table, $row ); // hardcoded columns only
}
WP_CLI::success( 'Seeded.' );
```

Conventions that keep seeders safe and re-runnable:

- **Idempotent where it matters.** A seeder that creates linked records (WP users, EDD payments) should skip rows already linked — e.g. `if ( ! empty( $row->payment_id ) ) continue;` — so reruns don't duplicate. A pure log-filler can be additive; say so in the script header and accept a count arg (`(int) ( $args[0] ?? 0 ) ?: 20`).
- **Link to real WP objects, not fakes.** Create real users with `wp_insert_user()` and reuse by email (`get_user_by`); mint EDD orders through the plugin's own purchase wrapper (e.g. an `EDD` integration class) rather than raw inserts, so the seeded data exercises the real code path. Write the resulting `user_id` / `payment_id` back onto the custom-table row.
- **Generate via WP-CLI, verify via `wp db query`.** Confirm row counts/links after seeding.
- **Dev-only.** Never ship `tools/`; never run against production. Use `current_time('mysql')` / `gmdate()` for timestamps, and seed `extra`/JSON columns with `wp_json_encode()`.

Note on randomness: scripts run by `wp eval-file` may warn on large int math (`$x * 2654435761` overflows to float) — keep PRNG seeds inside `& 0x7fffffff`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrapper methods that discard `$wpdb->insert()` return value cause silent failures | **Always** check the return value and propagate `$wpdb->last_error` upstream — callers cannot diagnose a failure the wrapper swallowed. Return `null`/`WP_Error` on failure, never silently return as if the insert succeeded |

## Notes

- `dbDelta()` can ADD columns but cannot remove them. Removing columns requires `ALTER TABLE DROP COLUMN` in a manual migration step.
- Never use `$wpdb->prepare()` with `%s` for integers — always `%d`. Using `%s` on an integer is not a security issue but causes type coercion surprises.
- Column names in `$wpdb->insert()` / `update()` / `delete()` are NOT escaped — they must be hardcoded, never user-supplied.
- Cache expensive custom queries: `$results = wp_cache_get( $cache_key, 'my_plugin' ); if ( false === $results ) { $results = $wpdb->get_results(...); wp_cache_set( $cache_key, $results, 'my_plugin', 300 ); }`
- Always include `bigint(20) unsigned NOT NULL AUTO_INCREMENT` as the primary key — matches WP core table conventions.
- Use `gmdate()` not `date()` for DB timestamps; WP's `current_time('mysql')` returns local time — use it only when you need WP's configured timezone.

## References

- `references/dbdelta-rules.md` — `dbDelta()` rules: strict SQL formatting requirements, column change limitations, and safe schema diff patterns
- `references/migration-strategies.md` — Versioned upgrade routines: `db_version` pattern, migration function registration, and idempotent migration checklist
- `references/wpdb-patterns.md` — `$wpdb` prepared statement patterns, insert/update/delete helpers, and custom-table query conventions
