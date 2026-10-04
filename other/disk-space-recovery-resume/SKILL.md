---
name: disk-space-recovery-resume
description: >
  Ante disco lleno (ENOSPC, no space left on device), audita espacio en modo
  seguro, propone liberación por GRUPOS (origen, impacto, fechas típicas), pide
  aprobación explícita del usuario, ejecuta lo aprobado y reanuda el trabajo que
  quedó bloqueado. Use when disk is full, write fails for lack of space, or the
  user asks to free space and continue a blocked procedure.
---

# Disk space recovery + resume blocked work

## Objetivo

Cuando el almacenamiento **bloquea** una tarea (escritura, `npm install`, crear archivos, etc.), generar una **revisión propuesta** en **agrupaciones lógicas** (no listados largos archivo por archivo), obtener **aprobación final del usuario** (o plan modificado y aceptado), **ejecutar** solo lo aprobado, **verificar** espacio recuperado y **reanudar** el procedimiento interrumpido.

## Palabra final del usuario (innegociable)

El usuario **siempre** tiene la **última palabra** sobre **cualquier** eliminación, vaciado de carpetas o `docker prune`. Sin frase explícita del tipo *“aprobado grupo A”* / *“sí, ejecutá eso”* sobre un plan concreto, el agente **solo** audita y propone; **no** ejecuta limpieza.

## Activación automática (entorno repo)

- **`npm run dev`** y **`npm run build`** ejecutan antes **`npm run disk:precheck`** (`predev` / `prebuild`). Si hay poco espacio, el script **falla** con un mensaje en stderr que indica usar este flujo en Cursor.
- El usuario pega el error o pide recovery → el agente entra en **Fase 1–2** (auditoría + tabla agrupada) y espera aprobación.

Variables: `BMC_DISK_MIN_FREE_MIB` (default **1024**), `BMC_DISK_PRECHECK_SKIP=1`, `BMC_DISK_PRECHECK_MODE=warn` (solo avisa, no corta `dev`/`build`). Ver `scripts/disk-space-precheck.sh`.

## Seguridad (obligatorio)

Alinear con [drive-space-optimizer](../drive-space-optimizer/SKILL.md):

1. No borrar información de usuario sin confirmación explícita.
2. Evitar `rm -rf` amplios, `sudo rm`, formateos o tocar carpetas de sistema sin validación humana.
3. Priorizar **cachés regenerables** y, cuando el usuario lo apruebe, **mover a `~/.Trash`** antes que borrado permanente.
4. Dudas → marcar **manual** y no ejecutar.

## Disparadores

- Fallo de **`disk:precheck`** al correr `npm run dev` / `npm run build` (mensaje “poco espacio en disco”).
- Mensajes de error: `ENOSPC`, `No space left on device`, `DISK FULL`, fallos de escritura por espacio.
- Usuario: liberar espacio, disco lleno, continuar después de limpiar.
- Sospecha de disco: builds o copias que fallan solo en este entorno.

## Fase 0 — Congelar contexto del bloqueo

Registrar en el chat (bullet corto):

| Campo | Contenido |
|--------|-----------|
| `blocked_operation` | Qué hacía el agente (ej. crear skill, `npm ci`, guardar vídeo). |
| `blocked_command_or_tool` | Comando o herramienta que falló, si aplica. |
| `workspace_path` | Repo o ruta donde se necesita espacio. |
| `resume_step` | Primer paso a reintentar tras verificar espacio (copiar literal). |

## Fase 1 — Auditoría solo lectura

1. Espacio en volumen relevante: `df -h /` y, si el trabajo es en otro volumen, `df -h <mount>`.
2. Desde la raíz del repo (si aplica): `npm run mac:storage-audit` → incorporar cifras al informe.
3. Si hace falta más detalle **solo lectura**, usar `du -sh` sobre candidatos típicos (Caches, Logs, DerivedData, Docker, `node_modules` de otros proyectos, Descargas). No eliminar en esta fase.

Opcional (solo lectura, para enriquecer “fechas” por grupo): muestreo con `find <dir> -type f -mtime +30` / `-mtime -1` para describir **antigüedad típica**, sin listar todo.

## Fase 2 — Propuesta al usuario (resumen agrupado)

Tabla Markdown por **grupo** (no archivo por archivo):

| Grupo | Qué es / cómo se generó | Tamaño aprox. | Antigüedad típica | Impacto si se elimina o vacía | Riesgo (`seguro` / `cuidado` / `manual`) | Acción propuesta |

Incluir:

```markdown
## Acciones propuestas (requieren tu aprobación)
- [ ] Grupo A: …
- [ ] Grupo B: …
```

Hasta **aprobación explícita** del usuario, **no ejecutar** limpieza.

## Fase 3 — Ejecución (solo lo aprobado)

1. Ejecutar únicamente ítems marcados por el usuario.
2. Preferencia: `mv` a `~/.Trash/<nombre-con-fecha>` o vaciado documentado de cachés; `docker system prune` solo si aprobó Docker explícitamente.
3. Evitar grupos `manual` salvo instrucción puntual.
4. `df -h` y comparar con la línea base.

## Fase 4 — Reanudar procedimiento

1. Confirmar espacio libre suficiente para la operación que falló.
2. Repetir **`resume_step`** de la Fase 0.
3. Si vuelve a fallar: repetir desde Fase 1.
4. Cierre breve: espacio recuperado, grupos ejecutados, resultado del reintento.

## Contrato de salida

```markdown
## Disk recovery — cierre
- Espacio antes / después:
- Grupos ejecutados (solo los aprobados):
- Reintento de `resume_step`:
- Pendientes manuales:
```

## Referencias del proyecto

- `npm run mac:storage-audit` → `scripts/mac-storage-audit-readonly.sh`
- `.cursor/skills/mac-performance-optimizer/PLAN-EJECUCION.md`
- `.cursor/rules/disk-space-recovery.mdc`
- `docs/team/orientation/DISK-SPACE-RECOVERY-AGENT.md`
