---
name: pytdc
description: "Therapeutics Data Commons. Conjuntos de dados prontos para IA em descoberta de drogas (ADME, toxicidade, DTI), benchmarks, divisões de scaffold, oráculos moleculares, para ML terapêutico e predição farmacológica."
---

# PyTDC (Therapeutics Data Commons)

## Visão Geral

PyTDC é uma plataforma de ciência aberta que fornece datasets e benchmarks prontos para IA em descoberta de drogas e desenvolvimento terapêutico. Acesse datasets curados cobrindo todo o pipeline terapêutico com métricas de avaliação padronizadas e divisões de dados significativas, organizados em três categorias: predição de instância única (propriedades moleculares/protéicas), predição de multi-instância (interações droga-alvo, DDI) e geração (geração de moléculas, retrossíntese).

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Trabalhando com descoberta de drogas ou datasets de ML terapêutico
- Fazendo benchmark de modelos de machine learning em tarefas farmacêuticas padronizadas
- Predizendo propriedades moleculares (ADME, toxicidade, bioatividade)
- Predizendo interações droga-alvo ou droga-droga
- Gerando novas moléculas com propriedades desejadas
- Acessando datasets curados com divisões adequadas de treino/teste (scaffold, cold-split)
- Usando oráculos moleculares para otimização de propriedades

## Instalação e Configuração

Instale PyTDC usando pip:

```bash
uv pip install PyTDC
```

Para atualizar para a versão mais recente:

```bash
uv pip install PyTDC --upgrade
```

Dependências principais (instaladas automaticamente):
- numpy, pandas, tqdm, seaborn, scikit_learn, fuzzywuzzy

Pacotes adicionais são instalados automaticamente conforme necessário para recursos específicos.

## Início Rápido

O padrão básico para acessar qualquer dataset de TDC segue esta estrutura:

```python
from tdc.<problem> import <Task>
data = <Task>(name='<Dataset>')
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
df = data.get_data(format='df')
```

Onde:
- `<problem>`: Um de `single_pred`, `multi_pred` ou `generation`
- `<Task>`: Categoria de tarefa específica (ex: ADME, DTI, MolGen)
- `<Dataset>`: Nome do dataset dentro dessa tarefa

**Exemplo - Carregando dados de ADME:**

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold')
# Retorna dict com DataFrames 'train', 'valid', 'test'
```

## Tarefas de Predição de Instância Única

A predição de instância única envolve prever propriedades de entidades biomédicas individuais (moléculas, proteínas, etc.).

### Categorias de Tarefas Disponíveis

#### 1. ADME (Absorção, Distribuição, Metabolismo, Excreção)

Prediga propriedades farmacocinéticas de moléculas de drogas.

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')  # Permeabilidade intestinal
# Outros datasets: HIA_Hou, Bioavailability_Ma, Lipophilicity_AstraZeneca, etc.
```

**Datasets ADME comuns:**
- Caco2 - Permeabilidade intestinal
- HIA - Absorção intestinal humana
- Bioavailability - Biodisponibilidade oral
- Lipophilicity - Coeficiente de partição octanol-água
- Solubility - Solubilidade aquosa
- BBB - Penetração da barreira hematoencefálica
- CYP - Metabolismo citocromo P450

#### 2. Toxicidade (Tox)

Prediga toxicidade e efeitos adversos de compostos.

```python
from tdc.single_pred import Tox
data = Tox(name='hERG')  # Cardiotoxicidade
# Outros datasets: AMES, DILI, Carcinogens_Lagunin, etc.
```

**Datasets de toxicidade comuns:**
- hERG - Toxicidade cardíaca
- AMES - Mutagenicidade
- DILI - Lesão hepática induzida por droga
- Carcinogens - Carcinogenicidade
- ClinTox - Toxicidade em ensaios clínicos

#### 3. HTS (High-Throughput Screening)

Predições de bioatividade a partir de dados de screening.

```python
from tdc.single_pred import HTS
data = HTS(name='SARSCoV2_Vitro_Touret')
```

#### 4. QM (Quantum Mechanics)

Propriedades mecânico-quânticas de moléculas.

```python
from tdc.single_pred import QM
data = QM(name='QM7')
```

#### 5. Outras Tarefas de Predição Única

- **Yields**: Predição de rendimento de reação química
- **Epitope**: Predição de epítopo para biológicos
- **Develop**: Predições de estágio de desenvolvimento
- **CRISPROutcome**: Predição de resultado de edição gênica

### Formato de Dados

