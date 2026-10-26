---
name: fechar-entrega
description: Registra mudanças, validações e pendências e realiza commit local quando autorizado pelo pedido ou fluxo do projeto. Use para fechar entrega ou sessão e preparar resumo de tarefa; não aprova code review/QA, não faz push e não publica no ClickUp.
---

# Fechar entrega

Consolide somente a entrega da sessão. Leia as regras locais e confirme repositório, branch, alterações próprias, validações e gates pendentes. Não transforme uma solicitação de resumo em autorização para commit.

## Perfil e registro

Na Intranet/Orca, leia [perfil Intranet](references/intranet.md), preservando os marcadores ClickUp, o evento de handoff e os contratos com o planejador/orquestrador. Fora desse contexto, use o padrão documental existente; sem padrão, prefira `docs/historico/entregas/<data>-<assunto>.md`. Não exija ClickUp nem escreva em caminhos externos herdados.

Registre objetivo, mudanças e motivo, arquivos afetados, verificações realmente executadas/resultados, migrations/deploy, limitações e próximos passos. Atualize o registro da mesma sessão em vez de duplicá-lo. Não atribua alterações de terceiros à entrega. Diff completo só quando exigido pelo projeto; exclua o próprio registro, artefatos derivados, binários e segredos.

## Commit e evidência

Com autorização já estabelecida, confira branch e índice, adicione caminhos explícitos e revise o diff staged antes do commit. Não inclua alterações alheias já staged, nem as descarte ou faça unstage silenciosamente. Siga a política local de branch e mensagem. Sem autorização ou com conflito no índice, conclua o registro e informe o impedimento concreto.

Registro entra junto da mudança quando o fluxo exige. Se o projeto determina review pós-commit, o relatório fica no commit separado previsto; correções subsequentes são nova alteração, com nova verificação. Não faça amend de commits já referenciados em índices de entrega.

Índice diário só quando o projeto o usa: acrescente após o último commit aplicável, verifique duplicação e serialize escritas concorrentes. Se não houve commit, diga “sem commit”; nunca atribua o HEAD anterior à nova entrega.

Não faça push, merge, deploy ou publicação externa por efeito desta skill. Resumo preparado para ClickUp não significa resumo publicado. Não marque DONE sem revisão e QA exigidos: fechar registro/commit pode terminar com gates pendentes.

Saída: resumo da entrega, validações, pendências, caminho do registro, hash do commit apenas se realizado e, no perfil Intranet/ORCA, o `FLUXO_EVENTO` consumido pelo orquestrador.
