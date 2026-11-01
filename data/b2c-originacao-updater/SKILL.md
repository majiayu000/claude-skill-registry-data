---
name: b2c-originacao-updater
description: 'Skill 1 de 2 do sistema GaaS. Lê a planilha "Orçamento B2C (B2C Produção
  diária)" em XLSX ou CSV e numa única passada grava dois registros por data na tabela
  b2c_daily_metrics: um com tipo=''total'' (Total B2C) e outro com tipo=''serasa_api''
  (canal integrado Serasa). A tabela precisa ter PK composta (data, tipo) — ver seção
  de migration. Acionar quando o usuário mencionar: atualizar originação B2C, subir
  planilha de produção diária, sincronizar resultados B2C, produção diária B2C, Serasa
  API.'
metadata:
  version: 1.0.0
  origin: cowork
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Ingestão de dados
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# 📊 B2C Originação Updater — GaaS Data Sync (Skill 1)

## Objetivo

Receber a planilha `Orçamento B2C (B2C Produção diária)`, fazer uma única passada e gravar **dois registros por data** na tabela `b2c_daily_metrics`:

| tipo | O que representa | Campos populados |
|------|-----------------|-----------------|
| `total` | Total B2C do dia (inclui todos os canais) | propostas_total, emissoes_total, percentual_conversao, observacoes |
| `serasa_api` | Canal integrado Serasa API isolado | emissoes_total, percentual_share, pct_conv_canal |

Isso permite comparar diariamente quanto do resultado total veio especificamente do canal Serasa.

---

## MIGRATION NECESSÁRIA (aplicar antes da primeira execução)

A tabela `b2c_daily_metrics` existe mas tem `data` como PRIMARY KEY simples. Precisa ser ajustada para suportar dois registros por data.

```sql
-- supabase/migrations/007_add_tipo_b2c_daily_metrics.sql

-- 1. Adicionar coluna tipo
ALTER TABLE b2c_daily_metrics
ADD COLUMN IF NOT EXISTS tipo VARCHAR(20) NOT NULL DEFAULT 'total';

-- 2. Adicionar coluna para %conv específica do canal Serasa
--    (disponível apenas em Março e Abril+ na planilha)
ALTER TABLE b2c_daily_metrics
ADD COLUMN IF NOT EXISTS pct_conv_canal DECIMAL(5,2);

-- 3. Adicionar coluna para share do canal no total do dia
--    (% integrado/dia — quanto do total veio da Serasa)
ALTER TABLE b2c_daily_metrics
ADD COLUMN IF NOT EXISTS percentual_share DECIMAL(5,2);

-- 4. Remover PK simples em data
--    ATENÇÃO: verificar nome real antes de dropar:
--    SELECT constraint_name FROM information_schema.table_constraints
--    WHERE table_name = 'b2c_daily_metrics' AND constraint_type = 'PRIMARY KEY';
ALTER TABLE b2c_daily_metrics DROP CONSTRAINT IF EXISTS b2c_daily_metrics_pkey;

-- 5. Nova PK composta (data + tipo)
ALTER TABLE b2c_daily_metrics
ADD CONSTRAINT b2c_daily_metrics_pkey PRIMARY KEY (data, tipo);

-- 6. Índices
CREATE INDEX IF NOT EXISTS idx_b2c_tipo      ON b2c_daily_metrics(tipo);
CREATE INDEX IF NOT EXISTS idx_b2c_data_tipo ON b2c_daily_metrics(data, tipo);

-- 7. Migrar dados existentes para não perder nada
UPDATE b2c_daily_metrics SET tipo = 'total' WHERE tipo IS NULL OR tipo = '';
```

### Schema final

```
b2c_daily_metrics (
  data                DATE NOT NULL,
  tipo                VARCHAR(20) NOT NULL DEFAULT 'total',  -- 'total' | 'serasa_api'
  propostas_total     INTEGER,        -- preenchido para 'total', NULL para 'serasa_api'
  emissoes_total      INTEGER,        -- cartões do dia (total) ou cartões Serasa
  percentual_conversao DECIMAL(5,2),  -- %conv do dia (para 'total')
  percentual_share    DECIMAL(5,2),   -- % do canal Serasa no total do dia (para 'serasa_api')
  pct_conv_canal      DECIMAL(5,2),   -- %conv específica do canal Serasa (Mar+ se disponível)
  observacoes         TEXT,           -- apenas para 'total'
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data, tipo)
)
```

