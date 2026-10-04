---
name: flowio
description: "Analise arquivos FCS (Flow Cytometry Standard) v2.0-3.1. Extraia eventos como arrays NumPy, leia metadados/canais, converta para CSV/DataFrame, para pré-processamento de dados de citometria de fluxo."
---

# FlowIO: Manipulador de Arquivos Flow Cytometry Standard

## Visão Geral

FlowIO é uma biblioteca Python leve para ler e escrever arquivos Flow Cytometry Standard (FCS). Analise metadados FCS, extraia dados de eventos e crie novos arquivos FCS com dependências mínimas. A biblioteca suporta as versões FCS 2.0, 3.0 e 3.1, sendo ideal para serviços backend, pipelines de dados e operações básicas de arquivos de citometria.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:

- Arquivos FCS precisam ser analisados ou ter metadados extraídos
- Dados de citometria de fluxo precisam ser convertidos em arrays NumPy
- Dados de eventos precisam ser exportados em formato FCS
- Arquivos FCS multi-dataset precisam ser separados
- Extração de informações de canais (scatter, fluorescência, tempo)
- Validação ou inspeção de arquivos de citometria
- Fluxos de pré-processamento antes de análise avançada

**Ferramentas Relacionadas:** Para análise avançada de citometria de fluxo, incluindo compensação, gating e suporte a FlowJo/GatingML, recomenda-se a biblioteca FlowKit como complemento ao FlowIO.

## Instalação

```bash
uv pip install flowio
```

Requer Python 3.9 ou posterior.

## Início Rápido

### Leitura Básica de Arquivo

```python
from flowio import FlowData

# Ler arquivo FCS
flow_data = FlowData('experiment.fcs')

# Acessar informações básicas
print(f"Versão FCS: {flow_data.version}")
print(f"Eventos: {flow_data.event_count}")
print(f"Canais: {flow_data.pnn_labels}")

# Obter dados de eventos como array NumPy
events = flow_data.as_array()  # Shape: (eventos, canais)
```

### Criando Arquivos FCS

```python
import numpy as np
from flowio import create_fcs

# Preparar dados
data = np.array([[100, 200, 50], [150, 180, 60]])  # 2 eventos, 3 canais
channels = ['FSC-A', 'SSC-A', 'FL1-A']

# Criar arquivo FCS
create_fcs('output.fcs', data, channels)
```

## Fluxos de Trabalho Principais

### Leitura e Análise de Arquivos FCS

A classe FlowData fornece a interface principal para ler arquivos FCS.

**Leitura Padrão:**

```python
from flowio import FlowData

# Leitura básica
flow = FlowData('sample.fcs')

# Acessar atributos
version = flow.version              # '3.0', '3.1', etc.
event_count = flow.event_count      # Número de eventos
channel_count = flow.channel_count  # Número de canais
pnn_labels = flow.pnn_labels        # Nomes curtos de canais
pns_labels = flow.pns_labels        # Nomes descritivos de marcadores

# Obter dados de eventos
events = flow.as_array()            # Pré-processados (ganho, escala log aplicados)
raw_events = flow.as_array(preprocess=False)  # Dados brutos
```

**Leitura Eficiente de Memória:**

Quando apenas metadados são necessários (sem dados de eventos):

```python
# Analisar apenas segmento TEXT, ignorar DATA e ANALYSIS
flow = FlowData('sample.fcs', only_text=True)

# Acessar metadados
metadata = flow.text  # Dicionário de palavras-chave do segmento TEXT
print(metadata.get('$DATE'))  # Data da aquisição
print(metadata.get('$CYT'))   # Nome do instrumento
```

**Tratamento de Arquivos Problemáticos:**

Alguns arquivos FCS têm discrepâncias de deslocamento ou erros:

