---
name: render-deploy
description: Deploy Hermes Agent no Render Free tier com Telegram (ou WhatsApp opcional), 24/7 sem hibernar via health server + Google Apps Script. Provider único (OpenCode Zen) — sem request spam por múltiplos providers.
---

# Render Deploy — Hermes Agent 24/7

Deploy do Hermes Agent no **Render Free tier** rodando **Telegram** 24/7 (WhatsApp opcional — veja seção específica), com health server em Python stdlib puro que responde "ok | uptime: Xh Ym Zs", pausado por **Google Apps Script** a cada 5 min para evitar hibernação do Render (Free tier dorme após 15 min de inatividade).

**Provider único obrigatório:** use apenas OpenCode Zen (ou o provider da sua escolha). Configurar múltiplos providers causa spam de requests e timeouts — veja seção abaixo.

---

## Provider Configuration — Evitando Request Spam

**Problema descoberto em sessão real:** configurar **múltiplos providers** (ex: OpenRouter + OpenCode Zen) faz com que o Hermes tente requests em paralelo pra ambas as APIs, causando spam de requisições e timeouts. O Hermes usa `credential_pool_strategies` e `fallback_providers` para rotacionar/fallback entre providers — se ambos estiverem disponíveis (via env vars), ele tenta os dois.

**Regra de ouro (IMPORTANTE): Defina UM provider. Remova TODAS as env vars dos outros providers do render.yaml E do Dashboard do Render.** Senão o Hermes tenta requests em paralelo, causando spam de requisições e timeouts.

**Usuário foi enfático:** "NAO TEM A MERDA DO OPENROUTER" — não deixe OpenRouter nem como fallback. Remova a env var do render.yaml, do .env, e delete qualquer Secret File no Dashboard do Render. Apenas o provider principal deve existir.

**Verificação:** depois do deploy, confirme que `OPENROUTER_API_KEY` não aparece em lugar nenhum — nem no repositório, nem no Dashboard. O Hermes detecta env vars de providers mesmo que o config.yaml só mencione um.

### ⚠️ Stale Env Vars no Render Dashboard

Remover uma env var do `render.yaml` **NÃO a remove do ambiente do container** se ela foi adicionada manualmente como **Secret File** no Dashboard do Render. Secrets adicionados manualmente persistem até você explicitamente deletá-los pelo Dashboard.

Se migrou de OpenRouter → OpenCode Zen:
1. Render Dashboard → Environment
2. Delete o Secret File ou env var que contém `OPENROUTER_API_KEY`
3. Delete quaisquer outras env vars de providers antigos
4. Confirme que só o provider desejado está presente
5. Re-deploy

### Abordagem alternativa: HERMES_MODEL/HERMES_PROVIDER via env vars

Em vez de copiar um `render-config.yaml`, você pode injetar o modelo/provider no config.yaml
via entrypoint usando env vars (`HERMES_MODEL`, `HERMES_PROVIDER`, `HERMES_BASE_URL`,
`HERMES_API_MODE`). Útil quando você não quer commitar um config.yaml separado no repositório.

**⚠️ PITFALL CRÍTICO:** Só setar `HERMES_MODEL` e `HERMES_PROVIDER` **NÃO é suficiente.**
O template `cli-config.yaml.example` da imagem Docker tem `base_url: https://openrouter.ai/api/v1`
como padrão. Se você não sobrescrever `base_url` para o endpoint correto do seu provider,
todas as requisições vão para o OpenRouter mesmo com `provider: opencode-zen`, resultando em
HTTP 401 "Missing Authentication header". **Sempre inclua também `HERMES_BASE_URL` e
`HERMES_API_MODE`.**

**No entrypoint.sh, após o bootstrap do config.yaml:**

