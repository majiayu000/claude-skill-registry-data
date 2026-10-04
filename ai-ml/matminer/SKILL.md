---
name: matminer
description: Matminer - Python library for data mining in materials science. Use when applying machine learning to materials data, generating features/featurizers for materials, accessing materials datasets, or building materials property prediction models. Provides 70+ featurizers for compositions and structures.
metadata:
    skill-author: MindSpore Science Team
---

# Matminer

## Overview

Matminer is a Python library for materials data mining. It provides tools for accessing materials datasets, generating features (featurizers) for machine learning, and building predictive models for materials properties.

## When to Use This Skill

Use this skill when:

1. **Generating composition-based features** - Need numerical descriptors from chemical formulas (e.g., elemental property statistics, stoichiometry, oxidation states)

2. **Generating structure-based features** - Have crystal structure data and need features like density, Coulomb matrices, RDFs, or symmetry descriptors

3. **Accessing materials datasets** - Want to load ready-made materials datasets (elastic tensors, band gaps, formation energies, etc.) for ML training

4. **Building property prediction models** - Creating ML pipelines for predicting materials properties (bulk modulus, band gap, formation energy)

5. **Converting data formats** - Need to transform string formulas to Composition objects, add oxidation states, or convert between pymatgen/ASE formats

6. **Featurizing electronic structure data** - Working with band structures or DOS and need features like band edges, effective mass, or orbital character

7. **Benchmarking ML algorithms** - Using Matbench datasets for reproducible comparison of materials ML methods

8. **Data retrieval from materials databases** - Fetching data from Materials Project, Citrine, or other materials repositories

## Installation

```bash
pip install matminer
```

For development installation:
```bash
git clone https://github.com/hackingmaterials/matminer.git
cd matminer
pip install -e .
```

## Quick Start

```python
from matminer.datasets import load_dataset
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Composition

# Load a dataset
df = load_dataset("elastic_tensor_2015")

# Create a featurizer
ep = ElementProperty.from_preset("magpie")

# Featurize a composition
comp = Composition("Fe3O4")
features = ep.featurize(comp)
```

## Featurizers

### Composition Featurizers

Features based on chemical composition (no structure required):

| Featurizer | Description |
|------------|-------------|
| `ElementProperty` | Elemental property statistics (mean, std, range, etc.) |
| `Meredig` | Features as defined in Meredig et al. |
| `ElementFraction` | Atomic fraction of each element |
| `TMetalFraction` | Fraction of magnetic transition metals |
| `Stoichiometry` | Norms of stoichiometric attributes |
| `BandCenter` | Band center estimation from electronegativity |
| `ValenceOrbital` | Attributes of valence orbital shells |
| `AtomicOrbitals` | HOMO/LUMO features from composition |
| `OxidationStates` | Oxidation state statistics |
| `IonProperty` | Ionic property attributes |
| `ElectronegativityDiff` | Electronegativity differences between anions/cations |
| `ElectronAffinity` | Electron affinity features |
| `CohesiveEnergy` | Cohesive energy per atom |
| `CohesiveEnergyMP` | Cohesive energy from Materials Project lookup |
| `Miedema` | Formation enthalpies of intermetallics |
| `YangSolidSolution` | Mixing thermochemistry for solid solutions |
| `WenAlloys` | Features for alloy properties |
| `AtomicPackingEfficiency` | Packing efficiency from geometric theory |

```python
from matminer.featurizers.composition import ElementProperty, Stoichiometry

# Using preset element properties (magpie is most common)
ep = ElementProperty.from_preset("magpie")
features = ep.featurize(Composition("Fe2O3"))

# Stoichiometric features
stoich = Stoichiometry()
stoich_features = stoich.featurize(Composition("NaCl"))
```

### Structure Featurizers

Features based on crystal structure:

