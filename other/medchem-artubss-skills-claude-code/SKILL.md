---
name: medchem
description: "Filtros de química medicinal. Aplique regras de similaridade a fármacos (Lipinski, Veber), filtros PAINS, alertas estruturais, métricas de complexidade, para priorização de compostos e filtragem de bibliotecas."
---

# Medchem

## Visão geral

Medchem é uma biblioteca Python para filtragem molecular e priorização em fluxos de trabalho de descoberta de fármacos. Aplique centenas de filtros moleculares bem estabelecidos e inovadores, alertas estruturais e regras de química medicinal para triar e priorizar bibliotecas de compostos em larga escala de forma eficiente. Regras e filtros são específicos do contexto—use como diretrizes combinadas com experiência de domínio.

## Quando usar esta habilidade

Esta habilidade deve ser usada quando:
- Aplicar regras de similaridade a fármacos (Lipinski, Veber, etc.) em bibliotecas de compostos
- Filtrar moléculas por alertas estruturais ou padrões PAINS
- Priorizar compostos para otimização de líderes
- Avaliar qualidade de compostos e propriedades de química medicinal
- Detectar grupos funcionais reativos ou problemáticos
- Calcular métricas de complexidade molecular

## Instalação

```bash
uv pip install medchem
```

## Capacidades principais

### 1. Regras de Química Medicinal

Aplique regras de similaridade a fármacos bem estabelecidas em moléculas usando o módulo `medchem.rules`.

**Regras Disponíveis:**
- Rule of Five (Lipinski)
- Rule of Oprea
- Rule of CNS
- Rule of leadlike (suave e restrita)
- Rule of three
- Rule of Reos
- Rule of drug
- Rule of Veber
- Golden triangle
- Filtros PAINS

**Aplicação de Regra Única:**

```python
import medchem as mc

# Apply Rule of Five to a SMILES string
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
passes = mc.rules.basic_rules.rule_of_five(smiles)
# Returns: True

# Check specific rules
passes_oprea = mc.rules.basic_rules.rule_of_oprea(smiles)
passes_cns = mc.rules.basic_rules.rule_of_cns(smiles)
```

**Múltiplas Regras com RuleFilters:**

```python
import datamol as dm
import medchem as mc

# Load molecules
mols = [dm.to_mol(smiles) for smiles in smiles_list]

# Create filter with multiple rules
rfilter = mc.rules.RuleFilters(
    rule_list=[
        "rule_of_five",
        "rule_of_oprea",
        "rule_of_cns",
        "rule_of_leadlike_soft"
    ]
)

# Apply filters with parallelization
results = rfilter(
    mols=mols,
    n_jobs=-1,  # Use all CPU cores
    progress=True
)
```

**Formato de Resultado:**
Os resultados são retornados como dicionários com status de aprovação/rejeição e informações detalhadas para cada regra.

### 2. Filtros de Alertas Estruturais

Detecte padrões estruturais potencialmente problemáticos usando o módulo `medchem.structural`.

**Filtros Disponíveis:**

1. **Common Alerts** - Alertas estruturais gerais derivados de curadoria ChEMBL e literatura
2. **NIBR Filters** - Conjunto de filtros do Novartis Institutes for BioMedical Research
3. **Lilly Demerits** - Sistema baseado em demérito da Eli Lilly (275 regras, moléculas rejeitadas com >100 demérito)

**Common Alerts:**

```python
import medchem as mc

# Create filter
alert_filter = mc.structural.CommonAlertsFilters()

# Check single molecule
mol = dm.to_mol("c1ccccc1")
has_alerts, details = alert_filter.check_mol(mol)

# Batch filtering with parallelization
results = alert_filter(
    mols=mol_list,
    n_jobs=-1,
    progress=True
)
```

**NIBR Filters:**

```python
import medchem as mc

# Apply NIBR filters
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1)
```

**Lilly Demerits:**

```python
import medchem as mc

# Calculate Lilly demerits
lilly = mc.structural.LillyDemeritsFilters()
results = lilly(mols=mol_list, n_jobs=-1)

# Each result includes demerit score and whether it passes (≤100 demerits)
```

### 3. API Funcional para Operações de Alto Nível

O módulo `medchem.functional` fornece funções convenientes para fluxos de trabalho comuns.

**Filtragem Rápida:**

```python
import medchem as mc

# Apply NIBR filters to a list
filter_ok = mc.functional.nibr_filter(
    mols=mol_list,
    n_jobs=-1
)

# Apply common alerts
alert_results = mc.functional.common_alerts_filter(
    mols=mol_list,
    n_jobs=-1
)
```

### 4. Detecção de Grupos Químicos

Identifique grupos químicos específicos e grupos funcionais usando `medchem.groups`.

**Grupos Disponíveis:**
- Hinge binders
- Phosphate binders
- Michael acceptors
- Grupos reativos
- Padrões SMARTS personalizados

**Uso:**

```python
import medchem as mc

# Create group detector
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])

# Check for matches
has_matches = group.has_match(mol_list)

# Get detailed match information
matches = group.get_matches(mol)
```

### 5. Catálogos Nomeados

Acesse coleções organizadas de estruturas químicas através de `medchem.catalogs`.

**Catálogos Disponíveis:**
- Grupos funcionais
- Grupos protetores
- Reagentes comuns
- Fragmentos padrão

**Uso:**

```python
import medchem as mc

# Access named catalogs
catalogs = mc.catalogs.NamedCatalogs

# Use catalog for matching
catalog = catalogs.get("functional_groups")
matches = catalog.get_matches(mol)
```

