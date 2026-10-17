---
name: honcho
description: >
  Self-hosted Honcho memory platform — Postgres + Redis + API + Worker.
  Workspace-scoped JWT auth (HS256). Alembic migrations via init container.
  Serves as persistent memory for OpenClaw and Hermes with workspace isolation.
  Critical Cilium gotcha: NetworkPolicy must use pod targetPort (8000), not service port (80).
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  author: dotfiles
  tags: [kubernetes, ai, honcho, memory, jwt, postgresql, redis, arm64, workspace]
---

# Honcho Skill

## ¿Qué es Honcho?

`plastic-labs/honcho` — plataforma de memoria persistente para agentes IA.
Expone una API HTTP v3 con workspaces, sessions, messages y peers.
Cada agente tiene su propio workspace aislado. Auth via JWT HS256.

- API docs: `http://honcho.cluster.home/docs`
- SDK: `@honcho-ai/sdk` (TypeScript) / Python client

## Stack

| Componente | Imagen | Puerto interno | Notas |
|------------|--------|----------------|-------|
| Postgres | `postgres:16-alpine` | 5432 | Persistence + Alembic schema |
| Redis | `redis:7-alpine` | 6379 | Cache + worker queue |
| API | `plastlabs/honcho` | **8000** | Service → port 80 → targetPort 8000 |
| Worker | `plastlabs/honcho` | — | Deriver background tasks |

**El servicio Kubernetes mapea 80 → 8000.** Toda NetworkPolicy que deje entrar
o salir hacia Honcho debe usar el targetPort **8000**, no el port 80.
Ver sección "Gotcha Cilium DNAT" más abajo.

---

## Arquitectura en cluster

```
Namespace: honcho
┌─────────────────────────────────────────────────────┐
│                                                     │
│  honcho-api (Deployment)                            │
│  ├─ initContainer: migrate-db                       │
│  │   python scripts/provision_db.py                 │
│  │   → alembic upgrade head (24 migraciones)        │
│  └─ container: honcho API :8000                     │
│                                                     │
│  honcho-worker (Deployment)                         │
│  ├─ initContainer: wait-for-api                     │
│  │   espera hasta que /health responde              │
│  └─ container: honcho worker (deriver tasks)        │
│                                                     │
│  honcho-postgres (Deployment)                       │
│  honcho-redis (Deployment)                          │
│                                                     │
│  Service/honcho-api → ClusterIP :80 → pod :8000     │
│  HTTPRoute → honcho.cluster.home                    │
│  PVC: honcho-postgres-data (longhorn-nvme)          │
└─────────────────────────────────────────────────────┘

Consumers:
  OpenClaw (openclaw ns) → honcho-api.honcho.svc:80 → pod :8000
  Hermes   (ai ns)       → honcho-api.honcho.svc:80 → pod :8000
```

---

## Alembic — migraciones (init container)

Honcho tiene **24 migraciones Alembic** que deben ejecutarse antes de que
el API arranque. Sin ellas el worker crashea:
```
sqlalchemy.exc.ProgrammingError: relation "public.active_queue_sessions" does not exist
```

**Solución**: init container en el Deployment del API que ejecuta `provision_db.py`:

```yaml
# charts/honcho/templates/api-deployment.yaml
initContainers:
  - name: migrate-db
    image: "{{ image }}"
    command: ["python", "scripts/provision_db.py"]
    workingDir: /app
    envFrom:
      - secretRef:
          name: honcho-secrets
```

`provision_db.py` llama `init_db()` → `alembic upgrade head`. Se ejecuta en
cada deploy: es idempotente, solo aplica las migraciones faltantes.

**NUNCA usar `kubectl exec` para ejecutar Alembic.** Siempre via init container
(correcto, reproducible, no depende del estado de un pod en vivo).

---

## Auth — JWT HS256 workspace-scoped

Honcho soporta dos modos:
- `AUTH_USE_AUTH=false` → cualquier key es aceptada (modo dev)
- `AUTH_USE_AUTH=true`  → valida JWT HS256 firmado con `AUTH_JWT_SECRET`

**En producción usar `AUTH_USE_AUTH=true` con keys workspace-scoped.**

### Tipos de JWT

