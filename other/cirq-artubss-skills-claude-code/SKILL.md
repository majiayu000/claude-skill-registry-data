---
name: cirq
description: Framework de computação quântica para construir, simular, otimizar e executar circuitos quânticos. Use esta skill ao trabalhar com algoritmos quânticos, design de circuitos quânticos, simulação quântica (com ou sem ruído), execução em hardware quântico (Google, IonQ, AQT, Pasqal), otimização e compilação de circuitos, modelagem e caracterização de ruído, ou experimentos e benchmarking quântico (VQE, QAOA, QPE, randomized benchmarking).
---

# Cirq - Computação Quântica com Python

Cirq é o framework open-source do Google Quantum AI para projetar, simular e executar circuitos quânticos em computadores quânticos e simuladores.

## Instalação

```bash
uv pip install cirq
```

Para integração com hardware:
```bash
# Google Quantum Engine
uv pip install cirq-google

# IonQ
uv pip install cirq-ionq

# AQT (Alpine Quantum Technologies)
uv pip install cirq-aqt

# Pasqal
uv pip install cirq-pasqal

# Azure Quantum
uv pip install azure-quantum cirq
```

## Início Rápido

### Circuito Básico

```python
import cirq
import numpy as np

# Criar qubits
q0, q1 = cirq.LineQubit.range(2)

# Construir circuito
circuit = cirq.Circuit(
    cirq.H(q0),              # Hadamard em q0
    cirq.CNOT(q0, q1),       # CNOT com q0 controle, q1 alvo
    cirq.measure(q0, q1, key='result')
)

print(circuit)

# Simular
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)

# Exibir resultados
print(result.histogram(key='result'))
```

### Circuito Parametrizado

```python
import sympy

# Definir parâmetro simbólico
theta = sympy.Symbol('theta')

# Criar circuito parametrizado
circuit = cirq.Circuit(
    cirq.ry(theta)(q0),
    cirq.measure(q0, key='m')
)

# Varrer valores de parâmetros
sweep = cirq.Linspace('theta', start=0, stop=2*np.pi, length=20)
results = simulator.run_sweep(circuit, params=sweep, repetitions=1000)

# Processar resultados
for params, result in zip(sweep, results):
    theta_val = params['theta']
    counts = result.histogram(key='m')
    print(f"θ={theta_val:.2f}: {counts}")
```

## Capacidades Principais

### Construção de Circuitos
Para informações abrangentes sobre construção de circuitos quânticos, incluindo qubits, gates, operações, gates customizados e padrões de circuitos, consulte:
- **[references/building.md](references/building.md)** - Guia completo de construção de circuitos

Tópicos comuns:
- Tipos de qubit (GridQubit, LineQubit, NamedQubit)
- Gates de um e dois qubits
- Gates e operações parametrizadas
- Decomposição de gates customizados
- Organização de circuitos com moments
- Padrões de circuitos padrão (estados Bell, GHZ, QFT)
- Importar/exportar (OpenQASM, JSON)
- Trabalhar com qudits e observáveis

### Simulação
Para informações detalhadas sobre simulação de circuitos quânticos, incluindo simulação exata, simulação com ruído, varreduras de parâmetros e a Máquina Virtual Quântica, consulte:
- **[references/simulation.md](references/simulation.md)** - Guia completo de simulação quântica

Tópicos comuns:
- Simulação exata (vetor de estado, matriz densidade)
- Amostragem e medições
- Varreduras de parâmetros (parâmetros únicos e múltiplos)
- Simulação com ruído
- Histogramas de estado e visualização
- Máquina Virtual Quântica (QVM)
- Valores esperados e observáveis
- Otimização de desempenho

### Transformação de Circuitos
Para informações sobre otimização, compilação e manipulação de circuitos quânticos, consulte:
- **[references/transformation.md](references/transformation.md)** - Guia completo de transformações de circuitos

