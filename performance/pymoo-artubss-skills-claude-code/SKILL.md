---
name: pymoo
description: "Framework de otimização multi-objetivo. NSGA-II, NSGA-III, MOEA/D, frentes de Pareto, tratamento de restrições, benchmarks (ZDT, DTLZ), para problemas de design e otimização em engenharia."
---

# Pymoo - Otimização Multi-Objetivo em Python

## Visão Geral

Pymoo é um framework Python abrangente para otimização com ênfase em problemas multi-objetivo. Resolva otimização com um ou múltiplos objetivos usando algoritmos de ponta (NSGA-II/III, MOEA/D), problemas de benchmark (ZDT, DTLZ), operadores genéticos personalizáveis e métodos de decisão multi-critério. Excele em encontrar soluções de trade-off (frentes de Pareto) para problemas com objetivos conflitantes.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Resolvendo problemas de otimização com um ou múltiplos objetivos
- Encontrando soluções Pareto-ótimas e analisando trade-offs
- Implementando algoritmos evolutivos (GA, DE, PSO, NSGA-II/III)
- Trabalhando com problemas de otimização com restrições
- Comparando algoritmos em problemas de teste padrão (ZDT, DTLZ, WFG)
- Personalizando operadores genéticos (crossover, mutação, seleção)
- Visualizando resultados de otimização em alta dimensão
- Tomando decisões entre múltiplas soluções competindo
- Tratando problemas com variáveis binárias, discretas, contínuas ou mistas

## Conceitos Fundamentais

### A Interface Unificada

Pymoo usa uma função consistente `minimize()` para todas as tarefas de otimização:

```python
from pymoo.optimize import minimize

result = minimize(
    problem,        # O que otimizar
    algorithm,      # Como otimizar
    termination,    # Quando parar
    seed=1,
    verbose=True
)
```

**O objeto resultado contém:**
- `result.X`: Variáveis de decisão da(s) solução(ões) ótima(s)
- `result.F`: Valores de objetivo da(s) solução(ões) ótima(s)
- `result.G`: Violações de restrições (se houver restrições)
- `result.algorithm`: Objeto do algoritmo com histórico

### Tipos de Problema

**Mono-objetivo:** Um objetivo para minimizar/maximizar
**Multi-objetivo:** 2-3 objetivos conflitantes → Frente de Pareto
**Muitos-objetivos:** 4+ objetivos → Frente de Pareto de alta dimensão
**Com restrições:** Objetivos + restrições de desigualdade/igualdade
**Dinâmico:** Objetivos ou restrições variando no tempo

## Fluxos de Trabalho Rápidos

### Fluxo de Trabalho 1: Otimização Mono-Objetivo

**Quando:** Otimizando uma função objetivo

**Passos:**
1. Defina ou selecione o problema
2. Escolha um algoritmo mono-objetivo (GA, DE, PSO, CMA-ES)
3. Configure critérios de término
4. Execute a otimização
5. Extraia a melhor solução

**Exemplo:**
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize

# Problema integrado
problem = get_problem("rastrigin", n_var=10)

# Configure Algoritmo Genético
algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True
)

# Otimize
result = minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    seed=1,
    verbose=True
)

print(f"Melhor solução: {result.X}")
print(f"Melhor objetivo: {result.F[0]}")
```

**Veja:** `scripts/single_objective_example.py` para exemplo completo

### Fluxo de Trabalho 2: Otimização Multi-Objetivo (2-3 objetivos)

**Quando:** Otimizando 2-3 objetivos conflitantes, precisa da frente de Pareto

**Escolha de algoritmo:** NSGA-II (padrão para bi/tri-objetivo)

**Passos:**
1. Defina problema multi-objetivo
2. Configure NSGA-II
3. Execute otimização para obter frente de Pareto
4. Visualize trade-offs
5. Aplique decisão (opcional)

**Exemplo:**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Problema de benchmark bi-objetivo
problem = get_problem("zdt1")

# Algoritmo NSGA-II
algorithm = NSGA2(pop_size=100)

# Otimize
result = minimize(problem, algorithm, ('n_gen', 200), seed=1)

# Visualize frente de Pareto
plot = Scatter()
plot.add(result.F, label="Frente Obtida")
plot.add(problem.pareto_front(), label="Frente Verdadeira", alpha=0.3)
plot.show()

print(f"Encontradas {len(result.F)} soluções Pareto-ótimas")
```

**Veja:** `scripts/multi_objective_example.py` para exemplo completo

