---
name: descobrindo-odoo-estrutura
description: "Descobre campos e estrutura de qualquer modelo do Odoo. Lista campos de tabela, busca campo por nome, inspeciona registro, faz consulta generica. Use quando: nao conhecer um modelo Odoo, precisar descobrir nome de campo, explorar estrutura de tabela, consulta em modelo nao mapeado."
---

# Descobrindo Odoo Estrutura

Skill para **descoberta de campos e estrutura** de modelos do Odoo.

> **QUANDO USAR:** Quando o Agent nao conhecer um modelo/campo especifico do Odoo
> e precisar descobrir a estrutura para enriquecer a resposta ao usuario.

## Casos de Uso

1. **Usuario pergunta sobre dado que nao esta mapeado**
   - Agent usa esta skill para descobrir campos
   - Retorna informacao enriquecida ao usuario

2. **Implementar nova consulta**
   - Descobrir estrutura do modelo
   - Mapear campos relevantes
   - Documentar em rastreando-odoo (references/relacionamentos.md)

3. **Debug de integracoes**
   - Inspecionar registro especifico
   - Verificar valores de campos

## Script Disponivel

### descobrindo.py

```bash
source .venv/bin/activate && \
python .claude/skills/descobrindo-odoo-estrutura/scripts/descobrindo.py [opcoes]
```

### Operacoes Disponiveis

| Operacao | Flag | Descricao | Exemplo |
|----------|------|-----------|---------|
| Listar campos | `--listar-campos` | Lista todos os campos do modelo | `--modelo res.partner --listar-campos` |
| Buscar campo | `--buscar-campo` | Busca campo por nome/descricao | `--modelo res.partner --buscar-campo cnpj` |
| Inspecionar | `--inspecionar` | Mostra todos os campos de um registro | `--modelo res.partner --inspecionar 123` |
| Consulta generica | `--filtro` | Consulta com filtro JSON | `--modelo res.partner --filtro '[["name","ilike","teste"]]'` |

### Parametros

| Parametro | Obrigatorio | Descricao |
|-----------|-------------|-----------|
| `--modelo` | Sim | Nome do modelo Odoo (ex: `res.partner`, `account.move`) |
| `--listar-campos` | Nao | Lista todos os campos do modelo |
| `--buscar-campo` | Nao | Termo para buscar nos nomes/descricoes dos campos |
| `--inspecionar` | Nao | ID do registro para inspecionar |
| `--filtro` | Nao | Filtro em formato JSON |
| `--campos` | Nao | Campos a retornar (JSON), usado com --filtro |
| `--limit` | Nao | Limite de resultados (padrao: 10) |
| `--json` | Nao | Saida em formato JSON |

## Exemplos de Uso

### Descobrir campos de um modelo
```bash
python .../descobrindo.py --modelo l10n_br_ciel_it_account.dfe --listar-campos
```

### Buscar campo especifico
```bash
python .../descobrindo.py --modelo res.partner --buscar-campo cnpj
```

### Inspecionar registro
```bash
python .../descobrindo.py --modelo res.partner --inspecionar 123
```

### Consulta generica com filtro
```bash
python .../descobrindo.py \
  --modelo res.partner \
  --filtro '[["vat","ilike","93209765"]]' \
  --campos '["id","name","vat"]' \
  --limit 5
```

## Modelos Conhecidos (Referencia)

| Modelo | Descricao | Skill Relacionada |
|--------|-----------|-------------------|
| `l10n_br_ciel_it_account.dfe` | Documentos Fiscais | rastreando-odoo |
| `l10n_br_ciel_it_account.dfe.line` | Linhas dos DFE | rastreando-odoo |
| `res.partner` | Parceiros (clientes, fornecedores) | rastreando-odoo |
| `account.move` | Faturas/Lancamentos | rastreando-odoo |
| `account.move.line` | Linhas de fatura | rastreando-odoo |
| `purchase.order` | Pedidos de compra | rastreando-odoo |
| `sale.order` | Pedidos de venda | rastreando-odoo |
| `product.product` | Produtos | - |

## Fluxo de Trabalho

```
Usuario pergunta sobre dado desconhecido
        │
        ▼
Agent verifica: modelo/campo conhecido?
        │
        ├── SIM → Usa rastreando-odoo para consultar fluxos
        │
        └── NAO → Usa esta skill para descobrir
                    │
                    ▼
              descobrindo.py --modelo X --listar-campos
                    │
                    ▼
              Retorna informacao ao usuario
```

## Relacionado

| Skill | Uso |
|-------|-----|
| rastreando-odoo | Consultas e rastreamento de fluxos documentais (NF, PO, SO, titulos) |
| integracao-odoo | Desenvolvimento de novas integracoes |
| gerindo-expedicao | Consultas de carteira, separacoes e estoque |
