---
name: identidad-argentum
description: Los tokens y reglas vigentes de la identidad visual Argentum — paleta (v1 + v2 fusionadas), tipografía, contraste verificado y reglas de uso. Usala al escribir o revisar código de interfaz, para no tener que convocar al brand-specialist por un lookup. Es la fuente citable de la marca; el que decide es el brand-specialist.
argument-hint: <archivo-o-token>
allowed-tools: Read Glob Grep
---

# Identidad Argentum — tokens y reglas vigentes

Esto es un **lookup**, no un criterio: cada valor ya está derivado y medido, se
cita y no se reinterpreta. Describe el **estado vigente**; el porqué de cada
valor está en los documentos de marca, en los ADR y en el historial de git.

**Fuentes y precedencia.** El valor de cada token vive en
[`src/app/globals.css`](../../../src/app/globals.css). Las reglas viven en
[`sistema-de-diseno.md`](../../../docs/marca/sistema-de-diseno.md) (v1.0),
[`sistema-de-diseno-v2.md`](../../../docs/marca/sistema-de-diseno-v2.md) (v2) y
los ADR [0008](../../../docs/adr/0008-identidad-visual-argentum.md),
[0015](../../../docs/adr/0015-identidad-visual-argentum-v2.md) y
[0028](../../../docs/adr/0028-dorado-brillante-solo-como-ornamento.md) (que
supersede parcialmente al 0015: dorado brillante, `.shiny` y duración del
brillo; donde `docs/marca/` dice otra cosa, gana el 0028). Si esta skill
no coincide con alguno de ellos, **ganan ellos** y se corrige la skill. Dueño:
`brand-specialist`.

Nombres: en `globals.css` los colores llevan el prefijo `--color-*` de
Tailwind v4 (`--celeste-400` → `--color-celeste-400` → `bg-celeste-400`).
Las tablas usan el nombre de marca.

**Alias del fondo de página.** `--crema`, `--color-crema` y `--color-bg` son el
mismo valor (`#FBF7F0`) con tres nombres. Solo `--color-crema` está declarado
en `globals.css` (clase `bg-crema`): `--crema` es el nombre de marca de las
tablas y `--color-bg` es el nombre de los documentos de v2, sin declarar. En
código se escribe `bg-crema`; los comentarios que dicen `--color-bg` hablan de
este mismo fondo.

**Prefijo `cat`.** En `--color-cat-*` (`bg-cat-<c>-bg`, `text-cat-<c>-text`),
`cat` significa **tipo** de entidad, el término de `CONTEXT.md`. Es un nombre
heredado de v1, que decía «categorías»; no se renombra (`decisiones-menores.md`
§6) y un prefijo de token no es vocabulario del dominio. Lo mismo vale para el
sufijo `*-provisorio`: se cae cuando cada token deje de serlo, no antes.

---

## 1. Tokens

### Color

