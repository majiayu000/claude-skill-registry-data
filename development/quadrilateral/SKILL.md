---
name: quadrilateral
description: Create quadrilateral geometry figures with vertices, angles, diagonals, and labels. Use when rendering quadrilaterals in mini-lessons or geometry questions.
---

# Quadrilateral Figure Skill

This skill guides you through creating quadrilateral visualizations using the `QuadrilateralFigure` component.

## When to Use This Skill

Invoke this skill when:
- Creating geometry mini-lessons involving quadrilaterals
- Rendering cuadrados, rectángulos, rombos, paralelogramos, trapecios, cometas
- Visualizing quadrilateral properties (parallel sides, equal sides, right angles, diagonals)
- Building interactive quadrilateral explorations
- Demonstrating área de cuadriláteros, propiedades de paralelogramos, etc.

## Supported Types

The component supports 9 quadrilateral types:
- `cuadrado` - Square (4 equal sides, 4 right angles)
- `rectangulo` - Rectangle (opposite sides equal, 4 right angles)
- `rombo` - Rhombus (4 equal sides, opposite angles equal)
- `paralelogramo` - Parallelogram (opposite sides parallel and equal)
- `trapecio` - Trapezoid (1 pair of parallel sides)
- `trapecio-isosceles` - Isosceles trapezoid (equal legs)
- `trapecio-rectangulo` - Right trapezoid (2 right angles)
- `cometa` - Kite (2 pairs of adjacent equal sides)
- `irregular` - Irregular quadrilateral

## Quick Start

### Forma más simple: Usando fromType (Recomendado)

```tsx
import { QuadrilateralFigure } from '@/components/figures/QuadrilateralFigure';

// Cuadrado de 100px
<QuadrilateralFigure fromType={{ type: 'cuadrado', size: 100 }} />

// Rectángulo de 120x80
<QuadrilateralFigure fromType={{ type: 'rectangulo', size: 120, height: 80 }} />

// Rombo con ángulo de 60°
<QuadrilateralFigure fromType={{ type: 'rombo', size: 80, angle: 60 }} />

// Trapecio isósceles
<QuadrilateralFigure
  fromType={{ type: 'trapecio-isosceles', size: 120, height: 80, baseRatio: 0.5 }}
/>
```

### Con marcas automáticas

```tsx
// Paralelogramo con marcas de lados paralelos y ángulos rectos
<QuadrilateralFigure
  fromType={{ type: 'paralelogramo', size: 100, height: 70, angle: 70 }}
  autoParallelMarks
  autoEqualMarks
  autoRightAngleMarkers
  showGrid
/>
```

### Con diagonales

```tsx
// Cuadrado con diagonales visibles
<QuadrilateralFigure
  fromType={{ type: 'cuadrado', size: 100 }}
  showDiagonals
  diagonals={{
    showIntersection: true,
    strokeStyle: 'dashed',
  }}
/>
```

### Usando ángulos (fromAngles)

Construir un cuadrilátero especificando los 4 ángulos interiores:

```tsx
// Ángulos simples (constraint genérico)
<QuadrilateralFigure fromAngles={[90, 90, 90, 90]} />

// Rombo con ángulos específicos (4 lados iguales)
<QuadrilateralFigure
  fromAngles={{
    angles: [60, 120, 60, 120],
    constraint: 'equalSides'
  }}
/>

// Paralelogramo (lados opuestos iguales)
<QuadrilateralFigure
  fromAngles={{
    angles: [70, 110, 70, 110],
    constraint: 'equalOppositeSides'
  }}
/>
```

**Nota importante:** A diferencia de los triángulos, 4 ángulos no determinan una única forma de cuadrilátero. Por ejemplo, 90-90-90-90 puede ser cualquier rectángulo. El parámetro `constraint` especifica qué tipo de cuadrilátero crear:

- `'generic'` (default): Forma razonable con proporciones equilibradas
- `'equalSides'`: 4 lados iguales (familia de rombos)
- `'equalOppositeSides'`: Lados opuestos iguales (familia de paralelogramos)
- `'cyclic'`: Inscrito en un círculo (ángulos opuestos deben sumar 180°)

