---
name: schema-development
description: Create and modify Visual Layout Builder schema components, breakpoints, and layouts. Use when working with types/schema.ts, creating new components, adding breakpoints, or modifying layout configurations. Helps ensure Component Independence architecture compliance.
allowed-tools: Read, Glob, Grep
---

# Schema Development Skill

Visual Layout Builder의 Schema 시스템 개발을 위한 전문 스킬입니다. Component Independence 아키텍처를 준수하며 schema를 생성, 수정, 검증합니다.

## When to Use

- `types/schema.ts` 타입 정의 작업
- 새로운 컴포넌트 생성 또는 수정
- Breakpoint 설정 및 관리
- Layout 구조 설계
- Schema 검증 로직 개선
- `lib/schema-utils.ts` 또는 `lib/schema-validation.ts` 작업

## Core Architecture Principles

### 1. Component Independence (핵심 원칙)

각 컴포넌트는 독립적으로 자신의 positioning, layout, styling을 정의합니다:

```typescript
interface Component {
  id: string                      // "c1", "c2", etc. (auto-generated)
  name: string                    // PascalCase required
  semanticTag: SemanticTag        // HTML5 semantic tags
  positioning: ComponentPositioning  // fixed, sticky, static, absolute, relative
  layout: ComponentLayout         // flex, grid, container, none
  styling?: ComponentStyling      // Optional visual properties
  responsive?: ResponsiveBehavior // Breakpoint-specific overrides
  responsiveCanvasLayout?: ResponsiveCanvasLayout  // Canvas grid positions
}
```

### 2. Semantic Tag Mapping

각 시맨틱 태그에 권장되는 positioning:

| Semantic Tag | Recommended Positioning | Use Case |
|--------------|------------------------|----------|
| `header` | `sticky` or `fixed` | 페이지 상단 네비게이션 |
| `nav` | `sticky` | 네비게이션 메뉴 |
| `main` | `static` | 주요 콘텐츠 영역 |
| `aside` | `sticky` or `static` | 사이드바 |
| `footer` | `static` | 페이지 하단 |
| `section` | `static` | 콘텐츠 섹션 |
| `article` | `static` | 독립적인 콘텐츠 |
| `div` | `static` | 일반 컨테이너 |
| `form` | `static` | 폼 영역 |

### 3. Layout Types

```typescript
// Flexbox (primary for page structure)
layout: {
  type: "flex",
  flex: {
    direction: "column",  // or "row"
    justify: "start",     // start, end, center, between, around, evenly
    items: "stretch",     // start, end, center, baseline, stretch
    gap: 16
  }
}

// Grid (for card layouts, galleries)
layout: {
  type: "grid",
  grid: {
    cols: 3,              // or "repeat(3, 1fr)"
    rows: "auto",
    gap: 24
  }
}

// Container (centered content)
layout: {
  type: "container",
  container: {
    maxWidth: "7xl",
    padding: 16,
    centered: true
  }
}
```

## Creating New Components

### Step 1: Generate Component ID

```typescript
import { generateComponentId } from '@/lib/schema-utils'

const newId = generateComponentId(existingComponents)
// Returns: "c1", "c2", etc.
```

### Step 2: Define Component Structure

```typescript
const newComponent: Component = {
  id: newId,
  name: "HeroSection",  // PascalCase!
  semanticTag: "section",
  positioning: {
    type: "static"
  },
  layout: {
    type: "flex",
    flex: {
      direction: "column",
      justify: "center",
      items: "center",
      gap: 24
    }
  },
  styling: {
    height: "500px",
    className: "min-h-[500px] px-4 text-center"
  },
  responsiveCanvasLayout: {
    mobile: { x: 0, y: 1, width: 4, height: 3 },
    tablet: { x: 0, y: 1, width: 8, height: 3 },
    desktop: { x: 0, y: 1, width: 12, height: 3 }
  }
}
```

### Step 3: Add to Schema

```typescript
// In store action or utility function
const updatedComponents = [...schema.components, newComponent]
const updatedLayouts = {
  ...schema.layouts,
  [currentBreakpoint]: {
    ...currentLayout,
    components: [...currentLayout.components, newId]
  }
}
```

## Breakpoint Management

### Dynamic Breakpoint Support

```typescript
// Valid breakpoint names
const validNames = [
  "mobile",      // Standard
  "tablet",      // Standard
  "desktop",     // Standard
  "laptop",      // Custom
  "4k",          // Custom (numbers allowed)
  "mobile-sm",   // Custom with hyphen
  "tablet_lg"    // Custom with underscore
]

// Invalid names (will fail validation)
const invalidNames = [
  "",                    // Empty
  "mobile@tablet",       // Special characters
  "mobile tablet",       // Spaces
  "모바일",               // Unicode
  "a".repeat(101),       // Too long (>100 chars)
  "constructor"          // Reserved word
]
```

### Creating Breakpoints

```typescript
const newBreakpoint: Breakpoint = {
  name: "laptop",
  minWidth: 1024,
  gridCols: 12,
  gridRows: 10
}

// Maximum 10 breakpoints allowed
```

## Validation Rules

### Component Validation

1. **Name must be PascalCase**: `MyComponent`, `HeroSection`
2. **ID must be unique**: No duplicates in components array
3. **Positioning type required**: Must specify type field
4. **Layout type required**: Must specify type field

### Canvas Layout Validation

```typescript
// 9 Canvas validation codes
- CANVAS_LAYOUT_ORDER_MISMATCH    // Canvas order ≠ DOM order
- COMPLEX_GRID_LAYOUT_DETECTED    // Side-by-side components
- CANVAS_COMPONENTS_OVERLAP       // Components overlapping
- CANVAS_OUT_OF_BOUNDS           // Outside grid bounds
- CANVAS_ZERO_SIZE               // width=0 or height=0
- CANVAS_NEGATIVE_COORDINATE     // x<0 or y<0 (ERROR)
- CANVAS_FRACTIONAL_COORDINATE   // Non-integer coordinates
- CANVAS_COMPONENT_NOT_IN_LAYOUT // Not in layout.components
- MISSING_CANVAS_LAYOUT          // No canvas position
```

## Schema Normalization

항상 스키마 수정 후 `normalizeSchema()` 호출:

```typescript
import { normalizeSchema } from '@/lib/schema-utils'

// After any schema modification
const normalizedSchema = normalizeSchema(updatedSchema)
```

이는 Breakpoint Inheritance (Mobile → Tablet → Desktop)를 처리합니다.

## Common Patterns

### GitHub-style Layout

```typescript
{
  structure: "sidebar-main",
  components: ["c1", "c2", "c3"],  // Header, Sidebar, Main
  roles: {
    header: "c1",
    sidebar: "c2",
    main: "c3"
  }
}
```

### Dashboard Layout

```typescript
{
  structure: "horizontal",
  components: ["c1", "c2", "c3", "c4"],  // Header, SideMenu, Content, Footer
  containerLayout: {
    type: "flex",
    flex: { direction: "column" }
  }
}
```

## Reference Files

- `types/schema.ts` - 모든 타입 정의
- `lib/schema-utils.ts` - 스키마 유틸리티 함수
- `lib/schema-validation.ts` - 검증 로직
- `lib/component-library.ts` - 사전 정의 컴포넌트
- `docs/schema-v2-examples.md` - 스키마 예제
