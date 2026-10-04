---
name: simpy
description: Framework de simulação de eventos discretos baseado em processos em Python. Use essa habilidade ao construir simulações de sistemas com processos, filas, recursos e eventos baseados em tempo, como sistemas de manufatura, operações de serviço, tráfego de rede, logística, ou qualquer sistema onde entidades interagem com recursos compartilhados ao longo do tempo.
---

# SimPy - Simulação de Eventos Discretos

## Visão Geral

SimPy é um framework de simulação de eventos discretos baseado em processos, construído sobre Python padrão. Use SimPy para modelar sistemas onde entidades (clientes, veículos, pacotes, etc.) interagem entre si e competem por recursos compartilhados (servidores, máquinas, largura de banda, etc.) ao longo do tempo.

**Capacidades principais:**
- Modelagem de processos usando funções geradoras Python
- Gerenciamento de recursos compartilhados (servidores, contêineres, stores)
- Agendamento e sincronização orientados a eventos
- Simulações em tempo real sincronizadas com tempo de parede
- Monitoramento abrangente e coleta de dados

## Quando Usar Essa Habilidade

Use a habilidade SimPy quando:

1. **Modelar sistemas de eventos discretos** - Sistemas onde eventos ocorrem em intervalos irregulares
2. **Contenção de recursos** - Entidades competem por recursos limitados (servidores, máquinas, pessoal)
3. **Análise de filas** - Estudar linhas de espera, tempos de serviço e throughput
4. **Otimização de processos** - Analisar processos de manufatura, logística ou serviços
5. **Simulação de rede** - Roteamento de pacotes, alocação de banda, análise de latência
6. **Planejamento de capacidade** - Determinar níveis ótimos de recursos para desempenho desejado
7. **Validação de sistema** - Testar comportamento do sistema antes da implementação

**Não adequado para:**
- Simulações contínuas com passos de tempo fixos (considere resolvedores ODE do SciPy)
- Processos independentes sem compartilhamento de recursos
- Otimização matemática pura (considere SciPy optimize)

## Início Rápido

### Estrutura Básica de Simulação

```python
import simpy

def process(env, name):
    """A simple process that waits and prints."""
    print(f'{name} starting at {env.now}')
    yield env.timeout(5)
    print(f'{name} finishing at {env.now}')

# Create environment
env = simpy.Environment()

# Start processes
env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))

# Run simulation
env.run(until=10)
```

### Padrão de Uso de Recurso

```python
import simpy

def customer(env, name, resource):
    """Customer requests resource, uses it, then releases."""
    with resource.request() as req:
        yield req  # Wait for resource
        print(f'{name} got resource at {env.now}')
        yield env.timeout(3)  # Use resource
        print(f'{name} released resource at {env.now}')

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer(env, 'Customer 1', server))
env.process(customer(env, 'Customer 2', server))
env.run()
```

## Conceitos Principais

### 1. Environment

O ambiente de simulação gerencia o tempo e agenda eventos.

```python
import simpy

# Standard environment (runs as fast as possible)
env = simpy.Environment(initial_time=0)

# Real-time environment (synchronized with wall-clock)
import simpy.rt
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)

# Run simulation
env.run(until=100)  # Run until time 100
env.run()  # Run until no events remain
```

### 2. Processos

Processos são definidos usando funções geradoras Python (funções com instruções `yield`).

```python
def my_process(env, param1, param2):
    """Process that yields events to pause execution."""
    print(f'Starting at {env.now}')

    # Wait for time to pass
    yield env.timeout(5)

    print(f'Resumed at {env.now}')

    # Wait for another event
    yield env.timeout(3)

    print(f'Done at {env.now}')
    return 'result'

# Start the process
env.process(my_process(env, 'value1', 'value2'))
```

### 3. Eventos

Eventos são o mecanismo fundamental para sincronização de processos. Processos fazem yield de eventos e retomam quando esses eventos são acionados.

**Tipos de eventos comuns:**
- `env.timeout(delay)` - Aguardar passagem de tempo
- `resource.request()` - Solicitar um recurso
- `env.event()` - Criar um evento personalizado
- `env.process(func())` - Processo como um evento
- `event1 & event2` - Aguardar todos os eventos (AllOf)
- `event1 | event2` - Aguardar qualquer evento (AnyOf)

