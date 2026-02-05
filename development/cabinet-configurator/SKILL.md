---
name: cabinet-configurator
description: Cabinet Editor web application development skill. Use when working on Cabinet Editor codebase - a 2D/3D furniture configurator built with Canvas API and Three.js. Covers architecture (Panel and Drawer classes, connections system, virtual panels), coordinate systems, panel/drawer movement logic, cabinet dimension changes (width/height/depth/base), 3D rendering with rank-based depth, ribs system, and drawer box calculations. Essential for debugging, adding features, or understanding how panels/drawers interact with cabinet sizing.
---

# Cabinet Configurator Skill

Development guide for Cabinet Editor - a web-based furniture configurator with 2D Canvas editing and 3D Three.js visualization.

## Project Setup

**Location:** `C:\Users\admin\Desktop\OMS\cabinet-editor`

**CRITICAL: Always use filesystem MCP tools for file operations**
- Use `filesystem:read_text_file`, `filesystem:edit_file`, `filesystem:write_file`
- NEVER use bash/powershell commands like `cat`, `sed`, `type`, etc. for reading/editing files
- Reason: Prevents encoding issues (UTF-8 vs CP1251/CP866), handles line endings correctly, provides proper error handling
- The filesystem tools have access to the project directory and handle Windows paths correctly

## Architecture Overview

### Core Classes

**App** (`js/App.js`)
- Main application controller
- Manages `this.cabinet` (width, height, depth, base)
- Stores `this.panels` Map of Panel instances
- Handles interaction (dragging, mode selection)
- Manages history (undo/redo)

**Panel** (`js/Panel.js`)
- Represents shelves and dividers
- Properties:
  - `type`: 'shelf' | 'divider'
  - `id`: unique identifier
  - `position`: { x?, y? } - center point (one coordinate per panel)
  - `bounds`: { startX, endX } for shelves, { startY, endY } for dividers
  - `connections`: { left?, right?, top?, bottom? } - references to adjacent Panel objects
  - `ribs`: array of rib objects (shelves only)
  - `isHorizontal`: true for shelves, false for dividers

**Drawer** (`js/Drawer.js`)
- Represents pull-out drawer boxes
- Properties:
  - `type`: 'drawer'
  - `id`: unique identifier
  - `connections`: { bottomShelf, topShelf, leftDivider, rightDivider } - Panel/virtual panel references
  - `volume`: calculated 3D bounding box { x: {start, end}, y: {start, end}, z: {start, end} }
  - `boxLength`: selected standard box size (270, 350, 450, 550mm)
  - `parts`: calculated drawer components (front, leftSide, rightSide, back, bottom)

**Viewer3D** (`js/Viewer3D.js`)
- Three.js 3D visualization
- Manages scene, camera, renderer, controls
- Builds cabinet structure and panel meshes

### Panel System

**Shelves (horizontal panels)**
- `position.y`: Y coordinate of shelf center
- `bounds.startX`, `bounds.endX`: left and right edges
- `connections.left`/`right`: dividers that bound the shelf horizontally
- `connections.top`/`bottom`: used by dividers that terminate at this shelf

**Dividers (vertical panels)**
- `position.x`: X coordinate of divider center  
- `bounds.startY`, `bounds.endY`: bottom and top edges
- `connections.bottom`/`top`: shelves that bound the divider vertically
- `connections.left`/`right`: used by shelves that terminate at this divider

**Virtual Panels**
Drawers can connect to "virtual panels" representing cabinet boundaries:
- `type: 'left'` or `'right'`: virtual side panels at cabinet edges
- `type: 'bottom'` or `'top'`: virtual horizontal panels at cabinet base/roof
- Virtual panels don't exist in `app.panels` Map but behave like real panels for drawer connections
- Enable drawers to span full width/height of cabinet

## Coordinate System

**Canvas coordinates (2D):**
- Origin (0,0) at bottom-left
- X increases right (0 to cabinet.width)
- Y increases up (0 to cabinet.height)
- Cabinet structure:
  - Left side: x = CONFIG.DSP/2 (8mm)
  - Right side: x = cabinet.width - CONFIG.DSP/2
  - Bottom (plinth top): y = cabinet.base
  - Top (roof bottom): y = cabinet.height - CONFIG.DSP

**3D coordinates:**
- X/Y match 2D canvas
- Z is depth: 0 (back) to cabinet.depth (front)
- Panels recede based on `rank`: depth = (cabinet.depth - 3) - rank

**Key measurements:**
- `CONFIG.DSP`: 16mm (panel thickness for ДСП)
- `CONFIG.HDF`: 3mm (back panel thickness for ХДФ)
- `CONFIG.MIN_GAP`: 150mm (minimum spacing between panels)
- `CONFIG.MIN_SIZE`: 200mm (minimum panel dimension)
- `cabinet.base`: plinth height (min 60mm)
- `cabinet.width`: total cabinet width (400-3000mm)
- `cabinet.height`: total cabinet height
- `cabinet.depth`: total cabinet depth (300-800mm, adjustable in 1mm increments)

## Movement Logic

### Movable Cabinet Boundaries

Cabinet boundaries (sides, bottom, roof) can be moved in "move" mode by detecting them in `findPanelAt()`:

**Left/Right Sides** (`moveSide` method):
- Changes `cabinet.width`
- Left side: shifts all panels right when expanding
- Right side: only changes width
- Limits: MIN_CABINET_WIDTH (400mm) to MAX_CABINET_WIDTH (3000mm)
- Cannot pass through dividers (MIN_GAP spacing)

**Bottom** (`moveHorizontalSide` with `isBottom`):
- Changes `cabinet.base` (plinth height, min 60mm)
- Dividers WITHOUT `connections.bottom`: `bounds.startY = cabinet.base` (stretch/shrink)
- Dividers WITH `connections.bottom`: no change (stay with shelf)
- Shelves: remain at absolute Y coordinates (do not move)
- Updates `position.y` for affected dividers

**Roof** (`moveHorizontalSide` with `!isBottom`):
- Changes `cabinet.height` (total height)
- Cannot pass through shelves (stops at highest shelf + MIN_GAP)
- Dividers WITHOUT `connections.top`: stretch `bounds.endY` to new height
- Updates `position.y` for stretched dividers

### Panel Movement

**Shelves:**
- Move vertically (change `position.y`)
- `bounds.startX`/`endX` determined by `connections.left`/`right`
- Connected dividers update their `bounds.startY` or `bounds.endY`

**Dividers:**
- Move horizontally (change `position.x`)
- `bounds.startY`/`endY` determined by `connections.bottom`/`top`
- Connected shelves update their `bounds.startX` or `bounds.endX`

**Important:** After changing `bounds`, always update `position`:
```javascript
// For dividers
panel.position.y = (panel.bounds.startY + panel.bounds.endY) / 2;

// For shelves  
panel.position.x = (panel.bounds.startX + panel.bounds.endX) / 2;
```

### Update Pattern

When moving panels that affect others:
1. Update the moved panel's position/bounds
2. Call `updateConnectedPanels(movedPanel)` to update connected panels
3. Update ribs: `panel.updateRibs(this.panels, this.cabinet.width)` for affected shelves
4. Call `updateMesh(this, panel)` for 3D updates
5. Call `render2D(this)` and `renderAll3D(this)` to redraw

When moving cabinet boundaries:
1. Update `cabinet.width`/`height`/`base`
2. Update affected panel bounds and positions
3. Call `updateCalc()` to recalculate derived dimensions
4. Update ribs for all shelves
5. Call `updateCanvas()` if canvas scaling changed
6. Call `viewer3D.rebuildCabinet()` to rebuild 3D structure
7. Call `render2D(this)` and `renderAll3D(this)`

## 3D Rendering

### Rank System

Panels have a `rank` that determines their Z-depth (recess from front):

```javascript
calculatePanelRank(panel) {
  // Fixed ranks
  if (panel.type === 'back') return -1;  // ХДФ back
  if (panel.type === 'left' || panel.type === 'right') return 0;  // Sides
  if (panel.type === 'bottom' || panel.type === 'top') return 1;  // Floor/ceiling
  
  // Dynamic rank = max(parent ranks) + 1
  let maxRank = 0;
  for (let parent of Object.values(panel.connections)) {
    if (parent?.type) {
      maxRank = Math.max(maxRank, this.calculatePanelRank(parent));
    }
  }
  return maxRank + 1;
}
```

**3D depth calculation:**
```javascript
const rank = app.calculatePanelRank(panel);
const depth = (cabinet.depth - 3) - rank;  // Recess from front
```

### Cabinet Structure (3D)

Built by `Viewer3D.rebuildCabinet()`:
- Left/right sides: 16mm thick, full height, depth - 3mm
- Bottom/top: between sides, 16mm thick, depth - 4mm
- Back (ХДФ): 3mm thick, behind everything
- Front/back plinth: 16mm thick, below base height

## Drawer System

Drawers are pull-out boxes defined by 4 boundary panels (real or virtual).

### Drawer Structure

**Connections:**
- `bottomShelf`: lower boundary (shelf or virtual 'bottom')
- `topShelf`: upper boundary (shelf or virtual 'top')
- `leftDivider`: left boundary (divider or virtual 'left')
- `rightDivider`: right boundary (divider or virtual 'right')

**Volume Calculation** (`calculateVolume`):
```javascript
// Find minimum depth among connected panels (based on rank)
const depths = [
  (cabinet.depth - CONFIG.HDF) - calculatePanelRank(bottomShelf),
  (cabinet.depth - CONFIG.HDF) - calculatePanelRank(topShelf),
  (cabinet.depth - CONFIG.HDF) - calculatePanelRank(leftDivider),
  (cabinet.depth - CONFIG.HDF) - calculatePanelRank(rightDivider)
];
const minDepth = Math.min(...depths);

// For virtual panels, use cabinet dimensions directly
const leftEdge = leftDivider.type === 'left' 
  ? CONFIG.DSP 
  : leftDivider.position.x + CONFIG.DSP;

const volume = {
  x: { start: leftEdge, end: rightEdge },
  y: { start: bottomEdge, end: topEdge },
  z: { start: CONFIG.DSP, end: minDepth - 2 }  // 16mm offset from back for rib + 2mm clearance from panel
};
```

**Box Length Selection:**
- Standard sizes: 270, 350, 450, 550mm (from `CONFIG.DRAWER.SIZES`)
- Selected based on available depth: `volDepth + CONFIG.DSP`
- If no suitable size, drawer creation fails

**Parts Calculation** (`calculateParts`):
Drawer consists of 5 components with precise dimensions and Z-coordinates:

1. **Front panel** (facade)
   - Width: `volWidth - 4mm` (2mm gaps on sides)
   - Height: `volHeight - 30mm` (26mm gap on top, 4mm on bottom)
   - Depth: 16mm (CONFIG.DSP)
   - Position Z: `frontZ = vol.z.end`

2. **Left/Right sides**
   - Height: `volHeight - 56mm`
   - Depth: `boxLength - 26mm`
   - Thickness: 16mm
   - Z range: `[sidesZ1, sidesZ2]` where `sidesZ2 = frontZ - 16`

3. **Back panel**
   - Width: `volWidth - 42mm`
   - Height: `volHeight - 68mm`
   - Positioned at: `backZ = sidesZ1 + CONFIG.DRAWER.BACK_OFFSET`

4. **Bottom panel**
   - Width: `volWidth - 42mm`
   - Depth: `boxLength - 44mm`
   - Z range: `[bottomZ1, bottomZ2]` starting at `sidesZ1 + 16 + BOTTOM_OFFSET`

**Drawer Config Constants** (from `CONFIG.DRAWER`):
```javascript
DRAWER: {
  SIZES: [270, 320, 370, 420, 470, 520, 570, 620],  // Стандартные длины коробов (8 размеров)
  MIN_WIDTH: 150,    // Минимальная ширина ящика (как MIN_GAP)
  MAX_WIDTH: 1200,   // Максимальная ширина ящика
  MIN_HEIGHT: 80,    // Минимальная высота ящика
  MAX_HEIGHT: 400,   // Максимальная высота ящика
  GAP_FRONT: 2,      // Зазоры фасада
  GAP_TOP: 28,
  GAP_BOTTOM: 2,
  SIDE_OFFSET_X: 5,  // Отступы боковин
  SIDE_OFFSET_Y: 17,
  INNER_OFFSET: 21,  // Отступ задней стенки/дна
  BACK_OFFSET: 2,
  BOTTOM_OFFSET: 2
}
```

### Drawer Lifecycle

**Adding a drawer** (`addDrawer`):
1. Find 4 boundary panels at click position (or use virtual panels)
2. Create Drawer instance with connections
3. Call `drawer.calculateParts(app)` - returns false if volume too small
4. Add to `app.drawers` Map
5. Call `updateDrawerMeshes(app, drawer)` for 3D
6. Save history and render

**Updating drawers:**
Drawers must be recalculated when connected panels move or cabinet dimensions change:
```javascript
// After panel movement
for (let drawer of app.drawers.values()) {
  if (drawer.connections includes movedPanel) {
    drawer.updateParts(app);
    updateDrawerMeshes(app, drawer);
  }
}

// After cabinet dimension change (width/height/depth/base)
for (let drawer of app.drawers.values()) {
  drawer.updateParts(app);
  updateDrawerMeshes(app, drawer);
}
```

**Deleting drawers:**
- Delete when any connected panel is deleted
- Can be deleted individually in delete mode
- Use `removeDrawerMeshes(app, drawer)` before removing from Map

**Mirroring:**
When mirroring cabinet content:
```javascript
// Swap left/right divider connections
const tempLeft = drawer.connections.leftDivider;
drawer.connections.leftDivider = drawer.connections.rightDivider;
drawer.connections.rightDivider = tempLeft;

// Update virtual panel types if present
if (leftDivider?.type === 'right') leftDivider.type = 'left';
if (rightDivider?.type === 'left') rightDivider.type = 'right';

drawer.updateParts(app);
```

### 3D Rendering

**Drawer meshes** (from `render3D.js`):
- Each drawer creates 5 separate meshes (front, sides, back, bottom)
- Stored in `app.mesh3D` with keys: `${drawer.id}-front`, `${drawer.id}-leftSide`, etc.
- Material: orange color (`0xff9800`) to distinguish from panels
- Box geometry with precise dimensions from `drawer.parts`

**Update pattern:**
```javascript
import { updateDrawerMeshes, removeDrawerMeshes } from './modules/render3D.js';

// After drawer modification
updateDrawerMeshes(app, drawer);  // Removes old meshes, creates new ones

// Before deletion
removeDrawerMeshes(app, drawer);  // Cleans up all 5 meshes
```

**Global export** (for HTML inline scripts):
```javascript
// In main.js
import { updateDrawerMeshes } from './modules/render3D.js';
window.updateDrawerMeshes = updateDrawerMeshes;
```

## Ribs System

Ribs (ребра жесткости) are vertical supports under shelves, preventing sagging.

**When added:**
- Shelves longer than threshold need ribs
- Thresholds: 800mm (no ribs), 1000mm (1 rib), 1200mm (2 ribs)

**Calculation** (`Panel.updateRibs()`):
```javascript
updateRibs(allPanels, cabinetWidth) {
  const shelfWidth = this.bounds.endX - this.bounds.startX;
  
  // Find dividers that cross this shelf
  const crossingDividers = Array.from(allPanels.values())
    .filter(p => !p.isHorizontal && 
                 p.bounds.startY <= this.position.y &&
                 p.bounds.endY >= this.position.y &&
                 p.position.x > this.bounds.startX &&
                 p.position.x < this.bounds.endX)
    .map(p => p.position.x)
    .sort((a, b) => a - b);
  
  // Calculate segments between dividers
  const points = [
    this.bounds.startX,
    ...crossingDividers,
    this.bounds.endX
  ];
  
  // Add ribs to segments that need them
  this.ribs = [];
  for (let i = 0; i < points.length - 1; i++) {
    const segmentStart = points[i] + (crossingDividers.includes(points[i]) ? CONFIG.DSP : 0);
    const segmentEnd = points[i + 1];
    const segmentWidth = segmentEnd - segmentStart;
    
    const ribsNeeded = calculateRibsForSegment(segmentWidth);
    if (ribsNeeded > 0) {
      // Distribute ribs evenly in segment
      for (let j = 0; j < ribsNeeded; j++) {
        const ribX = segmentStart + (segmentWidth / (ribsNeeded + 1)) * (j + 1);
        this.ribs.push({ startX: ribX, endX: ribX + CONFIG.DSP });
      }
    }
  }
}
```

