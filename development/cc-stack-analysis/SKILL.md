---
name: cc-stack-analysis
scope: meta-configuration
target: claude-code-itself
description: Expert skill for analyzing Claude Code primitive structures (skills, commands, hooks) in projects. Performs deep quality analysis, detects naming conflicts, validates best practices, identifies missing configurations, and provides actionable recommendations for improving Claude Code setup. This is about analyzing the TOOL configuration itself, not project code.
keywords: claude-code, cc-stack-analysis, cc-analysis, meta-configuration, primitive-analysis, quality-audit, structure-validation, best-practices, configuration-health, cc-audit, tool-analysis
allowed-tools: Read,Grep,Glob,Write,Edit,Bash
---

# Claude Code Stack Analysis

> **⚠️ META-CONFIGURAÇÃO**
> Esta skill analisa a ESTRUTURA de primitivos do Claude Code (skills, commands, hooks), não código de projeto.

---

## 🎯 Objetivo

Analisar a qualidade e estrutura das configurações do Claude Code em um projeto, identificando:
- Problemas de nomenclatura e convenções
- Conflitos de escopo (meta vs domínio)
- Gaps na configuração
- Oportunidades de otimização
- Conformidade com best practices

---

## 📊 Dimensões de Análise

### 1. Inventário Estrutural
**O que fazer:**
- Listar todos os primitivos (skills, commands, hooks)
- Mapear estrutura de diretórios
- Identificar arquivos órfãos ou malformados
- Verificar existência de CLAUDE.md

**Comandos:**
```bash
# Estrutura completa
find .claude -type f -name "*.md" -o -name "*.sh" -o -name "*.py"

# Skills
find .claude/skills -type f -name "SKILL.md"

# Commands
find .claude/commands -type f -name "*.md"

# Hooks
find .claude/hooks -type f -name "*.sh" -o -name "*.py"

# Configurações
cat .claude/settings.json 2>/dev/null || echo "settings.json não encontrado"
```

### 2. Análise de Nomenclatura
**O que validar:**
- Prefixo consistente (`cc-` para meta, `[projeto]-` para domínio)
- Nomes descritivos e sem ambiguidade
- Ausência de conflitos com primitivos padrão
- Seguimento de convenção kebab-case

**Padrões esperados:**
```yaml
# Meta-repo
Skills:    cc-[funcionalidade]    # Exemplo: cc-hooks-setup
Commands:  cc-[ação].md           # Exemplo: cc-diagnose.md
Hooks:     cc-[evento]-[ação].sh  # Exemplo: cc-session-start.sh

# Projeto de domínio
Skills:    [prefix]-[funcionalidade]    # Exemplo: app-auth-agent
Commands:  [prefix]-[ação].md           # Exemplo: app-deploy.md
Hooks:     [prefix]-[evento]-[ação].sh  # Exemplo: app-pretool-validate.sh
```

**Problemas comuns:**
- ❌ `hooks-setup` → ✅ `cc-hooks-setup` (falta prefixo)
- ❌ `app_auth_agent` → ✅ `app-auth-agent` (underscore em vez de hífen)
- ❌ `cc-agent` → ✅ `cc-agent-config` (muito genérico)

### 3. Validação de Frontmatter (Skills)
**Campos obrigatórios:**
```yaml
---
name: [nome-da-skill]              # OBRIGATÓRIO: deve coincidir com nome do diretório
scope: [meta-configuration|domain-implementation]  # OBRIGATÓRIO
target: [claude-code-itself|application-feature|...]  # OBRIGATÓRIO
description: [mínimo 150 caracteres]  # OBRIGATÓRIO
keywords: [pelo menos 5 keywords relevantes]  # OBRIGATÓRIO
allowed-tools: [lista de tools]    # OPCIONAL mas recomendado
---
```

**Validações específicas:**

