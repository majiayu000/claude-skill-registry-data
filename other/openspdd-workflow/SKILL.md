---
name: openspdd-workflow
description: Skill de engenharia de prompts estruturados via OpenSPDD (Spec-Driven Prompt Development / REASONS Canvas). Use quando precisar conduzir a análise estratégica de uma proposta OpenSpec (spdd-analysis), transformar análise em um REASONS Canvas executável (spdd-reasons-canvas) ou governar a geração de código mecânica sem alucinações (spdd-generate).
license: MIT
metadata:
  author: local
  version: "1.0"
---

# Skill — OpenSPDD Workflow (REASONS Canvas)

Este skill define o padrão do **OpenSPDD** (Spec-Driven Prompt Development), a metodologia de transição entre a especificação arquitetural e a geração determinística de código COBOL.

---

## 🎯 Por que OpenSPDD?

Em linguagens antigas e de formato estrito como COBOL (onde um erro na coluna 7 ou 11 quebra o compilador), pedir para uma IA "gerar o código diretamente" causa alucinações de formatação e quebra de regras.

O OpenSPDD resolve isso dividindo o processo em 3 operações:
1. **`spdd-analysis`**: Analisa a proposta OpenSpec e disseca as 4 divisões COBOL, variáveis e riscos.
2. **`spdd-reasons-canvas`**: Converte a análise num contrato executável rígido de 7 dimensões (**REASONS**).
3. **`spdd-generate`**: Executa as operações do Canvas com tolerância zero a desvios e validação mecânica imediata.

---

## 🔄 As Três Operações do OpenSPDD

```
┌────────────────────────────────────────────────────────┐
│                   CICLO OPENSPDD                       │
├────────────────────────────────────────────────────────┤
│ 1. spdd-analysis        (openspec/change/ → Análise)   │
│ 2. spdd-reasons-canvas  (Análise → REASONS Canvas)     │
│ 3. spdd-generate        (REASONS Canvas → Código COBOL)│
└────────────────────────────────────────────────────────┘
```

---

### Operação 1: `spdd-analysis /openspec/change/{proposta}`

**Agente executor:** `cobol-planner.agent`  
**Destino do arquivo:** `spdd/analysis/{ID}-[Analysis]-{proposta}.md`  
*(Convenção de ID: `COB-XXX-YYYYMMDDHHmm`, ex.: `COB-001-202609061730-[Analysis]-modulo.md`)*

