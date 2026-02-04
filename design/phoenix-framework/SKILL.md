---
name: phoenix-framework
description: Phoenix framework guidelines for router configuration and deprecated modules. Use when writing Phoenix router files, adding routes, or configuring scopes. Prevents duplicate module prefix bugs from scope aliasing and use of deprecated Phoenix.View.
---

# Phoenix Framework Guidelines

## Router Scope Aliasing

Router `scope` blocks include an optional alias that is **automatically prefixed** to all routes within the scope.

**Never** create your own `alias` for route definitions—the scope provides it:

```elixir
scope "/admin", AppWeb.Admin do
  pipe_through :browser

  live "/users", UserLive, :index
end
```

The `UserLive` route points to `AppWeb.Admin.UserLive` automatically.

**Always** be mindful of this when creating routes to avoid duplicate module prefixes like `AppWeb.Admin.Admin.UserLive`.

## Deprecated Modules

- **Never** use `Phoenix.View` - it is no longer included with Phoenix
