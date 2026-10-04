---
name: lamindb
description: Esta habilidade deve ser usada ao trabalhar com LaminDB, um framework de dados de código aberto para biologia que torna dados consultáveis, rastreáveis, reproduzíveis e FAIR. Use ao gerenciar datasets biológicos (scRNA-seq, espacial, citometria de fluxo, etc.), rastrear workflows computacionais, curar e validar dados com ontologias biológicas, construir data lakehouses, ou garantir linhagem de dados e reprodutibilidade em pesquisa biológica. Aborda gerenciamento de dados, anotação, ontologias (genes, tipos de célula, doenças, tecidos), validação de esquema, integrações com orquestradores de workflow (Nextflow, Snakemake) e plataformas MLOps (W&B, MLflow), e estratégias de deployment.
---

# LaminDB

## Visão Geral

LaminDB é um framework de dados de código aberto para biologia projetado para tornar dados consultáveis, rastreáveis, reproduzíveis e FAIR (Encontráveis, Acessíveis, Interoperáveis, Reutilizáveis). Fornece uma plataforma unificada que combina arquitetura lakehouse, rastreamento de linhagem, feature stores, ontologias biológicas, capacidades LIMS (Laboratory Information Management System) e ELN (Electronic Lab Notebook) através de uma única API Python.

**Proposta de Valor Principal:**
- **Consultabilidade**: Pesquisar e filtrar datasets por metadados, features e termos de ontologia
- **Rastreabilidade**: Rastreamento automático de linhagem de dados brutos até análise e resultados
- **Reprodutibilidade**: Controle de versão para dados, código e ambiente
- **Conformidade FAIR**: Anotações padronizadas usando ontologias biológicas

## Quando Usar Esta Habilidade

Use esta habilidade quando:

- **Gerenciar datasets biológicos**: scRNA-seq, bulk RNA-seq, transcriptômica espacial, citometria de fluxo, dados multimodais, dados de prontuário eletrônico
- **Rastrear workflows computacionais**: Notebooks, scripts, execução de pipeline (Nextflow, Snakemake, Redun)
- **Curar e validar dados**: Validação de esquema, padronização, anotação baseada em ontologia
- **Trabalhar com ontologias biológicas**: Genes, proteínas, tipos de célula, tecidos, doenças, pathways (via Bionty)
- **Construir data lakehouses**: Interface de consulta unificada em múltiplos datasets
- **Garantir reprodutibilidade**: Versionamento automático, rastreamento de linhagem, captura de ambiente
- **Integrar pipelines ML**: Conectar com Weights & Biases, MLflow, HuggingFace, scVI-tools
- **Fazer deploy de infraestrutura de dados**: Configurar sistemas de gerenciamento de dados locais ou baseados em nuvem
- **Colaborar em datasets**: Compartilhar dados curados e anotados com metadados padronizados

## Capacidades Principais

LaminDB oferece seis áreas de capacidade interconectadas, cada uma documentada em detalhes na pasta references.

### 1. Conceitos Centrais e Linhagem de Dados

**Entidades principais:**
- **Artifacts**: Datasets versionados (DataFrame, AnnData, Parquet, Zarr, etc.)
- **Records**: Entidades experimentais (amostras, perturbações, instrumentos)
- **Runs & Transforms**: Rastreamento de linhagem computacional (qual código produziu quais dados)
- **Features**: Campos de metadados tipados para anotação e consulta

**Workflows principais:**
- Criar e versionar artifacts de arquivos ou objetos Python
- Rastrear execução de notebook/script com `ln.track()` e `ln.finish()`
- Anotar artifacts com features tipadas
- Visualizar gráficos de linhagem de dados com `artifact.view_lineage()`
- Consultar por proveniência (encontrar todos os outputs de código/inputs específicos)

**Referência:** `references/core-concepts.md` - Leia para informações detalhadas sobre artifacts, records, runs, transforms, features, versionamento e rastreamento de linhagem.

### 2. Gerenciamento de Dados e Consultas

