---
name: circle
description: Create circle geometry figures with center, radius, sectors, arcs, chords, and angles. Use when rendering circles, circumferences, or sectors in mini-lessons or geometry questions.
---

# Circle Figure Skill

This skill guides you through creating circle visualizations using the `CircleFigure` component.

## When to Use This Skill

Invoke this skill when:
- Creating geometry mini-lessons involving circles or circumferences
- Rendering circles, sectors, or arcs in practice questions
- Visualizing circle properties (radius, diameter, chords, angles)
- Building interactive circle explorations
- Demonstrating area, circumference, sectors, central angles, inscribed angles, etc.

## Quick Start

### Circunferencia simple

```tsx
import { CircleFigure } from '@/components/figures/CircleFigure';

// Circunferencia con centro visible
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  mode="circunferencia"
  showCenter
/>
```

### Circulo relleno (default)

```tsx
// Circulo con relleno azul semitransparente
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  showRadius={{ toAngle: 45, label: 'r' }}
/>
```

### Arco con angulo (API unificada - recomendada)

```tsx
// Arco con angulo central y sector - todo en una configuracion
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  arcs={[{
    startAngle: 0,
    endAngle: 90,
    showAngle: true,      // Muestra arco del angulo central
    showDegrees: true,    // Muestra valor en grados
    showSector: true,     // Muestra sector relleno
    showRadii: true,      // Muestra lineas de radio
  }]}
/>
```

### Multiples arcos

```tsx
// Varios arcos con diferentes colores
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  arcs={[
    { startAngle: 0, endAngle: 90, showAngle: true, showDegrees: true },
    { startAngle: 120, endAngle: 180, showSector: true, showRadii: true },
  ]}
/>
```

### Sector circular (API legacy)

```tsx
// Sector de 90 grados (cuarto de circulo)
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  sector={{ startAngle: 0, endAngle: 90, showRadii: true }}
/>
```

### Arco resaltado (API legacy)

```tsx
// Arco de 120 grados
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  arc={{ startAngle: 30, endAngle: 150, strokeWidth: 4 }}
/>
```

### Angulo central (API legacy)

```tsx
// Angulo central con medida en grados
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  centralAngle={{
    startAngle: 0,
    endAngle: 60,
    showDegrees: true,
  }}
/>
```

### Cuerda

```tsx
// Cuerda entre dos puntos de la circunferencia
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  chords={[
    { fromAngle: 30, toAngle: 150, showEndpoints: true },
  ]}
/>
```

### Con grid de fondo

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  showGrid
/>
```

---

## Props Reference

### Required Props

| Prop | Type | Description |
|------|------|-------------|
| `center` | `LabeledPoint` | Centro del circulo con coordenadas y etiqueta opcional |
| `radius` | `number` | Radio en pixeles SVG |

### LabeledPoint

```typescript
interface LabeledPoint {
  x: number;          // Coordenada X
  y: number;          // Coordenada Y
  label?: string;     // Etiqueta del punto (ej: 'O')
  labelOffset?: { x: number; y: number };  // Ajuste de posicion del label
}
```

### Display Mode

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `standalone` | `boolean` | `true` | `true`: renderiza `<svg>`, `false`: renderiza `<g>` para uso en CartesianPlane |
| `mode` | `'circunferencia' \| 'circulo'` | `'circulo'` | `circunferencia`: solo borde, `circulo`: con relleno |

### Center and Lines

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showCenter` | `boolean` | `false` | Mostrar punto del centro |
| `showRadius` | `boolean \| RadiusConfig` | `false` | Mostrar linea del radio |
| `showDiameter` | `boolean \| DiameterConfig` | `false` | Mostrar linea del diametro |

### RadiusConfig

```typescript
interface RadiusConfig {
  toAngle?: number;        // Angulo en grados (0 = derecha, aumenta en sentido horario)
  label?: string;          // Etiqueta (ej: 'r', '5 cm')
  color?: string;          // Color personalizado
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  showMeasurement?: boolean;
}
```

### DiameterConfig

```typescript
interface DiameterConfig {
  angle?: number;          // Angulo del diametro (0 = horizontal)
  label?: string;          // Etiqueta (ej: 'd', '10 cm')
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  endpointLabels?: [string, string];  // Labels para los extremos
}
```

### Unified Arcs (API Recomendada)

| Prop | Type | Description |
|------|------|-------------|
| `arcs` | `UnifiedArcConfig[]` | Array de arcos con configuracion unificada (preferido sobre sector/arc/centralAngle separados) |

### UnifiedArcConfig

