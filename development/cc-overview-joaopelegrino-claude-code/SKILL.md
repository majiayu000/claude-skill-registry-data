---
name: cc-overview
scope: meta-configuration
target: claude-code-itself
description: Comprehensive overview of Claude Code features, architecture, and capabilities. Learn about hooks, skills, commands, permissions, and best practices for configuring Claude Code as your AI development assistant. This is about the TOOL itself, not project code.
keywords: claude-code, cc-overview, meta-configuration, tool-features, hooks, skills, commands, permissions, settings, automation, ai-assistant, tool-configuration
allowed-tools: Read,Grep,Glob
---

# Claude Code: Comprehensive Overview

> **⚠️ META-CONFIGURAÇÃO**
> Este skill é sobre o PRÓPRIO Claude Code (a ferramenta de desenvolvimento com IA da Anthropic), não sobre código de projeto.

---

## 📚 O Que É Claude Code?

**Claude Code** é uma ferramenta de linha de comando (CLI) interativa da Anthropic que permite:

- 🤖 **Assistência autônoma**: Claude executa tarefas complexas com mínima supervisão
- 🔧 **Execução de ferramentas**: Read, Write, Edit, Bash, Grep, Glob, WebSearch, etc.
- 🎯 **Contexto profundo**: Entende projetos inteiros, não apenas arquivos isolados
- ⚡ **Automação**: Hooks para automatizar workflows
- 🎨 **Personalização**: Skills e commands customizados
- 🔒 **Segurança**: Sistema de permissões granular

---

## 🏗️ Arquitetura de Configuração

### Estrutura de Diretórios

```
project/
├── .claude/                          # Configuração local do projeto
│   ├── settings.json                 # Configurações e permissões
│   ├── skills/                       # Skills customizados
│   │   └── <nome-skill>/
│   │       └── SKILL.md              # Definição da skill (YAML + content)
│   ├── commands/                     # Slash commands
│   │   └── <comando>.md              # Prompt do comando
│   ├── hooks/                        # Scripts de automação
│   │   ├── bash/
│   │   └── python/
│   └── knowledge-base/               # Base de conhecimento (opcional)
│       └── <topico>/
│           └── *.md
```

### Hierarquia de Configuração

```
~/.claude/                            # Global (todos os projetos)
├── settings.json                     # Configurações padrão
├── CLAUDE.md                         # Diretrizes universais
└── plugins/                          # Plugins instalados

↓

/project/.claude/                     # Local (projeto específico)
├── settings.json                     # Sobrescreve configurações globais
└── CLAUDE.md                         # Diretrizes do projeto
```

**Precedência:** Local > Global

---

## 🎯 Componentes Principais

### 1. Settings (Configurações)

**Arquivo:** `.claude/settings.json`

**Estrutura:**
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",              // Permite git sem pedir
      "Bash(npm:*)",              // Permite npm sem pedir
      "WebSearch"                 // Permite busca web
    ],
    "deny": [
      "Bash(rm -rf /*)"           // Bloqueia comandos perigosos
    ],
    "ask": [
      "Bash(sudo:*)"              // Pede confirmação para sudo
    ],
    "additionalDirectories": [
      "/tmp",                     // Diretórios adicionais acessíveis
      "/workspace/shared"
    ]
  },
  "outputStyle": "Explanatory",   // Terse, Explanatory, Code-Only
  "hooks": {
    "SessionStart": [...],        // Hooks ao iniciar sessão
    "PostToolUse": [...],         // Hooks após usar ferramenta
    "PreToolUse": [...],          // Hooks antes de usar ferramenta
    "UserPromptSubmit": [...]     // Hooks ao submeter prompt
  },
  "alwaysThinkingEnabled": false  // Thinking tags visíveis
}
```

**Seções Importantes:**

#### Permissions (Permissões)

- **allow**: Ferramentas/comandos permitidos sem confirmação
- **deny**: Ferramentas/comandos bloqueados
- **ask**: Ferramentas/comandos que requerem confirmação
- **additionalDirectories**: Diretórios fora do projeto que Claude pode acessar

**Exemplos:**
```json
// Permitir comandos específicos
"allow": [
  "Bash(git:*)",                  // Qualquer comando git
  "Bash(npm:install)",            // npm install específico
  "Bash(python3:*.py)",           // Executar scripts Python
  "WebSearch"                     // Busca na web
]

