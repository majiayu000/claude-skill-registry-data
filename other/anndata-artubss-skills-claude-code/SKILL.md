---
name: anndata
description: Esta habilidade deve ser usada ao trabalhar com matrizes de dados anotados em Python, particularmente para análise de genômica de célula única, gerenciamento de medições experimentais com metadados ou manipulação de datasets biológicos em larga escala. Use quando as tarefas envolvam objetos AnnData, arquivos h5ad, dados de RNA-seq de célula única ou integração com ferramentas scanpy/scverse.
---

# AnnData

## Visão Geral

AnnData é um pacote Python para manipular matrizes de dados anotados, armazenando medições experimentais (X) junto com metadados de observações (obs), metadados de variáveis (var) e anotações multidimensionais (obsm, varm, obsp, varp, uns). Originalmente desenvolvido para genômica de célula única através do Scanpy, agora funciona como um framework de propósito geral para qualquer dado anotado que requeira armazenamento, manipulação e análise eficientes.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Criar, ler ou escrever objetos AnnData
- Trabalhar com h5ad, zarr ou outros formatos de dados genômicos
- Realizar análise de RNA-seq de célula única
- Gerenciar datasets grandes com matrizes esparsas ou modo backed
- Concatenar múltiplos datasets ou lotes experimentais
- Fazer subsetting, filtragem ou transformação de dados anotados
- Integrar com scanpy, scvi-tools ou outras ferramentas do ecossistema scverse

## Instalação

```bash
uv pip install anndata

# Com dependências opcionais
uv pip install anndata[dev,test,doc]
```

## Início Rápido

### Criando um objeto AnnData
```python
import anndata as ad
import numpy as np
import pandas as pd

# Criação mínima
X = np.random.rand(100, 2000)  # 100 células × 2000 genes
adata = ad.AnnData(X)

# Com metadados
obs = pd.DataFrame({
    'cell_type': ['T cell', 'B cell'] * 50,
    'sample': ['A', 'B'] * 50
}, index=[f'cell_{i}' for i in range(100)])

var = pd.DataFrame({
    'gene_name': [f'Gene_{i}' for i in range(2000)]
}, index=[f'ENSG{i:05d}' for i in range(2000)])

adata = ad.AnnData(X=X, obs=obs, var=var)
```

### Lendo dados
```python
# Ler arquivo h5ad
adata = ad.read_h5ad('data.h5ad')

# Ler com modo backed (para arquivos grandes)
adata = ad.read_h5ad('large_data.h5ad', backed='r')

# Ler outros formatos
adata = ad.read_csv('data.csv')
adata = ad.read_loom('data.loom')
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')
```

### Escrevendo dados
```python
# Escrever arquivo h5ad
adata.write_h5ad('output.h5ad')

# Escrever com compressão
adata.write_h5ad('output.h5ad', compression='gzip')

# Escrever outros formatos
adata.write_zarr('output.zarr')
adata.write_csvs('output_dir/')
```

### Operações básicas
```python
# Fazer subset por condições
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# Fazer subset por índices
subset = adata[0:50, 0:100]

# Adicionar metadados
adata.obs['quality_score'] = np.random.rand(adata.n_obs)
adata.var['highly_variable'] = np.random.rand(adata.n_vars) > 0.8

# Acessar dimensões
print(f"{adata.n_obs} observations × {adata.n_vars} variables")
```

## Capacidades Principais

### 1. Estrutura de Dados

Compreenda a estrutura do objeto AnnData incluindo X, obs, var, layers, obsm, varm, obsp, varp, uns e componentes raw.

**Veja**: `references/data_structure.md` para informações abrangentes sobre:
- Componentes principais (X, obs, var, layers, obsm, varm, obsp, varp, uns, raw)
- Criando objetos AnnData de várias fontes
- Acessando e manipulando componentes de dados
- Práticas eficientes em memória

### 2. Operações de Entrada/Saída

Leia e escreva dados em vários formatos com suporte para compressão, modo backed e armazenamento em nuvem.

**Veja**: `references/io_operations.md` para detalhes sobre:
- Formatos nativos (h5ad, zarr)
- Formatos alternativos (CSV, MTX, Loom, 10X, Excel)
- Modo backed para datasets grandes
- Acesso a dados remotos
- Conversão de formatos
- Otimização de desempenho

Comandos comuns:
```python
# Ler/escrever h5ad
adata = ad.read_h5ad('data.h5ad', backed='r')
adata.write_h5ad('output.h5ad', compression='gzip')

# Ler dados 10X
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# Ler formato MTX
adata = ad.read_mtx('matrix.mtx').T
```

### 3. Concatenação

Combine múltiplos objetos AnnData ao longo de observações ou variáveis com estratégias de junção flexíveis.

**Veja**: `references/concatenation.md` para cobertura abrangente de:
- Concatenação básica (axis=0 para observações, axis=1 para variáveis)
- Tipos de junção (inner, outer)
- Estratégias de merge (same, unique, first, only)
- Rastreamento de fontes de dados com labels
- Concatenação preguiçosa (AnnCollection)
- Concatenação em disco para datasets grandes

