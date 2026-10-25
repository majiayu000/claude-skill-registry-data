---
name: valuation-pme"
description: Calcula valuation de PME por DCF, múltiplos comparáveis e patrimonial, ajusta o EBITDA com one-offs, projeta FCFF/FCFE e estrutura faixa de preço para venda ou aporte.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Sócio querendo vender, captar com investidor, sucessão, pré-IPO, partilha em divórcio, valuation para combinação de negócios (CPC 15). Trabalho técnico com 2-6 semanas.

## Inputs necessários

1. DREs e balanços últimos 3-5 anos
2. Plano de negócios / projeção de receita 5-10 anos
3. CAPEX histórico e projetado
4. Estrutura de capital (dívida, custo)
5. WACC do setor
6. Múltiplos comparáveis (transações privadas, empresas listadas)
7. Especificidades do negócio (clientes únicos, concorrência, regulação)

## 3 abordagens (combinadas)

### 1. DCF — Fluxo de Caixa Descontado

**Estrutura FCFF (livre para a firma)**:
```
EBITDA
(−) D&A (depreciação e amortização)
= EBIT
(−) IR/CSLL sobre EBIT
= NOPAT
(+) D&A
(−) CAPEX
(−) ΔCapital de giro
= FCFF
```

**Estrutura FCFE (livre ao acionista)**:
```
FCFF
+/- Variação da dívida líquida
- Juros líquidos de IR
= FCFE
```

**Desconto pelo WACC**:
```
WACC = (E/V) × Ke + (D/V) × Kd × (1 − T)
```
- Ke (custo do equity): CAPM ajustado: Rf + β × (Rm − Rf) + prêmio de país + prêmio de tamanho
- Kd (custo da dívida): taxa contratada × (1 − IR)
- E/V e D/V: estrutura ótima de capital

**Valor terminal**:
- Modelo Gordon: TV = FCFF_n × (1+g) / (WACC − g), com g de longo prazo (~3-5% no Brasil).
- Ou Múltiplo de saída: TV = EBITDA_n × M.

**Equity value**:
```
Enterprise Value = Σ FCFF_t / (1+WACC)^t + TV / (1+WACC)^n
Equity Value = EV − Dívida líquida
Preço por cota = Equity Value / quantidade de cotas
```

### 2. Múltiplos comparáveis

Identificar transações similares e usar média/mediana:

| Múltiplo | Aplicação |
|---|---|
| EV/EBITDA | Comparação de operação |
| EV/Receita | Negócios com prejuízo / margens em estabilização (SaaS, scale-ups) |
| P/E (PL) | Empresas listadas estáveis |
| EV/Cliente | Telco, SaaS |
| EV/Loja | Varejo |

**Fontes**:
- Transações privadas: research de M&A boutique
- Listadas: B3, fontes (ABMI&A, Capital IQ, terminais Bloomberg)
- Brasil PME 2025-2026: EV/EBITDA típico 4x–8x dependendo do setor

### 3. Patrimonial (livro / valor justo dos ativos)

Aplicável a:
- Holdings de ativos (imobiliária, holding patrimonial)
- Empresa em descontinuidade (liquidação)
- Piso de valor (não pode ser inferior ao patrimônio líquido contábil/avaliado)

```
Valor patrimonial = Ativo a valor justo − Passivo a valor justo
```

## EBITDA ajustado (Quality of Earnings)

```
EBITDA contábil
+ One-offs não recorrentes (multas, indenizações, custos M&A)
- Receitas não recorrentes (venda de ativo, ganho cambial)
+ Diferença de pró-labore vs. mercado (sócio que paga pouco a si mesmo)
+ Despesas pessoais lançadas na empresa (carro do sócio etc.)
± Operações com partes relacionadas a preços de mercado
= EBITDA AJUSTADO
```

## Capital de giro (NWC)

```
NWC = Clientes + Estoque − Fornecedores
ΔNWC = NWC_t − NWC_t-1
```

Crescimento de receita demanda mais capital de giro → reduz FCFF.

## Templates

### Modelo DCF (5 anos + perpetuidade)

```
                     Ano 1    Ano 2    Ano 3    Ano 4    Ano 5    TV
Receita líquida      ____     ____     ____     ____     ____     —
Crescimento %        ___%     ___%     ___%     ___%     ___%     ___%
EBITDA               ____     ____     ____     ____     ____     —
Margem %             ___%     ___%     ___%     ___%     ___%     —
D&A                  ____     ____     ____     ____     ____
EBIT                 ____     ____     ____     ____     ____
IR/CSLL (___%)       ____     ____     ____     ____     ____
NOPAT                ____     ____     ____     ____     ____
+ D&A                ____     ____     ____     ____     ____
- CAPEX              ____     ____     ____     ____     ____
- ΔNWC               ____     ____     ____     ____     ____
FCFF                 ____     ____     ____     ____     ____     ___ (TV)

WACC: ___%   g: ___%   Período: ___ anos
PV(FCFF) Ano 1: ____ ... Ano 5: ____
PV(TV): ____
EV = ____
Dívida líquida: ____
Equity Value: ____
```

### Sensibilidade

```
                   WACC 10%   12%    14%    16%
g 3%               EV ___     ___    ___    ___
g 4%               EV ___     ___    ___    ___
g 5%               EV ___     ___    ___    ___
```

### Faixa de valor

```
Abordagem            Mínimo    Médio     Máximo
DCF                   R$ X      R$ Y      R$ Z
Múltiplos EBITDA      R$ X      R$ Y      R$ Z
Patrimonial          R$ X      R$ Y      R$ Z

FAIXA RECOMENDADA: R$ ___ a R$ ___
PREÇO ALVO PARA NEGOCIAÇÃO: R$ ___
ANCORAGEM (mínimo aceitável): R$ ___
```

## Erros comuns

- Usar EBITDA não ajustado (one-offs distorcem).
- WACC genérico sem ajustar para tamanho/risco da PME (usar Damodaran + prêmio Brasil + prêmio tamanho).
- g de perpetuidade > WACC ou > crescimento da economia → modelo explode.
- Projeção otimista demais em receita sem fundamento.
- Múltiplos de empresas listadas aplicados a PME sem desconto de iliquidez (DLOM 20-30%).
- Não considerar capital de giro adicional para suportar crescimento.
- Esquecer dívida fora do balanço (avais, garantias, leasing operacional pré-IFRS 16).

## Checklist

- [ ] EBITDA ajustado documentado item a item
- [ ] Projeção 5+ anos consistente com plano de negócios
- [ ] WACC fundamentado (Rf, β, prêmio mercado, prêmio Brasil, prêmio tamanho)
- [ ] g razoável (≤ inflação + crescimento real do PIB)
- [ ] Múltiplos comparáveis com fontes
- [ ] Sensibilidade WACC × g
- [ ] Patrimonial como piso
- [ ] Faixa final defensável
- [ ] Relatório assinado pelo contador (CRC)

## Referências

- CPC 15 (combinação de negócios)
- CPC 1 (impairment — usa cálculos similares)
- CFC NBC TG 04 (Avaliação por valor justo)
- Damodaran (cost of equity, country risk premium)
- Iudícibus, Marion (referencial brasileiro)
- Resolução CFC NBC PA 11 (Auditoria — alguns valuations precisam de auditor)