## Recursos

SimPy fornece vários tipos de recursos para cenários diferentes. Para detalhes abrangentes, consulte `references/resources.md`.

### Resumo de Tipos de Recursos

| Tipo de Recurso | Caso de Uso |
|-----------------|------------|
| Resource | Capacidade limitada (servidores, máquinas) |
| PriorityResource | Fila baseada em prioridade |
| PreemptiveResource | Alta prioridade pode interromper baixa prioridade |
| Container | Materiais em massa (combustível, água) |
| Store | Armazenamento de objetos Python (FIFO) |
| FilterStore | Recuperação seletiva de itens |
| PriorityStore | Itens ordenados por prioridade |

### Referência Rápida

```python
import simpy

env = simpy.Environment()

# Basic resource (e.g., servers)
resource = simpy.Resource(env, capacity=2)

# Priority resource
priority_resource = simpy.PriorityResource(env, capacity=1)

# Container (e.g., fuel tank)
fuel_tank = simpy.Container(env, capacity=100, init=50)

# Store (e.g., warehouse)
warehouse = simpy.Store(env, capacity=10)
```

## Padrões de Simulação Comuns

### Padrão 1: Fila Cliente-Servidor

```python
import simpy
import random

def customer(env, name, server):
    arrival = env.now
    with server.request() as req:
        yield req
        wait = env.now - arrival
        print(f'{name} waited {wait:.2f}, served at {env.now}')
        yield env.timeout(random.uniform(2, 4))

def customer_generator(env, server):
    i = 0
    while True:
        yield env.timeout(random.uniform(1, 3))
        i += 1
        env.process(customer(env, f'Customer {i}', server))

env = simpy.Environment()
server = simpy.Resource(env, capacity=2)
env.process(customer_generator(env, server))
env.run(until=20)
```

### Padrão 2: Produtor-Consumidor

```python
import simpy

def producer(env, store):
    item_id = 0
    while True:
        yield env.timeout(2)
        item = f'Item {item_id}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')
        item_id += 1

def consumer(env, store):
    while True:
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')
        yield env.timeout(3)

env = simpy.Environment()
store = simpy.Store(env, capacity=10)
env.process(producer(env, store))
env.process(consumer(env, store))
env.run(until=20)
```

### Padrão 3: Execução de Tarefas em Paralelo

```python
import simpy

def task(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} done at {env.now}')
    return f'{name} result'

def coordinator(env):
    # Start tasks in parallel
    task1 = env.process(task(env, 'Task 1', 5))
    task2 = env.process(task(env, 'Task 2', 3))
    task3 = env.process(task(env, 'Task 3', 4))

    # Wait for all to complete
    results = yield task1 & task2 & task3
    print(f'All done at {env.now}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

## Guia de Workflow

### Passo 1: Defina o Sistema

Identifique:
- **Entidades**: O que se move pelo sistema? (clientes, peças, pacotes)
- **Recursos**: Quais são as restrições? (servidores, máquinas, banda)
- **Processos**: Quais são as atividades? (chegada, serviço, partida)
- **Métricas**: O que medir? (tempos de espera, utilização, throughput)

### Passo 2: Implemente Funções de Processo

Crie funções geradoras para cada tipo de processo:

```python
def entity_process(env, name, resources, parameters):
    # Arrival logic
    arrival_time = env.now

    # Request resources
    with resource.request() as req:
        yield req

        # Service logic
        service_time = calculate_service_time(parameters)
        yield env.timeout(service_time)

    # Departure logic
    collect_statistics(env.now - arrival_time)
```

### Passo 3: Configure Monitoramento

Use utilitários de monitoramento para coletar dados. Consulte `references/monitoring.md` para técnicas abrangentes.

```python
from scripts.resource_monitor import ResourceMonitor

# Create and monitor resource
resource = simpy.Resource(env, capacity=2)
monitor = ResourceMonitor(env, resource, "Server")

# After simulation
monitor.report()
```

### Passo 4: Execute e Analise

```python
# Run simulation
env.run(until=simulation_time)

# Generate reports
monitor.report()
stats.report()

