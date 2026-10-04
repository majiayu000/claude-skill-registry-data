---
name: qutip
description: "Simulações e análise de mecânica quântica usando QuTiP (Quantum Toolbox in Python). Use quando trabalhar com sistemas quânticos incluindo: (1) estados quânticos (kets, bras, matrizes densidade), (2) operadores e gates quânticos, (3) evolução temporal e dinâmica (Schrödinger, equações mestras, Monte Carlo), (4) sistemas quânticos abertos com dissipação, (5) medições quânticas e emaranhamento, (6) visualização (esfera de Bloch, funções de Wigner), (7) estados estacionários e funções de correlação, ou (8) métodos avançados (teoria de Floquet, HEOM, resolutores estocásticos). Manipula sistemas quânticos fechados e abertos em vários domínios incluindo óptica quântica, computação quântica e física da matéria condensada."
---

# QuTiP: Quantum Toolbox in Python

## Visão Geral

QuTiP oferece ferramentas abrangentes para simular e analisar sistemas mecânicos quânticos. Manipula sistemas quânticos fechados (unitários) e abertos (dissipativos) com múltiplos resolutores otimizados para diferentes cenários.

## Instalação

```bash
uv pip install qutip
```

Pacotes opcionais para funcionalidade adicional:

```bash
# Processamento de informação quântica (circuitos, gates)
uv pip install qutip-qip

# Visualizador de trajetória quântica
uv pip install qutip-qtrl
```

## Início Rápido

```python
from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Criar estado quântico
psi = basis(2, 0)  # |0⟩ state

# Criar operador
H = sigmaz()  # Hamiltonian

# Evolução temporal
tlist = np.linspace(0, 10, 100)
result = sesolve(H, psi, tlist, e_ops=[sigmaz()])

# Plotar resultados
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

## Capacidades Principais

### 1. Objetos e Estados Quânticos

Crie e manipule estados e operadores quânticos:

```python
# Estados
psi = basis(N, n)  # Fock state |n⟩
psi = coherent(N, alpha)  # Coherent state |α⟩
rho = thermal_dm(N, n_avg)  # Thermal density matrix

# Operadores
a = destroy(N)  # Annihilation operator
H = num(N)  # Number operator
sx, sy, sz = sigmax(), sigmay(), sigmaz()  # Pauli matrices

# Sistemas compostos
psi_AB = tensor(psi_A, psi_B)  # Tensor product
```

**Veja** `references/core_concepts.md` para cobertura abrangente de objetos quânticos, estados, operadores e produtos tensoriais.

### 2. Evolução Temporal e Dinâmica

Múltiplos resolutores para diferentes cenários:

```python
# Sistemas fechados (evolução unitária)
result = sesolve(H, psi0, tlist, e_ops=[num(N)])

# Sistemas abertos (dissipação)
c_ops = [np.sqrt(0.1) * destroy(N)]  # Collapse operators
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Trajetórias quânticas (Monte Carlo)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=500, e_ops=[num(N)])
```

**Guia de seleção de resolutor:**
- `sesolve`: Estados puros, evolução unitária
- `mesolve`: Estados mistos, dissipação, sistemas abertos gerais
- `mcsolve`: Saltos quânticos, contagem de fótons, trajetórias individuais
- `brmesolve`: Acoplamento fraco sistema-banho
- `fmmesolve`: Hamiltonianos periódicos no tempo (Floquet)

**Veja** `references/time_evolution.md` para documentação detalhada do resolutor, Hamiltonianos dependentes do tempo e opções avançadas.

### 3. Análise e Medição

Calcule quantidades físicas:

```python
# Valores de expectativa
n_avg = expect(num(N), psi)

# Medidas de entropia
S = entropy_vn(rho)  # Von Neumann entropy
C = concurrence(rho)  # Entanglement (two qubits)

# Fidelidade e distância
F = fidelity(psi1, psi2)
D = tracedist(rho1, rho2)

# Funções de correlação
corr = correlation_2op_1t(H, rho0, taulist, c_ops, A, B)
w, S = spectrum_correlation_fft(taulist, corr)

# Estados estacionários
rho_ss = steadystate(H, c_ops)
```

**Veja** `references/analysis.md` para cálculos de entropia, fidelidade, medições, funções de correlação e estados estacionários.

### 4. Visualização

Visualize estados quânticos e dinâmica:

```python
# Esfera de Bloch
b = Bloch()
b.add_states(psi)
b.show()

# Função de Wigner (espaço de fases)
xvec = np.linspace(-5, 5, 200)
W = wigner(psi, xvec, xvec)
plt.contourf(xvec, xvec, W, 100, cmap='RdBu')

# Distribuição de Fock
plot_fock_distribution(psi)

# Visualização de matriz
hinton(rho)  # Hinton diagram
matrix_histogram(H.full())  # 3D bars
```

**Veja** `references/visualization.md` para animações de esfera de Bloch, funções de Wigner, funções Q e visualizações de matriz.

### 5. Métodos Avançados

Técnicas especializadas para cenários complexos:

```python
# Teoria de Floquet (Hamiltonianos periódicos)
T = 2 * np.pi / w_drive
f_modes, f_energies = floquet_modes(H, T, args)
result = fmmesolve(H, psi0, tlist, c_ops, T=T, args=args)

# HEOM (não-Markoviano, acoplamento forte)
from qutip.nonmarkov.heom import HEOMSolver, BosonicBath
bath = BosonicBath(Q, ck_real, vk_real)
hsolver = HEOMSolver(H_sys, [bath], max_depth=5)
result = hsolver.run(rho0, tlist)