---

## ESTRUTURA DA PLANILHA FONTE

A planilha é uma ferramenta de gestão interna. Os dados úteis começam na **linha 73** — ignorar as linhas 1–72 completamente.

- **Header:** linha 73 (índice 72 base-0 no CSV)
- **Dados:** linha 74 em diante (índice 73+)
- **Separador CSV:** ponto-e-vírgula (`;`)
- **Encoding:** Windows-1252 / Latin-1 — `raw.decode('latin-1')`, nunca UTF-8
- **Números brasileiros:** `.` = milhar, `,` = decimal (`3.306` → 3306 / `1,59%` → 1.59)
- **Layout:** horizontal — cada mês num bloco de colunas, não é tabela vertical

### Posições — tipo `total`

| Mês | Col data | Col Propostas | Col Cartões | Col %Conv | Col Obs |
|-----|----------|---------------|-------------|-----------|---------|
| Jan | 1 | 3 | 4 | 5 | 6 |
| Fev | 12 | 14 | 15 | 16 | 17 |
| Mar | 21 | 23 | 24 | 25 | 26 |
| Abr | 32 | 34 | 35 | 36 | 37 |
| Mai | 43 | 45 | 46 | 47 | 48 |
| Jun | 50 | 52 | 53 | 54 | 55 |
| Jul | 57 | 59 | 60 | 61 | 62 |
| Ago | 64 | 66 | 67 | 68 | 69 |
| Set | 71 | 73 | 74 | 75 | 76 |
| Out | 78 | 80 | 81 | 82 | 83 |
| Nov | 85 | 87 | 88 | 89 | 90 |
| Dez | 92 | 94 | 95 | 96 | 97 |

### Posições — tipo `serasa_api`

Colunas adjacentes ao bloco de cada mês. Jan e Fev têm 2 campos; Mar e Abr têm 3 (inclui %conv do canal).

| Mês | Col data | Col integrado (cartões) | Col % share/dia | Col %conv canal |
|-----|----------|-------------------------|-----------------|-----------------|
| Jan | 1 | 9 | 10 | — |
| Fev | 12 | 18 | 19 | — |
| Mar | 21 | 28 | 29 | 30 |
| Abr | 32 | 39 | 40 | 41 |
| Mai–Dez | — | sem dados ainda | — | — |

> Mai–Dez não têm colunas Serasa preenchidas ainda. Ignorar silenciosamente e informar no resumo.

### Células a ignorar

- `#DIV/0!` → sem dados
- Células vazias
- Linhas sem nenhum dado numérico relevante

---

## PARSER COMPLETO (Python)