| Payload | Tipo | Uso |
|---------|------|-----|
| `{"t":"","w":"openclaw"}` | Workspace-scoped | Solo accede al workspace `openclaw` |
| `{"t":"","w":"hermes"}` | Workspace-scoped | Solo accede al workspace `hermes` |
| `{"t":"","ad":true}` | Admin | Accede a todos los workspaces |

### Generar keys

```bash
# 1. Generar JWT secret (guardar en secrets.yml)
python3 -c "import secrets; print(secrets.token_hex(32))"

# 2. Generar workspace key para openclaw
SECRET="<tu-jwt-secret>"
python3 -c "import jwt; print(jwt.encode({'t':'','w':'openclaw'}, '$SECRET', 'HS256'))"

# 3. Generar workspace key para hermes
python3 -c "import jwt; print(jwt.encode({'t':'','w':'hermes'}, '$SECRET', 'HS256'))"

# 4. Generar admin key (solo para administración)
python3 -c "import jwt; print(jwt.encode({'t':'','ad':True}, '$SECRET', 'HS256'))"
```

### Secrets por rol

Cada consumer guarda su workspace-scoped key en su propio `secrets.yml`:

```yaml
# roles/install-openclaw/defaults/secrets.yml (gitignored)
openclaw_honcho_api_key: "eyJ..."   # JWT con {"w":"openclaw"}

# roles/install-hermes-agent/defaults/secrets.yml (gitignored)
hermes_honcho_api_key: "eyJ..."     # JWT con {"w":"hermes"}
```

La key de admin (`honcho_admin_key`) solo vive en `roles/install-honcho/defaults/secrets.yml`.

### Verificar aislamiento

```bash
# JWT openclaw NO puede acceder al workspace hermes → 401
curl -H "Authorization: Bearer $OPENCLAW_KEY" \
  http://honcho.cluster.home/v3/workspaces/hermes
# → 401 Unauthorized

# JWT hermes NO puede acceder al workspace openclaw → 401
curl -H "Authorization: Bearer $HERMES_KEY" \
  http://honcho.cluster.home/v3/workspaces/openclaw
# → 401 Unauthorized
```

---

## SDK Python — env vars oficiales

El Honcho Python SDK lee exactamente estas variables de entorno:

| Env var | Propósito | Ejemplo |
|---------|-----------|---------|
| `HONCHO_URL` | URL del API (primary) | `http://honcho-api.honcho.svc.cluster.local` |
| `HONCHO_BASE_URL` | URL del API (alias) | igual que HONCHO_URL |
| `HONCHO_API_KEY` | JWT o API key de autenticación | `eyJ...` |
| `HONCHO_WORKSPACE_ID` | Workspace ID (primary) | `hermes` |
| `HONCHO_WORKSPACE` | Workspace ID (alias, añadido por compatibilidad) | `hermes` |

**Hermes** usa el SDK Python y lee `HONCHO_URL` + `HONCHO_WORKSPACE_ID`.
Para garantizar compatibilidad, el deployment de Hermes setea los 5 nombres.

**OpenClaw** usa el plugin `@honcho-ai/openclaw-honcho` (TypeScript) con el SDK JS.
El SDK JS lee `baseUrl` de `openclaw.json` config (no env var).

---

## API v3 — endpoints clave

```bash
# Health check (sin auth)
GET /health → {"status":"ok"}

# Crear workspace (POST /v3/workspaces con body {id: "..."})
POST /v3/workspaces
Authorization: Bearer <jwt>
{"id": "hermes"}
→ {"id":"hermes","created_at":"..."}

# GET workspace existente
POST /v3/workspaces       # con id ya existente → devuelve el existente (idempotente)
PUT  /v3/workspaces/{workspace_id}   # update

# Listar workspaces
POST /v3/workspaces/list
{"filter": null}

# Crear peer
POST /v3/workspaces/{workspace_id}/peers
{"id": "user-123", "metadata": {}}

# Listar peers
POST /v3/workspaces/{workspace_id}/peers/list
{}

# Crear session para un peer
POST /v3/workspaces/{workspace_id}/peers/{peer_id}/sessions
{"metadata": {...}}

# Chat con contexto de memoria
POST /v3/workspaces/{workspace_id}/peers/{peer_id}/chat
```

---

