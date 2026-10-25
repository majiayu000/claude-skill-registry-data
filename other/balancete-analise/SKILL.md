---
name: balancete-analise"
description: Lê e analisa balancetes mensais identificando inconsistências (saldos invertidos, contas obsoletas, variações anormais) e construindo conclusões para o cliente.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Após o fechamento mensal (skill 37), antes de entregar ao cliente. Também na chegada de cliente novo (revisão dos últimos 12 meses).

## Inputs necessários

1. Balancete de verificação do mês fechado
2. Balancete dos 3 meses anteriores (para comparar)
3. DRE acumulada
4. Notas explicativas (movimentos atípicos)

## Análise estruturada (4 dimensões)

### 1. Integridade

- Soma débitos = soma créditos? (deve fechar com tolerância zero)
- Conta sintética = soma das analíticas?
- Contas com nome inadequado ("Outros", "Diversos") concentrando muito saldo?
- Contas zeradas há mais de 6 meses → candidatas a inativação

### 2. Coerência (saldos por natureza)

| Conta | Natureza esperada | Sinal de alerta |
|---|---|---|
| Caixa | Devedor (saldo positivo no D) | Crédito = caixa estourado (impossível fisicamente) |
| Bancos | Devedor | Crédito = saldo negativo / cheque especial — registrar como passivo |
| Clientes | Devedor | Crédito = adiantamentos de cliente (separar) |
| Estoques | Devedor | Crédito = baixa indevida |
| Fornecedores | Credor | Débito = adiantamento ou pagamento duplicado |
| Tributos a recolher | Credor | Débito = recuperar (passar para 1.1.4) |
| Capital social | Credor | Débito = capital a integralizar |
| Receitas (3) | Credor | Débito anormal (devolução excessiva, estorno) |
| Despesas (5) | Devedor | Crédito anormal (recuperação, reversão de provisão) |

### 3. Variações relevantes

Para cada conta:
- Variação % vs. mês anterior
- Variação absoluta R$
- Vs. orçamento (se houver)
- Sinalizar variações > 20% para investigação

Exemplos típicos:
- Despesas com pessoal +30%: contratações, dissídio, HE excessiva, rescisão.
- Receita −15%: queda de vendas, cliente perdido, sazonalidade.
- Estoque +50%: compra antecipada, encalhe, erro inventário.
- Tributos a recolher +100%: apuração não paga, parcelamento.

### 4. Indicadores

| Indicador | Fórmula | Interpretação |
|---|---|---|
| Margem bruta | (Rec líq − CMV) / Rec líq | Saúde do produto |
| Margem operacional | LO / Rec líq | Eficiência |
| Margem líquida | LL / Rec líq | Resultado final |
| EBITDA | LO + Deprec + Amort | Geração operacional |
| Liquidez corrente | AC / PC | Capacidade de honrar curto prazo (>1 ok) |
| Liquidez seca | (AC − Estoque) / PC | Sem depender de venda |
| Endividamento | Passivo / Ativo | < 60% saudável p/ PME |
| Prazo médio recebimento | Clientes × 360 / Receita | Dias para receber |
| Prazo médio pagamento | Fornecedores × 360 / Compras | Dias para pagar |
| Giro de estoque | CMV / Estoque médio | Quantas vezes vende o estoque |
| ROE | LL / PL | Retorno do capital próprio |

## Templates

### Pacote de análise para cliente

```
COMPETÊNCIA __/____ — Cliente __________

DESTAQUES DO MÊS
* Receita líquida: R$ ___ (vs ___ mês anterior, var __%)
* Margem bruta: __% (vs __%)
* Lucro operacional: R$ ___ (margem __%)
* Lucro líquido: R$ ___
* Caixa em mãos: R$ ___ + Aplicações R$ ___

PRINCIPAIS VARIAÇÕES
1. _____________ +__% — motivo: __________
2. _____________ -__% — motivo: __________
3. _____________ +__% — motivo: __________

INDICADORES
Liquidez corrente: __ (saudável > 1)
Endividamento: __% (saudável < 60%)
PMR (recebimento): __ dias
PMP (pagamento): __ dias
Giro de estoque: __ vezes/ano
ROE acumulado: __%

PONTOS DE ATENÇÃO
[ ] _____________
[ ] _____________
[ ] _____________

RECOMENDAÇÕES
1. _____________
2. _____________
```

## Erros comuns

- Apenas entregar PDF sem leitura — cliente não enxerga o que importa.
- Concentrar conta "Outras despesas" — perde rastreabilidade.
- Não reverter saldo invertido (cheque especial em conta de banco como devedor).
- Saldo de tributos a recuperar virando "ativo morto" — sem aproveitamento.
- Variar 50% e não comentar com o cliente.
- Indicadores sem benchmark do setor — número solto não diz nada.

## Checklist

- [ ] Soma D = soma C
- [ ] Saldos por natureza coerentes
- [ ] Contas inativas identificadas para inativação
- [ ] Variações > 20% explicadas
- [ ] Indicadores calculados
- [ ] Pacote de análise pronto
- [ ] Comentários personalizados ao cliente

## Referências

- CPC 26 (apresentação)
- NBC TG 1.000 (PME)
- ITG 2000
- Análise das Demonstrações Contábeis — referenciais de mercado (Iudícibus, Marion, Matarazzo)
