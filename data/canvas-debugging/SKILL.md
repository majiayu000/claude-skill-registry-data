---
name: canvas-debugging
description: Debug canvas layout issues, grid positioning problems, and component overlap. Use when troubleshooting Konva canvas rendering, grid constraints, snap-to-grid behavior, or visual layout mismatches. Includes Canvas→CSS Grid conversion debugging.
allowed-tools: Read, Glob, Grep
---

# Canvas Debugging Skill

Visual Layout Builder의 Konva 기반 Canvas 시스템 디버깅을 위한 전문 스킬입니다. Grid 위치 계산, 컴포넌트 충돌, 스냅 동작 문제를 해결합니다.

## When to Use

- Canvas에서 컴포넌트 위치가 잘못 표시될 때
- Grid 스냅이 예상대로 동작하지 않을 때
- 컴포넌트 겹침(overlap) 문제 발생 시
- Canvas→CSS Grid 변환 오류 디버깅
- Breakpoint 전환 시 레이아웃 문제
- 드래그 앤 드롭 동작 이상
- `components/canvas/` 관련 이슈

## Canvas System Architecture

### Core Components

```
components/canvas/
├── KonvaCanvas.tsx      # Main canvas with Konva Stage/Layer
├── ComponentNode.tsx    # Individual component rendering
├── ComponentPreview.tsx # Drag preview
├── Canvas.tsx           # Canvas + component management
└── index.ts             # Public exports
```

### Canvas Coordinate System

```
Canvas Grid (0-based coordinates)
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│0,0│1,0│2,0│3,0│4,0│5,0│6,0│7,0│8,0│9,0│10 │11 │ Row 0
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│0,1│1,1│2,1│...│...│...│...│...│...│...│...│11,1 Row 1
├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
│...│...│...│...│...│...│...│...│...│...│...│...│ ...
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘

CanvasLayout:
- x: Grid column start (0-based)
- y: Grid row start (0-based)
- width: Number of columns to span
- height: Number of rows to span
```

### CSS Grid Conversion (1-based)

```typescript
// Canvas (0-based) → CSS Grid (1-based)
gridColumn: `${x + 1} / ${x + width + 1}`
gridRow: `${y + 1} / ${y + height + 1}`
gridArea: `${y + 1} / ${x + 1} / ${y + height + 1} / ${x + width + 1}`

// Example: Canvas { x: 0, y: 0, width: 12, height: 1 }
// → CSS Grid: "1 / 1 / 2 / 13" (grid-area format)
```

## Common Issues & Solutions

### Issue 1: Component Position Mismatch

**Symptom**: Component appears in wrong position after drag

**Debug Steps**:

```typescript
// 1. Check pixel-to-grid conversion
const cellWidth = canvasWidth / gridCols
const cellHeight = canvasHeight / gridRows

console.log('Cell dimensions:', { cellWidth, cellHeight })

// 2. Verify snap calculation
const gridX = Math.floor(pixelX / cellWidth)
const gridY = Math.floor(pixelY / cellHeight)

console.log('Grid position:', { gridX, gridY })

// 3. Check responsiveCanvasLayout
console.log('Component layout:', component.responsiveCanvasLayout?.[breakpoint])
```

**Common Causes**:
- `Math.round()` vs `Math.floor()` inconsistency
- Canvas padding/margin not accounted for
- Breakpoint mismatch (editing mobile, viewing desktop)

### Issue 2: Component Overlap Detection

**Symptom**: Components overlap but no warning shown

**Debug with schema-validation.ts**:

```typescript
import { validateSchema } from '@/lib/schema-validation'

const result = validateSchema(schema)

// Check for overlap warnings
const overlapWarnings = result.warnings?.filter(
  w => w.code === 'CANVAS_COMPONENTS_OVERLAP'
)

console.log('Overlapping components:', overlapWarnings)
```

**Overlap Detection Logic**:

```typescript
function checkOverlap(a: CanvasLayout, b: CanvasLayout): boolean {
  // Check if rectangles overlap
  return !(
    a.x + a.width <= b.x ||   // a is left of b
    b.x + b.width <= a.x ||   // b is left of a
    a.y + a.height <= b.y ||  // a is above b
    b.y + b.height <= a.y     // b is above a
  )
}
```

