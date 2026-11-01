---
name: report-live-release-engineer
description: Operar e evoluir o Report Live Afinz/GaaS com build imutável, certificação,
  publicação no único Google Sheets/Slides vivo, rollback, QA visual e contratos de
  dados. Usar ao alterar report-sync, report-sync-v4-setup, migrations, Master Deck
  Spec, blueprints, confiança/prontidão, design system, PDF de QA ou uma release do
  deck.
metadata:
  version: 1.0.0
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Report Live
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Report Live Release Engineer

Tratar o deck como destino de publicação, nunca como fonte de verdade. Preservar um único Sheet e um único Slides vivo.

## Começar

1. Localizar o workspace `ACALENDARIO APP`.
2. Ler integralmente os arquivos obrigatórios em `references/project-map.md`.
3. Inspecionar `git status`; preservar alterações alheias.
4. Identificar a fase pedida: `audit`, `build`, `certify`, `publish` ou `rollback`.
5. Não tocar no deck vivo durante `audit`, `build` ou `certify`.

## Audit

- Comparar código, migrations, Master Deck Spec, vault e último run.
- Verificar CT-1 a CT-9, especialmente missing, SUM/SUM, iso-dias, CPA nomeado e cutoff.
- Tratar prontidão, confiança e elegibilidade como estados independentes e coerentes.
- Inspecionar PDF ou thumbnails para qualquer afirmação visual.
- Registrar achados por slide e por arquétipo.

## Build

- Adquirir ou respeitar idempotência por perfil, período e hashes.
- Gerar manifesto, tabs, ações, narrativa e blueprints.
- Persistir fontes, hashes e artefato no bucket privado.
- Não escrever no Sheets/Slides.
- Reusar IDs determinísticos por `slide_instance_id`.

## Certify

- Executar validações estruturais e editoriais.
- Bloquear publicação se houver erro `blocking` ou `error`.
- Reprovar linha posicional incompleta, null→0, delta contra missing, slide bloqueado como render e narrativa vazia.
- Comparar com a publicação anterior e produzir diff legível.
- Usar golden run e chaos run quando o renderer ou contrato mudar.

## Publish

- Exigir artefato certificado.
- Adquirir lock exclusivo por deck.
- Gravar o Sheet, reconstruir/atualizar slides, substituir narrativas e exportar PDF.
- Registrar `report_publications` e marcar a anterior como `superseded`.
- Liberar lock em `finally`.
- Entregar link vivo, run, publication version, hash e resultado das validações.

## Rollback

- Selecionar publicação histórica certificada.
- Revalidar o artefato.
- Reaplicar o blueprint sem consultar ou recalcular as fontes.
- Registrar motivo, publicação revertida e nova publicação.

## Design e storytelling

- Usar tema claro Afinz.
- Aplicar tokens e arquétipos; não criar layout ad hoc por parceiro.
- Corpo mínimo 11 pt; anexo 9 pt.
- Usar lima apenas para takeaway/total.
- Não aceitar dump monoespaçado como tabela final.
- Um slide precisa responder pergunta, decisão, evidência e limite de leitura.

## Segurança

- Nunca expor secrets.
- Não aplicar migrations nem fazer deploy em produção sem autorização explícita.
- Antes de promoção, verificar RLS, advisors e compatibilidade com runs legados.
- Em recuperação legada, exigir opt-in explícito.

## Handoff

Atualizar `Afinz-CRM-Midia-Vault/08-Engenharia/Report-Live-Versionamento-e-Publicacao.md` com estado, evidência, pendências e próximo passo. Não usar o chat como única fonte de verdade.


## PPTX/PDF sob demanda e migração da gaas-loop

A parte de render da gaas-loop foi preservada em [legacy-render/WORKFLOW.md](references/legacy-render/WORKFLOW.md), como registro de 28/09/2026, não como contrato atual. Antes de gerar PPTX/PDF, conferir renderer, filas e RPCs em origin/main. Não assumir que dependências descritas como ausentes em setembro continuam ausentes. Não executar a antiga parte loop. Usar gaas-growth-loop-operator para Fila e atualização de notas.
