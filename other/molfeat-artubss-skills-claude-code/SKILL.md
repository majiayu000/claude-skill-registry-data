---
name: molfeat
description: "Featurização molecular para ML (100+ featurizadores). ECFP, MACCS, descritores, modelos pré-treinados (ChemBERTa), converter SMILES em features, para QSAR e ML molecular."
---

# Molfeat - Hub de Featurização Molecular

## Visão Geral

Molfeat é uma biblioteca Python abrangente para featurização molecular que unifica 100+ embeddings pré-treinados e featurizadores artesanais. Converta estruturas químicas (strings SMILES ou moléculas RDKit) em representações numéricas para tarefas de machine learning incluindo modelagem QSAR, triagem virtual, busca de similaridade e aplicações de deep learning. Oferece processamento paralelo rápido, transformadores compatíveis com scikit-learn e caching integrado.

## Quando Usar Esta Skill

Esta skill deve ser usada ao trabalhar com:
- **Machine learning molecular**: Construir modelos QSAR/QSPR, predição de propriedades
- **Triagem virtual**: Ranking de bibliotecas de compostos para atividade biológica
- **Busca de similaridade**: Encontrar moléculas estruturalmente similares
- **Análise de espaço químico**: Clustering, visualização, redução de dimensionalidade
- **Deep learning**: Treinar redes neurais em dados moleculares
- **Pipelines de featurização**: Converter SMILES em representações prontas para ML
- **Quiminformática**: Qualquer tarefa que requer extração de features moleculares

## Instalação

```bash
uv pip install molfeat

# Com todas as dependências opcionais
uv pip install "molfeat[all]"
```

**Dependências opcionais para featurizadores específicos:**
- `molfeat[dgl]` - Modelos GNN (variantes GIN)
- `molfeat[graphormer]` - Modelos Graphormer
- `molfeat[transformer]` - ChemBERTa, ChemGPT, MolT5
- `molfeat[fcd]` - Descritores FCD
- `molfeat[map4]` - Fingerprints MAP4

## Conceitos Principais

Molfeat organiza a featurização em três classes hierárquicas:

### 1. Calculadores (`molfeat.calc`)

Objetos chamáveis que convertem moléculas individuais em vetores de features. Aceitam objetos RDKit `Chem.Mol` ou strings SMILES.

**Use calculadores para:**
- Featurização de molécula única
- Loops de processamento customizado
- Computação direta de features

**Exemplo:**
```python
from molfeat.calc import FPCalculator

calc = FPCalculator("ecfp", radius=3, fpSize=2048)
features = calc("CCO")  # Retorna array numpy (2048,)
```

### 2. Transformadores (`molfeat.trans`)

Transformadores compatíveis com scikit-learn que envolvem calculadores para processamento em lote com paralelização.

**Use transformadores para:**
- Featurização em lote de datasets moleculares
- Integração com pipelines scikit-learn
- Processamento paralelo (utilização automática de CPU)

**Exemplo:**
```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator

transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
features = transformer(smiles_list)  # Processamento paralelo
```

### 3. Transformadores Pré-treinados (`molfeat.trans.pretrained`)

Transformadores especializados para modelos de deep learning com inferência em lote e caching.

**Use transformadores pré-treinados para:**
- Embeddings moleculares estado-da-arte
- Transfer learning a partir de datasets químicos grandes
- Extração de features de deep learning

**Exemplo:**
```python
from molfeat.trans.pretrained import PretrainedMolTransformer

transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)
embeddings = transformer(smiles_list)  # Embeddings de deep learning
```

## Workflow de Quick Start

### Featurização Básica

```python
import datamol as dm
from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer

# Carregar dados moleculares
smiles = ["CCO", "CC(=O)O", "c1ccccc1", "CC(C)O"]

# Criar calculador e transformador
calc = FPCalculator("ecfp", radius=3)
transformer = MoleculeTransformer(calc, n_jobs=-1)

# Featurizar moléculas
features = transformer(smiles)
print(f"Shape: {features.shape}")  # (4, 2048)
```

