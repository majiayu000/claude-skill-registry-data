---
name: matchms
description: "Análise de espectrometria de massas. Processa mzML/MGF/MSP, similaridade espectral (cosine, modified cosine), harmonização de metadados, identificação de compostos, para metabolômica e processamento de dados MS."
---

# Matchms

## Visão Geral

Matchms é uma biblioteca Python de código aberto para processamento e análise de dados de espectrometria de massas. Importe espectros de vários formatos, padronize metadados, filtre picos, calcule similaridades espectrais e construa workflows analíticos reproduzíveis.

## Capacidades Principais

### 1. Importação e Exportação de Dados de Espectrometria de Massas

Carregue espectros de múltiplos formatos de arquivo e exporte dados processados:

```python
from matchms.importing import load_from_mgf, load_from_mzml, load_from_msp, load_from_json
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json

# Import spectra
spectra = list(load_from_mgf("spectra.mgf"))
spectra = list(load_from_mzml("data.mzML"))
spectra = list(load_from_msp("library.msp"))

# Export processed spectra
save_as_mgf(spectra, "output.mgf")
save_as_json(spectra, "output.json")
```

**Formatos suportados:**
- mzML e mzXML (formatos brutos de espectrometria de massas)
- MGF (Mascot Generic Format)
- MSP (formato de biblioteca espectral)
- JSON (compatível com GNPS)
- Referências metabolomics-USI
- Pickle (serialização Python)

Para documentação detalhada de importação/exportação, consulte `references/importing_exporting.md`.

### 2. Filtragem e Processamento de Espectros

Aplique filtros abrangentes para padronizar metadados e refinar dados de picos:

```python
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks

# Apply default metadata harmonization filters
spectrum = default_filters(spectrum)

# Normalize peak intensities
spectrum = normalize_intensities(spectrum)

# Filter peaks by relative intensity
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01, intensity_to=1.0)

# Require minimum peaks
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

**Categorias de filtros:**
- **Processamento de metadados**: Harmonize nomes de compostos, derive estruturas químicas, padronize aductos, corrija cargas
- **Filtragem de picos**: Normalize intensidades, selecione por m/z ou intensidade, remova picos de precursor
- **Controle de qualidade**: Exija número mínimo de picos, valide m/z de precursor, garanta completude de metadados
- **Anotação química**: Adicione impressões digitais, derive InChI/SMILES, repare incompatibilidades estruturais

Matchms fornece mais de 40 filtros. Para a referência completa de filtros, consulte `references/filtering.md`.

### 3. Cálculo de Similaridades Espectrais

Compare espectros usando várias métricas de similaridade:

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine, CosineHungarian

# Calculate cosine similarity (fast, greedy algorithm)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())

# Calculate modified cosine (accounts for precursor m/z differences)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=ModifiedCosine(tolerance=0.1))

# Get best matches
best_matches = scores.scores_by_query(query_spectra[0], sort=True)[:10]
```

**Funções de similaridade disponíveis:**
- **CosineGreedy/CosineHungarian**: Similaridade cosseno baseada em picos com diferentes algoritmos de correspondência
- **ModifiedCosine**: Similaridade cosseno considerando diferenças de massa de precursor
- **NeutralLossesCosine**: Similaridade baseada em padrões de perda neutra
- **FingerprintSimilarity**: Similaridade de estrutura molecular usando impressões digitais
- **MetadataMatch**: Compare campos de metadados definidos pelo usuário
- **PrecursorMzMatch/ParentMassMatch**: Filtragem simples baseada em massa

Para documentação detalhada de funções de similaridade, consulte `references/similarity.md`.

### 4. Construção de Pipelines de Processamento

Crie workflows de análise reproduzíveis e multi-etapas:

```python
from matchms import SpectrumProcessor
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, remove_peaks_around_precursor_mz

# Define a processing pipeline
processor = SpectrumProcessor([
    default_filters,
    normalize_intensities,
    lambda s: select_by_relative_intensity(s, intensity_from=0.01),
    lambda s: remove_peaks_around_precursor_mz(s, mz_tolerance=17)
])

# Apply to all spectra
processed_spectra = [processor(s) for s in spectra]
```

### 5. Trabalho com Objetos Spectrum

A classe central `Spectrum` contém dados de espectro de massa:

```python
from matchms import Spectrum
import numpy as np

# Create a spectrum
mz = np.array([100.0, 150.0, 200.0, 250.0])
intensities = np.array([0.1, 0.5, 0.9, 0.3])
metadata = {"precursor_mz": 250.5, "ionmode": "positive"}

spectrum = Spectrum(mz=mz, intensities=intensities, metadata=metadata)

# Access spectrum properties
print(spectrum.peaks.mz)           # m/z values
print(spectrum.peaks.intensities)  # Intensity values
print(spectrum.get("precursor_mz")) # Metadata field

# Visualize spectra
spectrum.plot()
spectrum.plot_against(reference_spectrum)
```

### 6. Gestão de Metadados

Padronize e harmonize metadados de espectros:

```python
# Metadata is automatically harmonized
spectrum.set("Precursor_mz", 250.5)  # Gets harmonized to lowercase key
print(spectrum.get("precursor_mz"))   # Returns 250.5

# Derive chemical information
from matchms.filtering import derive_inchi_from_smiles, derive_inchikey_from_inchi
from matchms.filtering import add_fingerprint

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan", nbits=2048)
```

## Workflows Comuns

Para workflows típicos de análise de espectrometria de massas, incluindo:
- Carregamento e pré-processamento de bibliotecas espectrais
- Correspondência de espectros desconhecidos contra bibliotecas de referência
- Filtragem de qualidade e limpeza de dados
- Comparações de similaridade em larga escala
- Agrupamento espectral baseado em rede

Consulte `references/workflows.md` para exemplos detalhados.

## Instalação

```bash
uv pip install matchms
```

Para processamento de estrutura molecular (SMILES, InChI):
```bash
uv pip install matchms[chemistry]
```

## Documentação de Referência

Documentação de referência detalhada está disponível no diretório `references/`:
- `filtering.md` - Referência completa de funções de filtro com descrições
- `similarity.md` - Todas as métricas de similaridade e quando usá-las
- `importing_exporting.md` - Detalhes de formato de arquivo e operações de E/S
- `workflows.md` - Padrões de análise comuns e exemplos

Carregue essas referências conforme necessário para informações detalhadas sobre capacidades específicas do matchms.