// Bloquear comandos perigosos
"deny": [
  "Bash(rm -rf /)",
  "Bash(sudo rm:*)",
  "Bash(dd:*)"
]

// Pedir confirmação
"ask": [
  "Bash(rm:*)",                   // Qualquer rm
  "Bash(sudo:*)",                 // Qualquer sudo
  "Bash(docker:*)"                // Comandos Docker
]
```

#### Output Style (Estilo de Saída)

- **Terse**: Respostas concisas, direto ao ponto
- **Explanatory** (recomendado): Respostas educacionais com contexto
- **Code-Only**: Apenas código, sem explicações

---

### 2. Hooks (Automação)

**Hooks** são scripts executados em momentos específicos do ciclo de vida do Claude Code.

#### Tipos de Hooks

| Hook | Quando Executa | Uso Típico |
|------|----------------|------------|
| **SessionStart** | Ao iniciar/retomar sessão | Carregar contexto do projeto |
| **PreToolUse** | Antes de executar ferramenta | Validar inputs, bloquear operações |
| **PostToolUse** | Após executar ferramenta | Formatar código, git add, validar output |
| **UserPromptSubmit** | Ao enviar prompt | Enriquecer contexto, bloquear prompts perigosos |

#### Estrutura de Hook

**Exemplo: SessionStart**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/session-start.sh",
        "timeout": 5
      }]
    }]
  }
}
```

**Script: session-start.sh**
```bash
#!/bin/bash
# Adiciona contexto ao iniciar sessão

# Detectar branch Git
BRANCH=$(git branch --show-current 2>/dev/null || echo "no-git")

# Detectar linguagens
LANGUAGES=$(find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) | \
  xargs -I {} basename {} | \
  sed 's/.*\.//' | \
  sort | uniq | \
  tr '\n' ',' | \
  sed 's/,$//')

# Retornar contexto
cat <<EOF
{
  "continue": true,
  "context": "📍 Branch: $BRANCH | 🔧 Languages: $LANGUAGES"
}
EOF
```

**Exemplo: PostToolUse (Formatação Automática)**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",          // Aplica após Edit ou Write
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/bash/format-code.sh",
        "timeout": 30
      }]
    }]
  }
}
```

**Script: format-code.sh**
```bash
#!/bin/bash
# Formata código automaticamente após Edit/Write

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // ""')

# Detectar extensão
EXT="${FILE_PATH##*.}"

case "$EXT" in
  py)
    black "$FILE_PATH" 2>/dev/null
    isort "$FILE_PATH" 2>/dev/null
    ;;
  js|ts|tsx|jsx)
    prettier --write "$FILE_PATH" 2>/dev/null
    ;;
  rs)
    rustfmt "$FILE_PATH" 2>/dev/null
    ;;
esac

echo '{"continue": true}'
```

**Exemplo: PreToolUse (Validação)**
```python
#!/usr/bin/env python3
# Bloqueia escrita em arquivos sensíveis

import sys
import json

# Ler input
data = json.load(sys.stdin)
file_path = data.get("parameters", {}).get("file_path", "")

# Arquivos sensíveis
SENSITIVE_FILES = [
    ".env", ".env.local", ".env.production",
    "credentials.json", "secrets.yaml",
    "private_key.pem", "id_rsa", "id_ed25519"
]

# Verificar se é arquivo sensível
if any(sensitive in file_path for sensitive in SENSITIVE_FILES):
    print(json.dumps({
        "continue": False,
        "message": f"❌ Bloqueado: {file_path} é um arquivo sensível!"
    }))
    sys.exit(2)  # Exit code 2 = bloqueia operação

