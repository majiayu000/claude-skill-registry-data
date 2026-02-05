---
name: navigation-architect
description: Designs and implements navigation flows using Expo Router (file-based routing). Use when adding new screens, handling deep links, or restructuring the app's layout.
---

# Navigation Architect Skill

This skill ensures that the app's navigation is intuitive, performant, and follows Expo Router best practices.

## Core Concepts

- **File-based Routing**: Map the file system to the app's navigation structure.
- **Dynamic Routes**: Use `[id].tsx` for dynamic segments.
- **Layouts**: Use `_layout.tsx` for shared UI (headers, tabs).
- **Groups**: Use `(group)` folders to organize routes without affecting the URL.
- **Typed Routes**: Leverage Expo Router's static typing for navigation.

## Instructions

1. **Map User Flow**: Define how the user moves between screens.
2. **Structure `app/`**: Create the directory structure that matches the flow.
3. **Handle Params**: Use `useLocalSearchParams` for passing data.
4. **Deep Linking**: Ensure all routes are accessible via URI schemes.
5. **Modals**: Use layout groups and specific screen options for presentation.

## Example

```bash
app/
  (tabs)/
    index.tsx       # Home tab
    settings.tsx    # Settings tab
    _layout.tsx     # Tab bar configuration
  details/
    [id].tsx        # Item detail screen
  _layout.tsx       # Root layout (Stack, ThemeProvider)
```
