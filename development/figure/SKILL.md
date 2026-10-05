---
name: figure
description: Called by /plot to generate and upgrade econometric figures to top-journal standards.
---

# Publication-Quality Figures

This skill generates figure code that meets the formatting standards of top economics journals (AER, QJE, ReStud, Econometrica, JPE). It covers the most common econometric figure types with precise control over fonts, colors, dimensions, and export formats.

## Step 0: Workflow Interface

When called by `/plot` or another upstream command, this skill accepts a structured context block. **Do not re-ask the user for information already present in the context.**

```
strategy:         DiD | RDD | IV | PanelFE | SC | OLS
figure_type:      event_study | parallel_trends | rdd_binscatter | mccrary |
                  iv_scatter | sc_gap | sc_placebo | coefplot | binscatter |
                  density | timeseries | multipanel
software:         python | r | stata
data_path:        path to clean dataset (e.g., data/clean/analysis.parquet)
Y_var:            outcome variable name
D_var:            treatment variable name
Z_var:            instrument variable name (IV only)
running_var:      running variable name (RDD only)
cutoff_value:     numeric cutoff (RDD only)
time_var:         time/period variable name
id_var:           unit identifier variable name
treatment_timing: first treatment period (DiD/Event Study)
fig_num:          integer, for file naming (e.g., 3 → fig03_...)
project_name:     string
```

When called standalone (not via `/plot`), prompt the user for `strategy`, `figure_type`, and `software` before proceeding.

**Strategy → required figures routing (execute only figures matching `figure_type`):**

| `strategy` | 必须 (Must) | 推荐 (Recommended) |
|---|---|---|
| `DiD` | `parallel_trends`, `event_study` | `coefplot` (robustness specs) |
| `RDD` | `rdd_binscatter`, `mccrary` | `coefplot` (bandwidth sensitivity) |
| `IV` | `iv_scatter` (first stage + exclusion) | `binscatter` (Z–Y reduced form) |
| `PanelFE` | `coefplot` | `parallel_trends`, `binscatter` |
| `SC` | `sc_gap`, `sc_placebo` | `parallel_trends` (pre-period fit) |
| `OLS` | `binscatter` | `coefplot`, `density` |

**Output convention (always dual-format):**

Every figure must be saved in two files:
- `figures/figNN_name.pdf` — vector, for journal submission (`\includegraphics{}`)
- `figures/figNN_name.png` — 300 DPI raster, for draft preview and slides

## Journal Requirements Summary

| Requirement | AER / QJE / ReStud Standard |
|-------------|----------------------------|
| File format | PDF (vector) or EPS; PNG at 300+ DPI for raster |
| Dimensions | Width: 3.4in (single column) or 7in (full page); height ≤ 9in |
| Font | Matching journal body font; minimum 8pt for labels |
| Colors | Must be readable in grayscale; avoid red-green pairs |
| Line width | ≥ 0.5pt for data lines; ≥ 0.75pt for axes |
| Legend | Inside plot area or below; no box border preferred |
| Notes | Figure notes below, starting with "Notes:" |
| Numbering | "Figure 1:", "Figure 2:" etc. in caption |

## Base Setup: Journal-Ready Defaults

### Python (matplotlib)

```python
# Python — journal-quality defaults
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# AER/QJE style defaults
plt.rcParams.update({
    'figure.figsize': (7, 4.5),
    'figure.dpi': 300,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern Roman'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.5,
    'lines.markersize': 5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# Grayscale-safe palette: differentiate series with LINESTYLE + MARKER first,
# color second. This ensures figures are readable when printed in black & white.
# Rule: never rely on color alone to distinguish two series.
COLORS = [
    '#000000',   # black        — primary series / treated
    '#555555',   # dark gray    — secondary series / control / synthetic
    '#999999',   # medium gray  — tertiary series
    '#cccccc',   # light gray   — reference / placebo / background
]
MARKERS    = ['o', 's', '^', 'D']          # circle, square, triangle, diamond
LINESTYLES = ['-', '--', '-.', ':']        # solid, dashed, dash-dot, dotted

# Color for fills / shaded CI bands — always use low alpha so gray stays readable
FILL_ALPHA = 0.15

# For figures that genuinely benefit from color (slides, online appendix),
# use this color-enhanced palette as an explicit opt-in:
COLORS_COLOR = ['#2c3e50', '#2980b9', '#27ae60', '#e67e22']  # dark-blue-green-orange
```

### R (ggplot2)

```r
# R — journal-quality ggplot2 theme
library(ggplot2)
library(scales)

theme_econ <- function(base_size = 11, base_family = "serif") {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      # Clean axes
      panel.grid.major = element_line(color = "grey90", linewidth = 0.3),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "black", linewidth = 0.5),
      axis.ticks = element_line(color = "black", linewidth = 0.3),
      # Text
      axis.title = element_text(size = rel(1.1)),
      axis.text = element_text(size = rel(0.9), color = "black"),
      plot.title = element_text(size = rel(1.2), face = "bold", hjust = 0),
      plot.subtitle = element_text(size = rel(0.95), color = "grey30"),
      plot.caption = element_text(size = rel(0.8), hjust = 0, color = "grey40"),
      # Legend
      legend.position = "bottom",
      legend.title = element_blank(),
      legend.background = element_blank(),
      legend.key = element_blank(),
      # Margins
      plot.margin = margin(10, 15, 10, 10)
    )
}

# Grayscale-safe palette: differentiate with linetype + shape, color secondary
# Never rely on color alone to distinguish series (must survive B&W printing)
econ_gray  <- c("#000000", "#555555", "#999999", "#cccccc")
econ_ltype <- c("solid", "dashed", "dotdash", "dotted")
econ_shape <- c(16, 15, 17, 18)   # circle, square, triangle, diamond

# Color opt-in for slides / online appendix only:
econ_colors <- c("#2c3e50", "#2980b9", "#27ae60", "#e67e22")

# Export function
save_econ_fig <- function(plot, filename, width = 7, height = 4.5) {
  ggsave(filename, plot, width = width, height = height, dpi = 300,
         device = cairo_pdf)  # vector PDF with embedded fonts
}
```

