---
name: scanpy
description: "Análise de RNA-seq de célula única. Carregue dados .h5ad/10X, QC, normalização, PCA/UMAP/t-SNE, clustering Leiden, genes marcadores, anotação de tipo celular, trajetória, para análise de scRNA-seq."
---

# Scanpy: Análise de Célula Única

## Visão Geral

Scanpy é um toolkit Python escalável para analisar dados de RNA-seq de célula única, construído sobre AnnData. Aplique essa habilidade para fluxos de trabalho completos de célula única, incluindo controle de qualidade, normalização, redução de dimensionalidade, clustering, identificação de genes marcadores, visualização e análise de trajetória.

## Quando Usar Essa Habilidade

Essa habilidade deve ser usada quando:
- Analisar dados de RNA-seq de célula única (.h5ad, 10X, formatos CSV)
- Executar controle de qualidade em conjuntos de dados de scRNA-seq
- Criar visualizações UMAP, t-SNE ou PCA
- Identificar clusters celulares e encontrar genes marcadores
- Anotar tipos celulares com base na expressão gênica
- Conduzir inferência de trajetória ou análise de pseudotempo
- Gerar gráficos de célula única com qualidade de publicação

## Início Rápido

### Importação Básica e Configuração

```python
import scanpy as sc
import pandas as pd
import numpy as np

# Configure settings
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=80, facecolor='white')
sc.settings.figdir = './figures/'
```

### Carregando Dados

```python
# From 10X Genomics
adata = sc.read_10x_mtx('path/to/data/')
adata = sc.read_10x_h5('path/to/data.h5')

# From h5ad (AnnData format)
adata = sc.read_h5ad('path/to/data.h5ad')

# From CSV
adata = sc.read_csv('path/to/data.csv')
```

### Compreendendo a Estrutura AnnData

O objeto AnnData é a estrutura de dados central no scanpy:

```python
adata.X          # Expression matrix (cells × genes)
adata.obs        # Cell metadata (DataFrame)
adata.var        # Gene metadata (DataFrame)
adata.uns        # Unstructured annotations (dict)
adata.obsm       # Multi-dimensional cell data (PCA, UMAP)
adata.raw        # Raw data backup

# Access cell and gene names
adata.obs_names  # Cell barcodes
adata.var_names  # Gene names
```

## Fluxo de Trabalho de Análise Padrão

### 1. Controle de Qualidade

Identifique e filtre células e genes de baixa qualidade:

```python
# Identify mitochondrial genes
adata.var['mt'] = adata.var_names.str.startswith('MT-')

# Calculate QC metrics
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)

# Visualize QC metrics
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
             jitter=0.4, multi_panel=True)

# Filter cells and genes
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.pct_counts_mt < 5, :]  # Remove high MT% cells
```

**Use o script de QC para análise automatizada:**
```bash
python scripts/qc_analysis.py input_file.h5ad --output filtered.h5ad
```

### 2. Normalização e Pré-processamento

```python
# Normalize to 10,000 counts per cell
sc.pp.normalize_total(adata, target_sum=1e4)

# Log-transform
sc.pp.log1p(adata)

# Save raw counts for later
adata.raw = adata

# Identify highly variable genes
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pl.highly_variable_genes(adata)

# Subset to highly variable genes
adata = adata[:, adata.var.highly_variable]

# Regress out unwanted variation
sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])

# Scale data
sc.pp.scale(adata, max_value=10)
```

### 3. Redução de Dimensionalidade

```python
# PCA
sc.tl.pca(adata, svd_solver='arpack')
sc.pl.pca_variance_ratio(adata, log=True)  # Check elbow plot

# Compute neighborhood graph
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)

# UMAP for visualization
sc.tl.umap(adata)
sc.pl.umap(adata, color='leiden')

# Alternative: t-SNE
sc.tl.tsne(adata)
```

### 4. Clustering

```python
# Leiden clustering (recommended)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color='leiden', legend_loc='on data')

# Try multiple resolutions to find optimal granularity
for res in [0.3, 0.5, 0.8, 1.0]:
    sc.tl.leiden(adata, resolution=res, key_added=f'leiden_{res}')
```

### 5. Identificação de Genes Marcadores