Datasets de predição única geralmente retornam DataFrames com colunas:
- `Drug_ID` ou `Compound_ID`: Identificador único
- `Drug` ou `X`: String SMILES ou representação molecular
- `Y`: Label alvo (contínuo ou binário)

## Tarefas de Predição de Multi-Instância

A predição de multi-instância envolve prever propriedades de interações entre múltiplas entidades biomédicas.

### Categorias de Tarefas Disponíveis

#### 1. DTI (Drug-Target Interaction)

Prediga afinidade de ligação entre drogas e alvos protéicos.

```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split()
```

**Datasets disponíveis:**
- BindingDB_Kd - Constante de dissociação (52.284 pares)
- BindingDB_IC50 - Concentração inibitória máxima (991.486 pares)
- BindingDB_Ki - Constante de inibição (375.032 pares)
- DAVIS, KIBA - Datasets de ligação de quinase

**Formato de dados:** Drug_ID, Target_ID, Drug (SMILES), Target (sequência), Y (afinidade de ligação)

#### 2. DDI (Drug-Drug Interaction)

Prediga interações entre pares de drogas.

```python
from tdc.multi_pred import DDI
data = DDI(name='DrugBank')
split = data.get_split()
```

Tarefa de classificação multiclasse que prediz tipos de interação. Dataset contém 191.808 pares de DDI com 1.706 drogas.

#### 3. PPI (Protein-Protein Interaction)

Prediga interações proteína-proteína.

```python
from tdc.multi_pred import PPI
data = PPI(name='HuRI')
```

#### 4. Outras Tarefas de Multi-Predição

- **GDA**: Associações gene-doença
- **DrugRes**: Predição de resistência a drogas
- **DrugSyn**: Predição de sinergia de drogas
- **PeptideMHC**: Ligação de peptídeo-MHC
- **AntibodyAff**: Predição de afinidade de anticorpo
- **MTI**: Interações miRNA-alvo
- **Catalyst**: Predição de catalisador
- **TrialOutcome**: Predição de resultado de ensaio clínico

## Tarefas de Geração

As tarefas de geração envolvem criar novas entidades biomédicas com propriedades desejadas.

### 1. Geração Molecular (MolGen)

Gere moléculas diversas e inéditas com propriedades químicas desejáveis.

```python
from tdc.generation import MolGen
data = MolGen(name='ChEMBL_V29')
split = data.get_split()
```

Use com oráculos para otimizar propriedades específicas:

```python
from tdc import Oracle
oracle = Oracle(name='GSK3B')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')  # Avalie SMILES
```

Veja `references/oracles.md` para todas as funções de oráculo disponíveis.

### 2. Retrossíntese (RetroSyn)

Prediga reagentes necessários para sintetizar uma molécula alvo.

```python
from tdc.generation import RetroSyn
data = RetroSyn(name='USPTO')
split = data.get_split()
```

Dataset contém 1.939.253 reações do banco de dados USPTO.

### 3. Geração de Moléculas Pareadas

Gere pares de moléculas (ex: pares pró-droga-droga).

```python
from tdc.generation import PairMolGen
data = PairMolGen(name='Prodrug')
```

Para documentação detalhada de oráculos e workflows de geração molecular, consulte `references/oracles.md` e `scripts/molecular_generation.py`.

## Grupos de Benchmark

Grupos de benchmark fornecem coleções curadas de datasets relacionados para avaliação sistemática de modelos.

### Grupo de Benchmark ADMET

```python
from tdc.benchmark_group import admet_group
group = admet_group(path='data/')

# Obtenha datasets de benchmark
benchmark = group.get('Caco2_Wang')
predictions = {}

for seed in [1, 2, 3, 4, 5]:
    train, valid = benchmark['train'], benchmark['valid']
    # Treine o modelo aqui
    predictions[seed] = model.predict(benchmark['test'])

# Avalie com 5 seeds necessárias
results = group.evaluate(predictions)
```

**O Grupo ADMET inclui 22 datasets** cobrindo absorção, distribuição, metabolismo, excreção e toxicidade.

### Outros Grupos de Benchmark

Grupos de benchmark disponíveis incluem coleções para:
- Propriedades ADMET
- Interações droga-alvo
- Predição de combinação de drogas
- E mais tarefas terapêuticas especializadas

Para workflows de avaliação de benchmark, veja `scripts/benchmark_evaluation.py`.

## Funções de Dados

TDC fornece utilitários abrangentes de processamento de dados organizados em quatro categorias.

### 1. Divisões de Dataset

Recupere partições de treino/validação/teste com várias estratégias:

```python
# Divisão por scaffold (padrão para a maioria das tarefas)
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])

# Divisão aleatória
split = data.get_split(method='random', seed=42, frac=[0.8, 0.1, 0.1])

# Divisão fria (para tarefas DTI/DDI)
split = data.get_split(method='cold_drug', seed=1)  # Drogas não vistas no teste
split = data.get_split(method='cold_target', seed=1)  # Alvos não vistos no teste
```

**Estratégias de divisão disponíveis:**
- `random`: Embaralhamento aleatório
- `scaffold`: Baseado em scaffold (para diversidade química)
- `cold_drug`, `cold_target`, `cold_drug_target`: Para tarefas DTI
- `temporal`: Divisões baseadas em tempo para datasets temporais

### 2. Avaliação de Modelo

Use métricas padronizadas para avaliação:

```python
from tdc import Evaluator

# Para classificação binária
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred)

# Para regressão
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

**Métricas disponíveis:** ROC-AUC, PR-AUC, F1, Accuracy, RMSE, MAE, R2, Spearman, Pearson, e mais.

### 3. Processamento de Dados

TDC fornece 11 utilitários de processamento principais:

```python
from tdc.chem_utils import MolConvert

# Conversão de formato molecular
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

**Utilitários de processamento incluem:**
- Conversão de formato molecular (SMILES, SELFIES, PyG, DGL, ECFP, etc.)
- Filtros de molécula (PAINS, drug-likeness)
- Binarização de label e conversão de unidade
- Balanceamento de dados (over/under-sampling)
- Negative sampling para dados pareados
- Transformação de grafo
- Recuperação de entidade (CID para SMILES, UniProt para sequência)

Para documentação abrangente de utilitários, veja `references/utilities.md`.

### 4. Oráculos de Geração de Moléculas

TDC fornece 17+ funções de oráculo para otimização molecular:

```python
from tdc import Oracle

# Oráculo único
oracle = Oracle(name='DRD2')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# Múltiplos oráculos
oracle = Oracle(name='JNK3')
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

Para documentação completa de oráculos, veja `references/oracles.md`.

## Recursos Avançados

### Recuperar Datasets Disponíveis

```python
from tdc.utils import retrieve_dataset_names

# Obtenha todos os datasets ADME
adme_datasets = retrieve_dataset_names('ADME')

# Obtenha todos os datasets DTI
dti_datasets = retrieve_dataset_names('DTI')
```

### Transformações de Label

```python
# Obtenha mapeamento de label
label_map = data.get_label_map(name='DrugBank')

# Converta labels
from tdc.chem_utils import label_transform
transformed = label_transform(y, from_unit='nM', to_unit='p')
```

### Queries de Banco de Dados

```python
from tdc.utils import cid2smiles, uniprot2seq

# Converta PubChem CID para SMILES
smiles = cid2smiles(2244)

# Converta ID UniProt para sequência de aminoácido
sequence = uniprot2seq('P12345')
```

## Workflows Comuns

### Workflow 1: Treinar um Modelo de Predição Única

Veja `scripts/load_and_split_data.py` para um exemplo completo:

```python
from tdc.single_pred import ADME
from tdc import Evaluator

# Carregue dados
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold', seed=42)

train, valid, test = split['train'], split['valid'], split['test']

# Treine o modelo (você implementa)
# model.fit(train['Drug'], train['Y'])

# Avalie
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### Workflow 2: Avaliação de Benchmark

Veja `scripts/benchmark_evaluation.py` para um exemplo completo com múltiplas seeds e protocolo de avaliação adequado.

### Workflow 3: Geração Molecular com Oráculos

Veja `scripts/molecular_generation.py` para um exemplo de geração direcionada a objetivo usando funções de oráculo.

## Recursos

Esta skill inclui recursos agrupados para workflows comuns de TDC:

### scripts/

- `load_and_split_data.py`: Template para carregar e dividir datasets de TDC com várias estratégias
- `benchmark_evaluation.py`: Template para executar avaliações de grupo de benchmark com protocolo apropriado de 5 seeds
- `molecular_generation.py`: Template para geração molecular usando funções de oráculo

### references/

- `datasets.md`: Catálogo abrangente de todos os datasets disponíveis organizados por tipo de tarefa
- `oracles.md`: Documentação completa de todos os 17+ oráculos de geração de moléculas
- `utilities.md`: Guia detalhado para utilitários de processamento de dados, divisão e avaliação

## Recursos Adicionais

- **Website Oficial**: https://tdcommons.ai
- **Documentação**: https://tdc.readthedocs.io
- **GitHub**: https://github.com/mims-harvard/TDC
- **Paper**: NeurIPS 2021 - "Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development"