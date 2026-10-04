---
name: enrich-phase-7
description: Fase 7 do enrich-lead — Marca, concorrentes, montar JSON, salvar DB
user-invocable: false
---

# Fase 7 — Marca, Concorrentes, Montar JSON & Salvar

Leia o state file COMPLETO:
```bash
cat data/_state/enrichment-progress.json
```

Voce precisa de TODOS os data_points acumulados das fases 2-6.

---

## 7.1 Padroes da marca

Com base em TUDO que foi coletado, analise:

1. **Cores predominantes**: quais cores aparecem no site, logo, Instagram?
2. **Tom de comunicacao**: formal, informal, tecnico, descontraido?
3. **Publico-alvo aparente**: jovens, familias, empresarios, mulheres?
4. **Estilo visual**: minimalista, colorido, profissional, caseiro?
5. **Slogan/tagline**: o negocio tem um?

Crie data_point:
```json
{
  "category": "brand",
  "label": "Padroes da marca",
  "value": "Resumo em 1 linha",
  "detail": {
    "cores": ["azul", "branco"],
    "tom": "formal",
    "publico_alvo": "...",
    "estilo_visual": "...",
    "slogan": "..."
  },
  "source_type": "briefing",
  "source_name": "analise"
}
```

## 7.2 Concorrentes (rapido, sem profundidade)

Uma unica pesquisa:
```
WebSearch: "{palavras-chave do nicho}" "{cidade}" site
```

Liste apenas nome + URL. NAO faca WebFetch nos concorrentes.
```json
{
  "category": "competitors",
  "label": "Concorrentes com site",
  "value": "3 encontrados",
  "detail": ["nome1 - url1", "nome2 - url2", "nome3 - url3"]
}
```

## 7.3 Montar JSON completo

Junte TODOS os data_points das fases 2-7:

```json
{
  "input": {
    "name": "[nome]",
    "city": "[cidade]",
    "source": "[source]",
    "niche": "[nicho]",
    "original_data": {}
  },
  "data_points": [],
  "summary": "[resumo de vendas em 2-3 frases em portugues]",
  "sales_score": 0,
  "generated_at": "[ISO timestamp]"
}
```

## 7.4 Calcular Sales Score (1-10)

Formula:
- Sem site = +3
- Sem redes sociais ativas = +2
- Negocio novo (<12 meses, calcular pela data_abertura do CNPJ) = +2
- Concorrentes com site = +1
- Tem telefone = +1
- Tem CNPJ ativo = +1
- Ja tem site bom = -3
- Muitos canais de venda (3+) = -1

## 7.5 Escrever Summary

2-3 frases DIRETAS e OBJETIVAS em portugues. Deve ser um PITCH pronto para o vendedor.

Exemplo:
"Clinica medica aberta ha 2 anos em Florianopolis, CRM ativo. Sem site e sem presenca digital alem do Instagram (450 seguidores). 3 concorrentes diretos ja tem site profissional. Otimo candidato para proposta de site."

## 7.6 Salvar no banco

Tente via curl primeiro:
```bash
curl -s -X POST http://localhost:3002/api/briefings \
  -H "Content-Type: application/json" \
  -d '{...}'
```

Se falhar, salve direto no SQLite:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import sqlite3, json
from datetime import datetime

db = sqlite3.connect('data/vendedor.db')
db.execute('''CREATE TABLE IF NOT EXISTS briefings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_source TEXT NOT NULL,
    lead_id TEXT NOT NULL,
    lead_name TEXT NOT NULL,
    lead_city TEXT DEFAULT '',
    detected_niche TEXT DEFAULT '',
    niche_label TEXT DEFAULT '',
    briefing_json TEXT NOT NULL DEFAULT '{}',
    status TEXT DEFAULT 'pending',
    error_message TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    site_built INTEGER DEFAULT 0,
    site_sold INTEGER DEFAULT 0,
    site_url TEXT DEFAULT '',
    site_built_at TEXT DEFAULT '',
    UNIQUE(lead_source, lead_id)
);''')

briefing = BRIEFING_JSON_COMPLETO
data = json.dumps(briefing, ensure_ascii=False)

db.execute('''INSERT OR REPLACE INTO briefings
    (lead_source, lead_id, lead_name, lead_city, detected_niche, niche_label, briefing_json, status, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'done', datetime('now'))''',
    ('SOURCE', 'ID', 'NOME', 'CIDADE', 'NICHO', 'LABEL', data))
db.commit()
db.close()
print('Briefing salvo no vendedor.db')
"
```

## 7.7 Exibir resultado

Mostre ao usuario:

```
========================================
  BRIEFING COMPLETO
========================================
  Lead: [nome] ([cidade])
  Nicho: [nicho] → [estrategia]
  Score de Venda: [X]/10
========================================

  RESUMO:
  [summary]

  IDENTIDADE:
  - CNPJ: [valor]
  - Razao Social: [valor]
  - Abertura: [data] ([X meses])
  - Porte: [valor]

  REGISTRO PROFISSIONAL:
  - [CRM/CRO/OAB]: [valor]

  PRESENCA WEB:
  - Site: [URL] | Tech: [stack] | SSL: [sim/nao]
  - Instagram: [@user] ([seguidores] seg.)
  - Facebook: [URL]
  - LinkedIn: [URL]

  IMAGENS CAPTURADAS:
  - Logo: [N]
  - Fotos estabelecimento: [N]
  - Fotos produtos: [N]
  - Fotos equipe: [N]
  - Posts Instagram: [N]
  - Total: [N] imagens

  CANAIS DE VENDA:
  - iFood: [sim/nao]
  - Doctoralia: [sim/nao]
  - [outros por nicho]

  MARCA:
  - Cores: [cores]
  - Tom: [formal/informal]
  - Publico: [descricao]

  HISTORIA:
  [texto se encontrado]

  CONCORRENTES COM SITE:
  1. [nome] - [url]
  2. [nome] - [url]
  3. [nome] - [url]

  Salvo em: data/vendedor.db
========================================
```

## 7.8 Marcar state como completo

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import json
from datetime import datetime
with open('data/_state/enrichment-progress.json') as f: state = json.load(f)
state['current_phase'] = 7
state['completed_at'] = datetime.now().isoformat()
state['phases']['phase_7'] = {'status': 'complete', 'result': 'Briefing salvo no vendedor.db'}
with open('data/_state/enrichment-progress.json', 'w') as f: json.dump(state, f, indent=2, ensure_ascii=False)
"
```

## CRITERIO DE CONCLUSAO
- Brand analysis completa
- Concorrentes buscados
- JSON completo montado com TODOS data_points
- Sales score calculado (1-10)
- Summary escrito em portugues (pitch pronto)
- Salvo no vendedor.db (curl ou SQLite)
- Resultado formatado exibido ao usuario
- State file marcado como completo