### Stata

```stata
* Stata — journal-quality graph scheme
set scheme s2color
graph set window fontface "Times New Roman"

* Global graph options for consistency
global graph_opts ///
    graphregion(color(white) margin(small)) ///
    plotregion(margin(medium)) ///
    ylabel(, angle(horizontal) nogrid labsize(small)) ///
    xlabel(, labsize(small)) ///
    legend(region(lcolor(none)) size(small) rows(1) position(6))

* Export as PDF
graph export "figure.pdf", as(pdf) replace
```

## Common Econometric Figure Types

### 1. Event Study / Dynamic Treatment Effects

```python
# Python — event study plot
import pandas as pd

def plot_event_study(coefs, ses, periods, ref_period=-1,
                     treatment_time=0, title="Event Study",
                     ylabel="Coefficient Estimate",
                     fig_num=1, cluster_desc="entity level",
                     pretrend_pval=None):
    """
    Event study plot with dual confidence intervals (standard in AER/QJE).
    - 95% CI: thin errorbar lines (outer bound)
    - 90% CI: thick errorbar lines (inner bound, emphasizes economic significance)
    - Pre-period shaded in light gray to visually separate pre/post
    - Reference period (ref_period) plotted as hollow circle at zero
    """
    import numpy as np
    fig, ax = plt.subplots(figsize=(7, 4.5))

    coefs  = np.array(coefs)
    ses    = np.array(ses)
    periods = np.array(periods)

    # Mask out reference period (normalized to 0 by construction)
    mask = periods != ref_period

    # Dual CI bounds
    ci95_lo = coefs - 1.96 * ses
    ci95_hi = coefs + 1.96 * ses
    ci90_lo = coefs - 1.645 * ses
    ci90_hi = coefs + 1.645 * ses

    # Pre-treatment shading
    pre_mask = periods < treatment_time
    if pre_mask.any():
        ax.axvspan(periods[pre_mask].min() - 0.5,
                   treatment_time - 0.5,
                   alpha=0.06, color='grey', zorder=0)

    # 95% CI — thin outer lines
    ax.errorbar(periods[mask], coefs[mask],
                yerr=np.array([coefs[mask] - ci95_lo[mask],
                               ci95_hi[mask] - coefs[mask]]),
                fmt='none', color=COLORS[0], linewidth=0.8,
                capsize=3, capthick=0.8, zorder=3, label='95% CI')

    # 90% CI — thick inner lines
    ax.errorbar(periods[mask], coefs[mask],
                yerr=np.array([coefs[mask] - ci90_lo[mask],
                               ci90_hi[mask] - coefs[mask]]),
                fmt='none', color=COLORS[0], linewidth=2.0,
                capsize=0, zorder=4, label='90% CI')

    # Point estimates (filled) + reference period (hollow at zero)
    ax.plot(periods[mask], coefs[mask], 'o', color=COLORS[0],
            markersize=5, linewidth=0, zorder=5)
    ax.plot([ref_period], [0], 'o', color='white',
            markeredgecolor=COLORS[0], markersize=5, zorder=5)

    # Zero line and treatment cutoff
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=treatment_time - 0.5, color=COLORS[1],
               linewidth=0.8, linestyle='--')
    ax.text(treatment_time - 0.5, ax.get_ylim()[1],
            'Treatment', ha='right', va='top',
            fontsize=9, color=COLORS[1])

    # Pre-trend annotation
    if pretrend_pval is not None:
        ax.text(0.02, 0.97,
                f"Pre-trend joint test: p = {pretrend_pval:.3f}",
                transform=ax.transAxes, fontsize=9,
                va='top', ha='left', color='black')

    ax.set_xlabel("Periods Relative to Treatment")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(frameon=False, fontsize=9, loc='lower right')

    notes = (f"Notes: 90% (thick) and 95% (thin) confidence intervals shown. "
             f"Standard errors clustered at the {cluster_desc}. "
             f"Reference period: t = {ref_period} (normalized to zero).")
    fig.text(0, -0.05, notes, ha='left', fontsize=8, color='#444444',
             wrap=True, transform=ax.transAxes)

    plt.tight_layout()
    save_fig(fig, fig_num, "event_study")
    return fig
```

```r
# R — event study with fixest
library(fixest)

es <- feols(y ~ i(rel_time, treat, ref = -1) | entity_id + year,
            data = df, cluster = ~entity_id)

# fixest iplot (quick)
iplot(es, xlab = "Periods Relative to Treatment",
      ylab = "Coefficient Estimate",
      main = "Event Study: Dynamic Treatment Effects")

# ggplot2 version (full control)
library(broom)
es_df <- tidy(es, conf.int = TRUE) %>%
  filter(grepl("rel_time", term)) %>%
  mutate(period = as.numeric(gsub(".*::(-?\\d+):.*", "\\1", term)))

# Add reference period
es_df <- bind_rows(es_df,
  tibble(period = -1, estimate = 0, conf.low = 0, conf.high = 0))

ggplot(es_df, aes(x = period, y = estimate)) +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high),
              fill = econ_colors[1], alpha = 0.15) +
  geom_point(color = econ_colors[1], size = 2) +
  geom_line(color = econ_colors[1], linewidth = 0.8) +
  geom_hline(yintercept = 0, linewidth = 0.5) +
  geom_vline(xintercept = -0.5, linetype = "dashed", color = "grey50") +
  labs(x = "Periods Relative to Treatment",
       y = "Coefficient Estimate",
       title = "Event Study: Dynamic Treatment Effects",
       caption = "Notes: 95% confidence intervals shown. Standard errors clustered at entity level.") +
  theme_econ()

save_econ_fig(last_plot(), "event_study.pdf")
```