Tópicos comuns:
- Framework de transformer
- Decomposição de gates
- Otimização de circuitos (mesclar gates, ejetar gates Z, eliminar operações negligenciáveis)
- Compilação de circuitos para hardware
- Roteamento de qubits e inserção de SWAP
- Transformers customizados
- Pipelines de transformação

### Integração com Hardware
Para informações sobre execução de circuitos em hardware quântico real de vários provedores, consulte:
- **[references/hardware.md](references/hardware.md)** - Guia completo de integração com hardware

Provedores suportados:
- **Google Quantum AI** (cirq-google) - Processadores Sycamore, Weber
- **IonQ** (cirq-ionq) - Computadores quânticos de íon aprisionado
- **Azure Quantum** (azure-quantum) - Backends IonQ e Honeywell
- **AQT** (cirq-aqt) - Alpine Quantum Technologies
- **Pasqal** (cirq-pasqal) - Computadores quânticos de átomo neutro

Os tópicos incluem representação de dispositivos, seleção de qubits, autenticação, gerenciamento de jobs e otimização de circuitos para hardware.

### Modelagem de Ruído
Para informações sobre modelagem de ruído, simulação com ruído, caracterização e mitigação de erros, consulte:
- **[references/noise.md](references/noise.md)** - Guia completo de modelagem de ruído

Tópicos comuns:
- Canais de ruído (depolarização, amortecimento de amplitude, amortecimento de fase)
- Modelos de ruído (constante, específico de gate, específico de qubit, térmico)
- Adicionar ruído a circuitos
- Ruído de leitura
- Caracterização de ruído (randomized benchmarking, XEB)
- Visualização de ruído (heatmaps)
- Técnicas de mitigação de erros

### Experimentos Quânticos
Para informações sobre design de experimentos, varreduras de parâmetros, coleta de dados e uso do framework ReCirq, consulte:
- **[references/experiments.md](references/experiments.md)** - Guia completo de experimentos quânticos

Tópicos comuns:
- Padrões de design de experimentos
- Varreduras de parâmetros e coleta de dados
- Estrutura do framework ReCirq
- Algoritmos comuns (VQE, QAOA, QPE)
- Análise e visualização de dados
- Análise estatística e estimativa de fidelidade
- Coleta de dados em paralelo

## Padrões Comuns

### Template de Algoritmo Variacional

```python
import scipy.optimize

def variational_algorithm(ansatz, cost_function, initial_params):
    """Template para algoritmos quânticos variacionais."""

    def objective(params):
        circuit = ansatz(params)
        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)
        return cost_function(result)

    # Otimizar
    result = scipy.optimize.minimize(
        objective,
        initial_params,
        method='COBYLA'
    )

    return result

# Definir ansatz
def my_ansatz(params):
    q = cirq.LineQubit(0)
    return cirq.Circuit(
        cirq.ry(params[0])(q),
        cirq.rz(params[1])(q)
    )

# Definir função de custo
def my_cost(result):
    state = result.final_state_vector
    # Calcular custo baseado no estado
    return np.real(state[0])

# Executar otimização
result = variational_algorithm(my_ansatz, my_cost, [0.0, 0.0])
```

### Template de Execução em Hardware

```python
def run_on_hardware(circuit, provider='google', device_name='weber', repetitions=1000):
    """Template para executar em hardware quântico."""

    if provider == 'google':
        import cirq_google
        engine = cirq_google.get_engine()
        processor = engine.get_processor(device_name)
        job = processor.run(circuit, repetitions=repetitions)
        return job.results()[0]

    elif provider == 'ionq':
        import cirq_ionq
        service = cirq_ionq.Service()
        result = service.run(circuit, repetitions=repetitions, target='qpu')
        return result

    elif provider == 'azure':
        from azure.quantum.cirq import AzureQuantumService
        # Configurar workspace...
        service = AzureQuantumService(workspace)
        result = service.run(circuit, repetitions=repetitions, target='ionq.qpu')
        return result

    else:
        raise ValueError(f"Unknown provider: {provider}")
```

