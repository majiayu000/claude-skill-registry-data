---
name: deepchem
description: "Kit de ferramentas de machine learning molecular. Predição de propriedades (ADMET, toxicidade), GNNs (GCN, MPNN), benchmarks MoleculeNet, modelos pré-treinados, featurização, para ML em descoberta de fármacos."
---

# DeepChem

## Visão Geral

DeepChem é uma biblioteca Python abrangente para aplicar machine learning à química, ciência de materiais e biologia. Habilite predição de propriedades moleculares, descoberta de fármacos, design de materiais e análise de biomoléculas através de redes neurais especializadas, métodos de featurização molecular e modelos pré-treinados.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Carregando e processando dados moleculares (strings SMILES, arquivos SDF, sequências de proteínas)
- Prevendo propriedades moleculares (solubilidade, toxicidade, afinidade de ligação, propriedades ADMET)
- Treinando modelos em conjuntos de dados químicos/biológicos
- Usando conjuntos de dados benchmark MoleculeNet (Tox21, BBBP, Delaney, etc.)
- Convertendo moléculas em features prontas para ML (fingerprints, representações em grafo, descritores)
- Implementando redes neurais convolucionais de grafos para moléculas (GCN, GAT, MPNN, AttentiveFP)
- Aplicando transfer learning com modelos pré-treinados (ChemBERTa, GROVER, MolFormer)
- Prevendo propriedades de cristais/materiais (bandgap, energia de formação)
- Analisando sequências de proteínas ou DNA

## Capacidades Principais

### 1. Carregamento e Processamento de Dados Moleculares

DeepChem fornece loaders especializados para vários formatos de dados químicos:

```python
import deepchem as dc

# Carregar CSV com SMILES
featurizer = dc.feat.CircularFingerprint(radius=2, size=2048)
loader = dc.data.CSVLoader(
    tasks=['solubility', 'toxicity'],
    feature_field='smiles',
    featurizer=featurizer
)
dataset = loader.create_dataset('molecules.csv')

# Carregar arquivos SDF
loader = dc.data.SDFLoader(tasks=['activity'], featurizer=featurizer)
dataset = loader.create_dataset('compounds.sdf')

# Carregar sequências de proteínas
loader = dc.data.FASTALoader()
dataset = loader.create_dataset('proteins.fasta')
```

**Loaders Principais**:
- `CSVLoader`: Dados tabulares com identificadores moleculares
- `SDFLoader`: Arquivos de estrutura molecular
- `FASTALoader`: Sequências de proteínas/DNA
- `ImageLoader`: Imagens moleculares
- `JsonLoader`: Conjuntos de dados em formato JSON

### 2. Featurização Molecular

Converta moléculas em representações numéricas para modelos de ML.

#### Árvore de Decisão para Seleção de Featurizer

```
O modelo é uma rede neural de grafos?
├─ SIM → Use featurizers de grafos
│   ├─ GNN padrão → MolGraphConvFeaturizer
│   ├─ Message passing → DMPNNFeaturizer
│   └─ Pré-treinado → GroverFeaturizer
│
└─ NÃO → Que tipo de modelo?
    ├─ ML tradicional (RF, XGBoost, SVM)
    │   ├─ Baseline rápido → CircularFingerprint (ECFP)
    │   ├─ Interpretável → RDKitDescriptors
    │   └─ Cobertura máxima → MordredDescriptors
    │
    ├─ Deep learning (não-grafo)
    │   ├─ Redes densas → CircularFingerprint
    │   └─ CNN → SmilesToImage
    │
    ├─ Modelos de sequência (LSTM, Transformer)
    │   └─ SmilesToSeq
    │
    └─ Análise de estrutura 3D
        └─ CoulombMatrix
```

#### Exemplo de Featurização

```python
# Fingerprints (para ML tradicional)
fp = dc.feat.CircularFingerprint(radius=2, size=2048)

# Descritores (para modelos interpretáveis)
desc = dc.feat.RDKitDescriptors()

# Features de grafos (para GNNs)
graph_feat = dc.feat.MolGraphConvFeaturizer()

# Aplicar featurização
features = fp.featurize(['CCO', 'c1ccccc1'])
```

