---
name: specsfy-07-implement
description: "Use quando o usuário pede para implementar, executar ou concluir tarefas da seção `14. Tarefas` de `specs/{id}-{slug}/spec.md`, criar o código definido pela fonte única, continuar a próxima tarefa pronta ou finalizar a feature. Use também quando uma transição automática iniciar ou retomar a entrega. Use para produção; para apenas criar testes use specsfy-06-tdd-bdd, e para apenas decompor use specsfy-05-tasks."
---

# Implementar as tarefas e criar o código

Execute a seção `14. Tarefas` de `spec.md` em ordem de dependência, mantendo a fonte única, testes, código, evidências e checkboxes coerentes.

## Orquestrar a conversa

Ao concluir esta etapa ou detectar trabalho de outra etapa, anuncie
`Pendência detectada: <descrição> — ação: resolvendo nesta etapa` e resolva-a
quando pertencer ao próprio escopo. Quando houver troca de responsabilidade,
anuncie `Transição automática: $specsfy-07-implement → $<destino> — motivo:
<motivo> — resultado esperado: <resultado>` e carregue imediatamente a skill de
destino, sem pedir confirmação nem repetir o comando. Continue na mesma
conversa. Depois de uma correção necessária a esta etapa, anuncie `Retomada
automática: $<destino> → $specsfy-07-implement — pendência resolvida:
<resultado>` e retome-a imediatamente. Reavalie o estado após cada handoff para
evitar ciclos. Não peça confirmação para o handoff; ações sensíveis continuam
exigindo autorização específica.

## Gate inicial

1. Leia `specs/specs/<NNNN>-<slug>/spec.md`, evidências indexadas em `specs/specs/<NNNN>-<slug>/research/`, instruções do repositório e código relevante. Não procure `tasks.md`, `plan.md`, `research.md` ou `data-model.md`.
2. Exija `Formato: Specsfy/2.0`, `Status: Planned` ou `Implementing`,
   `Definition Gate: Passed` e `Plan Gate: Passed`.
3. Execute os validadores contra `specs/specs/<NNNN>-<slug>/spec.md`. Se um gate
   falhar por tarefa, predecessor TDD ou RED ausente em um plano antes aprovado,
   anuncie a pendência e retorne automaticamente para
   `$specsfy-05-tasks`; não altere produção. Essa skill reabre o Ato II, chama
   TDD/BDD e retoma esta implementação depois de validar novamente o plano. Para
   outra falha, carregue automaticamente a skill responsável pelo gate.
4. Execute a suite base relevante. Registre falhas preexistentes e não as atribua à nova mudança.
5. Antes da primeira alteração de produção, defina `Status: Implementing` e
   `Delivery Gate: In Progress`.
6. Selecione trabalho pronto com:

```bash
python3 .agents/skills/specsfy-07-implement/scripts/next_task.py specs/specs/<NNNN>-<slug>/spec.md
```

Se não houver tarefa pronta, diferencie `concluído` de `bloqueado por dependência`.

## Executar uma tarefa

1. Confirme ID, tipo, referências, dependências, arquivos e resultado verificável; marque `PREP` imediatamente após essa confirmação.
2. Para `[TEST]`, siga `$specsfy-06-tdd-bdd`: leia o Gherkin de referência na
   spec e use-o para desenhar o teste TDD; adicione marcadores e observe RED
   válido. Nunca crie ou execute `.feature`. Em PHP, use Pest; em Node, use
   somente o runner confirmado pelo usuário.
3. Para `[CODE]`, confirme o predecessor TDD concluído cobrindo os mesmos IDs,
   com RED registrado na seção 11. Sem isso, pare e não altere produção.
   Anuncie a pendência e retorne automaticamente para
   `$specsfy-05-tasks`, que reabre o plano, chama `$specsfy-06-tdd-bdd` e
   retoma esta skill depois do novo `Plan Gate: Passed`.
4. Escreva a menor mudança de produção que torna o teste TDD verde.
5. Depois de alterar produção e antes de marcar `EXECUTE`, monitore o contexto:

```bash
python3 -B .agents/skills/specsfy-setup/scripts/monitor_context.py \
  --project . --check
```

   Para stack pendente, faça handoff a `$specsfy-aux-stack`; para persistência,
   a `$specsfy-aux-database`; para regra confirmada, a
   `$specsfy-aux-rules`. Revise `PROJECT.md` em toda mudança de aplicação. Se
   não houver impacto material na história, finalidade, capacidades ou limites,
   registre a avaliação na evidência da tarefa e repita com
   `--acknowledge-project-no-change`. Não marque a tarefa enquanto o monitor
   retornar `PENDING`.
