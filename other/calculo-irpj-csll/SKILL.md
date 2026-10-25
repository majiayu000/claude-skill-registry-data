---
name: calculo-irpj-csll"
description: Centraliza decisões e cálculos de IRPJ e CSLL nos três regimes (Simples, Presumido, Real), com adicional de IR, JCP, equivalência patrimonial e prejuízo fiscal.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

> ⚠️ **AVISO FISCAL — CONFIRA ANTES DE GERAR A GUIA.** Todo código de receita (DARF/DAS), alíquota, base de cálculo, valor e data de vencimento gerado por este agente é **rascunho de apoio** e pode variar por ano, regime tributário, município ou caso específico. **Confira sempre na fonte oficial vigente (Receita Federal / e-CAC / legislação estadual e municipal) antes de transmitir declaração ou pagar guia.** A conferência final é responsabilidade do contador responsável.

## Quando usar

Skill consolidadora — útil quando o cliente está revisando regime tributário ou quer entender como IRPJ/CSLL se comporta. Para apuração detalhada, use 01 (Simples), 02 (Presumido) ou 03 (Real).

## Resumo dos regimes

| Tema | Simples | Presumido | Real |
|---|---|---|---|
| Periodicidade | Mensal (DAS) | Trimestral | Trim ou Anual c/ estim. |
| Base IRPJ | Receita × % do anexo | Receita × % presunção | Lucro real ajustado |
| Alíquota IRPJ | Embutida no DAS | 15% + adicional 10% | 15% + adicional 10% |
| Adicional 10% | Não aplica | Trimestral: > R$ 60k | Trimestral: > R$ 60k / Anual: > R$ 240k |
| Alíquota CSLL | Embutida no DAS | 9% s/ base presumida | 9% s/ lucro real (15-20% inst. fin.) |
| Compensação prejuízo | N/A | N/A | Sim, limite 30% |
| DCTFWeb / ECF | DCTFWeb / DEFIS | DCTFWeb / ECF | DCTFWeb / ECF + ECD |

## Inputs necessários

1. Regime tributário atual e do ano-calendário inteiro
2. Receita bruta + receitas financeiras + ganhos de capital
3. Despesas e custos (para Real)
4. Saldo de prejuízo fiscal e base negativa CSLL (para Real)
5. JCP recebidos ou pagos (deduz no Real, é receita financeira)
6. IRRF retido por terceiros (compensa com IRPJ devido)
7. Lucros distribuídos (isentos em IRPJ na PF — Lei 9.249/95 art. 10)

## Decisões frequentes

### 1. Pagar JCP em vez de dividendo (Real)

```
JCP máximo = TJLP × Patrimônio Líquido (excluídas reservas de reavaliação)
```
- Limite: maior entre 50% do lucro líquido do exercício OU 50% das reservas de lucros.
- Despesa dedutível para a PJ (15% IRPJ + 9% CSLL = 24% economia tributária no Real).
- IRRF de 15% na fonte para o sócio (definitivo para PF).
- **Compensação de JCP**: vantajoso para empresas no Real com PJ sócia (sócia tributada novamente é evitada).

### 2. Equivalência patrimonial (controlada Brasil)
- Resultado positivo = exclusão do lucro real (já tributado na controlada).
- Resultado negativo = adição (não pode reduzir o lucro real).
- IFRS no investimento: lucros ainda não realizados em equivalência são adicionados; perdas são adicionadas.

### 3. Lucros distribuídos
- PF: isenção (art. 10, Lei 9.249/95) — atenção: PL 1.087/2025 propõe tributação de 10% sobre dividendos > R$ 20k/mês a partir de 2026 (acompanhar status).
- PJ: distribuição entre PJ no Brasil também é isenta para a sócia (não tributa).

### 4. Cálculo do adicional de IR
- 10% sobre o que **exceder** R$ 20.000/mês (ou R$ 60k tri / R$ 240k ano).
- Importante: o adicional incide sobre a parcela excedente, **não** sobre o valor total.

## Templates

### Comparativo rápido entre Presumido e Real

```
RECEITA BRUTA ANUAL: R$ _________

PRESUMIDO
  Base IRPJ (% × receita): R$ _________
  IRPJ 15% + adicional: R$ _________
  CSLL 9% × base: R$ _________
  PIS 0,65% × receita: R$ _________
  COFINS 3,0% × receita: R$ _________
  Carga total: R$ _________

REAL
  LAIR estimado: R$ _________
  Lucro real ajustado: R$ _________
  IRPJ + adicional: R$ _________
  CSLL 9%: R$ _________
  PIS 1,65% × receita − créditos: R$ _________
  COFINS 7,6% × receita − créditos: R$ _________
  Carga total: R$ _________

DIFERENÇA: R$ _________ ➝ Migrar [ ] Sim  [ ] Não
```

## Erros comuns

- Calcular adicional sobre o lucro inteiro em vez do excedente.
- Não considerar a margem real da empresa na escolha entre Presumido e Real (margem baixa = Real é melhor; margem alta = Presumido).
- JCP sem TJLP atualizada ou sem ata de aprovação.
- Distribuir lucro do Real sem balanço — distribuição "presumida" só é permitida para empresas no Presumido (Lei 9.249, art. 10) com base no lucro presumido líquido do IRPJ/CSLL.
- Esquecer que adicional aparece em DCTFWeb separado do IRPJ.

## Checklist

- [ ] Regime confirmado (DEFIS/ECF do ano anterior)
- [ ] Receita conferida em ECD (Real) ou apuração (Presumido)
- [ ] JCP/dividendos com ata de aprovação
- [ ] Adicional calculado sobre o excedente
- [ ] IRRF de terceiros compensado
- [ ] Códigos DARF: IRPJ 2089 (Presumido), 2362 (Real estimativa), 2430 (Real anual ajuste); CSLL 2372/2484
- [ ] DCTFWeb e ECF/DEFIS conciliados

## Referências

- RIR/2018 (Decreto 9.580)
- Lei 9.249/1995
- Lei 9.430/1996 (apuração e adicional)
- IN RFB 1.700/2017
- Lei 9.959/2000 e 11.196/2005 (JCP)
