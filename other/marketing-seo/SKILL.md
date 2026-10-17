---
name: marketing-seo
description: "Marketing de la web: SEO on-page y local, GA4 + Tag Manager (contenedores, dataLayer, Consent Mode) y MCPs de analítica para operar con agentes (GA4 oficial, Search Console, PostHog). Úsala para posicionar y medir; el diseño es de ui-ux-pro-max."
---

# marketing-seo (Senzu)

El directorio de crecimiento: que la web **se encuentre** (SEO), **se mida** (GA4/GTM) y se pueda
**operar con agentes** (MCPs de analítica). Trabaja SOBRE una web ya construida — el diseño es de
`ui-ux-pro-max`, el plan de eventos nace en `ui-ux-pro-max §references/es/measurement.md` y la pasada
técnica de salida es `/lanzar` (`ui-verify §references/launch-checklist.md`): esta skill no los duplica,
los profundiza.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Posicionar: keywords, on-page, SEO local, schema, contenido | `references/seo-onpage.md` |
| Instrumentar: GA4, Google Tag Manager (contenedor), dataLayer, Consent Mode | `references/analytics-gtm.md` |
| MCPs: leer datos con IA, o que el agente CREE/organice el contenedor GTM | `references/mcp-tools.md` |
| Definir QUÉ medir (conversiones por negocio) | `ui-ux-pro-max §references/es/measurement.md` (la fuente del plan) |
| Checklist técnico de salida (sitemap, OG, robots…) | `ui-verify §references/launch-checklist.md` |
| Varios idiomas (hreflang, slugs) | `code-quality §references/i18n.md` |
| Titulares y textos que venden | `ui-ux-pro-max §references/es/copywriting.md` |

## Principios (aplican siempre)
1. **SEO es contenido útil + técnica correcta**, en ese orden: sin contenido que responda a la búsqueda,
   ningún truco técnico posiciona. Nada de keyword stuffing ni texto IA sin revisar publicado a granel.
2. **Se mide lo que mueve el negocio** (2-5 conversiones), detrás del consentimiento, sin PII. El plan de
   medición manda; GTM es solo el vehículo.
3. **Un contenedor GTM limpio o ninguno**: si solo hay GA4 + 2 eventos, `gtag` directo basta; GTM entra
   cuando hay múltiples tags (Ads, píxeles, herramientas) o quien publica no toca código.
4. Cambios de SEO se documentan (qué se cambió y por qué) y se les da TIEMPO (semanas, no días) antes de
   juzgar; la fuente de verdad del resultado es Search Console + la analítica, no la intuición.
5. Con MCPs: el agente LEE datos para diagnosticar, y puede CREAR/organizar el contenedor GTM (Stape MCP)
   — pero NUNCA publica una versión sin aprobación explícita del usuario; los cambios en la web siguen
   el flujo normal (plan → cambio → verificación).

## Relación con otras skills
UI/diseño → `ui-ux-pro-max` · lanzamiento → `ui-verify` (/lanzar) · idiomas → `code-quality/i18n` ·
rendimiento (Core Web Vitals) → `code-quality/performance` + launch-checklist §3.
