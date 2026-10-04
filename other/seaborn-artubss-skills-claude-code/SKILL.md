---
name: seaborn
description: "Visualização estatística. Gráficos de dispersão, boxplots, violins, mapas de calor, matriz de pares, regressão, matrizes de correlação, KDE, gráficos facetados, para análise exploratória e figuras para publicação."
---

# Seaborn Visualização Estatística

## Visão Geral

Seaborn é uma biblioteca Python para criar gráficos estatísticos de qualidade para publicação. Use essa skill para plotagem orientada a dataset, análise multivariada, estimação estatística automática e figuras complexas em múltiplos painéis com código mínimo.

## Filosofia de Design

Seaborn segue esses princípios fundamentais:

1. **Orientada a dataset**: Trabalhe diretamente com DataFrames e variáveis nomeadas em vez de coordenadas abstratas
2. **Mapeamento semântico**: Traduzir automaticamente valores de dados em propriedades visuais (cores, tamanhos, estilos)
3. **Consciente estatisticamente**: Agregação integrada, estimação de erros e intervalos de confiança
4. **Padrões estéticos**: Temas prontos para publicação e paletas de cores pronta para uso
5. **Integração com matplotlib**: Compatibilidade total com customização matplotlib quando necessário

## Início Rápido

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Carregar dataset de exemplo
df = sns.load_dataset('tips')

# Criar uma visualização simples
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## Interfaces Principais de Plotagem

### Interface de Função (Tradicional)

A interface de função fornece funções de plotagem especializadas organizadas por tipo de visualização. Cada categoria tem funções **em nível de eixo** (plotam em um único eixo) e funções **em nível de figura** (gerenciam a figura inteira com faceting).

**Quando usar:**
- Análise exploratória rápida
- Visualizações com um único propósito
- Quando você precisa de um tipo de gráfico específico

### Interface de Objetos (Moderna)

A interface `seaborn.objects` fornece uma API declarativa e composável semelhante a ggplot2. Construa visualizações encadeando métodos para especificar mapeamentos de dados, marcadores, transformações e escalas.

**Quando usar:**
- Visualizações em camadas complexas
- Quando você precisa de controle fino sobre transformações
- Criar tipos de gráficos personalizados
- Geração programática de gráficos

```python
from seaborn import objects as so

# Sintaxe declarativa
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)
```

## Funções de Plotagem por Categoria

### Gráficos de Relação (Relacionamento Entre Variáveis)

**Use para:** Explorar como duas ou mais variáveis se relacionam

- `scatterplot()` - Exibir observações individuais como pontos
- `lineplot()` - Mostrar tendências e mudanças (agrega automaticamente e calcula IC)
- `relplot()` - Interface em nível de figura com faceting automático

**Parâmetros principais:**
- `x`, `y` - Variáveis primárias
- `hue` - Codificação de cor para variável categórica/contínua adicional
- `size` - Codificação de tamanho de ponto/linha
- `style` - Codificação de estilo de marcador/linha
- `col`, `row` - Facet em múltiplos subgráficos (somente nível de figura)

```python
# Dispersão com múltiplos mapeamentos semânticos
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time', size='size', style='sex')

# Gráfico de linhas com intervalos de confiança
sns.lineplot(data=timeseries, x='date', y='value', hue='category')

# Gráfico de relação facetado
sns.relplot(data=df, x='total_bill', y='tip',
            col='time', row='sex', hue='smoker', kind='scatter')
```

### Gráficos de Distribuição (Distribuições Univariadas e Bivariadas)

**Use para:** Entender dispersão, forma e densidade de probabilidade dos dados

- `histplot()` - Distribuições de frequência baseadas em barras com binagem flexível
- `kdeplot()` - Estimativas de densidade suave usando kernels gaussianos
- `ecdfplot()` - Distribuição cumulativa empírica (sem parâmetros para sintonizar)
- `rugplot()` - Marcas de tick para observações individuais
- `displot()` - Interface em nível de figura para distribuições univariadas e bivariadas
- `jointplot()` - Gráfico bivariado com distribuições marginais
- `pairplot()` - Matriz de relacionamentos aos pares em todo o dataset

