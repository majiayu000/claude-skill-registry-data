---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: jitter
description: Control Jitter (jitter.video) for exporting animations, replacing assets, modifying text, and rendering frames at specific times programmatically via Playwriter.
---

# Jitter Programmatic Control Skill

Control Jitter (jitter.video) for exporting animations, replacing assets, and modifying text.

## Setup

Load utils before interacting with Jitter:

```javascript
// Create your own tab (there is no default page), then load utils once per page
state.page = await context.newPage()
await state.page.addInitScript({ path: './skills/jitter/dist/jitter-utils.js' })

// Navigate to project
await state.page.goto('https://jitter.video/file/?id=YOUR_FILE_ID')

// Wait for app to be ready
await state.page.evaluate(() => jitterUtils.waitForApp())
```

## API Reference

### Traversal

| Function                | Description                        |
| ----------------------- | ---------------------------------- |
| `findNodeById(id)`      | Find node by ID                    |
| `findAllMediaNodes()`   | Get all images/SVGs/videos/GIFs    |
| `findAllTextNodes()`    | Get all text nodes                 |
| `getArtboards()`        | Get all artboards with dimensions  |
| `findNodesByType(type)` | Find nodes by layer type           |
| `findNodesByName(name)` | Find nodes by name (partial match) |
| `flattenTree()`         | Get all nodes as flat array        |

### Actions

| Function                       | Description                 |
| ------------------------------ | --------------------------- |
| `replaceAssetUrl(nodeId, url)` | Replace image/SVG/video URL |
| `replaceText(nodeId, text)`    | Replace text content        |
| `updateNode(nodeId, props)`    | Update any node properties  |
| `batchReplace(replacements)`   | Batch update multiple nodes |
| `selectNodes(nodeIds)`         | Select nodes by ID          |
| `removeNodes(nodeIds)`         | Remove nodes                |
| `undo()` / `redo()`            | Undo/redo actions           |

### Export

| Function                                    | Description                      |
| ------------------------------------------- | -------------------------------- |
| `generateExportUrl(opts)`                   | Generate export URL with options |
| `generateExportUrlFromCurrentProject(opts)` | Export URL for current project   |
| `parseJitterUrl(url)`                       | Parse file/node IDs from URL     |
| `getFileMeta()`                             | Get current file metadata        |

### Snapshot & Restore

| Function                                           | Description                               |
| -------------------------------------------------- | ----------------------------------------- |
| `createSnapshot(nodeIds)`                          | Save node states                          |
| `restoreFromSnapshot(snapshot)`                    | Restore saved states                      |
| `duplicateProject()`                               | Clone current project                     |
| `withTemporaryChanges(nodeIds, changes, callback)` | Apply temp changes, run callback, restore |

### Waiting

| Function                        | Description            |
| ------------------------------- | ---------------------- |
| `waitForApp(timeout?)`          | Wait for app to load   |
| `waitForSync(delay?)`           | Wait for server sync   |
| `waitForNode(nodeId, timeout?)` | Wait for node to exist |
| `isAppReady()`                  | Check if app is ready  |

## Examples

### Replace Assets and Export

```javascript
// Get all media nodes
const media = await state.page.evaluate(() => jitterUtils.findAllMediaNodes())

// Replace specific assets
await state.page.evaluate(() => {
  jitterUtils.batchReplace([
    { nodeId: 'abc123', data: { url: 'https://example.com/new-image.svg' } },
    { nodeId: 'def456', data: { url: 'https://example.com/new-photo.jpg' } },
  ])
})

// Wait for sync then export
await state.page.evaluate(() => jitterUtils.waitForSync())
const exportUrl = await state.page.evaluate(() =>
  jitterUtils.generateExportUrlFromCurrentProject({ profile: 'lottie' }),
)
await state.page.goto(exportUrl)
```

### Export with Temporary Changes

```javascript
await state.page.evaluate(async () => {
  const nodeIds = ['node1', 'node2']
  const changes = {
    node1: { url: 'https://temp-asset.svg' },
    node2: { text: 'Temporary Text' },
  }

  await jitterUtils.withTemporaryChanges(nodeIds, changes, async () => {
    // Changes applied here, will be restored after
    const url = jitterUtils.generateExportUrlFromCurrentProject()
    // ... navigate to export URL and download
  })
  // Original values automatically restored
})
```

