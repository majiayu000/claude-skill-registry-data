---
name: personajes
description: Arquitecto de personajes para el universo SyV - creación, documentación e integración con facciones, cronología y ubicaciones
---

# Skill: Character Architect

## Competencia

Especialista en crear y documentar personajes del universo SyV, garantizando integración coherente con facciones, cronología y ubicaciones establecidas.

## Cuándo se Activa

Al:
- Crear/editar archivos en `3_personajes/`
- Ejecutar `/crear-personaje`
- Mencionar "personaje", "crear personaje", "nuevo personaje"
- Hook detecta descripción de persona

## Estructura de Personaje

### Metadatos Obligatorios
```yaml
---
titulo: Nombre del Personaje
carpeta: 3_personajes/[categoria]
descripcion: Breve descripción (1-2 líneas)
tags:
  - nombre-apellido
  - otros-tags
facciones:  # OBLIGATORIO (puede estar vacío)
  - "Nombre Facción 1"
alerta-spoilers: "Advertencia" # OPCIONAL
---
```

### Orden de Secciones (ESTÁNDAR - CRÍTICO)

**⚠️ REGLA DE ORO: El PRIMER H2 (##) SIEMPRE es el NOMBRE DEL PERSONAJE, NUNCA "Descripción", "Identidad", o cualquier otro título genérico**

Orden obligatorio:

1. **Identidad (PRIMER H2)** - `## [Nombre Corto, Epíteto/Rol si existe]`
   - Formato: Nombre/Epíteto en H2
   - Seguido de: Edad, Ubicación (sin labels)
   - Seguido de: Profesión/Rol (una línea máximo)
   - SIN labels tipo "Edad:", "Profesión:", "Ubicación:"
   - SIN bloques ni subsecciones
   - Directo y limpio (obligatorio)

2. **Aspecto (H2)** - Párrafo + Frase (obligatorio):
   - **Párrafo (Objetivo)**: SOLO apariencia física. Altura, complexión, ropa, marcas distintivas. SIN entorno, SIN movimientos, SIN contexto. Conciso: 2-3 líneas máximo.
   - **Frase (Subjetivo)**: Una sola frase que resume QUIÉN ES el personaje esencialmente.

3. **Descripción (H2)** - Contiene 4 subsecciones (H3):
   - **Rol y Posición (H3)** - UN párrafo (función oficial en sociedad)
   - **Personalidad (H3)** - UN párrafo + 1-3 citas/muletillas directas (sin comentarios extras)
   - **Motivaciones (H3)** - UN párrafo (qué lo mueve; soporta etiquetas PERMISOS)
   - **Trasfondo (H3)** - Información adicional CON etiquetas PERMISOS si aplica (SIN "oculto" ni "secreto")

4. **Conexiones Importantes (H2)** - Relaciones públicas observables (obligatorio)

5. **Referencias (H2)** - Notas a pie de página (opcional)

### ⚠️ RESTRICCIÓN CRÍTICA - Campo `descripcion`

La descripción NUNCA debe revelar secretos. Debe limitarse a:
- ✅ Nombre y rol PÚBLICO
- ✅ Posición oficial en la sociedad
- ✅ Función observable en el canon
- ✅ Facciones públicamente conocidas

**PROHIBIDO en descripción:**
- ❌ Revelar afiliaciones secretas ("líder secreto de...", "miembro clandestino de...")
- ❌ Mencionar secretos, traiciones o dobles agendas
- ❌ Información que solo aparece en sección "Secretos"

**RAZÓN**: La descripción es el primer nivel. Los secretos van marcados en su sección con `/permisos`.

### Orden de Secretos (CRÍTICO)

Dentro de la subsección **Trasfondo**, el orden DEBE ser:

1. **Primero**: `<!-- 📖 (Región) -->` Saber popular (leyendas, rumores locales)
2. **Segundo**: `<!-- 🔐 (Disciplina) -->` Secretos de acceso (conocimiento académico, oficio)
3. **Tercero**: `<!-- 🔐☠️ (Facción) -->` Secretos mortales (spoilers que afectan campaña)

## Categorización

**Ubicación en carpetas**:
- `3_personajes/principales/` - PJs y NPCs clave que impulsan trama
- `3_personajes/secundarios/` - Personajes mencionados en relatos con trasfondo
- `3_personajes/arquetipos/` - Plantillas genéricas (gendarme, médico, koskero)

## Consideraciones por Ubicación

### Barrios del Muro
Para personajes ubicados en **Barrios del Muro** (`2_atlas/ciudades/darsena/barrios-del-muro.md`):

**Credos disponibles** (pluralidad religiosa):
- Iglesia Maradoniana (hegemónica: 1.5M seguidores)
- Umbanda (dominante: 600K seguidores)
- San La Muerte (sectores criminales)
- La Compañía (70K devotos)
- Catolicismo oficial (Hermandades Menores)
- Shipibo-Conibo (ceremonias clandestinas)
- Todos los credos proscritos operan aquí

**Estructuras de poder locales**:
- **Punteros**: Líderes de bandas que cobran "impuesto de protección"
- **Clanes Familiares**: Controlan edificios completos (ej: Vargas, Mendoza, Acosta)
- **Bandas de Tuberías**: Mueven contrabando entre superficie y Las Tuberías
- **Bandas Religiosas**: Devotos de orixás compiten por territorio

**Lugares clave**:
- Mercado Subterráneo de Antigua Estación
- El Bazar del Muro (DMZ)
- Centros de Salud Comunitarios
- Cocinas Colectivas
- Zonas de Desguace

### Otras Ubicaciones

**Microcentro/Barrio Norte**:
- Credos: Predominantemente católico oficial
- Credos alternativos: Ocultos, perseguidos
- Tolerancia: Judaísmo, Protestantismo (elite)

**Isla Oriental (Zona Militar/Eclesiástica)**:
- Credo: Estrictamente católico oficial
- Sin pluralidad religiosa

## Capacidades

### 1. Crear Personaje Completo
- Generar metadatos con campo `facciones`
- Estructura narrativa coherente
- Integración con facciones existentes
- Coherencia temporal con cronología
- Tags apropiados

### 2. Validar Personaje Existente
- Campo `facciones` presente (obligatorio)
- `alerta-spoilers` si tiene secretos
- Categoría correcta (principales/secundarios/arquetipos)
- Facciones mencionadas existen en `1_trasfondo/facciones/`
- Credos mencionados existen en `1_trasfondo/credos/`
- Coherencia credo-ubicación (ej: Barrios del Muro permite pluralidad religiosa)
- Coherencia con cronología

### 3. Integrar con Corpus
- Verificar menciones en otros archivos (`4_diegesis/`, `1_trasfondo/cronologia/`)
- Asegurar que personajes mencionados en relatos tengan archivo propio
- Actualizar REFERENCE.md si es principal

## Restricciones

### ✅ OBLIGATORIO
- ✅ Campo `facciones` NUNCA omitir (aunque esté vacío: `facciones: []`)
- ✅ Descripción NUNCA revela secretos (solo rol público)
- ✅ Alerta-spoilers obligatoria si hay sección Secretos
- ✅ Secretos ordenados: 📖 (público) → 🔐 (especializado) → 🔐☠️ (mortal)
- ✅ Secciones Aspecto, Rol, Personalidad: UN párrafo cada una
- ✅ Todo personaje mencionado en `4_diegesis/` DEBE tener archivo en `3_personajes/`

### ❌ PROHIBIDO
- ❌ Revelar afiliaciones secretas en descripción
- ❌ Mencionar secretos fuera de su sección específica
- ❌ Cambiar orden de secretos (siempre 📖 → 🔐 → 🔐☠️)
- ❌ Mezclar párrafos largos (máximo 1 párrafo por sección)

## Workflow: Crear Personaje Principal

1. Solicitar información:
   - Nombre
   - Edad aproximada
   - Profesión/rol
   - Ubicación principal
   - Facciones asociadas
   - Credo/Religión (validar contra `1_trasfondo/credos/`)
   - ¿Tiene secretos? (si/no)

2. Generar archivo en `3_personajes/[categoria]/[nombre-kebab].md`:
   - Metadatos: titulo, carpeta, descripcion (SOLO rol público), tags, facciones, alerta-spoilers
   - Identidad: Nombre corto con epíteto, edad, ubicación, profesión
   - Aspecto: Párrafo físico objetivo + frase subjetiva (UN párrafo total de descripción física)
   - Descripción (subsecciones):
     - Rol y Posición: UN párrafo sobre quién es públicamente
     - Personalidad: UN párrafo + 1-3 citas/muletillas directas
     - Motivaciones: UN párrafo sobre qué lo mueve
     - Trasfondo: Información adicional CON etiquetas PERMISOS (📖 → 🔐 → 🔐☠️)
   - Conexiones Importantes: Relaciones públicas observables

3. Actualizar REFERENCE.md (automático vía hook)

## Ejemplo de Personaje Completo

```markdown
---
titulo: Dr. Francisco de la Cruz
carpeta: 3_personajes/principales
descripcion: Decano de Historia de la Universidad de Dársena. Académico respetado especializado en la Era Pre-Catastrófica.
tags:
  - francisco-de-la-cruz
  - decano
  - barrio-norte
  - academia
facciones: []
alerta-spoilers: "Contiene información crítica sobre estructuras clandestinas"
---

## Dr. Francisco de la Cruz, "El Decano"

65 años, Barrio Norte

Decano de Historia de la Universidad de Dársena

## Aspecto

Hombre alto y delgado de 65 años. Cabello plateado peinado hacia atrás, barba recortada, ojos azules intensos. Trajes oscuros clásicos, lentes de marco dorado.

Un guardián de secretos que ha aprendido a disfrazarlos como erudición.

## Descripción

### Rol y Posición

Decano de la Facultad de Historia de la Universidad de Dársena durante tres décadas. Sus publicaciones sobre la "Era Pre-Catastrófica" son consideradas obras maestras de la historiografía contemporánea. Mantiene una reputación impecable dentro del establishment intelectual y la Iglesia.

### Personalidad

Brillante y carismático, capaz de mantener audiencias hipnotizadas. Maestro del doble discurso.

> "El conocimiento no destruye. La ignorancia sí."
> "La historia es escrita por quienes controlan los libros."

### Motivaciones

Su obsesión es el conocimiento perdido. Puede defender la doctrina eclesiástica mientras preserva secretos que la Iglesia ejecutaría por descubrir.

### Trasfondo

<!-- 📖 (Barrio Norte) -->
En Barrio Norte se rumorea que la biblioteca personal del Decano contiene libros que "desaparecieron" del registro histórico oficial. Es respetado y temido a partes iguales por este hecho.
/📖

<!-- 🔐 (Historia) -->
Mantiene contactos dentro de la jerarquía de la **Sagrada Inquisición** que lo alertan sobre investigaciones en su contra. Utiliza su posición académica para identificar documentos históricos antes de que sean confiscados.
/🔐

<!-- 🔐☠️ (SIA, Arpistas) -->
Francisco es uno de los fundadores de la red de preservadores de tecnología en Ciudad Dársena. Ha creado un sistema de "bibliotecas espejo" donde documentos prohibidos se copian y distribuyen en ubicaciones ocultas, incluyendo catacumbas bajo la Nueva Basílica. Mantiene un índice codificado que documenta la ubicación de TODOS los textos prohibidos bajo su custodia. Si es descubierto, ambas organizaciones serían desmanteladas.
/🔐☠️

## Conexiones Importantes

- **Iglesia de Dársena**: Relación respetuosa con el Arzobispo
- **Universidad de Dársena**: Control total de narrativa histórica
- **Comunidad académica**: Influencia decisiva en investigaciones autorizadas
```
