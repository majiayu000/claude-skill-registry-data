---
name: desarrollar-asignadas
description: >-
  Revisar el tablero (Azure DevOps por MCP, o el tablero local de archivos según DEC-006),
  tomar las Tareas asignadas sin dependencias pendientes y desarrollarlas en paralelo: un
  worktree y un worker por tarjeta, con la misión única de armar-mision.py. Dos modos de
  lanzamiento con el mismo flujo: dentro de Orca (variable ORCA_APP_VERSION; workers en
  pestañas) o sin Orca (IntelliJ o terminal: worktrees de git y claude -p / gemini -p;
  references/sin-orca.md). Verifica siempre otro agente en sólo lectura: otro motor si hay, o
  uno del mismo motor con contexto limpio (DEC-005). El orquestador queda atento hasta que la
  última termina. Con DEC-005 confirmada las respuestas del plan salen de la decisión; si no,
  se piden: el plan, tomar la tarjeta y un "Aprobar" por Tarea. Usar cuando se pida "desarrollá
  mis tareas asignadas", "arrancá con lo que tengo asignado", "poné a trabajar el tablero",
  "/desarrollar-asignadas". Español (Argentina); no inventa: #ID, estados y dependencias son
  dato duro.
---

# Desarrollar asignadas (Orca o sin Orca + tablero)

Orquesta el desarrollo de las tarjetas asignadas al usuario en el tablero
autorizado, respetando las dependencias declaradas entre ellas, disparando
en paralelo lo que está libre en worktrees separados (una ventana o un
worker por tarjeta), con una verificación independiente, y pidiendo un "Aprobar"
humano antes de cerrar el ciclo de cada una (push, comentario de cierre y
link del MR).

## Modo sin Orca (IntelliJ o terminal) y tablero local

Sin la variable `ORCA_APP_VERSION` el flujo es **el mismo** con otro lanzador: los worktrees se abren con `git
worktree add` después del `bin/gate-worktree.py`; cada worker se lanza con `claude -p "Leé y seguí la misión de
<archivo>" --add-dir <núcleo>` (o `gemini -p … --include-directories`) parado en su worktree, y se reanuda con
`--resume`; el verificador igual, en sólo lectura (Claude: sub-agente sin herramientas de escritura; Gemini:
`--approval-mode plan --policy bin/gemini-verificador-solo-lectura.toml`). Los diffs se miran en el IDE. Lo
operativo, paso a paso, y las decisiones abiertas de ese modo están en `references/sin-orca.md`.

**Tablero local (`DEC-006`).** Si el proyecto usa el tablero local, «el tablero» es `cerebro-digital/<modulo>/backlog/`
y se opera con `bin/tablero-local.py`, mismos GATEs, sin MCP (detalle: `backlog/README.md` del módulo).

**Motor único (`DEC-005`, modo solo).** Si el proyecto desarrolla con un solo motor, verifica **otro agente del
mismo motor, con contexto limpio y sólo lectura**, y el veredicto lo declara («Verificado por: Claude Code ·
sub-agente de sólo lectura»). Si hay otro motor instalado, se prefiere.

## 0. Elegir el modo de lanzamiento (antes que nada)

Un solo flujo, dos formas de lanzar los workers. Orca define en cada sesión que abre la
variable de entorno `ORCA_APP_VERSION`; fuera de Orca no existe. Lo primero es mirarla:

```
echo "${ORCA_APP_VERSION:-}"      # Bash
$env:ORCA_APP_VERSION             # PowerShell
```

- **Vacía → modo sin Orca** (`references/sin-orca.md`): los mismos pasos, con worktrees de
  git y `claude -p` / `gemini -p` en segundo plano. No se intenta abrir Orca ni "simularlo".
- **Con valor → modo Orca**, y en el plan del paso 4 se informa la versión de Orca.

## Prerrequisito

Lo fija `DEC-006`. Con **tablero local** no hace falta nada: `bin/tablero-local.py` lee y
escribe los archivos del módulo. Con **Azure DevOps, Jira u otro tablero por MCP**, el MCP tiene
que estar conectado (`/mcp` lo muestra activo); si no lo está, avisar y derivar a
`cerebro-digital/configuracion-ia/integracion-azure-mcp/00-index.md` en vez de intentar leer el board.

## Flujo

1. **Relevar.** Con tablero local: `bin/tablero-local.py listar --asignado <yo> --json` y se
   descartan los estados terminales. Con Azure: `search_work_items` / `list_work_items` filtrando por el
   tablero autorizado ([[tablero-autorizado]]: org `{{AZURE_ORG}}`, proyecto
   `{{AZURE_PROYECTO}}`, team `{{AZURE_TEAM}}`) +
   `AssignedTo = @Me` + estado no terminal (no `Done`/`Closed`/`Removed`).

2. **Armar el grafo de dependencias.** Por cada tarjeta traída: `get_work_item`
   (relaciones *Related*) + leer en la descripción el campo/texto donde se
   declaran dependencias explícitas ("depende de #NNNN"). Clasificar cada
   una en:
   - **Libre**: sin dependencia pendiente dentro del lote relevado.
   - **Bloqueada**: depende de otra tarjeta del mismo lote que todavía no
     está validada/cerrada. Registrar de qué `#ID` depende.

3. **Repo destino por tarjeta.** La lista de repos no está fija en esta
   skill: se descubre en cada corrida, porque van a ir apareciendo más
   (`<repo-front-1>`, `<repo-front-2>`, `<repo-infra>`, etc.).

   **3.1 Descubrir los repos candidatos.**
   - **Primero, la carpeta padre de este repo** (repos hermanos, que es
     como están clonados hoy: por ejemplo `<repo-back>`,
     `<repo-front>`): cada subcarpeta que sea un repo git
     (`git -C <carpeta> rev-parse --is-inside-work-tree`).
   - **Después, adentro de este repo**, en `back/*` y `front/*` (mismo
     chequeo). Es la convención documentada en `back/README.md` y
     `front/README.md`: el código se clona en `back/<repo>` y
     `front/<app>`.
   - Dónde viven los repos de código es una **decisión abierta** (ver la
     tabla de decisiones abiertas de `references/sin-orca.md`); mientras
     tanto se aceptan las dos ubicaciones, sin aviso.
   - De cada uno, anotar la ruta, el nombre de la carpeta y el remoto
     `origin` (el último tramo de la URL es el nombre real del repo en
     GitLab).
   - Si un mismo repo (mismo remoto `origin`) aparece en los dos lugares,
     **preguntar** cuál usar.
   - `orca repo list --json`: qué repos ya están registrados en Orca y con
     qué `id`. El `--repo id:<id>` del paso 6 sale de acá.
   - **Excluir este repositorio** (el del Cerebro): es el del
     conocimiento, no el del código ([[decisiones#DEC-001]]). Solo es
     destino si la tarjeta es explícitamente sobre el Cerebro o las skills.

   **3.2 Buscar la evidencia en la tarjeta**, en este orden:
   1. El campo **«Componente / repo:»** de la Descripción (plantilla de
      Tarea).
   2. El **Área** (Area Path) y la **etiqueta**, si nombran un repo o una
      capa.
   3. El **prefijo del título** («Backend -», «API -», «Front -»,
      «Infra -»…).
   4. La **Historia padre**: si todas sus Tareas hermanas ya tienen repo, se
      muestra como pista, nunca como prueba.

   **3.3 Decidir.**
   - **Coincidencia exacta y única** entre la evidencia y el nombre de un
     repo descubierto → repo inferido. En el plan del paso 4 se muestra
     **de dónde salió** (por ejemplo: «Componente / repo: <repo-back>»).
   - **Coincidencia aproximada** (un alias o un nombre viejo, por ejemplo
     «backend-monolito» → `<repo-back>`) → se muestra como
     **propuesta ⚠** con el porqué, y se confirma en el paso 4. No se da
     por buena en silencio.
   - **Varias opciones, ninguna o evidencia contradictoria** (el título
     dice «Front» y el campo dice back) → **preguntar** por tarjeta, en
     criollo y con los repos descubiertos como opciones. Nunca repartir a
     ciegas.
   - **La tarjeta nombra un repo que no está clonado** (ni en la carpeta
     padre ni en `back/` / `front/`) → avisar y preguntar (¿se clona?, ¿se deja para otra corrida?). No
     clonar por cuenta propia.
   - **El repo está clonado pero no registrado en Orca** → avisar y
     preguntar antes de `orca repo add`.

   Si varias tarjetas del lote van a repos distintos, se reparten en
   worktrees de su propio repo. El techo de paralelo (paso 6) es por
   máquina, no por repo.

4. **Mostrar el plan y confirmar.** Si `DEC-005` (modo desatendido) está **confirmada** en
   `decisiones.md`, las respuestas de este paso (base, motor, permisos, autorización de commits)
   salen de la DEC y se citan en el plan; sólo lo que la DEC no fija se pregunta. Si no, antes de
   tocar Azure u Orca, presentar
   en un solo mensaje, y pedir confirmación explícita (Sí / ajustar) —nunca
   arrancar en silencio—:
   - la versión de Orca (paso 0), libres (con repo inferido) vs bloqueadas
     (con su dependencia);
   - por cada libre, **de qué rama sale**, con el porqué de la propuesta
     (GATE de WORKTREE de [[AGENTS]]: la base se pregunta, nunca se
     infiere), y **cuántos worktrees hay abiertos** en la máquina;
   - **con qué motor se programa y quién verifica**, según `DEC-005`: con motor
     único (modo solo) programa Claude y verifica otro agente del mismo motor con
     contexto limpio, sin preguntar; con dos motores instalados, el humano elige
     cuál programa y verifica el otro (punto 6.2). Se corre `claude --version` (y
     `gemini --version` si aplica): si el que hace falta no responde, se dice acá y
     esa Tarea no se despacha;
   - si programa Gemini, su modo de permisos (`--approval-mode`): se
     recomienda `auto_edit`, que aprueba solo las ediciones y deja los
     comandos para que el humano los apruebe en la pestaña;
   - que los workers hacen **commits locales de trabajo** (la evidencia
     TDD) y no pushean: entra en el mismo "sí" del plan;
   - **avisos**, sin pregunta aparte: el Cerebro de `develop` atrasado
     respecto de `main`, un el `ARCHITECTURE.md` de la carpeta `docs` del repo que contradice
     al Cerebro, Tareas que tocan los mismos archivos (van en serie) y
     Tareas que van a superar los 20 archivos ([[orquestador-desarrollo]]
     §«Convenciones del Cerebro: reglas que se chequean»).

5. **Tomar cada tarjeta libre.** Delegar en [[tomar-tarea]] para cada una
   (respeta su gate de "ya la tiene otra persona" y pasa a Assigned+Active
   con confirmación).

6. **Orquestar en Orca.** Se usa la guía de la versión instalada (`orca
   skills get orchestration`) y el mismo ejecutable `orca` para toda la
   corrida.
   - `orca status --json` y `orca orchestration run-create --objective
     "<lote>" --json` → `run_id` para todo el lote.
   - **Hasta 8 Tareas en simultáneo**, y nunca más que lo que deja el techo
     de 8 worktrees por máquina contando los que ya están abiertos. Las que
     no entran quedan pendientes para la próxima corrida (no se lanzan a
     ciegas).
   - Por cada Tarea se anota el **SHA de la base** (`git -C <repo>
     rev-parse <base confirmada>`): lo que se verifica son los commits
     `<sha-base>..<rama>`.
   - **Base al día antes de despachar (regla dura).** Todo lo que se envía
     contempla lo último de la rama base, sin importar cuándo se empezó el
     trabajo. Antes de despachar **cualquier** worker o verificador —también
     sobre un worktree que ya existe (ajuste, retoma, verificación)— y antes
     de abrir o actualizar un MR: `git -C <worktree> fetch origin` y
     `git -C <worktree> rev-list --count HEAD..origin/<base>`. Si es mayor
     que 0, se trae `origin/<base>` a la rama **con merge, nunca rebase** (ya
     se pusheó: no se reescribe historia), se resuelven los conflictos, se
     corre la suite completa (el comando de la suite completa del stack) y,
     si hay `openapi.yaml`, Spectral, y se anota el **nuevo SHA de base** (el
     audit pasa a ser `<nuevo-sha-base>..<rama>`). Si el conflicto cambia
     comportamiento o la suite queda en rojo por lo traído, se frena y se
     avisa en criollo: no se despacha. La misión del worker y la del
     verificador dicen que la rama ya contiene la base al día y con qué SHA.
     Sin eso la misión no sale.
   - **Si programa Claude** (worker supervisado de Orca):
     - `orca orchestration task-create --spec "<la misión del punto 6.1>"
       --task-title "#<ID> <título>" --run <run_id> --json` → `task_id`.
     - `orca orchestration worker-start --task <task_id> --worktree
       new-top-level --repo id:<id del repo, del paso 3.1> --name
       <ID>-<slug> --base-branch <base confirmada> --agent claude --run
       <run_id> --json`. Crea el worktree, abre la ventana y deja al worker
       **supervisado**: su aviso de terminado le llega al orquestador.
     - **Se confirma que arrancó:** `orca orchestration worker-read
       --dispatch <dispatch_id> --source auto --json`. Si la misión quedó
       cargada sin enviarse, se avisa y se sigue la referencia `recovery-and-cleanup` de la skill `orchestration` de Orca
       (`orca skills get orchestration`).
     - Si `worker-start` sale distinto de 0, **no se relanza**: se lee el
       recibo (`failedStage`, `residualResources`) y la misma receta.
   - **Si programa Gemini** (Orca no lo lanza como worker supervisado):
     - `orca worktree create --repo id:<id> --name <ID>-<slug>
       --base-branch <base confirmada> --no-parent --json` (Orca abre además
       una terminal vacía: se cierra con `orca terminal close`), y en ese worktree una
       pestaña a la vista: `orca terminal create --worktree path:<ruta>
       --title "Programa Gemini #<ID>" --command "gemini -i 'Leé y seguí la
       misión de <archivo de misión>' --approval-mode
       <el del plan> --include-directories <ruta del repositorio del Cerebro>,<carpeta
       de la misión>" --json`. La misión (la del 6.1) va en un archivo fuera
       de los repos.
     - El orquestador lo sigue **leyendo esa terminal**, no por el inbox:
       `orca terminal wait --terminal <identificador> --for tui-idle
       --timeout-ms 60000 --json` y `orca terminal read --terminal
       <identificador> --json`, en segundo plano. La misión le pide cerrar
       con una línea `TAREA-TERMINADA` (o `TAREA-FALLIDA`) y su resumen, y
       escribir `PREGUNTA-ORQUESTADOR: …` cuando tiene una duda bloqueante;
       el orquestador la contesta con `orca terminal send --terminal
       <identificador> --text "<respuesta>" --enter --json`. Los marcadores
       se buscan **al principio de una línea**, y ante la duda se confirman
       con `orca terminal read --screen` (la consola sale en pedazos y la
       misión misma los menciona).
     - **Si la pestaña espera una aprobación** (con `auto_edit`, Gemini pide
       permiso en la pestaña para cada comando: commits, tests), el
       orquestador lo ve con `orca terminal read --screen` y **le avisa al
       humano en ese momento**, con la Tarea y el comando: la aprobación la
       da el humano en la pestaña, no el orquestador.
   - **Nunca** `orca worktree create` + `orchestration dispatch` para un
     worker de Claude: queda sin supervisión, su aviso de terminado no le
     llega a nadie y el flujo se pierde.

   ### 6.0 El orquestador queda atento (regla dura)

   Lanzada la tanda, el orquestador **no se va**: queda escuchando hasta
   que la última Tarea termine, y le avisa al humano de cada cosa que pasa.

   - **La espera está siempre corriendo**, en segundo plano: `orca
     orchestration check --wait --types "worker_done,escalation,question"
     --timeout-ms 900000 --json` para los workers de Claude, y la lectura de
     la terminal para los de Gemini. En Claude Code van como comandos en
     segundo plano, que despiertan al orquestador y siguen corriendo aunque
     esté esperando al humano.
   - **Cada mensaje se procesa al llegar**, se confirma (`check --ack
     <delivery_id> --wait …`) y se vuelve a esperar. Orca repite el mismo
     mensaje hasta el `--ack`, así que ninguno queda sin confirmar mientras
     se espera al humano: se anota y se sigue escuchando.
     - **Pregunta de un worker:** si es técnica y tiene una recomendación
       clara (un nombre interno, un mecanismo del framework, dónde va un
       archivo), la contesta el orquestador (`orca orchestration reply --id
       <message_id> --body "<respuesta>" --json`, o `terminal send` si es
       Gemini) y se la lista al humano para que la vete (fuente 5 de
       [[AGENTS]]). Si es un dato duro o una regla de negocio sin fuente,
       se le trae al humano **en ese momento** y su respuesta vuelve
       después. Ningún worker queda más de unos minutos sin respuesta sin
       que el humano lo sepa.
     - **Escalamiento o bloqueo:** se le avisa al humano en ese momento.
     - **Terminó una Tarea** (`worker_done` o `TAREA-TERMINADA`): **se le
       avisa al humano en ese momento** —*«Terminó la #NNNN: ‹resumen›.
       Arranco la verificación con ‹el verificador›.»*— y se sigue con el
       6.2. El worker de Claude se libera antes del `--ack` (`orca
       orchestration worker-release --dispatch <dispatch_id> --json`), y la
       pestaña de Gemini se cierra (`orca terminal close --terminal
       <identificador> --json`): el trabajo queda en el worktree.
     - **Falló** (`--outcome failed` o `TAREA-FALLIDA`): se avisa con lo
       que dijo el worker, no va a la verificación, el worktree queda
       intacto para que decida el humano, y se da el resumen del 6.3.
   - **Una espera vacía o vencida no es una falla**: es un punto de control.
     Después de tres seguidas, `orca orchestration worker-list --run
     <run_id> --json` y se actúa según `projection.attention` y
     `projection.nextAction`. Sin prueba positiva de que un worker se cortó,
     nunca se lo frena, abandona ni relanza.
   - **No se da por terminado** mientras quede una Tarea abierta: `worker-list
     --run <run_id> --json` sin filas `active`, `reclaimable` ni `retained`,
     ninguna pestaña de Gemini del lote abierta (`orca terminal list`), y
     cada Tarea con su resultado dicho al humano.

   ### 6.1 Misión que recibe cada worker

   **La arma `bin/armar-mision.py`** (`--rol worker --entorno orca --motor <claude|gemini>`), la
   misma plantilla que usa `references/sin-orca.md`: la Tarea **completa** pegada (el orquestador
   la lee del tablero y la guarda en un `.md` fuera de los repos, con el Gherkin de la Historia
   padre), el worktree y el SHA de base, `AGENTS.md`, el método (`tdd-ciclo-y-evidencia.md`,
   `crear-endpoint.md`, `contrato-openapi.md`, la guía del stack), las skills por ruta absoluta
   (`guiar-tdd` y, en back, `armar-swagger`; **no** `auditar-codigo`, que es del verificador), la
   arquitectura (`esqueleto-proyectos.md`, `decisiones.md`, `aplicacion/`), las convenciones C1 a
   C8 **copiadas del orquestador**, los límites (un módulo, sin PHI, sin push ni Merge Request ni
   tablero ni Cerebro; lo gris va como pendiente a confirmar, no se inventa), el modo de pruebas de
   la Tarea, el resultado esperado y el canal (Claude: `ask` y `worker_done`; Gemini: una línea
   `PREGUNTA-ORQUESTADOR: …` y `TAREA-TERMINADA` / `TAREA-FALLIDA`). Todo en español. El texto de
   la misión **no vive acá**: si hay que cambiarlo, se cambia el script y su prueba. La rama se
   crea con la convención real (`metodologia/convenciones-git.md`): `task/<ID>-<slug>`,
   `bugfix/<ID>-<slug>`, `hotfix/<ID>-<slug>`, antes del primer commit. **No se exige ni se corre
   [[auditar-tarea]]**: es opcional y sólo corre si alguien la pide.

   ### 6.2 Verificación: otro agente, en sólo lectura

   Quien programa no se aprueba a sí mismo: **verifica otro agente** (el otro
   motor si hay dos; si no, uno del mismo motor con contexto limpio, `DEC-005`), con
   contexto nuevo y en **sólo lectura**, sobre el **mismo worktree** de la
   Tarea. Así no se suman worktrees y entran 8 Tareas a la vez.

   - **Si programó Claude, verifica Gemini, en una pestaña de Orca** sobre
     el worktree de la Tarea: `orca terminal create --worktree
     path:<ruta> --title "Verifica Gemini #<ID>" --command "gemini -i 'Leé
     y seguí la misión de <archivo de misión>' --approval-mode plan --policy <ruta del repositorio del Cerebro>/bin/gemini-verificador-solo-lectura.toml
     --include-directories <ruta del repositorio del Cerebro>,<carpeta de la
     misión>" --json`. Comillas simples adentro: las dobles escapadas rompen
     el comando en PowerShell.
     - **La política es obligatoria.** El modo `plan` solo no alcanza: sin
       interacción pasa a modo automático, en la pestaña cualquiera puede
       cambiar de modo, y deja escribir `.md` sueltos. La política prohíbe
       cambiar de modo, escribir, guardar memoria, usar servidores MCP,
       encadenar comandos y publicar, y deja sólo git de lectura, los tests
       y Spectral. Si la pestaña dice `Policy file error`, Gemini corrió
       **sin** ella: se cierra y el veredicto es SIN DATOS.
     - El orquestador lee el veredicto con `orca terminal wait` y `orca
       terminal read` (siguiendo el `nextCursor`), hasta el bloque
       `VEREDICTO-INICIO` … `VEREDICTO-FIN`, con techo de 20 minutos: si no
       aparece, es SIN DATOS y se avisa. Al leer el veredicto, la pestaña se
       cierra (`orca terminal close`), siempre antes de la entrega.
   - **Si programó Gemini, verifica Claude**, como sub-agente de **sólo
     lectura** del orquestador (sin herramientas de edición ni escritura),
     con la misión del verificador y la ruta del worktree. No escribe, no
     commitea, no corre nada que modifique y no escribe por MCP. No se ve en
     una pestaña: el control es la foto de abajo.
   - **Foto antes y después:** `git -C <worktree> status --porcelain` y
     `git rev-parse HEAD` del worktree y del repositorio del Cerebro. Si el
     verificador dejó algo cambiado, se frena y decide el humano.
   - **La misión del verificador** la arma `bin/armar-mision.py` (`--rol verificador --entorno orca
     --motor <el otro>`): la Tarea completa con el Gherkin del padre (el verificador no lee el
     tablero), el worktree, la rama y el SHA de base, las skills por ruta absoluta (`verificar-tdd`,
     `code-review.md`, `auditar-codigo`), los comandos exactos de `verificar-tdd.py` (con el `--modo`
     de la Tarea) y `auditar-diff.py`, el control 5-quater con C1 a C8 (un veredicto por regla), el
     linter de OpenAPI con `bin/spectral-oas.yaml`, las dos clases de `SIN DATOS` y el bloque
     `VEREDICTO-INICIO … FIN`. Si el front no tiene dependencias instaladas, el **verificador** corre
     el comando de instalación del stack en su worktree antes de verificar (el orquestador coordina,
     no ejecuta).
   - **Cómo se sabe quién verificó:** la pestaña muestra `Gemini CLI
     v<versión>` y el modo `plan`; el comentario de cierre y el resumen lo
     registran como «‹motor› v‹versión› · ‹modelo›».
   - Sin verificador independiente no hay verificación: la Tarea no se despacha (paso
     4). Si falla a mitad de camino, el control queda **SIN DATOS**, y SIN
     DATOS no es aprobado.

   ### 6.3 Validación y entrega: un "Aprobar" por Tarea

   1. **Una sola pregunta por Tarea**, apenas está la verificación: *«¿Validás
      la #NNNN?»* (Aprobar / Ajustar). Lleva, para que el "Aprobar" cubra todo
      lo que se va a escribir:
      - el resumen del worker y la verificación (HALLAZGO y SIN DATOS: el
        humano los manda a ajustar o los acepta), y qué cambió del README;
      - los **pendientes a confirmar** de este desarrollo y los que ya había
        sin resolver en la tarjeta ([[comentar-tarea]] §«Antes de cerrar una
        Tarea»);
      - lo que va a pasar con el "Aprobar": subir el respaldo `evidencia/<ID>`
        a `origin`, reorganizar la rama **por importancia** (alrededor de 10
        commits, como guía), pushear la rama de la Tarea, y **el comentario de cierre tal como se va a ver**, con el link
        para abrir el Merge Request. Lo único que se completa después, y la
        pregunta lo dice, es el último commit y la cantidad de commits, que
        recién existen al reorganizar.
   2. **Ajustar:** una Tarea nueva para un worker nuevo, del mismo motor y
      **en el mismo worktree**, con lo que hay que cambiar (Claude:
      `task-create` + `worker-start --task <nuevo> --worktree path:<ruta>
      --agent claude --run <run_id> --json`; Gemini: se cierra la pestaña
      anterior, si quedó abierta, y se abre otra con la misión de ajuste).
      Antes de despachar rige la «Base al día» del paso 6, aunque el
      worktree ya exista. Vuelve a pasar por 6.2 y por esta pregunta.
   3. **Aprobar:** el orquestador hace, sin volver a preguntar:
      - la reorganización de la rama ([[orquestador-desarrollo]]
        §«Commits: de trabajo, y pocos en el Merge Request»): respaldo
        `evidencia/<ID>` subido a `origin`, commits por importancia (alrededor
        de 10), `git diff evidencia/<ID> HEAD` vacío;
      - el push de la rama de la Tarea;
      - el comentario de cierre en la tarjeta ([[comentar-tarea]]
        §«Comentario de cierre de desarrollo»), sólo el comentario (`System.History`
        en Azure; `bin/tablero-local.py comentar` en el tablero local), con
        el guard de [[tablero-autorizado]];
      - el link para abrir el Merge Request (antes, la «Base al día» del
        paso 6: si `develop` avanzó, se trae con merge y se re-verifica), que **abre el humano** (la IA no
        abre Merge Requests por cuenta propia: muestra el link):
        `https://<host-gitlab>/<grupo>/<proyecto>/-/merge_requests/new?merge_request%5Bsource_branch%5D=<rama>&merge_request%5Btarget_branch%5D=<base>`
        (`<grupo>/<proyecto>` sale de `git remote get-url origin`), con el
        título `feat: [AB#<ID>] <título en español>` y la descripción lista
        para pegar.
   4. **No se cambia el Estado.** Al tomarla, la tarjeta quedó congelada si
      está en un sprint, y una tarjeta congelada sólo se comenta
      ([[cambios-en-el-backlog]] §4). Pasarla a revisión o cerrarla lo
      decide una persona.
   5. **Resumen al humano, siempre**, al terminar cada Tarea —entregada,
      frenada o fallida—, con el molde de [[orquestador-desarrollo]]
      §«Resumen al terminar cada Tarea». Al terminar el lote, la tabla con
      todas.

7. **Bloqueadas.** No se disparan en esta corrida. Quedan listadas con su
   dependencia. Cuando el humano aprueba la tarjeta que las bloqueaba, el
   orquestador —que sigue atento— lo avisa y las vuelve a proponer por el
   paso 4 (aprobada no es mergeada: la base se pregunta de nuevo).

## Barreras

- **Los datos del GATE de WORKTREE los da `bin/gate-worktree.py`** (worktrees abiertos en la máquina,
  árbol sucio, rama ya con worktree, base atrás de `origin`) y los del cierre, `bin/datos-cierre.py`.
  La pregunta al humano se hace con esos números a la vista; un script que no corrió es `SIN DATOS`.

- **Dos modos, un flujo.** Con `ORCA_APP_VERSION` los workers van en pestañas de Orca;
  sin ella, en worktrees de git con `claude -p` / `gemini -p` (`references/sin-orca.md`,
  paso 0). Nunca un sub-agente interno **para programar**.
- **Gate de tablero.** Todo lo que lee/escribe se acota al tablero
  autorizado ([[tablero-autorizado]]); si el destino no coincide, no se
  escribe y se avisa.
- **No asumir dependencias ni repo destino.** Si el texto de la tarjeta no
  deja claro de qué depende, o el Area Path no permite inferir el repo, se
  pregunta — nunca se completa el hueco por cuenta propia.
- **Tres confirmaciones, ni una más:** el plan (paso 4), tomar la tarjeta
  (paso 5) y el "Aprobar" de cada Tarea (6.3), que cubre todo lo que se
  escribe después: reorganizar, pushear y el comentario de cierre.
- **Quien verifica no es quien programó** (`DEC-005`): el otro motor si hay dos; otro
  agente del mismo motor, con contexto limpio, si hay uno.
- **El orquestador queda atento (6.0)** hasta que la última Tarea termina,
  y avisa de cada una.
- **Fuera de pasarla a Active al tomarla (paso 5), el Estado de la tarjeta
  no lo cambia este flujo.**
- **Todo trabajo que escribe en un worktree va a la vista:** un worker
  supervisado de Orca, una pestaña, o un `claude -p` con su registro en
  `borrador/`. **Prohibido** usar un
  sub-agente interno para escribir en un worktree; los sub-agentes internos
  se usan **sólo** para leer: la verificación de Claude y auditorías.
- **Sin la verificación independiente no se pide el "Aprobar".** SIN
  DATOS no es aprobado: se declara, no se da por bueno.
- **Commits por importancia en el Merge Request** (alrededor de 10 por
  Tarea, como guía); los de TDD quedan en `evidencia/<ID>`, subida a
  `origin` sin Merge Request. Esa rama y la de la Tarea no se borran hasta
  terminar el sprint.
- **Siempre por `desarrollo`.** El método de desarrollo se aplica tal cual, al programar y
  al revisar.
- **Todo en español (Argentina)**, sin PHI, al grano.

## Contexto adicional

- La versión sin Orca (IntelliJ): `references/sin-orca.md`
- Tomar la tarjeta antes de codear: [[tomar-tarea]]
- Reglas que se chequean, commits y resumen por Tarea: [[orquestador-desarrollo]]
- Pendientes a confirmar y revisión antes de cerrar: [[comentar-tarea]]
- Auditoría de Tareas técnicas (opcional, a pedido): [[auditar-tarea]]
- Método de desarrollo y revisión (punto de entrada único al código): [[desarrollo]]
- Consultas de solo lectura al board: [[consultar-backlog]]
- Tablero único autorizado: [[tablero-autorizado]]
- Setup del MCP de Azure DevOps: `integracion-azure-mcp/00-index`
- Política de sólo lectura del verificador Gemini:
  `bin/gemini-verificador-solo-lectura.toml`
- Convención de ramas, commits y MR (obligatoria antes de commitear):
  `metodologia/convenciones-git.md`
- Arquitectura y stack por capa, y convenciones del back:
  `arquitectura/esqueleto-proyectos.md`, `arquitectura/decisiones.md`,
  `arquitectura/frontend/index.md`
