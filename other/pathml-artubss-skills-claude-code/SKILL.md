---
name: pathml
description: Kit de ferramentas de patologia computacional para análise de imagens de lâminas inteiras (WSI) e dados de imagem multiparamétrica. Use esta habilidade ao trabalhar com lâminas de histopatologia, imagens coradas com H&E, imunofluorescência multiplex (CODEX, Vectra), proteômica espacial, detecção/segmentação de núcleos, construção de gráficos de tecido ou treinamento de modelos ML em dados de patologia. Suporta 160+ formatos de lâmina incluindo Aperio SVS, NDPI, DICOM, OME-TIFF para fluxos de trabalho de patologia digital.
---

# PathML

## Visão Geral

PathML é um kit de ferramentas Python abrangente para fluxos de trabalho de patologia computacional, projetado para facilitar aprendizado de máquina e análise de imagens para imagens de patologia de lâmina inteira. O framework fornece ferramentas modulares e compostas para carregamento de diversos formatos de lâminas, pré-processamento de imagens, construção de gráficos espaciais, treinamento de modelos de aprendizado profundo e análise de dados de imagem multiparamétrica de tecnologias como CODEX e imunofluorescência multiplex.

## Quando Usar Esta Habilidade

Aplique esta habilidade para:
- Carregar e processar imagens de lâminas inteiras (WSI) em vários formatos proprietários
- Pré-processar imagens de tecido coradas com H&E com normalização de coloração
- Fluxos de trabalho de detecção, segmentação e classificação de núcleos
- Construir gráficos de células e tecidos para análise espacial
- Treinar ou implantar modelos de aprendizado de máquina (HoVer-Net, HACTNet) em dados de patologia
- Analisar imagem multiparamétrica (CODEX, Vectra, MERFISH) para proteômica espacial
- Quantificar expressão de marcadores de imunofluorescência multiplex
- Gerenciar conjuntos de dados de patologia em larga escala com armazenamento HDF5
- Análise baseada em tiles e operações de costura

## Capacidades Principais

PathML fornece seis áreas de capacidade principais documentadas em detalhes em arquivos de referência:

### 1. Carregamento de Imagens e Formatos

Carregue imagens de lâminas inteiras de 160+ formatos proprietários, incluindo Aperio SVS, Hamamatsu NDPI, Leica SCN, Zeiss ZVI, DICOM e OME-TIFF. PathML trata automaticamente formatos específicos de fabricantes e fornece interfaces unificadas para acessar pirâmides de imagem, metadados e regiões de interesse.

**Veja:** `references/image_loading.md` para formatos suportados, estratégias de carregamento e trabalho com diferentes tipos de lâminas.

### 2. Pipelines de Pré-processamento

Construa pipelines de pré-processamento modulares ao compor transformações para manipulação de imagem, controle de qualidade, normalização de coloração, detecção de tecido e operações de máscara. A arquitetura Pipeline do PathML permite pré-processamento reproduzível e escalável em grandes conjuntos de dados.

**Transformações principais:**
- `StainNormalizationHE` - Normalização de coloração Macenko/Vahadane
- `TissueDetectionHE`, `NucleusDetectionHE` - Segmentação de tecido/núcleo
- `MedianBlur`, `GaussianBlur` - Redução de ruído
- `LabelArtifactTileHE` - Controle de qualidade para artefatos

**Veja:** `references/preprocessing.md` para catálogo completo de transformações, construção de pipeline e fluxos de trabalho de pré-processamento.

### 3. Construção de Gráficos

Construa gráficos espaciais que representem relacionamentos celulares e de nível de tecido. Extraia recursos de objetos segmentados para criar representações baseadas em gráficos adequadas para redes neurais de gráficos e análise espacial.

**Veja:** `references/graphs.md` para métodos de construção de gráficos, extração de recursos e fluxos de trabalho de análise espacial.

### 4. Aprendizado de Máquina

Treine e implante modelos de aprendizado profundo para detecção, segmentação e classificação de núcleos. PathML integra PyTorch com modelos pré-construídos (HoVer-Net, HACTNet), DataLoaders personalizados e suporte ONNX para inferência.

**Modelos principais:**
- **HoVer-Net** - Segmentação e classificação simultânea de núcleos
- **HACTNet** - Classificação hierárquica de tipo de célula

**Veja:** `references/machine_learning.md` para treinamento de modelos, avaliação, fluxos de trabalho de inferência e trabalho com conjuntos de dados públicos.