```stata
* Stata — event study plot
reghdfe y ib(-1).rel_time, absorb(entity_id year) cluster(entity_id)

coefplot, vertical drop(_cons) ///
    yline(0, lcolor(black) lwidth(thin)) ///
    xline(4.5, lcolor(gs8) lpattern(dash)) ///
    ciopts(recast(rcap) lcolor(navy) lwidth(thin)) ///
    mcolor(navy) msymbol(circle) ///
    ytitle("Coefficient Estimate") ///
    xtitle("Periods Relative to Treatment") ///
    title("Event Study: Dynamic Treatment Effects") ///
    note("Notes: 95% CIs shown. SEs clustered at entity level.") ///
    $graph_opts
graph export "event_study.pdf", as(pdf) replace
```

### 2. Coefficient Plot (Multiple Models)

```python
# Python — coefficient plot comparing specifications
def plot_coefplot(models, model_names, var_names, var_labels=None):
    fig, ax = plt.subplots(figsize=(7, 0.6 * len(var_names) + 1.5))
    var_labels = var_labels or var_names
    n_models = len(models)
    offsets = np.linspace(-0.15 * (n_models-1), 0.15 * (n_models-1), n_models)

    for j, (coefs, ses, name) in enumerate(zip(
        [m['coefs'] for m in models],
        [m['ses'] for m in models],
        model_names)):

        y_pos = np.arange(len(var_names)) + offsets[j]
        ax.errorbar(coefs, y_pos, xerr=1.96 * np.array(ses),
                    fmt='o', color=COLORS[j], markersize=5,
                    capsize=3, linewidth=1.2, label=name)

    ax.axvline(x=0, color='black', linewidth=0.5)
    ax.set_yticks(range(len(var_names)))
    ax.set_yticklabels(var_labels)
    ax.set_xlabel("Coefficient Estimate")
    ax.legend(loc='lower right', frameon=False)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("coefplot.pdf")
```

```r
# R — coefficient plot with modelsummary/modelplot
library(modelsummary)

modelplot(list("OLS" = m1, "IV" = m2, "FE" = m3),
          coef_map = c("x1" = "Treatment", "x2" = "Income", "x3" = "Education"),
          color = "model") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  labs(x = "Coefficient Estimate", y = "") +
  scale_color_manual(values = econ_colors[1:3]) +
  theme_econ()
```

### 3. Binned Scatter Plot (binscatter)

```python
# Python — binned scatter with linear fit
def plot_binscatter(x, y, n_bins=20, controls=None, xlabel="X", ylabel="Y",
                    title="", residualize=False):
    import statsmodels.api as sm

    if residualize and controls is not None:
        # Residualize both x and y on controls
        x = sm.OLS(x, sm.add_constant(controls)).fit().resid
        y = sm.OLS(y, sm.add_constant(controls)).fit().resid

    # Create bins
    bins = pd.qcut(x, n_bins, duplicates='drop')
    bin_means = pd.DataFrame({'x': x, 'y': y, 'bin': bins}).groupby('bin').mean()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(bin_means['x'], bin_means['y'], color=COLORS[0],
               s=40, zorder=5, edgecolors='white', linewidth=0.5)

    # Linear fit
    z = np.polyfit(bin_means['x'], bin_means['y'], 1)
    x_line = np.linspace(bin_means['x'].min(), bin_means['x'].max(), 100)
    ax.plot(x_line, np.polyval(z, x_line), color=COLORS[1],
            linewidth=1.2, linestyle='--')

    slope, pval = z[0], sm.OLS(y, sm.add_constant(x)).fit().pvalues[1]
    ax.annotate(f"Slope = {slope:.3f} (p = {pval:.3f})",
                xy=(0.05, 0.95), xycoords='axes fraction',
                fontsize=10, va='top')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig("binscatter.pdf")
```

```r
# R — binscatter with binsreg (Cattaneo et al.)
library(binsreg)
binsreg(y = df$y, x = df$x, w = ~ x1 + x2,  # controls
        data = df, dots = c(0, 0), line = c(3, 3),
        ci = c(3, 3), cb = c(3, 3),
        title = "Binned Scatter: Y vs X",
        x.label = "X Variable", y.label = "Y Variable")

# ggplot2 manual version
library(dplyr)
df_binned <- df %>%
  mutate(bin = ntile(x, 20)) %>%
  group_by(bin) %>%
  summarize(x = mean(x), y = mean(y))

ggplot(df_binned, aes(x = x, y = y)) +
  geom_point(color = econ_colors[1], size = 3) +
  geom_smooth(method = "lm", se = FALSE, color = econ_colors[2],
              linetype = "dashed", linewidth = 0.8) +
  labs(x = "X Variable", y = "Y Variable") +
  theme_econ()
```

```stata
* Stata — binscatter
ssc install binscatter

binscatter y x, controls(x1 x2) nquantiles(20) ///
    lcolor(navy) mcolor(navy) ///
    ytitle("Y Variable") xtitle("X Variable") ///
    title("Binned Scatter: Y vs X") ///
    $graph_opts
graph export "binscatter.pdf", as(pdf) replace
```

### 4. RDD Visualization

