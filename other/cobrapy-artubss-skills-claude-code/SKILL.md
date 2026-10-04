---
name: cobrapy
description: "Modelagem metabólica baseada em restrições (COBRA). FBA, FVA, knockouts de genes, amostragem de fluxo, modelos SBML, para análise de biologia de sistemas e engenharia metabólica."
---

# COBRApy - Reconstrução e Análise Baseada em Restrições

## Visão Geral

COBRApy é uma biblioteca Python para reconstrução e análise baseada em restrições (COBRA) de modelos metabólicos, essencial para pesquisa em biologia de sistemas. Trabalhe com modelos metabólicos em escala de genoma, realize simulações computacionais do metabolismo celular, conduza análises de engenharia metabólica e preveja comportamentos fenotípicos.

## Capacidades Principais

COBRApy oferece ferramentas abrangentes organizadas em várias áreas principais:

### 1. Gerenciamento de Modelos

Carregue modelos existentes de repositórios ou arquivos:
```python
from cobra.io import load_model

# Load bundled test models
model = load_model("textbook")  # E. coli core model
model = load_model("ecoli")     # Full E. coli model
model = load_model("salmonella")

# Load from files
from cobra.io import read_sbml_model, load_json_model, load_yaml_model
model = read_sbml_model("path/to/model.xml")
model = load_json_model("path/to/model.json")
model = load_yaml_model("path/to/model.yml")
```

Salve modelos em vários formatos:
```python
from cobra.io import write_sbml_model, save_json_model, save_yaml_model
write_sbml_model(model, "output.xml")  # Preferred format
save_json_model(model, "output.json")  # For Escher compatibility
save_yaml_model(model, "output.yml")   # Human-readable
```

### 2. Estrutura e Componentes do Modelo

Acesse e inspecione componentes do modelo:
```python
# Access components
model.reactions      # DictList of all reactions
model.metabolites    # DictList of all metabolites
model.genes          # DictList of all genes

# Get specific items by ID or index
reaction = model.reactions.get_by_id("PFK")
metabolite = model.metabolites[0]

# Inspect properties
print(reaction.reaction)        # Stoichiometric equation
print(reaction.bounds)          # Flux constraints
print(reaction.gene_reaction_rule)  # GPR logic
print(metabolite.formula)       # Chemical formula
print(metabolite.compartment)   # Cellular location
```

### 3. Análise de Equilíbrio de Fluxo (FBA)

Execute simulação padrão de FBA:
```python
# Basic optimization
solution = model.optimize()
print(f"Objective value: {solution.objective_value}")
print(f"Status: {solution.status}")

# Access fluxes
print(solution.fluxes["PFK"])
print(solution.fluxes.head())

# Fast optimization (objective value only)
objective_value = model.slim_optimize()

# Change objective
model.objective = "ATPM"
solution = model.optimize()
```

FBA parcimonioso (minimizar fluxo total):
```python
from cobra.flux_analysis import pfba
solution = pfba(model)
```

FBA geométrico (encontrar solução central):
```python
from cobra.flux_analysis import geometric_fba
solution = geometric_fba(model)
```

### 4. Análise de Variabilidade de Fluxo (FVA)

Determine intervalos de fluxo para todas as reações:
```python
from cobra.flux_analysis import flux_variability_analysis

# Standard FVA
fva_result = flux_variability_analysis(model)

# FVA at 90% optimality
fva_result = flux_variability_analysis(model, fraction_of_optimum=0.9)

# Loopless FVA (eliminates thermodynamically infeasible loops)
fva_result = flux_variability_analysis(model, loopless=True)

# FVA for specific reactions
fva_result = flux_variability_analysis(
    model,
    reaction_list=["PFK", "FBA", "PGI"]
)
```

### 5. Estudos de Deleção de Gene e Reação

Realize análises de knockout:
```python
from cobra.flux_analysis import (
    single_gene_deletion,
    single_reaction_deletion,
    double_gene_deletion,
    double_reaction_deletion
)

# Single deletions
gene_results = single_gene_deletion(model)
reaction_results = single_reaction_deletion(model)

# Double deletions (uses multiprocessing)
double_gene_results = double_gene_deletion(
    model,
    processes=4  # Number of CPU cores
)

# Manual knockout using context manager
with model:
    model.genes.get_by_id("b0008").knock_out()
    solution = model.optimize()
    print(f"Growth after knockout: {solution.objective_value}")
# Model automatically reverts after context exit
```

### 6. Meio de Crescimento e Meio Mínimo