```python
# Ignorar discrepâncias de deslocamento entre seções HEADER e TEXT
flow = FlowData('problematic.fcs', ignore_offset_discrepancy=True)

# Usar deslocamentos do HEADER em vez de deslocamentos do TEXT
flow = FlowData('problematic.fcs', use_header_offsets=True)

# Ignorar erros de deslocamento completamente
flow = FlowData('problematic.fcs', ignore_offset_error=True)
```

**Excluindo Canais Nulos:**

```python
# Excluir canais específicos durante análise
flow = FlowData('sample.fcs', null_channel_list=['Time', 'Null'])
```

### Extração de Metadados e Informações de Canais

Arquivos FCS contêm metadados ricos no segmento TEXT.

**Palavras-Chave de Metadados Comuns:**

```python
flow = FlowData('sample.fcs')

# Metadados no nível do arquivo
text_dict = flow.text
acquisition_date = text_dict.get('$DATE', 'Desconhecido')
instrument = text_dict.get('$CYT', 'Desconhecido')
data_type = flow.data_type  # 'I', 'F', 'D', 'A'

# Metadados do canal
for i in range(flow.channel_count):
    pnn = flow.pnn_labels[i]      # Nome curto (ex: 'FSC-A')
    pns = flow.pns_labels[i]      # Nome descritivo (ex: 'Forward Scatter')
    pnr = flow.pnr_values[i]      # Intervalo/valor máximo
    print(f"Canal {i}: {pnn} ({pns}), Intervalo: {pnr}")
```

**Identificação de Tipo de Canal:**

FlowIO categoriza automaticamente os canais:

```python
# Obter índices por tipo de canal
scatter_idx = flow.scatter_indices    # [0, 1] para FSC, SSC
fluoro_idx = flow.fluoro_indices      # [2, 3, 4] para canais FL
time_idx = flow.time_index            # Índice do canal de tempo (ou None)

# Acessar tipos de canal específicos
events = flow.as_array()
scatter_data = events[:, scatter_idx]
fluorescence_data = events[:, fluoro_idx]
```

**Segmento ANALYSIS:**

Se presente, acesse resultados processados:

```python
if flow.analysis:
    analysis_keywords = flow.analysis  # Dicionário de palavras-chave ANALYSIS
    print(analysis_keywords)
```

### Criação de Novos Arquivos FCS

Gere arquivos FCS a partir de arrays NumPy ou outras fontes de dados.

**Criação Básica:**

```python
import numpy as np
from flowio import create_fcs

# Criar dados de eventos (linhas=eventos, colunas=canais)
events = np.random.rand(10000, 5) * 1000

# Definir nomes de canais
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']

# Criar arquivo FCS
create_fcs('output.fcs', events, channel_names)
```

**Com Nomes Descritivos de Canais:**

```python
# Adicionar nomes descritivos opcionais (PnS)
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']
descriptive_names = ['Forward Scatter', 'Side Scatter', 'FITC', 'PE', 'Time']

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names)
```

**Com Metadados Personalizados:**

```python
# Adicionar metadados de segmento TEXT
metadata = {
    '$SRC': 'Script Python',
    '$DATE': '19-OCT-2025',
    '$CYT': 'Instrumento Sintético',
    '$INST': 'Laboratório A'
}

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names,
           metadata=metadata)
```

**Nota:** FlowIO exporta como FCS 3.1 com dados de ponto flutuante de precisão simples.

### Exportação de Dados Modificados

Modifique arquivos FCS existentes e exporte-os novamente.

**Abordagem 1: Usando Método write_fcs():**

```python
from flowio import FlowData

# Ler arquivo original
flow = FlowData('original.fcs')

# Escrever com metadados atualizados
flow.write_fcs('modified.fcs', metadata={'$SRC': 'Dados modificados'})
```

**Abordagem 2: Extrair, Modificar e Recriar:**

Para modificar dados de eventos:

```python
from flowio import FlowData, create_fcs

# Ler e extrair dados
flow = FlowData('original.fcs')
events = flow.as_array(preprocess=False)

# Modificar dados de eventos
events[:, 0] = events[:, 0] * 1.5  # Escalar primeiro canal

# Criar novo arquivo FCS com dados modificados
create_fcs('modified.fcs',
           events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata=flow.text)
```

### Tratamento de Arquivos FCS Multi-Dataset

Alguns arquivos FCS contêm múltiplos datasets em um único arquivo.

**Detecção de Arquivos Multi-Dataset:**

```python
from flowio import FlowData, MultipleDataSetsError

try:
    flow = FlowData('sample.fcs')
except MultipleDataSetsError:
    print("Arquivo contém múltiplos datasets")
    # Use read_multiple_data_sets() em vez disso
```

**Leitura de Todos os Datasets:**

```python
from flowio import read_multiple_data_sets

# Ler todos os datasets do arquivo
datasets = read_multiple_data_sets('multi_dataset.fcs')

print(f"Encontrados {len(datasets)} datasets")

# Processar cada dataset
for i, dataset in enumerate(datasets):
    print(f"\nDataset {i}:")
    print(f"  Eventos: {dataset.event_count}")
    print(f"  Canais: {dataset.pnn_labels}")

    # Obter dados de eventos para este dataset
    events = dataset.as_array()
    print(f"  Shape: {events.shape}")
    print(f"  Valores médios: {events.mean(axis=0)}")
```

**Leitura de Dataset Específico:**

```python
from flowio import FlowData

# Ler primeiro dataset (nextdata_offset=0)
first_dataset = FlowData('multi.fcs', nextdata_offset=0)

# Ler segundo dataset usando deslocamento NEXTDATA do primeiro
next_offset = int(first_dataset.text['$NEXTDATA'])
if next_offset > 0:
    second_dataset = FlowData('multi.fcs', nextdata_offset=next_offset)
```

## Pré-processamento de Dados

FlowIO aplica transformações de pré-processamento FCS padrão quando `preprocess=True`.

**Etapas de Pré-processamento:**

1. **Escala de Ganho:** Multiplicar valores por palavra-chave PnG (ganho)
2. **Transformação Logarítmica:** Aplicar transformação exponencial PnE se presente
   - Fórmula: `value = a * 10^(b * raw_value)` onde PnE = "a,b"
3. **Escala de Tempo:** Converter valores de tempo para unidades apropriadas

**Controle de Pré-processamento:**

```python
# Dados pré-processados (padrão)
preprocessed = flow.as_array(preprocess=True)

# Dados brutos (sem transformações)
raw = flow.as_array(preprocess=False)
```

## Tratamento de Erros

Trate exceções comuns do FlowIO apropriadamente.

```python
from flowio import (
    FlowData,
    FCSParsingError,
    DataOffsetDiscrepancyError,
    MultipleDataSetsError
)

try:
    flow = FlowData('sample.fcs')
    events = flow.as_array()

except FCSParsingError as e:
    print(f"Falha ao analisar arquivo FCS: {e}")
    # Tentar com análise relaxada
    flow = FlowData('sample.fcs', ignore_offset_error=True)

except DataOffsetDiscrepancyError as e:
    print(f"Discrepância de deslocamento detectada: {e}")
    # Usar parâmetro ignore_offset_discrepancy
    flow = FlowData('sample.fcs', ignore_offset_discrepancy=True)

except MultipleDataSetsError as e:
    print(f"Múltiplos datasets detectados: {e}")
    # Usar read_multiple_data_sets em vez disso
    from flowio import read_multiple_data_sets
    datasets = read_multiple_data_sets('sample.fcs')

except Exception as e:
    print(f"Erro inesperado: {e}")
```

## Casos de Uso Comuns

### Inspeção do Conteúdo de Arquivo FCS

Exploração rápida da estrutura de arquivo FCS:

```python
from flowio import FlowData

flow = FlowData('unknown.fcs')

print("=" * 50)
print(f"Arquivo: {flow.name}")
print(f"Versão: {flow.version}")
print(f"Tamanho: {flow.file_size:,} bytes")
print("=" * 50)

print(f"\nEventos: {flow.event_count:,}")
print(f"Canais: {flow.channel_count}")

print("\nInformações de Canal:")
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    ch_type = "scatter" if i in flow.scatter_indices else \
              "fluoro" if i in flow.fluoro_indices else \
              "time" if i == flow.time_index else "outro"
    print(f"  [{i}] {pnn:10s} | {pns:30s} | {ch_type}")

print("\nMetadados Principais:")
for key in ['$DATE', '$BTIM', '$ETIM', '$CYT', '$INST', '$SRC']:
    value = flow.text.get(key, 'N/D')
    print(f"  {key:15s}: {value}")
```

### Processamento em Lote de Múltiplos Arquivos

Processe um diretório de arquivos FCS:

```python
from pathlib import Path
from flowio import FlowData
import pandas as pd

# Encontrar todos os arquivos FCS
fcs_files = list(Path('data/').glob('*.fcs'))

# Extrair informações resumidas
summaries = []
for fcs_path in fcs_files:
    try:
        flow = FlowData(str(fcs_path), only_text=True)
        summaries.append({
            'filename': fcs_path.name,
            'version': flow.version,
            'events': flow.event_count,
            'channels': flow.channel_count,
            'date': flow.text.get('$DATE', 'N/D')
        })
    except Exception as e:
        print(f"Erro ao processar {fcs_path.name}: {e}")

# Criar DataFrame resumido
df = pd.DataFrame(summaries)
print(df)
```

### Conversão de FCS para CSV

Exporte dados de eventos em formato CSV:

```python
from flowio import FlowData
import pandas as pd

# Ler arquivo FCS
flow = FlowData('sample.fcs')

# Converter para DataFrame
df = pd.DataFrame(
    flow.as_array(),
    columns=flow.pnn_labels
)

# Adicionar metadados como atributos
df.attrs['fcs_version'] = flow.version
df.attrs['instrument'] = flow.text.get('$CYT', 'Desconhecido')

# Exportar para CSV
df.to_csv('output.csv', index=False)
print(f"Exportados {len(df)} eventos para CSV")
```

### Filtragem de Eventos e Re-exportação

Aplique filtros e salve dados filtrados:

```python
from flowio import FlowData, create_fcs
import numpy as np

# Ler arquivo original
flow = FlowData('sample.fcs')
events = flow.as_array(preprocess=False)

# Aplicar filtragem (exemplo: limite no primeiro canal)
fsc_idx = 0
threshold = 500
mask = events[:, fsc_idx] > threshold
filtered_events = events[mask]

print(f"Eventos originais: {len(events)}")
print(f"Eventos filtrados: {len(filtered_events)}")

# Criar novo arquivo FCS com dados filtrados
create_fcs('filtered.fcs',
           filtered_events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata={**flow.text, '$SRC': 'Dados filtrados'})
```

### Extração de Canais Específicos

Extraia e processe canais específicos:

```python
from flowio import FlowData
import numpy as np

flow = FlowData('sample.fcs')
events = flow.as_array()

# Extrair apenas canais de fluorescência
fluoro_indices = flow.fluoro_indices
fluoro_data = events[:, fluoro_indices]
fluoro_names = [flow.pnn_labels[i] for i in fluoro_indices]

print(f"Canais de fluorescência: {fluoro_names}")
print(f"Shape: {fluoro_data.shape}")

# Calcular estatísticas por canal
for i, name in enumerate(fluoro_names):
    channel_data = fluoro_data[:, i]
    print(f"\n{name}:")
    print(f"  Média: {channel_data.mean():.2f}")
    print(f"  Mediana: {np.median(channel_data):.2f}")
    print(f"  Desvio padrão: {channel_data.std():.2f}")
```

## Melhores Práticas