```python
# Python — RDD plot with local polynomial fit
def plot_rdd(running_var, outcome, cutoff, bandwidth=None,
             n_bins=20, title="Regression Discontinuity"):
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Binned means (separate for each side)
    for side, mask, color in [("Control", running_var < cutoff, COLORS[0]),
                               ("Treated", running_var >= cutoff, COLORS[1])]:
        x_side = running_var[mask]
        y_side = outcome[mask]
        bins = pd.qcut(x_side, min(n_bins, len(x_side)//5), duplicates='drop')
        bm = pd.DataFrame({'x': x_side, 'y': y_side, 'bin': bins}).groupby('bin').mean()
        ax.scatter(bm['x'], bm['y'], color=color, s=35, zorder=5,
                   edgecolors='white', linewidth=0.5)

        # Local polynomial fit
        z = np.polyfit(x_side, y_side, 1)
        x_fit = np.linspace(x_side.min(), x_side.max(), 200)
        ax.plot(x_fit, np.polyval(z, x_fit), color=color, linewidth=1.5)

    # Cutoff line
    ax.axvline(x=cutoff, color='grey', linewidth=1, linestyle='--')
    ax.set_xlabel("Running Variable")
    ax.set_ylabel("Outcome")
    ax.set_title(title)

    if bandwidth:
        ax.axvspan(cutoff - bandwidth, cutoff + bandwidth,
                   alpha=0.05, color='grey')

    plt.tight_layout()
    plt.savefig("rdd_plot.pdf")
```

```r
# R — RDD plot (rdrobust)
library(rdrobust)
rdplot(y = df$y, x = df$running_var, c = cutoff,
       title = "Regression Discontinuity",
       x.label = "Running Variable", y.label = "Outcome",
       col.dots = econ_colors[1:2], col.lines = econ_colors[1:2])

# ggplot2 version
ggplot(df, aes(x = running_var, y = y)) +
  geom_point(aes(color = running_var >= cutoff), alpha = 0.15, size = 1) +
  geom_smooth(data = filter(df, running_var < cutoff),
              method = "lm", formula = y ~ poly(x, 1),
              color = econ_colors[1], fill = econ_colors[1], alpha = 0.1) +
  geom_smooth(data = filter(df, running_var >= cutoff),
              method = "lm", formula = y ~ poly(x, 1),
              color = econ_colors[2], fill = econ_colors[2], alpha = 0.1) +
  geom_vline(xintercept = cutoff, linetype = "dashed", color = "grey40") +
  scale_color_manual(values = econ_colors[1:2], guide = "none") +
  labs(x = "Running Variable", y = "Outcome",
       title = "Regression Discontinuity Design") +
  theme_econ()
```

```stata
* Stata — RDD plot
rdplot y running_var, c(cutoff) ///
    graph_options(title("Regression Discontinuity") ///
    ytitle("Outcome") xtitle("Running Variable") ///
    $graph_opts)
graph export "rdd_plot.pdf", as(pdf) replace
```

### 5. Kernel Density / Distribution Comparison

```python
# Python — overlapping density plot
from scipy.stats import gaussian_kde

def plot_density(groups, labels, xlabel="Value", title=""):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, (data, label) in enumerate(zip(groups, labels)):
        kde = gaussian_kde(data, bw_method='silverman')
        x_grid = np.linspace(data.min() - data.std(), data.max() + data.std(), 300)
        ax.plot(x_grid, kde(x_grid), color=COLORS[i], linewidth=1.5, label=label)
        ax.fill_between(x_grid, kde(x_grid), alpha=0.1, color=COLORS[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density")
    ax.set_title(title)
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig("density.pdf")
```

```r
# R — density comparison
ggplot(df, aes(x = outcome, fill = group, color = group)) +
  geom_density(alpha = 0.15, linewidth = 0.8) +
  scale_fill_manual(values = econ_colors[1:2]) +
  scale_color_manual(values = econ_colors[1:2]) +
  labs(x = "Outcome", y = "Density",
       title = "Distribution by Group") +
  theme_econ()
```

```stata
* Stata — density comparison
twoway (kdensity outcome if group == 0, lcolor(navy) lwidth(medthick)) ///
       (kdensity outcome if group == 1, lcolor(cranberry) lwidth(medthick) ///
        lpattern(dash)), ///
       legend(label(1 "Control") label(2 "Treatment")) ///
       ytitle("Density") xtitle("Outcome") ///
       title("Distribution by Group") ///
       $graph_opts
graph export "density.pdf", as(pdf) replace
```

### 6. Time Series / Trend Plot

```python
# Python — time series with shaded recession bars
def plot_timeseries(dates, series_dict, recessions=None,
                    ylabel="", title=""):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, (label, values) in enumerate(series_dict.items()):
        ax.plot(dates, values, color=COLORS[i], linewidth=1.5,
                linestyle=LINESTYLES[i], label=label)

    if recessions:
        for start, end in recessions:
            ax.axvspan(start, end, alpha=0.08, color='grey')

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(frameon=False, loc='best')
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("timeseries.pdf")
```

```r
# R — time series with recession shading
library(ggplot2)

ggplot(df, aes(x = date, y = value)) +
  geom_rect(data = recessions,
            aes(xmin = start, xmax = end, ymin = -Inf, ymax = Inf),
            inherit.aes = FALSE, fill = "grey", alpha = 0.1) +
  geom_line(aes(color = series, linetype = series), linewidth = 0.8) +
  scale_color_manual(values = econ_colors) +
  labs(x = "", y = "Value", title = "Time Series Comparison") +
  theme_econ()
```

### 7. Synthetic Control Gap Plot

