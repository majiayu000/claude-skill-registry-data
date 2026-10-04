---
name: dask
description: "Computação paralela/distribuída. Escale pandas/NumPy além da memória disponível, DataFrames/Arrays paralelos, processamento multi-arquivo, grafos de tarefas, para datasets maiores que RAM e workflows paralelos."
---

# Dask

## Visão Geral

Dask é uma biblioteca Python para computação paralela e distribuída que habilita três capacidades críticas:
- **Execução maior que a memória** em máquinas individuais para dados que excedem a RAM disponível
- **Processamento paralelo** para melhor velocidade computacional entre múltiplos núcleos
- **Computação distribuída** suportando datasets em escala de terabytes entre múltiplas máquinas

Dask escala de laptops (processando ~100 GiB) para clusters (processando ~100 TiB) mantendo APIs Python familiares.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Processar datasets que excedem a RAM disponível
- Escalar operações pandas ou NumPy para datasets maiores
- Paralelizar computações para melhorias de performance
- Processar múltiplos arquivos eficientemente (CSVs, Parquet, JSON, logs de texto)
- Construir workflows paralelos customizados com dependências de tarefas
- Distribuir cargas de trabalho entre múltiplos núcleos ou máquinas

## Capacidades Principais

Dask fornece cinco componentes principais, cada um adequado para diferentes casos de uso:

### 1. DataFrames - Operações Paralelas com Pandas

**Propósito**: Escalar operações pandas para datasets maiores através de processamento paralelo.

**Quando Usar**:
- Dados tabulares excedem a RAM disponível
- Necessidade de processar múltiplos arquivos CSV/Parquet juntos
- Operações pandas são lentas e precisam de paralelização
- Escalar de prototipagem pandas para produção

**Documentação de Referência**: Para orientação completa sobre DataFrames Dask, consulte `references/dataframes.md` que inclui:
- Leitura de dados (arquivos únicos, múltiplos arquivos, padrões glob)
- Operações comuns (filtragem, groupby, joins, agregações)
- Operações customizadas com `map_partitions`
- Dicas de otimização de performance
- Padrões comuns (ETL, séries temporais, processamento multi-arquivo)

**Exemplo Rápido**:
```python
import dask.dataframe as dd

# Ler múltiplos arquivos como um único DataFrame
ddf = dd.read_csv('data/2024-*.csv')

# Operações são lazy até compute() ser chamado
filtered = ddf[ddf['value'] > 100]
result = filtered.groupby('category').mean().compute()
```

**Pontos-Chave**:
- Operações são lazy (constroem grafo de tarefas) até `.compute()` ser chamado
- Use `map_partitions` para operações customizadas eficientes
- Converta para DataFrame cedo quando trabalhar com dados estruturados de outras fontes

### 2. Arrays - Operações Paralelas com NumPy

**Propósito**: Estender capacidades NumPy para datasets maiores que a memória usando algoritmos de blocos.

**Quando Usar**:
- Arrays excedem a RAM disponível
- Operações NumPy precisam de paralelização
- Trabalhar com datasets científicos (HDF5, Zarr, NetCDF)
- Necessidade de álgebra linear paralela ou operações com arrays

**Documentação de Referência**: Para orientação completa sobre Arrays Dask, consulte `references/arrays.md` que inclui:
- Criar arrays (de NumPy, aleatório, do disco)
- Estratégias de chunking e otimização
- Operações comuns (aritmética, reduções, álgebra linear)
- Operações customizadas com `map_blocks`
- Integração com HDF5, Zarr e XArray

**Exemplo Rápido**:
```python
import dask.array as da

# Criar array grande com chunks
x = da.random.random((100000, 100000), chunks=(10000, 10000))

# Operações são lazy
y = x + 100
z = y.mean(axis=0)

# Computar resultado
result = z.compute()
```

**Pontos-Chave**:
- Tamanho de chunk é crítico (buscar ~100 MB por chunk)
- Operações funcionam em chunks em paralelo
- Rechunk dados quando necessário para operações eficientes
- Use `map_blocks` para operações não disponíveis em Dask

