---
name: qiskit
description: Kit de ferramentas abrangente de computação quântica para construir, otimizar e executar circuitos quânticos. Use quando trabalhar com algoritmos quânticos, simulações ou hardware quântico, incluindo (1) Construção de circuitos quânticos com portas e medições, (2) Execução de algoritmos quânticos (VQE, QAOA, Grover), (3) Transpilar/otimizar circuitos para hardware, (4) Executar em IBM Quantum ou outros provedores, (5) Química quântica e ciência dos materiais, (6) Aprendizado de máquina quântico, (7) Visualizar circuitos e resultados, ou (8) Qualquer tarefa de desenvolvimento de computação quântica.
---

# Qiskit

## Visão Geral

Qiskit é o framework de computação quântica de código aberto mais popular do mundo com 13M+ downloads. Construa circuitos quânticos, otimize para hardware, execute em simuladores ou em computadores quânticos reais, e analise resultados. Suporta IBM Quantum (sistemas com 100+ qubits), IonQ, Amazon Braket e outros provedores.

**Principais Características:**
- Transpilar 83x mais rápido que concorrentes
- 29% menos portas de dois qubits em circuitos otimizados
- Execução agnóstica de backend (simuladores locais ou hardware em nuvem)
- Bibliotecas abrangentes de algoritmos para otimização, química e ML

## Início Rápido

### Instalação

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### Primeiro Circuito

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Cria estado Bell (qubits emaranhados)
qc = QuantumCircuit(2)
qc.h(0)           # Hadamard no qubit 0
qc.cx(0, 1)       # CNOT do qubit 0 para 1
qc.measure_all()  # Mede ambos os qubits

