---
name: copy-push
description: Úsalo SIEMPRE antes de redactar el mensaje de una campaña push o slot (título ≤100 chars, mensaje ≤200 chars).
---

# Copy para push y slot

Un push compite con WhatsApp y el banco por 2 segundos de atención. Estas son
las reglas del formato corto.

## 0. Antes de escribir

1. `search_cerebro("tono de voz")` — el tono de FinZen manda sobre cualquier
   fórmula de este skill.
2. Ten claro: ¿a quién le hablas (segmento y su causa — ver skill
   `campanas-retencion`), qué UNA acción quieres que haga, y por qué AHORA?

## 1. Anatomía del mensaje

```
Título (≤100):  el gancho — beneficio o momento, específico
Mensaje (≤200): valor concreto + UNA llamada a la acción
```

Estos dos SON los parámetros `title` y `message` de `propose_campaign` — no un
concepto aparte. Lo que discutas acá como "Título" tiene que llegar intacto
al parámetro `title` cuando formalices; no lo reinventes ni lo reemplaces por
un nombre de campaña distinto.

- **Las primeras 5 palabras deciden.** El usuario ve el título truncado en la
  pantalla bloqueada: el gancho va al inicio, no al final.
- **Una idea, una acción.** Dos CTAs = cero clics.
- **La acción debe ser pequeña**: "reajústalo en 10 segundos", "míralo en 1
  minuto". Nadie abre un push para hacer una tarea grande.

## 2. Principios (heredados del oficio, válidos en 200 chars)

| Principio | Mal | Bien |
|---|---|---|
| Beneficio > feature | "Nueva función de presupuestos" | "Tu presupuesto se reajusta solo — míralo" |
| Específico > vago | "Mejora tus finanzas" | "Tu presupuesto de Comida se pasó RD$1,300" * |
| Lenguaje del usuario | "Optimiza tu flujo de gastos" | "Se te está yendo el dinero en comida" |
| Activo y directo | "Tu meta puede ser configurada" | "Ponle fecha a tu meta" |
| Honesto | urgencia falsa, "última oportunidad" | urgencia real con fecha ("tu prueba vence el jueves") |

\* Solo si el dato viene de un tool o del propio sistema de FinZen — nunca
inventar cifras en el copy (regla dura #1).

**Cifra del usuario sí; cifra del negocio no.** "Tu presupuesto de Comida se pasó
RD$1,300" es dato del propio usuario y va sin problema. "El 84% de los usuarios
nunca transacciona" es una estadística del negocio en una pieza publicable y
necesita aprobación previa, aunque venga de un tool (regla dura 15e).

## 2b. El registro y los dos arquetipos

Del Manual de Marca, y aplica a cada push que escribas:

- **Español dominicano de la Gen Z, en "tú".** Suena a conversación entre
  amigos, nunca a tutorial ni a pitch. Expresiones como *chelitos, manin,
  bróder, pa'* funcionan cuando fluyen; forzarlas se nota.
- **Enseña como El Sabio y conecta como El Everyman — nunca uno sin el otro.**
  El Sabio da claridad ("se te pasó el presupuesto de comida"); el Everyman da
  cercanía ("a todos nos pasa a fin de mes"). Un push que solo instruye suena a
  banco; uno que solo empatiza no dice nada útil.
- **Nunca** juzgues cómo gasta el usuario, ni uses culpa o miedo como gancho.
  FinZen celebra el avance, no castiga el error.

Las cinco prohibiciones absolutas están en la regla dura 15 y aplican también
acá. El resto del método de contenido vive en `conceptos-contenido`.

## 3. Fórmulas de gancho que funcionan en push

- **{Logra el resultado} sin {el dolor}** — "Ordena tus gastos sin mover un dedo"
- **Pregunta que toca el dolor** — "¿Sabes en qué se te fue el dinero este mes?"
- **Dato propio del usuario** (el más potente) — "Llevas 5 días de racha"
- **Momento oportuno** — "Fin de quincena: 2 minutos para cuadrar tus números"
- **Zenio como ayudante** — "Zenio te lo resuelve en 10 segundos"

## 4. Reglas duras del formato

- Título ≤ 100 y mensaje ≤ 200 caracteres (límites del API — se validan).
- **Cuenta los caracteres antes de proponer.**
- Máximo 1 emoji, y solo si el tono del Cerebro lo permite. Nada de MAYÚSCULAS
  sostenidas ni signos de exclamación dobles.
- Español neutro-dominicano según la guía del Cerebro; "tú", nunca "usted".
- Nada de PII ni datos sensibles en el push (se ve en pantalla bloqueada):
  categorías y montos genéricos sí, detalles íntimos no.
- **Los planes se nombran como en la app: Gratis, Plus, Pro.** `FREE` y
  `PREMIUM` son nombres de la API; un push que dice "pásate a PREMIUM" habla de
  un plan que el usuario no encuentra en Suscripciones. Plus = PREMIUM.
- La duración de la prueba gratis se confirma con el socio antes de
  escribirla (la app muestra 21 días en Pro; hubo una anterior distinta).

## 5. Entrega al socio

Propón **una versión principal + 1-2 alternativas** con una línea de racional
cada una (qué gancho usa y por qué encaja con la causa del segmento). La
principal va en `propose_campaign`; las alternativas se mencionan en el chat.

---
*Adaptado de `copywriting` y `sms` — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT).*