### Salvar e Carregar Configuração

```python
# Salvar configuração do featurizador para reprodutibilidade
transformer.to_state_yaml_file("featurizer_config.yml")

# Recarregar configuração exata
loaded = MoleculeTransformer.from_state_yaml_file("featurizer_config.yml")
```

### Lidar com Erros Graciosamente

```python
# Processar dataset com possíveis SMILES inválidos
transformer = MoleculeTransformer(
    calc,
    n_jobs=-1,
    ignore_errors=True,  # Continuar em falhas
    verbose=True          # Log de detalhes de erro
)

features = transformer(smiles_with_errors)
# Retorna None para moléculas com falha
```

## Escolhendo o Featurizador Certo

### Para Machine Learning Tradicional (RF, SVM, XGBoost)

**Comece com fingerprints:**
```python
# ECFP - Mais popular, uso geral
FPCalculator("ecfp", radius=3, fpSize=2048)

# MACCS - Rápido, bom para scaffold hopping
FPCalculator("maccs")

# MAP4 - Eficiente para triagem em larga escala
FPCalculator("map4")
```

**Para modelos interpretáveis:**
```python
# Descritores 2D RDKit (200+ propriedades nomeadas)
from molfeat.calc import RDKitDescriptors2D
RDKitDescriptors2D()

# Mordred (1800+ descritores abrangentes)
from molfeat.calc import MordredDescriptors
MordredDescriptors()
```

**Combine múltiplos featurizadores:**
```python
from molfeat.trans import FeatConcat

concat = FeatConcat([
    FPCalculator("maccs"),      # 167 dimensões
    FPCalculator("ecfp")         # 2048 dimensões
])  # Resultado: features combinadas 2215-dimensionais
```

### Para Deep Learning

**Embeddings baseados em transformer:**
```python
# ChemBERTa - Pré-treinado em 77M compostos PubChem
PretrainedMolTransformer("ChemBERTa-77M-MLM")

# ChemGPT - Modelo de linguagem autorregressivo
PretrainedMolTransformer("ChemGPT-1.2B")
```

**Redes neurais gráficas:**
```python
# Modelos GIN com diferentes objetivos de pré-treinamento
PretrainedMolTransformer("gin-supervised-masking")
PretrainedMolTransformer("gin-supervised-infomax")

# Graphormer para química quântica
PretrainedMolTransformer("Graphormer-pcqm4mv2")
```

### Para Busca de Similaridade

```python
# ECFP - Uso geral, mais amplamente utilizado
FPCalculator("ecfp")

# MACCS - Rápido, similaridade baseada em scaffold
FPCalculator("maccs")

# MAP4 - Eficiente para grandes bases de dados
FPCalculator("map4")

# USR/USRCAT - Similaridade de forma 3D
from molfeat.calc import USRDescriptors
USRDescriptors()
```

### Para Abordagens Baseadas em Farmacóforo

```python
# FCFP - Baseado em grupo funcional
FPCalculator("fcfp")

# CATS - Distribuições de pares farmacóforos
from molfeat.calc import CATSCalculator
CATSCalculator(mode="2D")

# Gobbi - Features farmacóforas explícitas
FPCalculator("gobbi2D")
```

## Workflows Comuns

### Construir um Modelo QSAR

```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

# Featurizar moléculas
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X = transformer(smiles_train)

# Treinar modelo
model = RandomForestRegressor(n_estimators=100)
scores = cross_val_score(model, X, y_train, cv=5)
print(f"R² = {scores.mean():.3f}")

# Salvar configuração para deployment
transformer.to_state_yaml_file("production_featurizer.yml")
```

### Pipeline de Triagem Virtual

```python
from sklearn.ensemble import RandomForestClassifier

# Treinar em moléculas ativas/inativas conhecidas
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X_train = transformer(train_smiles)
clf = RandomForestClassifier(n_estimators=500)
clf.fit(X_train, train_labels)

# Rastrear grande biblioteca
X_screen = transformer(screening_library)  # ex: 1M de compostos
predictions = clf.predict_proba(X_screen)[:, 1]

# Rankear e selecionar top hits
top_indices = predictions.argsort()[::-1][:1000]
top_hits = [screening_library[i] for i in top_indices]
```

