---
name: lead-phase-6
description: Fase 6 do lead-finder — Resumo final, CSV e fechar sessao
user-invocable: false
---

# Fase 6 — Resumo + CSV + Fechar

Leia o state file:
```bash
cat data/_state/lead-finder-progress.json
```

## 6.1 Garantir CSV salvo

Verifique que todos os leads foram salvos via `instagram_append_lead` na Fase 4.
Se algum ficou pendente, salve agora.

Identifique o CSV gerado:
```bash
ls -t leads/leads_*.csv | head -1
```

## 6.2 Mostrar resumo

```
========================================
  RESULTADO — Lead Finder (Playwright)
========================================
  Nicho: [nicho] | Cidade: [cidade]
  Candidatos Google:     XX
  Do cache (pulados):    XX
  Validados:             XX
  Leads encontrados:     XX
    QUENTES: XX
    MORNOS:  XX
    FRIOS:   XX
  Similares descobertos: XX
  CSV: leads/leads_XXXXXXXX.csv
========================================

  TOP LEADS:
  ──────────────────────────────────────
  1. @username (QUENTE, score 8)
     Nome: [full_name]
     [followers] seg. | [posts] posts
     Bio: [resumo bio]
     Site: nenhum
     Fotos: [N] imagens HD capturadas
     Motivos: sem site, conta comercial, conta nova

  2. @username (QUENTE, score 7)
     ...
  ──────────────────────────────────────

  PROXIMO PASSO:
  /enrich-lead --nome "X" --cidade "Y" --nicho "Z" --source "instagram" --id "@username" --instagram "username"
========================================
```

## 6.3 Fechar sessao do browser

NAO faca logout do Instagram — os cookies persistem entre sessoes.
Apenas navegue para uma pagina neutra:
```
browser_navigate: about:blank
```

Isso deixa a sessao do Instagram ativa para a proxima vez.

## 6.4 Atualizar state

Marque a sessao como completa:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import json
from datetime import datetime
with open('data/_state/lead-finder-progress.json') as f: state = json.load(f)
state['current_phase'] = 6
state['phases']['phase_6'] = {'status': 'complete'}
state['completed_at'] = datetime.now().isoformat()
with open('data/_state/lead-finder-progress.json', 'w') as f: json.dump(state, f, indent=2, ensure_ascii=False)
"
```

## CRITERIO DE CONCLUSAO
- CSV verificado e path confirmado
- Resumo formatado mostrado ao usuario
- Top leads listados com detalhes
- Sessao do browser limpa (sem logout)
- Sugestao de /enrich-lead para os melhores leads
- State marcado como completo