```typescript
interface UnifiedArcConfig {
  startAngle: number;        // Angulo de inicio (grados)
  endAngle: number;          // Angulo de fin (grados)

  // Apariencia del arco
  strokeWidth?: number;      // Ancho del trazo (default: 4)
  color?: string;            // Color del arco y elementos relacionados

  // Opciones unificadas - combina lo que antes eran 3 configs separadas
  showAngle?: boolean;       // Mostrar arco del angulo central en el centro
  showDegrees?: boolean;     // Mostrar valor en grados
  angleLabel?: string;       // Etiqueta personalizada (ej: 'theta', 'alpha')
  angleArcRadius?: number;   // Radio del arco del angulo (default: 25)
  showSector?: boolean;      // Mostrar sector relleno (pie slice)
  sectorFill?: string;       // Color del relleno del sector
  sectorOpacity?: number;    // Opacidad del sector (0-1, default: 0.3)
  showRadii?: boolean;       // Mostrar lineas de radio en los bordes
}
```

**Ventajas de la API unificada:**
- Una sola configuracion en lugar de tres props separadas
- Soporte para multiples arcos con un array
- Menos codigo repetitivo (no hay que especificar los mismos angulos 3 veces)

### Sector and Arc (API Legacy)

| Prop | Type | Description |
|------|------|-------------|
| `sector` | `SectorConfig` | Configuracion del sector circular (legacy) |
| `arc` | `ArcConfig` | Configuracion del arco resaltado (legacy) |

### SectorConfig

```typescript
interface SectorConfig {
  startAngle: number;      // Angulo de inicio (grados)
  endAngle: number;        // Angulo de fin (grados)
  fill?: string;           // Color de relleno
  fillOpacity?: number;    // Opacidad (0-1)
  stroke?: string;         // Color del borde
  showRadii?: boolean;     // Mostrar lineas de radio en los bordes
}
```

### ArcConfig

```typescript
interface ArcConfig {
  startAngle: number;      // Angulo de inicio (grados)
  endAngle: number;        // Angulo de fin (grados)
  strokeWidth?: number;    // Ancho del trazo
  color?: string;          // Color del arco
  showLength?: boolean;    // Mostrar longitud del arco
}
```

### Angles

| Prop | Type | Description |
|------|------|-------------|
| `centralAngle` | `CentralAngleConfig` | Angulo central |
| `inscribedAngle` | `InscribedAngleConfig` | Angulo inscrito |

### CentralAngleConfig

```typescript
interface CentralAngleConfig {
  startAngle: number;      // Angulo de inicio (grados)
  endAngle: number;        // Angulo de fin (grados)
  showDegrees?: boolean;   // Mostrar valor en grados
  label?: string;          // Etiqueta personalizada (ej: 'theta', 'alpha')
  arcRadius?: number;      // Radio del arco de visualizacion
  color?: string;
}
```

### InscribedAngleConfig

```typescript
interface InscribedAngleConfig {
  vertex: LabeledPoint | number;  // Vertice en la circunferencia (punto o angulo)
  arcStart: number;        // Inicio del arco subtendido
  arcEnd: number;          // Fin del arco subtendido
  showDegrees?: boolean;
  label?: string;
  color?: string;
  arcRadius?: number;
}
```

### Chords

| Prop | Type | Description |
|------|------|-------------|
| `chords` | `ChordConfig[]` | Array de configuraciones de cuerdas |

### ChordConfig

```typescript
interface ChordConfig {
  fromAngle: number;       // Punto de inicio (angulo en grados)
  toAngle: number;         // Punto de fin (angulo en grados)
  label?: string;          // Etiqueta de la cuerda
  color?: string;
  strokeStyle?: 'solid' | 'dashed' | 'dotted';
  showEndpoints?: boolean; // Mostrar marcadores en los extremos
}
```

### Points on Circle

| Prop | Type | Description |
|------|------|-------------|
| `points` | `PointOnCircleConfig[]` | Puntos a marcar en la circunferencia |

### PointOnCircleConfig

```typescript
interface PointOnCircleConfig {
  angle: number;           // Angulo en grados (0 = derecha)
  label?: string;          // Etiqueta del punto
  radius?: number;         // Radio del marcador en pixeles
  color?: string;
}
```

### Visual Styling

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fill` | `string` | `'rgba(59,130,246,0.15)'` | Color de relleno (modo circulo) |
| `fillOpacity` | `number` | - | Opacidad del relleno |
| `stroke` | `string` | `'rgb(59,130,246)'` | Color del borde |
| `strokeWidth` | `number` | `2` | Ancho del borde |

### Grid and Background

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showGrid` | `boolean` | `false` | Mostrar cuadricula |
| `gridSize` | `number` | `20` | Tamano de celda |
| `gridColor` | `string` | `'rgb(229,231,235)'` | Color de la cuadricula |

