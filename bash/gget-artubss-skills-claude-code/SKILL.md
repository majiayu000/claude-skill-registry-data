---
name: gget
description: "Kit de ferramentas CLI/Python para consultas rápidas de bioinformática. Preferido para buscas BLAST rápidas. Acesso a 20+ bancos de dados: informações de genes (Ensembl/UniProt), AlphaFold, ARCHS4, Enrichr, OpenTargets, COSMIC, downloads de genoma. Para BLAST avançado/processamento em lote, use biopython. Para integração multi-banco de dados, use bioservices."
---

# gget

## Visão geral

gget é uma ferramenta de bioinformática de linha de comando e pacote Python que fornece acesso unificado a 20+ bancos de dados genômicos e métodos de análise. Consulte informações de genes, análise de sequências, estruturas de proteínas, dados de expressão e associações com doenças através de uma interface consistente. Todos os módulos gget funcionam tanto como ferramentas de linha de comando quanto como funções Python.

**Importante**: Os bancos de dados consultados pelo gget são continuamente atualizados, o que às vezes altera sua estrutura. Os módulos gget são testados automaticamente em base quinzenal e atualizados para corresponder às novas estruturas de banco de dados quando necessário.

## Instalação

Instale gget em um ambiente virtual limpo para evitar conflitos:

```bash
# Usando uv (recomendado)
uv pip install gget

# Ou usando pip
uv pip install --upgrade gget

# Em Python/Jupyter
import gget
```

## Início Rápido

Padrão básico de uso para todos os módulos:

```bash
# Linha de comando
gget <module> [arguments] [options]

# Python
gget.module(arguments, options)
```

A maioria dos módulos retorna:
- **Linha de comando**: JSON (padrão) ou CSV com flag `-csv`
- **Python**: DataFrame ou dicionário

Flags comuns entre módulos:
- `-o/--out`: Salvar resultados em arquivo
- `-q/--quiet`: Suprimir informações de progresso
- `-csv`: Retornar formato CSV (apenas linha de comando)

## Categorias de Módulos

### 1. Referência & Informações de Genes

#### gget ref - Downloads de Genoma de Referência

Recupere links de download e metadados para genomas de referência do Ensembl.

**Parâmetros**:
- `species`: Formato Genus_species (ex: 'homo_sapiens', 'mus_musculus'). Atalhos: 'human', 'mouse'
- `-w/--which`: Especifique tipos de retorno (gtf, cdna, dna, cds, cdrna, pep). Padrão: todos
- `-r/--release`: Número de lançamento do Ensembl (padrão: mais recente)
- `-l/--list_species`: Listar espécies de vertebrados disponíveis
- `-liv/--list_iv_species`: Listar espécies de invertebrados disponíveis
- `-ftp`: Retornar apenas links FTP
- `-d/--download`: Download de arquivos (requer curl)

**Exemplos**:
```bash
# Listar espécies disponíveis
gget ref --list_species

# Obter todos os arquivos de referência para humano
gget ref homo_sapiens

# Download apenas anotação GTF para camundongo
gget ref -w gtf -d mouse
```

```python
# Python
gget.ref("homo_sapiens")
gget.ref("mus_musculus", which="gtf", download=True)
```

#### gget search - Busca de Genes

Localize genes por nome ou descrição entre espécies.

**Parâmetros**:
- `searchwords`: Um ou mais termos de busca (case-insensitive)
- `-s/--species`: Espécie alvo (ex: 'homo_sapiens', 'mouse')
- `-r/--release`: Número de lançamento do Ensembl
- `-t/--id_type`: Retornar 'gene' (padrão) ou 'transcript'
- `-ao/--andor`: 'or' (padrão) encontra QUALQUER termo; 'and' requer TODOS
- `-l/--limit`: Máximo de resultados a retornar

**Retorna**: ensembl_id, gene_name, ensembl_description, ext_ref_description, biotype, URL

**Exemplos**:
```bash
# Buscar genes relacionados a GABA em humano
gget search -s human gaba gamma-aminobutyric

# Encontrar gene específico, requer todos os termos
gget search -s mouse -ao and pax7 transcription
```

```python
# Python
gget.search(["gaba", "gamma-aminobutyric"], species="homo_sapiens")
```

#### gget info - Informações de Gene/Transcrição

Recupere metadados abrangentes de genes e transcrições do Ensembl, UniProt e NCBI.

