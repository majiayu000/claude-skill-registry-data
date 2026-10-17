---
name: openclaw
description: >
  OpenClaw personal AI gateway — orquestador principal que habla con Holmes, Kagent y Hermes
  como subagentes. Todo el tráfico LLM pasa por LiteLLM (nunca directo a OpenRouter).
  RBAC readonly sin acceso a Secrets. kubernetes-mcp sidecar para visibilidad del cluster.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  author: dotfiles
  tags: [kubernetes, ai, openclaw, telegram, litellm, openrouter, rbac, arm64, orchestrator]
---

# OpenClaw Skill

## ¿Qué es OpenClaw?

`openclaw/openclaw` — gateway de IA personal (TypeScript). Servidor en puerto 18789,
conecta canales (Telegram) y rutea a cualquier backend LLM. Imagen oficial multi-arch (arm64 ✅).

- Docs: https://docs.openclaw.ai / K8s: https://docs.openclaw.ai/install/kubernetes
- **Sin Helm chart.** Upstream usa Kustomize. Este rol usa Jinja2, consistente con el repo.

---

## Arquitectura (estado actual)

```
Usuario (Telegram)
      │
      ▼
┌─────────────────────────────────────────────────┐
│  Namespace: openclaw                            │
│                                                 │
│  Deployment/openclaw                            │
│  ├─ initContainer: init-config (busybox)        │
│  │   copia ConfigMap → PVC en cada restart      │
│  ├─ container: openclaw-gateway :18789          │
│  │   OPENAI_API_BASE → litellm-proxy.ai:4000    │
│  │   OPENAI_API_KEY  → sk-hermes-internal       │
│  └─ container: kubernetes-mcp (sidecar :8080)   │
│      kubernetes-mcp-server v0.0.60              │
│      expone /mcp vía HTTP en localhost           │
│                                                 │
│  PVC: openclaw-data (10Gi smb-nas)              │
│  ConfigMap: openclaw-config                     │
│    ├─ openclaw.json  (gateway + model + mcp)    │
│    └─ AGENTS.md      (system prompt completo)   │
│  Secret: openclaw-secrets                       │
│    ├─ OPENCLAW_GATEWAY_TOKEN                    │
│    ├─ TELEGRAM_BOT_TOKEN (token propio)         │
│    └─ TELEGRAM_ALLOWED_USERS                    │
│                                                 │
│  Service/openclaw  → ClusterIP :18789           │
│  HTTPRoute         → openclaw.cluster.home      │
│  NetworkPolicy     → egress controlado          │
│  ServiceAccount    → openclaw (readonly+net)    │
└──────┬──────────────────────┬───────────────────┘
       │ OPENAI_API_BASE       │ localhost:8080/mcp
       ▼                       ▼
┌─────────────────┐   ┌──────────────────────┐
│ ai/litellm-proxy│   │ kubernetes API (RBAC) │
│ gpt-4o alias    │   │ readonly, sin Secrets │
│ → gpt-oss-120b  │   └──────────────────────┘
└────────┬────────┘
         │ OPENCLAW_OPENROUTER_API_KEY (nunca expuesta al pod)
         ▼
    OpenRouter API
```

---

## Routing LLM — cadena completa

| Capa | Valor |
|------|-------|
| Config (`openclaw_model_primary`) | `litellm/openclaw-gemini` |
| LiteLLM alias `openclaw-gemini` primario | `openrouter/google/gemma-4-31b-it:free` (OPENROUTER key) |
| LiteLLM alias `openclaw-gemini` secundario | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` (OPENCLAW key) |
| Fallback chain | `gemma4-free → free2 → deepseek4v-free` |
| Key en OpenRouter | `OPENCLAW_OPENROUTER_API_KEY` (solo en `ai/litellm-secrets`) |

**OpenClaw nunca ve la API key de OpenRouter.** Solo conoce `sk-hermes-internal`.

### `drop_params: true` — obligatorio para modelos no-Claude

OpenClaw envía `thinking=medium` a LiteLLM. Los modelos no-Anthropic no soportan
el parámetro `thinking` y pueden devolver respuesta vacía (HTTP 200 con content=null)
en lugar de error 400. Resultado: LiteLLM NO activa el fallback, y OpenClaw detecta
`empty response detected` y reintenta una vez.

**Fix**: `drop_params: true` en cada entrada de `openclaw-gemini` en LiteLLM:
```yaml
- model_name: openclaw-gemini
  litellm_params:
    model: openrouter/google/gemma-4-31b-it:free
    api_key: os.environ/OPENROUTER_API_KEY
    drop_params: true   # ← crítico: elimina thinking/budget_tokens