#### O que faz:
1. Lê integralmente os artefatos da change OpenSpec (`proposal.md`, `design.md`, `tasks.md`).
2. Lê o código atual em `src/CALCULADORA.cbl` e as regras em `AGENTS.md`.
3. Elabora a análise cobrindo 4 seções:
   - **1. Contexto e Objetivos**: Resumo executivo da mudança e valor de negócio.
   - **2. Inventário Conceitual COBOL**:
     - `IDENTIFICATION DIVISION`: `PROGRAM-ID`, autor, data.
     - `ENVIRONMENT DIVISION`: configurações de máquina.
     - `DATA DIVISION (WORKING-STORAGE)`: novas variáveis `WS-`, cláusulas `PIC` (ex.: `9(5)`, `S9(10)`), níveis (01, 77).
     - `PROCEDURE DIVISION`: parágrafos a criar/modificar, instruções aritméticas (`ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `COMPUTE`), pontos de decisão e `PERFORM`.
   - **3. Riscos, Ambiguidade e Salvaguardas**: Limite de 72 colunas, transbordamento de picture (`ON SIZE ERROR`), divisão por zero, compatibilidade com compilador GnuCOBOL.
   - **4. Rastreabilidade de Quality Gates**: Fitness functions impactadas, comandos de compilação e teste.

---

### Operação 2: `spdd-reasons-canvas /spdd/analysis/{analysis}`

**Agente executor:** `cobol-planner.agent`  
**Destino do arquivo:** `spdd/prompt/{ID}-[Code]-{proposta}.md`

#### O que faz:
Transforma a análise estratégica no prompt estruturado canônico **REASONS Canvas**:

```markdown
# REASONS Canvas — [Nome da Feature]

**ID:** COB-XXX-YYYYMMDDHHmm-[Code]-[proposta]  
**Data:** YYYY-MM-DD  
**Origem:** spdd/analysis/[arquivo-de-analise].md  
**Alvo:** src/CALCULADORA.cbl  

---

## 1. Requirements (Requisitos)
- REQ-01: Descrição do cálculo matemático exato.
- REQ-02: Entrada de dados via ACCEPT e saída formatada com PIC Z ou PIC -.
- REQ-03: Não quebrar nenhuma operação existente (soma, subtração, divisão, etc.).
- REQ-04: Passar nas 13 fitness functions de arquitetura (make fitness).

## 2. Entities (Entidades COBOL)
- Arquivo alvo: src/CALCULADORA.cbl
- Novas variáveis Working-Storage:
  - WS-VARIAVEL-X: PIC 9(5) VALUE ZEROS.
- Parágrafos afetados: PROCESSAR-OPCAO, CALCULAR-OPERACAO.

## 3. Approach (Abordagem)
- Sequência de passos para a implementação do código sem replanejar.

## 4. Structure (Estrutura e Colunas)
- Colunas 1-6: Vazio
- Coluna 7: Espaço (ou '*' para comentários)
- Área A (colunas 8-11): Declarações de nível 01, nomes de SECTION e parágrafos.
- Área B (colunas 12-72): Sentenças COBOL, DISPLAY, ACCEPT, COMPUTE, PERFORM.

## 5. Operations (Operações de Execução para o Coder)
- OP-01: Transicionar fase do harness com `python3 scripts/harness/phase_cli.py set apply <proposta>`.
- OP-02: Adicionar a nova opção no menu DISPLAY.
- OP-03: Declarar as novas variáveis na WORKING-STORAGE SECTION.
- OP-04: Implementar o parágrafo de cálculo na PROCEDURE DIVISION.
- OP-05: Executar compilação com `make build` (ou cobc -x).
- OP-06: Executar sensores de arquitetura com `make fitness`.
- OP-07: Executar teste funcional com `make smoke-test`.
- OP-08: Atualizar tarefas em `openspec/changes/<proposta>/tasks.md` e rodar `openspec validate <proposta> --strict`.

## 6. Norms (Normas e Convenções)
- Ponto final obrigatório ao fim de cada sentença.
- Nomes em MAIÚSCULAS com hífens.
- Prefixo WS- para variáveis de Working Storage.
- Comentários em português iniciando na coluna 7.

## 7. Safeguards (Salvaguardas de Qualidade)
- Rollback: git checkout -- src/CALCULADORA.cbl em caso de falha irreversível.
- Gate de compilação: cobc -x deve retornar exit code 0.
- Gate de arquitetura: make fitness deve retornar 13/13 OK.
```

---

### Operação 3: `spdd-generate /spdd/prompt/{reasons-canvas}`

**Agente executor:** `cobol-coder.agent`

#### O que faz:
1. **Desbloqueia o Gate de Fase**:
   ```bash
   python3 scripts/harness/phase_cli.py set apply <proposta>
   ```
2. **Lê o REASONS Canvas**: Carrega o arquivo `spdd/prompt/{reasons-canvas}`.
3. **Executa as Operações**: Segue a lista `Operations` de forma determinística, linha a linha.
4. **Executa os Sensores**:
   ```bash
   make build        # cobc -x -o calculadora src/CALCULADORA.cbl
   make fitness      # python3 -m unittest discover -s tests/fitness
   make smoke-test   # ./calculadora com input simulado
   ```
5. **Atualiza a Especificação**: Marca as caixas em `openspec/changes/{proposta}/tasks.md` e valida:
   ```bash
   openspec validate <proposta> --strict
   ```
6. **Emite Handoff**: Sugere handoff para o `cobol-reviewer.agent`.

---

## 🛡️ Benefícios do Fluxo no SDLC

| Benefício | Sem OpenSPDD | Com OpenSPDD |
|-----------|--------------|--------------|
| **Formatação de Colunas** | Fácil quebrar colunas 8/12/72 | Definida estritamente na seção Structure |
| **Alucinação de Lógica** | Agente decide lógica no impulso | Agente segue as Operations do Canvas |
| **Rastreabilidade** | Código sem vínculo com a spec | ID único liga Spec → Análise → Canvas → Código |
| **Segurança de Fase** | Edições prematuras bloqueadas | Escrita só é liberada com transição para `apply` |