### 3. Bags - Processamento Paralelo de Dados Não-Estruturados

**Propósito**: Processar dados não-estruturados ou semi-estruturados (texto, JSON, logs) com operações funcionais.

**Quando Usar**:
- Processar arquivos de texto, logs ou registros JSON
- Limpeza de dados e ETL antes de análise estruturada
- Trabalhar com objetos Python que não se encaixam em formatos array/dataframe
- Necessidade de processamento streaming eficiente em memória

**Documentação de Referência**: Para orientação completa sobre Bags Dask, consulte `references/bags.md` que inclui:
- Leitura de arquivos de texto e JSON
- Operações funcionais (map, filter, fold, groupby)
- Conversão para DataFrames
- Padrões comuns (análise de logs, processamento JSON, processamento de texto)
- Considerações de performance

**Exemplo Rápido**:
```python
import dask.bag as db
import json

# Ler e analisar arquivos JSON
bag = db.read_text('logs/*.json').map(json.loads)

# Filtrar e transformar
valid = bag.filter(lambda x: x['status'] == 'valid')
processed = valid.map(lambda x: {'id': x['id'], 'value': x['value']})

# Converter para DataFrame para análise
ddf = processed.to_dataframe()
```

**Pontos-Chave**:
- Use para limpeza inicial de dados, depois converta para DataFrame/Array
- Use `foldby` em vez de `groupby` para melhor performance
- Operações são streaming e eficientes em memória
- Converta para formatos estruturados (DataFrame) para operações complexas

### 4. Futures - Paralelização Baseada em Tarefas

**Propósito**: Construir workflows paralelos customizados com controle fino sobre execução de tarefas e dependências.

**Quando Usar**:
- Construir workflows dinâmicos e evolutivos
- Necessidade de execução imediata de tarefas (não lazy)
- Computações dependem de condições de runtime
- Implementar algoritmos paralelos customizados
- Necessidade de computações com estado

**Documentação de Referência**: Para orientação completa sobre Futures Dask, consulte `references/futures.md` que inclui:
- Configurar cliente distribuído
- Submeter tarefas e trabalhar com futures
- Dependências de tarefas e movimento de dados
- Coordenação avançada (filas, locks, eventos, actors)
- Padrões comuns (varredura de parâmetros, tarefas dinâmicas, algoritmos iterativos)

**Exemplo Rápido**:
```python
from dask.distributed import Client

client = Client()  # Criar cluster local

# Submeter tarefas (executa imediatamente)
def process(x):
    return x ** 2

futures = client.map(process, range(100))

# Coletar resultados
results = client.gather(futures)

client.close()
```

**Pontos-Chave**:
- Requer cliente distribuído (mesmo para máquina única)
- Tarefas executam imediatamente quando submetidas
- Pré-scatter dados grandes para evitar transferências repetidas
- ~1ms de overhead por tarefa (não adequado para milhões de tarefas minúsculas)
- Use actors para workflows com estado

### 5. Schedulers - Backends de Execução

**Propósito**: Controlar como e onde tarefas Dask executam (threads, processos, distribuído).

**Quando Escolher Scheduler**:
- **Threads** (padrão): Operações NumPy/Pandas, bibliotecas que liberam GIL, benefício de memória compartilhada
- **Processes**: Código Python puro, processamento de texto, operações ligadas ao GIL
- **Synchronous**: Debugging com pdb, profiling, entender erros
- **Distributed**: Necessidade de dashboard, clusters multi-máquina, recursos avançados

**Documentação de Referência**: Para orientação completa sobre Schedulers Dask, consulte `references/schedulers.md` que inclui:
- Descrições detalhadas de schedulers e características
- Métodos de configuração (global, context manager, por-compute)
- Considerações de performance e overhead
- Padrões comuns e troubleshooting
- Configuração de threads para performance ótima

