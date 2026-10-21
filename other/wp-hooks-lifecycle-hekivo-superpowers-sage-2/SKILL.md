---
name: wp-hooks-lifecycle
description: Use when adding, moving or debugging WordPress actions and filters in an Acorn project - add_action/add_filter priority and accepted_args, where a hook belongs (setup or filters files vs a provider boot()), load order (mu-plugins, plugins_loaded, after_setup_theme, init), when Acorn boots per profile, hooks that never fire on Acorn routes, REST or Livewire requests (template_redirect, wp_head), save_post firing twice in the block editor, the_content priorities. For ACF hooks use acf-native; for provider structure use acorn-stack.
---

# WordPress hooks and lifecycle under Acorn

The rules of the Plugin API never change. What changes per profile is **when Acorn boots** relative to WordPress's load order, and therefore which hooks a provider's `boot()` can still catch. Read the profile from the session context.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.test}}`, `{{runner.cache}}`) come from the session context; on Lando they default to `lando wp`, `lando wp acorn` and the project's test and cache tooling. Never run WP-CLI or PHP on the host.

## When to use

- Adding a hook and deciding where it lives and at what priority.
- A hook "never fires", fires twice, fires with stale data, or fires on some request types only.
- Removing a hook added by a plugin, the theme or a package.
- Content or markup is altered unexpectedly by a core filter (`wpautop`, `wptexturize`, kses).

Not for: ACF-specific hooks and the ACF save flow (`acf-native`), provider structure and caches (`acorn-stack`), REST route design (`acorn-routes-api`).

## Inputs required

1. Profile and the hook that boots Acorn (session context: theme include time, or `after_setup_theme` at a given priority).
2. The behaviour to implement: side effect (action) or value transformation (filter), and the first moment the data it needs exists.
3. The request types involved: front end, admin, REST, AJAX, cron, WP-CLI, Acorn route, Livewire update.

### Load order (WordPress 7.1.3 `wp-settings.php`)

```
mu-plugins: top-level *.php in alphabetical order (subfolders need a loader such as bedrock-autoloader)
  → muplugins_loaded
  → core taxonomies and post types created
  → active plugins (plugin_loaded per file)
  → pluggable.php (wp_get_current_user, wp_verify_nonce, wp_mail…)
  → plugins_loaded
  → setup_theme
  → theme functions.php: child theme first, then parent
  → after_setup_theme
  → $wp->init() (current user set up)
  → init
  → wp_loaded
  → request: parse_request → wp → template_redirect → template (wp_head → content → wp_footer) → shutdown
