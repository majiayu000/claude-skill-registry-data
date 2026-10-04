---
name: feature-flow
description: Orquestra o ciclo de vida de novas funcionalidades e tarefas técnicas. Use para "criar feature", "iniciar tarefa", "branch" ou "gerar boilerplate".
---

## Workflow

1. **Requirement Storage**: Se invocado pelo PO, gera o documento `docs/features/NNN-nome-da-feature.md` com os critérios de aceite (DoD) e valor de negócio.
2. **Branching**: O Tech Lead ou Dev cria a branch `<type>/<kebab-case>` (Tipos: feat, fix, refactor, chore).
3. **Tasking**: O Tech Lead gera arquivos técnicos sequenciais `001-nome.md` em `docs/todo/` baseados no documento da feature. O arquivo gerado DEVE refletir a estrutura definida no Spec Kit (`memorys/templates/task.md` ou `memorys/templates/bug.md`).
4. **Scaffolding**: Gera boilerplate (Entities, Controllers, Services) seguindo o padrão injetado no `memorys/architecture.md`.
