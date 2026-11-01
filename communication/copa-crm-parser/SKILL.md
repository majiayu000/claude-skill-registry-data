---
name: copa-crm-parser
description: Interpretar e consolidar os resultados CRM da campanha Copa 2026, seguindo
  os arquivos e o fluxo desta skill.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Relatórios
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Skill: copa-crm-parser

## Quando usar
Acionar sempre que o usuário quiser atualizar, regenerar ou analisar os resultados CRM da campanha Copa do Mundo 2026 (Meu Afinz Visa Bate Um Bolão). Triggers:
- "atualizar resultados copa"
- "subir novo csv de resultados"
- "gerar xlsx copa"
- "resultados copa" + arquivo anexado
- "síntese copa" / "performance copa"

## O que faz
Recebe o arquivo de resultados SFMC (CSV ou XLSX no formato multi-bloco da Afinz) e gera `Copa2026_CRM.xlsx` com:
- **Aba Diário**: 1 linha por disparo/dia, join completo CRM + funil de aquisição
- **Aba Semanal**: agregado por semana × parceiro × tipo × canal, com linha de totais

## Contexto da campanha
- **Nome**: Meu Afinz Visa Bate Um Bolão — Copa do Mundo 2026
- **Período**: 15 Abr – 15 Ago 2026
- **Parceiros**: B2C (Afinz direto), Bem Barato, Plurix, DIA
- **Canais CRM**: WPP (WhatsApp Mkt), EMAIL, SMS, PUSH
- **Funil**: proposta_uniq → aprovados_uniq → finalizados
- **Tipos**: Aquisição, Rentabilização, Reativação
- **Ondas**: O1(01/04), O2(15/04-launch), O3(01/05), O4(15/05), O5(01/06), O6(15/06)

## Estrutura do arquivo de resultados SFMC

O CSV/XLSX tem layout multi-bloco em colunas paralelas na mesma sheet:

| Colunas (1-based) | Bloco         | Campos principais |
|-------------------|---------------|-------------------|
| 1–7               | WPP           | journey, activity, date, sent, delivered, read |
| 9–15              | EMAIL         | journey, activity, date, sent, delivered, opens, clicks |
| 17–22             | SMS           | journey, activity, date, sent_uniq, delivered_uniq, undelivered |
| 24–32             | PERF (funil)  | journey, activity, date_inicio, canal, proposta, aprovados, finalizados, assistida, independente |
| 36–43             | PUSH          | journey, activity, date, attempts, success, fail, not_found, unregistered |

- Linha 1: filtros de pivot (ignorar)
- Linha 2: primeiros dados do bloco PERF (começa antes dos outros)
- Linha 3: headers dos blocos CRM (WPP/EMAIL/SMS/PUSH)
- Linha 4+: dados

## Regras de detecção Copa
Filtrar linhas onde journey ou activity contém `copa` (case-insensitive).

## Taxonomia e incongruências conhecidas

### Padrão de activity name
`empresa_produto_parceiro_tipo_canal_publico_descricao_frequencia`

Exemplo: `afz_car_vis_aqs_email_bsp_disp1copa_pontual`
- pos[0]=empresa, pos[1]=produto, pos[2]=parceiro, pos[3]=tipo, pos[4]=canal, pos[5]=público

### Mapeamento de parceiro (com incongruências)
```python
PARTNER_MAP = {
    # Activity name pos[2] ou pos[0]
    'bbt': 'Bem Barato',   # WPP activities BB (afz_car_bbt_...)
    'bb':  'Bem Barato',   # Email activities BB (afz_car_vis_aqs_email_bb_...)
                           # INCONGRUÊNCIA: mesma empresa, duas siglas
    'dia': 'DIA',
    'vis': 'B2C',          # Visa/Afinz direto quando empresa=afz
    # Journey name (contains)
    'PLURIX': 'Plurix',    # Journeys usam nome completo, não 'plx' da taxonomia
    'B2B2C_BB': 'Bem Barato',
    'B2B2C_DIA': 'DIA',
    'B2C': 'B2C',
}
# Regra: se empresa=plu (pos[0]), parceiro=Plurix independente do resto
```

