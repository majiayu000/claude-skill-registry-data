---
name: seo-audit
description: Audita los metadatos SEO de una página o ruta (title, description, canonical, Open Graph, robots) frente a las convenciones de SEO del proyecto y enumera lo que falta o está mal. Úsalo cuando la persona pida revisar/auditar el SEO, revisar las meta tags o verificar que una página esté lista para buscadores (p. ej. "audita el SEO de la página de precios", "revisa las meta tags de esta ruta").
---

Audita los metadatos SEO de la página/ruta que indique la persona.

1. Lee `docs/conventions/seo.md` para conocer las tags requeridas del proyecto, los formatos de valor (p. ej. longitud del title, longitud de la description), las reglas por tipo de página y qué páginas deben indexarse frente a `noindex`.
2. Identifica los archivos fuente de la página/ruta y dónde se define su metadata.
3. Verifica cada ítem requerido frente al documento de convenciones:
   - `<title>` — presente, único, dentro de la regla de longitud.
   - meta `description` — presente, dentro de la longitud, descriptiva.
   - URL canónica — presente y correcta.
   - Open Graph / tags sociales — `og:title`, `og:description`, `og:image`, etc. según se requiera.
   - directivas `robots` — correctas para este tipo de página (p. ej. `noindex` en páginas privadas/utilitarias).
   - Datos estructurados, si la convención lo requiere.
4. Produce un informe en forma de lista de verificación: cada ítem marcado como Presente / Falta / Incorrecto, con el archivo:línea y una sugerencia concreta de corrección para cada problema.

Ejemplo de hallazgo: `Falta canonical — añádelo a app/pricing/page.tsx; la convención exige uno en cada página indexable.`

NO reescribas la metadata de forma silenciosa a menos que la persona lo pida — informa primero los hallazgos. Da siempre prioridad a `docs/conventions/seo.md` por encima de consejos genéricos de SEO.
