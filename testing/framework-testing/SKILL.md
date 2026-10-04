---
name: "framework-testing"
description: "Especialista em Engenharia de Testes de Software. Domínio abrangente de técnicas de Caixa-Preta (BVA, Partições de Equivalência, Tabelas de Decisão, FSM, Pairwise), Caixa-Branca (CFG, McCabe, MC/DC, Fluxo de Dados/du-paths, Program Slicing), Teste de Mutação, Integração (Call Graph, MM-Paths), TDD e Gestão de Testes ISTQB."
---

# Habilidade de IA: Engenharia de Testes (Testing Specialist)

Esta skill orienta a inteligência artificial a agir como especialista de nível sênior em **Engenharia e Qualidade de Testes de Software**, fundamentada nos corpos de conhecimento clássicos e acadêmicos: **Paul C. Jorgensen** (*Software Testing: A Craftsman's Approach*), **Ali Mili & Fairouz Tchier** (*Software Testing: Concepts and Operations*) e **Brian Hambling et al.** (*Software Testing: ISTQB/ISEB Guide*).

O objetivo é projetar, arquitetar e implementar suítes de testes rigorosas, balanceadas e matematicamente fundamentadas para garantir que nenhuma regressão atinja o ambiente de produção.

---

## 🧭 Fundamentos e Princípios de Engenharia de Testes

### 1. Cadeia de Propagação: Defeito, Erro e Falha
- **Defeito (Fault / Bug)**: Anomalia estática presente no código-fonte ou especificação gerada por um engano humano.
- **Erro (Error)**: Estado intermediário incorreto do sistema durante a execução decorrente de um defeito ativado.
- **Falha (Failure)**: Desvio externamente observável entre o comportamento esperado pelo oráculo e a saída/resultado real do sistema.

### 2. O Problema do Oráculo (The Oracle Problem)
Um **Oráculo de Teste** é qualquer mecanismo capaz de determinar se a saída gerada pelo programa sob teste está correta para uma dada entrada.
- Quando o oráculo direto é viável: Asserções explícitas, valores nominais e contratos.
- Quando o oráculo direto é ausente ou caro: Aplicação de **Testes Metamórficos (Metamorphic Testing)** através de relações relacionais ($f(k \cdot x) = k \cdot f(x)$) e **Property-Based Testing**.

### 3. A Pirâmide de Testes e Estratégia de Isolamento
- **Testes Unitários (70-80%)**: Testam unidades atômicas no nível de método ou classe com isolamento total via Mocks, Stubs e Spies.
- **Testes de Integração (15-20%)**: Testam a colaboração inter-módulos e inter-classes usando Grafo de Chamadas e MM-Paths.
- **Testes Ponta a Ponta / E2E (5-10%)**: Testam fluxos de usuário completos (Testes Atômicos de Sistema) em ambiente integrado.

---

## 📐 Técnicas Formais de Caixa-Preta (Funcionais)

Consulte o guia completo em [black-box-techniques.md](./references/black-box-techniques.md).

### 1. Análise de Valor Limite (Boundary Value Analysis - BVA)
Para cada variável contínua em $[a, b]$, amostre os pontos canônicos:
- $a$ ($min$), $a^+$ ($min+$), $nom$ ($nominal$), $b^-$ ($max-$), $b$ ($max$), $a^-$ ($min-$), $b^+$ ($max+$).
- **BVA Tradicional ($4n + 1$)**: Hipótese de falha simples dentro dos limites válidos.
- **BVA de Robustez ($6n + 1$)**: Testa limites válidos e valores imediatamente fora do domínio para validar tratamento de exceções.
- **BVA de Pior Caso (Worst-Case - $5^n$)**: Produto cartesiano de todos os 5 pontos em todas as $n$ variáveis para detectar falhas por interações múltiplas.
- **BVA de Pior Caso Robusto ($7^n$)**: Combinação exaustiva de valores válidos e inválidos.

### 2. Partições de Equivalência (Equivalence Partitioning)
- **Normal Fraca**: 1 valor de cada classe válida (hipótese de falha simples).
- **Normal Forte**: Produto cartesiano de todas as partições válidas (interações).
- **Robusta Fraca**: Cobre classes inválidas isoladamente, uma por teste.
- **Robusta Forte**: Combinação cartesiana de todas as partições válidas e inválidas.

### 3. Tabelas de Decisão (Decision Tables)
- Mapeamento completo de combinações booleanas para regras de negócio intrincadas.
- Aplicação de álgebra booleana para simplificação por "Don't Care" ($-$) e verificação de completude e consistência das regras.

### 4. Máquinas de Estados Finitos (FSM) e Teste Combinatorial (Pairwise)
- **Cobertura de Transições (0-switch)** e **Pares de Transições (1-switch)** para sistemas reativos orientados a eventos.
- **All-Pairs / Matrizes Ortogonais**: Redução exponencial de combinações de parâmetros garantindo 100% de cobertura de pares de interação ($t=2$).

---

## 🔬 Técnicas Formais de Caixa-Branca (Estruturais)

Consulte o guia completo em [white-box-and-dataflow.md](./references/white-box-and-dataflow.md).

### 1. Grafo de Fluxo de Controle (CFG) e Complexidade Ciclomática
- **Complexidade Ciclomática de McCabe**: $V(G) = e - n + 2p$ ou $V(G) = d + 1$ (onde $d$ é o número de nós de predicado).
- **Teste de Caminhos Básicos (Basis Path Testing)**: Construção de um conjunto de $V(G)$ caminhos linearmente independentes na base do grafo.

### 2. Hierarquia de Cobertura Estrutural
- **Statement ($C_0$)**: 100% das instruções executadas.
- **Branch / Decision ($C_1$)**: 100% dos ramos condicionais (Verdadeiro e Falso) exercitados.
- **Modified Condition/Decision Coverage (MC/DC)**: Cada condição atômica dentro de uma expressão booleana composta demonstra alterar de forma independente o resultado final. Exigido para sistemas críticos de alta confiabilidade.

### 3. Teste de Fluxo de Dados (Data Flow Testing)
- Análise de pares de definição e uso: $\text{def}(v, n)$ e $\text{use}(v, n)$ ($\text{c-use}$ computacional e $\text{p-use}$ de predicado).
- Critérios de cobertura: **All-Defs**, **All-Uses** e **All-DU-Paths** (todos os caminhos simples livres de definição entre criação e uso).

### 4. Fatiamento de Programas (Program Slicing)
- **Static Slicing**: Identificação das instruções que impactam uma variável em determinado ponto do código para isolamento seguro de suítes de regressão.
- **Dynamic Slicing**: Rastreamento da fatia ativada durante execuções com falha para localização automática da causa-raiz do defeito.

---

## 🧬 Teste de Mutação e Modelos de Confiabilidade

Consulte o guia completo em [mutation-and-fault-based-testing.md](./references/mutation-and-fault-based-testing.md).

- **Escore de Mutação ($MS$)**:
  $$MS(T, P) = \frac{\text{Mutantes Mortos}}{\text{Total de Mutantes} - \text{Mutantes Equivalentes}} \times 100\%$$
- **Operadores de Mutação**: AOR (Aritméticos), ROR (Relacionais), COR (Condicionais), SDL (Deleção de Instruções).
- **Modelo de Semeadura de Defeitos de Mills (Captura-Recaptura)**:
  $$\hat{N} = \frac{n \cdot S}{s} \implies N_{\text{residual}} = n \left(\frac{S}{s} - 1\right)$$

---

## 🏗️ Estratégias de Integração e Orientação a Objetos

Consulte o guia completo em [integration-and-system-testing.md](./references/integration-and-system-testing.md).

- **Integração por Grafo de Chamadas**: Pairwise Integration e Neighborhood Integration em vez de decomposição estática ingênua.
- **MM-Paths (Method-to-Method Paths)**: Cadeias de execução de métodos inter-classes disparadas por mensagens.
- **Testes OO**: Mitigação para armadilhas de Herança (Flattening de testes), Polimorfismo (Matrizes de Ligação Dinâmica) e Estado de Objeto.

---

## 📋 Documentos de Referência Aprofundada

1. [Técnicas de Caixa-Preta (BVA, Partições, Tabelas de Decisão, FSM, Pairwise)](./references/black-box-techniques.md)
2. [Teste Estrutural, Complexidade de McCabe, MC/DC e Fluxo de Dados](./references/white-box-and-dataflow.md)
3. [Teste de Mutação, Semeadura de Defeitos e Testes Metamórficos](./references/mutation-and-fault-based-testing.md)
4. [Estratégias de Integração, MM-Paths e Testes OO](./references/integration-and-system-testing.md)
5. [Gestão de Testes, Revisões Estáticas e ISTQB](./references/istqb-test-management-and-reviews.md)

---

## 🛠️ Exemplo Prático: BVA + Tabela de Decisão em TypeScript

```typescript
import { describe, it, expect } from 'vitest';

// Função de cálculo de desconto e elegibilidade
export interface DiscountInput {
  customerAge: number;   // Limites válidos: [18, 100]
  cartValue: number;     // Limites válidos: [1, 10000]
  isLoyalMember: boolean;
}

export function calculateDiscount(input: DiscountInput): number {
  if (input.customerAge < 18 || input.customerAge > 100) {
    throw new Error('Idade fora do intervalo permitido [18, 100].');
  }
  if (input.cartValue < 1 || input.cartValue > 10000) {
    throw new Error('Valor do carrinho fora do intervalo [1, 10000].');
  }

  if (input.isLoyalMember && input.cartValue >= 1000) {
    return 0.20; // 20% desconto
  }
  if (input.isLoyalMember || input.customerAge >= 60) {
    return 0.10; // 10% desconto
  }
  return 0.0;
}

describe('calculateDiscount - BVA & Decision Table Tests', () => {
  // 1. Testes de Robustez nos Limites de Idade [18, 100]
  it.each([
    { age: 17, cart: 500, loyal: false, error: true },   // min- (Robusto Inválido)
    { age: 18, cart: 500, loyal: false, expected: 0.0 }, // min
    { age: 19, cart: 500, loyal: false, expected: 0.0 }, // min+
    { age: 99, cart: 500, loyal: false, expected: 0.10 },// max- (Idoso)
    { age: 100, cart: 500, loyal: false, expected: 0.10 },// max
    { age: 101, cart: 500, loyal: false, error: true },  // max+ (Robusto Inválido)
  ])('valida limites de idade (BVA): age=$age', ({ age, cart, loyal, expected, error }) => {
    if (error) {
      expect(() => calculateDiscount({ customerAge: age, cartValue: cart, isLoyalMember: loyal })).toThrow();
    } else {
      const discount = calculateDiscount({ customerAge: age, cartValue: cart, isLoyalMember: loyal });
      expect(discount).toBe(expected);
    }
  });

  // 2. Testes de Regras da Tabela de Decisão
  it('aplica 20% de desconto para membro fiel com carrinho >= 1000', () => {
    const discount = calculateDiscount({ customerAge: 30, cartValue: 1000, isLoyalMember: true });
    expect(discount).toBe(0.20);
  });
});
```

---

## 🔗 Integração com Outras Skills
- [qa-engineer](../../roles/qa-engineer/SKILL.md): Planejamento e orquestração de qualidade e relatórios de defeitos.
- [framework-pytest](../framework-testing-python/SKILL.md): Automação de testes em Python com fixtures e testes parametrizados formais.
- [framework-unittest](../framework-testing-python/SKILL.md): Testes unitários com classes TestCase estruturadas.
- [framework-jest](../framework-testing-javascript/SKILL.md) / [framework-mocha](../framework-testing-javascript/SKILL.md): Automação em ecossistemas JS/TS.
- [framework-criterion](../framework-criterion/SKILL.md): Testes em baixo nível para linguagens compiladas C/C++.