## Helm chart local (`charts/honcho/`)

El chart está en el repo, no en un registry externo.

```
charts/honcho/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── api-deployment.yaml      # API + init container migrate-db
    ├── worker-deployment.yaml   # Worker + init container wait-for-api
    ├── postgres-deployment.yaml
    ├── redis-deployment.yaml
    ├── secret.yaml              # DB password + JWT secret (AUTH_USE_AUTH, AUTH_JWT_SECRET)
    ├── service.yaml
    └── httproute.yaml
```

Variables clave en `values.yaml`:
```yaml
llm:
  baseUrl: "http://litellm-proxy.ai.svc.cluster.local:4000/v1"
  apiKey: "sk-hermes-internal"
  model: "kimi-free"   # ← CRÍTICO: debe soportar tool_choice:any (ver gotcha abajo)
  embedMessages: "false"
auth:
  useAuth: "true"       # "false" = dev mode (any key accepted)
  jwtSecret: ""         # Injected from Ansible secrets.yml
postgresql:
  dbPassword: ""        # Injected from Ansible secrets.yml
```

**`llm.model` se inyecta en el Secret** (`secret.yaml`) como `DERIVER_MODEL`, `SUMMARY_MODEL`,
`DREAM_MODEL` y `DIALECTIC_LEVELS`. Cambiar el valor en `values.yaml` actualiza el Secret en el
próximo `make honcho`, pero **no reinicia los pods automáticamente**. Siempre hacer:
```bash
kubectl rollout restart deployment/honcho-worker deployment/honcho-api -n honcho
```

---

## Deploy

```bash
# Prerequisitos: generar secrets primero
cp roles/install-honcho/defaults/secrets.yml.example \
   roles/install-honcho/defaults/secrets.yml
# Editar: honcho_db_password, honcho_jwt_secret, honcho_admin_key

# Deploy
make honcho

# Equivalente
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini --tags ai-honcho
```

La primera vez, los init containers ejecutan las 24 migraciones Alembic (~30s extra).

---

## Por qué Honcho (y no alternativas)

Honcho es la elección más opinionada de este stack. Hay alternativas más simples
(mem0, LangChain memory, PostgreSQL propio). Mi opinión sobre por qué Honcho:

**Honcho sí**: tiene un modelo de dialectic reasoning — el deriver LLM sintetiza
memorias en segundo plano sin bloquear la respuesta del usuario. La memoria no es solo
"guardar el último mensaje" sino "inferir qué es importante y construir un user profile".
Para un asistente personal de largo plazo (Tito hablando con el mismo usuario todos los
días), esto marca diferencia real.

**Honcho no**: el dialectic usa un LLM extra (kimi-free), lo que añade latencia y un
punto de fallo. Si el LLM del deriver es lento (modelos :free) o no soporta `tool_choice:any`
(Nemotron), la memoria se "silencia" sin error visible. Honcho es complejo de debuggear.

**Decisión**: Honcho está bien para el caso de uso actual (agente personal conversacional
a largo plazo). Si el stack fuera una API pública con miles de usuarios, usaría algo más
simple. Pero para UN usuario conversando diario con Tito, el overhead vale.

**Sobre el modelo del deriver**: `kimi-free` (Moonshot kimi-k2.6:free) es el único
modelo :free que ha demostrado soportar `tool_choice: any` sin problemas. Si hay que
cambiar, elegir un modelo con soporte nativo de Anthropic tool use. Nemotron nunca.

## Gotcha — `tool_choice: "any"` rechazado por Nemotron/OpenRouter

**Síntoma:** OpenClaw muestra "⚠️ Something went wrong while processing your request" en cada mensaje.
Los logs del honcho-worker no tienen errores visibles, pero la memoria no se guarda ni se recupera.

**Causa raíz:** Honcho v3 envía `tool_choice: "any"` (convención Anthropic) en sus llamadas
de dialectic/deriver al LLM. Nemotron via OpenRouter solo acepta `"none"`, `"auto"`, `"required"` →
devuelve HTTP 400 → el worker de reasoning falla silenciosamente → la memoria se escribe pero
la síntesis de contexto no funciona → OpenClaw no puede recuperar contexto → error en respuesta.