```

### When Acorn boots, per profile

| Concern | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Acorn boots (providers `register()` + `boot()`) | While `functions.php` is included: after `setup_theme`, before `after_setup_theme` | Inside the main file's `after_setup_theme` callback (priority set by the plugin) | Inside a committed mu-plugin's `after_setup_theme` callback |
| Plain hooks without dependencies | `app/setup.php`, `app/filters.php` (loaded by `functions.php` right after the boot, so `app()` already works there) | Bootstrap files required by the main plugin file at mu-plugin include time (`app()` does **not** work at their file scope) | A provider `boot()`; theme supports and menus from `config/theme.php` through the project's theme provider |
| Hooks for `muplugins_loaded`, `plugins_loaded`, `setup_theme` | Impossible from a theme (already fired); needs a plugin or mu-plugin | Bootstrap files, file scope | A mu-plugin file, file scope |
| `after_setup_theme` from a provider `boot()` | Any priority | Only priorities **greater** than the boot priority | Only priorities greater than the boot priority |
| `init` and later from `boot()` | Yes | Yes | Yes |

Why the strict "greater": `WP_Hook` iterates priorities and copies the callback list of the priority it is running, so a callback added at the running priority is skipped for that request; a lower one already ran.

## Procedure

1. **Pick the hook** by when the data exists (table in [references/hook-timing.md](references/hook-timing.md)): CPTs on `init`, current user on `init` or later, main query on `template_redirect`, rendered HTML on `the_content` priority ≥ 12.
2. **Pick the place**:
   - needs services, config or DI → the feature provider's `boot()`;
   - plain hook, no dependencies → the profile's bootstrap/setup file, delegating to a class (`[Some::class, 'method']`);
   - must fire before Acorn boots (table above) → a bootstrap file at file scope (mu-plugin profiles) or a separate mu-plugin;
   - container bindings → `register()`, never hooks there.
   Patterns and examples: [references/acorn-hook-patterns.md](references/acorn-hook-patterns.md).
3. **Write the callback**: filters return the value on every path; `$accepted_args` covers every parameter you read; guard the context first (post type, autosave, revision, `is_admin()`, `wp_doing_ajax()`, `wp_doing_cron()`, `defined('WP_CLI')`); keep it thin and named so it can be removed and tested.
4. **Check the request types** the hook must cover (next section).
5. **Native first**: before writing custom code, confirm there is no core hook or argument that already does it (read `wp/wp-includes/default-filters.php`, `class-wp-hook.php`, the plugin's source).

### Requests where template hooks never fire

| Request | Runs | Never runs |
|---|---|---|
| Acorn route (`routes/web.php`, `routes/api.php`, Livewire endpoints) | Full load through `wp_loaded`, then `parse_request`, where Acorn answers and exits; `shutdown` | `wp`, `template_redirect`, `wp_enqueue_scripts`, `wp_head`, `the_content`, `wp_footer` |
| REST (`/wp-json/…`) | Full load, `parse_request` → `rest_api_init` → endpoint → exit | Template hooks |
| Admin, AJAX (`admin-ajax.php`) | `admin_init`, admin enqueue hooks | Front-end template hooks |
| WP-CLI, cron | Full load | Request and template hooks; `is_admin()` is false in CLI |

Acorn never routes paths under wp-admin, `wp-login.php`, the registration URL, `/wp-json` or any path ending in `.php`. Language plugins that prefix URLs do not see a prefix on Livewire update requests; see `acorn-livewire`.

### Block editor saves (two requests)

The block editor saves post fields over REST (`POST /wp/v2/<type>/<id>`), then posts the classic meta boxes, ACF included, to `post.php?meta-box-loader=1` (`wp-admin/edit-form-blocks.php`).

- In the REST request, `wp_insert_post_data`, `transition_post_status` and `save_post` see the **old** meta-box values.
- In the meta-box request, `save_post` fires again **before** ACF stores the new values.
- Logic that needs new ACF values hooks `acf/save_post` at priority > 10; blocking rules go in `acf/validate_value` (both in `acf-native`).
- `save_post` also fires for autosaves and revisions: guard with `wp_is_post_autosave()` / `wp_is_post_revision()` and check the type (or use `save_post_{post_type}`).
- `wp_update_post()` inside `save_post` loops: unhook, update, re-hook, or change `$data` in `wp_insert_post_data` instead.

Content filters (`the_content` order, `wptexturize`, `wpautop`, kses, `pre_get_posts`): [references/filter-gotchas.md](references/filter-gotchas.md).

## Verification

```bash
{{runner.wp}} eval 'global $wp_filter; print_r(array_map(fn ($p) => array_keys($p), $wp_filter["save_post"]->callbacks ?? []));'
{{runner.wp}} eval 'var_dump(did_action("after_setup_theme"), did_action("init"));'
{{runner.cache}}
{{runner.test}}
```

Then exercise every request type the hook must cover (load the page, save in the block editor, call the route) and read the log. For timing questions, log `current_action()` and `did_action()` from the callback. Query Monitor's hooks panel helps when installed; the `$wp_filter` dump works everywhere.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Callback never runs | Registered after the hook fired: `plugins_loaded` / `setup_theme` from a provider, or `after_setup_theme` at a priority ≤ the boot priority | Move it to a bootstrap file or a later hook; compare with the table above |
| Provider hooks never run on one environment | Provider not registered, or skipped after an exception (logged as `Skipping provider`) | See `acorn-stack` |
| Filter result is `null` / empty | A code path without `return` | Return the value on every path |
| Parameters missing | `$accepted_args` too low | Set it to the number of parameters used |
| Runs twice on save | REST + meta-box requests, autosaves, revisions | Guard; move ACF-dependent logic to `acf/save_post` |
| Sees old ACF values on save | Hooked `save_post` in the REST request | `acf/save_post` priority > 10 |
| Infinite loop on save | `wp_update_post()` inside `save_post` | Unhook / re-hook or use `wp_insert_post_data` |
| `remove_action()` has no effect | Removed before it was added, different priority, closure, or a different object instance | Remove later with the same callable and priority; closures cannot be removed |
| Assets or head tags missing on an endpoint | Acorn route or REST request: template hooks do not run | Send what the response needs from the controller or component |
| Broken markup after a Tailwind arbitrary class | `wptexturize` treated part of the attribute as text | See `filter-gotchas.md`; fix the markup before disabling the filter site-wide |
| `app()` / facades fatal at file load | Called at file scope before Acorn booted (mu-plugin bootstrap file) | Call them inside callbacks that run after the boot |

## Escalation

Stop and ask when: the fix needs a hook earlier than the profile allows and no mu-plugin exists for it; a third-party callback must be removed and it is a closure; disabling a core filter (`wptexturize`, `wpautop`, kses) site-wide is the only option; the hook runs on shared remote infrastructure where testing means changing production data.

<!-- verified:
wp/wp-settings.php:506-548 — mu-plugins loop then muplugins_loaded; :565-566 core taxonomies/post types; :582-607 active plugins; :612 pluggable.php; :630 plugins_loaded; :705 setup_theme; :741-747 theme functions.php; :757 after_setup_theme; :766 $wp->init(); :779 init; :801 wp_loaded;
wp/wp-includes/load.php:986-994 — mu-plugins are top-level *.php only, sorted; :1096-1112 — wp_get_active_and_valid_themes lists the child (stylesheet) path before the parent (template);
wp/wp-includes/class-wp-hook.php:339-358 — iteration over priorities, foreach copies the running priority's callbacks;
wp/wp-includes/class-wp.php:148,418 — do_parse_request filter and parse_request action; :819-841 main() then fires wp;
wp/wp-includes/default-filters.php:549 — rest_api_loaded on parse_request; :350 wp_enqueue_scripts runs inside wp_head;
wp/wp-admin/edit-form-blocks.php:187-195 — meta boxes posted to post.php?meta-box-loader=1;
vendor/roots/acorn/src/Roots/Acorn/Application/Concerns/Bootable.php:212-245 — excluded admin/login/registration/REST/.php paths, matched routes handled on parse_request; :290-300 handleRequest exits;
refs/roots-sage/functions.php:35-61 — Sage boots Acorn, then loads app/setup.php and app/filters.php;
mu-plugin and project-root boot on after_setup_theme checked in a real Acorn mu-plugin main file and a Radicle-style project mu-plugin (concept only)
-->
