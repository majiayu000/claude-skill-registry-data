---
name: visualization
description: "Publication-quality statistical visualization with mandatory best practices. Use when creating plots, charts, figures, or any data visualization. Enforces accessibility, uncertainty display, proper labeling, and statistical accuracy."

---

<skill_content>

<overview>
Visualization is not decoration—it is statistical communication. A well-designed plot reveals patterns that tables cannot, while a poor plot misleads more effectively than wrong numbers. Every visualization is an argument about data, and this skill enforces the standards that make those arguments honest, accessible, and reproducible.

The difference between amateur and professional visualization is not aesthetics but statistical integrity: showing uncertainty, avoiding perceptual tricks, ensuring accessibility, and documenting what you've done. This skill enforces visualization practices that meet publication standards while preventing common manipulations.
</overview>

<philosophy>
<core_principle>
"The purpose of visualization is insight, not pictures" - Ben Shneiderman

FUNDAMENTAL RULES:
1. Every estimate needs uncertainty bands
2. Every axis needs units
3. Every color scheme needs accessibility testing
4. Every truncated axis needs justification
5. Every plot needs to be reproducible
</core_principle>
</philosophy>

<mandatory_requirements>

<requirement priority="critical">
  <name>Complete Axis Labeling</name>
  <description>MUST label all axes with variable names AND units in parentheses</description>
  <rationale>Cleveland (1985) found unlabeled axes were the #1 source of misinterpretation in published figures</rationale>
  <consequence>Readers misinterpret scale, leading to order-of-magnitude errors in interpretation</consequence>
</requirement>

<requirement priority="critical">
  <name>Uncertainty Visualization</name>
  <description>ALL point estimates MUST show confidence intervals or standard errors</description>
  <rationale>Cumming et al. (2007) demonstrate that showing uncertainty reduces overconfidence in conclusions by 40%</rationale>
  <consequence>False precision, overconfident claims, inability to distinguish signal from noise</consequence>
</requirement>

<requirement priority="critical">
  <name>Accessibility Compliance</name>
  <description>MUST use colorblind-safe palettes, test with simulator, provide non-color redundancy</description>
  <rationale>8% of men and 0.5% of women have color vision deficiency (Neitz & Neitz, 2011)</rationale>
  <consequence>Excludes ~4% of readers, may violate journal/grant accessibility requirements</consequence>
</requirement>

<requirement priority="high">
  <name>Resolution and Format Standards</name>
  <description>Minimum 144 DPI for screens, 300 DPI for print, vector format for publication</description>
  <rationale>Journal standards require 300+ DPI; low resolution causes rejection at submission</rationale>
  <consequence>Desk rejection from journals, pixelated figures in presentations</consequence>
</requirement>

<requirement priority="high">
  <name>Honest Scaling</name>
  <description>Y-axis MUST start at zero for bar charts, ratios, and percentages unless explicitly justified</description>
  <rationale>Huff (1954) "How to Lie with Statistics" - truncated axes are the most common manipulation</rationale>
  <consequence>Exaggerated effects, misleading comparisons, ethical violations</consequence>
</requirement>

<requirement priority="critical">
  <name>Return Figure Objects for Display</name>
  <description>MUST return figure objects (fig, plt.gcf(), or plt.gca()) as the last expression in the cell. NEVER use plt.show() - it prevents inline display in notebooks and breaks reproducibility</description>
  <rationale>Notebook environments (Jupyter, marimo) automatically display the last expression. plt.show() blocks execution, prevents inline display, and makes figures inaccessible for further manipulation. Returning figure objects enables notebook display, programmatic access, and proper figure management</rationale>
  <consequence>Figures don't display in notebooks, code execution blocked, figures cannot be saved or manipulated programmatically, breaks notebook workflow</consequence>
</requirement>

</mandatory_requirements>

<thinking_process>
When creating statistical visualizations:
1. Choose plot type based on data structure and question
2. Set up proper figure dimensions and resolution
3. Plot data with appropriate aesthetics
4. Add ALL required labels with units
5. Include uncertainty measures (CI, SE, prediction bands)
6. Test accessibility (colorblind simulation)
7. Add statistical annotations (p-values, R², n)
8. Save in multiple formats (PNG for viewing, PDF for publication)
9. Return figure object (fig, plt.gcf(), or plt.gca()) as last expression - NEVER use plt.show()
10. Document code for reproducibility
</thinking_process>

