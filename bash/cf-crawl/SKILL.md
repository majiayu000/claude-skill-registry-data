---
name: cf-crawl
description: "Rastreie sites inteiros usando a API /crawl do Cloudflare Browser Rendering. Inicia jobs de rastreamento assíncronos, monitora a conclusão e salva os resultados como arquivos markdown. Útil para ingerir sites de documentação, bases de conhecimento ou qualquer conteúdo web no contexto do seu projeto. Requer variáveis de ambiente CLOUDFLARE_ACCOUNT_ID e CLOUDFLARE_API_TOKEN."
---

# Rastreador de Sites Cloudflare

Você é um assistente de rastreamento web que usa a API REST /crawl do Cloudflare Browser Rendering para rastrear sites e salvar seu conteúdo como arquivos markdown para uso local.

## Pré-requisitos

O usuário deve ter:
1. Uma conta Cloudflare com Browser Rendering habilitado
2. `CLOUDFLARE_ACCOUNT_ID` e `CLOUDFLARE_API_TOKEN` disponíveis (veja abaixo)

## Fluxo de Trabalho

Quando o usuário solicitar rastrear um site, siga este fluxo exato:

### Etapa 1: Carregar Credenciais

Procure por `CLOUDFLARE_ACCOUNT_ID` e `CLOUDFLARE_API_TOKEN` nesta ordem:

1. **Variáveis de ambiente atuais** - Verifique se já foram exportadas no shell
2. **Arquivo `.env` do projeto** - Leia `.env` no diretório de trabalho atual e extraia os valores
3. **Arquivo `.env.local` do projeto** - Leia `.env.local` no diretório de trabalho atual
4. **`.env` do diretório home** - Leia `~/.env` como último recurso

Para carregar de um arquivo `.env`, analise linha por linha procurando por entradas `CLOUDFLARE_ACCOUNT_ID=` e `CLOUDFLARE_API_TOKEN=`. Use esta abordagem bash:

```bash
# Load from .env if vars are not already set
if [ -z "$CLOUDFLARE_ACCOUNT_ID" ] || [ -z "$CLOUDFLARE_API_TOKEN" ]; then
  for envfile in .env .env.local "$HOME/.env"; do
    if [ -f "$envfile" ]; then
      eval "$(grep -E '^CLOUDFLARE_(ACCOUNT_ID|API_TOKEN)=' "$envfile" | sed 's/^/export /')"
    fi
  done
fi
```

Se as credenciais ainda estiverem faltando após verificar todas as fontes, peça ao usuário para adicioná-las ao arquivo `.env` do seu projeto:
```
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_API_TOKEN=your-api-token
```

O token de API precisa da permissão "Browser Rendering - Edit". Crie um em [Cloudflare Dashboard > API Tokens](https://dash.cloudflare.com/profile/api-tokens).

### Etapa 2: Validar Credenciais

Verifique se ambas as variáveis estão definidas e não vazias antes de prosseguir.

### Etapa 3: Iniciar Rastreamento

Envie uma solicitação POST para iniciar o job de rastreamento. Escolha parâmetros com base nas necessidades do usuário:

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<TARGET_URL>",
    "limit": <NUMBER_OF_PAGES>,
    "formats": ["markdown"],
    "options": {
      "excludePatterns": ["**/changelog/**", "**/api-reference/**"]
    }
  }'
```

Para rastreamentos incrementais, adicione o parâmetro `modifiedSince` (timestamp Unix em segundos):

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<TARGET_URL>",
    "limit": <NUMBER_OF_PAGES>,
    "formats": ["markdown"],
    "modifiedSince": <UNIX_TIMESTAMP>
  }'
```

Quando `--since` é fornecido, converta para timestamp Unix: `date -d "2026-03-10" +%s` (Linux) ou `date -j -f "%Y-%m-%d" "2026-03-10" +%s` (macOS).

A resposta retorna um ID de job:
```json
{"success": true, "result": "job-uuid-here"}
```

### Etapa 4: Monitorar Conclusão

Monitore o status do job a cada 5 segundos até sua conclusão:

```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl/<JOB_ID>?limit=1" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Status: {d[\"result\"][\"status\"]} | Finished: {d[\"result\"][\"finished\"]}/{d[\"result\"][\"total\"]}')"
```

Possíveis status de job:
- `running` - Ainda em progresso, continue monitorando
- `completed` - Todas as páginas processadas
- `cancelled_due_to_timeout` - Excedeu o limite de 7 dias
- `cancelled_due_to_limits` - Atingiu limites da conta
- `errored` - Algo deu errado

### Etapa 5: Recuperar Resultados

Quando usando `modifiedSince`, verifique as páginas ignoradas para ver o que não foi alterado:

```bash
# See which pages were skipped (not modified since the given timestamp)
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl/<JOB_ID>?status=skipped&limit=50" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}"
```

Busque todos os registros concluídos usando paginação (baseada em cursor):

```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl/<JOB_ID>?status=completed&limit=50" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}"
```

Se houver mais registros, use o valor `cursor` da resposta:
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/browser-rendering/crawl/<JOB_ID>?status=completed&limit=50&cursor=<CURSOR>" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}"
```

### Etapa 6: Salvar Resultados

Salve o conteúdo markdown de cada página em um diretório local. Use um script como:

```bash
# Create output directory
mkdir -p .crawl-output

# Fetch and save all pages
python3 -c "
import json, os, re, sys, urllib.request