**Exemplo Rápido**:
```python
import dask
import dask.dataframe as dd

# Usar threads para DataFrame (padrão, bom para numérico)
ddf = dd.read_csv('data.csv')
result1 = ddf.mean().compute()  # Usa threads

# Usar processes para trabalho pesado em Python
import dask.bag as db
bag = db.read_text('logs/*.txt')
result2 = bag.map(python_function).compute(scheduler='processes')

# Usar synchronous para debugging
dask.config.set(scheduler='synchronous')
result3 = problematic_computation.compute()  # Pode usar pdb

# Usar distributed para monitoramento e escala
from dask.distributed import Client
client = Client()
result4 = computation.compute()  # Usa distributed com dashboard
```

**Pontos-Chave**:
- Threads: Menor overhead (~10 µs/tarefa), melhor para trabalho numérico
- Processes: Evita GIL (~10 ms/tarefa), melhor para trabalho Python
- Distributed: Dashboard de monitoramento (~1 ms/tarefa), escala para clusters
- Pode trocar schedulers por computação ou globalmente

## Melhores Práticas

Para orientação abrangente sobre otimização de performance, estratégias de gerenciamento de memória e armadilhas comuns a evitar, consulte `references/best-practices.md`. Princípios-chave incluem:

### Comece com Soluções Mais Simples
Antes de usar Dask, explore:
- Algoritmos melhores
- Formatos de arquivo eficientes (Parquet em vez de CSV)
- Código compilado (Numba, Cython)
- Amostragem de dados

### Regras Críticas de Performance

**1. Não Carregue Dados Localmente Depois Passe para Dask**
```python
# Errado: Carrega todos os dados em memória primeiro
import pandas as pd
df = pd.read_csv('large.csv')
ddf = dd.from_pandas(df, npartitions=10)

# Correto: Deixe Dask manipular o carregamento
import dask.dataframe as dd
ddf = dd.read_csv('large.csv')
```

**2. Evite Chamadas Repetidas a compute()**
```python
# Errado: Cada compute é separado
for item in items:
    result = dask_computation(item).compute()

# Correto: Um único compute para todos
computations = [dask_computation(item) for item in items]
results = dask.compute(*computations)
```

**3. Não Construa Grafos de Tarefas Excessivamente Grandes**
- Aumentar tamanhos de chunk se houver milhões de tarefas
- Use `map_partitions`/`map_blocks` para fundir operações
- Verificar tamanho do grafo de tarefas: `len(ddf.__dask_graph__())`

**4. Escolha Tamanhos de Chunk Apropriados**
- Alvo: ~100 MB por chunk (ou 10 chunks por núcleo em memória do worker)
- Muito grande: Overflow de memória
- Muito pequeno: Overhead de agendamento

**5. Use o Dashboard**
```python
from dask.distributed import Client
client = Client()
print(client.dashboard_link)  # Monitorar performance, identificar gargalos
```

## Padrões de Workflow Comuns

### Pipeline ETL
```python
import dask.dataframe as dd

# Extract: Ler dados
ddf = dd.read_csv('raw_data/*.csv')

# Transform: Limpar e processar
ddf = ddf[ddf['status'] == 'valid']
ddf['amount'] = ddf['amount'].astype('float64')
ddf = ddf.dropna(subset=['important_col'])

# Load: Agregar e salvar
summary = ddf.groupby('category').agg({'amount': ['sum', 'mean']})
summary.to_parquet('output/summary.parquet')
```

### Pipeline Não-Estruturado para Estruturado
```python
import dask.bag as db
import json

# Começar com Bag para dados não-estruturados
bag = db.read_text('logs/*.json').map(json.loads)
bag = bag.filter(lambda x: x['status'] == 'valid')

# Converter para DataFrame para análise estruturada
ddf = bag.to_dataframe()
result = ddf.groupby('category').mean().compute()
```

### Computação com Array em Larga Escala
```python
import dask.array as da

# Carregar ou criar array grande
x = da.from_zarr('large_dataset.zarr')

# Processar em chunks
normalized = (x - x.mean()) / x.std()

# Salvar resultado
da.to_zarr(normalized, 'normalized.zarr')
```

