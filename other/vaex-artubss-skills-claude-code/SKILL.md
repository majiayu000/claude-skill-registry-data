---
name: vaex
description: Use essa skill para processar e analisar grandes conjuntos de dados tabulares (bilhões de linhas) que excedem a RAM disponível. Vaex excels em operações DataFrame out-of-core, avaliação lazy, agregações rápidas, visualização eficiente de big data e machine learning em datasets grandes. Aplique quando usuários precisarem trabalhar com arquivos CSV/HDF5/Arrow/Parquet grandes, realizar estatísticas rápidas em datasets massivos, criar visualizações de big data ou construir pipelines de ML que não cabem em memória.
---

# Vaex

## Visão Geral

Vaex é uma biblioteca Python de alta performance projetada para DataFrames lazy e out-of-core, para processar e visualizar conjuntos de dados tabulares muito grandes para caber em RAM. Vaex pode processar mais de um bilhão de linhas por segundo, permitindo exploração de dados interativa e análise em datasets com bilhões de linhas.

## Quando Usar Esta Skill

Use Vaex quando:
- Processar conjuntos de dados tabulares maiores que a RAM disponível (gigabytes a terabytes)
- Realizar agregações estatísticas rápidas em datasets massivos
- Criar visualizações e heatmaps de grandes conjuntos de dados
- Construir pipelines de machine learning em big data
- Converter entre formatos de dados (CSV, HDF5, Arrow, Parquet)
- Precisar de avaliação lazy e colunas virtuais para evitar overhead de memória
- Trabalhar com dados astronômicos, séries temporais financeiras ou outros datasets científicos em larga escala

## Capacidades Principais

Vaex fornece seis áreas principais de capacidade, cada uma documentada em detalhes no diretório references:

### 1. DataFrames e Carregamento de Dados

Carregue e crie DataFrames Vaex de várias fontes, incluindo arquivos (HDF5, CSV, Arrow, Parquet), DataFrames pandas, arrays NumPy e dicionários. Consulte `references/core_dataframes.md` para:
- Abrir arquivos grandes eficientemente
- Converter de pandas/NumPy/Arrow
- Trabalhar com datasets de exemplo
- Entender a estrutura de DataFrames

### 2. Processamento e Manipulação de Dados

Realize filtragem, crie colunas virtuais, use expressões e agregue dados sem carregar tudo na memória. Consulte `references/data_processing.md` para:
- Filtragem e seleções
- Colunas virtuais e expressões
- Operações groupby e agregações
- Operações com strings e manipulação de datetime
- Trabalhar com dados faltantes

### 3. Performance e Otimização

Aproveite a avaliação lazy de Vaex, estratégias de cache e operações eficientes em memória. Consulte `references/performance.md` para:
- Entender avaliação lazy
- Usar `delay=True` para operações em lote
- Materializar colunas quando necessário
- Estratégias de cache
- Operações assíncronas

### 4. Visualização de Dados

Crie visualizações interativas de grandes conjuntos de dados, incluindo heatmaps, histogramas e scatter plots. Consulte `references/visualization.md` para:
- Criar plots 1D e 2D
- Visualizações de heatmap
- Trabalhar com seleções
- Personalizar plots e subplots

### 5. Integração de Machine Learning

Construa pipelines de ML com transformers, encoders e integração com scikit-learn, XGBoost e outros frameworks. Consulte `references/machine_learning.md` para:
- Escalabilidade de features e encoding
- PCA e redução de dimensionalidade
- Clustering K-means
- Integração com scikit-learn/XGBoost/CatBoost
- Serialização e deploy de modelos

### 6. Operações de I/O

Leia e escreva dados eficientemente em vários formatos com performance otimizada. Consulte `references/io_operations.md` para:
- Recomendações de formato de arquivo
- Estratégias de export
- Trabalhar com Apache Arrow
- Manipulação de CSV para arquivos grandes
- Acesso a dados remotos e em servidor

## Padrão Quick Start

Para a maioria das tarefas Vaex, siga este padrão:

```python
import vaex

# 1. Abrir ou criar DataFrame
df = vaex.open('large_file.hdf5')  # ou .csv, .arrow, .parquet
# OU
df = vaex.from_pandas(pandas_df)

# 2. Explorar os dados
print(df)  # Mostra primeiras/últimas linhas e info de colunas
df.describe()  # Resumo estatístico

# 3. Criar colunas virtuais (sem overhead de memória)
df['new_column'] = df.x ** 2 + df.y

# 4. Filtrar com seleções
df_filtered = df[df.age > 25]

# 5. Computar estatísticas (rápido, avaliação lazy)
mean_val = df.x.mean()
stats = df.groupby('category').agg({'value': 'sum'})

# 6. Visualizar
df.plot1d(df.x, limits=[0, 100])
df.plot(df.x, df.y, limits='99.7%')

# 7. Exportar se necessário
df.export_hdf5('output.hdf5')
```

## Trabalhando com Referencias

Os arquivos de referência contêm informações detalhadas sobre cada área de capacidade. Carregue referencias no contexto conforme a tarefa específica:

- **Operações básicas**: Comece com `references/core_dataframes.md` e `references/data_processing.md`
- **Problemas de performance**: Verifique `references/performance.md`
- **Tarefas de visualização**: Use `references/visualization.md`
- **Pipelines de ML**: Consulte `references/machine_learning.md`
- **I/O de arquivos**: Consulte `references/io_operations.md`

## Boas Práticas

1. **Use formatos HDF5 ou Apache Arrow** para performance otimizada com grandes conjuntos de dados
2. **Aproveite colunas virtuais** em vez de materializar dados para economizar memória
3. **Processe em lotes** usando `delay=True` ao executar múltiplos cálculos
4. **Exporte para formatos eficientes** em vez de manter dados em CSV
5. **Use expressões** para cálculos complexos sem armazenamento intermediário
6. **Perfil com `df.stat()`** para entender uso de memória e otimizar operações

## Padrões Comuns

### Padrão: Converter Large CSV para HDF5
```python
import vaex

# Abrir large CSV (processa em chunks automaticamente)
df = vaex.from_csv('large_file.csv')

# Exportar para HDF5 para acesso mais rápido no futuro
df.export_hdf5('large_file.hdf5')

# Carregamentos futuros são instantâneos
df = vaex.open('large_file.hdf5')
```

### Padrão: Agregações Eficientes
```python
# Use delay=True para operações em lote
mean_x = df.x.mean(delay=True)
std_y = df.y.std(delay=True)
sum_z = df.z.sum(delay=True)

# Executa tudo de uma vez
results = vaex.execute([mean_x, std_y, sum_z])
```

### Padrão: Colunas Virtuais para Feature Engineering
```python
# Sem overhead de memória - computado na hora
df['age_squared'] = df.age ** 2
df['full_name'] = df.first_name + ' ' + df.last_name
df['is_adult'] = df.age >= 18
```

## Recursos

Esta skill inclui documentação de referência no diretório `references/`:

- `core_dataframes.md` - Criação de DataFrames, carregamento e estrutura básica
- `data_processing.md` - Filtragem, expressões, agregações e transformações
- `performance.md` - Estratégias de otimização e avaliação lazy
- `visualization.md` - Plotagem e visualizações interativas
- `machine_learning.md` - Pipelines de ML e integração de modelos
- `io_operations.md` - Formatos de arquivo e import/export de dados