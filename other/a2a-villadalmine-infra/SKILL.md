---
name: a2a
description: >
  Agent-to-Agent (A2A) bidireccional OpenClaw↔Hermes — ambas direcciones operacionales.
  OpenClaw→Hermes: ✅ ask_hermes_agent via MCP :8000. Fix: max_iterations=15 (era 90).
  Hermes→OpenClaw: ✅ bridge.js stateful Node.js :18790 (no supergateway).
  ask_hermes_agent PONG en 9s (era 37s). E2E 13/13 PASS 2026-05-28.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  author: dotfiles
  tags: [a2a, agent-to-agent, mcp, messaging-bridge, hermes, openclaw, honcho, telegram, debate]
---

# A2A — Agent-to-Agent entre OpenClaw y Hermes

## Conceptos clave: MCP vs A2A

| Concepto | Descripción |
|----------|-------------|
| **MCP tool calling** | Un agente llama una función en otro. Síncrono, pull-only. El resultado es un string. Es "usar una herramienta". |
| **A2A via messaging bridge** | Un agente envía una pregunta al loop de razonamiento autónomo del otro. El receptor razona con su LLM + MCPs propios y responde con análisis propio. Es "hablar con otro agente". |
| **A2A protocol (Google)** | Estándar peer-to-peer con Agent Cards, streaming SSE, push proactivo. No implementado aún (Fase 4). |

La distinción importante: `ask_hermes_agent("DEBATE...")` no llama una función — **dispara el AIAgent completo de Hermes** con sus propios MCPs (kubernetes, kagent, prometheus). Hermes razona de forma autónoma y devuelve su análisis. Eso es A2A real.

---

## Diagrama de flujo completo

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MODO MCP CLÁSICO (tool calling, síncrono)                                   │
│                                                                              │
│  OpenClaw ──[MCP call]──► Hermes tool:                                       │
│                            conversations_list / messages_send / messages_read │
│                            events_poll / events_wait                          │
│                            ← devuelve string inmediato, sin razonamiento      │
│                                                                              │
│  Hermes ──[MCP call]──► OpenClaw tool (vía bridge :18790):                   │
│                           conversations_list / messages_send / messages_read  │
│                           events_poll / events_wait                           │
│                           ← devuelve string inmediato, sin razonamiento       │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  MODO A2A (debate autónomo, cada agente razona con sus MCPs)                 │
│                                                                              │
│  OpenClaw llama ask_hermes_agent("DEBATE T1 — Mi posición: X. Tu análisis?") │
│       │                                                                      │
│       ▼                                                                      │
│  Hermes AIAgent loop:                                                        │
│    ├─ consulta kubernetes MCP (pods, logs, estado)                            │
│    ├─ consulta kagent MCP (helm, prometheus, cilium)                          │
│    ├─ consulta openclaw MCP (historial conversación con usuario)              │
│    └─ forma respuesta autónoma fundamentada en datos reales                   │
│       │                                                                      │
│       ▼                                                                      │
│  OpenClaw recibe respuesta de Hermes                                         │
│  OpenClaw forma réplica e itera (ask_hermes_agent("DEBATE T2 — Historial..."))│
│       │                                                                      │
│       ▼                                                                      │
│  Síntesis final → usuario via Telegram (@tito_es_tu_bot)                    │
│                                                                              │
│  (Hermes también puede iniciar: ask_openclaw_agent("Mi análisis: X"))        │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  DIFERENCIA CLAVE: MCP vs A2A                                                │
│                                                                              │
│  MCP: "Ejecuta esta función y devuélveme el resultado"                       │
│       → El receptor NO razona, solo ejecuta                                  │
│       → Resultado determinístico, rápido                                     │
│       → Ejemplo: conversations_list() → lista de sesiones                   │
│                                                                              │
│  A2A: "Piensa sobre este problema y dame tu análisis"                        │
│       → El receptor razona autónomamente con sus propios MCPs                │
│       → Resultado no determinístico, puede tardar 30-90s                    │
│       → Ejemplo: ask_hermes_agent("Debate T1: ¿mejor storage para K8s?")    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Arquitectura actual (verificado 2026-06-12)

