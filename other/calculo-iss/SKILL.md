---
name: calculo-iss"
description: Apura ISS sobre serviços, identifica o município competente conforme LC 116/2003 com alterações da LC 175/2020, trata retenção pelo tomador e aplica alíquota mínima de 2%.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

> ⚠️ **AVISO FISCAL — CONFIRA ANTES DE GERAR A GUIA.** Todo código de receita (DARF/DAS), alíquota, base de cálculo, valor e data de vencimento gerado por este agente é **rascunho de apoio** e pode variar por ano, regime tributário, município ou caso específico. **Confira sempre na fonte oficial vigente (Receita Federal / e-CAC / legislação estadual e municipal) antes de transmitir declaração ou pagar guia.** A conferência final é responsabilidade do contador responsável.

## Quando usar

Prestadores de serviço de qualquer regime (Simples paga via DAS, Presumido/Real via DAM/guia municipal). Apuração mensal — vencimento conforme legislação municipal (geralmente dia 10 ou 15 do mês subsequente).

## Inputs necessários

1. Item da Lista Anexa da LC 116/2003 que corresponde ao serviço
2. Município do estabelecimento prestador e município do tomador
3. Alíquota municipal vigente (mín 2% — LC 157/2016, máx 5%)
4. Valor da NFS-e + descontos + materiais aplicados (dedutíveis em alguns itens)
5. Tomador é PJ obrigada a reter? (cada município define)
6. Operação se enquadra na lista de exceções da LC 116 (recolhimento no local da execução)?
7. Empresa do Simples? (recolhe ISS dentro do DAS, salvo retenção pelo tomador)

## Onde recolher: prestador ou tomador?

A regra geral é **prestador** (seu município). Mas a LC 116/2003, art. 3º, lista exceções em que o ISS é devido **no município do tomador / local de execução**:

- Construção civil (item 7.02 e 7.05)
- Limpeza, manutenção, vigilância, segurança
- Cessão de andaimes/palcos
- Recreação e lazer
- Fornecimento de mão de obra
- Saúde, agenciamento (LC 175/2020 — planos de saúde, cartões, leasing, agenciamento de fundos)

A LC 175/2020 trouxe a regra do **domicílio do tomador** para serviços financeiros, planos e cartões — operacionalizada pelo CGOA via sistema padrão nacional.

## Cálculo

```
ISS = Base × Alíquota
Base = Valor da NFS-e − materiais dedutíveis (itens 7.02/7.05) − descontos incondicionais
```

- **Item 7.02 e 7.05 (construção civil)**: deduzir materiais incorporados à obra fornecidos pelo prestador (se admitido pela legislação municipal — Lei municipal pode ser mais restritiva).
- **Subempreitada**: deduzir o valor pago a subempreiteiros que tenham recolhido ISS (item 7.02).

### Alíquota mínima 2% (LC 157/2016)
Vedação a benefícios que reduzam a carga abaixo de 2%, salvo para itens 7.02, 7.05, 16.01 (transporte público).

## Retenção pelo tomador

- Quando obrigatória pela lei municipal (geralmente PJ tomadora de serviço de outra cidade ou para os itens da LC 116, art. 3º).
- Tomador retém o ISS, recolhe na guia municipal própria e fornece o comprovante ao prestador.
- O prestador **não** recolhe novamente; abate na sua apuração mensal.
- Para Simples: tomador retém o ISS na alíquota destacada na NFS-e (alíquota efetiva do Simples + porção ISS do anexo).

## Templates

```
NFS-e nº ____ Data ____ Item LC 116 ____
Município prestador: __________  Município tomador: __________
ISS devido a: [ ] prestador  [ ] tomador (LC 116 art. 3º)

Valor do serviço.................. R$ _________
(−) Materiais (item 7.02/7.05).... R$ _________
(−) Subempreitadas (com ISS)..... R$ _________
(=) BASE........................... R$ _________
ALÍQUOTA: ___%
ISS......................... R$ _________
Retido pelo tomador? [ ] Sim ➝ Compensar na apuração mensal
```

### Exemplo

Construtora em SP presta serviço em Campinas (item 7.02): NFS-e R$ 100.000, materiais R$ 30.000.
- Base = 100.000 − 30.000 = R$ 70.000
- Alíquota Campinas (item 7.02) = 5%
- ISS = R$ 3.500 (recolhido em Campinas pelo prestador, via guia DAM Campinas).

## Erros comuns

- Recolher ISS no município errado (prestador vs. local da execução nas exceções da LC 116).
- Empresa do Simples: a alíquota de ISS retida pelo tomador deve ser a alíquota do anexo do Simples (informada no XML), nunca a alíquota cheia municipal (Resolução CGSN 140, art. 27).
- Dupla tributação por dois municípios — exige PER/DCOMP municipal ou ação judicial.
- Não emitir NFS-e em municípios que adotaram o padrão nacional (Sistema NFS-e nacional desde 2023).
- Esquecer dedução de materiais em construção civil quando a lei municipal permite.
- Prestador autônomo (PF) tributado pela ISSQN fixa — não confundir com PJ.

## Checklist

- [ ] Item LC 116 identificado corretamente
- [ ] Local de incidência verificado (regra geral × exceções art. 3º)
- [ ] Alíquota municipal conferida (lei municipal vigente)
- [ ] Materiais/subempreitadas deduzidos (quando cabível)
- [ ] Retenção pelo tomador identificada e abatida
- [ ] NFS-e transmitida e XML arquivado
- [ ] DAM/guia municipal paga no vencimento
- [ ] Para Simples: valor ISS dentro do DAS confere

## Referências

- LC 116/2003 — Lei do ISS
- LC 157/2016 — alíquota mínima 2%
- LC 175/2020 — local do tomador para serviços específicos + Sistema CGOA
- Lei municipal vigente (revisar a cada ano)
- Súmula 274 STJ — cabe restituição de ISS pago a município incompetente
