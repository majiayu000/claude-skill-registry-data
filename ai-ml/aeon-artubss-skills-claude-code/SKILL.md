---
name: aeon
description: Esta skill deve ser usada para tarefas de machine learning em séries temporais, incluindo classificação, regressão, clustering, forecasting, detecção de anomalias, segmentação e busca de similaridade. Use quando trabalhar com dados temporais, padrões sequenciais ou observações indexadas por tempo que requerem algoritmos especializados além de abordagens padrão de ML. Particularmente adequada para análise univariada e multivariada de séries temporais com APIs compatíveis com scikit-learn.
---

# Aeon — Machine Learning para Séries Temporais

## Visão Geral

Aeon é um toolkit Python compatível com scikit-learn para machine learning em séries temporais. Fornece algoritmos estado-da-arte para classificação, regressão, clustering, forecasting, detecção de anomalias, segmentação e busca de similaridade.

## Quando Usar Esta Skill

Aplique esta skill quando:
- Classificar ou prever a partir de dados de séries temporais
- Detectar anomalias ou mudanças de ponto em sequências temporais
- Agrupar padrões semelhantes de séries temporais
- Fazer forecast de valores futuros
- Encontrar padrões repetidos (motifs) ou subsequências incomuns (discords)
- Comparar séries temporais com métricas de distância especializadas
- Extrair features de dados temporais

## Instalação

```bash
uv pip install aeon
```

## Capacidades Principais

### 1. Classificação de Séries Temporais

Categorizar séries temporais em classes predefinidas. Consulte `references/classification.md` para o catálogo completo de algoritmos.

**Início Rápido:**
```python
from aeon.classification.convolution_based import RocketClassifier
from aeon.datasets import load_classification

# Carregar dados
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Treinar classificador
clf = RocketClassifier(n_kernels=10000)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
```

**Seleção de Algoritmo:**
- **Velocidade + Desempenho**: `MiniRocketClassifier`, `Arsenal`
- **Máxima Acurácia**: `HIVECOTEV2`, `InceptionTimeClassifier`
- **Interpretabilidade**: `ShapeletTransformClassifier`, `Catch22Classifier`
- **Datasets Pequenos**: `KNeighborsTimeSeriesClassifier` com distância DTW

### 2. Regressão de Séries Temporais

Prever valores contínuos a partir de séries temporais. Consulte `references/regression.md` para algoritmos.

**Início Rápido:**
```python
from aeon.regression.convolution_based import RocketRegressor
from aeon.datasets import load_regression

X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

reg = RocketRegressor()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

### 3. Clustering de Séries Temporais

Agrupar séries temporais semelhantes sem labels. Consulte `references/clustering.md` para métodos.

**Início Rápido:**
```python
from aeon.clustering import TimeSeriesKMeans

clusterer = TimeSeriesKMeans(
    n_clusters=3,
    distance="dtw",
    averaging_method="ba"
)
labels = clusterer.fit_predict(X_train)
centers = clusterer.cluster_centers_
```

### 4. Forecasting

Prever valores futuros de séries temporais. Consulte `references/forecasting.md` para forecasters.

**Início Rápido:**
```python
from aeon.forecasting.arima import ARIMA

forecaster = ARIMA(order=(1, 1, 1))
forecaster.fit(y_train)
y_pred = forecaster.predict(fh=[1, 2, 3, 4, 5])
```

### 5. Detecção de Anomalias

Identificar padrões incomuns ou outliers. Consulte `references/anomaly_detection.md` para detectores.

**Início Rápido:**
```python
from aeon.anomaly_detection import STOMP

detector = STOMP(window_size=50)
anomaly_scores = detector.fit_predict(y)

# Scores mais altos indicam anomalias
threshold = np.percentile(anomaly_scores, 95)
anomalies = anomaly_scores > threshold
```

### 6. Segmentação

Particionar séries temporais em regiões com mudanças de ponto. Consulte `references/segmentation.md`.

**Início Rápido:**
```python
from aeon.segmentation import ClaSPSegmenter

segmenter = ClaSPSegmenter()
change_points = segmenter.fit_predict(y)
```

### 7. Busca de Similaridade

Encontrar padrões semelhantes dentro ou entre séries temporais. Consulte `references/similarity_search.md`.

**Início Rápido:**
```python
from aeon.similarity_search import StompMotif

# Encontrar padrões recorrentes
motif_finder = StompMotif(window_size=50, k=3)
motifs = motif_finder.fit_predict(y)
```

## Extração de Features e Transformações

Transformar séries temporais para feature engineering. Consulte `references/transformations.md`.

**Features ROCKET:**
```python
from aeon.transformations.collection.convolution_based import RocketTransformer

rocket = RocketTransformer()
X_features = rocket.fit_transform(X_train)

# Use features com qualquer classificador sklearn
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(X_features, y_train)
```

**Features Estatísticas:**
```python
from aeon.transformations.collection.feature_based import Catch22

catch22 = Catch22()
X_features = catch22.fit_transform(X_train)
```

**Pré-processamento:**
```python
from aeon.transformations.collection import MinMaxScaler, Normalizer

scaler = Normalizer()  # Z-normalization
X_normalized = scaler.fit_transform(X_train)
```

## Métricas de Distância

Medidas especializadas de distância temporal. Consulte `references/distances.md` para catálogo completo.

**Uso:**
```python
from aeon.distances import dtw_distance, dtw_pairwise_distance

# Distância única
distance = dtw_distance(x, y, window=0.1)

# Distâncias pairwise
distance_matrix = dtw_pairwise_distance(X_train)

# Use com classificadores
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier

clf = KNeighborsTimeSeriesClassifier(
    n_neighbors=5,
    distance="dtw",
    distance_params={"window": 0.2}
)
```

**Distâncias Disponíveis:**
- **Elásticas**: DTW, DDTW, WDTW, ERP, EDR, LCSS, TWE, MSM
- **Lock-step**: Euclidiana, Manhattan, Minkowski
- **Baseadas em forma**: Shape DTW, SBD

## Redes de Deep Learning

Arquiteturas neurais para séries temporais. Consulte `references/networks.md`.

**Arquiteturas:**
- Convolucional: `FCNClassifier`, `ResNetClassifier`, `InceptionTimeClassifier`
- Recorrente: `RecurrentNetwork`, `TCNNetwork`
- Autoencoders: `AEFCNClusterer`, `AEResNetClusterer`

**Uso:**
```python
from aeon.classification.deep_learning import InceptionTimeClassifier

clf = InceptionTimeClassifier(n_epochs=100, batch_size=32)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

## Datasets e Benchmarking

Carregar benchmarks padrão e avaliar desempenho. Consulte `references/datasets_benchmarking.md`.

**Carregar Datasets:**
```python
from aeon.datasets import load_classification, load_regression

# Classificação
X_train, y_train = load_classification("ArrowHead", split="train")

# Regressão
X_train, y_train = load_regression("Covid3Month", split="train")
```

**Benchmarking:**
```python
from aeon.benchmarking import get_estimator_results

# Comparar com resultados publicados
published = get_estimator_results("ROCKET", "GunPoint")
```

## Workflows Comuns

### Pipeline de Classificação

```python
from aeon.transformations.collection import Normalizer
from aeon.classification.convolution_based import RocketClassifier
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('normalize', Normalizer()),
    ('classify', RocketClassifier())
])

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
```

### Extração de Features + ML Tradicional

```python
from aeon.transformations.collection import RocketTransformer
from sklearn.ensemble import GradientBoostingClassifier

# Extrair features
rocket = RocketTransformer()
X_train_features = rocket.fit_transform(X_train)
X_test_features = rocket.transform(X_test)

# Treinar ML tradicional
clf = GradientBoostingClassifier()
clf.fit(X_train_features, y_train)
predictions = clf.predict(X_test_features)
```

### Detecção de Anomalias com Visualização

```python
from aeon.anomaly_detection import STOMP
import matplotlib.pyplot as plt

detector = STOMP(window_size=50)
scores = detector.fit_predict(y)

plt.figure(figsize=(15, 5))
plt.subplot(2, 1, 1)
plt.plot(y, label='Time Series')
plt.subplot(2, 1, 2)
plt.plot(scores, label='Anomaly Scores', color='red')
plt.axhline(np.percentile(scores, 95), color='k', linestyle='--')
plt.show()
```

## Melhores Práticas

### Preparação de Dados

1. **Normalizar**: A maioria dos algoritmos se beneficia de z-normalization
   ```python
   from aeon.transformations.collection import Normalizer
   normalizer = Normalizer()
   X_train = normalizer.fit_transform(X_train)
   X_test = normalizer.transform(X_test)
   ```

2. **Lidar com Valores Ausentes**: Imputar antes da análise
   ```python
   from aeon.transformations.collection import SimpleImputer
   imputer = SimpleImputer(strategy='mean')
   X_train = imputer.fit_transform(X_train)
   ```

3. **Verificar Formato de Dados**: Aeon espera shape `(n_samples, n_channels, n_timepoints)`

### Seleção de Modelo

1. **Comece Simples**: Começar com variantes ROCKET antes de deep learning
2. **Use Validação**: Dividir dados de treinamento para tuning de hiperparâmetros
3. **Compare Baselines**: Testar contra métodos simples (1-NN Euclidiana, Naive)
4. **Considere Recursos**: ROCKET para velocidade, deep learning se GPU disponível

### Guia de Seleção de Algoritmo

**Para Prototipagem Rápida:**
- Classificação: `MiniRocketClassifier`
- Regressão: `MiniRocketRegressor`
- Clustering: `TimeSeriesKMeans` com Euclidiana

**Para Máxima Acurácia:**
- Classificação: `HIVECOTEV2`, `InceptionTimeClassifier`
- Regressão: `InceptionTimeRegressor`
- Forecasting: `ARIMA`, `TCNForecaster`

**Para Interpretabilidade:**
- Classificação: `ShapeletTransformClassifier`, `Catch22Classifier`
- Features: `Catch22`, `TSFresh`

**Para Datasets Pequenos:**
- Baseado em distância: `KNeighborsTimeSeriesClassifier` com DTW
- Evitar: Deep learning (requer muitos dados)

## Documentação de Referência

Informações detalhadas disponíveis em `references/`:
- `classification.md` - Todos os algoritmos de classificação
- `regression.md` - Métodos de regressão
- `clustering.md` - Algoritmos de clustering
- `forecasting.md` - Abordagens de forecasting
- `anomaly_detection.md` - Métodos de detecção de anomalias
- `segmentation.md` - Algoritmos de segmentação
- `similarity_search.md` - Busca de padrões e descoberta de motifs
- `transformations.md` - Extração de features e pré-processamento
- `distances.md` - Métricas de distância para séries temporais
- `networks.md` - Arquiteturas de deep learning
- `datasets_benchmarking.md` - Ferramentas de carregamento e avaliação de dados

## Recursos Adicionais

- Documentação: https://www.aeon-toolkit.org/
- GitHub: https://github.com/aeon-toolkit/aeon
- Exemplos: https://www.aeon-toolkit.org/en/stable/examples.html
- Referência da API: https://www.aeon-toolkit.org/en/stable/api_reference.html