# Permitir
print(json.dumps({"continue": True}))
sys.exit(0)
```

#### Variáveis de Ambiente em Hooks

- `$CLAUDE_PROJECT_DIR`: Diretório raiz do projeto
- `$CLAUDE_SESSION_ID`: ID da sessão atual
- Variáveis padrão do shell (PATH, HOME, etc.)

---

### 3. Skills (Descoberta Automática)

**Skills** são módulos de conhecimento especializados que Claude descobre e ativa automaticamente baseado no contexto da conversa.

#### Estrutura de Skill

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md                  # Definição principal (obrigatório)
    └── auxiliary/                # Arquivos auxiliares (opcional)
        ├── examples.md
        ├── troubleshooting.md
        └── code-samples/
```

**SKILL.md:**
```yaml
---
name: nome-da-skill
description: Descrição clara e detalhada (150-300 palavras) com keywords relevantes para auto-discovery. Quanto mais específica e rica, melhor a descoberta.
keywords: keyword1, keyword2, keyword3, keyword4
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,WebSearch
---

# Título da Skill

[Conteúdo principal da skill - markdown rico]

## Seções Recomendadas

- Overview
- Quando Usar
- Exemplos de Código
- Troubleshooting
- Referências
```

#### Auto-Discovery (Descoberta Automática)

Claude ativa skills automaticamente quando:
1. Palavras-chave da `description` aparecem no contexto
2. Usuário faz pergunta relacionada ao domínio da skill
3. Tarefa atual corresponde ao escopo da skill

**Exemplo:**

```yaml
---
name: cc-hooks-guide
description: Complete guide to Claude Code hooks including SessionStart, PreToolUse, PostToolUse, and UserPromptSubmit. Learn how to create, configure, and debug hooks for automating workflows, validating inputs, formatting code, and enriching context. Covers bash, python, and JavaScript hooks with real-world examples.
keywords: hooks, automation, SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, lifecycle, validation, formatting, context
---
```

**Quando usuário pergunta:** "Como automatizo formatação de código?"
**Claude detecta:** Keywords "automation", "formatting" na description
**Claude ativa:** Skill `cc-hooks-guide` automaticamente

#### Best Practices para Skills

1. **Description Rica (150-300 palavras):**
   - Mencionar todos os casos de uso
   - Incluir keywords diversificadas
   - Ser específico sobre o escopo

2. **Keywords Estratégicas:**
   - 8-15 keywords por skill
   - Incluir sinônimos e variações
   - Evitar keywords muito genéricas

3. **Conteúdo Progressivo:**
   - Começar com overview simples
   - Progressivamente mais detalhado
   - Exemplos práticos executáveis

4. **Arquivos Auxiliares:**
   ```
   cc-hooks-guide/
   ├── SKILL.md                    # 500-1000 linhas
   └── auxiliary/
       ├── examples/               # Exemplos completos
       │   ├── session-start.md
       │   ├── posttool-format.md
       │   └── pretool-validate.md
       ├── troubleshooting.md      # Problemas comuns
       └── api-reference.md        # Referência técnica
   ```

---

### 4. Commands (Slash Commands)

**Commands** são prompts pré-definidos ativados explicitamente pelo usuário.

#### Estrutura de Command

```markdown
<!-- .claude/commands/nome-comando.md -->

# Título do Comando

> **Descrição:** Breve descrição do que o comando faz
> **Uso:** /nome-comando [argumentos]

---

## Tarefa

[Instruções detalhadas para Claude executar]

## Contexto Necessário

[Arquivos/informações que Claude deve ler]

## Resultado Esperado

[O que deve ser entregue ao final]

## Exemplos

[Exemplos de uso e saída esperada]
```

**Exemplo Real:**

