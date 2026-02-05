---
name: cc-separation-guide
scope: meta-configuration
target: claude-code-itself
description: Complete guide for separating meta-configurations (Claude Code tool configuration) from domain configurations (project implementation). Learn how to avoid conflicts when working with multiple projects, especially those using agent SDKs/ADKs like Google ADK, LangChain, or Anthropic SDK. Covers namespace isolation, prefixing conventions, CLAUDE.md hierarchy, scope declaration, and conflict detection strategies.
keywords: claude-code, cc-separation, meta-configuration, domain-configuration, namespace, prefixes, conflict-resolution, scope, agent-sdk, adk, separation-of-concerns, project-isolation, cc-conventions
allowed-tools: Read,Grep,Glob,Edit
---

# Claude Code: Separação Meta vs Domínio

> **⚠️ META-CONFIGURAÇÃO CRÍTICA**
> Este skill trata da SEPARAÇÃO entre configurações DO Claude Code (meta) e configurações DE PROJETOS (domínio). Essencial para evitar conflitos.

---

## 🎯 Problema a Resolver

### Cenário de Conflito

Quando você tem:

1. **Meta-repositório** (`/workspace/claude-code`):
   - Base de conhecimento SOBRE Claude Code
   - Skills para CONFIGURAR Claude Code
   - Templates para APLICAR em projetos

2. **Projeto-alvo** (`/workspace/meu-projeto`):
   - Implementação de funcionalidades
   - Skills DE DOMÍNIO (ex: authentication, API)
   - Pode usar SDKs agênticos (Google ADK, LangChain)

**Problema:** Ambos usam terminologia similar:
- "agent", "skill", "command", "hook"
- Mas significados DIFERENTES

**Resultado sem separação:**
- 🔴 Claude confunde "agent do Claude Code" com "agent do projeto"
- 🔴 Skills de meta ativam quando devia ativar skills de domínio
- 🔴 Commands conflitam (ex: `/setup` - setup de quê?)
- 🔴 Hooks executam no contexto errado

---

## 🏗️ Arquitetura de Separação

### Princípio Fundamental

```
META-CONFIGURAÇÃO          ≠          CONFIGURAÇÃO DE DOMÍNIO
(Sobre a ferramenta)                  (Sobre o projeto)

Target: Claude Code                   Target: Funcionalidades
Prefixo: cc-                          Prefixo: <projeto>-
Escopo: meta-configuration            Escopo: domain-implementation
Keywords: claude-code, tool, meta     Keywords: application, feature, app
```

### Visualização da Separação