1. **Eficiência de Memória:** Use `only_text=True` quando dados de eventos não forem necessários
2. **Tratamento de Erros:** Envolva operações de arquivo em blocos try-except para código robusto
3. **Detecção Multi-Dataset:** Verifique MultipleDataSetsError e use função apropriada
4. **Controle de Pré-processamento:** Defina explicitamente parâmetro `preprocess` com base em necessidades de análise
5. **Problemas de Deslocamento:** Se análise falhar, tente parâmetro `ignore_offset_discrepancy=True`
6. **Validação de Canal:** Verifique contagens e nomes de canais antes do processamento
7. **Preservação de Metadados:** Ao modificar arquivos, preserve palavras-chave originais do segmento TEXT

## Tópicos Avançados

### Entendimento da Estrutura de Arquivo FCS

Arquivos FCS consistem em quatro segmentos:

1. **HEADER:** Versão FCS e deslocamentos de bytes para outros segmentos
2. **TEXT:** Pares chave-valor de metadados (separados por delimitadores)
3. **DATA:** Dados de evento brutos (formato binário/float/ASCII)
4. **ANALYSIS** (opcional): Resultados do processamento de dados

Acesse esses segmentos via atributos FlowData:
- `flow.header` - Segmento HEADER
- `flow.text` - Palavras-chave do segmento TEXT
- `flow.events` - Segmento DATA (como bytes)
- `flow.analysis` - Palavras-chave do segmento ANALYSIS (se presentes)

### Referência Detalhada da API

Para documentação abrangente da API, incluindo todos os parâmetros, métodos, exceções e referência de palavras-chave FCS, consulte o arquivo de referência detalhado:

**Leia:** `references/api_reference.md`

A referência inclui:
- Documentação completa da classe FlowData
- Todas as funções utilitárias (read_multiple_data_sets, create_fcs)
- Classes de exceção e tratamento
- Detalhes da estrutura de arquivo FCS
- Palavras-chave comuns do segmento TEXT
- Fluxos de trabalho com exemplos estendidos

Ao trabalhar com operações FCS complexas ou encontrar formatos de arquivo incomuns, carregue esta referência para orientação detalhada.

## Notas de Integração

**Arrays NumPy:** Todos os dados de eventos são retornados como ndarrays NumPy com shape (eventos, canais)

**DataFrames Pandas:** Converta facilmente em DataFrames para análise:
```python
import pandas as pd
df = pd.DataFrame(flow.as_array(), columns=flow.pnn_labels)
```

**Integração com FlowKit:** Para análise avançada (compensação, gating, suporte a FlowJo), use biblioteca FlowKit que se baseia nas capacidades de análise do FlowIO

**Aplicações Web:** As dependências mínimas do FlowIO o tornam ideal para serviços backend que processam uploads FCS

## Solução de Problemas

**Problema:** "Erro de discrepância de deslocamento"
**Solução:** Use parâmetro `ignore_offset_discrepancy=True`

**Problema:** "Erro de múltiplos datasets"
**Solução:** Use função `read_multiple_data_sets()` em vez do construtor FlowData

**Problema:** Memória insuficiente com arquivos grandes
**Solução:** Use `only_text=True` para operações apenas de metadados, ou processe eventos em chunks

**Problema:** Contagens de canal inesperadas
**Solução:** Verifique canais nulos; use parâmetro `null_channel_list` para excluir

**Problema:** Impossível modificar dados de eventos no local
**Solução:** FlowIO não suporta modificação direta; extraia dados, modifique e use `create_fcs()` para salvar

## Resumo

FlowIO fornece capacidades essenciais de manipulação de arquivos FCS para fluxos de trabalho de citometria de fluxo. Use-o para análise, extração de metadados e criação de arquivo. Para operações de arquivo simples e extração de dados, FlowIO é suficiente. Para análise complexa, incluindo compensação e gating, integre com FlowKit ou outras ferramentas especializadas.