```python
# Find marker genes for each cluster
sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')

# Visualize results
sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
sc.pl.rank_genes_groups_heatmap(adata, n_genes=10)
sc.pl.rank_genes_groups_dotplot(adata, n_genes=5)

# Get results as DataFrame
markers = sc.get.rank_genes_groups_df(adata, group='0')
```

### 6. Anotação de Tipo Celular

```python
# Define marker genes for known cell types
marker_genes = ['CD3D', 'CD14', 'MS4A1', 'NKG7', 'FCGR3A']

# Visualize markers
sc.pl.umap(adata, color=marker_genes, use_raw=True)
sc.pl.dotplot(adata, var_names=marker_genes, groupby='leiden')

# Manual annotation
cluster_to_celltype = {
    '0': 'CD4 T cells',
    '1': 'CD14+ Monocytes',
    '2': 'B cells',
    '3': 'CD8 T cells',
}
adata.obs['cell_type'] = adata.obs['leiden'].map(cluster_to_celltype)

# Visualize annotated types
sc.pl.umap(adata, color='cell_type', legend_loc='on data')
```

### 7. Salvar Resultados

```python
# Save processed data
adata.write('results/processed_data.h5ad')

# Export metadata
adata.obs.to_csv('results/cell_metadata.csv')
adata.var.to_csv('results/gene_metadata.csv')
```

## Tarefas Comuns

### Criando Gráficos com Qualidade de Publicação

```python
# Set high-quality defaults
sc.settings.set_figure_params(dpi=300, frameon=False, figsize=(5, 5))
sc.settings.file_format_figs = 'pdf'

# UMAP with custom styling
sc.pl.umap(adata, color='cell_type',
           palette='Set2',
           legend_loc='on data',
           legend_fontsize=12,
           legend_fontoutline=2,
           frameon=False,
           save='_publication.pdf')

# Heatmap of marker genes
sc.pl.heatmap(adata, var_names=genes, groupby='cell_type',
              swap_axes=True, show_gene_labels=True,
              save='_markers.pdf')

# Dot plot
sc.pl.dotplot(adata, var_names=genes, groupby='cell_type',
              save='_dotplot.pdf')
```

Consulte `references/plotting_guide.md` para exemplos de visualização abrangentes.

### Inferência de Trajetória

```python
# PAGA (Partition-based graph abstraction)
sc.tl.paga(adata, groups='leiden')
sc.pl.paga(adata, color='leiden')

# Diffusion pseudotime
adata.uns['iroot'] = np.flatnonzero(adata.obs['leiden'] == '0')[0]
sc.tl.dpt(adata)
sc.pl.umap(adata, color='dpt_pseudotime')
```

### Expressão Diferencial Entre Condições

```python
# Compare treated vs control within cell types
adata_subset = adata[adata.obs['cell_type'] == 'T cells']
sc.tl.rank_genes_groups(adata_subset, groupby='condition',
                         groups=['treated'], reference='control')
sc.pl.rank_genes_groups(adata_subset, groups=['treated'])
```

### Pontuação de Gene Set

```python
# Score cells for gene set expression
gene_set = ['CD3D', 'CD3E', 'CD3G']
sc.tl.score_genes(adata, gene_set, score_name='T_cell_score')
sc.pl.umap(adata, color='T_cell_score')
```

### Correção de Batch

```python
# ComBat batch correction
sc.pp.combat(adata, key='batch')

# Alternative: use Harmony or scVI (separate packages)
```

## Parâmetros-Chave para Ajustar

### Controle de Qualidade
- `min_genes`: Mínimo de genes por célula (tipicamente 200-500)
- `min_cells`: Mínimo de células por gene (tipicamente 3-10)
- `pct_counts_mt`: Limite mitocondrial (tipicamente 5-20%)

### Normalização
- `target_sum`: Contagem alvo por célula (padrão 1e4)

### Seleção de Features
- `n_top_genes`: Número de HVGs (tipicamente 2000-3000)
- `min_mean`, `max_mean`, `min_disp`: Parâmetros de seleção de HVG

### Redução de Dimensionalidade
- `n_pcs`: Número de componentes principais (verifique o gráfico de razão de variância)
- `n_neighbors`: Número de vizinhos (tipicamente 10-30)

