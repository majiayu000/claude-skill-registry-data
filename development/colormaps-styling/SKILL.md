---
name: colormaps-styling
description: Master color management and visual styling with Colorcet. Use this skill when selecting appropriate colormaps, creating accessible and colorblind-friendly visualizations, applying consistent themes, or customizing plot aesthetics with perceptually uniform color palettes.
compatibility: Requires colorcet >= 3.1.0, holoviews >= 1.18.0, panel >= 1.3.0, bokeh >= 3.0.0
---

# Colormaps & Styling Skill

## Overview

Master color management and visual styling with Colorcet and theme customization. This skill covers selecting appropriate colormaps, creating accessible visualizations, and consistent application styling.

## Dependencies

- colorcet >= 3.1.0
- holoviews >= 1.18.0
- panel >= 1.3.0
- bokeh >= 3.0.0

## Core Capabilities

### 1. Colorcet Colormap Selection

Colorcet provides perceptually uniform colormaps designed for scientific visualization:

```python
import colorcet as cc
from colorcet import cm
import holoviews as hv
import pandas as pd

# View available colormaps
print(list(cm.keys()))

# Common perceptually uniform colormaps
# cet_gray - Pure grayscale, good for single-channel data
# cet_blues - Blue sequential scale
# cet_reds - Red sequential scale
# cet_goertzel - Full spectrum, good for data with structure
# cet_cyclic_c1 - Cyclic colormap for angular data
# cet_cyclic_c7 - Alternative cyclic colormap

# Use in visualization
scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=hv.dim('value').norm(),
    cmap=cm['cet_goertzel'],
    colorbar=True
)
```

### 2. Colormap Categories

Colorcet provides organized colormaps by category:

```python
from colorcet import cm

# Sequential colormaps (low to high intensity)
sequential = {
    'gray': cm['cet_gray_r'],
    'blue': cm['cet_blues'],
    'green': cm['cet_greens'],
    'orange': cm['cet_oranges'],
    'red': cm['cet_reds'],
    'fire': cm['cet_fire']
}

# Diverging colormaps (opposite ends emphasize)
diverging = {
    'bwy': cm['cet_bwy'],
    'gwv': cm['cet_gwv'],
    'coolwarm': cm['cet_coolwarm'],
    'cyclic': cm['cet_cyclic_c1']
}

# Categorical colormaps (distinct colors)
categorical = {
    'tab10': cm['cet_c6'],
    'tab20': cc.palette['tab20'],
}

# Cyclic colormaps (angle/circular data)
cyclic = {
    'cyclic_c1': cm['cet_cyclic_c1'],
    'cyclic_c7': cm['cet_cyclic_c7'],
    'cyclic_msp': cm['cet_cyclic_msp']
}
```

### 3. Accessibility and Colorblindness

```python
from colorcet import cm

# Colorblind-friendly palettes
colorblind_safe = {
    'deuteranopia': cm['cet_d4'],      # Red-green colorblind
    'protanopia': cm['cet_p3'],        # Red-green colorblind
    'tritanopia': cm['cet_t10'],       # Blue-yellow colorblind
    'achromatomaly': cm['cet_gray_r']  # Grayscale safe
}

def create_accessible_plot(data, value_column):
    """Create plot safe for all color vision types"""
    return hv.Scatter(data, 'x', 'y', vdims=[value_column]).opts(
        color=hv.dim(value_column).norm(),
        cmap=cm['cet_gray_r'],  # Grayscale safe for all
        size=hv.dim(value_column).norm(min=50, max=200),  # Use size as backup
        colorbar=True
    )
```

### 4. Custom Color Mapping

```python
import colorcet as cc
from bokeh.models import LinearColorBar

# Create custom color palette
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

# Map to numerical data
scatter = hv.Scatter(data, 'x', 'y', vdims=['category']).opts(
    color=hv.dim('category').categorize({
        'A': '#FF6B6B',
        'B': '#4ECDC4',
        'C': '#45B7D1',
        'D': '#FFA07A',
        'E': '#98D8C8'
    }),
    size=100
)

# Or use Colorcet's categorical palettes
scatter = hv.Scatter(data, 'x', 'y', vdims=['category']).opts(
    color=hv.dim('category').categorize(dict(zip(
        data['category'].unique(),
        cc.palette['category20']
    ))),
    size=100
)
```

### 5. Normalized Color Mapping

