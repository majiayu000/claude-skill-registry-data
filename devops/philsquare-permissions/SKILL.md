---
name: Philsquare Permissions
description: This skill should be used when the user asks to "add permissions to a policy", "create a policy with roles", "set up role permissions", "configure rolePermissions", "use BasePolicy", or when working with Laravel policies that need role-based permission management. Also activate when creating or modifying policies in a project using philsquare/permissions.
---

# Philsquare Permissions Package

This skill provides guidance for implementing role-based permissions through Laravel policies using the philsquare/permissions package.

## Package Detection

Check if the project uses this package by looking for:
- `philsquare/permissions` in `composer.json`
- Policies extending `Philsquare\Permissions\BasePolicy`
- A `rolePermissions()` method in existing policies

## Core Concepts

### BasePolicy

All policies requiring role-based permissions must extend `BasePolicy`:

```php
use Philsquare\Permissions\BasePolicy;

class PostPolicy extends BasePolicy
{
    public function rolePermissions(): array
    {
        return [
            'admin' => $this->permissions()->all(),
        ];
    }

    // Policy methods...
}
```

### How Authorization Works

1. User calls `$user->can('update', $post)` or `Gate::authorize('update', $post)`
2. Laravel routes to the policy's `update()` method
3. `BasePolicy::before()` runs first, checking if user's roles have the permission
4. If permission exists (`post:update`), the policy method executes
5. If permission missing, access denied immediately

The `before()` hook converts:
- Policy class: `PostPolicy` to `post`
- Method: `updateEta` to `update-eta`
- Combined: `post:update-eta`

### Permission Naming Convention

Permissions are stored in kebab-case: `{model}:{action}`

| Policy Method | Database Permission |
|---------------|---------------------|
| `viewAny()` | `model:view-any` |
| `forceDelete()` | `model:force-delete` |
| `updateEta()` | `model:update-eta` |

## The rolePermissions() Method

Define which roles can access which policy methods:

```php
public function rolePermissions(): array
{
    return [
        'admin' => $this->permissions()->all(),
        'manager' => $this->permissions()->crud(['approve', 'reject']),
        'editor' => $this->permissions()->only(['viewAny', 'view', 'update']),
        'viewer' => $this->permissions()->only(['viewAny', 'view']),
    ];
}
```

## Permission Helpers

Access via `$this->permissions()` in any policy extending BasePolicy.

### `all()`
Returns all public methods (excluding system methods like `before`, `allow`, `deny`).

### `crud(array $additional = [])`
Returns: `viewAny`, `view`, `create`, `update`, `delete` plus any additional methods.

```php
$this->permissions()->crud(['publish', 'archive'])
// Returns: viewAny, view, create, update, delete, publish, archive
```

### `only(array $methods)`
Returns only the specified methods.

```php
$this->permissions()->only(['viewAny', 'view'])
```

### `except(array $methods)`
Returns all methods except specified ones.

```php
$this->permissions()->except(['delete', 'forceDelete'])
```

## Policy Method Implementation

Policy methods define business logic for when actions are allowed:

```php
public function update(User $user, Order $order): bool
{
    // Role check happens in before() hook
    // This method handles additional business logic
    return $order->status === 'draft';
}
```

Return `true` to allow, `false` to deny. The role permission check happens first in `before()`.

## Syncing Permissions

After modifying policies, run:

```bash
php artisan permissions:refresh
```

This scans all policies extending BasePolicy and syncs role-permission mappings to the database.

**Add to deployment scripts** to auto-sync on deploy.

## Defining Roles

Roles are created automatically when `permissions:refresh` runs. Use an enum for type safety:

```php
namespace App\Enums;

enum Roles: string
{
    case Admin = 'admin';
    case Manager = 'manager';
    case Editor = 'editor';
}
```

Use in policies:

```php
use App\Enums\Roles;

public function rolePermissions(): array
{
    return [
        Roles::Admin->value => $this->permissions()->all(),
    ];
}
```

## Additional Resources

For detailed helper documentation, consult:
- **`references/permission-helpers.md`** - Complete helper method reference with examples