```python
# Python — treated vs synthetic control + gap
def plot_synth(years, treated, synthetic, treatment_year, title=""):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Panel A: Levels
    ax = axes[0]
    ax.plot(years, treated, color=COLORS[0], linewidth=1.5, label="Treated")
    ax.plot(years, synthetic, color=COLORS[1], linewidth=1.5,
            linestyle='--', label="Synthetic Control")
    ax.axvline(x=treatment_year, color='grey', linewidth=0.8, linestyle='--')
    ax.set_title("(a) Treated vs. Synthetic Control")
    ax.set_ylabel("Outcome")
    ax.legend(frameon=False)

    # Panel B: Gap
    ax = axes[1]
    gap = np.array(treated) - np.array(synthetic)
    ax.plot(years, gap, color=COLORS[0], linewidth=1.5)
    ax.fill_between(years, 0, gap, where=np.array(years) >= treatment_year,
                    alpha=0.15, color=COLORS[0])
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=treatment_year, color='grey', linewidth=0.8, linestyle='--')
    ax.set_title("(b) Treatment Effect (Gap)")
    ax.set_ylabel("Treated − Synthetic")

    for ax in axes:
        ax.set_xlabel("Year")
    plt.tight_layout()
    plt.savefig("synth_plot.pdf")
```

### 8. McCrary Density Test Plot (RDD — Manipulation Check)

The McCrary plot is a **mandatory** diagnostic for every RDD paper. It visualizes the density of the running variable around the cutoff and flags sorting/manipulation. Always pair with the formal `rddensity` test p-value.

```python
# Python — McCrary density plot using rddensity output
# pip install rdd  (or use the rddensity R package via rpy2)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def plot_mccrary(running_var, cutoff, bandwidth=None,
                 n_bins=30, fig_num=2, rddensity_pval=None):
    """
    McCrary (2008) / Cattaneo et al. density continuity test plot.
    Left panel: histogram + separate KDE fits on each side.
    Annotates with rddensity p-value if provided.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    rv = np.array(running_var)
    left  = rv[rv < cutoff]
    right = rv[rv >= cutoff]

    # Histogram (same bin width, separate colors)
    bins = np.linspace(rv.min(), rv.max(), n_bins + 1)
    ax.hist(left,  bins=bins, color=COLORS[1], alpha=0.35,
            linewidth=0.4, edgecolor='white', label='Below cutoff')
    ax.hist(right, bins=bins, color=COLORS[0], alpha=0.55,
            linewidth=0.4, edgecolor='white', label='Above cutoff')

    # KDE fits — separate for each side
    x_left  = np.linspace(left.min(),  cutoff, 200)
    x_right = np.linspace(cutoff, right.max(), 200)
    kde_l = gaussian_kde(left,  bw_method='silverman')
    kde_r = gaussian_kde(right, bw_method='silverman')

    # Scale KDE to histogram counts
    bin_width = bins[1] - bins[0]
    scale = len(rv) * bin_width
    ax.plot(x_left,  kde_l(x_left)  * scale, color=COLORS[1],
            linewidth=1.8, linestyle='--')
    ax.plot(x_right, kde_r(x_right) * scale, color=COLORS[0],
            linewidth=1.8, linestyle='-')

    # Cutoff line
    ax.axvline(x=cutoff, color='black', linewidth=1.0, linestyle='-')

    # Bandwidth shading (optional)
    if bandwidth is not None:
        ax.axvspan(cutoff - bandwidth, cutoff + bandwidth,
                   alpha=0.04, color='grey')

    # Annotation
    pval_text = (f"rddensity p-value = {rddensity_pval:.3f}"
                 if rddensity_pval is not None else "")
    interp = (" → No evidence of manipulation"
              if rddensity_pval is not None and rddensity_pval > 0.1
              else (" → Possible manipulation" if rddensity_pval is not None else ""))
    if pval_text:
        ax.text(0.98, 0.97, pval_text + interp,
                transform=ax.transAxes, fontsize=9,
                va='top', ha='right', color='black')

    ax.set_xlabel("Running Variable (centered at cutoff)")
    ax.set_ylabel("Count")
    ax.set_title("Density Continuity Test (McCrary)")
    ax.legend(frameon=False, fontsize=9)

    notes = ("Notes: Histogram of running variable around the cutoff. "
             "Dashed (solid) line shows kernel density estimate below (above) cutoff. "
             "Cattaneo et al. (2018) rddensity test for density discontinuity.")
    fig.text(0, -0.05, notes, ha='left', fontsize=8, color='#444444',
             wrap=True, transform=ax.transAxes)

    plt.tight_layout()
    save_fig(fig, fig_num, "mccrary_density")
    return fig
```

```r
# R — McCrary plot using rddensity
library(rddensity)
library(rdplotdensity)

rdd_test <- rddensity(X = df$running_var, c = cutoff)
summary(rdd_test)   # p-value for density discontinuity

rdplotdensity(rdd_test, df$running_var,
              xlabel = "Running Variable (centered at cutoff)",
              ylabel = "Density",
              title  = "Density Continuity Test (McCrary)")
```

```stata
* Stata — McCrary test (DCdensity) + rddensity
ssc install rddensity
ssc install lpdensity

* Visual + test
rddensity running_var, c(cutoff) plot ///
    graph_options(title("Density Continuity Test") ///
    xtitle("Running Variable") ytitle("Density") $graph_opts)
graph export "figures/fig02_mccrary.pdf", as(pdf) replace
```

### 9. IV First-Stage and Exclusion Restriction Scatter

Two side-by-side scatter plots are standard in IV papers: (a) Z → D (first stage, must show strong correlation), (b) Z → Y (reduced form, evidence for exclusion restriction — Z should affect Y only through D).

