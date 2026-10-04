---
name: adherencia-reglas
description: >
  Mide qué fracción de las reglas propias del proyecto se cumple de verdad, contándolo sobre el
  historial de sesiones que Claude Code ya guarda en disco. Se activa al preguntar si una norma,
  protocolo o convención se está aplicando, al revisar si un CLAUDE.md sirve de algo, al decidir si
  una regla debe pasar a ser hook, o al cerrar una jornada para ver la adherencia del día. Trae su
  propio instrumento determinista, sin modelo de lenguaje de por medio. NO juzga si la regla es
  buena ni si el trabajo estuvo bien hecho: cuenta ocasiones y respuestas.
license: MIT
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/medir_adherencia.py *)
compatibility: >
  Solo Claude Code. Lee los transcripts JSONL locales de ~/.claude/projects/, cuyo formato la
  documentación de Anthropic declara interno y sujeto a cambios entre versiones. Probada contra
  Claude Code 2.x en julio de 2026. Python 3.9+, biblioteca estándar, sin red. Solo lectura.
metadata:
  version: "1.1"
  validated_with: claude-opus-5
  validation_date: "2026-07-27"
---

# adherencia-reglas: el espejo de las normas propias

> **Principio rector.** Una regla escrita y no medida es una intención. Este proyecto lleva meses
> acumulando normas en CLAUDE.md, en skills y en protocolos. El 25/07/2026 contó por primera vez
> cuántas se cumplían. La que ordena pasar la puerta de salida antes de publicar un texto, con hook
> propio y skill dueña, se cumplía en **103 de 132 ocasiones (78,0 %)**, medida el 27/07/2026 con ventana de 6 pasos,
> ámbito declarado y desde su fecha de alta. Sale de un historial privado: lo reproducible es el
> ejemplo que trae el paquete.
>
> Esa cifra empezó el día siendo 24 %, pasó por 26 %, 38 % y 63 % y acabó en el 78,0 % de arriba.
> Aquí ponía «acabó en 80 %», que no cuadraba con las 103 de 132 de dos líneas antes: ese 80 era el
> resto de una cifra de la mitad inglesa, 72 de 90, que ya se había corregido en su sitio y se quedó
> viva aquí. Es exactamente el defecto que este documento describe, dentro del propio documento. No
> lo cazó ningún gate porque todos comprueban que un texto cuadre con el código, no que cuadre
> **consigo mismo**. Lo encontró una simulación ciega leyendo las dos frases seguidas.
>
> **Ninguna de las anteriores estaba mal calculada.** Cada una medía un objeto distinto: todos los
> ficheros o solo los que van dirigidos a alguien; desde siempre o desde el alta de la regla;
> datando las sesiones por la fecha del fichero o por la que traen dentro. Medir una regla obliga a
> definirla, y definirla es donde está el trabajo.

## Qué mide y qué no

**Mide adherencia**, que es con qué frecuencia una acción sigue a su disparador sin que nadie lo
recuerde en ese momento.

**No mide incumplimiento.** Una regla puede no aplicar a todos sus disparadores: la puerta de salida
no se le pasa a un borrador interno de trabajo. Leer la tasa como culpa es el error más fácil.

**No juzga la regla.** Un 20 % puede significar una regla ignorada o puede significar una regla mal
escrita. Esa lectura es de quien lee.

## Cómo se usa

```
python ${CLAUDE_SKILL_DIR}/medir_adherencia.py
```

Sin argumentos mide la conversación principal de todos los proyectos. Para acotar a uno:

```
python ${CLAUDE_SKILL_DIR}/medir_adherencia.py --sesiones "~/.claude/projects/MI-PROYECTO"
```

`${CLAUDE_SKILL_DIR}` es el directorio donde vive este `SKILL.md` y Claude Code lo sustituye antes
de ejecutar nada. **Aquí ponía la ruta escrita a mano, `~/.claude/skills/adherencia-reglas/`.** Esa
ruta solo existe si la skill se copia a mano: instalada desde el marketplace de plugins el fichero
vive en otro sitio y el comando fallaba, o sea que la vía de instalación principal estaba rota.
Cazado el 27/07/2026 contra la documentación oficial. La sustitución en `allowed-tools` necesita
Claude Code 2.1.129 o posterior; en versiones anteriores el comando funciona igual y solo pide
permiso una vez.