### 6. Complexidade Molecular

Calcule métricas de complexidade que aproximam acessibilidade sintética usando `medchem.complexity`.

**Métricas Comuns:**
- Complexidade de Bertz
- Complexidade de Whitlock
- Complexidade de Barone

**Uso:**

```python
import medchem as mc

# Calculate complexity
complexity_score = mc.complexity.calculate_complexity(mol)

# Filter by complexity threshold
complex_filter = mc.complexity.ComplexityFilter(max_complexity=500)
results = complex_filter(mols=mol_list)
```

### 7. Filtragem de Restrições

Aplique restrições personalizadas baseadas em propriedades usando `medchem.constraints`.

**Restrições de Exemplo:**
- Faixas de peso molecular
- Limites de LogP
- Limites de TPSA
- Contagem de ligações rotáveis

**Uso:**

```python
import medchem as mc

# Define constraints
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140,
    rotatable_bonds_max=10
)

# Apply constraints
results = constraints(mols=mol_list, n_jobs=-1)
```

### 8. Linguagem de Consulta Medchem

Use uma linguagem de consulta especializada para critérios de filtragem complexos.

**Exemplos de Consulta:**
```
# Molecules passing Ro5 AND not having common alerts
"rule_of_five AND NOT common_alerts"

# CNS-like molecules with low complexity
"rule_of_cns AND complexity < 400"

# Leadlike molecules without Lilly demerits
"rule_of_leadlike AND lilly_demerits == 0"
```

**Uso:**

```python
import medchem as mc

# Parse and apply query
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
```

## Padrões de Fluxo de Trabalho

### Padrão 1: Triagem Inicial de Biblioteca de Compostos

Filtre uma grande coleção de compostos para identificar candidatos similares a fármacos.

```python
import datamol as dm
import medchem as mc
import pandas as pd

# Load compound library
df = pd.read_csv("compounds.csv")
mols = [dm.to_mol(smi) for smi in df["smiles"]]

# Apply primary filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_veber"])
rule_results = rule_filter(mols=mols, n_jobs=-1, progress=True)

# Apply structural alerts
alert_filter = mc.structural.CommonAlertsFilters()
alert_results = alert_filter(mols=mols, n_jobs=-1, progress=True)

# Combine results
df["passes_rules"] = rule_results["pass"]
df["has_alerts"] = alert_results["has_alerts"]
df["drug_like"] = df["passes_rules"] & ~df["has_alerts"]

# Save filtered compounds
filtered_df = df[df["drug_like"]]
filtered_df.to_csv("filtered_compounds.csv", index=False)
```

### Padrão 2: Filtragem de Otimização de Líderes

Aplique critérios mais rigorosos durante otimização de líderes.

```python
import medchem as mc

# Create comprehensive filter
filters = {
    "rules": mc.rules.RuleFilters(rule_list=["rule_of_leadlike_strict"]),
    "alerts": mc.structural.NIBRFilters(),
    "lilly": mc.structural.LillyDemeritsFilters(),
    "complexity": mc.complexity.ComplexityFilter(max_complexity=400)
}

# Apply all filters
results = {}
for name, filt in filters.items():
    results[name] = filt(mols=candidate_mols, n_jobs=-1)

# Identify compounds passing all filters
passes_all = all(r["pass"] for r in results.values())
```

### Padrão 3: Identificar Grupos Químicos Específicos

Encontre moléculas contendo grupos funcionais ou scaffolds específicos.

```python
import medchem as mc

# Create group detector for multiple groups
group_detector = mc.groups.ChemicalGroup(
    groups=["hinge_binders", "phosphate_binders"]
)

# Screen library
matches = group_detector.get_all_matches(mol_list)

# Filter molecules with desired groups
mol_with_groups = [mol for mol, match in zip(mol_list, matches) if match]
```

## Melhores Práticas

1. **O Contexto Importa**: Não aplique filtros cegamente. Entenda o alvo biológico e o espaço químico.

2. **Combine Múltiplos Filtros**: Use regras, alertas estruturais e conhecimento de domínio juntos para melhores decisões.

3. **Use Paralelização**: Para grandes conjuntos de dados (>1000 moléculas), sempre use `n_jobs=-1` para processamento paralelo.

4. **Refinamento Iterativo**: Comece com filtros amplos (Ro5), depois aplique critérios mais específicos (CNS, leadlike) conforme necessário.

5. **Documente Decisões de Filtragem**: Rastreie quais moléculas foram filtradas e por quê para reprodutibilidade.

6. **Valide Resultados**: Lembre-se que fármacos comercializados frequentemente falham em filtros padrão—use esses como diretrizes, não como regras absolutas.

7. **Considere Pródrogas**: Moléculas projetadas como pródrogas podem intencionalmente violar regras padrão de química medicinal.

## Recursos

### references/api_guide.md
Referência API abrangente cobrindo todos os módulos medchem com assinaturas de função detalhadas, parâmetros e tipos de retorno.

### references/rules_catalog.md
Catálogo completo de regras, filtros e alertas disponíveis com descrições, limites e referências bibliográficas.

### scripts/filter_molecules.py
Script pronto para produção para fluxos de trabalho de filtragem em lote. Suporta múltiplos formatos de entrada (CSV, SDF, SMILES), combinações de filtros configuráveis e relatórios detalhados.

**Uso:**
```bash
python scripts/filter_molecules.py input.csv --rules rule_of_five,rule_of_cns --alerts nibr --output filtered.csv
```

## Documentação

Documentação oficial: https://medchem-docs.datamol.io/
Repositório GitHub: https://github.com/datamol-io/medchem