```
Usuario (Telegram @tito_es_tu_bot)
    │
    ▼
OpenClaw (Tito) — namespace: openclaw, node: srv-rk1-nvme-02
    │ pod: openclaw-* (4 containers)
    │   ├─ openclaw-gateway     :18789  — AI gateway, Telegram, Honcho memory, STT/TTS
    │   ├─ kubernetes-mcp       :8080   — K8s MCP sidecar
    │   ├─ smee-client          —       — webhook relay GitHub→Telegram
    │   └─ openclaw-mcp-bridge  :18790  — bridge.js stateful (Node.js)
    │         `openclaw mcp serve` spawned ONCE at startup
    │         GET /mcp → 200 SSE keepalive (Python MCP SDK no 405)
    │         POST /mcp initialize → cached childInitResult
    │         POST /mcp tools/* → routed via child stdin/stdout
    │
    ├─[MCP HTTP :8000]─────────────────────────────────────────────────────────┐
    │  Tools: hermes__ask_hermes_agent / conversations_list / messages_send/etc │
    │                                                                           ▼
    │                                                          hermes-agent-mcp.ai:8000
    │                                                                           │
    │                                                          Hermes — ns: ai, node: srv-rk1-nvme-01
    │                                                          ├─ LiteLLM proxy (razonamiento)
    │                                                          ├─ kubernetes MCP sidecar :8080
    │                                                          ├─ kagent MCP :8084  ← NetworkPolicy fix (ai ns)
    │                                                          └─ openclaw MCP :18790/mcp ←──┐
    │                                                                           │              │
    │                                                          Hermes razona                  │
    │                                                          y responde                     │
    │                                                                                         │
    └─[bridge.js stateful :18790]───────────────────────────────────────────────────────────┘
       session key fijo: "agent:main:main" (no lookup via conversations_list)
       sentAt timestamp: filtra eventos anteriores al mensaje enviado
       getEvents(): parsea structuredContent.events o text fallback (JSON)
       events_wait timeout: 60s (era 90s), hasta 3 intentos
       Tools: openclaw__ask_openclaw_agent / conversations_list / messages_send / etc.

Honcho (namespace: honcho, :80 → pod :8000)
    ├─ workspace "openclaw" — memoria de OpenClaw (peers, conversaciones)
    └─ workspace "hermes"   — memoria de Hermes
```

---

## Estado por dirección (2026-06-12)

| Dirección | Estado | Detalle |
|-----------|--------|---------|
| **OpenClaw → Hermes** | ✅ Operacional | `ask_hermes_agent` PONG en **9s** (era 37s). Hermes MCP stateless. |
| **Hermes → OpenClaw** | ✅ Operacional | bridge.js stateful: no supergateway. Session key fijo, sentAt filter, getEvents() helper. |
| **Audio STT (voz→texto)** | ✅ Operacional | whisper-stt in-cluster (2026-06-12). Fix: SSRF guard parcheado con `OPENCLAW_ALLOW_PRIVATE_MEDIA=1`. |
| **Audio TTS (texto→voz)** | ✅ Operacional | edge-tts Microsoft (OpenClaw: node-edge-tts; Hermes: edge-tts en PVC via initContainer). |
| **Honcho memoria** | ✅ Ambos | `[plugins] Honcho memory ready` en ambos pods. Peer map en PVC (no amnésico). |
| **Scope upgrade** | ✅ Resuelto | paired.json bypass aplicado (ver AGENTS.md) |

### Fix aplicado: Hermes MCP stateless (2026-06-11)

**Síntoma**: todas las herramientas `hermes__*` desde OpenClaw fallaban con `Session not found (-32600)` después de reiniciar Hermes, sin reiniciar OpenClaw. Error cada vez que Hermes se actualizaba o crasheaba.