Comandos comuns:
```python
# Concatenar observações (combinar amostras)
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',
    label='batch',
    keys=['batch1', 'batch2', 'batch3']
)

# Concatenar variáveis (combinar modalidades)
adata = ad.concat([adata_rna, adata_protein], axis=1)

# Concatenação preguiçosa
from anndata.experimental import AnnCollection
collection = AnnCollection(
    ['data1.h5ad', 'data2.h5ad'],
    join_obs='outer',
    label='dataset'
)
```

### 4. Manipulação de Dados

Transforme, faça subset, filtre e reorganize dados eficientemente.

**Veja**: `references/manipulation.md` para orientação detalhada sobre:
- Subsetting (por índices, nomes, máscaras booleanas, condições de metadados)
- Transposição
- Cópia (cópias completas vs visões)
- Renomeação (observações, variáveis, categorias)
- Conversões de tipo (strings para categóricos, esparso/denso)
- Adição/remoção de componentes de dados
- Reordenação
- Filtragem de controle de qualidade

Comandos comuns:
```python
# Fazer subset por metadados
filtered = adata[adata.obs['quality_score'] > 0.8]
hv_genes = adata[:, adata.var['highly_variable']]

# Transpor
adata_T = adata.T

# Copiar vs visão
view = adata[0:100, :]  # Visão (referência leve)
copy = adata[0:100, :].copy()  # Cópia independente

# Converter strings para categóricos
adata.strings_to_categoricals()
```

### 5. Melhores Práticas

Siga padrões recomendados para eficiência de memória, desempenho e reprodutibilidade.

**Veja**: `references/best_practices.md` para diretrizes sobre:
- Gerenciamento de memória (matrizes esparsas, categóricos, modo backed)
- Visões vs cópias
- Otimização de armazenamento de dados
- Otimização de desempenho
- Trabalhando com dados raw
- Gerenciamento de metadados
- Reprodutibilidade
- Tratamento de erros
- Integração com outras ferramentas
- Armadilhas comuns e soluções

Recomendações principais:
```python
# Use matrizes esparsas para dados esparsos
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)

# Converter strings para categóricos
adata.strings_to_categoricals()

# Use modo backed para arquivos grandes
adata = ad.read_h5ad('large.h5ad', backed='r')

# Armazene raw antes de filtrar
adata.raw = adata.copy()
adata = adata[:, adata.var['highly_variable']]
```

## Integração com o Ecossistema Scverse

AnnData funciona como a estrutura de dados fundacional para o ecossistema scverse:

### Scanpy (Análise de célula única)
```python
import scanpy as sc

# Pré-processamento
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Redução de dimensionalidade
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Visualização
sc.pl.umap(adata, color=['cell_type', 'leiden'])
```

### Muon (Dados multimodais)
```python
import muon as mu

# Combinar dados de RNA e proteína
mdata = mu.MuData({'rna': adata_rna, 'protein': adata_protein})
```

### Integração com PyTorch
```python
from anndata.experimental import AnnLoader

# Criar DataLoader para aprendizado profundo
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

for batch in dataloader:
    X = batch.X
    # Treinar modelo
```

## Fluxos de Trabalho Comuns

### Análise de RNA-seq de célula única
```python
import anndata as ad
import scanpy as sc

# 1. Carregar dados
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. Controle de qualidade
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[adata.obs['n_genes'] > 200]
adata = adata[adata.obs['n_counts'] < 50000]

# 3. Armazenar raw
adata.raw = adata.copy()

# 4. Normalizar e filtrar
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']]

# 5. Salvar dados processados
adata.write_h5ad('processed.h5ad')
```

### Integração de lotes
```python
# Carregar múltiplos lotes
adata1 = ad.read_h5ad('batch1.h5ad')
adata2 = ad.read_h5ad('batch2.h5ad')
adata3 = ad.read_h5ad('batch3.h5ad')

# Concatenar com rótulos de lote
adata = ad.concat(
    [adata1, adata2, adata3],
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='inner'
)

# Aplicar correção de lote
import scanpy as sc
sc.pp.combat(adata, key='batch')

# Continuar análise
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### Trabalhando com datasets grandes
```python
# Abrir em modo backed
adata = ad.read_h5ad('100GB_dataset.h5ad', backed='r')

# Filtrar baseado em metadados (sem carregamento de dados)
high_quality = adata[adata.obs['quality_score'] > 0.8]

# Carregar subset filtrado
adata_subset = high_quality.to_memory()

# Processar subset
process(adata_subset)

# Ou processar em chunks
chunk_size = 1000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    process(chunk)
```

## Solução de Problemas

### Erros de falta de memória
Use modo backed ou converta para matrizes esparsas:
```python
# Modo backed
adata = ad.read_h5ad('file.h5ad', backed='r')

# Matrizes esparsas
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
```

### Leitura lenta de arquivos
Use compressão e formatos apropriados:
```python
# Otimizar para armazenamento
adata.strings_to_categoricals()
adata.write_h5ad('file.h5ad', compression='gzip')

# Use Zarr para armazenamento em nuvem
adata.write_zarr('file.zarr', chunks=(1000, 1000))
```

### Problemas de alinhamento de índices
Sempre alinhe dados externos no índice:
```python
# Errado
adata.obs['new_col'] = external_data['values']

# Correto
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

## Recursos Adicionais

- **Documentação oficial**: https://anndata.readthedocs.io/
- **Tutoriais Scanpy**: https://scanpy.readthedocs.io/
- **Ecossistema Scverse**: https://scverse.org/
- **Repositório GitHub**: https://github.com/scverse/anndata