### Fluxo de Trabalho 3: Otimização com Muitos-Objetivos (4+ objetivos)

**Quando:** Otimizando 4 ou mais objetivos

**Escolha de algoritmo:** NSGA-III (projetado para muitos objetivos)

**Diferença principal:** Deve fornecer direções de referência para orientar a população

**Passos:**
1. Defina problema com muitos-objetivos
2. Gere direções de referência
3. Configure NSGA-III com direções de referência
4. Execute a otimização
5. Visualize usando Gráfico de Coordenadas Paralelas

**Exemplo:**
```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP

# Problema com muitos-objetivos (5 objetivos)
problem = get_problem("dtlz2", n_obj=5)

# Gere direções de referência (obrigatório para NSGA-III)
ref_dirs = get_reference_directions("das-dennis", n_dim=5, n_partitions=12)

# Configure NSGA-III
algorithm = NSGA3(ref_dirs=ref_dirs)

# Otimize
result = minimize(problem, algorithm, ('n_gen', 300), seed=1)

# Visualize com Coordenadas Paralelas
plot = PCP(labels=[f"f{i+1}" for i in range(5)])
plot.add(result.F, alpha=0.3)
plot.show()
```

**Veja:** `scripts/many_objective_example.py` para exemplo completo

### Fluxo de Trabalho 4: Definição de Problema Personalizado

**Quando:** Resolvendo problema de otimização específico do domínio

**Passos:**
1. Estenda a classe `ElementwiseProblem`
2. Defina `__init__` com dimensões e limites do problema
3. Implemente método `_evaluate` para objetivos (e restrições)
4. Use com qualquer algoritmo

**Exemplo sem restrições:**
```python
from pymoo.core.problem import ElementwiseProblem
import numpy as np

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,              # Número de variáveis
            n_obj=2,              # Número de objetivos
            xl=np.array([0, 0]),  # Limites inferiores
            xu=np.array([5, 5])   # Limites superiores
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Defina objetivos
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0]-1)**2 + (x[1]-1)**2

        out["F"] = [f1, f2]
```

**Exemplo com restrições:**
```python
class ConstrainedProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,        # Restrições de desigualdade
            n_eq_constr=1,         # Restrições de igualdade
            xl=np.array([0, 0]),
            xu=np.array([5, 5])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Objetivos
        out["F"] = [f1, f2]

        # Restrições de desigualdade (g <= 0)
        out["G"] = [g1, g2]

        # Restrições de igualdade (h = 0)
        out["H"] = [h1]
```

**Regras de formulação de restrições:**
- Desigualdade: Expresse como `g(x) <= 0` (viável quando ≤ 0)
- Igualdade: Expresse como `h(x) = 0` (viável quando = 0)
- Converta `g(x) >= b` para `-(g(x) - b) <= 0`

**Veja:** `scripts/custom_problem_example.py` para exemplos completos

### Fluxo de Trabalho 5: Tratamento de Restrições

**Quando:** O problema tem restrições de viabilidade

**Opções de abordagem:**

**1. Viabilidade Primeiro (Padrão - Recomendado)**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2

# Funciona automaticamente com problemas com restrições
algorithm = NSGA2(pop_size=100)
result = minimize(problem, algorithm, termination)

# Verifique viabilidade
feasible = result.CV[:, 0] == 0  # CV = violação de restrição
print(f"Soluções viáveis: {np.sum(feasible)}")
```

**2. Método de Penalidade**
```python
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

# Envolva o problema para converter restrições em penalidades
problem_penalized = ConstraintsAsPenalty(problem, penalty=1e6)
```

**3. Restrição como Objetivo**
```python
from pymoo.constraints.as_obj import ConstraintsAsObjective

# Trate violação de restrição como objetivo adicional
problem_with_cv = ConstraintsAsObjective(problem)
```

**4. Algoritmos Especializados**
```python
from pymoo.algorithms.soo.nonconvex.sres import SRES

# SRES tem tratamento de restrições integrado
algorithm = SRES()
```

**Veja:** `references/constraints_mcdm.md` para guia abrangente de tratamento de restrições

### Fluxo de Trabalho 6: Tomada de Decisão a partir da Frente de Pareto

**Quando:** Tem frente de Pareto, precisa selecionar solução(ões) preferida(s)

**Passos:**
1. Execute otimização multi-objetivo
2. Normalize objetivos para [0, 1]
3. Defina pesos de preferência
4. Aplique método MCDM
5. Visualize solução selecionada

**Exemplo usando Pseudo-Pesos:**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights
import numpy as np

# Após obter resultado da otimização multi-objetivo
# Normalize objetivos
F_norm = (result.F - result.F.min(axis=0)) / (result.F.max(axis=0) - result.F.min(axis=0))

# Defina preferências (devem somar 1)
weights = np.array([0.3, 0.7])  # 30% f1, 70% f2

# Aplique tomada de decisão
dm = PseudoWeights(weights)
selected_idx = dm.do(F_norm)

# Obtenha solução selecionada
best_solution = result.X[selected_idx]
best_objectives = result.F[selected_idx]

print(f"Solução selecionada: {best_solution}")
print(f"Valores de objetivo: {best_objectives}")
```

