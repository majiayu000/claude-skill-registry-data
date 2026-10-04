---
name: datamol
description: "Wrapper Pythônico ao redor do RDKit com interface simplificada e padrões sensatos. Preferido para descoberta de fármacos padrão: análise de SMILES, padronização, descritores, fingerprints, clustering, conformadores 3D, processamento paralelo. Retorna objetos nativos rdkit.Chem.Mol. Para controle avançado ou parâmetros customizados, use rdkit diretamente."
---

# Habilidade de Quimioinformática Datamol

## Visão Geral

Datamol é uma biblioteca Python que fornece uma camada de abstração leve e Pythônica sobre RDKit para quimioinformática molecular. Simplifique operações moleculares complexas com padrões sensatos, paralelização eficiente e capacidades de I/O modernas. Todos os objetos moleculares são instâncias nativas `rdkit.Chem.Mol`, garantindo compatibilidade total com o ecossistema RDKit.

**Capacidades principais**:
- Conversão de formatos moleculares (SMILES, SELFIES, InChI)
- Padronização e sanitização de estruturas
- Descritores e fingerprints moleculares
- Geração e análise de conformadores 3D
- Clustering e seleção de diversidade
- Análise de scaffolds e fragmentos
- Aplicação de reações químicas
- Visualização e alinhamento
- Processamento em lote com paralelização
- Suporte a armazenamento em nuvem via fsspec

## Instalação e Configuração

Guie os usuários para instalar datamol:

```bash
uv pip install datamol
```

**Convenção de import**:
```python
import datamol as dm
```

## Fluxos de Trabalho Principais

### 1. Manipulação Básica de Moléculas

**Criando moléculas a partir de SMILES**:
```python
import datamol as dm

# Molécula única
mol = dm.to_mol("CCO")  # Etanol

# A partir de lista de SMILES
smiles_list = ["CCO", "c1ccccc1", "CC(=O)O"]
mols = [dm.to_mol(smi) for smi in smiles_list]

# Tratamento de erros
mol = dm.to_mol("invalid_smiles")  # Retorna None
if mol is None:
    print("Falha ao analisar SMILES")
```

**Convertendo moléculas para SMILES**:
```python
# SMILES canônico
smiles = dm.to_smiles(mol)

# SMILES isomérico (inclui estereoquímica)
smiles = dm.to_smiles(mol, isomeric=True)

# Outros formatos
inchi = dm.to_inchi(mol)
inchikey = dm.to_inchikey(mol)
selfies = dm.to_selfies(mol)
```

**Padronização e sanitização** (sempre recomendado para moléculas fornecidas pelo usuário):
```python
# Sanitizar molécula
mol = dm.sanitize_mol(mol)

# Padronização completa (recomendado para datasets)
mol = dm.standardize_mol(
    mol,
    disconnect_metals=True,
    normalize=True,
    reionize=True
)

# Para strings SMILES diretamente
clean_smiles = dm.standardize_smiles(smiles)
```

### 2. Leitura e Escrita de Arquivos Moleculares

Consulte `references/io_module.md` para documentação abrangente de I/O.

**Lendo arquivos**:
```python
# Arquivos SDF (mais comuns em química)
df = dm.read_sdf("compounds.sdf", mol_column='mol')

# Arquivos SMILES
df = dm.read_smi("molecules.smi", smiles_column='smiles', mol_column='mol')

# CSV com coluna SMILES
df = dm.read_csv("data.csv", smiles_column="SMILES", mol_column="mol")

# Arquivos Excel
df = dm.read_excel("compounds.xlsx", sheet_name=0, mol_column="mol")

# Leitor universal (detecção automática de formato)
df = dm.open_df("file.sdf")  # Funciona com .sdf, .csv, .xlsx, .parquet, .json
```

**Escrevendo arquivos**:
```python
# Salvar como SDF
dm.to_sdf(mols, "output.sdf")
# Ou a partir de DataFrame
dm.to_sdf(df, "output.sdf", mol_column="mol")

# Salvar como arquivo SMILES
dm.to_smi(mols, "output.smi")

# Excel com imagens de moléculas renderizadas
dm.to_xlsx(df, "output.xlsx", mol_columns=["mol"])
```

**Suporte a arquivos remotos** (S3, GCS, HTTP):
```python
# Ler do armazenamento em nuvem
df = dm.read_sdf("s3://bucket/compounds.sdf")
df = dm.read_csv("https://example.com/data.csv")

# Escrever no armazenamento em nuvem
dm.to_sdf(mols, "s3://bucket/output.sdf")
```

