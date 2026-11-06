---
name: release-notes
description: Redactar notas de versión desde Conventional Commits (último tag..HEAD) para CHANGELOG, GitHub Release o Google Play (whatsnew, ≤ 500 caracteres); no valida (release-preflight) ni publica (release).
allowed-tools: Read, Write, Edit, Bash(git log *), Bash(git show *), Bash(git describe *), Bash(git tag --list *), Bash(wc *)
---

# release-notes

Genera las notas de la próxima versión desde `git log <último-tag>..HEAD`. Destino: `changelog` (sección nueva en `CHANGELOG.md`, por defecto), `github` (cuerpo del GitHub Release, texto para pegar) o `play` (`distribution/whatsnew/whatsnew-es-ES`).

## Cuándo usarla
- Se prepara una versión y hay que resumir qué cambió para el usuario.
- Se quiere la entrada de `CHANGELOG.md`, el cuerpo de un GitHub Release o las «Novedades» de Google Play.

## Cuándo NO usarla
- Comprobar secretos, migraciones o versión antes de publicar → usa `release-preflight`.
- Publicar la versión → usa `release`.
- Documentar una decisión técnica → usa `registrar-decision`.

## Precondiciones
- Repositorio con historial accesible; las notas se basan en commits, no en el working tree.
- Último tag: `git describe --tags --abbrev=0`. Sin tags, el rango es todo el historial y se indica.
- Versión objetivo conocida (la fija `release-preflight`); si falta, encabezado `## [Sin publicar]`.

## Pasos
1. Rango: `git log <último-tag>..HEAD --no-merges --pretty="%h|%s|%b%x1e"`.
2. Clasificar cada commit por tipo Conventional Commits:

   | Tipo | Sección de las notas |
   |---|---|
   | `!` o `BREAKING CHANGE:` | Cambios importantes (primero, con lo que debe hacer el usuario) |
   | `feat` | Novedades |
   | `fix` | Correcciones |
   | `perf` | Rendimiento |
   | `security`, o `fix` de seguridad | Seguridad |
   | `refactor`, `docs`, `test`, `chore`, `ci`, `build`, `style` | Omitir (salvo que cambien algo visible) |

3. Reescribir para el usuario: qué puede hacer ahora o qué se arregló, en una línea, sin clases, tablas ni rutas. Fusionar commits del mismo cambio.
4. Filtrar datos sensibles: ni claves, URLs privadas ni detalles explotables. Ante la duda, omitir y avisar. Notas en español, con el vocabulario de la app (tramo, notas, copiloto).
5. Commits sin formato Conventional Commits: no inventar el tipo; listarlos aparte en el informe.
6. Escribir la salida según el destino:
   - `changelog`: insertar `## [<versión>] - <AAAA-MM-DD>` sobre la versión anterior (crear con `# Changelog` si no existe).
   - `github`: mismas secciones, sin encabezado de versión.
   - `play`: escribir `distribution/whatsnew/whatsnew-es-ES` (sobrescribir). Solo texto plano para el usuario final de Play: viñetas `• `, sin encabezados ni Markdown, y sin cambios internos que no vea (paquete, CI, build). Máximo 500 caracteres; recortar fusionando o quitando lo menor.
7. Resumen: commits leídos, incluidos, omitidos y sin formato (y, en `play`, caracteres usados).

## Notas de Play
- El archivo se commitea junto con la versión (`chore(release): v<v>`).
- El CI lo sube con `whatsNewDirectory`. En subida manual se pegan en «Novedades» envueltas en `<es-ES>…</es-ES>` (ver `docs/play.md`).

## Validaciones / tests
- `git log <último-tag>..HEAD --no-merges --oneline` tiene tantas líneas como incluidos + omitidos + sin formato.
- `git diff -- CHANGELOG.md` sin valores parecidos a claves, tokens ni URLs internas.
- `play`: `wc -m distribution/whatsnew/whatsnew-es-ES` ≤ 500.

## Definition of Done
- [ ] Rango correcto (último tag o historial completo declarado).
- [ ] Solo secciones con contenido; cambios importantes primero.
- [ ] Lenguaje de usuario, sin jerga interna ni datos sensibles.
- [ ] `play`: archivo `whatsnew-es-ES` con viñetas `• ` y ≤ 500 caracteres (`wc -m`).
- [ ] Commits sin formato reportados, no inventados.

## Docs a actualizar
- `CHANGELOG.md` · `distribution/whatsnew/whatsnew-es-ES` · docs/ESTADO.md (skill `session-handoff`)
