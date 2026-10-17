---
name: commitear-con-ticket
description: Procedimiento corto para commitear el trabajo de un ticket — verificar el árbol contra el ticket, dejarlo verde, agregar por camino explícito y comentar el issue. Usala siempre que vayas a commitear trabajo con ticket.
when_to_use: Cuando un especialista terminó un ticket y el delivery-specialist va a verificar y commitear.
---

# Commitear con ticket

El **formato del mensaje** (tipos, alcance, Cambios/Razones, `Ticket: #n`) es de
`convenciones-git`. Esta skill es solo el orden de los pasos.

1. `rtk gh issue view <n> --comments`: el ticket es la intención del commit.
2. `rtk git status` y `rtk git diff` completos.
3. Cada archivo cambiado se explica por el ticket. Lo que no, no entra:
   se reporta con su dueño.
4. Árbol verde, siempre, aunque el especialista diga que ya corrió:
   ```bash
   rtk pnpm typecheck && rtk pnpm lint && rtk pnpm test
   ```
   Más `rtk pnpm build` si el ticket toca el build. Si algo falla, no se
   commitea: se devuelve al especialista con la salida.
5. Nada de secretos, `.env`, correos, rutas absolutas ni artefactos de build.
6. `rtk git add <archivo> <archivo>`. **Nunca** `git add -A` ni `git add .`.
7. `rtk git commit` con el mensaje de `convenciones-git`. Cierra con
   `Ticket: #n`, **nunca** `Closes` ni `Fixes`.
8. Comentá el issue con sha y título, y dejalo **abierto**:
   ```bash
   rtk gh issue comment <n> --body "Commit <sha>: <título>"
   ```

Una intención por commit. Si el árbol tiene dos, son dos commits.
