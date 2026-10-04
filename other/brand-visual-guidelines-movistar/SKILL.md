---
name: Brand Visual Guidelines - Movistar
key: brand-visual-guidelines-movistar
description: Fuente única de verdad para paleta cromatica, tipografías y espaciados de la identidad visual vigente de Movistar. Consumido por la HTML Component Library y por cualquier skill que genere output visual.
version: 2.0.0
owner: superreal
status: active
source: 091022_Movistar_Refresh_Guidelines.pptx + 2025_Movistar_Toolkit_OnePage.pdf
---

# Brand Visual Guidelines - Movistar

Fuente única de verdad visual. Todos los archivos que generen HTML, CSS o cualquier output visual consumen estas definiciones. Ningun componente define colores o tipografías propios.

> **HEX del azul confirmado:** #0066FF (confirmado por el cliente, junio 2026).

---

## 1. Paleta cromática

### Colores principales

| Token | Color | HEX | Rol |
|---|---|---|---|
| `--movistar-blue` | Azul Movistar | `#0066FF` | Color principal. Identifica la marca. |
| `--movistar-white` | Blanco Movistar | `#FFFAF5` | Fondo prioritario. No es blanco puro. |
| `--movistar-black` | Negro Movistar | `#262423` | Transmite calidad y toque premium. |

### Colores secundarios

| Token | Color | HEX |
|---|---|---|
| `--movistar-blue-light` | Azul claro | `#D3EEFF` |
| `--movistar-green-light` | Verde claro | `#CEF7BF` |
| `--movistar-yellow-light` | Amarillo claro | `#FFE99C` |
| `--movistar-coral-light` | Coral claro | `#FFC5A8` |
| `--movistar-blue-dark` | Azul oscuro | `#022D67` |
| `--movistar-green-dark` | Verde oscuro | `#38552B` |
| `--movistar-yellow-dark` | Amarillo oscuro | `#5E4A09` |
| `--movistar-coral-dark` | Coral oscuro | `#62301A` |

### Proporción orientativa de uso

- 40% Azul Movistar
- 30% Blanco Movistar
- 10% Negro Movistar
- 20% Colores secundarios (repartidos entre los cuatro claros)

### Reglas de combinación

- No mezclar dos colores secundarios distintos en una misma pieza.
- El Azul Movistar debe estar siempre presente como ancla cromatica en toda comunicación.
- No usar colores secundarios oscuros como fondo. Los fondos validos son: Azul, Blanco, Negro (excepcional), y secundarios claros.
- Máximo un contenedor destacado por pieza.
- No combinar contenedor destacado + palabra resaltada en título. Elegir uno.

### Referencias Pantone / RAL (para producción)

| Color | Pantone | RAL |
|---|---|---|
| Azul Movistar #0066FF | 2386C | 5015 |
| Azul claro #D3EEFF | 657C | 250 85 10 |
| Azul oscuro #022D67 | 294C | 5013 |
| Verde claro #CEF7BF | 2274C | 140 85 20 |
| Verde oscuro #38552B | 2266C | 130 40 30 |
| Amarillo claro #FFE99C | 2001C | 090 90 40 |
| Amarillo oscuro #5E4A09 | 2308C | 100 40 30 |
| Coral claro #FFC5A8 | 473C | 050 80 30 |
| Coral oscuro #62301A | 1545C | 050 30 20 |
| Blanco Movistar #FFFAF5 | 9285C | 9001 |
| Negro Movistar #262423 | 419C | 8022 |

---

## 2. Tipografia

### Tipografia corporativa: Movistar Sans

Tipografia exclusiva con licencia. Variable font con eje de peso (wght: 300-800) y eje de inclinación (slnt: 0-90).

| Peso | font-weight | Uso principal |
|---|---|---|
| Extrabold | 800 | Titulares de impacto, hero, precios destacados |
| Bold | 700 | Titulares secundarios, CTAs |
| Medium | 500 | Subtitulos, etiquetas, labels |
| Regular | 400 | Body text, parrafos |
| Light | 300 | Disclaimers, texto legal, notas al pie |

