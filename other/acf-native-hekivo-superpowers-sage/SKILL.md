---
name: acf-native
description: Use when building or reviewing ACF field behaviour or the post save flow - validate before publish, required/maxlength settings, hiding a field (conditional_logic), dynamic choices, running code after save - acf/validate_value, acf/load_field, acf/prepare_field, acf/save_post, acf.getField, wp_insert_post_data, save_post - including projects where ACF may not be installed (Radicle). Maps each need to the native mechanism verified in local source. For ACF Composer scaffolding use acorn-scaffolding; for escaping ACF output use wp-security-escaping.
---

# ACF and WordPress: native first

Most "new" behaviour around fields already exists as a field setting, an ACF hook or a WordPress hook. Re-implementing it duplicates ACF, splits the rule in two places and usually breaks in the block editor. This skill names the native mechanism, makes you check it in the installed source, and only then allows custom code.

Runner commands are written as placeholders filled from the session context: `{{runner.wp}}` (Lando default `lando wp`), `{{runner.acorn}}` (`lando wp acorn`), `{{runner.composer}}` (`lando composer`), `{{runner.cache}}` (the project's cache-clear command). Never run `wp`, `composer` or `php` on the host.

## When to use

- Validating field values before publish (cross-field rules, external data, limits).
- Choices that depend on data, hiding or locking a field per user/state, computed values.
- Logic that must run after ACF stored the values, or on saves that never post the ACF form.
- Admin or block-editor JavaScript that touches ACF fields.
- Reviewing code for custom endpoints, meta boxes or editor hooks that duplicate ACF.

## Inputs required

- The need in one sentence ("block publishing when the external ID is already used").
- The active profile and app path from the session context.
- Whether ACF (Pro) is installed and its version: `{{runner.wp}} plugin list --name=advanced-custom-fields-pro --fields=name,status,version` (or `advanced-custom-fields`).
- Where the field group is defined (ACF Composer class, local JSON, or the admin UI).

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Detect ACF first, before naming any `acf/*` hook.** Look at `site.versions` in the session context, the lock file (`composer.lock` entries `wpengine/advanced-custom-fields-pro`, `*/advanced-custom-fields`) and the plugins folder. Say what you found.
   - **ACF absent** (the default on `radicle-app`): solve it with native WordPress and stop there. Register the fields with `register_post_meta()` (`show_in_rest`, `single`, `type`, a `sanitize_callback` and an `auth_callback`); block publish-only with `rest_pre_insert_{post_type}` returning a `WP_Error` (the block editor saves through REST; new meta values are in `$request['meta']`, fall back to stored meta; check only when the target status is `publish` or `future`, so drafts still save) plus `wp_insert_post_data` for classic, quick-edit and CLI saves (keep the post a draft instead of publishing). Register both from a service provider (on `radicle-app`, one listed in `composer.json` `extra.acorn.providers`). Be honest about the UI: the `WP_Error` message shows as an editor notice that names the field, not inline under it. Recommend adding ACF only if the user asks for an admin field UI or inline field errors, and then through the project's Composer registry (wp-packages.org `wp-plugin/*` by default; see `wp-composer-plugins`), never wpackagist unless the project already uses it.
   - **ACF present**: continue with step 2.
2. **Name the need** in one sentence.
3. **Find the mechanism** in the table below, then the signature in [references/hooks.md](references/hooks.md) or [references/js-api.md](references/js-api.md).
4. **Verify the behaviour in the installed source**, not from memory (paths relative to the WordPress content dir and the core dir):
   - ACF PHP: `plugins/advanced-custom-fields-pro/includes/validation.php`, `acf-field-functions.php`, `acf-value-functions.php`, `acf-form-functions.php`, `forms/form-post.php`.
   - ACF JS: `plugins/advanced-custom-fields-pro/assets/build/js/acf-input.min.js` (minified; search for the action or filter name).
   - WordPress: `wp-includes/post.php` (`wp_insert_post`, `register_post_meta`), `wp-includes/meta.php` (`register_meta`), `wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php` (`rest_pre_insert_{post_type}`), `wp-admin/includes/post.php` (`edit_post`). Name the file and line you checked in the answer.
5. **Implement with the native mechanism.** Field rules belong in the field definition (ACF Composer `app/Fields/**` or local JSON). Hooks go in a service provider `boot()` (or the project's bootstrap `filters.php` / `actions.php`) and delegate to a class in `app/`.
6. **Custom code only for a real gap** (example: ACF does not validate quick edit, bulk edit, WP-CLI or REST saves). Write the reason in the issue or PR ("Native APIs used") and in a code comment next to the custom code.
7. **Audit**: tell the user to run `node scripts/audit-native.mjs <app-path>` (script path relative to this skill folder; pass the detected app path, `.` on `radicle-app`) and run it yourself when you can. Read every finding you introduced. Output is JSON: `tool`, `findings[]`, `notes[]`.
8. Clear caches after PHP changes: `{{runner.cache}}`.

### Profiles

| | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| ACF present | usually (ACF Pro via Composer) | usually (ACF Pro via Composer) | **not installed by default**; confirm before using any `acf/*` hook |
| Field definitions | theme `app/Fields/**` (ACF Composer) or local JSON | plugin `app/Fields/**` (ACF Composer) | register meta natively (`register_post_meta` with `show_in_rest`) and block attributes; add ACF only if the project chose it |
| Where hooks go | theme provider `boot()` or `app/filters.php` | plugin provider `boot()` or the plugin's bootstrap `filters.php` / `actions.php` | provider listed in `composer.json` `extra.acorn.providers` |
| Native-first still applies to | ACF + WordPress hooks | ACF + WordPress hooks | WordPress hooks only: `wp_insert_post_data`, `rest_pre_insert_{post_type}`, `register_post_meta` `sanitize_callback` / `auth_callback`, block attributes |

### Need → native mechanism

| Need | Use | Not |
|---|---|---|
| Required, max length, number range, min/max rows | Field settings: `required`, `maxlength`, `min`/`max`, repeater `min`/`max` | Re-checking them in a custom endpoint or JS |
| Business validation on save (cross-field, external data) | `acf/validate_value/key={field_key}` returning `true` or a message; sibling values from `$_POST['acf'][<field_key>]`; form-level errors through `acf/validate_save_post` + `acf_add_validation_error()` | `editor.preSavePost`, a custom "check" endpoint |
| Choices that depend on data | `acf/load_field/key=…` (prefer `key=`: unique and unaffected by other code filtering by `name=`) | Hard-coded choices, JS that injects options |
| Hide or lock a field per context | `acf/prepare_field[/key=…]` returning `false` hides it; `readonly` / `disabled` settings | CSS such as `acf-hidden` (it does not hide on its own) |
| Value nobody types (hashes, timestamps, flags) | Plain post meta written by code | A readonly ACF field |
| Show/hide inside one field group | `conditional_logic` in the field definition | JS |
| Show/hide across field groups | ACF JS API (`acf.getField()`, `ready_field/key=…`) | Page reloads |
| Transform before storing / after reading | `acf/update_value[/key=…]`, `acf/format_value[/key=…]`, defaults with `acf/load_value` | Post-processing in templates |
| Logic that needs the saved values | `acf/save_post` priority > 10 (ACF stores values at 10); priority < 10 sees only `$_POST['acf']` | `save_post` / `wp_insert_post_data` during the block editor REST request (old meta) |
| Rule on saves without the ACF form (quick/bulk edit, CLI, REST) | `wp_insert_post_data` / `transition_post_status`, skipping requests that carry `$_POST['acf']` | Assuming ACF validation runs there (it does not) |
| Assets for screens with ACF forms | `acf/input/admin_enqueue_scripts` + `get_current_screen()` check | `admin_enqueue_scripts` on every admin page |
| Editor behaviour in JS | `acf.addFilter('select2_args')`, `acf.addAction('ready_field/key=…')`, `field.val()`, repeater `add()` / `remove($row)` / `$rows()` | Raw DOM edits of ACF markup |
| Expose field groups and content to AI agents | ACF 6.8 Abilities (`acf/settings/enable_acf_ai`, per-item `allow_ai_access`); see wp-abilities-mcp | Custom REST endpoints that describe fields |

Depth: [references/save-flow.md](references/save-flow.md) (classic vs block editor sequence), [references/traps.md](references/traps.md), [references/docs.md](references/docs.md).

## Verification

- The rule fires where expected: publish in the block editor (validation error on the field), save a draft (no validation), quick edit (only your WordPress-hook guard runs).
- `node scripts/audit-native.mjs <app-path>` shows no new finding without a written reason.
- `{{runner.wp}} eval 'var_dump(has_filter("acf/validate_value/key=field_x"));'` returns a priority, not `false` (the provider booted).
- Tests, if the project has them, cover the validator class (`{{runner.test}}`).

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Validation does not run when saving a draft | ACF's block-editor wrapper validates only when the target status is `publish` or `future`; autosave and preview skip it | Expected; enforce draft rules with a WordPress hook if they really matter |
| A guard on `wp_insert_post_data` rejects a valid first publish | The block editor sends the REST request first, before the meta-box request carries `$_POST['acf']`; meta is still old | Validate with `acf/validate_value`; react in `acf/save_post` > 10; skip the REST request in the guard |
| `acf/save_post` handler reads old values | Priority below 10 | Use priority 20 (or read `$_POST['acf']` deliberately) |
| Filter on `name=` stops working or fights another plugin/theme | Several fields share the name, or other code filters the same name | Use `/key=field_…` |
| Field "hidden" with `acf-hidden` still renders | The class alone does not hide | `acf/prepare_field` returning `false`, or make it code-managed meta |
| JSON stored with `update_post_meta()` is corrupted | Meta functions unslash the value | `update_post_meta($id, $key, wp_slash($json))` |
| `acf/*` hooks never fire on `radicle-app` | ACF is not installed | Use `register_post_meta` + `rest_pre_insert_{post_type}` / `wp_insert_post_data` (step 1); add ACF only on request, through the project's registry (wp-composer-plugins) |
| Renamed ACF Composer group loses data | Field keys derive from group + field names; `_<name>` reference meta is orphaned | Plan renames with a migration that rewrites the reference meta |

## Escalation

- Hook timing or "which request runs this hook": wp-hooks-lifecycle.
- Creating the field group, block or options page class: acorn-scaffolding.
- Escaping and sanitising the values on output: wp-security-escaping.
- The mechanism seems missing in the installed version: check the ACF changelog for the installed version through docs-brain before writing custom code, and tell the user which gap you found.

<!-- verified:
wp-content/plugins/advanced-custom-fields-pro/includes/validation.php:357-360 — validate_value type/name/key/generic filters with ($valid,$value,$field,$input);
validation.php:223 — acf_add_validation_error($input,$message); :257 do_action('acf/validate_save_post'); :38 wp_ajax_acf/validate_save_post;
includes/acf-field-functions.php:70,81 — acf/load_field + type/name/key variations; :568,575 acf/prepare_field + variations;
includes/acf-value-functions.php:146 load_value ($value,$post_id,$field); :200 format_value adds $escape_html; :244 update_value ($value,$post_id,$field,$original);
includes/acf-form-functions.php:139-152 — acf_save_post kses-filters $_POST['acf'] for users without unfiltered_html, then do_action('acf/save_post'); :180 _acf_do_save_post at default priority 10;
includes/forms/form-post.php:42 — ACF saves on save_post priority 10;
includes/assets.php:394 — do_action('acf/input/admin_enqueue_scripts');
assets/build/js/acf-input.min.js — savePost wrapper: validates only when status is publish/future, skips isAutosave/isPreview; "<action>_field/key=" variations built for ready/append/etc.;
acf.php:185 — enable_acf_ai default false; src/AI/AI.php:30-46 Abilities only when enabled;
radicle-app facts checked against a licensed local Radicle project; not reproduced here;
wp/wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php:1531 — rest_pre_insert_{post_type}($prepared_post,$request); :750-754,951-955 a WP_Error from prepare_item_for_database aborts create/update;
wp/wp-includes/post.php:2812 register_post_meta; meta.php:1449-1450,1512-1525 sanitize_callback/auth_callback defaults and sanitize_{type}_meta_{key}_for_{subtype} filter; post.php:4978 wp_insert_post_data($data,$postarr,$unsanitized_postarr,$update).
-->
