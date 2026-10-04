---
name: evo-cluster-naming
description: Assign human-readable, non-overlapping representative names to clusters using TF-IDF and centroid proximity.
---

# Cluster Naming

## Usage
```python
import sys; sys.path.insert(0, '/app/environment/skills/evo-cluster-naming/scripts')
from name_utils import name_all_levels
level_names = name_all_levels(label_matrix, texts, embeddings)
# returns dict: (level_idx, cluster_path_tuple) -> name string
```
