---
name: efd-icms-ipi"
description: Gera, valida e transmite a EFD ICMS/IPI mensal — escrituração de NFs de entrada/saída, apuração de ICMS próprio, ICMS-ST, IPI e DIFAL — com cruzamento de C100/C170/E110.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Empresas do Lucro Real e Presumido (e Simples acima do sublimite estadual). Apuração mensal, transmissão até o **dia 25 do mês subsequente** (regra geral, alguns estados têm calendário próprio — RS, RJ, ES).

## Inputs necessários

1. NFs de entrada e saída do mês (XML)
2. Conhecimentos de transporte (CT-e) recebidos e emitidos
3. Inventário (Bloco H) — entrega anual, no SPED de fevereiro
4. Apurações de ICMS próprio, ICMS-ST e IPI
5. Saldo credor anterior e benefícios fiscais aplicáveis
6. Cadastro completo de produtos com NCM, unidade, código

## Estrutura de blocos

| Bloco | Conteúdo |
|---|---|
| 0 | Abertura, identificação, cadastros (0150 participantes, 0200 itens, 0300 ativo imob) |
| B | ISS — opcional, alguns estados |
| C | Documentos fiscais — mercadorias (NF-e, NFC-e, NF, CT-e antigo) |
| D | Documentos fiscais — serviços de transporte (CT-e, NF de serviço comunicação) |
| E | Apuração ICMS, IPI, ICMS-ST, ICMS-DIFAL, FECOEP |
| G | Controle de Crédito do ICMS do Ativo Permanente (CIAP) |
| H | Inventário (anual) |
| K | Controle da Produção e do Estoque (Livro K) — indústria/atacadista |
| 1 | Outras informações (1200 controle créditos extemporâneos, 1300 combustíveis, 1400 declarações por município) |
| 9 | Encerramento |

## Passo a passo

### 1. Cadastros (Bloco 0)
- 0000: identificação do estabelecimento, perfil (A com escrituração analítica, B sintética, C analítica reduzida).
- 0150: participantes (clientes, fornecedores) — somente os movimentados no mês.
- 0200: itens movimentados (NCM atualizada — TIPI vigente).

### 2. Documentos fiscais (Bloco C)
- C100: cabeçalho da NF (data, valor, CFOP, modelo).
- C170: itens (mercadoria, NCM, CFOP, CST ICMS/IPI, valor, ICMS, IPI, PIS/COFINS).
- C190: registros analíticos (consolidação por CST + CFOP + alíquota — base do E110/E116).

Atenção:
- Lançar **NF cancelada** (C100 com situação 2 — cancelada) — não escriturar valores.
- NF denegada/inutilizada: registrar conforme situação (3, 4, 5).
- Devoluções: CFOPs 1.201/2.201, 5.201/6.201; com créditos espelho.

### 3. Bloco E — apuração

| Registro | Conteúdo |
|---|---|
| E110 | Apuração ICMS próprio (débitos, créditos, saldo) |
| E111 | Ajustes da apuração (débito/crédito por motivo) |
| E116 | Obrigações de ICMS — guia(s) a recolher |
| E200 | Apuração ICMS-ST (UF a UF) |
| E210 | Detalhamento ICMS-ST por UF |
| E520 | Apuração IPI |
| E530 | Ajustes IPI |

### 4. CIAP (Bloco G)
- Aquisição de imobilizado para a atividade gera crédito de ICMS em **48 parcelas**.
- G110 controle do ativo, G125 lançamentos mensais por bem.

### 5. Inventário (Bloco H — anual)
- Levantamento físico em 31/12. Entrega na EFD de **fevereiro** do ano seguinte.
- Cada item com NCM, unidade, quantidade, valor unitário, valor total.

### 6. Bloco K (Livro de Produção)
Obrigatório para indústrias e atacadistas com receita > limites estaduais:
- K200 estoque escriturado, K220 outras movimentações, K230 itens produzidos, K235 insumos consumidos, K250 produção de terceiros.
- Bloqueio frequente: produto sem ficha técnica, consumo desproporcional.

### 7. Validação e transmissão
- PVA EFD ICMS/IPI: validar (zero erro de bloqueio).
- Assinar com e-CNPJ.
- Transmitir via Receitanet.
- Recibo + protocolo arquivados 5 anos.

## Templates

### C170 (item de NF de saída)

```
|C170|001|PROD0001|Produto X|10,00|UN|1500,00|0,00|0|5102|...|
```

### Conferência de E110

```
DÉBITOS:
  Débitos por NFs saída......... R$ _________
  Débitos por outros (E111)...... R$ _________
CRÉDITOS:
  Créditos por NFs entrada...... R$ _________
  Créditos por estorno/outros... R$ _________
SALDO ANTERIOR................. R$ _________
SALDO APURADO.................. R$ _________
RECOLHIDO (E116)............... R$ _________
```

## Erros comuns

- CFOP incompatível com a operação (ex.: 5.949 para venda interna — usar 5.102/5.405).
- CST ICMS errado para Simples Nacional (CST 020/CSOSN apenas em emitente Simples).
- Bloco K com K235 sem ficha técnica → autuação.
- NF de aquisição de imobilizado sem CIAP — perde o crédito ICMS.
- Não escriturar CT-e (frete) — perde crédito.
- Inventário (Bloco H) não entregue em fevereiro — multa.
- DIFAL Convênio 93/2015 escriturado errado pós-LC 190/2022.

## Checklist

- [ ] Todos os XMLs do mês importados e conciliados (DANFEs vs EFD)
- [ ] CFOPs e CSTs revisados
- [ ] CIAP atualizado (48 parcelas)
- [ ] Ajustes E111 com código de ajuste correto (Tabela 5.1.1 Ajustes)
- [ ] DIFAL escriturado em E300 (quando aplicável)
- [ ] PVA com 0 erros
- [ ] Saldo apurado bate com sistema fiscal interno
- [ ] Recibo arquivado

## Referências

- Convênio ICMS s/n 1970 (escrituração)
- Convênio ICMS 143/2006 + Ajuste SINIEF 2/2009 (EFD)
- Guia Prático EFD ICMS/IPI vigente (gov.br/sped)
- IN RFB 1.371/2013 (procedimentos federais EFD)
- Tabela 5.1.1 Códigos de Ajuste por UF
