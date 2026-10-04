---
name: commit
description: Escribe un mensaje de Conventional Commits para los cambios en stage y crea el commit, incluyendo la línea de coautoría de atribución de IA. Úsalo cuando la persona pida hacer commit, escribir un mensaje de commit o guardar cambios (p. ej. "haz commit de esto", "escribe un mensaje de commit para estos cambios"). No hace push.
---

Crea un commit bien formado para los cambios actuales.

1. Lee `CONTRIBUTING.md` para conocer las reglas de commit del proyecto (tipos permitidos, convenciones de scope, estilo del asunto, footers requeridos). Sigue ese documento por encima de los valores por defecto de abajo.
2. Inspecciona lo que está en stage con `git status` y `git diff --staged`. Si no hay nada en stage, revisa `git diff` y agrega al stage los archivos correspondientes; pregunta antes de hacer stage si es ambiguo.
3. **Formatea antes de commitear** — el CI lo exige: si hay archivos `.md` en el
   cambio, corre `bash .github/scripts/format.sh` (Prettier) y re-agrega al
   stage lo que cambie; si el proyecto ya tiene su propio `[COMANDO_LINT]`/formatter,
   córrelo también sobre los archivos tocados.
4. Redacta un mensaje de Conventional Commits:
   - Formato: `<type>(<optional scope>): <short imperative subject>`
   - Tipos comunes: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.
   - Mantén el asunto por debajo de ~72 caracteres; añade un cuerpo que explique el porqué cuando el cambio no sea trivial.
   - Usa `!` o un footer `BREAKING CHANGE:` para cambios que rompen compatibilidad.
5. Para trabajo asistido por IA, añade la línea de atribución/coautoría en el footer según lo definido en `CONTRIBUTING.md` (un trailer `Co-Authored-By:`).
6. Crea el commit. Muestra el mensaje final a la persona.

Ejemplo de asunto: `feat(auth): add password reset via email`.

NO hagas push, NO modifiques (amend) ni reescribas el historial existente, y NO incluyas cambios no relacionados — mantén cada commit enfocado.