**Causa raíz**: el MCP server de Hermes era **stateful** por defecto: guardaba una sesión en memoria por cada cliente `initialize`. OpenClaw cacheaba su `mcp-session-id` del primer handshake y no volvía a hacer `initialize` (el protocolo asume que las sesiones son persistentes). Un restart de Hermes borraba las sesiones en memoria → OpenClaw enviaba el session-id viejo → 404/error.

**Fix**: `server.settings.stateless_http = True` en `hermes-static-mcp.yaml.j2`. En modo stateless, el server no mantiene sesiones — cada POST `/mcp` es completamente independiente. El session-id de la cabecera `mcp-session-id` es ignorado.

**Por qué stateless es la elección correcta**: el A2A debe ser resiliente a reinicios en cualquier orden. Si Hermes y OpenClaw se reinician independientemente (actualizaciones, crashloops), no deberían necesitar coordinación manual. Stateless logra eso a costo cero en este caso de uso (una sola conexión, sin push asíncrono del server). El único trade-off es que las notificaciones push del server no funcionan — pero el messaging bridge no las usa.

### Fix aplicado: Hermes TTS edge-tts en PVC (2026-06-11)

**Síntoma**: `text_to_speech_tool()` fallaba con `no tts engine configured`. Los logs de Hermes mostraban que `lazy_deps.py` intentaba `pip install edge-tts` pero fallaba.

**Causa raíz**: el container de Hermes tiene `readOnlyRootFilesystem: true`. `lazy_deps.py` instala dependencias en el venv activo al ser invocado; como el venv está en la imagen (read-only), la instalación falla. No hay error visible — `lazy_deps` captura la excepción y el TTS simplemente no está disponible.

**Fix**: initContainer `install-tts` que instala `edge-tts==7.2.7` con `--no-deps` en el PVC (`/opt/data/pylibs`). El container principal lo ve via `PYTHONPATH=/opt/data/pylibs`.

**Por qué `--no-deps` es crítico**: `edge-tts` depende de `pydantic` (versión 2.13.4). Sin `--no-deps`, pip la arrastra al PVC. Como `PYTHONPATH` antepone `/opt/data/pylibs` al Python path, el pydantic 2.13.4 shadowea el 2.12.5 pineado de la imagen → `ImportError` en los módulos de Hermes → el agente no arranca. Con `--no-deps`, solo se instala `edge-tts` + `srt` + `tabulate` (sus deps de runtime que no están en la imagen). Verificado en vivo que el agente mantiene 2.12.5 y el TTS funciona.

**Por qué PVC y no emptyDir**: emptyDir se pierde en cada restart → la instalación se repite en cada boot (~30s). El PVC persiste la instalación; el initContainer hace un check `if [ ! -d pylibs/edge_tts ]` y sale en milisegundos si ya está instalado.

### Fix aplicado: audio STT SSRF guard (2026-06-12)

Ver `skills/openclaw/SKILL.md#audio--stt-voztexto-y-tts-textovoz` para la causa raíz completa.
Resumen: `whisper-stt.ai.svc.cluster.local` era bloqueada por el SSRF guard de OpenClaw
dos veces (sufijo `.local` + IP privada). El voice note se inlineaba crudo → context overflow.
Fix: sed patch al arrancar + `OPENCLAW_ALLOW_PRIVATE_MEDIA=1`.

El análisis completo está en `docs/audio-honcho-a2a-2026-06-12.md`.

### Fix aplicado: ask_hermes_agent timeout (2026-05-28, inicial)

**Síntoma**: `[tools] hermes__ask_hermes_agent failed: MCP error -32001: Request timed out`
**Causa**: AIAgent con max_iterations=90 + hermes-qwen (llama-3.1-8b NPU, 4096 token limit, ~30s/turno) → context overflow + excede timeout MCP
**Fix**: max_iterations=15 en hermes-static-mcp.yaml.j2 + kubectl patch directo
**Resultado esperado**: 2-3 turns × 30s = ~60-90s por debate, dentro del timeout de 600s de OpenClaw