**Parâmetros principais:**
- `x`, `y` - Variáveis (y opcional para univariado)
- `hue` - Separar distribuições por categoria
- `stat` - Normalização: "count", "frequency", "probability", "density"
- `bins` / `binwidth` - Controle de binagem do histograma
- `bw_adjust` - Multiplicador de largura de banda KDE (maior = mais suave)
- `fill` - Preencher área sob a curva
- `multiple` - Como lidar com hue: "layer", "stack", "dodge", "fill"

```python
# Histograma com normalização de densidade
sns.histplot(data=df, x='total_bill', hue='time',
             stat='density', multiple='stack')

# KDE bivariado com contornos
sns.kdeplot(data=df, x='total_bill', y='tip',
            fill=True, levels=5, thresh=0.1)

# Gráfico conjunto com marginais
sns.jointplot(data=df, x='total_bill', y='tip',
              kind='scatter', hue='time')

# Relacionamentos aos pares
sns.pairplot(data=df, hue='species', corner=True)
```

### Gráficos Categóricos (Comparações Através de Categorias)

**Use para:** Comparar distribuições ou estatísticas entre categorias discretas

**Gráficos categóricos de dispersão:**
- `stripplot()` - Pontos com jitter para mostrar todas as observações
- `swarmplot()` - Pontos não sobrepostos (algoritmo beeswarm)

**Comparações de distribuição:**
- `boxplot()` - Quartis e outliers
- `violinplot()` - KDE + informação de quartil
- `boxenplot()` - Boxplot aprimorado para datasets maiores

**Estimativas estatísticas:**
- `barplot()` - Média/agregado com intervalos de confiança
- `pointplot()` - Estimativas pontuais com linhas conectoras
- `countplot()` - Contagem de observações por categoria

**Em nível de figura:**
- `catplot()` - Gráficos categóricos facetados (defina o parâmetro `kind`)

**Parâmetros principais:**
- `x`, `y` - Variáveis (uma tipicamente categórica)
- `hue` - Agrupamento categórico adicional
- `order`, `hue_order` - Controlar ordem de categorias
- `dodge` - Separar níveis de hue lado a lado
- `orient` - "v" (vertical) ou "h" (horizontal)
- `kind` - Tipo de gráfico para catplot: "strip", "swarm", "box", "violin", "bar", "point"

```python
# Gráfico swarm mostrando todos os pontos
sns.swarmplot(data=df, x='day', y='total_bill', hue='sex')

# Gráfico violin com split para comparação
sns.violinplot(data=df, x='day', y='total_bill',
               hue='sex', split=True)

# Gráfico de barras com barras de erro
sns.barplot(data=df, x='day', y='total_bill',
            hue='sex', estimator='mean', errorbar='ci')

# Gráfico categórico facetado
sns.catplot(data=df, x='day', y='total_bill',
            col='time', kind='box')
```

### Gráficos de Regressão (Relacionamentos Lineares)

**Use para:** Visualizar regressões lineares e resíduos

- `regplot()` - Gráfico de regressão em nível de eixo com dispersão + linha ajustada
- `lmplot()` - Nível de figura com suporte a faceting
- `residplot()` - Gráfico de resíduos para avaliar ajuste do modelo

**Parâmetros principais:**
- `x`, `y` - Variáveis para regressão
- `order` - Ordem de regressão polinomial
- `logistic` - Ajustar regressão logística
- `robust` - Usar regressão robusta (menos sensível a outliers)
- `ci` - Largura do intervalo de confiança (padrão 95)
- `scatter_kws`, `line_kws` - Customizar propriedades de dispersão e linha

```python
# Regressão linear simples
sns.regplot(data=df, x='total_bill', y='tip')

# Regressão polinomial com faceting
sns.lmplot(data=df, x='total_bill', y='tip',
           col='time', order=2, ci=95)

# Verificar resíduos
sns.residplot(data=df, x='total_bill', y='tip')
```

### Gráficos de Matriz (Dados Retangulares)

**Use para:** Visualizar matrizes, correlações e dados estruturados em grade

- `heatmap()` - Matriz codificada por cor com anotações
- `clustermap()` - Mapa de calor agrupado hierarquicamente

**Parâmetros principais:**
- `data` - Dataset retangular bidimensional (DataFrame ou array)
- `annot` - Exibir valores nas células
- `fmt` - String de formato para anotações (ex: ".2f")
- `cmap` - Nome do colormap
- `center` - Valor no centro do colormap (para colormaps divergentes)
- `vmin`, `vmax` - Limites da escala de cor
- `square` - Forçar células quadradas
- `linewidths` - Espaço entre células