```
┌─────────────────────────────────────────────────────────────┐
│  Meta-Repositório: /workspace/claude-code                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ .claude/                                               │ │
│  │ ├── skills/                                            │ │
│  │ │   ├── cc-overview/           ← Sobre Claude Code   │ │
│  │ │   ├── cc-hooks-guide/        ← Sobre Claude Code   │ │
│  │ │   └── cc-separation-guide/   ← Sobre Claude Code   │ │
│  │ ├── commands/                                          │ │
│  │ │   ├── cc-setup.md            ← Setup do Claude Code │ │
│  │ │   └── cc-diagnose.md                                │ │
│  │ └── CLAUDE.md                  ← Diretrizes META      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

                              ≠

┌─────────────────────────────────────────────────────────────┐
│  Projeto: /workspace/meu-app                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ .claude/                                               │ │
│  │ ├── skills/                                            │ │
│  │ │   ├── app-auth-agent/        ← Autenticação da app │ │
│  │ │   ├── app-api-setup/         ← API da app          │ │
│  │ │   └── app-deploy/            ← Deploy da app       │ │
│  │ ├── commands/                                          │ │
│  │ │   ├── app-setup.md           ← Setup da APP        │ │
│  │ │   └── app-test.md            ← Testes da app       │ │
│  │ └── CLAUDE.md                  ← Diretrizes PROJETO  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Convenções de Nomenclatura

### Regra de Ouro

```
SE artefato é SOBRE Claude Code → prefixo cc-
SE artefato é SOBRE projeto → prefixo do projeto
NUNCA usar nomes genéricos sem prefixo
```

### Tabela de Prefixos

| Contexto | Prefixo | Exemplo Skill | Exemplo Command |
|----------|---------|---------------|-----------------|
| **Meta** (Claude Code) | `cc-` | `cc-hooks-guide` | `cc-setup.md` |
| **Projeto Web** | `app-` | `app-auth-setup` | `app-deploy.md` |
| **Backend API** | `api-` | `api-endpoints` | `api-test.md` |
| **Microserviço** | `svc-` | `svc-payments` | `svc-deploy.md` |
| **SDK Agêntico** | `<sdk>-` | `cva-agent-types` | `cva-new-agent.md` |

### Exemplos Corretos vs Incorretos

#### Skills

| ✅ Correto | ❌ Incorreto | Problema |
|-----------|-------------|----------|
| `cc-hooks-setup` | `hooks-setup` | Ambíguo (hooks de quê?) |
| `app-auth-flow` | `auth-flow` | Conflita com auth do Claude Code |
| `cva-healthcare-pipeline` | `healthcare-pipeline` | Sem namespace, genérico |

#### Commands

| ✅ Correto | ❌ Incorreto | Problema |
|-----------|-------------|----------|
| `/cc:setup` | `/setup` | Conflita com setup de projeto |
| `/app:deploy` | `/deploy` | Ambíguo (deploy de quê?) |
| `/api:test` | `/test` | Genérico demais |

#### Hooks

| ✅ Correto | ❌ Incorreto | Problema |
|-----------|-------------|----------|
| `cc-posttool-format.sh` | `format.sh` | Não indica contexto |
| `app-posttool-lint.sh` | `lint.sh` | Pode conflitar |

---

## 📝 Declaração Explícita de Escopo

### YAML Frontmatter Obrigatório

Toda skill DEVE declarar seu escopo no frontmatter:

#### Meta-Skill (Claude Code)

```yaml
---
name: cc-hooks-guide
scope: meta-configuration              # ← OBRIGATÓRIO
target: claude-code-itself             # ← O QUE configura
description: Complete guide to Claude Code hooks. This is about CONFIGURING the Claude Code TOOL itself, not project code.
keywords: claude-code, cc-hooks, meta-configuration, tool-configuration, automation
allowed-tools: Read,Edit,Write
---

# Claude Code Hooks Guide

> **⚠️ META-CONFIGURAÇÃO**
> Este skill configura o PRÓPRIO Claude Code, não código de projeto.
```

#### Domain-Skill (Projeto)

```yaml
---
name: app-auth-setup
scope: domain-implementation           # ← OBRIGATÓRIO
target: application-feature            # ← O QUE implementa
description: Authentication setup for the application using OAuth2 and JWT. This is about APPLICATION functionality, not Claude Code configuration.
keywords: application, app-auth, authentication, oauth2, jwt, security
allowed-tools: Read,Edit,Write,Bash
---

# Application Authentication Setup

> **🎯 FUNCIONALIDADE DO PROJETO**
> Este skill implementa autenticação na aplicação, não configura Claude Code.
```

### Campos Obrigatórios

| Campo | Meta | Domínio | Propósito |
|-------|------|---------|-----------|
| `scope` | `meta-configuration` | `domain-implementation` | Identifica escopo |
| `target` | `claude-code-itself` | `application-feature` | Identifica alvo |
| `description` | Deve incluir "Claude Code" e "tool" | Deve incluir nome do projeto/feature | Auto-discovery |
| `keywords` | Incluir `claude-code`, `cc-*`, `meta` | Incluir nome do projeto, features | Evitar sobreposição |

---

## 🧭 Hierarquia CLAUDE.md

### Estrutura de Precedência

```
~/.claude/CLAUDE.md                    # Nível 1: Global
    ↓  (princípios universais de desenvolvimento)

/workspace/claude-code/CLAUDE.md       # Nível 2: Meta
    ↓  (diretrizes de configuração do Claude Code)

/workspace/meu-projeto/CLAUDE.md       # Nível 3: Projeto
    ↓  (diretrizes específicas do projeto)
```

**Regra de Precedência:**
```
Projeto (mais específico) > Meta > Global (mais genérico)
```

### Conteúdo de Cada CLAUDE.md

#### Global (`~/.claude/CLAUDE.md`)

```markdown
# CLAUDE.md - Diretrizes Globais

