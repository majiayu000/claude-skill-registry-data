---
name: dre-gerencial"
description: Monta DRE gerencial (interno, por centro de custo, por produto/cliente) com margem de contribuição, ponto de equilíbrio e comparativos vs. orçamento e período anterior.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Cliente que quer gestão financeira ativa — não só fiscal. Com DRE gerencial é possível tomar decisões de preço, mix de produto, corte de despesa, fechamento de loja, etc.

## Inputs necessários

1. DRE contábil (do balancete)
2. Plano de centros de custo (CC)
3. Plano de produtos / unidades de negócio
4. Custos variáveis vs. fixos (classificação por conta)
5. Orçamento aprovado (para comparativo)
6. Volume vendido por produto (unidades)

## Estrutura DRE gerencial

```
RECEITA BRUTA
(−) Devoluções e abatimentos
(−) Impostos sobre venda (ICMS, PIS, COFINS, ISS, IPI)
= RECEITA LÍQUIDA

(−) CUSTOS VARIÁVEIS
   Custo de mercadoria / produto
   Comissão sobre venda
   Frete sobre venda
   Tarifa de cartão
= MARGEM DE CONTRIBUIÇÃO (R$ e %)

(−) CUSTOS FIXOS / DESPESAS FIXAS
   Pessoal indireto
   Aluguel
   Energia / utilidades
   Marketing
   Despesas administrativas
   Depreciação (não-caixa)
= EBITDA (se isolar dep/amort)
(−) Depreciação e amortização
= EBIT (LUCRO OPERACIONAL)

(±) RESULTADO FINANCEIRO
   Receitas financeiras
   Despesas financeiras
= LAIR

(−) IRPJ + CSLL
= LUCRO LÍQUIDO
```

## Margem de contribuição (MC)

```
MC = Receita − Custos Variáveis
MC % = MC / Receita
```

A MC mostra quanto sobra de cada real vendido para pagar custos fixos e gerar lucro.

### Por produto

```
Produto A: Preço R$ 100 − CV R$ 60 = MC R$ 40 (40%)
Produto B: Preço R$ 200 − CV R$ 160 = MC R$ 40 (20%)
```

Mesma MC absoluta, MC% diferente — vender mais de A é mais eficiente em termos de margem.

## Ponto de equilíbrio

```
PE (em R$) = Custos Fixos / MC %
PE (em unidades) = Custos Fixos / MC unitária
```

**Exemplo**: Custos fixos R$ 100.000/mês, MC% médio 40%:
- PE em R$ = 100.000 / 0,4 = **R$ 250.000** de receita.
- Empresa precisa faturar R$ 250.000 para empatar.

### Variantes
- **PE econômico**: incluindo custo de oportunidade do capital (lucro mínimo desejado).
- **PE financeiro**: excluindo despesas não-caixa (depreciação, amortização).

## Centro de custo

Cada despesa rateada/alocada por CC:
- **Diretos**: alocação 1:1 (salário do operador da máquina X → CC máquina X)
- **Indiretos**: rateio por critério (m², horas-máquina, número de funcionários)

## Comparativos

| Coluna | Conteúdo |
|---|---|
| Realizado | Mês fechado |
| Orçado | Plano |
| Variação | (Real − Orçado) e % |
| Acumulado ano | Soma jan a mês |
| Mesmo mês ano anterior | Comparar sazonalidade |
| Variação YoY | Var contra ano anterior |

## Templates

### DRE gerencial mensal

```
                            REAL %REC    ORÇ %REC   VAR R$  VAR %
Receita bruta              ____  100,0  ____ 100,0  _____   ___
(−) Deduções               (___) (___)  (___)(___)  _____   ___
Receita líquida            ____  100,0  ____ 100,0  _____   ___
(−) Custo variável total   (___) (___)  (___)(___)  _____   ___
   CMV/CPV                 (___)        (___)
   Comissão                (___)        (___)
   Tarifa cartão           (___)        (___)
   Frete                   (___)        (___)
MARGEM CONTRIBUIÇÃO        ____   __%   ____  __%   _____   ___

(−) Custo fixo / Despesa fixa
   Pessoal indireto        (___)        (___)
   Aluguel                 (___)        (___)
   Energia                 (___)        (___)
   Marketing               (___)        (___)
   Adm                     (___)        (___)
EBITDA                     ____   __%   ____  __%   _____   ___
(−) Depreciação            (___)        (___)
EBIT                       ____   __%   ____  __%   _____   ___
(±) Resultado financeiro   ____         ____
LAIR                       ____   __%   ____  __%   _____   ___
(−) IRPJ + CSLL            (___)        (___)
LUCRO LÍQUIDO              ____   __%   ____  __%   _____   ___

PONTO DE EQUILÍBRIO MENSAL: R$ ____ (CF / MC%)
RECEITA NECESSÁRIA P/ LUCRO ALVO R$ X: (CF + Lucro) / MC%
```

## Erros comuns

- Custo variável que na verdade é fixo (aluguel da loja não vira variável só porque é "operacional").
- Comissão sobre venda lançada em despesa de marketing — distorce MC.
- DRE gerencial sem amarração com a contábil (≠ saldo) → cliente desconfia.
- Não ratear despesas indiretas → CC fica com lucro irreal.
- Ponto de equilíbrio em unidades sem usar MC unitária do mix médio.
- Comparativos sem mesma base (ex.: real com IPI / orçado sem IPI).

## Checklist

- [ ] Soma da DRE gerencial = DRE contábil
- [ ] Custos classificados (variável × fixo)
- [ ] Margem de contribuição por produto/UN
- [ ] Ponto de equilíbrio calculado
- [ ] Comparativos: real, orçado, ano anterior
- [ ] Centro de custo com rateios documentados
- [ ] Variações > 10% comentadas
- [ ] Apresentação ao cliente

## Referências

- CPC 26 (apresentação contábil)
- Boa prática gerencial — bibliografia (Padoveze, Atkinson, Anthony)
- Resolução CFC 1.121/2008 (estrutura conceitual)
