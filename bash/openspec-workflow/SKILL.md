---
name: openspec-workflow
description: Skill de governança SDLC com OpenSpec para desenvolvimento guiado por especificação (Spec-Driven Development). Use quando precisar planejar mudanças, executar opsx-propose, estruturar proposal.md, design.md e tasks.md, validar conformidade com openspec validate --strict e gerenciar o ciclo de vida de mudanças.
license: MIT
metadata:
  author: local
  version: "1.0"
---

# Skill — OpenSpec Workflow (SDLC)

Este skill define o padrão operacional do **OpenSpec** como framework obrigatório de especificação no SDLC (Software Development Life Cycle) do projeto.

---

## 🎯 Objetivo e Princípios

O OpenSpec estabelece o desenvolvimento guiado por especificação (*Spec-Driven Development*), garantindo que:
1. **Nenhum código é escrito sem especificação prévia.**
2. **Mudanças são atômicas, rastreáveis e versionadas em `openspec/changes/<change-name>/`.**
3. **O ciclo de vida da mudança é validado mecanicamente via CLI antes e depois da implementação.**
4. **Alinhamento com o Harness Gate**: O estado da mudança é sincronizado com o CLI de fases (`scripts/harness/phase_cli.py`).

---

## 📂 Estrutura de uma Change OpenSpec

Toda proposta de mudança reside em `openspec/changes/<change-name>/` e contém 4 artefatos canônicos:

```
openspec/changes/<change-name>/
├── .openspec.yaml    ← Metadados da change (schema, data, flags)
├── proposal.md       ← Motivação, escopo, capacidades e impacto
├── design.md         ← Decisões de arquitetura, contratos e alternativas
└── tasks.md          ← Checklist determinístico organizado por fases
```

---

## 🚀 Operações do Ciclo de Vida (SDLC)

### 1. `opsx-propose` (Proposição de Mudança)

Objetivo: Criar e validar os artefatos de planejamento sem tocar em código de produção.

#### Passo a Passo:
1. **Definir nome da change**: Formato estrito em kebab-case (ex.: `adicionar-operacao-modulo`, `implementar-funcao-logaritmo`).
2. **Definir fase no harness**:
   ```bash
   python3 scripts/harness/phase_cli.py set proposal <change-name>
   ```
   *Nota: O hook `pre-tool-write-guard.py` garante que apenas caminhos de planejamento (`openspec/`, `spdd/`) possam ser editados.*
3. **Criar diretório**: `openspec/changes/<change-name>/`.
4. **Criar `.openspec.yaml`**:
   ```yaml
   schema: spec-driven
   created: YYYY-MM-DD
   skip_specs: false # ou true se for documentação/tooling pura
   ```
5. **Criar `proposal.md`**:
   - `## Why`: Por que a mudança é necessária?
   - `## What Changes`: O que muda especificamente?
   - `## Capabilities`: Novas capacidades (`### New Capabilities`) e modificadas (`### Modified Capabilities`).
   - `## Impact`: Dependências, arquivos afetados, risco.
6. **Criar `design.md`**:
   - `## Context`: Estado atual do sistema.
   - `## Architecture & Design Decisions`: Decisões técnicas (ex.: variáveis COBOL em Working-Storage, novas instruções PROCEDURE DIVISION, tratamento de erro de divisão por zero).
   - `## Trade-offs & Alternatives Considered`: Alternativas avaliadas.
7. **Criar `tasks.md`**:
   Checklist hierárquico estruturado pelas fases:
   - `## 1. Fase 1 - Propose (OpenSpec)`
   - `## 2. Fase 2 - Analysis (OpenSPDD)`
   - `## 3. Fase 3 - Canvas (OpenSPDD REASONS)`
   - `## 4. Fase 4 - Generate (Implementação COBOL)`
   - `## 5. Fase 5 - Review & Docs (Validação)`
8. **Validar a Change**:
   ```bash
   openspec validate <change-name> --strict
   ```

---

### 2. `opsx-apply` (Acompanhamento e Conclusão)

Objetivo: Validar que todas as tarefas foram cumpridas pelo agente de código e que a mudança está pronta para archive.

#### Passo a Passo:
1. O agente de implementação marca as tarefas concluídas em `tasks.md`:
   ```markdown
   - [x] 1.1 Criar proposta OpenSpec
   - [x] 2.1 Concluir análise SPDD
   - [x] 3.1 Gerar REASONS Canvas
   - [x] 4.1 Implementar em src/CALCULADORA.cbl
   - [x] 4.2 Compilar com cobc -x
   - [x] 4.3 Passar nas fitness functions (make fitness)
   ```
2. Executar validação final:
   ```bash
   openspec validate <change-name> --strict
   ```

---

### 3. `opsx-archive` (Opcional - Arquivamento)

Quando a change é finalizada e mergeada:
```bash
openspec archive <change-name>
```

---

## 🛡️ Regras de Ouro OpenSpec

1. **Nunca pule `openspec validate <change-name> --strict`**. Se a validação falhar, o plano é inválido.
2. **Kebab-case obrigatório**: Sempre use nomes em minúsculas com hífen.
3. **Tarefas atômicas**: Cada item em `tasks.md` deve ser verificável com sim/não.
4. **Zero código na proposal**: Não edite `src/` ou `docs/` durante a fase `proposal`.
