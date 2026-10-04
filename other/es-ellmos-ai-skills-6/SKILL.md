---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Renombrado evolutivo de archivos con archivos wrapper. Permite renombrar sin rupturas drásticas — las referencias se actualizan orgánicamente mediante el uso.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="migrate-rename banner">

> **Español** — Versión oficial en español de `migrate-rename`.


# Renombrado de archivos con wrappers (Migración evolutiva) (Español)

> Permite renombrar archivos SIN rupturas drásticas. Las referencias se actualizan orgánicamente a través del uso diario.

---

## Principio: Migración evolutiva

```
BEFORE:                          AFTER:
old_file.md                      new_file.md (renamed)
   |                                |
   +-- Reference A                  +-- old_file.md (wrapper)
   +-- Reference B                         |
   +-- Reference C                         +-- Log table
                                           +-- Instructions
                                           +-- Link to new_file.md
```

Cuando alguien accede a la ruta antigua:
1. Llega al archivo wrapper
2. Añade una entrada al registro (log)
3. Corrige la referencia que le llevó allí
4. Continúa hacia el archivo real

---

## Paso a paso

### 1. Renombrar el archivo

```bash
mv old_file.md new_file.md
```

### 2. Crear el archivo wrapper

Cree `old_file.md` con el siguiente contenido:

```markdown
# OLD_FILE.md - REDIRECTED (Deutsch)

**Status:** This file has been renamed to `new_file.md`

---

## Migration Log

| Date | Who | Origin | Reference corrected? |
|------|-----|--------|---------------------|
| YYYY-MM-DD | [Name] | Initial migration | n/a (wrapper created) |

---

## Instructions

1. **Leave a log entry** (in table above)
2. **Check origin**: What sent you here?
3. **Correct reference**: Change `old_file.md` -> `new_file.md`
4. **Go to the actual file**: `new_file.md`

---

**Target file:** `new_file.md`
```

### 3. Corregir inmediatamente las referencias críticas
- Archivos de ayuda (documentación principal)
- Referencias en el prompt del sistema
- Código CLI que utiliza directamente la ruta

### 4. Migrar las referencias restantes de forma evolutiva
El resto se corrige automáticamente a través del uso.

---

## ¿Cuándo usar el método Wrapper?

**SÍ - El wrapper es útil:**
- Muchas referencias potenciales
- El archivo es referenciado por varios socios/herramientas
- No es un archivo crítico del sistema

**NO - Cambiar todo directamente:**
- Pocas referencias y conocidas
- Archivos críticos del sistema (configuración, esquema de BD)
- Rutas de rendimiento crítico

---

## Limpieza

Transcurridos aproximadamente 30 días o cuando el registro no muestre nuevas entradas:
1. Mover el archivo wrapper a `_archive/deprecated/`
2. O eliminar por completo (si no hay más entradas)

---

## Registro de cambios

### 1.0.0 (2026-03-15)
- Adaptado desde BACH v3.8.0

---

*Adaptado desde BACH v3.8.0 | Versión independiente*