```python
import holoviews as hv
import numpy as np

data = pd.DataFrame({
    'x': np.random.randn(1000),
    'y': np.random.randn(1000),
    'value': np.random.exponential(2, 1000)
})

# Linear normalization
scatter_linear = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=hv.dim('value').norm(),
    cmap=cc.palette['rainbow']
)

# Log normalization for exponential data
scatter_log = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=hv.transform.log1p('value').norm(),
    cmap=cc.palette['rainbow']
)

# Histogram equalization
from sklearn.preprocessing import PowerTransformer
power_transform = PowerTransformer()
normalized_values = power_transform.fit_transform(data[['value']])

scatter_eq = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=normalized_values,
    cmap=cc.palette['rainbow']
)
```

## HoloViews and Panel Styling

### 1. Global Styling

```python
from holoviews import opts
import colorcet as cc

# Set global defaults
opts.defaults(
    opts.Curve(line_width=2, color='navy'),
    opts.Scatter(size=100, color='red', alpha=0.6),
    opts.Image(cmap=cc.cm['cet_goertzel']),
    opts.Bars(color='teal'),
)

# These apply to all new plots
curve = hv.Curve(data, 'x', 'y')  # Uses navy color
scatter = hv.Scatter(data, 'x', 'y')  # Uses red color
```

### 2. Element-Specific Styling

```python
# Customize individual plot elements
styled_scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    # Sizes and positions
    size=hv.dim('value').norm(min=50, max=500),
    alpha=0.7,

    # Colors
    color=hv.dim('value').norm(),
    cmap=cc.cm['cet_fire'],

    # Interactive styling
    hover_fill_color='yellow',
    selection_fill_color='red',
    selection_fill_alpha=0.3,
    nonselection_fill_alpha=0.1,

    # Tools and interactions
    tools=['hover', 'box_select', 'tap'],
    toolbar='right',

    # Annotations
    title='Styled Scatter Plot',
    xlabel='X Axis Label',
    ylabel='Y Axis Label',

    # Layout
    width=800,
    height=600,
    responsive=True
)
```

### 3. Legend and Colorbar Styling

```python
# Custom legend positioning and styling
overlay = (
    hv.Curve(data1, label='Series 1') *
    hv.Curve(data2, label='Series 2') *
    hv.Curve(data3, label='Series 3')
).opts(
    legend_position='top_left',
    legend_muted_alpha=0.2,  # Muted when legend item clicked
    legend_font_size=12,
    legend_label_text_font_size='12pt'
)

# Colorbar styling
heatmap = hv.Image(data).opts(
    colorbar=True,
    colorbar_position='right',
    colorbar_width=15,
    cmap=cc.cm['cet_fire']
)
```

### 4. Multi-Element Styling

```python
# Create coherent styling across multiple plots
def styled_plot(plot, title, cmap=cc.cm['cet_gray']):
    return plot.opts(
        title=title,
        cmap=cmap,
        width=600,
        height=400,
        responsive=True,
        fontsize=12,
        active_tools=['pan', 'wheel_zoom']
    )

# Create multiple styled plots
plots = [
    styled_plot(hv.Curve(data1), 'Series 1'),
    styled_plot(hv.Curve(data2), 'Series 2'),
    styled_plot(hv.Curve(data3), 'Series 3')
]

layout = hv.Column(*plots)
```

## Panel Theme Customization

### 1. Built-in Themes

```python
import panel as pn

pn.extension('material')  # Material Design theme
# Other themes: 'default', 'bootstrap', 'material'

# Apply theme-specific styling
template = pn.template.MaterialTemplate(
    title='Themed Dashboard',
    header_background='#2E86DE',
    sidebar_width=300,
    main=[plots],
    sidebar=[controls]
)
```

### 2. Custom CSS Styling

```python
import panel as pn

# Custom CSS for elements
styled_widget = pn.widgets.FloatSlider(
    name='Value',
    start=0,
    end=100,
    value=50,
    styles={
        'background': '#F0F0F0',
        'border': '2px solid #2E86DE',
        'padding': '10px',
        'border-radius': '5px'
    }
)

# Custom CSS for entire panel
custom_panel = pn.Column(
    pn.pane.Markdown('# Custom Styled Panel'),
    styled_widget,
    styles={
        'background': '#F9F9F9',
        'padding': '20px',
        'border-left': '5px solid #2E86DE'
    }
)
```

### 3. Dark Mode Support

```python
import panel as pn

pn.extension('material')

template = pn.template.MaterialTemplate(
    title='Dashboard',
    theme='dark',  # or 'light'
    header_background='#1a1a1a',
    header_color='#ffffff',
    # Content adapts to dark theme
    main=[plots]
)

# Or detect system preference
import platform
system_dark = platform.system() == 'Darwin'  # macOS dark mode
```

## Best Practices

### 1. Choose Appropriate Colormaps

