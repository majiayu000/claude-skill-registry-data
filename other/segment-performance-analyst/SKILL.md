---
name: segment-performance-analyst
description: Diagnosticar aquisição CRM por segmento, decompondo volume, funil, custo,
  CAC, canais, BUs e disparos internos. Use quando for necessário entender quais segmentos
  explicam produção, eficiência, queda, ganho, concentração ou oportunidade sem depender
  apenas de médias gerais.
metadata:
  version: 1.0.1
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Análise CRM
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Segment Performance Analyst

## Objetivo

Explicar a contribuição e a dispersão interna de cada segmento de aquisição.

## Pré-condições

Consumir:

- gate do `$growth-data-quality-monitor`;
- registros do `$crm-dispatch-intelligence`.

## Workflow

1. Agrupar os disparos válidos por segmento.
2. Calcular somas antes das taxas: custo, base, propostas, aprovados e cartões.
3. Derivar conversão e CAC usando os totais agregados.
4. Comparar:
   - último dia fechado vs. média dos 7 anteriores;
   - 7d vs. 7d anteriores;
   - MTD vs. ritmo/meta quando aplicável;
   - 28d vs. histórico do próprio segmento.
5. Decompor a variação por disparo, canal, BU, oferta e parceiro.
6. Medir concentração:
   - participação dos três maiores disparos;
   - participação do canal dominante;
   - participação da BU dominante.
7. Identificar dispersão entre disparos vencedores e perdedores.
8. Classificar o segmento:
   - motor de produção;
   - eficiente sem escala;
   - escala ineficiente;
   - deterioração;
   - baixa evidência.

## Regras

- Não esconder outliers relevantes em médias.
- Não recomendar escala quando o resultado depende de um único disparo.
- Não comparar segmentos com etapas incompatíveis sem ressalva.
- Explicar se a mudança veio de volume, mix, taxa ou custo.
- Usar o histórico documentado do vault como contexto, nunca como dado atual.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Para cada segmento emitir:

- métricas e deltas;
- decomposição da mudança;
- concentração;
- melhores e piores disparos;
- canal e BU dominantes;
- classificação operacional;
- severidade, confiança e ação.

Incluir dados para:

- barras de produção com delta;
- dispersão volume x conversão com CAC;
- tendência de até quatro segmentos;
- tabela operacional.
