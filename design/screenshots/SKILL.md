---
name: Screenshots
description: Use this skill to read screenshots from the user's ShareX folder for visual game information. Covers finding recent screenshots and reading game UI state.
---

# Screenshots Skill

This skill enables reading screenshots captured via ShareX to view visual game information.

## ShareX Screenshot Location

```
Z:\Users\Heiner\Documents\ShareX\Screenshots\2025-12\
```

Screenshots are named with the pattern: `{process}_{randomId}.{png|jpg}`
- FFXIV screenshots: `ffxiv_dx11_*.png` or `ffxiv_dx11_*.jpg`

## Finding the Most Recent Screenshot

### Get Latest FFXIV Screenshot

Use Glob to find recent screenshots, sorted by modification time (most recent first):

```
Glob pattern: ffxiv_dx11_*
Path: Z:\Users\Heiner\Documents\ShareX\Screenshots\2025-12
```

The first result is the most recent screenshot.

### Example Workflow

1. User takes screenshot with ShareX
2. Claude uses Glob to find latest screenshot:
   ```
   Z:\Users\Heiner\Documents\ShareX\Screenshots\2025-12\ffxiv_dx11_*.png
   ```
3. Claude uses Read tool to view the image
4. Claude analyzes the visual content

## Use Cases

### Reading Game UI
- API documentation from SND MacrosLibrary window
- Current player position/zone from game UI
- Addon states and configurations
- Error messages or dialogs

### Debugging
- Visual confirmation of script behavior
- UI state when something goes wrong
- Plugin windows and settings

## Complementary Tools

| Tool | Purpose |
|------|---------|
| **ShareX Screenshots** | Visual game state, UI, plugin windows |
| **ChatTwo Debug** | Script echo output, error messages, debug logs |

Use screenshots for **what you see**, use ChatTwo for **what scripts output**.

## Folder Structure Note

ShareX organizes by year-month folders:
- `2025-12` for December 2025
- Adjust the path when month changes