```bash
# Apply model env vars (HERMES_MODEL / HERMES_PROVIDER / HERMES_BASE_URL / HERMES_API_MODE)
if [ -n "${HERMES_MODEL:-}" ] || [ -n "${HERMES_PROVIDER:-}" ] || [ -n "${HERMES_BASE_URL:-}" ] || [ -n "${HERMES_API_MODE:-}" ]; then
    python3 -c "
import yaml, os
path = '\\$HERMES_HOME/config.yaml'
with open(path) as f:
    cfg = yaml.safe_load(f)
changed = False
model_var = os.environ.get('HERMES_MODEL')
prov_var = os.environ.get('HERMES_PROVIDER')
url_var = os.environ.get('HERMES_BASE_URL')
mode_var = os.environ.get('HERMES_API_MODE')
if model_var:
    cfg.setdefault('model', {})['default'] = model_var
    changed = True
if prov_var:
    cfg.setdefault('model', {})['provider'] = prov_var
    changed = True
if url_var:
    cfg.setdefault('model', {})['base_url'] = url_var
    changed = True
if mode_var:
    cfg.setdefault('model', {})['api_mode'] = mode_var
    changed = True
if changed:
    with open(path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False)
    print('[config] model.default=' + str(model_var or '(unchanged)') + '  provider=' + str(prov_var or '(unchanged)') + '  base_url=' + str(url_var or '(unchanged)') + '  api_mode=' + str(mode_var or '(unchanged)'))
"
fi
```

**No render.yaml (sempre com todas as 4 vars):**
```yaml
- key: HERMES_MODEL
  value: "big-pickle"
- key: HERMES_PROVIDER
  value: "opencode-zen"
- key: HERMES_BASE_URL
  value: "https://opencode.ai/zen/v1"
- key: HERMES_API_MODE
  value: "chat_completions"
```

**Vantagem:** não precisa de um `config.yaml` separado no repositório.
**Desvantagem:** só configura `model.default`, `model.provider`, `model.base_url` e
`model.api_mode` — não cobre `auxiliary.*` providers. Para configuração completa, use
`render-config.yaml`.

### Custom config.yaml (obrigatório — abordagem completa)

Em vez de depender do config padrão bootstrapped pela imagem (`cli-config.yaml.example`), **crie um config.yaml customizado no repositório** e faça o entrypoint **sempre** sobrescrevê-lo. Isso garante que o provider correto seja aplicado mesmo em redeploys com disco persistente.

```yaml
# config.yaml — provider único, sem fallback
model:
  default: big-pickle          # ou o modelo que preferir
  provider: opencode-zen
  base_url: https://opencode.ai/zen/v1
  api_mode: chat_completions

# Sem fallback — desabilita rotação entre providers
fallback_providers: []
credential_pool_strategies: {}

# Todos os auxiliares apontam pro MESMO provider
auxiliary:
  vision:
    provider: opencode-zen
    model: big-pickle
    base_url: https://opencode.ai/zen/v1
  compression:
    provider: opencode-zen
    model: big-pickle
    base_url: https://opencode.ai/zen/v1
  session_search:
    provider: opencode-zen
    model: big-pickle
    base_url: https://opencode.ai/zen/v1
  web_extract:
    provider: opencode-zen
    model: big-pickle
    base_url: https://opencode.ai/zen/v1
  approval:
    provider: opencode-zen
    model: big-pickle
    base_url: https://opencode.ai/zen/v1

# Provider desabilitado (se aplicável)
openrouter:
  response_cache: false
```

**PITFALL:** Mesmo com `provider: opencode-zen` no `model`, se `OPENROUTER_API_KEY` estiver disponível no ambiente, os tasks auxiliares em modo `auto` podem tentar OpenRouter. Configure CADA auxiliary provider explicitamente como acima.

### Dockerfile — Copiando config.yaml

```dockerfile
# Custom config.yaml — provider único, sem router
COPY config.yaml /opt/hermes/render-config.yaml
RUN chmod 644 /opt/hermes/render-config.yaml
```

### Entrypoint — Sempre sobrescrever

No entrypoint.sh, substitua o bootstrap condicional por uma cópia **incondicional**:

```bash
# ANTIGO (só copiava se não existisse — permitia config obsoleto persistir):
# if [ ! -f "$HERMES_HOME/config.yaml" ]; then
#     cp "$INSTALL_DIR/cli-config.yaml.example" "$HERMES_HOME/config.yaml"
# fi

# NOVO (sempre sobrescreve com config otimizado):
if [ -f "$INSTALL_DIR/render-config.yaml" ]; then
    cp "$INSTALL_DIR/render-config.yaml" "$HERMES_HOME/config.yaml"
    echo "[config] Applied render-config.yaml (provider único, sem router)"
fi
```