<implementation_pattern>

<code_template>
```python
# CRITICAL: Publication-quality visualization template

@app.cell
def create_publication_figure(df, x_var, y_var, group_var=None):
    """
    Every visualization must meet publication standards.
    This template enforces labeling, uncertainty, accessibility, and
    reproducibility requirements that prevent common mistakes.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import os
    from matplotlib import cm

    # MANDATORY: Set publication-quality defaults
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'axes.linewidth': 1.5,
        'axes.grid': True,
        'grid.alpha': 0.3,
    })

    # MANDATORY: Colorblind-safe palette
    # Source: Wong, B. (2011) Nature Methods 8, 441
    colorblind_colors = [
        '#0173B2',  # Blue
        '#DE8F05',  # Orange
        '#029E73',  # Green
        '#CC78BC',  # Light purple
        '#ECE133',  # Yellow
        '#56B4E9',  # Light blue
        '#F0E442',  # Light yellow
    ]

    # Create figure with specific size for journal column width
    # Single column: 3.5", double column: 7"
    fig, ax = plt.subplots(figsize=(7, 5), dpi=144)

    # Get data statistics for annotations
    n_obs = len(df)
    x_mean = df[x_var].mean()
    y_mean = df[y_var].mean()

    if group_var is None:
        # Single group with confidence band
        ax.scatter(df[x_var], df[y_var], alpha=0.6, s=50,
                  color=colorblind_colors[0], edgecolor='black', linewidth=0.5)

        # Add regression line with confidence interval
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(df[x_var], df[y_var])

        x_line = np.linspace(df[x_var].min(), df[x_var].max(), 100)
        y_line = slope * x_line + intercept

        # Calculate confidence interval for regression line
        from scipy.stats import t
        predict_se = std_err * np.sqrt(1/n_obs + (x_line - x_mean)**2 / ((df[x_var] - x_mean)**2).sum())
        margin = t.ppf(0.975, n_obs - 2) * predict_se

        ax.plot(x_line, y_line, color=colorblind_colors[0], linewidth=2,
               label=f'Fit (R² = {r_value**2:.3f})')
        ax.fill_between(x_line, y_line - margin, y_line + margin,
                       alpha=0.2, color=colorblind_colors[0], label='95% CI')

        # Add statistical annotation
        ax.text(0.05, 0.95, f'n = {n_obs}\np = {p_value:.3f}',
               transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    else:
        # Multiple groups with distinct colors and markers
        markers = ['o', 's', '^', 'D', 'v', '<', '>']
        groups = df[group_var].unique()

        for i, group in enumerate(groups):
            subset = df[df[group_var] == group]
            color = colorblind_colors[i % len(colorblind_colors)]
            marker = markers[i % len(markers)]

            # Plot with confidence intervals
            x_vals = subset.groupby(x_var)[y_var].mean()
            x_sems = subset.groupby(x_var)[y_var].sem()

            ax.errorbar(x_vals.index, x_vals.values, yerr=1.96*x_sems.values,
                       marker=marker, markersize=8, linewidth=2, capsize=5,
                       color=color, label=f'{group} (n={len(subset)})',
                       alpha=0.8)

    # MANDATORY: Complete axis labeling with units
    # Extract units from variable names if formatted as "variable (unit)"
    x_label = x_var if '(' in x_var else f"{x_var} (units)"
    y_label = y_var if '(' in y_var else f"{y_var} (units)"

    ax.set_xlabel(x_label, fontweight='bold')
    ax.set_ylabel(y_label, fontweight='bold')

    # MANDATORY: Informative title
    if group_var:
        ax.set_title(f'{y_var} vs {x_var} by {group_var}\n(Mean ± 95% CI)',
                    fontweight='bold', pad=20)
    else:
        ax.set_title(f'{y_var} vs {x_var}\n(with 95% Confidence Band)',
                    fontweight='bold', pad=20)

    # MANDATORY: Grid for readability
    ax.grid(True, alpha=0.3, linestyle='--')

    # MANDATORY: Legend with sample sizes
    if group_var or True:  # Always show legend for clarity
        ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)

    # Check if y-axis should start at zero (for ratios, percentages, counts)
    if any(keyword in y_var.lower() for keyword in ['percent', 'ratio', 'proportion', 'count']):
        y_min, y_max = ax.get_ylim()
        if y_min > 0:
            ax.set_ylim(bottom=0, top=y_max * 1.1)
            ax.annotate('Note: Y-axis starts at zero', xy=(0.5, -0.15),
                       xycoords='axes fraction', ha='center', fontsize=9, style='italic')

    # Add data source and timestamp for reproducibility
    fig.text(0.99, 0.01, f'Data: {n_obs} observations | Generated: {pd.Timestamp.now().strftime("%Y-%m-%d")}',
            ha='right', fontsize=8, style='italic', alpha=0.7)

    # Tight layout to prevent label cutoff
    plt.tight_layout()

    # MANDATORY: Save in multiple formats
    os.makedirs("./images", exist_ok=True)

    # Screen viewing (PNG at 144 DPI)
    plt.savefig("./images/figure_screen.png", dpi=144, bbox_inches="tight")

    # Publication (PDF vector format)
    plt.savefig("./images/figure_publication.pdf", bbox_inches="tight")

    # High-res for presentations (PNG at 300 DPI)
    plt.savefig("./images/figure_highres.png", dpi=300, bbox_inches="tight")

    print("Figure saved in three formats:")
    print("  ./images/figure_screen.png (144 DPI for screens)")
    print("  ./images/figure_publication.pdf (vector for journals)")
    print("  ./images/figure_highres.png (300 DPI for presentations)")

    # CRITICAL: Return figure for inline display in notebook
    # Do NOT call plt.show() - it prevents inline display and blocks execution
    # Do NOT call plt.close() - this would prevent display
    # MUST return figure object (fig, plt.gcf(), or plt.gca()) as last expression
    return fig,
```
</code_template>

