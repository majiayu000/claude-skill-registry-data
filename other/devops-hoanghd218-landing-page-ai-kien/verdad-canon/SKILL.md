---
name: verdad-canon
description: Validador de coherencia canónica - garantiza que afirmaciones sobre SyV son verdaderas en el universo, ejecutando cambios automáticos moderados para asegurar consistencia narrativa
---

# Skill: Garantizador de Verdad Canónica

## Competencia

Especialista en garantizar la coherencia de afirmaciones sobre el universo SyV mediante validación exhaustiva del canon y ejecución autónoma de cambios MODERADOS. Funciona como un "assert" sobre el universo: dada una afirmación (ej: "No existen vehículos a combustión en Dársena"), este skill:

1. Revisa TODO el canon (cronología, ubicaciones, personajes, narrativas, tecnología)
2. Identifica referencias que contradicen la afirmación
3. Categoriza cada referencia (IGNORAR / CAMBIAR / REPLANTEAR)
4. Ejecuta cambios manteniendo estilo narrativo y coherencia
5. Valida que la afirmación sea ahora verdadera en el universo
6. Genera reporte detallado de cambios realizados

Único en su funcionalidad: no crea contenido nuevo (como `/crear-personaje`) ni solo valida (como `/validar-canon`), sino que **repara el canon** para garantizar verdad de una afirmación.

## Cuándo se Activa

Automáticamente al ejecutarse:
- `/crear-verdad "afirmación de hecho sobre universo SyV"`

O cuando se detecta:
- Afirmaciones directas sobre estado del canon (ej: "En Dársena solo hay transporte eléctrico")
- Solicitud explícita de garantizar coherencia de un hecho específico
- Necesidad de "fijar" una verdad canónica

## Expertise de Validación

### Tier 1: Archivos Críticos (Obligatorio revisar PRIMERO)

**Tecnología y Anatema Mecánico** (Definen qué es posible):
- `1_trasfondo/codex/anatema-mecanico.md` - FUENTE DE VERDAD sobre tecnología permitida/prohibida post-2061
- `1_trasfondo/codex/otras-tecnologias-prohibidas.md` - Restricciones específicas, vigilancia, castigos
- `2_atlas/tecnologia-y-ciencia/anatema-mecanico.md` - Estado técnico actual (2178)
- `2_atlas/tecnologia-y-ciencia/computacion-y-datos.md` - Sistemas de datos permitidos
- `2_atlas/tecnologia-y-ciencia/electricidad.md` - FUENTE DE VERDAD sobre infraestructura energética, Nodos, reactores, vigilancia
- `2_atlas/tecnologia-y-ciencia/` - Especificaciones de tecnología disponible

**Infraestructura Crítica** (Definen funcionamiento ciudad):
- `1_trasfondo/facciones/iglesia-de-darsena/iglesia.md` - Ministerio de Infraestructura y Sistemas Críticos, jerarquía técnica
- `2_atlas/ciudades/darsena/` - Ubicación Torres Hidropónicas, Nodos, generadores (información clasificada)

### Tier 2: Contexto Temporal y Geográfico (Muy importante)

**Cronología** (Define cuándo es posible):
- `1_trasfondo/cronologia/cronología.md` - FUENTE INMUTABLE de hitos y eras (2020-2178)
- Hitos inamovibles: 2029 Noche Global, 2030 Meteorito, 2035 Nacimiento QIA, 2048 Fin de los Secretos, 2061 Gran Silencio, 2061 Anatema, 2161 Confederación

**Geografía de Ciudades** (Define dónde es posible):
- `2_atlas/ciudades/darsena/` (7 zonas) - Capital de facto, máximo control religioso
- `2_atlas/ciudades/cordoba.md` - República industrial, 30M habitantes
- `2_atlas/ciudades/mendoza.md` - Región andina, 2M habitantes
- `2_atlas/ciudades/san-luis/san-luis.md` - Control militar, 1M habitantes
- `2_atlas/ciudades/fuerte-san-martin/fuerte-san-martin.md` - Nueva prosperidad, 1.5M habitantes

### Tier 3: Actores y Métodos (Importante)

**Personajes** (Definen quién se desplaza, cómo):
- `3_personajes/` - Cómo personajes principales/secundarios usan transporte
- Validar: Si personaje llega en "auto de combustión", ¿es coherente con fecha/ubicación?

**Facciones** (Definen métodos de transporte):
- `1_trasfondo/facciones/iglesia-de-darsena/` - Iglesia controla tecnología
- `1_trasfondo/facciones/fuerzas-armadas/` - Armada/Ejército tienen acceso exclusivo
- `1_trasfondo/facciones/union/` - Gremio controla comercio/transporte
- Facciones clandestinas: Arpistas (preservan tecnología prohibida)

**Distancias y Velocidades** (Definen posibilidad de viajes):
- `.claude/database/geographic-database.yml` - Velocidades realistas (pie 5km/día, caballo 40km/día, aire 500km/día)

### Tier 4: Narrativas y Casos de Borde (Casos de borde)

**Diegesis** (Historias y relatos):
- `4_diegesis/` - Narrativas con transporte, desplazamientos
- Ejemplo: "Damián llega a Dársena en avión" → validar coherencia

**Aventuras** (Escenarios de juego):
- `5_aventuras/` - Escenarios con viajes, movilidad

**Clima** (Contexto ambiental):
- `2_atlas/climas/` - Dársena siempre lluvia perpetua, clima post-guerra

## Capacidades

### 1. Análisis de Afirmación
- **Parseo**: Extraer sujeto, contexto, negación vs afirmación
- **Clasificación**: Determinar tipo (tecnología, geografía, persona, tiempo)
- **Alcance**: Específico (Dársena) vs general (confederación) vs universal
- **Coherencia inicial**: Verificar si contradice canon inamovible
- **Ejemplo**: "No existen vehículos a combustión en Dársena"
  - Sujeto: vehículos a combustión
  - Contexto: en Dársena
  - Tipo: NEGACIÓN + TECNOLOGÍA
  - Alcance: ESPECÍFICO (Dársena) → revisar también confederadas

### 2. Búsqueda Exhaustiva
- **Patrones Grep**: Motor, vehículo, narrativo, por ciudades (4+ categorías)
- **Archivos**: Paralela en 2_atlas, 3_personajes, 1_trasfondo, 4_diegesis, 5_aventuras
- **Compilación**: Crear índice de todas referencias encontradas
- **Deduplicación**: Eliminar menciones idénticas

### 3. Categorización de Referencias
- **IGNORAR**: Referencia compatible CON afirmación (sin cambios necesarios)
- **CAMBIAR**: Contradice pero reemplazo es trivial (palabra, frase, máximo párrafo)
- **REPLANTEAR**: Contradice severamente, requiere reescritura 3+ párrafos manteniendo personajes
- **BLOQUEAR**: Imposible reconciliar, requiere decisión manual

### 4. Evaluación de Impacto Narrativo
- **Cosmético**: Nombre de tecnología (bajo impacto)
- **Ambientación**: Descriptor (impacto medio)
- **Trama**: Personaje depende de ello (alto impacto)
- **Cascada**: ¿Afecta otros archivos?
- **Severidad**: Trivial → Moderado → Severo → Imposible

### 5. Ejecución de Cambios
- **Edit Tool**: Reemplazar líneas específicas manteniendo contexto
- **Write Tool**: Si cambio muy grande, reescribir archivo
- **Orden**: Tier 1 (crítica) → Tier 2 → Tier 3 → Tier 4
- **Validación en tiempo real**: Verificar sintaxis post-cambio
- **Rollback**: Si Edit falla, detener y reportar

### 6. Validación Post-Cambios
- Ejecutar `/validar-canon` (completo) - detectar nuevas contradicciones
- Ejecutar `/validar-metadatos` (archivos modificados) - YAML intacto
- Ejecutar `/validar-permisos` (si hay bloques <!-- 🔐 -->) - coherencia de secretos
- Rescan de referencias - verificar resolución
- **Criterios**: ✅ VÁLIDO / ⚠️ ADVERTENCIAS / ❌ INVÁLIDO

### 7. Generación de Reporte
- **8 secciones**: Análisis → Búsqueda → Categorización → Ejecución → Validación → Estadísticas → Resultado → Siguiente
- **Detalle por cambio**: Archivo, línea, antes/después, validación
- **Estadísticas**: Referencias encontradas, ignoradas, cambiadas, replanteadas
- **Advertencias**: Nuevas contradicciones, validaciones fallidas