# Export data for further analysis
monitor.export_csv('results.csv')
```

## Recursos Avançados

### Interação de Processos

Processos podem interagir através de eventos, yields de processos e interrupções. Consulte `references/process-interaction.md` para padrões detalhados.

**Mecanismos principais:**
- **Sinalização de eventos**: Eventos compartilhados para coordenação
- **Yields de processo**: Aguardar conclusão de outros processos
- **Interrupções**: Retomar processos forcadamente para preempção

### Simulações em Tempo Real

Sincronize a simulação com o tempo de parede para aplicações hardware-in-the-loop ou interativas. Consulte `references/real-time.md`.

```python
import simpy.rt

env = simpy.rt.RealtimeEnvironment(factor=1.0)  # 1:1 time mapping
# factor=0.5 means 1 sim unit = 0.5 seconds (2x faster)
```

### Monitoramento Abrangente

Monitore processos, recursos e eventos. Consulte `references/monitoring.md` para técnicas incluindo:
- Rastreamento de variáveis de estado
- Monkey-patching de recursos
- Rastreamento de eventos
- Coleta estatística

## Scripts e Templates

### basic_simulation_template.py

Template completo para construir simulações de fila com:
- Parâmetros configuráveis
- Coleta de estatísticas
- Geração de clientes
- Uso de recursos
- Geração de relatórios

**Uso:**
```python
from scripts.basic_simulation_template import SimulationConfig, run_simulation

config = SimulationConfig()
config.num_resources = 2
config.sim_time = 100
stats = run_simulation(config)
stats.report()
```

### resource_monitor.py

Utilitários de monitoramento reutilizáveis:
- `ResourceMonitor` - Rastrear recurso único
- `MultiResourceMonitor` - Monitorar múltiplos recursos
- `ContainerMonitor` - Rastrear níveis de contêiner
- Cálculo automático de estatísticas
- Funcionalidade de exportação CSV

**Uso:**
```python
from scripts.resource_monitor import ResourceMonitor

monitor = ResourceMonitor(env, resource, "My Resource")
# ... run simulation ...
monitor.report()
monitor.export_csv('data.csv')
```

## Documentação de Referência

Guias detalhados para tópicos específicos:

- **`references/resources.md`** - Todos os tipos de recursos com exemplos
- **`references/events.md`** - Sistema de eventos e padrões
- **`references/process-interaction.md`** - Sincronização de processos
- **`references/monitoring.md`** - Técnicas de coleta de dados
- **`references/real-time.md`** - Configuração de simulação em tempo real

## Boas Práticas

1. **Funções geradoras**: Sempre use `yield` em funções de processo
2. **Gerenciadores de contexto de recurso**: Use `with resource.request() as req:` para limpeza automática
3. **Reprodutibilidade**: Configure `random.seed()` para resultados consistentes
4. **Monitoramento**: Colete dados durante a simulação, não apenas no final
5. **Validação**: Compare casos simples com soluções analíticas
6. **Documentação**: Comente a lógica de processo e escolhas de parâmetros
7. **Design modular**: Separe lógica de processo, estatísticas e configuração

## Armadilhas Comuns

1. **Esquecer yield**: Processos devem fazer yield de eventos para pausar
2. **Reutilização de eventos**: Eventos podem ser acionados apenas uma vez
3. **Vazamento de recursos**: Use gerenciadores de contexto ou garanta liberação
4. **Operações bloqueantes**: Evite chamadas Python bloqueantes em processos
5. **Unidades de tempo**: Mantenha consistência na interpretação de unidades de tempo
6. **Deadlocks**: Garanta que pelo menos um processo possa fazer progresso

## Exemplos de Casos de Uso

- **Manufatura**: Agendamento de máquinas, linhas de produção, gerenciamento de inventário
- **Saúde**: Simulação de sala de emergência, fluxo de pacientes, alocação de pessoal
- **Telecomunicações**: Tráfego de rede, roteamento de pacotes, alocação de banda
- **Transporte**: Fluxo de tráfego, logística, roteamento de veículos
- **Operações de serviço**: Call centers, checkout de varejo, agendamento de consultas
- **Sistemas de computador**: Agendamento de CPU, gerenciamento de memória, operações de E/S