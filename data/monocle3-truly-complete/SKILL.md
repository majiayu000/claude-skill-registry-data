---
name: monocle3-truly-complete
description: Monocle3 单细胞轨迹分析工具包 - 100%覆盖文档（18个文件：完整教程+API+轨迹推断）
---

# Monocle3-Truly-Complete Skill

Comprehensive assistance with Monocle 3 for single-cell trajectory analysis, including co-embedding, projection, and advanced visualization techniques.

## When to Use This Skill

This skill should be triggered when:

### Data Analysis & Processing
- **Loading and preprocessing single-cell data** - Working with CellDataSet objects, UMI filtering, size factor estimation
- **Co-embedding multiple datasets** - Combining reference and query datasets for comparative analysis
- **Projecting query data onto reference** - Using transform models to map new data into existing reference space
- **Cell type label transfer** - Transferring annotations from reference to query cells using nearest neighbor indexing

### Installation & Setup
- **Installing Monocle 3** - Setting up R environment, Bioconductor dependencies, GitHub installation
- **Troubleshooting installation issues** - Resolving gdal, Xcode, gfortran, or reticulate errors
- **Testing installation** - Verifying that Monocle 3 is properly installed and functional

### Visualization & Analysis
- **Creating trajectory plots** - Generating 2D/3D UMAP visualizations with cell type annotations
- **Comparing datasets** - Visualizing combined reference and query datasets
- **Interactive plotting** - Working with plotly for 3D trajectory visualizations

## Quick Reference

### Essential Code Examples

**Example 1: Basic Installation**
```r
# Install Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install(version = "3.21")

# Install Monocle 3
devtools::install_github('cole-trapnell-lab/monocle3')
```

**Example 2: Loading Reference and Query Datasets**
```r
library(monocle3)
library(Matrix)

# Load reference dataset
cds_ref <- new_cell_data_set(matrix_ref,
                             cell_metadata = cell_ann_ref,
                             gene_metadata = gene_ann_ref)

# Load query dataset
cds_qry <- new_cell_data_set(matrix_qry,
                             cell_metadata = cell_ann_qry,
                             gene_metadata = gene_ann_qry)
```

**Example 3: Gene Filtering and UMI Cutoffs**
```r
# Find shared genes
genes_shared <- intersect(row.names(cds_ref), row.names(cds_qry))

# Keep only shared genes
cds_ref <- cds_ref[genes_shared,]
cds_qry <- cds_qry[genes_shared,]

# Apply UMI cutoffs (example: 1000)
cds_ref <- cds_ref[, colData(cds_ref)[['Total_mRNAs']] >= 1000]
cds_qry <- cds_qry[, colData(cds_qry)[['n.umi']] >= 1000]
```

**Example 4: Processing Reference Dataset**
```r
# Estimate size factors
cds_ref <- estimate_size_factors(cds_ref)
cds_qry <- estimate_size_factors(cds_qry)

# Process reference with PCA and UMAP
cds_ref <- preprocess_cds(cds_ref, num_dim=100)
cds_ref <- reduce_dimension(cds_ref, build_nn_index=TRUE)

# Save transform models for projection
save_transform_models(cds_ref, 'cds_ref_test_models')
```

**Example 5: Project Query Data into Reference Space**
```r
# Load reference transform models
cds_qry <- load_transform_models(cds_qry, 'cds_ref_test_models')

# Apply transformations to query data
cds_qry <- preprocess_transform(cds_qry)
cds_qry <- reduce_dimension_transform(cds_qry)
```

**Example 6: Cell Type Label Transfer**
```r
# Transfer cell type labels from reference to query
cds_qry <- transfer_cell_labels(cds_qry,
                                reduction_method='UMAP',
                                ref_coldata=colData(cds_ref),
                                ref_column_name='Main_cell_type',
                                query_column_name='cell_type_xfr',
                                transform_models_dir='cds_ref_test_models')

# Fix any missing labels
cds_qry <- fix_missing_cell_labels(cds_qry,
                                   reduction_method='UMAP',
                                   from_column_name='cell_type_xfr',
                                   to_column_name='cell_type_fix')
```