### Issue 3: Grid Snap Not Working

**Symptom**: Components don't snap to grid when dragged

**Debug Steps**:

```typescript
// lib/snap-to-grid.ts
export function snapToGrid(
  x: number,
  y: number,
  cellWidth: number,
  cellHeight: number
): { x: number; y: number } {
  console.log('Input:', { x, y })
  console.log('Cell size:', { cellWidth, cellHeight })

  const snappedX = Math.round(x / cellWidth) * cellWidth
  const snappedY = Math.round(y / cellHeight) * cellHeight

  console.log('Snapped:', { snappedX, snappedY })

  return { x: snappedX, y: snappedY }
}
```

**Check Grid Constraints**:

```typescript
import { GRID_CONSTRAINTS } from '@/lib/schema-utils'

console.log('Grid constraints:', {
  minCols: GRID_CONSTRAINTS.minCols,  // 4
  maxCols: GRID_CONSTRAINTS.maxCols,  // 24
  minRows: GRID_CONSTRAINTS.minRows,  // 4
  maxRows: GRID_CONSTRAINTS.maxRows   // 50
})
```

### Issue 4: Canvas Out of Bounds

**Symptom**: Component placed outside grid bounds

**Validation Code**: `CANVAS_OUT_OF_BOUNDS`

```typescript
function validateBounds(layout: CanvasLayout, gridCols: number, gridRows: number) {
  const issues = []

  if (layout.x < 0 || layout.y < 0) {
    issues.push('CANVAS_NEGATIVE_COORDINATE')
  }

  if (layout.x + layout.width > gridCols) {
    issues.push(`Out of bounds: x(${layout.x}) + width(${layout.width}) > gridCols(${gridCols})`)
  }

  if (layout.y + layout.height > gridRows) {
    issues.push(`Out of bounds: y(${layout.y}) + height(${layout.height}) > gridRows(${gridRows})`)
  }

  return issues
}
```

### Issue 5: Breakpoint Layout Inheritance

**Symptom**: Component has layout in mobile but not in desktop

**Debug**:

```typescript
// Check responsiveCanvasLayout for all breakpoints
const component = schema.components.find(c => c.id === 'c1')

console.log('Canvas layouts by breakpoint:')
for (const bp of schema.breakpoints) {
  const layout = component?.responsiveCanvasLayout?.[bp.name]
  console.log(`  ${bp.name}:`, layout || 'MISSING')
}

// After normalization
const normalized = normalizeSchema(schema)
const normalizedComponent = normalized.components.find(c => c.id === 'c1')

console.log('After normalization:')
for (const bp of normalized.breakpoints) {
  const layout = normalizedComponent?.responsiveCanvasLayout?.[bp.name]
  console.log(`  ${bp.name}:`, layout || 'STILL MISSING')
}
```

### Issue 6: CSS Grid Conversion Errors

**Symptom**: AI-generated code doesn't match canvas layout

**Debug canvas-to-grid.ts**:

```typescript
import { canvasToGridPositions } from '@/lib/canvas-to-grid'

const positions = canvasToGridPositions(
  schema.components,
  'desktop',
  12,  // gridCols
  8    // gridRows
)

console.log('Grid positions:')
positions.forEach(p => {
  console.log(`  ${p.componentId}:`)
  console.log(`    gridColumn: ${p.gridColumn}`)
  console.log(`    gridRow: ${p.gridRow}`)
  console.log(`    gridArea: ${p.gridArea}`)
})
```

**Expected Format**:

```
c1 (Header):
  gridColumn: "1 / 13"    // Full width (12 cols)
  gridRow: "1 / 2"        // 1 row height
  gridArea: "1 / 1 / 2 / 13"
```

## Visual Layout Descriptor Debugging

