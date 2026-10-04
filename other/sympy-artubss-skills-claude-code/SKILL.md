---
name: sympy
description: Use esta competência ao trabalhar com matemática simbólica em Python. Esta competência deve ser usada para tarefas de computação simbólica incluindo resolução de equações algebraicamente, realização de operações de cálculo (derivadas, integrais, limites), manipulação de expressões algébricas, trabalho com matrizes simbolicamente, cálculos de física, problemas de teoria dos números, computações de geometria e geração de código executável a partir de expressões matemáticas. Aplique esta competência quando o usuário precisa de resultados simbólicos exatos em vez de aproximações numéricas, ou ao trabalhar com fórmulas matemáticas que contêm variáveis e parâmetros.
---

# SymPy - Matemática Simbólica em Python

## Visão Geral

SymPy é uma biblioteca Python para matemática simbólica que permite cálculo exato usando símbolos matemáticos em vez de aproximações numéricas. Esta competência fornece orientação abrangente para realizar álgebra simbólica, cálculo, álgebra linear, resolução de equações, cálculos de física e geração de código usando SymPy.

## Quando Usar Esta Competência

Use esta competência quando:
- Resolver equações simbolicamente (algébricas, diferenciais, sistemas de equações)
- Realizar operações de cálculo (derivadas, integrais, limites, séries)
- Manipular e simplificar expressões algébricas
- Trabalhar com matrizes e álgebra linear simbolicamente
- Fazer cálculos de física (mecânica, mecânica quântica, análise vetorial)
- Computações de teoria dos números (primos, fatoração, aritmética modular)
- Cálculos geométricos (geometria 2D/3D, geometria analítica)
- Converter expressões matemáticas em código executável (Python, C, Fortran)
- Gerar saída LaTeX ou outro formato matemático
- Precisar de resultados matemáticos exatos (ex: `sqrt(2)` não `1.414...`)

## Capacidades Principais

### 1. Fundamentos de Computação Simbólica

**Criando símbolos e expressões:**
```python
from sympy import symbols, Symbol
x, y, z = symbols('x y z')
expr = x**2 + 2*x + 1

# Com suposições
x = symbols('x', real=True, positive=True)
n = symbols('n', integer=True)
```

**Simplificação e manipulação:**
```python
from sympy import simplify, expand, factor, cancel
simplify(sin(x)**2 + cos(x)**2)  # Retorna 1
expand((x + 1)**3)  # x**3 + 3*x**2 + 3*x + 1
factor(x**2 - 1)    # (x - 1)*(x + 1)
```

**Para fundamentos detalhados:** Veja `references/core-capabilities.md`

### 2. Cálculo

**Derivadas:**
```python
from sympy import diff
diff(x**2, x)        # 2*x
diff(x**4, x, 3)     # 24*x (terceira derivada)
diff(x**2*y**3, x, y)  # 6*x*y**2 (derivadas parciais)
```

**Integrais:**
```python
from sympy import integrate, oo
integrate(x**2, x)              # x**3/3 (indefinida)
integrate(x**2, (x, 0, 1))      # 1/3 (definida)
integrate(exp(-x), (x, 0, oo))  # 1 (imprópria)
```

**Limites e Séries:**
```python
from sympy import limit, series
limit(sin(x)/x, x, 0)  # 1
series(exp(x), x, 0, 6)  # 1 + x + x**2/2 + x**3/6 + x**4/24 + x**5/120 + O(x**6)
```

**Para operações de cálculo detalhadas:** Veja `references/core-capabilities.md`

### 3. Resolução de Equações

**Equações algébricas:**
```python
from sympy import solveset, solve, Eq
solveset(x**2 - 4, x)  # {-2, 2}
solve(Eq(x**2, 4), x)  # [-2, 2]
```

**Sistemas de equações:**
```python
from sympy import linsolve, nonlinsolve
linsolve([x + y - 2, x - y], x, y)  # {(1, 1)} (linear)
nonlinsolve([x**2 + y - 2, x + y**2 - 3], x, y)  # (não-linear)
```