| Featurizer | Description |
|------------|-------------|
| `DensityFeatures` | Density and density-like features |
| `GlobalSymmetryFeatures` | Spacegroup, crystal system |
| `Dimensionality` | Structure dimensionality (0D, 1D, 2D, 3D) |
| `RadialDistributionFunction` | RDF of crystal structure |
| `PartialRadialDistributionFunction` | PRDF by element pairs |
| `ElectronicRadialDistributionFunction` | Electronic RDF (ReDF) |
| `CoulombMatrix` | Nuclear Coulombic interaction matrix |
| `SineCoulombMatrix` | Coulomb matrix for periodic crystals |
| `OrbitalFieldMatrix` | Valence shell electron representation |
| `BondFractions` | Fraction of each bond type |
| `BagofBonds` | Bag of Bonds vector representation |
| `GlobalInstabilityIndex` | Global instability index |
| `StructuralHeterogeneity` | Variance in bond lengths/atomic volumes |
| `ChemicalOrdering` | Species ordering deviation from random |
| `MaximumPackingEfficiency` | Maximum packing efficiency |
| `StructuralComplexity` | Shannon information entropy |
| `JarvisCFID` | Classical Force-Field Inspired Descriptors |
| `MinimumRelativeDistances` | Relative distance to closest neighbor |
| `SiteStatsFingerprint` | Statistics of site features across structure |
| `XRDPowderPattern` | Powder diffraction pattern |
| `EwaldEnergy` | Coulombic interaction energy |

```python
from matminer.featurizers.structure import DensityFeatures, CoulombMatrix
from pymatgen.core import Structure

# Load structure and featurize
structure = Structure.from_file("my_structure.cif")

# Density features
df = DensityFeatures()
density_features = df.featurize(structure)

# Coulomb matrix
cm = CoulombMatrix()
matrix_features = cm.featurize(structure)
```

### Site Featurizers

Features for individual crystallographic sites:

| Featurizer | Description |
|------------|-------------|
| `CoordinationNumber` | Number of nearest neighbors |
| `AverageBondLength` | Average bond length at site |
| `AverageBondAngle` | Average bond angles at site |
| `LocalPropertyDifference` | Property differences vs neighbors |
| `ChemicalSRO` | Chemical short range ordering |
| `EwaldSiteEnergy` | Site energy from Coulombic interactions |
| `SiteElementalProperty` | Elemental properties of atom at site |
| `VoronoiFingerprint` | Voronoi tessellation features |
| `CrystalNNFingerprint` | Local order parameters |
| `OPSiteFingerprint` | Local structure order parameters |
| `ChemEnvSiteFingerprint` | Resemblance to ideal environments |
| `AGNIFingerprints` | Gaussian window function features |
| `SOAP` | Smooth overlap of atomic positions |
| `BondOrientationalParameter` | Spherical harmonics of local neighbors |
| `GaussianSymmFunc` | Gaussian symmetry function features |
| `GeneralizedRadialDistributionFunction` | GRDF for a site |
| `AngularFourierSeries` | Angular and radial Fourier series |
| `IntersticeDistribution` | Interstice distribution around site |

```python
from matminer.featurizers.site import CoordinationNumber, LocalPropertyDifference

cn = CoordinationNumber()
cn_val = cn.featurize(structure, idx=0)  # For site 0

lpd = LocalPropertyDifference()
lpd_features = lpd.featurize(structure, idx=0)
```

### Electronic Structure Featurizers

Features from band structure and DOS:

| Featurizer | Description |
|------------|-------------|
| `BandFeaturizer` | Features from band structure |
| `BranchPointEnergy` | Branch point energy, band edge positions |
| `DOSFeaturizer` | DOS features near Fermi level |
| `SiteDOS` | Fractional s/p/d/f DOS for a site |
| `Hybridization` | Orbital character at band edges |
| `DosAsymmetry` | DOS asymmetry near Fermi level |
| `DopingFermi` | Fermi level at different doping levels |

```python
from matminer.featurizers.bandstructure import BandFeaturizer
from matminer.featurizers.dos import DOSFeaturizer

# Band structure features
bf = BandFeaturizer()
bs_features = bf.featurize(bandstructure_object)

# DOS features
dos_f = DOSFeaturizer()
dos_features = dos_f.featurize(dos_object)
```

### Conversion Featurizers

Transform data between formats:

```python
from matminer.featurizers.conversions import (
    StrToComposition,
    StructureToComposition,
    StructureToOxidStructure,
    CompositionToOxidComposition,
    ASEAtomstoStructure,
    PymatgenFunctionApplicator,
)

# String to Composition
s2c = StrToComposition()
df = s2c.featurize_dataframe(df, "formula")

# Add oxidation states to structure
s2o = StructureToOxidStructure()
df = s2o.featurize_dataframe(df, "structure")

# Convert ASE atoms to pymatgen structure
aa2s = ASEAtomstoStructure()
df = aa2s.featurize_dataframe(df, "ase_atoms", ignore_errors=True)
```

## Best Practices

### Choosing Featurizers

1. **Match featurizer to available data**
   - Composition-only: Use `ElementProperty`, `Stoichiometry`, `OxidationStates`
   - Structure available: Add `DensityFeatures`, `CoulombMatrix`, `GlobalSymmetryFeatures`
   - Band structure/DOS: Use `BandFeaturizer`, `DOSFeaturizer`

2. **Start with established presets**
   - `ElementProperty.from_preset("magpie")` - Most widely used, 132 features
   - `ElementProperty.from_preset("matminer")` - Expanded property set
   - These are battle-tested on many materials ML problems

3. **Consider feature interpretability**
   - `ElementProperty` features have clear physical meaning
   - Matrix featurizers (`CoulombMatrix`) are less interpretable
   - SOAP provides atomic environment fingerprints

4. **Avoid feature redundancy**
   - Multiple property-based featurizers may overlap
   - Use `MultipleFeaturizer` to combine non-overlapping sets
   - Apply feature selection after generation

### Handling Missing Data

1. **Use `ignore_errors=True` in featurize_dataframe**
   ```python
   df = featurizer.featurize_dataframe(df, col_id, ignore_errors=True)
   ```

2. **Check for NaN values after featurization**
   ```python
   # Check which rows failed
   failed_rows = df[featurizer.feature_labels()].isna().any(axis=1)
   print(f"Failed: {failed_rows.sum()} / {len(df)}")
   ```

3. **Use `return_input_on_error=True` to identify problem cases**
   ```python
   df = featurizer.featurize_dataframe(
       df, col_id,
       ignore_errors=True,
       return_input_on_error=True  # Returns input instead of NaN
   )
   ```

4. **Common causes of missing features**
   - Missing oxidation states (use `StructureToOxidStructure`)
   - Unusual compositions (rare elements may lack property data)
   - Invalid structures (check with `structure.is_valid()`)

5. **Imputation strategies**
   ```python
   from sklearn.impute import SimpleImputer
   imputer = SimpleImputer(strategy="median")
   X_imputed = imputer.fit_transform(X)
   ```

### Parallel Processing

1. **Use `n_jobs` parameter for multi-core processing**
   ```python
   df = featurizer.featurize_dataframe(
       df, "composition",
       n_jobs=4,          # Number of parallel workers
       pbar=True          # Show progress bar
   )
   ```

2. **Optimal `n_jobs` setting**
   - Start with `n_jobs=-1` (use all CPUs)
   - For memory-intensive featurizers, reduce to half of CPUs
   - SOAP and matrix featurizers may need lower `n_jobs`

3. **Combine with `MultipleFeaturizer` for efficiency**
   ```python
   from matminer.featurizers.base import MultipleFeaturizer

   combined = MultipleFeaturizer([
       ElementProperty.from_preset("magpie"),
       Stoichiometry(),
       DensityFeatures(),
   ])

   df = combined.featurize_dataframe(df, ["composition"], n_jobs=4)
   ```

4. **Memory considerations**
   - Large datasets (>50k rows): Process in chunks
   - Monitor memory usage during parallel featurization
   - Structure featurizers typically need more memory

### Feature Selection

1. **Remove constant/near-constant features**
   ```python
   from sklearn.feature_selection import VarianceThreshold
   selector = VarianceThreshold(threshold=0.01)
   X_selected = selector.fit_transform(X)
   ```

2. **Use model-based selection**
   ```python
   from sklearn.feature_selection import SelectFromModel
   from sklearn.ensemble import RandomForestRegressor

   selector = SelectFromModel(
       RandomForestRegressor(n_estimators=100, random_state=42),
       threshold="median"
   )
   X_selected = selector.fit_transform(X_train, y_train)
   ```