**Para meta-skills (scope: meta-configuration):**
- ✅ `name` deve começar com `cc-`
- ✅ `scope` deve ser `meta-configuration`
- ✅ `target` deve ser `claude-code-itself`
- ✅ `keywords` deve incluir `claude-code` e `cc-*`
- ✅ `description` deve mencionar "Claude Code" ou "tool configuration"

**Para skills de domínio (scope: domain-implementation):**
- ✅ `name` deve começar com prefixo do projeto (não `cc-`)
- ✅ `scope` deve ser `domain-implementation`
- ✅ `target` deve ser relacionado ao domínio (`application-feature`, `business-logic`, etc.)
- ✅ `keywords` NÃO devem incluir `claude-code` ou `meta` (evitar conflito)

**Como validar:**
```bash
# Extrair frontmatter de todas as skills
for skill in .claude/skills/*/SKILL.md; do
  echo "=== $skill ==="
  sed -n '/^---$/,/^---$/p' "$skill"
done

# Verificar campo específico
grep -h "^name:" .claude/skills/*/SKILL.md
grep -h "^scope:" .claude/skills/*/SKILL.md
grep -h "^keywords:" .claude/skills/*/SKILL.md
```

### 4. Análise de Keywords (Detecção de Conflitos)
**O que verificar:**
- Keywords muito genéricas (`automation`, `setup`, `agent`)
- Sobreposição entre meta-skills e domain-skills
- Falta de keywords específicas

**Estratégia de análise:**
```bash
# Extrair todas as keywords
grep -h "^keywords:" .claude/skills/*/SKILL.md | \
  sed 's/keywords: //' | \
  tr ',' '\n' | \
  sort | uniq -c | sort -rn

# Detectar duplicações (aparecem >1 vez)
# Se keyword aparece em meta E domain = CONFLITO POTENCIAL
```

**Exemplo de conflito:**
```yaml
# cc-automation-setup/SKILL.md (meta)
keywords: automation, hooks, setup, meta  # ← "automation" é genérico

# app-automation-workflow/SKILL.md (domínio)
keywords: automation, workflows, ci-cd    # ← "automation" conflita!

# ✅ SOLUÇÃO:
# cc-automation-setup/SKILL.md
keywords: claude-code, cc-automation, tool-automation, hook-automation, meta-configuration

# app-automation-workflow/SKILL.md
keywords: application, app-automation, workflow-automation, ci-cd-pipeline, deployment
```

### 5. Análise de Hooks
**O que validar:**
- Permissões de execução (`chmod +x`)
- Estrutura de input/output correta (JSON via stdin/stdout)
- Timeout razoável (< 60s para maioria, < 300s para complexos)
- Tratamento de erros
- Documentação inline

**Validação de permissões:**
```bash
# Listar hooks sem permissão de execução
find .claude/hooks -type f \( -name "*.sh" -o -name "*.py" \) ! -perm -u+x
```

**Validação de estrutura:**
```bash
# Hooks bash devem ter shebang
find .claude/hooks -name "*.sh" -exec grep -L "^#!/bin/bash" {} \;

# Hooks python devem ter shebang
find .claude/hooks -name "*.py" -exec grep -L "^#!/usr/bin/env python" {} \;

# Hooks devem ler stdin e retornar JSON
grep -L "cat\|read" .claude/hooks/**/*.sh  # Detecta hooks que não leem stdin
grep -L "echo.*{" .claude/hooks/**/*.sh    # Detecta hooks que não retornam JSON
```

**Verificar registro em settings.json:**
```bash
# Hooks definidos em settings.json
jq '.hooks' .claude/settings.json

# Comparar com hooks existentes no filesystem
# Se hook existe em settings.json mas não em filesystem = PROBLEMA
# Se hook existe em filesystem mas não em settings.json = UNUSED
```

### 6. Análise de Commands
**O que validar:**
- Estrutura markdown consistente
- Frontmatter com escopo claro
- Instruções executáveis (não ambíguas)
- Exemplos de uso
- Estimativa de tempo (quando aplicável)

