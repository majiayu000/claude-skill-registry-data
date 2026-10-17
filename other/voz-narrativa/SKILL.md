---
name: voz-narrativa
description: Las reglas de lengua de la prosa épica del catálogo — registro alto, escenario dramático, ritmo amplio, metáfora madre sostenida, estructura y prohibiciones. Usala al redactar el contexto o la semblanza de una ficha, y al revisar cualquier prosa del catálogo. Es la fuente citable de la voz; el que decide es el narrative-specialist.
argument-hint: <archivo-de-contenido-o-párrafo>
allowed-tools: Read Glob Grep
---

# Voz narrativa del catálogo

Estas son las **reglas de lengua** de la prosa que se publica en una **ficha**.
Se citan, no se interpretan: cada regla está escrita para poder verificarse
contra un párrafo concreto y responder sí o no.

Las **muestras versionadas** están en [`muestras.md`](./muestras.md), en este
repositorio. Son de destino: **el texto que hay que escribir se parece a ellas.**
No se bajan de internet y no se trabaja de memoria: se abren.

> **La voz es épica y el registro es alto.** Escenario dramático, período
> amplio, léxico rico, metáfora sostenida. El lector tiene doce años o más, y
> **no** se le escribe para abajo. Ver *Audiencia*, y el **ADR 0012**, que es el
> que fijó esto.

---

## 1. Audiencia

El lector es **de doce años en adelante**: chicos grandes y adultos. Ese piso no
es un adorno; es lo que hace verificable todo lo que sigue, porque una regla no
puede medirse contra «cualquiera».

De dónde sale el número: las muestras exigen sostener una subordinación de tres
grados, entender vocabulario abstracto sin ilustración (*soberanía*,
*emancipación*, *proscripciones*) y traer del colegio un piso de referencias
históricas. Eso es lectura de secundaria, no de primaria.

Consecuencias directas, y las tres importan:

- **No se simplifica.** Una palabra difícil no se cambia por una fácil: se
  sostiene con el contexto de su oración.
- **No se explica de más.** El lector completa. Un texto que aclara todo le quita
  el trabajo, y con el trabajo se va el placer.
- **Tampoco se vuelve hermético.** Rico no es oscuro. Si una oración solo se
  entiende releyéndola dos veces, está mal escrita, y el registro alto no es una
  excusa.

**La versión para chicos existe y está pospuesta**, no cancelada: es otra lengua
y quizás otro diseño, y tiene su entrada en `docs/decisiones-pendientes.md`.
Mientras tanto, **no se escribe una prosa intermedia que le sirva a los dos.** Un
texto que intenta las dos audiencias no consigue ninguna.

---

## 2. Ritmo — se cuenta, no se estima

Los números salen de **contar los cuatro textos de las muestras 1 y 2**
(Brown y César). Son conteos manuales y pueden variar en una palabra según cómo se cuente un inciso con raya:

| Texto | Oraciones | Palabras | Media | Máximo |
| --- | ---: | ---: | ---: | ---: |
| Contexto de Brown | 4 | 162 | 40,5 | 53 |
| Semblanza de Brown | 5 | 155 | 31 | 37 |
| Contexto de César | 7 | 210 | 30 | 42 |
| Semblanza de César | 11 | 247 | 22,5 | 34 |

De ahí salen las reglas:

1. **La media de palabras por oración cae entre 22 y 42.** El piso es tan
   importante como el techo: un texto de media 15 puede ser correcto y no es esta
   voz. La amplitud del período **es** el registro.
2. **Ninguna oración pasa de 55 palabras.** El máximo observado es 53. Una
   oración más larga que eso deja de ser un período y pasa a ser un descuido: se
   parte o se poda.
3. **Cadencia: al menos una oración de 20 palabras o menos cada cinco.** Es la
   respiración que hace que el período largo se lea en vez de aplastar.
4. **Los párrafos dicen una sola cosa.** El contexto puede ser un párrafo único;
   la semblanza rara vez pasa de tres.

