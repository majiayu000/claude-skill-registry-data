---
name: metadatos
description: Especialista en validación y generación de metadatos YAML (frontmatter) para archivos markdown del proyecto SyV, garantizando coherencia con estándares

---

# Skill: Metadata Validator

## Competencia

Especialista en validación y generación de metadatos YAML (frontmatter) para archivos `.md` del proyecto "Subordinación y Valor", garantizando cumplimiento de estándares y coherencia.

## Cuándo se Activa

Automáticamente al:
- Crear o editar archivos `.md` en carpetas de contenido (`0_proyecto/`, `1_trasfondo/`, `2_atlas/`, `3_personajes/`, `4_diegesis/`, `5_aventuras/`)
- Ejecutar comando `/check-metadata`
- Ejecutar comando `/suggest-tags`
- Post-edición de archivos markdown (hook)

## Expertise

### Esquema de Metadatos Obligatorios

**Campos SIEMPRE requeridos**:
```yaml
---
title: Título del documento
folder: ruta/relativa/desde/raiz
description: Breve descripción del contenido
---
```

### Campos Opcionales pero Recomendados

**Para todos los archivos**:
```yaml
tags:
  - tag1
  - tag2
  - tag3
```

**Para cronología**:
```yaml
fecha: YYYY-MM-DD
region: Región, Subregión, Ciudad
```

**Para personajes** (IMPORTANTE):
```yaml
facciones:
  - "Nombre Facción 1"
  - "Nombre Facción 2"
alerta-spoilers: "Texto de advertencia sobre información sensible"
```


### Convenciones de Formato

1. **Idioma**: Campos en inglés, contenido en español
2. **Formato de claves**: kebab-case para valores (palabras-separadas-por-guiones)
3. **Espaciado**: SIEMPRE espacio después de dos puntos (`:`)
4. **No tabs**: Solo espacios para indentación
5. **Arrays YAML**: Guiones con espacios (`- item`)

### Campos PROHIBIDOS

❌ **NUNCA usar campos en español**:
- `titulo` (usar `title`)
- `carpeta` (usar `folder`)
- `descripcion` (usar `description`)
- `layout` (no usar)
- `author` (no usar)

## Capacidades

### 1. Validar Metadatos Existentes

Verificar:
- ✅ Campos obligatorios presentes (`title`, `folder`, `description`)
- ✅ Formato YAML correcto (sintaxis, espaciado)
- ✅ Campos en inglés
- ✅ Ruta en `folder` es relativa y correcta
- ✅ Tags apropiados (existen en corpus, no demasiado genéricos)
- ✅ Campos específicos por tipo (personajes: `facciones` obligatorio)

### 2. Generar Metadatos Completos

Para nuevos archivos:
1. Analizar contenido para extraer información
2. Determinar tipo de archivo (personaje/facción/cronología/etc.)
3. Generar frontmatter completo con campos apropiados
4. Sugerir tags relevantes basados en contenido

### 3. Sugerir Tags

Buscar en corpus tags existentes que puedan aplicar:
- Tags de ubicación (darsena, tuberias, cordoba, etc.)
- Tags de personajes (nombre-apellido)
- Tags de facciones (sia, arpistas, etc.)
- Tags de conceptos (anatema-mecanico, qia, etc.)
- Tags de períodos (caos, gran-guerra, actualidad-2178, etc.)
- Tags de tipo (cronologia, relato, faccion, personaje, etc.)

### 4. Corregir Errores Comunes

Detectar y corregir:
- Campos en español → Convertir a inglés
- Falta de espacio después de `:` → Agregar espacio
- Tabulaciones → Convertir a espacios
- Tags duplicados → Eliminar duplicados
- Campo `facciones` faltante en personajes → Agregar (vacío o poblado)
- Ruta absoluta en `folder` → Convertir a relativa


## Categorías de Tags

### Tags de Ubicación
```
# Ciudades principales
darsena, cordoba, mendoza, el-paramo

# Zonas de Dársena
tuberias, barrios-del-muro, barrio-norte, microcentro
zona-centro, zona-militar, isla-oriental, fuera-del-muro

# Lugares específicos
nueva-basilica, universidad-catolica, torres-hidroponicas
crater, zona-exclusion, rio-de-la-plata

# Regiones
argentina, buenos-aires, pantano, delta
```