```python
# Mapa de calor de correlação
corr = df.corr()
sns.heatmap(corr, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True)

# Mapa de calor agrupado
sns.clustermap(data, cmap='viridis',
               standard_scale=1, figsize=(10, 10))
```

## Grids Multi-Plot

Seaborn fornece objetos grid para criar figuras complexas em múltiplos painéis:

### FacetGrid

Criar subgráficos baseados em variáveis categóricas. Mais útil quando chamado através de funções em nível de figura (`relplot`, `displot`, `catplot`), mas pode ser usado diretamente para gráficos personalizados.

```python
g = sns.FacetGrid(df, col='time', row='sex', hue='smoker')
g.map(sns.scatterplot, 'total_bill', 'tip')
g.add_legend()
```

### PairGrid

Mostrar relacionamentos aos pares entre todas as variáveis em um dataset.

```python
g = sns.PairGrid(df, hue='species')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)
g.add_legend()
```

### JointGrid

Combinar gráfico bivariado com distribuições marginais.

```python
g = sns.JointGrid(data=df, x='total_bill', y='tip')
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.histplot)
```

## Funções em Nível de Figura vs Nível de Eixo

Entender essa distinção é crucial para uso efetivo de seaborn:

### Funções em Nível de Eixo
- Plotar em um único objeto `Axes` matplotlib
- Integram-se facilmente em figuras matplotlib complexas
- Aceitam parâmetro `ax=` para posicionamento preciso
- Retornam objeto `Axes`
- Exemplos: `scatterplot`, `histplot`, `boxplot`, `regplot`, `heatmap`

**Quando usar:**
- Construir layouts customizados multi-plot
- Combinar diferentes tipos de gráficos
- Precisar de controle em nível matplotlib
- Integrar com código matplotlib existente

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='x', ax=axes[0, 1])
sns.boxplot(data=df, x='cat', y='y', ax=axes[1, 0])
sns.kdeplot(data=df, x='x', y='y', ax=axes[1, 1])
```

### Funções em Nível de Figura
- Gerenciar figura inteira incluindo todos os subgráficos
- Faceting integrado via parâmetros `col` e `row`
- Retornar objetos `FacetGrid`, `JointGrid` ou `PairGrid`
- Usar `height` e `aspect` para tamanho (por subgráfico)
- Não podem ser colocadas em figura existente
- Exemplos: `relplot`, `displot`, `catplot`, `lmplot`, `jointplot`, `pairplot`

**Quando usar:**
- Visualizações facetadas (múltiplos pequenos)
- Análise exploratória rápida
- Layouts multi-painel consistentes
- Não precisa combinar com outros tipos de gráficos

```python
# Faceting automático
sns.relplot(data=df, x='x', y='y', col='category', row='group',
            hue='type', height=3, aspect=1.2)
```

## Requisitos de Estrutura de Dados

### Dados em Forma Longa (Preferido)

Cada variável é uma coluna, cada observação é uma linha. Esse formato "tidy" fornece máxima flexibilidade:

```python
# Estrutura de forma longa
   subject  condition  measurement
0        1    control         10.5
1        1  treatment         12.3
2        2    control          9.8
3        2  treatment         13.1
```

**Vantagens:**
- Funciona com todas as funções seaborn
- Fácil remapear variáveis para propriedades visuais
- Suporta complexidade arbitrária
- Natural para operações DataFrame

### Dados em Forma Larga

Variáveis espalhadas por colunas. Útil para dados retangulares simples:

```python
# Estrutura de forma larga
   control  treatment
