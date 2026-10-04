---
name: rdkit
description: "Kit de ferramentas de quiminformática para controle molecular refinado. Análise de SMILES/SDF, descritores (MW, LogP, TPSA), fingerprints, busca de subestruturas, geração 2D/3D, similaridade, reações. Para fluxos de trabalho padrão com interface mais simples, use datamol (wrapper do RDKit). Use rdkit para controle avançado, sanitização customizada, algoritmos especializados."
---

# Kit de Ferramentas de Quiminformática RDKit

## Visão Geral

RDKit é uma biblioteca abrangente de quiminformática fornecendo APIs Python para análise e manipulação de moléculas. Esta habilidade fornece orientações para leitura/escrita de estruturas moleculares, cálculo de descritores, fingerprinting, busca de subestruturas, reações químicas, geração de coordenadas 2D/3D e visualização molecular. Use esta habilidade para descoberta de medicamentos, química computacional e tarefas de pesquisa quiminformática.

## Capacidades Principais

### 1. I/O Molecular e Criação

**Leitura de Moléculas:**

Leia estruturas moleculares de vários formatos:

```python
from rdkit import Chem

# De strings SMILES
mol = Chem.MolFromSmiles('Cc1ccccc1')  # Retorna objeto Mol ou None

# De arquivos MOL
mol = Chem.MolFromMolFile('path/to/file.mol')

# De blocos MOL (dados em string)
mol = Chem.MolFromMolBlock(mol_block_string)

# De InChI
mol = Chem.MolFromInchi('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H')
```

**Escrita de Moléculas:**

Converta moléculas em representações textuais:

```python
# Para SMILES canônico
smiles = Chem.MolToSmiles(mol)

# Para bloco MOL
mol_block = Chem.MolToMolBlock(mol)

# Para InChI
inchi = Chem.MolToInchi(mol)
```

**Processamento em Lote:**

Para processar múltiplas moléculas, use objetos Supplier/Writer:

```python
# Leia arquivos SDF
suppl = Chem.SDMolSupplier('molecules.sdf')
for mol in suppl:
    if mol is not None:  # Verifique erros de análise
        # Processe a molécula
        pass

# Leia arquivos SMILES
suppl = Chem.SmilesMolSupplier('molecules.smi', titleLine=False)

# Para arquivos grandes ou dados comprimidos
with gzip.open('molecules.sdf.gz') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Processe a molécula
        pass

# Processamento multithreaded para grandes conjuntos de dados
suppl = Chem.MultithreadedSDMolSupplier('molecules.sdf')

# Escreva moléculas em SDF
writer = Chem.SDWriter('output.sdf')
for mol in molecules:
    writer.write(mol)
writer.close()
```

**Notas Importantes:**
- Todas as funções `MolFrom*` retornam `None` em caso de falha com mensagens de erro
- Sempre verifique se há `None` antes de processar moléculas
- Moléculas são automaticamente sanitizadas na importação (valida valência, percebe aromaticidade)

### 2. Sanitização e Validação Molecular

RDKit sanitiza automaticamente moléculas durante a análise, executando 13 etapas incluindo verificação de valência, percepção de aromaticidade e atribuição de quiralidade.

**Controle de Sanitização:**

```python
# Desabilite sanitização automática
mol = Chem.MolFromSmiles('C1=CC=CC=C1', sanitize=False)

# Sanitização manual
Chem.SanitizeMol(mol)

# Detecte problemas antes da sanitização
problems = Chem.DetectChemistryProblems(mol)
for problem in problems:
    print(problem.GetType(), problem.Message())

# Sanitização parcial (pule etapas específicas)
from rdkit.Chem import rdMolStandardize
Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL ^ Chem.SANITIZE_PROPERTIES)
```

**Problemas de Sanitização Comuns:**
- Átomos com valência explícita excedentem máximo permitido levantarão exceções
- Anéis aromáticos inválidos causarão erros de kekulização
- Elétrons radicais podem não ser corretamente atribuídos sem especificação explícita

### 3. Análise e Propriedades Moleculares

**Acessando Estrutura Molecular:**

