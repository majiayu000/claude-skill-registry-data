---
name: plano-contas-cpc"
description: Estrutura plano de contas alinhado aos CPCs (1, 16, 27, 47, 48), com referencial fiscal da ECF/ECD e níveis 5/7 dígitos para integração com SPED.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Implantação de novo cliente, abertura de empresa, migração de ERP, ou ajuste do plano para atender ECD/ECF e demonstrações IFRS (CPC). Plano consistente reduz erros de classificação, malha fina e retrabalho de fechamento.

## Princípios de estruturação

1. **Hierarquia clara**: 4-7 níveis com totalizadores (sintéticas) e analíticas com saldo.
2. **Padrão SPED**: cada conta analítica vinculada a conta referencial (Anexo III IN RFB 2.003 — ECD).
3. **Aderência aos CPCs**: separar imobilizado tangível (CPC 27), intangível (CPC 4), instrumentos financeiros (CPC 48), receita (CPC 47), arrendamento (CPC 6/IFRS 16).
4. **DRE estruturada**: receita bruta → deduções (impostos sobre venda, devoluções) → receita líquida → custos → lucro bruto → despesas operacionais → resultado financeiro → resultado antes IR → IRPJ/CSLL → resultado líquido.

## Estrutura sugerida (5 dígitos)

```
1 ATIVO
1.1 ATIVO CIRCULANTE
1.1.1 Disponibilidades
1.1.1.01 Caixa
1.1.1.01.01 Caixa Geral
1.1.1.02 Bancos conta movimento
1.1.1.02.01 Banco do Brasil — c/c 1234-5
1.1.1.03 Aplicações financeiras
1.1.2 Clientes
1.1.2.01 Clientes nacionais
1.1.2.02 (-) Provisão para perdas em créditos (PCLD)
1.1.3 Estoques
1.1.3.01 Mercadorias para revenda
1.1.3.02 Matérias-primas
1.1.3.03 Produtos acabados
1.1.4 Tributos a recuperar
1.1.4.01 ICMS a recuperar
1.1.4.02 PIS/COFINS a recuperar
1.1.4.03 IRPJ/CSLL antecipações
1.1.5 Adiantamentos e despesas antecipadas

1.2 ATIVO NÃO-CIRCULANTE
1.2.1 Realizável a longo prazo
1.2.2 Investimentos (CPC 18 — equivalência patrimonial)
1.2.3 Imobilizado (CPC 27)
1.2.3.01 Terrenos
1.2.3.02 Edificações
1.2.3.03 Máquinas e equipamentos
1.2.3.04 Veículos
1.2.3.05 Móveis e utensílios
1.2.3.06 Software (instalado em ativo) / direitos de uso
1.2.3.99 (-) Depreciação acumulada
1.2.4 Intangível (CPC 4)
1.2.4.01 Marcas e patentes
1.2.4.02 Software adquirido
1.2.4.99 (-) Amortização acumulada
1.2.5 Direitos de uso — leasing IFRS 16 / CPC 6 (R2)

2 PASSIVO
2.1 PASSIVO CIRCULANTE
2.1.1 Fornecedores
2.1.2 Empréstimos e financiamentos curto prazo
2.1.3 Obrigações trabalhistas
2.1.3.01 Salários a pagar
2.1.3.02 INSS a recolher
2.1.3.03 IRRF folha
2.1.3.04 FGTS
2.1.3.05 Provisão de férias + 1/3 e encargos
2.1.3.06 Provisão de 13º + encargos
2.1.4 Obrigações tributárias
2.1.4.01 ICMS a recolher
2.1.4.02 ISS a recolher
2.1.4.03 PIS/COFINS
2.1.4.04 IRPJ/CSLL
2.1.5 Outras obrigações

2.2 PASSIVO NÃO-CIRCULANTE
2.2.1 Empréstimos e financiamentos longo prazo
2.2.2 Tributos parcelados RFB/PGFN
2.2.3 Provisões fiscais e trabalhistas (CPC 25)
2.2.4 Passivo de leasing (IFRS 16)

2.3 PATRIMÔNIO LÍQUIDO
2.3.1 Capital social
2.3.2 Reservas de capital
2.3.3 Reservas de lucros (legal, estatutária, retenção)
2.3.4 Lucros/prejuízos acumulados
2.3.5 Ajustes de avaliação patrimonial (CPC 13)

3 RECEITAS
3.1 Receita bruta
3.1.1 Vendas mercadorias
3.1.2 Receita serviços
3.2 Deduções da receita bruta
3.2.1 Impostos sobre venda (ICMS, ISS, PIS, COFINS, IPI)
3.2.2 Devoluções e abatimentos
3.3 Outras receitas operacionais
3.4 Receita financeira

4 CUSTOS
4.1 CMV / CPV / CSP
4.1.1 Mercadorias / matéria-prima
4.1.2 Mão de obra direta
4.1.3 Custos indiretos / gastos gerais

5 DESPESAS
5.1 Despesas com pessoal
5.2 Despesas administrativas
5.3 Despesas comerciais
5.4 Despesas financeiras
5.5 Outras despesas operacionais
5.6 Despesa de IR/CSLL

6 RESULTADO (zera no fechamento)
```

## Mapeamento referencial

Cada conta analítica precisa ter código do plano referencial fiscal (ECD/ECF). Exemplo:

| Conta empresa | Conta referencial |
|---|---|
| 1.1.1.02.01 BB c/c | 1.01.01.01.01.01 |
| 1.1.2.01 Clientes | 1.01.02.01.01.01 |
| 3.1.1 Vendas mercadorias | 3.01.01.01.01.01 |

## Templates

### Tabela do Bloco 0 da ECD (registros I050)

```
|I050|01-01-2026|01|S|1|1|||1 ATIVO|
|I050|01-01-2026|01|S|2|1.1|1|1|1 ATIVO CIRCULANTE|
|I050|01-01-2026|01|A|5|1.1.1.02.01|1.1.1.02|1|Banco do Brasil c/c 1234-5|
```

## Erros comuns

- Conta de despesa "Outros" virando entulho — toda despesa deve ter natureza específica.
- Imobilizado com depreciação acumulada na mesma conta do ativo (correto: subconta redutora 1.2.3.99).
- Tributos a recolher misturados com a recuperar.
- Falta de provisão de férias e 13º na competência (regime de competência).
- Receita financeira contabilizada em receita operacional → distorce DRE.
- Conta sem código referencial → ECD/ECF não validam.
- Conta criada para um único lançamento (planos inflados, difícil de auditar).

## Checklist

- [ ] 1 conta para cada natureza relevante, sem genéricos
- [ ] Sintéticas e analíticas distinguidas
- [ ] Plano referencial 100% mapeado
- [ ] Reflete os CPCs aplicáveis ao porte
- [ ] DRE estruturada CPC 26
- [ ] Balanço estruturado CPC 26 (CC, PNC, PL)
- [ ] Separação clara entre operacional e financeiro
- [ ] Documentado para o ERP (parametrização)

## Referências

- CPC 26 (apresentação demonstrações)
- CPC 27 (Ativo Imobilizado)
- CPC 4 (Intangível)
- CPC 6 (R2) / IFRS 16 (Arrendamento)
- CPC 47 (Receita)
- CPC 48 (Instrumentos Financeiros)
- IN RFB 2.003/2021 (ECD) — Anexo III referencial
