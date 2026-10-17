---
name: autoviz
version: 1.0.0
description: Automatic exploratory data analysis and visualization with a single line
  of code - generates comprehensive charts, detects patterns, and exports to HTML/notebooks
type: reference
author: workspace-hub
category: data-analysis
capabilities:
- One-line automatic EDA
- Feature distribution analysis
- Correlation detection and visualization
- Outlier identification and highlighting
- Automated chart type selection
- Export to HTML and Jupyter notebooks
- Support for large datasets with sampling
- Categorical and numerical feature analysis
tools:
- autoviz
- pandas
- matplotlib
- seaborn
- plotly
tags:
- autoviz
- eda
- exploratory-data-analysis
- visualization
- automated
- charts
- correlation
- distribution
- outliers
- feature-analysis
platforms:
- python
related_skills:
- ydata-profiling
- pandas-data-processing
- polars
- plotly
- streamlit
requires: []
scripts_exempt: true
---

# Autoviz

## When to Use This Skill

### USE AutoViz when:

- **Quick EDA** - Need rapid insights into a new dataset
- **Initial exploration** - Starting analysis on unfamiliar data
- **Pattern discovery** - Automatically detect relationships between variables
- **Presentation prep** - Need charts quickly for stakeholder meetings
- **Large datasets** - Built-in sampling handles big data efficiently
- **Feature analysis** - Understanding distribution and importance of features
- **Correlation hunting** - Finding relationships without manual chart creation
- **Report generation** - Export comprehensive HTML reports
### DON'T USE AutoViz when:

- **Custom visualizations** - Need highly specific chart designs
- **Interactive dashboards** - Use Streamlit or Dash instead
- **Real-time data** - Streaming visualization requirements
- **Production systems** - Charts for automated pipelines (use Plotly/Altair)
- **Precise statistical tests** - Need formal hypothesis testing
- **Domain-specific plots** - Specialized visualizations not in standard EDA

## Prerequisites

```bash
# Basic installation
pip install autoviz

# With all visualization backends
pip install autoviz matplotlib seaborn plotly bokeh

# Using uv (recommended)
uv pip install autoviz pandas matplotlib seaborn plotly

# Jupyter notebook support
pip install autoviz ipywidgets notebook

# Verify installation
python -c "from autoviz import AutoViz_Class; print('AutoViz ready!')"
```

## Complete Examples

### Example 1: Sales Data EDA Pipeline

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def sales_eda_pipeline(
    data_path: str,
    output_dir: str,

*See sub-skills for full details.*
### Example 2: Machine Learning Feature Analysis

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
import os

def ml_feature_analysis(
    X: pd.DataFrame,
    y: pd.Series,

*See sub-skills for full details.*
### Example 3: Multi-Dataset Comparison

```python
from autoviz import AutoViz_Class
import pandas as pd
import numpy as np
import os
from datetime import datetime

def compare_datasets(
    datasets: dict,
    output_dir: str = "comparison_output"

*See sub-skills for full details.*

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic one-line EDA functionality
  - Chart format options (png, svg, html, bokeh, server)
  - Large dataset handling with sampling
  - Feature distribution analysis
  - Correlation detection
  - Outlier identification
  - HTML and notebook export
  - Complete pipeline examples
  - Integration with Streamlit and Polars
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://github.com/AutoViML/AutoViz
- **PyPI**: https://pypi.org/project/autoviz/
- **Tutorial**: https://towardsdatascience.com/autoviz-a-new-tool-for-automated-visualization-ec9c1744a6ad
- **Examples**: https://github.com/AutoViML/AutoViz/tree/master/examples

---

**Automate your exploratory data analysis with AutoViz - one line of code, comprehensive insights!**

## Sub-Skills

- [1. Basic One-Line EDA](1-basic-one-line-eda/SKILL.md)
- [2. Chart Format and Output Options (+1)](2-chart-format-and-output-options/SKILL.md)
- [4. Feature Analysis and Distribution Plots](4-feature-analysis-and-distribution-plots/SKILL.md)
- [5. Correlation Detection](5-correlation-detection/SKILL.md)
- [6. Outlier Detection and Highlighting](6-outlier-detection-and-highlighting/SKILL.md)
- [7. Export to HTML and Notebooks](7-export-to-html-and-notebooks/SKILL.md)
- [AutoViz with Streamlit (+1)](autoviz-with-streamlit/SKILL.md)
- [1. Sample Large Datasets (+3)](1-sample-large-datasets/SKILL.md)
- [Common Issues](common-issues/SKILL.md)