**Capacidades de consulta:**
- Exploração e lookup de registry com auto-complete
- Recuperação de registro único com `get()`, `one()`, `one_or_none()`
- Filtragem com operadores de comparação (`__gt`, `__lte`, `__contains`, `__startswith`)
- Consultas baseadas em features (consultar por metadados anotados)
- Traversal entre registries com sintaxe de duplo underscore
- Busca de texto completo em registries
- Consultas lógicas avançadas com objetos Q (AND, OR, NOT)
- Streaming de datasets grandes sem carregar em memória

**Workflows principais:**
- Navegar artifacts com filtros e ordenação
- Consultar por features, data de criação, criador, tamanho, etc.
- Fazer streaming de arquivos grandes em chunks ou com slicing de array
- Organizar dados com chaves hierárquicas
- Agrupar artifacts em collections

**Referência:** `references/data-management.md` - Leia para padrões de consulta abrangentes, exemplos de filtragem, estratégias de streaming e melhores práticas de organização de dados.

### 3. Anotação e Validação

**Processo de curação:**
1. **Validação**: Confirmar que datasets correspondem aos esquemas desejados
2. **Padronização**: Corrigir typos, mapear sinônimos para termos canônicos
3. **Anotação**: Vincular datasets a entidades de metadados para consultabilidade

**Tipos de esquema:**
- **Esquemas flexíveis**: Validar apenas colunas conhecidas, permitir metadados adicionais
- **Esquemas minimamente necessários**: Especificar colunas essenciais, permitir extras
- **Esquemas rígidos**: Controle completo sobre estrutura e valores

**Tipos de dados suportados:**
- DataFrames (Parquet, CSV)
- AnnData (genômica de célula única)
- MuData (multimodal)
- SpatialData (transcriptômica espacial)
- TileDB-SOMA (arrays escaláveis)

**Workflows principais:**
- Definir features e esquemas para validação de dados
- Usar `DataFrameCurator` ou `AnnDataCurator` para validação
- Padronizar valores com `.cat.standardize()`
- Mapear para ontologias com `.cat.add_ontology()`
- Salvar artifacts curados com vinculação de esquema
- Consultar datasets validados por features

**Referência:** `references/annotation-validation.md` - Leia para workflows de curação detalhados, padrões de design de esquema, tratamento de erros de validação e melhores práticas.

### 4. Ontologias Biológicas

**Ontologias disponíveis (via Bionty):**
- Genes (Ensembl), Proteínas (UniProt)
- Tipos de célula (CL), Linhagens celulares (CLO)
- Tecidos (Uberon), Doenças (Mondo, DOID)
- Fenótipos (HPO), Pathways (GO)
- Fatores experimentais (EFO), Estágios de desenvolvimento
- Organismos (NCBItaxon), Drogas (DrugBank)

**Workflows principais:**
- Importar ontologias públicas com `bt.CellType.import_source()`
- Pesquisar ontologias com correspondência de palavra-chave ou exata
- Padronizar termos usando mapeamento de sinônimos
- Explorar relacionamentos hierárquicos (pais, filhos, ancestrais)
- Validar dados contra termos de ontologia
- Anotar datasets com registros de ontologia
- Criar termos e hierarquias customizadas
- Tratar contextos multiorganismo (humano, camundongo, etc.)

**Referência:** `references/ontologies.md` - Leia para operações abrangentes de ontologia, estratégias de padronização, navegação de hierarquia e workflows de anotação.

### 5. Integrações

**Orquestradores de workflow:**
- Nextflow: Rastrear processos e outputs de pipeline
- Snakemake: Integrar em regras de Snakemake
- Redun: Combinar com rastreamento de tarefas de Redun

**Plataformas MLOps:**
- Weights & Biases: Vincular experimentos com artifacts de dados
- MLflow: Rastrear modelos e experimentos
- HuggingFace: Rastrear fine-tuning de modelos
- scVI-tools: Workflows de análise de célula única

**Sistemas de armazenamento:**
- Sistema de arquivos local, AWS S3, Google Cloud Storage
- Compatível com S3 (MinIO, Cloudflare R2)
- Endpoints HTTP/HTTPS (somente leitura)
- Datasets HuggingFace

**Array stores:**
- TileDB-SOMA (com suporte cellxgene)
- DuckDB para consultas SQL em arquivos Parquet

