---
name: gtars
description: Toolkit de alta performance para análise de intervalos genômicos em Rust com bindings Python. Use ao trabalhar com regiões genômicas, arquivos BED, tracks de cobertura, detecção de sobreposições, tokenização para modelos de ML, ou análise de fragmentos em genômica computacional e aplicações de aprendizado de máquina.
---

# Gtars: Ferramentas e Algoritmos Genômicos em Rust

## Visão Geral

Gtars é um toolkit Rust de alta performance para manipular, analisar e processar dados de intervalos genômicos. Oferece ferramentas especializadas para detecção de sobreposições, análise de cobertura, tokenização para aprendizado de máquina e gerenciamento de sequências de referência.

Use esta skill ao trabalhar com:
- Arquivos de intervalos genômicos (formato BED)
- Detecção de sobreposições entre regiões genômicas
- Geração de tracks de cobertura (WIG, BigWig)
- Pré-processamento e tokenização de ML genômica
- Análise de fragmentos em genômica de célula única
- Recuperação e validação de sequência de referência

## Instalação

### Instalação Python

Instale os bindings Python do gtars:

```bash
uv pip install gtars
```

### Instalação CLI

Instale as ferramentas de linha de comando (requer Rust/Cargo):

```bash
# Instalar com todos os recursos
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Ou instalar recursos específicos apenas
cargo install gtars-cli --features "uniwig overlaprs"
```

### Biblioteca Rust

Adicione ao Cargo.toml para projetos Rust:

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## Capacidades Principais

Gtars é organizado em módulos especializados, cada um focado em tarefas específicas de análise genômica:

### 1. Detecção de Sobreposições e Indexação IGD

Detecte eficientemente sobreposições entre intervalos genômicos usando a estrutura de dados Integrated Genome Database (IGD).

**Quando usar:**
- Encontrar elementos reguladores sobrepostos
- Anotação de variantes
- Comparar picos de ChIP-seq
- Identificar características genômicas compartilhadas

**Exemplo rápido:**
```python
import gtars

# Construir índice IGD e consultar sobreposições
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

Veja `references/overlap.md` para documentação abrangente de detecção de sobreposições.

### 2. Geração de Track de Cobertura

Gere tracks de cobertura a partir de dados de sequenciamento com o módulo uniwig.

**Quando usar:**
- Perfis de acessibilidade ATAC-seq
- Visualização de cobertura ChIP-seq
- Cobertura de leitura RNA-seq
- Análise de cobertura diferencial

**Exemplo rápido:**
```bash
# Gerar track de cobertura BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

Veja `references/coverage.md` para workflows detalhados de análise de cobertura.

### 3. Tokenização Genômica

Converta regiões genômicas em tokens discretos para aplicações de aprendizado de máquina, particularmente para modelos de deep learning em dados genômicos.

**Quando usar:**
- Pré-processamento para modelos de ML genômica
- Integração com biblioteca geniml
- Criação de codificações de posição
- Treinamento de modelos transformer em sequências genômicas

**Exemplo rápido:**
```python
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

Veja `references/tokenizers.md` para documentação de tokenização.

### 4. Gerenciamento de Sequência de Referência

Gerencie sequências de genoma de referência e calcule digests seguindo o protocolo GA4GH refget.

**Quando usar:**
- Validar integridade do genoma de referência
- Extrair sequências genômicas específicas
- Calcular digests de sequência
- Comparações entre referências

**Exemplo rápido:**
```python
# Carregar referência e extrair sequências
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

Veja `references/refget.md` para operações de sequência de referência.

### 5. Processamento de Fragmentos

Divida e analise arquivos de fragmentos, particularmente útil para dados de genômica de célula única.

**Quando usar:**
- Processar dados de ATAC-seq de célula única
- Dividir fragmentos por códigos de barras de célula
- Análise de fragmentos baseada em cluster
- Controle de qualidade de fragmentos

**Exemplo rápido:**
```bash
# Dividir fragmentos por clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

Veja `references/cli.md` para comandos de processamento de fragmentos.

### 6. Pontuação de Fragmentos

Pontue sobreposições de fragmentos contra datasets de referência.

**Quando usar:**
- Avaliar enriquecimento de fragmentos
- Comparar dados experimentais com referências
- Computação de métricas de qualidade
- Pontuação em lote entre amostras

**Exemplo rápido:**
```bash
# Pontuar fragmentos contra referência
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## Workflows Comuns

### Workflow 1: Análise de Sobreposição de Picos

Identifique características genômicas sobrepostas:

```python
import gtars

# Carregar dois conjuntos de regiões
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# Encontrar sobreposições
overlapping_peaks = peaks.filter_overlapping(promoters)

# Exportar resultados
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### Workflow 2: Pipeline de Track de Cobertura

Gere tracks de cobertura para visualização:

```bash
# Etapa 1: Gerar cobertura
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# Etapa 2: Converter para BigWig para genome browsers
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### Workflow 3: Pré-processamento de ML

Prepare dados genômicos para aprendizado de máquina:

```python
from gtars.tokenizers import TreeTokenizer
import gtars

# Etapa 1: Carregar regiões de treinamento
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# Etapa 2: Criar tokenizer
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# Etapa 3: Tokenizar regiões
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# Etapa 4: Usar tokens no pipeline de ML
# (integrar com geniml ou modelos personalizados)
```

## Uso de Python vs CLI

**Use API Python quando:**
- Integrar com pipelines de análise
- Precisar de controle programático
- Trabalhar com NumPy/Pandas
- Construir workflows personalizados

**Use CLI quando:**
- Análises rápidas e únicas
- Scripting em shell
- Processamento em lote de arquivos
- Prototipar workflows

## Documentação de Referência

Documentação abrangente de módulos:

- **`references/python-api.md`** - Referência completa da API Python com operações RegionSet, integração NumPy e exportação de dados
- **`references/overlap.md`** - Indexação IGD, detecção de sobreposições e operações de conjunto
- **`references/coverage.md`** - Geração de track de cobertura com uniwig
- **`references/tokenizers.md`** - Tokenização genômica para aplicações de ML
- **`references/refget.md`** - Gerenciamento de sequência de referência e digests
- **`references/cli.md`** - Referência completa da interface de linha de comando

## Integração com geniml

Gtars funciona como a base para o pacote Python geniml, fornecendo operações principais de intervalo genômico para workflows de aprendizado de máquina. Ao trabalhar em tarefas relacionadas a geniml, use gtars para pré-processamento de dados e tokenização.

## Características de Performance

- **Performance nativa Rust**: Execução rápida com baixa sobrecarga de memória
- **Processamento paralelo**: Operações multi-thread para grandes datasets
- **Eficiência de memória**: Suporte a streaming e memory-mapped files
- **Operações zero-copy**: Integração NumPy com cópia mínima de dados

## Formatos de Dados

Gtars funciona com formatos genômicos padrão:

- **BED**: Intervalos genômicos (3 colunas ou estendido)
- **WIG/BigWig**: Tracks de cobertura
- **FASTA**: Sequências de referência
- **Fragment TSV**: Arquivos de fragmentos de célula única com códigos de barras

## Tratamento de Erros e Depuração

Ative logging verboso para solução de problemas:

```python
import gtars

# Ativar logging de debug
gtars.set_log_level("DEBUG")
```

```bash
# Modo verbose da CLI
gtars --verbose <command>
```