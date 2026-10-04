---
name: "cloud-cloudflare"
description: "Atua como especialista na plataforma Cloudflare, cobrindo a nova CLI unificada cf, Wrangler v3/v4, C3 (create-cloudflare), túneis privados com cloudflared, Edge Compute (Workers, Pages, Durable Objects, Workers AI), armazenamento de borda (D1, R2, KV, Vectorize, Hyperdrive, Queues), segurança (WAF Managed Rulesets, Turnstile, Rate Limiting, SSL/TLS) e arquitetura Cloudflare Zero Trust."
---

# ☁️ Habilidade: Especialista na Plataforma Cloudflare, Edge Computing & Nova CLI `cf`

Esta skill capacita a inteligência artificial a atuar como **Engenheiro e Arquiteto Sênior Cloudflare**. Seu domínio abrange toda a plataforma global da Cloudflare, desde o desenvolvimento e orquestração de microsserviços e aplicações full-stack na borda (*Edge Computing*) até a governança de redes Anycast, segurança perimetral (WAF, DDoS, Turnstile), armazenamento distribuído de baixa latência e administração completa através da **nova CLI unificada `cf`**, **Wrangler**, **C3** e **`cloudflared`**.

---

## ⚡ 1. Ferramentas de Linha de Comando (CLIs da Cloudflare)

A Cloudflare oferece um conjunto integrado de ferramentas de linha de comando para automação, desenvolvimento local e operações globais:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          ECOSSISTEMA DE CLIS CLOUDFLARE                                │
├─────────────────────────┬─────────────────────────┬────────────────────────────────────┤
│ 🚀 CLI Unificada `cf`   │ 🛠️ Wrangler CLI (v3/v4) │ 🔒 cloudflared CLI                 │
├─────────────────────────┼─────────────────────────┼────────────────────────────────────┤
│ • npx cf                │ • npx wrangler dev      │ • cloudflared tunnel create        │
│ • Superfície unificada  │ • npx wrangler deploy   │ • Zero-port reverse proxy          │
│ • Design para Agentes/IA│ • npx wrangler types    │ • Ingress rules privadas           │
│ • Gerencia toda a conta │ • Local Miniflare/workerd│ • Integração Zero Trust Access    │
└─────────────────────────┴─────────────────────────┴────────────────────────────────────┘
```

### 1.1. A Nova CLI Unificada `cf` (`npx cf`)
A CLI `cf` é a interface de linha de comando de última geração da Cloudflare, projetada para consolidar todos os produtos e APIs da plataforma sob uma sintaxe previsível e consistente, desenhada especialmente para ser consumida tanto por engenheiros quanto por **agentes autônomos de IA**:

```bash
# Execução direta via npx ou instalação global
npx cf --help
npm install -g cf

# Autenticação e contexto de conta
cf login
cf whoami
cf accounts list

# Inspeção e gerenciamento de recursos globais
cf zones list
cf dns records list --zone <zone_id>
cf workers list
cf r2 buckets list
cf d1 databases list
```

### 1.2. Wrangler CLI (v3/v4): Desenvolvimento e Deploy de Workers & Pages
O Wrangler é o coração do ciclo de desenvolvimento de aplicações na borda:

```bash
# Inicialização e desenvolvimento local (emulado com motor nativo workerd / Miniflare)
npx wrangler dev
npx wrangler dev --remote         # Executa contra recursos reais da Cloudflare

# Geração automática de contratos de tipagem TypeScript a partir do wrangler.jsonc/toml
npx wrangler types

# Deploy para produção ou ambientes específicos (staging/preview)
npx wrangler deploy
npx wrangler deploy --env staging

# Gerenciamento de segredos de ambiente criptografados
npx wrangler secret put API_SECRET_KEY
npx wrangler secret list
npx wrangler secret delete API_SECRET_KEY

# Streaming de telemetria e logs de execução em tempo real
npx wrangler tail
npx wrangler tail --format pretty --status error
```

### 1.3. C3 (`create-cloudflare`): Scaffolding de Projetos
Inicialização padronizada de aplicações Workers e Pages com templates modernos:
```bash
# Inicialização interativa de novos projetos com frameworks suportados
npm create cloudflare@latest meu-projeto-edge
# Suporta: Hono, Astro, Next.js (OpenNext), Remix, Nuxt, SvelteKit
```

### 1.4. `cloudflared` CLI: Túneis Privados e Zero Trust
Permite conectar servidores, contêineres e redes locais diretamente à rede da Cloudflare sem expor nenhuma porta pública de entrada na internet:

```bash
# Autenticação do cloudflared com a conta Cloudflare
cloudflared tunnel login