**Acá Brown y César no coinciden, y hay que decirlo.** La semblanza de César
cumple la cadencia con holgura —tiene oraciones de 13, 16 y 19 palabras entre los
períodos largos— y la de Brown no tiene ninguna por debajo de 27. La regla está
escrita del lado de César, porque esa alternancia es lo que separa un período
amplio de un muro. Si la preferencia del proyecto fuera la otra, la regla cambia
y este párrafo se reescribe.

Extensión:

| Campo | Extensión | Función |
| --- | --- | --- |
| `resumen` | hasta 280 caracteres (lo impone el descriptor) | Vidriera: qué fue y por qué importa. Sin metáfora y sin suspenso. |
| `contexto` | 160 a 220 palabras | El escenario: el mundo en tensión del que emerge el personaje. |
| `semblanza` | 150 a 300 palabras | El retrato: quién era, probado con hechos. |

Contar es parte del trabajo. Si no contaste, no verificaste.

---

## 3. Léxico

**El léxico elevado es el material, no el adorno.** *Anquilosado*, *efervescencia*,
*crisol*, *pugnas*, *endémica*, *antaño*, *albor*, *clave de bóveda*: esas
palabras están en las muestras y están bien. **No se reemplazan por sinónimos
llanos.**

Lo que sí se controla:

- **Se sostiene por el contexto, no por el diccionario.** Una palabra rara está
  bien puesta cuando la oración deja adivinar qué significa aunque no se sepa.
  «El anquilosado orden colonial» funciona: *orden colonial* ancla, *anquilosado*
  agrega. Una palabra rara sobre un sujeto también raro no se sostiene, y sale.
- **El término técnico o extranjero se glosa en su misma oración**, por
  aposición o por inciso. Es lo que hacen las muestras: «una aristocracia
  senatorial obscenamente opulenta, los *optimates*»; «la *dignitas* —el
  prestigio y la posición de un hombre—». Un término técnico suelto sin glosa es
  el único defecto de léxico que este registro no perdona. En las muestras hay
  uno: *viri militares*, que pasa sin explicación.
- **Los términos en otra lengua van en cursiva** —*optimates*, *dignitas*— salvo
  que ya sean castellanos de uso.
- **Un adjetivo por sustantivo, dos como excepción.** La acumulación no es
  riqueza: es ruido. Las muestras casi nunca apilan tres.
- **Nada de fórmulas de época.** *Cabe destacar*, *sin lugar a dudas*, *no es
  menos cierto que*: son relleno con aspecto de solemnidad.

**Español literario neutro.** Sin marcas regionales fuertes y sin voseo: el
narrador cuenta, no le habla al lector. Sin españolismos (*coger*, *ordenador*,
*vosotros*).

**Ortografía completa.** Tildes todas, incluidas las de mayúscula. Apertura de
interrogación y exclamación (`¿`, `¡`). Comillas latinas «», nunca rectas (ver §9). **Raya
de inciso —así—**, que en este registro es un signo de trabajo: Brown y César
la usan para incrustar la glosa sin romper el período.

**Prohibido sin excepción:** emoji, negritas o cursivas de énfasis dentro de la
prosa (la cursiva es para extranjerismos y títulos), mayúsculas de énfasis,
signos de exclamación.

---

## 4. La metáfora madre

Es el rasgo más característico de la voz y el que más fácil se hace mal.

**Una por ficha, y una sola.** Sale del oficio o del mundo del personaje: marina
en un marino —faro, brújula, corrientes, lobo de mar, puntas de lanza contra
flotas—; forja y mármol en un romano —aleación, martillar, los cimientos del
Capitolio—.

- **Se sostiene**: aparece al menos tres veces a lo largo del texto y las tres
  pertenecen a la misma familia. Una imagen suelta no es una metáfora madre, es
  un adorno.
- **No se mezcla.** Un personaje no puede ser a la vez un faro, una aleación y
  una semilla. Dos familias de imágenes en el mismo texto se anulan.