**Equações diferenciais:**
```python
from sympy import Function, dsolve, Derivative
f = symbols('f', cls=Function)
dsolve(Derivative(f(x), x) - f(x), f(x))  # Eq(f(x), C1*exp(x))
```

**Para métodos de resolução detalhados:** Veja `references/core-capabilities.md`

### 4. Matrizes e Álgebra Linear

**Criação de matrizes e operações:**
```python
from sympy import Matrix, eye, zeros
M = Matrix([[1, 2], [3, 4]])
M_inv = M**-1  # Inversa
M.det()        # Determinante
M.T            # Transposta
```

**Autovalores e autovetores:**
```python
eigenvals = M.eigenvals()  # {autovalor: multiplicidade}
eigenvects = M.eigenvects()  # [(autoval, mult, [autovetores])]
P, D = M.diagonalize()  # M = P*D*P^-1
```

**Resolvendo sistemas lineares:**
```python
A = Matrix([[1, 2], [3, 4]])
b = Matrix([5, 6])
x = A.solve(b)  # Resolve Ax = b
```

**Para álgebra linear abrangente:** Veja `references/matrices-linear-algebra.md`

### 5. Física e Mecânica

**Mecânica clássica:**
```python
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod
from sympy import symbols

# Definir sistema
q = dynamicsymbols('q')
m, g, l = symbols('m g l')

# Lagrangiana (T - V)
L = m*(l*q.diff())**2/2 - m*g*l*(1 - cos(q))

# Aplicar método de Lagrange
LM = LagrangesMethod(L, [q])
```

**Análise vetorial:**
```python
from sympy.physics.vector import ReferenceFrame, dot, cross
N = ReferenceFrame('N')
v1 = 3*N.x + 4*N.y
v2 = 1*N.x + 2*N.z
dot(v1, v2)  # Produto escalar
cross(v1, v2)  # Produto vetorial
```

**Mecânica quântica:**
```python
from sympy.physics.quantum import Ket, Bra, Commutator
psi = Ket('psi')
A = Operator('A')
comm = Commutator(A, B).doit()
```

**Para capacidades de física detalhadas:** Veja `references/physics-mechanics.md`

### 6. Matemática Avançada

A competência inclui suporte abrangente para:

- **Geometria:** Geometria analítica 2D/3D, pontos, linhas, círculos, polígonos, transformações
- **Teoria dos Números:** Primos, fatoração, MDC/MMC, aritmética modular, equações diofantinas
- **Combinatória:** Permutações, combinações, partições, teoria de grupos
- **Lógica e Conjuntos:** Lógica booleana, teoria de conjuntos, conjuntos finitos e infinitos
- **Estatística:** Distribuições de probabilidade, variáveis aleatórias, esperança, variância
- **Funções Especiais:** Gama, Bessel, polinômios ortogonais, funções hipergeométricas
- **Polinômios:** Álgebra de polinômios, raízes, fatoração, bases de Groebner

**Para tópicos avançados detalhados:** Veja `references/advanced-topics.md`

### 7. Geração de Código e Saída

**Converter para funções executáveis:**
```python
from sympy import lambdify
import numpy as np

expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')  # Criar função NumPy
x_vals = np.linspace(0, 10, 100)
y_vals = f(x_vals)  # Avaliação numérica rápida
```

**Gerar código C/Fortran:**
```python
from sympy.utilities.codegen import codegen
[(c_name, c_code), (h_name, h_header)] = codegen(
    ('my_func', expr), 'C'
)
```

**Saída LaTeX:**
```python
from sympy import latex
latex_str = latex(expr)  # Converter para LaTeX para documentos
```

**Para geração de código abrangente:** Veja `references/code-generation-printing.md`

## Trabalhando com SymPy: Melhores Práticas

### 1. Sempre Defina Símbolos Primeiro