**Estrutura esperada:**
```markdown
# Título do Command

> **Escopo:** [meta-configuration | domain-implementation]
> **Uso:** /[prefix]:[nome]
> **Descrição:** [O que este comando faz]
> **Tempo estimado:** [X-Y minutos] (opcional)

---

## Tarefa

[Descrição clara da tarefa]

## Passos

1. [Passo 1]
2. [Passo 2]
...

## Resultado Esperado

[O que deve acontecer ao final]
```

**Validações:**
```bash
# Commands devem ter frontmatter
for cmd in .claude/commands/*.md; do
  if ! grep -q "^>" "$cmd"; then
    echo "❌ $cmd: falta frontmatter"
  fi
done

# Commands devem ter seção de tarefa
for cmd in .claude/commands/*.md; do
  if ! grep -q "## Tarefa" "$cmd"; then
    echo "⚠️ $cmd: falta seção 'Tarefa'"
  fi
done
```

### 7. Análise de CLAUDE.md
**O que validar:**
- Existência de CLAUDE.md na raiz do projeto
- Declaração clara de escopo (meta vs domínio)
- Prefixo definido
- Estrutura adequada ao tipo de projeto

**Campos esperados:**

**Para meta-repo:**
```markdown
# CLAUDE.md - Meta-Configuração Claude Code

> **📍 ESCOPO:** meta-configuration
> **🎯 PREFIXO:** `cc-`
> **📅 Criado:** [DATA]

[Documentação sobre configuração do Claude Code]
```

**Para projeto de domínio:**
```markdown
# CLAUDE.md - Projeto [NOME]

> **📍 ESCOPO:** domain-implementation
> **🎯 PREFIXO:** `[projeto]-`
> **📅 Criado:** [DATA]

[Documentação sobre o projeto]

---

**Meta-configuração herdada de:**
`/caminho/para/claude-code/CLAUDE.md`
```

**Validação:**
```bash
# Verificar existência
if [ ! -f "CLAUDE.md" ]; then
  echo "❌ CLAUDE.md não encontrado na raiz do projeto"
fi

# Verificar declaração de escopo
if ! grep -q "ESCOPO:" CLAUDE.md; then
  echo "⚠️ CLAUDE.md não declara escopo (meta-configuration ou domain-implementation)"
fi

# Verificar declaração de prefixo
if ! grep -q "PREFIXO:" CLAUDE.md; then
  echo "⚠️ CLAUDE.md não declara prefixo para primitivos"
fi
```

### 8. Análise de Settings.json
**O que validar:**
- JSON válido (sem erros de sintaxe)
- Hooks registrados corretamente
- Permissions adequadas ao projeto
- Output style configurado
- Caminhos de hooks válidos

**Validação de sintaxe:**
```bash
# Validar JSON
jq empty .claude/settings.json 2>&1 && echo "✅ JSON válido" || echo "❌ JSON inválido"
```

**Validação de hooks:**
```bash
# Extrair comandos de hooks
jq -r '.hooks[][].hooks[].command' .claude/settings.json 2>/dev/null | while read cmd; do
  # Expandir variáveis
  cmd_expanded="${cmd//\$CLAUDE_PROJECT_DIR/.}"

  if [ ! -f "$cmd_expanded" ]; then
    echo "❌ Hook não encontrado: $cmd_expanded"
  fi
done
```

**Validação de permissions:**
```bash
# Verificar se há permissions configuradas
if ! jq -e '.permissions' .claude/settings.json >/dev/null 2>&1; then
  echo "⚠️ Nenhuma permission configurada em settings.json"
fi

# Listar permissions permitidas
jq -r '.permissions.allow[]' .claude/settings.json 2>/dev/null
```

---

## 🎯 Sistema de Scoring

### Categorias de Qualidade (Pesos)