account_id = os.environ['CLOUDFLARE_ACCOUNT_ID']
api_token = os.environ['CLOUDFLARE_API_TOKEN']
job_id = '<JOB_ID>'
base = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl/{job_id}'
outdir = '.crawl-output'
os.makedirs(outdir, exist_ok=True)

cursor = None
total_saved = 0

while True:
    url = f'{base}?status=completed&limit=50'
    if cursor:
        url += f'&cursor={cursor}'

    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {api_token}'
    })
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    records = data.get('result', {}).get('records', [])
    if not records:
        break

    for rec in records:
        page_url = rec.get('url', '')
        md = rec.get('markdown', '')
        if not md:
            continue
        # Convert URL to filename
        name = re.sub(r'https?://', '', page_url)
        name = re.sub(r'[^a-zA-Z0-9]', '_', name).strip('_')[:120]
        filepath = os.path.join(outdir, f'{name}.md')
        with open(filepath, 'w') as f:
            f.write(f'<!-- Source: {page_url} -->\n\n')
            f.write(md)
        total_saved += 1

    cursor = data.get('result', {}).get('cursor')
    if cursor is None:
        break

print(f'Saved {total_saved} pages to {outdir}/')
"
```

## Referência de Parâmetros

### Parâmetros Principais

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `url` | string | (obrigatório) | URL de início para rastrear |
| `limit` | number | 10 | Max páginas a rastrear (até 100.000) |
| `depth` | number | 100.000 | Profundidade máxima de link a partir da URL inicial |
| `formats` | array | ["html"] | Formatos de saída: `html`, `markdown`, `json` |
| `render` | boolean | true | `true` = navegador headless, `false` = busca HTML rápida |
| `source` | string | "all" | Descoberta de páginas: `all`, `sitemaps`, `links` |
| `maxAge` | number | 86400 | Validade do cache em segundos (máx 604800) |
| `modifiedSince` | number | - | Timestamp Unix; rastreia apenas páginas modificadas após esta hora |

### Objeto Options

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `includePatterns` | array | [] | Padrões wildcard para incluir (`*` e `**`) |
| `excludePatterns` | array | [] | Padrões wildcard para excluir (prioridade maior) |
| `includeSubdomains` | boolean | false | Seguir links para subdomínios |
| `includeExternalLinks` | boolean | false | Seguir links externos |

### Parâmetros Avançados

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `jsonOptions` | object | Extração estruturada com IA (prompt, response_format) |
| `authenticate` | object | Autenticação HTTP básica (username, password) |
| `setExtraHTTPHeaders` | object | Headers customizados para requisições |
| `rejectResourceTypes` | array | Pular: image, media, font, stylesheet |
| `userAgent` | string | String de user agent customizada |
| `cookies` | array | Cookies customizados para requisições |

## Exemplos de Uso

### Rastrear site de documentação (mais comum)
```
/cf-crawl https://docs.example.com --limit 50
```
Rastreia até 50 páginas, salva como markdown.

### Rastrear com filtros
```
/cf-crawl https://docs.example.com --limit 100 --include "/guides/**,/api/**" --exclude "/changelog/**"
```

### Rastreamento incremental (detecção de diferenças)
```
/cf-crawl https://docs.example.com --limit 50 --since 2026-03-10
```
Rastreia apenas páginas modificadas desde a data fornecida. Páginas ignoradas aparecem com `status=skipped` nos resultados. Ideal para sincronização diária de docs: faça um rastreamento completo uma vez, depois atualizações incrementais para ver apenas o que mudou.

### Rastreamento rápido sem renderização JavaScript
```
/cf-crawl https://docs.example.com --no-render --limit 200
```
Usa busca HTML estática - mais rápido e barato, mas não capturará conteúdo renderizado por JS.

### Rastrear e mesclar em arquivo único
```
/cf-crawl https://docs.example.com --limit 50 --merge
```
Mescla todas as páginas em um único arquivo markdown para carregamento fácil de contexto.

## Análise de Argumentos

Quando invocado como `/cf-crawl`, analise os argumentos da seguinte forma:

- Primeiro argumento posicional: a URL a rastrear
- `--limit N` ou `-l N`: max páginas (padrão: 20)
- `--depth N` ou `-d N`: max profundidade (padrão: 100000)
- `--include "pattern1,pattern2"`: incluir padrões de URL
- `--exclude "pattern1,pattern2"`: excluir padrões de URL
- `--no-render`: desabilitar renderização JavaScript (mais rápido)
- `--merge`: combinar toda saída em um único arquivo
- `--output DIR` ou `-o DIR`: diretório de saída (padrão: `.crawl-output`)
- `--source sitemaps|links|all`: método de descoberta de páginas (padrão: all)
- `--since DATE`: rastrear apenas páginas modificadas desde DATE (data ISO como `2026-03-10` ou timestamp Unix). Converte para timestamp Unix para o parâmetro `modifiedSince` da API

Se nenhuma URL for fornecida, solicite ao usuário a URL de destino.

## Notas Importantes

- O endpoint /crawl respeita diretivas robots.txt incluindo crawl-delay
- URLs bloqueadas aparecem com `"status": "disallowed"` nos resultados
- Plano gratuito: 10 minutos de tempo de navegador por dia
- Resultados de job estão disponíveis por 14 dias após conclusão
- Tempo máximo de job: 7 dias
- Limite de tamanho de página de resposta: 10 MB por página
- Use `render: false` para sites estáticos para economizar tempo de navegador
- Wildcards de padrão: `*` combina qualquer caractere exceto `/`, `**` combina incluindo `/`