3. **Correlation-based pruning**
   ```python
   # Remove highly correlated features
   corr_matrix = X.corr().abs()
   upper = corr_matrix.where(
       np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
   )
   to_drop = [col for col in upper.columns if any(upper[col] > 0.95)]
   X = X.drop(columns=to_drop)
   ```

4. **Feature importance analysis**
   ```python
   # Get importance from fitted model
   importances = model.feature_importances_
   feature_names = featurizer.feature_labels()

   # Sort by importance
   sorted_idx = np.argsort(importances)[::-1]
   for i in sorted_idx[:10]:
       print(f"{feature_names[i]}: {importances[i]:.4f}")
   ```

## Dataset Loading

### load_dataset

```python
from matminer.datasets import load_dataset

# Load by dataset name
df = load_dataset("jarvis_dft_3d")

# Get dataset info
from matminer.datasets import get_dataset_info
info = get_dataset_info("elastic_tensor_2015")
```

### load_dataset_from_df

```python
from matminer.datasets import load_dataset_from_df
import pandas as pd

# Load dataset from existing dataframe with custom processing
df = pd.read_csv("my_data.csv")
df = load_dataset_from_df(df, dataset_name="my_dataset")
```

### Convenience Loaders

```python
from matminer.datasets.convenience_loaders import (
    load_jarvis_dft_3d,
    load_elastic_tensor,
    load_dielectric_constant,
)

# Load with specific options
df = load_jarvis_dft_3d(drop_nan_columns=["bulk modulus"])
df = load_elastic_tensor()
```

## Feature Generation

### Single Object Featurization

```python
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Composition

# Create featurizer with preset
ep = ElementProperty.from_preset("magpie")

# Featurize single composition
comp = Composition("Fe3O4")
features = ep.featurize(comp)
labels = ep.feature_labels()

print(f"Features: {features}")
print(f"Labels: {labels}")
```

### DataFrame Featurization

```python
from matminer.datasets import load_dataset
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import StrToComposition

# Load dataset
df = load_dataset("elastic_tensor_2015")

# Convert string to composition
df = StrToComposition().featurize_dataframe(df, "formula")

# Add features to dataframe
ep = ElementProperty.from_preset("magpie")
df = ep.featurize_dataframe(df, "composition", ignore_errors=True)
```

### Multiple Featurizers

```python
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty, Stoichiometry
from matminer.featurizers.structure import DensityFeatures

# Combine multiple featurizers
featurizer = MultipleFeaturizer([
    ElementProperty.from_preset("magpie"),
    Stoichiometry(),
    DensityFeatures(),
])

# Apply all at once
df = featurizer.featurize_dataframe(df, ["composition", "structure"])
```

### Parallel Featurization

```python
# Use multiple processes for speed
df = ep.featurize_dataframe(
    df,
    "composition",
    ignore_errors=True,
    pbar=True,  # Progress bar
    n_jobs=4    # Parallel jobs
)
```

## Machine Learning Pipeline

### Regression Example

```python
from matminer.datasets import load_dataset
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import StrToComposition
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = load_dataset("elastic_tensor_2015")

# Prepare features
df = StrToComposition().featurize_dataframe(df, "formula")
ep = ElementProperty.from_preset("magpie")
df = ep.featurize_dataframe(df, "composition", ignore_errors=True)

# Prepare data
X = df[ep.feature_labels()]
y = df["K_VRH"]  # Bulk modulus target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f} GPa")
print(f"R2: {r2_score(y_test, y_pred):.3f}")
```

### Classification Example

```python
from matminer.datasets import load_dataset
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.conversions import StrToComposition
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = load_dataset("matbench_expt_is_metal")

# Prepare features
df = StrToComposition().featurize_dataframe(df, "composition")
ep = ElementProperty.from_preset("magpie")
df = ep.featurize_dataframe(df, "composition", ignore_errors=True)

# Prepare data
X = df[ep.feature_labels()]
y = df["is_metal"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
```