> **Escopo:** Todos os projetos
> **Foco:** Princípios universais de desenvolvimento

## Conteúdo

- Princípios de execução autônoma
- Gestão de dependências
- Versionamento (SemVer)
- CI/CD patterns
- Quality gates
- Observabilidade

**Aplicável a:** Qualquer projeto, qualquer linguagem
```

#### Meta (`/workspace/claude-code/CLAUDE.md`)

```markdown
# CLAUDE.md - Meta-Configuração Claude Code

> **Escopo:** Configuração do Claude Code
> **Foco:** Como configurar a ferramenta

## Conteúdo

- Separação meta vs domínio
- Prefixos obrigatórios (cc-)
- Estrutura de skills/commands/hooks
- Convenções de nomenclatura
- Templates para projetos

**Aplicável a:** Configuração do Claude Code em qualquer projeto
```

#### Projeto (`/workspace/meu-projeto/CLAUDE.md`)

```markdown
# CLAUDE.md - Projeto [Nome]

> **Escopo:** Desenvolvimento do projeto [Nome]
> **Prefixo:** `app-`

## Conteúdo

- Arquitetura do projeto
- Convenções específicas (app- prefix)
- Workflows de desenvolvimento
- Testing strategies
- Deployment procedures

**Herda de:** `/workspace/claude-code/CLAUDE.md` (meta-config)
**Sobrescreve:** Diretrizes conflitantes (precedência)
```

---

## 🔍 Detecção de Contexto

### Checklist de Verificação

Claude deve SEMPRE verificar antes de executar tarefas:

#### 1. Qual diretório estou?

```bash
pwd
# /workspace/claude-code        → Contexto META
# /workspace/meu-projeto        → Contexto PROJETO
```

#### 2. Qual CLAUDE.md tem precedência?

```python
if exists("/workspace/meu-projeto/CLAUDE.md"):
    context = "project"
    prefix = extract_prefix_from_claudemd()  # ex: "app-"
elif exists("/workspace/claude-code/CLAUDE.md"):
    context = "meta"
    prefix = "cc-"
else:
    context = "global"
    prefix = None  # use generic
```

#### 3. Prefixo esperado?

```
Contexto META → cc-
Contexto PROJETO → <projeto>- (extrair de CLAUDE.md)
```

#### 4. Keywords evitam conflito?

```yaml
# META
keywords: claude-code, cc-*, tool-*, meta-configuration

# PROJETO
keywords: application, app-*, feature-*, business-logic

# ✅ Zero sobreposição
```

---

## 🎭 Resolução de Ambiguidades

### Cenário 1: Pergunta Sobre "Agent"

**Pergunta ambígua:**
```
"Como configuro um agent?"
```

**Claude detecta ambiguidade:**
```python
# Verificar contexto
pwd = get_current_directory()

if "claude-code" in pwd:
    # Contexto meta
    likely_meaning = "Claude Code agent (autonomous AI)"
    relevant_skill = "cc-agent-config"
else:
    # Contexto projeto
    likely_meaning = "Domain agent (LLM agent, workflow agent)"
    relevant_skill = "app-agent-setup"  # ou similar

# Se não houver certeza (keywords ambíguas), PERGUNTAR
```

**Claude pergunta ao usuário:**
```
🤔 Preciso clarificar o contexto da sua pergunta:

Você quer:

A) **Configurar Claude Code** (o agente autônomo da Anthropic)?
   → Contexto: Meta-configuração
   → Skill relevante: cc-agent-config
   → Exemplo: Configurar comportamento, permissões, output style

B) **Criar/configurar um agente de domínio** no seu projeto?
   → Contexto: Implementação de projeto
   → Skill relevante: app-agent-setup
   → Exemplo: Agente LLM, workflow agent, microserviço

Qual dos dois?
```

### Cenário 2: Auto-Discovery Correto

#### Usuário em `/workspace/claude-code`

```
Pergunta: "Como adiciono hooks?"

Claude detecta:
  - pwd: /workspace/claude-code
  - CLAUDE.md: Meta-configuração
  - Prefixo esperado: cc-

Claude busca skills:
  - Match: cc-hooks-guide
  - Keywords: claude-code, hooks, tool-configuration, meta