**Example 7: Combining and Visualizing Datasets**
```r
# Label datasets for visualization
colData(cds_ref)[['data_set']] <- 'reference'
colData(cds_qry)[['data_set']] <- 'query'

# Combine datasets
cds_combined <- combine_cds(list(cds_ref, cds_qry),
                            keep_all_genes=TRUE,
                            cell_names_unique=TRUE,
                            keep_reduced_dims=TRUE)

# Plot combined data
plot_cells(cds_combined, color_cells_by='data_set')
```

**Example 8: Basic Visualization**
```r
# Plot individual datasets
plot_cells(cds_ref)
plot_cells(cds_qry)

# Color by specific metadata
plot_cells(cds_combined, color_cells_by='Main_cell_type')
```

## Key Concepts

### Core Monocle 3 Objects
- **CellDataSet (cds)** - Primary data structure containing expression matrix, cell metadata, and gene metadata
- **Transform Models** - Saved PCA/UMAP transformations from reference data for projecting query data
- **Nearest Neighbor Index** - Spatial index used for efficient cell type label transfer

### Analysis Workflow
1. **Data Loading** - Import expression matrices and metadata
2. **Preprocessing** - Filter genes, apply UMI cutoffs, estimate size factors
3. **Reference Processing** - Create PCA/UMAP embeddings with nearest neighbor indexing
4. **Projection** - Transform query data into reference space using saved models
5. **Label Transfer** - Transfer annotations from reference to query cells
6. **Visualization** - Plot trajectories and compare datasets

### Key Parameters
- **build_nn_index=TRUE** - Required for cell type label transfer
- **num_dim** - Number of PCA dimensions (typically 50-100)
- **reduction_method** - 'UMAP' or 'PCA' for visualization and label transfer

## Reference Files

This skill includes comprehensive documentation in `references/`:

### getting_started.md
- **17 pages** of detailed installation and projection workflows
- **Installation Guide** - Complete setup with troubleshooting for gdal, Xcode, gfortran errors
- **Projection Tutorial** - Step-by-step co-embedding and label transfer workflow
- **Code Examples** - 26 practical examples covering data loading, processing, and visualization

### visualization.md
- **Interactive 3D plotting** with plotly integration
- **Advanced trajectory visualizations** showing cell partitions
- **Web-based exploration tools** for large datasets

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. **Start with installation** - Follow the getting_started.md installation guide carefully
2. **Use the projection workflow** - The co-embedding tutorial provides a complete end-to-end example
3. **Master the basics first** - Focus on data loading, gene filtering, and basic visualization before attempting advanced projection

### For Intermediate Users
1. **Customize projection parameters** - Adjust num_dim, UMI cutoffs, and visualization options
2. **Batch process multiple datasets** - Use the transform model system for efficient analysis of many query datasets
3. **Troubleshoot common issues** - Reference the installation troubleshooting section for gdal, Xcode, and gfortran problems

### For Advanced Users
1. **Optimize performance** - Use BPCells for large datasets and tune nearest neighbor indexing
2. **Custom visualization** - Extend plotly visualizations for interactive exploration
3. **Pipeline integration** - Incorporate Monocle 3 into larger single-cell analysis workflows

### Navigation Tips
- **Search by function name** - Quick reference includes the most commonly used functions
- **Check examples first** - Each concept has multiple code examples with different approaches
- **Reference the original URLs** - Documentation includes links to official Monocle 3 documentation

## Resources

### references/
Organized documentation extracted from official sources:
- **Step-by-step tutorials** with complete code workflows
- **Installation troubleshooting** with specific error solutions
- **Multiple code examples** showing different approaches to the same task
- **Links to original documentation** for further reading

### scripts/
Add helper scripts for common automation tasks such as:
- **Batch projection** of multiple query datasets
- **Automated installation** scripts
- **Custom visualization** functions

### assets/
Add templates and examples such as:
- **Example metadata files** showing proper formatting
- **Configuration templates** for common analysis scenarios
- **Boilerplate code** for starting new projects

## Notes

- This skill covers **Monocle 3 version 1.4.25+** with Bioconductor 3.21 and R 4.4.1+
- **Projection workflow** is the key feature - enabling comparison of large datasets without memory issues
- **Transform models** can be reused across multiple query datasets for consistent analysis
- Code examples include **both simple and advanced approaches** for flexibility

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from the official Monocle 3 documentation