# Criação de um túnel nomeado
cloudflared tunnel create producao-tunnel

# Roteamento de tráfego DNS para o túnel
cloudflared tunnel route dns producao-tunnel api.minhaempresa.com

# Execução do túnel baseado no arquivo de configuração
cloudflared tunnel run producao-tunnel
```

#### Exemplo de `config.yml` para Ingress Rules Privadas:
```yaml
tunnel: <UUID_DO_TUNEL>
credentials-file: /etc/cloudflared/<UUID_DO_TUNEL>.json

ingress:
  # Roteamento para microsserviço interno seguro
  - hostname: api.minhaempresa.com
    service: http://localhost:8080
    originRequest:
      connectTimeout: 10s
      noTLSVerify: false
  # Fallback obrigatório: retorna 404 para qualquer outro tráfego
  - service: http_status:404
```

---

## ⚡ 2. Edge Compute & Runtime (Workers, Pages & Durable Objects)

### 2.1. Arquitetura V8 Isolates (`workerd`)
Ao contrário de contêineres e funções serverless tradicionais (como AWS Lambda) que dependem de máquinas virtuais pesadas ou processos Node.js com cold start de 200ms–2s, os Workers da Cloudflare rodam sobre o motor open-source **`workerd`** com **V8 Isolates**:
- **Cold Start Zero** (< 5 milissegundos).
- **Consumo de Memória Mínimo**: Centenas de isolates compartilham o mesmo processo com isolamento de memória seguro no nível do runtime V8.
- **Padrões Web Standards**: Suporte nativo a `Fetch API`, `Streams`, `Web Crypto`, `TextEncoder/TextDecoder`, `URLPattern`.

### 2.2. Exemplo Canônico de Worker com TypeScript (`wrangler.jsonc`)

#### Configuração `wrangler.jsonc`:
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "api-gateway-edge",
  "main": "src/index.ts",
  "compatibility_date": "2024-09-01",
  "compatibility_flags": ["nodejs_compat"],
  // Binds para Bancos e Armazenamento
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "app-production-db",
      "database_id": "xxxx-xxxx-xxxx"
    }
  ],
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "app-media-bucket"
    }
  ],
  "kv_namespaces": [
    {
      "binding": "CACHE_KV",
      "id": "yyyy-yyyy-yyyy"
    }
  ]
}
```

#### Código TypeScript do Worker (`src/index.ts`):
```typescript
export interface Env {
  DB: D1Database;
  STORAGE: R2Bucket;
  CACHE_KV: KVNamespace;
  API_SECRET_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Rota de Health Check
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "healthy", region: request.cf?.colo }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    // Consulta otimizada com D1 (SQLite distribuído)
    if (url.pathname === "/users" && request.method === "GET") {
      // Checa cache na borda via KV
      const cached = await env.CACHE_KV.get("active_users", "json");
      if (cached) {
        return Response.json(cached, { headers: { "X-Cache": "HIT" } });
      }

      const { results } = await env.DB.prepare(
        "SELECT id, name, email, created_at FROM users WHERE active = 1 LIMIT 50"
      ).all();

      // Salva no KV em background sem bloquear a resposta ao usuário
      ctx.waitUntil(env.CACHE_KV.put("active_users", JSON.stringify(results), { expirationTtl: 300 }));

      return Response.json(results, { headers: { "X-Cache": "MISS" } });
    }

    return new Response("Not Found", { status: 404 });
  }
};
```

---

## 💾 3. Armazenamento e Bancos de Dados na Borda

A Cloudflare oferece uma suíte completa de persistência sem servidor na borda:

| Serviço | Modelo de Dados | Caso de Uso Principal | Diferencial Técnico |
| :--- | :--- | :--- | :--- |
| **D1** | SQL Relacional (SQLite) | Perfis, autenticação, catálogos, transações | Réplicas de leitura globais, ACID, sem provisionamento. |
| **R2** | Armazenamento de Objetos (S3 API) | Mídias, uploads, backups, datasets de ML | **Zero Egress Fees** (sem taxa de saída de dados). |
| **Workers KV** | Chave-Valor Global | Configurações, tokens, cache de sessões | Leitura ultrarrápida (sub-milissegundo) distribuída. |
| **Vectorize** | Banco Vetorial de Embeddings | Busca semântica, RAG, classificação de IA | Integração nativa com Workers AI e modelos de embeddings. |
| **Hyperdrive** | Acelerador de Conexões SQL | PostgreSQL e MySQL externos | Connection pooling e caching de queries na borda global. |
| **Queues** | Filas de Mensageria Assíncrona | Processamento em lote, pipelines de dados | Entrega garantida *at-least-once*, sem servidores de fila. |