| Categoria | Peso | Descrição |
|-----------|------|-----------|
| **Nomenclatura** | 20% | Consistência de prefixos, convenções, clareza |
| **Estrutura** | 20% | Organização de diretórios, completude de arquivos |
| **Documentação** | 15% | CLAUDE.md, frontmatter, inline docs |
| **Validação** | 15% | Frontmatter válido, JSON válido, sintaxe correta |
| **Best Practices** | 15% | Seguimento de convenções, separação de escopo |
| **Completude** | 15% | Gaps identificados, features missing |

### Fórmula de Score

```
Score Final = (
  (Nomenclatura_Score * 0.20) +
  (Estrutura_Score * 0.20) +
  (Documentação_Score * 0.15) +
  (Validação_Score * 0.15) +
  (BestPractices_Score * 0.15) +
  (Completude_Score * 0.15)
) * 100

Escala: 0-100
```

### Classificação

| Score | Classificação | Ação Recomendada |
|-------|---------------|------------------|
| **90-100** | 🟢 Excelente | Manutenção preventiva |
| **80-89** | 🟢 Bom | Melhorias incrementais |
| **70-79** | 🟡 Aceitável | Resolver problemas médios |
| **60-69** | 🟡 Precisa melhorar | Refatoração parcial |
| **50-59** | 🟠 Problemático | Refatoração significativa |
| **0-49** | 🔴 Crítico | Reconfiguração completa |

---

## 📋 Workflow de Análise

### Fase 1: Descoberta (5-10 min)
```bash
# 1. Identificar contexto do projeto
pwd
cat CLAUDE.md 2>/dev/null | head -20

# 2. Mapear estrutura
tree -L 3 .claude/ 2>/dev/null || find .claude -maxdepth 3 -type f

# 3. Inventariar primitivos
echo "=== SKILLS ==="
find .claude/skills -name "SKILL.md" -exec echo {} \;

echo "=== COMMANDS ==="
find .claude/commands -name "*.md" -exec echo {} \;

echo "=== HOOKS ==="
find .claude/hooks -type f \( -name "*.sh" -o -name "*.py" \)

echo "=== SETTINGS ==="
jq . .claude/settings.json 2>/dev/null || echo "settings.json não encontrado"
```