### 5. Imagem Multiparamétrica

Analise dados de proteômica espacial e expressão gênica de CODEX, Vectra, MERFISH e outras plataformas de imagem multiplex. PathML fornece classes de slide especializadas e transformações para processar dados multiparamétricos, segmentação de células com Mesmer e fluxos de trabalho de quantificação.

**Veja:** `references/multiparametric.md` para fluxos de trabalho CODEX/Vectra, segmentação de células, quantificação de marcadores e integração com AnnData.

### 6. Gerenciamento de Dados

Armazene e gerencie eficientemente grandes conjuntos de dados de patologia usando formato HDF5. PathML trata tiles, máscaras, metadados e recursos extraídos em estruturas de armazenamento unificadas otimizadas para fluxos de trabalho de aprendizado de máquina.

**Veja:** `references/data_management.md` para integração HDF5, gerenciamento de tiles, organização de conjuntos de dados e estratégias de processamento em lote.

## Início Rápido

### Instalação

```bash
# Instalar PathML
uv pip install pathml

# Com dependências opcionais para todos os recursos
uv pip install pathml[all]
```

### Exemplo de Fluxo de Trabalho Básico

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline, StainNormalizationHE, TissueDetectionHE

# Carregue uma imagem de lâmina inteira
wsi = SlideData.from_slide("path/to/slide.svs")

# Crie pipeline de pré-processamento
pipeline = Pipeline([
    TissueDetectionHE(),
    StainNormalizationHE(target='normalize', stain_estimation_method='macenko')
])

# Execute o pipeline
pipeline.run(wsi)

# Acesse tiles processados
for tile in wsi.tiles:
    processed_image = tile.image
    tissue_mask = tile.masks['tissue']
```

### Fluxos de Trabalho Comuns

**Análise de Imagem H&E:**
1. Carregue WSI com a classe de slide apropriada
2. Aplique detecção de tecido e normalização de coloração
3. Execute detecção de núcleo ou treine modelos de segmentação
4. Extraia recursos e construa gráficos espaciais
5. Conduza análise subsequente

**Imagem Multiparamétrica (CODEX):**
1. Carregue slide CODEX com `CODEXSlide`
2. Colapsar dados de canal com múltiplas execuções
3. Segmente células usando modelo Mesmer
4. Quantifique expressão de marcadores
5. Exporte para AnnData para análise de célula única

**Treinamento de Modelos ML:**
1. Prepare conjunto de dados com dados de patologia pública
2. Crie PyTorch DataLoader com conjuntos de dados PathML
3. Treine HoVer-Net ou modelos personalizados
4. Avalie em conjuntos de testes retidos
5. Implante com ONNX para inferência

## Referências para Documentação Detalhada

Ao trabalhar em tarefas específicas, consulte o arquivo de referência apropriado para informações abrangentes:

- **Carregamento de imagens:** `references/image_loading.md`
- **Fluxos de trabalho de pré-processamento:** `references/preprocessing.md`
- **Análise espacial:** `references/graphs.md`
- **Treinamento de modelos:** `references/machine_learning.md`
- **CODEX/IF multiplex:** `references/multiparametric.md`
- **Armazenamento de dados:** `references/data_management.md`

## Recursos

Esta habilidade inclui documentação de referência abrangente organizada por área de capacidade. Cada arquivo de referência contém informações detalhadas de API, exemplos de fluxo de trabalho, melhores práticas e orientação de solução de problemas para funcionalidade PathML específica.

### references/

Arquivos de documentação fornecendo cobertura aprofundada das capacidades PathML:

- `image_loading.md` - Formatos de imagem de lâmina inteira, estratégias de carregamento, classes de slide
- `preprocessing.md` - Catálogo completo de transformações, construção de pipeline, fluxos de trabalho de pré-processamento
- `graphs.md` - Métodos de construção de gráficos, extração de recursos, análise espacial
- `machine_learning.md` - Arquiteturas de modelos, fluxos de trabalho de treinamento, avaliação, inferência
- `multiparametric.md` - Análise CODEX, Vectra, IF multiplex, segmentação de células, quantificação
- `data_management.md` - Armazenamento HDF5, gerenciamento de tiles, organização de conjuntos de dados, processamento em lote

Carregue estas referências conforme necessário ao trabalhar em tarefas específicas de patologia computacional.