```python
import re, csv, io, os, datetime

# Posições tipo 'total'
TOTAL_POSITIONS = {
    'Janeiro':   {'date': 1,  'prop': 3,  'cart': 4,  'conv': 5,  'obs': 6},
    'Fevereiro': {'date': 12, 'prop': 14, 'cart': 15, 'conv': 16, 'obs': 17},
    'Março':     {'date': 21, 'prop': 23, 'cart': 24, 'conv': 25, 'obs': 26},
    'Abril':     {'date': 32, 'prop': 34, 'cart': 35, 'conv': 36, 'obs': 37},
    'Maio':      {'date': 43, 'prop': 45, 'cart': 46, 'conv': 47, 'obs': 48},
    'Junho':     {'date': 50, 'prop': 52, 'cart': 53, 'conv': 54, 'obs': 55},
    'Julho':     {'date': 57, 'prop': 59, 'cart': 60, 'conv': 61, 'obs': 62},
    'Agosto':    {'date': 64, 'prop': 66, 'cart': 67, 'conv': 68, 'obs': 69},
    'Setembro':  {'date': 71, 'prop': 73, 'cart': 74, 'conv': 75, 'obs': 76},
    'Outubro':   {'date': 78, 'prop': 80, 'cart': 81, 'conv': 82, 'obs': 83},
    'Novembro':  {'date': 85, 'prop': 87, 'cart': 88, 'conv': 89, 'obs': 90},
    'Dezembro':  {'date': 92, 'prop': 94, 'cart': 95, 'conv': 96, 'obs': 97},
}

# Posições tipo 'serasa_api' — apenas meses com dados disponíveis
SERASA_POSITIONS = {
    'Janeiro':   {'date': 1,  'cart': 9,  'share': 10, 'conv_canal': None},
    'Fevereiro': {'date': 12, 'cart': 18, 'share': 19, 'conv_canal': None},
    'Março':     {'date': 21, 'cart': 28, 'share': 29, 'conv_canal': 30},
    'Abril':     {'date': 32, 'cart': 39, 'share': 40, 'conv_canal': 41},
}

MONTH_ABBR = {
    'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06',
    'jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'
}

LAYOUT_CHECKPOINTS = {
    1:  'Janeiro',    12: 'Fevereiro',
    21: 'Março',      32: 'Abril',
    3:  'Propostas',  4:  'Cartões Emitidos',  5: '%Conv.',
    9:  'integrado',  10: '% integrado/dia',
    18: 'integrado',  19: '% integrado/dia',
    28: 'integrado',  29: '% integrado/dia',
    39: 'integrado',  40: '% integrado/dia',
}

def parse_br_number(val):
    val = str(val).strip()
    if not val or val in ['#DIV/0!', '-', '', 'None']:
        return None
    val = val.replace('.', '').replace(',', '.').replace('%', '')
    try:
        return float(val)
    except:
        return None

def parse_date_cell(val, year):
    m = re.match(r'(\d+)[-/](\w+)', str(val).strip())
    if m:
        mon_num = MONTH_ABBR.get(m.group(2).lower()[:3])
        if mon_num:
            return f"{year}-{mon_num}-{int(m.group(1)):02d}"
    return None

def get_cell(row, idx):
    return row[idx].strip() if idx < len(row) else ''

def detect_year(filepath):
    match = re.search(r'20(\d{2})', os.path.basename(filepath))
    return int('20' + match.group(1)) if match else datetime.datetime.now().year

def load_rows(filepath):
    with open(filepath, 'rb') as f:
        content = f.read().decode('latin-1')
    return list(csv.reader(io.StringIO(content), delimiter=';', quotechar='"'))

def validate_layout(header_cols):
    issues = []
    for idx, expected in LAYOUT_CHECKPOINTS.items():
        actual = header_cols[idx].strip() if idx < len(header_cols) else 'MISSING'
        if actual != expected:
            issues.append(f"Col {idx}: esperado '{expected}', encontrado '{actual}'")
    return issues

def extract_records(filepath):
    """
    Retorna lista de registros para upsert.
    Cada data pode gerar até 2 registros: tipo='total' e tipo='serasa_api'.
    """
    year = detect_year(filepath)
    rows = load_rows(filepath)
    header_cols = rows[72]

    issues = validate_layout(header_cols)
    if issues:
        raise ValueError("Layout mudou — interrompendo:\n" + "\n".join(issues))

    records = []

    for row in rows[73:]:

        # --- tipo 'total' ---
        for month, pos in TOTAL_POSITIONS.items():
            date_str = get_cell(row, pos['date'])
            if not date_str:
                continue
            parsed_date = parse_date_cell(date_str, year)
            if not parsed_date:
                continue
            prop = parse_br_number(get_cell(row, pos['prop']))
            cart = parse_br_number(get_cell(row, pos['cart']))
            conv = parse_br_number(get_cell(row, pos['conv']))
            obs  = get_cell(row, pos['obs'])
            if prop is None and cart is None:
                continue
            records.append({
                'data':                 parsed_date,
                'tipo':                 'total',
                'propostas_total':      int(prop) if prop is not None else None,
                'emissoes_total':       int(cart) if cart is not None else None,
                'percentual_conversao': round(conv, 2) if conv is not None else None,
                'percentual_share':     None,
                'pct_conv_canal':       None,
                'observacoes':          ' '.join(obs.replace('\n', ' ').split()) or None,
            })

        # --- tipo 'serasa_api' ---
        for month, pos in SERASA_POSITIONS.items():
            date_str = get_cell(row, pos['date'])
            if not date_str:
                continue
            parsed_date = parse_date_cell(date_str, year)
            if not parsed_date:
                continue
            cart  = parse_br_number(get_cell(row, pos['cart']))
            share = parse_br_number(get_cell(row, pos['share']))
            conv_canal = parse_br_number(get_cell(row, pos['conv_canal'])) \
                         if pos['conv_canal'] else None
            if cart is None:
                continue
            records.append({
                'data':                 parsed_date,
                'tipo':                 'serasa_api',
                'propostas_total':      None,
                'emissoes_total':       int(cart),
                'percentual_conversao': None,
                'percentual_share':     round(share, 2) if share is not None else None,
                'pct_conv_canal':       round(conv_canal, 2) if conv_canal is not None else None,
                'observacoes':          None,
            })

    return records
```

