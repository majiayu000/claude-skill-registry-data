---
name: evo-web-scaffold-generator
description: Python utility that creates the output directory structure, copies input data, downloads d3.v6.min.js locally, and writes the index.html and style.css files for the stock visualization dashboard.
---

# evo-web-scaffold-generator

Generates the web app scaffold: directory structure, data copying, D3.js library, HTML, and CSS.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-web-scaffold-generator/scripts')
from utils import setup_output_directory, copy_input_data, download_d3_library, generate_index_html, generate_style_css

setup_output_directory()
copy_input_data()
download_d3_library()
generate_index_html()
generate_style_css()
```

## Functions

- `setup_output_directory(output_dir)` - Creates /root/output with js/, css/, data/, data/indiv-stock/ subdirs
- `copy_input_data(input_dir, output_dir)` - Copies stock-descriptions.csv and indiv-stock/ files
- `download_d3_library(output_dir)` - Downloads d3.v6.min.js from CDN
- `generate_index_html(output_dir)` - Generates index.html with container layout for bubble chart + table
- `generate_style_css(output_dir)` - Generates style.css with tooltip, table, highlight styles