### 3. Descritores e Propriedades Moleculares

Consulte `references/descriptors_viz.md` para documentação detalhada de descritores.

**Computando descritores para uma única molécula**:
```python
# Obter conjunto padrão de descritores
descriptors = dm.descriptors.compute_many_descriptors(mol)
# Retorna: {'mw': 46.07, 'logp': -0.03, 'hbd': 1, 'hba': 1,
#           'tpsa': 20.23, 'n_aromatic_atoms': 0, ...}
```

**Computação em lote de descritores** (recomendado para datasets):
```python
# Computar para todas as moléculas em paralelo
desc_df = dm.descriptors.batch_compute_many_descriptors(
    mols,
    n_jobs=-1,      # Usar todos os núcleos da CPU
    progress=True   # Mostrar barra de progresso
)
```

**Descritores específicos**:
```python
# Aromaticidade
n_aromatic = dm.descriptors.n_aromatic_atoms(mol)
aromatic_ratio = dm.descriptors.n_aromatic_atoms_proportion(mol)

# Estereoquímica
n_stereo = dm.descriptors.n_stereo_centers(mol)
n_unspec = dm.descriptors.n_stereo_centers_unspecified(mol)

# Flexibilidade
n_rigid = dm.descriptors.n_rigid_bonds(mol)
```

**Filtragem de semelhança a fármacos (Regra de Cinco de Lipinski)**:
```python
# Filtrar compostos
def is_druglike(mol):
    desc = dm.descriptors.compute_many_descriptors(mol)
    return (
        desc['mw'] <= 500 and
        desc['logp'] <= 5 and
        desc['hbd'] <= 5 and
        desc['hba'] <= 10
    )

druglike_mols = [mol for mol in mols if is_druglike(mol)]
```

### 4. Fingerprints e Similaridade Molecular

**Gerando fingerprints**:
```python
# ECFP (Extended Connectivity Fingerprint, padrão)
fp = dm.to_fp(mol, fp_type='ecfp', radius=2, n_bits=2048)

# Outros tipos de fingerprint
fp_maccs = dm.to_fp(mol, fp_type='maccs')
fp_topological = dm.to_fp(mol, fp_type='topological')
fp_atompair = dm.to_fp(mol, fp_type='atompair')
```

**Cálculos de similaridade**:
```python
# Distâncias aos pares dentro de um conjunto
distance_matrix = dm.pdist(mols, n_jobs=-1)

# Distâncias entre dois conjuntos
distances = dm.cdist(query_mols, library_mols, n_jobs=-1)

# Encontrar moléculas mais similares
from scipy.spatial.distance import squareform
dist_matrix = squareform(dm.pdist(mols))
# Distância menor = similaridade maior (Distância Tanimoto = 1 - Similaridade Tanimoto)
```

### 5. Clustering e Seleção de Diversidade

Consulte `references/core_api.md` para detalhes de clustering.

**Clustering Butina**:
```python
# Agrupar moléculas por similaridade estrutural
clusters = dm.cluster_mols(
    mols,
    cutoff=0.2,    # Limite de distância Tanimoto (0=idêntico, 1=completamente diferente)
    n_jobs=-1      # Processamento paralelo
)

# Cada cluster é uma lista de índices de moléculas
for i, cluster in enumerate(clusters):
    print(f"Cluster {i}: {len(cluster)} moléculas")
    cluster_mols = [mols[idx] for idx in cluster]
```

**Importante**: O clustering Butina constrói uma matriz de distância completa - adequado para ~1000 moléculas, não para 10.000+.

**Seleção de diversidade**:
```python
# Escolher subconjunto diverso
diverse_mols = dm.pick_diverse(
    mols,
    npick=100  # Selecionar 100 moléculas diversas
)

# Escolher centroides de clusters
centroids = dm.pick_centroids(
    mols,
    npick=50   # Selecionar 50 moléculas representativas
)
```

### 6. Análise de Scaffolds

Consulte `references/fragments_scaffolds.md` para documentação completa de scaffolds.

**Extraindo scaffolds Murcko**:
```python
# Obter scaffold Bemis-Murcko (estrutura central)
scaffold = dm.to_scaffold_murcko(mol)
scaffold_smiles = dm.to_smiles(scaffold)
```

**Análise baseada em scaffold**:
```python
# Agrupar compostos por scaffold
from collections import Counter

scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Contar frequência de scaffold
scaffold_counts = Counter(scaffold_smiles)
most_common = scaffold_counts.most_common(10)

# Criar mapeamento scaffold-para-moléculas
scaffold_groups = {}
for mol, scaf_smi in zip(mols, scaffold_smiles):
    if scaf_smi not in scaffold_groups:
        scaffold_groups[scaf_smi] = []
    scaffold_groups[scaf_smi].append(mol)
```

