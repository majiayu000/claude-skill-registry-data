---
name: orbit-cron-audit
description: Audit `wp_schedule_event` / `wp_schedule_single_event` calls in a WordPress plugin — check for missed schedules, duplicate registrations on every page load, missing unschedule on deactivation, hooks scheduled but never registered (zombie crons), and overlapping cron windows that cause performance regressions. Use when the user says "cron audit", "wp_schedule_event", "scheduled tasks", "WP-Cron", or has a customer report of "site slow at certain times".
---

# 🪐 orbit-cron-audit — wp_schedule_event hygiene

WP-Cron is plugin teams' favourite way to schedule background work — and where most introduce bugs (zombie crons, missing unschedule, duplicate registrations).

---

## Quick start

```bash
# Static audit (read code)
claude "/orbit-cron-audit Review ~/plugins/my-plugin for cron registration hygiene."

# Live state (read DB)
wp-env run cli wp cron event list --format=table

# All plugins' cron events (find conflicts)
wp-env run cli wp cron event list --format=csv | grep my_plugin
```

Output: `reports/cron-audit-<timestamp>.md`.

---

## What it checks

### 1. Schedule registered on `init` (not at file-load)
```php
// ❌ Re-runs on every request
if ( ! wp_next_scheduled( 'my_plugin_task' ) ) {
  wp_schedule_event( time(), 'hourly', 'my_plugin_task' );
}

// ✅ Once on activation
register_activation_hook( __FILE__, 'my_plugin_activate' );
function my_plugin_activate() {
  if ( ! wp_next_scheduled( 'my_plugin_task' ) ) {
    wp_schedule_event( time(), 'hourly', 'my_plugin_task' );
  }
}
```

The "if not scheduled" check still hits the DB on every page load — even idempotently. Move it to activation.

### 2. Unschedule on deactivation + uninstall
```php
register_deactivation_hook( __FILE__, 'my_plugin_deactivate' );
function my_plugin_deactivate() {
  $timestamp = wp_next_scheduled( 'my_plugin_task' );
  if ( $timestamp ) wp_unschedule_event( $timestamp, 'my_plugin_task' );
  // Or, more aggressively, clear all of plugin's scheduled events:
  wp_clear_scheduled_hook( 'my_plugin_task' );
}
```

If you forget this, **deactivated plugins still fire their hooks**, leading to the classic "I deactivated it but it's still doing X" bug.

### 3. Custom interval registered before use
```php
// ❌ Schedule with interval before declaring it
wp_schedule_event( time(), 'every_5_min', 'my_plugin_task' );  // fails silently

// ✅ Declare via filter first
add_filter( 'cron_schedules', 'my_plugin_cron_schedules' );
function my_plugin_cron_schedules( $s ) {
  $s['every_5_min'] = [ 'interval' => 300, 'display' => __( 'Every 5 minutes', 'my-plugin' ) ];
  return $s;
}
```

### 4. Hook actually registered for the scheduled event
```php
// ❌ Scheduled but no listener — task never fires
wp_schedule_event( time(), 'hourly', 'my_plugin_task' );
// (no add_action for 'my_plugin_task' anywhere)

// ✅ Schedule + handler
add_action( 'my_plugin_task', 'my_plugin_run_task' );
function my_plugin_run_task() { /* ... */ }
```

This is the **zombie cron** — scheduled, fires every hour, but does nothing because the handler isn't registered. Wastes DB writes forever.

### 5. Long-running task without DOING_CRON guard
```php
add_action( 'my_plugin_task', 'my_plugin_run_task' );
function my_plugin_run_task() {
  if ( ! defined( 'DOING_CRON' ) || ! DOING_CRON ) {
    return;  // refuse to run if called outside cron
  }
  // expensive 30-second work
}
```

Without the guard, manually visiting `wp-cron.php` from the browser triggers the task during the request. UX hit.

### 6. Single-event vs recurring choice
```php
// One-off task
wp_schedule_single_event( time() + 60, 'my_plugin_send_email', [ $user_id ] );

// Recurring
wp_schedule_event( time(), 'hourly', 'my_plugin_task' );
```

Single events run once and self-clean. Recurring events keep firing until unscheduled. Choose right.

### 7. Cron storm (many tasks at the same minute)
If 5 plugins all schedule at minute 0 of every hour, that minute spikes every hour. Better to use random delays:
```php
$offset = wp_rand( 0, 600 );  // 0-10 min random
wp_schedule_event( time() + $offset, 'hourly', 'my_plugin_task' );
```

---

## Live DB inspection

```bash
# Every scheduled cron event
wp-env run cli wp cron event list --format=table

# Sample output:
# +--------------------------+------------------+------------+---------------+
# | hook                     | next_run_gmt     | next_run   | recurrence    |
# +--------------------------+------------------+------------+---------------+
# | my_plugin_task           | 2026-04-29 13:00 | 1714388400 | 3600          |
# | my_plugin_orphan_task    | 2026-04-29 14:00 | 1714392000 | 3600          |  ← no handler
# | another_plugin_task      | 2026-04-29 13:00 | 1714388400 | 3600          |
# +--------------------------+------------------+------------+---------------+

# Run a specific event manually
wp-env run cli wp cron event run my_plugin_task

# Delete a zombie event
wp-env run cli wp cron event delete my_plugin_orphan_task
```

---

## Replace WP-Cron with real cron (production)

WP-Cron is a poor man's scheduler — it only fires when someone visits the site. For low-traffic sites, schedules drift. For high-traffic, every visitor pays the cron-check cost.

```bash
# 1. Disable WP-Cron in wp-config.php
define( 'DISABLE_WP_CRON', true );

# 2. Hit wp-cron.php from real cron every 5 min
*/5 * * * * curl -s https://example.com/wp-cron.php?doing_wp_cron > /dev/null
```

Plugins should NOT change `DISABLE_WP_CRON` (that's a site-owner decision), but should be tested under both modes.

---

## Output

```markdown
# Cron Audit — my-plugin

## Static analysis
✓ 1 hook scheduled in activation: my_plugin_daily_task
✓ 1 hook unscheduled in deactivation
✓ 1 add_action handler for my_plugin_daily_task
❌ Custom interval `every_5_min` used at line 42 but never declared
   → Schedule call fails silently. Add filter `cron_schedules`.
❌ my_plugin_task scheduled BUT no add_action listener found
   → Zombie cron. Either remove the schedule or add the handler.

## Live state (port 8881)
- my_plugin_daily_task — runs hourly ✓
- my_plugin_orphan_task — runs hourly ❌ (no handler)
- my_plugin_one_time_email — runs once at 2026-04-29 13:00 ✓

## Severity: HIGH (zombie cron + bad interval)

## Fix order
1. Remove zombie schedule (line 17): `wp_clear_scheduled_hook('my_plugin_orphan_task')`
2. Declare custom interval before use (line 33): add `cron_schedules` filter
3. Re-test with: wp cron event list
```

---

## Pair with `/orbit-db-profile`

Cron audit catches the **structural** issues (missing handler, bad interval). DB profile catches the **runtime** cost (cron tasks slowing pages). Run both — together they cover scheduled-task health.