```

Diferencia de `modify_params: true` (global, solo convierte params Anthropic→OpenAI)
vs `drop_params: true` (por modelo, elimina params desconocidos antes de enviar).

### Bug fix: `openai/` prefix + `api_base` (no `openrouter/`)

LiteLLM 1.82.x tiene un bug en `/v1/messages` (Anthropic passthrough): emite
`message_start` dos veces → `Unexpected event order` en el stream parser de OpenClaw.

**Fix**: usar `model: openai/<modelo>` + `api_base: https://openrouter.ai/api/v1`
en vez de `model: openrouter/<modelo>`. Fuerza `/v1/chat/completions` (OpenAI-compat).

Env var en el Deployment de LiteLLM:
```yaml
LITELLM_USE_CHAT_COMPLETIONS_URL_FOR_ANTHROPIC_MESSAGES: "true"
```

### Prefijo `openai/` automático

OpenClaw añade `openai/` a cualquier modelo sin provider prefix. Si config tiene
`gpt-5.4`, lo envía como `openai/gpt-5.4`. LiteLLM necesita alias con ese nombre exacto.
Usar `litellm/gpt-4o` en config evita el warning `[model-selection] Falling back to openai/...`.

---

## kubernetes-mcp sidecar

Sidecar `kubernetes-mcp-server:v0.0.60` en el mismo pod. Mismo patrón que Hermes Agent.

- Expone MCP en `http://127.0.0.1:8080/mcp`
- Genera kubeconfig desde el ServiceAccount token al arrancar
- RBAC: readonly sin Secrets (ver sección RBAC)

En `openclaw.json`:
```json
"mcpServers": {
  "kubernetes": {
    "url": "http://127.0.0.1:8080/mcp",
    "timeout": 120
  }
}
```

---

## RBAC — readonly extendido (sin Secrets)

**Regla de oro: ningún nivel permite leer `secrets` excepto `cluster-admin`.**

### Nivel actual: `readonly`

Recursos con `get/list/watch`:
- Core: pods, pods/log, services, endpoints, namespaces, nodes, events, configmaps, PVCs, PVs
- Apps: deployments, replicasets, statefulsets, daemonsets
- Batch: jobs, cronjobs
- Network: networkpolicies (networking.k8s.io)
- Cilium: networkpolicies, clusterwidenetworkpolicies, endpoints, identities, LBIPPools, L2Policies
- Gateway: httproutes, gateways, grpcroutes

### Cambiar nivel
```bash
# Operator (añade exec/logs + create/patch deployments/jobs)
ansible-playbook playbooks/bootstrap.yml --tags openclaw \
  -e "openclaw_rbac_level=operator"

# Volver a readonly
ansible-playbook playbooks/bootstrap.yml --tags openclaw
```

### Verificar
```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:openclaw:openclaw -n ai
# → no

kubectl auth can-i list networkpolicies \
  --as=system:serviceaccount:openclaw:openclaw
# → yes
```

---

## MCP Servers (subagentes activos)

| Nombre | URL | Transport | Propósito |
|--------|-----|-----------|-----------|
| `kubernetes` | `http://127.0.0.1:8080/mcp` | `streamable-http` | Cluster inspection (sidecar local) |
| `kagent` | `http://kagent-tools.kagent.svc.cluster.local:8084/mcp` | `streamable-http` | kubectl/helm via kagent-tools |

**holmes fue eliminado** — holmesgpt solo expone REST (`/api/chat`, `/api/model`), no MCP.
**hermes** — activo en puerto 8000 (messaging bridge MCP). Ver `skills/a2a/SKILL.md`.

Transport confirmado:
- `kubernetes-mcp-server`: responde a POST `/mcp` con `Content-Type: application/json` → **streamable-http**
- `kagent-tools`: kagent-controller usa `Post http://kagent-tools.kagent:8084/mcp` → **streamable-http**
- SSE (`/sse`) funciona para kubectl manual pero OpenClaw necesita streamable-http para cargar tools

---

## A2A MCP Bridge — Hermes→OpenClaw (bridge.js en :18790)

OpenClaw expone sus propias herramientas MCP para que Hermes las consuma. Esto se implementa con
un bridge stateful Node.js que corre como proceso secundario dentro del container openclaw-gateway.

```
Hermes ──[POST /mcp]──► bridge.js :18790 ──[stdio]──► openclaw mcp serve (child process)
       ──[GET /mcp]──► bridge.js devuelve 200 SSE keepalive (Python MCP SDK lo requiere)
```

### Por qué bridge.js (no supergateway)

Se evaluaron tres diseños — el historial de bugs es importante:

1. **supergateway SSE mode** — descartado: race condition cuando el pod de Hermes se reinicia.
   El pod viejo hace un clean disconnect pero el `mcp serve` hijo retiene el "transport slot";
   el nuevo pod falla con "Already connected to a transport" → supergateway crashea.

2. **supergateway streamableHttp + proxy Node.js** — descartado: supergateway stateless
   reinicializa `mcp serve` en CADA POST (no solo `initialize`). Cada reinit tarda ~8s
   (reconectar WS a openclaw gateway + registrar 100+ tools). Con connect_timeout=30s esto
   causa TimeoutError antes de que tools/list retorne.

3. **bridge.js stateful** ✅ — `mcp serve` se inicia UNA VEZ al arrancar el container.
   Initialize handshake se hace en startup y el resultado se cachea. Todos los tool calls
   van al hijo ya-inicializado via stdio. Sin overhead de reinit, sin race conditions.

### Diagrama bridge.js

```
Container startup:
  bridge.js ──[spawn]──► mcp serve ──[WS]──► openclaw gateway
               ──[stdio initialize]──► handshake (una vez)
               ──[stdio notifications/initialized]──► ready

HTTP requests from Hermes:
  POST /mcp (initialize)    → devuelve childInitResult cacheado
  POST /mcp (tools/list)    → forwarded via child.stdin → response via readline
  POST /mcp (tools/call)    → forwarded via child.stdin → response via readline
  GET  /mcp                 → 200 SSE keepalive vacío (Python MCP SDK satisfied)
  POST /mcp (notifications) → 202 swallowed (no llegan al hijo)
```

### Configuración relevante

```yaml
# roles/install-openclaw/defaults/main.yml
openclaw_mcp_bridge_enabled: true
openclaw_mcp_bridge_port: 18790    # port donde escucha bridge.js

# roles/install-hermes-agent/defaults/main.yml
hermes_openclaw_mcp_url: "http://openclaw.openclaw.svc.cluster.local:18790/mcp"
hermes_openclaw_mcp_timeout: 120
hermes_openclaw_mcp_connect_timeout: 30
```

### Verificar el bridge

```bash
# Desde dentro del pod openclaw
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  wget -qO- http://localhost:18790/mcp \
  --post-data='{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  --header='Content-Type: application/json'
# → {"jsonrpc":"2.0","id":1,"result":{"tools":[...]}}

# Logs del bridge (aparecen en stderr del container)
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway | grep '\[bridge\]'
# → [bridge] :18790 ready
# → [bridge] mcp serve ready, proto: 2024-11-05

# Desde Hermes — verificar que ve las tools de openclaw
kubectl exec -n ai deploy/hermes-agent-mcp -c hermes-agent -- \
  wget -qO- --timeout=10 http://openclaw.openclaw.svc.cluster.local:18790/mcp \
  --post-data='{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  --header='Content-Type: application/json' | head -c 300
```

Ver `skills/a2a/SKILL.md` para documentación completa del bridge A2A bidireccional.

---

## NetworkPolicy — egress (openclaw namespace)

| Destino | Puerto | Propósito |
|---------|--------|-----------|
| DNS | 53 UDP/TCP | Resolución de nombres |
| `ai/litellm-proxy` | 4000 TCP | Todo el tráfico LLM (service=targetPort) |
| `kagent/*` | 8084 TCP | kagent-tools MCP (service=targetPort) |
| `ai/hermes-agent-mcp` | 8000 TCP | Hermes MCP (service=targetPort) |
| `honcho/*` | **8000** TCP | Honcho memory API (service port 80 → pod targetPort 8000) |
| `monitoring/*` | 9090 TCP | Prometheus queries |
| External HTTPS | 443 TCP | Telegram API |
| K8s API server | 6443 TCP | RBAC / kubectl via SA |
| `192.168.178.0/24` | 80,443,8080,554 TCP | Red home (análisis read-only) |

**Cilium DNAT — regla crítica:** Cilium evalúa NetworkPolicy DESPUÉS del DNAT.
Siempre usar el **targetPort del pod**, no el port del Service.

- Honcho: Service `80` → targetPort **`8000`** → NetworkPolicy usa `8000`
- LiteLLM / Kagent / Hermes: service port = targetPort → no hay diferencia

**Trampa con debug pods:** un pod sin `app=openclaw` label no tiene la NetworkPolicy
aplicada y puede conectar aunque el pod real no pueda. Siempre testear la conectividad
con `--labels="app=openclaw"` para simular el entorno real:

```bash
kubectl run -n openclaw nw-test --restart=Never --image=curlimages/curl \
  --labels="app=openclaw" \
  --command -- sh -c 'curl -s --max-time 8 http://honcho-api.honcho.svc.cluster.local/health; echo EXIT:$?'
sleep 12; kubectl logs -n openclaw nw-test; kubectl delete pod -n openclaw nw-test
# EXIT:0 = OK, EXIT:28 = NetworkPolicy bloqueando
```