**Divisão baseada em scaffold para ML**:
```python
# Garantir que conjuntos de treino e teste tenham scaffolds diferentes
scaffold_to_mols = {}
for mol, scaf in zip(mols, scaffold_smiles):
    if scaf not in scaffold_to_mols:
        scaffold_to_mols[scaf] = []
    scaffold_to_mols[scaf].append(mol)

# Dividir scaffolds em treino/teste
import random
scaffolds = list(scaffold_to_mols.keys())
random.shuffle(scaffolds)
split_idx = int(0.8 * len(scaffolds))
train_scaffolds = scaffolds[:split_idx]
test_scaffolds = scaffolds[split_idx:]

# Obter moléculas para cada divisão
train_mols = [mol for scaf in train_scaffolds for mol in scaffold_to_mols[scaf]]
test_mols = [mol for scaf in test_scaffolds for mol in scaffold_to_mols[scaf]]
```

### 7. Fragmentação Molecular

Consulte `references/fragments_scaffolds.md` para detalhes de fragmentação.

**Fragmentação BRICS** (16 tipos de ligação):
```python
# Fragmentar molécula
fragments = dm.fragment.brics(mol)
# Retorna: conjunto de SMILES de fragmentos com pontos de ligação como '[1*]CCN'
```

**Fragmentação RECAP** (11 tipos de ligação):
```python
fragments = dm.fragment.recap(mol)
```

**Análise de fragmentos**:
```python
# Encontrar fragmentos comuns na biblioteca de compostos
from collections import Counter

all_fragments = []
for mol in mols:
    frags = dm.fragment.brics(mol)
    all_fragments.extend(frags)

fragment_counts = Counter(all_fragments)
common_frags = fragment_counts.most_common(20)

# Pontuação baseada em fragmentos
def fragment_score(mol, reference_fragments):
    mol_frags = dm.fragment.brics(mol)
    overlap = mol_frags.intersection(reference_fragments)
    return len(overlap) / len(mol_frags) if mol_frags else 0
```

### 8. Geração de Conformadores 3D

Consulte `references/conformers_module.md` para documentação detalhada de conformadores.

**Gerando conformadores**:
```python
# Gerar conformadores 3D
mol_3d = dm.conformers.generate(
    mol,
    n_confs=50,           # Número a gerar (automático se None)
    rms_cutoff=0.5,       # Filtrar conformadores similares (Ångströms)
    minimize_energy=True,  # Minimizar com campo de força UFF
    method='ETKDGv3'      # Método de embedding (recomendado)
)

# Acessar conformadores
n_conformers = mol_3d.GetNumConformers()
conf = mol_3d.GetConformer(0)  # Obter primeiro conformador
positions = conf.GetPositions()  # Array Nx3 de coordenadas de átomos
```

**Clustering de conformadores**:
```python
# Agrupar conformadores por RMSD
clusters = dm.conformers.cluster(
    mol_3d,
    rms_cutoff=1.0,
    centroids=False
)

# Obter conformadores representativos
centroids = dm.conformers.return_centroids(mol_3d, clusters)
```

**Cálculo de SASA**:
```python
# Calcular área de superfície acessível ao solvente
sasa_values = dm.conformers.sasa(mol_3d, n_jobs=-1)

# Acessar SASA a partir de propriedades do conformador
conf = mol_3d.GetConformer(0)
sasa = conf.GetDoubleProp('rdkit_free_sasa')
```

### 9. Visualização

Consulte `references/descriptors_viz.md` para documentação de visualização.

**Grade básica de moléculas**:
```python
# Visualizar moléculas
dm.viz.to_image(
    mols[:20],
    legends=[dm.to_smiles(m) for m in mols[:20]],
    n_cols=5,
    mol_size=(300, 300)
)

# Salvar em arquivo
dm.viz.to_image(mols, outfile="molecules.png")

# SVG para publicações
dm.viz.to_image(mols, outfile="molecules.svg", use_svg=True)
```

**Visualização alinhada** (para análise SAR):
```python
# Alinhar moléculas por subestrutura comum
dm.viz.to_image(
    similar_mols,
    align=True,  # Ativar alinhamento MCS
    legends=activity_labels,
    n_cols=4
)
```