**Parâmetros**:
- `ens_ids`: Um ou mais IDs do Ensembl (também suporta IDs do WormBase, Flybase). Limite: ~1000 IDs
- `-n/--ncbi`: Desabilitar recuperação de dados do NCBI
- `-u/--uniprot`: Desabilitar recuperação de dados do UniProt
- `-pdb`: Incluir identificadores PDB (aumenta tempo de execução)

**Retorna**: ID UniProt, ID gene NCBI, nome de gene primário, sinônimos, nomes de proteína, descrições, biotype, transcrição canônica

**Exemplos**:
```bash
# Obter informações para múltiplos genes
gget info ENSG00000034713 ENSG00000104853 ENSG00000170296

# Incluir IDs PDB
gget info ENSG00000034713 -pdb
```

```python
# Python
gget.info(["ENSG00000034713", "ENSG00000104853"], pdb=True)
```

#### gget seq - Recuperação de Sequência

Obtenha sequências de nucleotídeos ou aminoácidos para genes e transcrições.

**Parâmetros**:
- `ens_ids`: Um ou mais identificadores do Ensembl
- `-t/--translate`: Obter sequências de aminoácidos em vez de nucleotídeos
- `-iso/--isoforms`: Retornar todas as variantes de transcrição (apenas IDs de genes)

**Retorna**: Sequências em formato FASTA

**Exemplos**:
```bash
# Obter sequências de nucleotídeos
gget seq ENSG00000034713 ENSG00000104853

# Obter todas as isoformas de proteína
gget seq -t -iso ENSG00000034713
```

```python
# Python
gget.seq(["ENSG00000034713"], translate=True, isoforms=True)
```

### 2. Análise de Sequência & Alinhamento

#### gget blast - Buscas BLAST

BLAST de sequências de nucleotídeos ou aminoácidos contra bancos de dados padrão.

**Parâmetros**:
- `sequence`: String de sequência ou caminho para arquivo FASTA/.txt
- `-p/--program`: blastn, blastp, blastx, tblastn, tblastx (auto-detectado)
- `-db/--database`:
  - Nucleotídeo: nt, refseq_rna, pdbnt
  - Proteína: nr, swissprot, pdbaa, refseq_protein
- `-l/--limit`: Máximo de hits (padrão: 50)
- `-e/--expect`: Corte de E-value (padrão: 10.0)
- `-lcf/--low_comp_filt`: Habilitar filtragem de baixa complexidade
- `-mbo/--megablast_off`: Desabilitar MegaBLAST (apenas blastn)

**Exemplos**:
```bash
# BLAST de sequência de proteína
gget blast MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# BLAST de arquivo com banco de dados específico
gget blast sequence.fasta -db swissprot -l 10
```

```python
# Python
gget.blast("MKWMFK...", database="swissprot", limit=10)
```

#### gget blat - Buscas BLAT

Localize posições genômicas de sequências usando BLAT do UCSC.

**Parâmetros**:
- `sequence`: String de sequência ou caminho para arquivo FASTA/.txt
- `-st/--seqtype`: 'DNA', 'protein', 'translated%20RNA', 'translated%20DNA' (auto-detectado)
- `-a/--assembly`: Assembly alvo (padrão: 'human'/hg38; opções: 'mouse'/mm39, 'zebrafinch'/taeGut2, etc.)

**Retorna**: genome, query size, posições de alinhamento, matches, mismatches, percentual de alinhamento

**Exemplos**:
```bash
# Encontrar localização genômica em humano
gget blat ATCGATCGATCGATCG

# Buscar em assembly diferente
gget blat -a mm39 ATCGATCGATCGATCG
```

```python
# Python
gget.blat("ATCGATCGATCGATCG", assembly="mouse")
```

#### gget muscle - Alinhamento Múltiplo de Sequências

Alinhe múltiplas sequências de nucleotídeos ou aminoácidos usando Muscle5.

**Parâmetros**:
- `fasta`: Sequências ou caminho para arquivo FASTA/.txt
- `-s5/--super5`: Usar algoritmo Super5 para processamento mais rápido (grandes datasets)

**Retorna**: Sequências alinhadas em formato ClustalW ou FASTA alinhado (.afa)

**Exemplos**:
```bash
# Alinhar sequências de arquivo
gget muscle sequences.fasta -o aligned.afa

# Usar Super5 para grande dataset
gget muscle large_dataset.fasta -s5
```