### SVG Options

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `number` | auto | Ancho del SVG |
| `height` | `number` | auto | Alto del SVG |
| `viewBox` | `string` | auto | ViewBox personalizado |
| `padding` | `number` | `40` | Padding alrededor del circulo |
| `className` | `string` | - | Clases CSS adicionales |
| `ariaLabel` | `string` | - | Label para accesibilidad |

---

## Common Patterns

### Area del Circulo

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  mode="circulo"
  showCenter
  showRadius={{ toAngle: 0, label: 'r' }}
  showGrid
/>
// Area = pi * r^2
```

### Longitud de la Circunferencia

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  mode="circunferencia"
  showCenter
  showRadius={{ toAngle: 0, label: 'r' }}
/>
// Circunferencia = 2 * pi * r
```

### Area del Sector (API unificada)

```tsx
// Con la API unificada, todo en un solo arco
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  arcs={[{
    startAngle: 0,
    endAngle: 90,
    showSector: true,
    showRadii: true,
    showAngle: true,
    showDegrees: true,
  }]}
/>
// Area sector = (angulo/360) * pi * r^2
```

### Longitud del Arco (API unificada)

```tsx
// Arco con angulo central - todo en una configuracion
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  arcs={[{
    startAngle: 30,
    endAngle: 150,
    showAngle: true,
    showDegrees: true,
  }]}
/>
// Longitud arco = (angulo/360) * 2 * pi * r
```

### Angulo Inscrito

```tsx
// El angulo inscrito es la mitad del angulo central
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  inscribedAngle={{
    vertex: 180,  // Vertice en la circunferencia (angulo 180 grados)
    arcStart: 60,
    arcEnd: 120,
    showDegrees: true,
  }}
  centralAngle={{
    startAngle: 60,
    endAngle: 120,
    showDegrees: true,
  }}
/>
// Angulo inscrito = angulo central / 2
```

### Radio y Diametro

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  showRadius={{ toAngle: 45, label: 'r' }}
  showDiameter={{ angle: 0, label: 'd' }}
/>
// d = 2r
```

### Cuerda y su Relacion con el Radio

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  chords={[
    { fromAngle: 30, toAngle: 150, label: 'c', showEndpoints: true },
  ]}
  showRadius={{ toAngle: 30, label: 'r' }}
/>
```

### Semicirculo

```tsx
<CircleFigure
  center={{ x: 200, y: 150, label: 'O' }}
  radius={80}
  showCenter
  sector={{
    startAngle: 0,
    endAngle: 180,
    showRadii: true,
  }}
/>
```

---

## Color Palette

| Elemento | Light Mode | Dark Mode |
|----------|-----------|-----------|
| Circle fill | `rgba(59,130,246,0.15)` | `rgba(59,130,246,0.3)` |
| Circle stroke | `rgb(59,130,246)` | `rgb(96,165,250)` |
| Center point | `rgb(239,68,68)` | `rgb(248,113,113)` |
| Radius/Diameter | `rgb(168,85,247)` | `rgb(192,132,252)` |
| Sector fill | `rgba(168,85,247,0.3)` | `rgba(168,85,247,0.4)` |
| Arc | `rgb(245,158,11)` | `rgb(251,191,36)` |
| Angle arc | `rgb(245,158,11)` | `rgb(251,191,36)` |
| Chord | `rgb(16,185,129)` | `rgb(52,211,153)` |
| Grid | `rgb(229,231,235)` | `rgb(75,85,99)` |
| Labels | `rgb(17,24,39)` | `rgb(255,255,255)` |

---

## Debug Page

Para experimentar interactivamente con todas las opciones:

**URL:** `/admin/figure-debug`

Selecciona "Circunferencia" en el selector de tipo de figura.

La pagina de debug permite:
- Seleccionar modo (circulo vs circunferencia)
- Ajustar posicion del centro y radio con sliders
- Activar/desactivar opciones visuales (centro, radio, diametro, grid)
- **Agregar/eliminar arcos con la API unificada** (sector + angulo + arco en uno)
- Configurar cada arco con: angulos, mostrar angulo, mostrar grados, mostrar sector, mostrar radios
- Agregar/eliminar cuerdas con angulos personalizados
- Seleccionar presets (circulo basico, circunferencia, sector 90, semicirculo)
- Ver propiedades calculadas (circunferencia, area, longitud de arcos)
- Copiar el codigo generado con la API unificada

