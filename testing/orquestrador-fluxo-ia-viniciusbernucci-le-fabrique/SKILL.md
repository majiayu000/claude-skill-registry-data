---
name: orquestrador-fluxo-ia
description: Orquestra tarefas de desenvolvimento no fluxo Intranet/ORCA depois do planejamento do Tech Lead, acionando automaticamente planejamento operacional, implementação, revisão, revalidação, QA, integração e publicação no ClickUp. Use ao continuar uma tarefa desse fluxo; preserva os checkpoints humanos de ClickUp, Tech Lead, criação das worktrees, correções de code review e push/PR.
---

# Orquestrador do fluxo de desenvolvimento com IA

Seja o único ponto de entrada do fluxo. Leia [estado e gates](references/estado-e-gates.md), o ticket, `AGENTS.md`, `CLAUDE.md` e o estado persistido da tarefa. Decida a próxima etapa pela evidência existente e acione a skill ou o agente responsável; não peça ao usuário para escolher ou invocar componentes internos.

## Contrato de automação

- Os checkpoints humanos são exatamente: selecionar as tarefas no ClickUp, executar `tech-lead`, criar as worktrees no ORCA, aplicar as correções propostas pelo code review e fazer push/abrir PRs. Não automatize esses cinco pontos.
- Depois que o `tech-lead` entregar uma especificação pronta, assuma a coordenação. Pare em `AGUARDANDO_WORKTREES_ORCA`, mostrando somente repositório, nome e caminho esperado. Quando o usuário confirmar as worktrees, prossiga automaticamente.
- Não use relato de sucesso como gate. Avance por commits, relatórios, matrizes e estados gravados.
- Preserve a separação de papéis: quem implementa não aprova o próprio código ou QA. O orquestrador coordena; não substitui os especialistas.
- Relatórios e filas vivem em `docs/historico/reviews/`. O especialista apenas os escreve; depois do gate, o orquestrador faz um commit documental explícito por repositório, sem push, para que a evidência não fique solta ou misturada ao código.
- Correções de code review nunca são aplicadas automaticamente. O usuário aplica à mão ou indica os IDs (um a um ou em lote) para o agente aplicar e commitar, conforme "Aplicação sob indicação do usuário" do `review-loop-driver`. O orquestrador organiza a fila e, quando o usuário informar que terminou, revalida os IDs afetados.
- Correções de QA podem ser delegadas automaticamente ao `implementador-de-ticket`, pois são falhas funcionais contra critérios já aprovados. Limite a três ciclos; se o mesmo bloqueio persistir, registre a evidência e peça decisão.
- Nunca use `main` como branch de trabalho ou integração. Push e abertura de PR são sempre manuais. A publicação final no ClickUp pode ser automática quando houver integração e autorização registrada.

## Roteamento automático

1. **Entrada manual:** receba a especificação produzida pelo `tech-lead`. Se estiver incompleta, devolva ao checkpoint humano; não execute o Tech Lead pelo usuário.
2. **Planejamento automático:** acione `worktree-planner`. Ele cria o plano, os prompts e o estado persistente.
3. **Pausa ORCA:** aguarde apenas a criação manual das worktrees. Confirme paths e branches antes de delegar.
4. **Implementação:** delegue cada plano ao agente da worktree, usando `implementador-de-ticket` quando disponível. Cada agente testa, documenta, aciona `fechar-entrega`, commita e devolve evidências.
5. **Gate técnico único:** acione `revisor-de-codigo` uma vez por worktree/conjunto de commits. Os agentes `code-reviewer`, `clean-code-reviewer` e `security-reviewer` são especialidades internas desse gate, nunca gates paralelos adicionais.
6. **Correções sob indicação:** acione `review-loop-driver`, grave a fila priorizada, faça o commit documental do relatório+fila e pare em `AGUARDANDO_CORRECOES_REVIEW`. Nesse estado, cada mensagem do usuário que indicar IDs dispara a aplicação só desses IDs, com commit, e volta ao mesmo estado; nada é aplicado sem indicação. Quando o usuário disser que terminou as correções, peça ao `revisor-de-codigo` revalidação focal dos IDs corrigidos. Se ainda houver bloqueantes, atualize e commite a fila antes de retornar ao mesmo checkpoint humano.
7. **Gate funcional:** acione `revisor-de-qa`. Commite o relatório de QA separadamente. Se houver `FAIL`, transforme os bugs em fila, corrija e rode o modo de revalidação de QA para os cenários falhos e regressões impactadas; persista cada nova evidência.
8. **Integração:** quando revisão técnica e QA estiverem aprovados, integre na branch definida no plano `99-merge-e-limpeza`, nunca na `main`, e execute as verificações pós-merge.
9. **Revisão final:** rode `revisor-de-codigo` sobre o diff integrado e `review-guide` para gerar o roteiro humano/PR. Se surgir bloqueio novo, gere a fila e retorne ao checkpoint humano de correções; depois reintegre e revalide. Sem bloqueios, faça um commit documental dos relatórios finais.
10. **Push e PR manuais:** prepare comandos, títulos, descrições e evidências, então pare em `AGUARDANDO_PUSH_PRS`. Não faça push nem abra PR.
11. **ClickUp:** quando o usuário fornecer ou confirmar as URLs dos PRs, acione `publicador-clickup`. Sem integração disponível, gere o texto pronto e mantenha o estado pendente.

Atualize o estado após cada transição, incluindo caminhos e hashes das evidências. Termine somente em `CONCLUIDO`, ou com um bloqueio concreto que exija ação humana.
