---
name: expokit
description: Add and use ExpoKit UI components (buttons, inputs, sheets, dialogs, toasts, pickers, charts, 3D and Liquid Glass) in an Expo or React Native app. Use when the user asks for a UI component, screen or chart in an Expo app, mentions ExpoKit or expo-kit, or wants animated native-feeling UI.
---

# ExpoKit

ExpoKit works like shadcn/ui for Expo: the CLI copies component **source** into the app. There is no `expokit`
package to import from, and you should never re-implement a component that ExpoKit has.

## Workflow

1. **Find the item.** If the `expokit` MCP server is connected, call `search_items` (or `list_items`), then `view_item`
   for props, the import line and examples. Without it, run `npx @expokit/cli@latest add --list`, or read
   https://expokit.in/llms.txt.
2. **Add it** from the app's root folder (where `package.json` is):
   ```bash
   npx @expokit/cli@latest add <name> [<name>...]
   ```
   The first run also does `init`: it writes `components.json`, adds the `@/*` path alias to `tsconfig.json`, copies
   files to `src/components/ui/` (or `components/ui/` without `src/`), copies the shared theme `lib/kit.tsx`, and runs
   `npx expo install` for packages like `react-native-svg` and `expo-haptics`.
3. **Open the copied file** to confirm the export name and props, then import it with the alias:
   ```tsx
   import { BottomSheet } from '@/components/ui/bottom-sheet';
   ```
4. **Use only props that exist.** Follow the examples from `view_item` or the docs page
   `https://expokit.in/docs/components/<name>`.

## Theming

Components read colours, radius and light / dark from `useKit()`. To re-skin all of them, wrap the app once:

```tsx
import { KitProvider } from '@/lib/kit';

<KitProvider accent="#6366f1" radius={14}>{children}</KitProvider>
```

`scheme="light" | "dark" | "system"` forces a mode. In your own UI next to ExpoKit components, use
`const { colors, radius } = useKit()` instead of hard-coded colours so everything matches.

## Pro items

Items marked PRO need an ExpoKit Pro plan. If `add` says "not logged in", ask the user to run
`npx @expokit/cli@latest login` themselves (token from https://expokit.in/account). Never ask
for the token in chat, and don't write a look-alike of a Pro component instead.

## Don'ts

- Don't `npm install expokit` or import from `expo-kit` — the code lives in the app.
- Don't overwrite files the user edited: `add` keeps changed shared files unless you pass `--force` (ask first).
- Don't add Reanimated, Skia or Gesture Handler just for ExpoKit — it doesn't need them.
