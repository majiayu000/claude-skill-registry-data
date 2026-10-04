---
name: astropy
description: Biblioteca Python abrangente para astronomia e astrofísica. Esta skill deve ser usada ao trabalhar com dados astronômicos, incluindo coordenadas celestes, unidades físicas, arquivos FITS, cálculos cosmológicos, sistemas de tempo, tabelas, sistemas de coordenadas mundiais (WCS) e análise de dados astronômicos. Use quando as tarefas envolvem transformações de coordenadas, conversões de unidades, manipulação de arquivos FITS, cálculos de distâncias cosmológicas, conversões de escalas de tempo ou processamento de dados astronômicos.
---

# Astropy

## Visão Geral

Astropy é o pacote Python principal para astronomia, fornecendo funcionalidades essenciais para pesquisa astronômica e análise de dados. Use astropy para transformações de coordenadas, cálculos com unidades e quantidades, operações com arquivos FITS, cálculos cosmológicos, manipulação precisa de tempo, manipulação de dados tabulares e processamento de imagens astronômicas.

## Quando Usar Esta Skill

Use astropy quando as tarefas envolvem:
- Converter entre sistemas de coordenadas celestes (ICRS, Galactic, FK5, AltAz, etc.)
- Trabalhar com unidades e quantidades físicas (converter Jy para mJy, parsecs para km, etc.)
- Ler, escrever ou manipular arquivos FITS (imagens ou tabelas)
- Cálculos cosmológicos (distância de luminosidade, tempo de lookback, parâmetro de Hubble)
- Manipulação precisa de tempo com diferentes escalas de tempo (UTC, TAI, TT, TDB) e formatos (JD, MJD, ISO)
- Operações com tabelas (ler catálogos, cross-matching, filtragem, join)
- Transformações WCS entre coordenadas de pixel e coordenadas mundiais
- Constantes astronômicas e cálculos

## Início Rápido

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# Units and quantities
distance = 100 * u.pc
distance_km = distance.to(u.km)

# Coordinates
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# Time
t = Time('2023-01-15 12:30:00')
jd = t.jd  # Julian Date

# FITS files
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# Tables
table = Table.read('catalog.fits')