### Find and Update Text

```javascript
const textNodes = await state.page.evaluate(() => jitterUtils.findAllTextNodes())
// [{ id, name, text, fontSize, fontFamily }, ...]

await state.page.evaluate(() => {
  jitterUtils.replaceText('textNodeId', 'New headline')
})
```

## Export Profiles

| Profile      | Output                         |
| ------------ | ------------------------------ |
| `lottie`     | Lottie JSON (vector animation) |
| `mp4`        | H.264 video                    |
| `gif`        | Animated GIF                   |
| `webm`       | WebM video                     |
| `prores4444` | ProRes 4444 (with alpha)       |
| `pngs`       | PNG sequence                   |

## Lottie Export Limitations

- **NodeIds are NOT preserved** in exported Lottie - cannot map back to Jitter nodes
- **Text becomes shapes** - not editable Lottie text layers
- **Images are embedded** as base64, no external URLs
- **Videos** export as first frame only

**Workaround:** Always modify assets in Jitter before export using `replaceAssetUrl()`.

### Inspecting exported Lottie files

Lottie JSON files from Jitter contain **giant base64-encoded image strings** that make
them unreadable. Use `jq` with `walk()` to truncate long strings before inspecting:

```bash
# Pretty-print with long strings truncated and huge arrays summarized
jq 'walk(
  if type == "string" and length > 80 then .[:80] + "..."
  elif type == "array" and length >= 20 then .[:3] + ["\(length - 3) more items..."]
  else . end
)' exported.json

# Pipe to less for paging
jq 'walk(
  if type == "string" and length > 80 then .[:80] + "..."
  elif type == "array" and length >= 20 then .[:3] + ["\(length - 3) more items..."]
  else . end
)' exported.json | less
```

This replaces embedded base64 image data with truncated previews and collapses
large arrays (20+ items, common in Bezier path data) to just the first 3 elements
plus a count, so you can read the animation structure without scrolling through
walls of encoded pixels or coordinate lists.

## Rendering Frames (Seek + Screenshot)

Jitter has a hidden `/api/renderer/` page with a headless rendering engine. It exposes
`window.jitter.renderFrame(timeMs)` which renders a full-quality frame at any point
in the animation and returns a raw PNG. This is the same engine Jitter's own export
backend uses (server-side Puppeteer calling `renderFrame()` in a loop).

### Getting file and artboard IDs

From the editor page URL `https://jitter.video/file/?id=FILE_ID&nodeId=ARTBOARD_ID`,
or programmatically:

```javascript
const fileId = await state.page.evaluate(() => window.app.props.fileMeta.id)
const artboard = await state.page.evaluate(() => {
  const conf = window.app.getState().observableImmutableConf.getSnapshot()
  const root = conf.roots[0]
  return { id: root.id, width: root.item.width, height: root.item.height, duration: root.item.duration }
})
```

### Opening the renderer

Navigate to `/api/renderer/` with these URL params. **Use a separate page** from the
editor so you don't lose editor state.

| Param | Required | Description |
|---|---|---|
| `file` | yes | project file ID |
| `artboardId` | yes | which artboard to render |
| `width` | yes | output width in px (use artboard width for 1:1) |
| `height` | yes | output height in px (use artboard height for 1:1) |
| `bucket` | yes | `snackthis-userdata` (the default S3 bucket) |
| `superSampling` | yes | must be `2` or higher; `1` fails Zod validation |
| `noBg` | no | `true` for transparent background |
| `addWatermark` | no | `false` to skip watermark |
| `playbackDirection` | no | `normal`, `reverse`, or `boomerang` |
| `vfe` | no | video fallback export, `off` for stills |

```javascript
const rendererUrl = [
  'https://jitter.video/api/renderer/',
  `?file=${fileId}`,
  `&bucket=snackthis-userdata`,
  `&artboardId=${artboardId}`,
  `&width=${width}`,
  `&height=${height}`,
  `&superSampling=2`,
  `&noBg=false`,
  `&addWatermark=false`,
  `&playbackDirection=normal`,
  `&vfe=off`,
].join('')

state.rendererPage = await context.newPage()
await state.rendererPage.goto(rendererUrl, { waitUntil: 'domcontentloaded' })
```

### Waiting for the renderer to be ready

The page dispatches a `jitterLoadEvent` custom event when ready, or sets
`window.jitter` directly. Wait for either:

