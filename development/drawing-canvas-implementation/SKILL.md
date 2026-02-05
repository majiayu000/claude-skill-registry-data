---
name: drawing-canvas-implementation
description: Implement real-time collaborative drawing canvas with brush tools, color picker, undo/clear functionality, and canvas-to-image export. Use when building drawing UI, handling stroke synchronization, managing drawing state, or uploading drawings to storage.
compatibility: HTML5 Canvas API, React hooks, real-time event handling, Convex file storage
metadata:
  author: PictionAI
  category: frontend
  frameworks: Next.js, React, Canvas API
---

# Drawing Canvas Implementation

## Overview

This skill implements a full-featured Pictionary drawing canvas with real-time collaborative features, local drawing tools (brush, eraser, color picker), and integration with Convex file storage for drawing export and archival.

## Core Architecture

### Canvas State Management

```typescript
interface DrawingState {
  strokes: Stroke[]; // Array of all strokes
  currentStroke: Point[]; // Current drawing in progress
  currentColor: string; // Hex color
  currentSize: number; // Brush size in pixels
  isErasing: boolean; // Eraser mode toggle
  canUndo: boolean; // Undo availability
}

interface Stroke {
  points: Point[]; // Array of coordinates
  color: string; // Stroke color
  size: number; // Brush size
  isEraser: boolean; // Is eraser stroke
  timestamp: number; // When drawn
}

interface Point {
  x: number;
  y: number;
  pressure?: number; // Pen pressure (0-1) for tablets
}
```

## Component Structure

### DrawingCanvas Component

Main canvas component with all drawing tools.

```typescript
interface DrawingCanvasProps {
  gameId: Id<"games">;
  turnId: Id<"turns">;
  isDrawer: boolean; // Can draw if true
  onDrawingUpdate?: (strokes: Stroke[]) => void;
  onDrawingComplete?: (imageUrl: string) => void;
  timeLimit: number; // In seconds
}
```

### Drawing Tools

#### Brush Tool

- **Mode**: Normal drawing
- **Default Size**: 3-20px adjustable
- **Color**: Any hex color via picker
- **Pressure Sensitivity**: Optional for tablet support

#### Eraser Tool

- **Mode**: Removes strokes (or paints white)
- **Size**: 3-50px adjustable
- **Option**: Erase individual strokes or continuous area

#### Color Picker

- **Palette**: Predefined colors + custom hex input
- **Current Color**: Display + picker
- **Recent Colors**: Last 5 used colors

#### Undo

- **Action**: Remove last stroke
- **Limit**: Full history (no limit)
- **Button State**: Disabled when no strokes

#### Clear

- **Action**: Clear entire canvas
- **Confirmation**: Ask before clear (optional)

## Event Handling

### Mouse Events

```typescript
// Mouse down - start stroke
canvas.addEventListener("mousedown", (e) => {
  const point = getCanvasPoint(e);
  currentStroke = [point];
  drawPoint(point);
});

// Mouse move - continue stroke
canvas.addEventListener("mousemove", (e) => {
  if (!isDrawing) return;
  const point = getCanvasPoint(e);
  currentStroke.push(point);
  drawLine(currentStroke[currentStroke.length - 2], point);
});

// Mouse up - finish stroke
canvas.addEventListener("mouseup", (e) => {
  if (currentStroke.length > 0) {
    strokes.push({
      points: currentStroke,
      color: currentColor,
      size: currentSize,
      isEraser: isErasing,
      timestamp: Date.now(),
    });
  }
  currentStroke = [];
  redrawCanvas();
});
```

### Touch Events (Mobile)

```typescript
canvas.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  const point = getCanvasPoint(touch);
  currentStroke = [point];
});

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  const point = getCanvasPoint(touch);
  currentStroke.push(point);
  drawLine(currentStroke[currentStroke.length - 2], point);
});

canvas.addEventListener('touchend', (e) => {
  strokes.push({ points: currentStroke, ... });
  currentStroke = [];
  redrawCanvas();
});
```

## Canvas Rendering

### Line Drawing (Smooth)

```typescript
function drawLine(from: Point, to: Point) {
  ctx.strokeStyle = currentColor;
  ctx.lineWidth = currentSize;
  ctx.lineJoin = "round";
  ctx.lineCap = "round";

  ctx.beginPath();
  ctx.moveTo(from.x, from.y);
  ctx.lineTo(to.x, to.y);
  ctx.stroke();
}
```

### Full Canvas Redraw

