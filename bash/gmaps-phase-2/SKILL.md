---
name: gmaps-phase-2
description: Fase 2 do gmaps-leads — Executar script Python de scraping
user-invocable: false
---

# Fase 2 — Executar Script Python

Leia o state file:
```bash
cat data/_state/gmaps-progress.json
```

## 2.1 Executar o scraper

Execute o comando montado na Fase 1:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python gmaps_leads.py [COMANDO_DA_FASE_1]
```

O script:
- Gera queries automaticamente
- Scrape Google Maps via Playwright headless
- Verifica websites (live, dead, no_url)
- Aplica filtros
- Exporta CSV em leads/
- Mostra resumo no terminal

**TIMEOUT:** O script pode demorar. Use timeout de 600000ms (10 min).

## 2.2 Capturar resultado

Do output do script, extraia:
- Path do CSV gerado (linha "CSV: leads/...")
- Total scrapeados
- Total filtrados
- Leads listados

## 2.3 Salvar no state

Atualize: csv_path, total_found, total_filtered.

Se o script falhar:
- Timeout → sugerir reduzir --limite ou focar em bairro especifico
- Playwright error → verificar instalacao
- Registrar erro no state e avisar usuario

## CRITERIO DE CONCLUSAO
- Script executou sem erro
- CSV gerado com pelo menos 1 lead
- Totais salvos no state
- Se zero resultados: registrar e avisar usuario