## Restricciones Críticas

| Aspecto | Regla | Justificación |
|---------|-------|---------------|
| **Alcance de cambios** | MODERADO: Párrafos completos, NO capítulos | Preservar narrativa compleja, mantener coherencia |
| **Archivos intocables** | NINGUNO - revisar TODO AL INICIO | Usuario aprobó revisión total del canon |
| **Orden de revisión** | Tier 1 → 2 → 3 → 4 | Criticidad: tecnología → geografía → personajes → narrativa |
| **Combustibles fósiles** | NO existen (excepto generadores de electricidad) | Post-2061 bajo Anatema Mecánico |
| **Ciudades confederadas** | Dársena primaria, revisar también: Córdoba, Mendoza, San Luis, FSM | Cobertura regional consistente |
| **Preservación de estilo** | OBLIGATORIO: Mantener tono, ritmo, emociones originales | No cambiar "color" narrativo |
| **Perspectiva temporal** | SIEMPRE desde 2178 (Hermano Archivista Pedro) | Fuentes válidas: físicas, NO digitales |
| **Hitos inamovibles** | NO pueden modificarse: 2030 Meteorito, 2048 Fin de los Secretos, 2061 Gran Silencio, 2061 Anatema, 2161 Confederación | Canon base inquebrantable |

## Workflows Comunes

### Workflow: Afirmación sobre Tecnología
```
Afirmación: "No existen vehículos a combustión en [región]"
  ↓
Tier 1: Revisar anatema-mecanico.md → ¿Permitido post-2061?
  ↓
Tier 2: Revisar ciudades atlas → ¿Menciona vehículos fósil?
  ↓
Tier 3: Revisar personajes → ¿Alguien usa vehículo fósil?
  ↓
Tier 4: Revisar diegesis → ¿Hay escenas con vehículos fósil?
  ↓
Categorizar → Cambiar/Replantear referencias
  ↓
Validar post-cambios
  ↓
Generar resumen
```

### Workflow: Afirmación sobre Ubicación
```
Afirmación: "[Característica específica] en [ciudad]"
  ↓
Tier 2: Revisar descripción ciudad → ¿Coherente?
  ↓
Tier 1: Revisar contexto tecnológico → ¿Posible?
  ↓
Tier 3: Revisar personajes que viven en ciudad → ¿Qué dicen?
  ↓
Tier 4: Revisar diegesis con ubicación → ¿Hay contradicción?
  ↓
Categorizar → Cambiar/Replantear referencias
  ↓
Validar post-cambios
  ↓
Generar resumen
```

## Validaciones Ejecutadas Automáticamente

1. **Canonicidad de Afirmación**: ¿Contradice hitos inamovibles?
2. **Coherencia Temporal**: ¿Año/período soporta la afirmación?
3. **Coherencia Tecnológica**: ¿Anatema Mecánico permite?
4. **Coherencia Geográfica**: ¿Ubicación/distancias realistas?
5. **Coherencia Narrativa**: ¿Personajes/facciones pueden acceder a eso?
6. **Coherencia de Permisos**: ¿Bloques <!-- 🔐 --> siguen siendo válidos?

## Ejemplo de Uso

**Entrada**: `/crear-verdad "No existen vehículos a combustión en Dársena"`

**Flujo**:
1. PARSEO: Sujeto=vehículos combustión, Contexto=Dársena, Tipo=NEGACIÓN
2. BÚSQUEDA: Encontrar 23 referencias (7 ignorar, 12 cambiar, 4 replantear)
3. EJECUCIÓN: Edit 12 archivos, cambios típicos:
   - "autobús de gasolina" → "autobús blindado"
   - "motor a nafta" → "motor eléctrico"
4. REPLANTEAMIENTOS: 4 párrafos reescritos preservando personajes/emociones
5. VALIDACIÓN: /validar-canon PASA, 0 errores nuevos
6. SALIDA: Reporte 8-secciones con estadísticas

**Resultado**: "No existen vehículos a combustión en Dársena" es ahora VERDADERA en canon