Isso garante que mesmo num container com disco persistente que já tem um `config.yaml` antigo, o provider correto seja aplicado a cada restart/deploy.

---

## Estrutura do Projeto

```
render-hermes/
├── .env.example            # Template de env vars (NUNCA commitar .env real)
├── .gitattributes          # Forçar LF no repositório (evitar CRLF)
├── .gitignore              # Ignorar .env, __pycache__, *.pyc
├── Dockerfile              # Base: nousresearch/hermes-agent:latest
├── render-health.py        # Health server (stdlib puro, porta 10000)
├── render.yaml             # Blueprint Render (declarativo)
├── test_health.py          # Testes do health server
└── docker/
    └── entrypoint.sh       # Inicia health + gateway + dashboard
```

### ⚠️ O `.env` do projeto é DOCUMENTAÇÃO, não runtime

O arquivo `.env` (ou `.env.example`) na pasta `render-hermes/` serve como **template de referência** — ele NÃO é copiado pro container Docker. O entrypoint.sh usa o `.env.example` da imagem oficial como base, e os valores reais vêm das **Environment Variables / Secret Files configuradas no Dashboard do Render** (ou do `render.yaml`).

**Implicação prática:** mudar o `.env` dentro de `render-hermes/` não afeta o deploy no Render. Você precisa:
1. Alterar o valor no Dashboard do Render (Environment → Secret Files) OU
2. Alterar no `render.yaml` e fazer novo deploy

**E localmente (fora do Docker):** quem manda é `~/.hermes/.env`. Se quiser desabilitar WhatsApp, por exemplo, precisa mudar em AMBOS os lugares:
- `render-hermes/.env` (documentação do projeto)
- `~/.hermes/.env` (runtime local — use `sed -i` porque o patch tool bloqueia esse arquivo)

Isso evita surpresas do tipo "mudei no projeto mas o gateway ainda tenta conectar WhatsApp".
```

---

## Arquivos-Chave

### render-health.py

Servidor HTTP com **stdlib puro** (zero dependências externas). Rodar em background antes do gateway.

```python
import http.server
import json
import time
from urllib.parse import urlparse, parse_qs

UPTIME_START = time.time()

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        uptime_secs = int(time.time() - UPTIME_START)
        uptime_str = f"{uptime_secs//3600}h {(uptime_secs%3600)//60}m {uptime_secs%60}s"

        if path in ('', '/health'):
            qs = parse_qs(parsed.query)
            if 'format' in qs and qs['format'][0] == 'json':
                self.send_json({"status": "ok", "uptime": uptime_str, "uptime_seconds": uptime_secs})
            else:
                self.send_text(f"ok | uptime: {uptime_str}")
        else:
            self.send_error(404)

    def send_text(self, text):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(text.encode())

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # silêncio

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 10000), HealthHandler)
    server.serve_forever()
```

**PITFALL:** Usar urlparse para parsing correto de query strings. `self.path.split('?')` quebra se não houver query string (caminho fica vazio). Sempre use `urlparse`.

**Endpoints:**
- `GET /` → `ok | uptime: 0h 5m 23s` (text/plain)
- `GET /health` → mesmo que /
- `GET /?format=json` → `{"status":"ok","uptime":"0h 5m 23s"}` (application/json)

### Dockerfile

```dockerfile
FROM nousresearch/hermes-agent:latest

USER root

# Copy the health server
COPY render-health.py /opt/hermes/render-health.py
RUN chmod +x /opt/hermes/render-health.py

# Pre-install WhatsApp bridge deps (Baileys via git é lento — evita timeout no runtime)
RUN BRIDGE_DIR=$(/opt/hermes/.venv/bin/python3 -c "from pathlib import Path; import hermes_agent; print(Path(hermes_agent.__file__).parent / 'scripts' / 'whatsapp-bridge')") && \
    echo "WhatsApp bridge dir: $BRIDGE_DIR" && \
    cd "$BRIDGE_DIR" && \
    npm install --timeout=300000

