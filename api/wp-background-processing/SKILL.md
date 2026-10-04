---
name: wp-background-processing
description: "Use when a WordPress plugin needs to run work outside the HTTP request cycle — scheduling async or recurring jobs with Action Scheduler (as_enqueue_async_action, as_schedule_single_action, as_schedule_recurring_action, as_unschedule_action), implementing WP_Background_Process (push_to_queue, save, dispatch, is_queue_empty), registering WP Cron events (wp_schedule_event, wp_clear_scheduled_hook), batch-processing large datasets without hitting PHP timeouts, tracking job progress, handling retries on failure, or debugging the actionscheduler_actions table. Triggers: \"schedule this for later\", \"run this without hitting timeout\", \"queue these items for background processing\", \"why is my cron not running\", \"Action Scheduler job keeps failing\", \"as_enqueue_async_action\", \"WP_Background_Process\", \"push_to_queue\", \"dispatch the queue\", \"DISABLE_WP_CRON\", \"process records in batches\", \"send emails in the background\", \"WP Cron not firing\", \"batch import without timeout\", \"scheduled action not running\", \"background job stuck\", \"wp action-scheduler list\", \"recurring cron event\", \"progress tracking for batch job\", \"retry failed background tasks\", \"chunked processing to avoid timeout\", \"scheduled action completes but nothing happens\", \"my hook never fires in cron\", \"handler registered behind is_admin\", \"job runs in admin but not from cron\", \"webhook fired twice\", \"background job double-processed\", \"make my background job idempotent\". Not for: real-time AJAX handlers or synchronous REST endpoints."
---

# WordPress Background Processing

> **Model note:** Scaffolding a new Action Scheduler or `WP_Background_Process` implementation is pattern-matching — `haiku` handles it well. Debugging a stuck queue or race condition across async jobs requires reasoning; use `sonnet`.

Implement background jobs and queued tasks in WordPress plugins. Three primary tools with distinct trade-offs: Action Scheduler (persistent, battle-tested), `WP_Background_Process` (lightweight, no DB table), WP Cron (built-in, unreliable timing).

## When to use

- "Process a large batch of items in the background", "queue a long-running task".
- "Set up Action Scheduler", "use WooCommerce queue".
- "Implement WP_Background_Process", "chunked batch import".
- "Background email sending", "async API calls".
- "Fix a WP Cron job not firing", "make scheduled tasks reliable".
- "The scheduled action completes but nothing happens", "the handler only runs in the admin".

**Not for:** One-off scheduled events (use `wp_schedule_single_event`). REST API async patterns — use `wp-rest-api`.

## Method

### 1. Choose the right tool

| Tool | Persistent | Retry | Progress | Requires | Best for |
|---|---|---|---|---|---|
| Action Scheduler | ✅ DB table | ✅ Configurable | Via hooks | AS or WC | Reliable multi-step queues |
| WP_Background_Process | ✅ Options API | ❌ Manual | Via option | ~5KB class | Simple batches, no WC dep |
| WP Cron | ❌ (transient) | ❌ | ❌ | Nothing | Maintenance, low-priority tasks |

**Rule of thumb:** WooCommerce already installed → Action Scheduler. Simple background batch → `WP_Background_Process`. Periodic cleanup task → WP Cron.

### 2. Action Scheduler

Bundled with WooCommerce. Can also be installed as a standalone library.

**Standalone install:**
```bash
composer require woocommerce/action-scheduler
```
```php
require_once plugin_dir_path( __FILE__ ) . 'vendor/woocommerce/action-scheduler/action-scheduler.php';
```

**Schedule and handle actions:**
```php
// Schedule a single action (fires once ASAP)
as_enqueue_async_action( 'my_plugin_process_item', [ 'item_id' => 123 ], 'my-plugin' );

// Schedule a recurring action
as_schedule_recurring_action( time(), HOUR_IN_SECONDS, 'my_plugin_hourly_sync', [], 'my-plugin' );

// Schedule a single action in the future
as_schedule_single_action( time() + 300, 'my_plugin_delayed_job', [ 'batch' => 1 ], 'my-plugin' );

// Handle the action
add_action( 'my_plugin_process_item', function( $item_id ) {
    $result = my_plugin_do_work( $item_id );
    if ( is_wp_error( $result ) ) {
        // AS will retry on exception; throw to trigger retry
        throw new \Exception( $result->get_error_message() );
    }
} );
```