```python
# Python
gget.muscle("sequences.fasta", save=True)
```

#### gget diamond - Alinhamento Local de Sequência

Realize alinhamento local rápido de proteínas ou DNA traduzido usando DIAMOND.

**Parâmetros**:
- Query: Sequências (string/lista) ou caminho de arquivo FASTA
- `--reference`: Sequências de referência (string/lista) ou caminho de arquivo FASTA (obrigatório)
- `--sensitivity`: fast, mid-sensitive, sensitive, more-sensitive, very-sensitive (padrão), ultra-sensitive
- `--threads`: Threads de CPU (padrão: 1)
- `--diamond_db`: Salvar banco de dados para reuso
- `--translated`: Habilitar alinhamento de nucleotídeo para aminoácido

**Retorna**: Percentual de identidade, comprimentos de sequência, posições de match, gap openings, E-values, bit scores

**Exemplos**:
```bash
# Alinhar contra referência
gget diamond GGETISAWESQME -ref reference.fasta --threads 4

# Salvar banco de dados para reuso
gget diamond query.fasta -ref ref.fasta --diamond_db my_db.dmnd
```

```python
# Python
gget.diamond("GGETISAWESQME", reference="reference.fasta", threads=4)
```

### 3. Análise Estrutural & de Proteína

#### gget pdb - Estruturas de Proteína

Consulte o RCSB Protein Data Bank para estrutura e metadados.

**Parâmetros**:
- `pdb_id`: Identificador PDB (ex: '7S7U')
- `-r/--resource`: Tipo de dados (pdb, entry, pubmed, assembly, entity types)
- `-i/--identifier`: ID de assembly, entity ou chain

**Retorna**: Formato PDB (estruturas) ou JSON (metadados)

**Exemplos**:
```bash
# Download de estrutura PDB
gget pdb 7S7U -o 7S7U.pdb

# Obter metadados
gget pdb 7S7U -r entry
```

```python
# Python
gget.pdb("7S7U", save=True)
```

#### gget alphafold - Predição de Estrutura de Proteína

Preveja estruturas 3D de proteínas usando AlphaFold2 simplificado.

**Setup Obrigatório**:
```bash
# Instale OpenMM primeiro
uv pip install openmm

# Depois configure AlphaFold
gget setup alphafold
```

**Parâmetros**:
- `sequence`: Sequência de aminoácidos (string), múltiplas sequências (lista) ou arquivo FASTA. Múltiplas sequências acionam modelagem de multímero
- `-mr/--multimer_recycles`: Iterações de reciclagem (padrão: 3; recomenda-se 20 para precisão)
- `-mfm/--multimer_for_monomer`: Aplicar modelo de multímero a proteínas únicas
- `-r/--relax`: Relaxamento AMBER para modelo melhor classificado
- `plot`: Apenas Python; gerar visualização 3D interativa (padrão: True)
- `show_sidechains`: Apenas Python; incluir cadeias laterais (padrão: True)

**Retorna**: Arquivo de estrutura PDB, dados de erro de alinhamento JSON, visualização 3D opcional

**Exemplos**:
```bash
# Prever estrutura de proteína única
gget alphafold MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# Prever multímero com maior precisão
gget alphafold sequence1.fasta -mr 20 -r
```

```python
# Python com visualização
gget.alphafold("MKWMFK...", plot=True, show_sidechains=True)

# Predição de multímero
gget.alphafold(["sequence1", "sequence2"], multimer_recycles=20)
```

#### gget elm - Motivos Lineares Eucarióticos

Preveja Motivos Lineares Eucarióticos em sequências de proteína.

**Setup Obrigatório**:
```bash
gget setup elm
```

**Parâmetros**:
- `sequence`: Sequência de aminoácidos ou Acc UniProt
- `-u/--uniprot`: Indica que a sequência é Acc UniProt
- `-e/--expand`: Incluir nomes de proteína, organismos, referências
- `-s/--sensitivity`: Sensibilidade de alinhamento DIAMOND (padrão: "very-sensitive")
- `-t/--threads`: Número de threads (padrão: 1)

**Retorna**: Dois outputs:
1. **ortholog_df**: Motivos lineares de proteínas ortólogas
2. **regex_df**: Motivos correspondidos diretamente na sequência de entrada

