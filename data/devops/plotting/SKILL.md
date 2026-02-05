---
name: plotting
description: Creates publication-quality scientific plots. Use when making plots, figures, or visualizations. Applies tueplots TMLR styling, LaTeX rendering, no titles.
version: 1.0.0
---

# Scientific Plotting

```python
from tueplots import bundles
import matplotlib.pyplot as plt

plt.rcParams.update(bundles.tmlr2023())
plt.rcParams.update({"text.usetex": True})
```

No titles. Save as PDF with `bbox_inches="tight"`.

Use latex to render formula
```python
plt.plot(x,y,label=r"$\sigma$)
```