**Fix (aplicado 2026-06-01):**
1. `charts/honcho/values.yaml`: `llm.model: "kimi-free"` — Moonshot kimi-k2.6:free soporta tool_choice correctamente
2. `roles/install-litellm-proxy/tasks/main.yml`: `litellm_settings.modify_params: true` — LiteLLM dropa params no soportados como fallback de seguridad

**Regla:** solo usar modelos como `llm.model` en Honcho que soporten **`tool_choice: "any"` o `"required"`**.
Modelos confirmados como problemáticos: Nemotron (`nvidia/nemotron-3-super-120b-a12b`).
Modelos confirmados como funcionando: kimi-k2.6:free, Kimi, modelos con soporte nativo de Anthropic tool_choice.

---

## Gotcha — Peer map de OpenClaw fuera del PVC (memoria "amnésica")

**Síntoma:** las memorias se guardan en Honcho (Postgres tiene los datos) pero
después de cada restart del pod, Tito no recuerda nada y arranca de cero.

**Causa raíz:** el plugin `openclaw-honcho` guarda su peer map (mapeo
chat/usuario → peer/session IDs de Honcho) en `/home/node/.honcho/openclaw-peers.json`.
El PVC `openclaw-data` solo montaba `/home/node/.openclaw` → el peer map vivía
en el filesystem efímero del contenedor → en cada restart se perdía el mapeo
y el plugin creaba peers/sessions nuevos, dejando huérfanas las memorias viejas.

**Fix (2026-06-10):** `openclaw-deployment.yaml.j2` monta además
`/home/node/.honcho` desde el mismo PVC con `subPath: .honcho-state`
(en gateway, sidecar y MCP bridge). El init container crea el directorio con
ownership 1000:1000. Las memorias pre-fix siguen en Postgres pero quedaron
asociadas a peers viejos — se reconstruyen con el uso.

## Gotcha — Cilium evalúa NetworkPolicy POST-DNAT

**Regla crítica:** cuando Cilium aplica una NetworkPolicy de egress, evalúa el puerto
**DESPUÉS del DNAT** (después de que el ClusterIP se traduce al pod IP).

El servicio `honcho-api` mapea: Service port **80** → pod targetPort **8000**.
Cuando OpenClaw conecta a `honcho-api.honcho.svc.cluster.local:80`, Cilium ve
la conexión como destino **port 8000** (el targetPort real del pod).

Por eso la NetworkPolicy de egress en OpenClaw debe usar **8000**, no 80:

```yaml
# roles/install-openclaw/templates/openclaw-network.yaml.j2
# CORRECTO:
- to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: honcho
  ports:
    - port: 8000      # ← targetPort del pod, no service port
      protocol: TCP

# INCORRECTO (bloqueará aunque parezca lógico):
# ports:
#   - port: 80        # ← service port → Cilium no lo ve así post-DNAT
```

**Cómo detectarlo:** debug pods sin el label de NetworkPolicy pueden conectar
(el NetworkPolicy no aplica a ellos). Solo los pods con `app=openclaw` son
afectados. Usar `curl -s --max-time 8 ... EXIT:$?` → `EXIT:28` = timeout (bloqueado).

**Aplica a cualquier servicio con service port ≠ targetPort:**
- LiteLLM: service 4000 = targetPort 4000 → NetworkPolicy port 4000 ✅
- Honcho: service 80 ≠ targetPort 8000 → NetworkPolicy debe usar 8000

---

## Troubleshooting

### Worker crashea en startup

```bash
kubectl logs -n honcho deploy/honcho-worker --tail=30
# Si ves: "relation ... does not exist" → Alembic no corrió
# Si ves: init container "migrate-db" no está → actualizar chart y redeploy

# Verificar que el init container corrió las 24 migraciones
kubectl logs -n honcho <api-pod> -c migrate-db
# → "Running upgrade ... -> ..., Apply ..."
# → "INFO  [alembic.runtime.migration] Running upgrade ..."
```

### API retorna 500 / errores de schema

```bash
# Forzar re-run de migraciones: reiniciar el deployment
kubectl rollout restart deploy/honcho-api -n honcho
# → init container migrate-db corre de nuevo (idempotente)
```

### OpenClaw no puede conectar a Honcho