**Exemplos**:
```bash
# Prever motivos de sequência
gget elm LIAQSIGQASFV -o results

# Usar acesso UniProt com informações expandidas
gget elm --uniprot Q02410 -e
```

```python
# Python
ortholog_df, regex_df = gget.elm("LIAQSIGQASFV")
```

### 4. Dados de Expressão & Doença

#### gget archs4 - Correlação de Genes & Expressão em Tecido

Consulte o banco de dados ARCHS4 para genes correlacionados ou dados de expressão em tecido.

**Parâmetros**:
- `gene`: Símbolo do gene ou ID do Ensembl (com flag `--ensembl`)
- `-w/--which`: 'correlation' (padrão, retorna 100 genes mais correlacionados) ou 'tissue' (atlas de expressão)
- `-s/--species`: 'human' (padrão) ou 'mouse' (apenas dados de tecido)
- `-e/--ensembl`: A entrada é ID do Ensembl

**Retorna**:
- **Modo correlation**: Símbolos de genes, coeficientes de correlação de Pearson
- **Modo tissue**: Identificadores de tecido, valores min/Q1/median/Q3/max de expressão

**Exemplos**:
```bash
# Obter genes correlacionados
gget archs4 ACE2

# Obter expressão em tecido
gget archs4 -w tissue ACE2
```

```python
# Python
gget.archs4("ACE2", which="tissue")
```

#### gget cellxgene - Dados de RNA-seq de Célula Única

Consulte CZ CELLxGENE Discover Census para dados de célula única.

**Setup Obrigatório**:
```bash
gget setup cellxgene
```

**Parâmetros**:
- `--gene` (-g): Nomes de genes ou IDs do Ensembl (case-sensitive! 'PAX7' para humano, 'Pax7' para camundongo)
- `--tissue`: Tipo(s) de tecido
- `--cell_type`: Tipo(s) de célula específicos
- `--species` (-s): 'homo_sapiens' (padrão) ou 'mus_musculus'
- `--census_version` (-cv): Versão ("stable", "latest" ou datada)
- `--ensembl` (-e): Usar IDs do Ensembl
- `--meta_only` (-mo): Retornar apenas metadados
- Filtros adicionais: disease, development_stage, sex, assay, dataset_id, donor_id, ethnicity, suspension_type

**Retorna**: Objeto AnnData com matrizes de contagem e metadados (ou dataframes apenas de metadados)

**Exemplos**:
```bash
# Obter dados de célula única para genes e tipos de célula específicos
gget cellxgene --gene ACE2 ABCA1 --tissue lung --cell_type "mucus secreting cell" -o lung_data.h5ad

# Apenas metadados
gget cellxgene --gene PAX7 --tissue muscle --meta_only -o metadata.csv
```

```python
# Python
adata = gget.cellxgene(gene=["ACE2", "ABCA1"], tissue="lung", cell_type="mucus secreting cell")
```

#### gget enrichr - Análise de Enriquecimento

Execute análise de enriquecimento de ontologia em listas de genes usando Enrichr.

**Parâmetros**:
- `genes`: Símbolos de genes ou IDs do Ensembl
- `-db/--database`: Banco de dados de referência (suporta atalhos: 'pathway', 'transcription', 'ontology', 'diseases_drugs', 'celltypes')
- `-s/--species`: human (padrão), mouse, fly, yeast, worm, fish
- `-bkg_l/--background_list`: Genes de fundo para comparação
- `-ko/--kegg_out`: Salvar imagens de vias KEGG com genes destacados
- `plot`: Apenas Python; gerar resultados gráficos

**Atalhos de Banco de Dados**:
- 'pathway' → KEGG_2021_Human
- 'transcription' → ChEA_2016
- 'ontology' → GO_Biological_Process_2021
- 'diseases_drugs' → GWAS_Catalog_2019
- 'celltypes' → PanglaoDB_Augmented_2021

**Exemplos**:
```bash
# Análise de enriquecimento para ontologia
gget enrichr -db ontology ACE2 AGT AGTR1

# Salvar vias KEGG
gget enrichr -db pathway ACE2 AGT AGTR1 -ko ./kegg_images/
```

```python
# Python com plot
gget.enrichr(["ACE2", "AGT", "AGTR1"], database="ontology", plot=True)
```

#### gget bgee - Ortologia & Expressão