**Visualização:**
- Vitessce para visualização interativa espacial/célula única

**Controle de versão:**
- Integração Git para rastreamento de código-fonte

**Referência:** `references/integrations.md` - Leia para padrões de integração, exemplos de código e troubleshooting para sistemas de terceiros.

### 6. Configuração e Deployment

**Instalação:**
- Básico: `uv pip install lamindb`
- Com extras: `uv pip install 'lamindb[gcp,zarr,fcs]'`
- Módulos: bionty, wetlab, clinical

**Tipos de instância:**
- SQLite local (desenvolvimento)
- Cloud storage + SQLite (pequenas equipes)
- Cloud storage + PostgreSQL (produção)

**Opções de armazenamento:**
- Sistema de arquivos local
- AWS S3 com regiões e permissões configuráveis
- Google Cloud Storage
- Endpoints compatíveis com S3 (MinIO, Cloudflare R2)

**Configuração:**
- Gerenciamento de cache para arquivos em nuvem
- Configurações de sistema multiusuário
- Sincronização de repositório Git
- Variáveis de ambiente

**Padrões de deployment:**
- Migração dev local → produção em nuvem
- Deployments multi-região
- Armazenamento compartilhado com instâncias pessoais

**Referência:** `references/setup-deployment.md` - Leia para instalação detalhada, configuração, setup de armazenamento, gerenciamento de banco de dados, melhores práticas de segurança e troubleshooting.

## Workflows de Casos de Uso Comuns

### Caso de Uso 1: Análise de RNA-seq de Célula Única com Validação de Ontologia

```python
import lamindb as ln
import bionty as bt
import anndata as ad

# Iniciar rastreamento
ln.track(params={"analysis": "scRNA-seq QC and annotation"})

# Importar ontologia de tipo de célula
bt.CellType.import_source()

# Carregar dados
adata = ad.read_h5ad("raw_counts.h5ad")

# Validar e padronizar tipos de célula
adata.obs["cell_type"] = bt.CellType.standardize(adata.obs["cell_type"])

# Curar com esquema
curator = ln.curators.AnnDataCurator(adata, schema)
curator.validate()
artifact = curator.save_artifact(key="scrna/validated.h5ad")

# Vincular anotações de ontologia
cell_types = bt.CellType.from_values(adata.obs.cell_type)
artifact.feature_sets.add_ontology(cell_types)

ln.finish()
```

### Caso de Uso 2: Construindo um Data Lakehouse Consultável

```python
import lamindb as ln

# Registrar múltiplos experimentos
for i, file in enumerate(data_files):
    artifact = ln.Artifact.from_anndata(
        ad.read_h5ad(file),
        key=f"scrna/batch_{i}.h5ad",
        description=f"scRNA-seq batch {i}"
    ).save()

    # Anotar com features
    artifact.features.add_values({
        "batch": i,
        "tissue": tissues[i],
        "condition": conditions[i]
    })

# Consultar em todos os experimentos
immune_datasets = ln.Artifact.filter(
    key__startswith="scrna/",
    tissue="PBMC",
    condition="treated"
).to_dataframe()

# Carregar datasets específicos
for artifact in immune_datasets:
    adata = artifact.load()
    # Analisar
```

### Caso de Uso 3: Pipeline ML com Integração W&B

```python
import lamindb as ln
import wandb

# Inicializar ambos os sistemas
wandb.init(project="drug-response", name="exp-42")
ln.track(params={"model": "random_forest", "n_estimators": 100})

# Carregar dados de treinamento do LaminDB
train_artifact = ln.Artifact.get(key="datasets/train.parquet")
train_data = train_artifact.load()

# Treinar modelo
model = train_model(train_data)

# Fazer log em W&B
wandb.log({"accuracy": 0.95})

# Salvar modelo no LaminDB com vinculação a W&B
import joblib
joblib.dump(model, "model.pkl")
model_artifact = ln.Artifact("model.pkl", key="models/exp-42.pkl").save()
model_artifact.features.add_values({"wandb_run_id": wandb.run.id})

ln.finish()
wandb.finish()
```

### Caso de Uso 4: Integração com Pipeline Nextflow