### Workflow Paralelo Customizado
```python
from dask.distributed import Client

client = Client()

# Scatter dataset grande uma única vez
data = client.scatter(large_dataset)

# Processar em paralelo com dependências
futures = []
for param in parameters:
    future = client.submit(process, data, param)
    futures.append(future)

# Coletar resultados
results = client.gather(futures)
```

## Selecionando o Componente Certo

Use este guia de decisão para escolher o componente Dask apropriado:

**Tipo de Dados**:
- Dados tabulares → **DataFrames**
- Arrays numéricos → **Arrays**
- Texto/JSON/logs → **Bags** (depois converter para DataFrame)
- Objetos Python customizados → **Bags** ou **Futures**

**Tipo de Operação**:
- Operações pandas padrão → **DataFrames**
- Operações NumPy padrão → **Arrays**
- Tarefas paralelas customizadas → **Futures**
- Processamento de texto/ETL → **Bags**

**Nível de Controle**:
- Alto nível, automático → **DataFrames/Arrays**
- Baixo nível, manual → **Futures**

**Tipo de Workflow**:
- Grafo de computação estático → **DataFrames/Arrays/Bags**
- Dinâmico, evolutivo → **Futures**

## Considerações de Integração

### Formatos de Arquivo
- **Eficientes**: Parquet, HDF5, Zarr (colunares, comprimidos, amigos de paralelização)
- **Compatíveis mas lentos**: CSV (use apenas para ingestão inicial)
- **Para Arrays**: HDF5, Zarr, NetCDF

### Conversão Entre Coleções
```python
# Bag → DataFrame
ddf = bag.to_dataframe()

# DataFrame → Array (para dados numéricos)
arr = ddf.to_dask_array(lengths=True)

# Array → DataFrame
ddf = dd.from_dask_array(arr, columns=['col1', 'col2'])
```

### Com Outras Bibliotecas
- **XArray**: Envolve arrays Dask com dimensões rotuladas (geoespacial, imaging)
- **Dask-ML**: Machine learning com APIs compatíveis com scikit-learn
- **Distributed**: Gerenciamento avançado de cluster e monitoramento

## Debugging e Desenvolvimento

### Workflow de Desenvolvimento Iterativo

1. **Testar em dados pequenos com scheduler synchronous**:
```python
dask.config.set(scheduler='synchronous')
result = computation.compute()  # Pode usar pdb, fácil debugging
```

2. **Validar com threads em amostra**:
```python
sample = ddf.head(1000)  # Amostra pequena
# Testar lógica, depois escalar para dataset completo
```

3. **Escalar com distributed para monitoramento**:
```python
from dask.distributed import Client
client = Client()
print(client.dashboard_link)  # Monitorar performance
result = computation.compute()
```

### Problemas Comuns

**Erros de Memória**:
- Diminuir tamanhos de chunk
- Usar `persist()` estrategicamente e deletar quando pronto
- Verificar memory leaks em funções customizadas

**Início Lento**:
- Grafo de tarefas muito grande (aumentar tamanhos de chunk)
- Use `map_partitions` ou `map_blocks` para reduzir tarefas

**Paralelização Pobre**:
- Chunks muito grandes (aumentar número de partições)
- Usar threads com código Python (trocar para processes)
- Dependências de dados impedindo paralelismo

## Arquivos de Referência

Todos os arquivos de documentação de referência podem ser lidos conforme necessário para informações detalhadas:

- `references/dataframes.md` - Guia completo de DataFrame Dask
- `references/arrays.md` - Guia completo de Array Dask
- `references/bags.md` - Guia completo de Bag Dask
- `references/futures.md` - Guia completo de Futures Dask e computação distribuída
- `references/schedulers.md` - Guia completo de seleção e configuração de scheduler
- `references/best-practices.md` - Otimização abrangente de performance e troubleshooting

Carregar estes arquivos quando usuários precisarem de informações detalhadas sobre componentes específicos Dask, operações ou padrões além da orientação rápida fornecida aqui.