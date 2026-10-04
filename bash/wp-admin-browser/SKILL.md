---
name: wp-admin-browser
description: "Use when a WordPress admin panel needs real browser interaction via Chrome DevTools MCP — logging in, navigating admin menus, clicking buttons, filling and submitting forms, creating/editing/deleting content through the UI, creating a temporary test admin user, verifying JS state or localStorage, capturing screenshots, or obtaining a REST nonce via admin-ajax.php. Triggers: \"open WP admin\", \"log in to WordPress\", \"navigate to Settings\", \"create a test user in admin\", \"click Save Changes\", \"fill in this form in the browser\", \"take a screenshot of the admin page\", \"upload media through the browser\", \"check the admin menu\", \"verify this in the browser\", \"use Chrome DevTools MCP\", \"fill_form in admin\", \"evaluate_script in admin\", \"admin panel is in maintenance mode\", \"get a REST nonce\", \"session expired re-login\", \"interact with the WP dashboard\", \"navigate to Plugins Add New\", \"test this in the actual admin UI\", \"create a temp admin account for testing\", \"check localStorage in admin\". Not for: headless automated testing without a browser — use `wp-plugin-testing`; PHP code changes that do not require browser interaction."
---

# WordPress Admin via Browser (Chrome DevTools MCP)

> **Model note:** Primarily MCP tool calls — navigate, fill, click. `haiku` works for simple CRUD flows. Complex UI sequences (multi-step forms, dynamic AJAX state) use `sonnet` to handle unexpected DOM states.

## When to use

- "Log in to the WordPress admin", "navigate to Settings > General", "create a test user".
- "Submit a form in WP admin", "upload a file via the media library", "save plugin settings".
- "Create a temporary admin account for testing instead of using the main admin user".
- "Verify a feature works end-to-end through the browser UI".

**Not for:** Headless automated testing without a real browser — use `wp-plugin-testing`. PHP code changes and plugin logic that don't require browser interaction.

## Core Rules — Non-Negotiable

1. **Never touch the main admin user.** Always create a temporary admin for testing.
2. **All data operations go through the browser UI.** No WP-CLI, no direct DB, no REST API calls to mutate data — use WordPress forms.
3. **Navigate via menus, not hardcoded URLs.** Click the menu item; don't jump straight to `/wp-admin/users.php?action=...`.
4. **Use `fill_form` + click for all inputs.** Never skip the form and post directly.

---

## Step 1 — Log In

```js
// POST to wp-login.php via fetch (fastest, no UI needed for login itself)
async () => {
  const res = await fetch('/wp-login.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      log: 'YOUR_USER',
      pwd: 'YOUR_PASS',
      'wp-submit': 'Log In',
      redirect_to: '/wp-admin/',
      testcookie: '1',
    }),
    credentials: 'include',
    redirect: 'follow',
  });
  return { ok: res.ok, url: res.url };
}
```

Login via `fetch` is acceptable because it's a pure auth step — no data mutation.

---

## Step 2 — Create a Temporary Admin User

**Always create a temp user before any testing that requires admin actions.**

Navigate to Users → Add New via menu clicks, not direct URL.

```
Admin menu → Users → Add New
```

Fill the form using `fill_form`:

| Field | Value |
|-------|-------|
| Username | `tmp_admin_<timestamp>` |
| Email | `tmp+<timestamp>@example.com` |
| First Name | `Temp` |
| Last Name | `Admin` |
| Role | `Administrator` |
| Password | strong generated password |
| Send notification | unchecked |

After testing: **delete the temp user** via Users list → hover → Delete.

---

## Step 3 — Get a REST Nonce (for read-only API calls only)

```js
async () => {
  return fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {
    credentials: 'include',
  }).then(r => r.text());
}
```

Use nonce only for **GET** requests to read data. All mutations go through WP forms.

---

## Browser Interaction Rules

### Navigation
```
✅ Click: Admin menu → Submenu item
❌ Never: navigate_page to hardcoded /wp-admin/edit.php?post_type=...
```