</implementation_pattern>

<examples>

<example context="treatment_effects" difficulty="basic">
<description>Visualizing treatment effects with proper uncertainty bands</description>
<code>
```python
@app.cell
def plot_treatment_effects():
    #Treatment effects must show uncertainty to enable
    # proper inference. This example shows the gold standard for
    # presenting experimental results with multiple treatments.

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import os

    # Simulated treatment effects from an experiment
    treatments = ['Control', 'Treatment A', 'Treatment B', 'Treatment C']
    effects = [0, 2.3, 3.7, 1.8]
    std_errors = [0.5, 0.6, 0.8, 0.7]
    sample_sizes = [102, 98, 95, 101]
    p_values = [1.000, 0.001, 0.0001, 0.042]

    # MANDATORY: Colorblind-safe palette
    colors = ['#808080', '#0173B2', '#029E73', '#DE8F05']

    fig, ax = plt.subplots(figsize=(10, 6), dpi=144)

    # Calculate 95% confidence intervals
    ci_lower = [e - 1.96*se for e, se in zip(effects, std_errors)]
    ci_upper = [e + 1.96*se for e, se in zip(effects, std_errors)]

    # Create coefficient plot (forest plot style)
    y_positions = range(len(treatments))

    for i, (treatment, effect, lower, upper, n, p, color) in enumerate(
        zip(treatments, effects, ci_lower, ci_upper, sample_sizes, p_values, colors)
    ):
        # Plot point estimate
        ax.scatter(effect, i, s=150, color=color, zorder=3,
                  edgecolors='black', linewidth=1.5)

        # Plot confidence interval
        ax.plot([lower, upper], [i, i], linewidth=3, color=color, alpha=0.7)

        # Add caps to CI
        cap_width = 0.05
        ax.plot([lower, lower], [i-cap_width, i+cap_width], linewidth=2, color=color)
        ax.plot([upper, upper], [i-cap_width, i+cap_width], linewidth=2, color=color)

        # Add text annotations with sample size and p-value
        significance = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(upper + 0.2, i, f'n={n}, p={p:.3f} {significance}',
               verticalalignment='center', fontsize=9)

    # MANDATORY: Reference line at zero
    ax.axvline(0, color='red', linestyle='--', alpha=0.5, linewidth=1.5,
              label='No effect')

    # Shade region of practical significance (example: ±0.5)
    ax.axvspan(-0.5, 0.5, alpha=0.1, color='gray',
              label='Region of practical equivalence')

    # MANDATORY: Complete labeling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(treatments)
    ax.set_xlabel('Treatment Effect (units of outcome)', fontweight='bold', fontsize=12)
    ax.set_title('Treatment Effects with 95% Confidence Intervals\nRelative to Control Group',
                fontweight='bold', fontsize=14)

    # Add grid for easier reading
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')

    # Legend
    ax.legend(loc='upper right', frameon=True)

    # Add interpretation guide
    fig.text(0.12, 0.02,
            'Interpretation: Points show estimates, bars show 95% CI. ' +
            'Effects excluding zero are statistically significant at α=0.05.',
            fontsize=9, style='italic', wrap=True)

    # Statistical significance legend
    fig.text(0.88, 0.02,
            '*** p<0.001, ** p<0.01, * p<0.05, ns: not significant',
            ha='right', fontsize=8, style='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    # Save
    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/treatment_effects.png", dpi=144, bbox_inches="tight")
    plt.savefig("./images/treatment_effects.pdf", bbox_inches="tight")

    print("Treatment effect plot created with:")
    print("   - 95% confidence intervals")
    print("   - Sample sizes and p-values")
    print("   - Colorblind-safe colors")
    print("   - Reference line at zero")
    print("   - Region of practical equivalence")

    # Return figure for inline display
    return plt.gcf(),
```
</code>
<lesson>
Forest plots are the gold standard for showing treatment effects. Always include: point estimates, confidence intervals, sample sizes, p-values, and a reference line at zero.
</lesson>
</example>