```python
# Itere átomos e ligações
for atom in mol.GetAtoms():
    print(atom.GetSymbol(), atom.GetIdx(), atom.GetDegree())

for bond in mol.GetBonds():
    print(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType())

# Informação de anéis
ring_info = mol.GetRingInfo()
ring_info.NumRings()
ring_info.AtomRings()  # Retorna tuplas de índices de átomos

# Verifique se átomo está em anel
atom = mol.GetAtomWithIdx(0)
atom.IsInRing()
atom.IsInRingSize(6)  # Verifique anéis de 6 membros

# Encontre o menor conjunto de anéis menores (SSSR)
from rdkit.Chem import GetSymmSSSR
rings = GetSymmSSSR(mol)
```

**Estereoquímica:**

```python
# Encontre centros quirais
from rdkit.Chem import FindMolChiralCenters
chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
# Retorna lista de tuplas (atom_idx, chirality)

# Atribua estereoquímica a partir de coordenadas 3D
from rdkit.Chem import AssignStereochemistryFrom3D
AssignStereochemistryFrom3D(mol)

# Verifique estereoquímica de ligação
bond = mol.GetBondWithIdx(0)
stereo = bond.GetStereo()  # STEREONONE, STEREOZ, STEREOE, etc.
```

**Análise de Fragmentos:**

```python
# Obtenha fragmentos desconectados
frags = Chem.GetMolFrags(mol, asMols=True)

# Fragmente em ligações específicas
from rdkit.Chem import FragmentOnBonds
frag_mol = FragmentOnBonds(mol, [bond_idx1, bond_idx2])

# Conte sistemas de anéis
from rdkit.Chem.Scaffolds import MurckoScaffold
scaffold = MurckoScaffold.GetScaffoldForMol(mol)
```

### 4. Descritores e Propriedades Moleculares

**Descritores Básicos:**

```python
from rdkit.Chem import Descriptors

# Peso molecular
mw = Descriptors.MolWt(mol)
exact_mw = Descriptors.ExactMolWt(mol)

# LogP (lipofilicidade)
logp = Descriptors.MolLogP(mol)

# Área de superfície polar topológica
tpsa = Descriptors.TPSA(mol)

# Número de doadores/aceitadores de ligação de hidrogênio
hbd = Descriptors.NumHDonors(mol)
hba = Descriptors.NumHAcceptors(mol)

# Número de ligações rotatórias
rot_bonds = Descriptors.NumRotatableBonds(mol)

# Número de anéis aromáticos
aromatic_rings = Descriptors.NumAromaticRings(mol)
```

**Cálculo de Descritores em Lote:**

```python
# Calcule todos os descritores de uma vez
all_descriptors = Descriptors.CalcMolDescriptors(mol)
# Retorna dicionário: {'MolWt': 180.16, 'MolLogP': 1.23, ...}

# Obtenha lista de nomes de descritores disponíveis
descriptor_names = [desc[0] for desc in Descriptors._descList]
```

**Regra de Cinco de Lipinski:**

```python
# Verifique similaridade com droga
mw = Descriptors.MolWt(mol) <= 500
logp = Descriptors.MolLogP(mol) <= 5
hbd = Descriptors.NumHDonors(mol) <= 5
hba = Descriptors.NumHAcceptors(mol) <= 10

is_drug_like = mw and logp and hbd and hba
```

### 5. Fingerprints e Similaridade Molecular

**Tipos de Fingerprint:**

```python
from rdkit.Chem import AllChem, RDKFingerprint
from rdkit.Chem.AtomPairs import Pairs, Torsions
from rdkit.Chem import MACCSkeys

# Fingerprint topológico RDKit
fp = Chem.RDKFingerprint(mol)

# Fingerprints Morgan (fingerprints circulares, similares a ECFP)
fp = AllChem.GetMorganFingerprint(mol, radius=2)
fp_bits = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)

# Chaves MACCS (chave estrutural de 166 bits)
fp = MACCSkeys.GenMACCSKeys(mol)

# Fingerprints de pares de átomos
fp = Pairs.GetAtomPairFingerprint(mol)

# Fingerprints de torção topológica
fp = Torsions.GetTopologicalTorsionFingerprint(mol)

# Fingerprints Avalon (se disponível)
from rdkit.Avalon import pyAvalonTools
fp = pyAvalonTools.GetAvalonFP(mol)
```

**Cálculo de Similaridade:**

```python
from rdkit import DataStructs

# Calcule similaridade de Tanimoto
fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, radius=2)
fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, radius=2)
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)

# Calcule similaridade para múltiplas moléculas
similarities = DataStructs.BulkTanimotoSimilarity(fp1, [fp2, fp3, fp4])

# Outras métricas de similaridade
dice = DataStructs.DiceSimilarity(fp1, fp2)
cosine = DataStructs.CosineSimilarity(fp1, fp2)
```