```typescript
import { describeVisualLayout } from '@/lib/visual-layout-descriptor'

const description = describeVisualLayout(
  schema.components,
  'desktop',
  12,
  8
)

console.log('Summary:', description.summary)
console.log('\nRow by row:')
description.rowByRow.forEach(row => console.log('  ', row))

console.log('\nSpatial relationships:')
description.spatialRelationships.forEach(rel => console.log('  ', rel))

console.log('\nImplementation hints:')
description.implementationHints.forEach(hint => console.log('  ', hint))
```

## Canvas Validation Codes

| Code | Type | Description |
|------|------|-------------|
| `CANVAS_LAYOUT_ORDER_MISMATCH` | Warning | Canvas order ≠ DOM order |
| `COMPLEX_GRID_LAYOUT_DETECTED` | Warning | Side-by-side components |
| `CANVAS_COMPONENTS_OVERLAP` | Warning | Components overlapping |
| `CANVAS_OUT_OF_BOUNDS` | Warning | Outside grid bounds |
| `CANVAS_ZERO_SIZE` | Warning | width=0 or height=0 |
| `CANVAS_NEGATIVE_COORDINATE` | **Error** | x<0 or y<0 |
| `CANVAS_FRACTIONAL_COORDINATE` | Warning | Non-integer coordinates |
| `CANVAS_COMPONENT_NOT_IN_LAYOUT` | Warning | Not in layout.components |
| `MISSING_CANVAS_LAYOUT` | Warning | No canvas position |

## Debugging Konva Rendering

### Stage/Layer Issues

```typescript
// In KonvaCanvas.tsx
useEffect(() => {
  console.log('Stage dimensions:', {
    width: stageRef.current?.width(),
    height: stageRef.current?.height()
  })

  console.log('Layer children:', layerRef.current?.children?.length)
}, [])
```

### Component Node Position

```typescript
// In ComponentNode.tsx
const handleDragEnd = (e: Konva.KonvaEventObject<DragEvent>) => {
  const node = e.target
  console.log('Drag end position:', {
    x: node.x(),
    y: node.y(),
    absolutePosition: node.absolutePosition()
  })

  // Convert to grid
  const gridX = Math.floor(node.x() / cellWidth)
  const gridY = Math.floor(node.y() / cellHeight)
  console.log('Grid position:', { gridX, gridY })
}
```

## Grid Constraint Validation

```typescript
import { calculateMinimumGridSize } from '@/lib/grid-constraints'

// Check if grid can be reduced
const { minCols, minRows } = calculateMinimumGridSize(
  schema.components,
  'desktop'
)

console.log('Minimum required grid:', { minCols, minRows })
console.log('Current grid:', {
  cols: breakpoint.gridCols,
  rows: breakpoint.gridRows
})

if (breakpoint.gridCols < minCols || breakpoint.gridRows < minRows) {
  console.warn('Grid too small for components!')
}
```

## Quick Debug Checklist

```bash
# 1. Check current breakpoint
console.log('Current breakpoint:', currentBreakpoint)

# 2. Verify grid configuration
console.log('Grid config:', breakpoint)

# 3. Log all component positions
schema.components.forEach(c => {
  const layout = c.responsiveCanvasLayout?.[currentBreakpoint]
  console.log(`${c.id} (${c.name}):`, layout || 'NO LAYOUT')
})

# 4. Run validation
const result = validateSchema(schema)
console.log('Validation:', result)

# 5. Check CSS Grid output
const gridPositions = canvasToGridPositions(
  schema.components,
  currentBreakpoint,
  breakpoint.gridCols,
  breakpoint.gridRows
)
console.log('CSS Grid positions:', gridPositions)
```

## Reference Files

- `components/canvas/KonvaCanvas.tsx` - Canvas 렌더링
- `components/canvas/ComponentNode.tsx` - 컴포넌트 노드
- `lib/canvas-to-grid.ts` - Canvas→CSS Grid 변환
- `lib/canvas-utils.ts` - Canvas 유틸리티
- `lib/grid-constraints.ts` - Grid 제약 조건
- `lib/snap-to-grid.ts` - 스냅 로직
- `lib/schema-validation.ts` - Canvas 검증 로직
- `lib/visual-layout-descriptor.ts` - 시각적 레이아웃 설명