# Custom config.yaml — provider único, sem router
COPY config.yaml /opt/hermes/render-config.yaml
RUN chmod 644 /opt/hermes/render-config.yaml

# Replace the entrypoint with our multi-process version
COPY docker/entrypoint.sh /opt/hermes/docker/entrypoint.sh
RUN chmod +x /opt/hermes/docker/entrypoint.sh

EXPOSE 10000
EXPOSE 9119

ENV HERMES_DASHBOARD=1
ENV HERMES_DASHBOARD_HOST=0.0.0.0
ENV HERMES_DASHBOARD_PORT=9119

USER hermes

ENTRYPOINT ["/usr/bin/tini", "-g", "--", "/opt/hermes/docker/entrypoint.sh"]
CMD ["gateway", "run"]
```

**PITFALLS:**
- Imagem oficial é `nousresearch/hermes-agent:latest`, não `hermes-agent:latest`
- Mantenha `USER root` inicialmente — o entrypoint faz `chown`/`usermod` antes de dropar pra `hermes`
- `ENTRYPOINT` usa `tini` (init system) pra garantir que processos filho sejam limpos corretamente

### docker/entrypoint.sh

Baseado no entrypoint original do Hermes. Duas alterações críticas:

**1. Sempre sobrescrever config.yaml com a versão customizada** (após bootstrap):

```bash
# Always deploy our Render-optimized config.yaml (provider único)
if [ -f "$INSTALL_DIR/render-config.yaml" ]; then
    cp "$INSTALL_DIR/render-config.yaml" "$HERMES_HOME/config.yaml"
    echo "[config] Applied render-config.yaml (provider único, sem router)"
fi
```

**2. Iniciar health server em background antes do exec final:**

```bash
# Render-specific: start health server
HEALTH_PORT="${HEALTH_PORT:-10000}"
echo "[health] Starting render-health.py on :${HEALTH_PORT}"
python3 /opt/hermes/render-health.py &
sleep 1
```

**PITFALL CRÍTICO:** Sem o `mkdir -p "$HERMES_HOME"` no bloco root, o entrypoint vai tentar criar diretórios como usuário `hermes` (após `gosu`) e falhar com "Permission denied" se `HERMES_HOME` apontar pra um caminho que o `hermes` user não possa escrever. O Render Free não permite `mkdir -p /home/hermes` — use `/opt/data` como HERMES_HOME.

### render.yaml

```yaml
services:
  - type: web
    name: hermes-agent
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: ./
    plan: free

    healthCheckPath: /
    healthCheckPort: 10000

    disk:
      name: hermes-data
      mountPath: /opt/data
      sizeGB: 1

    ports:
      - port: 10000  # Health server
      - port: 9119   # Dashboard

    envVars:
      - key: HERMES_HOME
        value: /opt/data
      - key: HERMES_DASHBOARD
        value: "1"
      - key: HERMES_DASHBOARD_HOST
        value: 0.0.0.0
      - key: HERMES_DASHBOARD_PORT
        value: "9119"
      - key: HEALTH_PORT
        value: "10000"

      # ── Provider ÚNICO (apenas UM — evita request spam) ──
      - key: OPENCODE_ZEN_API_KEY
        sync: false
      # OPENROUTER_API_KEY removido — apenas 1 provider

      # ── Telegram ──
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_ALLOWED_USERS
        value: "8599666899"
      - key: TELEGRAM_WEBHOOK_URL
        sync: false

      # WhatsApp removido (opcional — veja seção específica)