# Invariância permutacional (partículas idênticas)
psi = dicke(N, j, m)  # Dicke states
Jz = jspin(N, 'z')  # Collective operators
```

**Veja** `references/advanced.md` para teoria de Floquet, HEOM, invariância permutacional, resolutores estocásticos, superoperadores e otimização de desempenho.

## Fluxos de Trabalho Comuns

### Simulando um Oscilador Harmônico Amortecido

```python
# Parâmetros do sistema
N = 20  # Hilbert space dimension
omega = 1.0  # Oscillator frequency
kappa = 0.1  # Decay rate

# Hamiltoniano e operadores collapse
H = omega * num(N)
c_ops = [np.sqrt(kappa) * destroy(N)]

# Estado inicial
psi0 = coherent(N, 3.0)

# Evolução temporal
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Visualizar
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨n⟩')
plt.title('Photon Number Decay')
plt.show()
```

### Dinâmica de Emaranhamento de Dois Qubits

```python
# Criar estado de Bell
psi0 = bell_state('00')

# Desfasamento local em cada qubit
gamma = 0.1
c_ops = [
    np.sqrt(gamma) * tensor(sigmaz(), qeye(2)),
    np.sqrt(gamma) * tensor(qeye(2), sigmaz())
]

# Rastrear emaranhamento
def compute_concurrence(t, psi):
    rho = ket2dm(psi) if psi.isket else psi
    return concurrence(rho)

tlist = np.linspace(0, 10, 100)
result = mesolve(qeye([2, 2]), psi0, tlist, c_ops)

# Calcular concurrence para cada estado
C_t = [concurrence(state.proj()) for state in result.states]

plt.plot(tlist, C_t)
plt.xlabel('Time')
plt.ylabel('Concurrence')
plt.title('Entanglement Decay')
plt.show()
```

### Modelo de Jaynes-Cummings

```python
# Parâmetros do sistema
N = 10  # Cavity Fock space
wc = 1.0  # Cavity frequency
wa = 1.0  # Atom frequency
g = 0.05  # Coupling strength

# Operadores
a = tensor(destroy(N), qeye(2))  # Cavity
sm = tensor(qeye(N), sigmam())  # Atom

# Hamiltoniano (RWA)
H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())

# Estado inicial: cavidade em estado coerente, átomo em estado fundamental
psi0 = tensor(coherent(N, 2), basis(2, 0))

# Dissipação
kappa = 0.1  # Cavity decay
gamma = 0.05  # Atomic decay
c_ops = [np.sqrt(kappa) * a, np.sqrt(gamma) * sm]

# Observáveis
n_cav = a.dag() * a
n_atom = sm.dag() * sm

# Evoluir
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[n_cav, n_atom])

# Plotar
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
axes[0].plot(tlist, result.expect[0])
axes[0].set_ylabel('⟨n_cavity⟩')
axes[1].plot(tlist, result.expect[1])
axes[1].set_ylabel('⟨n_atom⟩')
axes[1].set_xlabel('Time')
plt.tight_layout()
plt.show()
```

## Dicas para Simulações Eficientes

1. **Truncar espaços de Hilbert**: Use a menor dimensão que capture a dinâmica
2. **Escolha o resolutor apropriado**: `sesolve` para estados puros é mais rápido que `mesolve`
3. **Termos dependentes do tempo**: Formato de string (ex: `'cos(w*t)'`) é mais rápido
4. **Armazene apenas dados necessários**: Use `e_ops` em vez de armazenar todos os estados
5. **Ajuste tolerâncias**: Equilibre precisão e tempo de computação via `Options`
6. **Trajetórias paralelas**: `mcsolve` usa automaticamente múltiplos CPUs
7. **Verifique convergência**: Varie `ntraj`, tamanho do espaço de Hilbert e tolerâncias

## Solução de Problemas

**Problemas de memória**: Reduza a dimensão do espaço de Hilbert, use opção `store_final_state` ou considere métodos de Krylov

**Simulações lentas**: Use dependência de tempo baseada em string, aumente tolerâncias ligeiramente ou tente `method='bdf'` para problemas rígidos

**Instabilidades numéricas**: Diminua passos de tempo (opção `nsteps`), aumente tolerâncias ou verifique se Hamiltoniano/operadores estão definidos corretamente

**Erros de importação**: Garanta que QuTiP esteja instalado corretamente; gates quânticos requerem pacote `qutip-qip`

## Referências

Esta skill inclui documentação de referência detalhada:

- **`references/core_concepts.md`**: Objetos quânticos, estados, operadores, produtos tensoriais, sistemas compostos
- **`references/time_evolution.md`**: Todos os resolutores (sesolve, mesolve, mcsolve, brmesolve, etc.), Hamiltonianos dependentes do tempo, opções do resolutor
- **`references/visualization.md`**: Esfera de Bloch, funções de Wigner, funções Q, distribuições de Fock, gráficos de matriz
- **`references/analysis.md`**: Valores de expectativa, entropia, fidelidade, medidas de emaranhamento, funções de correlação, estados estacionários
- **`references/advanced.md`**: Teoria de Floquet, HEOM, invariância permutacional, métodos estocásticos, superoperadores, dicas de desempenho

## Recursos Externos

- Documentação: https://qutip.readthedocs.io/
- Tutoriais: https://qutip.org/qutip-tutorials/
- Referência de API: https://qutip.readthedocs.io/en/stable/apidoc/apidoc.html
- GitHub: https://github.com/qutip/qutip