NetworkPolicy también tiene **ingress** desde `monitoring` en port 18789 para
recibir webhooks de AlertManager.

### NetworkPolicy cross-namespace (kagent)

`kagent-tools` vive en el namespace `kagent`. Se necesita una NetworkPolicy de **ingress** en ese namespace:

```yaml
# Desplegada por install-openclaw (openclaw-network.yaml.j2)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-openclaw-to-kagent-tools
  namespace: kagent          # ← namespace destino, no openclaw
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: kagent-tools
  policyTypes:
    - Ingress
  ingress:
    - from:                  # kagent-controller (mismo namespace)
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kagent
      ports:
        - port: 8084
    - from:                  # openclaw gateway
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: openclaw
      ports:
        - port: 8084
```

**Trampa:** añadir una NetworkPolicy con podSelector activa enforcement en ese pod.
Si solo permites openclaw, el `kagent-controller` queda bloqueado → falla reconciliación de MCPServer CRDs cada 2 min.

---

## Honcho — Memoria persistente

OpenClaw usa el plugin `openclaw-honcho` para memoria de conversación persistente.
La memoria está en el **workspace `openclaw`** del Honcho self-hosted en namespace `honcho`.

### Configuración en `openclaw.json` (ConfigMap)

```json
"plugins": {
  "allow": ["openclaw-honcho"],
  "entries": {
    "openclaw-honcho": {
      "enabled": true,
      "config": {
        "baseUrl": "http://honcho-api.honcho.svc.cluster.local",
        "apiKey": "<workspace-scoped-jwt>",
        "workspaceId": "openclaw",
        "timeoutMs": 30000
      }
    }
  },
  "slots": {"memory": "openclaw-honcho"}
}
```

### Variables Ansible relevantes

| Variable | Valor default | Descripción |
|----------|--------------|-------------|
| `openclaw_honcho_url` | `http://honcho-api.honcho.svc.cluster.local` | URL del API |
| `openclaw_honcho_workspace` | `openclaw` | Workspace ID |
| `openclaw_honcho_timeout_ms` | `30000` | Timeout en ms |
| `openclaw_honcho_api_key` | en `secrets.yml` | JWT workspace-scoped |

### Verificación

```bash
# Honcho memory cargó correctamente
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway | grep -i honcho
# → "Honcho memory ready — peer map: /home/node/.honcho/openclaw-peers.json (N known senders)"

# Si falla: "Failed to initialize Honcho: ConnectionError"
# → Verificar NetworkPolicy (port 8000, no 80) y que honcho-api esté Running
```

Ver `skills/honcho/SKILL.md` para arquitectura completa, JWT auth y troubleshooting.

---

## Telegram

### Token propio (separado de Hermes)
OpenClaw debe tener su propio bot token. Solo un proceso puede hacer polling por token.
Hermes está a 0 réplicas mientras OpenClaw usa el token compartido temporal.
**Próximo paso:** crear bot nuevo en `@BotFather` y actualizar `secrets.yml`.

### health-monitor 120s
Si Telegram no conecta en 120s, el health-monitor mata el proceso → CrashLoopBackOff.
Para debug sin Telegram: `openclaw_telegram_enabled: false` en defaults antes del deploy.

---

## Init container (versión actual — busybox copy)

```yaml
initContainers:
  - name: init-config
    image: busybox:1.36
    command: [sh, -c, |
      mkdir -p /home/node/.openclaw
      cp /etc/openclaw/openclaw.json /home/node/.openclaw/openclaw.json
      chown 1000:1000 /home/node/.openclaw/openclaw.json || true
    ]
```

**No usar** el patrón anterior con `onboard` — regeneraba el config ignorando el ConfigMap.

---

## Audio — STT (voz→texto) y TTS (texto→voz)

OpenClaw soporta audio bidireccional via Telegram: voice notes entrantes se transcriben,
y si configuraste TTS, las respuestas salen también como audio.

### Arquitectura de audio

```
Telegram voice note (OGG/Opus)
  → OpenClaw tools.media.audio (provider "openai", baseUrl custom)
  → http://whisper-stt.ai.svc.cluster.local:9000/v1/audio/transcriptions
  → transcript reemplaza el body del mensaje

Respuesta de texto
  → messages.tts (provider "microsoft", voz es-AR-TomasNeural)
  → node-edge-tts → voice note Telegram
```

### SSRF Guard — el bloqueo oculto de ClusterIP privadas

**Causa raíz del fallo de STT** (descubierta 2026-06-12): OpenClaw tiene un guard SSRF
(`isBlockedHostnameOrIp` en `dist/ssrf-*.js`) que bloquea **silenciosamente** cualquier
request a hostnames `.local` o IPs privadas. `whisper-stt.ai.svc.cluster.local` activa
el bloqueo DOS veces: por sufijo `.local` + por la IP de ClusterIP.

**El resultado sin fix**: el voice note no se transcribe — se inlinea crudo en el prompt
(~267k tokens) → `Context overflow` → el agente responde "no puedo procesar audio".
No aparece ningún error en los logs; parece que el agent simplemente no puede procesar audio.

**Fix**: env var `OPENCLAW_ALLOW_PRIVATE_MEDIA=1` + sed patch al arranque del gateway que
cortocircuita `isBlockedHostnameOrIp` cuando esa var está seteada.

**Por qué sed en lugar de fix upstream**: no tenemos acceso al código fuente ni podemos
hacer rebuild (la imagen se buildea con kaniko en el cluster, el proceso tarda 15+ min).
El schema `MediaUnderstandingModelSchema` tampoco tiene `allowPrivateNetwork` (solo existe
en el schema de modelos LLM, no de media). El patch sed es frágil pero verificable:
busca el patrón exacto y falla gently (`|| true`) si no lo encuentra.

### `apiKey` en media.audio — campo inválido (NUNCA)

El schema del gateway es `.strict()`. El bloque `tools.media.audio.models[]` NO acepta
`apiKey`. Poner `"apiKey": "cualquier-cosa"` invalida el entry entero → el gateway no arranca.
Si el server STT exigiera auth: usar `headers: {"Authorization": "Bearer <key>"}` (sí está en el schema).

### Variables Ansible para audio

| Var | Default | Nota |
|-----|---------|------|
| `openclaw_audio_stt_enabled` | `false` | Activa el SSRF patch + config STT |
| `openclaw_stt_base_url` | `http://whisper-stt.ai.svc.cluster.local:9000/v1` | Endpoint interno Whisper |
| `openclaw_tts_auto` | `inbound` | `always`=siempre audio, `off`=desactivar |
| `openclaw_tts_voice` | `es-AR-TomasNeural` | Cualquier voz Edge neural |

**TTS 100% local (piper)**: no es posible con la imagen actual. El único speech provider
implementado es `microsoft` (alias `edge`, cloud-gratis). Para TTS local hace falta rebuild.

### Verificación

```bash
# El pod tiene OPENCLAW_ALLOW_PRIVATE_MEDIA=1
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- env | grep PRIVATE
# → OPENCLAW_ALLOW_PRIVATE_MEDIA=1

# El patch SSRF se aplicó al arrancar
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway | grep ssrf-patch
# → [ssrf-patch] isBlockedHostnameOrIp cortocircuitado en ssrf-*.js

# Test real: transcribir desde dentro del pod
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  node -e 'const fs=require("fs"),https=require("https"),http=require("http");
    const buf=Buffer.from("RIFF..."); // audio de prueba
    console.log("seria largo, mejor con node infer audio")'
# Más fácil: enviar un voice note real por Telegram y ver los logs:
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway --follow | grep -i "audio\|transcript\|stt"
```

---

## Smee Webhook Relay (container smee-client)

**Qué hace**: escucha el canal Smee (`openclaw_smee_url`) y re-formatea los webhooks
de GitHub Actions como mensajes Telegram enviados via OpenClaw CLI.

**Por qué un container separado (no un plugin)**: el CLI de OpenClaw (`openclaw message send`)
es la forma canónica de inyectar mensajes sin usar el gateway HTTP. Usar un plugin requeriría
rebuild de imagen; el container extra es declarativo y se despliega con Ansible.

**Por qué Smee y no un webhook directo**: el cluster usa Cilium L2 + IP pública dinámica.
Smee.io actúa como relay estable. No es ideal para producción (punto de fallo externo), pero
para notificaciones de CI es aceptable. La alternativa correcta sería un tunnel (ngrok/cloudflare)
o un Ingress con IP estática.

```bash
# Ver webhook relay
kubectl logs -n openclaw deploy/openclaw -c smee-client --tail=20
# Esperado: "Smee adapter listening on port 18000..."
```

---

## Troubleshooting — MCP connectivity

### ¿Está cargando tools del MCP?

```bash
# Ver si [bundle-mcp] logró conectar en startup
kubectl exec -n openclaw <pod> -c openclaw-gateway -- \
  sh -c "grep 'bundle-mcp' /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
# Sin output = conectó silenciosamente (kubernetes con streamable-http no loguea éxito)
# Con "failed to start server X" = falló

# Ver qué tool calls hace el agente en tiempo real
kubectl logs -n openclaw -l app=openclaw -c openclaw-gateway --follow \
  | grep -E 'tool|mcp|bundle'

# Verificar config MCP que tiene el pod en este momento
kubectl exec -n openclaw <pod> -c openclaw-gateway -- \
  sh -c "cat /home/node/.openclaw/openclaw.json" | python3 -m json.tool | grep -A5 '"mcp"'
```

### MCP kubernetes no carga tools (tools: [])

```bash
# 1. Verificar que el sidecar responde streamable-http
kubectl exec -n openclaw <pod> -c openclaw-gateway -- \
  sh -c 'curl -s -X POST http://127.0.0.1:8080/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"test\",\"version\":\"1.0\"}}}" \
    | head -c 200'
# Debe devolver: event: message\ndata: {"jsonrpc":"2.0","id":1,"result":...}

# 2. Verificar que openclaw.json tiene transport correcto
# Debe tener: "url": "http://127.0.0.1:8080/mcp", "transport": "streamable-http"
# NO "url": ".../sse" (SSE da 400 en /mcp con GET)
```

### MCP kagent falla con "Connect Timeout Error"

```bash
# 1. Verificar NetworkPolicy en kagent namespace
kubectl get networkpolicy -n kagent

# 2. Si existe allow-openclaw-to-kagent-tools, verificar que permite kagent interno también
kubectl get networkpolicy allow-openclaw-to-kagent-tools -n kagent -o yaml | grep -A5 'ingress'
# Debe haber DOS reglas: una para namespace kagent, otra para namespace openclaw

# 3. Ver si kagent-controller también falla (confirma que la NP bloqueó el tráfico interno)
kubectl logs -n kagent deploy/kagent-controller --tail=10 | grep error

# 4. Confirmar egress de openclaw hacia puerto 8084
kubectl get networkpolicy openclaw-egress -n openclaw -o yaml | grep 8084
```

### Trampa NetworkPolicy cross-namespace

Al crear una NetworkPolicy con `podSelector` en un namespace ajeno, **se activa enforcement**
y se bloquea todo el tráfico no explícitamente permitido — incluido el del controlador interno.

**Síntoma:** `kagent-controller` loguea cada 2min:
```
"error":"Post http://kagent-tools.kagent:8084/mcp: i/o timeout"
```
**Fix:** añadir en la misma NetworkPolicy un `from: namespaceSelector: kagent`.

### ¿Qué MCP está usando el bot al responder?

```bash
# Seguir el log file en tiempo real mientras hablas por Telegram
kubectl exec -n openclaw $(kubectl get pod -n openclaw -l app=openclaw -o name | head -1) \
  -c openclaw-gateway -- \
  sh -c "tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log" \
  | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        msg = d.get('1', '')
        if any(k in str(msg).lower() for k in ['tool', 'mcp', 'kagent', 'kubernetes', 'call']):
            print(msg)
    except: pass
"
```

Si ves `kubernetes_*` tool calls → usa el sidecar kubernetes-mcp.
Si ves `kagent_*` o herramientas de helm/kubectl → usa kagent-tools MCP.

## Gotchas conocidos

| Problema | Causa | Fix |
|----------|-------|-----|
| CrashLoop a los 120s exactos | Telegram no conecta → health-monitor mata el proceso | Token válido o `telegram_enabled: false` |
| `Unknown model: openai/X` | LiteLLM no tiene alias `openai/X` | Añadir entry con ese nombre en litellm tasks |
| ConfigMap no recarga en caliente | subPath mount no propaga updates | Rollout restart (el checksum annotation lo fuerza) |
| `ai-hermes-deploy` levanta Hermes | Tag cubre litellm + hermes | Usar `--skip-tags ai-hermes-agent` |
| 429 en todos los modelos :free | Rate limit OpenRouter por key | Fallback a nemotron (más estable) |
| `message_start` error en stream | Bug LiteLLM `/v1/messages` doble emit | `openai/` prefix + `api_base` + env var |
| MCP tools no cargan, `tools: []` | Transport SSE en vez de streamable-http | `"transport": "streamable-http"` + URL `/mcp` |
| kagent-controller falla con i/o timeout | NetworkPolicy de ingress solo permite openclaw | Añadir regla `from: namespace kagent` en la misma NP |
| ask_openclaw_agent lento o stale reply | bridge.js buscaba session key en cada call; sin sentAt filter | Session key `'agent:main:main'` fijo + `sentAt` timestamp en waitForReply |

---

## Deploy

```bash
# Prerequisitos
cp roles/install-openclaw/defaults/secrets.yml.example \
   roles/install-openclaw/defaults/secrets.yml
vim roles/install-openclaw/defaults/secrets.yml  # token Telegram + gateway token

# Deploy
make openclaw

# Solo litellm sin tocar Hermes
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
  --tags ai-hermes-deploy --skip-tags ai-hermes-agent
```

---

## Verificación post-deploy

```bash
# 1. Pod tiene 2 containers (gateway + kubernetes-mcp sidecar)
kubectl get pod -n openclaw -l app=openclaw \
  -o jsonpath='{.items[0].spec.containers[*].name}'
# → openclaw-gateway kubernetes-mcp

# 2. No hay OPENROUTER_API_KEY expuesta al pod
kubectl exec -n openclaw <pod> -- env | grep -E "OPENAI|OPENROUTER"
# → OPENAI_API_BASE=http://litellm-proxy... OPENAI_API_KEY=sk-hermes-internal

# 3. LiteLLM responde para openclaw
kubectl exec -n openclaw <pod> -- sh -c \
  'curl -s -X POST http://litellm-proxy.ai.svc.cluster.local:4000/v1/chat/completions \
   -H "Authorization: Bearer sk-hermes-internal" \
   -H "Content-Type: application/json" \
   -d "{\"model\":\"openai/gpt-4o\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":5}" \
   | grep -o "\"model\":\"[^\"]*\""'
# → "model":"nvidia/..." o "model":"gpt-oss-..."

# 4. kubernetes-mcp sidecar responde
kubectl exec -n openclaw <pod> -c kubernetes-mcp -- \
  wget -qO- http://localhost:8080/mcp | head -c 100

# 5. RBAC: NO puede leer secrets
kubectl auth can-i get secrets \
  --as=system:serviceaccount:openclaw:openclaw -n ai
# → no
```

---

## Acceso

```bash
# Web UI
https://openclaw.cluster.home

# Gateway token
kubectl get secret openclaw-secrets -n openclaw \
  -o jsonpath='{.data.OPENCLAW_GATEWAY_TOKEN}' | base64 -d

# Port-forward
kubectl port-forward -n openclaw svc/openclaw 18789:18789
```

---

## Grafana

```bash
# Tráfico OpenClaw en LiteLLM dashboard
# Dashboard: "LiteLLM AI Traffic" → filter model=~"openai/gpt-4o|openclaw-.*"

kubectl port-forward -n ai svc/litellm-proxy 4000:4000 &
curl http://localhost:4000/spend/logs \
  -H "Authorization: Bearer sk-hermes-internal" | jq '.[-5:]'
```

---

## Arquitectura multi-agente (estado actual)

```
Usuario (Telegram)
    │
    ▼
OpenClaw (orquestador)
    ├── kubernetes MCP (sidecar :8080)  → cluster inspection (read-only)
    ├── Kagent  MCP (:8084)             → kubectl, helm, Cilium, Prometheus
    └── Hermes  MCP (:8000) ✅ ONLINE  → messaging bridge + agente autónomo
```

### Canal A2A con Hermes — messaging bridge (E2E 13/13 PASS 2026-05-28)

Hermes expone un **messaging bridge MCP completo** en puerto 8000. OpenClaw puede:
- `conversations_list` → ver qué conversaciones Telegram tiene Hermes activas
- `messages_send(target, message)` → enviar un mensaje real al chat de Hermes
- `events_poll(session_key, cursor)` → leer respuestas de Hermes
- `ask_hermes_agent(question)` → delegar al loop autónomo completo de Hermes (PONG 9s)

**Diferencia vs tool calling clásico:** `messages_send` hace que Hermes reciba el mensaje
como si fuera del usuario — procesa con su LLM + kubernetes MCP + kagent MCP y responde
autónomamente. No es una función, es un agente razonando.

**Bidireccional activo:** bridge.js stateful en `:18790` — Hermes puede llamar `ask_openclaw_agent`.
Session key fijo `'agent:main:main'`, sentAt filter (evita stale replies), getEvents() helper.

Ver `skills/a2a/SKILL.md` para arquitectura completa, tests y roadmap.

### AlertManager → OpenClaw (pendiente)
```yaml
# kube-prometheus-stack values
alertmanager:
  config:
    receivers:
      - name: openclaw-webhook
        webhook_configs:
          - url: "http://openclaw.openclaw.svc.cluster.local:18789/webhook/alertmanager"
            send_resolved: true
```

Flujo: AlertManager → OpenClaw → llama a Holmes (investiga) → resume → Telegram.

### Red home y análisis de seguridad (read-only)
NetworkPolicy permite egress a `192.168.178.0/24`. OpenClaw puede:
- Consultar dispositivos (Hue, cámaras ONVIF, NAS)
- Analizar tráfico vía Prometheus/Cilium metrics
- **No puede escribir ni actuar** en esta fase (todo read-only)

---

## Storage

| Var | Default | Override |
|-----|---------|----------|
| `openclaw_storage_class` | `smb-nas` | `local-path` |
| `openclaw_storage_size` | `10Gi` | any |

---

## Stale Spool Lock — bug PID 1 en contenedores (2026-06-01)

### Síntoma
OpenClaw arranca, recibe mensajes de Telegram (aparecen en el log como
`Inbound message`), pero NO responde. El spool tiene archivos `*.processing`.

### Causa raíz
OpenClaw usa un archivo `*.processing` como lock mientras procesa un mensaje.
Al terminar, lo elimina. Si el pod se reinicia mientras procesa, el archivo queda.

En contenedores, **el proceso principal siempre tiene PID 1**. OpenClaw verifica
si el proceso que creó el lock sigue vivo consultando si el PID registrado existe.
Como PID 1 siempre existe en el nuevo pod, el lock nunca se detecta como stale.

**Resultado**: el queue de mensajes queda bloqueado indefinidamente en cada restart.

### Fix permanente (initContainer)

`openclaw-deployment.yaml.j2` tiene un initContainer `init-config` (busybox) que
ahora incluye:
```sh
find /home/node/.openclaw/telegram -name '*.processing' -type f 2>/dev/null | while read f; do
  mv "$f" "${f%.processing}" && echo "Released stale spool lock: $f"
done || true
```
Convierte `*.processing → *.json` antes de que OpenClaw arranque → queue drena normal.

### Fix manual (si el pod ya está atascado)

```bash
# Ver locks stale
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  ls /home/node/.openclaw/telegram/ingress-spool-default/

# Liberar el lock (renombrar, no borrar — para que OpenClaw procese el mensaje)
kubectl exec -n openclaw deploy/openclaw -c openclaw-gateway -- \
  mv /home/node/.openclaw/telegram/ingress-spool-default/XXXXXXXXX.json.processing \
     /home/node/.openclaw/telegram/ingress-spool-default/XXXXXXXXX.json
```
Tras el rename, OpenClaw detecta el archivo y lo procesa en segundos.

### Nota sobre LiteLLM restart + Undici pool

Cada vez que LiteLLM se reinicia, el pool HTTP de OpenClaw (Undici/Node.js)
queda stale y las llamadas al modelo fallan con ECONNREFUSED.
**Regla**: siempre reiniciar OpenClaw inmediatamente después de reiniciar LiteLLM.

---

## Honcho — Integración memoria

`openclaw-honcho` plugin activado en `plugins.slots.memory`.

| Var | Valor |
|-----|-------|
| `openclaw_honcho_url` | `http://honcho-api.honcho.svc.cluster.local` |
| `openclaw_honcho_workspace` | `openclaw` |
| `openclaw_honcho_timeout_ms` | `90000` (90s — modelos free toman 18-57s) |
| API key JWT | `{"alg":"HS256","w":"openclaw"}` — workspace isolado de `hermes` |

**Workspace isolation**: el JWT de OpenClaw codifica `"w":"openclaw"`, el de Hermes
codifica `"w":"hermes"`. Son memorias completamente separadas.

---

## Ansible — tags LiteLLM-only

```bash
# Solo LiteLLM (sin tocar Hermes ni OpenClaw):
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags ai-litellm-proxy

# Solo OpenClaw:
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags openclaw
```
Tras cambiar LiteLLM config: siempre `kubectl rollout restart deployment/litellm-proxy -n ai`
y luego `kubectl rollout restart deployment/openclaw -n openclaw`.

---

## Repo Paths

```
roles/install-openclaw/
├── defaults/main.yml              # vars (modelo, RBAC, Telegram, LiteLLM, MCP)
├── defaults/secrets.yml           # gitignored
├── defaults/secrets.yml.example
└── templates/
    ├── openclaw-deployment.yaml.j2  # Deployment + init + kubernetes-mcp sidecar
    ├── openclaw-configmap.yaml.j2   # openclaw.json (mcpServers) + AGENTS.md
    ├── openclaw-rbac.yaml.j2        # SA + ClusterRole (readonly+net, sin Secrets)
    ├── openclaw-network.yaml.j2     # Service + HTTPRoute + NetworkPolicy expandida
    ├── openclaw-pvc.yaml.j2
    └── openclaw-secret.yaml.j2

roles/install-litellm-proxy/tasks/main.yml  # aliases openclaw-gemini, gemma4-free, etc.
skills/openclaw/SKILL.md                    # este archivo
```

Makefile: `make openclaw` | `make openclaw-rbac LEVEL=<level>`