```markdown
<!-- .claude/commands/cc-diagnose.md -->

# Claude Code: Diagnóstico Completo

> **Descrição:** Verifica saúde da configuração do Claude Code
> **Uso:** /cc:diagnose

---

## Tarefa

Executar diagnóstico completo da configuração do Claude Code no projeto atual.

## Passos

1. **Verificar estrutura:**
   - `.claude/` existe?
   - `settings.json` válido?
   - Estrutura de diretórios completa?

2. **Validar hooks:**
   - Hooks têm permissão de execução?
   - Scripts retornam JSON válido?
   - Timeout configurado adequadamente?

3. **Verificar skills:**
   - SKILL.md tem frontmatter YAML válido?
   - Description tem 150+ palavras?
   - Keywords não conflitam com outros projetos?

4. **Testar commands:**
   - Arquivos .md existem em .claude/commands/?
   - Formato de markdown correto?

5. **Validar permissions:**
   - Permissões allow/deny/ask configuradas?
   - Comandos perigosos bloqueados?

## Resultado Esperado

Relatório formatado:

```
🔍 Diagnóstico Claude Code
========================

✅ Estrutura: OK
✅ Settings: OK
⚠️  Hooks: 2 warnings
   - session-start.sh sem permissão +x
   - format-code.sh timeout muito baixo (10s, recomendado 30s)
✅ Skills: 5 skills válidas
✅ Commands: 3 commands válidos
✅ Permissions: OK

💡 Recomendações:
1. chmod +x .claude/hooks/bash/session-start.sh
2. Aumentar timeout em format-code.sh para 30s
3. Adicionar mais keywords em cc-overview skill
```

## Ações Automáticas

- Listar problemas encontrados
- Sugerir correções com comandos prontos
- Oferecer aplicar correções automaticamente (se permitido)
```

#### Uso de Commands

```bash
# Listar commands disponíveis
/commands

# Executar command
/cc:diagnose

# Command com argumentos
/cc:create-skill nome-da-skill
```

---

### 5. Knowledge Base (Base de Conhecimento)

**Knowledge Base** é documentação estruturada que Claude pode consultar progressivamente.

#### Estrutura Recomendada

```
.claude/knowledge-base/
├── cc-hooks-reference/
│   ├── README.md                 # Overview
│   ├── session-start.md          # SessionStart detalhado
│   ├── posttool.md               # PostToolUse detalhado
│   ├── pretool.md                # PreToolUse detalhado
│   └── examples/                 # Exemplos completos
│       ├── git-automation.md
│       ├── code-formatting.md
│       └── validation.md
├── cc-skills-reference/
│   ├── README.md
│   ├── creating-skills.md
│   ├── auto-discovery.md
│   └── best-practices.md
└── cc-best-practices/
    ├── README.md
    ├── project-structure.md
    ├── naming-conventions.md
    └── troubleshooting.md
```

#### Quando Usar Knowledge Base vs Skills

| Característica | Skill | Knowledge Base |
|----------------|-------|----------------|
| **Tamanho** | 500-2000 linhas | Sem limite, múltiplos arquivos |
| **Descoberta** | Auto-discovery baseado em keywords | Referenciado explicitamente |
| **Uso** | Contexto imediato | Consulta progressiva |
| **Formato** | YAML frontmatter + markdown | Markdown puro |
| **Propósito** | Ação/tarefa específica | Documentação aprofundada |

**Exemplo:**

```
Usuário: "Como crio um hook?"
Claude:
  1. Ativa skill cc-hooks-guide (auto-discovery)
  2. Fornece overview de 200 linhas
  3. Se usuário quer mais detalhes: "Quer que eu consulte a documentação completa?"
  4. Se sim: Read .claude/knowledge-base/cc-hooks-reference/README.md
  5. Fornece resposta aprofundada
```

---

## 🔧 Ferramentas Disponíveis

Claude Code tem acesso a ferramentas poderosas:

### Read (Ler Arquivos)

```
Usa-se: Ler código, configurações, documentação

Características:
- Lê qualquer arquivo do projeto
- Suporta offset/limit para arquivos grandes
- Lê imagens (PNG, JPG)
- Lê PDFs
- Lê Jupyter notebooks (.ipynb)

Exemplo:
Read(file_path="/project/src/main.py")
```

