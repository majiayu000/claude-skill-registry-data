---
name: arrancar-proyecto
description: >-
  Arrancar un proyecto con este template conversando: preguntar en UN solo mensaje lo básico que
  hace falta (nuevo o existente, nombres, módulo, solo o equipo, tablero, quién sos, dónde está el
  código), mostrar el plan con los comandos exactos, y con el "sí" correr todo por script
  (bin/arrancar-proyecto.py: instanciar, git init, instalar, enchufar el proyecto existente,
  informe). Usar cuando se pida "arrancá un proyecto", "instanciá el template", "agarrá el proyecto
  X", "sumale el template a mi carpeta", "quiero empezar con esto", "/arrancar-proyecto". Se usa
  parado en una copia del template (o en un núcleo ya instanciado, para enchufar otro proyecto). No
  inventa ningún dato: lo que no se contesta, se pregunta de nuevo o queda pendiente. Español
  (Argentina).
---

# Arrancar un proyecto

Es la puerta de entrada del template. Vos decís «arrancá un proyecto» o «agarrá el proyecto X» y el
template **pregunta lo que necesita, una sola vez, todo junto**. Nada de leer pasos.

## Dónde se usa

Parado en **una copia del template** (la carpeta copiada o clonada a donde va a vivir el núcleo del
proyecto; el nombre de la carpeta es libre). Si la carpeta ya está instanciada, la skill lo detecta y
sólo hace lo que falte (por ejemplo, enchufar otro proyecto existente).

> Si Claude Code está abierto **adentro de tu proyecto** y el template no está ahí, esta skill no
> existe todavía: copiá el template al lado, abrí Claude Code en esa copia y pedilo ahí.

## Paso 1 — Las preguntas, en un solo mensaje y en criollo

Se preguntan **todas juntas**, cada una con la recomendación al lado, y se termina el turno. Lo que ya
se puede deducir no se pregunta: se propone y se marca «propuesto».

1. **¿Proyecto nuevo o ya existe una carpeta con código?** Si existe: la ruta, si es back o front, y
   si la carpeta queda donde está (enlace, recomendado) o se muda adentro del núcleo.
2. **Nombres:** el proyecto, el producto o sistema, la organización (propuesto: tu nombre).
3. **El módulo:** un slug corto para el Cerebro (propuesto desde el nombre del proyecto).
4. **¿Solo o en equipo?** (propuesto: solo; **equipo sólo si decís que va a haber un equipo**: cambia el
   tablero, quién escribe el Cerebro y quién confirma, `DEC-006`).
5. **Tablero:** local (archivos del Cerebro; propuesto en modo solo), Azure DevOps, Jira u otro por
   MCP. Si es Azure: organización, proyecto y team, tal cual se llaman.
6. **Quién sos** (tu nombre firma las diferencias aceptadas y los cortes; propuesto: tu usuario de git).
6-bis. **¿Con qué lo vas a hacer?** Back (lenguaje y framework), front, base de datos, build y tests
   (`DEC-003`; propuesto: lo que diga el proyecto existente si lo hay; **si todavía no sabés, queda vacío** y
   se cierra antes de la primera Tarea que lo necesite). Se pasa con `--stack-back`, `--stack-front`,
   `--stack-base`, `--stack-build`, y **el comando que corre la suite completa** de cada repo
   (`--comando-tests-back`, `--comando-tests-front`): con eso las guías `tdd-stack-*.md` dejan de ser plantilla.
   Y **qué tipo de aplicación es** (web, Electron, escritorio con webview como Tauri, escritorio nativo, móvil, línea
   de comandos, API): de eso sale el motor de pruebas de punta a punta (`--stack-e2e`; propuesto según lo que diga
   el proyecto, p. ej. «web: Playwright, data-testid»).
7. Si hay proyecto existente: **¿agrego a su `CLAUDE.md` la línea que importa las reglas del núcleo?**
   (propuesto: sí; es una línea, reversible).

Formato: una lista numerada con la propuesta entre paréntesis, y el cierre *«Contestame lo que
quieras cambiar; lo demás va como está propuesto»*. Si la persona pegó el **prompt maestro**
([references/prompt-maestro.md](references/prompt-maestro.md)), todo lo que ya contestó ahí se toma como dado y
no se vuelve a preguntar.

## Paso 2 — El plan, y un solo «sí»

Con las respuestas se muestra **el comando exacto** que se va a correr y qué va a pasar, en cinco
líneas (instanciar → git init → instalar → enchufar el proyecto → informe), y se espera el «sí».
Proponer y ejecutar son turnos distintos.

```bash
python -I bin/arrancar-proyecto.py --proyecto "<nombre>" --producto "<producto>" --organizacion "<org>" --modulo <slug> \
    --modo <solo|equipo> --tablero <local|azure|jira|otro> --autor "<quién>" \
    [--existente "<ruta>" --como <back|front> [--mover] [--importar-reglas]] \
    [--azure-org <org> --azure-proyecto <proyecto> --azure-team <team>]
```

`--dry-run` muestra sin tocar: se usa si la persona duda.

## Paso 3 — Correr y contar

Se corre el comando **una vez**, se muestra su salida resumida y, si frenó, en qué paso y cómo seguir
(el script para en el primer paso que falla y no deja nada a medias). Después, el cierre:

- qué quedó hecho (módulo, modo, tablero, autor; si se enchufó un proyecto, dónde quedó el enlace y
  los cuatro informes en `borrador/adopcion/`);
- lo que sigue y lo decide una persona: **DEC-003** en lo que no se dijo al arrancar; la primera
  ficha funcional; y, si hay proyecto existente, la pregunta *«¿absorbo la app en modo documentar
  ahora?»* → [[absorber-aplicacion]] (lee los informes, no todo el repo; cada ítem entra al Cerebro con
  un «sí»).

## Barreras

- **No se inventa ningún dato**: nombre, slug, organización, tablero o rutas que no se contestaron se
  vuelven a preguntar o quedan `⚠` pendientes; nunca se completan «por default» sin decirlo.
- **Un solo «sí» sobre el plan mostrado**, y nada se corre antes.
- **No se toca el código del proyecto existente**; lo único que se escribe ahí es la línea del
  `CLAUDE.md`, y sólo si se aceptó en la pregunta 7.
- **No se escribe conocimiento en el Cerebro**: eso es [[absorber-aplicacion]], ítem por ítem.
- Todo en español (Argentina).
