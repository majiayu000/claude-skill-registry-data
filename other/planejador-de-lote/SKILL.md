---
name: planejador-de-lote
description: Coordena grill-me → tech-lead → worktree-planner para transformar uma ou mais demandas em lote executável. Use para iniciar ou revisar o planejamento do fluxo Intranet; não executa implementação nem dispara o orquestrador sem pedido.
---

# Planejador de lote

Entrada do planejamento para Claude, Antigravity e Codex. Leia [configuração por projeto](../_shared/perfil-projeto.md), regras locais e [execução portátil](../_shared/execucao-portavel.md). Carregar uma skill significa ler seu SKILL.md e seguir suas instruções com as ferramentas disponíveis; não depende de um comando exclusivo de um cliente.

Leia [perfis de risco](../_shared/perfis-de-risco.md) e [contexto e automação](../_shared/contexto-e-automacao.md). Classifique cada tarefa como simples/padrao/critico e registre justificativa, critérios e gates aplicáveis. Preserve controles de banco/Git em todos os perfis. Não use o tamanho do diff como classificação de risco.

## Encadeamento

1. Identifique as demandas selecionadas pelo usuário, com IDs/links quando existirem. Consulte fontes conectadas e o código antes de perguntar. ClickUp é opcional; sem vínculo, gere uma chave local estável e registre “não possui ID vinculado”, sem inventar ticket externo.
2. Carregue **grill-me** para esclarecer objetivo, comportamento atual, regras de negócio, bordas e fora do escopo do lote. Pergunte o que só o usuário pode decidir. Reutilize respostas e fatos documentados entre demandas; registre hipóteses e questões em aberto. Não confunda falta de requisito com permissão para inventá-lo.
3. Assim que a entrevista permitir critérios observáveis, carregue **tech-lead** automaticamente com todas as respostas. Ele produz tickets e dependências, sem iniciar implementação. Questões essenciais não resolvidas deixam a tarefa BLOQUEADA_NO_PLANEJAMENTO; continue as demais.
4. Ao concluir os tickets, carregue **worktree-planner** automaticamente para preparar cada feature. Ele usa a especificação já produzida, sem repetir a entrevista, e grava planos, prompts e estados. Não peça ao usuário para invocar essas etapas.
5. Consolide o manifesto na pasta de planos configurada, com data/fuso do projeto (Intranet: `{FONTE_CLAUDE}/worktrees/AAAA-MM-DD/lote-AAAA-MM-DD-{slug}.md` e America/Sao_Paulo). Use slug estável do lote; em colisão, reutilize só se for retomada do mesmo lote, senão acrescente sufixo. Nunca sobrescreva outro lote do dia.

Manifesto: identificador do lote; data/fuso; demandas incluídas/excluídas; referências de especificações/estados; por tarefa: chave, ID externo opcional, camadas, perfil/justificativa, IDs de critérios, dependências e status; grafo sem ciclos; ordem de execução/integração; base ref + SHA por repositório; branch de revisão por grupo; recursos necessários e riscos. Não copie critérios completos já especificados. Use o prefixo de revisão configurado (default revisao/AAAA-MM-DD-{slug}), com sufixos -2, -3 apenas para grupos incompatíveis. Todos os planos referenciam este mesmo manifesto.

## Conclusão

Marque PRONTA_PARA_ORQUESTRAR somente a tarefa com critérios essenciais, contratos, planos e validação viável definidos. Não marque especificação como aprovada pelo usuário se apenas foi inferida: registre a origem de cada decisão. Distingua prontidão técnica de autorização para executar.

Entregue caminhos e um resumo do lote, pendências e a instrução “execute orquestrador-fluxo-ia com este manifesto”. **Planejar não inicia execução.** Se o usuário já pediu explicitamente planejar e executar, carregue o orquestrador ao concluir, sem confirmação adicional. Fora disso, encerre no plano pronto; a próxima chamada do orquestrador autoriza criar worktrees, implementar, corrigir por auditoria, commitar, integrar e limpar o lote. Nunca push/PR nem publicação externa implícita.
