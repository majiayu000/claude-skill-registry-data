---
name: plotly
description: Biblioteca interativa de visualização de dados científicos e estatísticos para Python. Use ao criar gráficos, plots ou visualizações incluindo scatter plots, gráficos de linhas, gráficos de barras, heatmaps, plots 3D, mapas geográficos, distribuições estatísticas, gráficos financeiros e dashboards. Suporta visualizações rápidas (Plotly Express) e personalização refinada (graph objects). Gera HTML interativo ou imagens estáticas (PNG, PDF, SVG).
---

# Plotly

Biblioteca gráfica Python para criar visualizações interativas de qualidade para publicação com mais de 40 tipos de gráficos.

## Início Rápido

Instale Plotly:
```bash
uv pip install plotly
```

Uso básico com Plotly Express (API de alto nível):
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='My First Plot')
fig.show()
```

## Escolhendo Entre APIs

### Use Plotly Express (px)
Para visualizações rápidas e padrão com padrões sensatos:
- Trabalhando com DataFrames do pandas
- Criando tipos de gráficos comuns (scatter, line, bar, histogram, etc.)
- Precisando de codificação automática de cores e legendas
- Desejando código mínimo (1-5 linhas)

Veja [reference/plotly-express.md](reference/plotly-express.md) para o guia completo.

### Use Graph Objects (go)
Para controle refinado e visualizações customizadas:
- Tipos de gráficos não disponíveis em Plotly Express (mesh 3D, isosurface, gráficos financeiros complexos)
- Construindo figuras multi-trace complexas do zero
- Precisando de controle preciso sobre componentes individuais
- Criando visualizações especializadas com formas e anotações customizadas

Veja [reference/graph-objects.md](reference/graph-objects.md) para o guia completo.

**Nota:** Plotly Express retorna um Figure de graph objects, então você pode combinar as abordagens:
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='Custom Title')  # Use métodos go em figura px
fig.add_hline(y=10)                     # Adicione formas
```

## Capacidades Principais

### 1. Tipos de Gráficos

Plotly suporta mais de 40 tipos de gráficos organizados em categorias:

**Gráficos Básicos:** scatter, line, bar, pie, area, bubble

**Gráficos Estatísticos:** histogram, box plot, violin, distribution, error bars

**Gráficos Científicos:** heatmap, contour, ternary, image display

**Gráficos Financeiros:** candlestick, OHLC, waterfall, funnel, time series

**Mapas:** scatter maps, choropleth, density maps (visualização geográfica)

**Gráficos 3D:** scatter3d, surface, mesh, cone, volume

**Especializados:** sunburst, treemap, sankey, parallel coordinates, gauge

Para exemplos detalhados e uso de todos os tipos de gráficos, veja [reference/chart-types.md](reference/chart-types.md).

### 2. Layouts e Estilo

**Subplots:** Crie figuras multi-plot com eixos compartilhados:
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**Templates:** Aplique estilo coordenado:
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# Built-in: plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**Personalização:** Controle cada aspecto da aparência:
- Cores (sequências discretas, escalas contínuas)
- Fontes e texto
- Eixos (intervalos, ticks, grids)
- Legendas
- Margens e tamanho
- Anotações e formas

Para opções completas de layout e estilo, veja [reference/layouts-styling.md](reference/layouts-styling.md).

### 3. Interatividade

Recursos interativos integrados:
- Tooltips hover com dados customizáveis
- Pan e zoom
- Alternância de legenda
- Seleção por caixa/lasso
- Rangesliders para séries temporais
- Botões e dropdowns
- Animações

```python
# Template hover customizado
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)

# Adicione rangeslider
fig.update_xaxes(rangeslider_visible=True)

# Animações
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

Para guia completo de interatividade, veja [reference/export-interactivity.md](reference/export-interactivity.md).

### 4. Opções de Exportação

**HTML Interativo:**
```python
fig.write_html('chart.html')                       # Totalmente independente
fig.write_html('chart.html', include_plotlyjs='cdn')  # Arquivo menor
```

**Imagens Estáticas (requer kaleido):**
```bash
uv pip install kaleido
```

```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

Para opções completas de exportação, veja [reference/export-interactivity.md](reference/export-interactivity.md).

## Workflows Comuns

### Visualização de Dados Científicos

```python
import plotly.express as px

# Scatter plot com linha de tendência
fig = px.scatter(df, x='temperature', y='yield', trendline='ols')

# Heatmap de matriz
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# Plot de superfície 3D
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### Análise Estatística

```python
# Comparação de distribuição
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# Box plot com todos os pontos
fig = px.box(df, x='category', y='value', points='all')

# Violin plot
fig = px.violin(df, x='group', y='measurement', box=True)
```

### Séries Temporais e Financeiro

```python
# Série temporal com rangeslider
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# Gráfico candlestick
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### Dashboards Multi-Plot

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Scatter', 'Bar', 'Histogram', 'Box'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## Integração com Dash

Para aplicações web interativas, use Dash (framework de web app do Plotly):

```bash
uv pip install dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('Dashboard'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## Arquivos de Referência

- **[plotly-express.md](reference/plotly-express.md)** - API de alto nível para visualizações rápidas
- **[graph-objects.md](reference/graph-objects.md)** - API de baixo nível para controle refinado
- **[chart-types.md](reference/chart-types.md)** - Catálogo completo de mais de 40 tipos de gráficos com exemplos
- **[layouts-styling.md](reference/layouts-styling.md)** - Subplots, templates, cores, personalização
- **[export-interactivity.md](reference/export-interactivity.md)** - Opções de exportação e recursos interativos

## Recursos Adicionais

- Documentação oficial: https://plotly.com/python/
- Referência de API: https://plotly.com/python-api-reference/
- Fórum da comunidade: https://community.plotly.com/