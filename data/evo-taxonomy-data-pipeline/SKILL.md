---
name: evo-taxonomy-data-pipeline
description: Load, normalize, and output e-commerce category taxonomy data using Pandas 2.2.0-safe patterns.
---

# Taxonomy Data Pipeline

Loads Amazon/Facebook/Google CSVs, normalizes category_path text, splits hierarchical levels, writes outputs.

## Usage
```python
import sys; sys.path.insert(0, '/app/environment/skills/evo-taxonomy-data-pipeline/scripts')
from utils import load_source_csvs, normalize_category_paths, split_hierarchy_columns, write_unified_outputs

df = load_source_csvs('/root/data/amazon_product_categories.csv','/root/data/fb_product_categories.csv','/root/data/google_shopping_product_categories.csv')
df = normalize_category_paths(df)
df = split_hierarchy_columns(df)
write_unified_outputs(df, '/root/output/unified_taxonomy_full.csv', '/root/output/unified_taxonomy_hierarchy.csv')
```
