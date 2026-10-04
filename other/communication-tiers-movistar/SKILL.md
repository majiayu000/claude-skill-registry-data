---
name: Niveles de Comunicación - Movistar
key: communication-tiers-movistar
description: Framework LOVE/CHOOSE/BUY que determina la flexibilidad visual y el enfoque creativo de cada campaña. El Planner clasifica la campaña; el Creative Copywriter adapta el territorio creativo; el Art Director ajusta la rigidez del sistema visual.
version: 1.0.0
owner: superreal
status: active
source: Brand Guardian v4 RAG Movistar (secciones 8 y 9) - validado por Comunicación Movistar
depends_on:
  - brand-voice-movistar
  - brand-visual-composition-movistar
---

# Niveles de Comunicación - Movistar (LOVE / CHOOSE / BUY)

El sistema de marca Movistar se adapta a una pirámide de comunicación con dos polos: **Notoriedad** (rigidez de aplicación) y **Relevancia** (libertad de aplicación). Cada campaña se clasifica en uno de tres niveles que determinan cuánta libertad creativa tiene el equipo.

> Origen: Brand Guardian v4 RAG Movistar, secciones 8 y 9. Esta clasificación es obligatoria: cada campaña DEBE tener un nivel asignado antes de que el Creative Copywriter empiece a idear.

---

## 1. LOVE (máxima libertad)

### Objetivo
Crear conexión emocional con la audiencia. Se centra en valores de marca, no en productos ni precios. Genera cercanía, confianza y engagement.

### Flexibilidad visual
- Máxima libertad creativa. Recursos disruptivos y no convencionales permitidos.
- Paleta de colores secundarios como protagonista (frescura, dinamismo).
- La fotografía puede romper convenciones (encuadres inesperados, grano, colores expresivos).
- Se puede trabajar con el equipo Corporativo de Marca para propuestas excepcionales.

### M Expresiva
En comunicaciones LOVE se pueden usar dos tipos de M expresiva:

**Tipo 1: M protagonista (forma y color intactos)**
- Ampliar tamaño de la M
- Modificar posición
- Integrar en mensajes tipográficos
- Debe ser validado por el equipo de marca si se modifica el sistema de firma

**Tipo 2: Transformación creativa de la M**
- La M se transforma para adaptarse al contenido (festivales, eventos, patrocinios)
- Debe estar vinculada con la realidad (incluso en acabados tecnológicos)
- Solo en contextos donde el reconocimiento de Movistar esté garantizado
- Ejemplo: M en arena del desierto (universo Dune), M formada por luces de concierto

**Don'ts de M Expresiva:**
- No hacerla demasiado compleja
- No transformarla en objetos
- No usar conceptos poco elevados

### Señales para clasificar como LOVE
- Campaña de marca / branding puro
- Contenido cultural o de entretenimiento
- Patrocinios y eventos
- Campañas de posicionamiento emocional
- Sin mención de producto/precio concreto

---

## 2. CHOOSE (libertad moderada)

### Objetivo
Destacar productos, servicios y sus atributos (velocidad 5G+, personalización). Aumentar notoriedad y consideración. Influir en decisión de compra SIN enfocarse en precio.

### Flexibilidad visual
- Recursos gráficos flexibles pero garantizando reconocimiento de marca.
- Elementos gráficos innovadores permitidos para reforzar el mensaje clave.
- Productos pueden aparecer con carácter aspiracional (elevar calidad de pieza).
- Colores secundarios como apoyo, no como protagonistas.

### Contenido
- Beneficios de servicios y productos desde una perspectiva elevada.
- Se pueden comunicar atributos: diversidad, cercanía, adaptación.
- Se muestra la gama amplia de soluciones (capacidad 360°).
- NUNCA precios, ofertas ni promociones.

### Señales para clasificar como CHOOSE
- Lanzamiento de producto/servicio
- Campañas de consideración
- Comunicación de atributos funcionales
- Comparativas implícitas con competencia
- Se nombra el producto pero no su precio

---

## 3. BUY (máxima rigidez)

### Objetivo
Motivar la compra. Se enfoca en precio y promociones.

### Flexibilidad visual
- Uso rígido del sistema de layout y elementos de marca principales (logotipo, tipografía, colores principales).
- Reconocimiento y presencia de marca deben estar asegurados.
- Recursos sencillos y directos: CTAs claros, contenedores.
- Cada pieza debe ser clara, sencilla de comprender y mantener calidad.
- "Menos es más": evitar piezas visualmente pobres o sobrecargadas.

### Contenido
- Precios, beneficios, promociones.
- Composición de precios según reglas de `brand-visual-composition-movistar` (sección 7).
- CTAs de acción directa.

### Señales para clasificar como BUY
- Campaña promocional / oferta
- Comunicación de precio explícito
- Campañas de conversión directa
- Black Friday, campañas estacionales de venta
- Upgrade/cross-sell con precio

---

## Tabla resumen

| Dimensión | LOVE | CHOOSE | BUY |
|-----------|------|--------|-----|
| Foco | Valores, emoción | Producto, atributos | Precio, promoción |
| Paleta | Secundarios como protagonistas | Secundarios como apoyo | Principales (Azul, Blanco, Negro) |
| Layout | Libre, disruptivo | Flexible con reconocimiento | Rígido, sistema estándar |
| M | Puede ser expresiva | Estándar con flexibilidad | Estándar estricto |
| Fotografía | Expresiva, rupturista | Aspiracional con producto | Funcional, limpia |
| Copy | Emocional, cultural | Beneficio elevado | Directo, precio claro |
| Precio | Nunca | Nunca | Siempre |

---

## Cómo usan los agentes esta skill

### Planner (Estrategia de Medios)
- **OBLIGATORIO:** clasifica cada campaña en LOVE / CHOOSE / BUY en su output.
- Criterio: si el brief menciona precio o promoción, es BUY. Si menciona producto sin precio, es CHOOSE. Si es posicionamiento puro, es LOVE.
- Si el brief es ambiguo, propone nivel y lo marca como `ajuste_propuesto` para el humano.
- El nivel se incluye como campo `communication_tier` en el JSON de estrategia.

### Creative Copywriter
- Lee el `communication_tier` de la estrategia del Planner.
- Adapta el territorio creativo al nivel:
  - LOVE: ideas emocionales, culturales, disruptivas. Sin producto ni precio.
  - CHOOSE: ideas centradas en beneficio del producto. Tono aspiracional.
  - BUY: ideas directas, precio protagonista, CTA claro.
- Si el Planner no asignó tier, el Creative Copywriter lo infiere del brief y lo documenta como flag.

### Art Director (Campaign Design)
- Lee el `communication_tier` para ajustar la rigidez del sistema visual:
  - LOVE: puede romper grid, usar M expresiva, colores secundarios libres.
  - CHOOSE: sigue grid pero con flexibilidad en recursos gráficos.
  - BUY: grid estricto, composición de precios según reglas, paleta principal.
- Si la pieza es BUY y no tiene composición de precios correcta, lo marca como flag.

### Campaign Manager
- Verifica en Cierre que el tier asignado es coherente con el brief original.
- Flag si el Creative Copywriter ha escrito copies BUY para una campaña clasificada LOVE o viceversa.

---

## Mantenimiento

- Cualquier cambio requiere validación del equipo de Comunicación Movistar.
- Cambios mayores incrementan `versión`.
- Si se detecta discrepancia con Brand Guardian v4, se sincroniza y documenta.