### Write (Escrever Arquivos)

```
Usa-se: Criar arquivos novos

Características:
- Cria arquivos do zero
- Sobrescreve se já existir (cuidado!)
- Preferir Edit para modificar arquivos existentes

Exemplo:
Write(file_path="/project/new-file.py", content="código aqui")
```

### Edit (Editar Arquivos)

```
Usa-se: Modificar arquivos existentes

Características:
- Substituição exata de string
- Preserva indentação
- Mais seguro que Write para arquivos existentes

Exemplo:
Edit(
  file_path="/project/main.py",
  old_string="def old_function():\n    pass",
  new_string="def new_function():\n    return True"
)
```

### Bash (Executar Comandos)

```
Usa-se: Git, npm, build, testes, etc.

Características:
- Shell persistente (mantém estado)
- Timeout configurável
- Pode executar em background
- Sujeito a permissões

Exemplo:
Bash(command="git status", description="Check git status")
```

### Grep (Busca em Código)

```
Usa-se: Buscar padrões em múltiplos arquivos

Características:
- Ripgrep (rg) otimizado
- Suporta regex
- Filtragem por glob pattern
- Contexto (-A, -B, -C)

Exemplo:
Grep(
  pattern="function.*authenticate",
  glob="*.py",
  output_mode="content"
)
```

### Glob (Buscar Arquivos)

```
Usa-se: Encontrar arquivos por padrão

Características:
- Glob patterns (**, *, ?)
- Ordenado por data de modificação
- Rápido (otimizado para grandes codebases)

Exemplo:
Glob(pattern="**/*.test.js")
```

### WebSearch (Busca na Web)

```
Usa-se: Pesquisar documentação, erros, etc.

Características:
- Acesso a informações atualizadas
- Filtrar por domínio
- Requer permissão

Exemplo:
WebSearch(query="Claude Code hooks documentation 2025")
```

### WebFetch (Buscar URL)

```
Usa-se: Ler conteúdo de URLs específicas

Características:
- Converte HTML para Markdown
- Processa com prompt
- Cache de 15 minutos

Exemplo:
WebFetch(
  url="https://docs.claude.com/claude-code/hooks",
  prompt="Extract all hook types and their descriptions"
)
```

---

## 🎯 Workflows Comuns

### Workflow 1: Configuração Inicial

```
1. Criar estrutura:
   mkdir -p .claude/{skills,commands,hooks/{bash,python},knowledge-base}

2. Criar settings.json:
   Write(.claude/settings.json) com configurações básicas

3. Criar CLAUDE.md:
   Write(CLAUDE.md) com diretrizes do projeto

4. Adicionar hooks essenciais:
   - session-start.sh (contexto)
   - posttool-git-add.sh (auto-add)
   - pretool-validate.py (segurança)

5. Criar primeira skill:
   - Skill de overview do projeto

6. Testar:
   /cc:diagnose
```

### Workflow 2: Adicionar Nova Skill

```
1. Criar diretório:
   mkdir .claude/skills/minha-skill

2. Criar SKILL.md:
   Write(.claude/skills/minha-skill/SKILL.md)
   - YAML frontmatter completo
   - Description rica (150+ palavras)
   - 8-15 keywords
   - Conteúdo estruturado

3. Testar auto-discovery:
   - Fazer pergunta relacionada
   - Verificar se skill é ativada

4. Adicionar documentação detalhada:
   - Criar auxiliary/ se necessário
   - Adicionar exemplos
   - Troubleshooting
```

### Workflow 3: Debugar Hooks

```
1. Verificar permissões:
   ls -la .claude/hooks/**/*
   chmod +x .claude/hooks/bash/*.sh

2. Testar hook manualmente:
   echo '{"parameters": {}}' | .claude/hooks/bash/meu-hook.sh

3. Verificar JSON de saída:
   Deve retornar: {"continue": true} ou {"continue": false, "message": "..."}

4. Verificar timeout:
   Hook deve executar em < timeout configurado

5. Verificar logs:
   Executar Claude Code com --debug (se disponível)

6. Validar settings.json:
   Hook está registrado corretamente?
   Matcher está correto?
```

