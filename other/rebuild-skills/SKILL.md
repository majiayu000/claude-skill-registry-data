---
name: rebuild-skills
description: Rewrite third-party skills as DME Technology originals. Use when onboarding new skills from marketplace or repos. Applies DME standards and optimizes for our agent architecture.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Grep Glob
argument-hint: [skill-name | --all | --list]
---

# Rebuild Skills -- Portfolio DME Technology

Reescrever skills de terceiros como propriedade intelectual da DME, otimizadas para nossos agents.

## Argumentos

- `$ARGUMENTS` = nome da skill -> reescreve apenas essa
- `$ARGUMENTS` = --all -> reescreve todas as skills que ainda tem conteudo de terceiros
- `$ARGUMENTS` = --list -> lista skills candidatas a reescrita

## Processo por skill

### 1. Ler a skill original
Ler `~/.claude/skills/<nome>/SKILL.md` e extrair:
- O que ela faz (funcionalidade core)
- Quais ferramentas usa
- Qual agent deveria consumi-la

### 2. Reescrever seguindo padroes DME

Regras obrigatorias:
- ZERO emojis em todo o conteudo
- Portugues correto com acentos e cedilha nos textos descritivos
- Frontmatter em ingles (padrao agentskills.io)
- Conteudo tecnico (codigo, comandos) em ingles
- Remover qualquer referencia ao autor/repo original
- Remover branding de terceiros
- Adaptar exemplos para stacks DME (Next.js, Supabase, Railway, etc.)
- Adicionar contexto de seguranca DME onde aplicavel
- Manter o conteudo tecnico valioso, descartar o generico

### 3. Validar a skill reescrita

- Verificar que o frontmatter esta correto (name, description, campos opcionais)
- Verificar que nao tem emojis
- Verificar que a description e clara o suficiente para invocacao automatica
- Verificar que esta referenciada no agent correto via campo `skills`

### 4. Mapeamento Agent x Skill

Consultar os agents em `~/.claude/agents/` para saber qual agent consome qual skill.
Se a skill nao esta mapeada a nenhum agent, avaliar:
- Deve ser acoplada a um agent existente?
- Deve ser independente (invocacao direta)?
- Deve ser removida (sem valor para DME)?

### 5. Reportar

Para cada skill reescrita, mostrar:
```
SKILL: [nome]
STATUS: reescrita / mantida / removida
AGENT: [qual agent consome]
MUDANCAS: [lista do que mudou]
```
