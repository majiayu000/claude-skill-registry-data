---
name: caracterizar-comportamiento
description: >-
  Ponerle una RED a una aplicación existente antes de tocarla: armar el corpus de casos de un
  slice desde la radiografía (bin/armar-corpus.py), completarlo con una persona con datos de
  prueba y marcadores, grabarlo contra la aplicación vieja con bin/paridad.py (el golden, firmado
  por el script) y, si es refactor, dejar también los tests de caracterización en el repositorio
  con el commit test(caracterizacion). Es la fase «primero la red» que refactor-y-migracion.md
  exige, y la que después usa modernizar-slice para probar paridad. Usar cuando se pida "ponele
  una red a este módulo", "grabá cómo responde hoy", "armá el corpus de paridad", "test de
  caracterización", "/caracterizar-comportamiento". No cambia comportamiento ni toca la app
  vieja; nunca graba datos de personas. Español (Argentina).
---

# Caracterizar el comportamiento de lo que ya existe

**Un test de caracterización no valida: congela.** Captura lo que la aplicación hace hoy, esté bien o
mal, para que cualquier cambio que lo altere se note. Es la única red posible cuando el código ya está
escrito, y por eso [refactor-y-migracion.md](../../skills/desarrollo/references/metodo/refactor-y-migracion.md)
dice «sin red no se refactoriza ni se migra: `SIN DATOS`».

Dos formas, que se eligen por lo que la aplicación expone:

| Forma | Cuándo | Herramienta | Qué produce |
|---|---|---|---|
| **Corpus + golden** (caja negra) | La app expone HTTP, un comando o algo observable desde afuera | `bin/armar-corpus.py` + `bin/paridad.py grabar` | `borrador/paridad/<slice>/corpus.json` y `golden.json` firmado |
| **Tests de caracterización en el repo** (caja blanca) | Refactor en el lugar: hay que proteger funciones y clases que no se ven desde afuera | El stack de tests del repo, guiados por esta skill | commits `test(caracterizacion): <qué congela>` |

Para una migración alcanza la primera; para un refactor suelen hacer falta las dos.

## Lo que NO hace

- **No toca la aplicación vieja.** Grabar es leerla corriendo; nada más.
- **No inventa casos ni valores.** El esqueleto sale de la radiografía (cada caso con `archivo:línea`); lo
  que el script dejó `<completar>` lo completa una persona con **datos de prueba sembrados**, nunca con
  datos reales. `bin/paridad.py` avisa si una respuesta grabada parece traer un correo o un documento.
- **No corre casos que mutan** (POST/PUT/DELETE, comandos que escriben) sin un "sí" explícito y datos
  recién sembrados (`--permitir-mutaciones`).
- **No escribe el golden a mano, ni lo escribe un modelo.** Lo graba el script y lo firma; un golden editado
  no verifica y vale `SIN DATOS`.
- **No arregla lo que encuentra.** Un comportamiento raro se anota como regla candidata y va a la
  curaduría de [[planificar-modernizacion]].

## Pasos

1. **Qué slice y contra qué oráculo.** En criollo: qué módulo, dónde corre la aplicación vieja (URL local
   o comando), con qué datos de prueba, y si hay casos que mutan. Si la vieja no corre en esta máquina,
   `SIN DATOS`: no se graba contra producción ni contra un host remoto sin un "sí" y `--permitir-remoto`.
2. **Esqueleto del corpus.**
   ```bash
   python bin/armar-corpus.py borrador/absorcion/<fecha>/01b-radiografia.json --slice <modulo>
   ```
   Un caso `CP-nn` por endpoint y un borde por cada regla candidata `RC-nn` de la radiografía (umbral, condición que
   frena, cambio de estado, validación declarativa, función de cálculo).
3. **Completar con una persona.** Ítem por ítem: ids de prueba, cuerpos con marcadores (`<persona>`,
   `<documento>`), el valor exacto en el borde (30 y 31 si la regla dice «hasta 30»), y qué regla cubre
   cada caso (`regla`). Se agregan casos de **error** (lo que la vieja contesta cuando se le pide mal): son
   los que más diferencias muestran después. Se borra lo que no aplica. Cada caso cita su `archivo:línea`. Al
   terminar, `python bin/armar-corpus.py <radiografia.json> --slice <modulo> --verificar <corpus.json>` dice qué endpoint o
   regla quedó sin caso y cuántos `<completar>` faltan.
4. **Grabar.**
   ```bash
   python bin/paridad.py grabar --corpus borrador/paridad/<slice>/corpus.json --oraculo http://127.0.0.1:<puerto> --salida borrador/paridad/<slice>/golden.json
   python bin/paridad.py verificar --golden borrador/paridad/<slice>/golden.json --corpus borrador/paridad/<slice>/corpus.json
   ```
   El golden lleva la firma y el hash del corpus: si el corpus cambia, se vuelve a grabar. Corpus y golden
   se **versionan** (sin PHI) en el repositorio del Cerebro bajo `cerebro-digital/<modulo>/aplicacion/paridad/<slice>/`
   cuando una persona los da por buenos; `borrador/` es el lugar de trabajo.
5. **Si es refactor, los tests en el repo.** Por cada función o clase que la radiografía señaló con reglas,
   un test que fija la salida actual para entradas representativas (incluidos los bordes y los errores),
   escrito con el stack de tests del repositorio y **sin tocar código de producción**. Commit
   `test(caracterizacion): <qué congela>` **antes** de cualquier otro (o un `test(rojo)` si lo primero ya es un cambio
   de regla decidido): `bin/verificar-tdd.py --modo caracterizacion`
   lo exige en ese orden.
6. **Cerrar.** La fila del slice en `aplicacion/modernizacion.md` pasa a `red` (con `cerebro-curator`, con el
   "sí"), citando corpus y golden. Lo raro que apareció va como `RC-nn` a la curaduría.

## Barreras

- **Sin la radiografía no hay esqueleto**: `SIN DATOS`, no un corpus de memoria.
- **Un caso con `<completar>` no se graba.** El script lo cuenta; la persona lo cierra o lo borra.
- **Nunca PHI** en corpus, golden ni tests: si los datos de prueba de la vieja tienen datos reales, primero
  se siembran datos de mentira, después se graba.
- **Los tests de caracterización no se tocan después** durante el refactor ([refactor.md](../../skills/desarrollo/references/metodo/refactor.md)); si uno se pone en rojo, el cambio alteró algo.
- Todo en español (Argentina).

## Cómo entra en el veredicto

| Estado | Cuándo |
|---|---|
| **OK** | Corpus sin `<completar>`, golden que verifica, cada endpoint y cada regla del slice con al menos un caso (lo cuenta `bin/armar-corpus.py --verificar <corpus.json>`), y (en refactor) `test(caracterizacion)` antes de tocar producción |
| **HALLAZGO** | Un endpoint o regla del slice sin caso, un caso que muta grabado sin "sí", datos de personas en el golden |
| **SIN DATOS** | La vieja no corrió, el golden no verifica o la radiografía no está |