### Incongruências documentadas (não corrigir, apenas classificar corretamente)
1. **Bem Barato dupla sigla**: `bb` (emails) vs `bbt` (WPP) — ambos → Bem Barato
2. **Plurix dupla representação**: empresa `plu_` nas activities, nome `PLURIX` nas journeys
3. **`upo`** no campo público (plu_car_vis_aqs_sms_upo_...) → não existe na taxonomia → classificar como público='Upload'
4. **`rec`** ambíguo: como público=Recência (pos[5]), como área=Recorrente (pos[1]) → resolver por posição
5. **Segmentos ad-hoc**: `clus2`, `clustermar`, `ecred`, `int`, `21D`, `SAB`, `PROPRI`, `FASE1` → capturar no campo `segmento_adhoc`
6. **Grafia de período**: `ABR26`=`ABRI26`, `MAI26`=`MAIO26` → normalizar para mesmo valor
7. **Journey sem B2B2C**: `JOR_AQUISICAO_BB_...` deveria ser `JOR_AQUISICAO_B2B2C_BB_...` → ainda é Bem Barato
8. **Carrinho abandonado usa `_aqs_`**: journeys `ABD_REATIVACAO`, `PROPRI_ABD`, `SAB_ABD`, `21D_ABD` têm `_aqs_` no activity name mas são Reativação — classificar pelo nome da journey
9. **Finalizados ECRED ausentes no SFMC**: journeys ABD (carrinho abandonado via ECRED) não têm resultado no bloco PERF. Resultado real vem do GaaS (coluna `Emitidos`). Mapeamento manual em `ECRED_FINALIZADOS` no script.

### Mapeamento de tipo
```python
TIPO_TOKENS = [
    ('JOR_RENTABILIZACAO', 'Rentabilização'),
    ('_rnt_',              'Rentabilização'),
    ('sorteio',            'Rentabilização'),
    ('cartonista',         'Rentabilização'),
    ('REATIVACAO',         'Reativação'),
    ('_rtv_',              'Reativação'),
    # Incongruência 8: carrinho abandonado usa _aqs_ mas é Reativação
    ('abd_reativacao',     'Reativação'),
    ('propri_abd',         'Reativação'),
    ('sab_abd',            'Reativação'),
    ('21d_abd',            'Reativação'),
    # default: 'Aquisição'
]
```

### Finalizados ECRED (Incongruência 9)
Atualizar `ECRED_FINALIZADOS` no script a cada ciclo com dados do GaaS (Performance > aba ECRED).
Chave: `(activity_name, 'YYYY-MM-DD')` → int emitidos.

## Lógica de join CRM + PERF
- Chave: `(activity_name, data)` — exata nos dois blocos
- 123/141 linhas fazem match completo
- 18 linhas CRM-only (rentabilização/sorteio sem funil) → colunas funil ficam vazias
- 0 linhas PERF-only sem CRM (ECRED-API aparece no bloco PERF com canal='ECRED-API')
- Finalizados = PERF + ECRED_FINALIZADOS (somados)

## Colunas do output

### Aba Diário
| Coluna | Descrição |
|--------|-----------|
| data | YYYY-MM-DD |
| semana_inicio | segunda-feira da semana (YYYY-MM-DD) |
| partner | B2C / Bem Barato / Plurix / DIA |
| tipo | Aquisição / Rentabilização / Reativação |
| canal | WPP / EMAIL / SMS / PUSH / ECRED-API |
| journey | nome da jornada SFMC |
| activity | nome da atividade SFMC |
| enviados | int |
| entregues | int |
| abertos_lidos | int (null para SMS) |
| cliques | int (só EMAIL) |
| proposta | int (null se sem funil) |
| aprovados | int |
| finalizados | int |
| tx_entrega | % fórmula Excel |
| tx_abertura | % fórmula Excel |
| tx_conv_fin | % fórmula Excel |

### Aba Semanal
Mesmos campos agregados por (semana × partner × tipo × canal), com linha TOTAL.

## Como executar
Rodar o script `scripts/parse_copa_crm.py` passando o caminho do arquivo de entrada.
O script gera `Copa2026_CRM.xlsx` na mesma pasta do arquivo de entrada ou no workspace.

## Instruções para Claude
1. Identificar o arquivo de resultados anexado (CSV ou XLSX)
2. Copiar para o diretório de trabalho se necessário
3. Rodar `python scripts/parse_copa_crm.py <caminho_arquivo>`
4. Rodar recalc.py para resolver fórmulas
5. Mover output para workspace folder
6. Apresentar resumo: total de linhas, parceiros, período, totais de enviados/finalizados
