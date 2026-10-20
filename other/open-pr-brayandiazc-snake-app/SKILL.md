---
name: open-pr
description: Redacta un pull request para la rama actual rellenando la plantilla de PR del repositorio en función de los cambios de la rama. Úsalo cuando la persona pida abrir/crear un PR, preparar un pull request o escribir la descripción de un PR (p. ej. "abre un PR", "redacta el pull request de esta rama"). No hace merge.
---

Prepara un pull request para la rama actual.

0. **Antes de redactar nada, deja el cambio listo.** Es el único momento en que alguien
   mira el conjunto completo, y lo que no se actualice aquí no se actualiza nunca:
   - Corre el subagente **`doc-keeper`** sobre el diff: sincroniza `docs/architecture/*`,
     **los diagramas** (entidades, pantallas, auth, componentes), el ADR si hubo decisión,
     la entrada del `CHANGELOG.md` y el ítem del roadmap que la spec declaró.
   - Corre **`bash .githooks/pre-push`**: los siete checks del CI, en unos quince
     segundos y sin gastar minutos de Actions.
   - Repasa [`docs/conventions/definition-of-done.md`](../../../docs/conventions/definition-of-done.md),
     y en especial lo que **ninguna máquina comprueba**: revisión humana del esquema,
     autorización probada con otro rol, los cuatro estados de la UI.

   **Si algo queda en rojo, no abras el PR**: dilo y arréglalo primero. Un PR que nace
   rojo se normaliza y deja de mirarse.

1. Lee `.github/PULL_REQUEST_TEMPLATE.md` para conocer las secciones requeridas y la lista de verificación.
2. Reúne contexto sobre los cambios de la rama:
   - `git log <base>..HEAD --oneline` para la lista de commits (la base suele ser `main`).
   - `git diff <base>...HEAD --stat` y revisa los diffs relevantes.
3. Rellena cada sección de la plantilla usando ese contexto:
   - Resumen de qué cambió y por qué.
   - Issues vinculados / ADRs o especificaciones relacionados si se mencionan.
   - Notas de pruebas (qué ejecutaste o qué debería revisar quien haga la revisión).
   - Marca los ítems de la lista de verificación que realmente apliquen; deja el resto para la persona autora.
4. Crea el PR con la CLI `gh` (p. ej. `gh pr create --title ... --body ...`) si la rama está pusheada; de lo contrario, muestra la plantilla rellenada para que la persona la pegue.
5. Informa la URL del PR o el cuerpo redactado.

NO hagas merge, NO apruebes, y NO marques ítems de la lista de verificación que no estén realmente hechos. Escribe un PR en borrador si el trabajo está incompleto.