### Structure-Based ML

```python
from matminer.datasets import load_dataset
from matminer.featurizers.structure import SiteStatsFingerprint, CoulombMatrix
from sklearn.ensemble import GradientBoostingRegressor

# Load structure dataset
df = load_dataset("matbench_log_kvrh")

# Featurize structures
cm = CoulombMatrix(flatten=True)
df = cm.featurize_dataframe(df, "structure", ignore_errors=True)

# Train model
X = df[cm.feature_labels()]
y = df["log10(K_VRH)"]

model = GradientBoostingRegressor(n_estimators=200, random_state=42)
model.fit(X, y)
```

### Feature Selection

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestRegressor

# Feature selection using model importance
selector = SelectFromModel(
    RandomForestRegressor(n_estimators=100, random_state=42),
    threshold="median"
)
X_selected = selector.fit_transform(X_train, y_train)
print(f"Features selected: {X_selected.shape[1]} / {X_train.shape[1]}")
```

## Troubleshooting

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `FeaturizationError` | Invalid composition/structure | Use `ignore_errors=True` or validate input |
| `KeyError` in featurize_dataframe | Column name mismatch | Check column exists and has correct type |
| Memory errors during parallel processing | Large dataset + many features | Reduce `n_jobs` or process in chunks |
| NaN values in output | Missing elemental data | Check for rare elements; use imputation |
| Slow featurization | Large dataset, single process | Increase `n_jobs`, use `MultipleFeaturizer` |

### Featurization Failures

1. **Composition featurizer fails**
   ```python
   # Check composition validity
   comp = Composition("Fe3O4")
   print(comp.is_valid())  # Should be True

   # Check for elements with missing data
   from pymatgen.core.periodic_table import Element
   el = Element("Pu")  # Rare elements may lack property data
   ```

2. **Structure featurizer fails**
   ```python
   # Validate structure
   structure = Structure.from_file("structure.cif")
   if not structure.is_valid():
       print("Invalid structure")

   # Add oxidation states if needed
   from matminer.featurizers.conversions import StructureToOxidStructure
   s2o = StructureToOxidStructure()
   structure = s2o.featurize(structure)
   ```

3. **Site featurizer fails**
   - Ensure structure has correct site indexing
   - Some site featurizers require oxidation states
   - Check neighbor-finding parameters

### Dataset Loading Issues

1. **Dataset not found**
   ```python
   # List available datasets
   from matminer.datasets import get_available_datasets
   print(get_available_datasets())
   ```

2. **Download timeout**
   - Large datasets may take time on first load
   - Check internet connection
   - Dataset cached locally after first download

3. **Version mismatch**
   - Ensure matminer version supports the dataset
   - Update matminer: `pip install --upgrade matminer`

### Performance Optimization

1. **Slow featurization on large datasets**
   ```python
   # Process in chunks
   chunk_size = 5000
   for i in range(0, len(df), chunk_size):
       chunk = df.iloc[i:i+chunk_size]
       df.iloc[i:i+chunk_size] = featurizer.featurize_dataframe(
           chunk, col_id, n_jobs=4
       )
   ```

2. **Memory-intensive featurizers**
   - `CoulombMatrix` with `flatten=True` creates many features
   - `SOAP` generates large descriptor vectors
   - Use `SiteStatsFingerprint` with limited stats

3. **Redundant calculations**
   - Use `MultipleFeaturizer` to avoid repeated neighbor-finding
   - Cache intermediate results if needed

## Available Datasets

Matminer provides 45+ ready-made datasets. Key datasets include:

| Dataset | Description | Entries |
|---------|-------------|---------|
| `elastic_tensor_2015` | Elastic properties from DFT-PBE | 1,181 |
| `dielectric_constant` | Dielectric properties from DFPT-PBE | 1,056 |
| `piezoelectric_tensor` | Piezoelectric properties | 941 |
| `flla` | Formation energies (Faber et al.) | 3,938 |
| `jarvis_dft_3d` | JARVIS 3D materials database | 25,923 |
| `jarvis_dft_2d` | JARVIS 2D materials database | 636 |
| `jarvis_ml_dft_training` | JARVIS ML training data | 24,759 |
| `expt_gap` | Experimental band gaps | 6,354 |
| `expt_gap_kingsbury` | Experimental band gaps with mp-ids | 4,604 |
| `expt_formation_enthalpy` | Experimental formation enthalpies | 1,276 |
| `expt_formation_enthalpy_kingsbury` | Formation enthalpies with mp-ids | 2,135 |
| `glass_binary` | Binary metallic glass formation | 5,959 |
| `glass_binary_v2` | Binary glass (deduplicated) | 5,483 |
| `glass_ternary_hipt` | Ternary metallic glass (sputtering) | 5,170 |
| `glass_ternary_landolt` | Ternary metallic glass (Landolt) | 7,191 |
| `superconductivity2018` | Superconductivity Tc values | 16,414 |
| `boltztrap_mp` | Thermoelectric properties | 8,924 |
| `castelli_perovskites` | Perovskite band gaps and formation | 18,928 |
| `steel_strength` | Steel yield/tensile strength | 312 |
| `citrine_thermal_conductivity` | Experimental thermal conductivity | 872 |
| `heusler_magnetic` | Heusler alloy magnetic properties | 1,153 |
| `double_perovskites_gap` | Double perovskite band gaps | 1,306 |
| `double_perovskites_gap_lumo` | Double perovskite LUMO data | 55 |
| `wolverton_oxides` | Perovskite oxide properties | 4,914 |
| `phonon_dielectric_mp` | Phonon and dielectric properties | 1,296 |
| `m2ax` | M2AX compound elastic properties | 223 |
| `brgoch_superhard_training` | Superhard material training data | 2,574 |
| `tholander_nitrides` | Zn-Ti-N, Zn-Zr-N, Zn-Hf-N polymorphs | 12,815 |
| `ucsb_thermoelectrics` | Experimental thermoelectric materials | 1,093 |
| `ricci_boltztrap_mp_tabular` | Electronic transport database | 47,737 |
| `mp_all_20181018` | Materials Project database copy | 83,989 |
| `mp_nostruct_20181018` | MP data without structures | 83,989 |

### Matbench Datasets

| Dataset | Description | Entries |
|---------|-------------|---------|
| `matbench_steels` | Steel yield strengths | 312 |
| `matbench_glass` | Bulk metallic glass formation | 5,680 |
| `matbench_expt_gap` | Experimental band gaps | 4,604 |
| `matbench_expt_is_metal` | Metal/non-metal classification | 4,921 |
| `matbench_dielectric` | Refractive index from structure | 4,764 |
| `matbench_log_gvrh` | Log shear modulus from structure | 10,987 |
| `matbench_log_kvrh` | Log bulk modulus from structure | 10,987 |
| `matbench_mp_e_form` | DFT formation energy from structure | 132,752 |
| `matbench_mp_gap` | DFT band gap from structure | 106,113 |
| `matbench_mp_is_metal` | DFT metallicity from structure | 106,113 |
| `matbench_perovskites` | Perovskite formation energy | 18,928 |
| `matbench_phonons` | Phonon vibration properties | 1,265 |
| `matbench_jdft2d` | 2D exfoliation energies | 636 |

## Resources

- GitHub: https://github.com/hackingmaterials/matminer
- Documentation: https://hackingmaterials.github.io/matminer/
- Examples: https://github.com/hackingmaterials/matminer_examples
- Support Forum: https://matsci.org/c/matminer/16
- Language: Python

## Citation

```bibtex
@article{Ward2018,
  author = {Ward, Logan and Dunn, Alexander and Faghaninia, Alireza and
            Zimmermann, N. E. R. and Bajaj, S. and Wang, Q. and
            Montoya, J. H. and Chen, J. and Bystrom, K. and Dylla, M. and
            Chard, K. and Asta, M. and Persson, K. and Snyder, G. J. and
            Foster, I. and Jain, A.},
  title = {Matminer: An open source toolkit for materials data mining},
  journal = {Computational Materials Science},
  volume = {152},
  pages = {60-69},
  year = {2018},
  doi = {10.1016/j.commatsci.2018.05.018}
}
```