**Clustering e Diversidade:**

```python
# Clustering de Butina baseado em similaridade de fingerprint
from rdkit.ML.Cluster import Butina

# Calcule matriz de distância
dists = []
fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2) for mol in mols]
for i in range(len(fps)):
    sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i])
    dists.extend([1-sim for sim in sims])

# Agrupe com limiar de distância
clusters = Butina.ClusterData(dists, len(fps), distThresh=0.3, isDistData=True)
```

### 6. Busca de Subestruturas e SMARTS

**Correspondência Básica de Subestruturas:**

```python
# Defina query usando SMARTS
query = Chem.MolFromSmarts('[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1')  # Anel benzeno

# Verifique se molécula contém subestrutura
has_match = mol.HasSubstructMatch(query)

# Obtenha todas as correspondências (retorna tupla de tuplas com índices de átomos)
matches = mol.GetSubstructMatches(query)

# Obtenha apenas primeira correspondência
match = mol.GetSubstructMatch(query)
```

**Padrões SMARTS Comuns:**

```python
# Álcoois primários
primary_alcohol = Chem.MolFromSmarts('[CH2][OH1]')

# Ácidos carboxílicos
carboxylic_acid = Chem.MolFromSmarts('C(=O)[OH]')

# Amidas
amide = Chem.MolFromSmarts('C(=O)N')

# Heterociclos aromáticos
aromatic_n = Chem.MolFromSmarts('[nR]')  # Nitrogênio aromático em anel

# Macrociclos (anéis > 12 átomos)
macrocycle = Chem.MolFromSmarts('[r{12-}]')
```

**Regras de Correspondência:**
- Propriedades não especificadas em query correspondem a qualquer valor em target
- Hidrogênios são ignorados a menos que explicitamente especificados
- Átomo query carregado não corresponde a átomo target descarregado
- Átomo query aromático não corresponde a átomo target alifático (a menos que query seja genérica)

### 7. Reações Químicas

**SMARTS de Reação:**

```python
from rdkit.Chem import AllChem

# Defina reação usando SMARTS: reagentes >> produtos
rxn = AllChem.ReactionFromSmarts('[C:1]=[O:2]>>[C:1][O:2]')  # Redução de cetona

# Aplique reação a moléculas
reactants = (mol1,)
products = rxn.RunReactants(reactants)

# Produtos é tupla de tuplas (uma tupla por conjunto de produtos)
for product_set in products:
    for product in product_set:
        # Sanitize produto
        Chem.SanitizeMol(product)
```

**Características de Reação:**
- Mapeamento de átomos preserva átomos específicos entre reagentes e produtos
- Átomos dummy em produtos são substituídos por átomos correspondentes de reagentes
- Ligações "any" herdam ordem de ligação de reagentes
- Quiralidade preservada a menos que explicitamente alterada

**Similaridade de Reação:**

```python
# Gere fingerprints de reação
fp = AllChem.CreateDifferenceFingerprintForReaction(rxn)

# Compare reações
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
```

### 8. Geração de Coordenadas 2D e 3D

**Geração de Coordenadas 2D:**

```python
from rdkit.Chem import AllChem

# Gere coordenadas 2D para representação
AllChem.Compute2DCoords(mol)

# Alinhe molécula a estrutura modelo
template = Chem.MolFromSmiles('c1ccccc1')
AllChem.Compute2DCoords(template)
AllChem.GenerateDepictionMatching2DStructure(mol, template)
```

**Geração de Coordenadas 3D e Conformadores:**

```python
# Gere conformador 3D único usando ETKDG
AllChem.EmbedMolecule(mol, randomSeed=42)

# Gere múltiplos conformadores
conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=10, randomSeed=42)

# Otimize geometria com campo de força
AllChem.UFFOptimizeMolecule(mol)  # Campo de força UFF
AllChem.MMFFOptimizeMolecule(mol)  # Campo de força MMFF94

# Otimize todos os conformadores
for conf_id in conf_ids:
    AllChem.MMFFOptimizeMolecule(mol, confId=conf_id)

# Calcule RMSD entre conformadores
from rdkit.Chem import AllChem
rms = AllChem.GetConformerRMS(mol, conf_id1, conf_id2)

# Alinhe moléculas
AllChem.AlignMol(probe_mol, ref_mol)
```

**Embedding Constrangido:**