### 3.1. D1: Migrações e Consultas
```bash
# Criação do banco D1
npx wrangler d1 create app-production-db

# Criação de arquivo de migração
npx wrangler d1 migrations create app-production-db criar_tabela_usuarios

# Aplicação local das migrações
npx wrangler d1 migrations apply app-production-db --local

# Aplicação em produção na borda global
npx wrangler d1 migrations apply app-production-db --remote
```

### 3.2. R2: Armazenamento S3-Compatível
```typescript
// Upload de arquivo para o R2 com metadados customizados
await env.STORAGE.put("uploads/relatorio.pdf", request.body, {
  httpMetadata: { contentType: "application/pdf" },
  customMetadata: { autor: "sistema", data: new Date().toISOString() }
});

// Download com streaming direto
const object = await env.STORAGE.get("uploads/relatorio.pdf");
if (!object) return new Response("Objeto não encontrado", { status: 404 });

const headers = new Headers();
object.writeHttpMetadata(headers);
headers.set("etag", object.httpEtag);
return new Response(object.body, { headers });
```

---

## 🛡️ 4. Segurança de Borda, WAF, DNS & Zero Trust

### 4.1. Web Application Firewall (WAF) & Managed Rulesets
- **Cloudflare Managed Ruleset**: Regras mantidas e atualizadas dinamicamente pela equipe de inteligência de ameaças da Cloudflare contra vulnerabilidades zero-day (ex.: Log4j, Spring4Shell).
- **OWASP Core Ruleset**: Proteção rigorosa contra o OWASP Top 10 (SQLi, XSS, RFI/LFI) com escore de anomalia configurável (*Paranoia Level* 1 a 4).
- **Custom Rules**: Expressões booleanas para bloqueio e desafio:
  ```text
  (http.request.uri.path contains "/admin" and not ip.src in {203.0.113.0/24}) -> Action: Block
  (cf.threat_score gt 40 and not cf.client.bot) -> Action: Managed Challenge
  ```
- **Rate Limiting Rules**: Proteção contra brute force e exaustão de recursos limitando, por exemplo, 5 requisições por minuto no endpoint `/api/login` por endereço IP.

### 4.2. Cloudflare Turnstile: Proteção Anti-Bot sem Fricção
Substituto inteligente e que preserva a privacidade contra CAPTCHAs invasivos:
- Validação invisível de telemetria do navegador sem desafios visuais irritantes.
- Verificação do lado do servidor via chamada HTTP simples:
```typescript
const formData = await request.formData();
const token = formData.get("cf-turnstile-response");
const ip = request.headers.get("CF-Connecting-IP");

const verifyRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({
    secret: env.TURNSTILE_SECRET_KEY,
    response: token as string,
    remoteip: ip || ""
  })
});

const outcome = await verifyRes.json<{ success: boolean }>();
if (!outcome.success) {
  return new Response("Falha na validação anti-bot", { status: 403 });
}
```

### 4.3. DNS Anycast, Caching & SSL/TLS
- **DNS Anycast**: Resolução com latência média global inferior a 15ms, suporte automático a DNSSEC e CNAME flattening na raiz (`@`).
- **Cache Rules**: Controle granular de TTL na borda ignorando ou respeitando cabeçalhos `Cache-Control` por URI ou extensão.
- **SSL/TLS Mode**:
  - *Full (Strict)*: Exige certificado TLS válido e emitido por autoridade confiável no servidor de origem.
  - *mTLS (Mutual TLS)*: Autenticação mútua com certificados de cliente para APIs e comunicação entre microsserviços.

### 4.4. Arquitetura Cloudflare Zero Trust (Cloudflare One)
- **Cloudflare Access**: Proteção de aplicações internas sem VPN via proxy reverso autenticado com provedores de identidade corporativos (Google Workspace, Okta, Microsoft Entra ID).
- **Cloudflare Gateway**: Inspeção profunda de tráfego de saída DNS, HTTP/HTTPS e de rede com filtragem de malware e políticas de DLP (Data Loss Prevention).
- **Device Posture**: Concessão de acesso condicionada à saúde da máquina do usuário (presença de antivírus, disco criptografado e versão do SO).
