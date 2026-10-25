---
name: esocial-rescisao"
description: Executa o desligamento de empregado no eSocial com S-2299, calcula verbas rescisórias por motivo, gera GRRF/FGTS, comunica seguro-desemprego e respeita prazos do art. 477 da CLT.
allowed-tools: Read Grep Bash Edit Write
user-invocable: true
---

## Quando usar

Sempre que houver término do contrato de trabalho — sem justa causa, com justa causa, pedido de demissão, acordo, fim de contrato, aposentadoria, falecimento. Prazo: **até 10 dias** após o desligamento (CLT art. 477 §6º) para pagamento e quitação.

Evento eSocial:
- **S-2299** — Desligamento (CLT)
- **S-2399** — Término de TSV (estagiário, dirigente sem vínculo)

## Inputs necessários

1. Data de desligamento e motivo (código S-2299)
2. Aviso prévio: trabalhado, indenizado, dispensa
3. Saldo de salário do mês
4. Férias proporcionais e vencidas + 1/3
5. 13º proporcional
6. Saldo FGTS + multa (40% sem justa causa, 20% acordo, 0% justa causa/pedido)
7. Valores de descontos (vale-transporte, plano de saúde, contribuições)
8. Movimentação Conta-Salário e plano de saúde (continuidade ou suspensão)
9. PCMSO/PPRA: ASO demissional

## Códigos S-2299 — motivos

| Código | Motivo | Aviso prévio | Saque FGTS | Multa 40% | Seguro-desemp |
|---|---|---|---|---|---|
| 02 | Rescisão sem justa causa pelo empregador | Sim | Sim | Sim | Sim |
| 03 | Rescisão com justa causa pelo empregador | Não | Não | Não | Não |
| 04 | Culpa recíproca | 50% | Sim | 20% | Não |
| 05 | Término contrato a prazo determinado | Não | Sim | Não | Não |
| 06 | Pedido de demissão | Indenizado p/ empregado | Não | Não | Não |
| 07 | Acordo entre partes (Lei 13.467/2017) | 50% | 80% | 20% | Não |
| 09 | Aposentadoria | Não | Sim | Não | Não |
| 10 | Falecimento | — | Sim (dependentes) | Não | Não |
| 11 | Justa causa pelo empregado (rescisão indireta) | Sim | Sim | Sim | Sim |
| 14 | Encerramento atividades empresa | Sim | Sim | Sim | Sim |

## Cálculo padrão (rescisão sem justa causa)

```
Saldo salário = (dias trabalhados / 30) × salário
Aviso indenizado = 1 salário (+ acréscimo Lei 12.506/2011: 3 dias por ano completo, máx 60 dias adicionais)
Férias vencidas = 1 salário + 1/3 (se já completou período aquisitivo)
Férias proporcionais = (avos / 12) × salário + 1/3
13º proporcional = (avos / 12) × salário
FGTS depositado no mês + multa 40% sobre o saldo
```

Atenção: aviso indenizado projeta tempo de serviço e integra para todos os efeitos (Súmula 305 TST).

## Passo a passo

### 1. Definir motivo e calcular verbas

### 2. Emitir TRCT (Termo de Rescisão)
- Modelo padrão MTP. Detalhar cada verba e desconto.

### 3. Pagar até o 10º dia (art. 477 §6º)
- Multa do art. 477 §8º: salário do empregado em favor dele se houver atraso.

### 4. Enviar S-2299
- Prazo: até dia 15 do mês subsequente (mas o pagamento é em 10 dias).

### 5. Gerar GRRF (FGTS rescisório)
- Conectividade Social ICP > Movimento de Rescisão > GRRF.
- Saldo FGTS + multa (40%, 20% ou 0% conforme motivo).
- Pagamento até a data do pagamento das verbas.

### 6. Sefip / DAE / Conectividade
- A partir do eSocial completo, GFIP foi descontinuado para CPP/IRRF, mas GRRF ainda é gerada via Conectividade Social até implementação plena do FGTS Digital (em rollout).

### 7. Comunicar seguro-desemprego
- Empregador Web — gerar requerimento + chave do trabalhador
- Trabalhador acessa portal Empregador/Trabalhador e dá entrada online
- Carências: 12, 9 ou 6 meses (1ª, 2ª, 3ª solicitação)

### 8. Plano de saúde
- Aviso ao trabalhador da Lei 9.656/98: opção de manutenção (aposentadoria 1 ano de plano = 1 ano de extensão; demissão 1/3 do tempo de plano, mín 6 meses, máx 24).

### 9. Homologação
- Reforma trabalhista de 2017 dispensou homologação no sindicato (CLT art. 477 §3º revogado), mas convenção coletiva pode exigir.

## Templates

### TRCT — verbas típicas (sem justa causa)

```
TRCT — _________________________ CPF _________ Adm: __/__/__ Demissão: __/__/__
Motivo: 02 — sem justa causa (eSocial)

VERBAS:
  Saldo salário (___ dias)............... R$ _________
  Aviso prévio indenizado (__ dias)..... R$ _________
  Férias vencidas + 1/3.................. R$ _________
  Férias proporcionais (__/12) + 1/3..... R$ _________
  13º proporcional (__/12)............... R$ _________
DESCONTOS:
  INSS sobre rescisão.................... R$ _________
  IRRF (DARF separado)................... R$ _________
  Vale-transporte (já creditado)......... R$ _________

LÍQUIDO............................. R$ _________

FGTS:
  Saldo na conta vinculada............... R$ _________
  Depósitos rescisórios (mês corrente)... R$ _________
  Multa 40%.............................. R$ _________
  GRRF a pagar........................... R$ _________
```

## Erros comuns

- Não pagar em 10 dias → multa 477 §8º (1 salário).
- Confundir aviso trabalhado com indenizado nos cálculos (trabalhado: empregado trabalha, recebe normal; indenizado: paga e libera).
- Esquecer Lei 12.506/2011 (3 dias por ano + 30 dias base).
- Acordo Lei 13.467/2017 com multa 40% (correto: 20%).
- Rescisão indireta sem provas → reverte em justa causa.
- Não dar baixa no plano de saúde → continua cobrando da empresa.
- Justa causa sem documentação (advertências, suspensões) → revertida em juízo.

## Checklist

- [ ] Motivo S-2299 correto
- [ ] Cálculo de verbas conferido
- [ ] ASO demissional realizado
- [ ] TRCT entregue e assinado
- [ ] Pagamento em até 10 dias
- [ ] GRRF emitida e paga (FGTS Digital)
- [ ] S-2299 transmitido até dia 15 do mês seguinte
- [ ] Chave seguro-desemprego entregue (quando cabível)
- [ ] Plano de saúde: opção de manutenção comunicada
- [ ] PIS retirado do PIS/PASEP (saque-rescisão)

## Referências

- CLT arts. 477 a 491
- Lei 13.467/2017 (Reforma Trabalhista)
- Lei 12.506/2011 (aviso prévio proporcional)
- Lei 8.036/1990 (FGTS)
- Lei 9.656/1998 art. 30/31 (plano de saúde)
- Manual eSocial S-1.5 (S-2299)