**Batch queue (fan-out pattern):**
```php
function my_plugin_queue_all_items() {
    $items = get_posts( [ 'post_type' => 'my_type', 'posts_per_page' => -1, 'fields' => 'ids' ] );
    foreach ( $items as $id ) {
        // Skip if already scheduled
        if ( ! as_has_scheduled_action( 'my_plugin_process_item', [ 'item_id' => $id ], 'my-plugin' ) ) {
            as_enqueue_async_action( 'my_plugin_process_item', [ 'item_id' => $id ], 'my-plugin' );
        }
    }
}
```

**Cancel scheduled actions:**
```php
as_unschedule_action( 'my_plugin_hourly_sync', [], 'my-plugin' );
as_unschedule_all_actions( 'my_plugin_process_item', [], 'my-plugin' );
```

**Monitor via WP-CLI:**
```bash
wp action-scheduler list --group=my-plugin --status=pending
wp action-scheduler run --group=my-plugin
```

### 3. WP_Background_Process

Lightweight 2-class library using WP options + transients for queue state. No extra DB table.

```bash
composer require deliciousbrains/wp-background-processing
```

**Extend the class:**
```php
class My_Plugin_Batch_Process extends WP_Background_Process {

    protected $action = 'my_plugin_batch'; // Unique key — used for cron and option names

    protected function task( $item ) {
        // Process one item. Return false to remove from queue; return $item to re-queue.
        $result = my_plugin_process( $item['id'] );
        if ( is_wp_error( $result ) ) {
            // Log and skip — returning $item would re-queue endlessly
            error_log( 'my-plugin: failed item ' . $item['id'] . ': ' . $result->get_error_message() );
            return false;
        }
        return false; // Done — remove from queue
    }

    protected function complete() {
        parent::complete();
        update_option( 'my_plugin_batch_complete', time() );
        do_action( 'my_plugin_batch_complete' );
    }
}
```

**Push items and dispatch:**
```php
$process = new My_Plugin_Batch_Process();

$items = get_ids_to_process();
foreach ( $items as $id ) {
    $process->push_to_queue( [ 'id' => $id ] );
}
$process->save()->dispatch();
```

**Check status:**
```php
if ( $process->is_queue_empty() ) { /* done */ }
```

### 4. WP Cron

Built-in. Fires on page load — unreliable on low-traffic sites. Use for non-critical periodic tasks.

```php
// Register custom interval
add_filter( 'cron_schedules', function( $schedules ) {
    $schedules['every_15_minutes'] = [
        'interval' => 15 * MINUTE_IN_SECONDS,
        'display'  => __( 'Every 15 Minutes', 'my-plugin' ),
    ];
    return $schedules;
} );

// Schedule on activation; clear on deactivation
register_activation_hook( __FILE__, function() {
    if ( ! wp_next_scheduled( 'my_plugin_cron_job' ) ) {
        wp_schedule_event( time(), 'every_15_minutes', 'my_plugin_cron_job' );
    }
} );
register_deactivation_hook( __FILE__, function() {
    wp_clear_scheduled_hook( 'my_plugin_cron_job' );
} );

// Handle
add_action( 'my_plugin_cron_job', function() {
    my_plugin_do_maintenance();
} );
```

**Make WP Cron reliable on low-traffic sites:** Set up a real system cron to call `wp-cron.php` and disable the page-load trigger:

```bash
# System cron (every 5 minutes)
*/5 * * * * wget -q -O - https://example.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1
```

```php
// wp-config.php
define( 'DISABLE_WP_CRON', true );
```

### 5. Progress tracking

Track batch progress for admin UI display:

```php
// Increment progress in task()
protected function task( $item ) {
    $progress = get_option( 'my_plugin_batch_progress', [ 'done' => 0, 'total' => 0 ] );
    // ... do work ...
    $progress['done']++;
    update_option( 'my_plugin_batch_progress', $progress );
    return false;
}

// Poll via REST or AJAX
add_action( 'wp_ajax_my_plugin_batch_progress', function() {
    wp_send_json_success( get_option( 'my_plugin_batch_progress', [ 'done' => 0, 'total' => 0 ] ) );
} );
```

