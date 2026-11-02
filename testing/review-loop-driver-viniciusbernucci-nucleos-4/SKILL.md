---
name: review-loop-driver
description: Consolida a fila de review e coordena correções por decisão do auditor no lote ou por indicação do usuário fora dele. Use para aplicar achados autorizados e registrar commits; não refaz review nem aprova QA.
---

# Condutor das correções

Resolva uma vez por projeto a [configuração local](../_shared/perfil-projeto.md). Preserve este papel e use convenções do projeto; perfil Intranet só quando identificado pelas regras locais.

Leia relatório, auditoria, ticket, critérios, branch e estado atual. No lote, leia [execução portátil](../_shared/execucao-portavel.md). Montar fila por si só não autoriza implementar fora do lote.

## Fila rastreável

Grave docs/historico/reviews/fila-{assunto}-{data}.md na camada revisada. Chave por item: tarefa + repositório + relatório + ID original. Preserve IDs e origens ao consolidar causas compartilhadas. Registre base/HEAD de origem, severidade, bloqueio, decisão, justificativa, dependências, executor, status, commit e evidência de verificação. Ordene por dependência e severidade. Suspeita não confirmada fica em investigação.

## Aplicação por decisão do auditor

A chamada do orquestrador autoriza executar o lote; não peça ao usuário seleção de IDs. Aplique somente APLICAR da auditoria correspondente ao relatório e ao código atual. ADIAR e REJEITAR ficam documentados, sem editar código por esses itens. Auditoria bloqueada isola a tarefa.

1. Confirme worktree, branch da tarefa, base/HEAD e git status. Nunca main/master. Preserve alterações alheias, inclusive staged; não faça unstage nem commit de material desconhecido.
2. Gere prompt ao especialista da camada (implementador-de-ticket) com IDs, evidências, regra de negócio, plano mínimo, arquivos e teste esperado. Delegue em sessão de implementação; não implemente no papel de auditor/revisor. Dependência nova ou necessidade de mudar regra retorna ao auditor, sem expansão silenciosa de escopo.
3. Se o código mudou e invalida o achado, devolva ao auditor com o diff; não aplique plano obsoleto nem marque verificado por relato.
4. Execute as verificações pertinentes e permitidas. Verificações essenciais indisponíveis resultam em BLOCKED, nunca em aprovação inventada. Falha dentro do escopo é corrigida; persistência após três ciclos isola a tarefa.
5. Commit fix: em português, por unidade lógica/rodada, com caminhos explícitos, sem push/co-autoria. Não faça amend de commits já usados como evidência ou indexados. Atualize o registro existente da tarefa com uma seção de correções e os IDs; não gere nova entrega nem nova linha no índice diário por ID.
6. Atualize a fila para aplicado/aguarda verificação com hash real. Devolva automaticamente ao orquestrador para revisor-de-codigo em revalidação focal. Só o revisor independente marca VERIFICADO; AINDA PRESENTE, REGRESSÃO ou BLOQUEADO retornam ao auditor.

Relatórios/fila ainda não commitados entram no commit documental do orquestrador. Não faça merge por esta skill.

## Aplicação sob indicação do usuário — fora do lote

Revisão avulsa termina no relatório. Se o usuário pedir “aplica REVIEW-003”, um filtro de severidade ou a fila toda, aplique somente esse conjunto pendente, conferindo origem e escopo. Se o pedido for ambíguo, esclareça os IDs; não exija IDs quando o pedido já abrange claramente toda a fila. Pode executar diretamente o papel de implementador após encerrar o papel de revisão, declarando que a verificação independente continua pendente. Use as mesmas verificações, commit e registro descritos acima. Entregue hashes, IDs e pendências; não inicie o lote inteiro sem pedido.

Estados: pendente, em andamento, aplicado/aguarda verificação, verificado, adiado, rejeitado, bloqueado. Preserve relatório original e justificativas; não declare entrega aprovada sem review, auditoria e QA exigidos. Nunca publicação externa automática.
