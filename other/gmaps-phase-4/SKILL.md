---
name: gmaps-phase-4
description: Fase 4 do gmaps-leads — Enriquecer top leads com CNPJ (opcional)
user-invocable: false
---

# Fase 4 — Enriquecer com CNPJ (Opcional)

Esta fase e OPCIONAL. So execute se:
- O usuario pediu --enrich-cnpj
- OU existem leads promissores (sem site + com telefone)

Leia o state file:
```bash
cat data/_state/gmaps-progress.json
```

## 4.1 Selecionar leads para enriquecer

Do CSV, selecione os top 5-10 leads mais promissores:
- Prioridade: sem site + com telefone + boa nota
- NAO enriquecer mais de 10 (BrasilAPI tem rate limits)

## 4.2 Buscar CNPJ para cada lead

Para cada lead selecionado:

```
WebSearch: CNPJ "{nome}" "{cidade}"
```

Procure padrao CNPJ: `\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}`

Se encontrou:
```
WebFetch: https://brasilapi.com.br/api/cnpj/v1/{cnpj_sem_pontuacao}
```

Extraia: razao_social, nome_fantasia, data_inicio_atividade, porte, cnae, socios, endereco.

## 4.3 Atualizar no DB

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import sqlite3
db = sqlite3.connect('data/gmaps_leads.db')
db.execute('''UPDATE visited SET
    cnpj = ?,
    razao_social = ?,
    nome_fantasia = ?,
    data_abertura = ?,
    idade_meses = ?,
    porte = ?,
    cnae = ?,
    cnpj_status = ?
    WHERE name = ? AND address LIKE ?''',
    ('CNPJ', 'RAZAO', 'FANTASIA', 'DATA', MESES, 'PORTE', 'CNAE', 'STATUS', 'NOME', '%ENDERECO%'))
db.commit()
db.close()
"
```

## 4.4 Mostrar resultado

```
CNPJ ENRIQUECIDO:
  1. [nome] → CNPJ: [cnpj] | Abertura: [data] ([X meses]) | Porte: [porte]
  2. [nome] → Nao encontrado
  ...
```

Se --max-idade-empresa foi passado, filtrar leads cuja idade_meses > max.

## CRITERIO DE CONCLUSAO
- Top leads selecionados
- CNPJ buscado via WebSearch + BrasilAPI
- DB atualizado com dados do CNPJ
- Resultado mostrado ao usuario
- Se nenhum CNPJ encontrado: registrar e seguir