```python
from sympy import symbols
x, y, z = symbols('x y z')
# Agora x, y, z podem ser usados em expressões
```

### 2. Use Suposições para Melhor Simplificação

```python
x = symbols('x', positive=True, real=True)
sqrt(x**2)  # Retorna x (não Abs(x)) devido à suposição positiva
```

Suposições comuns: `real`, `positive`, `negative`, `integer`, `rational`, `complex`, `even`, `odd`

### 3. Use Aritmética Exata

```python
from sympy import Rational, S
# Correto (exato):
expr = Rational(1, 2) * x
expr = S(1)/2 * x

# Incorreto (ponto flutuante):
expr = 0.5 * x  # Cria valor aproximado
```

### 4. Avaliação Numérica Quando Necessário

```python
from sympy import pi, sqrt
result = sqrt(8) + pi
result.evalf()    # 5.96371554103586
result.evalf(50)  # 50 dígitos de precisão
```

### 5. Converta para NumPy para Desempenho

```python
# Lento para muitas avaliações:
for x_val in range(1000):
    result = expr.subs(x, x_val).evalf()

# Rápido:
f = lambdify(x, expr, 'numpy')
results = f(np.arange(1000))
```

### 6. Use Resolvedores Apropriados

- `solveset`: Equações algébricas (primário)
- `linsolve`: Sistemas lineares
- `nonlinsolve`: Sistemas não-lineares
- `dsolve`: Equações diferenciais
- `solve`: Propósito geral (legado, mas flexível)

## Estrutura de Arquivos de Referência

Esta competência usa arquivos de referência modulares para diferentes capacidades:

1. **`core-capabilities.md`**: Símbolos, álgebra, cálculo, simplificação, resolução de equações
   - Carregue quando: Computação simbólica básica, cálculo, ou resolução de equações

2. **`matrices-linear-algebra.md`**: Operações matriciais, autovalores, sistemas lineares
   - Carregue quando: Trabalhar com matrizes ou problemas de álgebra linear

3. **`physics-mechanics.md`**: Mecânica clássica, mecânica quântica, vetores, unidades
   - Carregue quando: Cálculos de física ou problemas de mecânica

4. **`advanced-topics.md`**: Geometria, teoria dos números, combinatória, lógica, estatística
   - Carregue quando: Tópicos matemáticos avançados além de álgebra e cálculo básicos

5. **`code-generation-printing.md`**: Lambdify, codegen, saída LaTeX, impressão
   - Carregue quando: Converter expressões em código ou gerar saída formatada

## Padrões Comuns de Casos de Uso

### Padrão 1: Resolver e Verificar

```python
from sympy import symbols, solve, simplify
x = symbols('x')

# Resolver equação
equation = x**2 - 5*x + 6
solutions = solve(equation, x)  # [2, 3]

# Verificar soluções
for sol in solutions:
    result = simplify(equation.subs(x, sol))
    assert result == 0
```

### Padrão 2: Pipeline Simbólico para Numérico

```python
# 1. Definir problema simbólico
x, y = symbols('x y')
expr = sin(x) + cos(y)

# 2. Manipular simbolicamente
simplified = simplify(expr)
derivative = diff(simplified, x)

# 3. Converter para função numérica
f = lambdify((x, y), derivative, 'numpy')

# 4. Avaliar numericamente
results = f(x_data, y_data)
```

### Padrão 3: Documentar Resultados Matemáticos

```python
# Computar resultado simbolicamente
integral_expr = Integral(x**2, (x, 0, 1))
result = integral_expr.doit()

# Gerar documentação
print(f"LaTeX: {latex(integral_expr)} = {latex(result)}")
print(f"Pretty: {pretty(integral_expr)} = {pretty(result)}")
print(f"Numérico: {result.evalf()}")
```

## Integração com Fluxos de Trabalho Científicos

### Com NumPy

