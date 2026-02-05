---
name: managing-canvas-operations
description: Managing canvas operations in StickerNest including pan, zoom, selection, viewport, and canvas interactions. Use when implementing canvas navigation, selection tools, drag operations, viewport manipulation, or working with canvas coordinates. Covers useCanvasStore viewport, selection state, and gesture handling.
---

# Managing Canvas Operations

StickerNest's canvas is the core workspace where widgets and stickers live. This skill covers viewport manipulation, selection, and canvas interactions.

## Canvas Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  CanvasPage                                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  CanvasRenderer (DOM mode)                            │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Viewport Transform Layer                       │  │  │
│  │  │  transform: translate(panX, panY) scale(zoom)   │  │  │
│  │  │  ┌─────────────────────────────────────────┐    │  │  │
│  │  │  │  Canvas Content                         │    │  │  │
│  │  │  │  - Widgets                              │    │  │  │
│  │  │  │  - Stickers                             │    │  │  │
│  │  │  │  - Grid                                 │    │  │  │
│  │  │  └─────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Viewport State

The viewport is managed in `useCanvasStore`:

```typescript
interface ViewportState {
  panX: number;      // Horizontal offset (pixels)
  panY: number;      // Vertical offset (pixels)
  zoom: number;      // Zoom level (1 = 100%, 0.5 = 50%, 2 = 200%)
  width: number;     // Canvas width
  height: number;    // Canvas height
}

// Access viewport
const viewport = useCanvasStore((s) => s.viewport);
const { panX, panY, zoom } = viewport;

// Update viewport
useCanvasStore.getState().setViewport({ zoom: 1.5 });
```

## Pan Operations

### Programmatic Pan

```typescript
// Relative pan (add to current position)
useCanvasStore.getState().pan(deltaX, deltaY);

// Absolute pan (set position)
useCanvasStore.getState().setViewport({ panX: 100, panY: 200 });

// Pan to center on a point
function panToCenter(targetX: number, targetY: number) {
  const { width, height, zoom } = useCanvasStore.getState().viewport;
  useCanvasStore.getState().setViewport({
    panX: (width / 2) - (targetX * zoom),
    panY: (height / 2) - (targetY * zoom),
  });
}
```

### Mouse/Touch Pan

```typescript
function usePanGesture() {
  const [isPanning, setIsPanning] = useState(false);
  const lastPos = useRef({ x: 0, y: 0 });

  const onPointerDown = (e: React.PointerEvent) => {
    if (e.button === 1 || e.button === 2 || spaceHeld) { // Middle click, right click, or space
      setIsPanning(true);
      lastPos.current = { x: e.clientX, y: e.clientY };
      e.currentTarget.setPointerCapture(e.pointerId);
    }
  };

  const onPointerMove = (e: React.PointerEvent) => {
    if (!isPanning) return;
    const deltaX = e.clientX - lastPos.current.x;
    const deltaY = e.clientY - lastPos.current.y;
    useCanvasStore.getState().pan(deltaX, deltaY);
    lastPos.current = { x: e.clientX, y: e.clientY };
  };

  const onPointerUp = () => setIsPanning(false);

  return { onPointerDown, onPointerMove, onPointerUp, isPanning };
}
```

## Zoom Operations

### Programmatic Zoom

```typescript
// Zoom to level
useCanvasStore.getState().setViewport({ zoom: 1.5 });

// Zoom relative (multiply current)
const { zoom } = useCanvasStore.getState().viewport;
useCanvasStore.getState().setViewport({ zoom: zoom * 1.1 });

// Zoom centered on point
function zoomAtPoint(factor: number, centerX: number, centerY: number) {
  const { panX, panY, zoom } = useCanvasStore.getState().viewport;
  const newZoom = Math.max(0.1, Math.min(5, zoom * factor)); // Clamp 10%-500%

  // Adjust pan to keep point stationary
  const scale = newZoom / zoom;
  const newPanX = centerX - (centerX - panX) * scale;
  const newPanY = centerY - (centerY - panY) * scale;

  useCanvasStore.getState().setViewport({
    zoom: newZoom,
    panX: newPanX,
    panY: newPanY,
  });
}
```

### Mouse Wheel Zoom

```typescript
function useWheelZoom() {
  const onWheel = useCallback((e: WheelEvent) => {
    e.preventDefault();
    const factor = e.deltaY > 0 ? 0.9 : 1.1; // Zoom out/in
    zoomAtPoint(factor, e.clientX, e.clientY);
  }, []);

  useEffect(() => {
    const canvas = document.getElementById('canvas');
    canvas?.addEventListener('wheel', onWheel, { passive: false });
    return () => canvas?.removeEventListener('wheel', onWheel);
  }, [onWheel]);
}
```

### Pinch-to-Zoom (Touch)

```typescript
function usePinchZoom() {
  const initialDistance = useRef(0);
  const initialZoom = useRef(1);

  const onTouchStart = (e: TouchEvent) => {
    if (e.touches.length === 2) {
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      initialDistance.current = Math.hypot(dx, dy);
      initialZoom.current = useCanvasStore.getState().viewport.zoom;
    }
  };

  const onTouchMove = (e: TouchEvent) => {
    if (e.touches.length === 2) {
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      const distance = Math.hypot(dx, dy);
      const scale = distance / initialDistance.current;
      const newZoom = Math.max(0.1, Math.min(5, initialZoom.current * scale));

      // Center point between fingers
      const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;

      zoomAtPoint(newZoom / useCanvasStore.getState().viewport.zoom, centerX, centerY);
    }
  };
}
```

## Selection State

```typescript
interface SelectionState {
  selectedIds: Set<string>;      // All selected widget IDs
  primaryId: string | null;      // Primary selection (for single-select ops)
  mode: 'single' | 'multi';      // Selection mode
  isSelecting: boolean;          // Currently drag-selecting
  selectionBox: {                // Drag selection rectangle
    startX: number;
    startY: number;
    endX: number;
    endY: number;
  } | null;
}
```

### Selection Operations

```typescript
// Select single widget
useCanvasStore.getState().selectWidget(widgetId);

// Add to selection (multi-select)
useCanvasStore.getState().addToSelection(widgetId);

// Toggle selection
useCanvasStore.getState().toggleSelection(widgetId);

// Clear selection
useCanvasStore.getState().clearSelection();

// Select multiple
useCanvasStore.getState().setSelection(new Set(['id1', 'id2', 'id3']));

// Check if selected
const isSelected = useCanvasStore((s) => s.selection.selectedIds.has(widgetId));
```

### Drag Selection Box

```typescript
function useDragSelection() {
  const startSelection = (x: number, y: number) => {
    useCanvasStore.getState().setSelectionBox({
      startX: x, startY: y, endX: x, endY: y
    });
  };

  const updateSelection = (x: number, y: number) => {
    const box = useCanvasStore.getState().selection.selectionBox;
    if (box) {
      useCanvasStore.getState().setSelectionBox({
        ...box, endX: x, endY: y
      });
    }
  };

  const finishSelection = () => {
    const box = useCanvasStore.getState().selection.selectionBox;
    if (box) {
      // Find widgets inside box
      const widgets = useCanvasStore.getState().widgets;
      const selected = new Set<string>();

      const minX = Math.min(box.startX, box.endX);
      const maxX = Math.max(box.startX, box.endX);
      const minY = Math.min(box.startY, box.endY);
      const maxY = Math.max(box.startY, box.endY);

      widgets.forEach((widget, id) => {
        if (widget.x >= minX && widget.x + widget.width <= maxX &&
            widget.y >= minY && widget.y + widget.height <= maxY) {
          selected.add(id);
        }
      });

      useCanvasStore.getState().setSelection(selected);
      useCanvasStore.getState().setSelectionBox(null);
    }
  };
}
```

## Coordinate Conversions

### Screen to Canvas Coordinates

```typescript
function screenToCanvas(screenX: number, screenY: number): { x: number; y: number } {
  const { panX, panY, zoom } = useCanvasStore.getState().viewport;
  const canvasEl = document.getElementById('canvas');
  const rect = canvasEl?.getBoundingClientRect() ?? { left: 0, top: 0 };

  return {
    x: (screenX - rect.left - panX) / zoom,
    y: (screenY - rect.top - panY) / zoom,
  };
}
```

### Canvas to Screen Coordinates

```typescript
function canvasToScreen(canvasX: number, canvasY: number): { x: number; y: number } {
  const { panX, panY, zoom } = useCanvasStore.getState().viewport;
  const canvasEl = document.getElementById('canvas');
  const rect = canvasEl?.getBoundingClientRect() ?? { left: 0, top: 0 };

  return {
    x: canvasX * zoom + panX + rect.left,
    y: canvasY * zoom + panY + rect.top,
  };
}
```

## Grid Snapping

```typescript
interface GridSettings {
  snapToGrid: boolean;
  gridSize: number;        // e.g., 20 pixels
  showGrid: boolean;
  snapToCenter: boolean;
  showCenterGuides: boolean;
}

// Snap position to grid
function snapToGrid(pos: { x: number; y: number }): { x: number; y: number } {
  const { snapToGrid, gridSize } = useCanvasStore.getState().grid;
  if (!snapToGrid) return pos;

  return {
    x: Math.round(pos.x / gridSize) * gridSize,
    y: Math.round(pos.y / gridSize) * gridSize,
  };
}
```

## Keyboard Shortcuts

```typescript
// Common canvas shortcuts
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    // Zoom shortcuts
    if (e.ctrlKey || e.metaKey) {
      if (e.key === '=' || e.key === '+') {
        e.preventDefault();
        zoomIn();
      } else if (e.key === '-') {
        e.preventDefault();
        zoomOut();
      } else if (e.key === '0') {
        e.preventDefault();
        resetZoom(); // 100%
      }
    }

    // Selection shortcuts
    if (e.key === 'Escape') {
      clearSelection();
    }
    if (e.key === 'a' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      selectAll();
    }
    if (e.key === 'Delete' || e.key === 'Backspace') {
      deleteSelected();
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

## Fit to Content

```typescript
function fitToContent() {
  const widgets = useCanvasStore.getState().widgets;
  if (widgets.size === 0) return;

  // Find bounding box of all widgets
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

  widgets.forEach((widget) => {
    minX = Math.min(minX, widget.x);
    minY = Math.min(minY, widget.y);
    maxX = Math.max(maxX, widget.x + widget.width);
    maxY = Math.max(maxY, widget.y + widget.height);
  });

  const contentWidth = maxX - minX;
  const contentHeight = maxY - minY;
  const { width: viewWidth, height: viewHeight } = useCanvasStore.getState().viewport;

  // Calculate zoom to fit with padding
  const padding = 50;
  const zoomX = (viewWidth - padding * 2) / contentWidth;
  const zoomY = (viewHeight - padding * 2) / contentHeight;
  const newZoom = Math.min(zoomX, zoomY, 2); // Cap at 200%

  // Center content
  const centerX = (minX + maxX) / 2;
  const centerY = (minY + maxY) / 2;

  useCanvasStore.getState().setViewport({
    zoom: newZoom,
    panX: viewWidth / 2 - centerX * newZoom,
    panY: viewHeight / 2 - centerY * newZoom,
  });
}
```

## Reference Files

| File | Purpose |
|------|---------|
| `src/state/useCanvasStore.ts` | Viewport and selection state |
| `src/components/canvas/CanvasRenderer.tsx` | DOM canvas rendering |
| `src/components/canvas/CanvasViewport.tsx` | Viewport transform layer |
| `src/hooks/useCanvasGestures.ts` | Pan/zoom gesture handling |
| `src/utils/canvasCoordinates.ts` | Coordinate conversion utilities |