```python
# Python — IV diagnostic scatter (2-panel)
def plot_iv_scatter(Z, D, Y, Z_label="Instrument (Z)",
                    D_label="Treatment (D)", Y_label="Outcome (Y)",
                    fig_num=3, fstat=None):
    """
    Panel (a): First stage — Z vs D scatter + OLS fit line + F-stat annotation
    Panel (b): Exclusion check — Z vs Y scatter + OLS fit line
    If |corr(Z,Y)| > |corr(Z,D)| × 0.8, print a red warning.
    """
    import statsmodels.api as sm
    from scipy import stats

    Z, D, Y = np.array(Z), np.array(D), np.array(Y)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, x, y, xlabel, ylabel, title_suffix in [
        (axes[0], Z, D, Z_label, D_label, "First Stage (Z → D)"),
        (axes[1], Z, Y, Z_label, Y_label, "Reduced Form (Z → Y)"),
    ]:
        # Binned scatter (30 bins) for readability
        bins = pd.qcut(x, 30, duplicates='drop')
        bm = pd.DataFrame({'x': x, 'y': y, 'bin': bins}).groupby('bin').mean()
        ax.scatter(bm['x'], bm['y'], color=COLORS[0], s=30, zorder=5,
                   edgecolors='white', linewidth=0.4)

        # OLS fit + CI band
        fit = sm.OLS(y, sm.add_constant(x)).fit()
        x_line = np.linspace(x.min(), x.max(), 200)
        y_hat  = fit.params[0] + fit.params[1] * x_line
        ax.plot(x_line, y_hat, color=COLORS[0], linewidth=1.5)

        r, p = stats.pearsonr(x, y)
        ax.text(0.05, 0.95, f"ρ = {r:.3f}  (p = {p:.3f})",
                transform=ax.transAxes, fontsize=9, va='top')

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(f"({chr(97 + list(axes).index(ax))}) {title_suffix}")

    # First-stage F-stat annotation
    if fstat is not None:
        color = 'black' if fstat >= 10 else 'red'
        axes[0].text(0.05, 0.82, f"First-stage F = {fstat:.1f}",
                     transform=axes[0].transAxes, fontsize=9,
                     va='top', color=color)

    # Exclusion restriction warning
    r_ZD = abs(np.corrcoef(Z, D)[0, 1])
    r_ZY = abs(np.corrcoef(Z, Y)[0, 1])
    if r_ZY > r_ZD * 0.8:
        axes[1].text(0.05, 0.72,
                     "⚠ |corr(Z,Y)| > 0.8×|corr(Z,D)|\nExclusion may be weak",
                     transform=axes[1].transAxes, fontsize=8,
                     va='top', color='red')

    notes = ("Notes: Binned scatter plots (30 bins). Panel (a) shows the first-stage "
             "relationship between the instrument and treatment. Panel (b) shows the "
             "reduced-form relationship; large correlation relative to Panel (a) may "
             "indicate violation of the exclusion restriction.")
    fig.text(0, -0.06, notes, ha='left', fontsize=8, color='#444444',
             wrap=True, transform=axes[0].transAxes)

    plt.tight_layout()
    save_fig(fig, fig_num, "iv_scatter")
    return fig
```

```r
# R — IV scatter (2-panel with ggplot2 + patchwork)
library(ggplot2); library(patchwork); library(dplyr)

bin_scatter <- function(data, x_var, y_var, n_bins = 30) {
  data %>%
    mutate(bin = ntile(.data[[x_var]], n_bins)) %>%
    group_by(bin) %>%
    summarise(x = mean(.data[[x_var]]), y = mean(.data[[y_var]]))
}

p_first <- ggplot(bin_scatter(df, "Z", "D"), aes(x, y)) +
  geom_point(size = 2, color = econ_gray[1]) +
  geom_smooth(method = "lm", se = TRUE, color = econ_gray[1],
              fill = econ_gray[3], alpha = 0.15, linewidth = 0.9) +
  labs(x = "Instrument (Z)", y = "Treatment (D)",
       title = "(a) First Stage: Z → D") + theme_econ()

p_reduced <- ggplot(bin_scatter(df, "Z", "Y"), aes(x, y)) +
  geom_point(size = 2, color = econ_gray[2]) +
  geom_smooth(method = "lm", se = TRUE, color = econ_gray[2],
              fill = econ_gray[3], alpha = 0.15, linewidth = 0.9,
              linetype = "dashed") +
  labs(x = "Instrument (Z)", y = "Outcome (Y)",
       title = "(b) Reduced Form: Z → Y") + theme_econ()

combined <- p_first | p_reduced
save_econ_fig(combined, "figures/fig03_iv_scatter.pdf", width = 12, height = 4.5)
```

### 10. Synthetic Control Placebo Plot

The placebo (permutation) plot is **mandatory** for SC papers. It runs the same SC procedure for every donor unit, plots all resulting gaps, and shows whether the treated unit's post-treatment gap is extreme relative to the placebo distribution.

