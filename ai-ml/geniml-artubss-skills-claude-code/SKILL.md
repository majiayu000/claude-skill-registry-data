---
name: geniml
description: Essa habilidade deve ser usada ao trabalhar com dados de intervalos genômicos (arquivos BED) para tarefas de machine learning. Use para treinar embeddings de regiões (Region2Vec, BEDspace), análise de scATAC-seq de célula única (scEmbed), construir picos consensuais (universos), ou qualquer análise baseada em ML de regiões genômicas. Aplica-se a coleções de arquivos BED, dados scATAC-seq, conjuntos de dados de acessibilidade de cromatina e aprendizado de recursos genômicos baseado em regiões.
---

# Geniml: Machine Learning em Intervalos Genômicos

## Visão Geral

Geniml é um pacote Python para construir modelos de machine learning em dados de intervalos genômicos de arquivos BED. Ele fornece métodos não supervisionados para aprender embeddings de regiões genômicas, células únicas e rótulos de metadados, habilitando buscas por similaridade, agrupamento e tarefas de ML subsequentes.

## Instalação

Instale geniml usando uv:

```bash
uv uv pip install geniml
```

Para dependências de ML (PyTorch, etc.):

```bash
uv uv pip install 'geniml[ml]'
```

Versão de desenvolvimento do GitHub:

```bash
uv uv pip install git+https://github.com/databio/geniml.git
```

## Capacidades Principais

Geniml fornece cinco capacidades primárias, cada uma detalhada em arquivos de referência dedicados:

### 1. Region2Vec: Embeddings de Regiões Genômicas

Treine embeddings não supervisionados de regiões genômicas usando aprendizado estilo word2vec.

**Use para:** Redução de dimensionalidade de arquivos BED, análise de similaridade de regiões, vetores de recursos para ML subsequente.

**Workflow:**
1. Tokenize arquivos BED usando uma referência de universo
2. Treine o modelo Region2Vec nos tokens
3. Gere embeddings para regiões

**Referência:** Veja `references/region2vec.md` para workflow detalhado, parâmetros e exemplos.

### 2. BEDspace: Embeddings Conjuntos de Regiões e Metadados

Treine embeddings compartilhados para conjuntos de regiões e rótulos de metadados usando StarSpace.

**Use para:** Buscas conscientes de metadados, consultas entre modalidades (região→rótulo ou rótulo→região), análise conjunta de conteúdo genômico e condições experimentais.

**Workflow:**
1. Pré-processe regiões e metadados
2. Treine o modelo BEDspace
3. Calcule distâncias
4. Faça consultas entre regiões e rótulos

**Referência:** Veja `references/bedspace.md` para workflow detalhado, tipos de busca e exemplos.

### 3. scEmbed: Embeddings de Acessibilidade de Cromatina de Célula Única

Treine modelos Region2Vec em dados scATAC-seq para embeddings em nível de célula.

**Use para:** Agrupamento de scATAC-seq, anotação de tipo de célula, redução de dimensionalidade de células únicas, integração com workflows scanpy.

**Workflow:**
1. Prepare AnnData com coordenadas de picos
2. Pré-tokenize células
3. Treine o modelo scEmbed
4. Gere embeddings de células
5. Agrupe e visualize com scanpy

**Referência:** Veja `references/scembed.md` para workflow detalhado, parâmetros e exemplos.

### 4. Picos Consensuais: Construção de Universos

Construa conjuntos de picos de referência (universos) a partir de coleções de arquivos BED usando múltiplos métodos estatísticos.

**Use para:** Criar referências de tokenização, padronizar regiões entre conjuntos de dados, definir recursos consensuais com rigor estatístico.

**Workflow:**
1. Combine arquivos BED
2. Gere pistas de cobertura
3. Construa universo usando método CC, CCF, ML ou HMM

**Métodos:**
- **CC (Corte de Cobertura)**: Baseado em limiar simples
- **CCF (Corte de Cobertura Flexível)**: Intervalos de confiança para limites
- **ML (Máxima Verossimilhança)**: Modelagem probabilística de posições
- **HMM (Modelo de Markov Oculto)**: Modelagem complexa de estados

**Referência:** Veja `references/consensus_peaks.md` para comparação de métodos, parâmetros e exemplos.

### 5. Utilitários: Ferramentas de Suporte

Ferramentas adicionais para cache, aleatorização, avaliação e busca.

**Utilitários disponíveis:**
- **BBClient**: Cache de arquivos BED para acesso repetido
- **BEDshift**: Aleatorização preservando contexto genômico
- **Evaluation**: Métricas para qualidade de embeddings (silhueta, Davies-Bouldin, etc.)
- **Tokenization**: Utilitários de tokenização de regiões (hard, soft, baseada em universo)
- **Text2BedNN**: Backends de busca neural para consultas genômicas

**Referência:** Veja `references/utilities.md` para uso detalhado de cada utilitário.

## Workflows Comuns

### Pipeline Básico de Embedding de Regiões

```python
from geniml.tokenization import hard_tokenization
from geniml.region2vec import region2vec
from geniml.evaluation import evaluate_embeddings

# Passo 1: Tokenize arquivos BED
hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokens/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)

# Passo 2: Treine Region2Vec
region2vec(
    token_folder='tokens/',
    save_dir='model/',
    num_shufflings=1000,
    embedding_dim=100
)

# Passo 3: Avalie
metrics = evaluate_embeddings(
    embeddings_file='model/embeddings.npy',
    labels_file='metadata.csv'
)
```

### Pipeline de Análise de scATAC-seq

