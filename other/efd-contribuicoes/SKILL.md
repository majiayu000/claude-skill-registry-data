---
name: efd-contribuicoes"
description: Gera EFD-Contribuições mensal (PIS, COFINS, CPRB), escriturando débitos e créditos por CST, segregando regime cumulativo/não-cumulativo e aplicando exclusão do ICMS (Tema 69).
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

PJ tributada por Lucro Real (não-cumulativo), Presumido (cumulativo), e empresas que recolhem CPRB. Apuração mensal, transmissão até o **dia 10 do segundo mês subsequente** ao período (ex.: janeiro entrega até 10 de março).

## Inputs necessários

1. NFs de entrada e saída do mês (XMLs)
2. Apuração de PIS e COFINS (skills 08 e 09)
3. CSTs PIS/COFINS por item (Tabela 4.3.3)
4. CFOPs e participantes
5. Receitas financeiras (apenas para apuração PIS/COFINS no não-cumulativo, conforme Decreto 8.426/2015)
6. Ajustes da apuração (estornos, créditos extemporâneos)
7. Receita por estabelecimento e por código de atividade

## Estrutura de blocos

| Bloco | Conteúdo |
|---|---|
| 0 | Abertura, identificação, cadastros (0140 estabelecimentos, 0150 participantes, 0200 itens, 0500 contas contábeis) |
| A | Documentos fiscais — serviços (NFS-e, conhecimentos, etc.) |
| C | Documentos fiscais — mercadorias |
| D | Documentos fiscais — serviços de transporte/comunicação |
| F | Demais documentos e operações (F100 outras receitas, F200 incorporação imobiliária, F500 receita por regime caixa) |
| I | Operações das financeiras |
| M | Apuração da contribuição (M100 créditos PIS, M200 PIS devido, M500 créditos COFINS, M600 COFINS devida) |
| P | Apuração CPRB |
| 1 | Informações complementares (1010, 1100, 1500 retenções) |
| 9 | Encerramento |

## Passo a passo

### 1. Cadastros
- 0140 por estabelecimento, com regime de apuração (cumulativo/não-cum), código de atividade.
- 0200 itens — NCM, unidade, alíquotas PIS/COFINS quando diferenciadas.
- 0500 contas contábeis usadas (vincula a EFD à ECD).

### 2. Documentos
Tipos de bloco por origem:
- A: serviços tomados/prestados.
- C: NFs eletrônicas e modelos antigos.
- D: CT-e e similares.

Cada item escriturado com:
- CST PIS (01 tributada, 04 alíquota zero, 05 reduzida, 06 isenta, 07 monofásico, 49 outras saídas, 50 entrada com crédito etc.)
- CST COFINS (mesma tabela)
- Alíquotas e valores

### 3. Bloco F — receitas e operações específicas
- F500: receita pelo **regime de caixa** (atenção: empresas optantes pelo caixa para Presumido).
- F600: retenções na fonte sofridas (CSRF) — abate da contribuição.
- F700: deduções diversas.

### 4. Bloco M — apuração
- M100/M105: detalhamento dos créditos de PIS por tipo de operação.
- M200/M210: PIS devido por código de receita.
- M500/M505/M600/M610: idem para COFINS.

### 5. CSTs comuns

| CST | Operação |
|---|---|
| 01 | Saída tributada (não cumulativo) |
| 02 | Saída tributada com alíquota diferenciada |
| 04 | Saída alíquota zero |
| 05 | Saída substituição tributária |
| 06 | Saída isenta |
| 07 | Saída com suspensão |
| 08 | Saída sem incidência |
| 09 | Saída com diferimento |
| 49 | Outras saídas |
| 50 | Entrada com direito a crédito (insumo, MP) |
| 51 | Entrada com crédito vinculado a receita não tributada |
| 52 | Entrada com crédito vinculado a receita exportação |
| 53 | Entrada com crédito vinculado a tributada e não tributada |
| 70 | Entrada com 0% |
| 98/99 | Outras |

### 6. Validação e transmissão
- PVA EFD-Contribuições: zero erro de bloqueio.
- Assinar com e-CNPJ.
- Transmitir até dia 10 do segundo mês subsequente.

## Erros comuns

- CST PIS/COFINS divergente entre nota e bloco M (NF entrada com CST 50 mas crédito não escriturado no M105).
- ICMS não excluído da base (Tema 69) — gera divergência com DCTFWeb e com PIS/COFINS pago.
- F600 retenções não preenchidas — perde compensação.
- Receita financeira: lembrar Decreto 8.426/2015 — alíquotas 0,65% / 4% no não-cumulativo (não é alíquota zero como antes).
- Empresa cumulativa lançando créditos no Bloco M100 (vedado).
- Esquecer Bloco P (CPRB) quando a empresa optou pela desoneração.

## Checklist

- [ ] Cadastros 0140/0150/0200/0500 atualizados
- [ ] CSTs revisados por amostra (auditoria de NF)
- [ ] Bloco M batendo com apuração interna (PIS/COFINS apurados)
- [ ] ICMS excluído da base (Tema 69)
- [ ] F500/F600 (caixa, retenções) preenchidos
- [ ] PVA com 0 erros de bloqueio
- [ ] Recibo arquivado
- [ ] DCTFWeb e EFD-Contribuições conciliadas

## Referências

- IN RFB 1.252/2012 (instituição da EFD-Contribuições)
- IN RFB 2.121/2022 (regulamento PIS/COFINS)
- Lei 14.592/2023 (consolidação Tema 69)
- Decreto 8.426/2015 (receita financeira)
- Guia Prático EFD-Contribuições (versão vigente)
- Tabela 4.3.3 CSTs PIS/COFINS
