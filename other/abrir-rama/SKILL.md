---
name: abrir-rama
description: Abre la rama de una rebanada con el nombre correcto. Usala al empezar una rebanada, antes de que cualquier especialista toque el árbol.
when_to_use: Cuando el delivery-specialist va a crear una rama, o cuando alguien pregunta cómo se llama la rama de un ticket.
---

# Abrir la rama

Una rama **por rebanada**, no por ticket. El nombre lo gobierna
`convenciones-git` (tipo, número del ticket que abre la rebanada, descripción
en inglés): citala, no la copies.

```
<tipo>/<n>-<descripcion-en-kebab-case>
```

## Pasos

1. `rtk git status` y `rtk git branch --show-current`: el árbol tiene que estar
   limpio y tenés que saber de dónde salís.
2. Salí siempre de `development` actualizada, nunca de una rama de trabajo
   ajena ni de `main`:
   ```bash
   rtk git switch development && rtk git pull --ff-only
   rtk git switch -c <tipo>/<n>-<descripcion>
   ```
3. Si el árbol no está limpio, no ramifiques: reportá qué hay y de quién es.
   Excepción: si el trabajo sin commitear es el de esta rebanada (lo dejó la
   sesión principal), `git switch -c` lo lleva a la rama nueva; no hagas stash.

4. Mové las tarjetas de los tickets de la rebanada a **`En curso`**
   (`publicar-issues`, sección «Mover la tarjeta»).

Después del `git switch -c`, la rama queda local. El push es otro momento
(`publicar-pr`) y tiene portón del usuario.
