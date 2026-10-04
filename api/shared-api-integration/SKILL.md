---
name: shared-api-integration
description: >
  Consumo de APIs REST con Python — requests, httpx, manejo de
  autenticación, rate limiting, paginación y errores.
  Trigger: Cuando necesitás traer datos de APIs, hacer requests HTTP, o integrar servicios externos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: shared-api-integration

APIs REST. Traé datos de afuera sin morir en el intento.

## Trigger

- Necesitás datos de una API externa
- Hay que autenticarse (Bearer token, API key, OAuth)
- La API tiene rate limiting y tenés que manejarlo
- Querés integrar un servicio (Slack, GitHub, Notion) en un pipeline

## Workflow LEND

```
1. ANALIZAR
   ├── Endpoint: ¿URL base? ¿documentación?
   ├── Auth: ¿API key, Bearer, OAuth, Basic?
   ├── Límites: ¿rate limit? ¿por minuto, por hora?
   └── Datos: ¿JSON, XML, CSV? ¿paginación?

2. OFRECER (Menú del Senior)
   ├── A) requests — simple, síncrono, para scripts y pipelines
   ├── B) httpx — async, HTTP/2, cliente moderno
   └── C) SDK oficial — si el servicio tiene SDK, usalo (pygithub, slack-sdk, etc.)

3. ELEGIR → confirmación

4. HACER
   ├── Cliente: session = requests.Session() (reusa conexión, headers)
   ├── Headers: {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
   ├── Manejo de errores: response.raise_for_status() + try/except
   ├── Rate limiting: time.sleep(60/requests_per_minute) o tenacity para retry
   ├── Paginación: while next_page: fetch + append
   ├── Timeout: timeout=30 siempre. Nunca requests sin timeout.
   └── .env para credenciales, nunca hardcodeadas

5. VERIFICAR
   ├── La respuesta tiene el formato esperado (validar contra schema)
   ├── El rate limiting se respeta
   └── Los errores se manejan con mensajes claros
```

## Patrones

- **Session > requests.get()**: reusa conexión TCP, headers, cookies
- **Timeout siempre**: `timeout=30` o la app cuelga para siempre
- **Retry con backoff**: tenacity o urllib3 Retry para errores transitorios (429, 503)
- **.env para secrets**: credenciales nunca en el código
- **SDK > raw requests**: si el servicio tiene SDK, usalo. Maneja auth, rate limits, etc.

## Anti-patrones

- ❌ requests sin timeout — si la API no responde, tu app se cuelga para siempre
- ❌ Hardcodear tokens — .env o secrets manager, nunca en el código
- ❌ No manejar rate limit — 401 por exceder el límite y toda la integración rota
- ❌ Ignorar errores HTTP — response.ok sin verificar el status code
- ❌ Una conexión nueva por request — usá Session() para reusar conexiones
