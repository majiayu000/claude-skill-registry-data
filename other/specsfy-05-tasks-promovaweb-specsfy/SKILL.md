---
name: specsfy-05-tasks
description: "Use quando o usuário quer quebrar ou decompor a especificação em tarefas, preencher ou atualizar a seção `14. Tarefas` de `spec.md`, ordenar dependências, planejar fatias verticais ou preparar a execução. Use também quando uma transição automática pedir planejamento, replanejamento ou retomada após RED. Use somente para editar o backlog dentro da fonte única; não crie tasks.md, não escreva código nem marque trabalho como concluído."
---

# Quebrar a especificação em tarefas

Preencha a seção `14. Tarefas` de `specs/specs/<NNNN>-<slug>/spec.md`. O arquivo permanece a única fonte da verdade; cada tarefa precisa ser pequena, verificável, ordenada e ligada a IDs definidos nele.

## Orquestrar a conversa

Ao concluir esta etapa ou detectar trabalho de outra etapa, anuncie
`Pendência detectada: <descrição> — ação: resolvendo nesta etapa` e resolva-a
quando pertencer ao próprio escopo. Quando houver troca de responsabilidade,
anuncie `Transição automática: $specsfy-05-tasks → $<destino> — motivo:
<motivo> — resultado esperado: <resultado>` e carregue imediatamente a skill de
destino, sem pedir confirmação nem repetir o comando. Continue na mesma
conversa. Depois de uma correção necessária a esta etapa, anuncie `Retomada
automática: $<destino> → $specsfy-05-tasks — pendência resolvida:
<resultado>` e retome-a imediatamente. Reavalie o estado após cada handoff para
evitar ciclos. Não peça confirmação para o handoff; ações sensíveis continuam
exigindo autorização específica.

## Pré-condições

1. Leia a spec indicada em `specs/specs/<NNNN>-<slug>/spec.md` e exija
   `Formato: Specsfy/2.0`, `Definition Gate: Passed` e `Status` `Defined`,
   `Planned` ou `Implementing`. Aceite os dois últimos somente para
   replanejamento automático de uma pendência detectada em etapa posterior.
2. Execute a validação da especificação quando o gate ainda não estiver comprovado.
3. Inspecione o repositório para usar stack, comandos e caminhos reais. Em PHP,
   use Pest para TDD; em Node sem PHP, pergunte qual runner adotar e recomende
   Vitest antes de gerar caminhos ou comandos.
4. Execute o monitor antes de planejar:

```bash
python3 -B .agents/skills/specsfy-setup/scripts/monitor_context.py \
  --project .
```

   Use os sinais de stack, aplicação, regras e persistência para planejar a
   documentação junto da mudança, sem inferir requisito novo.
5. Se faltar uma decisão que mude arquitetura, dados ou aceite, anuncie e
   retorne automaticamente para `$specsfy-02-backlog`. Depois da decisão,
   use `$specsfy-update-spec` quando a spec já tiver sido aprovada ou
   `$specsfy-03-specify` durante a definição inicial.

## Gerar

Use `.specsfy/templates/custom/Tasks.md` como contrato quando existir e recorra
a `.specsfy/templates/Tasks.md` caso contrário. Substitua somente o conteúdo
das seções `14. Tarefas` e `15. Ordem de execução` em
`<raiz>/specs/specs/<NNNN>-<slug>/spec.md`; preserve todas as outras seções.

- Se a spec estiver `Planned` ou `Implementing`, anuncie a pendência, reabra o
  Ato II e defina `Status: Defined`, `Plan Gate: Pending` e
  `Delivery Gate: Pending` antes de editar. Gate e evidência posteriores não
  permanecem válidos sobre o plano alterado.
- Em uma spec já `Defined`, defina `Plan Gate: Pending` e
  `Delivery Gate: Pending` antes de editar.
- Preserve IDs existentes ao atualizar; não renumere tarefas concluídas.
- Organize em setup mínimo, fundação indispensável, histórias em prioridade e fechamento.
- Mantenha histórias como fatias verticais independentemente demonstráveis.
- Para cada `AC`, crie uma tarefa `[TEST] [TDD]` distinta cujo desenho usa o
  Gherkin mantido na spec como referência. O conjunto dessas tarefas materializa pelo
  menos três casos TDD distintos para a feature inteira e para cada `US`, `FR`
  e `NFR`.
- Nunca crie tarefa para arquivo `.feature` ou step definition e nunca execute
  o Gherkin da spec.
- Em PHP, a tarefa TDD aponta para teste Pest e exige marcador `SPECSFY`; em
  Node, usa o runner confirmado pelo usuário e o script `test:tdd`.