Recupere dados de ortologia e expressão de genes do banco de dados Bgee.

**Parâmetros**:
- `ens_id`: ID gene do Ensembl ou ID gene NCBI (para espécies não-Ensembl). Múltiplos IDs suportados quando `type=expression`
- `-t/--type`: 'orthologs' (padrão) ou 'expression'

**Retorna**:
- **Modo orthologs**: Genes correspondentes entre espécies com IDs, nomes, informações taxonômicas
- **Modo expression**: Entidades anatômicas, pontuações de confiança, status de expressão

**Exemplos**:
```bash
# Obter ortólogos
gget bgee ENSG00000169194

# Obter dados de expressão
gget bgee ENSG00000169194 -t expression

# Múltiplos genes
gget bgee ENSBTAG00000047356 ENSBTAG00000018317 -t expression
```

```python
# Python
gget.bgee("ENSG00000169194", type="orthologs")
```

#### gget opentargets - Associações de Doença & Fármaco

Recupere associações de doença e fármaco do OpenTargets.

**Parâmetros**:
- ID gene do Ensembl (obrigatório)
- `-r/--resource`: diseases (padrão), drugs, tractability, pharmacogenetics, expression, depmap, interactions
- `-l/--limit`: Limitar contagem de resultados
- Argumentos de filtro (variam por recurso):
  - drugs: `--filter_disease`
  - pharmacogenetics: `--filter_drug`
  - expression/depmap: `--filter_tissue`, `--filter_anat_sys`, `--filter_organ`
  - interactions: `--filter_protein_a`, `--filter_protein_b`, `--filter_gene_b`

**Exemplos**:
```bash
# Obter doenças associadas
gget opentargets ENSG00000169194 -r diseases -l 5

# Obter fármacos associados
gget opentargets ENSG00000169194 -r drugs -l 10

# Obter expressão em tecido
gget opentargets ENSG00000169194 -r expression --filter_tissue brain
```

```python
# Python
gget.opentargets("ENSG00000169194", resource="diseases", limit=5)
```

#### gget cbio - cBioPortal Genômica do Câncer

Trace mapas de calor de genômica do câncer usando dados cBioPortal.

**Dois subcomandos**:

**search** - Encontrar IDs de estudo:
```bash
gget cbio search breast lung
```

**plot** - Gerar mapas de calor:

**Parâmetros**:
- `-s/--study_ids`: IDs de estudo cBioPortal separados por espaço (obrigatório)
- `-g/--genes`: Nomes de genes ou IDs do Ensembl separados por espaço (obrigatório)
- `-st/--stratification`: Coluna para organizar dados (tissue, cancer_type, cancer_type_detailed, study_id, sample)
- `-vt/--variation_type`: Tipo de dados (mutation_occurrences, cna_nonbinary, sv_occurrences, cna_occurrences, Consequence)
- `-f/--filter`: Filtrar por valor de coluna (ex: 'study_id:msk_impact_2017')
- `-dd/--data_dir`: Diretório de cache (padrão: ./gget_cbio_cache)
- `-fd/--figure_dir`: Diretório de saída (padrão: ./gget_cbio_figures)
- `-dpi`: Resolução (padrão: 100)
- `-sh/--show`: Exibir plot em janela
- `-nc/--no_confirm`: Pular confirmações de download

**Exemplos**:
```bash
# Buscar estudos
gget cbio search esophag ovary

# Criar mapa de calor
gget cbio plot -s msk_impact_2017 -g AKT1 ALK BRAF -st tissue -vt mutation_occurrences
```

```python
# Python
gget.cbio_search(["esophag", "ovary"])
gget.cbio_plot(["msk_impact_2017"], ["AKT1", "ALK"], stratification="tissue")
```

#### gget cosmic - Banco de Dados COSMIC

Busque no banco de dados COSMIC (Catalogue Of Somatic Mutations In Cancer).

**Importante**: Custos de licença se aplicam para uso comercial. Requer credenciais de conta COSMIC.

**Parâmetros**:
- `searchterm`: Nome de gene, ID do Ensembl, notação de mutação ou ID de amostra
- `-ctp/--cosmic_tsv_path`: Caminho para arquivo TSV COSMIC baixado (obrigatório para consulta)
- `-l/--limit`: Máximo de resultados (padrão: 100)

