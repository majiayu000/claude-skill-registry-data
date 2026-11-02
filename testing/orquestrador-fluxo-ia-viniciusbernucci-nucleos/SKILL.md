---
name: orquestrador-fluxo-ia
description: Executa um lote planejado até commits, review auditado, correções, QA, integração em revisao/ e limpeza segura. Use para executar ou retomar o manifesto do planejador-de-lote; sem checkpoints humanos intermediários, push ou PR.
---

# Orquestrador do fluxo de IA

Chamar esta skill para executar um lote autoriza criação de worktrees, delegação, implementação, correções auditadas, commits, integração local e limpeza segura. Não peça ao usuário escolha de IDs de review, criação manual de worktree ou confirmação para avançar fases. O planejamento termina antes desta chamada; leia o manifesto pronto, não replique tech-lead/worktree-planner.

Leia [configuração por projeto](../_shared/perfil-projeto.md), [execução portátil](../_shared/execucao-portavel.md), [perfis](../_shared/perfis-de-risco.md), [contexto e automação](../_shared/contexto-e-automacao.md), regras locais aplicáveis, manifesto e estados. Consulte [estado e gates](references/estado-e-gates.md) ao transicionar e [integração e limpeza](references/integracao-e-limpeza.md) nessas fases. Após compactação, releia regras locais, esta skill e estado; referências conforme a próxima ação. Não carregue todas as skills dos executores na sessão coordenadora.

## Coordenação

Use sessões independentes para implementação, review e os gates de auditoria/QA exigidos pelo perfil. Delegação está autorizada neste fluxo. Prefira contexto novo com pacote mínimo por papel, sem histórico completo. Não aprove autorrevisão; indisponibilidade de executor independente para gate exigido é bloqueio registrado. Subagentes devolvem FLUXO_EVENTO compacto, caminhos de relatórios e hashes; só o coordenador atualiza manifesto, estados e índice diário. Use event/render da ferramenta Contexto quando configurada, com revisão esperada e ID idempotente; não mantenha duas fontes de estado. Um relato sem evidência não satisfaz gate.

Trabalhe por dependências: independentes podem avançar em paralelo quando houver recursos, dependentes esperam origem aprovada. Um bloqueio real isola a tarefa e suas dependentes; as demais seguem. Nunca peça decisões de negócio no meio do lote: registre a lacuna no pacote final. Ausência de credencial/permissão, teste essencial indisponível ou risco destrutivo não autoriza contornar proteção. Se todas estiverem impedidas, encerre COM_BLOQUEIOS, sem apresentar o lote como concluído com sucesso.

Limites: nunca escrita em main/master, push ou PR; nunca dados/.env de produção; nunca dependência nova silenciosa nem alterações alheias; nunca force, reset, rebase destrutivo ou exclusão de branches. Verificações que toquem banco seguem as regras locais de isolamento (Intranet: CLAUDE.md §2); sem prova de isolamento, não execute e não marque PASS.

## Ciclo por tarefa e camada

