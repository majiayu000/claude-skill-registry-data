---
name: growth-report-operator
description: Orquestrar e consolidar análises especializadas de qualidade de dados,
  disparos CRM, segmentos, campanhas de mídia e measurement em um único relatório
  operator owner. Use para gerar reports diários ou semanais de aquisição, totalizar
  registros, reconciliar conflitos, priorizar ações e criar o storytelling final ou
  rascunho de e-mail.
metadata:
  version: 1.0.1
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Relatórios
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Growth Report Operator

## Objetivo

Produzir uma única leitura operacional confiável a partir das saídas dos cinco especialistas.

## Ordem de execução

1. Executar `$growth-data-quality-monitor`.
2. Se o gate permitir, executar em paralelo:
   - `$crm-dispatch-intelligence`
   - `$segment-performance-analyst`
   - `$paid-media-campaign-analyst`
   - `$measurement-attribution-auditor`
3. Aguardar todos terminarem ou declararem falha.
4. Validar cada saída contra [shared-output-contract.md](references/shared-output-contract.md).
5. Reconciliar totais e conflitos.
6. Produzir storytelling e e-mail único.

## Reconciliação

- Fonte agregada não pode contradizer a soma dos registros granulares sem explicação.
- Segmentos devem reconciliar com disparos válidos.
- Campanhas devem reconciliar com o total por plataforma.
- Measurement pode rebaixar ou bloquear conclusões de mídia.
- Data quality pode limitar qualquer seção.
- Quando dois agentes repetirem o mesmo sinal, fundir evidências e manter uma ação.
- Não somar métricas incompatíveis entre CRM e mídia.

## Priorização

Usar:

`prioridade = impacto x urgência x confiança / esforço`

Classificar:

- `Agir hoje`
- `Acompanhar`
- `Investigar`

Limitar o resumo executivo a:

- estado geral;
- três mudanças materiais;
- risco principal;
- oportunidade principal;
- ação prioritária.

## Storytelling

Aplicar:

`Estado -> Mudança -> Origem -> Impacto -> Decisão -> Ação`

Depois aprofundar:

1. qualidade dos dados;
2. produção e meta;
3. aquisição CRM;
4. disparos prioritários por segmento;
5. mídia por campanha;
6. rentabilização até clique;
7. plano de ação.

## E-mail

Gerar:

- assunto com data;
- resumo executivo;
- tabelas curtas;
- detalhes granulares somente dos itens materiais;
- gráficos compactos quando o ambiente permitir;
- nota de confiança e atualização;
- indicação clara de que não foi enviado quando a integração não estiver ativa.

Não enviar e-mail sem autorização explícita e integração disponível.

## Saída

Seguir [shared-output-contract.md](references/shared-output-contract.md).

Além do relatório, emitir uma seção de auditoria com:

- agentes concluídos;
- agentes com falha;
- fontes limitadas;
- totais reconciliados;
- conflitos resolvidos;
- conclusões bloqueadas.