### Usando vértices (control total)

Cuando necesitas control preciso sobre las coordenadas:

```tsx
<QuadrilateralFigure
  vertices={[
    { x: 100, y: 50, label: 'A' },
    { x: 300, y: 50, label: 'B' },
    { x: 300, y: 200, label: 'C' },
    { x: 100, y: 200, label: 'D' },
  ]}
  showGrid
/>
```

---

## Props Reference

### Construcción del cuadrilátero (usar UNO de estos)

| Prop | Type | Description |
|------|------|-------------|
| `fromType` | `FromTypeConfig` | **Recomendado.** Construir desde tipo predefinido |
| `fromAngles` | `[n,n,n,n] \| FromAnglesConfig` | Construir desde 4 ángulos interiores |
| `fromSquare` | `FromSquareConfig` | Construir cuadrado desde centro y lado |
| `fromRectangle` | `FromRectangleConfig` | Construir rectángulo desde centro y dimensiones |
| `vertices` | `[LabeledPoint, LabeledPoint, LabeledPoint, LabeledPoint]` | Control total de coordenadas |

### fromType

```typescript
interface FromTypeConfig {
  type: QuadrilateralType;  // 'cuadrado', 'rectangulo', 'rombo', etc.
  size: number;             // Tamaño base (ancho para rect, diagonal para rombo)
  height?: number;          // Alto (para rect, trapecio, cometa)
  angle?: number;           // Ángulo en grados (para rombo, paralelogramo)
  baseRatio?: number;       // Ratio base menor/mayor (para trapecios, 0-1)
  centerX?: number;         // Centro X (default: auto)
  centerY?: number;         // Centro Y (default: auto)
  rotation?: number;        // Rotación en grados (default: 0)
}
```

### fromAngles

Construye un cuadrilátero especificando los 4 ángulos interiores (deben sumar 360°).

```typescript
// Forma simple: array de 4 ángulos
fromAngles={[90, 90, 90, 90]}

// Forma completa con configuración
interface FromAnglesConfig {
  angles: [number, number, number, number];  // 4 ángulos en grados (suma = 360°)
  constraint?: QuadAngleConstraint;          // Tipo de restricción (default: 'generic')
  size?: number;                             // Tamaño máximo (default: 150)
  rotation?: number;                         // Rotación en grados
  centerX?: number;                          // Centro X (default: 200)
  centerY?: number;                          // Centro Y (default: 150)
}

type QuadAngleConstraint =
  | 'generic'           // Forma genérica con proporciones equilibradas
  | 'equalSides'        // 4 lados iguales (familia de rombos)
  | 'equalOppositeSides'// Lados opuestos iguales (familia de paralelogramos)
  | 'cyclic';           // Inscrito en círculo (ángulos opuestos suman 180°)
```

**Restricciones por constraint:**
- `generic`: No hay restricciones adicionales
- `equalSides`: Los ángulos opuestos deben ser iguales (α₁=α₃, α₂=α₄)
- `equalOppositeSides`: Los ángulos opuestos deben ser iguales
- `cyclic`: Los ángulos opuestos deben sumar 180° (α₁+α₃=180°, α₂+α₄=180°)

### fromSquare

```typescript
interface FromSquareConfig {
  center: { x: number; y: number };
  side: number;              // Longitud del lado
  rotation?: number;         // Rotación en grados
}
```

### fromRectangle

```typescript
interface FromRectangleConfig {
  center: { x: number; y: number };
  width: number;
  height: number;
  rotation?: number;
}
```

### LabeledPoint

```typescript
interface LabeledPoint {
  x: number;
  y: number;
  label?: string;     // Etiqueta del vértice (ej: 'A', 'B', 'C', 'D')
  labelOffset?: { x: number; y: number };
}
```

### Side Configuration