```python
# Em script de processo Nextflow
import lamindb as ln

ln.track()

# Carregar artifact de entrada
input_artifact = ln.Artifact.get(key="raw/batch_${batch_id}.fastq.gz")
input_path = input_artifact.cache()

# Processar (alinhamento, quantificação, etc.)
# ... lógica de processo Nextflow ...

# Salvar output
output_artifact = ln.Artifact(
    "counts.csv",
    key="processed/batch_${batch_id}_counts.csv"
).save()

ln.finish()
```

## Checklist de Começando

Para começar a usar LaminDB efetivamente:

1. **Instalação & Configuração** (`references/setup-deployment.md`)
   - Instalar LaminDB e extras necessários
   - Autenticar com `lamin login`
   - Inicializar instância com `lamin init --storage ...`

2. **Aprender Conceitos Centrais** (`references/core-concepts.md`)
   - Entender Artifacts, Records, Runs, Transforms
   - Praticar criação e recuperação de artifacts
   - Implementar `ln.track()` e `ln.finish()` em workflows

3. **Dominar Consultas** (`references/data-management.md`)
   - Praticar filtragem e pesquisa de registries
   - Aprender consultas baseadas em features
   - Experimentar streaming de arquivos grandes

4. **Configurar Validação** (`references/annotation-validation.md`)
   - Definir features relevantes ao domínio de pesquisa
   - Criar esquemas para tipos de dados
   - Praticar workflows de curação

5. **Integrar Ontologias** (`references/ontologies.md`)
   - Importar ontologias biológicas relevantes (genes, tipos de célula, etc.)
   - Validar anotações existentes
   - Padronizar metadados com termos de ontologia

6. **Conectar Ferramentas** (`references/integrations.md`)
   - Integrar com orquestradores de workflow existentes
   - Vincular plataformas ML para rastreamento de experimentos
   - Configurar armazenamento em nuvem e compute

## Princípios Principais

Siga esses princípios ao trabalhar com LaminDB:

1. **Rastreie tudo**: Use `ln.track()` no início de toda análise para captura automática de linhagem

2. **Valide cedo**: Defina esquemas e valide dados antes de análise extensa

3. **Use ontologias**: Aproveite ontologias biológicas públicas para anotações padronizadas

4. **Organize com chaves**: Estruture chaves de artifact hierarquicamente (ex: `project/experiment/batch/file.h5ad`)

5. **Consulte metadados primeiro**: Filtre e pesquise antes de carregar arquivos grandes

6. **Versione, não duplique**: Use versionamento integrado em vez de criar novas chaves para modificações

7. **Anote com features**: Defina features tipadas para metadados consultáveis

8. **Documente completamente**: Adicione descrições a artifacts, esquemas e transforms

9. **Aproveite a linhagem**: Use `view_lineage()` para entender proveniência de dados

10. **Comece localmente, escale para nuvem**: Desenvolva localmente com SQLite, faça deploy em nuvem com PostgreSQL

## Arquivos de Referência

Esta habilidade inclui documentação de referência abrangente organizada por capacidade:

- **`references/core-concepts.md`** - Artifacts, records, runs, transforms, features, versionamento, linhagem
- **`references/data-management.md`** - Consultas, filtragem, pesquisa, streaming, organização de dados
- **`references/annotation-validation.md`** - Design de esquema, workflows de curação, estratégias de validação
- **`references/ontologies.md`** - Gerenciamento de ontologia biológica, padronização, hierarquias
- **`references/integrations.md`** - Orquestradores de workflow, plataformas MLOps, sistemas de armazenamento, ferramentas
- **`references/setup-deployment.md`** - Instalação, configuração, deployment, troubleshooting

Leia o(s) arquivo(s) de referência relevante(s) baseado na capacidade específica de LaminDB necessária para a tarefa em mãos.

## Recursos Adicionais

- **Documentação Oficial**: https://docs.lamin.ai
- **Referência de API**: https://docs.lamin.ai/api
- **Repositório GitHub**: https://github.com/laminlabs/lamindb
- **Tutorial**: https://docs.lamin.ai/tutorial
- **FAQ**: https://docs.lamin.ai/faq