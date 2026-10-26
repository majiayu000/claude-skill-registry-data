---
name: verificar-fuente
description: Verifica si una fuente de datos externa (sitio web, API, feed RSS) se puede usar en el pipeline de ingesta — comprueba su robots.txt, si bloquea agentes de IA, si el endpoint responde y qué formato devuelve. Úsala SIEMPRE antes de agregar cualquier fuente nueva o antes de afirmar que una fuente está disponible o bloqueada.
---

# Verificar una fuente de datos

Comprueba si una fuente externa se puede integrar al pipeline, **con peticiones reales**, no por
suposición. Este proyecto ya cometió el error de afirmar que un `robots.txt` prohibía el acceso sin
haberlo leído; esa afirmación casi cuesta la mejor fuente de datos del proyecto.

## Regla ética que gobierna esta verificación

**Un sitio que bloquea explícitamente a los rastreadores de IA queda descartado, sin excepción**,
aunque nuestro colector use un `User-Agent` propio que no caiga bajo esos nombres. Disfrazar el
origen para evadir una restricción declarada es incompatible con un proyecto que exige transparencia
a un operador de servicios públicos.

Si el veredicto es "bloqueado", **no propongas formas de sortearlo.** Propón la vía indirecta
legítima (por ejemplo, Google News RSS) o descarta la fuente.

## Procedimiento

### Paso 1 — Leer el `robots.txt` (obligatorio, siempre primero)

```
WebFetch: https://<dominio>/robots.txt
```

Busca **literalmente** estos nombres de agente:

`anthropic-ai` · `Claude-Web` · `ClaudeBot` · `GPTBot` · `CCBot` · `ChatGPT-User` · `OAI-SearchBot`

- **Si aparece cualquiera con `Disallow: /`** → **VEREDICTO: DESCARTADA.** Detente aquí. No pruebes
  más endpoints de ese dominio.
- Anota también qué rutas están prohibidas para `User-agent: *`.

### Paso 2 — Buscar el punto de entrada estructurado

En orden de preferencia (de mejor a peor):

1. **API REST documentada** — lo ideal
2. **API REST de WordPress** — prueba `/wp-json/wp/v2/posts` (así se encontró la fuente de Acuacar)
3. **Feed RSS/Atom** — prueba `/feed/`, `/rss.xml`, `/feed.xml`, `/atom.xml`
4. **Sitemap** — prueba `/sitemap.xml`, `/sitemap_index.xml`
5. **HTML** — último recurso, frágil, evítalo si hay cualquier alternativa

### Paso 3 — Probar la respuesta de verdad

Haz la petición y registra el resultado literal:

- Código HTTP
- `Content-Type`
- Tamaño de la respuesta
- Si es JSON o XML: qué campos trae realmente
- Cabeceras de paginación si existen (`X-WP-Total`, `X-WP-TotalPages`)

**No reportes que algo "funciona" si no viste la respuesta.** Un `429 Too Many Requests` significa
*pendiente de reintentar*, no *descartado* — anótalo así.

### Paso 4 — Evaluar la utilidad real

- ¿El contenido habla de cortes de agua en Cartagena, o es genérico?
- ¿Con qué frecuencia se actualiza?
- ¿Trae fecha estructurada, o hay que inferirla del texto?
- ¿Hay forma de pedir solo lo nuevo? (`?after=`, `?modified_after=`, `If-Modified-Since`)

## Formato del reporte

```markdown
### <Nombre de la fuente> — <dominio>

| Verificación | Resultado |
|---|---|
| `robots.txt` | <qué dice sobre agentes de IA y sobre `*`> |
| Punto de entrada | <URL exacta probada> |
| Respuesta | HTTP <código> · <content-type> · <tamaño> |
| Campos útiles | <lista real, no supuesta> |
| Actualización | <frecuencia observada> |

**Veredicto:** ✅ Usar · ⚠️ Permitida, pendiente de <qué> · ⏳ Reintentar · ❌ Descartada
**Motivo:** <una línea>
**Capa del pipeline:** L1 oficial · L2 prensa · L3 social · L4 ciudadana · ninguna
```

## Al terminar

1. Informa el resultado en la conversación, con su tabla resumen; si pasa a ser fuente en uso, anótala en `docs/06-etica-de-datos.md`.
2. Si es un hallazgo relevante, dilo explícitamente al usuario.
3. Si la fuente queda descartada por bloqueo de IA, **agrégala a la lista `deny` de
   `.claude/settings.json`** para que la regla sea imposible de violar por accidente.
