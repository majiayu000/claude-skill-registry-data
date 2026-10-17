---
name: sweetviz
version: 1.0.0
description: Automated EDA comparison reports with target analysis, feature comparison,
  and HTML report generation for pandas DataFrames
author: workspace-hub
category: data-analysis
type: skill
capabilities:
- One-line automated EDA reports
- Target variable analysis
- Feature comparison between datasets
- Train vs test data comparison
- Intra-set comparisons (subpopulations)
- HTML report generation
- Correlation analysis
- Missing value visualization
- Distribution analysis
- Categorical and numerical analysis
tools:
- sweetviz
- pandas
- numpy
- matplotlib
tags:
- sweetviz
- eda
- data-analysis
- comparison
- target-analysis
- html-report
- feature-comparison
- visualization
- profiling
platforms:
- python
related_skills:
- ydata-profiling
- autoviz
- pandas-data-processing
- polars
- great-tables
requires: []
scripts_exempt: true
---

# Sweetviz

## When to Use This Skill

### USE Sweetviz when:

- **Dataset comparison** - Comparing train vs test, before vs after, or any two datasets
- **Target variable analysis** - Understanding how features relate to a target
- **Quick EDA reports** - Need comprehensive EDA in one line of code
- **Feature comparison** - Analyzing feature distributions across subsets
- **HTML reports** - Creating shareable, interactive analysis reports
- **Intra-set analysis** - Comparing subpopulations within a dataset
- **Data validation** - Checking for data drift between datasets
- **Feature selection** - Identifying important features for modeling
### DON'T USE Sweetviz when:

- **Very large datasets** - Over 1M rows (use sampling)
- **Streaming data** - Need real-time analysis
- **Deep statistical tests** - Need p-values and hypothesis testing
- **Custom visualizations** - Specific chart requirements
- **Interactive dashboards** - Use Streamlit or Dash instead
- **Text/NLP analysis** - Use dedicated NLP tools

## Prerequisites

```bash
# Basic installation
pip install sweetviz

# Using uv (recommended)
uv pip install sweetviz pandas numpy

# With Jupyter support
pip install sweetviz pandas numpy jupyter

# Verify installation
python -c "import sweetviz as sv; print(f'Sweetviz version: {sv.__version__}')"
```
### System Requirements

- Python 3.6 or higher
- pandas 0.25.3 or higher
- numpy
- matplotlib (for internal plotting)
- Modern web browser (for viewing HTML reports)

## Complete Examples

### Example 1: ML Dataset Profiling Pipeline

```python
#!/usr/bin/env python3
"""ml_profiling_pipeline.py - Complete ML dataset profiling with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import os

*See sub-skills for full details.*
### Example 2: Data Quality Assessment

```python
#!/usr/bin/env python3
"""data_quality_assessment.py - Data quality assessment with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

*See sub-skills for full details.*
### Example 3: Feature Selection Analysis

```python
#!/usr/bin/env python3
"""feature_selection_analysis.py - Feature analysis for ML with Sweetviz"""

import sweetviz as sv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os


*See sub-skills for full details.*

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic EDA report generation (analyze)
  - Target variable analysis
  - Dataset comparison (compare)
  - Intra-set comparison (compare_intra)
  - Feature configuration options
  - Pairwise analysis control
  - ML profiling pipeline example
  - Data quality assessment example
  - Feature selection analysis example
  - Streamlit integration
  - Data pipeline integration
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://github.com/fbdesignpro/sweetviz
- **PyPI**: https://pypi.org/project/sweetviz/
- **Medium Article**: https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34

---

**Generate powerful EDA comparison reports with Sweetviz - analyze, compare, and understand your data!**

## Sub-Skills

- [1. Basic EDA Report (Analyze)](1-basic-eda-report-analyze/SKILL.md)
- [2. Target Variable Analysis](2-target-variable-analysis/SKILL.md)
- [3. Dataset Comparison (Compare)](3-dataset-comparison-compare/SKILL.md)
- [4. Intra-set Comparison (Compare_Intra) (+1)](4-intra-set-comparison-compareintra/SKILL.md)
- [6. Pairwise Analysis Control](6-pairwise-analysis-control/SKILL.md)
- [Sweetviz with Streamlit (+1)](sweetviz-with-streamlit/SKILL.md)
- [Sweetviz in Data Pipeline](sweetviz-in-data-pipeline/SKILL.md)
- [1. Use Target Analysis for ML Projects (+4)](1-use-target-analysis-for-ml-projects/SKILL.md)
- [Common Issues](common-issues/SKILL.md)
