---
name: umbrella-blazor-register-nav-item
description: 'Add a nav item to the Blazor NavMenu.razor for a new feature, inside the correct AuthorizeView policy block and section, following the existing nav structure.'
---

# Register Blazor Nav Item

## Purpose

Add a navigation link for a new feature to `NavMenu.razor`, placed inside the correct `<AuthorizeView>` policy block and logical section group. Nav items are always controlled by `<AuthorizeView>` — they are only rendered for users who satisfy the policy, matching the `[Authorize]` policy applied to the index and manage pages.

## Discovery (read these before writing anything)

1. Read `Web\<AppName>.Web.Client\Layout\Shared\NavMenu.razor` in full to understand the existing structure — how sections are grouped with `<div class="nav-header">`, how `<AuthorizeView>` blocks are arranged by policy, and the naming/icon conventions.
2. Identify which `<AuthorizeView>` block matches the policy used by the new feature's index page. If no matching block exists, a new one must be added.
3. Note the icon library in use (typically FontAwesome) and choose an appropriate icon for the feature.

---

## Step 1 -- Locate the correct AuthorizeView block

Find the `<AuthorizeView Policy="@<AppName>PolicyNames.<Policy>">` block that matches the policy on the new feature's pages. The nav item goes inside this block.

```razor
<AuthorizeView Policy="@SharedPolicyNames.<Policy>" Context="<contextVarName>">
    <div class="nav-header">Section Name</div>
    <!-- existing items -->

    <!-- ADD HERE, in alphabetical order by label -->
    <div class="nav-item">
        <NavLink class="nav-link" href="/admin/<route-plural>">
            <i class="fas fa-<icon-name>" aria-hidden="true"></i>
            <span><Label></span>
        </NavLink>
    </div>
</AuthorizeView>
```

**Rules:**
- Place the new `<div class="nav-item">` in alphabetical order by label within the same contiguous group and authorization block. Preserve nested policy blocks and established section structure; do not globally reorder unrelated navigation while adding one item.
- The `href` must match the index page route exactly (e.g. `/admin/industries`).
- The `<span>` label is the human-readable plural name of the feature (e.g. `Industries`, `Career Quiz Questions`).
- `aria-hidden="true"` on the icon element is required for accessibility.
- Do not add a `<div class="nav-header">` unless creating an entirely new section — use the existing section header.

### If no matching AuthorizeView block exists

Add a new block at the appropriate position in the nav hierarchy:

```razor
<AuthorizeView Policy="@SharedPolicyNames.<Policy>" Context="<policy>Context">
    <div class="nav-header"><Section Name></div>
    <div class="nav-item">
        <NavLink class="nav-link" href="/admin/<route-plural>">
            <i class="fas fa-<icon-name>" aria-hidden="true"></i>
            <span><Label></span>
        </NavLink>
    </div>
</AuthorizeView>
```

The `Context` attribute value must be unique within the file — use a descriptive name (e.g. `siteSettingsContext`, `adminContext`).

---

## Step 2 -- Choose an icon

Use a FontAwesome Free icon that relates to the feature's subject matter. Browse at fontawesome.com/icons (free filter). Common examples from the codebase:

| Feature type | Icon |
|---|---|
| Industry / sector | `fa-industry` |
| People / users | `fa-users` |
| Documents | `fa-file-alt` |
| Settings | `fa-cog` |
| Education | `fa-graduation-cap` |
| Messages | `fa-envelope` |
| Charts / analytics | `fa-chart-bar` |
| Questions / quiz | `fa-question-circle` |

If unsure, check what icon an analogous existing feature uses.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The new `<div class="nav-item">` is inside a `<AuthorizeView>` block whose policy matches the `[Authorize]` attribute on the index and manage pages.
2. The `href` on the `<NavLink>` matches the index page route.
3. The item is in alphabetical order by label within its section.
4. The icon has `aria-hidden="true"`.
5. No new `<div class="nav-header">` was added unless the feature genuinely belongs to a new section that didn't previously exist.
6. Existing nested authorization blocks and unrelated navigation order were preserved; ordering was evaluated within the new item's actual contiguous peer group.