---

## Integration with Mini-Lessons

### In Step Components

```tsx
// En Step2Explore.tsx
import { CircleFigure } from '@/components/figures/CircleFigure';

export default function Step2Explore({ isActive }: LessonStepProps) {
  const [showSector, setShowSector] = useState(false);
  const [sectorAngle, setSectorAngle] = useState(90);

  return (
    <div className="flex flex-col items-center">
      <CircleFigure
        center={{ x: 200, y: 150, label: 'O' }}
        radius={80}
        showCenter
        sector={showSector ? {
          startAngle: 0,
          endAngle: sectorAngle,
          showRadii: true,
        } : undefined}
      />

      <div className="mt-4 space-y-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={showSector}
            onChange={(e) => setShowSector(e.target.checked)}
          />
          Mostrar sector
        </label>

        {showSector && (
          <input
            type="range"
            min="10"
            max="360"
            value={sectorAngle}
            onChange={(e) => setSectorAngle(Number(e.target.value))}
          />
        )}
      </div>
    </div>
  );
}
```

### With Animation

```tsx
import { motion } from 'framer-motion';

// Wrap CircleFigure in motion.div for animations
<motion.div
  initial={{ opacity: 0, scale: 0.8 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.5 }}
>
  <CircleFigure
    center={{ x: 200, y: 150, label: 'O' }}
    radius={80}
    showCenter
  />
</motion.div>
```

### Inside CartesianPlane

```tsx
import { CartesianPlane } from '@/components/figures/CartesianPlane';
import { CircleFigure } from '@/components/figures/CircleFigure';

// Circulo centrado en el origen del plano cartesiano
<CartesianPlane xRange={[-5, 5]} yRange={[-5, 5]} scale={30} showAxes showGrid>
  <CircleFigure
    standalone={false}  // Importante: renderiza <g> en lugar de <svg>
    center={{ x: 0, y: 0, label: 'O' }}
    radius={90}  // En coordenadas del plano (90px = 3 unidades con scale=30)
    showCenter
    showRadius={{ toAngle: 0, label: 'r = 3' }}
  />
</CartesianPlane>
```

---

## Utility Functions

Las funciones matematicas estan disponibles en `@/lib/geometry/circleUtils`:

```typescript
import {
  // Calculos basicos
  circumference,           // Circunferencia = 2 * pi * r
  area,                    // Area = pi * r^2
  arcLength,               // Longitud de arco
  sectorArea,              // Area de sector
  chordLength,             // Longitud de cuerda

  // Conversiones de coordenadas
  polarToCartesian,        // Polar a Cartesiano (convencion SVG)
  cartesianToPolar,        // Cartesiano a Polar
  pointOnCircle,           // Punto en la circunferencia

  // Generacion de paths SVG
  circlePath,              // Path completo del circulo
  describeArc,             // Path de un arco
  describeSector,          // Path de un sector

  // Posicionamiento de labels
  calculateCenterLabelPosition,
  calculateCircumferenceLabelPosition,
  calculateRadiusLabelPosition,
  calculateChordLabelPosition,
  calculateAngleLabelPosition,

  // Validacion
  validateCircle,          // Valida centro y radio
  validateSector,          // Valida angulos del sector
  validateChord,           // Valida angulos de la cuerda

  // Utilidades de angulos
  normalizeAngle,          // Normaliza a 0-360
  angleDifference,         // Diferencia entre angulos
  inscribedAngleFromCentral, // Angulo inscrito = central / 2
} from '@/lib/geometry/circleUtils';
```

### Example Usage

```typescript
import { circumference, area, arcLength, sectorArea } from '@/lib/geometry/circleUtils';

const radius = 5;

console.log('Circunferencia:', circumference(radius));  // 31.416...
console.log('Area:', area(radius));                     // 78.54...
console.log('Longitud arco 90°:', arcLength(radius, 90));  // 7.854...
console.log('Area sector 90°:', sectorArea(radius, 90));   // 19.635...
```

---

## Angle Convention

Los angulos en CircleFigure siguen la convencion SVG:
- **0 grados** = derecha (posicion 3 en un reloj)
- **Los angulos aumentan en sentido horario**
- **90 grados** = abajo
- **180 grados** = izquierda
- **270 grados** = arriba

```
        270°
         |
  180° --O-- 0°
         |
        90°
```

Esto es diferente a la convencion matematica estandar donde los angulos aumentan en sentido antihorario. La convencion SVG se usa porque el eje Y esta invertido en SVG (Y aumenta hacia abajo).