---

## VALIDAÇÃO

```python
def validate_records(records):
    errors, warnings = [], []
    seen = set()
    for r in records:
        key = (r['data'], r['tipo'])
        if key in seen:
            errors.append(f"Duplicata no arquivo: {r['data']} / {r['tipo']}")
        seen.add(key)
        if r['emissoes_total'] and r['emissoes_total'] < 0:
            errors.append(f"{r['data']} ({r['tipo']}): emissões negativas")
        if r['tipo'] == 'total' and r['propostas_total'] and r['emissoes_total']:
            if r['emissoes_total'] > r['propostas_total']:
                warnings.append(f"{r['data']}: cartões ({r['emissoes_total']}) > propostas ({r['propostas_total']})")
    return errors, warnings
# Se errors → mostrar tudo e NÃO executar upsert
```

---

## UPSERT NO SUPABASE

```sql
INSERT INTO b2c_daily_metrics
  (data, tipo, propostas_total, emissoes_total,
   percentual_conversao, percentual_share, pct_conv_canal, observacoes, updated_at)
VALUES
  {values}
ON CONFLICT (data, tipo) DO UPDATE SET
  propostas_total       = EXCLUDED.propostas_total,
  emissoes_total        = EXCLUDED.emissoes_total,
  percentual_conversao  = EXCLUDED.percentual_conversao,
  percentual_share      = EXCLUDED.percentual_share,
  pct_conv_canal        = EXCLUDED.pct_conv_canal,
  observacoes           = EXCLUDED.observacoes,
  updated_at            = NOW();
```

Batches de 50 registros.

---

## SAÍDA PARA O USUÁRIO

```
✅ B2C Originação atualizada com sucesso

📊 Processamento:
  • Arquivo: Orçamento_B2C_2026.xlsx
  • Registros extraídos: 207 (103 total + 89 serasa_api + 15 sem Serasa)
  • Meses com dados Total: Jan → Abr
  • Meses com dados Serasa API: Jan → Abr  |  Mai–Dez: sem colunas ainda

🔄 Upsert em b2c_daily_metrics:
  tipo='total'      → inseridos: 10 | atualizados: 93
  tipo='serasa_api' → inseridos:  8 | atualizados: 81

📈 Últimos 5 dias — Total vs Serasa:
  Data        | Total cart | Serasa cart | Share Serasa | %Conv canal
  2026-04-13  |    125     |    123      |    98,40%    |   3,90%
  2026-04-12  |    134     |    128      |    95,52%    |   5,96%
  2026-04-11  |    104     |    102      |    98,08%    |   4,79%
  2026-04-10  |    140     |    138      |    98,57%    |   4,22%
  2026-04-09  |    183     |    177      |    96,72%    |   4,61%
```

---

## TRATAMENTO DE ERROS

| Situação | Ação |
|----------|------|
| Layout mudou (col deslocada) | Parar, reportar posições conflitantes |
| Erros de validação | Mostrar tudo, não subir nada |
| Coluna `tipo` não existe (migration não aplicada) | Reportar — não executar upsert |
| Meses Mai–Dez sem Serasa | Informar no resumo, não é erro |
| Falha parcial no batch | Reportar batch exato para retry |

---

## DETECÇÃO DO ANO

1. Nome do arquivo — regex `20\d{2}` (ex: `Orçamento_B2C_20226` → 2026)
2. Ano corrente da sessão
3. Perguntar ao usuário