Gerencie o meio de crescimento:
```python
# View current medium
print(model.medium)

# Modify medium (must reassign entire dict)
medium = model.medium
medium["EX_glc__D_e"] = 10.0  # Set glucose uptake
medium["EX_o2_e"] = 0.0       # Anaerobic conditions
model.medium = medium

# Calculate minimal media
from cobra.medium import minimal_medium

# Minimize total import flux
min_medium = minimal_medium(model, minimize_components=False)

# Minimize number of components (uses MILP, slower)
min_medium = minimal_medium(
    model,
    minimize_components=True,
    open_exchanges=True
)
```

### 7. Amostragem de Fluxo

Amostre o espaço de fluxo viável:
```python
from cobra.sampling import sample

# Sample using OptGP (default, supports parallel processing)
samples = sample(model, n=1000, method="optgp", processes=4)

# Sample using ACHR
samples = sample(model, n=1000, method="achr")

# Validate samples
from cobra.sampling import OptGPSampler
sampler = OptGPSampler(model, processes=4)
sampler.sample(1000)
validation = sampler.validate(sampler.samples)
print(validation.value_counts())  # Should be all 'v' for valid
```

### 8. Envelopes de Produção

Calcule planos de fase de fenótipo:
```python
from cobra.flux_analysis import production_envelope

# Standard production envelope
envelope = production_envelope(
    model,
    reactions=["EX_glc__D_e", "EX_o2_e"],
    objective="EX_ac_e"  # Acetate production
)

# With carbon yield
envelope = production_envelope(
    model,
    reactions=["EX_glc__D_e", "EX_o2_e"],
    carbon_sources="EX_glc__D_e"
)

# Visualize (use matplotlib or pandas plotting)
import matplotlib.pyplot as plt
envelope.plot(x="EX_glc__D_e", y="EX_o2_e", kind="scatter")
plt.show()
```

### 9. Preenchimento de Lacunas

Adicione reações para tornar modelos viáveis:
```python
from cobra.flux_analysis import gapfill

# Prepare universal model with candidate reactions
universal = load_model("universal")

# Perform gapfilling
with model:
    # Remove reactions to create gaps for demonstration
    model.remove_reactions([model.reactions.PGI])

    # Find reactions needed
    solution = gapfill(model, universal)
    print(f"Reactions to add: {solution}")
```

### 10. Construção de Modelos

Construa modelos do zero:
```python
from cobra import Model, Reaction, Metabolite

# Create model
model = Model("my_model")

# Create metabolites
atp_c = Metabolite("atp_c", formula="C10H12N5O13P3",
                   name="ATP", compartment="c")
adp_c = Metabolite("adp_c", formula="C10H12N5O10P2",
                   name="ADP", compartment="c")
pi_c = Metabolite("pi_c", formula="HO4P",
                  name="Phosphate", compartment="c")

# Create reaction
reaction = Reaction("ATPASE")
reaction.name = "ATP hydrolysis"
reaction.subsystem = "Energy"
reaction.lower_bound = 0.0
reaction.upper_bound = 1000.0

# Add metabolites with stoichiometry
reaction.add_metabolites({
    atp_c: -1.0,
    adp_c: 1.0,
    pi_c: 1.0
})

# Add gene-reaction rule
reaction.gene_reaction_rule = "(gene1 and gene2) or gene3"

# Add to model
model.add_reactions([reaction])

# Add boundary reactions
model.add_boundary(atp_c, type="exchange")
model.add_boundary(adp_c, type="demand")

# Set objective
model.objective = "ATPASE"
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Carregar Modelo e Prever Crescimento

```python
from cobra.io import load_model

# Load model
model = load_model("ecoli")

# Run FBA
solution = model.optimize()
print(f"Growth rate: {solution.objective_value:.3f} /h")

# Show active pathways
print(solution.fluxes[solution.fluxes.abs() > 1e-6])
```

### Fluxo de Trabalho 2: Triagem de Knockout de Gene

```python
from cobra.io import load_model
from cobra.flux_analysis import single_gene_deletion

# Load model
model = load_model("ecoli")

# Perform single gene deletions
results = single_gene_deletion(model)

# Find essential genes (growth < threshold)
essential_genes = results[results["growth"] < 0.01]
print(f"Found {len(essential_genes)} essential genes")

# Find genes with minimal impact
neutral_genes = results[results["growth"] > 0.9 * solution.objective_value]
```

### Fluxo de Trabalho 3: Otimização de Meio

```python
from cobra.io import load_model
from cobra.medium import minimal_medium

# Load model
model = load_model("ecoli")

