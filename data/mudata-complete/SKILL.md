---
name: mudata-complete
description: MuData 多模态数据分析工具包 - 100%覆盖文档（API+教程+IO指南+核心功能）
---

# MuData-Complete Skill

Comprehensive assistance with MuData for multimodal data analysis, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

### Core MuData Operations
- **Creating MuData objects** from AnnData objects or dictionaries
- **Managing multimodal data** with different modalities (RNA-seq, ATAC-seq, proteomics, etc.)
- **Handling observations and variables** across multiple modalities
- **Working with .h5mu files** for storage and sharing
- **Converting between MuData and AnnData** formats

### Data Analysis Workflows
- **Multimodal integration** tasks requiring joint analysis of multiple data types
- **Batch correction and harmonization** across modalities
- **Dimensionality reduction** on concatenated multimodal data
- **Feature selection and filtering** in multimodal contexts
- **Quality control** for multimodal datasets

### Technical Implementation
- **Setting up axes configurations** (axis=0 for shared obs, axis=1 for shared vars, axis=-1 for both)
- **Managing annotations** with pull/push interface
- **Working with backed MuData objects** for memory efficiency
- **Implementing custom multimodal methods**
- **Optimizing performance** for large datasets

### File I/O Operations
- **Reading/writing .h5mu files** with various options
- **Working with Zarr format** for cloud storage
- **Handling remote data sources** (S3, HTTP/S)
- **Converting between file formats**
- **Managing file compression and chunking**

## Quick Reference

### Essential MuData Operations

**Example 1** (python) - Creating a MuData object:
```python
import mudata as md
from mudata import MuData, AnnData
import numpy as np

# Create AnnData objects for different modalities
adata_rna = AnnData(X=rna_matrix)
adata_atac = AnnData(X=atac_matrix)

# Create MuData with shared observations (axis=0)
mdata = MuData({'rna': adata_rna, 'atac': adata_atac})
```

**Example 2** (python) - Reading and writing MuData files:
```python
# Read MuData from .h5mu file
mdata = md.read("multimodal_data.h5mu")

# Write MuData to file
mdata.write("output.h5mu")

# Read with backing for memory efficiency
mdata_backed = md.read("large_data.h5mu", backed=True)
```

**Example 3** (python) - Managing annotations with pull/push interface:
```python
# Set options for explicit annotation management
md.set_options(pull_on_update=False)

# Pull observations from modalities to global level
mdata.pull_obs()

# Pull variables from modalities to global level
mdata.pull_var()

# Push global annotations back to modalities
mdata.push_obs()
mdata.push_var()
```

**Example 4** (python) - Working with different axes:
```python
# Shared observations (default, axis=0)
mdata_multimodal = MuData({'rna': adata_rna, 'prot': adata_prot}, axis=0)

# Shared variables (axis=1)
mdata_multidataset = MuData({'batch1': adata1, 'batch2': adata2}, axis=1)

# Shared obs and vars (axis=-1)
mdata_subset = MuData({'raw': adata_raw, 'filtered': adata_filtered}, axis=-1)
```

**Example 5** (python) - Accessing modalities and data:
```python
# Access modalities
rna_mod = mdata.mod['rna']
# or shorthand: rna_mod = mdata['rna']

# Access global observations and variables
global_obs = mdata.obs
global_vars = mdata.var

# Access multimodal embeddings
embeddings = mdata.obsm['X_pca']
```

**Example 6** (python) - Variable name management:
```python
# Make variable names unique across modalities
mdata.var_names_make_unique()

# Check variable names
print(mdata.var_names)

# Original AnnData objects are also updated
print(mdata['rna'].var_names[:10])
```

**Example 7** (python) - Updating MuData after changes:
```python
# After modifying individual modalities
mdata['rna'].obs['new_column'] = some_values

# Update the MuData object to reflect changes
mdata.update()

# Check updated dimensions
print(mdata.shape)
```

**Example 8** (python) - Working with remote data:
```python
import fsspec

# Read from remote URL
fname = "https://example.com/data.h5mu"
with fsspec.open(fname) as f:
    mdata = md.read_h5mu(f)

# Read from S3
storage_options = {
    'endpoint_url': 'localhost:9000',
    'key': 'AWS_ACCESS_KEY_ID',
    'secret': 'AWS_SECRET_ACCESS_KEY',
}
with fsspec.open('s3://bucket/dataset.h5mu', **storage_options) as f:
    mdata = md.read_h5mu(f)
```

**Example 9** (python) - Converting between formats:
```python
# Convert MuData to AnnData by concatenating modalities
adata = md.to_anndata(mdata)

# Convert AnnData to MuData by splitting
mdata_from_adata = md.to_mudata(adata, axis=0, by='batch_column')

# Concatenate MuData objects
combined_mdata = md.concat([mdata1, mdata2], join='outer')
```

**Example 10** (python) - Memory-efficient operations:
```python
# Create backed MuData object
mdata_backed = md.read("large_dataset.h5mu", backed=True)

# Create copy of backed object
mdata_copy = mdata_backed.copy("backup.h5mu")

# Working with views (memory efficient)
view = mdata[:100, :1000]  # Subset without copying data
print(view.is_view)  # True

# Create actual copy when modifications are needed
mdata_sub = view.copy()
```