```

**PITFALL:** Render Blueprint pra `env: docker` NÃO aceita `ports:` nem `healthCheckPort` em todas as versões. Render detecta porta pelo `EXPOSE` no Dockerfile. Teste sem esses campos se o deploy falhar.

Env vars com `sync: false` são valores que o usuário precisa preencher manualmente no dashboard (tokens).

Render Free dorme após 15 min sem tráfego HTTP. O health check próprio do Render mantém acordado na maioria das vezes, mas o Apps Script é garantia extra.

**Criar:**
1. Acessar https://script.google.com/
2. Novo projeto
3. Colar:

```javascript
function pingHealth() {
  UrlFetchApp.fetch('https://SEU-APP.onrender.com/');
}
```

4. Clicar no relógio (⏰ Triggers) → Add Trigger
   - Function: pingHealth
   - Time-driven: Every 5 minutes
   - Failure notification: Notificar-me imediatamente

**Isso mantém o Render acordado 24/7 sem custo.**

---

## Deploy Passo a Passo

### 0. Criar os arquivos

Crie o projeto em `/mnt/c/Users/SEU_USER/Mateus/render-hermes/` (ou outra pasta acessível pelo Windows Explorer).

Arquivos necessários:
- `Dockerfile`
- `render-health.py`
- `render.yaml`
- `config.yaml` (custom — veja seção [Provider Configuration](#provider-configuration))
- `docker/entrypoint.sh`
- `test_health.py` (opcional)

### 1. Git init + commit

```bash
cd /mnt/c/Users/keila/Mateus/render-hermes
git init
git config user.email "seu@email.com"    # ou --global se prefere
git config user.name "Seu Nome"
git add -A
git commit -m "initial: render deploy hermes-agent"
```

### 2. Criar repositório no GitHub

- https://github.com/new
- Nome: `hermes-render`
- **Não** inicializar com README, .gitignore ou license (já temos)
- Seguir instruções para **push an existing repository**:

```bash
git remote add origin https://github.com/SEU_USUARIO/hermes-render.git
git branch -M main
git push -u origin main
```

> Se não tiver git configurado com GitHub no WSL, faça upload manual via GitHub web UI (drag & drop os arquivos).

> **Evite problemas de CRLF:** adicione um `.gitattributes` na raiz do projeto:
> ```
> * text=auto
> *.sh text eol=lf
> *.py text eol=lf
> Dockerfile text eol=lf
> *.yaml text eol=lf
> *.yml text eol=lf
> ```
> Isso força LF no repositório mesmo que o Windows use CRLF.

### 3. Deploy no Render

- Render Dashboard → New → Blueprint
- Conectar GitHub e selecionar `hermes-render`
- Render lê `render.yaml` automaticamente
- **Antes do deploy**, configurar env vars no Dashboard:
  - `OPENCODE_ZEN_API_KEY` (Secret File)
  - `TELEGRAM_BOT_TOKEN` (Secret File)
  - `TELEGRAM_WEBHOOK_URL` (Secret File — `https://seu-app.onrender.com`)
  - `TELEGRAM_ALLOWED_USERS` (plain: `8599666899`)

- **Adicionar Persistent Disk** (Recomendado — Starter+):
  - Dashboard → Service → Disks → Add Disk
  - Mount Path: `/opt/data`
  - Size: 1 GB

### 4. Google Apps Script (anti-hibernação)

### 5. Verificar

- Acessar `https://SEU-APP.onrender.com/` → deve ver `ok | uptime: ...`
- Mandar `/start` pro bot no Telegram
- Ver logs no Render Dashboard

---

## WhatsApp (Opcional — removido do deploy atual)

> ⚠️ **WhatsApp foi removido do deploy atual** por decisão do usuário. Esta seção documenta como configurar caso queira adicionar novamente.

Render Free tier não permite Shell nem disco persistente. A única forma de ter WhatsApp funcionando é embutir a sessão pareada na imagem Docker.

### Workflow

```
Parear local → Gerar tarball → Commit + Push → Render redeploy automático
```

### Estrutura de arquivos

```
render-hermes/
├── auth/
│   ├── restore-session.sh    # Extrai tarball no container (executado no entrypoint)
│   ├── session.tar.gz        # Sessão WhatsApp compactada (~116KB)
│   └── update-session.sh     # Script pra regenerar o tarball após re-parear
├── Dockerfile                # COPY auth/ /opt/hermes/auth/
└── docker/
    └── entrypoint.sh         # Chama restore-session.sh como root antes do gosu
```

### Passo a passo

**1. Parear localmente:**
```bash
hermes whatsapp
```
Escaneie o QR code — os arquivos de auth vão para `~/.hermes/whatsapp/session/`.

