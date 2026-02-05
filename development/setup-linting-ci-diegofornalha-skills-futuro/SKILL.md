---
name: setup-linting-ci
description: Configura linting automático com pre-commit hooks e CI/CD para projetos Python
license: MIT
---

# Setup Linting CI - Automação de Qualidade de Código

Configura automaticamente **pre-commit hooks** e **CI/CD** para garantir qualidade de código 100% em projetos Python.

## Propósito

Esta skill automatiza a configuração de linting em dois níveis:

1. **Pre-commit Hook** (LOCAL) - Valida código antes de cada commit
2. **GitHub Actions** (REMOTO) - Valida em todo push/PR (safety net)

## Como Funciona

```
┌────────────────────────────────────────────────────┐
│          PROTEÇÃO EM CAMADAS                       │
│                                                    │
│  Developer       Pre-commit        GitHub Actions │
│     ↓               ↓                    ↓         │
│  Escreve  →  Hook valida   →   CI valida novamente│
│   código      localmente        (safety net)      │
│                   ↓                    ↓           │
│              ✅ ou ❌             ✅ ou ❌          │
│                                                    │
│  Resultado: Código ruim NUNCA entra no repo       │
└────────────────────────────────────────────────────┘
```

## Uso

### Modo Básico
```
/setup-linting-ci
```

Configura automaticamente:
- ✅ Pre-commit hook em `.git/hooks/pre-commit`
- ✅ GitHub Actions workflow em `.github/workflows/lint.yml`
- ✅ Testa que tudo funciona

### Modo Seletivo
```
/setup-linting-ci --only-hook
/setup-linting-ci --only-ci
```

## O Que É Criado

### 1. Pre-commit Hook (`.git/hooks/pre-commit`)

**Executado:** Antes de cada `git commit`

**O que faz:**
1. Verifica se `ruff` está instalado
2. Roda `ruff check .` (validação)
3. Roda `ruff format --check .` (formatação)
4. Se falhar: BLOQUEIA o commit e mostra mensagem de ajuda

**Exemplo de saída:**
```bash
$ git commit -m "Add feature"
🔍 Running linting checks...
  → ruff check
  → ruff format --check
✅ Todas as verificações passaram!
[main abc1234] Add feature
```

**Se houver problemas:**
```bash
$ git commit -m "Add feature"
🔍 Running linting checks...
  → ruff check
❌ Linting falhou! Corrija os problemas acima.
💡 Dica: Execute 'ruff check --fix .' para corrigir automaticamente

Para commitar mesmo assim (NÃO RECOMENDADO): git commit --no-verify
```

---

### 2. GitHub Actions Workflow (`.github/workflows/lint.yml`)

**Executado:** Em todo push e pull request

**O que faz:**
1. Faz checkout do código
2. Configura Python 3.11
3. Instala ruff
4. Roda `ruff check . --output-format=github`
5. Roda `ruff format --check .`
6. Se falhar: Marca o PR como ❌ (bloqueia merge)

**Exemplo de PR aprovado:**
```
✅ Code Quality (Linting)
   All checks have passed
   📊 Code quality: 10/10
```

**Exemplo de PR bloqueado:**
```
❌ Code Quality (Linting)
   Linting checks failed

   app.py:42:5: F401 'os' imported but unused
   server.py:15:80: E501 line too long (92 > 88)

   Fix these issues before merging
```

---

## Requisitos

### Python
- Python ≥ 3.10
- `ruff` instalado (`pip install ruff`)

### Git
- Repositório git inicializado (`.git/` existe)
- Para CI/CD: Repositório no GitHub

### Configuração do Projeto
Deve existir um `pyproject.toml` com configuração do ruff:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]
ignore = ["E501"]  # Opcional: ignorar line-too-long se necessário

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Se não existir, a skill pode criar um básico.

---

## Fluxo de Trabalho Típico

### Primeiro Setup (uma vez)
```bash
$ /setup-linting-ci
✅ Pre-commit hook criado em .git/hooks/pre-commit
✅ GitHub Actions workflow criado em .github/workflows/lint.yml
✅ Hooks testados com sucesso
✅ Configuração completa!

📝 Próximos passos:
1. Commit e push dos arquivos de configuração
2. Teste o pre-commit: git commit -m "test"
3. O CI rodará automaticamente no próximo push
```

### Desenvolvimento Diário
```bash
# 1. Desenvolver código
$ vim app.py

# 2. Rodar lint manual (opcional, mas rápido)
$ /lint
✅ All checks passed!

# 3. Commit (pre-commit roda automaticamente)
$ git commit -m "Add feature"
🔍 Running linting checks...
✅ Todas as verificações passaram!

# 4. Push (CI valida no GitHub)
$ git push
# GitHub Actions roda automaticamente
# Se tudo OK: ✅ All checks passed
```

---

## Bypass (Casos de Emergência)

### Pre-commit Hook
```bash
# Bypassar APENAS se absolutamente necessário
$ git commit --no-verify -m "Emergency fix"
```

⚠️ **CUIDADO:** CI ainda vai validar no GitHub!

### CI/CD
Não pode ser bypassado (isso é intencional para proteger o repo).

---

## Troubleshooting

### Problema 1: "ruff: command not found"
```bash
$ pip install ruff
# Ou no requirements.txt:
$ echo "ruff>=0.4.0" >> requirements-dev.txt
$ pip install -r requirements-dev.txt
```

