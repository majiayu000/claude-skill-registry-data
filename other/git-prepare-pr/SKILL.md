---
name: git-prepare-pr
description: Redactar la descripción de un PR (resumen, tipo, hito, DoD, pruebas) para pegar o revisar; no hace push ni gh pr create. Para commits usa git-commit.
allowed-tools: Read, Grep, Bash(git status*), Bash(git log*), Bash(git diff*), Bash(git branch*)
---

# git-prepare-pr

Genera el texto de un PR. No publica nada. El flujo habitual del proyecto es commit directo a `main` con el gate en verde y push solo con permiso del usuario; esta skill sirve cuando se quiere una rama con PR.

## Cuándo usarla
- La rama está lista y hace falta la descripción del PR (para pegar o revisar).

## Cuándo NO usarla
- Crear el commit → usa `git-commit`.
- Revisar la calidad del código → usa `architecture-review` o `security-review`.
- Ejecutar `git push` o `gh pr create`: solo con petición explícita del usuario y fuera de esta skill.

## Precondiciones
- Rama con commits propios respecto a `main`; árbol limpio (si no, avisar y sugerir `git-check`).
- Hito activo conocido: `docs/ESTADO.md` y `ROADMAP.md`.
- Si existe `.github/pull_request_template.md`, leerlo y seguirlo; si no, usar la estructura del paso 3.

## Pasos
1. Recopilar el cambio: `git log main..HEAD --oneline` y `git diff main...HEAD --stat`; leer el diff de los archivos clave.
2. Resumen: 1-3 frases con qué cambia y por qué.
3. Estructura mínima: Resumen · Tipo (feat, fix, refactor, perf, test, docs, build, ci, chore) · Hito · Checklist DoD · Cómo se probó.
4. Hito: indicar el activo y confirmar que el cambio no sale de él.
5. Checklist DoD: marcar `[x]` solo lo comprobado en esta sesión (gate Android, `:motor:test`, sin secretos, ESTADO.md, DECISIONES.md, sin tests desactivados). Lo no verificado queda `[ ]` con nota.
6. Cómo se probó: comandos reales ejecutados y su resultado; pruebas manuales en dispositivo; capturas si hay UI. Nada inventado.
7. Entregar el texto en el chat. Preguntar si el usuario quiere push o `gh pr create`; sin respuesta afirmativa explícita, no ejecutarlos.

## Validaciones / tests
- El texto conserva todas las secciones (y casillas, si hay plantilla).
- Cada casilla marcada tiene evidencia (comando o revisión) en "Cómo se probó".
- Gate ejecutado, o dicho expresamente que no se ha ejecutado.

## Definition of Done
- [ ] Descripción completa con resumen, tipo, hito, checklist y pruebas.
- [ ] Checklist honesto, sin secretos en el texto.
- [ ] No se ejecutó `git push` ni `gh pr create` sin petición explícita.

## Docs a actualizar
- docs/ESTADO.md si el PR cierra un hito (skill `session-handoff`)
