---
name: superpowers-sage:wp-capabilities
description: >
  WordPress capabilities and roles — add_role, remove_role, add_cap, remove_cap,
  current_user_can, user_can, WP_Roles, custom capabilities, administrator editor
  author contributor subscriber, capability mapping, meta capabilities,
  map_meta_cap, register_post_type capabilities, custom post type capabilities,
  WP_User roles and caps, ACF field group visibility by role.
  Invoke for: custom roles, multi-role sites, restrict content by capability,
  map_meta_cap, "hide ACF field from role", "register capability for CPT".
user-invocable: false
---
# WordPress Capabilities and Authorization

## When to use

When implementing access control, permission checks, or role-based authorization in a Sage/Acorn project. This includes protecting REST API endpoints, restricting admin features, creating custom capabilities for custom post types, and bridging WordPress capabilities with Laravel-style Gates and Policies via Acorn.

## Inputs required

- The resource or action being protected (e.g., a CPT, an API endpoint, an admin page)
- The user roles that need access
- Whether custom capabilities are needed or built-in ones suffice
- Whether JWT middleware or Acorn guards are involved (cross-reference acorn-middleware)

## Procedure

### 1. Understand the capability hierarchy

WordPress authorization follows: **Roles -> Capabilities -> Meta Capabilities**.

- **Roles** are named collections of capabilities (administrator, editor, author, contributor, subscriber).
- **Capabilities** are granular permissions (edit_posts, manage_options, upload_files).
- **Meta capabilities** are virtual capabilities that map dynamically based on context (e.g., `edit_post` for a specific post maps to `edit_posts` or `edit_others_posts` depending on ownership).

### 2. Common capability groups

| Group | Capabilities |
|---|---|
| Options | `manage_options`, `manage_network_options` |
| Posts | `edit_posts`, `edit_others_posts`, `publish_posts`, `delete_posts`, `read_private_posts` |
| Pages | `edit_pages`, `edit_others_pages`, `publish_pages`, `delete_pages` |
| Users | `list_users`, `create_users`, `edit_users`, `delete_users`, `promote_users` |
| Uploads | `upload_files` |
| Plugins/Themes | `activate_plugins`, `edit_plugins`, `switch_themes`, `edit_themes` |

### 3. Check capabilities in code

```php
// In Service classes or controllers
if (current_user_can('edit_post', $post_id)) {
    // User can edit this specific post (meta capability — ownership checked)
}

if (current_user_can('manage_options')) {
    // User is an administrator
}
```

### 4. Register custom capabilities for CPTs (Poet)

When registering a CPT via Poet (`config/poet.php`), use `map_meta_cap` to enable granular capability mapping:

```php
// config/poet.php
'post' => [
    'project' => [
        'label' => 'Projects',
        'capability_type' => 'project',
        'map_meta_cap' => true,
        // This generates: edit_project, edit_projects, edit_others_projects,
        // publish_projects, delete_project, delete_projects, etc.
    ],
],
```

Then grant these capabilities to roles:

```php
// In a ServiceProvider boot() method
$editor = get_role('editor');
$editor->add_cap('edit_projects');
$editor->add_cap('edit_others_projects');
$editor->add_cap('publish_projects');
$editor->add_cap('delete_projects');
```

### 5. Role management

```php
// Add a custom role
add_role('project_manager', 'Project Manager', [
    'read' => true,
    'edit_projects' => true,
    'publish_projects' => true,
    'delete_projects' => true,
]);

// Remove a role
remove_role('project_manager');

// Add/remove capabilities from existing roles
$role = get_role('editor');
$role->add_cap('manage_project_settings');
$role->remove_cap('manage_project_settings');
```

**Important:** Role changes are written to the database. Run `add_role`/`add_cap` only once (e.g., on plugin activation or behind a version check), not on every request.

### 6. REST API permission callbacks

```php
register_rest_route('app/v1', '/projects', [
    'methods' => 'POST',
    'callback' => [$this, 'createProject'],
    'permission_callback' => function (\WP_REST_Request $request) {
        return current_user_can('publish_projects');
    },
]);
```

### 7. Map capabilities to JWT middleware guards

When using JWT authentication (see acorn-middleware), map WordPress capabilities to middleware guards:

```php
// In a middleware class
public function handle($request, Closure $next, string $capability)
{
    $user = wp_get_current_user();
    if (!$user->exists() || !$user->has_cap($capability)) {
        return response()->json(['error' => 'Forbidden'], 403);
    }
    return $next($request);
}

// Route registration
Route::middleware(['jwt.auth', 'capability:edit_projects'])
    ->post('/projects', [ProjectController::class, 'store']);
```

### 8. Gate/Policy pattern with Acorn

Use Laravel-style authorization on top of WordPress capabilities:

```php
// In AuthServiceProvider boot()
Gate::define('update-project', function ($user, $project) {
    return current_user_can('edit_post', $project->ID);
});

// Usage in controller
if (Gate::allows('update-project', $project)) {
    // Authorized
}
```

### 9. Meta capability mapping example

```php
add_filter('map_meta_cap', function (array $caps, string $cap, int $user_id, array $args) {
    if ($cap === 'edit_project') {
        $post = get_post($args[0]);
        if ((int) $post->post_author === $user_id) {
            return ['edit_projects'];
        }
        return ['edit_others_projects'];
    }
    return $caps;
}, 10, 4);
```

## Verification

1. Test with different user roles using `wp user create` and `wp role list` (WP-CLI).
2. Verify `current_user_can()` returns expected results for each role.
3. Confirm REST API endpoints return 403 for unauthorized users and 200 for authorized ones.
4. Check that custom CPT capabilities are properly mapped: `wp cap list editor`.
5. Use Query Monitor's "Capability Checks" panel to audit capability checks at runtime.

## Failure modes

- **Capabilities not persisting:** `add_cap()` writes to DB. If called repeatedly on every request, it causes unnecessary DB writes. Gate behind a version check or activation hook.
- **Meta capability not mapping:** Forgot `map_meta_cap => true` on CPT registration, so `current_user_can('edit_project', $id)` always returns false.
- **JWT user context missing:** `current_user_can()` returns false because `wp_set_current_user()` was not called after JWT validation. Ensure middleware sets user context.
- **Role removed but capabilities orphaned:** Removing a role does not remove its capabilities from users who were assigned that role. Clean up explicitly.
- **Super admin bypass:** In multisite, super admins bypass all capability checks. Account for this in testing.

## Escalation

- If capability checks pass in WP admin but fail in REST/Acorn routes, check that JWT middleware is correctly setting the WordPress current user before capability checks run.
- If custom CPT capabilities are not recognized, verify the CPT is registered with `capability_type` set to a unique slug and `map_meta_cap => true`.
- For complex multi-role authorization logic, consider whether Acorn Gates/Policies provide cleaner abstraction than raw `current_user_can()` checks scattered through code.