<example context="time_series_with_events" difficulty="intermediate">
<description>Time series with intervention points and uncertainty bands</description>
<code>
```python
@app.cell
def plot_time_series_with_intervention():
    #Time series plots must clearly show when interventions
    # occurred and quantify uncertainty around trends. This example shows
    # best practices for interrupted time series visualization.

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy import stats
    import os

    # Generate example time series data
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
    n_points = len(dates)

    # Pre-intervention trend
    pre_intervention = 36  # Month 36 is intervention
    trend_pre = 100 + 2 * np.arange(pre_intervention)
    noise_pre = np.random.normal(0, 10, pre_intervention)

    # Post-intervention (level shift + trend change)
    level_shift = 20
    trend_change = -1.5
    trend_post = (100 + 2 * pre_intervention + level_shift +
                 trend_change * np.arange(n_points - pre_intervention))
    noise_post = np.random.normal(0, 12, n_points - pre_intervention)

    # Combine
    values = np.concatenate([trend_pre + noise_pre, trend_post + noise_post])

    df = pd.DataFrame({
        'date': dates,
        'value': values,
        'period': ['Pre' if i < pre_intervention else 'Post' for i in range(n_points)]
    })

    # Calculate rolling mean and std for uncertainty band
    df['rolling_mean'] = df['value'].rolling(window=3, center=True).mean()
    df['rolling_std'] = df['value'].rolling(window=3, center=True).std()

    # VISUALIZATION
    fig, ax = plt.subplots(figsize=(14, 7), dpi=144)

    # Different colors for pre/post periods
    pre_color = '#0173B2'  # Blue
    post_color = '#DE8F05'  # Orange

    # Plot pre-intervention
    pre_data = df[df['period'] == 'Pre']
    ax.plot(pre_data['date'], pre_data['value'],
           marker='o', markersize=4, linewidth=1.5,
           color=pre_color, label='Pre-intervention', alpha=0.8)

    # Plot post-intervention
    post_data = df[df['period'] == 'Post']
    ax.plot(post_data['date'], post_data['value'],
           marker='s', markersize=4, linewidth=1.5,
           color=post_color, label='Post-intervention', alpha=0.8)

    # Add uncertainty bands (±1.96 SE)
    ax.fill_between(df['date'],
                   df['rolling_mean'] - 1.96*df['rolling_std'].fillna(0),
                   df['rolling_mean'] + 1.96*df['rolling_std'].fillna(0),
                   alpha=0.2, color='gray', label='95% CI (rolling)')

    # MANDATORY: Mark intervention point
    intervention_date = dates[pre_intervention]
    ax.axvline(intervention_date, color='red', linestyle='--', linewidth=2,
              label='Intervention', alpha=0.7)

    # Add shaded region for intervention period
    ax.axvspan(intervention_date, dates[-1], alpha=0.1, color='yellow')

    # Fit trend lines for each period
    from sklearn.linear_model import LinearRegression

    # Pre-intervention trend
    X_pre = np.arange(len(pre_data)).reshape(-1, 1)
    model_pre = LinearRegression().fit(X_pre, pre_data['value'])
    trend_line_pre = model_pre.predict(X_pre)
    ax.plot(pre_data['date'], trend_line_pre, '--',
           color=pre_color, linewidth=2, alpha=0.5)

    # Post-intervention trend
    X_post = np.arange(len(post_data)).reshape(-1, 1)
    model_post = LinearRegression().fit(X_post, post_data['value'])
    trend_line_post = model_post.predict(X_post)
    ax.plot(post_data['date'], trend_line_post, '--',
           color=post_color, linewidth=2, alpha=0.5)

    # Add annotations with effect sizes
    pre_slope = model_pre.coef_[0]
    post_slope = model_post.coef_[0]
    level_change = trend_line_post[0] - trend_line_pre[-1]

    # Text box with results
    textstr = f'Pre-trend: {pre_slope:.2f}/month\n'
    textstr += f'Post-trend: {post_slope:.2f}/month\n'
    textstr += f'Level change: {level_change:.1f} units\n'
    textstr += f'Trend change: {post_slope - pre_slope:.2f}/month'

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=props)

    # MANDATORY: Complete labeling
    ax.set_xlabel('Date', fontweight='bold', fontsize=12)
    ax.set_ylabel('Outcome Measure (units)', fontweight='bold', fontsize=12)
    ax.set_title('Interrupted Time Series Analysis\nWith Intervention Effect Quantification',
                fontweight='bold', fontsize=14)

    # Format x-axis dates
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator([1, 4, 7, 10]))

    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', frameon=True)

    # Add note about statistical testing
    fig.text(0.5, 0.01,
            'Note: Formal interrupted time series analysis required for causal inference',
            ha='center', fontsize=9, style='italic')

    plt.tight_layout()

    # Save
    os.makedirs("./images", exist_ok=True)
    plt.savefig("./images/time_series_intervention.png", dpi=144, bbox_inches="tight")
    plt.savefig("./images/time_series_intervention.pdf", bbox_inches="tight")

    print("Time series plot created with:")
    print("   - Clear intervention marking")
    print("   - Pre/post trend lines")
    print("   - Uncertainty bands")
    print("   - Effect size quantification")
    print("   - Proper date formatting")

    # Return figure for inline display
    return plt.gcf(),
```
</code>
<best_practice>
For interrupted time series: Always mark the intervention clearly, show pre/post trends separately, quantify level and slope changes, and include uncertainty bands.
</best_practice>
</example>