# Calculate minimal medium for 50% of max growth
target_growth = model.slim_optimize() * 0.5
min_medium = minimal_medium(
    model,
    target_growth,
    minimize_components=True
)

print(f"Minimal medium components: {len(min_medium)}")
print(min_medium)
```

### Fluxo de Trabalho 4: Análise de Incerteza de Fluxo

```python
from cobra.io import load_model
from cobra.flux_analysis import flux_variability_analysis
from cobra.sampling import sample

# Load model
model = load_model("ecoli")

# First check flux ranges at optimality
fva = flux_variability_analysis(model, fraction_of_optimum=1.0)

# For reactions with large ranges, sample to understand distribution
samples = sample(model, n=1000)

# Analyze specific reaction
reaction_id = "PFK"
import matplotlib.pyplot as plt
samples[reaction_id].hist(bins=50)
plt.xlabel(f"Flux through {reaction_id}")
plt.ylabel("Frequency")
plt.show()
```

### Fluxo de Trabalho 5: Gerenciador de Contexto para Mudanças Temporárias

Use gerenciadores de contexto para fazer modificações temporárias:
```python
# Model remains unchanged outside context
with model:
    # Temporarily change objective
    model.objective = "ATPM"

    # Temporarily modify bounds
    model.reactions.EX_glc__D_e.lower_bound = -5.0

    # Temporarily knock out genes
    model.genes.b0008.knock_out()

    # Optimize with changes
    solution = model.optimize()
    print(f"Modified growth: {solution.objective_value}")

# All changes automatically reverted
solution = model.optimize()
print(f"Original growth: {solution.objective_value}")
```

## Conceitos-Chave

### Objetos DictList
Os modelos usam objetos `DictList` para reações, metabolitos e genes - comportando-se como listas e dicionários:
```python
# Access by index
first_reaction = model.reactions[0]

# Access by ID
pfk = model.reactions.get_by_id("PFK")

# Query methods
atp_reactions = model.reactions.query("atp")
```

### Restrições de Fluxo
Os limites de reação definem intervalos de fluxo viáveis:
- **Irreversível**: `lower_bound = 0, upper_bound > 0`
- **Reversível**: `lower_bound < 0, upper_bound > 0`
- Defina ambos os limites simultaneamente com `.bounds` para evitar inconsistências

### Regras Gene-Reação (GPR)
Lógica booleana vinculando genes a reações:
```python
# AND logic (both required)
reaction.gene_reaction_rule = "gene1 and gene2"

# OR logic (either sufficient)
reaction.gene_reaction_rule = "gene1 or gene2"

# Complex logic
reaction.gene_reaction_rule = "(gene1 and gene2) or (gene3 and gene4)"
```

### Reações de Troca
Reações especiais representando importação/exportação de metabolitos:
- Nomeadas com prefixo `EX_` por convenção
- Fluxo positivo = secreção, fluxo negativo = absorção
- Gerenciadas através do dicionário `model.medium`

## Melhores Práticas

1. **Use gerenciadores de contexto** para modificações temporárias a fim de evitar problemas de gerenciamento de estado
2. **Valide modelos** antes da análise usando `model.slim_optimize()` para garantir viabilidade
3. **Verifique o status da solução** após otimização - `optimal` indica solução bem-sucedida
4. **Use FVA sem loops** quando a viabilidade termodinâmica importa
5. **Defina fraction_of_optimum** apropriadamente em FVA para explorar espaço subótimo
6. **Paralelizando** operações computacionalmente caras (amostragem, duplas deleções)
7. **Prefira formato SBML** para intercâmbio de modelos e armazenamento de longo prazo
8. **Use slim_optimize()** quando apenas o valor objetivo for necessário para desempenho
9. **Valide amostras de fluxo** para garantir estabilidade numérica

## Resolução de Problemas

**Soluções inviáveis**: Verifique restrições de meio, limites de reação e consistência do modelo
**Otimização lenta**: Tente diferentes solvers (GLPK, CPLEX, Gurobi) via `model.solver`
**Soluções ilimitadas**: Verifique se as reações de troca têm limites superiores apropriados
**Erros de importação**: Certifique-se de que o formato de arquivo está correto e os identificadores SBML são válidos

## Referências

Para fluxos de trabalho e padrões de API detalhados, consulte:
- `references/workflows.md` - Exemplos de fluxo de trabalho detalhados passo a passo
- `references/api_quick_reference.md` - Assinaturas de funções comuns e padrões

Documentação oficial: https://cobrapy.readthedocs.io/en/latest/