---
name: new-spec
description: Genera una nueva especificación de cambio ligera copiando el directorio de plantilla de especificación en una carpeta de especificación con nombre. Úsalo cuando la persona quiera iniciar una especificación, planificar un cambio/funcionalidad o crear un documento de diseño antes de implementar (p. ej. "especifica el rediseño del checkout", "crea una especificación para el nuevo flujo de autenticación").
argument-hint: "[nombre del cambio]"
---

Crea una nueva especificación de cambio cuyo nombre está en `$ARGUMENTS`.

1. Lee `specs/README.md` para conocer el flujo de trabajo de las especificaciones, la convención de nombres de carpeta y qué espera cada sección de la plantilla. Sigue ese documento si difiere de los pasos siguientes.
2. Convierte `$ARGUMENTS` en `<change-name>` con formato slug (minúsculas, separado por guiones).
3. Calcula `NNNN`: el mayor prefijo numérico de 4 dígitos existente en `specs/` **y**
   `specs/archive/` (si existe), más uno; si no hay ninguna, `0001`.
4. Copia todo el directorio `specs/_template/` a `specs/NNNN-<change-name>/` (conserva cada archivo de la plantilla).
5. En los archivos copiados, completa los metadatos obvios:
   - El título del cambio (la forma legible de `$ARGUMENTS`)
   - Estado: `Borrador`
   - Fecha: la fecha de hoy (`YYYY-MM-DD`)
   - Deja problem, goals, non-goals y approach como indicaciones para la persona autora.
6. **Rellena «Evidencia»** antes que el objetivo: quién pagaría y qué lo respalda, si ya
   existe, y qué experimento se hizo. Mira primero
   [`docs/product/roadmap.md`](../../../docs/product/roadmap.md) — puede que la
   respuesta ya esté. En una `fix/*` o de tooling, escribe «No aplica: corrección»: la
   sección existe para decidir qué construir, no para dar teatro a lo que ya está roto.
7. **Ata la spec al roadmap.** Lee `docs/product/roadmap.md` y rellena el campo
   _Ítem de roadmap_ de `proposal.md` con la versión y el ítem literal que esta spec
   completa. Si hay varios candidatos, pregunta con AskUserQuestion en vez de elegir
   por tu cuenta. Si no existe ningún ítem que encaje, dilo: o se añade al roadmap
   ahora, o el cambio debería contrastarse antes contra el roadmap (¿entra en esta versión?,
   ¿qué sale a cambio?). Anota también la spec junto al ítem en el roadmap
   (`(specs/NNNN-<slug>/)`).
8. Si `specs/README.md` mantiene un índice de especificaciones, añade una entrada para la nueva especificación.
9. Informa la ruta del directorio creado y enumera los archivos que la persona autora aún debe completar.

Ejemplo: `/new-spec rediseño del checkout` → `specs/0007-checkout-redesign/` (si la
última especificación era la `0006`).

**Rama ↔ spec:** la rama que implemente esta spec debe llamarse `feat/<change-name>`
(o `fix/<change-name>`) — mismo slug. El hook `spec-guardrails.sh` bloquea editar
código en ramas `feat/*`/`fix/*` cuya spec no exista, así que crea la spec ANTES de
crear la rama de implementación (o desde la rama, antes de tocar código). El hook
también bloquea mientras `proposal.md`, `design.md` o `tasks.md` conserven líneas de
la plantilla sin rellenar: deja los archivos completos (o borra las secciones que no
apliquen) antes de implementar.

NO empieces a implementar el cambio, y NO elimines ni sobrescribas una carpeta de
especificación existente — si ya existe alguna `specs/*-<change-name>/` (con
cualquier prefijo `NNNN-`; el nombre sin prefijo no va a existir nunca), detente y
pregunta.
