---
name: enrich-phase-1
description: Fase 1 do enrich-lead — Parsear parametros e detectar nicho
user-invocable: false
---

# Fase 1 — Parse & Detect Niche

Leia os argumentos passados pelo orchestrator: $ARGUMENTS

## 1.1 Parsear parametros

Extraia:
- `--nome "X"` → nome do negocio (OBRIGATORIO)
- `--cidade "X"` → cidade (OBRIGATORIO)
- `--nicho "X"` → nicho/categoria (opcional)
- `--source "X"` → fonte: instagram ou gmaps (opcional)
- `--id "X"` → ID do lead: username ou name|phone (opcional)
- `--telefone "X"` → telefone (opcional)
- `--website "X"` → URL do site atual (opcional)
- `--instagram "X"` → username do Instagram (opcional)

Se --nome ou --cidade estiverem faltando, PARE e avise o usuario.

## 1.2 Detectar nicho → estrategia

Mapeie o --nicho para uma estrategia:

```
ESTRATEGIAS:
  medical    → clinica_medica, medicina_estetica, clinica_fertilidade, nutricionista
  dental     → dentista
  legal      → advogado
  psychology → psicologo
  food       → restaurante, personal_chef, buffet_festas, hamburgueria, pizzaria, cafeteria, padaria, sorveteria, acaiteria, doceria, cervejaria
  hospitality → pet_hotel, coworking, hotel, pousada, hostel
  beauty     → salao_beleza, estetica, tatuagem, massagem_terapia, barbearia
  fitness    → academia, escola_esportiva, beach_tennis_padel, crossfit, pilates
  realty     → imobiliaria
  finance    → contador, assessoria_investimentos
  education  → escola_idiomas, autoescola, escola_infantil, escola_premium
  tech       → software_erp, agencia_marketing, desenvolvimento_web, consultoria_ti
  generic    → qualquer outro nicho
```

Se o nicho nao bater com nenhum, use `generic`.

## 1.3 Salvar no state file

Atualize o state file com os dados parseados:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import json
from datetime import datetime
with open('data/_state/enrichment-progress.json') as f: state = json.load(f)
state['current_phase'] = 1
state['lead_id'] = 'ID_AQUI'
state['nome'] = 'NOME_AQUI'
state['cidade'] = 'CIDADE_AQUI'
state['nicho'] = 'NICHO_AQUI'
state['strategy'] = 'STRATEGY_AQUI'
state['source'] = 'SOURCE_AQUI'
state['started_at'] = datetime.now().isoformat()
state['phases']['phase_1'] = {'status': 'complete'}
# Se tem instagram, ja salvar
if 'INSTAGRAM_AQUI':
    state['discovered_urls']['instagram_username'] = 'INSTAGRAM_AQUI'
if 'WEBSITE_AQUI':
    state['discovered_urls']['site_url'] = 'WEBSITE_AQUI'
with open('data/_state/enrichment-progress.json', 'w') as f: json.dump(state, f, indent=2, ensure_ascii=False)
print('Fase 1 completa')
"
```

## 1.4 Mostrar ao usuario

```
Nicho: [nicho] → Estrategia: [estrategia]
Pesquisas planejadas: X universais + Y especificas do nicho
```

## CRITERIO DE CONCLUSAO
- Todos os parametros obrigatorios parseados (nome, cidade)
- Nicho mapeado para estrategia
- State file criado e populado
- Usuario viu o plano