1. **Criação:** execute o plano de worktrees, já nas branches finais, verificando base/SHA, estado local e topologia. Prepare automaticamente o Contexto conforme [worktrees automáticas](../_shared/worktrees-automaticas.md), inclusive em reutilização e worktrees de integração. Exija recibo `prepared: true` antes de delegar; não transfira init/configuração ao usuário. Durante o lote, não troque branch do checkout principal do usuário; a única troca é a entrega final da branch de revisão. Registre paths e recibo no estado.
2. **Implementação:** forneça o prompt “## 3. Prompt para o executor (Claude, Antigravity ou Codex)” do 01/02 e o caminho absoluto. Para plano legado, aceite “## 3. Prompt para o Claude CLI”, substituindo apenas o contrato operacional obsoleto pelas regras atuais e registrando a migração. Use implementador-de-ticket e fechar-entrega. Exija commit local, registro e validações reais; acrescente o índice diário de modo idempotente.
3. **Review:** revisor-de-codigo em sessão independente, cobertura completa uma vez por escopo fixado. Suas especialidades de correção/performance, qualidade e segurança não são gates repetidos adicionais.
4. **Auditoria:** auditor-de-review em outra sessão quando houver achados ou perfil critico, contra relatório, código e negócio. Todo achado recebe APLICAR/ADIAR/REJEITAR fundamentado; incerteza essencial gera AUDITORIA_BLOQUEADA e isolamento. Sem achados e cobertura completa em simples/padrao, registre NA_SEM_ACHADOS com relatório/SHA, sem nova sessão; limitações essenciais bloqueiam.
5. **Correções:** review-loop-driver em “Aplicação por decisão do auditor” delega somente APLICAR ao especialista da camada. Commit por rodada/unidade lógica, sem amend de evidência anterior. Auditor não implementa.
6. **Revalidação:** revisor-de-codigo focal nos IDs, commits e impacto; AINDA PRESENTE/REGRESSÃO retorna ao auditor. No máximo três rodadas de correção por tarefa, incluindo revisão final. Persistindo bloqueio, isole. Não reinicie o contador ao mudar de fase ou de camada.
7. **QA:** revisor-de-qa independente nos perfis padrao/critico e em simples quando critérios não foram demonstrados pelo revisor. Em simples, COBERTO_NO_REVIEW exige evidência independente para todos os critérios; nunca dispense teste necessário por orçamento. FAIL no escopo vira correção pelo implementador, commit e revalidação, até três rodadas. BLOCKED essencial isola. Correção exige revalidação técnica focal e auditoria de novos achados.
8. **Documentos:** commite relatórios exigidos pelo perfil e registro, adicionados explicitamente na branch da tarefa. Um commit documental por rodada; documentos sem efeito executável não invalidam testes. Gere cabeçalhos, inventários e projeções com scripts; não peça à IA para copiar diffs ou estados. Evidências preservam snapshot de código e hashes originais.
9. **Prontidão conjunta:** tarefa que cruza camadas só fica PRONTA_PARA_INTEGRAR se ambas satisfizerem os gates e o contrato de integração. Não integre metade de feature bloqueada. Dependentes só avançam com a origem aprovada.

## Fechamento do lote

Integre as tarefas prontas conforme a referência de integração, depois execute verificações pós-merge, review de interação entre tarefas, auditoria dos achados e QA dos fluxos combinados afetados. Correções retornam à branch de tarefa responsável, seguidas de revalidação, commit e reintegração; nunca “corrija direto” em main ou esconda uma falha na branch de revisão.

Só publique no manifesto uma branch de revisão como aprovada após todos os seus gates finais. Se um componente falhar, reconstrua um candidato novo sem ele nem suas dependentes, preservando branches/histórico existentes; não deixe o manifesto apontando para snapshot reprovado como aprovado.

Teste manual e verificação de telas são no checkout principal, nunca em worktree: depois de commitar os documentos finais, entregue a branch de revisão aprovada no checkout principal de cada repositório, conforme a referência de integração e o perfil do projeto (só com o checkout limpo; senão, comandos no pacote). Grave o pacote preliminar de revisão, faça a limpeza segura e finalize o pacote com inventário real das worktrees removidas/mantidas. Commit dos documentos finais no repositório da camada antes de remover a worktree de integração e trocar o checkout principal. O pacote central aponta para esses commits e branches, resultados de gates, decisões ADIAR/REJEITAR, limitações, tarefas isoladas, roteiro de telas/diffs e sugestões de PR.

Status final: PRONTO_PARA_REVISAO_HUMANA somente sem tarefas/limpeza obrigatória bloqueadas; PARCIAL_COM_BLOQUEIOS se houver entregas aprovadas e itens isolados; BLOQUEADO se nada pôde ser entregue. Sem simular sucesso. Informe branch/SHA por repositório, se cada checkout principal ficou na branch de revisão e o caminho do pacote. O usuário revisa telas no checkout principal e diffs, faz push e abre PRs.

Publicação no ClickUp não faz parte implícita desta execução. Depois, só publique se houver pedido explícito ou autorização válida de fluxo específico; sem isso entregue o resumo pronto. Não invente publicador-clickup como ferramenta/skill instalada.
