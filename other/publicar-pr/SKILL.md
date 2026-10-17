---
name: publicar-pr
description: Push, PR y merge de una rebanada contra development, con los dos portones del usuario, y cierre de los tickets. Usala cuando una rebanada ya está commiteada y toca publicarla.
when_to_use: Cuando el delivery-specialist terminó el commit y pregunta al usuario si publica, o cuando el usuario ya dijo que sí al push o al merge.
---

# Publicar: push, PR y merge

Hooks que lo hacen cumplir: `bloquear-git-push.sh` y `limitar-gh.sh`. Nunca
`main`, nunca forzado, `--base development` siempre literal.

## Portón 1 — antes del push

Terminá el turno con sha, título y qué quedó hecho, y preguntá si lo publicás.
**Sin un sí explícito del usuario no se pushea.** Un "seguí" de otro ticket no
vale.

Con el sí:

```bash
rtk git push -u origin <rama>
rtk gh pr create --base development --head <rama> \
  --title "tipo(alcance): mensaje breve" --body-file <archivo-fuera-del-repo>
```

Cuerpo, corto y con esta forma (sin `Closes` ni `Fixes`):

```markdown
## Qué trae
## Tickets
- #12 — <título>
## Criterios de aceptación
- Verificado con <comando>: <criterio>
- A verificar por el usuario: <criterio>
```

Comentá cada issue con el número de PR, dejalo **abierto** y mové su tarjeta a
**`En revisión`** (`publicar-issues`, sección «Mover la tarjeta»).

## Portón 2 — antes del merge

Terminá el turno con el número de PR y preguntá si lo mergeás. Con el sí:

```bash
rtk gh pr merge <n> --squash
```

(`--merge` o `--rebase` solo si el usuario lo pidió.)

## Cierre de tickets

Solo con el PR mergeado en `development`; se comprueba, no se supone:

```bash
rtk gh pr view <n> --json state,mergedAt
rtk gh issue close <t> --comment "Mergeado en development por el PR #<n>."
```

Un ticket con algún criterio sin marca («verificado con…» o «a verificar por el
usuario») sigue abierto.

Si el usuario dice que no a un portón: no insistas, dejá el estado como está y
reportalo. El merge a `main` y el despliegue son del usuario.