El nombre de la carpeta lo pone Claude Code a partir de la ruta de trabajo, así que se mira con
`ls ~/.claude/projects`.

| Opción | Para qué |
|---|---|
| `--sesiones RUTA` | qué historial se mide. Vale un proyecto o la raíz que los contiene |
| `--reglas FICHERO` | qué reglas se miden. Por defecto, el `reglas.json` de al lado |
| `--acciones` | qué acciones aparecen en tu historial y con qué rutas. **Por aquí se empieza** |
| `--por-dia N` | desglosa los últimos N días **con sesiones**, que no son siempre los N del calendario |
| `--curva-ventana` | cómo cambia la tasa según el plazo de respuesta |
| `--sensibilidad` | cuánto mueve la cifra **cada** decisión arbitraria, no solo la ventana |
| `--subagentes` | incluye las sesiones de subagentes, que son otro universo |
| `--sin-colapsar` | cuenta cada escritura en vez de cada racha |
| `--respuesta-en-ambito` | exige que la respuesta caiga en el MISMO ámbito que el disparador |
| `--json` | salida para encadenar con otra cosa |

**Las dos vistas que no conviene saltarse.** Una tasa global miente por omisión en dos direcciones.
`--curva-ventana` enseña que el plazo elegido mueve la cifra treinta y tres puntos, del 49,7 % con
ventana 2 al 83,0 % con ventana 40 sobre los mismos datos. Y `--por-dia` enseña lo que el promedio
tapa: la puerta de salida se cumplió el **91 %** el 22 de julio, que es el día en que se cableó,
sobre 76 ocasiones, y el **25 %** al día siguiente sobre solo 4. Ese 25 % no es una caída medida: el
instrumento le pone un asterisco justo por eso, porque cuatro ocasiones no son una tasa.

**`--sensibilidad` existe por un hallazgo incómodo.** La opción `--curva-ventana` se escribió porque
alguien se quejó de ese parámetro en concreto. Una auditoría que miraba el razonamiento de la
jornada en lugar de sus defectos hizo la pregunta general: **qué otros números de esta herramienta son un umbral
elegido a ojo y publicado sin su sensibilidad**. Había dos más, el colapso de rachas y la muestra
mínima. Ninguna de las cuatro rondas de revisión los tocó, porque cada ronda reaccionó a una queja
concreta y nadie generalizó. La vista los enseña **los cuatro** a la vez, contando el de si la
respuesta tiene que caer en el mismo ámbito, que el propio bloque llama el supuesto más grande del
instrumento. Aquí ponía «los tres», heredado de cuando ese cuarto se numeró «2-bis» para no tocar la
cuenta. Un caso del banco falla si alguien añade un parámetro nuevo sin meterlo aquí.

El colapso no es cosmético: sobre el historial de este proyecto, una regla pasa del 57,1 % al 20,0 %
según se cuente una racha de escrituras como una ocasión o como varias.

Salidas: `0` todas las reglas por encima de su umbral, `1` alguna por debajo, `2` no se pudo medir.

**Falla ruidosamente ante una configuración mala**, porque los tres casos siguientes pasaban callando
y daban resultados sin sentido: un `ambito` escrito como texto en vez de lista (se recorre por
caracteres y filtra al azar), una ventana de cero o negativa y dos reglas con el mismo identificador.

## Las reglas se declaran fuera del código

En `reglas.json`. Cada una necesita qué situación la dispara, qué respuesta exige, en cuántos pasos
vale esa respuesta y **desde cuándo existe la regla**.