# Cosmology
d_L = Planck18.luminosity_distance(z=1.0)
```

## Capacidades Principais

### 1. Unidades e Quantidades (`astropy.units`)

Manipule quantidades físicas com unidades, realize conversões de unidades e garanta consistência dimensional em cálculos.

**Operações principais:**
- Crie quantidades multiplicando valores por unidades
- Converta entre unidades usando o método `.to()`
- Realize operações aritméticas com manipulação automática de unidades
- Use equivalências para conversões específicas de domínio (espectral, doppler, paralaxe)
- Trabalhe com unidades logarítmicas (magnitudes, decibéis)

**Veja:** `references/units.md` para documentação abrangente, sistemas de unidades, equivalências, otimização de desempenho e aritmética de unidades.

### 2. Sistemas de Coordenadas (`astropy.coordinates`)

Represente posições celestes e transforme entre diferentes frames de coordenadas.

**Operações principais:**
- Crie coordenadas com `SkyCoord` em qualquer frame (ICRS, Galactic, FK5, AltAz, etc.)
- Transforme entre sistemas de coordenadas
- Calcule separações angulares e ângulos de posição
- Combine coordenadas com catálogos
- Inclua distância para operações de coordenadas 3D
- Manipule movimentos próprios e velocidades radiais
- Consulte objetos nomeados em bancos de dados online

**Veja:** `references/coordinates.md` para descrições detalhadas de frames de coordenadas, transformações, frames dependentes do observador (AltAz), matching de catálogos e dicas de desempenho.

### 3. Cálculos Cosmológicos (`astropy.cosmology`)

Realize cálculos cosmológicos usando modelos cosmológicos padrão.

**Operações principais:**
- Use cosmologias incorporadas (Planck18, WMAP9, etc.)
- Crie modelos cosmológicos personalizados
- Calcule distâncias (luminosidade, comóvel, diâmetro angular)
- Compute idades e tempos de lookback
- Determine o parâmetro de Hubble em qualquer redshift
- Calcule parâmetros de densidade e volumes
- Realize cálculos inversos (encontre z para uma distância dada)

**Veja:** `references/cosmology.md` para modelos disponíveis, cálculos de distância, cálculos de tempo, parâmetros de densidade e efeitos de neutrino.

### 4. Manipulação de Arquivos FITS (`astropy.io.fits`)

Leia, escreva e manipule arquivos FITS (Flexible Image Transport System).

**Operações principais:**
- Abra arquivos FITS com context managers
- Acesse HDUs (Header Data Units) por índice ou nome
- Leia e modifique headers (palavras-chave, comentários, histórico)
- Trabalhe com dados de imagem (arrays NumPy)
- Manipule dados de tabela (tabelas binárias e ASCII)
- Crie novos arquivos FITS (simples ou multi-extensão)
- Use memory mapping para arquivos grandes
- Acesse arquivos FITS remotos (S3, HTTP)

**Veja:** `references/fits.md` para operações abrangentes de arquivo, manipulação de header, manipulação de imagem e tabela, arquivos multi-extensão e considerações de desempenho.

### 5. Operações com Tabelas (`astropy.table`)

Trabalhe com dados tabulares com suporte para unidades, metadados e vários formatos de arquivo.

**Operações principais:**
- Crie tabelas a partir de arrays, listas ou dicionários
- Leia/escreva tabelas em múltiplos formatos (FITS, CSV, HDF5, VOTable)
- Acesse e modifique colunas e linhas
- Ordene, filtre e indexe tabelas
- Realize operações estilo banco de dados (join, group, aggregate)
- Empilhe e concatene tabelas
- Trabalhe com colunas com unidades (QTable)
- Manipule dados ausentes com masking

**Veja:** `references/tables.md` para criação de tabelas, operações de I/O, manipulação de dados, ordenação, filtragem, joins, grouping e dicas de desempenho.

### 6. Manipulação de Tempo (`astropy.time`)

Representação precisa de tempo e conversão entre escalas de tempo e formatos.

**Operações principais:**
- Crie objetos Time em vários formatos (ISO, JD, MJD, Unix, etc.)
- Converta entre escalas de tempo (UTC, TAI, TT, TDB, etc.)
- Realize operações aritméticas de tempo com TimeDelta
- Calcule tempo sideral para observadores
- Compute correções de tempo de viagem de luz (barricêntrico, heliocêntrico)
- Trabalhe com arrays de tempo de forma eficiente
- Manipule tempos mascarados (ausentes)

**Veja:** `references/time.md` para formatos de tempo, escalas de tempo, conversões, aritmética, recursos de observação e manipulação de precisão.

### 7. Sistema de Coordenadas Mundiais (`astropy.wcs`)

Transforme entre coordenadas de pixel em imagens e coordenadas mundiais.

**Operações principais:**
- Leia WCS a partir de headers FITS
- Converta coordenadas de pixel para coordenadas mundiais (e vice-versa)
- Calcule pegadas de imagem
- Acesse parâmetros de WCS (pixel de referência, projeção, escala)
- Crie objetos WCS personalizados

**Veja:** `references/wcs_and_other_modules.md` para operações e transformações de WCS.

## Capacidades Adicionais

O arquivo `references/wcs_and_other_modules.md` também cobre:

### NDData e CCDData
Contêineres para datasets n-dimensionais com metadados, incerteza, masking e informações de WCS.

### Modelagem
Framework para criar e ajustar modelos matemáticos a dados astronômicos.

### Visualização
Ferramentas para exibição de imagem astronômica com stretching e scaling apropriados.

### Constantes
Constantes físicas e astronômicas com unidades adequadas (velocidade da luz, massa solar, constante de Planck, etc.).

### Convolução
Kernels de processamento de imagem para suavização e filtragem.

### Estatísticas
Funções estatísticas robustas, incluindo sigma clipping e rejeição de outliers.

## Instalação

```bash
# Install astropy
uv pip install astropy