```python
# Python — SC placebo (in-space permutation) plot
def plot_sc_placebo(years, treated_gap, placebo_gaps,
                    treatment_year, mspe_ratio_threshold=5,
                    fig_num=4):
    """
    Placebo inference plot for synthetic control.
    - Gray lines: donor unit gaps (all placebo runs)
    - Optionally exclude high pre-MSPE placebos (ratio > threshold)
    - Black solid line: treated unit gap
    - Post-treatment p-value = rank of treated gap / total gaps
    """
    years = np.array(years)
    treated_gap = np.array(treated_gap)

    # MSPE filter: drop placebos with pre-period MSPE >> treated unit
    pre_mask = years < treatment_year
    treated_pre_mspe = np.mean(treated_gap[pre_mask] ** 2)

    filtered_gaps = []
    for gap in placebo_gaps:
        gap = np.array(gap)
        donor_pre_mspe = np.mean(gap[pre_mask] ** 2)
        if donor_pre_mspe <= mspe_ratio_threshold * treated_pre_mspe:
            filtered_gaps.append(gap)

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Donor gaps (light gray)
    for gap in filtered_gaps:
        ax.plot(years, gap, color=COLORS[2], linewidth=0.6,
                alpha=0.5, zorder=1)

    # Treated gap (black, thick)
    ax.plot(years, treated_gap, color=COLORS[0],
            linewidth=2.0, zorder=5, label='Treated unit')

    # Zero line and treatment cutoff
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=treatment_year, color=COLORS[1],
               linewidth=0.8, linestyle='--')

    # Post-treatment p-value (rank of treated)
    post_mask = years >= treatment_year
    treated_post = np.mean(np.abs(treated_gap[post_mask]))
    donor_posts  = [np.mean(np.abs(g[post_mask])) for g in filtered_gaps]
    rank = sum(d >= treated_post for d in donor_posts) + 1
    pval = rank / (len(filtered_gaps) + 1)

    ax.text(0.98, 0.97,
            f"Permutation p = {pval:.3f}  (rank {rank}/{len(filtered_gaps)+1})",
            transform=ax.transAxes, fontsize=9,
            va='top', ha='right', color='black')

    ax.set_xlabel("Year")
    ax.set_ylabel("Gap (Treated − Synthetic)")
    ax.set_title("Placebo Test: In-Space Permutation")
    ax.legend(frameon=False, fontsize=9)

    notes = (f"Notes: Each gray line shows the gap between a donor unit and its "
             f"synthetic control (placebo runs). Donor units with pre-treatment MSPE "
             f"more than {mspe_ratio_threshold}× the treated unit are excluded "
             f"({len(placebo_gaps) - len(filtered_gaps)} units removed). "
             f"Permutation p-value = fraction of placebos with post-treatment gap "
             f"≥ treated unit.")
    fig.text(0, -0.06, notes, ha='left', fontsize=8, color='#444444',
             wrap=True, transform=ax.transAxes)

    plt.tight_layout()
    save_fig(fig, fig_num, "sc_placebo")
    return fig
```

```r
# R — SC placebo plot with ggplot2
library(ggplot2); library(dplyr); library(tidyr)

# placebo_df: columns = year, unit_id, gap
# treated_df: columns = year, gap

ggplot() +
  # Donor gaps
  geom_line(data = placebo_df,
            aes(x = year, y = gap, group = unit_id),
            color = econ_gray[3], linewidth = 0.5, alpha = 0.5) +
  # Treated gap
  geom_line(data = treated_df,
            aes(x = year, y = gap),
            color = econ_gray[1], linewidth = 1.8) +
  geom_hline(yintercept = 0, linewidth = 0.5) +
  geom_vline(xintercept = treatment_year,
             linetype = "dashed", color = econ_gray[2]) +
  labs(x = "Year", y = "Gap (Treated − Synthetic)",
       title = "Placebo Test: In-Space Permutation",
       caption = paste0("Notes: Gray lines = donor placebo gaps. ",
                        "Black = treated unit. Permutation p = ", pval, ".")) +
  theme_econ()

save_econ_fig(last_plot(), "figures/fig04_sc_placebo.pdf")
```

### 11. Multi-Panel Figures

```python
# Python — multi-panel layout
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

for i, (ax, data, title) in enumerate(zip(
    axes.flat, datasets, panel_titles)):
    ax.scatter(data['x'], data['y'], color=COLORS[0], s=20, alpha=0.5)
    ax.set_title(f"({chr(97+i)}) {title}", fontsize=11)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

plt.tight_layout()
plt.savefig("multipanel.pdf")
```

```r
# R — multi-panel with patchwork
library(patchwork)

p1 <- ggplot(df, aes(x, y1)) + geom_point(size = 1, alpha = 0.3) +
  labs(title = "(a) Panel A") + theme_econ()
p2 <- ggplot(df, aes(x, y2)) + geom_point(size = 1, alpha = 0.3) +
  labs(title = "(b) Panel B") + theme_econ()
p3 <- ggplot(df, aes(x, y3)) + geom_line() +
  labs(title = "(c) Panel C") + theme_econ()
p4 <- ggplot(df, aes(x, y4)) + geom_line() +
  labs(title = "(d) Panel D") + theme_econ()

combined <- (p1 | p2) / (p3 | p4)
save_econ_fig(combined, "multipanel.pdf", width = 12, height = 9)
```

```stata
* Stata — multi-panel with graph combine
graph combine panel_a panel_b panel_c panel_d, ///
    rows(2) cols(2) ///
    title("Figure 1: Main Results") ///
    $graph_opts
graph export "multipanel.pdf", as(pdf) replace
```

## Standardized Figure Notes Format

Every figure **must** include a Notes line directly below the figure. Notes supply the information a reader needs to evaluate the figure without consulting the text. Use this template:

```
Notes: [What the figure shows — figure type and main variable]. [Sample description:
unit, time period, N]. [CI level and SE clustering]. [Key methodological detail
(bandwidth, bin count, reference period, MSPE filter, etc.)].
[Any data transformation or restriction].
```

**Figure-type specific templates:**

| Figure | Required Notes Content |
|---|---|
| Event study | CI level (90%/95%), SE cluster unit, reference period, pre-trend p-value |
| Parallel trends | Group definitions (treated/control), sample period, smoothing method if any |
| RDD binscatter | Bin count, bandwidth (if restricted), polynomial order, cutoff value |
| McCrary density | Test statistic name (rddensity), p-value, bandwidth |
| IV scatter | Bin count, first-stage F-stat, exclusion restriction caveat |
| SC gap | Donor pool size, weight method (Abadie et al.), pre-period RMSPE |
| SC placebo | Number of placebos, MSPE filter threshold, permutation p-value formula |
| Coefplot | SE type, specs included, omitted baseline |

