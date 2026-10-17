---
name: publicar-issues
description: Crea, comenta y edita issues del tracker con gh de forma barata — título, cuerpo, etiquetas y dependencias como texto. Usala al publicar un corte aprobado o al comentar un issue.
when_to_use: Cuando el delivery-specialist publica tickets aprobados, comenta un issue o lista los desbloqueados.
---

# Publicar issues

Fuente de las reglas: `docs/agents/issue-tracker.md`. Los tipos del título son
los de `convenciones-git`. El vocabulario es el de `CONTEXT.md` (rebanada,
cimiento, ticket).

## Antes de publicar

- **El corte tiene que estar aprobado por el usuario.** Sin aprobación explícita
  no se publica nada.
- Etiquetas: todo ticket lleva `tipo:`, `area:` y `prioridad:` (esquema en
  `docs/agents/issue-tracker.md`); `tamano:`, `espera:` y `bloqueada` cuando
  corresponda. Verificá con `rtk gh label list --limit 100`: sin el límite, `gh` muestra solo
  30 y parece que faltan etiquetas que sí existen. Una inexistente hace fallar el `create`, y
  crear etiquetas está denegado. No uses `ready-for-agent`.
- Publicá en **orden de dependencia**: los bloqueantes primero, para que el
  número de `Bloqueada por:` ya exista.

## Crear

```bash
rtk gh issue create --title "tipo(alcance): mensaje breve" \
  --label <existente> --body-file <archivo-fuera-del-repo>
```

Cuerpo, en español:

```markdown
Bloqueada por: #12            (solo si hay; arriba de todo)

## Qué tiene que quedar andando
## Criterios de aceptación
## Qué tiene que quedar en pie
## Cómo se verifica
```

Dice en el cuerpo, no en el título, si es cimiento o rebanada.

## Leer y listar con poco texto

```bash
rtk gh issue view <n> --comments
rtk gh issue list --state open --json number,title
```

Pedí `body` y `comments` solo del issue que vas a trabajar.

## Mover la tarjeta en el tablero

El tablero es el proyecto 2 de `luciano-stefano-meloclaps`. Columnas: `Backlog`,
`Listo`, `En curso`, `En revisión`, `Hecho`. Solo se mueven tarjetas
(`item-edit`); el proyecto y sus campos no se tocan.

```bash
O=luciano-stefano-meloclaps; P=PVT_kwHOBS9uN84BgJQ7
ITEM=$(rtk gh project item-list 2 --owner $O --limit 100 --format json \
  --jq '.items[]|select(.content.number==<n>)|.id')
CAMPO=$(rtk gh project field-list 2 --owner $O --format json \
  --jq '.fields[]|select(.name=="Status")|.id')
OPC=$(rtk gh project field-list 2 --owner $O --format json \
  --jq '.fields[]|select(.name=="Status")|.options[]|select(.name=="<columna>")|.id')
rtk gh project item-edit --id $ITEM --project-id $P --field-id $CAMPO --single-select-option-id $OPC
```

Si falla por permisos, el `GH_TOKEN` no tiene `project`: reportalo y seguí, el
tablero no bloquea el trabajo.

## Cargar los campos de la tarjeta

Al publicar un ticket, además de las etiquetas, cargá en su tarjeta los campos
`Tipo`, `Área`, `Prioridad` y, si corresponde, `Tamaño` y `Espera`, y asigná el
hito con `--milestone`. Son los que se ven en
la vista **Kanban**. Es el mismo comando de arriba cambiando el nombre del
campo (`Status` por `Tipo`, `Área`, `Prioridad` o `Tamaño`) y el valor de la
opción. Los valores son los de las etiquetas: `Prioridad` va con inicial
mayúscula (`Crítica`, `Alta`, `Media`, `Baja`) y `Tamaño` en `S`, `M` o `L`.
Un campo vacío no aparece en la tarjeta.

`Hecho` no se mueve a mano: al cerrar el issue lo pone el tablero.

## Lo que la guarda no deja pasar

`limitar-gh.sh` deniega un `gh` que aparece dentro de otro comando. Para evitarlo:
un comando `gh` por llamada, sin `cd … && gh`, y sin escribir `gh` ni
`gh project` como texto dentro del cuerpo de un heredoc. Escribí el cuerpo en
un archivo fuera del repo y pasalo con `--body-file`.

## Reglas duras

- No cerrar ni editar un issue que no creaste, salvo pedido explícito.
- Cerrar es de `publicar-pr`: solo con el PR mergeado en `development`.
- Dependencias siempre como texto, nunca con `gh api`.