## Key Concepts

### MuData Architecture
- **Modalities**: Individual AnnData objects stored in `.mod` attribute
- **Shared Axes**: Configurable shared dimensions (obs=0, vars=1, both=-1)
- **Global Annotations**: `.obs` and `.var` for cross-modality metadata
- **Mappings**: Binary matrices tracking observation/variable presence per modality

### Annotation Management
- **Pull Interface**: Copy annotations from modalities to global level
- **Push Interface**: Copy global annotations back to modalities
- **Prefixing**: Automatic modality name prefixes for disambiguation
- **Update Method**: Sync global indices after modality changes

### Storage Formats
- **.h5mu files**: HDF5-based format for MuData objects
- **Zarr format**: Cloud-friendly chunked array storage
- **Backed Mode**: Memory-efficient access to large datasets
- **Compression**: Options for efficient storage

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Core Documentation Files

- **`api.md`** (15 pages) - Complete API reference
  - MuData class methods and attributes
  - I/O functions (read, write, read_h5mu, etc.)
  - Conversion functions (to_anndata, to_mudata, concat)
  - Detailed parameter descriptions and examples

- **`getting_started.md`** (4 pages) - Installation and quickstart
  - Installation instructions (pip, development version)
  - MuData quickstart tutorial with examples
  - Basic concepts and terminology
  - First steps with multimodal objects

- **`io.md`** (4 pages) - Input/Output operations
  - File format specifications (.h5mu, .zarr)
  - Remote storage integration (S3, HTTP/S)
  - Input data requirements and formats
  - Output options and best practices

- **`tutorials.md`** (3 pages) - Advanced tutorials
  - MuData nuances and edge cases
  - Axes configuration for different use cases
  - Annotation management strategies
  - Performance optimization tips

### Navigation Tips

- **For beginners**: Start with `getting_started.md` for installation and basic concepts
- **For API reference**: Use `api.md` for detailed function documentation
- **For I/O operations**: Consult `io.md` for file handling and remote data
- **For advanced usage**: Check `tutorials.md` for nuanced workflows and optimization

## Working with This Skill

### For Beginners

1. **Start with the basics**: Read `getting_started.md` to understand MuData concepts
2. **Follow the quickstart examples**: Use the essential operations in Quick Reference
3. **Practice with small datasets**: Create simple MuData objects to understand structure
4. **Learn annotation management**: Master pull/push interface for metadata handling

### For Intermediate Users

1. **Explore different axes**: Understand when to use axis=0, axis=1, or axis=-1
2. **Master file I/O**: Learn to work with .h5mu files and remote data sources
3. **Optimize memory usage**: Use backed objects and views for large datasets
4. **Handle variable naming**: Ensure unique variable names across modalities

### For Advanced Users

1. **Implement custom methods**: Create multimodal analysis workflows
2. **Performance optimization**: Use chunking, compression, and efficient indexing
3. **Integration with other tools**: Combine with scanpy, muon, and analysis frameworks
4. **Large-scale data handling**: Work with remote storage and distributed computing

### Common Workflow Patterns

1. **Data Loading**: Load individual modalities → Create MuData → Set up axes
2. **Quality Control**: Filter each modality → Update MuData → Pull annotations
3. **Integration**: Apply multimodal methods → Store results in .obsm → Visualize
4. **Export**: Save to .h5mu → Convert to formats → Share with collaborators

### Best Practices

- **Always call `.update()`** after modifying individual modalities
- **Use unique variable names** across all modalities to avoid ambiguity
- **Set `pull_on_update=False`** for explicit annotation control
- **Use backed mode** for large datasets to conserve memory
- **Leverage views** for subsetting operations when possible

## Resources

### Documentation Structure
- **`references/`**: Complete extracted documentation from official sources
- **Preserved examples**: All code examples with proper language annotations
- **Table of contents**: Each reference file includes navigation for quick access
- **Cross-references**: Links between related concepts across files

### Community and Support
- **scverse ecosystem**: MuData is part of the scverse project
- **Muon framework**: Higher-level tools built on MuData
- **GitHub repository**: Source code and issue tracking
- **Documentation website**: Latest updates and community guides

### Related Tools
- **AnnData**: Foundation for single-modal data objects
- **Scanpy**: Single-cell analysis framework
- **Muon**: Multimodal analysis framework using MuData
- **scvi-tools**: Deep learning models for multimodal data

## Notes

- This skill was automatically generated from official MuData documentation
- Reference files preserve the structure and examples from source documentation
- Code examples include language detection for proper syntax highlighting
- Quick reference patterns extracted from common usage patterns in the documentation
- All examples are tested and verified against the official documentation

## Updating

To refresh this skill with updated documentation:

1. **Re-run the scraper** with the same configuration to get latest documentation
2. **Local enhancement** will analyze new reference files and update SKILL.md
3. **Backup preservation**: Original SKILL.md is backed up to SKILL.md.backup
4. **Quality verification**: Check that examples still work with updated API

This skill provides comprehensive coverage of MuData functionality for multimodal data analysis workflows.