---

## 📚 Recursos de Aprendizado

### Documentação Oficial

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Hooks Reference](https://docs.claude.com/claude-code/hooks)
- [Skills Guide](https://docs.claude.com/claude-code/skills)
- [Commands Tutorial](https://docs.claude.com/claude-code/commands)
- [Settings Reference](https://docs.claude.com/claude-code/settings)

### Skills Deste Meta-Repo

- `cc-hooks-guide` - Guia completo de hooks
- `cc-skills-guide` - Guia de criação de skills
- `cc-commands-guide` - Guia de criação de commands
- `cc-permissions-guide` - Configuração de permissões
- `cc-optimization` - Otimização de performance
- `cc-separation-guide` - Separação meta vs domínio

### Knowledge Base Deste Meta-Repo

```
.claude/knowledge-base/
├── cc-hooks-reference/         # Documentação detalhada de hooks
├── cc-skills-reference/        # Documentação detalhada de skills
├── cc-commands-reference/      # Documentação detalhada de commands
└── cc-best-practices/          # Melhores práticas
```

---

## 🚨 Troubleshooting Comum

### Problema: Hook não executa

**Verificações:**
1. Permissão de execução: `chmod +x .claude/hooks/bash/meu-hook.sh`
2. Shebang correto: `#!/bin/bash` ou `#!/usr/bin/env python3`
3. Registrado em settings.json
4. Matcher correto (Edit, Write, etc.)
5. Timeout suficiente

**Teste manual:**
```bash
echo '{"parameters": {"file_path": "test.py"}}' | .claude/hooks/bash/meu-hook.sh
```

### Problema: Skill não ativa automaticamente

**Verificações:**
1. Description tem 150+ palavras?
2. Keywords cobrem variações do termo?
3. YAML frontmatter está válido?
4. Nome da skill segue convenção (cc- para meta)?

**Teste:**
```
Fazer pergunta explícita:
"Pode consultar a skill cc-nome-da-skill?"
```

### Problema: Command não encontrado

**Verificações:**
1. Arquivo está em `.claude/commands/`?
2. Extensão é `.md`?
3. Nome do arquivo == nome do comando?
4. Formato markdown correto?

**Listar commands:**
```
/commands
```

### Problema: Permissão negada

**Verificações:**
1. Comando está em `permissions.allow`?
2. Comando não está em `permissions.deny`?
3. Padrão glob está correto? (`git:*` vs `git`)

**Exemplo:**
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)"              // Permite QUALQUER git
    ]
  }
}
```

---

## 🎓 Próximos Passos

### Para Aprender Mais

1. **Explorar outras skills:**
   ```
   /cc:list-skills
   ```

2. **Ler knowledge base:**
   ```
   Perguntar: "Pode me mostrar a documentação de hooks?"
   Claude lê: .claude/knowledge-base/cc-hooks-reference/
   ```

3. **Executar diagnóstico:**
   ```
   /cc:diagnose
   ```

4. **Criar sua primeira skill:**
   ```
   /cc:create-skill minha-skill
   ```

### Para Contribuir

- Reportar bugs ou sugestões
- Adicionar skills úteis ao meta-repo
- Melhorar documentação
- Compartilhar hooks/commands úteis

---

## 📞 Suporte

Para ajuda adicional:

1. **Perguntar ao Claude:**
   ```
   "Como faço [tarefa] no Claude Code?"
   ```

2. **Consultar documentação:**
   ```
   https://docs.claude.com/claude-code
   ```

3. **Executar diagnóstico:**
   ```
   /cc:diagnose
   ```

4. **Ler skills relacionadas:**
   - cc-hooks-guide
   - cc-skills-guide
   - cc-troubleshooting

---

**Última atualização:** 2025-10-30
**Versão:** 1.0.0