# With optional dependencies for full functionality
uv pip install astropy[all]
```

## Fluxos de Trabalho Comuns

### Convertendo Coordenadas Entre Sistemas

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# Create coordinate
c = SkyCoord(ra='05h23m34.5s', dec='-69d45m22s', frame='icrs')

# Transform to galactic
c_gal = c.galactic
print(f"l={c_gal.l.deg}, b={c_gal.b.deg}")

# Transform to alt-az (requires time and location)
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

observing_time = Time('2023-06-15 23:00:00')
observing_location = EarthLocation(lat=40*u.deg, lon=-120*u.deg)
aa_frame = AltAz(obstime=observing_time, location=observing_location)
c_altaz = c.transform_to(aa_frame)
print(f"Alt={c_altaz.alt.deg}, Az={c_altaz.az.deg}")
```

### Lendo e Analisando Arquivos FITS

```python
from astropy.io import fits
import numpy as np

# Open FITS file
with fits.open('observation.fits') as hdul:
    # Display structure
    hdul.info()

    # Get image data and header
    data = hdul[1].data
    header = hdul[1].header

    # Access header values
    exptime = header['EXPTIME']
    filter_name = header['FILTER']

    # Analyze data
    mean = np.mean(data)
    median = np.median(data)
    print(f"Mean: {mean}, Median: {median}")
```

### Cálculos de Distância Cosmológica

```python
from astropy.cosmology import Planck18
import astropy.units as u
import numpy as np

# Calculate distances at z=1.5
z = 1.5
d_L = Planck18.luminosity_distance(z)
d_A = Planck18.angular_diameter_distance(z)

print(f"Luminosity distance: {d_L}")
print(f"Angular diameter distance: {d_A}")

# Age of universe at that redshift
age = Planck18.age(z)
print(f"Age at z={z}: {age.to(u.Gyr)}")

# Lookback time
t_lookback = Planck18.lookback_time(z)
print(f"Lookback time: {t_lookback.to(u.Gyr)}")
```

### Combinando Catálogos

```python
from astropy.table import Table
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u

# Read catalogs
cat1 = Table.read('catalog1.fits')
cat2 = Table.read('catalog2.fits')

# Create coordinate objects
coords1 = SkyCoord(ra=cat1['RA']*u.degree, dec=cat1['DEC']*u.degree)
coords2 = SkyCoord(ra=cat2['RA']*u.degree, dec=cat2['DEC']*u.degree)

# Find matches
idx, sep, _ = coords1.match_to_catalog_sky(coords2)

# Filter by separation threshold
max_sep = 1 * u.arcsec
matches = sep < max_sep

# Create matched catalogs
cat1_matched = cat1[matches]
cat2_matched = cat2[idx[matches]]
print(f"Found {len(cat1_matched)} matches")
```

## Melhores Práticas

1. **Sempre use unidades**: Anexe unidades a quantidades para evitar erros e garantir consistência dimensional
2. **Use context managers para arquivos FITS**: Garante o fechamento adequado de arquivos
3. **Prefira arrays em vez de loops**: Processe múltiplas coordenadas/tempos como arrays para melhor desempenho
4. **Verifique os frames de coordenadas**: Verifique o frame antes das transformações
5. **Use a cosmologia apropriada**: Escolha o modelo cosmológico correto para sua análise
6. **Manipule dados ausentes**: Use colunas mascaradas para tabelas com valores ausentes
7. **Especifique escalas de tempo**: Seja explícito sobre escalas de tempo (UTC, TT, TDB) para timing preciso
8. **Use QTable para tabelas com unidades**: Quando as colunas da tabela têm unidades
9. **Verifique a validade de WCS**: Verifique WCS antes de usar transformações
10. **Cache de valores frequentemente usados**: Cálculos caros (ex: distâncias cosmológicas) podem ser colocados em cache

## Documentação e Recursos

- Documentação oficial do Astropy: https://docs.astropy.org/en/stable/
- Tutoriais: https://learn.astropy.org/
- GitHub: https://github.com/astropy/astropy

## Arquivos de Referência

Para informações detalhadas sobre módulos específicos:
- `references/units.md` - Unidades, quantidades, conversões e equivalências
- `references/coordinates.md` - Sistemas de coordenadas, transformações e matching de catálogos
- `references/cosmology.md` - Modelos cosmológicos e cálculos
- `references/fits.md` - Operações e manipulação de arquivos FITS
- `references/tables.md` - Criação de tabelas, I/O e operações
- `references/time.md` - Formatos de tempo, escalas e cálculos
- `references/wcs_and_other_modules.md` - WCS, NDData, modelagem, visualização, constantes e utilitários