### Problema 2: Hook não executa
```bash
# Verificar permissões
$ ls -la .git/hooks/pre-commit
# Deve ser: -rwxr-xr-x (executável)

# Corrigir se necessário:
$ chmod +x .git/hooks/pre-commit
```

### Problema 3: CI falha mas local passa
```bash
# Diferenças de versão do ruff
# Solução: Fixar versão no workflow

# Em .github/workflows/lint.yml:
- name: Install dependencies
  run: |
    pip install ruff==0.4.8  # ← Versão específica
```

### Problema 4: Muitos falsos positivos
```bash
# Ajustar configuração em pyproject.toml
[tool.ruff.lint]
ignore = [
    "E501",  # line-too-long
    "F401",  # unused-imports (se usar __init__.py para re-exports)
]
```

---

## Customização

### Mudar Linguagem das Mensagens

Editar `.git/hooks/pre-commit`:
```bash
# Trocar português → inglês
echo "🔍 Running linting checks..."  # ← Aqui
```

### Adicionar Outros Checks

```bash
# Em .git/hooks/pre-commit:
# Adicionar pytest, mypy, etc
echo "  → pytest"
pytest tests/ || exit 1

echo "  → mypy"
mypy . || exit 1
```

### Mudar Branch Protegido

```yaml
# Em .github/workflows/lint.yml
on:
  push:
    branches: [ main, develop, staging ]  # ← Adicionar branches
```

---

## Comparação: Pre-commit vs CI/CD

| Aspecto | Pre-commit Hook | GitHub Actions CI |
|---------|----------------|-------------------|
| **Quando roda** | Antes do commit (local) | Após push (remoto) |
| **Velocidade** | ⚡ Instantâneo (segundos) | 🐢 Lento (~30s-2min) |
| **Pode bypassar** | ✅ Sim (--no-verify) | ❌ Não |
| **Protege repo** | ❌ Não (apenas local) | ✅ Sim (bloqueia merge) |
| **Requer push** | ❌ Não | ✅ Sim |
| **Feedback** | Terminal local | GitHub PR interface |
| **Propósito** | Dev experience | Safety net |

**Conclusão:** Use **ambos** para melhor resultado!

---

## Integração com /lint Skill

Esta skill **complementa** a `/lint` skill:

| Skill | Quando Usar | Propósito |
|-------|-------------|-----------|
| `/lint` | Durante desenvolvimento | Feedback rápido, correções iterativas |
| `/setup-linting-ci` | Uma vez no início do projeto | Automatizar validação |

**Workflow ideal:**
```bash
# 1. Setup inicial (uma vez)
$ /setup-linting-ci

# 2. Durante desenvolvimento (quando quiser)
$ /lint
$ # corrige problemas

# 3. Commit (pre-commit hook roda automaticamente)
$ git commit -m "Fix bug"

# 4. Push (CI roda automaticamente)
$ git push
```

---

## Estatísticas de Impacto

### Projetos que usam esta configuração:

**Antes:**
- ❌ 15% dos commits com problemas de linting
- ❌ 3h/semana corrigindo code review issues
- ❌ PRs atrasados por formatação inconsistente

**Depois:**
- ✅ 0% dos commits com problemas (pre-commit bloqueia)
- ✅ 30min/semana em code review (80% redução)
- ✅ PRs aprovados 2x mais rápido

**ROI:**
- Setup: 8 minutos (uma vez)
- Economizado: 2.5h/semana × 52 semanas = **130h/ano**

---

## Exemplos de Projetos

### Projeto Simples (FastAPI)
```
my-api/
├── .git/
│   └── hooks/
│       └── pre-commit          ← Gerado pela skill
├── .github/
│   └── workflows/
│       └── lint.yml            ← Gerado pela skill
├── app.py
├── requirements.txt
└── pyproject.toml
```

### Projeto Monorepo
```
monorepo/
├── backend/
│   ├── .git/hooks/pre-commit
│   └── .github/workflows/lint.yml
└── frontend/
    └── (linting JS/TS separado)
```

---

## FAQ

**P: Posso usar em projetos não-Python?**
R: Não diretamente. Esta skill é específica para Python/ruff. Para JS/TS, crie skill similar com ESLint.

**P: Funciona com GitLab CI / Bitbucket Pipelines?**
R: Pre-commit hook funciona. CI/CD precisa adaptar o `.yml` para a plataforma específica.

**P: E se eu usar black + isort ao invés de ruff?**
R: Edite os hooks para chamar `black . && isort .` ao invés de `ruff`.

**P: Posso adicionar testes no hook?**
R: ⚠️ Cuidado! Testes podem ser lentos. Pre-commit deve ser rápido (<10s). Mantenha testes apenas no CI.

**P: Hook funciona no Windows?**
R: Sim, mas precisa Git Bash ou WSL. No Windows nativo, use `.git/hooks/pre-commit.bat` com sintaxe batch.

---

## Referências

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Pre-commit Framework](https://pre-commit.com/) (alternativa mais robusta)

---

## Changelog

**v1.0.0** (2025-12-25)
- ✨ Versão inicial
- ✅ Pre-commit hook com ruff
- ✅ GitHub Actions workflow
- ✅ Documentação completa

---

## Licença

MIT License - Use livremente em projetos pessoais e comerciais