Claude ativa: cc-hooks-guide
Claude responde: "Hooks do Claude Code (SessionStart, PostToolUse, etc.)"
```

#### Usuário em `/workspace/meu-app`

```
Pergunta: "Como adiciono hooks?"

Claude detecta:
  - pwd: /workspace/meu-app
  - CLAUDE.md: Projeto (prefixo app-)
  - Prefixo esperado: app-

Claude busca skills:
  - Match: app-hooks-workflow (se existir)
  - Keywords: application, webhooks, event-handlers

Se skill existe:
  Claude ativa: app-hooks-workflow
  Claude responde: "Hooks da aplicação (webhooks, lifecycle events)"

Se skill NÃO existe:
  Claude pergunta: "Você quer configurar hooks do Claude Code ou implementar hooks na aplicação?"
```

### Cenário 3: Command Conflitante

**Comando:** `/setup`

```python
# Verificar contexto
pwd = get_current_directory()

if "claude-code" in pwd:
    # Buscar /cc:setup ou cc-setup.md
    execute_command("cc-setup")
else:
    # Buscar /<projeto>:setup ou <projeto>-setup.md
    project_prefix = extract_prefix()
    execute_command(f"{project_prefix}-setup")

# Se comando não existe, sugerir criar com prefixo
```

---

## 📊 Matriz de Conflitos Comuns

| Termo Ambíguo | Contexto Meta | Contexto Projeto |
|---------------|---------------|------------------|
| **agent** | Claude Code (IA autônoma) | Agente de domínio (LLM, workflow) |
| **skill** | Claude Code skill (SKILL.md) | Agent skill (capability, function) |
| **hook** | Claude Code lifecycle hook | Webhook, event handler |
| **command** | Slash command do Claude Code | CLI command, API endpoint |
| **tool** | Claude Code tool (Read, Write) | External tool (API client, lib) |
| **setup** | Setup do Claude Code | Setup do projeto/ambiente |
| **config** | Claude Code config (settings.json) | App config (env vars, config files) |

### Como Disambiguar

1. **Usar qualificadores:**
   ```
   "Claude Code hook" vs "application hook"
   "Claude Code agent" vs "domain agent"
   "Claude Code skill" vs "agent skill"
   ```

2. **Verificar prefixo:**
   ```
   cc-hook-setup     → META (Claude Code)
   app-hook-handler  → DOMÍNIO (Application)
   ```

3. **Verificar keywords:**
   ```yaml
   # Meta
   keywords: claude-code, tool, meta, cc-*

   # Domínio
   keywords: application, feature, app-*, business
   ```

4. **Perguntar quando incerto:**
   ```
   Claude: "Para clarificar: você está perguntando sobre
           configuração do Claude Code ou implementação do projeto?"
   ```

---

## 🛠️ Aplicação em Novos Projetos

### Template: Novo Projeto

#### Passo 1: NÃO Copiar Meta-Repo Inteiro

```bash
# ❌ ERRADO
cp -r /workspace/claude-code/.claude /workspace/novo-projeto/