### Busca de Similaridade

```python
from sklearn.metrics.pairwise import cosine_similarity

# Molécula de consulta
calc = FPCalculator("ecfp")
query_fp = calc(query_smiles).reshape(1, -1)

# Fingerprints da base de dados
transformer = MoleculeTransformer(calc, n_jobs=-1)
database_fps = transformer(database_smiles)

# Computar similaridade
similarities = cosine_similarity(query_fp, database_fps)[0]
top_similar = similarities.argsort()[-10:][::-1]
```

### Integração com Pipeline Scikit-learn

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Criar pipeline ponta a ponta
pipeline = Pipeline([
    ('featurizer', MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Treinar e prever diretamente em SMILES
pipeline.fit(smiles_train, y_train)
predictions = pipeline.predict(smiles_test)
```

### Comparar Múltiplos Featurizadores

```python
featurizers = {
    'ECFP': FPCalculator("ecfp"),
    'MACCS': FPCalculator("maccs"),
    'Descriptors': RDKitDescriptors2D(),
    'ChemBERTa': PretrainedMolTransformer("ChemBERTa-77M-MLM")
}

results = {}
for name, feat in featurizers.items():
    transformer = MoleculeTransformer(feat, n_jobs=-1)
    X = transformer(smiles)
    # Avaliar com seu modelo ML
    score = evaluate_model(X, y)
    results[name] = score
```

## Descobrir Featurizadores Disponíveis

Use ModelStore para explorar todos os featurizadores disponíveis:

```python
from molfeat.store.modelstore import ModelStore

store = ModelStore()

# Listar todos os modelos disponíveis
all_models = store.available_models
print(f"Total featurizadores: {len(all_models)}")

# Buscar modelos específicos
chemberta_models = store.search(name="ChemBERTa")
for model in chemberta_models:
    print(f"- {model.name}: {model.description}")

# Obter informações de uso
model_card = store.search(name="ChemBERTa-77M-MLM")[0]
model_card.usage()  # Mostrar exemplos de uso

# Carregar modelo
transformer = store.load("ChemBERTa-77M-MLM")
```

## Features Avançadas

### Pré-processamento Customizado

```python
class CustomTransformer(MoleculeTransformer):
    def preprocess(self, mol):
        """Pipeline de pré-processamento customizado"""
        if isinstance(mol, str):
            mol = dm.to_mol(mol)
        mol = dm.standardize_mol(mol)
        mol = dm.remove_salts(mol)
        return mol

transformer = CustomTransformer(FPCalculator("ecfp"), n_jobs=-1)
```

### Processamento em Lote de Datasets Grandes

```python
def featurize_in_chunks(smiles_list, transformer, chunk_size=10000):
    """Processar datasets grandes em chunks para gerenciar memória"""
    all_features = []
    for i in range(0, len(smiles_list), chunk_size):
        chunk = smiles_list[i:i+chunk_size]
        features = transformer(chunk)
        all_features.append(features)
    return np.vstack(all_features)
```

### Caching de Embeddings Caros

```python
import pickle

cache_file = "embeddings_cache.pkl"
transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)

try:
    with open(cache_file, "rb") as f:
        embeddings = pickle.load(f)
except FileNotFoundError:
    embeddings = transformer(smiles_list)
    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)
```

## Dicas de Performance

1. **Use paralelização**: Defina `n_jobs=-1` para utilizar todos os núcleos da CPU
2. **Processamento em lote**: Processe múltiplas moléculas de uma vez em vez de loops
3. **Escolha featurizadores apropriados**: Fingerprints são mais rápidos que modelos de deep learning
4. **Cache modelos pré-treinados**: Aproveite o caching integrado para uso repetido
5. **Use float32**: Defina `dtype=np.float32` quando a precisão permitir
6. **Lidar com erros eficientemente**: Use `ignore_errors=True` para datasets grandes

## Referência de Featurizadores Comuns

**Referência rápida para featurizadores frequentemente usados:**

| Featurizador | Tipo | Dimensões | Velocidade | Caso de Uso |
|------------|------|------------|-----------|----------|
| `ecfp` | Fingerprint | 2048 | Rápido | Uso geral |
| `maccs` | Fingerprint | 167 | Muito rápido | Similaridade de scaffold |
| `desc2D` | Descritores | 200+ | Rápido | Modelos interpretáveis |
| `mordred` | Descritores | 1800+ | Médio | Features abrangentes |
| `map4` | Fingerprint | 1024 | Rápido | Triagem em larga escala |
| `ChemBERTa-77M-MLM` | Deep learning | 768 | Lento* | Transfer learning |
| `gin-supervised-masking` | GNN | Variável | Lento* | Modelos baseados em grafo |

*Primeira execução é lenta; execuções subsequentes se beneficiam do caching

## Recursos

Esta skill inclui documentação de referência abrangente:

### references/api_reference.md
Documentação completa da API cobrindo:
- `molfeat.calc` - Todas as classes calculadora e parâmetros
- `molfeat.trans` - Classes transformadora e métodos
- `molfeat.store` - Uso de ModelStore
- Padrões comuns e exemplos de integração
- Dicas de otimização de performance

**Quando carregar:** Referenciar ao implementar calculadores específicos, compreender parâmetros de transformadores ou integrar com scikit-learn/PyTorch.

### references/available_featurizers.md
Catálogo abrangente de todos os 100+ featurizadores organizados por categoria:
- Modelos de linguagem baseados em transformer (ChemBERTa, ChemGPT)
- Redes neurais gráficas (GIN, Graphormer)
- Descritores moleculares (RDKit, Mordred)
- Fingerprints (ECFP, MACCS, MAP4 e 15+ outros)
- Descritores farmacóforos (CATS, Gobbi)
- Descritores de forma (USR, ElectroShape)
- Descritores baseados em scaffold

**Quando carregar:** Referenciar ao selecionar o featurizador ideal para uma tarefa específica, explorar opções disponíveis ou compreender características de featurizadores.

**Dica de busca:** Use grep para encontrar tipos específicos de featurizadores:
```bash
grep -i "chembert" references/available_featurizers.md
grep -i "pharmacophore" references/available_featurizers.md
```

### references/examples.md
Exemplos de código prático para cenários comuns:
- Instalação e quick start
- Exemplos de calculador e transformador
- Uso de modelos pré-treinados
- Integração com scikit-learn e PyTorch
- Workflows de triagem virtual
- Construção de modelos QSAR
- Busca de similaridade
- Troubleshooting e melhores práticas

**Quando carregar:** Referenciar ao implementar workflows específicos, troubleshooting de problemas ou aprender padrões de molfeat.

## Troubleshooting

### Moléculas Inválidas
Abilitar manipulação de erros para pular SMILES inválidos:
```python
transformer = MoleculeTransformer(
    calc,
    ignore_errors=True,
    verbose=True
)
```

### Problemas de Memória com Datasets Grandes
Processar em chunks ou usar abordagens de streaming para datasets > 100K moléculas.

### Dependências de Modelos Pré-treinados
Alguns modelos requerem pacotes adicionais. Instale extras específicas:
```bash
uv pip install "molfeat[transformer]"  # Para ChemBERTa/ChemGPT
uv pip install "molfeat[dgl]"          # Para modelos GIN
```

### Reprodutibilidade
Salve configurações exatas e documente versões:
```python
transformer.to_state_yaml_file("config.yml")
import molfeat
print(f"molfeat versão: {molfeat.__version__}")
```

## Recursos Adicionais

- **Documentação Oficial**: https://molfeat-docs.datamol.io/
- **Repositório GitHub**: https://github.com/datamol-io/molfeat
- **Pacote PyPI**: https://pypi.org/project/molfeat/
- **Tutorial**: https://portal.valencelabs.com/datamol/post/types-of-featurizers-b1e8HHrbFMkbun6