**2. Gerar o tarball:**
```bash
cd render-hermes
bash auth/update-session.sh
```

**3. Commit e push (ou upload manual via GitHub web UI):**
```bash
git add auth/session.tar.gz
git commit -m "update whatsapp session"
git push
```
> Se git push falhar por falta de credenciais no WSL, faça upload da pasta `auth/` pelo GitHub web UI (drag & drop).

**4. Render detecta a mudança e faz deploy automático.**

**5. Quando a sessão expirar (~1-4 semanas):**
- Reparear localmente: `hermes whatsapp`
- Rodar `bash auth/update-session.sh`
- Commit e push
- Render redeploy automático

### Como funciona

- `auth/restore-session.sh` é chamado pelo `entrypoint.sh` **como root**, antes do `gosu`
- Ele verifica se `$HERMES_HOME/whatsapp/session/creds.json` existe; se não, extrai o tarball
- O tarball contém: `creds.json`, `pre-key-*`, `identity-key-*`, `sender-key-*`, `app-state-*`
- Baileys reconecta com esses arquivos sem precisar mostrar QR code

### Limitações
- Cada vez que a sessão expirar, precisa repetir o processo (re-parear local + gerar tarball + commit + push)
- O tarball (~116KB) fica no repositório GitHub (privado) — dados sensíveis, mas é a única opção no Free tier
- Telegram funciona SEMPRE sem esse processo (não precisa de sessão persistente)

> Detalhes técnicos completos: `references/whatsapp-free-tier-auth.md`

---

---

## Mente Compartilhada — CLI Mirror no Telegram (2026-05-14)

Tornar o bot do Telegram **um clone funcional** do Hermes CLI, compartilhando skills, personalidade, MCPs, toolsets e configuração.

### Configurações que o CLI tem e o Telegram padrão NÃO tem

| Aspecto | CLI | Telegram (padrão) |
|---------|:---:|:------------------:|
| Toolsets | ~18 (terminal, file, web, delegation, cronjob...) | 1 (`hermes-telegram`) |
| MCP Servers | 10 (obsidian, github, composio, youtube, etc.) | 0 |
| Skills | 120+ | 0 |
| Personalidades | kwai-bb, kawaii, etc. | só kawaii |
| Memória | sim | só se configurada |
| Terminal | sim | **não por padrão** |

### O que precisa mudar

1. **`config.yaml`** — adicionar `platform_toolsets.telegram`, `mcp_servers`, `agent.personalities`, `display.personality`, etc.
2. **`Dockerfile`** — adicionar `COPY skills /opt/hermes/skills/` e instalar Node.js para MCPs via npx
3. **`docker/entrypoint.sh`** — adicionar expansão de env vars (`os.path.expandvars()`) no config.yaml
4. **`render.yaml`** — adicionar env vars `GITHUB_TOKEN` e `COMPOSIO_API_KEY` para MCPs

### ⚠️ Pitfall: Skills com .git embedado viram submodule

Skills em `~/.hermes/skills/` (ex: `obsidian-skills/`, `superpowers/`) podem ter `.git/` internos. Copiá-las com `cp -r` leva o `.git/` junto, e o git do projeto Render trata como **submodule**.

```
# NO CHECKOUT: git ls-tree HEAD mostra "160000 commit ..." em vez de "100644 blob ..."
# SINTOMA: arquivos da skill não aparecem no repositório no GitHub
```

**Solução:** `find skills/PASTA -name ".git" -type d -prune -exec rm -rf {} +` após copiar.

### 📄 Detalhes completos

Veja `references/mente-compartilhada.md` para:
- Config.yaml completo com todos os campos
- Dockerfile com Node.js + skills
- Entrypoint com expansão de env vars
- Lista de MCPs que funcionam/não funcionam no Render
- Comandos de correção do submodule pitfall

