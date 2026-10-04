---
name: instanciar
description: Instancia esta plantilla en un proyecto real mediante una entrevista guiada — detecta si el proyecto es nuevo o existente, rellena los placeholders, adapta los docs al tipo de proyecto y decide la política de permisos. Úsalo cuando la persona clone/adopte esta plantilla y quiera configurarla para su proyecto (p. ej. "instancia esta plantilla", "configura este template para mi proyecto", "arranca el proyecto desde esta base").
---

<!-- Skill de ejemplo de la plantilla — adáptalo o elimínalo según tu proyecto. -->

Convierte esta plantilla en la documentación real de un proyecto mediante una entrevista.
Lee `TEMPLATE-USAGE.md` primero: es la fuente de verdad del catálogo de placeholders (§3),
las reglas de borrado por tipo (§7) y el flujo de adopción (§2). Sigue ese documento si
difiere de los pasos de abajo.

## Paso 0 — Guardián de seguridad (antes de nada)

Detente y avisa si estás sobre el REPO-FUENTE del template (no una instancia):

- Revisa `git remote -v`. Si el origin es el repositorio de la plantilla
  (`project-starter-template-es-ai`), NO instancies: estarías destruyendo la plantilla.
- En ese caso, pregunta explícitamente si de verdad se quiere modificar la plantilla
  original antes de continuar.

## Paso 1 — Detectar contexto (nuevo vs. existente)

Sin preguntar aún, inspecciona el repo para deducir el contexto:

- ¿Hay código real? (`package.json`, `Gemfile`, `pyproject.toml`, `go.mod`, `src/`, etc.)
- ¿El historial de git tiene commits propios del proyecto o es un clon recién iniciado?
- ¿Siguen intactos los `[PLACEHOLDERS]`?
  (`grep -rno '\[[A-ZÁÉÍÓÚÑ0-9_/]\+\]' --include='*.md' .`)

Deduce **NUEVO** (repo vacío / placeholders intactos) o **EXISTENTE** (ya hay código).

## Paso 2 — Confirmar y entrevistar (usa AskUserQuestion)

Muestra tu deducción del Paso 1 y deja corregirla. Luego pregunta SOLO lo que no puedas
inferir. En proyectos existentes, pre-rellena las respuestas leyendo el código.

- **Lote A · Contexto y tipo:** nuevo/existente; tipo (Web · Móvil · Escritorio ·
  API/servicio · Librería).
- **Lote B · Identidad:** nombre, autor, usuario/org de GitHub, empresa (opcional),
  email de soporte, email de seguridad, licencia y año. Infiere autor/usuario de
  `git config` y el año de la fecha del sistema.
- **Lote C · Stack:** runtime, gestor de paquetes, base de datos (o "ninguna"), puerto,
  comandos (instalar / dev / test / lint). En existente: LÉELO del código, no preguntes.
- **Lote D · Capacidades:** ¿API? ¿autenticación? ¿i18n? ¿SEO/web pública? ¿emails
  transaccionales? ¿sistema de diseño/UI? (Cada "no" implica borrar su convención.)
- **Lote E · Permisos:** ¿dejar el `ask:[Bash]` conservador de `.claude/settings.json`,
  o crear `.claude/settings.local.json` con una allowlist de solo-lectura?

  Los **tres guardrails** (git, secretos y specs) vienen **activos**: solo se tocan si
  la persona lo pide expresamente, y entonces queda escrito en el ADR del Paso 6.

  Activa además los git hooks del clon, que no viajan en el repositorio:
  `bash .github/scripts/check-hooks-enabled.sh --arreglar`. Sin eso, `pre-commit` no
  formatea y `pre-push` no verifica: los fallos se descubren en el CI.

## Paso 3 — Rellenar / fusionar según contexto

Reemplaza los placeholders del catálogo (`TEMPLATE-USAGE.md §3`) con las respuestas:
`[NOMBRE_DEL_PROYECTO]`, `[AUTOR]`, `[USUARIO_GITHUB]`, `[NOMBRE_EMPRESA]`,
`[URL_REPOSITORIO]`, `[AÑO]`, `[EMAIL_SOPORTE]`, `[EMAIL_SEGURIDAD]`, `[RUNTIME]`,
`[GESTOR_DE_PAQUETES]`, `[BASE_DE_DATOS]`, `[PUERTO]`, `[COMANDO_*]`, `[URL_*]`, `[FECHA]`.

