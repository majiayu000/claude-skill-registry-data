---
name: snapshot
description: "Crea y restaura checkpoints del estado de configuración de Jarvis y del proyecto activo. Activar con: /snapshot create, /snapshot list, /snapshot restore <id>, /snap create — o antes de cualquier operación destructiva. Inspirado en el sistema snapshot/rollback de Hermes Agent."
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Snapshot — Checkpoints de Estado

> Inspirado en el sistema `/snapshot` + `/rollback` de Hermes Agent (NousResearch).
> Safety net antes de operaciones riesgosas. Nunca borra snapshots automáticamente.

---

## ¿Cuándo crear un snapshot?

Crear automáticamente (sin que el usuario lo pida) antes de:
- Modificar `~/.claude/CLAUDE.md` o `~/.claude/settings.json`
- Ejecutar curator o fusiones de skills
- Migraciones de base de datos o cambios de schema
- Force-push o rebase en branches compartidos
- Cualquier operación marcada como destructiva

---

## Comandos

### `/snapshot create [nombre]` o `/snap`

```
1. Generar ID: YYYY-MM-DD-HH-MM-SS (timestamp UTC)
2. Crear directorio: ~/.claude/snapshots/<id>/
3. Capturar archivos de configuración:
   - ~/.claude/CLAUDE.md
   - ~/.claude/settings.json
   - ~/.claude/goals.md (si existe)
   - ~/.claude/cerebro/index.md
   - ~/.claude/cerebro/log.md
4. Capturar estado git del proyecto activo:
   - git log --oneline -10 > git-log.txt
   - git diff HEAD > git-diff.txt
   - git status > git-status.txt
5. Crear metadata.json
6. Confirmar: "📸 Snapshot creado: <id>"
```

**Estructura del snapshot:**
```
~/.claude/snapshots/YYYY-MM-DD-HH-MM-SS/
├── metadata.json
├── CLAUDE.md
├── settings.json
├── goals.md
├── cerebro-index.md
├── cerebro-log.md
├── git-log.txt
├── git-diff.txt
└── git-status.txt
```

### `/snapshot list`

```
1. Glob ~/.claude/snapshots/*/metadata.json
2. Mostrar tabla: ID | Fecha | Proyecto | Razón
3. Ordenar por más reciente primero
```

### `/snapshot restore <id>`

```
⚠️ Confirmar con el usuario antes de ejecutar

1. Verificar que el snapshot existe
2. Mostrar qué se va a restaurar
3. Esperar confirmación explícita
4. Al confirmar:
   a. Crear snapshot del estado ACTUAL primero (pre-restore backup)
   b. Copiar archivos de config al destino
   c. Informar: "✅ Restaurado desde <id>"
```

### `/snapshot prune [--keep N]`

```
1. Por defecto mantener los últimos 30 snapshots
2. Eliminar los más antiguos que excedan el límite
3. NUNCA eliminar snapshots con "pinned": true en metadata.json
```

---

## metadata.json — Estructura

```json
{
  "id": "YYYY-MM-DD-HH-MM-SS",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "nombre-del-proyecto",
  "project_path": "/ruta/absoluta/proyecto",
  "reason": "descripcion de por que se creo",
  "pinned": false,
  "files_captured": ["CLAUDE.md", "settings.json", "goals.md"]
}
```

---

## `/rollback [N]` — Git rollback

```
/rollback         → muestra últimos 10 commits con opción de restaurar
/rollback 3       → muestra qué se pierde al hacer git reset --soft HEAD~3
/rollback apply N → ejecuta git reset --soft HEAD~N (confirmar antes)
```

**Regla:** `/rollback apply` siempre crea un snapshot antes de ejecutar.

---

## Límites de seguridad

- Snapshots nunca se borran automáticamente
- `restore` siempre hace pre-restore backup antes de restaurar
- No incluir tokens ni API keys en snapshots (sanitizar automáticamente)
- Máximo 50 snapshots antes de requerir `/snapshot prune`