0     10.5       12.3
1      9.8       13.1
```

**Casos de uso:**
- Série temporal simples
- Matrizes de correlação
- Mapas de calor
- Gráficos rápidos de dados de array

**Convertendo forma larga para longa:**
```python
df_long = df.melt(var_name='condition', value_name='measurement')
```

## Paletas de Cores

Seaborn fornece paletas de cores cuidadosamente projetadas para diferentes tipos de dados:

### Paletas Qualitativas (Dados Categóricos)

Distinguir categorias através de variação de matiz:
- `"deep"` - Padrão, cores vívidas
- `"muted"` - Mais suave, menos saturado
- `"pastel"` - Claro, dessaturado
- `"bright"` - Altamente saturado
- `"dark"` - Valores escuros
- `"colorblind"` - Seguro para deficiência de visão de cores

```python
sns.set_palette("colorblind")
sns.color_palette("Set2")
```

### Paletas Sequenciais (Dados Ordenados)

Mostrar progressão de valores baixos para altos:
- `"rocket"`, `"mako"` - Ampla gama de luminância (bom para mapas de calor)
- `"flare"`, `"crest"` - Luminância restrita (bom para pontos/linhas)
- `"viridis"`, `"magma"`, `"plasma"` - Uniforme perceptualmente do matplotlib

```python
sns.heatmap(data, cmap='rocket')
sns.kdeplot(data=df, x='x', y='y', cmap='mako', fill=True)
```

### Paletas Divergentes (Dados Centrados)

Enfatizar desvios de um ponto médio:
- `"vlag"` - Azul para vermelho
- `"icefire"` - Azul para laranja
- `"coolwarm"` - Frio para quente
- `"Spectral"` - Arco-íris divergente

```python
sns.heatmap(correlation_matrix, cmap='vlag', center=0)
```

### Paletas Personalizadas

```python
# Criar paleta personalizada
custom = sns.color_palette("husl", 8)

# Gradiente claro para escuro
palette = sns.light_palette("seagreen", as_cmap=True)

# Paleta divergente de matizes
palette = sns.diverging_palette(250, 10, as_cmap=True)
```

## Temas e Estética

### Definir Tema

`set_theme()` controla a aparência geral:

```python
# Definir tema completo
sns.set_theme(style='whitegrid', palette='pastel', font='sans-serif')

# Redefinir para padrões
sns.set_theme()
```

### Estilos

Controlar fundo e aparência da grade:
- `"darkgrid"` - Fundo cinza com grade branca (padrão)
- `"whitegrid"` - Fundo branco com grade cinza
- `"dark"` - Fundo cinza, sem grade
- `"white"` - Fundo branco, sem grade
- `"ticks"` - Fundo branco com marcas de eixo

```python
sns.set_style("whitegrid")

# Remover espinhas
sns.despine(left=False, bottom=False, offset=10, trim=True)

# Estilo temporário
with sns.axes_style("white"):
    sns.scatterplot(data=df, x='x', y='y')
```

### Contextos

Escalar elementos para diferentes casos de uso:
- `"paper"` - Menor (padrão)
- `"notebook"` - Ligeiramente maior
- `"talk"` - Slides de apresentação
- `"poster"` - Grande formato

```python
sns.set_context("talk", font_scale=1.2)

# Contexto temporário
with sns.plotting_context("poster"):
    sns.barplot(data=df, x='category', y='value')
```

## Melhores Práticas

### 1. Preparação de Dados

Sempre use DataFrames bem estruturados com nomes de coluna significativos:

```python
# Bom: Colunas nomeadas em DataFrame
df = pd.DataFrame({'bill': bills, 'tip': tips, 'day': days})
sns.scatterplot(data=df, x='bill', y='tip', hue='day')

# Evitar: Arrays sem nome
sns.scatterplot(x=x_array, y=y_array)  # Perde rótulos de eixo
```

### 2. Escolha o Tipo de Gráfico Certo

**Contínuo x, contínuo y:** `scatterplot`, `lineplot`, `kdeplot`, `regplot`
**Contínuo x, categórico y:** `violinplot`, `boxplot`, `stripplot`, `swarmplot`
**Uma variável contínua:** `histplot`, `kdeplot`, `ecdfplot`
**Correlações/matrizes:** `heatmap`, `clustermap`
**Relacionamentos aos pares:** `pairplot`, `jointplot`

### 3. Use Funções em Nível de Figura para Faceting

```python
# Em vez de criação manual de subgráficos
sns.relplot(data=df, x='x', y='y', col='category', col_wrap=3)

# Não: Criar subgráficos manualmente para faceting simples
```

### 4. Aproveite Mapeamentos Semânticos

Use `hue`, `size` e `style` para codificar dimensões adicionais:

```python
sns.scatterplot(data=df, x='x', y='y',
                hue='category',      # Cor por categoria
                size='importance',    # Tamanho por variável contínua
                style='type')         # Estilo de marcador por tipo
