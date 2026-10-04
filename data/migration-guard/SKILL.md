---
name: migration-guard
description: Revisa una migración de base de datos antes de desplegarla para asegurar que sea segura — reversible, no destructiva y compatible hacia atrás — siguiendo las convenciones de base de datos del proyecto. Úsala siempre que crees, revises o apruebes una migración de esquema o de datos (p. ej. "revisa esta migración", "¿es seguro desplegar esta migración?").
---

Revisa la migración que indique la persona (o la del diff actual) en busca de riesgos.

1. Lee [`docs/conventions/database.md`](../../../docs/conventions/database.md) para
   las reglas de migración del proyecto (nomenclatura, reversibilidad, estrategia de
   índices, tipos de columna permitidos) y
   [`docs/architecture/database.md`](../../../docs/architecture/database.md) para el
   modelo de datos actual que toca.
2. Verifica la **reversibilidad**: existe un `down`/rollback que funcione, o el
   cambio está documentado explícitamente como irreversible con su justificación.
3. Revisa la **pérdida de datos**: eliminar columnas/tablas, reducir tipos o añadir
   una columna `NOT NULL` sin valor por defecto/backfill. Marca cualquier paso
   destructivo.
4. Revisa la **compatibilidad hacia atrás** para despliegues sin downtime: ¿pueden
   convivir el código viejo y el nuevo con el nuevo esquema durante el rollout?
   Prefiere expandir → migrar → contraer en vez de un cambio rompedor de un solo paso.
5. Revisa **bloqueos / tablas grandes**: operaciones que reescriben o bloquean por
   mucho tiempo tablas grandes (p. ej. añadir una columna not-null, ciertos índices).
   Sugiere la variante segura para la base de datos del proyecto.
6. Confirma un **plan de rollback** y que la migración sea **idempotente / segura de
   reintentar** cuando la herramienta lo permita.

Salida: un veredicto breve (segura / no segura), los riesgos concretos encontrados y
los cambios mínimos para hacerla segura. Si la decisión es relevante (p. ej. una
migración irreversible), recomienda registrar un ADR en
[`docs/decisions/`](../../../docs/decisions/README.md).

NO ejecutes la migración. NO relajes las reglas de base de datos del proyecto para que
una migración pase — corrige la migración en su lugar.