**Destacando subestruturas**:
```python
# Destacar átomos e ligações específicos
dm.viz.to_image(
    mol,
    highlight_atom=[0, 1, 2, 3],  # Índices de átomos
    highlight_bond=[0, 1, 2]      # Índices de ligações
)
```

**Visualização de conformadores**:
```python
# Exibir múltiplos conformadores
dm.viz.conformers(
    mol_3d,
    n_confs=10,
    align_conf=True,
    n_cols=3
)
```

### 10. Reações Químicas

Consulte `references/reactions_data.md` para documentação de reações.

**Aplicando reações**:
```python
from rdkit.Chem import rdChemReactions

# Definir reação a partir de SMARTS
rxn_smarts = '[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[Cl:3]'
rxn = rdChemReactions.ReactionFromSmarts(rxn_smarts)

# Aplicar à molécula
reactant = dm.to_mol("CC(=O)O")  # Ácido acético
product = dm.reactions.apply_reaction(
    rxn,
    (reactant,),
    sanitize=True
)

# Converter para SMILES
product_smiles = dm.to_smiles(product)
```

**Aplicação de reação em lote**:
```python
# Aplicar reação à biblioteca
products = []
for mol in reactant_mols:
    try:
        prod = dm.reactions.apply_reaction(rxn, (mol,))
        if prod is not None:
            products.append(prod)
    except Exception as e:
        print(f"Falha na reação: {e}")
```

## Paralelização

Datamol inclui paralelização integrada para muitas operações. Use o parâmetro `n_jobs`:
- `n_jobs=1`: Sequencial (sem paralelização)
- `n_jobs=-1`: Usar todos os núcleos da CPU disponíveis
- `n_jobs=4`: Usar 4 núcleos

**Funções que suportam paralelização**:
- `dm.read_sdf(..., n_jobs=-1)`
- `dm.descriptors.batch_compute_many_descriptors(..., n_jobs=-1)`
- `dm.cluster_mols(..., n_jobs=-1)`
- `dm.pdist(..., n_jobs=-1)`
- `dm.conformers.sasa(..., n_jobs=-1)`

**Barras de progresso**: Muitas operações em lote suportam o parâmetro `progress=True`.

## Fluxos de Trabalho Comuns e Padrões

### Pipeline Completo: Carregamento de Dados → Filtragem → Análise

```python
import datamol as dm
import pandas as pd

# 1. Carregar moléculas
df = dm.read_sdf("compounds.sdf")

# 2. Padronizar
df['mol'] = df['mol'].apply(lambda m: dm.standardize_mol(m) if m else None)
df = df[df['mol'].notna()]  # Remover moléculas que falharam

# 3. Computar descritores
desc_df = dm.descriptors.batch_compute_many_descriptors(
    df['mol'].tolist(),
    n_jobs=-1,
    progress=True
)

# 4. Filtrar por semelhança a fármacos
druglike = (
    (desc_df['mw'] <= 500) &
    (desc_df['logp'] <= 5) &
    (desc_df['hbd'] <= 5) &
    (desc_df['hba'] <= 10)
)
filtered_df = df[druglike]

# 5. Agrupar e selecionar subconjunto diverso
diverse_mols = dm.pick_diverse(
    filtered_df['mol'].tolist(),
    npick=100
)

# 6. Visualizar resultados
dm.viz.to_image(
    diverse_mols,
    legends=[dm.to_smiles(m) for m in diverse_mols],
    outfile="diverse_compounds.png",
    n_cols=10
)
```

### Análise de Relação Estrutura-Atividade (SAR)

```python
# Agrupar por scaffold
scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Criar DataFrame com atividades
sar_df = pd.DataFrame({
    'mol': mols,
    'scaffold': scaffold_smiles,
    'activity': activities  # Dados de atividade fornecidos pelo usuário
})

# Analisar cada série de scaffold
for scaffold, group in sar_df.groupby('scaffold'):
    if len(group) >= 3:  # Precisar de múltiplos exemplos
        print(f"\nScaffold: {scaffold}")
        print(f"Contagem: {len(group)}")
        print(f"Intervalo de atividade: {group['activity'].min():.2f} - {group['activity'].max():.2f}")

        # Visualizar com atividades como legendas
        dm.viz.to_image(
            group['mol'].tolist(),
            legends=[f"Atividade: {act:.2f}" for act in group['activity']],
            align=True  # Alinhar por subestrutura comum
        )
```

### Pipeline de Triagem Virtual

