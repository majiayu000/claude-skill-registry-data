---
name: observability-and-debugging
description: "Implementa un workflow de observabilidad y debugging para apps backend/frontend con logging estructurado, trazas de sesión y métricas básicas. USE FOR: debug de errores intermitentes, reproducir bugs, investigar latencia, monitorear WebSocket/HTTP, diagnosticar timeouts, fallos de reconexión y regresiones de rendimiento."
---

# Observability and Debugging

## Objetivo
Estandarizar cómo diagnosticar incidentes y bugs en sistemas fullstack usando tres pilares: logs estructurados, trazas de sesión y métricas operativas mínimas.

## Resultado Esperado
- Incidente reproducido o delimitado con evidencia objetiva.
- Señales clave instrumentadas en backend y frontend.
- Hipótesis priorizadas con pasos de validación claros.
- Cierre con causa raíz probable, impacto y acciones preventivas.

## Entradas Mínimas
- Síntoma principal (error, timeout, latencia, reconexión fallida).
- Entorno afectado (local/dev/staging/prod).
- Ventana temporal aproximada del fallo.
- Ruta funcional impactada (endpoint/página/stream WS).

## Flujo Paso a Paso

### 1. Definir el incidente
- Redactar un resumen de 1-2 líneas del problema.
- Identificar severidad inicial:
  - `S1`: caída total o corrupción de datos.
  - `S2`: funcionalidad principal degradada.
  - `S3`: problema menor o intermitente con workaround.
- Capturar evidencia inicial (capturas, logs, payload, timestamp).

Chequeo de salida:
- El problema está definido con contexto suficiente para iniciar análisis.

### 2. Establecer correlación por sesión/request
- Generar o propagar `session_id`/`request_id` en backend y frontend.
- Confirmar que cada evento relevante incluye el identificador de correlación.
- En WebSocket, usar `session_id` consistente desde inicialización hasta cierre.

Decisiones:
- Si no existe correlación: implementarla primero antes de seguir investigando.
- Si hay múltiples hops (proxy, gateway): preservar ID en todos los saltos.

Chequeo de salida:
- Se puede reconstruir una historia de ejecución end-to-end por ID.

### 3. Instrumentar logging estructurado
- Usar formato JSON o clave-valor uniforme.
- Incluir campos mínimos: `timestamp`, `level`, `service`, `env`, `session_id/request_id`, `event`, `duration_ms`, `status`, `error_code`.
- Evitar datos sensibles (tokens, secretos, PII).

Decisiones:
- Errores reproducibles: aumentar nivel temporalmente a `debug` en área afectada.
- Alto volumen: muestreo de logs no críticos para reducir ruido.

Chequeo de salida:
- Logs legibles por máquina y comparables entre servicios.

### 4. Añadir trazas de sesión
- Definir spans por operación clave:
  - `http.request`
  - `simulation.init`
  - `ws.connect`
  - `ws.stream_tick`
  - `ws.disconnect`
- Añadir atributos: tamaño payload, número de mensajes, estado final, motivo de cierre.

Decisiones:
- Si hay latencia alta: priorizar spans de cola, serialización y red.
- Si hay desconexiones: capturar códigos de cierre WS y retries.

Chequeo de salida:
- Existe timeline por sesión con tiempos y puntos de falla.

### 5. Definir métricas básicas
- Métricas recomendadas:
  - `http_requests_total` (por ruta/status)
  - `http_request_duration_ms` (p50/p90/p99)
  - `ws_active_connections`
  - `ws_messages_sent_total`
  - `ws_message_size_bytes`
  - `ws_disconnect_total` (por código)
  - `simulation_start_total`
  - `simulation_failed_total`
- Configurar alertas mínimas sobre errores y latencia.

Decisiones:
- Sin dashboard: empezar con export simple + umbrales en logs.
- Con dashboard: panel rápido de salud por endpoint y stream.

Chequeo de salida:
- Hay visibilidad cuantitativa para detectar y comparar degradaciones.

### 6. Ejecutar triage guiado por hipótesis
- Formular 2-3 hipótesis máximas, ordenadas por probabilidad/impacto.
- Diseñar experimento por hipótesis:
  - Qué métrica/log/span la valida o descarta.
  - Qué resultado esperado confirma la hipótesis.
- Ejecutar cambios mínimos para validar (sin refactors amplios).

Chequeo de salida:
- Hipótesis confirmada o descartada con evidencia.

### 7. Cierre y prevención
- Documentar:
  - causa raíz (confirmada o más probable),
  - impacto,
  - mitigación aplicada,
  - deuda técnica pendiente,
  - acción preventiva (test, alerta, runbook).
- Crear tareas para endurecer observabilidad en zonas ciegas.

Chequeo de salida:
- Existe plan concreto para reducir recurrencia del incidente.

## Playbooks Rápidos

### A. Timeouts HTTP
1. Revisar `p95/p99` por endpoint.
2. Verificar spans lentos por fase.
3. Confirmar límites de timeout de cliente y servidor.
4. Reducir payload o costo por request.

### B. Desconexiones WebSocket
1. Registrar código de cierre y momento.
2. Correlacionar con picos de mensajes/tamaño.
3. Verificar heartbeat/retry/backoff del cliente.
4. Validar límites de infraestructura (proxy/load balancer).

### C. Bug intermitente no reproducible
1. Activar logging aumentado por ventana limitada.
2. Forzar correlación por `session_id`.
3. Capturar muestra representativa de sesiones fallidas vs exitosas.
4. Comparar diferencias en secuencia de eventos.

## Reglas de Calidad
- No debuggear a ciegas: siempre con hipótesis y evidencia.
- No mezclar fixes de comportamiento con refactors grandes en el mismo ciclo.
- No registrar secretos ni datos sensibles en logs/trazas.
- No cerrar incidente sin acción preventiva verificable.

## Definición de Terminado
- Logs estructurados activos en puntos críticos.
- Correlación end-to-end disponible por sesión/request.
- Métricas mínimas expuestas y revisadas.
- Incidente documentado con causa/mitigación/prevención.

## Plantilla Rápida de Ejecución
1. Definir incidente y severidad.
2. Asegurar correlación por `session_id/request_id`.
3. Instrumentar logs estructurados.
4. Instrumentar trazas por operaciones clave.
5. Exponer métricas base y umbrales.
6. Ejecutar hipótesis y validar evidencia.
7. Cerrar con RCA y prevención.