```python
# Bad: Jet colormap has poor perceptual uniformity
scatter = hv.Scatter(data, 'x', 'y').opts(cmap='jet')

# Good: Use perceptually uniform colormap
scatter = hv.Scatter(data, 'x', 'y').opts(
    cmap=cc.cm['cet_goertzel'],
    color=hv.dim('value').norm()
)
```

### 2. Layer Styling Logically

```python
# Create helper function for consistent styling
class PlotStylist:
    COLORS = {'primary': '#2E86DE', 'secondary': '#A23B72'}
    DEFAULTS = {
        'width': 700,
        'height': 400,
        'responsive': True,
        'toolbar': 'right'
    }

    @staticmethod
    def apply(plot, **kwargs):
        style_dict = {**PlotStylist.DEFAULTS, **kwargs}
        return plot.opts(**style_dict)

styled = PlotStylist.apply(scatter, title='My Plot')
```

### 3. Accessibility First

```python
# Use multiple visual encodings
accessible_scatter = hv.Scatter(data, 'x', 'y', vdims=['category', 'value']).opts(
    # Primary: Color with accessibility in mind
    color=hv.dim('category').categorize({
        'A': '#1b9e77',
        'B': '#d95f02',
        'C': '#7570b3'
    }),
    # Backup: Size encodes value
    size=hv.dim('value').norm(min=100, max=300),
    # Backup: Shape (if using multiple marker types)
    # Pattern: Different patterns for patterns
    # Label: Include legend
    legend_position='top_left'
)
```

### 4. Color Consistency

```python
# Define palette once, use everywhere
BRAND_COLORS = {
    'primary': '#2E86DE',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#D62839',
    'error': '#9B2226'
}

# Use in all visualizations
def create_branded_plot(data, success_column):
    return hv.Scatter(data, 'x', 'y', vdims=[success_column]).opts(
        color=hv.dim(success_column).categorize({
            True: BRAND_COLORS['success'],
            False: BRAND_COLORS['error']
        }),
        cmap=cc.cm['cet_gray_r']  # For continuous data
    )
```

## Common Patterns

### Pattern 1: Sequential Color Scale
```python
def create_heatmap_with_scale(data, value_col):
    return hv.HeatMap(data).opts(
        cmap=cc.cm['cet_fire'],
        colorbar=True,
        color=hv.dim(value_col).norm()
    )
```

### Pattern 2: Category Color Mapping
```python
def categorize_colors(data, category_col, palette='tab10'):
    categories = data[category_col].unique()
    color_map = dict(zip(categories, cc.palette[palette][:len(categories)]))

    return hv.Scatter(data, vdims=[category_col]).opts(
        color=hv.dim(category_col).categorize(color_map),
        legend_position='top_left'
    )
```

### Pattern 3: Diverging Scale for Anomalies
```python
def create_anomaly_plot(data, value_col):
    # Center scale around 0
    return hv.HeatMap(data).opts(
        cmap=cc.cm['cet_bwy'],  # Blue-white-red diverging
        clim=(-data[value_col].abs().max(), data[value_col].abs().max()),
        colorbar=True
    )
```

## Integration with Other HoloViz Tools

- **HoloViews**: Core styling system
- **Panel**: Theme and CSS customization
- **hvPlot**: Colormap support in quick plots
- **Datashader**: Colormap application in rasterized plots
- **GeoViews**: Geographic-specific colormaps

## Common Use Cases

1. **Scientific Visualization**: Publication-quality color choices
2. **Business Dashboards**: Brand-aligned color schemes
3. **Accessibility**: Colorblind-friendly visualizations
4. **Data Exploration**: Multi-scale colormaps
5. **Report Generation**: Consistent visual identity
6. **Interactive Applications**: Theme switching

## Troubleshooting

### Issue: Colors Don't Match Between Plots
- Define color palette once, reference consistently
- Verify colormap normalization is identical
- Check color categories are complete

### Issue: Visualization Hard to Read
- Increase contrast with darker/lighter colors
- Use size or pattern as backup to color
- Check against colorblind vision simulator

### Issue: Colors Look Different on Different Devices
- Use perceptually uniform colormaps
- Test on multiple screens
- Provide PDF export for print-safe colors

## Resources

- [Colorcet Documentation](https://colorcet.holoviz.org)
- [Colorcet Gallery](https://colorcet.holoviz.org/user_guide/index.html)
- [HoloViews Styling](https://holoviews.org/user_guide/Styling_Plots.html)
- [Colorblind Accessibility](https://www.color-blindness.com)
- [Bokeh Color Customization](https://docs.bokeh.org/en/latest/docs/reference/colors.html)