### Template de Estudo de Ruído

```python
def noise_comparison_study(circuit, noise_levels):
    """Comparar desempenho do circuito em diferentes níveis de ruído."""

    results = {}

    for noise_level in noise_levels:
        # Criar circuito com ruído
        noisy_circuit = circuit.with_noise(cirq.depolarize(p=noise_level))

        # Simular
        simulator = cirq.DensityMatrixSimulator()
        result = simulator.run(noisy_circuit, repetitions=1000)

        # Analisar
        results[noise_level] = {
            'histogram': result.histogram(key='result'),
            'dominant_state': max(
                result.histogram(key='result').items(),
                key=lambda x: x[1]
            )
        }

    return results

# Executar estudo
noise_levels = [0.0, 0.001, 0.01, 0.05, 0.1]
results = noise_comparison_study(circuit, noise_levels)
```

## Melhores Práticas

1. **Design de Circuitos**
   - Use tipos de qubit apropriados para sua topologia
   - Mantenha circuitos modulares e reutilizáveis
   - Rotule medições com chaves descritivas
   - Valide circuitos contra restrições de dispositivos antes da execução

2. **Simulação**
   - Use simulação de vetor de estado para estados puros (mais eficiente)
   - Use simulação de matriz densidade apenas quando necessário (estados mistos, ruído)
   - Aproveite varreduras de parâmetros em vez de execuções individuais
   - Monitore o uso de memória para sistemas grandes (2^n cresce rapidamente)

3. **Execução em Hardware**
   - Sempre teste em simuladores primeiro
   - Selecione os melhores qubits usando dados de calibração
   - Otimize circuitos para o gateset do hardware alvo
   - Implemente mitigação de erros para execuções em produção
   - Armazene resultados de hardware caros imediatamente

4. **Otimização de Circuitos**
   - Comece com transformers built-in de alto nível
   - Encadeie múltiplas otimizações em sequência
   - Acompanhe a redução de profundidade e contagem de gates
   - Valide a correção após a transformação

5. **Modelagem de Ruído**
   - Use modelos de ruído realistas a partir de dados de calibração
   - Inclua todas as fontes de erro (gate, decoerência, leitura)
   - Caracterize antes de mitigar
   - Mantenha circuitos rasos para minimizar acúmulo de ruído

6. **Experimentos**
   - Estruture experimentos com separação clara (geração de dados, coleta, análise)
   - Use padrões ReCirq para reprodutibilidade
   - Salve resultados intermediários com frequência
   - Paralelizar tarefas independentes
   - Documente completamente com metadados

## Recursos Adicionais

- **Documentação Oficial**: https://quantumai.google/cirq
- **Referência de API**: https://quantumai.google/reference/python/cirq
- **Tutoriais**: https://quantumai.google/cirq/tutorials
- **Exemplos**: https://github.com/quantumlib/Cirq/tree/master/examples
- **ReCirq**: https://github.com/quantumlib/ReCirq

## Problemas Comuns

**Circuito muito profundo para hardware:**
- Use transformers de otimização de circuitos para reduzir profundidade
- Consulte `transformation.md` para técnicas de otimização

**Problemas de memória na simulação:**
- Mude de simulador de matriz densidade para simulador de vetor de estado
- Reduza o número de qubits ou use simulador stabilizer para circuitos Clifford

**Erros de validação de dispositivos:**
- Verifique conectividade de qubits com device.metadata.nx_graph
- Decomponha gates para gateset nativo do dispositivo
- Consulte `hardware.md` para compilação específica de dispositivos

**Simulação com ruído muito lenta:**
- Simulação de matriz densidade é O(2^2n) - considere reduzir qubits
- Use modelos de ruído seletivamente apenas em operações críticas
- Consulte `simulation.md` para otimização de desempenho