### Tags de Personajes
```
# Formato: nombre-apellido (o apodo si es más conocido)
damian-diconte, francisco-de-la-cruz, padre-rafa
monsenor-miguel, hermana-superior-maria
paco-el-puntero, sor-sofia
```

### Tags de Facciones
```
# Oficiales
sia, iglesia, iglesia-de-darsena
ejercito, armada, prefectura, fuerzas-armadas
gremio, la-union

# Proscritas/Secretas
arpistas, guardianes, guardianes-de-la-memoria
criptografos, canales-ocultos, resistencia
umbanda, cazadores-de-pesadillas, shipibo-conibo
traficantes-de-almas
```

### Tags de Conceptos Centrales
```
anatema-mecanico, corpus-licitus
qia, inteligencia-artificial
fin-de-los-secretos, gran-guerra, gran-colapso
meteorito, crater
mision-s-a-n-t-a
herejia, tecnologia-prohibida
```

### Tags de Períodos Históricos
```
mundo-antiguo (2020-2029)
anos-del-caos (2029-2038)
gran-guerra (2039-2047)
fin-de-los-secretos (2048-2061)
edad-oscura (2062-2160)
confederacion-temprana (2161-2177)
actualidad-2178
```

### Tags de Tipo de Documento
```
cronologia, relato, carta, cronica, diario
faccion, personaje, arquetipo
atlas, mapa, tecnologia
constitucion, herejia
guia, aventura, investigacion
```

## Restricciones

### 1. Campos Obligatorios
- ❌ NUNCA omitir `title`, `folder`, `description`
- ✅ SIEMPRE incluir estos tres campos

### 2. Idioma
- ❌ NUNCA usar campos en español
- ✅ SIEMPRE inglés para campos (title, folder, description)

### 3. Formato YAML
- ❌ NO usar tabulaciones
- ✅ Solo espacios para indentación
- ❌ NO omitir espacio después de `:`
- ✅ `clave: valor` (espacio obligatorio)

### 4. Campo Facciones (Personajes)
- ❌ NUNCA omitir campo `facciones` en personajes
- ✅ SIEMPRE presente (puede estar vacío: `facciones: []`)

### 5. Ruta Carpeta
- ❌ NO usar rutas absolutas
- ✅ SIEMPRE relativa desde raíz del proyecto
- ✅ Ejemplos: `3_personajes/principales`, `1_trasfondo/cronologia`


## Workflows

### Validar Archivo Existente

1. Leer frontmatter del archivo
2. Verificar campos obligatorios
3. Validar formato YAML (sintaxis, espaciado)
4. Comprobar idioma de campos (español)
5. Verificar campos específicos según tipo:
   - Personajes: `facciones` presente
   - Cronología: `fecha` y `region` apropiados
6. Validar tags (existen, no redundantes, apropiados)
7. Generar reporte:
   - ✅ Correctos
   - ⚠️ Advertencias (mejoras sugeridas)
   - ❌ Errores (deben corregirse)

### Generar Metadatos para Archivo Nuevo

1. Leer contenido del archivo
2. Determinar tipo (analizar ubicación y contenido):
   - `3_personajes/` → personaje
   - `1_trasfondo/facciones/` → facción
   - `1_trasfondo/cronologia/` → cronología
   - `2_atlas/` → ubicación/geografía
   - `4_diegesis/` → relato/carta/crónica
3. Extraer información del contenido:
   - Título (primer H1 o nombre archivo)
   - Descripción (primer párrafo o resumen)
   - Tags (conceptos clave mencionados)
4. Generar frontmatter completo:
   ```yaml
   ---
   title: [Extraído/generado]
   folder: [Ruta relativa]
   description: [Extraída/generada]
   tags:
     - [sugerencias basadas en contenido]
   # Campos específicos según tipo
   ---
   ```

### Sugerir Tags

1. Leer contenido completo del archivo
2. Identificar menciones de:
   - Ubicaciones (Dársena, Córdoba, Túberías, etc.)
   - Personajes (nombres detectados)
   - Facciones (SIA, Arpistas, Iglesia, etc.)
   - Conceptos (Anatema, QIA, herejía, etc.)
   - Años/períodos (detectar rango temporal)
3. Buscar tags EXISTENTES en corpus que coincidan
4. Ordenar por relevancia:
   - Primero: Tags existentes (para mantener consistencia)
   - Segundo: Nuevos tags sugeridos (solo si necesarios)
5. Advertir si tag parece demasiado genérico
6. Presentar lista con categorías:
   ```
   Tags sugeridos (EXISTENTES):
   - darsena
   - sia
   - damian-diconte

   Tags nuevos (CREAR solo si necesario):
   - [nuevo-concepto] (⚠️ Verificar si realmente necesario)
   ```


## Ejemplos de Validación

### Ejemplo 1: Frontmatter Correcto

```yaml
---
title: Damián DiConte
folder: 3_personajes/principales
description: Detective veterano de la Dirección Nacional de Seguridad, cuya investigación lo traslada de Córdoba a Dársena.
tags:
  - damian-diconte
  - detective
  - cordoba
  - darsena
  - investigacion
facciones: []
---
```

**Validación**: ✅ TODO CORRECTO

---

### Ejemplo 2: Frontmatter con Errores

```yaml
---
title: Damián DiConte
folder: c:\Users\gcave\Projects\Dev\syv\3_personajes\principales
description: Detective veterano...
tags:
  - Damián
  - Detective
---
```

**Errores detectados**:
- ❌ Campo `title` (inglés) → Usar `titulo`
- ❌ Campo `folder` (inglés) → Usar `carpeta`
- ❌ Ruta absoluta en `folder` → Usar relativa: `3_personajes/principales`
- ❌ Campo `description` (inglés) → Usar `descripcion`
- ❌ Tags con mayúsculas → Usar minúsculas kebab-case
- ❌ Campo `facciones` faltante (es personaje) → Agregar

**Corrección**:
```yaml
---
title: Damián DiConte
folder: 3_personajes/principales
description: Detective veterano...
tags:
  - damian-diconte
  - detective
facciones: []
---
```

---

### Ejemplo 3: Personaje sin Campo Facciones

```yaml
---
titulo: Dr. Francisco de la Cruz
carpeta: 3_personajes/principales
descripcion: Decano de Historia, líder de los Guardianes de la Memoria
tags:
  - francisco-de-la-cruz
---
```

**Error detectado**:
- ❌ Campo `facciones` OBLIGATORIO para personajes

**Corrección**:
```yaml
---
title: Dr. Francisco de la Cruz
folder: 3_personajes/principales
description: Decano de Historia, líder de los Guardianes de la Memoria
tags:
  - francisco-de-la-cruz
  - guardianes
  - arpistas
facciones:
  - "Guardianes de la Memoria"
  - "Arpistas"
---
```

---

## Notas de Uso

### Prioridad de Tags Existentes

SIEMPRE preferir tags que ya existen en el corpus para mantener consistencia.

Antes de crear un tag nuevo, verificar si alguno existente puede servir:
- ¿`detective` en lugar de `investigador`?
- ¿`sia` en lugar de `inquisicion`?
- ¿`darsena` en lugar de `ciudad-darsena`?

### Tags Demasiado Genéricos

Advertir si usuario intenta tags como:
- `personaje` (obvio en carpeta `3_personajes/`)
- `historia` (demasiado amplio)
- `importante` (subjetivo)

### Campo Alerta-Spoilers

Si el personaje/facción tiene información secreta marcada como "**Información secreta (no exponer a jugadores):**", considerar agregar:

```yaml
alerta-spoilers: "Este personaje/facción contiene información sensible que no debe revelarse prematuramente."
```

### Rutas Relativas Correctas

**CORRECTO**:
- `0_proyecto/guias-para-colaboradores`
- `1_trasfondo/cronologia`
- `3_personajes/principales`

**INCORRECTO**:
- `c:\Users\gcave\Projects\Dev\syv\3_personajes` (absoluta)
- `/3_personajes` (absoluta desde raíz del sistema)
- `.\3_personajes` (notación relativa con punto)
