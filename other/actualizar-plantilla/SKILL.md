---
name: actualizar-plantilla
description: Trae a este proyecto las mejoras que la plantilla de origen recibió después de la instanciación — lee .template-origin, calcula el diff del tooling (skills, hooks, scripts, workflows) contra la plantilla actual y propone aplicarlo. Úsalo cuando la persona quiera actualizar/sincronizar el proyecto con la plantilla (p. ej. "actualiza la plantilla", "trae las mejoras nuevas del template").
---

Sincroniza el **tooling** de este proyecto con la versión actual de su plantilla de
origen. Solo toca la capa reutilizable — nunca la documentación ya rellenada ni el código.

> El workflow `.github/workflows/template-update-check.yml` revisa semanalmente si la
> plantilla publicó mejoras y abre un issue de aviso — esta skill es la que las aplica.

## Paso 1 — Leer el origen

Lee `.template-origin` en la raíz (lo escribe `/instanciar`):

```
repo=https://github.com/brayandiazc/project-starter-template-es-ai
commit=<sha-de-la-plantilla-al-instanciar>
fecha=YYYY-MM-DD
versiones=<versiones del CHANGELOG de la plantilla al instanciar, separadas por coma>
```

Si no existe, pregunta de qué plantilla/variante vino el proyecto y desde qué fecha
aproximada, y usa el tag/commit de esa época como base.

## Paso 2 — Calcular el diff del tooling

Clona la plantilla a un directorio temporal y calcula qué cambió desde el commit de
origen, **limitado a las rutas de tooling**:

```bash
git clone --quiet <repo> /tmp/tpl-update && cd /tmp/tpl-update
git diff --stat <commit-origen>..HEAD -- \
  .claude/ .github/scripts/ .github/workflows/ specs/_template/ \
  docs/conventions/_template.md
```

Excluye siempre: `README.md`, `docs/` rellenados, `CHANGELOG.md`, `LICENSE` y cualquier
archivo que el proyecto haya adaptado (compara antes de pisar; si el archivo local
difiere de la versión vieja de la plantilla, es una adaptación local — muéstrala y
pregunta).

### Documentos: distingue NUEVO de EXISTENTE

«No tocar la documentación» es la regla correcta para los documentos que el proyecto ya
tiene rellenados. **No lo es para los que no existen.** Un proyecto que adoptó la
plantilla hace tiempo puede estar a dieciséis documentos de distancia —convenciones
nuevas, convenciones nuevas, la definición de terminado— y hoy no se los trae nadie: esta
skill los excluye por diseño y `/instanciar` cree que el proyecto es virgen.

```bash
# Documentos de la plantilla que el proyecto NO tiene: traerlos es seguro.
(cd /tmp/tpl-update && find docs legal design -type f -name "*.md" 2>/dev/null) \
  | while IFS= read -r f; do [ -e "$f" ] || echo "NUEVO: $f"; done
```

- **No existe** → se propone traerlo, con sus placeholders sin rellenar. Es documentación
  que falta, no documentación que se pisa.
- **Existe** → no se toca. Se lista como «revisar a mano» y ahí acaba la intervención.

### Y revisa los renombrados

**Es el fallo silencioso de esta skill**, así que va antes de proponer nada: un documento
que la plantilla renombró o fusionó no se sustituye, **se duplica**. Quedan los dos —el
tuyo con contenido y el nuevo vacío—, los dos son markdown válido, los enlaces resuelven
y ningún check chista.

Busca en el `CHANGELOG.md` de la plantilla, entre tu versión y la actual, las entradas de
`### Changed` y `### Removed` que mencionen rutas de archivo. Contrástalas con lo que
tiene el proyecto y propón la migración par por par: mover el contenido y borrar el
viejo, **nunca dejar ambos**.

### Checks que se volvieron más estrictos

Es el caso que más fácil rompe un proyecto ajeno: un check que ya existía **empieza a
exigir cosas que antes no exigía**, y el primer PR sale en rojo por decenas de motivos a
la vez. Un rojo así no se arregla: se ignora, y a partir de ahí el check deja de servir.

**Antes de traer un check nuevo o actualizado, córrelo y mira qué diría**, sin adoptarlo
todavía. Si señala mucho, resuélvelo en **un commit aparte y anterior**.

El caso concreto de hoy: `check-placeholders.sh` pasó a ver los **huecos en prosa**
(`[Un párrafo describiendo…]`), que antes eran invisibles. En un proyecto real son unos
160 de golpe. Tiene modo de migración:

```bash
bash .github/scripts/check-placeholders.sh --marcar
```

Los marca en una pasada **diciendo que están sin revisar**, para que el CI vuelva a verde
sin esconder nada: siguen listándose en cada ejecución hasta que alguien los escriba. Solo
toca la prosa — los placeholders `[MAYÚSCULAS]` son valores por sustituir y marcarlos en
bloque sí sería taparlos.

Ese commit va **antes** del que trae el check, y su mensaje debe decir que son heredados.

**Endurecimientos recientes** — lo que va a señalar el tooling nuevo en un proyecto
instanciado antes de que llegaran:

- `check-inheritance.sh`: tu `.template-origin` no tiene `versiones=` — añádela con las
  versiones que la plantilla tenía cuando instanciaste (están en su CHANGELOG).
- `check-placeholders.sh`: ya revisa `.github/` (salvo scripts/workflows) — el
  `[URL_REPOSITORIO]` de `ISSUE_TEMPLATE/config.yml` va a salir; rellénalo.
- `spec-guardrails.sh`: exige también `design.md` y `tasks.md` sin líneas de plantilla
  antes de editar código en `feat/*`/`fix/*`.
- `secret-guardrails.sh`: bloquea leer/escribir `.env` y llaves también vía Bash.

## Paso 3 — Proponer y aplicar

Presenta un resumen por archivo (nuevo / actualizado / eliminado en la plantilla) y deja
elegir qué aplicar. Trabaja en una rama `chore/update-template`. Aplica lo aceptado,
ejecuta la suite `bash .github/scripts/tests/run-tests.sh` si existe, y actualiza
`.template-origin` con el nuevo commit y la fecha de hoy.

## Paso 4 — Cierre

Muestra el diff final y recuerda abrir un PR. NO hagas commit ni push sin confirmación.

Ejemplo: `/actualizar-plantilla` → "la plantilla tiene 3 mejoras de tooling desde tu
instanciación (hook nuevo, script de enlaces, workflow de calidad); ¿aplico las 3?"

NO pises adaptaciones locales sin preguntar, NO toques documentación ya rellenada ni
código de producción, y NO apliques cambios de la plantilla que el proyecto decidió
eliminar (p. ej. convenciones borradas a propósito).