```python
import numpy as np
from sympy import symbols, lambdify

x = symbols('x')
expr = x**2 + 2*x + 1

f = lambdify(x, expr, 'numpy')
x_array = np.linspace(-5, 5, 100)
y_array = f(x_array)
```

### Com Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sin

x = symbols('x')
expr = sin(x) / x

f = lambdify(x, expr, 'numpy')
x_vals = np.linspace(-10, 10, 1000)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals)
plt.show()
```

### Com SciPy

```python
from scipy.optimize import fsolve
from sympy import symbols, lambdify

# Definir equação simbolicamente
x = symbols('x')
equation = x**3 - 2*x - 5

# Converter para função numérica
f = lambdify(x, equation, 'numpy')

# Resolver numericamente com palpite inicial
solution = fsolve(f, 2)
```

## Referência Rápida: Funções Mais Comuns

```python
# Símbolos
from sympy import symbols, Symbol
x, y = symbols('x y')

# Operações básicas
from sympy import simplify, expand, factor, collect, cancel
from sympy import sqrt, exp, log, sin, cos, tan, pi, E, I, oo

# Cálculo
from sympy import diff, integrate, limit, series, Derivative, Integral

# Resolução
from sympy import solve, solveset, linsolve, nonlinsolve, dsolve

# Matrizes
from sympy import Matrix, eye, zeros, ones, diag

# Lógica e conjuntos
from sympy import And, Or, Not, Implies, FiniteSet, Interval, Union

# Saída
from sympy import latex, pprint, lambdify, init_printing

# Utilitários
from sympy import evalf, N, nsimplify
```

## Exemplos de Introdução

### Exemplo 1: Resolver Equação Quadrática
```python
from sympy import symbols, solve, sqrt
x = symbols('x')
solution = solve(x**2 - 5*x + 6, x)
# [2, 3]
```

### Exemplo 2: Calcular Derivada
```python
from sympy import symbols, diff, sin
x = symbols('x')
f = sin(x**2)
df_dx = diff(f, x)
# 2*x*cos(x**2)
```

### Exemplo 3: Avaliar Integral
```python
from sympy import symbols, integrate, exp
x = symbols('x')
integral = integrate(x * exp(-x**2), (x, 0, oo))
# 1/2
```

### Exemplo 4: Autovalores de Matriz
```python
from sympy import Matrix
M = Matrix([[1, 2], [2, 1]])
eigenvals = M.eigenvals()
# {3: 1, -1: 1}
```

### Exemplo 5: Gerar Função Python
```python
from sympy import symbols, lambdify
import numpy as np
x = symbols('x')
expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')
f(np.array([1, 2, 3]))
# array([ 4,  9, 16])
```

## Solução de Problemas Comuns

1. **"NameError: name 'x' is not defined"**
   - Solução: Sempre defina símbolos usando `symbols()` antes de usar

2. **Resultados numéricos inesperados**
   - Problema: Usar números de ponto flutuante como `0.5` em vez de `Rational(1, 2)`
   - Solução: Use `Rational()` ou `S()` para aritmética exata

3. **Desempenho lento em loops**
   - Problema: Usar `subs()` e `evalf()` repetidamente
   - Solução: Use `lambdify()` para criar uma função numérica rápida

4. **"Can't solve this equation"**
   - Tente diferentes resolvedores: `solve`, `solveset`, `nsolve` (numérico)
   - Verifique se a equação é solúvel algebricamente
   - Use métodos numéricos se não existir solução de forma fechada

5. **Simplificação não funcionando como esperado**
   - Tente diferentes funções de simplificação: `simplify`, `factor`, `expand`, `trigsimp`
   - Adicione suposições aos símbolos (ex: `positive=True`)
   - Use `simplify(expr, force=True)` para simplificação agressiva

## Recursos Adicionais

- Documentação Oficial: https://docs.sympy.org/
- Tutorial: https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html
- Referência de API: https://docs.sympy.org/latest/reference/index.html
- Exemplos: https://github.com/sympy/sympy/tree/master/examples