<example context="publication_panel_figure" difficulty="advanced">
<description>Multi-panel publication-ready figure with shared aesthetics</description>
<code>
```python
@app.cell
def create_publication_panel_figure():
    #Multi-panel figures are standard in publications.
    # This example shows how to create a complex figure with multiple
    # related plots that share formatting and meet journal standards.

    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats
    import os

    # Generate example data
    np.random.seed(123)
    n = 200
    df = pd.DataFrame({
        'x': np.random.normal(50, 15, n),
        'y': np.random.normal(100, 20, n),
        'group': np.random.choice(['Control', 'Treatment'], n),
        'covariate': np.random.uniform(0, 100, n)
    })

    # Add treatment effect
    treatment_mask = df['group'] == 'Treatment'
    df.loc[treatment_mask, 'y'] += 10 + 0.3 * df.loc[treatment_mask, 'covariate']

    # MANDATORY: Set up publication-quality figure
    # For Nature/Science: width = 180mm (7.09 inches) for full page
    fig = plt.figure(figsize=(7, 8), dpi=300)

    # Use GridSpec for complex layout
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 0.8],
                          width_ratios=[1, 1], hspace=0.3, wspace=0.3)

    # Colorblind-safe colors
    colors = {'Control': '#0173B2', 'Treatment': '#DE8F05'}

    # PANEL A: Distribution comparison
    ax_a = fig.add_subplot(gs[0, :])

    for group in ['Control', 'Treatment']:
        subset = df[df['group'] == group]['y']

        # Histogram with KDE
        counts, bins, _ = ax_a.hist(subset, bins=20, alpha=0.5,
                                    label=group, color=colors[group],
                                    edgecolor='black', linewidth=0.5)

        # Add KDE
        kde = stats.gaussian_kde(subset)
        x_range = np.linspace(subset.min(), subset.max(), 100)
        kde_values = kde(x_range) * len(subset) * (bins[1] - bins[0])
        ax_a.plot(x_range, kde_values, color=colors[group],
                 linewidth=2, alpha=0.8)

        # Add mean line
        mean_val = subset.mean()
        ax_a.axvline(mean_val, color=colors[group], linestyle='--',
                    linewidth=2, alpha=0.7)

        # Add text with stats
        ax_a.text(mean_val, ax_a.get_ylim()[1]*0.9,
                 f'μ={mean_val:.1f}',
                 ha='center', fontsize=8, color=colors[group])

    ax_a.set_xlabel('Outcome (units)', fontweight='bold')
    ax_a.set_ylabel('Frequency', fontweight='bold')
    ax_a.set_title('A. Distribution by Group', fontweight='bold', loc='left')
    ax_a.legend(loc='upper right')
    ax_a.grid(True, alpha=0.3)

    # Statistical test annotation
    t_stat, p_value = stats.ttest_ind(df[df['group'] == 'Control']['y'],
                                      df[df['group'] == 'Treatment']['y'])
    ax_a.text(0.02, 0.95, f't-test: p={p_value:.3f}',
             transform=ax_a.transAxes, fontsize=9,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # PANEL B: Scatter plot with regression
    ax_b = fig.add_subplot(gs[1, 0])

    for group in ['Control', 'Treatment']:
        subset = df[df['group'] == group]
        ax_b.scatter(subset['covariate'], subset['y'],
                    alpha=0.6, s=30, color=colors[group],
                    edgecolor='black', linewidth=0.5, label=group)

        # Add regression line
        slope, intercept, r_value, _, _ = stats.linregress(subset['covariate'], subset['y'])
        x_line = np.linspace(subset['covariate'].min(), subset['covariate'].max(), 100)
        y_line = slope * x_line + intercept
        ax_b.plot(x_line, y_line, color=colors[group],
                 linewidth=2, alpha=0.8)

    ax_b.set_xlabel('Covariate (units)', fontweight='bold')
    ax_b.set_ylabel('Outcome (units)', fontweight='bold')
    ax_b.set_title('B. Relationship with Covariate', fontweight='bold', loc='left')
    ax_b.legend(loc='upper left', fontsize=9)
    ax_b.grid(True, alpha=0.3)

    # PANEL C: Box plot comparison
    ax_c = fig.add_subplot(gs[1, 1])

    positions = [1, 2]
    box_data = [df[df['group'] == 'Control']['y'],
               df[df['group'] == 'Treatment']['y']]

    bp = ax_c.boxplot(box_data, positions=positions,
                      widths=0.6, patch_artist=True,
                      showfliers=True, showmeans=True)

    # Color the boxes
    for patch, group in zip(bp['boxes'], ['Control', 'Treatment']):
        patch.set_facecolor(colors[group])
        patch.set_alpha(0.7)

    # Customize appearance
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color='black', linewidth=1.5)

    ax_c.set_xticks(positions)
    ax_c.set_xticklabels(['Control', 'Treatment'])
    ax_c.set_ylabel('Outcome (units)', fontweight='bold')
    ax_c.set_title('C. Group Comparison', fontweight='bold', loc='left')
    ax_c.grid(True, alpha=0.3, axis='y')

    # Add sample sizes
    for i, (pos, group) in enumerate(zip(positions, ['Control', 'Treatment'])):
        n_group = len(df[df['group'] == group])
        ax_c.text(pos, ax_c.get_ylim()[0] - 5, f'n={n_group}',
                 ha='center', fontsize=9)

    # PANEL D: Effect size with CI
    ax_d = fig.add_subplot(gs[2, :])

    # Calculate effect sizes for different quantiles
    quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
    effects = []
    ci_lower = []
    ci_upper = []

    for q in quantiles:
        control_q = df[df['group'] == 'Control']['y'].quantile(q)
        treatment_q = df[df['group'] == 'Treatment']['y'].quantile(q)
        effect = treatment_q - control_q
        effects.append(effect)

        # Bootstrap CI
        n_bootstrap = 1000
        bootstrap_effects = []
        for _ in range(n_bootstrap):
            control_sample = df[df['group'] == 'Control']['y'].sample(n=100, replace=True)
            treatment_sample = df[df['group'] == 'Treatment']['y'].sample(n=100, replace=True)
            bootstrap_effects.append(treatment_sample.quantile(q) - control_sample.quantile(q))

        ci_lower.append(np.percentile(bootstrap_effects, 2.5))
        ci_upper.append(np.percentile(bootstrap_effects, 97.5))

    # Plot quantile treatment effects
    ax_d.errorbar(quantiles, effects, yerr=[np.array(effects) - np.array(ci_lower),
                                            np.array(ci_upper) - np.array(effects)],
                 fmt='o-', markersize=8, linewidth=2, capsize=5,
                 color='#CC78BC', ecolor='gray', alpha=0.8)

    ax_d.axhline(0, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    ax_d.set_xlabel('Quantile', fontweight='bold')
    ax_d.set_ylabel('Treatment Effect (units)', fontweight='bold')
    ax_d.set_title('D. Quantile Treatment Effects (95% Bootstrap CI)',
                  fontweight='bold', loc='left')
    ax_d.grid(True, alpha=0.3)

    # Overall title
    fig.suptitle('Comprehensive Treatment Effect Analysis',
                fontsize=16, fontweight='bold', y=0.98)

    # Add figure caption
    caption = ("Figure 1. Multi-panel analysis of treatment effects. " +
              "(A) Distribution comparison showing treatment shifts the outcome distribution. " +
              "(B) Covariate relationship reveals heterogeneous treatment effects. " +
              "(C) Box plot comparison with means (triangles) and medians (lines). " +
              "(D) Quantile treatment effects show larger effects at higher quantiles.")

    fig.text(0.1, 0.01, caption, fontsize=9, wrap=True,
            ha='left', style='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 0.96])

    # Save in multiple formats
    os.makedirs("./images", exist_ok=True)

    # For submission (PDF)
    plt.savefig("./images/figure1_publication.pdf", bbox_inches="tight", dpi=300)

    # For review (PNG)
    plt.savefig("./images/figure1_review.png", bbox_inches="tight", dpi=300)

    # For presentations
    plt.savefig("./images/figure1_presentation.png", bbox_inches="tight", dpi=144)

    print("Publication-ready multi-panel figure created:")
    print("   - Four complementary panels (A-D)")
    print("   - Consistent color scheme throughout")
    print("   - Statistical annotations")
    print("   - Bootstrap confidence intervals")
    print("   - Complete figure caption")

    print("   - Saved in PDF (submission) and PNG (review) formats")

    # Return figure for inline display
    return plt.gcf(),
```
</code>
<power_user_tip>
For multi-panel figures: Use GridSpec for precise control, maintain consistent aesthetics across panels, label panels with letters (A, B, C...), and include a comprehensive caption that explains each panel.
</power_user_tip>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Missing uncertainty visualization (no error bars/CI)</what>
  <consequence>Readers cannot distinguish signal from noise, overconfident interpretations</consequence>
  <prevention>ALWAYS add error bars, confidence bands, or prediction intervals to estimates</prevention>
