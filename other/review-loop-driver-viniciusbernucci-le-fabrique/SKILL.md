---
name: review-loop-driver
description: Consolida relatórios do gate revisor-de-codigo ou de auditorias em uma fila priorizada, prepara um roteiro por item e aplica e commita somente os itens que o usuário indicar, um a um ou em lote. Use para processar reviews, aplicar correções indicadas ("aplica REVIEW-003", "aplica todos os ALTO") e acompanhar a fila; não aplica nada sem indicação, não revisa novamente e não aprova QA.
---

# Condutor do loop de correções

Leia os relatórios indicados, ticket, escopo da worktree e decisões do usuário. Aceite `code-review-*`, `security-review-*`, `clean-code-*`, o legado `clean-code-review-*` e relatórios de auditoria. Não misture revisões históricas ou de outras branches só porque estão na mesma pasta.

## Fila

Grave `docs/historico/reviews/fila-<assunto>-<data>.md` no repositório revisado. Registre base/HEAD ou estado local de origem e tabela: ID, severidade, origem+ID original, local, problema, bloqueia, status e evidência. Preserve IDs ao atualizar; una apenas achados com a mesma causa raiz e correção, conservando todas as origens.

Ordene CRÍTICO → ALTO → MÉDIO → BAIXO; empate por dependências, segurança, correção e manutenção. `BLOCKER` é bloqueante; `NIT` é opcional; `Critical/High/Medium/Low` correspondem aos nomes em português. `needs-validation` fica em investigação, sem promover a achado confirmado.

CRÍTICO e ALTO bloqueiam por padrão; demais itens seguem aceite e política local. Não promova toda segurança a CRÍTICO. Preserve a regra documentada de N requisições batch da Intranet apenas quando esse perfil se aplicar. Separe severidade de decisão de bloqueio.

Fora do escopo vira sugestão de nova tarefa, sem autorizar expansão. Um risco bloqueante não deixa de bloquear só por estar fora do escopo: registre a decisão necessária. Não publique tarefas externas automaticamente.

## Roteiro por item

Use caminhos reais da worktree e branch confirmados, nunca caminhos Windows herdados do exemplo. O prompt contém:

- Âncora: repositório, worktree, branch, base/HEAD e leituras externas necessárias.
- ID da correção e origem; cenário, evidência e plano do relatório.
- Escopo autorizado e arquivos relacionados; verificar se o código ainda corresponde ao achado.
- Correção mínima e teste de regressão apropriado; sem refatorações extras.
- Quem aplica: o usuário, ou o agente somente quando o usuário indicar o ID (ver "Aplicação sob indicação"). Nunca push nem merge.
- Evidência de conclusão: diff, verificações executadas/resultados, riscos e limitações.

Gere um item por vez, agrupando somente a mesma causa raiz já consolidada. O pedido de montar fila não autoriza implementar. No fluxo Intranet/ORCA, finalize em `AGUARDANDO_CORRECOES_REVIEW`, mostrando a ordem, os IDs e o roteiro, e diga que o usuário pode aplicar à mão ou indicar os IDs para o agente aplicar, um a um ou em lote.

## Aplicação sob indicação do usuário

Nada é aplicado automaticamente. Montar a fila, gerar roteiro ou terminar a revisão **não** autoriza editar código. O agente só aplica o que o usuário indicar explicitamente naquela mensagem:

- Um item: "aplica REVIEW-003".
- Lote: "aplica REVIEW-001, REVIEW-004 e REVIEW-007", "aplica todos os ALTO", "aplica a fila toda". Um filtro ou "toda" vale só para os itens pendentes que ele cobre no momento da indicação.
- Sem ID ou filtro claro ("pode corrigir", "resolve aí"), pergunte quais IDs. Indicação de uma mensagem não se estende à próxima.

Para cada indicação:

1. Confirme worktree, branch da tarefa (nunca `main`/`master`) e `git status`. Alteração alheia na árvore fica fora e é avisada.
2. Para cada ID indicado, verifique se o código ainda corresponde ao achado. Se não corresponder, não altere: marque `adiado` com o motivo e siga para o próximo.
3. Aplique a correção mínima do plano do relatório e o teste de regressão previsto. Sem refatoração extra e sem tocar item não indicado, mesmo que seja trivial ou esteja no mesmo arquivo; se a correção de um ID exigir mexer em outro, pare e pergunte.
4. Rode as verificações da camada (testes e build do ticket). Falha que você não consiga resolver no escopo do ID: pare, mostre a saída e não commite.
5. Commit na branch da tarefa: um commit por lote indicado, ou um por item se o usuário pedir. Adicione os arquivos um a um. Mensagem de uma linha, `fix: {o que mudou}`, sem ID do ClickUp e sem co-autoria. Nunca `--amend` sobre o commit de entrega já indexado. Nunca push.
6. Depois do commit, atualize a fila: IDs aplicados → `aplicado/aguarda verificação`, com o hash; não commite a fila (ela entra no próximo commit documental do orquestrador).
7. No chat: IDs aplicados, IDs adiados e o motivo, hash, verificações e resultado, itens pendentes restantes. **PARE** e aguarde a próxima indicação.

Este procedimento substitui `fechar-entrega` para commits de correção de review: não crie registro de entrega novo nem linha nova no índice diário. A revalidação dos IDs aplicados é feita depois pelo `revisor-de-codigo`, em modo revalidação, quando o usuário disser que terminou as correções; uma revalidação na mesma sessão que aplicou é autorrevisão e deve ser declarada como tal.

## Acompanhamento

Estados: pendente, em andamento, aplicado/aguarda verificação, verificado, adiado ou nova tarefa. Relato de aplicação não equivale a verificação. Atualize com a resposta ou evidência disponível; não invente execução nem marque testes não executados como passando.

Quando o usuário informar os hashes das correções, atualize os itens para `aplicado/aguarda verificação` e devolva o controle ao orquestrador. Quando não houver correção obrigatória pendente, informe “fila concluída; pronta para revalidação” e liste gates pendentes. Não declare entrega aprovada ou liberada para merge. Correções invalidam evidências afetadas: o orquestrador aciona revalidação focal, sem repetir toda revisão se o escopo não justificar. Atualize checklist semanal apenas se ele existir e pertencer ao pedido.

Fora da "Aplicação sob indicação do usuário", não altere código e não execute Git de escrita. Nunca publique mensagens externas nem inicie um ciclo infinito de melhorias. Novos problemas fora da entrega seguem para backlog.