6. Depois de cada tarefa `[CODE]`, anuncie
   `Transição automática: $specsfy-07-implement → $specsfy-documentator —
   motivo: implementação alterou o sistema — resultado esperado: docs/
   reconstruído e atual` e carregue `$specsfy-documentator`. Reconstrua a
   documentação a partir de todo o código existente, execute seu `--check` e
   retome esta skill somente quando a documentação estiver atual.
7. Para `[DOC]` ou `[OPS]`, produza a evidência específica pedida.
8. Marque `EXECUTE` somente quando a entrega e a documentação exigida existirem
   nos caminhos declarados.
9. Execute o teste TDD focal, a suite relacionada e checks estáticos;
   marque `VERIFY` somente com o resultado esperado.
10. Refatore somente com tudo verde.
11. Registre comando, resultado e IDs nas seções 11–13 e então marque `EVIDENCE`.
   Quando houver `Evidence Contract: 1`, grave também o comentário JSON
   `specsfy:evidence` no bloco da tarefa e execute:

```bash
python3 -B .agents/skills/specsfy-07-implement/scripts/verify_evidence.py \
  specs/specs/<NNNN>-<slug>/spec.md . --task TNNN
```

Quando uma execução completa produzir atestação schema 2, verifique novamente
com `--attestation PATH`. Exija commit compatível, binding da mesma spec/tarefa,
refs e comandos idênticos, checks realmente aprovados e SHA-256 atual de cada
arquivo. Atestação de `--self-test` não prova entrega.
12. Faça uma micro-retrospectiva: aplique uma melhoria segura encontrada ou registre “nenhuma melhoria necessária” com justificativa; então marque `IMPROVE`.
13. Na seção 14 de `specs/specs/<NNNN>-<slug>/spec.md`, altere o pai de `- [ ]` para `- [x]` somente quando os cinco itens estiverem concluídos.
14. Execute `validate_tasks.py`, recalcule a próxima tarefa e confira o próximo item retornado por `next_task.py`.

Atualize os itens conforme o trabalho acontece; não os marque em lote no encerramento. Tarefas `[P]` podem ser agrupadas apenas quando não tocam os mesmos arquivos ou estado. Se a execução revelar dependência oculta, torne-a explícita na seção 14.

## Controlar mudança de escopo

Pare quando a implementação exigir comportamento não descrito, contradizer um
`AC` ou mudar interface pública, dados, segurança ou fora de escopo. Anuncie a
pendência e carregue automaticamente `$specsfy-update-spec`. Essa skill
preserva o pedido, decide se precisa refinar a pessoa, atualiza a fonte
normativa, reabre somente os gates afetados e percorre validação, tarefas e
TDD/BDD. Retome esta skill somente com os gates novamente aprovados. Atualize na
ordem:

```text
specs/specs/<NNNN>-<slug>/spec.md (seções 1–13) → tarefas (seção 14) → testes → código → evidências na mesma spec
```

Correções internas reversíveis podem ser decididas no código e registradas no relato sem reabrir a especificação.

## Gate de conclusão

Quando todas as tarefas da seção 14 estiverem marcadas:

1. execute a suite completa disponível, lint, tipos e build;
2. execute a rastreabilidade de testes;
3. compare cada `AC`, `FR`, `NFR` e item da Definition of Done com evidência atual;
4. procure tarefas abertas, placeholders, testes pulados e falhas conhecidas;
5. execute novamente `monitor_context.py --project . --check` e resolva toda
   documentação pendente;
6. carregue `$specsfy-documentator`, reconstrua `docs/` e exija que o
   `build_documentation.py --project . --check` passe;
7. não declare conclusão se alguma evidência estiver ausente;
8. altere `Delivery Gate` para `Passed` somente com rastreabilidade completa e `Status` para `Complete` somente com os três gates e a DoD aprovados.

Depois do gate final, projete o resumo de entrega sem criar arquivo:

```bash
python3 -B .agents/skills/specsfy-07-implement/scripts/render_delivery.py \
  specs/specs/<NNNN>-<slug>/spec.md --format markdown
```

Use `--preview` enquanto a entrega estiver aberta. Publicar o texto em PR,
commit ou ferramenta externa exige pedido explícito; o script escreve somente
em stdout.

Leia `references/completion-gates.md` para o fechamento.

## Relatar

Informe tarefas concluídas, arquivos alterados, comandos e resultados, cobertura
de IDs, falhas preexistentes, próxima tarefa pronta ou o gate final. Ao final,
anuncie e carregue automaticamente `$specsfy-progress` para conferir a
visão global derivada da fonte. Em falha, anuncie a pendência, carregue
automaticamente a skill responsável quando necessário e deixe a tarefa aberta
até a correção e retomada.

## Especialistas sob demanda

Leia [references/specialists.md](references/specialists.md) antes de executar
uma tarefa cuja tecnologia ou risco não esteja coberto pelo contexto local.
Instale somente com autorização no projeto consumidor.