### Forms
```
✅ fill_form on visible fields → click Submit button
❌ Never: fetch POST directly to admin-post.php / admin-ajax.php for data changes
❌ Never: wp eval or wp post create via CLI for browser-visible operations
```

### Menus
Always wait for the page to load after each menu click before interacting with the next element.

---

## Data Operation Checklist

| Operation | Method |
|-----------|--------|
| Create post/page | Posts → Add New → fill form → Publish |
| Update user | Users → find user → Edit → fill form → Update |
| Delete item | List view → hover row → Delete (confirm dialog) |
| Change setting | Settings menu → fill field → Save Changes |
| Install plugin | Plugins → Add New → Search → Install → Activate |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using main admin for destructive tests | Create temp admin first |
| Navigating directly to `?action=delete&id=X` | Use list UI → Delete link |
| Using `wp user create` CLI to seed browser session | Use Add New User form |
| Skipping `fill_form` and posting via fetch | Always fill the visible form |
| Leaving temp admin after testing | Delete via Users list when done |

---

## JS State Verification

Use `evaluate_script` to inspect JavaScript state without touching the UI.

### Check scripts loaded + globals present

```js
() => ({
    // Verify a localized WP global is available
    myPlugin: typeof window.MY_PLUGIN,
    keys: Object.keys(window.MY_PLUGIN || {}),
    // Verify a library bundle loaded
    driverLoaded: !!window.driver?.js?.driver,
    // Check current URL
    url: location.href,
    hash: location.hash,
})
```

If `typeof window.MY_PLUGIN === 'undefined'` the script may not be enqueued for this screen, or the page is in maintenance mode (`document.title === 'Maintenance'`).

### SPA pages — always wait for React to render

```js
// Wrong: query DOM immediately after navigate
() => document.querySelector('.spa-element')  // returns null

// Right: wrap in setTimeout
() => new Promise(r => setTimeout(() => r(
    !!document.querySelector('.spa-element')
), 2000))
```

### Verify CSS selectors before committing

```js
() => {
    const selectors = [
        '#my-id',
        '.class-one.class-two',
        '.border-\\[\\#F0EDFB\\]',   // Tailwind escaped
    ];
    return selectors.map(s => ({
        selector: s,
        found: !!document.querySelector(s),
        count: document.querySelectorAll(s).length,
    }));
}
```

**Always test on the page where the selector is expected to exist.** A selector for the orders page returns `false` on the dashboard — that's not a bug.

### localStorage testing

```js
// Clear feature flags / completion state before testing
() => {
    Object.keys(localStorage)
        .filter(k => k.startsWith('myplugin_'))
        .forEach(k => localStorage.removeItem(k));
    return 'cleared';
}

// Read a specific key after an action
() => localStorage.getItem('myplugin_feature_completed')  // "true" or null
```

### Detect maintenance mode / redirect loop

If `navigate_page` lands on a blank page or unexpected content:

```js
() => ({ title: document.title, url: location.href })
// "Maintenance" title = WP in maintenance mode (.maintenance file or plugin)
// Redirected to /wp-login.php = session expired — re-login via fetch
```

### Re-login when session expires

```js
async () => {
    const res = await fetch('/wp-login.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            log: 'admin', pwd: 'admin',
            'wp-submit': 'Log In',
            redirect_to: '/wp-admin/',
            testcookie: '1',
        }),
        credentials: 'include',
        redirect: 'follow',
    });
    return { ok: res.ok, url: res.url };
}
```

---

## References

- [Chrome DevTools MCP tools](references/chrome-devtools-tools.md) — full tool params, interaction sequence template, priority rules
- [WordPress admin navigation](references/wp-admin-navigation.md) — menu paths, form submit patterns, success strings
- [Browser debug patterns](references/browser-debug-patterns.md) — console error capture, network request inspection, evaluate_script debug snippets, screenshot strategy, PHP error detection

---

## Cleanup

After every test session:
1. Log in as main admin (or existing admin).
2. Users → find all `tmp_admin_*` users → bulk delete.
3. Do **not** reassign their content (temp users have no content).