- **Se cobra al final.** Los contextos de Brown y César cierran con una imagen de la misma
  familia que abrió —«la clave de bóveda», «el mármol del Capitolio»—. Abrir una
  metáfora y no volver a ella es dejar la deuda impaga.
- **No se reutiliza entre fichas.** El «fuego estratégico» aparece en tres
  muestras —Brown, César y Balduino IV—, aplicado a un marino irlandés, a un
  patricio romano y a un rey cruzado. Una frase que sirve para los tres **no
  describe a ninguno**. Es el único defecto que las muestras comparten, y no
  se hereda.

**La prueba del traslado:** copiá la frase a la ficha de otro personaje. Si sigue
funcionando igual, no dice nada y se reescribe. Es el control más rápido que hay
contra la épica genérica, que es el modo de fallar de este registro: suena
grandiosa y no dice nada de nadie.

---

## 5. Estructura de cada item

### `contexto` — el escenario

- Describe **el mundo**, no la persona. Es una escena, no una introducción.
- **Abre con una tensión, no con una fecha.** «La República Romana del siglo I
  a.C. era una superpotencia en agonía»: la fecha entra, pero montada sobre la
  imagen.
- **No nombra al personaje** hasta la última oración, y ahí lo insinúa sin
  nombrarlo: «un patricio con un linaje divino y una deuda colosal se preparó
  para apostarlo todo».