```typescript
interface QuadSideConfig {
  label?: string;                      // Etiqueta del lado
  measurement?: string;                // Medida con unidades
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  showMeasurement?: boolean;
  parallelGroup?: number;              // Grupo de lados paralelos (1 o 2)
  parallelMarks?: number;              // Número de marcas (1, 2, 3)
  equalGroup?: number;                 // Grupo de lados iguales
  equalMarks?: number;                 // Número de marcas de igualdad
}
```

### Angle Configuration

```typescript
interface QuadAngleConfig {
  label?: string;
  showArc?: boolean;
  arcRadius?: number;
  color?: string;
  showDegrees?: boolean;
  isRightAngle?: boolean;              // Mostrar marcador de ángulo recto
}
```

### Diagonal Configuration

```typescript
interface DiagonalConfig {
  show?: boolean;
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  strokeWidth?: number;
  showIntersection?: boolean;          // Mostrar punto de intersección
  intersectionLabel?: string;          // Etiqueta del punto
  d1Label?: string;                    // Etiqueta diagonal 1
  d2Label?: string;                    // Etiqueta diagonal 2
}
```

### Visual Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fill` | `string` | `'rgba(59,130,246,0.15)'` | Color de relleno |
| `fillOpacity` | `number` | - | Opacidad del relleno |
| `stroke` | `string` | `'rgb(59,130,246)'` | Color del borde |
| `strokeWidth` | `number` | `2` | Ancho del borde |
| `showGrid` | `boolean` | `false` | Mostrar cuadrícula |
| `gridSize` | `number` | `20` | Tamaño de celda |
| `showVertices` | `boolean` | `true` | Mostrar puntos en vértices |
| `vertexRadius` | `number` | `4` | Radio de puntos |
| `showDiagonals` | `boolean` | `false` | Mostrar diagonales |
| `autoParallelMarks` | `boolean` | `false` | Detectar y marcar lados paralelos |
| `autoEqualMarks` | `boolean` | `false` | Detectar y marcar lados iguales |
| `autoRightAngleMarkers` | `boolean` | `false` | Detectar y marcar ángulos rectos |
| `autoDiagonalBisectionMarks` | `boolean` | `false` | Mostrar marcas de bisección en diagonales |
| `autoDiagonalEqualMarks` | `boolean` | `false` | Mostrar marcas de igualdad en diagonales |
| `autoDiagonalRightAngle` | `boolean` | `false` | Mostrar ángulo recto cuando diagonales son perpendiculares |
| `autoAngleArcs` | `boolean` | `false` | Mostrar arcos de ángulo con grados en todos los vértices |

### SVG Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `number` | auto | Ancho del SVG |
| `height` | `number` | auto | Alto del SVG |
| `viewBox` | `string` | auto | ViewBox personalizado |
| `padding` | `number` | `40` | Padding alrededor |
| `className` | `string` | - | Clases CSS adicionales |

---

## Common Patterns

### Propiedades del Cuadrado

```tsx
<QuadrilateralFigure
  fromType={{ type: 'cuadrado', size: 100 }}
  sides={[
    { label: 'a' },
    { label: 'a' },
    { label: 'a' },
    { label: 'a' },
  ]}
  showDiagonals
  diagonals={{ showIntersection: true }}
  autoEqualMarks
  autoRightAngleMarkers
/>
```

### Área del Rectángulo

```tsx
<QuadrilateralFigure
  fromType={{ type: 'rectangulo', size: 120, height: 80 }}
  sides={[
    { label: 'base', measurement: '6 cm' },
    { label: 'altura', measurement: '4 cm' },
    { label: 'base' },
    { label: 'altura' },
  ]}
  autoRightAngleMarkers
  showGrid
/>
```

### Rectángulo con Diagonales Iguales

```tsx
<QuadrilateralFigure
  fromType={{ type: 'rectangulo', size: 120, height: 80 }}
  showDiagonals
  autoRightAngleMarkers
  autoDiagonalBisectionMarks   // Diagonales se bisectan
  autoDiagonalEqualMarks       // Diagonales son iguales
/>
// Los rectángulos tienen diagonales iguales que se bisectan
```

### Propiedades del Rombo