### 6. Error handling patterns

Action Scheduler retries on uncaught exceptions. Control retry behaviour:
```php
// Fail permanently (no retry)
ActionScheduler_Logger::instance()->log( $action_id, 'Permanent failure: ' . $reason );
throw new ActionScheduler_InvalidActionException( $reason );

// Retry with delay (reschedule from handler)
as_schedule_single_action( time() + 300, 'my_plugin_process_item', $args, 'my-plugin' );
return; // Don't throw — AS won't auto-retry this run
```

### 7. Register the handler where the job actually runs

Background contexts run with `is_admin() === false`:

| Context | `is_admin()` |
|---|---|
| WP-Cron (`wp-cron.php`, system cron) | `false` |
| Action Scheduler queue runner | `false` |
| Payment gateway / third-party webhooks | `false` |
| WP-CLI | `false` |
| REST API request | `false` |
| `admin-ajax.php` | `true` |

So a handler registered inside an admin-only bootstrap never fires for the job it
was written for:

```php
// Bootstrap — handler is unreachable from the queue
if ( is_admin() ) {
    new My_Plugin\Admin\Controller(); // registers the AS handler in its constructor
}
```

This fails silently and looks healthy from the admin: the action schedules, the row
lands in `actionscheduler_actions`, the queue runner claims it, and — with no
listener attached — marks it complete. Nothing throws, nothing logs.

Register anything a background context must reach from an always-loaded bootstrap:

```php
// Always loaded — admin, front-end, cron, CLI, webhooks
new My_Plugin\Common\Queue_Controller();

if ( is_admin() ) {
    new My_Plugin\Admin\Controller(); // admin screens only
}
```

The same trap catches `admin_init` (never fires in cron), `current_screen`, and any
registration behind a capability check — the queue runner has no logged-in user.

**Detect it.** Grep the callback, then check what loads the file that registers it:

```bash
grep -rn "add_action( 'my_plugin_process_item'" .
# → is that class instantiated behind is_admin(), a screen check,
#   a current_user_can() gate, or hooked to admin_init?
```

Verify from outside the admin — an admin page load proves nothing here:

```bash
wp eval "do_action( 'my_plugin_process_item', 123 );"   # is_admin() is false
wp action-scheduler run --group=my-plugin
```

**Guard for re-entry.** A context you don't control can deliver the same job more
than once — webhook retries, a manual and an automatic path both completing, an
action rescheduled after a partial failure. Make the side effect idempotent with a
persisted flag instead of assuming one delivery:

```php
add_action( 'my_plugin_credit_order', function ( $order_id ) {
    $order = wc_get_order( $order_id );
    if ( ! $order || $order->get_meta( '_my_plugin_credited' ) ) {
        return; // already processed
    }
    my_plugin_credit( $order );
    $order->update_meta_data( '_my_plugin_credited', 1 );
    $order->save();
} );
```

## Notes

- Handlers for background work must be registered outside `is_admin()` — see §7. The
  failure is silent, so a "the job never runs" report starts by checking *where* the
  handler is registered, not what it does.
- Action Scheduler stores pending/failed actions in `{prefix}actionscheduler_actions` table — visible in WC → Status → Scheduled Actions. Check there first when debugging stuck jobs.
- WP Cron events do **not** persist across deactivation — always clear on `register_deactivation_hook`.
- Background processes that modify many posts/options should run in small chunks (50–100 items) to avoid timeout and memory limits. Use `$process->memory_exceeded()` and `$process->time_exceeded()` checks from `WP_Background_Process` to self-limit.
- On multisite: Action Scheduler is per-site. For network-wide jobs, run from the main site or loop via `switch_to_blog()`.

## References

- `references/action-scheduler-api.md` — Action Scheduler API: scheduling functions, queue management, batch operations, status constants, and WP Cron integration
- `references/batch-patterns.md` — Chunked processing patterns: chunk size rules, memory/time guards, `WP_Background_Process` subclass scaffold, and queue drain loop
- `references/wp-cron-intervals.md` — WP Cron built-in intervals, custom interval registration, debug commands, and cron health-check tools
