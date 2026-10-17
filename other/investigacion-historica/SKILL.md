---
name: investigacion-historica
description: Metodología para buscar y contrastar fuentes sobre un hecho de historia argentina, evaluar su calidad e independencia, y reconocer cuándo un tema entra en zona de disputa política vigente. Usala al armar el dossier de una ficha del catálogo. Es la fuente citable del proceso; el que decide qué investigar y cómo entregarlo es el historiador-specialist.
argument-hint: <entidad-o-hecho-a-investigar>
allowed-tools: Read Glob Grep WebFetch WebSearch
---

# Investigación histórica

Esta skill es la metodología con la que el `historiador-specialist` arma un
**dossier**: hechos, fuentes, y —cuando corresponde— posturas en disputa. No es
la regla de cómo se narra eso —esa es `voz-narrativa`—, es la regla de cómo se
**investiga** antes de que exista una sola línea de prosa.

> **El dossier es dato, no texto de catálogo.** Su lector es el
> `narrative-specialist`, no el usuario final. Se escribe para que otro pueda
> narrar sin tomar partido, no para que suene bien.

---

## 1. Cuándo hace falta más de una fuente

No todo dato necesita el mismo esfuerzo de contraste. La regla:

| Tipo de dato | Fuentes mínimas | Ejemplo |
| --- | --- | --- |
| Cronología sin controversia real | 1, si es confiable | Año de nacimiento, lugar de una batalla ya consolidado en la historiografía |
| Cifra o dato que varía según la fuente | 2, y se documenta el rango | Número de combatientes, bajas, fecha exacta de un hecho mal registrado en su época |
| Tema de la **lista acotada** de disputas políticas (ver sección 4) | 2 o más, de perspectivas distintas | Campaña del Desierto, última dictadura y sus actores |
| Cita textual | La fuente primaria o quien la transcribe con precisión | Nunca se reconstruye de memoria |

**Más fuentes no es siempre mejor.** Cinco fuentes que se copian entre sí no son
cinco fuentes independientes: son una, repetida. Lo que cuenta es que **no
compartan el mismo origen**.

---

## 2. Cómo evaluar una fuente

Antes de citar algo, preguntate:

1. **¿Es una fuente primaria, una secundaria académica, o una terciaria de
   divulgación?** Las tres sirven, pero no dicen lo mismo con la misma
   autoridad. Un archivo o un documento de época pesa distinto que un artículo
   de divulgación sin bibliografía.
2. **¿Tiene autoría identificable y método visible?** Un texto sin autor, sin
   fecha o sin cómo llegó a su dato es la fuente más débil que hay, aunque
   suene convincente.
3. **¿De dónde saca su información?** Si una fuente secundaria no cita de
   dónde sale un dato, no aporta independencia real: hay que rastrear su
   origen o descartarla para ese dato puntual.
4. **¿Tiene un sesgo declarado o detectable?** No descalifica a una fuente
   —casi ninguna carece de perspectiva—, pero cambia qué tan sola puede
   sostener un dato disputado. Un sesgo detectado es información para el
   dossier, no un motivo para ocultar la fuente.

**Ante la duda sobre la calidad de una fuente, se busca otra.** No se sostiene
un dato disputado con la única fuente que lo dice de una forma conveniente.

---

## 3. Hecho vs. interpretación — la distinción que sostiene todo lo demás

Es la misma distinción que hace `voz-narrativa` del lado de la prosa, pero acá
se aplica **antes**, en la investigación:

- **Hecho**: ocurrió, y las fuentes independientes coinciden en que ocurrió.
  Se documenta una vez, con su mejor fuente. Ejemplo: que hubo una expansión de
  la frontera sur bajo la conducción de Roca en la década de 1870-80 es un
  hecho.
- **Interpretación en disputa**: existe una discusión política **vigente**
  sobre cómo **calificar** ese hecho —no sobre si ocurrió—. Ejemplo: si esa
  expansión fue una consolidación territorial necesaria o un genocidio contra
  los pueblos originarios es una disputa política de hoy, no una pregunta de
  cronología.

**El criterio para reconocer una disputa, cuando el tema no está ya en la lista
de la sección 4:**

1. ¿Hay dos o más lecturas del mismo hecho que se contradicen entre sí, no en
   los datos, sino en cómo se lo valora o se lo llama?
2. ¿Esa discusión sigue viva hoy —en la política, el debate público o la
   historiografía argentina contemporánea—, no solo en el pasado?
3. ¿Elegir una de las lecturas equivaldría a que el catálogo tome partido en
   una discusión política actual?

Si las tres respuestas son sí, el tema entra en zona de disputa **aunque no
esté todavía en la lista acotada**. Documentalo como tal en el dossier y
señalá en tu informe que debería sumarse a la lista de `voz-narrativa` — esa
decisión no es tuya, pero detectarlo sí.

---

## 4. La lista acotada — vive en `voz-narrativa`, no acá

La skill `voz-narrativa` (sección 7, neutralidad ante disputas políticas)
mantiene la lista concreta de temas donde esta regla aplica hoy.

Se cita desde acá y no se duplica: si la lista cambia, cambia en un solo lugar.
**Antes de armar un dossier, revisá esa lista.** Si el tema investigado está
ahí, tu dossier necesita la sección de interpretaciones en disputa completa
(sección 5). Si no está, alcanza con los hechos, salvo que apliques el
criterio de la sección 3 y detectes un caso nuevo.

---

## 5. Cómo se documenta una disputa en el dossier

Por cada interpretación en disputa:

```
- Postura: <cómo se califica el hecho desde esta lectura>
  Fuente: <quién la sostiene, con qué autoridad>
  Vigencia: <por qué sigue siendo una lectura activa hoy, no histórica>
```

**Nunca una sola postura.** Si solo encontraste una lectura, todavía no
terminaste de buscar, o el tema no era en realidad una disputa —revisá el
criterio de la sección 3 de nuevo—.

**No se resuelve la disputa.** El dossier no dice cuál postura es correcta.
Eso es, literalmente, lo que existe para evitar: que alguien —vos, el
narrador, o el catálogo— tome partido sin decirlo.

---

## 6. El formato del dossier

El dossier es texto en el informe del `historiador-specialist`, no un archivo.
Estas son sus secciones:

```
## Ficha investigada           (entidad y tipo)
## Hechos                      (cada uno con su fuente)
## Interpretaciones en disputa (si el tema está en la lista; postura + fuente, una por lectura)
## Huecos                      (lo que no pude sostener con una fuente confiable)
## Fuentes consultadas         (listado completo, con qué tan independientes son entre sí)
## Nota para el narrador       (qué necesita saber para no tomar partido, si aplica)
```

Un dossier sin la sección de interpretaciones en disputa, cuando el tema
**está** en la lista, es un dossier incompleto: no alcanza con los hechos.

---

## 7. Qué no hace esta skill

- No decide **si** investigar. Eso lo define el `historiador-specialist` en su
  sección 2 (los tres casos que lo activan).
- No decide **cómo se narra** una disputa en la prosa final. Eso es
  `voz-narrativa`.
- No reemplaza el material que aporta el usuario. Es una fuente adicional,
  nunca la única ni la que prevalece por default ante una discrepancia.

---

## Precedencia

Los ADR de `docs/adr/` y el vocabulario de `CONTEXT.md` **ganan** sobre esta
skill. El ADR que crea este rol y fija su alcance es el **0014**. La lista de
temas en disputa vive en `voz-narrativa` y se cita, no se copia.