```tsx
<QuadrilateralFigure
  fromType={{ type: 'rombo', size: 80, angle: 60 }}
  showDiagonals
  autoEqualMarks
  autoParallelMarks
  autoDiagonalBisectionMarks   // Diagonales se bisectan
  autoDiagonalRightAngle       // Diagonales son perpendiculares
/>
// Diagonales del rombo se bisectan perpendicularmente
```

### Propiedades del Paralelogramo

```tsx
<QuadrilateralFigure
  fromType={{ type: 'paralelogramo', size: 120, height: 80, angle: 70 }}
  autoAngleArcs               // Muestra ángulos con grados automáticamente
  autoParallelMarks
  autoEqualMarks
/>
// Ángulos opuestos son iguales, consecutivos son suplementarios
```

### Trapecio con Bases

```tsx
<QuadrilateralFigure
  fromType={{ type: 'trapecio-isosceles', size: 140, height: 80, baseRatio: 0.5 }}
  sides={[
    { label: 'B', measurement: 'base mayor' },
    { label: 'l' },
    { label: 'b', measurement: 'base menor' },
    { label: 'l' },
  ]}
  autoParallelMarks
  showGrid
/>
```

### Cometa (Kite)

```tsx
<QuadrilateralFigure
  fromType={{ type: 'cometa', size: 100, height: 140 }}
  showDiagonals
  diagonals={{
    showIntersection: true,
    strokeStyle: 'dashed',
  }}
  autoEqualMarks
/>
// Diagonales perpendiculares, una bisecta a la otra
```

---

## Color Palette

| Elemento | Light Mode | Dark Mode |
|----------|-----------|-----------|
| Quadrilateral fill | `fill-blue-200` | `fill-blue-800/50` |
| Quadrilateral stroke | `stroke-blue-600` | `stroke-blue-400` |
| Diagonals | `stroke-purple-500` | `stroke-purple-400` |
| Parallel marks | `stroke-emerald-500` | `stroke-emerald-400` |
| Equal marks | `stroke-amber-500` | `stroke-amber-400` |
| Right angle marker | `stroke-red-500` | `stroke-red-400` |
| Angle arc | `stroke-amber-500` | `stroke-amber-400` |
| Grid | `stroke-gray-200` | `stroke-gray-700` |

---

## Debug Page

Para experimentar interactivamente con todas las opciones:

**URL:** `/admin/figure-debug`

Seleccionar **Cuadrilátero** como tipo de figura.

La página de debug permite:
- **Modo Por Tipo:** Seleccionar tipo de cuadrilátero y ajustar dimensiones
- **Modo Por Ángulos:** Especificar 4 ángulos interiores con selector de constraint
- **Modo Por Vértices:** Control manual de cada vértice
- Seleccionar presets (cuadrado, rectángulo, rombo, paralelogramo, trapecios, cometa)
- Activar/desactivar opciones visuales (diagonales, marcas paralelas, igualdad, ángulos rectos)
- Ver propiedades calculadas (tipo detectado, perímetro, área, convexidad)
- Copiar el código generado

---

## Integration with Mini-Lessons

### In Step Components

```tsx
// En Step2Explore.tsx
import { QuadrilateralFigure } from '@/components/figures/QuadrilateralFigure';

export default function Step2Explore({ isActive }: LessonStepProps) {
  const [showDiagonals, setShowDiagonals] = useState(false);

  return (
    <div className="flex flex-col items-center">
      <QuadrilateralFigure
        fromType={{ type: 'rombo', size: 80, angle: 60 }}
        showDiagonals={showDiagonals}
        autoEqualMarks
      />
      <button onClick={() => setShowDiagonals(!showDiagonals)}>
        {showDiagonals ? 'Ocultar' : 'Mostrar'} diagonales
      </button>
    </div>
  );
}
```