</mistake>

<mistake severity="critical">
  <what>Unlabeled or partially labeled axes</what>
  <consequence>Misinterpretation of scale, units, or variables being plotted</consequence>
  <prevention>Label BOTH axes with variable name AND units in parentheses</prevention>
</mistake>

<mistake severity="critical">
  <what>Using red-green color schemes</what>
  <consequence>Invisible to 8% of male readers with color blindness</consequence>
  <prevention>Use colorblind-safe palettes (blue-orange, purple-green), test with simulator</prevention>
</mistake>

<mistake severity="high">
  <what>Truncating y-axis to exaggerate differences</what>
  <consequence>Misleading visual impression, ethical violation, desk rejection</consequence>
  <prevention>Start bar charts at zero, clearly mark and justify any truncation</prevention>
</mistake>

<mistake severity="high">
  <what>Low resolution figures (< 144 DPI)</what>
  <consequence>Journal desk rejection, pixelated presentations</consequence>
  <prevention>Save at 144 DPI minimum for screens, 300 DPI for print, vector for publication</prevention>
</mistake>

<mistake severity="critical">
  <what>Using plt.show() instead of returning figure objects</what>
  <consequence>Figures don't display in notebooks, code execution blocked, figures cannot be saved or manipulated programmatically, breaks notebook workflow</consequence>
  <prevention>ALWAYS return figure object (fig, plt.gcf(), or plt.gca()) as the last expression. Notebooks automatically display the last expression. Never use plt.show()</prevention>