**Guia de Seleção**:
- **Conjuntos pequenos (<1K)**: CircularFingerprint ou RDKitDescriptors
- **Conjuntos médios (1K-100K)**: CircularFingerprint ou featurizers de grafos
- **Conjuntos grandes (>100K)**: Featurizers de grafos (MolGraphConvFeaturizer, DMPNNFeaturizer)
- **Transfer learning**: Featurizers de modelos pré-treinados (GroverFeaturizer)

Veja `references/api_reference.md` para documentação completa de featurizers.

### 3. Divisão de Dados

**Crítico**: Para tarefas de descoberta de fármacos, use `ScaffoldSplitter` para evitar data leakage de estruturas moleculares semelhantes aparecendo em conjuntos de treino e teste.

```python
# Divisão por scaffold (recomendado para moléculas)
splitter = dc.splits.ScaffoldSplitter()
train, valid, test = splitter.train_valid_test_split(
    dataset,
    frac_train=0.8,
    frac_valid=0.1,
    frac_test=0.1
)

# Divisão aleatória (para dados não-moleculares)
splitter = dc.splits.RandomSplitter()
train, test = splitter.train_test_split(dataset)

# Divisão estratificada (para classificação desbalanceada)
splitter = dc.splits.RandomStratifiedSplitter()
train, test = splitter.train_test_split(dataset)
```

**Splitters Disponíveis**:
- `ScaffoldSplitter`: Dividir por scaffolds moleculares (previne leakage)
- `ButinaSplitter`: Divisão molecular baseada em clustering
- `MaxMinSplitter`: Maximizar diversidade entre conjuntos
- `RandomSplitter`: Divisão aleatória
- `RandomStratifiedSplitter`: Preserva distribuições de classe

### 4. Seleção de Modelo e Treinamento

#### Guia Rápido de Seleção de Modelo

| Tamanho do Dataset | Tarefa | Modelo Recomendado | Featurizer |
|-------------|------|-------------------|------------|
| < 1K samples | Qualquer | SklearnModel (RandomForest) | CircularFingerprint |
| 1K-100K | Classificação/Regressão | GBDTModel ou MultitaskRegressor | CircularFingerprint |
| > 100K | Propriedades moleculares | GCNModel, AttentiveFPModel, DMPNNModel | MolGraphConvFeaturizer |
| Qualquer (pequeno preferível) | Transfer learning | ChemBERTa, GROVER, MolFormer | Específico do modelo |
| Estruturas cristalinas | Propriedades de materiais | CGCNNModel, MEGNetModel | Baseado em estrutura |
| Sequências de proteínas | Propriedades de proteínas | ProtBERT | Baseado em sequência |

#### Exemplo: ML Tradicional
```python
from sklearn.ensemble import RandomForestRegressor

# Encapsular modelo scikit-learn
sklearn_model = RandomForestRegressor(n_estimators=100)
model = dc.models.SklearnModel(model=sklearn_model)
model.fit(train)
```

#### Exemplo: Deep Learning
```python
# Regressor multitarefa (para fingerprints)
model = dc.models.MultitaskRegressor(
    n_tasks=2,
    n_features=2048,
    layer_sizes=[1000, 500],
    dropouts=0.25,
    learning_rate=0.001
)
model.fit(train, nb_epoch=50)
```

#### Exemplo: Redes Neurais de Grafos
```python
# Graph Convolutional Network
model = dc.models.GCNModel(
    n_tasks=1,
    mode='regression',
    batch_size=128,
    learning_rate=0.001
)
model.fit(train, nb_epoch=50)

# Graph Attention Network
model = dc.models.GATModel(n_tasks=1, mode='classification')
model.fit(train, nb_epoch=50)

# Attentive Fingerprint
model = dc.models.AttentiveFPModel(n_tasks=1, mode='regression')
model.fit(train, nb_epoch=50)
```

### 5. Benchmarks MoleculeNet

Acesso rápido a 30+ conjuntos de dados benchmark curados com divisões treino/validação/teste padronizadas:

```python
# Carregar conjunto de dados benchmark
tasks, datasets, transformers = dc.molnet.load_tox21(
    featurizer='GraphConv',  # ou 'ECFP', 'Weave', 'Raw'
    splitter='scaffold',     # ou 'random', 'stratified'
    reload=False
)
train, valid, test = datasets

# Treinar e avaliar
model = dc.models.GCNModel(n_tasks=len(tasks), mode='classification')
model.fit(train, nb_epoch=50)

metric = dc.metrics.Metric(dc.metrics.roc_auc_score)
test_score = model.evaluate(test, [metric])
```

**Conjuntos de Dados Comuns**:
- **Classificação**: `load_tox21()`, `load_bbbp()`, `load_hiv()`, `load_clintox()`
- **Regressão**: `load_delaney()`, `load_freesolv()`, `load_lipo()`
- **Propriedades quânticas**: `load_qm7()`, `load_qm8()`, `load_qm9()`
- **Materiais**: `load_perovskite()`, `load_bandgap()`, `load_mp_formation_energy()`

Veja `references/api_reference.md` para lista completa de conjuntos de dados.

### 6. Transfer Learning

Aproveite modelos pré-treinados para melhor desempenho, especialmente em conjuntos pequenos:

```python
# ChemBERTa (BERT pré-treinado em 77M moléculas)
model = dc.models.HuggingFaceModel(
    model='seyonec/ChemBERTa-zinc-base-v1',
    task='classification',
    n_tasks=1,
    learning_rate=2e-5  # LR mais baixa para fine-tuning
)
model.fit(train, nb_epoch=10)

# GROVER (transformador de grafos pré-treinado em 10M moléculas)
model = dc.models.GroverModel(
    task='regression',
    n_tasks=1
)
model.fit(train, nb_epoch=20)
```

**Quando usar transfer learning**:
- Conjuntos pequenos (< 1000 samples)
- Scaffolds moleculares novos
- Recursos computacionais limitados
- Necessidade de prototipagem rápida

Use o script `scripts/transfer_learning.py` para workflows de transfer learning guiados.

### 7. Avaliação de Modelo

```python
# Definir métricas
classification_metrics = [
    dc.metrics.Metric(dc.metrics.roc_auc_score, name='ROC-AUC'),
    dc.metrics.Metric(dc.metrics.accuracy_score, name='Accuracy'),
    dc.metrics.Metric(dc.metrics.f1_score, name='F1')
]

regression_metrics = [
    dc.metrics.Metric(dc.metrics.r2_score, name='R²'),
    dc.metrics.Metric(dc.metrics.mean_absolute_error, name='MAE'),
    dc.metrics.Metric(dc.metrics.root_mean_squared_error, name='RMSE')
]

# Avaliar
train_scores = model.evaluate(train, classification_metrics)
test_scores = model.evaluate(test, classification_metrics)
```

### 8. Fazendo Previsões

```python
# Prever no conjunto de teste
predictions = model.predict(test)

# Prever em novas moléculas
new_smiles = ['CCO', 'c1ccccc1', 'CC(C)O']
new_features = featurizer.featurize(new_smiles)
new_dataset = dc.data.NumpyDataset(X=new_features)

# Aplicar mesmas transformações do treinamento
for transformer in transformers:
    new_dataset = transformer.transform(new_dataset)

predictions = model.predict(new_dataset)
```

## Workflows Típicos

### Workflow A: Avaliação Rápida em Benchmark

Para avaliar um modelo em benchmarks padrão:

```python
import deepchem as dc

# 1. Carregar benchmark
tasks, datasets, _ = dc.molnet.load_bbbp(
    featurizer='GraphConv',
    splitter='scaffold'
)
train, valid, test = datasets

# 2. Treinar modelo
model = dc.models.GCNModel(n_tasks=len(tasks), mode='classification')
model.fit(train, nb_epoch=50)

# 3. Avaliar
metric = dc.metrics.Metric(dc.metrics.roc_auc_score)
test_score = model.evaluate(test, [metric])
print(f"Test ROC-AUC: {test_score}")
```

### Workflow B: Previsão com Dados Personalizados

Para treinar em conjuntos de dados moleculares personalizados:

```python
import deepchem as dc

# 1. Carregar e featurizar dados
featurizer = dc.feat.CircularFingerprint(radius=2, size=2048)
loader = dc.data.CSVLoader(
    tasks=['activity'],
    feature_field='smiles',
    featurizer=featurizer
)
dataset = loader.create_dataset('my_molecules.csv')

# 2. Dividir dados (use ScaffoldSplitter para moléculas!)
splitter = dc.splits.ScaffoldSplitter()
train, valid, test = splitter.train_valid_test_split(dataset)

# 3. Normalizar (opcional mas recomendado)
transformers = [dc.trans.NormalizationTransformer(
    transform_y=True, dataset=train
)]
for transformer in transformers:
    train = transformer.transform(train)
    valid = transformer.transform(valid)
    test = transformer.transform(test)

# 4. Treinar modelo
model = dc.models.MultitaskRegressor(
    n_tasks=1,
    n_features=2048,
    layer_sizes=[1000, 500],
    dropouts=0.25
)
model.fit(train, nb_epoch=50)

# 5. Avaliar
metric = dc.metrics.Metric(dc.metrics.r2_score)
test_score = model.evaluate(test, [metric])
```

### Workflow C: Transfer Learning em Pequeno Dataset

Para aproveitar modelos pré-treinados:

```python
import deepchem as dc

# 1. Carregar dados (modelos pré-treinados frequentemente precisam de SMILES bruto)
loader = dc.data.CSVLoader(
    tasks=['activity'],
    feature_field='smiles',
    featurizer=dc.feat.DummyFeaturizer()  # Modelo trata featurização
)
dataset = loader.create_dataset('small_dataset.csv')

# 2. Dividir dados
splitter = dc.splits.ScaffoldSplitter()
train, test = splitter.train_test_split(dataset)

# 3. Carregar modelo pré-treinado
model = dc.models.HuggingFaceModel(
    model='seyonec/ChemBERTa-zinc-base-v1',
    task='classification',
    n_tasks=1,
    learning_rate=2e-5
)

# 4. Fine-tune
model.fit(train, nb_epoch=10)

# 5. Avaliar
predictions = model.predict(test)
```

Veja `references/workflows.md` para 8 exemplos de workflows detalhados cobrindo geração molecular, ciência de materiais, análise de proteínas e mais.

## Scripts de Exemplo

Esta skill inclui três scripts prontos para produção no diretório `scripts/`:

### 1. `predict_solubility.py`
Treinar e avaliar modelos de predição de solubilidade. Funciona com benchmark Delaney ou dados CSV personalizados.

```bash
# Usar benchmark Delaney
python scripts/predict_solubility.py

# Usar dados personalizados
python scripts/predict_solubility.py \
    --data my_data.csv \
    --smiles-col smiles \
    --target-col solubility \
    --predict "CCO" "c1ccccc1"
```

### 2. `graph_neural_network.py`
Treinar várias arquiteturas de redes neurais de grafos em dados moleculares.

```bash
# Treinar GCN em Tox21
python scripts/graph_neural_network.py --model gcn --dataset tox21

# Treinar AttentiveFP em dados personalizados
python scripts/graph_neural_network.py \
    --model attentivefp \
    --data molecules.csv \
    --task-type regression \
    --targets activity \
    --epochs 100
```

### 3. `transfer_learning.py`
Fine-tune modelos pré-treinados (ChemBERTa, GROVER) em tarefas de predição de propriedades moleculares.

```bash
# Fine-tune ChemBERTa em BBBP
python scripts/transfer_learning.py --model chemberta --dataset bbbp

# Fine-tune GROVER em dados personalizados
python scripts/transfer_learning.py \
    --model grover \
    --data small_dataset.csv \
    --target activity \
    --task-type classification \
    --epochs 20
```

## Padrões Comuns e Melhores Práticas

### Padrão 1: Sempre Use Scaffold Splitting para Moléculas
```python
# BOM: Previne data leakage
splitter = dc.splits.ScaffoldSplitter()
train, test = splitter.train_test_split(dataset)

# RUIM: Moléculas semelhantes em treino e teste
splitter = dc.splits.RandomSplitter()
train, test = splitter.train_test_split(dataset)
```

### Padrão 2: Normalize Features e Targets
```python
transformers = [
    dc.trans.NormalizationTransformer(
        transform_y=True,  # Também normalizar valores de target
        dataset=train
    )
]
for transformer in transformers:
    train = transformer.transform(train)
    test = transformer.transform(test)
```