```javascript
const exportContext = await state.rendererPage.evaluate(() => {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Renderer timed out')), 30000)
    if (window.jitter) {
      clearTimeout(timeout)
      return resolve(window.jitter.exportContext)
    }
    document.addEventListener('jitterLoadEvent', (e) => {
      clearTimeout(timeout)
      if (e.detail.name === 'ready') resolve(e.detail)
      else if (e.detail.name === 'error') reject(new Error(e.detail.message))
    })
  })
})
// exportContext = { exportWidth, exportHeight, exportDuration }
```

### Rendering a frame at a specific time

`renderFrame(timeMs)` returns a raw binary PNG string. Convert to base64 inside
the browser, then decode to a Buffer in the sandbox:

```javascript
// Render frame at 4000ms (4 seconds into the animation)
const base64Png = await state.rendererPage.evaluate(async () => {
  const result = await window.jitter.renderFrame(4000)
  return btoa(result.pngString)
})

const fs = require('node:fs')
const buf = Buffer.from(base64Png, 'base64')
fs.writeFileSync('/tmp/frame-4000.png', buf)
```

The output is a full-resolution PNG matching the `width`/`height` params, with no
editor UI, selection handles, or chrome. Just the clean artboard content at that
exact animation frame.

**The artboard may be letterboxed inside the PNG.** With `width=1920&height=1080`
and `superSampling=2` the artboard rendered at half size (960x540) centered with
transparent padding. Before comparing against other renders, find the content
bbox once (`magick frame.png -alpha extract -threshold 50% -format "%@" info:`)
and crop + flatten onto the artboard fill color.

### Rendering multiple frames

Loop over timestamps to capture a sequence:

```javascript
const fps = 30
const durationMs = exportContext.exportDuration // e.g. 8450
const totalFrames = Math.ceil(durationMs / 1000 * fps)

for (let i = 0; i < totalFrames; i++) {
  const timeMs = Math.round(i / fps * 1000)
  const base64 = await state.rendererPage.evaluate(async (t) => {
    const result = await window.jitter.renderFrame(t)
    return btoa(result.pngString)
  }, timeMs)
  
  const buf = Buffer.from(base64, 'base64')
  fs.writeFileSync(`/tmp/frames/frame-${String(i).padStart(4, '0')}.png`, buf)
}
```

### Seeking on the editor timeline (alternative)

If you just need to visually scrub the editor timeline without the full renderer,
click on the **timeline ruler** element. The ruler spans from x=272 (0ms) to the
duration end. Clicking sets the time cursor:

```javascript
// On the editor page (not the renderer page)
const rulerY = 1120 // vertical center of the ruler bar
const rulerStartX = 272
const rulerEndX = 1962 // corresponds to total duration

const fraction = 4000 / 8450 // target time / total duration
const clickX = rulerStartX + (rulerEndX - rulerStartX) * fraction
await state.page.mouse.click(clickX, rulerY)
```

This updates the editor canvas preview but the canvas only shows the viewport-visible
portion of the artboard. For full-resolution artboard screenshots, use the
`/api/renderer/` approach above.

## Porting to Remotion / egaki

See [PORTING-TO-REMOTION.md](./PORTING-TO-REMOTION.md) for the full guide:
scene graph extraction, concept mapping table, easing usage, additive animation
model, and frame-by-frame comparison workflow.

All Jitter easings are exported from `egaki/video` as continuous-intensity
preset functions (e.g. `impulseOvershoot(96)`), generated by a port of
Jitter's own curve engine. See the easing mapping table in the porting guide.

**Quick reference** for `smooth:standard:v1`:
`cubic-bezier(lerp(0.3, 0.9, intensity/100), 0, 0, 1)`. At intensity 50:
`Easing.bezier(0.5, 0, 0, 1)`.

## Tips

1. **Wait for sync** after modifications before exporting (1-2 seconds)
2. **Asset URLs** must be publicly accessible - Jitter fetches server-side
3. All `*WithUndo` actions can be undone with Ctrl+Z
4. Node IDs are stable and bookmarkable via `?nodeId=xxx`
5. Export URLs require being logged in with project access
6. **`superSampling` must be 2 or higher** when using `/api/renderer/`; value `1` fails Zod validation
7. **Use a separate page** for the renderer so you don't lose editor state