```python
import scanpy as sc
from geniml.scembed import ScEmbed
from geniml.io import tokenize_cells

# Passo 1: Carregue dados
adata = sc.read_h5ad('scatac_data.h5ad')

# Passo 2: Tokenize células
tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokens.parquet'
)

# Passo 3: Treine scEmbed
model = ScEmbed(embedding_dim=100)
model.train(dataset='tokens.parquet', epochs=100)

# Passo 4: Gere embeddings
embeddings = model.encode(adata)
adata.obsm['scembed_X'] = embeddings

# Passo 5: Agrupe com scanpy
sc.pp.neighbors(adata, use_rep='scembed_X')
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

### Construção de Universo e Avaliação

```bash
# Gere cobertura
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# Construa universo com corte de cobertura
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50

# Avalie qualidade do universo
geniml universe evaluate \
  --universe universe.bed \
  --coverage-folder coverage/ \
  --bed-folder bed_files/
```

## Referência de CLI

Geniml fornece interfaces de linha de comando para operações principais:

```bash
# Treinamento de Region2Vec
geniml region2vec --token-folder tokens/ --save-dir model/ --num-shuffle 1000

# Pré-processamento de BEDspace
geniml bedspace preprocess --input regions/ --metadata labels.csv --universe universe.bed

# Treinamento de BEDspace
geniml bedspace train --input preprocessed.txt --output model/ --dim 100

# Busca em BEDspace
geniml bedspace search -t r2l -d distances.pkl -q query.bed -n 10

# Construção de universo
geniml universe build cc --coverage-folder coverage/ --output universe.bed --cutoff 5

# Aleatorização com BEDshift
geniml bedshift --input peaks.bed --genome hg38 --preserve-chrom --iterations 100
```

## Quando Usar Qual Ferramenta

**Use Region2Vec quando:**
- Trabalhar com dados genômicos em volume (ChIP-seq, ATAC-seq, etc.)
- Precisar de embeddings não supervisionados sem metadados
- Comparar conjuntos de regiões entre experimentos
- Construir recursos para aprendizado supervisionado subsequente

**Use BEDspace quando:**
- Metadados disponíveis (tipos de célula, tecidos, condições)
- Precisar fazer consultas de regiões por metadados ou vice-versa
- Desejar espaço de embedding conjunta para regiões e rótulos
- Construir bancos de dados genômicos pesquisáveis

**Use scEmbed quando:**
- Analisar dados de scATAC-seq de célula única
- Agrupar células por acessibilidade de cromatina
- Anotar tipos de célula a partir de scATAC-seq
- Integração com scanpy é desejada

**Use Construção de Universo quando:**
- Precisar de conjuntos de picos de referência para tokenização
- Combinar múltiplos experimentos em consenso
- Desejar definições de regiões rigorosas estatisticamente
- Construir referências padrão para um projeto

**Use Utilitários quando:**
- Precisar fazer cache de arquivos BED remotos (BBClient)
- Gerar modelos nulos para estatísticas (BEDshift)
- Avaliar qualidade de embeddings (Evaluation)
- Construir interfaces de busca (Text2BedNN)

## Melhores Práticas

### Diretrizes Gerais

- **Qualidade do universo é crítica**: Invista tempo na construção de universos abrangentes e bem construídos
- **Validação de tokenização**: Verifique cobertura (>80% é ideal) antes de treinar
- **Ajuste de parâmetros**: Experimente dimensões de embedding, taxas de aprendizado e épocas de treinamento
- **Avaliação**: Sempre valide embeddings com múltiplas métricas e visualizações
- **Documentação**: Registre parâmetros e seeds aleatórias para reprodutibilidade

### Considerações de Desempenho

- **Pré-tokenização**: Para scEmbed, sempre pré-tokenize células para treinamento mais rápido
- **Gerenciamento de memória**: Conjuntos de dados grandes podem exigir processamento em lotes ou downsampling
- **Recursos computacionais**: Métodos ML/HMM de universo são computacionalmente intensivos
- **Cache de modelo**: Use BBClient para evitar downloads repetidos

### Padrões de Integração

- **Com scanpy**: Embeddings de scEmbed se integram perfeitamente como entradas `adata.obsm`
- **Com BEDbase**: Use BBClient para acessar repositórios BED remotos
- **Com Hugging Face**: Exporte modelos treinados para compartilhamento e reprodutibilidade
- **Com R**: Use reticulate para integração R (veja referência de utilitários)

## Projetos Relacionados

Geniml faz parte do ecossistema BEDbase:

- **BEDbase**: Plataforma unificada para regiões genômicas
- **BEDboss**: Pipeline de processamento para arquivos BED
- **Gtars**: Ferramentas e utilitários genômicos
- **BBClient**: Cliente para repositórios BEDbase

## Recursos Adicionais

- **Documentação**: https://docs.bedbase.org/geniml/
- **GitHub**: https://github.com/databio/geniml
- **Modelos pré-treinados**: Disponíveis no Hugging Face (organização databio)
- **Publicações**: Citadas na documentação para detalhes metodológicos

## Solução de Problemas

**"Cobertura de tokenização muito baixa":**
- Verifique qualidade e completude do universo
- Ajuste limiar de p-value (tente 1e-6 em vez de 1e-9)
- Garanta que universo corresponda à montagem do genoma

**"Treinamento não convergindo":**
- Ajuste taxa de aprendizado (tente intervalo 0.01-0.05)
- Aumente épocas de treinamento
- Verifique qualidade de dados e pré-processamento

**"Erros de falta de memória":**
- Reduza tamanho de lote para scEmbed
- Processe dados em chunques
- Use pré-tokenização para dados de célula única

**"StarSpace não encontrado" (BEDspace):**
- Instale StarSpace separadamente: https://github.com/facebookresearch/StarSpace
- Defina parâmetro `--path-to-starspace` corretamente

Para solução de problemas detalhada e questões específicas do método, consulte o arquivo de referência apropriado.