# Executa localmente
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### Visualização

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # Diagrama do circuito
plot_histogram(counts)   # Histograma de resultados
```

## Capacidades Principais

### 1. Configuração e Instalação
Para instalação detalhada, autenticação e configuração da conta IBM Quantum:
- **Veja `references/setup.md`**

Tópicos cobertos:
- Instalação com uv
- Configuração de ambiente Python
- Configuração de conta IBM Quantum e token de API
- Execução local vs. em nuvem

### 2. Construção de Circuitos Quânticos
Para construir circuitos quânticos com portas, medições e composição:
- **Veja `references/circuits.md`**

Tópicos cobertos:
- Criação de circuitos com QuantumCircuit
- Portas de um qubit (H, X, Y, Z, rotações, portas de fase)
- Portas de múltiplos qubits (CNOT, SWAP, Toffoli)
- Medições e barreiras
- Composição de circuitos e propriedades
- Circuitos parametrizados para algoritmos variacionais

### 3. Primitives (Sampler e Estimator)
Para executar circuitos quânticos e computar resultados:
- **Veja `references/primitives.md`**

Tópicos cobertos:
- **Sampler**: Obtenha medições de bitstring e distribuições de probabilidade
- **Estimator**: Calcule valores esperados de observáveis
- Interface V2 (StatevectorSampler, StatevectorEstimator)
- Primitives do IBM Quantum Runtime para hardware
- Modos de Sessions e Batch
- Binding de parâmetros

### 4. Transpiração e Otimização
Para otimizar circuitos e preparar para execução em hardware:
- **Veja `references/transpilation.md`**

Tópicos cobertos:
- Por que a transpiração é necessária
- Níveis de otimização (0-3)
- Seis estágios de transpiração (init, layout, routing, translation, optimization, scheduling)
- Recursos avançados (virtual permutation elision, cancelamento de portas)
- Parâmetros comuns (initial_layout, approximation_degree, seed)
- Melhores práticas para circuitos eficientes

### 5. Visualização
Para exibir circuitos, resultados e estados quânticos:
- **Veja `references/visualization.md`**

Tópicos cobertos:
- Desenhos de circuitos (texto, matplotlib, LaTeX)
- Histogramas de resultados
- Visualização de estado quântico (esfera de Bloch, state city, QSphere)
- Topologia de backend e mapas de erro
- Customização e estilo
- Salvando figuras em qualidade de publicação

### 6. Backends de Hardware
Para executar em simuladores e computadores quânticos reais:
- **Veja `references/backends.md`**

Tópicos cobertos:
- Backends IBM Quantum e autenticação
- Propriedades e status de backends
- Execução em hardware real com primitives de Runtime
- Gerenciamento de trabalhos e fila
- Modo Session (algoritmos iterativos)
- Modo Batch (trabalhos paralelos)
- Simuladores locais (StatevectorSampler, Aer)
- Provedores de terceiros (IonQ, Amazon Braket)
- Estratégias de mitigação de erro

### 7. Workflow Qiskit Patterns
Para implementar o workflow de computação quântica em quatro etapas:
- **Veja `references/patterns.md`**

Tópicos cobertos:
- **Map**: Traduza problemas para circuitos quânticos
- **Optimize**: Transpilar para hardware
- **Execute**: Execute com primitives
- **Post-process**: Extraia e analise resultados
- Exemplo VQE completo
- Execução Session vs. Batch
- Padrões de workflow comuns

### 8. Algoritmos e Aplicações Quânticas
Para implementar algoritmos quânticos específicos:
- **Veja `references/algorithms.md`**

Tópicos cobertos:
- **Otimização**: VQE, QAOA, algoritmo de Grover
- **Química**: Estados fundamentais moleculares, estados excitados, Hamiltonianos
- **Aprendizado de Máquina**: Kernels quânticos, VQC, QNN
- **Bibliotecas de algoritmos**: Qiskit Nature, Qiskit ML, Qiskit Optimization
- Simulações de física e benchmarking

## Guia de Decisão de Workflow

**Se você precisa:**

- Instalar Qiskit ou configurar conta IBM Quantum → `references/setup.md`
- Construir um novo circuito quântico → `references/circuits.md`
- Entender portas e operações de circuitos → `references/circuits.md`
- Executar circuitos e obter medições → `references/primitives.md`
- Calcular valores esperados → `references/primitives.md`
- Otimizar circuitos para hardware → `references/transpilation.md`
- Visualizar circuitos ou resultados → `references/visualization.md`
- Executar em hardware IBM Quantum → `references/backends.md`
- Conectar a provedores de terceiros → `references/backends.md`
- Implementar workflow quântico ponta a ponta → `references/patterns.md`
- Construir algoritmo específico (VQE, QAOA, etc.) → `references/algorithms.md`
- Resolver problemas de química ou otimização → `references/algorithms.md`

## Melhores Práticas

### Workflow de Desenvolvimento

1. **Comece com simuladores**: Teste localmente antes de usar hardware
   ```python
   from qiskit.primitives import StatevectorSampler
   sampler = StatevectorSampler()
   ```

2. **Sempre transpilar**: Otimize circuitos antes da execução
   ```python
   from qiskit import transpile
   qc_optimized = transpile(qc, backend=backend, optimization_level=3)
   ```

3. **Use primitives apropriados**:
   - Sampler para bitstrings (algoritmos de otimização)
   - Estimator para valores esperados (química, física)

4. **Escolha modo de execução**:
   - Session: Algoritmos iterativos (VQE, QAOA)
   - Batch: Trabalhos paralelos independentes
   - Trabalho único: Experimentos isolados

### Otimização de Desempenho

- Use optimization_level=3 para produção
- Minimize portas de dois qubits (fonte principal de erro)
- Teste com simuladores com ruído antes do hardware
- Salve e reutilize circuitos transpilados
- Monitore convergência em algoritmos variacionais

### Execução em Hardware

- Verifique status do backend antes de enviar
- Use least_busy() para testes
- Salve IDs de trabalhos para recuperação posterior
- Aplique mitigação de erro (resilience_level)
- Comece com menos shots, aumente para execuções finais

## Padrões Comuns

### Padrão 1: Execução Simples de Circuito

```python
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### Padrão 2: Execução em Hardware com Transpiração

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc_optimized = transpile(qc, backend=backend, optimization_level=3)

sampler = Sampler(backend)
job = sampler.run([qc_optimized], shots=1024)
result = job.result()
```

### Padrão 3: Algoritmo Variacional (VQE)

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from scipy.optimize import minimize

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    def cost_function(params):
        bound_qc = ansatz.assign_parameters(params)
        qc_isa = transpile(bound_qc, backend=backend)
        result = estimator.run([(qc_isa, hamiltonian)]).result()
        return result[0].data.evs

    result = minimize(cost_function, initial_params, method='COBYLA')
```

## Recursos Adicionais

- **Documentação Oficial**: https://quantum.ibm.com/docs
- **Qiskit Textbook**: https://qiskit.org/learn
- **Referência de API**: https://docs.quantum.ibm.com/api/qiskit
- **Guia de Patterns**: https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns