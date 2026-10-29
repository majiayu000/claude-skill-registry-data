---
name: tanstack
description: "TanStack headless para datos: Query (estado del servidor: fetch, caché, invalidación, infinite, SSR), Table (orden/filtro/paginación, cliente o servidor) y Virtual (listas enormes). React, Vue, Svelte, Solid. Para dashboards y tablas de datos."
---

# tanstack (Senzu)

Librerías **headless** (lógica sin estilos) de TanStack para lo que la UI de datos repite mal a mano: el
estado del servidor, las tablas y las listas enormes. Headless = tú pones el markup y los tokens del design
system (`ui-ux-pro-max`); TanStack pone la lógica. Multi-framework real: React, Vue, Svelte, Solid (misma API,
adaptador por framework). ÚSALA tras `ui-ux-pro-max` (estilo y patrón decididos) y con `ui-styling` para los
componentes base; aquí va la mecánica de datos.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Datos del servidor: fetch con caché, mutaciones, invalidación, infinite, SSR | `references/query.md` |
| Tabla con orden, filtro, paginación, selección (cliente o servidor) y virtualización | `references/table-virtual.md` |
| Estilo, paleta, patrón de la vista (antes que nada) | `ui-ux-pro-max` |
| Componentes base accesibles (shadcn) donde montar la tabla | `ui-styling` |
| Diseño del endpoint que alimenta la tabla (paginación, filtros en servidor) | `code-quality §references/api-design.md` |

## Cuándo sí y cuándo no
- **Query (estado del servidor)**: en cuanto hay fetch + caché + recarga. Sustituye al `useEffect`+`useState`
  a mano y a meter datos de servidor en el store global (Redux/Pinia): el servidor NO es estado de cliente.
- **Table**: tablas con orden/filtro/paginación/selección. Headless: no impone diseño ni accesibilidad (eso
  lo pones tú). Para una lista simple de 10 filas, no hace falta: un `map` basta.
- **Virtual**: solo cuando pintas miles de filas/ítems y el DOM se ahoga. No lo metas "por si acaso".
- NO es un data grid con estilos (no es AG Grid): si el cliente quiere una hoja de cálculo completa llave en
  mano, evalúa esa otra opción; TanStack es piezas que ensamblas.

## Reglas duras
1. **El servidor no es estado de cliente**: datos remotos → Query; estado de UI (modal abierto, tab) → estado
   local o store. No los mezcles.
2. **La `queryKey` describe los datos** (incluye filtros/página/tenant): `['pedidos', { estado, page }]`. Una
   key mal hecha sirve datos de otro filtro o de otro usuario (aislamiento por tenant, también en la key).
3. **Tabla grande = paginación/orden/filtro en el SERVIDOR** (manual mode de Table + Query), no traer 50k
   filas al navegador. El endpoint pagina y filtra (`code-quality §api-design`).
4. **Headless no es accesible solo**: pon `<table>` semántica, `scope`, foco y teclado tú (ui-ux-pro-max,
   ui-verify). Virtual rompe el scroll nativo y la búsqueda del navegador: úsalo solo si de verdad hace falta.
5. **Invalida, no recargues a mano**: tras una mutación, `invalidateQueries` de lo que cambió; nada de volver
   a montar el componente ni refetch global.
6. **SSR (Next/Nuxt)**: prefetch en el servidor + hydrate; no dobles el fetch en cliente (`references/query.md`).

## Versión y relación con otras skills
TanStack v5 (`@tanstack/react-query`, `@tanstack/vue-query`, `@tanstack/react-table`, `@tanstack/react-virtual`).
`ui-ux-pro-max` decide estilo y patrón · `ui-styling` monta los componentes · `code-quality` el endpoint que
alimenta la tabla · `ui-verify` comprueba la tabla en móvil y con teclado · para animar filas, `motion-framer`.
