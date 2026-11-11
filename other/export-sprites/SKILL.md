---
name: export-sprites
description: Export Vỉa Hè Online's sprite set from canvas code (client/Tools/sprites.js) to PNGs under client/Assets/Resources/Sprites/. Use this skill right after changing anything in sprites.js, and whenever the user says "xuất hình", "cập nhật hình", "đổi màu áo", "thêm kiểu tóc", "vẽ lại quầy", "sao hình chưa đổi", or when Unity logs "Missing sprite ...". It needs a real browser because the art is Canvas 2D — drive it through the Chrome tools instead of asking the user to type in a console.
---

# Export the sprite set

None of the game's art is hand-drawn files: every sprite is code in
`client/Tools/sprites.js`, one canvas-drawing function each. After editing that code the PNGs
have to be re-rendered, otherwise Unity keeps loading the old set and the change looks
like it did nothing.

A real browser is required because `sprites.js` uses the Canvas 2D API and the project has no
`node-canvas`, so plain Node cannot render it.

## How

### 1. Start the export server

```bash
node client/Tools/export-server.mjs
```

Run it in the background. It serves the preview page at `http://localhost:5181/` and accepts
`POST /save?name=<file>`, writing each file into `client/Assets/Resources/Sprites/`. If port 5181
is taken, stop the old export server rather than switching ports — the page uses relative URLs so
a second instance works but is easy to confuse.

### 2. Open the page and call `exportSprites()`

Through the Chrome tools (`mcp__claude-in-chrome__*`): open a new tab at
`http://localhost:5181/`, let the page finish drawing, then evaluate in the page:

```js
await exportSprites()
```

It returns **the number of sprites written** — currently 56. Treat that number as the
proof it worked; "no error" is not evidence.

Chrome tool notes: load the tools in **one** `ToolSearch` call (`tabs_context_mcp`,
`tabs_create_mcp`, `navigate`, `javascript_tool`, `read_console_messages`, `tabs_close_mcp`),
check the user's open tabs first and **create a new tab** rather than taking one of theirs, and
close it when done.

With no browser automation available, ask the user to open `http://localhost:5181/`, press F12
and run `exportSprites()` — but that is the last resort.

### 3. Check the result

```bash
ls client/Assets/Resources/Sprites/*.png | wc -l      # sprite count
head -1 client/Assets/Resources/Sprites/sprites.txt   # must read: ppu,200
```

`sprites.txt` is what Unity actually reads (`SpriteLibrary.cs`): one line per sprite,
`name,pivotX,pivotY,border left,bottom,right,top`. `exportSprites()` rewrites it every run, so a
sprite deleted from `sprites.js` drops out of the list by itself — but **nobody deletes the stale
PNG**, so remove it by hand unless you want it in the build.

### 4. Stop the export server

Stop the background task when finished, or it holds port 5181 for the next run.

## Previewing without writing files

`http://localhost:5181/` shows every sprite with its name and size on a transparency
checkerboard. Screenshotting that page before calling `exportSprites()` is the cheap way to settle
"is this the right colour?" without touching `Resources`.

The page also exposes `window.SPRITES` (the descriptor array) and `window.CANVASES` (canvases by
name) for inspecting one sprite.

## Conventions of the sprite set

- Sprite names are English snake_case (project rule in `AGENTS.md`); text painted onto sprites
  stays Vietnamese.
- 200 px = 1 Unity unit (`PPU`). Do not change it; every size in the scene depends on it.
- UI sprites carry a `border` (9-slice) argument so they stretch without distorting corners.