```python
# Embed com parte de molécula constrangida a coordenadas específicas
AllChem.ConstrainedEmbed(mol, core_mol)
```

### 9. Visualização Molecular

**Desenho Básico:**

```python
from rdkit.Chem import Draw

# Desenhe molécula única para imagem PIL
img = Draw.MolToImage(mol, size=(300, 300))
img.save('molecule.png')

# Desenhe diretamente para arquivo
Draw.MolToFile(mol, 'molecule.png')

# Desenhe múltiplas moléculas em grade
mols = [mol1, mol2, mol3, mol4]
img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(200, 200))
```

**Destacando Subestruturas:**

```python
# Destaque correspondência de subestrutura
query = Chem.MolFromSmarts('c1ccccc1')
match = mol.GetSubstructMatch(query)

img = Draw.MolToImage(mol, highlightAtoms=match)

# Cores de destaque customizadas
highlight_colors = {atom_idx: (1, 0, 0) for atom_idx in match}  # Vermelho
img = Draw.MolToImage(mol, highlightAtoms=match,
                      highlightAtomColors=highlight_colors)
```

**Customizando Visualização:**

```python
from rdkit.Chem.Draw import rdMolDraw2D

# Crie drawer com opções customizadas
drawer = rdMolDraw2D.MolDraw2DCairo(300, 300)
opts = drawer.drawOptions()

# Customize opções
opts.addAtomIndices = True
opts.addStereoAnnotation = True
opts.bondLineWidth = 2

# Desenhe molécula
drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Salve em arquivo
with open('molecule.png', 'wb') as f:
    f.write(drawer.GetDrawingText())
```

**Integração com Jupyter Notebook:**

```python
# Habilite exibição inline em Jupyter
from rdkit.Chem.Draw import IPythonConsole

# Customize exibição padrão
IPythonConsole.ipython_useSVG = True  # Use SVG em vez de PNG
IPythonConsole.molSize = (300, 300)   # Tamanho padrão

# Moléculas agora exibem automaticamente
mol  # Mostra imagem de molécula
```

**Visualizando Bits de Fingerprint:**

```python
# Mostre que características moleculares um bit de fingerprint representa
from rdkit.Chem import Draw

# Para fingerprints Morgan
bit_info = {}
fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, bitInfo=bit_info)

# Desenhe ambiente para bit específico
img = Draw.DrawMorganBit(mol, bit_id, bit_info)
```

### 10. Modificação Molecular

**Adicionando/Removendo Hidrogênios:**

```python
# Adicione hidrogênios explícitos
mol_h = Chem.AddHs(mol)

# Remova hidrogênios explícitos
mol = Chem.RemoveHs(mol_h)
```

**Kekulização e Aromaticidade:**

```python
# Converta ligações aromáticas em alternância simples/dupla
Chem.Kekulize(mol)

# Configure aromaticidade
Chem.SetAromaticity(mol)
```

**Substituindo Subestruturas:**

```python
# Substitua subestrutura por outra estrutura
query = Chem.MolFromSmarts('c1ccccc1')  # Benzeno
replacement = Chem.MolFromSmiles('C1CCCCC1')  # Ciclohexano

new_mol = Chem.ReplaceSubstructs(mol, query, replacement)[0]
```

**Neutralizando Cargas:**

```python
# Remova cargas formais adicionando/removendo hidrogênios
from rdkit.Chem.MolStandardize import rdMolStandardize

# Usando Uncharger
uncharger = rdMolStandardize.Uncharger()
mol_neutral = uncharger.uncharge(mol)
```

### 11. Trabalhando com Hashes Moleculares e Padronização

**Hashing Molecular:**

```python
from rdkit.Chem import rdMolHash

# Gere hash do scaffold de Murcko
scaffold_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.MurckoScaffold)

# Hash de SMILES canônico
canonical_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.CanonicalSmiles)

# Hash de regioisômero (ignora estereoquímica)
regio_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.Regioisomer)
```

**SMILES Randomizado:**

```python
# Gere representações SMILES aleatórias (para aumento de dados)
from rdkit.Chem import MolToRandomSmilesVect

random_smiles = MolToRandomSmilesVect(mol, numSmiles=10, randomSeed=42)
```

### 12. Características Farmacofóricas e 3D

**Características Farmacofóricas:**

