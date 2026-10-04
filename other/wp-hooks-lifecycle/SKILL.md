---
name: superpowers-sage:wp-hooks-lifecycle
description: >
  WordPress hooks lifecycle — add_action, add_filter, do_action, apply_filters,
  remove_action, remove_filter, hook priority, plugins_loaded, init, wp_loaded,
  after_setup_theme, the_content filter, wp_enqueue_scripts, admin_enqueue_scripts,
  hook execution order, Acorn hook registration in AppServiceProvider, boot hooks,
  register hooks, WordPress hook reference, Tailwind CSS filter conflicts, save_post,
  transition_post_status, pre_get_posts, late hooks, early hooks.
  Invoke for: hook priority conflicts, unexpected filter behavior, wptexturize corruption,
  Acorn vs WordPress hook timing, save_post edge cases, enqueue order issues.
user-invocable: false
---
# WordPress Hooks and Lifecycle

## When to use

When adding, modifying, or debugging WordPress hooks (actions and filters) within a Sage/Acorn project. This covers where to place hooks in the Sage architecture, understanding execution order, managing priority, using dependency injection in callbacks, and diagnosing hook-related issues.

## Inputs required

- The behavior to implement or modify (what the hook should accomplish)
- Whether the task requires an action (side effect) or a filter (data transformation)
- The appropriate lifecycle stage for the hook

## Procedure

### 1. Understand actions vs filters

- **Actions** perform side effects: register post types, enqueue scripts, send emails, flush caches.
  - `add_action('hook_name', $callback, $priority, $accepted_args)`
  - Callback returns nothing (return value is ignored).
- **Filters** transform data: modify queries, alter output, change settings.
  - `add_filter('hook_name', $callback, $priority, $accepted_args)`
  - Callback MUST return the filtered value.

### 2. WordPress lifecycle order

See [`references/hook-timing.md`](references/hook-timing.md) for the full boot sequence and early/late hook guidance.

Quick reference:

```
plugins_loaded → after_setup_theme → init → wp_loaded → wp_enqueue_scripts → the_content
```

### 3. Where to place hooks in Sage

See [`references/acorn-hook-patterns.md`](references/acorn-hook-patterns.md) for the three correct hook locations in Acorn.

**Preferred: `boot()` method in a ServiceProvider:**

```php
class ProjectServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        add_action('init', [$this, 'registerPostTypes']);
        add_action('wp_enqueue_scripts', [$this, 'enqueueAssets']);
        add_filter('the_content', [$this, 'appendProjectMeta']);
        add_filter('pre_get_posts', [$this, 'modifyProjectQuery']);
    }
}
```

### 4. Priority and argument count

```php
// Default priority is 10, default accepted_args is 1
add_action('save_post', [$this, 'onSave'], 10, 3);

// Lower number = runs earlier
add_action('init', [$this, 'earlyInit'], 5);
add_action('init', [$this, 'lateInit'], 20);

// accepted_args must match callback parameters
add_filter('the_title', function (string $title, int $post_id) {
    return $title . ' #' . $post_id;
}, 10, 2);
```

### 5. Common hooks for Sage projects

| Hook | Type | Typical use |
|---|---|---|
| `after_setup_theme` | Action | Theme supports, nav menus, image sizes |
| `wp_enqueue_scripts` | Action | Enqueue front-end CSS/JS |
| `init` | Action | Register CPTs, taxonomies, shortcodes |
| `save_post` | Action | Post save side effects (cache invalidation, sync) |
| `pre_get_posts` | Action | Modify main query before execution |
| `the_content` | Filter | Modify post content output |
| `rest_api_init` | Action | Register REST routes |
| `admin_enqueue_scripts` | Action | Enqueue admin CSS/JS |

### 6. Filter gotchas with modern CSS frameworks

See [`references/filter-gotchas.md`](references/filter-gotchas.md) for `wptexturize`, `wpautop`, and `wp_kses_post` pitfalls that affect Tailwind v4 themes.

Key fix for Tailwind arbitrary variants:

```php
// In ThemeServiceProvider::boot()
add_filter('run_wptexturize', '__return_false');
```

## Verification

1. Use Query Monitor to verify hooks fire in the expected order and with expected callbacks.
2. Confirm `did_action('hook_name')` returns the expected count at the point in code where you need it.
3. For filters, log input and output values to confirm data transformation is correct.
4. Test hook removal by verifying the target callback no longer appears in Query Monitor.
5. Run the full page lifecycle and check that no "doing it wrong" notices appear in the debug log.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Hook never fires | Registered too late (after WordPress already fired it) | Check lifecycle order in `references/hook-timing.md` |
| Filter returns null | Missing `return` statement in filter callback | All data for that filter becomes null/empty |
| Hook fires multiple times | Common with `save_post` (autosaves, revisions) | Guard with `wp_is_post_autosave()` and `wp_is_post_revision()` |
| Cannot remove hook | Original was added with anonymous closure or different object instance | Cannot be removed without modifying the source |
| Wrong number of arguments | Callback receives fewer arguments than expected | Check `$accepted_args` parameter matches |
| Infinite loop | Filter modifies data that triggers the same filter | Use `remove_action` before the triggering call, then re-add |
| Hooks not firing from provider | Provider not registered | Verify provider is listed in `config/app.php` under `providers` |

## Escalation

- If a hook fires in unexpected order, dump `$wp_filter['hook_name']` to see all registered callbacks and their priorities.
- If hooks added in a ServiceProvider are not firing, verify the provider is listed in `config/app.php` under `providers`.
- For complex hook interaction debugging, enable `WP_DEBUG_LOG` and use `error_log()` with timestamps at each hook point to trace execution flow.
