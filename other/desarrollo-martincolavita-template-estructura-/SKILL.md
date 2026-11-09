---
name: desarrollo
description: >-
  Punto de entrada ÚNICO para escribir, revisar o migrar código del proyecto —back, front, base
  de datos, seguridad, entrega—. Trae el método propio completo: TDD con evidencia del rojo,
  endpoints con el contrato primero, simular la API, armar la suite, depurar, refactor,
  revisión por dimensiones, accesibilidad, observabilidad, migraciones, dependencias y
  secretos, Merge Request y entrega. Lo específico del stack vive en
  references/metodo/tdd-stack-back.md y tdd-stack-front.md (DEC-003). Guardarraíles: el código
  y el conocimiento no se mezclan, nada sale del repositorio sin un "sí", el lenguaje lo pone
  el repositorio; lo que no se puede verificar es SIN DATOS, que no es aprobado. Usar cuando se
  pida "programá esto", "hacé el endpoint", "escribí los tests", "revisá el código", "arreglá
  este bug", "por qué falla", "revisá la seguridad", "migrá la base", "preparemos la entrega",
  "/desarrollo". Español (Argentina).
---

# Desarrollo — el método propio del proyecto

Esta skill es **la puerta** a todo lo que es código. No escribe la solución por vos: fija **cómo**
se escribe, qué cuenta como evidencia, quién verifica y qué frena la entrega. Lo que una Tarea
del tablero define (**qué** hay que hacer: contrato, Escenarios, tests a escribir primero) manda
antes; recién después entra esto.

## La idea, en tres frases

1. **El contrato primero, el test después, el código al final.** Así el front y el back trabajan
   en paralelo y el test tiene algo concreto que verificar.
2. **Un ciclo que no deja evidencia no ocurrió.** El rojo tiene que haber fallado **en su
   aserción**, antes del código, y lo verifica **otro agente**.
3. **Tres estados, nunca dos.** OK / HALLAZGO / **SIN DATOS**, y SIN DATOS no es aprobado.

**Todos los comandos de esta skill se corren parados en la raíz del repositorio del Cerebro.**
Las rutas son relativas a ella.

---

## REGLA DE ORO: punto de entrada único