# ✅ CORRETO (copiar apenas templates)
mkdir -p /workspace/novo-projeto/.claude
cp -r /workspace/claude-code/.claude/templates/* \
      /workspace/novo-projeto/.claude/
```

**Por quê?**
- Meta-repo tem skills SOBRE Claude Code
- Projeto precisa de skills SOBRE funcionalidades
- Copiar tudo = conflito garantido

#### Passo 2: Adaptar Prefixos

```bash
cd /workspace/novo-projeto/.claude

# Substituir todos os cc- pelo prefixo do projeto
PROJECT_PREFIX="myapp"

# Skills
find skills/ -type f -name "*.md" -exec sed -i "s/cc-/${PROJECT_PREFIX}-/g" {} +

# Commands
find commands/ -type f -name "*.md" -exec sed -i "s/cc-/${PROJECT_PREFIX}-/g" {} +

# Hooks
find hooks/ -type f -exec sed -i "s/cc-/${PROJECT_PREFIX}-/g" {} +

# Renomear arquivos/diretórios
for dir in skills/cc-*; do
  mv "$dir" "${dir/cc-/${PROJECT_PREFIX}-}"
done
```

#### Passo 3: Criar CLAUDE.md do Projeto

```bash
cat > /workspace/novo-projeto/CLAUDE.md <<'EOF'
# CLAUDE.md - Projeto [Nome]

> **📍 ESCOPO:** Desenvolvimento do projeto [Nome]
> **🎯 PREFIXO:** `myapp-` (para skills, commands, hooks)
> **📅 Criado:** $(date +%Y-%m-%d)

---

## 🎯 Visão Geral

Este projeto implementa [descrição].

## 📐 Convenções

### Nomenclatura
- **Prefixo obrigatório:** `myapp-`
- **Escopo:** domain-implementation
- **Target:** application-feature

### Skills
- `myapp-overview` - Visão geral do projeto
- `myapp-auth` - Autenticação
- `myapp-api` - Endpoints da API
- `myapp-deploy` - Deploy

### Commands
- `/myapp:setup` - Setup do ambiente
- `/myapp:test` - Executar testes
- `/myapp:deploy` - Deploy para produção

---

**Meta-configuração herdada de:**
`/home/notebook/workspace/claude-code/CLAUDE.md`

**Documentação de referência:**
`/home/notebook/workspace/claude-code/ARCHITECTURE_ANALYSIS.md`
EOF
```

#### Passo 4: Atualizar Frontmatter das Skills

```yaml
# Template do meta-repo (claude-code)
---
name: cc-exemplo
scope: meta-configuration
target: claude-code-itself
description: Configure Claude Code hooks
keywords: claude-code, cc-exemplo, meta, tool-configuration
---

↓ TRANSFORMAR EM ↓

# Skill do projeto (novo-projeto)
---
name: myapp-exemplo
scope: domain-implementation         # ← Mudou
target: application-feature          # ← Mudou
description: Configure application webhooks for real-time notifications
keywords: application, myapp-exemplo, webhooks, notifications, app-feature  # ← Mudou
---
```

#### Passo 5: Validar Separação

```bash
# Checklist de validação
./scripts/validate-separation.sh

# Saída esperada:
# ✅ Todos os skills têm prefixo myapp-
# ✅ Todos os commands têm prefixo myapp-
# ✅ CLAUDE.md declara escopo: domain-implementation
# ✅ Keywords não sobrepõem com meta-keywords
# ✅ Nenhum cc- permaneceu (exceto em referências)
```

---

## ✅ Checklist de Validação

### Antes de Commitar no Meta-Repo

- [ ] Todos os skills têm prefixo `cc-`
- [ ] Todos os commands têm prefixo `cc-`
- [ ] Todos os hooks têm prefixo `cc-`
- [ ] CLAUDE.md declara `scope: meta-configuration`
- [ ] Skills têm `scope: meta-configuration` em YAML
- [ ] Skills têm `target: claude-code-itself` em YAML
- [ ] Keywords incluem `claude-code`, `cc-*`, `meta-configuration`
- [ ] Nenhuma keyword genérica que possa conflitar
- [ ] Documentação inline indica "META-CONFIGURAÇÃO"

### Antes de Aplicar em Projeto

- [ ] Copiei apenas templates, NÃO estrutura completa
- [ ] Substituí TODOS os `cc-` pelo prefixo do projeto
- [ ] Criei CLAUDE.md específico do projeto
- [ ] Atualizei frontmatter: `scope: domain-implementation`
- [ ] Atualizei frontmatter: `target: application-feature`
- [ ] Substituí keywords meta por keywords de domínio
- [ ] Validei que nenhum `cc-` permaneceu
- [ ] Executei script de validação de separação
- [ ] Documentei link para meta-repo no CLAUDE.md

---

## 🎓 Exemplos Práticos

### Exemplo 1: Projeto com Google ADK

**Problema:** Google ADK usa "agents" → conflito com "agent" do Claude Code

**Solução:**
```yaml
# Meta-skill (claude-code)
---
name: cc-agent-config
keywords: claude-code, autonomous-ai, claude-agent, tool-agent
description: Configure Claude Code autonomous agent behavior
---

# Project-skill (google-adk-project)
---
name: cva-agent-types
keywords: google-adk, llm-agents, sequential-agents, parallel-agents
description: Google ADK agent types (LLM, Sequential, Parallel)
---
```

**Resultado:** Zero sobreposição de keywords = zero conflito

### Exemplo 2: Projeto com LangChain

**Problema:** LangChain usa "tools" → conflito com "tools" do Claude Code

**Solução:**
```yaml
# Meta-skill
---
name: cc-tools-reference
keywords: claude-code-tools, read-tool, write-tool, bash-tool
description: Claude Code built-in tools (Read, Write, Edit, Bash)
---

# Project-skill
---
name: lc-tools-integration
keywords: langchain-tools, external-apis, tool-calling, function-calling
description: LangChain tool integration with external APIs
---
```

### Exemplo 3: Microserviços com Múltiplos Repos

**Estrutura:**
```
workspace/
├── claude-code/              # Meta-repo (cc-)
├── payment-service/          # Serviço 1 (pay-)
├── auth-service/             # Serviço 2 (auth-)
└── notification-service/     # Serviço 3 (notif-)
```

**Prefixos únicos:**
- Meta: `cc-`
- Payment: `pay-`
- Auth: `auth-`
- Notification: `notif-`

**Resultado:** Cada repo tem namespace isolado

---

## 🔧 Ferramentas de Validação

### Script: validate-separation.sh

```bash
#!/bin/bash
# Valida separação de escopo

# Detectar contexto
if [[ "$PWD" == *"claude-code"* ]]; then
  CONTEXT="meta"
  EXPECTED_PREFIX="cc-"
else
  CONTEXT="domain"
  EXPECTED_PREFIX=$(grep "PREFIXO:" CLAUDE.md 2>/dev/null | grep -oP '`\K[^`]+' || echo "UNKNOWN")
fi

echo "🔍 Validando separação de escopo..."
echo "📍 Contexto: $CONTEXT"
echo "🏷️  Prefixo esperado: $EXPECTED_PREFIX"

# Validar skills
echo ""
echo "📦 Validando skills..."
ERRORS=0

for skill in .claude/skills/*/SKILL.md; do
  SKILL_NAME=$(basename "$(dirname "$skill")")

  # Verificar prefixo
  if [[ "$SKILL_NAME" != $EXPECTED_PREFIX* ]]; then
    echo "❌ $SKILL_NAME (deveria começar com $EXPECTED_PREFIX)"
    ((ERRORS++))
  else
    # Verificar frontmatter
    SCOPE=$(grep "^scope:" "$skill" | cut -d':' -f2 | xargs)
    TARGET=$(grep "^target:" "$skill" | cut -d':' -f2 | xargs)

    if [[ "$CONTEXT" == "meta" ]]; then
      if [[ "$SCOPE" != "meta-configuration" ]]; then
        echo "⚠️  $SKILL_NAME: scope deveria ser 'meta-configuration', não '$SCOPE'"
      fi
      if [[ "$TARGET" != "claude-code-itself" ]]; then
        echo "⚠️  $SKILL_NAME: target deveria ser 'claude-code-itself', não '$TARGET'"
      fi
    fi

    echo "✅ $SKILL_NAME"
  fi
done

if [[ $ERRORS -gt 0 ]]; then
  echo ""
  echo "❌ $ERRORS erro(s) encontrado(s)"
  exit 1
else
  echo ""
  echo "✅ Validação concluída com sucesso!"
  exit 0
fi
```

---

## 📚 Recursos Adicionais

### Documentação Relacionada

- `ARCHITECTURE_ANALYSIS.md` - Análise detalhada de riscos
- `CLAUDE.md` - Diretrizes completas do meta-repo
- `cc-overview` - Overview do Claude Code
- `cc-hooks-guide` - Guia de hooks
- `cc-skills-guide` - Guia de skills

### Links Externos

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Skills Best Practices](https://docs.claude.com/claude-code/skills)
- [Naming Conventions](https://docs.claude.com/claude-code/best-practices)

---

**🎯 Próximo Passo:**

Aplicar estas diretrizes ao criar qualquer configuração nova:
1. Identificar contexto (meta ou domínio)
2. Usar prefixo correto
3. Declarar escopo no frontmatter
4. Validar separação com script
5. Documentar no CLAUDE.md

---

**Última atualização:** 2025-10-30
**Versão:** 1.0.0