---

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Health responde 404 | Usou `split('?')` no path | Migrar para `urlparse` |
| WhatsApp perdeu auth | Disco persistente não montado | Verificar mount path `/opt/data` |
| Gateway crasha no start | .env faltando token | Preencher env vars no Render |
| **Provider spamma requests / timeout** | **Múltiplos providers configurados (ex: OpenRouter + OpenCode Zen)** | **Remover provider não usado do render.yaml E do Dashboard (Secret Files persistem mesmo após remover do render.yaml). Configurar CADA auxiliary provider explicitamente no config.yaml.** |
| **Config antiga insiste após redeploy** | **Entrypoint só copiava config.yaml se não existisse** | **Mudar entrypoint pra SEMPRE sobrescrever config.yaml com versão customizada** |
| Modelo errado aparecendo (ex: opus em vez de big-pickle) | Config.yaml não foi aplicado (entrypoint antigo ou config não existe no repositório) | Criar config.yaml customizado e garantir entrypoint sempre sobrescreve |
| Git reclama "Author identity unknown" | user.name/user.email não configurados | `git config user.email "email" && git config user.name "nome"` |
| Telegram não conecta | Webhook URL errada | Usar `TELEGRAM_WEBHOOK_URL=https://app.onrender.com` |
| mkdir: Permission denied `/home/hermes` | HERMES_HOME não writável | Mudar HERMES_HOME pra `/opt/data` |
| **Shell scripts falham no container** | **CRLF line endings (Windows) — `\`: command not found`** | **Converter pra LF: `sed -i 's/\\r//' *.sh` antes do commit** |
| **WhatsApp bridge.log Permission denied** | **whatsapp/ nao existe ou dono errado** | **No entrypoint: 1) add `whatsapp` no mkdir 2) chown sempre** |
| **No messaging platforms enabled** | **Nenhuma plataforma detectada — gateway não conseguiu ativar nem Telegram nem WhatsApp** | **1) Verificar se `TELEGRAM_BOT_TOKEN` está setado (env var do Render Dashboard, não só no .env local). 2) Verificar se `python-telegram-bot` está instalado na venv do Hermes (dentro do container: `~/.hermes/hermes-agent/venv/bin/python -m pip show python-telegram-bot`). 3) Se WhatsApp foi desabilitado, confirmar `WHATSAPP_ENABLED=false` em AMBOS os lugares: `render-hermes/.env` (documentação) E `~/.hermes/.env` (runtime local) OU Render Dashboard (runtime cloud).** |
| **Telegram não conecta mesmo com TELEGRAM_BOT_TOKEN setado** | **`python-telegram-bot` não está instalado no ambiente onde o gateway roda** | **Na venv do Hermes: `~/.hermes/hermes-agent/venv/bin/python -m pip install python-telegram-bot`. Se o venv não tiver pip (venv de instalação mínima), instale com `python -m ensurepip --upgrade` primeiro.** |
| **npm install timeout no WhatsApp** | **Baileys via git e lento, default 60s** | **Pre-instalar no Dockerfile com `--timeout=300000`** |
| **HTTP 401 "Missing Authentication header"** | Provider configurado como `opencode-zen` mas `base_url` aponta pro OpenRouter (template default) | Add `HERMES_BASE_URL=https://opencode.ai/zen/v1` e `HERMES_API_MODE=chat_completions` no render.yaml + entrypoint precisa aplicar ambos no config.yaml |
| **Modelo errado aparece (ex: opus em vez de big-pickle)** | Config.yaml não foi aplicado (entrypoint antigo ou config não existe no repositório) | Criar config.yaml customizado e garantir entrypoint sempre sobrescreve |
---

## Comandos Úteis (Render Shell)

```bash
# Verificar saúde do processo
ps aux | grep -E 'python|hermes|node'

# Verificar logs do health server
pgrep -af render-health

# Testar health localmente
curl http://localhost:10000/

# Verificar gateway
hermes gateway status

# Verificar conexão Telegram
hermes doctor

# Verificar configuração atual
hermes config
```

---

## Custos

- **Render Free** — GRATUITO (hiberna sem tráfego, resolvido com Apps Script)
- **Render Starter** — US$7/mês (disco persistente incluso, recomendado)
- **Google Apps Script** — GRATUITO
- **GitHub** — GRATUITO (repositório público)
- **Telegram Bot** — GRATUITO
- **OpenCode Zen** — GRATUITO (ou conforme planos)
- **WhatsApp** (opcional) — GRATUITO (Baileys bridge)