- Faça cada tarefa `[CODE]` depender do predecessor TDD da mesma fatia com RED.
- Quando a fatia alterar manifests ou configuração estrutural, crie uma tarefa
  `[DOC]` para `.specsfy/STACK.md`. Quando alterar banco, schema, model
  persistente, tabela, campo, relação ou migration, crie uma tarefa `[DOC]`
  obrigatória para `.specsfy/DATABASE.md`.
- Para mudança de aplicação, inclua a revisão de `PROJECT.md` no fechamento da
  tarefa. Se não houver impacto material, exija justificativa na evidência em
  vez de criar conteúdo artificial.
- Faça toda tarefa `[CODE]` exigir a reconstrução independente de `docs/` por
  `$specsfy-documentator` antes de `EXECUTE`, inclusive quando a documentação
  já existia antes da mudança.
- Quando uma convenção virar regra confirmada, crie tarefa `[DOC]` para
  `.specsfy/RULES.md`.
- Dê a cada tarefa um resultado único, caminho exato e critério verificável.
- Anexe a cada tarefa, exatamente nesta ordem, os itens `PREP`, `EXECUTE`,
  `VERIFY`, `EVIDENCE` e `IMPROVE` definidos no template `Tasks.md` resolvido.
- Escreva os itens como resultados específicos da tarefa, não como frases genéricas copiadas.
- Mantenha pai e itens abertos ao gerar tarefas; a skill de implementação atualiza um item imediatamente após sua evidência.
- O item `IMPROVE` deve registrar uma melhoria concreta aplicada ou declarar que nenhuma foi necessária com justificativa.
- Quando a spec declarar `Evidence Contract: 1`, cada tarefa `[CODE]` concluída
  deve conter um comentário `specsfy:evidence` JSON com `task`, `refs`, `files`
  e `commands` (`run` e `exit`). Gere o comentário dentro do bloco da tarefa;
  nunca em arquivo paralelo.
- Marque `[P]` somente quando tarefas não compartilham arquivos, estado mutável ou dependência.
- Declare dependências por ID; não dependa apenas da ordem visual.
- Cubra todo `FR`, `NFR` e `AC` aplicável. Não crie tarefa sem referência, exceto setup/polish claramente justificado.
- Não inclua exemplos genéricos nem placeholders.

Formato canônico:

```markdown
- [ ] T001 [TEST] [TDD] [US-001] Derivar teste Pest do BDD da spec em tests/Feature/AuthTest.php — Refs: FR-002, AC-003 — Depends: none
- [ ] T002 [CODE] [US-001] Implementar validação em app/Services/AuthService.php — Refs: FR-002, AC-003 — Depends: T001
```

Tags permitidas após o ID: `[P]`, `[TEST]`, `[TDD]`, `[CODE]`,
`[DOC]`, `[OPS]` e `[US-NNN]`.

## Validar

Execute:

```bash
python3 .agents/skills/specsfy-05-tasks/scripts/validate_tasks.py specs/specs/<NNNN>-<slug>/spec.md --allow-draft
```

Corrija IDs duplicados, dependências inválidas/cíclicas, referências inexistentes,
itens sem três cenários BDD, AC sem tarefa TDD distinta, plano sem três
predecessores/casos TDD por
feature/`US`/`FR`/`NFR`, código sem predecessor TDD,
checklist ausente/fora de ordem, pai/itens
incoerentes, progresso em tarefa bloqueada ou tarefas vagas. Faça no máximo
três ciclos.
No contrato de evidência, o mesmo validador também rejeita arquivo ausente,
referência inválida, comando sem `exit: 0` ou tarefa concluída sem evidence.

Quando a estrutura passar ainda com `Plan Gate: Pending`, chame automaticamente
`$specsfy-06-tdd-bdd` no modo `prepare`. Ele usa o BDD da spec para
materializar o predecessor TDD, observa RED e conclui somente essa tarefa de
teste. Em seguida, retome automaticamente esta skill para:

1. execute novamente o validador com `--allow-draft`;
2. altere `Plan Gate` para `Passed` e defina `Status: Planned`;
3. registre o resultado em `Gate do Ato II — Plano`;
4. execute sem `--allow-draft`.

O modo estrito rejeita `Plan Gate: Passed` quando algum predecessor TDD
de uma tarefa `[CODE]` continua aberto. Se a validação falhar, mantenha
`Status: Defined`, `Plan Gate: Failed`, `Delivery Gate: Pending` e relate os
bloqueios.

## Relatar

Informe contagem total/por tipo, caminho crítico, oportunidades `[P]`, cobertura
de IDs e, quando o gate passar, anuncie e carregue automaticamente
`$specsfy-07-implement`. Nunca crie `tasks.md`.

## Especialistas sob demanda

Leia [references/specialists.md](references/specialists.md) ao decompor trabalho
de tecnologia, dados, interface ou operação que demande checklist próprio.