| Token | Valor | Rol / restricción |
| --- | --- | --- |
| `--celeste-50` | `#EAF4FE` | Fondo de bandas y notas; hover de celda tabular |
| `--celeste-150` | `#BFE0FC` | Borde sobre fondo celeste; filetes decorativos |
| `--celeste-400` | `#5DADE2` | Color de marca. **Superficie, nunca fondo de texto** |
| `--celeste-600` | `#1E96F5` | Superficie/borde **sin texto** |
| `--celeste-700` | `#0978D0` | Único fondo relleno con texto blanco (ADR 0008) |
| `--celeste-text` | `#0A5FA8` | Kicker, etiquetas, links |
| `--celeste-900` | `#0A3D66` | Fondo de panel invertido y del dorso de la tarjeta de repaso |
| `--celeste-cinta` | `#4FA8DE` | Exclusivo de la cinta bandera del header, decorativo |
| `--dorado-bg` | `#FFF8E8` | Fondo de tarjeta de liga (v1). Nunca sobre celeste |
| `--dorado-borde` | `#F0DFB8` | Borde de liga (v1) |
| `--dorado-filete` | `#F2D488` | Filete plano v1; respuesta del dorso de la tarjeta |
| `--dorado-text` | `#9A6900` | Texto dorado v1 (ADR 0008). Solo sobre `--dorado-bg` o `--blanco` |
| `--color-accent` | `#E0AC4C` | Dorado institucional v2. Decorativo, **nunca texto** |
| `--color-accent-300` | `#F7DE9B` | Hover del botón primario; texto dorado en panel invertido |
| `--color-accent-400` | `#EDC873` | Decorativo |
| `--color-accent-600` | `#D99A26` | Decorativo/borde, **nunca texto** |
| `--color-accent-700` | `#94691A` | Tope de texto dorado; texto/borde de `.btn-primary`. **Dorado de las cifras del hero** (sólido, sin brillo): 4.89:1 sobre `--blanco`, su fondo real (§3) |
| `--color-accent-800` | `#604411` | Texto chico; hover/activo del botón primario |
| `--laurel-bg` · `-borde` · `-text` · `-dark` | `#EAF0DF` · `#D6E2C2` · `#4B6A2C` · `#33471F` | Verde laurel (v1) |
| `--crema` (= `--color-crema` = `--color-bg`, ver arriba) | `#FBF7F0` | Fondo de página. Nunca blanco puro de página |
| `--blanco` | `#FFFFFF` | Tarjetas y superficies elevadas |
| `--arena-borde` · `--arena-borde-suave` | `#EDE4D6` · `#F5EFE4` | Bordes y divisores |
| `--borde-default` · `--borde-strong` | `#EDE4D6` · `#D6CAB8` | `border border-borde-default` |
| `--texto-titulo` | `#1F3B4D` | Títulos, valores destacados |
| `--texto-cuerpo` | `#4A4235` | Párrafos |
| `--texto-secundario` | `#6B5D4A` | Subtítulos, descripciones |
| `--texto-terciario` | `#7E705D` | Meta (ADR 0008). No sobre `--celeste-50` |
| `--texto-sobre-celeste` | `#FFFFFF` | Solo sobre `--celeste-700` o `--celeste-900` |
| `--ok` · `--ok-bg` | `#2E7C5A` · `#E9F5EF` | Acierto. Nunca en panel invertido |
| `--error` · `--error-bg` | `#C23A3A` · `#FBE9E9` | Error, fondos claros |
| `--alerta` · `--alerta-bg` | `#9F5F00` · `#FBF0DA` | Alerta |
| `--error-invertido` | `#DE9191` | Error dentro de panel invertido (ADR 0015). *Sin declarar todavía en `globals.css`*: baja cuando una pantalla lo use |
| `--color-foco` | = `--color-accent-700` | Anillo de foco por defecto |
| `--color-foco-invertido` | = `--blanco` | Anillo de foco en panel invertido |
| `--color-acento-repaso-100` · `-700` | `#EDE4F5` · `#6B3FA0` | Acento de "dominio": stat "Dominio de esta ficha" y resultado del quiz. No es un tipo |
| `--color-tarjetas-dorado-provisorio` | `#8A5E12` | **Solo `/tarjetas`**: `<h1>` "Tarjeta N" y "Racha actual" |
| `--color-tarjetas-carta-provisorio` | `#F5FAFF` | **Solo `/tarjetas`**: fondo del frente de la tarjeta |

**Tipos de entidad** (prefijo `cat`, ver arriba; v1, sin cambios). Fondo · borde · texto:

| Tipo | `cat-*-bg` | `cat-*-borde` | `cat-*-text` |
| --- | --- | --- | --- |
| Próceres (`proceres`) | `#EAF0DF` | `#D6E2C2` | `#4B6A2C` |
| Monumentos (`monumentos`) | `#EAF4FE` | `#CFE4F8` | `#0A5FA8` |
| Comidas (`comidas`) | `#FBECE4` | `#F2D6C7` | `#A8492A` |
| Fechas patrias (`fechas`) | `#FBE9EF` | `#F2CFDC` | `#96324F` |
| Animales (`animales`) | `#EFEAFB` | `#DDD2F4` | `#5A45A0` |
| Naturaleza (`naturaleza`) | `#E4F4EF` | `#C2E2D6` | `#1F7A5C` |

"Eventos históricos" (un tipo) tiene ícono pero no paleta: se deriva cuando una pantalla
la pida (brand-specialist).

