---
name: project-memory
description: |
  Armazena e consulta memória persistente de projetos em banco PostgreSQL.
  Use quando: (1) tomar decisões técnicas importantes, (2) identificar TODOs/melhorias,
  (3) documentar contexto do projeto, (4) consultar decisões anteriores.
  O Claude deve AUTOMATICAMENTE salvar decisões importantes e consultar memória relevante.
  Identificação do projeto é automática via git repo + branch.
---

# Project Memory

Sistema de memória persistente para projetos, com identificação automática via git.

## Comportamento 100% AUTOMÁTICO

### AO INICIAR SESSÃO:

Claude deve **sempre** ao iniciar uma nova sessão:
1. Executar `python ~/.claude/skills/project-memory/scripts/memory_api.py summary`
2. Mostrar resumo formatado ao usuário

Exemplo de output esperado:
```
📚 Contexto carregado para github.com/user/repo (branch: main)
   - 5 decisões técnicas ativas
   - 3 TODOs pendentes (1 alta prioridade)
   - Última decisão: "Usar PostgreSQL para o banco principal"
```

### SALVAR AUTOMATICAMENTE (sem perguntar):

| Gatilho | Tipo | Comando |
|---------|------|---------|
| Decisão entre alternativas | decision | `add --type decision` |
| Escolha de biblioteca | decision | `add --type decision` |
| Padrão de código definido | pattern | `add --type pattern` |
| Bug importante corrigido | note | `add --type note` |
| Melhoria identificada | todo | `add --type todo` |
| Débito técnico encontrado | todo | `add --type todo` |
| Contexto de negócio | context | `add --type context` |

Após salvar, mostrar notificação breve:
```
💾 Decisão salva: "Usar FastAPI"
```

### CONSULTAR AUTOMATICAMENTE:

- **Início de sessão**: Sempre carregar contexto
- **Antes de sugerir tecnologia**: Verificar se há decisão existente
- **Ao trabalhar em arquivo**: Buscar informações relacionadas

## Comandos Disponíveis

Todos os comandos detectam git repo/branch automaticamente.

### Adicionar entrada
```bash
python ~/.claude/skills/project-memory/scripts/memory_api.py add \
  --type decision \
  --title "Usar PostgreSQL" \
  --content "Escolhemos PostgreSQL porque..." \
  --tags "database,infrastructure" \
  --priority high
```

### Buscar
```bash
# Busca textual
python ~/.claude/skills/project-memory/scripts/memory_api.py search "autenticação"

# Busca em todas as branches
python ~/.claude/skills/project-memory/scripts/memory_api.py search "auth" --all-branches
```

### Listar
```bash
# Por tipo
python ~/.claude/skills/project-memory/scripts/memory_api.py list --type decision

# Por tag
python ~/.claude/skills/project-memory/scripts/memory_api.py list --tag security

# TODOs pendentes
python ~/.claude/skills/project-memory/scripts/memory_api.py todos

# Decisões
python ~/.claude/skills/project-memory/scripts/memory_api.py decisions

# Contexto
python ~/.claude/skills/project-memory/scripts/memory_api.py context
```

### Resumo (para início de sessão)
```bash
python ~/.claude/skills/project-memory/scripts/memory_api.py summary
```

### Atualizar status
```bash
python ~/.claude/skills/project-memory/scripts/memory_api.py update --id <uuid> --status completed
```

## Tipos de Entrada

- `decision`: Decisões técnicas (bibliotecas, arquitetura, padrões)
- `todo`: Melhorias futuras e tarefas pendentes
- `context`: Contexto do projeto (requisitos, regras de negócio)
- `pattern`: Padrões de código e convenções
- `note`: Anotações gerais importantes

## Prioridades

- `low`: Baixa prioridade
- `medium`: Média prioridade (padrão)
- `high`: Alta prioridade
- `critical`: Crítico

## Status

- `active`: Ativo (padrão)
- `completed`: Concluído
- `archived`: Arquivado
- `deprecated`: Descontinuado
