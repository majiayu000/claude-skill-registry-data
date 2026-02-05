---
name: facciones
description: Diseñador de facciones para SyV - creación completa con estructura canónica de 11 categorías, relaciones validadas y coherencia narrativa

---

# Skill: Faction Designer (Completo)

## Competencia

Especialista en diseñar y normalizar facciones para el universo SyV siguiendo la estructura canónica completa de 11 categorías. Garantiza coherencia narrativa, relaciones validadas y adaptación según complejidad (Simple/Compleja).

## Cuándo se Activa

Al:
- Ejecutar `/crear-faccion`
- Crear/editar archivos en `1_trasfondo/facciones/`
- Mencionar "facción", "crear facción", "organización", "normalizar facción"

## Estructura Canónica Completa

### I. METADATOS (YAML Frontmatter)
```yaml
---
title: [Nombre oficial]
folder: 1_trasfondo/facciones/[subcarpeta]
description: [Resumen breve 1-2 líneas]
tags:
  - faccion
  - [tipo: oficial/proscrita/secreta]
  - [ubicacion/otros slugs]
facciones: [Array opcional de facciones relacionadas]
---
```

### II. IDENTIFICACIÓN BÁSICA
- Nombre oficial
- Alias/Apodos (si aplica)
- Notas terminológicas (si hay ambigüedad)
- Tipo: Oficial/Proscrita/Secreta/Mítica
- Nivel de secretismo (bajo/medio/alto/absoluto)
- Estatus legal (oficial/tolerada/perseguida/mítica)

### III. CONTEXTO Y PROPÓSITO
- Introducción narrativa (1-3 párrafos: origen, lema, poder actual)
- Objetivos principales (declarados + ocultos si difieren)
- Ideología/Filosofía
- Motivaciones

### IV. ORGANIZACIÓN Y ESTRUCTURA
- Tipo de organización (jerárquica/horizontal/descentralizada/tribal/células)
- Estructura jerárquica (si aplica):
  - Liderazgo (líder supremo, consejo, veteranos)
  - Militancia (rangos intermedios)
  - Apoyo (voluntarios, auxiliares)
- Tamaño aproximado (total + por ubicación)
- Divisiones/Ramas/Dicasterios (si aplica)
- Reclutamiento (métodos, requisitos, iniciación)

### V. OPERACIONES Y MÉTODOS
- Modus operandi general
- Métodos y tácticas (estándar + casos complejos)
- Actividades principales (por tipo)
- Especializaciones (con sub-detalles)
- Equipamiento (armas/herramientas/símbolos)

### VI. RECURSOS Y CAPACIDADES
- Recursos materiales (propiedades, infraestructura, tesoro)
- Recursos humanos (expertises, red de contactos)
- Recursos de conocimiento (bibliotecas, archivos, inteligencia)
- Capacidades especiales (habilidades únicas)
- Debilidades/Limitaciones

### VII. RELACIONES EXTERNAS
- Relaciones institucionales (si es sub-facción)
- Relaciones diplomáticas:
  - Aliados
  - Neutrales/Pragmáticos
  - Rivales/Tensiones
  - Enemigos
- Alianzas secretas/Infiltraciones
- Patrocinadores/Fuentes de legitimidad
- Popularidad/Reputación pública

### VIII. PRESENCIA Y ALCANCE
- Alcance geográfico (local/regional/nacional/internacional)
- Presencia territorial por ubicación:
  - Sede principal
  - Bases secundarias
  - Personal aproximado
- Zonas de control/influencia
- Rutas secretas

### IX. ELEMENTOS TEMPORALES
- Investigaciones actuales (2178)
- Casos y operaciones activas (2178)
- Evolución temporal (origen, hitos, tendencia)

### X. INFORMACIÓN PRIVILEGIADA
- Doctrina (enseñanzas públicas vs prácticas secretas)
- Información secreta (no exponer a jugadores):
  - Secretos internos
  - Pactos ocultos
  - Conspiraciones
  - Contradicciones
- Personalidad institucional (características, cultura, debilidades)
- Significado narrativo (meta: función, temas, potencial)

### XI. PERSONAJES Y REFERENCIAS
- Personajes clave (nombre, cargo, rol, nota)
- Referencias cruzadas: `[^id]: Facción / "Apodo"`
- Relación con otros elementos (ubicaciones, eventos, artefactos)

## Adaptación según Complejidad

### Facciones SIMPLES (< 50 líneas)
**Para**: Grupos pequeños, secretos, descentralizados, células, facciones míticas

**Categorías obligatorias**:
- I. Metadatos
- II. Identificación Básica (mínima)
- III. Contexto y Propósito
- VII. Relaciones Externas (mínima)
- X. Información Privilegiada (secretos GM)
- XI. Referencias

**Estilo**: Narrativa fluida con subtítulos mínimos o sin ellos

**Ejemplos**: Cazadores de Pesadillas, Shipibo-Conibo, Canales Ocultos, Iluminati

### Facciones COMPLEJAS (> 50 líneas)
**Para**: Organizaciones grandes, oficiales, con jerarquías claras, instituciones

**Categorías obligatorias**:
- TODAS las 11 categorías (completas o parciales según aplique)