Las italicas (oblique 90deg) se reservan para resaltar palabras clave o términos en otros idiomas.

**La tipografía se inyecta con el slot `{{FONT_FACE_MIN}}` de `movistar-visual-production`** (los woff2 viven como archivos en `brand/fonts/` y assemble.py los embebe; nunca se copia base64 a mano).

### Fallbacks web-safe

```
font-family: "Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
```

**Importante:** el fallback anterior (tipografía "Telefónica") es de la identidad anterior y no debe usarse.

---

## 3. Logotipo: la M (resumen de valores)

- **Color por defecto:** Azul Movistar (#0066FF)
- **Versión invertida:** Blanco Movistar (#FFFAF5)
- **Tamaño mínimo digital:** 20px (nunca inferior a 60px en formatos digitales)
- **Tamaño mínimo impresión:** 10mm

Para las reglas completas de uso (prioridades de color, posición, área de protección, lockups, Do's/Don'ts), ver `brand-visual-composition-movistar` sección 1.

---

## 4. Espaciados (escala base)

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 40px;
  --space-2xl: 64px;
}
```

---

## 5. CSS variables (copiar en cualquier HTML del sistema)

```css
:root {
  /* Paleta principal */
  --movistar-blue: #0066FF;
  --movistar-white: #FFFAF5;
  --movistar-black: #262423;

  /* Paleta secundaria */
  --movistar-blue-light: #D3EEFF;
  --movistar-green-light: #CEF7BF;
  --movistar-yellow-light: #FFE99C;
  --movistar-coral-light: #FFC5A8;
  --movistar-blue-dark: #022D67;
  --movistar-green-dark: #38552B;
  --movistar-yellow-dark: #5E4A09;
  --movistar-coral-dark: #62301A;

  /* Semánticos */
  --movistar-primary: var(--movistar-blue);
  --movistar-bg: var(--movistar-white);
  --movistar-text: var(--movistar-black);
  --movistar-text-muted: #6F7176;
  --movistar-cta: var(--movistar-blue);
  --movistar-cta-hover: #005EEB; /* Brand Guardian v4 */

  /* Tipografia: el @font-face entra por slot {{FONT_FACE_MIN}} (movistar-visual-production) */
  --font-family: "Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;

  /* Espaciados */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 40px;
  --space-2xl: 64px;
}

body {
  font-family: var(--font-family);
  color: var(--movistar-text);
  background-color: var(--movistar-bg);
  line-height: 1.5;
}

h1 { font-size: 2.25rem; font-weight: var(--font-weight-extrabold); line-height: 1.15; color: var(--movistar-text); }
h2 { font-size: 1.75rem; font-weight: var(--font-weight-regular); line-height: 1.2; color: var(--movistar-text); } /* subtitulos en Regular: jerarquía por tamaño, no por peso (Refresh Guidelines 2025) */
h3 { font-size: 1.25rem; font-weight: var(--font-weight-medium); line-height: 1.3; color: var(--movistar-text); }
p  { font-size: 1rem; font-weight: var(--font-weight-regular); }
```

---

## 6. Contraste y accesibilidad

Para la matriz WCAG completa (7x7 con niveles AAA/AA/A/Prohibido), los colores semánticos con estados hover, y las reglas Do's/Don'ts de color por tipo de fondo, ver `brand-visual-composition-movistar` secciones 3 y 4.

Regla rápida: Negro sobre Blanco Movistar (AAA) y Blanco sobre Azul Movistar (AA) son siempre seguros. Secundarios claros sobre Blanco Movistar están prohibidos.

---

## Mantenimiento

- Este archivo es la ÚNICA fuente de tokens visuales del sistema. Ningún otro archivo define colores ni tipografías.
- HEX del azul: #0066FF, confirmado por el cliente en junio 2026 y alineado con las Refresh Guidelines 2025. Cerrado.
- Si se obtiene acceso al design system de Movistar (Figma, tokens JSON), migrar a ese formato y deprecar este archivo.
- Cambios mayores incrementan `versión`.