| Campo | Para qué | Si se omite |
|---|---|---|
| `disparador` · `respuesta` | las dos acciones que forman la obligación | falla |
| `desde` | fecha de alta de la regla | se juzgan meses sin regla |
| `ventana` | en cuántos pasos vale la respuesta | 6 |
| `direccion` | `antes` o `despues` | `despues` |
| `ambito` | zonas donde la regla aplica de verdad | mide una regla más ancha que la escrita |
| `umbral` | por debajo de qué tasa sale con código 1 | no juzga |

**`direccion` importa más de lo que parece.** Muchas obligaciones son «haz X antes de Y»: escanear
los repositorios antes de publicar, abrir el documento antes de actuar. Medidas hacia adelante salen
hundidas. La del escáner daba 7,7 % planteada al revés y 36,4 % bien. Ese último campo no es
decoración: sin él se juzgan meses en los que la norma no existía y sale una cifra bien calculada
sobre el objeto equivocado. La primera medición del proyecto dio 8,4 % sin acotar y 24,1 % acotando.

El campo `umbral` es opcional a propósito. Un umbral puesto a ojo es peor que ninguno, porque crea
una diana que nadie ha justificado.

## Qué hacer con el número

| Tasa | Lectura | Acción |
|---|---|---|
| alta y estable | ya es un hábito | la regla escrita sobra y ocupa sitio |
| a medias | se recuerda a veces | es la que más gana con un recordatorio o un hook |
| muy baja | escribirla no funciona | convertirla en mecanismo o retirarla |
| `n/d` | no hubo disparadores | no se pudo mirar, que no es un cero |

## Dos límites que hay que decir antes de enseñar la tabla

**Hay reglas que este instrumento no puede medir bien.** Conviene tenerlas identificadas en vez de
fingir que la tabla las cubre. La norma «antes de decir que algo no existe, búscalo» tiene como
disparador real una intención mía, que no deja ninguna llamada a herramienta. Aproximarla por
«escribir un documento» produce un denominador enorme y una tasa hundida que no significa nada.
El `reglas.json` de ejemplo no la trae, precisamente porque no se puede medir bien: lleva tres
reglas corrientes y una de ellas, `commit-por-unidad-cerrada`, con su aviso encima por ser de
esta misma familia. Si declaras una así, ponle el aviso tú.

**Una línea del historial no es una llamada.** El formato agrupa los trozos de streaming por
identificador de mensaje, así que la misma llamada aparece varias veces. El instrumento deduplica.
Sin eso, el recuento se infla un 58 % de forma desigual, o sea que deforma cualquier curva. Es
el fallo que tenía dentro el observatorio de degradación de este mismo proyecto, donde llegaba al
288 %. No daba ningún síntoma: los números salían mal en silencio.

## Las reglas cuyo disparador no deja rastro las mide otro instrumento

Este contador solo ve llamadas a herramientas. Una regla como «antes de decir que algo no existe,
búscalo» tiene como disparador una **intención**. Una intención no deja huella hasta que se
escribe. Aproximarla por «escribir un documento» produce un denominador enorme y una tasa hundida que
no significa nada. Por eso el ejemplo que viene en el paquete no la incluye.

Para esa familia de reglas hay otra vía que esta herramienta no cubre: si la regla tiene un hook
que la bloquea, el bloqueo queda escrito en el transcript y se puede contar por separado. Eso son
incidentes cazados y no ocasiones cumplidas.

**Son métricas distintas y conviene no mezclarlas.** Aquí se cuenta una tasa sobre las ocasiones en
que tocaba. Allí se cuentan incidentes cazados por un hook. Una regla sin hook y sin rastro de
herramienta se queda fuera de los dos. Ese hueco conviene tenerlo presente.

## Frontera con lo que ya existe

| Pregunta | Quién la responde |
|---|---|
| ¿el sistema es el que montaste? | `gobernanza-agentes-verificada` |
| ¿los guardianes bloquean cuando toca? | `guardianes-verificados-ia` |
| ¿y las reglas que no tienen guardián, se cumplieron? | **esta skill** |

Fuera del proyecto hay herramientas que abren este mismo historial para contar coste y consumo, más
otras que revisan los ficheros de reglas para ver si están bien escritos. Ninguna cruza las dos
cosas, que es justamente lo que aquí se hace.