### With Animation

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  <QuadrilateralFigure fromType={{ type: 'cuadrado', size: 100 }} />
</motion.div>
```

---

## Utility Functions

Las funciones matemáticas están disponibles en `@/lib/geometry/quadrilateralUtils`:

```typescript
import {
  // Cálculos básicos
  distance,           // Distancia entre puntos
  midpoint,           // Punto medio
  centroid,           // Centroide del cuadrilátero
  angleAtVertex,      // Ángulo en un vértice (grados)
  perimeter,          // Perímetro
  area,               // Área (fórmula del cordón)

  // Detección de propiedades
  areSidesParallel,       // Si dos lados son paralelos
  areSidesEqual,          // Si dos lados son iguales
  isRightAngle,           // Si un ángulo es recto
  detectParallelSides,    // Detectar todos los pares paralelos
  detectEqualSides,       // Detectar grupos de lados iguales
  detectRightAngles,      // Detectar vértices con ángulo recto
  detectQuadrilateralType, // Detectar tipo de cuadrilátero

  // Validación
  isConvex,               // Si es convexo
  isSelfIntersecting,     // Si se auto-intersecta
  validateQuadrilateral,  // Validación completa
  diagonalIntersection,   // Punto de intersección de diagonales

  // Construcción
  buildSquare,            // Construir cuadrado
  buildRectangle,         // Construir rectángulo
  buildRhombus,           // Construir rombo
  buildParallelogram,     // Construir paralelogramo
  buildTrapezoid,         // Construir trapecio
  buildIsoscelesTrapezoid, // Construir trapecio isósceles
  buildRightTrapezoid,    // Construir trapecio rectángulo
  buildKite,              // Construir cometa
  buildQuadrilateralFromType, // Construir desde tipo
  buildQuadrilateralFromAngles, // Construir desde ángulos

  // Validación de ángulos
  validateQuadrilateralAngles, // Validar que 4 ángulos formen cuadrilátero válido
} from '@/lib/geometry/quadrilateralUtils';
```

### Detect Quadrilateral Type

```typescript
import { detectQuadrilateralType } from '@/lib/geometry/quadrilateralUtils';

const vertices = [
  { x: 0, y: 0 },
  { x: 100, y: 0 },
  { x: 100, y: 100 },
  { x: 0, y: 100 },
];

const type = detectQuadrilateralType(vertices);
// Returns: 'cuadrado'
```

### Calculate Area

```typescript
import { area } from '@/lib/geometry/quadrilateralUtils';

const vertices = [
  { x: 0, y: 0 },
  { x: 100, y: 0 },
  { x: 100, y: 80 },
  { x: 0, y: 80 },
];

const areaValue = area(vertices);
// Returns: 8000 (100 * 80)
```

### Build Quadrilateral from Type

```typescript
import { buildQuadrilateralFromType } from '@/lib/geometry/quadrilateralUtils';

const vertices = buildQuadrilateralFromType({
  type: 'rombo',
  size: 100,
  angle: 60,
  centerX: 200,
  centerY: 150,
});

// Returns: [Point, Point, Point, Point]
```

### Build Quadrilateral from Angles

```typescript
import {
  validateQuadrilateralAngles,
  buildQuadrilateralFromAngles
} from '@/lib/geometry/quadrilateralUtils';

// Validar ángulos antes de construir
const angles: [number, number, number, number] = [60, 120, 60, 120];
const validation = validateQuadrilateralAngles(angles);

if (validation.valid) {
  // Construir rombo con esos ángulos
  const vertices = buildQuadrilateralFromAngles(
    angles,
    'equalSides',  // constraint
    150,           // maxSize
    200,           // centerX
    150            // centerY
  );
  // Returns: [Point, Point, Point, Point]
}
```

---

## Type Hierarchy

```
Cuadriláteros
├── Paralelogramos (2 pares de lados paralelos)
│   ├── Rectángulo (4 ángulos rectos)
│   │   └── Cuadrado (4 lados iguales + 4 ángulos rectos)
│   └── Rombo (4 lados iguales)
│       └── Cuadrado
├── Trapecios (1 par de lados paralelos)
│   ├── Trapecio isósceles (piernas iguales)
│   └── Trapecio rectángulo (2 ángulos rectos)
├── Cometa (2 pares de lados adyacentes iguales)
└── Irregular (sin propiedades especiales)
```

El algoritmo de detección clasifica automáticamente cualquier conjunto de 4 vértices en uno de estos tipos.