### Fase 2: Validação de Nomenclatura (10-15 min)
```bash
# 1. Extrair prefixo esperado de CLAUDE.md
EXPECTED_PREFIX=$(grep "PREFIXO:" CLAUDE.md | grep -o '`[^`]*`' | tr -d '`' | head -1)
echo "Prefixo esperado: $EXPECTED_PREFIX"

# 2. Validar skills
for skill_dir in .claude/skills/*/; do
  skill_name=$(basename "$skill_dir")

  if [[ ! "$skill_name" == $EXPECTED_PREFIX* ]]; then
    echo "❌ Skill $skill_name não começa com $EXPECTED_PREFIX"
  fi
done

# 3. Validar commands
for cmd in .claude/commands/*.md; do
  cmd_name=$(basename "$cmd" .md)

  if [[ ! "$cmd_name" == $EXPECTED_PREFIX* ]]; then
    echo "❌ Command $cmd_name não começa com $EXPECTED_PREFIX"
  fi
done

# 4. Validar hooks
for hook in .claude/hooks/**/*.*sh .claude/hooks/**/*.py; do
  [ -f "$hook" ] || continue
  hook_name=$(basename "$hook")

  if [[ ! "$hook_name" == $EXPECTED_PREFIX* ]] && [[ "$hook" != *"/examples/"* ]]; then
    echo "⚠️ Hook $hook_name não começa com $EXPECTED_PREFIX"
  fi
done
```

### Fase 3: Análise de Frontmatter (15-20 min)
```bash
# Para cada skill, validar frontmatter completo
for skill in .claude/skills/*/SKILL.md; do
  echo "=== Analisando: $skill ==="

  # Extrair frontmatter
  frontmatter=$(sed -n '/^---$/,/^---$/p' "$skill" | sed '1d;$d')

  # Validar campos obrigatórios
  for field in name scope target description keywords; do
    if ! echo "$frontmatter" | grep -q "^$field:"; then
      echo "❌ Campo obrigatório ausente: $field"
    fi
  done

  # Validar scope vs target
  scope=$(echo "$frontmatter" | grep "^scope:" | cut -d: -f2- | xargs)
  target=$(echo "$frontmatter" | grep "^target:" | cut -d: -f2- | xargs)

  if [[ "$scope" == "meta-configuration" ]] && [[ "$target" != "claude-code-itself" ]]; then
    echo "⚠️ Scope é meta-configuration mas target não é claude-code-itself"
  fi

  # Validar keywords
  keywords=$(echo "$frontmatter" | grep "^keywords:" | cut -d: -f2-)

  if [[ "$scope" == "meta-configuration" ]] && ! echo "$keywords" | grep -q "claude-code"; then
    echo "⚠️ Meta-skill deve ter keyword 'claude-code'"
  fi

  if [[ "$scope" == "domain-implementation" ]] && echo "$keywords" | grep -q "claude-code\|meta"; then
    echo "⚠️ Domain-skill não deve ter keywords 'claude-code' ou 'meta' (conflito)"
  fi
done
```

### Fase 4: Detecção de Conflitos de Keywords (10-15 min)
```bash
# Extrair todas as keywords e contar ocorrências
echo "=== Análise de Keywords ==="

all_keywords=$(grep -h "^keywords:" .claude/skills/*/SKILL.md | \
  sed 's/keywords: //' | \
  tr ',' '\n' | \
  sed 's/^ *//;s/ *$//' | \
  sort)

# Contar duplicações
duplicates=$(echo "$all_keywords" | uniq -d)

if [ -n "$duplicates" ]; then
  echo "⚠️ Keywords duplicadas detectadas:"
  echo "$duplicates"

  # Para cada keyword duplicada, mostrar em quais skills aparece
  while read -r keyword; do
    echo ""
    echo "Keyword '$keyword' aparece em:"
    grep -l "$keyword" .claude/skills/*/SKILL.md
  done <<< "$duplicates"
else
  echo "✅ Nenhuma duplicação de keywords detectada"
fi

# Detectar keywords muito genéricas
generic_keywords="automation setup config agent deployment testing build"
for generic in $generic_keywords; do
  if echo "$all_keywords" | grep -qw "$generic"; then
    echo "⚠️ Keyword genérica detectada: '$generic'"
    echo "   Skills usando essa keyword:"
    grep -l "keywords:.*$generic" .claude/skills/*/SKILL.md
  fi
done
```

### Fase 5: Análise de Hooks (10-15 min)
```bash
echo "=== Análise de Hooks ==="

# 1. Verificar permissões
echo "Hooks sem permissão de execução:"
find .claude/hooks -type f \( -name "*.sh" -o -name "*.py" \) ! -perm -u+x

# 2. Verificar shebang
echo ""
echo "Scripts Bash sem shebang:"
find .claude/hooks -name "*.sh" -exec grep -L "^#!/bin/bash\|^#!/usr/bin/env bash" {} \;

echo ""
echo "Scripts Python sem shebang:"
find .claude/hooks -name "*.py" -exec grep -L "^#!/usr/bin/env python" {} \;

# 3. Verificar estrutura de input/output
echo ""
echo "Hooks que podem não estar lendo stdin:"
for hook in .claude/hooks/**/*.sh; do
  [ -f "$hook" ] || continue
  if ! grep -q "cat\|read" "$hook"; then
    echo "⚠️ $hook: pode não estar lendo stdin"
  fi
done

# 4. Comparar hooks registrados vs existentes
echo ""
echo "Hooks registrados em settings.json:"
registered_hooks=$(jq -r '.hooks[][].hooks[].command' .claude/settings.json 2>/dev/null | \
  sed 's|\$CLAUDE_PROJECT_DIR|.|g')

echo "$registered_hooks" | while read -r hook_path; do
  if [ ! -f "$hook_path" ]; then
    echo "❌ Hook registrado não encontrado: $hook_path"
  fi
done

# 5. Hooks existentes mas não registrados
echo ""
echo "Hooks não registrados em settings.json:"
for hook in .claude/hooks/**/*.*sh .claude/hooks/**/*.py; do
  [ -f "$hook" ] || continue
  [ -x "$hook" ] || continue  # Só considerar executáveis

  hook_relative=".claude/${hook#*.claude/}"

  if ! echo "$registered_hooks" | grep -q "$hook_relative"; then
    echo "⚠️ Hook não registrado: $hook_relative"
  fi
done
```

### Fase 6: Cálculo de Score (10-15 min)
```bash
# Implementar sistema de scoring baseado em problemas detectados

# Inicializar scores
nomenclatura_score=100
estrutura_score=100
documentacao_score=100
validacao_score=100
bestpractices_score=100
completude_score=100

# Deduzir pontos baseado em problemas detectados

# Nomenclatura (deduzir 10 pontos por prefixo incorreto)
incorrect_prefixes=$(find .claude/skills .claude/commands -name "*.md" | wc -l)  # Simplificado
nomenclatura_score=$((nomenclatura_score - (incorrect_prefixes * 10)))

# Estrutura (deduzir por arquivos faltantes)
[ ! -f "CLAUDE.md" ] && estrutura_score=$((estrutura_score - 30))
[ ! -f ".claude/settings.json" ] && estrutura_score=$((estrutura_score - 20))

# Documentação (deduzir por frontmatter incompleto)
incomplete_frontmatter=$(grep -L "description:" .claude/skills/*/SKILL.md | wc -l)
documentacao_score=$((documentacao_score - (incomplete_frontmatter * 15)))

# Validação (deduzir por erros de sintaxe)
! jq empty .claude/settings.json 2>/dev/null && validacao_score=$((validacao_score - 40))

# Best practices (deduzir por keywords conflitantes)
conflicting_keywords=$(echo "$duplicates" | wc -l)
bestpractices_score=$((bestpractices_score - (conflicting_keywords * 10)))

# Completude (deduzir por hooks não registrados)
unregistered_hooks=$(find .claude/hooks -type f -executable | wc -l)  # Simplificado
completude_score=$((completude_score - (unregistered_hooks * 5)))

# Garantir scores >= 0
nomenclatura_score=$((nomenclatura_score < 0 ? 0 : nomenclatura_score))
estrutura_score=$((estrutura_score < 0 ? 0 : estrutura_score))
documentacao_score=$((documentacao_score < 0 ? 0 : documentacao_score))
validacao_score=$((validacao_score < 0 ? 0 : validacao_score))
bestpractices_score=$((bestpractices_score < 0 ? 0 : bestpractices_score))
completude_score=$((completude_score < 0 ? 0 : completude_score))

# Calcular score final
score_final=$(awk "BEGIN {
  printf \"%.1f\", (
    ($nomenclatura_score * 0.20) +
    ($estrutura_score * 0.20) +
    ($documentacao_score * 0.15) +
    ($validacao_score * 0.15) +
    ($bestpractices_score * 0.15) +
    ($completude_score * 0.15)
  )
}")

echo ""
echo "=== SCORE FINAL ==="
echo "Nomenclatura:   $nomenclatura_score/100 (20%)"
echo "Estrutura:      $estrutura_score/100 (20%)"
echo "Documentação:   $documentacao_score/100 (15%)"
echo "Validação:      $validacao_score/100 (15%)"
echo "Best Practices: $bestpractices_score/100 (15%)"
echo "Completude:     $completude_score/100 (15%)"
echo ""
echo "SCORE FINAL: $score_final/100"

# Classificação
if (( $(echo "$score_final >= 90" | bc -l) )); then
  echo "Classificação: 🟢 Excelente"
elif (( $(echo "$score_final >= 80" | bc -l) )); then
  echo "Classificação: 🟢 Bom"
elif (( $(echo "$score_final >= 70" | bc -l) )); then
  echo "Classificação: 🟡 Aceitável"
elif (( $(echo "$score_final >= 60" | bc -l) )); then
  echo "Classificação: 🟡 Precisa melhorar"
elif (( $(echo "$score_final >= 50" | bc -l) )); then
  echo "Classificação: 🟠 Problemático"
else
  echo "Classificação: 🔴 Crítico"
fi
```

### Fase 7: Geração de Relatório (10-15 min)

Gerar relatório markdown com:
- Executive summary (score, classificação)
- Inventário completo (primitivos detectados)
- Problemas por severidade (críticos, altos, médios, baixos)
- Recomendações priorizadas
- Roadmap de melhorias (quick wins vs long-term)

**Template:** Usar estrutura similar ao audit-report-template.md do BOM-STACK-PLANEJAMENTO, adaptado para análise de primitivos do Claude Code.

---

## 🛠️ Recomendações Padrão

### Problemas Críticos (Bloquear uso)

| Problema | Impacto | Recomendação |
|----------|---------|--------------|
| **settings.json inválido** | Configuração não carrega | Corrigir sintaxe JSON imediatamente |
| **Hooks sem permissão** | Hooks não executam | `chmod +x` em todos os hooks |
| **Conflito de escopo** | Auto-discovery quebrado | Renomear skills conflitantes com prefixo correto |
| **CLAUDE.md ausente** | Ambiguidade de contexto | Criar CLAUDE.md declarando escopo |

### Problemas Altos (Resolver em 7 dias)

| Problema | Impacto | Recomendação |
|----------|---------|--------------|
| **Prefixos inconsistentes** | Confusão, conflitos futuros | Padronizar todos os prefixos |
| **Keywords genéricas** | Colisão entre skills | Especializar keywords com namespaces |
| **Frontmatter incompleto** | Skills não descobertas | Completar YAML frontmatter |
| **Hooks não registrados** | Funcionalidades não ativas | Registrar em settings.json |

### Problemas Médios (Resolver em 30 dias)

| Problema | Impacto | Recomendação |
|----------|---------|--------------|
| **Documentação inline fraca** | Baixa manutenibilidade | Adicionar comentários, exemplos |
| **Commands sem estrutura** | Difícil de usar | Adicionar frontmatter, seções |
| **Hooks sem timeout** | Risco de travamento | Definir timeout apropriado |
| **Skills muito genéricas** | Auto-discovery impreciso | Especializar descrição, keywords |

### Melhorias Oportunísticas (Backlog)

| Melhoria | Benefício | Recomendação |
|----------|-----------|--------------|
| **Knowledge base vazio** | Menos contexto para Claude | Criar documentação de referência |
| **Templates ausentes** | Menos padronização | Criar templates para novos primitivos |
| **Tests ausentes** | Menor confiabilidade | Adicionar testes de validação |
| **CI/CD não configurado** | Validação manual | Automatizar validação em PRs |

---

## 🎓 Insights Educacionais

### Separação de Escopo: Meta vs Domínio

A confusão mais comum é misturar primitivos de configuração DO Claude Code com primitivos de implementação DO projeto.

**Regra de Ouro:**
```
SE o primitive configura, otimiza, ou debug o PRÓPRIO Claude Code:
  → scope: meta-configuration
  → prefixo: cc-
  → target: claude-code-itself
  → keywords: claude-code, cc-*, meta, tool-*

SE o primitive implementa funcionalidades DO projeto/aplicação:
  → scope: domain-implementation
  → prefixo: [projeto]-
  → target: application-feature (ou similar)
  → keywords: application, [projeto]-*, business-logic, feature-*
```

**Exemplo:**
```
❌ ERRADO (mistura conceitos):
   Skill: app-hooks-setup
   Descrição: "Configure hooks for the Claude Code tool"
   → Meta-conceito (Claude Code) em primitivo de domínio (app-)

✅ CORRETO (separado):
   # Meta-repo
   Skill: cc-hooks-setup
   Descrição: "Configure Claude Code lifecycle hooks"

   # Projeto
   Skill: app-webhook-handler
   Descrição: "Handle application webhooks for external integrations"
```

### Auto-Discovery: Como Funciona

Claude Code detecta skills relevantes baseado em:
1. **Keywords matching** (pergunta do usuário vs keywords da skill)
2. **Description similarity** (embedding vectors)
3. **Context awareness** (working directory, CLAUDE.md)

**Otimização:**
- Keywords específicas aumentam precision (menos false positives)
- Description detalhada aumenta recall (menos false negatives)
- Separação clara de escopo evita conflicts

**Exemplo:**
```yaml
# ❌ MAL OTIMIZADO (genérico)
keywords: hooks, setup, automation
description: Setup hooks

# ✅ BEM OTIMIZADO (específico)
keywords: claude-code, cc-hooks, hook-automation, SessionStart, PostToolUse, PreToolUse, lifecycle-hooks, meta-configuration
description: Expert in configuring Claude Code lifecycle hooks (SessionStart, PostToolUse, PreToolUse) including bash/python implementation, JSON I/O validation, timeout management, error handling, and registration in settings.json
```

---

## 🚀 Uso desta Skill

### Quando Ativar

Esta skill deve ser ativada quando o usuário:
- Pergunta "Como está minha configuração do Claude Code?"
- Pede "Analise a estrutura de skills/commands/hooks"
- Quer "Auditar a qualidade das configurações"
- Relata "Skills não estão sendo descobertas corretamente"
- Menciona "Validar separação de escopo meta vs domínio"

### Workflow Típico

```
Usuário: "Pode analisar minha configuração do Claude Code?"

Claude (ativa cc-stack-analysis):
  1. Executa Fase 1-7 do workflow
  2. Gera score e classificação
  3. Lista problemas priorizados
  4. Fornece recomendações acionáveis
  5. Oferece gerar relatório completo
```

### Integração com Outros Commands

Esta skill complementa:
- `/cc:manage-primitives` - CRUD operations nos primitivos
- `/cc:setup` - Configuração inicial de novos projetos
- `/cc:diagnose` - Diagnóstico de problemas específicos

**Workflow recomendado:**
```
1. /cc:stack-analysis → Identificar problemas
2. /cc:manage-primitives update → Corrigir problemas
3. /cc:stack-analysis → Validar correções
```

---

## ✅ Checklist de Análise Completa

- [ ] **Inventário estrutural** realizado (skills, commands, hooks, settings)
- [ ] **Nomenclatura validada** (prefixos, convenções, kebab-case)
- [ ] **Frontmatter validado** (campos obrigatórios, scope, target, keywords)
- [ ] **Conflitos de keywords** detectados e documentados
- [ ] **Hooks analisados** (permissões, estrutura, registro)
- [ ] **Commands analisados** (estrutura, frontmatter, clareza)
- [ ] **CLAUDE.md validado** (existência, escopo, prefixo)
- [ ] **Settings.json validado** (sintaxe, hooks, permissions)
- [ ] **Score calculado** (6 categorias ponderadas)
- [ ] **Classificação determinada** (Excelente → Crítico)
- [ ] **Problemas priorizados** (Críticos, Altos, Médios, Oportunísticos)
- [ ] **Recomendações geradas** (acionáveis, com exemplos)
- [ ] **Relatório formatado** (markdown, estruturado)

---

**Esta skill foi projetada para garantir qualidade e consistência nas configurações do Claude Code, facilitando manutenção, evolução e troubleshooting.**
