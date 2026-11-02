---
name: worktree-planner
description: Planeja isolamento de tickets em worktrees, contratos entre frentes, sequência de integração e prompts de execução. Use quando solicitado planejamento com worktrees ou no fluxo Intranet/Orca; não substitui o backlog do Tech Lead nem intercepta toda solicitação de implementação.
---

# Planejador de worktrees

Resolva uma vez por projeto a [configuração local](../_shared/perfil-projeto.md). Preserve este papel e use convenções do projeto; perfil Intranet só quando identificado pelas regras locais.

Prepare um plano operacional a partir de uma tarefa já definida. Não implemente nem execute Git de escrita; gere arquivos e comandos revisáveis. Leia o ticket, critérios de aceite, dependências, regras locais e topologia real dos repositórios.

No fluxo Intranet, aplique [perfis](../_shared/perfis-de-risco.md) e [contexto econômico](../_shared/contexto-e-automacao.md): especificação única, prompts por referência e artefatos proporcionais. Não copie contratos/regras já acessíveis ao executor.

## Perfil

- IntranetNova/docker-intranet com Orca e ClickUp: leia [perfil Intranet](references/intranet.md). Ele preserva os contratos de branches, registro, review pós-commit e índice diário. Confirme a topologia antes de usar seus caminhos.
- Outros projetos: descubra repositório(s), base, nomes e diretório de worktrees pela configuração local e pedido. Não importe limites de duas worktrees, caminhos Windows, SQL Server, ClickUp ou políticas de commit da Intranet.

## Plano portátil

1. Reutilize a especificação do Tech Lead quando existir; não rediscuta critérios já aprovados. Resolva lacunas que impedem um aceite observável. Sem critérios essenciais, registre o bloqueio e não gere um prompt executável incompleto.
2. Separe frentes apenas quando houver independência real. Identifique colisões de arquivos, símbolos compartilhados, contrato de API e ordem de integração. Trabalho dependente pode exigir sequência ou branch base diferente, não paralelismo fictício.
3. Registre caminhos reais, branch base e identificação do ponto inicial, branch da tarefa, arquivos esperados, limites de leitura/escrita, critérios de aceite, validação e handoff. Não gere comandos com placeholders pendentes.
4. Produza plano geral, um prompt por frente e o estado persistente consumido pelo `orquestrador-fluxo-ia`, no padrão documental do projeto. Sem padrão, use `documentacoes/planejamento/worktrees/`. Nomeie sem sobrescrever planos anteriores.
5. Inclua nos prompts somente instruções indisponíveis por referência. Confirme caminhos absolutos das skills e especificação; o executor lê esses arquivos sem depender de descoberta nativa. Transcreva contrato somente quando o acesso ao original não existir, registrando a razão. Não copie o texto e mande reler o original.
6. Descreva criação, integração e limpeza, com verificação de branch, estado local e trabalho ainda não integrado antes de qualquer remoção. A execução depende do pedido; gerar o plano não autoriza merge, push ou exclusão.
7. Inclua no prompt a preparação automática pelo criador/executor conforme [worktrees automáticas](../_shared/worktrees-automaticas.md): helper real, raiz da worktree e origem de configuração confirmada. O usuário não executa init. Planejamento apenas descreve; execução prepara e registra recibo antes de delegar.

Não embuta revisão técnica nos prompts de implementação. O gate oficial posterior é `revisor-de-codigo`, acionado pelo orquestrador depois dos commits das worktrees. Não confunda commit local com aprovação.

No fluxo do planejador-de-lote, devolva os arquivos ao coordenador para consolidar o manifesto e terminar o planejamento. Não inicie orquestrador-fluxo-ia sem pedido de execução já existente.

Saída: frentes/worktrees, dependências, ordem de integração, caminhos dos planos, arquivo de estado e bloqueios concretos.