### Fix aplicado: bridge.js askOpenclaw performance (2026-05-28)

**Síntoma**: `ask_openclaw_agent` tardaba 37s+ (visible en E2E test anterior)
**Causa raíz**:
1. `askOpenclaw` llamaba `conversations_list` para obtener el session key — round-trip innecesario
2. `waitForReply` sin filtro de timestamp — podía devolver eventos anteriores al mensaje (stale reply)
3. `getEvents()` ausente — código de parseo duplicado con try/catch frágil

**Fix** (en `bridge.js` embebido en `openclaw-deployment.yaml.j2`):
- Session key hardcodeado: `'agent:main:main'` (evita lookup)
- `sentAt = Date.now()` antes de `messages_send` → `waitForReply` solo acepta `ev.updatedAt >= sentAt`
- `getEvents(r)` helper: parsea `r.result.structuredContent.events` o text fallback (JSON)
- `events_wait timeout_ms`: 90000 → 60000 (3 intentos = 180s max)

**Resultado**: PONG en 9s (era 37s)

---

## Tests realizados (OpenClaw → Hermes) — todos ✅

### 1. Conectividad MCP (initialize)

```bash
# Desde pod openclaw → hermes-agent-mcp:8000
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  curl -s -X POST http://hermes-agent-mcp.ai.svc.cluster.local:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  -D /tmp/h.txt && grep -i mcp-session-id /tmp/h.txt
# → mcp-session-id: <uuid>
# → serverInfo: {"name":"hermes","version":"1.26.0"}
```

### 2. conversations_list ✅

```bash
SESSION=<uuid>
curl -X POST http://hermes-agent-mcp.ai.svc.cluster.local:8000/mcp \
  -H "mcp-session-id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"conversations_list","arguments":{"platform":"telegram","limit":10}}}'
# → session_key: "agent:main:telegram:dm:8492872858"
# → display_name: "villadalmine", chat_type: "dm"
```

### 3. messages_read ✅

```bash
curl ... -d '{"method":"tools/call","params":{"name":"messages_read","arguments":{
  "session_key": "agent:main:telegram:dm:8492872858", "limit": 5
}}}'
# → últimos 5 mensajes con role/content/timestamp/id
```

### 4. messages_send ✅ — pero es OUTGOING (del bot al usuario)

⚠️ **CRÍTICO — comportamiento real verificado:**
`messages_send` envía un mensaje FROM el bot de Hermes TO el usuario. Es **saliente**.
NO dispara el loop del agente de Hermes. **Para disparar razonamiento → usar `ask_hermes_agent`.**

### 5. events_poll ✅

⚠️ `events_poll` y `events_wait` esperan mensajes del USUARIO, no respuestas de Hermes.

### 6. ask_hermes_agent ✅ — DEBATE REAL CONFIRMADO

```bash
curl ... -d '{"method":"tools/call","params":{"name":"ask_hermes_agent","arguments":{
  "question": "DEBATE T1/2 — Tema: mejor storage para PVCs en K3s ARM64\nMi posición (OpenClaw): longhorn-nvme sobre NVMe en RK1 porque da replicación y failover. ¿Tu análisis?"
}}}'
# → Hermes razona con su LLM + kubernetes MCP + kagent
# → Devuelve análisis con tabla comparativa, recomendaciones por caso de uso
# → Tardó ~30s (normal para AIAgent completo)
```

---

## Tests realizados (Hermes → OpenClaw bridge)

### 1. Bridge endpoint accesible ✅

```bash
# Desde hermes pod: POST /mcp initialize
curl -s --max-time 5 -X POST http://openclaw.openclaw.svc.cluster.local:18790/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
# → event: message
# → data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{...}},"serverInfo":{"name":"openclaw","version":"2026.5.22"}}}

# GET /mcp (server notification channel — bridge responde con SSE keepalive vacío, no 405)
curl -sv --max-time 3 http://openclaw.openclaw.svc.cluster.local:18790/mcp 2>&1 | grep "HTTP/"
# → HTTP/1.1 200 OK  (no 405)
```

### 2. Hermes MCP: 3 servidores registrados ✅

```
kubectl logs -n ai deploy/hermes-agent-mcp -c hermes-agent | grep "registered.*tool\|server\(s\)"
# → registered 21 tool(s): (kubernetes)
# → registered 124 tool(s): (kagent)
# → registered 11 tool(s): (openclaw)  ← Hermes→OpenClaw operacional
# → MCP: registered 156 tool(s) from 3 server(s) (0 failed)
```

### 3. Diagnóstico rápido si falla

```bash
# Bridge logs
kubectl logs -n openclaw deploy/openclaw -c openclaw-mcp-bridge --tail=20
# Esperado: "[bridge] mcp serve ready, proto: 2024-11-05"
# Error: "[bridge] mcp serve exited code=..." → bridge auto-restarts en 3s

# Hermes MCP status
kubectl logs -n ai deploy/hermes-agent-mcp -c hermes-agent | grep -E "openclaw|failed|server\(s\)" | tail -5

# Test connectivity
kubectl exec -n ai deploy/hermes-agent-mcp -c hermes-agent -- \
  curl -s --max-time 5 -X POST http://openclaw.openclaw.svc.cluster.local:18790/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' | head -1
# Esperado: event: message
```

---

## Configuración deployed

### openclaw-mcp-bridge sidecar (openclaw-deployment.yaml.j2)

Stateful Node.js bridge (`/tmp/bridge.js`), no supergateway. Spawns `openclaw mcp serve` once, initializes it, routes all HTTP POST /mcp via stdio. GET /mcp → SSE keepalive. Child crash → auto-restart in 3s.

```
GET /mcp  → bridge returns 200 SSE keepalive (satisfies Python MCP SDK)
POST /mcp (initialize)     → bridge returns cached childInitResult immediately
POST /mcp (notifications/) → bridge returns 202, no round-trip
POST /mcp (tools/*)        → bridge routes to child stdin, returns stdout response
```

Key properties:
- **No auto-init overhead**: child initialized once at startup (~8s), subsequent tool calls are fast
- **No transport slot issue**: each HTTP request is independent, no SSE session state
- **Child restart**: bridge detects child exit, restarts in 3s, queued requests get error and retry

```yaml
- name: openclaw-mcp-bridge
  command: ["sh", "-c"]
  args:
    - |
      cat > /tmp/bridge.js << 'BRIDGEOF'
      # (stateful Node.js bridge — see openclaw-deployment.yaml.j2 for full source)
      # Spawns mcp serve, initializes once, HTTP server on BRIDGE_PORT
      BRIDGEOF
      GW_URL="ws://localhost:18789" GW_TOKEN="$OPENCLAW_GATEWAY_TOKEN" \
      BRIDGE_PORT="18790" node /tmp/bridge.js
```

### Hermes MCP config

```yaml
mcp_servers:
  kubernetes:
    url: http://127.0.0.1:8080/mcp
    timeout: 120
  kagent:
    url: http://kagent-tools.kagent.svc.cluster.local:8084/mcp
    timeout: 60
  openclaw:
    url: http://openclaw.openclaw.svc.cluster.local:18790/mcp   # stateful bridge
    timeout: 120
    connect_timeout: 30
```

### kagent-tools NetworkPolicy (openclaw-network.yaml.j2)

Allows `ai` namespace (Hermes) to reach kagent-tools MCP on port 8084. Without this, kagent MCP fails with i/o timeout from the Hermes pod.

