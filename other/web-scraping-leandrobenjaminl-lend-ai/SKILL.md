---
name: web-scraping
description: >
  Extracción de datos de sitios web — requests + BeautifulSoup, Selenium,
  y respeto por robots.txt y rate limiting.
  Trigger: Cuando necesitás scrapear sitios web, extraer datos de HTML, o automatizar navegación.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: web-scraping

Web scraping ético. Extraé datos sin romper el sitio ni violar términos.

## Trigger

- Los datos que necesitás están en una web sin API
- Hay que extraer información de múltiples páginas
- El sitio carga con JavaScript (requiere Selenium/Playwright)
- Necesitás monitorear cambios en una página

## Workflow LEND

```
1. ANALIZAR
   ├── ¿El sitio tiene API? si tiene, usala. Siempre preferí API sobre scraping.
   ├── robots.txt: ¿permite scraping? Respetalo.
   ├── Estático o dinámico: ¿el contenido carga con JS? (Selenium/Playwright vs BS4)
   ├── Volumen: ¿una página o 10k? define la estrategia
   └── Frecuencia: ¿one-shot o monitoreo continuo?

2. OFRECER (Menú del Senior)
   ├── A) BeautifulSoup — HTML estático, simple, rápido
   ├── B) Selenium — JS pesado, clics, navegación compleja
   └── C) Playwright — moderno, async, más rápido que Selenium

3. ELEGIR → confirmación

4. HACER
   ├── GET con headers: User-Agent real, no el de Python
   ├── Parsear: BeautifulSoup(response.text, 'html.parser')
   ├── Navegación: seguir links con href, paginación con next page
   ├── Rate limiting: time.sleep(1-3s) entre requests
   ├── Manejo de errores: capturar 403, 429, 503 con retry
   ├── Selenium: WebDriverWait para elementos dinámicos
   └── Datos extraídos: guardar en DataFrame o CSV

5. VERIFICAR
   ├── Los datos extraídos coinciden con lo que se ve en el navegador
   ├── No hay filas vacías o mal parseadas
   └── El scraper corrió dentro de los límites del robots.txt
```

## Patrones

- **robots.txt primero**: respetá las reglas del sitio. Si dice Disallow, no scrapees.
- **User-Agent real**: no uses el de Python/requests. Usá uno de Chrome real.
- **Rate limiting**: 1-3 segundos entre requests. No DDoSees el sitio.
- **BeautifulSoup para HTML estático**: es todo lo que necesitas el 80% del tiempo.
- **Playwright > Selenium**: más rápido, moderno, async. Mejor API.
- **Caché local**: guardá las páginas ya scrapeadas para no pedirlas de nuevo.

## Anti-patrones

- ❌ No respetar robots.txt — te pueden banear
- ❌ Sin rate limiting — 100 requests por segundo mata el servidor
- ❌ User-Agent de Python — los sitios bloquean bots genéricos
- ❌ Selenium cuando alcanza BS4 — es 10x más lento al pedo
- ❌ No manejar errores — un 503 mata todo el scraper sin aviso
