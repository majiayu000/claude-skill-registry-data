---
name: mutation-fuzzing-testing
description: "Especialista em Testes de Mutação (Mutation Testing), Engenharia de Fuzzing e Análise de Conformidade de Requisitos. Domina a injeção sistemática de falhas sintéticas, medição de Mutation Score, fuzzing guiado por cobertura (AFL++, libFuzzer, Atheris, Hypothesis), Test Gap Analysis e oráculos metamórficos."
---

# Mutation Testing, Fuzzing & Requirement Conformance Engineering

Esta skill orienta a inteligência artificial a conduzir testes de robustez extrema e validação de qualidade profunda utilizando **Testes de Mutação**, **Técnicas de Fuzzing** e **Auditoria de Conformidade de Requisitos**.

---

## 🧬 1. Testes de Mutação (Mutation Testing)

O Teste de Mutação avalia a eficácia real da suíte de testes introduzindo alterações pontuais sintéticas (*mutantes*) no código de produção. Se a suíte de testes passar mesmo após a alteração, o mutante **sobreviveu** (revelando um *Test Gap* de asserção fraca). Se qualquer teste falhar, o mutante foi **morto** (*Killed*).

### A. Operadores Canônicos de Mutação (Mutation Operators)
1. **AOR (Arithmetic Operator Replacement)**: Substituição de operadores aritméticos (`+` por `-`, `*` por `/`).
2. **ROR (Relational Operator Replacement)**: Substituição de operadores relacionais (`>` por `>=`, `==` por `!=`).
3. **COR (Conditional Operator Replacement)**: Inversão de operadores lógicos (`and` por `or`).
4. **SDL (Statement Deletion)**: Remoção de chamadas a métodos, atribuições ou instruções inteiras.
5. **LCR (Logical Connector Replacement)**: Negação de expressões booleanas (`if condition` vira `if not condition`).

### B. Métrica de Escore de Mutação (Mutation Score)
$$	ext{Mutation Score (MS)} = rac{	ext{Mutantes Mortos}}{	ext{Total de Mutantes} - 	ext{Mutantes Equivalentes}} 	imes 100\%$$
- **Mutante Equivalente**: Mutante sintaticamente diferente mas com comportamento semântico idêntico ao código original (deve ser desconsiderado do denominador).
- **Meta Corporativa Mínima**: $MS \ge 85\%$ para componentes críticos e $MS \ge 90\%$ para regras financeiras/segurança.

### C. Ferramental por Linguagem
- **Python**: `mutmut` (`mutmut run`, `mutmut results`, `mutmut show <id>`) e `Cosmic Ray`.
- **JavaScript / TypeScript**: `Stryker Mutator` (`npx stryker run`).
- **Java / Kotlin**: `PITest (PIT)`.
- **C / C++**: `Dextool Mutate` ou `Mull`.

---

## 💥 2. Engenharia de Fuzzing (Fuzz Testing)

O Fuzzing submete o programa a entradas semi-aleatórias, malformadas ou geradas geneticamente para detectar falhas de segurança, *panics*, estouros de memória, vazamentos e comportamentos inesperados.

### A. Tipos de Fuzzing
1. **Fuzzing Baseado em Propriedades (Property-Based Testing)**:
   - Utiliza geradores de entrada baseados em contratos (ex.: `Hypothesis` em Python, `fast-check` em JS).
   - Verifica invariantes universais (ex.: idempotência, relações inversas, limites de intervalo).
2. **Fuzzing Guiado por Cobertura (Coverage-Guided Fuzzing)**:
   - Instrumenta o código para medir blocos básicos alcançados e evolui os inputs que descobrem novos caminhos de execução.
   - Ferramentas: **libFuzzer**, **AFL++ (American Fuzzy Lop)**, **Google Atheris** (Python/C extensions).

### B. O Problema do Oráculo no Fuzzing
- **Oráculo de Falha Básica**: Detecção de crashes, *NullPointerException*, divisão por zero, loops infinitos (*Timeout*) ou uso indevido de memória (*ASan / AddressSanitizer*).
- **Oráculo Metamórfico**: Validação de propriedades de consistência relacional:
  $$f(	ext{entrada\_ordenada}) = f(	ext{entrada})$$

---

## 🎯 3. Auditoria de Conformidade com os Requisitos Iniciais

Testes com 100% de cobertura de linhas podem ainda assim violar os requisitos do sistema se validarem o comportamento errado ou deixarem critérios de aceitação de fora.

### A. Matriz de Rastreabilidade de Requisitos (RTM - Requirements Traceability Matrix)
Todo caso de teste deve estar explicitamente mapeado para um critério de aceitação original:
```text
[REQ-01: Pagamento Pix com Desconto]
├── Teste Funcional: test_pix_discount_applied_nominal()
├── Teste de Limite (BVA): test_pix_discount_boundary_values()
├── Teste de Mutação: mutante em `discount_rate` deve ser morto
└── Teste de Fuzzing: hypothesis_pix_arbitrary_amounts_never_negative()
```

### B. Test Gap Analysis
1. Identificar trechos de código com cobertura de execução verde mas com **mutantes sobreviventes**.
2. Criar asserções específicas para forçar a morte do mutante.
3. Testar se o requisito original cobre o caso de borda exposto pelo mutante.
### C. Metodologia EARS (Easy Approach to Requirements Syntax) & Testes Parametrizados
Para garantir conformidade total com os requisitos do sistema, estruture as regras de negócio nos 4 padrões sintáticos EARS antes da geração de código de teste:

1. **Ubiquitous (Onipresente)**: `The <system> shall <system response>.`
2. **Event-Driven (Disparado por Evento)**: `WHEN <trigger>, the <system> shall <system response>.`
3. **State-Driven (Orientado a Estado)**: `WHILE <in state>, the <system> shall <system response>.`
4. **Unwanted Behavior (Comportamento Indesejado / Exceção)**: `IF <trigger condition>, THEN the <system> shall <system response>.`

#### Mapeamento Mecânico EARS → Testes Parametrizados (JUnit 5 / Pytest)
Cada grupo de declarações EARS que compartilham a mesma operação de fronteira (arrange/act) é convertido deterministicamente em um teste parametrizado (`@ParameterizedTest` / `@pytest.mark.parametrize`):
- O identificador do requisito (`REQ-01`, `REQ-02`) atua como o rótulo da linha na tabela de dados.
- Elimina duplicação de asserções, garante que cada requisito tenha um caso de teste explícito e orienta a injeção de mutações focadas no critério de aceite.
