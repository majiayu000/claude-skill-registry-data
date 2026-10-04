---
name: enrich-phase-3
description: Fase 3 do enrich-lead — CNPJ e registro profissional
user-invocable: false
---

# Fase 3 — Identidade & Registro Profissional

Leia o state file:
```bash
cat data/_state/enrichment-progress.json
```

Extraia: nome, cidade, nicho, strategy.

## 3.1 Buscar CNPJ

```
WebSearch: CNPJ "{nome}" "{cidade}"
```

Procure o padrao de CNPJ nos resultados: `\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}`

Se o lead ja veio com CNPJ nos dados originais, use esse diretamente.

### Consultar dados do CNPJ

Se encontrou CNPJ, faca WebFetch:
```
WebFetch: https://brasilapi.com.br/api/cnpj/v1/{cnpj_sem_pontuacao}
```

Dados retornados: razao_social, nome_fantasia, data_inicio_atividade, porte, cnae_fiscal_descricao, logradouro, municipio, uf, telefone, email, qsa (socios).

Crie data_point:
```json
{
  "category": "identity",
  "label": "CNPJ",
  "value": "XX.XXX.XXX/XXXX-XX",
  "detail": {
    "razao_social": "...",
    "nome_fantasia": "...",
    "data_abertura": "...",
    "porte": "...",
    "cnae": "...",
    "socios": ["..."],
    "endereco": "...",
    "telefone": "...",
    "email": "..."
  },
  "source_type": "briefing",
  "source_name": "BrasilAPI",
  "fetched_at": "..."
}
```

Se NAO encontrou CNPJ: registre data_point com value "Nao encontrado" e siga em frente.

## 3.2 Registro profissional (por nicho)

Execute SOMENTE a pesquisa relevante para o nicho:

**medical (medico):**
```
WebSearch: consultacrm.com.br "{nome}" "{estado}"
WebSearch: CRM "{nome}" "{cidade}" medico
```
Se encontrar: numero CRM, especialidade, situacao.

**dental (dentista):**
```
WebSearch: CRO "{estado}" "{nome}" dentista
WebSearch: "{nome}" "{cidade}" dentista CRO
```

**legal (advogado):**
```
WebSearch: cna.oab.org.br "{nome}"
WebSearch: OAB "{estado}" "{nome}" advogado
WebSearch: jusbrasil.com.br "{nome}" advogado
```

**psychology (psicologo):**
```
WebSearch: CRP "{estado}" "{nome}" psicologo
```

**finance (contador):**
```
WebSearch: CRC "{estado}" "{nome}" contador
```

**realty (corretor):**
```
WebSearch: CRECI "{estado}" "{nome}" corretor
```

Para outros nichos (food, beauty, fitness, tech, hospitality, education, generic): PULE este passo — nao tem registro profissional obrigatorio.

Crie data_point com category "professional_registry" se encontrar.

## 3.3 Salvar no state

Append data_points ao state file e marque fase completa.

## CRITERIO DE CONCLUSAO
- CNPJ buscado (encontrado ou "nao encontrado" registrado)
- BrasilAPI consultada se CNPJ encontrado
- Registro profissional buscado para nichos aplicaveis
- data_points salvos no state
