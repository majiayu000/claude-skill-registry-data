---
name: ferias-13-salario"
description: Calcula e processa férias (período aquisitivo, gozo, abono pecuniário, terço constitucional) e 13º salário (1ª e 2ª parcela), com encargos, adiantamentos e eSocial.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

- **Férias**: a cada período aquisitivo de 12 meses do empregado (CLT art. 130). Concedidas dentro dos 12 meses do período concessivo.
- **13º salário**: 1ª parcela entre fevereiro e novembro (geralmente em novembro junto com folha); 2ª parcela até 20 de dezembro.

## Inputs necessários

1. Data de admissão e período aquisitivo a ser usufruído
2. Faltas injustificadas no período aquisitivo
3. Salário do mês concessão + média variáveis dos últimos 12 meses (HE, comissões, adicionais)
4. Opção do empregado: 30 dias gozo ou parcelamento (Reforma 2017: até 3 períodos, sendo um ≥ 14 dias e os outros ≥ 5)
5. Abono pecuniário (1/3 das férias convertido em dinheiro — opcional, art. 143)
6. Adiantamento 13º (1ª parcela)
7. Afastamentos no período (auxílio-doença não interrompe se < 6 meses; > 6 meses suspende — art. 133)

## Cálculo das férias

### Direito (art. 130 CLT)

| Faltas injustificadas | Direito |
|---|---|
| Até 5 | 30 dias |
| 6-14 | 24 dias |
| 15-23 | 18 dias |
| 24-32 | 12 dias |
| > 32 | Perde |

### Valores

```
Salário do mês × (dias_ferias / 30) = Valor das férias
+ 1/3 constitucional sobre o valor das férias
+ Abono pecuniário (10 dias × salário/30 + 1/3 sobre o abono) — se opção
+ Adicional de férias proporcional sobre médias (HE, adicionais, comissões dos últimos 12 meses)
```

### Descontos
- INSS sobre férias (e 1/3) — **incide** (Lei 8.212/91)
- IRRF sobre férias (e 1/3) — incide. Atenção: **abono pecuniário (10 dias) é isento de IRRF e INSS** (Lei 7.713/88 art. 6º).
- FGTS sobre férias e 1/3 — incide.

### Pagamento

Antecipado: **até 2 dias antes** do início das férias (CLT art. 145).

### Comunicação

- Aviso ao empregado com 30 dias de antecedência (CLT art. 135).
- Empregado opta por abono pecuniário com 15 dias de antecedência do término do período aquisitivo.

## Cálculo do 13º salário

### Direito
- Empregado com pelo menos **15 dias** trabalhados no mês (Lei 4.090/62) computa o mês integral.
- Avos: cada mês trabalhado = 1/12 do 13º.

### Cálculo

```
13º = Salário do mês de dezembro × (avos / 12)
```

Médias de variáveis (HE, adicionais) entram no 13º.

### Parcelas

- **1ª parcela** (até 30/11): metade do 13º estimado, **sem desconto INSS/IRRF**.
- **2ª parcela** (até 20/12): saldo do 13º, **com desconto INSS e IRRF** sobre o total.

### Encargos
- INSS empresa e empregado: incide
- IRRF: na 2ª parcela, em DARF separado (cód 0561)
- FGTS: depositado no mês da 2ª parcela

## Templates

### Cálculo de férias

```
EMPREGADO _________________ Adm: __/__/____ Per. aquis: __/__/____ a __/__/____
Faltas inj.: ___ → Direito: ___ dias
Salário fixo do mês: R$ _________
Média variáveis (12m): R$ _________
Salário base de cálculo: R$ _________

FÉRIAS:
  Valor das férias (___ dias): R$ _________
  + 1/3 constitucional: R$ _________
  + Abono pecuniário (___ dias): R$ _________
  + 1/3 sobre abono: R$ _________
  TOTAL BRUTO: R$ _________

DESCONTOS:
  INSS sobre férias (sem abono): R$ _________
  IRRF (sem abono): R$ _________

LÍQUIDO: R$ _________
```

### Cálculo do 13º (2ª parcela)

```
Avos: ___ / 12  Salário dez: R$ _________  Média variáveis: R$ _________
Base 13º total: R$ _________
1ª parcela paga em ___: R$ _________
Saldo 2ª parcela: R$ _________
INSS sobre o total do 13º: R$ _________
IRRF sobre o total: R$ _________
DARF 0561 a recolher: R$ _________
Líquido 2ª parcela: R$ _________
```

## Erros comuns

- IRRF/INSS sobre abono pecuniário (incorreto — é isento).
- Esquecer média de variáveis (HE habituais, comissões).
- 13º calculado sobre salário-mínimo quando o empregado tem comissão (precisa usar média).
- Pagar férias junto com a folha do mês (errado: deve ser 2 dias antes do início).
- Empregado afastado por > 6 meses por doença comum: não tem direito a férias do período em que esteve afastado.
- Adiantamento 13º sem opção formal do empregado (Lei 4.749/65 art. 2º — empregado pode pedir junto com férias se requerer em janeiro).
- Não recolher INSS sobre 1/3 de férias — o STF (RE 565.160) e STJ (Tema 985) discutiram, mas o entendimento atual é **incide INSS sobre 1/3 de férias** (em razão da Lei 8.212/91 art. 28 §9º "a"). Atenção: STF declarou inconstitucionalidade da incidência sobre 1/3 do empregador (Tema 985, repercussão geral, 2020) — contribuição patronal sobre 1/3. Verificar a versão final.

## Checklist

### Férias
- [ ] Aviso entregue 30 dias antes
- [ ] Direito a dias verificado (faltas)
- [ ] Médias de variáveis calculadas
- [ ] Abono pecuniário com pedido formal
- [ ] Pagamento 2 dias antes do início
- [ ] eSocial S-2230 (afastamento código 17 férias)
- [ ] Holerite específico de férias
- [ ] FGTS depositado

### 13º
- [ ] 1ª parcela paga até 30/11
- [ ] 2ª parcela paga até 20/12
- [ ] DARF IRRF separado
- [ ] eSocial S-1200 (categoria 13º)
- [ ] FGTS depositado
- [ ] Aviso prévio integrando avos quando rescisão até 30/11

## Referências

- CLT arts. 129 a 153 (férias)
- Lei 4.090/1962 e 4.749/1965 (13º)
- Lei 7.713/1988 art. 6º (isenção abono pecuniário)
- Lei 8.212/1991 art. 28 (INSS)
- RE 565.160 e Tema 985 STF (1/3 de férias — patronal)
- Súmula 7 e 89 TST