**3D rendering:**
- Ribs are 16mm wide, 100mm tall
- Positioned below shelf: `y = shelf.position.y - 100`
- Same depth as shelf (based on rank)

## Common Patterns

For detailed code examples, see [references/examples.md](references/examples.md).

### Adding a new panel
1. Create Panel instance with type, id, position, bounds, connections
2. Add to `app.panels` Map
3. Call `panel.updateRibs()` if shelf
4. Call `app.saveHistory()`
5. Call `render2D(app)` and `renderAll3D(app)`

### Deleting a panel
1. Find dependent panels via `connections`
2. Call `removeMesh(app, panel)` for each
3. Remove from `app.panels`
4. Recalculate bounds for affected panels
5. Update ribs for remaining shelves
6. Call `app.saveHistory()`
7. Call `render2D(app)` and `renderAll3D(app)`

### Changing cabinet dimensions
1. Update `app.cabinet.width`/`height`/`depth`/`base`
2. Update panel bounds that depend on cabinet size
3. Call `app.updateCalc()`
4. Recalculate ALL drawers (they depend on cabinet dimensions via virtual panels)
5. If width/height changed: `app.updateCanvas()`
6. Rebuild 3D: `app.viewer3D.rebuildCabinet()`
7. Update all panel meshes or call `renderAll3D(app)`

### Adding a drawer
1. Click in drawer mode to select area
2. Find 4 boundary panels (use virtual panels for cabinet edges)
3. Create Drawer instance: `new Drawer(id, connections)`
4. Calculate parts: `drawer.calculateParts(app)` - check return value
5. Add to `app.drawers` Map
6. Call `updateDrawerMeshes(app, drawer)` for 3D
7. Save history and render

## File Structure

```
cabinet-editor/
├── index.html           - UI structure, bottom sheets, event handlers
├── css/
│   └── main.css         - Styling
├── js/
│   ├── main.js          - Entry point, app initialization, global exports
│   ├── App.js           - Main application class
│   ├── Panel.js         - Panel class
│   ├── Drawer.js        - Drawer class
│   ├── Viewer3D.js      - 3D viewer class
│   ├── config.js        - Constants and configuration
│   ├── exportJSON.js    - Export functionality
│   └── modules/
│       ├── render2D.js       - Canvas 2D rendering
│       ├── render3D.js       - Three.js mesh management
│       ├── historyLogging.js - History UI
│       └── historyDebug.js   - History debugging tools
```

## Debugging Tips

**Check panel state:**
```javascript
// In browser console
window.app.panels.forEach(p => console.log(p.id, p.position, p.bounds, p.connections))
```

**Check drawer state:**
```javascript
// Inspect drawers
window.app.drawers.forEach(d => console.log(d.id, d.volume, d.boxLength, d.parts));

// Test drawer in specific area
const testDrawer = new Drawer('test', {
  bottomShelf: window.app.panels.get('shelf-0'),
  topShelf: window.app.panels.get('shelf-1'),
  leftDivider: { type: 'left', position: { x: 8 } },
  rightDivider: window.app.panels.get('divider-0')
});
testDrawer.calculateParts(window.app);
console.log(testDrawer);
```

**Verify connections:**
```javascript
// Check if connections are Panel objects, not IDs
const panel = window.app.panels.get('shelf-0');
console.log(panel.connections.left?.type); // Should be 'divider', not undefined
```

**Test cabinet dimensions:**
```javascript
console.log(window.app.cabinet); // { width, height, depth, base }
console.log(window.app.calc);    // { innerWidth, innerDepth, workHeight }
```

**Force 3D rebuild:**
```javascript
window.app.viewer3D.rebuildCabinet();
window.app.renderAll3D();
```