**Ninguna guía de desarrollo —propia o de terceros— se aplica sin pasar por acá.** No es
burocracia: una guía ajena aplicada suelta puede imponer una estructura de paquetes por capa
técnica que **rompe los límites de módulo** del proyecto ([[decisiones#DEC-002]]), y eso se
descubre recién cuando el código ya está escrito.

Si una sesión aplicó otra guía sin pasar por acá, **eso es un hallazgo**: se avisa y se revisa lo
que produjo contra la tabla de precedencia.

### Si la organización tiene un estándar corporativo

Se **envuelve**, no se copia ni se instala: se lee del servidor en el momento de usarlo (por el
MCP del repositorio que lo publica), se le aplica encima la **tabla de precedencia** de abajo, y
se descarta. Queda declarado en `DEPENDENCIAS-EXTERNAS.md` con el hash de árbol contra el que se
lo revisó. **Sin acceso al servidor el veredicto es `SIN DATOS`**: no se improvisa lo que el
estándar diría, porque eso es inventar un estándar ajeno.

---

## El método — organizado por cuándo lo vas a usar

### Todos los días

| Tema | Archivo |
|---|---|
| **Crear un endpoint** de punta a punta: contrato → tests → código → checklist | [crear-endpoint.md](references/metodo/crear-endpoint.md) |
| El ciclo rojo-verde y **qué cuenta como evidencia del rojo** | [tdd-ciclo-y-evidencia.md](references/metodo/tdd-ciclo-y-evidencia.md) |
| **Arreglar un bug** — el ciclo, y los tres tipos que no se parecen | [arreglar-un-bug.md](references/metodo/arreglar-un-bug.md) |
| **Depurar** — causa vs. síntoma, `trace_id`, qué nunca va en un log | [depurar.md](references/metodo/depurar.md) |
| **Refactor** y deuda técnica — la fase 3, y qué no se refactoriza | [refactor.md](references/metodo/refactor.md) |
| Revisión de código **por 5 dimensiones**, con severidad | [code-review.md](references/metodo/code-review.md) |
| **El Merge Request**: tamaño, descripción, checklist, quién revisa | [merge-request.md](references/metodo/merge-request.md) |
| Ramas, commits y espacios de trabajo | [ramas-y-commits.md](references/metodo/ramas-y-commits.md) |

### Según el stack (⚠ se completan al decidir `DEC-003`)

| Tema | Archivo |
|---|---|
| Back: dónde va cada cosa, cómo se ve un rojo válido en el runner, comandos | [tdd-stack-back.md](references/metodo/tdd-stack-back.md) |
| Front: idem, más la simulación de la API | [tdd-stack-front.md](references/metodo/tdd-stack-front.md) |
| **Simular la API en el front** desde el contrato | [simular-api-desde-el-contrato.md](references/metodo/simular-api-desde-el-contrato.md) |
| **Accesibilidad** — los 4 chequeos que cubren casi todo | [accesibilidad.md](references/metodo/accesibilidad.md) |

### Tests

| Tema | Archivo |
|---|---|
| Qué prueba un test unitario, y qué no | [tests-unitarios.md](references/metodo/tests-unitarios.md) |
| **Armar la suite**: 7 categorías, **mutación**, propiedades, tests inestables | [armar-la-suite.md](references/metodo/armar-la-suite.md) |
| **Pruebas de aceptación**: la capa que prueba el sistema desplegado contra los Escenarios de la Historia; qué expone el front; cuándo corre | [pruebas-de-aceptacion.md](references/metodo/pruebas-de-aceptacion.md) |

### Por hito

| Tema | Archivo |
|---|---|
| **Arrancar una funcionalidad** completa: back y front en paralelo | [arrancar-funcionalidad.md](references/metodo/arrancar-funcionalidad.md) |
| El **contrato OpenAPI** como fuente | [contrato-openapi.md](references/metodo/contrato-openapi.md) |
| **Seguridad y datos sensibles** — SAST, PHI, los controles que aplican | [seguridad-y-datos-sensibles.md](references/metodo/seguridad-y-datos-sensibles.md) |
| **Dependencias, configuración y secretos** | [dependencias-y-config.md](references/metodo/dependencias-y-config.md) |
| **Observabilidad** — las 4 señales, logs, alertas, chequeos de salud | [observabilidad.md](references/metodo/observabilidad.md) |
| **Cambiar el esquema de la base** sin romper: expandir/migrar/contraer | [migracion-de-base.md](references/metodo/migracion-de-base.md) |
| **Entregar** — qué tiene que exigir el pipeline, y volver atrás | [entregar-a-produccion.md](references/metodo/entregar-a-produccion.md) |
| **Refactor o migración** de una aplicación existente: red primero, caracterización, paridad, estrangulador | [refactor-y-migracion.md](references/metodo/refactor-y-migracion.md) |
| Ingeniería inversa de una aplicación existente | [ingenieria-inversa.md](references/metodo/ingenieria-inversa.md) |
| Adoptar un proyecto que ya trabaja con IA (su `CLAUDE.md`, skills, MCP) sin tirar nada ni quemar tokens | [adoptar-proyecto-existente.md](references/metodo/adoptar-proyecto-existente.md) |

### Cuando hace falta

| Tema | Archivo |
|---|---|
| **Rendimiento** — no se optimiza sin medir. Los 4 sospechosos | [rendimiento.md](references/metodo/rendimiento.md) |
| **Incidentes** en producción — contener antes de entender | [incidentes.md](references/metodo/incidentes.md) |
| **Entender código ajeno** — y el arranque de alguien nuevo | [entender-codigo-ajeno.md](references/metodo/entender-codigo-ajeno.md) |

Bibliografía (ideas tomadas con atribución, nunca texto): [referencias-externas.md](references/referencias-externas.md).

---

## Los seis guardarraíles

### G1 — El código y el conocimiento no se mezclan

Un pedido de **código** activa esta skill y las de verificación de los repos. **No** activa las
del Cerebro ni las del pipeline de Azure. Y al revés: redactar una Tarea, auditar una Historia o
bajar una ficha al tablero **no** activa esta skill.

El cruce a evitar es concreto: una sesión de código que se pone a escribir fichas de negocio, o
una sesión de tickets que se pone a generar código.

**Zona gris declarada:** el momento en que una Tarea se vuelve código. Ahí mandan las dos, en
este orden: la Tarea define **qué** hay que hacer (contrato, tests a escribir primero), y recién
después esta skill define **cómo** se escribe. Nunca simultáneo.

### Las skills que viven en los repositorios de código

Esta skill es el **método**; la **ejecución** dentro del código la hacen las skills de `back/` y
`front/`, que actúan dentro del repositorio clonado:

| Skill | Dónde vive | Qué hace | Relación con ésta |
|---|---|---|---|
| `guiar-tdd` | `back/` y `front/` | Conduce el ciclo rojo-verde **mientras se programa** | Aplica [tdd-ciclo-y-evidencia.md](references/metodo/tdd-ciclo-y-evidencia.md) |
| `verificar-tdd` | `back/` y `front/` | **Audita la evidencia** — la corre otro agente | Es el paso 5 del ciclo por Tarea. **No puede vivir acá**: quien produce nunca aprueba |
| `auditar-codigo` | `back/` y `front/` | **¿La entrega cumple lo que el pipeline exige?** Contrato de la Tarea, límites del módulo, tests cubiertos, sin PHI ni secretos | Distinta de [code-review.md](references/metodo/code-review.md), que mira si el código está bien escrito |
| `armar-swagger` | **sólo `back/`** | Consolida y valida el `openapi.yaml` | Es el paso obligatorio de [contrato-openapi.md](references/metodo/contrato-openapi.md) |
| `diagnosticar-repo` | `back/` y `front/` | Corre el Doctor sobre el repositorio clonado | Independiente |
| `consultar-cerebro` | `back/` y `front/` | Lectura del Cerebro, una ficha por vez | Independiente |

**El reparto, en una línea: acá está el MÉTODO; allá está la EJECUCIÓN dentro del código.**

- **`verificar-tdd` y `auditar-codigo` están afuera a propósito.** Si vivieran acá, el mismo
  agente que produjo leería la guía de cómo auditarse — y se pierde la independencia, que es la
  regla más fuerte del método.
- **`armar-swagger` sólo existe en `back/`.** En el front, ese ítem se verifica contra el contrato
  que consolidó el back.

> **Ojo con los conteos.** Cuando el proyecto cuenta sus skills (el número vive en `AGENTS.md` y lo
> verifica el hook), habla de las de
> `cerebro-digital/configuracion-ia/skills/`. Las de `back/` y `front/` **no entran en ese
> número**, pero **sí se versionan y sí las verifica el hook**: compara el par `.claude/skills`
> contra `.agents/skills` de cada uno y frena el commit si difieren.

### G2 — Punto de entrada único

Ya dicho arriba. Se repite acá porque sostiene a los otros cinco: si alguien entra por la puerta
de atrás, ninguna corrección se aplica.

### G3 — La precedencia está escrita, no se deduce

Cuando una guía externa y este proyecto dicen cosas distintas, **no se resuelve por criterio del
modelo**: se resuelve por la tabla de abajo. Lo que no esté en la tabla y choque, **se frena y se
pregunta**, no se elige. **Una fila de la tabla puede decir "se pregunta"**: estar en la tabla no
significa estar resuelto; significa que ya se miró.

### G4 — Nada sale del repositorio

**Nada sale de este repositorio hacia afuera sin un "sí" explícito sobre lo que se va a
publicar.** Publicar en un repositorio ajeno (una propuesta de mejora a un estándar corporativo,
un issue, un Merge Request) es un turno aparte: primero se muestra el contenido exacto y se
termina el turno; recién un "sí" nuevo habilita escribir afuera. Y si el token disponible es de
sólo lectura, directamente no está en el alcance.

### G5 — Lo externo se declara, con hash y detector de deriva

**Sólo aplica si el proyecto envuelve un estándar externo**; el template no trae el detector: se agrega
junto con la primera dependencia declarada, como dice `DEPENDENCIAS-EXTERNAS.md`. Si el proyecto sigue
skills de terceros, se declaran en `DEPENDENCIAS-EXTERNAS.md` con el hash
de árbol de cada una. **Importa más con el mecanismo de "leer del servidor", no menos:** como el
contenido se lee siempre actualizado, lo que puede quedar viejo son **nuestras correcciones**. Un
detector de deriva (comparar los hashes de hoy contra el ancla declarada) se corre una vez por
mes y devuelve **OK / HALLAZGO / SIN DATOS**; `SIN DATOS` no es OK. El ancla vive en el
manifiesto y en el script que compara: actualizarla es actualizar los dos.

### G6 — El lenguaje lo pone el repositorio

En los repos de la aplicación se escribe en el lenguaje y con las herramientas que el repo ya
usa (los que fija `DEC-003` y documentan `tdd-stack-back.md` / `tdd-stack-front.md`). Eso incluye
los tests de lo que no es la app (el pipeline, scripts, configuración): van al runner de tests del
repo, no a uno aparte.

- **Permitido sin preguntar:** `sh` adentro de un job del pipeline y el `Dockerfile`, porque es
  lo que trae la imagen.
- **Si con el lenguaje del repo se puede, se hace así.** Si otro lenguaje tenía ventajas, se
  anota en el Merge Request qué ganaría y qué sumaría, sin escribirlo.
- **Si con el lenguaje del repo no se puede, se frena y se pregunta antes de escribir una
  línea:** por qué no se puede, qué lenguaje se propone y qué agrega (herramienta a instalar,
  dependencias, jobs del template que se activan).

No aplica al repositorio del Cerebro: ahí `bin/` es Python a propósito.

> **Por qué.** En el proyecto de origen de este template entraron dos scripts en otro lenguaje
> para probar el pipeline: sumaron un requisito más, activaron un job del template que falló y
> quedaron fuera del runner de tests, así que no protegían nada.

---

## Tabla de precedencia

⚠ **A completar por el equipo** si la organización publica un estándar corporativo. Mientras no
haya estándar externo, gana el proyecto en todo y la tabla queda como molde. Los temas que casi
siempre chocan:

| Tema | El estándar externo dice | Nosotros decimos | Gana |
|---|---|---|---|
| Estructura de paquetes del back | <completar> | **Paquete por módulo de dominio** con 4 capas + `exceptions/` + `shared/` ([[decisiones#DEC-002]]); entre módulos sólo por la `application` del otro | **NOSOTROS** (salvo que el equipo cambie DEC-002) |
| Framework y estructura del front | <completar> | Lo que fije `DEC-003` | ⚠ a decidir |
| Test primero | <completar> | Lo mismo, **más evidencia**: el test tiene que haber fallado **en su aserción**, y lo verifica un agente distinto del que escribió el código | **LOS DOS** (el nuestro es más exigente) |
| Publicar en el repositorio del estándar | <completar> | Nada sale sin un "sí" explícito (G4) | **NOSOTROS** |
| Extensiones/librerías obligatorias, registry interno, dependencias aprobadas, autenticación y roles | <completar> | Si la organización lo define, se toma tal cual | **EL ESTÁNDAR** (si existe) |
| **Design tokens** | <completar> | Design system propio (`diseno/diseno-sistema.md` y `cerebro-mockup-design`); nunca hexadecimales a mano | ⚠ **se pregunta** si hay dos paletas |
| Cobertura mínima | <completar> | ⚠ umbral a definir por el equipo (`DEC-003`) | ⚠ a decidir |

---

## Lo que este método exige y una guía genérica no

| Agregado | Por qué |
|---|---|
| **Evidencia** del rojo antes del verde | Mandar «escribí el test primero» sin pedir prueba no cambia nada: un test escrito después cumple la letra |
| **Verificador distinto del productor** | Si el mismo agente codea y se aprueba, no hay control: hay una declaración |
| **Veredicto de tres estados** | Sin `SIN DATOS`, "no encontré nada" y "no pude mirar" se confunden, y el segundo pasa por aprobado |
| **Regla del cero** | Cero hallazgos sobre entrada externa no es aprobado: es no auditable |
| **Límites de módulo** ([[decisiones#DEC-002]]) | Sin esto, el código generado rompe la arquitectura del proyecto |
| **PHI prohibido con marcadores** | En código, tests, fixtures, logs, contrato y descripción del Merge Request |

---

## Barreras

- **Lo que no esté en la tabla de precedencia y choque, se pregunta.** No se elige.
- **Si no se puede leer una fuente externa, se reporta `SIN DATOS` y se dice qué falta** (red,
  token). No se improvisa lo que esa fuente diría. Todo `metodo/` funciona igual: es propio y no
  depende de nada.
- **Nunca se pega contenido de terceros dentro de este repositorio.** Se lee, se usa, se descarta
  (G5). Las citas mínimas con atribución van en `references/referencias-externas.md`.
- **Los comentarios del código, en español** (back y front). Se comenta poco —el código se explica
  por sus nombres, donde sólo los sustantivos del negocio que están en la base van en español y
  los verbos, roles técnicos y técnica en inglés (`arquitectura/esqueleto-proyectos.md`)—, pero el
  comentario que hace falta se escribe en español, igual que la documentación y los mensajes de
  commit.
- **Sin PHI** en nada que se versione o se publique. Marcadores: `<persona>`, `<documento>`,
  `<identificador>`, `<telefono>`, `<direccion>`, `<dato-sensible>`.