**Flags de download de banco de dados**:
- `-d/--download_cosmic`: Ativar modo de download
- `-gm/--gget_mutate`: Criar versão para gget mutate
- `-cp/--cosmic_project`: Tipo de banco de dados (cancer, census, cell_line, resistance, genome_screen, targeted_screen)
- `-cv/--cosmic_version`: Versão COSMIC
- `-gv/--grch_version`: Genoma de referência humano (37 ou 38)
- `--email`, `--password`: Credenciais COSMIC

**Exemplos**:
```bash
# Primeiro baixar banco de dados
gget cosmic -d --email user@example.com --password xxx -cp cancer

# Então consultar
gget cosmic EGFR -ctp cosmic_data.tsv -l 10
```

```python
# Python
gget.cosmic("EGFR", cosmic_tsv_path="cosmic_data.tsv", limit=10)
```

### 5. Ferramentas Adicionais

#### gget mutate - Gerar Sequências Mutadas

Gere sequências de nucleotídeos mutadas a partir de anotações de mutação.

**Parâmetros**:
- `sequences`: Caminho do arquivo FASTA ou entrada direta de sequência (string/lista)
- `-m/--mutations`: Arquivo CSV/TSV ou DataFrame com dados de mutação (obrigatório)
- `-mc/--mut_column`: Nome da coluna de mutação (padrão: 'mutation')
- `-sic/--seq_id_column`: Coluna de ID de sequência (padrão: 'seq_ID')
- `-mic/--mut_id_column`: Coluna de ID de mutação
- `-k/--k`: Comprimento de sequências flanqueadoras (padrão: 30 nucleotídeos)

**Retorna**: Sequências mutadas em formato FASTA

**Exemplos**:
```bash
# Mutação única
gget mutate ATCGCTAAGCT -m "c.4G>T"

# Múltiplas sequências com mutações de arquivo
gget mutate sequences.fasta -m mutations.csv -o mutated.fasta
```

```python
# Python
import pandas as pd
mutations_df = pd.DataFrame({"seq_ID": ["seq1"], "mutation": ["c.4G>T"]})
gget.mutate(["ATCGCTAAGCT"], mutations=mutations_df)
```

#### gget gpt - Geração de Texto com OpenAI

Gere texto em linguagem natural usando a API OpenAI.

**Setup Obrigatório**:
```bash
gget setup gpt
```

**Importante**: Tier gratuito limitado a 3 meses após criação de conta. Defina limites de faturamento mensal.

**Parâmetros**:
- `prompt`: Entrada de texto para geração (obrigatória)
- `api_key`: Autenticação OpenAI (obrigatória)
- Configuração de modelo: temperature, top_p, max_tokens, frequency_penalty, presence_penalty
- Modelo padrão: gpt-3.5-turbo (configurável)

**Exemplos**:
```bash
gget gpt "Explicar CRISPR" --api_key your_key_here
```

```python
# Python
gget.gpt("Explicar CRISPR", api_key="your_key_here")
```

#### gget setup - Instalar Dependências

Instale/baixe dependências de terceiros para módulos específicos.

**Parâmetros**:
- `module`: Nome do módulo que requer instalação de dependência
- `-o/--out`: Caminho da pasta de saída (apenas módulo elm)

**Módulos que requerem setup**:
- `alphafold` - Download de ~4GB de parâmetros de modelo
- `cellxgene` - Instala cellxgene-census (pode não suportar Python mais recente)
- `elm` - Download do banco de dados ELM local
- `gpt` - Configura integração OpenAI

**Exemplos**:
```bash
# Setup AlphaFold
gget setup alphafold

# Setup ELM com diretório customizado
gget setup elm -o /path/to/elm_data
```

```python
# Python
gget.setup("alphafold")
```

## Fluxos de Trabalho Comuns

### Fluxo de Trabalho 1: Descoberta de Gene para Análise de Sequência

Encontre e analise genes de interesse:

```python
# 1. Buscar genes
results = gget.search(["GABA", "receptor"], species="homo_sapiens")

# 2. Obter informações detalhadas
gene_ids = results["ensembl_id"].tolist()
info = gget.info(gene_ids[:5])

# 3. Recuperar sequências
sequences = gget.seq(gene_ids[:5], translate=True)
```

### Fluxo de Trabalho 2: Alinhamento de Sequência e Estrutura

Alinhe sequências e preveja estruturas:

```python
# 1. Alinhar múltiplas sequências