**Ligas** (v1, nombres del ADR 0008 §6 y `CONTEXT.md`). Fondo · texto:
Cobre 0–500 `#FBEDE4`·`#8A4E1F` — Plata 501–1500 `#F1F3F5`·`#5B666F` — Oro
1501–3000 `#F0E2C4`·`#83590A` — Litio 3001+ `#EAF0DF`·`#4B6A2C`.

### Gradientes y efectos (`:root` y clases de `globals.css`)

**Roles del dorado.** Hay dos dorados y se elige por una pregunta: ¿el texto se
lee? (ADR 0028).

| Rol | Qué usa | Contraste |
| --- | --- | --- |
| **Ornamento**: logotipo (`.au`, exento por WCAG 1.4.3); numerales que cumplen **las dos** condiciones (su información ya está en texto visible AA, y llevan `aria-hidden`); los dos filetes vigentes (header y divisor del hero, `.filete-dorado`) | `--dorado-brillante-stops` y `--brillo-banda` | Sin requisito |
| **Lo que se lee**: toda cifra o texto que informa | Dorado AA sólido, **sin banda de brillo**. Cifras del hero: `--color-accent-700` sobre `--blanco` | **≥ 4.5:1 contra el fondo real**; si es gradiente, en el peor punto |

Los tres roles del ornamento son un **techo, no una autorización**: un uso
nuevo además tiene que estar cubierto por v2 y por la regla 8. El umbral de
4.5:1 vale aunque el texto sea grande (las cifras del hero miden 38px, peso 400,
Cormorant de trazo fino; ADR 0008, pantallas de bajo brillo). Nadie lo baja a
3:1. `.shiny` desaparece del sistema: las cifras ya no brillan.

**Pasada única del brillo.** El brillo animado dura **una sola pasada**
(`animation-iteration-count: 1`), con retardo más duración **menores a 5 s**
(hoy 3.4 s, sin retardo; WCAG 2.2.2). Todos los consumidores arrancan a la vez,
sin secuencias ni escalonados; nada lo reinicia por script o temporizador; la
banda termina fuera de cuadro a la derecha (`100%` de `shinySweep`) y el
elemento queda en su gradiente estático, sin salto. Que se repita (cursor,
temporizador) exige un ADR nuevo.

| Nombre | Valor | Uso |
| --- | --- | --- |
| `--dorado-brillante-stops` | `#623F04 0%, #C98810 20%, #FFD250 50%, #C98810 80%, #623F04 100%` | **Única fuente** del dorado brillante. Solo la lista de stops, sin `linear-gradient()` ni ángulo |
| `--gradiente-filete` | `linear-gradient(90deg, var(--dorado-brillante-stops))` | Base estática del filete del header |
| `--gradiente-au` | `linear-gradient(100deg, var(--dorado-brillante-stops))` | Base de `.au` |
| `--brillo-banda` | `linear-gradient(100deg, transparent 20%, rgba(255,255,255,0.75) 50%, transparent 80%)` | Banda de brillo animada, compartida |
| `.au` | `--gradiente-au` + `--brillo-banda`, `blend-mode: normal, overlay`, `background-clip: text`, fallback `color: --color-accent-700`, `shinySweep` 3.4s, **una pasada** | Logotipo del header y numerales de rol 2. **No** cifras que se leen. `.shiny` (su gemela) se retira por el ADR 0028 |
| `.filete-dorado` | `--gradiente-filete` + `--brillo-banda`, misma animación, sin recorte a texto | Filete de 3px bajo la cinta del header y divisor del hero, `aria-hidden`; una pasada |
| `.au-dark` | 7 stops de v2: `#E8BE63 0% · #F2D488 18% · #F7DE9B 36% · #FFF3D0 50% · #F7DE9B 64% · #F2D488 82% · #E8BE63 100%`, `100deg`, fallback `--color-accent-300`. Estático | Texto dorado sobre panel invertido |
| `--gradiente-filete-invertido` | `linear-gradient(90deg, transparent, var(--color-accent-300), #fff3d0, var(--color-accent-300), transparent)`. Estático | Filete del dorso de la tarjeta, `h-[2px] w-[70px]`, `aria-hidden` |
| `@keyframes shinySweep` | Un solo keyframe y un solo bloque `prefers-reduced-motion: reduce` (`animation: none`, banda inmovilizada fuera de cuadro) para `.au` y `.filete-dorado`. Iteración: 1 | — |