**Outros métodos MCDM:**
- Programação de Compromisso: Selecione o mais próximo do ponto ideal
- Ponto de Joelho: Encontre soluções de trade-off equilibradas
- Contribuição de Hipervolume: Selecione subconjunto mais diverso

**Veja:**
- `scripts/decision_making_example.py` para exemplo completo
- `references/constraints_mcdm.md` para métodos MCDM detalhados

### Fluxo de Trabalho 7: Visualização

**Escolha visualização baseada no número de objetivos:**

**2 objetivos: Gráfico de Dispersão**
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Resultados Bi-Objetivo")
plot.add(result.F, color="blue", alpha=0.7)
plot.show()
```

**3 objetivos: Dispersão 3D**
```python
plot = Scatter(title="Resultados Tri-Objetivo")
plot.add(result.F)  # Renderiza automaticamente em 3D
plot.show()
```

**4+ objetivos: Gráfico de Coordenadas Paralelas**
```python
from pymoo.visualization.pcp import PCP

plot = PCP(
    labels=[f"f{i+1}" for i in range(n_obj)],
    normalize_each_axis=True
)
plot.add(result.F, alpha=0.3)
plot.show()
```

**Comparação de soluções: Diagrama de Pétalas**
```python
from pymoo.visualization.petal import Petal

plot = Petal(
    bounds=[result.F.min(axis=0), result.F.max(axis=0)],
    labels=["Custo", "Peso", "Eficiência"]
)
plot.add(solution_A, label="Design A")
plot.add(solution_B, label="Design B")
plot.show()
```

**Veja:** `references/visualization.md` para todos os tipos de visualização e uso

## Guia de Seleção de Algoritmo

### Problemas Mono-Objetivo

| Algoritmo | Melhor Para | Características Principais |
|-----------|-------------|---------------------------|
| **GA** | Uso geral | Flexível, operadores personalizáveis |
| **DE** | Otimização contínua | Bom para busca global |
| **PSO** | Paisagens suaves | Convergência rápida |
| **CMA-ES** | Problemas difíceis/com ruído | Auto-adaptativo |

### Problemas Multi-Objetivo (2-3 objetivos)

| Algoritmo | Melhor Para | Características Principais |
|-----------|-------------|---------------------------|
| **NSGA-II** | Benchmark padrão | Rápido, confiável, bem testado |
| **R-NSGA-II** | Regiões de preferência | Orientação por ponto de referência |
| **MOEA/D** | Problemas decomponíveis | Abordagem por escalarização |

### Problemas com Muitos-Objetivos (4+ objetivos)

| Algoritmo | Melhor Para | Características Principais |
|-----------|-------------|---------------------------|
| **NSGA-III** | 4-15 objetivos | Baseado em direção de referência |
| **RVEA** | Busca adaptativa | Evolução de vetor de referência |
| **AGE-MOEA** | Paisagens complexas | Geometria adaptativa |

### Problemas com Restrições

| Abordagem | Algoritmo | Quando Usar |
|-----------|-----------|-------------|
| Viabilidade-primeiro | Qualquer algoritmo | Região viável grande |
| Especializado | SRES, ISRES | Restrições pesadas |
| Penalidade | GA + penalidade | Compatibilidade com algoritmo |

**Veja:** `references/algorithms.md` para referência abrangente de algoritmos

## Problemas de Benchmark

### Acesso rápido a problemas:
```python
from pymoo.problems import get_problem

# Mono-objetivo
problem = get_problem("rastrigin", n_var=10)
problem = get_problem("rosenbrock", n_var=10)

# Multi-objetivo
problem = get_problem("zdt1")        # Frente convexa
problem = get_problem("zdt2")        # Frente não-convexa
problem = get_problem("zdt3")        # Frente desconectada