```python
# 1. Gerar fingerprints para consulta e biblioteca
query_fps = [dm.to_fp(mol) for mol in query_actives]
library_fps = [dm.to_fp(mol) for mol in library_mols]

# 2. Calcular similaridades
from scipy.spatial.distance import cdist
import numpy as np

distances = dm.cdist(query_actives, library_mols, n_jobs=-1)

# 3. Encontrar correspondências mais próximas (distância mínima para qualquer consulta)
min_distances = distances.min(axis=0)
similarities = 1 - min_distances  # Converter distância para similaridade

# 4. Classificar e selecionar principais sucessos
top_indices = np.argsort(similarities)[::-1][:100]  # Top 100
top_hits = [library_mols[i] for i in top_indices]
top_scores = [similarities[i] for i in top_indices]

# 5. Visualizar sucessos
dm.viz.to_image(
    top_hits[:20],
    legends=[f"Sim: {score:.3f}" for score in top_scores[:20]],
    outfile="screening_hits.png"
)
```

## Documentação de Referência

Para documentação detalhada da API, consulte estes arquivos de referência:

- **`references/core_api.md`**: Funções do namespace principal (conversões, padronização, fingerprints, clustering)
- **`references/io_module.md`**: Operações de I/O de arquivo (ler/escrever SDF, CSV, Excel, arquivos remotos)
- **`references/conformers_module.md`**: Geração de conformadores 3D, clustering, cálculos de SASA
- **`references/descriptors_viz.md`**: Descritores moleculares e funções de visualização
- **`references/fragments_scaffolds.md`**: Extração de scaffold, fragmentação BRICS/RECAP
- **`references/reactions_data.md`**: Reações químicas e datasets de brinquedo

## Boas Práticas

1. **Sempre padronize moléculas** de fontes externas:
   ```python
   mol = dm.standardize_mol(mol, disconnect_metals=True, normalize=True, reionize=True)
   ```

2. **Verifique valores None** após análise de moléculas:
   ```python
   mol = dm.to_mol(smiles)
   if mol is None:
       # Tratar SMILES inválido
   ```

3. **Use processamento paralelo** para datasets grandes:
   ```python
   result = dm.operation(..., n_jobs=-1, progress=True)
   ```

4. **Aproveite fsspec** para armazenamento em nuvem:
   ```python
   df = dm.read_sdf("s3://bucket/compounds.sdf")
   ```

5. **Use fingerprints apropriados** para similaridade:
   - ECFP (Morgan): Propósito geral, similaridade estrutural
   - MACCS: Rápido, espaço de características menor
   - Atom pairs: Considera pares de átomos e distâncias

6. **Considere limitações de escala**:
   - Clustering Butina: ~1.000 moléculas (matriz de distância completa)
   - Para datasets maiores: Use seleção de diversidade ou métodos hierárquicos

7. **Divisão por scaffold para ML**: Garantir separação adequada treino/teste por scaffold

8. **Alinhe moléculas** ao visualizar séries SAR

## Tratamento de Erros

```python
# Criação segura de moléculas
def safe_to_mol(smiles):
    try:
        mol = dm.to_mol(smiles)
        if mol is not None:
            mol = dm.standardize_mol(mol)
        return mol
    except Exception as e:
        print(f"Falha ao processar {smiles}: {e}")
        return None

# Processamento em lote seguro
valid_mols = []
for smiles in smiles_list:
    mol = safe_to_mol(smiles)
    if mol is not None:
        valid_mols.append(mol)
```

## Integração com Aprendizado de Máquina

```python
# Geração de features
X = np.array([dm.to_fp(mol) for mol in mols])

# Ou descritores
desc_df = dm.descriptors.batch_compute_many_descriptors(mols, n_jobs=-1)
X = desc_df.values

# Treinar modelo
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X, y_target)

# Prever
predictions = model.predict(X_test)
```

## Resolução de Problemas

**Problema**: Falha na análise de moléculas
- **Solução**: Use `dm.standardize_smiles()` primeiro ou tente `dm.fix_mol()`

**Problema**: Erros de memória com clustering
- **Solução**: Use `dm.pick_diverse()` em vez de clustering completo para conjuntos grandes

**Problema**: Geração de conformadores lenta
- **Solução**: Reduza `n_confs` ou aumente `rms_cutoff` para gerar menos conformadores

**Problema**: Falha no acesso a arquivo remoto
- **Solução**: Certifique-se de que fsspec e as bibliotecas apropriadas do provedor de nuvem estão instaladas (s3fs, gcsfs, etc.)

## Recursos Adicionais

- **Documentação Datamol**: https://docs.datamol.io/
- **Documentação RDKit**: https://www.rdkit.org/docs/
- **Repositório GitHub**: https://github.com/datamol-io/datamol