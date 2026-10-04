---
name: release
description: Corta una nueva versión — mueve la sección Unreleased del CHANGELOG a una versión SemVer con fecha, crea el commit y el tag, y opcionalmente el release de GitHub. Úsalo cuando la persona pida publicar/cortar una versión o preparar un release (p. ej. "corta la versión 1.2.0", "prepara el release", "publica una nueva versión"). No hace push sin confirmación.
---

Corta una versión siguiendo Keep a Changelog y Semantic Versioning (ver `CHANGELOG.md`
y `CONTRIBUTING.md`).

> **Automatización:** al fusionar `develop` → `main`, el workflow
> `.github/workflows/release.yml` detecta la versión fechada más reciente del
> CHANGELOG y, si no tiene tag, publica el tag y el release de GitHub solo. Esta
> skill prepara el corte (mover Unreleased → `X.Y.Z` con fecha y elegir la versión
> SemVer); el tag/release manual solo hace falta si el workflow no está activo.

## Pasos

1. **Precondiciones.** Verifica que el árbol esté limpio (`git status`) y que estés en la
   rama correcta según `CONTRIBUTING.md`: con Git Flow el release sale de `develop` hacia
   `main`, salvo un hotfix, que se corta en la propia `hotfix/*` (ver abajo); sin
   `develop`, desde `main`. Si hay cambios sin commit, detente y avisa.
2. **Leer lo pendiente.** Toma las entradas de la sección `## [Unreleased]` de
   `CHANGELOG.md`. Si está vacía, no hay nada que publicar: dilo y detente.
3. **Proponer la versión.** Lee la última versión publicada (tag `v*` o CHANGELOG) y
   propone el bump SemVer según el contenido: cambios incompatibles → **major**; solo
   `Added`/`Changed` → **minor**; solo `Fixed`/`Security` → **patch**. Deja que la
   persona confirme o corrija con AskUserQuestion.
4. **Actualizar el CHANGELOG.** Mueve las entradas de `Unreleased` a una nueva sección
   `## [X.Y.Z] - YYYY-MM-DD` (fecha de hoy), deja `Unreleased` con sus categorías vacías
   y actualiza los enlaces de comparación del pie del archivo.
5. **Sincronizar la versión del manifiesto.** Si el stack tiene un archivo que declara
   versión, súbela a `X.Y.Z` en el mismo commit — si no, el proyecto publica `v0.4.0`
   con el manifiesto diciendo `0.1.0`. Busca el que aplique y actualiza también su
   lockfile si el gestor lo regenera:
   - `package.json` (+ `package-lock.json` / `pnpm-lock.yaml`) · `*.gemspec` o
     `lib/**/version.rb` · `Cargo.toml` (+ `Cargo.lock`) · `pyproject.toml` ·
     `composer.json` · `pubspec.yaml` · `build.gradle` · `VERSION`.
   - Si no hay ninguno (proyecto sin manifiesto versionado), dilo y sigue: el
     CHANGELOG es la única fuente de la versión.
6. **Commit, sin tag.** Crea el commit `chore(release): vX.Y.Z` (con la coautoría de IA
   de `docs/conventions/ai-agents.md`) en una rama `chore/corte-vX.Y.Z` — recuerda que
   `git-guardrails.sh` no deja commitear directo en `develop`.
   **NO crees ni publiques el tag aquí.** `release.yml` solo publica si la versión
   **no tiene tag**: si lo creas tú, el workflow la da por publicada, no crea el release
   de GitHub, y encima el tag apunta al commit de la rama en vez de al merge en `main`.
7. **Llevarlo a producción.** PR de la rama de corte → `develop`, y después PR
   `develop` → `main`. Al fusionar en `main`, `release.yml` crea el tag `vX.Y.Z` sobre
   el merge y publica el release con las notas de esa sección del CHANGELOG.
8. **Solo si el workflow no está activo** (proyecto sin Actions, o `release.yml`
   borrado): entonces sí, tag anotado a mano y
   `gh release create vX.Y.Z --title "vX.Y.Z" --notes "<sección del CHANGELOG>"`.

## El corte es lo último antes de fusionar a `main`

El job `release` de `quality.yml` (`.github/scripts/check-release.sh`) bloquea los PRs
hacia `main` si la versión de arriba del CHANGELOG ya está publicada, si quedaron
entradas sueltas en `## [Unreleased]`, o si esa versión es **heredada de la plantilla**
(un CHANGELOG sin resetear deja arriba la última versión del repositorio origen). Es la misma regla dicha al revés: **nada llega a
producción sin versión**. Si el PR a `main` falla por eso, no lo esquives — corta la
versión.

## Hotfix (release desde `main`)

Un `hotfix/*` no pasa por `develop`, pero **también publica versión** (siempre un
**patch**). El orden es:

1. En la rama `hotfix/*` (nacida de `main`): el fix, su entrada en `## [Unreleased]` y
   el corte con esta skill — pasos 3 a 6, con el bump `patch`.
2. PR `hotfix/*` → `main`. El job `release` lo valida y, al fusionar, `release.yml`
   publica el tag y el release.
3. **Sincroniza a `develop`** con un PR `main` → `develop` (lo exige
   [`CONTRIBUTING.md`](../../../CONTRIBUTING.md)): si te lo saltas, `develop` no tiene
   ni el fix ni la sección de versión del CHANGELOG, y el próximo corte la pisa.

Ejemplo: "corta la versión" → propone `v1.3.0` → CHANGELOG actualizado + commit en
`chore/corte-v1.3.0`; el tag y el release los pone `release.yml` al llegar a `main`.

NO crees el tag a mano cuando `release.yml` esté activo (le robas el release), NO hagas
push ni publiques sin confirmación explícita, NO inventes entradas de changelog que no
estén en `Unreleased`, y NO saltes una versión SemVer.
