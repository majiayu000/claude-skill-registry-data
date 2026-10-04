---
name: voz-do-cliente
description: |
  Sintetiza o relatório semanal de análise de chamados do canal de Chat do ClickUp "Voz do cliente" em conhecimento local — temas recorrentes, volume quando o relatório traz número, e sinais de atrito novos vs. já conhecidos — registrado em knowledge/pesquisas/voz-do-cliente/ e indexado em knowledge/pesquisas/INDEX.md.
  Não cria nem infere achado que o relatório não contenha; nunca escreve de volta no ClickUp.
  Executado pelo agente agente-discovery. Feito para rodar sob demanda ou agendado semanalmente.
  Comandos: /voz-do-cliente run, /voz-do-cliente dry-run, /voz-do-cliente help
metadata:
  invocation: user
  inputs: canal de Chat do ClickUp "Voz do cliente" (relatório semanal de análise de chamados)
  outputs: entrada datada em knowledge/pesquisas/voz-do-cliente/, linha nova na tabela "Voz do cliente" de knowledge/pesquisas/INDEX.md
  side_effects: write-confirmed
  context: knowledge/pesquisas/INDEX.md, knowledge/decisions/2026-09-24-automacao-semanal-voz-do-cliente.md
  completion: relatório da semana sintetizado e registrado (ou "sem relatório novo" reportado), índice atualizado, lacunas sinalizadas
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>

# Voz do Cliente — síntese semanal

Transforma o relatório semanal de análise de chamados (canal de Chat do ClickUp "Voz do cliente") em
conhecimento rastreável — não a transcrição do relatório, mas o que ele diz sobre temas, volume e
tendência.

> **Quem executa:** o agente [agente-discovery](../../agents/agente-discovery.md).
> **Origem:** decisão de 2026-09-24 — ver
> `knowledge/decisions/2026-09-24-automacao-semanal-voz-do-cliente.md`.

## Fonte

- Canal de Chat do ClickUp: [Voz do cliente](https://app.clickup.com/9006076935/chat/r/8ccvn07-71131).
- **Formato do canal:** a mensagem principal costuma carregar só o assunto; o corpo do relatório vai
  como resposta na thread dela. Sempre buscar a thread antes de concluir que uma mensagem não tem
  conteúdo (`clickup_get_chat_message_replies`).

## Comandos

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `run` | `/voz-do-cliente run` | Busca o relatório mais recente do canal, sintetiza e grava. |
| `dry-run` | `/voz-do-cliente dry-run` | Gera a síntese e **apresenta** sem gravar nada. Use para revisar antes. |
| `help` | `/voz-do-cliente help` | Explica escopo, processo e formato. |

## Verificação de Conector (obrigatória)

Antes de rodar, verifique silenciosamente se o conector do ClickUp está ativo (ex.:
`clickup_get_chat_channels`). Se não estiver disponível, interrompa e oriente a conectar o ClickUp
(Configurações → Integrações → ClickUp).

## Processo

1. **Localizar o canal** "Voz do cliente" via `clickup_get_chat_channels` (o link já dá o canal; use-o
   para confirmar o ID).
2. **Buscar as mensagens mais recentes** (`clickup_get_chat_channel_messages`) e identificar o relatório
   mais recente ainda **não sintetizado** — comparar contra as entradas já registradas em
   `knowledge/pesquisas/voz-do-cliente/`.
3. **Buscar o corpo do relatório**: se a mensagem mais recente trouxer só o assunto, buscar a thread
   (`clickup_get_chat_message_replies`) para o conteúdo real.
4. **Sintetizar**, ficando estritamente dentro do que o relatório afirma:
   - temas recorrentes e, quando o relatório trouxer, volume/frequência por tema;
   - sinal novo vs. sinal já conhecido em semanas anteriores (comparar com entradas anteriores no
     índice);
   - qualquer recomendação que o próprio relatório já traga — não proponha uma nova.
5. **Checar idempotência**: se já existe entrada para o período deste relatório, **não gravar de novo** —
   reporte "sem relatório novo desde a última execução".
6. **Gravar** um arquivo novo em `knowledge/pesquisas/voz-do-cliente/AAAA-MM-DD-relatorio-chamados.md`
   (data do período coberto pelo relatório, não a data de execução da skill), com: período coberto, temas
   e volume, sinais novos, link da thread original.
7. **Atualizar a tabela "Voz do cliente"** em `knowledge/pesquisas/INDEX.md` com uma linha nova apontando
   para o arquivo.
8. **Reportar**: o que foi registrado (ou "sem relatório novo"), qualquer formato inesperado ou lacuna
   encontrada.

## Modo de confirmação

- **Interativo** (`run`/`dry-run` pedido na conversa): apresente a síntese antes de gravar, como qualquer
  skill `write-confirmed` do PM Loadout.
- **Agendado/autônomo**: a decisão de 2026-09-24 pré-autoriza a execução agendada a **gravar direto em
  `knowledge/pesquisas/`, sem confirmação por execução** — essa autorização cobre só esse escopo local.
  Postar, comentar ou enviar qualquer mensagem no ClickUp **nunca** está autorizado por essa skill, em
  nenhum modo — se isso um dia fizer sentido (ex.: avisar o squad de um tema novo), é uma decisão
  separada, feita sob confirmação, mesmo em execução agendada.

## Guardrails

- **Não fabrique tema, número ou causa** que o relatório não contenha. Relatório ambíguo ou insuficiente
  → registrar a lacuna, não inventar.
- **Uma reclamação isolada não vira "tendência"** sem o relatório indicar volume ou frequência — mesma
  régua de `aprendizado-produto`.
- **Nunca escreva de volta no ClickUp** — esta skill só lê o canal e grava localmente.
- **Nunca inclua CPF ou outro dado pessoal identificável** que eventualmente apareça citado num chamado —
  se aparecer no relatório de origem, sinalizar a lacuna e omitir do arquivo gravado.
- **Não crie entrada duplicada** para o mesmo período — checar o índice antes de gravar (passo 5).

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [../../../knowledge/pesquisas/INDEX.md](../../../knowledge/pesquisas/INDEX.md) | Índice central de pesquisas; tabela "Voz do cliente" recebe a linha nova |
| [../../../knowledge/decisions/2026-09-24-automacao-semanal-voz-do-cliente.md](../../../knowledge/decisions/2026-09-24-automacao-semanal-voz-do-cliente.md) | Decisão que autoriza a execução agendada e define o escopo da autonomia |
| [../../agents/agente-discovery.md](../../agents/agente-discovery.md) | Agente executor |