```typescript
function redrawCanvas() {
  // Clear canvas
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Redraw all strokes
  for (const stroke of strokes) {
    ctx.strokeStyle = stroke.color;
    ctx.lineWidth = stroke.size;

    ctx.beginPath();
    ctx.moveTo(stroke.points[0].x, stroke.points[0].y);

    for (let i = 1; i < stroke.points.length; i++) {
      ctx.lineTo(stroke.points[i].x, stroke.points[i].y);
    }
    ctx.stroke();
  }
}
```

## Canvas Export & Upload

### Capture Canvas as Image

```typescript
function captureCanvas(): Promise<Blob> {
  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => {
        resolve(blob!);
      },
      "image/png",
      0.95
    );
  });
}
```

### Upload to Convex Storage

```typescript
const uploadDrawing = useAction(
  api.actions.uploadDrawing.uploadDrawingScreenshot
);

async function saveDrawing() {
  const blob = await captureCanvas();
  const storageId = await uploadDrawing({
    gameId,
    turnId,
    drawingBlob: await blob.arrayBuffer(), // Base64 or buffer
  });

  return storageId; // Can fetch later with getUrl()
}
```

## Real-time Synchronization (Optional)

### Broadcast Strokes

```typescript
// On each stroke completion
const syncStrokes = useMutation(api.mutations.drawings.syncStrokes);

async function broadcastStroke(stroke: Stroke) {
  await syncStrokes({
    turn_id: turnId,
    stroke: stroke,
  });
}
```

### Listen for Remote Strokes

```typescript
const remoteStrokes = useQuery(api.queries.drawings.getTurnDrawing, {
  turn_id: turnId,
});

// Subscribe to updates
useEffect(() => {
  if (remoteStrokes?.strokes) {
    redrawCanvas(); // Redraw with remote strokes
  }
}, [remoteStrokes]);
```

## State Management Pattern

```typescript
export const DrawingCanvas = ({ isDrawer, ...props }: DrawingCanvasProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [currentColor, setCurrentColor] = useState("#000000");
  const [currentSize, setCurrentSize] = useState(5);
  const [isErasing, setIsErasing] = useState(false);

  useEffect(() => {
    if (!canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d")!;

    // Event handlers...
    // Canvas drawing logic...
  }, [strokes, currentColor, currentSize, isErasing]);

  const handleUndo = () => {
    setStrokes(strokes.slice(0, -1));
  };

  const handleClear = () => {
    if (confirm("Clear canvas?")) {
      setStrokes([]);
    }
  };

  return (
    <div className="drawing-container">
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        className="border-2 border-gray-300"
        style={{ cursor: isDrawer ? "crosshair" : "default" }}
      />
      <ToolBar
        color={currentColor}
        onColorChange={setCurrentColor}
        size={currentSize}
        onSizeChange={setCurrentSize}
        isErasing={isErasing}
        onEraserToggle={setIsErasing}
        onUndo={handleUndo}
        onClear={handleClear}
        canUndo={strokes.length > 0}
      />
    </div>
  );
};
```

## Canvas Sizing

### Responsive Canvas

```typescript
function resizeCanvas() {
  const container = canvas.parentElement!;
  const rect = container.getBoundingClientRect();

  canvas.width = rect.width;
  canvas.height = rect.height;

  redrawCanvas(); // Redraw at new size
}

window.addEventListener("resize", resizeCanvas);
```

### Aspect Ratio Preservation

```css
.drawing-container {
  aspect-ratio: 4 / 3;
  width: 100%;
  max-width: 800px;
}

canvas {
  width: 100%;
  height: 100%;
}
```

## Performance Optimization

### Stroke Batching

- Buffer strokes locally, sync every 500ms
- Reduces mutation calls
- Improves responsiveness

### Canvas Optimization

- Use `requestAnimationFrame` for smooth drawing
- Implement dirty rectangle invalidation
- Clear only changed regions (advanced)

### Memory Management

- Limit stroke history to ~1000 strokes
- Compress old strokes data if needed
- Clear temporary Point arrays

## Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support (15+)
- **Mobile**: Touch events supported

## Common Patterns

### Detect Drawing Changes

```typescript
const hasDrawn = strokes.length > 0;
```

### Save on Turn End

```typescript
useEffect(() => {
  if (turnState === "completed") {
    saveDrawing();
  }
}, [turnState]);
```

### Prevent Accidental Close

```typescript
useEffect(() => {
  const handleBeforeUnload = (e: BeforeUnloadEvent) => {
    if (strokes.length > 0) {
      e.preventDefault();
      e.returnValue = "";
    }
  };

  window.addEventListener("beforeunload", handleBeforeUnload);
  return () => window.removeEventListener("beforeunload", handleBeforeUnload);
}, [strokes]);
```

## See Also

- `components/game/drawing-canvas.tsx` - Full component implementation
- `components/game/tool-bar.tsx` - Tool controls UI
- Canvas API Docs: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