</mistake>

<mistake severity="medium">
  <what>Overcrowded plots with too many series</what>
  <consequence>Impossible to distinguish patterns, cognitive overload</consequence>
  <prevention>Limit to 5-7 series maximum, use facets or multiple panels for more</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<choosing_plot_type>
**Distribution**: Histogram + KDE, box plot, violin plot
**Comparison**: Grouped bar chart, dot plot with CI, paired slopes
**Relationship**: Scatter with regression line, hexbin for large n
**Time series**: Line plot with markers, area chart for cumulative
**Proportions**: Stacked bar (NOT pie charts)
**Uncertainty**: Forest plot, coefficient plot, funnel plot
</choosing_plot_type>

<accessibility_checklist>
□ Colorblind-safe palette used
□ Sufficient contrast (WCAG AA standard)
□ Patterns/shapes redundant with color
□ Font size ≥ 10pt
□ Alt text provided for screen readers
□ Grayscale-readable
</accessibility_checklist>

<journal_requirements>
**Nature/Science**: 180mm width, 300 DPI minimum, PDF preferred
**PLOS**: 6.83" width, vector format, CC-BY license notation
**Economics journals**: Often require EPS format, Times font
**Medical journals**: CONSORT flow diagram for RCTs required
</journal_requirements>

<honest_limitations>
- Visualization can mislead even with best practices
- Some patterns only visible in tables (exact values)
- Color alone insufficient for many distinctions
- Static plots miss temporal dynamics
- 2D projection loses multivariate relationships
</honest_limitations>

</interpretation_guide>

<references>
<paper>Cleveland, W.S. (1985). The Elements of Graphing Data. Foundational principles of statistical graphics.</paper>
<paper>Tufte, E.R. (2001). The Visual Display of Quantitative Information. Classic text on data visualization.</paper>
<paper>Cumming, G., Fidler, F., & Vaux, D.L. (2007). "Error bars in experimental biology." Journal of Cell Biology. Proper uncertainty visualization.</paper>
<paper>Wong, B. (2011). "Points of view: Color blindness." Nature Methods 8(6): 441. Colorblind-safe palette design.</paper>
<paper>Weissgerber, T.L., et al. (2015). "Beyond bar and line graphs." PLOS Biology. Problems with bar charts for continuous data.</paper>
<paper>Huff, D. (1954). How to Lie with Statistics. Common visualization manipulations.</paper>
</references>

</skill_content>