### Tipografía

| Rol | Familia y peso |
| --- | --- |
| Logotipo, `display`/`h1`/`h2`, cifras destacadas | Cormorant Garamond (`font-titulo`), **400** (ADR 0015) |
| `h3`, kickers | Cormorant Garamond, 600 (h3: interpretación, v2 §8). Única excepción: el kicker del hero de home (`hero.tsx`) va en Lora 500, por decisión del usuario; no se replica |
| Todo lo demás: cuerpo, labels, botones, chips, nav, meta, cifras de dashboard | Lora (`font-cuerpo`), 400/500/600 — reemplaza a Montserrat (ADR 0015) |
| Carga | `next/font/google` en `layout.tsx` (`--font-cormorant-garamond` 400/600 + itálica, `--font-lora` 400/500/600). Nunca `@import`. Itálica de Cormorant: en uso real solo 400 (epíteto, pie de foto, pista, resumen del quiz); el 600 se emite porque `next/font` no elige peso por estilo, sin sumar descargas. Lora no se carga en itálica |

| Token | Tamaño / interlineado / peso |
| --- | --- |
| `text-display` · `text-h1` · `text-h2` · `text-h3` | 36/1.1 · 30/1.15 · 24/1.2 · 18/1.3 |
| `text-body-lg` | 16px / 1.75 / 400 — cuerpo de lectura (ficha, tarjeta, enunciado) |
| `text-body` · `text-caption` | 14/1.7/400 · 13/1.6/400 — interfaz |
| `text-label` · `text-button` | 13/1.4/600 · 13/1/600 |
| `text-chip` | 11/1/600, tracking 0.06em, + `uppercase` en el componente |
| `text-meta` | 12/1.5/500 |
| `text-kicker` | 15/1/600, tracking 0.2em, + `uppercase`. Es el kicker de sección (`salas-del-catalogo.tsx`); el de 11px de v2 §6 no existe como token |
| `text-tile-title` | 26/1.15/400 |

`text-*` no incluye familia: un título necesita además `font-titulo`.

**Piso de tamaño: 11px.** Ninguna fila de esta skill baja de 11px (`text-chip`;
v1 y ADR 0015 §6, que subió el nav de 10 a 11). Texto más chico que un chip va
en `text-chip` o más. El código tiene valores arbitrarios de 9–10px que
**violan** este piso (§4); no son precedente.

### Espaciado, radios, sombras

