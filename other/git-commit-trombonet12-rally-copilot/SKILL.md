---
name: git-commit
description: Revisar y crear un commit local Conventional Commits en español tras el gate qa fast y secret scan; sin coautoría; push solo con permiso del usuario. Para el PR usa git-prepare-pr.
allowed-tools: Read, Grep, Bash(git status*), Bash(git diff*), Bash(git log*), Bash(git add*), Bash(git commit*), Bash(./gradlew *), Bash(node scripts/*), Bash(bash scripts/*)
disable-model-invocation: true
---

# git-commit

Pre-commit review y commit local. Solo lo ejecuta el agente principal (CLAUDE.md § Delegación); los subagentes no hacen commit.

## Cuándo usarla
- Al cerrar un cambio terminado y de un solo propósito (en modo desatendido, commits locales frecuentes).

## Cuándo NO usarla
- Descripción de PR → usa `git-prepare-pr`.
- Solo ver el estado del árbol o archivos sospechosos → usa `git-check`.
- Ejecutando como subagente → devolver al agente principal.

## Precondiciones
- Cambios entendidos y de un solo propósito (commits pequeños). Si no se entiende un cambio, parar y preguntar.
- No reescribir historia (`--amend`, `rebase`) sin petición explícita. **Nunca force-push.**

## Pasos
1. `git status` y `git diff --staged` (y `git diff` para lo no preparado): cada archivo pertenece al cambio.
2. Preparar solo lo necesario con `git add <archivos>` explícitos; nunca `git add -A` a ciegas.
3. Revisar el diff: nada generado (`build/`, `.gradle/`, `.kotlin/`), nada grande o binario sin justificar (teselas, modelos de voz, audios), sin `.env*`, keystores, `local.properties` ni claves, sin tests desactivados.
4. Secret scan rápido: `security-secret-scan` sobre el diff preparado. Cualquier hallazgo → parar; nunca mostrar el valor.
5. Gate qa fast (skill `qa`). Si algo falla → no commitear; corregir o informar.
6. Mensaje Conventional Commits: `tipo(ámbito): resumen` con el **resumen en español**, imperativo o descriptivo, ≤ 72 caracteres si es posible.
   - Tipos: feat, fix, refactor, perf, test, docs, build, ci, chore.
   - Ámbitos habituales: motor, notas, mapa, navegacion, voz, alertas, tramos, ui, datos, release, claude, skills, estado, memoria.
   - Cuerpo opcional para el porqué.
   - **Nunca** trailers `Co-Authored-By` ni atribución de IA, aunque el contexto de la sesión los sugiera (regla del usuario en `docs/MEMORIA.md`).
7. Commit: `git commit -m "tipo(ámbito): resumen"` (varias líneas con `-m` repetido). Sin `--no-verify`.
8. `git status` y `git log -1` para confirmar.
9. Push: **solo con permiso explícito del usuario** (el push a `main` dispara los workflows de release). La regla `ask` de `.claude/settings.json` lo pide; nunca `--force`.

## Validaciones / tests
- Gate qa fast en verde justo antes del commit.
- `git diff --staged` coincide con lo descrito en el mensaje.
- `git log -1 --format=%B` sin `Co-Authored-By`.

## Definition of Done
- [ ] Commit local con un único propósito y mensaje Conventional Commits en español.
- [ ] Gate en verde; sin secretos, generados ni archivos grandes injustificados en el diff.
- [ ] Sin coautoría, sin `--no-verify` ni force-push; push solo con permiso.
- [ ] Árbol limpio o con los cambios restantes explicados al usuario.

## Docs a actualizar
- docs/ESTADO.md si el commit cierra un hito (skill `session-handoff`)