# Muitos-objetivos
problem = get_problem("dtlz2", n_obj=5, n_var=12)
problem = get_problem("dtlz7", n_obj=4)
```

**Veja:** `references/problems.md` para referência completa de problemas de teste

## Personalização de Operadores Genéticos

### Configuração padrão de operadores:
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

algorithm = GA(
    pop_size=100,
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)
```

### Seleção de operador por tipo de variável:

**Variáveis contínuas:**
- Crossover: SBX (Simulated Binary Crossover)
- Mutação: PM (Polynomial Mutation)

**Variáveis binárias:**
- Crossover: TwoPointCrossover, UniformCrossover
- Mutação: BitflipMutation

**Permutações (TSP, agendamento):**
- Crossover: OrderCrossover (OX)
- Mutação: InversionMutation

**Veja:** `references/operators.md` para referência abrangente de operadores

## Desempenho e Resolução de Problemas

### Problemas comuns e soluções:

**Problema: Algoritmo não converge**
- Aumentar tamanho da população
- Aumentar número de gerações
- Verificar se o problema é multimodal (testar diferentes algoritmos)
- Verificar se restrições estão formuladas corretamente

**Problema: Distribuição ruim na frente de Pareto**
- Para NSGA-III: Ajuste direções de referência
- Aumentar tamanho da população
- Verificar eliminação de duplicatas
- Verificar escala do problema

**Problema: Poucas soluções viáveis**
- Usar abordagem restrição-como-objetivo
- Aplicar operadores de reparo
- Tentar SRES/ISRES para problemas com restrições
- Verificar formulação de restrições (deve ser g <= 0)

**Problema: Custo computacional alto**
- Reduzir tamanho da população
- Diminuir número de gerações
- Usar operadores mais simples
- Ativar paralelização (se o problema suportar)

### Melhores práticas:

1. **Normalize objetivos** quando escalas diferem significativamente
2. **Defina seed aleatória** para reprodutibilidade
3. **Salve histórico** para analisar convergência: `save_history=True`
4. **Visualize resultados** para entender qualidade da solução
5. **Compare com frente de Pareto verdadeira** quando disponível
6. **Use critérios de término apropriados** (gerações, avaliações, tolerância)
7. **Ajuste parâmetros de operadores** para características do problema

## Recursos

Esta competência inclui documentação de referência abrangente e exemplos executáveis:

### references/
Documentação detalhada para compreensão aprofundada:

- **algorithms.md**: Referência completa de algoritmos com parâmetros, uso e diretrizes de seleção
- **problems.md**: Problemas de teste de benchmark (ZDT, DTLZ, WFG) com características
- **operators.md**: Operadores genéticos (amostragem, seleção, crossover, mutação) com configuração
- **visualization.md**: Todos os tipos de visualização com exemplos e guia de seleção
- **constraints_mcdm.md**: Técnicas de tratamento de restrições e métodos de decisão multi-critério

**Padrões de busca em referências:**
- Detalhes de algoritmo: `grep -r "NSGA-II\|NSGA-III\|MOEA/D" references/`
- Métodos de restrição: `grep -r "Viabilidade Primeiro\|Penalidade\|Reparo" references/`
- Tipos de visualização: `grep -r "Scatter\|PCP\|Petal" references/`

### scripts/
Exemplos executáveis demonstrando fluxos de trabalho comuns:

- **single_objective_example.py**: Otimização mono-objetivo básica com GA
- **multi_objective_example.py**: Otimização multi-objetivo com NSGA-II, visualização
- **many_objective_example.py**: Otimização com muitos-objetivos com NSGA-III, direções de referência
- **custom_problem_example.py**: Definição de problemas personalizados (com e sem restrições)
- **decision_making_example.py**: Tomada de decisão multi-critério com diferentes preferências

**Execute exemplos:**
```bash
python3 scripts/single_objective_example.py
python3 scripts/multi_objective_example.py
python3 scripts/many_objective_example.py
python3 scripts/custom_problem_example.py
python3 scripts/decision_making_example.py
```

## Notas Adicionais

**Instalação:**
```bash
uv pip install pymoo
```

**Dependências:** NumPy, SciPy, matplotlib, autograd (opcional para baseado em gradiente)

**Documentação:** https://pymoo.org/

**Versão:** Esta competência é baseada em pymoo 0.6.x

**Padrões comuns:**
- Sempre use `ElementwiseProblem` para problemas personalizados
- Restrições formuladas como `g(x) <= 0` e `h(x) = 0`
- Direções de referência obrigatórias para NSGA-III
- Normalize objetivos antes de MCDM
- Use término apropriado: `('n_gen', N)` ou `get_termination("f_tol", tol=0.001)`