```python
from rdkit.Chem import ChemicalFeatures
from rdkit import RDConfig
import os

# Carregue fábrica de características
fdef_path = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_path)

# Obtenha características farmacofóricas
features = factory.GetFeaturesForMol(mol)

for feat in features:
    print(feat.GetFamily(), feat.GetType(), feat.GetAtomIds())
```

## Fluxos de Trabalho Comuns

### Análise de Similaridade com Medicamentos

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def analyze_druglikeness(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Calcule descritores de Lipinski
    results = {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol)
    }

    # Verifique Regra de Cinco de Lipinski
    results['Lipinski'] = (
        results['MW'] <= 500 and
        results['LogP'] <= 5 and
        results['HBD'] <= 5 and
        results['HBA'] <= 10
    )

    return results
```

### Triagem de Similaridade

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs

def similarity_screen(query_smiles, database_smiles, threshold=0.7):
    query_mol = Chem.MolFromSmiles(query_smiles)
    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2)

    hits = []
    for idx, smiles in enumerate(database_smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            if sim >= threshold:
                hits.append((idx, smiles, sim))

    return sorted(hits, key=lambda x: x[2], reverse=True)
```

### Filtragem por Subestrutura

```python
from rdkit import Chem

def filter_by_substructure(smiles_list, pattern_smarts):
    query = Chem.MolFromSmarts(pattern_smarts)

    hits = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol and mol.HasSubstructMatch(query):
            hits.append(smiles)

    return hits
```

## Melhores Práticas

### Tratamento de Erros

Sempre verifique se há `None` ao analisar moléculas:

```python
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    print(f"Falha ao analisar: {smiles}")
    continue
```

### Otimização de Performance

**Use formatos binários para armazenamento:**

```python
import pickle

# Pickle moléculas para carregamento rápido
with open('molecules.pkl', 'wb') as f:
    pickle.dump(mols, f)

# Carregue moléculas pickled (muito mais rápido que reanalisar)
with open('molecules.pkl', 'rb') as f:
    mols = pickle.load(f)
```

**Use operações em lote:**

```python
# Calcule fingerprints para todas as moléculas de uma vez
fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2) for mol in mols]

# Use cálculos de similaridade em lote
similarities = DataStructs.BulkTanimotoSimilarity(fps[0], fps[1:])
```

### Segurança em Thread

Operações RDKit são geralmente thread-safe para:
- I/O molecular (SMILES, blocos mol)
- Geração de coordenadas
- Fingerprinting e descritores
- Busca de subestruturas
- Reações
- Desenho

**Não thread-safe:** MolSuppliers quando acessados concorrentemente.

### Gerenciamento de Memória

Para grandes conjuntos de dados:

```python
# Use ForwardSDMolSupplier para evitar carregar arquivo inteiro
with open('large.sdf') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Processe uma molécula por vez
        pass

# Use MultithreadedSDMolSupplier para processamento paralelo
suppl = Chem.MultithreadedSDMolSupplier('large.sdf', numWriterThreads=4)
```

## Armadilhas Comuns

1. **Esquecer de verificar se há None:** Sempre valide moléculas após análise
2. **Falhas de sanitização:** Use `DetectChemistryProblems()` para depurar
3. **Hidrogênios faltando:** Use `AddHs()` ao calcular propriedades que dependem de hidrogênio
4. **2D vs 3D:** Gere coordenadas apropriadas antes de visualização ou análise 3D
5. **Regras de correspondência SMARTS:** Lembre-se que propriedades não especificadas correspondem a qualquer coisa
6. **Segurança em thread com MolSuppliers:** Não compartilhe objetos supplier entre threads

## Recursos

### references/

Esta habilidade inclui documentação de referência de API detalhada:

- `api_reference.md` - Listagem abrangente de módulos, funções e classes RDKit organizadas por funcionalidade
- `descriptors_reference.md` - Lista completa de descritores moleculares disponíveis com descrições
- `smarts_patterns.md` - Padrões SMARTS comuns para grupos funcionais e características estruturais

Carregue estas referências ao precisar de detalhes de API específicos, informações de parâmetros ou exemplos de padrões.

### scripts/

Scripts de exemplo para fluxos de trabalho RDKit comuns:

- `molecular_properties.py` - Calcule propriedades moleculares abrangentes e descritores
- `similarity_search.py` - Realize triagem de similaridade baseada em fingerprint
- `substructure_filter.py` - Filtre moléculas por padrões de subestrutura

Estes scripts podem ser executados diretamente ou usados como templates para fluxos de trabalho customizados.