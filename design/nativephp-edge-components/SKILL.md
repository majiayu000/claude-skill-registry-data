---
name: NativePHP EDGE Components
description: This skill should be used when the user asks about "EDGE component", "native-top-bar", "native-bottom-nav", "native-side-nav", "native-fab", "native ui component", "TopBar", "BottomNav", "SideNav", "Fab component", "native navigation", "nativephp-safe-area", "safe area insets", or needs to implement native UI elements that render natively on device.
version: 0.1.0
---

# NativePHP EDGE Components

This skill provides guidance for using EDGE (Element Definition and Generation Engine) components to render truly native UI elements in NativePHP Mobile apps.

## Overview

EDGE components are Blade components that generate JSON structures passed to the native layer, which renders platform-specific UI (iOS/Android). They provide native look and feel while being defined in PHP/Blade.

## How EDGE Works

1. Blade components (e.g., `<native:top-bar>`) render JSON structure
2. JSON is passed via HTTP header to native layer
3. Native code renders platform-appropriate UI
4. The `RenderEdgeComponents` middleware handles this automatically

## Safe Area Handling

Mobile devices have notches, rounded corners, and home indicators. Handle these with:

### CSS Class

Apply the `nativephp-safe-area` class to your main container:

```html
<body class="nativephp-safe-area">
    <!-- Content respects device safe areas -->
</body>
```

### CSS Variables

For custom layouts, use safe area CSS variables:

```css
.my-element {
    padding-top: var(--inset-top);
    padding-bottom: var(--inset-bottom);
    padding-left: var(--inset-left);
    padding-right: var(--inset-right);
}
```

### Viewport Configuration

For edge-to-edge rendering:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

## TopBar Component

Native top navigation bar with title and action buttons.

### Basic Usage

```blade
<native:top-bar title="Dashboard" />
```

### Full Example

```blade
<native:top-bar
    title="My App"
    subtitle="Welcome back"
    :show-navigation-icon="true"
    background-color="#1a1a2e"
    text-color="#ffffff"
    :elevation="4"
>
    <native:top-bar-action
        id="search"
        icon="search"
        label="Search"
        :url="route('search')"
    />
    <native:top-bar-action
        id="settings"
        icon="settings"
        label="Settings"
        :url="route('settings')"
    />
</native:top-bar>
```

### TopBar Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | string | Main heading text |
| `subtitle` | string | Secondary text below title |
| `show-navigation-icon` | bool | Show back/menu button (default: true) |
| `background-color` | string | Hex color for background |
| `text-color` | string | Hex color for text |
| `elevation` | int | Shadow depth 0-24 (Android only) |

### TopBarAction Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (required) |
| `icon` | string | Icon name (required) |
| `label` | string | Accessibility text and overflow menu text |
| `url` | string | Navigation target when tapped |
| `event` | string | Livewire event to dispatch instead of navigation |

**Action limits**: Android shows first 3 as icons, rest in overflow. iOS shows up to 5, then overflow.

## BottomNav Component

Native bottom navigation bar with tab items.

### Basic Usage

```blade
<native:bottom-nav>
    <native:bottom-nav-item
        id="home"
        icon="home"
        label="Home"
        :url="route('home')"
        :active="request()->routeIs('home')"
    />
    <native:bottom-nav-item
        id="search"
        icon="search"
        label="Search"
        :url="route('search')"
        :active="request()->routeIs('search')"
    />
    <native:bottom-nav-item
        id="profile"
        icon="person"
        label="Profile"
        :url="route('profile')"
        :active="request()->routeIs('profile')"
    />
</native:bottom-nav>
```

### BottomNav Properties

| Property | Type | Description |
|----------|------|-------------|
| `dark` | bool | Dark mode styling |
| `label-visibility` | string | When to show labels |

### BottomNavItem Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (required) |
| `icon` | string | Icon name (required) |
| `label` | string | Tab label (required) |
| `url` | string | Navigation URL (required) |
| `active` | bool | Whether tab is currently selected |
| `badge` | string | Badge text (e.g., notification count) |
| `badge-color` | string | Hex color for badge |
| `news` | bool | Show news indicator dot |

## SideNav Component

Native side/drawer navigation.

### Basic Usage

```blade
<native:side-nav>
    <native:side-nav-header
        title="My App"
        subtitle="user@example.com"
        icon="account_circle"
    />

    <native:side-nav-item
        id="dashboard"
        icon="dashboard"
        label="Dashboard"
        :url="route('dashboard')"
        :active="request()->routeIs('dashboard')"
    />

    <native:horizontal-divider />

    <native:side-nav-group heading="Settings" icon="settings">
        <native:side-nav-item
            id="account"
            icon="person"
            label="Account"
            :url="route('account')"
        />
        <native:side-nav-item
            id="preferences"
            icon="tune"
            label="Preferences"
            :url="route('preferences')"
        />
    </native:side-nav-group>
</native:side-nav>
```

### SideNav Properties

| Property | Type | Description |
|----------|------|-------------|
| `dark` | bool | Dark mode styling |
| `label-visibility` | string | When to show labels |
| `gestures-enabled` | bool | Enable swipe to open |

### SideNavHeader Properties

| Property | Type | Description |
|----------|------|-------------|
| `title` | string | Header title |
| `subtitle` | string | Header subtitle |
| `icon` | string | Icon name |
| `background-color` | string | Hex background color |
| `image-url` | string | Background image URL |
| `event` | string | Livewire event on tap |
| `show-close-button` | bool | Show close button |
| `pinned` | bool | Keep header visible when scrolling |