**LaTeX figure environment with Notes:**

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\textwidth]{figures/fig03_event_study}
  \caption{Event Study: Effect of Policy X on Outcome Y}
  \label{fig:event_study}
  \begin{minipage}{\textwidth}
    \footnotesize
    \textit{Notes:} 90\% (thick) and 95\% (thin) confidence intervals shown.
    Standard errors clustered at the firm level. Reference period: $t = -1$
    (normalized to zero). Pre-trend joint test: $p = 0.42$.
    Sample: manufacturing firms, 2000--2015 ($N = 8{,}320$ firm-year observations).
  \end{minipage}
\end{figure}
```

## Formatting Checklist

Before submitting to a journal, verify:

- [ ] **Vector format**: Exported as PDF (not PNG/JPG) for line plots
- [ ] **Readable in grayscale**: Print in B&W to check
- [ ] **Font consistency**: Same font family as paper body text
- [ ] **Axis labels**: Descriptive, with units (e.g., "Income (1000 USD)")
- [ ] **No chartjunk**: Remove gridlines, borders, and unnecessary decoration
- [ ] **Proper aspect ratio**: Not stretched or compressed
- [ ] **Legend placement**: Inside plot if space allows; below otherwise
- [ ] **Panel labels**: (a), (b), (c) for multi-panel figures
- [ ] **Notes below figure**: Data source, sample, key definitions
- [ ] **CI/SE shown**: For any estimated quantities (coefficients, treatment effects)
- [ ] **Reference lines**: Zero line for coefficient plots; cutoff for RDD; treatment date for event study

## Common Pitfalls

- **Using default matplotlib/ggplot themes**: They look unprofessional — always customize
- **Raster exports for line plots**: Use PDF/EPS, not PNG, for any plot with lines or text
- **Too many colors**: Limit to 3–4 distinguishable colors; use linestyle for additional series
- **Tiny axis labels**: Minimum 8pt after scaling to final size in the paper
- **Missing confidence intervals**: Never show point estimates without uncertainty
- **3D plots**: Almost never appropriate in economics — use 2D alternatives
- **Pie charts**: Never use in academic economics papers

## Output File Management

Consistent figure naming and directory layout prevents the most common assembly problem: the paper's `\includegraphics{}` calls pointing to files that don't exist or are scattered across subdirectories (`data/bartik/`, `data/results/`, `output/`, etc.).

### Standard Convention

Save **all** figures to a single `figures/` directory at the project root. Use zero-padded sequential prefixes:

```
figures/
  fig01_aaei_distribution.pdf
  fig02_parallel_trends.pdf
  fig03_event_study_wages.pdf
  fig04_event_study_employment.pdf
  fig05_heterogeneity_wage_group.pdf
  ...
```

The numeric prefix (`fig01_`, `fig02_`, ...) makes insertion order explicit and survives alphabetical sorting. The descriptive suffix means you can identify the figure without opening it.

### Python Helper

Add this to any figure-generating script to enforce the convention:

```python
import os, matplotlib.pyplot as plt

FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

def save_fig(fig, fig_num: int, name: str, formats=("pdf", "png")):
    """
    Save to figures/figNN_name.{pdf,png} with consistent naming.
    Default: always dual-format — PDF (vector, submission) + PNG 300 DPI (draft).
    Pass formats=("pdf",) only if PNG is explicitly not needed.
    """
    paths = []
    for fmt in formats:
        path = os.path.join(FIGURES_DIR, f"fig{fig_num:02d}_{name}.{fmt}")
        dpi = 300 if fmt == "png" else None   # PDF is vector; dpi irrelevant
        fig.savefig(path, bbox_inches='tight', dpi=dpi)
        print(f"Saved: {path}")
        paths.append(path)
    return paths

# Usage:
fig, ax = plt.subplots(figsize=(7, 4.5))
# ... plotting code ...
save_fig(fig, fig_num=3, name="event_study_wages")
# → figures/fig03_event_study_wages.pdf  (vector, for paper)
# → figures/fig03_event_study_wages.png  (300 DPI, for draft / slides)
```

### R Helper

```r
FIGURES_DIR <- "figures"
dir.create(FIGURES_DIR, showWarnings = FALSE, recursive = TRUE)

save_econ_fig <- function(plot, fig_num, name, width = 7, height = 4.5) {
  # Always dual-format: PDF (vector, submission) + PNG 300 DPI (draft/slides)
  pdf_path <- file.path(FIGURES_DIR, sprintf("fig%02d_%s.pdf", fig_num, name))
  png_path <- file.path(FIGURES_DIR, sprintf("fig%02d_%s.png", fig_num, name))

  ggsave(pdf_path, plot, width = width, height = height, device = cairo_pdf)
  ggsave(png_path, plot, width = width, height = height, dpi = 300, device = "png")

  cat("Saved:", pdf_path, "\n")
  cat("Saved:", png_path, "\n")
  invisible(list(pdf = pdf_path, png = png_path))
}

# Usage:
p <- ggplot(...) + theme_econ()
save_econ_fig(p, fig_num = 3, name = "event_study_wages")
# → figures/fig03_event_study_wages.pdf  (vector, for paper)
# → figures/fig03_event_study_wages.png  (300 DPI, for draft / slides)
```

### In the LaTeX Paper

```latex
% In preamble — point to figures/ once:
\graphicspath{{../figures/}}

% In the paper body — no path needed in each call:
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{fig03_event_study_wages}
  \caption{Event Study: Effect of AI Exposure on Log Wages}
  \label{fig:event_study}
\end{figure}
```

When multiple scripts generate figures (e.g., main analysis, robustness, heterogeneity), add a comment block at the top of each script listing which figure numbers it produces. This prevents two scripts overwriting the same file.
