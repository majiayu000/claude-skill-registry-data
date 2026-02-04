---
name: login-redirector
description: Handle WordPress login/logout redirects. Use when implementing custom redirect logic.
---

# Login Redirector

## Instructions

When setting up login or logout redirects:

1. **Login redirect**: Use `login_redirect` filter
2. **Logout redirect**: Use `logout_redirect` filter
3. **Parameters**: Both receive `$redirect_to`, `$request`, `$user`
4. **Return the redirect URL**

## Filter Parameters

```php
add_filter('login_redirect', $callback, 10, 3);
add_filter('logout_redirect', $callback, 10, 3);

/**
 * @param string $redirect_to The redirect destination URL
 * @param string $request The requested redirect destination URL
 * @param WP_User|WP_Error|null $user The logged-in user or error
 */
```

## Common Patterns

### 1. Redirect by User Role

```php
add_filter('login_redirect', 'retrologin_redirect_by_role', 10, 3);
function retrologin_redirect_by_role(string $redirect_to, string $request, $user): string {
    if ($user instanceof WP_User) {
        if (user_can($user, 'administrator')) {
            return admin_url();
        }
        return home_url('/dashboard/');
    }
    return $redirect_to;
}
```

### 2. Keep Requested URL

```php
add_filter('login_redirect', 'retrologin_keep_request', 10, 3);
function retrologin_redirect_keep_request(string $redirect_to, string $request, $user): string {
    // Use the page they were trying to access
    if (!empty($request) && strpos($request, 'wp-admin') === false) {
        return $request;
    }
    return $redirect_to;
}
```

### 3. Custom Logout Redirect

```php
add_filter('logout_redirect', 'retrologin_logout_redirect', 10, 3);
function retrologin_logout_redirect(string $redirect_to, string $requested_redirect_to, $user): string {
    return home_url('/thank-you/');
}
```

## Guidelines

-   Always check if `$user` is a valid WP_User
-   Handle WP_Error cases (failed login)
-   Return `$redirect_to` as fallback
-   Test redirects with different user roles
