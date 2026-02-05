---
name: take-screenshot
description: Take a screenshot of the game to see what's happening visually. Use when confused about surroundings, checking building placement, or debugging issues.
allowed-tools: Bash, Read
---

# Take Screenshot

Use this skill to visually see what's happening in the game.

## Take a Screenshot

```lua
game.take_screenshot{player=player, resolution={1920,1080}, zoom=0.5, path='agent-view.png', show_entity_info=true}
```

Run with:
```bash
pnpm --prefix /Users/golergka/Projects/factorio-agent eval "game.take_screenshot{player=player, resolution={1920,1080}, zoom=0.5, path='agent-view.png', show_entity_info=true}"
```

## View the Screenshot

Use the Read tool:
```
Read /Users/golergka/Library/Application Support/factorio/script-output/agent-view.png
```

## When to Take Screenshots

- After arriving at a new location
- Before placing buildings (check the area)
- After placing buildings (verify they work)
- When confused about what's around you
- When looking for resources
- When debugging production issues

## Screenshot Options

- `zoom=0.5` - Good for overview (change to 0.25 for wider, 1.0 for closer)
- `show_entity_info=true` - Shows alt-mode info (inventories, production)
- `resolution={1920,1080}` - Full HD resolution
