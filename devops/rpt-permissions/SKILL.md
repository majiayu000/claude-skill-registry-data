---
name: rpt-permissions
description: Configure RPT token exchange and permission-based authorization for affolterNET.Web.Bff. Use when setting up Keycloak permissions, resource policies, or fine-grained access control.
---

# RPT Permissions

Configure Keycloak RPT-based permission authorization.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Overview

RPT (Requesting Party Token) enables fine-grained permissions:
1. User authenticates and gets access token
2. BFF exchanges access token for RPT
3. RPT contains granted permissions
4. Controllers authorize based on permissions

## Quick Start

### Enable Authorization Mode

```csharp
var options = builder.Services.AddBffServices(isDev, config, opts => {
    opts.ConfigureBff = bff => {
        bff.AuthMode = AuthenticationMode.Authorize;
    };
});
```

### Use Permission Policies

```csharp
[Authorize(Policy = "admin-resource")]
[HttpGet("admin")]
public IActionResult AdminOnly() => Ok();

// Multiple permissions (any match)
[Authorize(Policy = "admin-resource,manager-resource")]
[HttpGet("management")]
public IActionResult Management() => Ok();
```

## Keycloak Configuration

### Resource Setup

1. Enable "Authorization" on your client
2. Create Resources (e.g., "admin-resource", "user-resource")
3. Create Scopes (e.g., "view", "manage", "create")
4. Create Policies (role-based, user-based, etc.)
5. Create Permissions linking policies to resources/scopes

### Permission Structure

```json
{
  "permissions": [
    {
      "rsname": "admin-resource",
      "scopes": ["view", "manage"]
    },
    {
      "rsname": "user-resource",
      "scopes": ["read", "create"]
    }
  ]
}
```

## Permission Checking in Code

### Using RequirePermission Attribute (Recommended)

```csharp
// Single permission
[RequirePermission("admin-resource:view")]
public IActionResult AdminView() { ... }

// Multiple permissions (any match)
[RequirePermission("admin-resource:manage", "user-resource:delete")]
public IActionResult AdminManage() { ... }
```

### Using Authorize Policy (Alternative)

```csharp
// Single permission
[Authorize(Policy = "admin-resource:view")]
public IActionResult AdminView() { ... }

// Multiple permissions (comma-separated)
[Authorize(Policy = "admin-resource:manage,user-resource:delete")]
public IActionResult AdminManage() { ... }
```

**Note:** `RequirePermission` is a convenience wrapper that sets the Policy internally.

### Programmatic Check

```csharp
public class MyController : ControllerBase
{
    public IActionResult ConditionalAction()
    {
        var permissions = User.FindAll("permission")
            .Select(c => c.Value);

        if (permissions.Contains("admin-resource:manage"))
        {
            // Admin-specific logic
        }

        return Ok();
    }
}
```

## SPA Permission Checking

```typescript
// Auth store
const useAuthStore = defineStore('auth', {
    state: () => ({
        permissions: [] as { resource: string; action: string }[]
    }),
    actions: {
        hasPermission(resource: string, action: string): boolean {
            return this.permissions.some(
                p => p.resource === resource && p.action === action
            );
        }
    }
});

// Component usage
<template>
    <button v-if="authStore.hasPermission('admin-resource', 'manage')">
        Admin Action
    </button>
</template>
```

## Permission Claims Format

When the RPT middleware processes permissions, it adds claims to the user identity:

| Property | Value |
|----------|-------|
| Claim Type | `"permission"` |
| Claim Value | `"{resource}:{scope}"` |

Examples: `"admin-resource:view"`, `"user-resource:create"`

## Caching

RPT tokens are cached per user to avoid repeated Keycloak calls:

```json
{
  "affolterNET": {
    "Web": {
      "PermissionCache": {
        "ExpirationMinutes": 5
      }
    }
  }
}
```

## Troubleshooting

### Permissions not recognized
- Verify `AuthMode` is `Authorize`
- Check Keycloak client has Authorization enabled
- Ensure resources/permissions are configured
- Review RPT token contents in jwt.io

### Permission denied unexpectedly
- Check policy evaluation in Keycloak
- Verify user has required role for policy
- Review permission-to-policy mappings

### RPT exchange fails
- Verify client credentials are correct
- Check Keycloak authorization services are enabled
- Review Keycloak logs for errors
