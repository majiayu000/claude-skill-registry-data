---
name: content-localizer
description: Adapts AndesRC content for specific regional markets (Mexico, Spain, LATAM). Handles lexical adaptation, cultural references, and geographic narratives. CRITICAL for Mexican market due to term sensitivities.
metadata:
  author: AndesRC
  version: "1.0"
---

# Content Localizer

## Purpose
Adapt content for specific regional markets while preserving brand voice and SEO optimization. This is CRITICAL for cultural authenticity and avoiding offensive errors.

## Market Priority

1. **México (Primary)** - CDMX focus
2. **Colombia** - Bogotá focus  
3. **España** - Madrid/Barcelona focus
4. **Chile** - Santiago focus
5. **Argentina** - Buenos Aires focus

## Lexical Adaptation Tables

### México vs España

| Categoría | México ✅ | España ❌ (Fase 1) | Notas |
|-----------|----------|-------------------|-------|
| Calzado | **Tenis** | Zapatillas | "Zapatillas" evoca ballet/formal en MX |
| Sujeción | **Agujetas** | Cordones | Uso exclusivo MX |
| Ropa | **Playera** | Camiseta | Estándar para ropa deportiva |
| Abrigo | **Sudadera/Chamarra** | Chaqueta | ⚠️ **CRÍTICO**: "Chaqueta" es vulgar en MX |
| Transporte | **Carro/Camión** | Coche/Autobús | Contexto de llegar a entrenamientos |
| Tecnología | **Celular** | Móvil | El dispositivo del coaching |
| Validación | **¡Qué padre!/¡Está chido!** | ¡Qué guay!/¡Mola! | Tono conversacional |

### ⚠️ CRITICAL WARNINGS

```
❌ NEVER use "chaqueta" in Mexican content (vulgar slang for masturbation)
❌ NEVER use "coger" casually in Mexican content (sexual connotation)
✅ Use "tomar" instead of "coger" for "to take"
✅ Use "chamarra" or "sudadera" for jacket/hoodie
```

## Geographic Narratives

### CDMX (Ciudad de México)

**Landmarks to reference:**
- **El Sope**: Pistas de arcilla en la 2da Sección de Chapultepec
- **El Ocotal**: Bosque para entrenamientos de fondo y altura
- **Reforma**: Domingos de "Muévete en Bici" (corredores toman la avenida)
- **Parque de los Viveros**: Popular para principiantes
- **Desierto de los Leones**: Trail running

**Climate & Altitude:**
- Altitud: 2,240m (affects breathing, requires adaptation)
- Temporada de lluvias: Mayo-Octubre (afternoon storms)
- Contaminación: Mention early morning runs to avoid smog

**Safety considerations:**
- Recommend well-lit routes
- Suggest running in groups
- Best hours: 6-8am, 5-7pm (daylight + less traffic)

### Bogotá

**Landmarks:**
- Parque Simón Bolívar
- Ciclovía dominical
- Cerros Orientales (trail)

**Altitude:** 2,640m (even higher than CDMX)

### Madrid/Barcelona (Phase 2)

**Tone adjustment:** More direct, less formal than LATAM Spanish.

## Localization Workflow

### Step 1: Lexical Scan
Replace terms using the adaptation table above.

### Step 2: Geographic Anchoring
Add local references (parks, routes, events) where appropriate.

### Step 3: Cultural Tone
- **LATAM**: More polite, softer tone ("¿Te gustaría...?")
- **Spain**: More direct ("Haz esto...")

### Step 4: Units & Formats
- Use metric system (km, not miles)
- Date format: DD/MM/YYYY for Spain, varies in LATAM

## Output

Produce a localized markdown file with all adaptations applied.

### Localization Metadata

Add to frontmatter:
```yaml
locale: es-MX  # or es-ES, es-CO, etc.
geoTarget: ["Mexico City", "CDMX"]
```