```yaml
# in NetworkPolicy allow-openclaw-to-kagent-tools
- from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: ai
  ports:
    - port: 8084
```

---

## Scope Upgrade Bypass (CRÍTICO)

`openclaw mcp serve` necesita scopes `operator.read, operator.write, operator.approvals, operator.pairing`.
El token de gateway solo tiene `operator.write` → scope upgrade → deadlock.

**Fix:** editar `paired.json` directamente en el PVC para pre-aprobar los scopes. Documentado en `AGENTS.md` sección "OpenClaw MCP Bridge Deadlock Bypass".

```bash
# Verificar si el device está en paired.json:
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  node -e 'const d=JSON.parse(require("fs").readFileSync("/home/node/.openclaw/devices/paired.json"));
  console.log(JSON.stringify(Object.keys(d).map(k=>({k,scopes:d[k].scopes})),null,2))'
```

---

## NetworkPolicy — gotcha post-DNAT

**Honcho** escucha en puerto 8000 (pod port), pero el Service es puerto 80. Kubernetes evalúa NetworkPolicy DESPUÉS del DNAT, con el puerto real del pod.

```yaml
# CORRECTO (egress desde openclaw → honcho):
egress:
  - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: honcho
    ports:
      - port: 8000   # POD port, no Service port
        protocol: TCP
```

---

## Cómo probar desde Telegram

### 1. OpenClaw → Hermes (dirección 1)

```
Tú → @tito_es_tu_bot: "Consulta a Hermes sobre el estado de los pods en el namespace ai"
```
OpenClaw usa `ask_hermes_agent` → Hermes consulta kubernetes MCP → responde con análisis.

### 2. Debate bidireccional

```
Tú → @tito_es_tu_bot: "Inicia un debate con Hermes sobre si deberíamos migrar a longhorn para los PVCs de observabilidad"
```
OpenClaw debate con Hermes, síntesis final al usuario.

### 3. Hermes → OpenClaw (dirección 2)

```
Tú → Hermes (Telegram): "Consulta a Tito (OpenClaw) sobre qué conversaciones recientes tiene"
```
Hermes usa `ask_openclaw_agent` → OpenClaw responde (requiere que la sesión SSE esté activa).

---

## Diagnóstico rápido

```bash
# Estado de pods
kubectl get pods -n openclaw -o wide
kubectl get pods -n ai -l app=hermes-agent-mcp

# Restarts del bridge
kubectl get pod -n openclaw -o jsonpath='{range .status.containerStatuses[*]}{.name}: {.restartCount}{"\n"}{end}'

# Logs bridge (ver si while-true está funcionando)
kubectl logs -n openclaw deploy/openclaw -c openclaw-mcp-bridge --tail=20

# Logs gateway (scope upgrades, WS connections)
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  node -e 'require("fs").readFileSync("/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log","utf8").split("\n").filter(Boolean).forEach(l=>{try{const j=JSON.parse(l);console.log(j.time.slice(0,19),j.message.slice(0,100));}catch(e){}})' 2>/dev/null | grep -E "scope|ws|mcp|upgrade" | tail -20

# Hermes MCP connections
kubectl logs -n ai deploy/hermes-agent-mcp -c hermes-agent | grep -E "openclaw|connected|failed" | tail -20

# Test manual SSE desde hermes namespace
kubectl exec -n ai deploy/hermes-agent-mcp -c hermes-agent -- \
  curl -sN --max-time 3 http://openclaw.openclaw.svc.cluster.local:18790/sse -H "Accept: text/event-stream"
# Esperado: event: endpoint + data: /message?sessionId=<uuid>
```

---

## Bugs encontrados y resueltos