### Padrão 3: Comece Simples, Depois Escale
1. Comece com Random Forest + CircularFingerprint (baseline rápido)
2. Tente XGBoost/LightGBM se RF funcionar bem
3. Mude para deep learning (MultitaskRegressor) se tiver >5K samples
4. Tente GNNs se tiver >10K samples
5. Use transfer learning para conjuntos pequenos ou scaffolds novos

### Padrão 4: Lidar com Dados Desbalanceados
```python
# Opção 1: Transformador de balanceamento
transformer = dc.trans.BalancingTransformer(dataset=train)
train = transformer.transform(train)

# Opção 2: Usar métricas balanceadas
metric = dc.metrics.Metric(dc.metrics.balanced_accuracy_score)
```

### Padrão 5: Evitar Problemas de Memória
```python
# Usar DiskDataset para conjuntos grandes
dataset = dc.data.DiskDataset.from_numpy(X, y, w, ids)

# Usar batch sizes menores
model = dc.models.GCNModel(batch_size=32)  # Em vez de 128
```

## Armadilhas Comuns

### Issue 1: Data Leakage em Descoberta de Fármacos
**Problema**: Usar divisão aleatória permite moléculas semelhantes em conjuntos treino/teste.
**Solução**: Sempre use `ScaffoldSplitter` para conjuntos de dados moleculares.

### Issue 2: GNN Underperforming vs Fingerprints
**Problema**: Redes neurais de grafos têm pior desempenho que fingerprints simples.
**Soluções**:
- Certifique-se que o dataset é grande o suficiente (>10K samples geralmente)
- Aumente as épocas de treinamento (50-100)
- Tente diferentes arquiteturas (AttentiveFP, DMPNN em vez de GCN)
- Use modelos pré-treinados (GROVER)

### Issue 3: Overfitting em Pequenos Conjuntos
**Problema**: Modelo memoriza dados de treino.
**Soluções**:
- Use regularização mais forte (aumente dropout para 0.5)
- Use modelos mais simples (Random Forest em vez de deep learning)
- Aplique transfer learning (ChemBERTa, GROVER)
- Colete mais dados

### Issue 4: Erros de Import
**Problema**: Erros de módulo não encontrado.
**Solução**: Certifique-se que DeepChem está instalado com dependências necessárias:
```bash
uv pip install deepchem
# Para modelos PyTorch
uv pip install deepchem[torch]
# Para todos os recursos
uv pip install deepchem[all]
```

## Documentação de Referência

Esta skill inclui documentação de referência abrangente:

### `references/api_reference.md`
Documentação completa de API incluindo:
- Todos os data loaders e seus casos de uso
- Classes de datasets e quando usar cada uma
- Catálogo completo de featurizers com guia de seleção
- Catálogo de modelos organizado por categoria (50+ modelos)
- Descrições de conjuntos de dados MoleculeNet
- Funções de métricas e avaliação
- Padrões de código comuns

**Quando consultar**: Busque neste arquivo quando precisar de detalhes específicos de API, nomes de parâmetros, ou quiser explorar opções disponíveis.

### `references/workflows.md`
Oito workflows detalhados end-to-end:
1. Predição de propriedades moleculares a partir de SMILES
2. Usando benchmarks MoleculeNet
3. Otimização de hiperparâmetros
4. Transfer learning com modelos pré-treinados
5. Geração molecular com GANs
6. Predição de propriedades de materiais
7. Análise de sequências de proteínas
8. Integração de modelo personalizado

**Quando consultar**: Use estes workflows como templates para implementar soluções completas.

## Notas de Instalação

Instalação básica:
```bash
uv pip install deepchem
```

Para modelos PyTorch (GCN, GAT, etc.):
```bash
uv pip install deepchem[torch]
```

Para todos os recursos:
```bash
uv pip install deepchem[all]
```

Se erros de import ocorrerem, o usuário pode precisar de dependências específicas. Verifique a documentação DeepChem para instruções detalhadas de instalação.

## Recursos Adicionais

- Documentação oficial: https://deepchem.readthedocs.io/
- Repositório GitHub: https://github.com/deepchem/deepchem
- Tutoriais: https://deepchem.readthedocs.io/en/latest/get_started/tutorials.html
- Paper: "MoleculeNet: A Benchmark for Molecular Machine Learning"