Archivos que se actualizan: `README.md`, `AGENTS.md` (resumen + comandos),
`docs/architecture/*`, `docs/product/*`, `.env.example`, `LICENSE` (año + autor),
`SECURITY.md` (emails), `CHANGELOG.md` (primera entrada).

- **NUEVO:** escribe directo desde las respuestas. Trabaja en el repo tal cual.
- **EXISTENTE:** lee el código e infiere para no dejar `[…]`. **NO sobrescribas**
  `README.md`, `LICENSE` ni `.gitignore` — propón el merge a mano. Trabaja en una rama
  `chore/adopt-doc-template`. Sugiere correr `/init` para integrar el contexto del código.

Además, escribe `.template-origin` en la raíz para que `/actualizar-plantilla` pueda
traer mejoras futuras de la plantilla:

```
repo=<URL de esta plantilla>
commit=<SHA del HEAD de la plantilla usado como base>
fecha=<YYYY-MM-DD de hoy>
```

## Paso 4 — Aplicar la decisión de permisos (Lote E)

Si se eligió "automático", crea `.claude/settings.local.json` con una allowlist de
comandos de solo-lectura (`ls, cat, head, tail, wc, grep, rg, find, tree, sort, uniq,
echo, pwd, which`, y `git status/log/diff/branch/show/remote`). Verifica que
`.claude/settings.local.json` esté en `.gitignore`. Si se eligió "conservador", no toques
nada de permisos.

Si se aceptaron los **guardrails de git** y/o los **guardrails de secretos**, añade los
bloques `hooks.PreToolUse` que apuntan a `.claude/hooks/git-guardrails.sh` (matcher
`Bash`) y `.claude/hooks/secret-guardrails.sh` (matcher `Write|Edit`) — el JSON completo
está en `docs/conventions/ai-agents.md`. Requieren `python3`.

## Paso 5 — Limpieza por tipo (regla de TEMPLATE-USAGE.md §7)

Borra los docs/convenciones que no apliquen:

- Móvil / Escritorio → borra `docs/conventions/seo.md`; reenfoca `ui`, `api`, `deploy`.
- API / Librería → borra los docs de UI (`conventions/seo.md`, `conventions/ui.md`,
  `architecture/screens.md`) y la carpeta `design/` con `DESIGN.md`.
- Cada capacidad respondida "no" en el Lote D → borra su convención (p. ej. sin i18n →
  `docs/conventions/i18n.md`) **y su skill asociada**: sin i18n → `i18n-parity`; sin
  base de datos → `migration-guard`; sin SEO/web pública → `seo-audit`; sin UI (API o
  librería) → `design-system-audit`, `accessibility-audit`, `copywriting`, `identidad`,
  `prototipo` y el subagente `designer`.
- **Siempre** borra los archivos exclusivos del repo-plantilla: el workflow
  `.github/workflows/template-parity.yml`, el script `.github/scripts/check-parity.sh`
  y la skill `.claude/skills/portar-cambio/` — solo sirven para mantener la familia de
  variantes, no a un proyecto instanciado.

Pregunta antes de borrar en bloque si hay ambigüedad.

## Paso 6 — Cierre

Registra la instanciación como el ADR `0002` (usa `docs/decisions/0000-template.md`):
contexto del proyecto, stack elegido, tipo, convenciones eliminadas y política de
permisos/guardrails — así el proyecto estrena su propio registro de decisiones.

Muestra un resumen del diff y la lista de placeholders que aún requieren decisión humana.
NO hagas commit — deja que la persona revise. En "existente", recuérdale que todo quedó
en la rama para abrir un PR. Sugiere borrar `TEMPLATE-USAGE.md` cuando termine.

Ejemplo: `/instanciar` → entrevista → repo con documentación real y `docs/` podados.

NO instancies sobre el repo-fuente del template (Paso 0), NO sobrescribas el código de
producción en proyectos existentes, NO hagas commit ni push por tu cuenta, y NO inventes
datos: si no puedes inferir un valor y la persona no lo da, deja el placeholder y
**márcalo como pendiente en su línea** —`[EMAIL_SEGURIDAD] <!-- pendiente: aún sin
buzón -->`, o con `#` dentro de un bloque de código—. `check-placeholders.sh` distingue
lo que decidiste dejar de lo que se te olvidó; sin la marca, falla.

Y no dejes el CHANGELOG ni los ADRs de la plantilla: son de otro repositorio. Resetea el
CHANGELOG conservando su `## [Unreleased]` (sin una entrada, `check-changelog.sh`
bloquea el primer PR) y borra todo ADR salvo el `0001`. Lo verifica
`check-inheritance.sh`.