- **Cierra abriendo, y con puntos suspensivos — en afirmación suspendida, nunca
  en pregunta.** Las cinco muestras versionadas (`muestras.md`) lo hacen así,
  sin excepción: entregan una imagen o un destino que queda en el aire, no una
  pregunta retórica. Es la misma regla que la sección 6 ya declara ("sin
  preguntas retóricas"): el cierre del contexto no es un lugar donde esa
  prohibición se levanta. Precisión añadida durante el ticket #51, después de
  que una primera vuelta probó el cierre en pregunta por pedido puntual y el
  propio corpus del usuario mostró que esa no es la convención.
- Da **fuerzas en pugna**, no lista de acontecimientos. Un contexto que enumera
  hechos en orden es una cronología disfrazada de escenario.

### `semblanza` — el retrato

- **No narra la cronología.** Retrata el carácter y lo **prueba con un hecho
  concreto**: los piratas del Egeo valen más que diez adjetivos.
- **Abre con una tesis sobre la persona**, no con su nacimiento. «Gayo Julio
  César no fue simplemente un producto de su tiempo; fue la fuerza catalizadora
  que aceleró su transformación».
- **Cero adjetivos de carácter sin escena que los sostenga.** Si un adjetivo no
  tiene su hecho al lado, se borra el adjetivo o se agrega el hecho. Es la regla
  que separa esta voz del panegírico.
- **Al menos una anécdota concreta**, ubicada o fechada, por semblanza.
- **Cierra con una imagen o con una frase de destino**, nunca con una enseñanza:
  «grabar su nombre en la eternidad».

### `resumen` — la vidriera

Una o dos frases, factuales, sin metáfora y sin suspenso. Es lo que se lee en el
listado y en una **tarjeta**: tiene que funcionar arrancado de la ficha. **Es el
único campo donde el registro baja**, y es a propósito: no es narración, es una
etiqueta.

---

## 6. Prohibiciones de contenido

Estas no son de estilo: son de producto, y una sola de ellas alcanza para
rechazar un texto.

- **No se inventa un hecho, una fecha, una cifra, una cita ni una anécdota.**
  Todo dato viene del material que entregó el usuario. Ante la duda, el dato no
  se escribe: se pregunta. **Esta prohibición se vuelve más importante con el
  registro alto, no menos**: la prosa épica es exactamente la que hace que un
  hecho falso suene verdadero, y nadie lo nota porque suena bien.
- **No se moraliza hacia el lector.** Nada de «nos enseña que», «su ejemplo nos
  recuerda», «gracias a él hoy podemos».
- **No se le habla al lector.** Tercera persona y pretérito. Sin preguntas
  retóricas y sin segunda persona.
- **Las sombras se cuentan, con dureza si corresponde.** Este registro sí juzga
  al individuo, y las muestras lo hacen: «crueldad pragmática», «su brutalidad
  contra los galos rebeldes», «obscenamente opulenta». Lo que no se hace es
  **santificar**. Un prócer sin sombras es propaganda, no historia.
- **No se juzga a pueblos ni a naciones.** Juzgar los actos de una persona es
  retrato; adjetivar a un pueblo entero no es historia.
- **Nada de anacronismos**, ni de lenguaje ni de ideas.
- **La crueldad se nombra, no se recrea.** Se puede contar que César crucificó a
  los piratas; no se describe la crucifixión.

---

## 7. Neutralidad ante disputas políticas

Esta regla la agregó el **ADR 0014**. No es una regla de estilo: es de
contenido, igual que las prohibiciones de la sección 6, y vive acá porque es su
vecina directa.

> **Se cuenta la verdad aunque sea dura. Lo que no se hace es tomar partido en
> una disputa política vigente sobre cómo calificar un hecho.**

**Alcance acotado, no todo el catálogo.** Aplica solo a temas donde existe hoy
una discusión política activa sobre cómo leer un hecho, no sobre si ocurrió.
Lista de arranque —abierta, no cerrada—:

- Los conflictos entre unitarios y federales.
- La anarquía del año 20.
- La Campaña del Desierto de Roca.
- La última dictadura militar y sus actores, incluida la guerrilla de los años
  setenta, con Montoneros nombrado explícitamente.

Esta es **la única fuente de la lista**: la `investigacion-historica` y el
`historiador-specialist` la citan, no la copian (ADR 0014).

La mayoría del catálogo —los próceres de baja polémica real— **no** cae bajo
esta regla y se escribe como siempre. Si aparece un tema nuevo que te parece
igual de disputado, decilo en tu informe: la lista se amplía, no se decide sola.

**No es una regla para suavizar.** Es lo opuesto a la sección 6, que ya permite
—y sigue permitiendo, sin cambios— juzgar los actos concretos de una persona
con dureza. El hecho duro se narra sin eufemismo: se puede nombrar a
**Montoneros** como lo que fue, una organización guerrillera, porque es un
hecho, no una interpretación. Se puede narrar el sometimiento de los pueblos
originarios en la Campaña del Desierto sin blindarlo.

**Lo que cambia es la etiqueta, no el hecho.** El patrón:

> Se narra el hecho duro sin eufemismo, y se agrega un contrapunto breve que
> reconoce que existe una lectura en disputa sobre cómo calificarlo — sin que la
> prosa falle a favor de ninguna. Ejemplo, con la Campaña del Desierto: se
> cuenta el sometimiento de los pueblos originarios tal cual fue, y se suma que
> para algunos esa expansión fue una consolidación territorial necesaria, y
> para otros un genocidio — sin que el texto se quede con una de las dos.

El contrapunto es **breve**: una frase, no un segundo párrafo. Si necesita más
espacio que eso, probablemente el tema merece que el `historiador-specialist`
entregue un dossier más detallado antes de escribirlo, no que la prosa se
alargue para sostenerlo.

**Es indiferente a la mirada de quien redacta.** Una posición personal —de
cualquier signo— no se traduce en prosa que favorezca un lado de una disputa
concreta. El registro puede seguir siendo épico y honrar el sacrificio humano
en general —eso ya lo permite la sección 6—, pero esta regla es específica: no
tomar partido en la lectura política de un hecho puntual de la lista.

**A quién obliga.** Al `narrative-specialist`, que escribe la prosa final. El
`historiador-specialist` hace la mitad anterior: detecta que un tema cae en la
lista y documenta las posturas con sus fuentes en el dossier; no redacta el
contrapunto, lo hace posible.

---

## 8. Marcas de cita y procedencia

**En la prosa no van marcas de cita.** Las muestras traen `[2], [3]`: vienen de
la herramienta con la que se generaron, apuntan a una bibliografía que este
repositorio no tiene, y cortan el período justo donde el ritmo importa. **Se
eliminan.**

La procedencia sí importa, y va donde ya vive la atribución en este proyecto:
**versionada, junto al contenido, invisible para el lector**. Se escribe como
comentario TSDoc arriba del objeto de la ficha, en
`contenido/<tipo>/<slug>.ts`:

```ts
/**
 * Fuentes de los hechos de esta ficha:
 * - <obra o página, autor, año> — para <qué hecho concreto sostiene>.
 */
```

Es el mismo criterio que el ADR 0009 aplica a las imágenes con `credito` y
`licencia`: la atribución es estructural y explícita, no un número entre
corchetes. Mostrarle las fuentes al lector sería un campo nuevo y una decisión de
producto; con la audiencia adulta es más razonable que antes, pero hoy no hace
falta.

---

## 9. El archivo es TypeScript

La prosa vive dentro de `contenido/<tipo>/<slug>.ts` como **tramos entre
comillas dobles concatenados con `+`**, de unas diez palabras por línea
(ADR 0030):

- **Todo tramo termina con un espacio**, salvo el último del campo, y ninguno
  empieza con espacio. Si falta ese espacio se pegan dos palabras, y ni el
  compilador ni el lint lo avisan: es el defecto propio de este formato.
- **Un cambio de párrafo es el tramo `"\n\n"`**, solo en su línea.
- **Una comilla doble recta dentro del texto no hace falta**: las citas van en
  comillas latinas «». Si aparece, se reescribe la frase.

Después de tocar un archivo de contenido se relee el final de cada tramo y se
corre `pnpm typecheck`: un texto que no compila no es un texto entregado.

---

## 10. Pasada final

Once controles. Cada uno se responde con sí o no sobre el texto que tenés
adelante, no sobre la intención.

1. ¿Conté las oraciones? Media entre 22 y 42, ninguna sobre 55, una corta cada
   cinco.
2. ¿La extensión de cada campo cae en su rango?
3. ¿Hay **una** metáfora madre, sostenida tres veces, de la misma familia, que
   se cobra al final?
4. ¿Pasa la prueba del traslado — ninguna frase serviría igual en otra ficha?
5. ¿El contexto abre con una tensión, no nombra al personaje hasta el final y
   cierra con puntos suspensivos?
6. ¿La semblanza abre con una tesis, prueba con un hecho concreto y no lista una
   cronología?
7. ¿Cada adjetivo de carácter tiene su escena al lado?
8. ¿Todo término técnico o extranjero está glosado en su oración, en cursiva?
9. ¿Todo hecho viene del material del usuario, sin una sola invención?
10. ¿Cero moraleja, cero segunda persona, cero santificación, sin marcas de
    cita? ¿Cada tramo termina con su espacio salvo el último del campo, sin
    espacios dobles ni comillas dobles rectas dentro de un tramo?
11. Si el tema está en la lista de la sección 7, ¿el hecho está narrado sin
    eufemismo y el contrapunto reconoce la disputa sin tomar partido?

Un texto que falla uno de los once no está terminado.

---

## Precedencia

Estas reglas son la fuente de la voz, pero **no son autoridad sobre el resto del
proyecto**. Si alguna contradice un ADR de `docs/adr/` o el vocabulario de
`CONTEXT.md`, **gana el ADR**. Ver la sección *Skills* de `CLAUDE.md`.

En particular: los términos del dominio no se cambian por una razón de estilo.
Una **ficha** es la página de una entidad y una **tarjeta** es una unidad de
repaso, también dentro de la prosa.

El ADR que fija la audiencia y el registro es el **0012**. Si alguna vez el
proyecto vuelve al registro llano, se escribe un ADR que lo supersede y esta
skill se reescribe con él; no se afloja una regla suelta para que pase un texto.