```bash
# 1. Verificar que el servicio existe
kubectl get svc -n honcho

# 2. Verificar que el health check responde
kubectl run -n honcho curl-test --restart=Never --image=curlimages/curl \
  --command -- curl -s http://honcho-api.honcho.svc.cluster.local/health
kubectl logs -n honcho curl-test; kubectl delete pod -n honcho curl-test

# 3. Verificar conectividad CON NetworkPolicy aplicada (usar label app=openclaw)
kubectl run -n openclaw nw-test --restart=Never --image=curlimages/curl \
  --labels="app=openclaw" \
  --command -- sh -c 'curl -s --max-time 8 http://honcho-api.honcho.svc.cluster.local/health; echo EXIT:$?'
sleep 12; kubectl logs -n openclaw nw-test; kubectl delete pod -n openclaw nw-test

# Si EXIT:28 → NetworkPolicy bloqueando → verificar que usa puerto 8000, no 80
kubectl get networkpolicy openclaw-egress -n openclaw -o yaml | grep -A5 "honcho"

# 4. Verificar en los logs de OpenClaw
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway --tail=30 | grep -i honcho
# → "Honcho memory ready" = OK
# → "Failed to initialize Honcho: ConnectionError" = NetworkPolicy o URL incorrecta
```

### JWT inválido / 401

```bash
# Verificar que el JWT secret en Honcho coincide con el usado para generar las keys
# El secret está en el Secret de K8s:
kubectl get secret honcho-secrets -n honcho -o jsonpath='{.data.AUTH_JWT_SECRET}' | base64 -d

# Regenerar una key y verificarla
SECRET=$(kubectl get secret honcho-secrets -n honcho -o jsonpath='{.data.AUTH_JWT_SECRET}' | base64 -d)
python3 -c "import jwt; print(jwt.decode('$KEY', '$SECRET', algorithms=['HS256']))"
# → debe mostrar {"t":"","w":"openclaw"} o similar sin error
```

---

## Verificación completa post-deploy

```bash
# 1. Todos los pods running
kubectl get pods -n honcho
# → honcho-api, honcho-worker, honcho-postgres, honcho-redis: Running

# 2. Health check
curl http://honcho.cluster.home/health
# → {"status":"ok"}

# 3. Crear workspace con key de admin
ADMIN_KEY=$(grep honcho_admin_key roles/install-honcho/defaults/secrets.yml | awk '{print $2}' | tr -d '"')
curl -X POST http://honcho.cluster.home/v3/workspaces/openclaw \
  -H "Authorization: Bearer $ADMIN_KEY"
# → {"id":"openclaw",...}

# 4. Workspace-scoped key solo accede a su workspace
OPENCLAW_KEY=$(grep openclaw_honcho_api_key roles/install-openclaw/defaults/secrets.yml | awk '{print $2}' | tr -d '"')
curl http://honcho.cluster.home/v3/workspaces/openclaw \
  -H "Authorization: Bearer $OPENCLAW_KEY"
# → 200 OK

curl http://honcho.cluster.home/v3/workspaces/hermes \
  -H "Authorization: Bearer $OPENCLAW_KEY"
# → 401 Unauthorized (aislamiento correcto)

# 5. OpenClaw muestra "Honcho memory ready" en logs
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway | grep -i honcho
# → "Honcho memory ready — peer map: ..."
```

---

## Workspaces configurados

| Workspace | Consumer | JWT en |
|-----------|----------|--------|
| `openclaw` | OpenClaw gateway | `roles/install-openclaw/defaults/secrets.yml` → `openclaw_honcho_api_key` |
| `hermes` | Hermes Agent | `roles/install-hermes-agent/defaults/secrets.yml` → `hermes_honcho_api_key` |

---

## Repo Paths

```
charts/honcho/                               # Helm chart local
roles/install-honcho/
├── defaults/main.yml                        # honcho_node_hostname, storage, auth
├── defaults/secrets.yml                     # gitignored: db_password, jwt_secret, admin_key
├── defaults/secrets.yml.example
└── tasks/main.yml                           # include_vars + helm deploy + rollout wait

roles/install-openclaw/templates/
└── openclaw-network.yaml.j2                 # egress port 8000 (post-DNAT targetPort)

Makefile: make honcho
```