**Estilo**: Estructura con subtítulos claros (## y ###), secciones bien definidas

**Ejemplos**: Iglesia de Dársena, SIA, Fuerzas Armadas, Exorcistas, Congregación

## Clasificación de Facciones

**Oficiales** (4):
- Iglesia de Dársena, SIA, Fuerzas Armadas, Gremio de Comercio

**Proscritas** (6):
- Arpistas, Resistencia Subterránea, Los Umbanda, Traficantes de Almas, Saqueadores, Hackers

**Secretas** (5):
- Guardianes de la Memoria, Canales Ocultos, Masones, Cazadores de Pesadillas, Shipibo-Conibo

**Mixtas/Especiales** (4):
- Exorcistas (rama de Iglesia), Congregación (rama de Iglesia), Refugiados y Parias (no-facción), Iluminati (mítica)

## Matriz de Relaciones (Validación)

### IMPOSIBLES (Enemigos Irreconciliables)
❌ **NUNCA pueden ser aliados**:
- SIA ↔ Arpistas
- SIA ↔ Hackers/Criptógrafos
- Iglesia ↔ Resistencia Subterránea
- Iglesia ↔ Los Umbanda
- Fuerzas Armadas ↔ Resistencia Subterránea

### TENSAS (Oficiales pero con conflicto)
⚠️ **Cooperación forzada con fricción**:
- Iglesia ↔ Fuerzas Armadas (cooperación oficial, tensa)
- Armada ↔ Ejército (tensión Dársena vs Córdoba)
- SIA ↔ Exorcistas (competencia por jurisdicción)

### SECRETAS (Requieren justificación narrativa)
🔒 **Posibles solo con secreto**:
- Arpistas ↔ Guardianes de la Memoria (infiltración)
- Guardianes ↔ Sectores de Iglesia (relación peligrosa)
- Sectores de Fuerzas Armadas ↔ Sectores de Iglesia (conspiración)
- Hackers ↔ DNS/SIA (reclutamiento forzoso)

## Workflow: Crear Facción Completa

### Fase 1: Recopilación Inicial
Solicitar al usuario:
1. **Nombre oficial** de la facción
2. **Tipo**: Oficial / Proscrita / Secreta / Mítica
3. **Alcance**: Local / Regional / Nacional / Internacional
4. **Complejidad estimada**: Simple (< 50 líneas) / Compleja (> 50 líneas)
5. **Propósito principal** en 1 frase
6. **Ubicación base** (Dársena, Córdoba, otro)
7. **Tamaño aproximado** (decenas, cientos, miles, indefinido)
8. **¿Tiene información secreta para GM?** (sí/no)

### Fase 2: Desarrollo de Categorías
Según complejidad (Simple/Compleja), desarrollar categorías:

**Para Facciones SIMPLES**:
- Narrativa fluida que integre naturalmente:
  - Identidad, tipo, alcance
  - Propósito y métodos
  - Relaciones clave (2-3 facciones)
  - Secretos GM (si aplica)
  - Referencias mínimas

**Para Facciones COMPLEJAS**:
- Estructura con subtítulos que cubra:
  - Introducción general
  - Estructura organizacional (jerarquía, ramas, tamaño)
  - Métodos operativos (con especialización si aplica)
  - Recursos y capacidades
  - Relaciones institucionales detalladas
  - Presencia geográfica
  - Casos/operaciones activas (2178)
  - Personajes clave
  - Significado narrativo

### Fase 3: Validación
1. **Coherencia cronológica**: Validar contra cronología 2020-2178
2. **Coherencia geográfica**: Validar ubicaciones y alcance
3. **Coherencia de relaciones**: Verificar contra Matriz (Imposibles/Tensas/Secretas)
4. **Coherencia tecnológica**: Verificar que recursos respeten Anatema Mecánico
5. **Coherencia narrativa**: Verificar que motivaciones sean claras

### Fase 4: Formato Final
1. **Metadatos YAML correctos**:
   ```yaml
   ---
   title: [Nombre Oficial]
   folder: 1_trasfondo/facciones/[subcarpeta]
   description: [Resumen 1-2 líneas]
   tags:
     - faccion
     - [tipo]
     - [otros slugs relacionados]
   ---
   ```

2. **Nombres en negrita**: Primera mención de facciones en **negrita**

3. **Referencias al pie**:
   ```markdown
   ---

   ### Referencias

   [^sia]: Sagrada Inquisición Argentina (SIA) / "Los Cirujanos del Alma"
   [^iglesia]: La Iglesia de Dársena
   ```

4. **Información secreta marcada**:
   ```markdown
   **Información secreta (no exponer a jugadores):**
   [Contenido solo para GM]
   ```

### Fase 5: Ubicación del Archivo
Determinar subcarpeta según tipo:
- **Oficiales mayores**: `iglesia-de-darsena/`, `fuerzas-armadas/`, `union/`
- **Ramas de Iglesia**: `iglesia-de-darsena/[nombre].md`
- **Proscritas/Secretas**: `facciones-menores/[nombre].md`

Generar archivo en: `1_trasfondo/facciones/[subcarpeta]/[nombre-kebab].md`

## Restricciones y Advertencias

✅ **HACER**:
- Adaptar estructura según complejidad (Simple/Compleja)
- Validar relaciones contra Matriz
- Incluir información secreta GM cuando sea relevante
- Usar referencias cruzadas con notas al pie
- Nombres de facciones en **negrita** primera mención
- Respetar Anatema Mecánico en recursos tecnológicos

❌ **EVITAR**:
- Crear alianzas imposibles (SIA + Arpistas, Iglesia + Resistencia)
- Facciones sin propósito claro
- Relaciones sin justificación narrativa
- Tecnología prohibida sin explicación
- Información contradictoria con canon establecido
