---
name: gmaps-phase-3
description: Fase 3 do gmaps-leads — Apresentar resultados e salvar no DB
user-invocable: false
---

# Fase 3 — Apresentar + Salvar no DB

Leia o state file:
```bash
cat data/_state/gmaps-progress.json
```

## 3.1 Ler CSV gerado

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
head -50 {csv_path}
```

Ou via Python para parsing completo:
```bash
.venv/bin/python3 -c "
import csv, json
with open('CSV_PATH') as f:
    reader = csv.DictReader(f)
    leads = list(reader)
print(json.dumps({
    'total': len(leads),
    'sem_site': len([l for l in leads if l.get('website_status') in ('no_url', 'dead', 'social_only')]),
    'com_telefone': len([l for l in leads if l.get('phone')]),
    'top_10': leads[:10]
}, ensure_ascii=False, indent=2))
"
```

## 3.2 Salvar no gmaps_leads.db

Insira os leads na tabela `visited` do banco:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import csv, sqlite3, json
from datetime import datetime

db = sqlite3.connect('data/gmaps_leads.db')

with open('CSV_PATH') as f:
    reader = csv.DictReader(f)
    for lead in reader:
        try:
            db.execute('''INSERT OR IGNORE INTO visited
                (name, address, phone, category, rating, reviews,
                 website, website_status, price_range,
                 google_maps_url, lat, lng,
                 niche, source, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'google_maps', datetime('now'))''',
                (lead.get('name',''), lead.get('address',''),
                 lead.get('phone',''), lead.get('category',''),
                 float(lead.get('rating') or 0), int(lead.get('reviews') or 0),
                 lead.get('website',''), lead.get('website_status',''),
                 lead.get('price_range',''),
                 lead.get('google_maps_url',''),
                 float(lead.get('lat') or 0), float(lead.get('lng') or 0),
                 'NICHO'))
        except Exception as e:
            pass

db.commit()
print(f'Leads salvos no gmaps_leads.db')
db.close()
"
```

## 3.3 Apresentar ao usuario

```
========================================
  RESULTADO — Google Maps
========================================
  Nicho: [nicho] | Local: [local]
  Total encontrados: [N]
  Apos filtros: [N]
  Sem website: [N]
  Com telefone: [N]
========================================

  TOP LEADS:
  ──────────────────────────────────────
  1. [nome]
     Tel: [phone] | Nota: [rating] | [reviews] aval. | Site: [status]
  2. [nome]
     ...
  ──────────────────────────────────────

  CSV: [path]
  DB: data/gmaps_leads.db

  Proximo passo: /enrich-lead --nome "X" --cidade "Y" --nicho "Z" --source "gmaps"
========================================
```

## CRITERIO DE CONCLUSAO
- CSV lido e parseado
- Leads salvos no gmaps_leads.db
- Resumo formatado mostrado ao usuario
- Top 10 leads listados com detalhes