| Grupo | Tokens |
| --- | --- |
| Espaciado | `xs` 4 · `sm` 8 · `md` 12 · `lg` 16 · `xl` 22 · `2xl` 32 (px) |
| Objetivo táctil | `--spacing-objetivo-tactil` 44px → `min-w-objetivo-tactil min-h-objetivo-tactil` |
| `max-w-xs…2xl` | Redirigidos a `--container-*` vía `--max-width-*` (colisión con el espaciado, ticket #73) |
| Radios | `sm` 8 · `md` 12 · `lg` 14 · `xl` 16 · `full` 9999 (px). Pisan los de Tailwind |
| Sombras | `shadow-sombra-sm`, `shadow-sombra-md`, `shadow-sombra-lg` (teñida de celeste) |

### Componentes con valor fijado

| Componente | Especificación |
| --- | --- |
| Botón primario | Outline: texto y borde `--color-accent-700`; hover/activo relleno `--color-accent-300` + texto `--color-accent-800`; foco `outline-2 outline-offset-2 outline-foco` (v2 §6, ADR 0015) |
| Panel invertido | Fondo `--celeste-900`; texto blanco, `.au-dark` o `--color-accent-300` |
| Cinta bandera | `linear-gradient(180deg, #4FA8DE 0 33.3%, #FFF 33.3% 66.6%, #4FA8DE 66.6% 100%)`, 40px, borde inferior `--color-accent`, seguida de `.filete-dorado` |
| Rombo separador | 5–6px, `rotate(45deg)`, `aria-hidden` |
| Plate / medallón | `border-radius: 150px 150px 2px 2px`; reemplaza al marco circular de v1 |
| Números romanos | Índice y salas: decorativos, `aria-hidden`; el nombre en texto es el identificador |
| Etiqueta de tipo (`/tarjetas`, frente y dorso) | `inline-block border px-[10px] py-xs font-cuerpo text-chip tracking-[0.14em] uppercase border-cat-<c>-text bg-cat-<c>-bg text-cat-<c>-text`; tipo desconocido: `border-texto-titulo bg-blanco text-texto-titulo`. **11px** (`text-chip`): el 9px de `tarjetas-repaso.tsx` y `franja-de-datos.tsx` está bajo el piso y se corrige en código |
| Marco de la tarjeta (`/tarjetas`) | Filete exterior 1px, filete interior 1px a 6px, cuatro rombos de 6px en las esquinas. Frente: `accent-700` / `accent-600` / `accent-700`. Dorso: `accent-600` / `accent-400` / `accent-300` |
| Numerales de esquina (`/tarjetas`) | `.au`, 17px, `aria-hidden`, esquina sup. izq. y (girado 180°) inf. der. del frente; rol 2 del dorado brillante (la información ya está en «Tarjeta N de M»). Aceptado por el usuario como "detalle de naipe"; no es precedente |

---

## 2. Reglas de uso

1. `--celeste-400` nunca lleva texto blanco. Con texto: `--texto-titulo` o `--celeste-900`.
2. `--celeste-600` no lleva texto. El único fondo relleno con texto blanco es `--celeste-700`.
3. Dorado y celeste no conviven en una superficie, salvo en el dorso de la tarjeta de repaso y en paneles invertidos (v1 §7, ADR 0015).
4. `--color-accent` y `--color-accent-600` son decorativos. Texto dorado: `--color-accent-700` o `--color-accent-800` sobre fondo claro; `--color-accent-300` o `.au-dark` sobre panel invertido.
5. El dorado brillante se cambia solo en `--dorado-brillante-stops`. No se bifurca: el filete y `.au` heredan juntos.
6. En panel invertido: `--error-invertido` en vez de `--error`, `--color-foco-invertido` en vez de `--color-foco`. `--ok`, `--error` y `--color-foco` no se usan ahí. `--error-invertido` es para errores de sistema, no para respuestas equivocadas (nada castiga).
7. Un panel invertido no muestra acierto con `--ok`. Si una pantalla lo necesita, se deriva `--ok-invertido` (brand-specialist, método del ADR 0015).
8. **Filetes.** El ornamento de v2 (cinta, `.au` animado, medallón, rombo, romanos, gradientes metálicos) va **solo** donde v2 lo cubre, y el dorado brillante solo en los tres roles de §1. Hay dos filetes brillantes, ambos `.filete-dorado`: el de 3px bajo la cinta del header y el divisor del hero. Un filete nuevo no se justifica con el ADR 0028. El del dorso de la tarjeta es `--gradiente-filete-invertido`, estático. Ligas, tipos y el resto de v1 siguen editoriales, sin degradé ni animación.
9. **Animación.** Todo brillo animado es de una sola pasada, de menos de 5 s en total, y arranca a la vez que los demás (§1). Cada animación respeta `prefers-reduced-motion` (`animation: none`, banda fuera de cuadro). Una repetición se decide con un ADR.
10. Texto justificado (`hyphens: auto`) solo en el cuerpo de ficha.
11. Íconos: Tabler outline copiado como SVG inline, con atribución; ninguna dependencia. Más de veinte es la señal para reconsiderar (ADR 0003, 0008).
12. No hay modo oscuro. Se decide con un ADR nuevo.
13. Cormorant Garamond nunca en 900. Versalita de Lora con `uppercase`, nunca `font-variant-caps: small-caps`.
14. Si compiten un componente de v1 y otro de v2 para el mismo uso, gana v2.
15. Foco visible en todo elemento interactivo: `outline-2 outline-offset-2 outline-foco` (o `outline-foco-invertido`). Nunca se quita el outline sin reemplazo.
16. Todo objetivo tocable mide al menos 44×44px (`--spacing-objetivo-tactil`), con al menos `--spacing-xs` (4px) entre objetivos adyacentes.
17. El color nunca es el único portador de significado (acierto/error también por forma, ícono o texto).
18. Los tokens `*-provisorio` solo existen en `/tarjetas`. No son escalones de ninguna rampa.
19. No hay escalón entre `--blanco` y `--celeste-50`: una celda de dos estados es `--blanco` (reposo) + `--celeste-50` (hover).
20. Los romanos de esquina de la tarjeta no autorizan romanos decorativos en otros componentes.

---

## 3. Contraste medido

Fórmula WCAG (luminancia relativa, canales linealizados). Piso: 4.5:1 texto,
3:1 no-texto (WCAG 1.4.11).

| Par | Contraste |
| --- | ---: |
| Blanco / `--celeste-700` | 4.56 |
| Blanco / `--celeste-900` | 11.22 |
| Blanco / `--celeste-600` | **3.12 — falla, sin texto** |
| Blanco / `--celeste-400` | **2.46 — falla, nunca** |
| `--texto-titulo` / `--celeste-400` | 4.77 |
| `--celeste-900` / `--celeste-400` | 4.56 |
| `--celeste-text` / `--celeste-50` | 5.87 |
| `--celeste-text` / `--crema` | 6.12 |
| `--texto-titulo` / `--blanco` | 11.72 |
| `--texto-titulo` / `--celeste-50` | 10.54 |
| `--texto-secundario` / `--blanco` | 6.38 |
| `--texto-secundario` / `--celeste-50` | 5.74 |
| `--texto-terciario` / `--crema` | 4.51 |
| `--texto-terciario` / `--celeste-50` | **4.33 — falla** |
| Textos principales / `--crema` | 5.98 a 10.98 |
| `--dorado-text` / `--dorado-bg` | 4.52 |
| `--dorado-text` / `--blanco` | 4.78 |
| `--dorado-text` / `--crema` | **4.48 — falla texto normal** |
| `--dorado-filete` / `--celeste-900` | 7.77 |
| `--color-accent` / `--crema` | **1.93 — falla, nunca texto** |
| `--color-accent-700` / `--crema` | 4.58 |
| `--color-accent-700` / `--celeste-50` | **4.39 — falla**, no sobre celeste |
| `--color-accent-700` (= `--color-foco`) / `--blanco` | 4.89 — **cifras del hero** (fondo real: `bg-blanco` del `<dl>`), ≥ 4.5 |
| `--color-accent-700` / `--celeste-900` | **2.29 — falla, no usar ahí** (incluye `--color-foco`) |
| `--color-accent-800` / `--crema` | 8.43 |
| `--color-accent-800` / `--color-accent-300` | 6.81 |
| `--color-accent-300` / `--celeste-900` | 8.48 |
| `#FFF3D0` / `--celeste-900` | 10.14 |
| `.au-dark` extremo `#E8BE63` / `--celeste-900` | 6.40 |
| `--color-foco-invertido` (blanco) / `--celeste-900` | 11.21 |
| `--ok` / `--ok-bg` | 4.53 |
| `--ok` / `--celeste-900` | **2.21 — falla, no usar ahí** |
| Blanco / `--ok` (botón, 14px) | 5.07 |
| `--error` / `--error-bg` | 4.53 |
| `--error` / `--crema` | 4.97 |
| `--error` / `--celeste-900` | **2.11 — falla, no usar ahí** |
| Blanco / `--error` (botón, 14px) | 5.30 |
| `--error-invertido` / `--celeste-900` | 4.58 |
| `--alerta` / `--alerta-bg` | 4.52 |
| `--color-acento-repaso-700` / `-100` | 5.98 |
| `--color-acento-repaso-700` / `--blanco` | 7.38 |
| Tipos, texto / fondo (los 6) | 4.62 a 6.38 |
| Ligas, texto / fondo (las 4) | 4.82 a 5.75 |
| Etiqueta: borde `cat-*-text` / `#F5FAFF` | 5.00 a 7.16 (neutro 11.17) |
| Etiqueta: fondo `cat-*-bg` / `--celeste-900` | 9.53 a 10.08 (neutro 11.22) |
| Etiqueta: borde `cat-*-text` / `--celeste-900` | 1.49 a 2.13 — redundante, delimita el fondo |
| Marco frente / `#F5FAFF`: `accent-700` · `accent-600` | 4.67 · 2.33 (decorativo) |
| Marco dorso / `--celeste-900`: `accent-600` · `accent-400` · `accent-300` | 4.59 · 7.00 · 8.48 |
| `--color-tarjetas-dorado-provisorio` / `--crema` · `--blanco` | 5.33 · 5.69 |
| `--texto-titulo` · `--texto-secundario` / `#F5FAFF` | 11.17 · 6.08 |
| `#F5FAFF` / `--crema` | 1.02 (no texto; delimitan marco y mazo) |
| `--celeste-150` / `#F5FAFF` · `--crema` | 1.31 · 1.29 (decorativo) |
| Centro dorado brillante `#FFD250` / `--crema` | **1.35 — falla** (deuda aceptada, §4) |
| `#FFD250` / `#F5FAFF` (romanos de la tarjeta) | **1.37 — falla** (decorativo, aceptado) |
| `#FFD250` / `--celeste-50` | **1.29 — falla** |
| `#FFD250` / `--blanco` | **1.44 — falla** (ornamento, sin requisito) |
| Salto interno del dorado brillante, `#623F04` → `#FFD250` | 6.53 (percepción de brillo, no es un par de AA) |

---

## 4. Deudas aceptadas

- **Centro del dorado brillante (`#FFD250`) bajo AA en reposo**: 1.35:1 sobre
  `--crema`. Aceptado por el usuario porque `.au` viste el logotipo y numerales
  decorativos; desde el ADR 0028 las cifras que se leen no lo usan. Si se vuelve a tocar, preguntar antes
  qué se prioriza: brillo interno, contraste contra el fondo u oscurecimiento
  general.
- **Pico de `--brillo-banda` sin remedir** contra la base vigente. El último
  número (1.81:1) se midió contra una base anterior. Alcanza a `.au` (logotipo
  sitewide); `.filete-dorado` no lleva texto. Se remide la próxima
  vez que se toque la banda o la base.
- **Riesgo de Lora a tamaño chico**: labels y botones (13–14px) medio-alto;
  chips y nav (11px) alto, kickers de sección (15px) medio; `tabular-nums` probable no-op. Verificar
  con render real antes de una tabla de cifras apiladas. Contingencia:
  `ui-monospace` acotado a los dígitos, nunca otra familia de marca.
- **Código bajo el piso de 11px.** `text-[9px]` en la etiqueta de tipo y en el
  `<dt>` de `franja-de-datos.tsx` (`/tarjetas`); `text-[10px]` en
  `nav-principal.tsx`, `estadisticas-catalogo.tsx`, `grilla-salas.tsx`,
  `grilla-laminas.tsx`, `quiz-pregunta.tsx`, `ficha-entidad.tsx` y el kicker de
  `tarjetas-repaso.tsx` (línea 152). El nav ya
  debía estar en 11px desde el ADR 0015. Ticket de código pendiente; hasta
  entonces la skill dicta 11px.
- **Código previo al ADR 0028.** `globals.css` todavía tiene `.shiny` y
  `infinite`, y `estadisticas-catalogo.tsx` usa `.shiny`. Lo vigente es lo que
  dice §1; el cambio de código es del `frontend-specialist` (ejecución del ADR).
- **Acento de repaso cerca del matiz de Animales** (`#6B3FA0` contra
  `#5A45A0`): puede leerse como ese tipo.
- **Tokens `*-provisorio` de `/tarjetas`**: pendiente que el usuario decida si
  esos dos valores pasan a toda la página; hasta entonces no se usan fuera.

---

## 5. Lo que esta skill no resuelve — convocá al `brand-specialist`

- Un token nuevo, o un par de tokens combinados cuyo contraste no está en la §3.
- Un componente que ningún documento cubre.
- Un conflicto v1/v2 que la regla 14 no alcance.
- Extender el ornamento de v2 a un componente que v2 no menciona.
- Modo oscuro, alto contraste o un cambio real de paleta o tipografía: siempre
  un ADR nuevo.
