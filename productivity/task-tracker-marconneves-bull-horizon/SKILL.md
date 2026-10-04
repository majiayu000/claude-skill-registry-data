---
name: task-tracker
description: Escaneia docs/todo/ procurando demandas pendentes e arquiva as concluídas em docs/done/. Use para "verificar tasks", "fechar task", "o que está pendente" ou "mover para done".
---

## Workflow

1. **Scan**: Varre `docs/todo/` listando todos os subdiretórios de demanda existentes.

2. **Análise de Status**: Para cada subdiretório, lê o arquivo de tasks e verifica:
   - Todos os itens `- [x]` marcados → Demanda **Concluída** ✅
   - Existem itens `- [ ]` pendentes → Demanda **Em Andamento** 🔄
   - Nenhum item marcado → Demanda **Não Iniciada** 📋

3. **Relatório**: Exibe um sumário classificado por status antes de qualquer ação.

4. **Arquivamento das Concluídas**: Para cada demanda com status Concluída:
   - Move o subdiretório de `docs/todo/<NNN-nome>/` para `docs/done/<NNN-nome>/`
   - Mantém os arquivos internos intactos (spec.md, plan.md, task.md)

5. **Confirmação**: Informa ao usuário quais demandas foram arquivadas e quantas permanecem pendentes.