| Bug | Causa | Fix |
|-----|-------|-----|
| `Session not found (-32600)` en TODAS las tools hermes__* desde OpenClaw (2026-06-11) | El MCP server de Hermes era stateful: cada restart de Hermes borraba las sessions; OpenClaw cacheaba su `mcp-session-id` del initialize y NUNCA re-handshakea → todas las tool calls fallaban hasta reiniciar OpenClaw | `server.settings.stateless_http = True` en hermes-static-mcp.yaml.j2 — cada POST es independiente, el A2A sobrevive reinicios en cualquier orden. Verificado: tools/call con session-id inventada responde OK |
| Hermes sin server "openclaw" tras bootstrap completo | Hermes registra MCPs SOLO al arrancar (3 intentos) y en el bootstrap se despliega antes que OpenClaw | install-openclaw ahora reinicia hermes-agent-mcp al final (tasks A2A restart ordering) |
| Hermes "no TTS engine configured" | edge-tts no está en la imagen y lazy_deps instala en el venv (read-only rootfs) → falla silenciosamente | initContainer `install-tts` instala edge-tts==7.2.7 en el PVC (`/opt/data/pylibs`) + `PYTHONPATH`; config `tts.provider: edge` + `voice.auto_tts`. Baked en Dockerfile para el próximo rebuild |
| `Honcho NetworkPolicy` | K8s evalúa NetworkPolicy post-DNAT → puerto 8000 (pod), no 80 (service) | egress port 8000 en openclaw-network.yaml.j2 |
| `events_wait timeout` | messages_send es OUTGOING — no dispara Hermes | usar ask_hermes_agent por turno |
| `scope upgrade deadlock` | mcp serve necesita scopes que el token no tiene; approval requiere token → chicken-and-egg | paired.json bypass (AGENTS.md) |
| `Already connected to transport` | supergateway SSE: stale `mcp serve` child holds transport slot after clean disconnect; new client → crash | Cambiado a proxy+streamableHttp: GET manejado por proxy (sin transport slot) |
| `ask_hermes_agent timeout (-32001)` | max_iterations=90 + NPU lento → excede timeout MCP (~90s) | max_iterations=15 en hermes-static-mcp.yaml.j2 |
| `GET /mcp → 405` | supergateway stateless streamableHttp no soporta GET /mcp | Proxy Node.js en :18790 responde GET con SSE keepalive vacío; POST forwarded a supergateway:18791 |
| `Python mcp client CancelledError` | Cliente GET /mcp → 405 → TaskGroup falla | Fix: mismo que arriba (proxy maneja GET) |
| `kagent MCP timeout` | NetworkPolicy `allow-openclaw-to-kagent-tools` no incluía namespace `ai` | Añadido ingress from `ai` ns en openclaw-network.yaml.j2 |
| `LiteLLM fallbacks broken` | `deepseek-free` 429 rate-limited; `local-fast` en context_window_fallbacks (mismo límite NPU 4096 → inútil) | Reemplazado con `free2, deepseek4v-free, nemotron`; local-fast eliminado de context_window_fallbacks |
| `ask_openclaw_agent lento (37s)` | `askOpenclaw` llamaba `conversations_list` antes de cada `messages_send`; sin filtro de timestamp → stale events | Session key fijo `'agent:main:main'`; `sentAt` timestamp filter; `getEvents()` helper |

---

## Roadmap

| Fase | Descripción | Estado |
|------|-------------|--------|
| Fase 1 | OpenClaw → Hermes: ask_hermes_agent via MCP :8000 | ✅ Operacional |
| Fase 2 | Honcho compartido (ambos agentes usan misma instancia) | ✅ Operacional |
| Fase 3 | Hermes → OpenClaw: proxy+supergateway bridge :18790/mcp | ✅ Operacional |
| Fase 3.1 | Fix GET /mcp (Python MCP SDK): proxy Node.js maneja GET con SSE keepalive | ✅ Resuelto |
| Fase 3.2 | Fix kagent MCP (ai ns NetworkPolicy) + LiteLLM fallback chains | ✅ Resuelto |
| Fase 4 | Google A2A protocol (Agent Cards, push bidireccional) | ⬜ Backlog |