### SideNavItem Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (required) |
| `icon` | string | Icon name (required) |
| `label` | string | Item label (required) |
| `url` | string | Navigation URL (required) |
| `active` | bool | Whether item is selected |
| `badge` | string | Badge text |
| `badge-color` | string | Badge color |
| `open-in-browser` | bool | Open URL in external browser |

### SideNavGroup Properties

| Property | Type | Description |
|----------|------|-------------|
| `heading` | string | Group heading text (required) |
| `icon` | string | Group icon |
| `expanded` | bool | Whether group is expanded |

## Fab (Floating Action Button) Component

Floating action button for primary actions.

### Basic Usage

```blade
<native:fab
    icon="add"
    :url="route('create')"
/>
```

### Full Example

```blade
<native:fab
    icon="add"
    label="Create New"
    :url="route('create')"
    size="large"
    position="bottom-end"
    :bottom-offset="16"
    :elevation="6"
    :corner-radius="16"
    container-color="#6200ee"
    content-color="#ffffff"
/>
```

### Fab Properties

| Property | Type | Description |
|----------|------|-------------|
| `icon` | string | Icon name (required) |
| `label` | string | Extended FAB label |
| `url` | string | Navigation URL |
| `event` | string | Livewire event to dispatch |
| `size` | string | 'small', 'regular', 'large' |
| `position` | string | 'bottom-start', 'bottom-end', etc. |
| `bottom-offset` | int | Pixels from bottom |
| `elevation` | int | Shadow depth |
| `corner-radius` | int | Corner rounding |
| `container-color` | string | Background hex color |
| `content-color` | string | Icon/text hex color |

## HorizontalDivider Component

Visual separator between items.

```blade
<native:horizontal-divider />
```

## Available Icons

EDGE components use Material Design icons. Common icons:

- Navigation: `home`, `menu`, `arrow_back`, `close`, `search`
- Actions: `add`, `edit`, `delete`, `share`, `settings`
- Communication: `email`, `chat`, `notifications`, `phone`
- Content: `folder`, `file_copy`, `link`, `cloud`
- Social: `person`, `group`, `account_circle`
- Media: `play_arrow`, `pause`, `camera`, `mic`

Full list: https://fonts.google.com/icons

## Combining EDGE with Web Content

EDGE components render natively while your web content renders in the WebView:

```blade
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body class="nativephp-safe-area">
    {{-- Native top bar --}}
    <native:top-bar title="My App">
        <native:top-bar-action id="menu" icon="menu" />
    </native:top-bar>

    {{-- Web content --}}
    <main class="p-4">
        @yield('content')
    </main>

    {{-- Native bottom nav --}}
    <native:bottom-nav>
        <native:bottom-nav-item id="home" icon="home" label="Home" :url="route('home')" />
        <native:bottom-nav-item id="profile" icon="person" label="Profile" :url="route('profile')" />
    </native:bottom-nav>
</body>
</html>
```

## EDGE with Inertia/Vue/React Apps

**Important**: When using Inertia.js with Vue or React, EDGE components MUST be placed in the `app.blade.php` layout file, NOT in your JavaScript components.

### Why?

EDGE components are Blade components that generate JSON passed via HTTP headers to the native layer. They need to be processed by Laravel's Blade engine, which happens in the layout file before Inertia renders your JavaScript components.

### Example Setup

**resources/views/app.blade.php:**
```blade
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    @vite(['resources/js/app.js'])
    @inertiaHead
</head>
<body class="nativephp-safe-area">
    {{-- EDGE components go here in the Blade layout --}}
    <native:top-bar title="{{ config('app.name') }}" />

    {{-- Inertia renders your Vue/React components here --}}
    @inertia

    {{-- Bottom navigation --}}
    <native:bottom-nav>
        <native:bottom-nav-item
            id="home"
            icon="home"
            label="Home"
            :url="route('home')"
            :active="request()->routeIs('home')"
        />
        <native:bottom-nav-item
            id="search"
            icon="search"
            label="Search"
            :url="route('search')"
            :active="request()->routeIs('search')"
        />
        <native:bottom-nav-item
            id="profile"
            icon="person"
            label="Profile"
            :url="route('profile')"
            :active="request()->routeIs('profile')"
        />
    </native:bottom-nav>
</body>
</html>
```

Your Vue/React components then render inside the `@inertia` directive, with native navigation chrome handled by EDGE.

### Dynamic EDGE Properties

You can pass data from your controller to EDGE components via Inertia's shared data:

**app/Http/Middleware/HandleInertiaRequests.php:**
```php
public function share(Request $request): array
{
    return array_merge(parent::share($request), [
        'pageTitle' => fn () => $request->route()?->getName() ?? 'Home',
    ]);
}
```

**resources/views/app.blade.php:**
```blade
<native:top-bar :title="$page['props']['pageTitle'] ?? 'My App'" />
```

## Fetching Live Documentation

For detailed EDGE documentation:

- **Overview**: `https://nativephp.com/docs/mobile/2/edge-components/overview`
- **Top Bar**: `https://nativephp.com/docs/mobile/2/edge-components/top-bar`
- **Bottom Navigation**: `https://nativephp.com/docs/mobile/2/edge-components/bottom-nav`
- **Side Navigation**: `https://nativephp.com/docs/mobile/2/edge-components/side-nav`
- **Icons**: `https://nativephp.com/docs/mobile/2/edge-components/icons`
- **Web View & Safe Areas**: `https://nativephp.com/docs/mobile/2/the-basics/web-view`

Use WebFetch to retrieve the latest EDGE component details.