### Clustering
- `resolution`: Granularidade de clustering (0,4-1,2, maior = mais clusters)

## Armadilhas Comuns e Melhores Práticas

1. **Sempre salve contagens bruras**: `adata.raw = adata` antes de filtrar genes
2. **Verifique gráficos de QC cuidadosamente**: Ajuste os limites com base na qualidade do conjunto de dados
3. **Use Leiden em vez de Louvain**: Mais eficiente e melhores resultados
4. **Tente várias resoluções de clustering**: Encontre a granularidade ideal
5. **Valide anotações de tipo celular**: Use múltiplos genes marcadores
6. **Use `use_raw=True` para gráficos de expressão gênica**: Mostra contagens originais
7. **Verifique a razão de variância PCA**: Determine o número ideal de PCs
8. **Salve resultados intermediários**: Fluxos de trabalho longos podem falhar no meio do caminho

## Recursos Inclusos

### scripts/qc_analysis.py
Script de controle de qualidade automatizado que calcula métricas, gera gráficos e filtra dados:

```bash
python scripts/qc_analysis.py input.h5ad --output filtered.h5ad \
    --mt-threshold 5 --min-genes 200 --min-cells 3
```

### references/standard_workflow.md
Fluxo de trabalho passo a passo completo com explicações detalhadas e exemplos de código para:
- Carregamento e configuração de dados
- Controle de qualidade com visualização
- Normalização e scaling
- Seleção de features
- Redução de dimensionalidade (PCA, UMAP, t-SNE)
- Clustering (Leiden, Louvain)
- Identificação de genes marcadores
- Anotação de tipo celular
- Inferência de trajetória
- Expressão diferencial

Leia essa referência ao executar uma análise completa do zero.

### references/api_reference.md
Guia de referência rápida para funções do scanpy organizadas por módulo:
- Leitura/escrita de dados (`sc.read_*`, `adata.write_*`)
- Pré-processamento (`sc.pp.*`)
- Ferramentas (`sc.tl.*`)
- Plotagem (`sc.pl.*`)
- Estrutura e manipulação de AnnData
- Configurações e utilitários

Use isso para consulta rápida de assinaturas de função e parâmetros comuns.

### references/plotting_guide.md
Guia de visualização abrangente incluindo:
- Gráficos de controle de qualidade
- Visualizações de redução de dimensionalidade
- Visualizações de clustering
- Gráficos de genes marcadores (heatmaps, dot plots, violin plots)
- Gráficos de trajetória e pseudotempo
- Personalização com qualidade de publicação
- Figuras multi-painel
- Paletas de cores e estilo

Consulte isso ao criar figuras prontas para publicação.

### assets/analysis_template.py
Template de análise completa fornecendo um fluxo de trabalho completo desde o carregamento de dados até a anotação de tipo celular. Copie e customize esse template para novas análises:

```bash
cp assets/analysis_template.py my_analysis.py
# Edit parameters and run
python my_analysis.py
```

O template inclui todas as etapas padrão com parâmetros configuráveis e comentários úteis.

## Recursos Adicionais

- **Documentação oficial do scanpy**: https://scanpy.readthedocs.io/
- **Tutoriais do scanpy**: https://scanpy-tutorials.readthedocs.io/
- **Ecossistema scverse**: https://scverse.org/ (ferramentas relacionadas: squidpy, scvi-tools, cellrank)
- **Melhores práticas**: Luecken & Theis (2019) "Current best practices in single-cell RNA-seq"

## Dicas para Análise Eficaz

1. **Comece com o template**: Use `assets/analysis_template.py` como ponto de partida
2. **Rode o script de QC primeiro**: Use `scripts/qc_analysis.py` para filtragem inicial
3. **Consulte referências conforme necessário**: Carregue referências de fluxo de trabalho e API no contexto
4. **Itere no clustering**: Tente múltiplas resoluções e métodos de visualização
5. **Valide biologicamente**: Verifique se genes marcadores correspondem aos tipos celulares esperados
6. **Documente parâmetros**: Registre limites de QC e configurações de análise
7. **Salve pontos de controle**: Escreva resultados intermediários em etapas-chave