---
name: identidad
description: Define la identidad visual de un producto — propone dos o tres direcciones de color y tipografía justificadas por lo que el producto es, las escribe en design/tokens.css y las deja listas para verlas aplicadas en preview.html antes de decidir. Úsalo tras definir el producto y ANTES de prototipar (p. ej. "define la identidad", "qué paleta usamos", "elige los colores del producto"). No construye vistas.
---

Cada producto es **su propia marca**. La paleta que trae `design/tokens.css` es un
punto de partida deliberadamente neutro, para que nada arranque sin colores — no un
mandato. Esta skill es quien decide los definitivos.

## Cuándo

Entre el **Paso 1** del arranque (producto definido: sabes para quién es y en qué
registro vive) y el **prototipo**. Antes es adivinar; después ya hay vistas construidas
con los colores equivocados.

## El reparto de trabajo

**El juicio de diseño no lo pones tú: lo pone la skill `frontend-design`**, que ya está
instalada y es mejor en eso que cualquier instrucción que escribamos aquí — trae la
calibración contra los tres _looks_ por defecto de la IA (crema + serif + terracota;
negro + verde ácido; broadsheet con reglas finas) y el método de dos pasadas con
autocrítica.

Lo que **sí** es trabajo de esta skill, y `frontend-design` no puede saber, es el
contrato de este repositorio: veinte tokens, dos temas, OKLCH, contraste AA verificado y
tipografías con licencia libre. Eres el adaptador entre una dirección de diseño y
`design/tokens.css`.

## Paso 1 — Leer el producto, no inventarlo

Del `README.md` y de `docs/product/business-model.md`: para quién es, qué problema
ataca y en qué registro vive. Si están sin rellenar, **detente**: pregúntaselo a la
persona
primero. Una identidad sin producto detrás es decoración.

El **registro** manda más que el gusto:

| Registro                                    | Qué pide                                              | Por qué                                                                   |
| ------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| Herramienta densa (editor, timeline, panel) | Oscuro primero, cromas bajos, **un** acento saturado  | Sesiones largas, el contenido es el protagonista y el cromo debe callarse |
| Producto de trabajo (CRUD, dashboard)       | Claro primero, contraste alto, acento en las acciones | Uso diurno intercalado, se escanea más que se contempla                   |
| Consumo o marketing                         | Más libertad cromática y tipográfica                  | Se visita poco rato y hay que recordarlo                                  |

## Paso 2 — Pedir la dirección a `frontend-design`

Invócala con un brief construido a partir del Paso 1: sujeto concreto, audiencia,
trabajo de la página y registro. Pídele explícitamente **dos o tres direcciones
distintas**, cada una con:

- 4–6 colores con nombre y valor,
- una pareja display + cuerpo (y utilitaria si hace falta),
- una frase de por qué **esta** dirección para **este** producto.

Si alguna se parece a lo que producirías para cualquier producto del mismo sector,
descártala antes de enseñarla. La regla de `docs/conventions/ai-agents.md` es que el
diseño **sin dirección** converge a plantilla genérica: proponer con criterio no viola
esa regla, derivar por defecto sí.

## Paso 3 — Traducir al contrato de tokens

Aquí es donde esta skill gana su sitio. `frontend-design` devuelve 4–6 colores; el
sistema necesita **veinte tokens en dos temas**. Reglas:

- **`primary`** — la acción, no la marca. Es el color de «continuar», y por eso tiene que
  cumplir AA sobre `base-100` en los dos temas. Si el color de marca no llega, se ajusta
  la luminancia y el de marca vive en el logo, no en los botones.
- **`accent`** — el que se gasta una sola vez por pantalla. Saturado, para lo que debe
  destacar de verdad.
- **`base-100/200/300`** — tres superficies apiladas, no tres grises al azar: fondo,
  fondo alterno y bordes. En registro herramienta suelen hacer falta más niveles; si es
  el caso, dilo en vez de forzar tres.
- **`base-content`** — el texto. Nunca negro puro sobre blanco puro.
- **`neutral`, `info`, `success`, `warning`, `error`** — heredan la temperatura de la
  paleta; que no parezcan pegados de otro sistema.
- Cada `*-content` es el color **encima** de su pareja, y se elige por contraste, no por
  estética.
- **Valores en OKLCH**, porque su luminancia es perceptual y hace predecible
  ajustar la luminancia sin cambiar el tono.

Y el tema oscuro **no es el claro invertido**: se recalculan `primary` y `accent` por
luminancia para mantener AA sobre el fondo oscuro. Los tres bloques de `tokens.css`
—claro, `prefers-color-scheme`, `[data-theme="dark"]`— deben quedar coherentes.

**Si el registro elegido es oscuro-primero, hay que invertir los bloques**, no solo
confiar en el toggle: `tokens.css` viene con el claro en `:root`, y `:root` es lo que se
ve antes de que nadie elija nada. La cabecera del archivo explica el cambio (paleta
oscura a `:root`, clara a `[data-theme="light"]`, media query a `prefers-color-scheme:
light`). Dejarlo a medias da un editor que arranca en blanco y salta a oscuro, que es
exactamente el defecto que el registro quería evitar.

**Tipografías: solo licencia libre** (OFL, Apache, MIT) y self-hosted vía Fontsource. Una
tipografía de pago en el camino crítico es una dependencia legal en cada producto. Si la
dirección pide uno de pago, propón el equivalente libre y dilo.

## Paso 4 — Verlo aplicado antes de decidir

Escribe la primera dirección en `design/tokens.css` y **pide que abran
`design/preview.html`**. Ahí están trece secciones de componentes reales, los dos temas
y el **contraste AA recalculado en vivo**: si un badge sale rojo, esa pareja no se usa en
texto y hay que ajustar la luminancia.

Itera con la persona sobre el preview, no sobre descripciones. Una paleta se juzga
viéndola; un párrafo que la describe no se puede juzgar.

Si hay varias direcciones, aplícalas **de una en una** y deja que compare.

## Paso 5 — Registrar la elegida

Un ADR con `/new-adr`: qué dirección se eligió, **para qué registro**, y cuáles se
descartaron con su motivo. Sin eso, dentro de seis meses alguien —tú incluido— «mejora»
la paleta sin saber por qué era así.

Regenera `DESIGN.md` con `bash .github/scripts/design-md.sh --write` (el CI verifica
que esté sincronizado) y actualiza los assets de marca en `docs/conventions/ui.md`.
`design/README.md` no lleva valores — enlaza a `DESIGN.md` a propósito.

## Refuerzo opcional

Si el plugin **Impeccable** está instalado (ver `design/README.md`), pasa
`/impeccable audit` sobre el preview con la paleta aplicada: sus detectores deterministas
cazan defaults de IA —«AI beige», serif en cursiva, el punto que pulsa— que un ojo cansado
deja pasar. Sus tokens no mandan sobre los nuestros: manda `tokens.css`.

## NO hagas

- **No construyas vistas.** Eso es `/prototipo`, y va después. Aquí solo se decide la
  identidad.
- **No inventes la identidad si el producto no está definido.** Sin saber para quién es
  relleno, la propuesta sale de la nada y se nota.
- **No dejes el tema oscuro para luego.** Un color elegido solo en claro casi siempre
  falla AA en oscuro, y arreglarlo después obliga a mover toda la paleta.
- **No crees copias de los valores** (un `tokens.json`, una tabla a mano): `tokens.css`
  es la única fuente; lo que necesite otro formato se genera desde ahí.
- No propongas una dirección que no puedas justificar con una frase sobre **este**
  producto. Si la justificación sirve para cualquier otro, no es una dirección.