```

### 5. Controle Estimação Estatística

Muitas funções calculam estatísticas automaticamente. Entenda e customize:

```python
# Lineplot calcula média e IC de 95% por padrão
sns.lineplot(data=df, x='time', y='value',
             errorbar='sd')  # Usar desvio padrão em vez disso

# Barplot calcula média por padrão
sns.barplot(data=df, x='category', y='value',
            estimator='median',  # Usar mediana em vez disso
            errorbar=('ci', 95))  # IC com bootstrap
```

### 6. Combine com Matplotlib

Seaborn integra-se perfeitamente com matplotlib para ajuste fino:

```python
ax = sns.scatterplot(data=df, x='x', y='y')
ax.set(xlabel='Rótulo X Personalizado', ylabel='Rótulo Y Personalizado',
       title='Título Personalizado')
ax.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
```

### 7. Salve Figuras de Alta Qualidade

```python
fig = sns.relplot(data=df, x='x', y='y', col='group')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.pdf')  # Formato vetorial para publicações
```

## Padrões Comuns

### Análise Exploratória de Dados

```python
# Visão geral rápida de todos os relacionamentos
sns.pairplot(data=df, hue='target', corner=True)

# Exploração de distribuição
sns.displot(data=df, x='variable', hue='group',
            kind='kde', fill=True, col='category')

# Análise de correlação
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
```

### Figuras de Qualidade para Publicação

```python
sns.set_theme(style='ticks', context='paper', font_scale=1.1)

g = sns.catplot(data=df, x='treatment', y='response',
                col='cell_line', kind='box', height=3, aspect=1.2)
g.set_axis_labels('Condição de Tratamento', 'Resposta (μM)')
g.set_titles('{col_name}')
sns.despine(trim=True)

g.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### Figuras Complexas em Múltiplos Painéis

```python
# Usando subplots matplotlib com seaborn
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.scatterplot(data=df, x='x1', y='y', hue='group', ax=axes[0, 0])
sns.histplot(data=df, x='x1', hue='group', ax=axes[0, 1])
sns.violinplot(data=df, x='group', y='y', ax=axes[1, 0])
sns.heatmap(df.pivot_table(values='y', index='x1', columns='x2'),
            ax=axes[1, 1], cmap='viridis')

plt.tight_layout()
```

### Série Temporal com Bandas de Confiança

```python
# Lineplot agrega automaticamente e mostra IC
sns.lineplot(data=timeseries, x='date', y='measurement',
             hue='sensor', style='location', errorbar='sd')

# Para mais controle
g = sns.relplot(data=timeseries, x='date', y='measurement',
                col='location', hue='sensor', kind='line',
                height=4, aspect=1.5, errorbar=('ci', 95))
g.set_axis_labels('Data', 'Medição (unidades)')
```

## Solução de Problemas

### Problema: Legenda Fora da Área do Gráfico

Funções em nível de figura colocam legendas fora por padrão. Para mover para dentro:

```python
g = sns.relplot(data=df, x='x', y='y', hue='category')
g._legend.set_bbox_to_anchor((0.9, 0.5))  # Ajuste posição
```

### Problema: Rótulos Sobrepostos

```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

### Problema: Figura Muito Pequena

Para funções em nível de figura:
```python
sns.relplot(data=df, x='x', y='y', height=6, aspect=1.5)
```

Para funções em nível de eixo:
```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='x', y='y', ax=ax)
```

### Problema: Cores Não Suficientemente Distintas

```python
# Usar paleta diferente
sns.set_palette("bright")

# Ou especificar número de cores
palette = sns.color_palette("husl", n_colors=len(df['category'].unique()))
sns.scatterplot(data=df, x='x', y='y', hue='category', palette=palette)
```

### Problema: KDE Muito Suave ou Áspero

```python
# Ajuste largura de banda
sns.kdeplot(data=df, x='x', bw_adjust=0.5)  # Menos suave
sns.kdeplot(data=df, x='x', bw_adjust=2)    # Mais suave
```

## Recursos

Esta skill inclui materiais de referência para exploração mais aprofundada:

### references/

- `function_reference.md` - Listagem abrangente de todas as funções seaborn com parâmetros e exemplos
- `objects_interface.md` - Guia detalhado da API moderna seaborn.objects
- `examples.md` - Casos de uso comuns e padrões de código para diferentes cenários de análise

Carregue arquivos de referência conforme necessário para assinaturas de função detalhadas, parâmetros avançados ou exemplos específicos.