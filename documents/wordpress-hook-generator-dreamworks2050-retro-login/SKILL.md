---
name: wordpress-hook-generator
description: Generate WordPress actions and filters with proper naming conventions. Use when creating hooks for the login page or plugin functionality.
---

# WordPress Hook Generator

## Instructions

When the user wants to add a WordPress hook:

1. **Determine hook type**:

    - **Action** (`add_action`): Performs an action, no return value
    - **Filter** (`add_filter`): Modifies data, must return a value

2. **Apply naming convention**:

    - Prefix: `retrologin_`
    - Example: `retrologin_login_head`, `retrologin_custom_message`

3. **Create callback function**:

    - Use namespace: `Retrologin\`
    - Or use string callback: `'retrologin_callback'`

4. **Register the hook**:
    - Actions: `add_action('hook_name', 'callback', priority, args)`
    - Filters: `add_filter('hook_name', 'callback', priority, args)`

## Example

```php
// Action: Enqueue assets on login page
add_action('login_enqueue_scripts', 'retrologin_enqueue_assets');

function retrologin_enqueue_assets(): void {
    wp_enqueue_style('retrologin-login', plugins_url('dist/assets/login.css', __FILE__));
}

// Filter: Change logo URL
add_filter('login_headerurl', 'retrologin_login_logo_url');

function retrologin_login_logo_url(): string {
    return home_url('/');
}
```

## Common Login Hooks

| Hook                    | Type   | Purpose              |
| ----------------------- | ------ | -------------------- |
| `login_enqueue_scripts` | Action | Enqueue CSS/JS       |
| `login_headerurl`       | Filter | Logo link URL        |
| `login_headertitle`     | Filter | Logo title text      |
| `login_message`         | Filter | Message above form   |
| `login_footer_text`     | Filter | Footer text          |
| `login_redirect`        | Filter | Redirect after login |