## Banco

Son **tres bancos y 160 casos**, todos sobre trazas fabricadas y nunca sobre el historial real: un banco
que dependa de los datos de hoy cambia de resultado mañana.

`run_tests_adherencia.py` lleva 59 casos y prueba la lógica.

**Y los tres bancos están verificados por mutación, que es lo que separa un banco de un adorno.** No
hay que creérselo: `python mutar.py` lo hace delante de quien lo ejecute, quince sabotajes contra los
tres bancos. Dice cuántos se cazan. Hoy, quince de quince y cero huecos. Una mutación que nadie caza no
es un fallo del código: es una línea que el banco no vigila. El fichero medido se restaura al acabar
y también si matan el proceso a mitad, porque la copia intacta vive en disco y no en el flujo del
programa; mientras esa copia esté ahí, `test_seguridad.py` se pone rojo.

`test_seguridad.py` lleva 17 casos y es el que da derecho a fiarse: esta herramienta lee el historial
completo de sesiones, donde hay nombres, cuentas bancarias, documentos de identidad y claves pegadas
por descuido. Se plantan canarios de mentira en un historial de juguete y se exige que no salgan por
las vistas de agregados ni por ningún camino de error, además de la comprobación de que no escribe
nada. **`--acciones` queda fuera de esa promesa a propósito**: enseña rutas del historial porque para
eso existe. Sin una ruta de ejemplo nadie sabría si su vocabulario casa con su trabajo. Que la salida
sea agregada se puede ver leyendo el código; leerlo no es garantizarlo.

`test_portabilidad.py` lleva 84 casos y prueba otra cosa: que la herramienta sirva fuera de esta máquina.
Rutas POSIX y de Windows, vocabulario de otro proyecto, configuración mal escrita y otra estructura
de carpetas. Existe porque el primero no cubría nada de eso. Ninguno de esos casos da error: todos
devuelven números, y los números están mal.

**El segundo banco nació de un cambio de diseño, y hubo que hacerlo DOS veces.** Cinco acciones del
mapa (`gate-texto`, `buscador`, `regenerar`, `escanear-repos`, `salud`) eran nombres de scripts de
este proyecto, así que en cualquier otro medían cero para siempre; se sacaron al bloque
`acciones_shell` de `reglas.json`. Lo que no se vio entonces es que otras tres (`escribir-doctrina`,
`leer-skill`, `leer-rag`) llevaban el nombre de sus CARPETAS y tenían el mismo defecto: se sacaron
igual, al bloque `carpetas_doctrina`, el 25/07 y por una suite escrita desde el README sin mirar el
código. Arreglar la mitad de un defecto deja la otra mitad con aspecto de estar arreglada.

**Declarar un nombre que ya existe lo AMPLÍA, no lo sustituye.** El propio se prueba primero y el de
fábrica sigue detrás. El README prometía «redefinir»; se probó a hacerlo verdad y rompió seis casos
de este banco, porque lo que hace falta es ampliar: `eval_golden` es OTRA forma de ejecutar una suite
que se suma a `pytest` en vez de sustituirla. Lo que se corrigió fue la promesa y la conducta se
quedó como estaba, con un aviso por pantalla cuando ocurre.

**Y la mutación sirvió para algo más que confirmar.** El caso que vigilaba la deduplicación se quedó
CIEGO al cambiar el diseño: ponía tres escrituras seguidas y el colapso de repeticiones ya las
juntaba, así que pasaba igual sin deduplicar. Con una lectura en medio vuelve a discriminar. Un test
puede dejar de proteger cuando el código cambia debajo. Sin mutaciones nadie se entera.

Sobre el historial real se comprobó además que **discrimina**: pares que se cumplen por construcción
dan entre 62 % y 86 %, y tres pares sin relación causal dan 0,0 % los tres.

---
*adherencia-reglas · creada el 25/07/2026. Nace de medir un sistema real en vez de imaginar una
necesidad: primero se midió que el problema existía y cuánto costaba, y solo entonces se construyó.*
