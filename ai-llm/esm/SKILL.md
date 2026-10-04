---
name: esm
description: Conjunto abrangente de ferramentas para modelos de linguagem de proteínas, incluindo ESM3 (design multimodal generativo de proteínas em sequência, estrutura e função) e ESM C (embeddings e representações eficientes de proteínas). Use essa skill ao trabalhar com sequências de proteínas, estruturas ou predição de função; designing de proteínas inovadoras; geração de embeddings de proteínas; inverse folding; ou tarefas de engenharia de proteínas. Suporta tanto uso local de modelos quanto Forge API baseada em nuvem para inferência escalável.
---

# ESM: Evolutionary Scale Modeling

## Visão Geral

O ESM oferece modelos de linguagem de proteína de última geração para entender, gerar e designing de proteínas. Essa skill permite trabalhar com duas famílias de modelos: ESM3 para design generativo de proteínas em sequência, estrutura e função, e ESM C para aprendizado eficiente de representações de proteínas e embeddings.

## Capacidades Principais

### 1. Geração de Sequência de Proteína com ESM3

Gere sequências de proteínas inovadoras com propriedades desejadas usando modelagem generativa multimodal.

**Quando usar:**
- Designing de proteínas com propriedades funcionais específicas
- Conclusão de sequências de proteína parciais
- Geração de variantes de proteínas existentes
- Criação de proteínas com características estruturais desejadas

**Uso básico:**

```python
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# Load model locally
model: ESM3InferenceClient = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

# Create protein prompt
protein = ESMProtein(sequence="MPRT___KEND")  # '_' representa posições mascaradas

# Generate completion
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
print(protein.sequence)
```

**Para uso remoto/nuvem via Forge API:**

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
from esm.sdk.api import ESMProtein, GenerationConfig

# Connect to Forge
model = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", url="https://forge.evolutionaryscale.ai", token="<token>")

# Generate
protein = model.generate(protein, GenerationConfig(track="sequence", num_steps=8))
```

Veja `references/esm3-api.md` para especificações detalhadas do modelo ESM3, configurações avançadas de geração e exemplos de prompting multimodal.

### 2. Predição de Estrutura e Inverse Folding

Use a track de estrutura do ESM3 para predição de estrutura a partir da sequência ou inverse folding (design de sequência a partir da estrutura).

**Predição de estrutura:**

```python
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

# Predict structure from sequence
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_with_structure = model.generate(
    protein,
    GenerationConfig(track="structure", num_steps=protein.sequence.count("_"))
)

# Access predicted structure
coordinates = protein_with_structure.coordinates  # 3D coordinates
pdb_string = protein_with_structure.to_pdb()
```

**Inverse folding (sequência a partir de estrutura):**

```python
# Design sequence for a target structure
protein_with_structure = ESMProtein.from_pdb("target_structure.pdb")
protein_with_structure.sequence = None  # Remove sequence

# Generate sequence that folds to this structure
designed_protein = model.generate(
    protein_with_structure,
    GenerationConfig(track="sequence", num_steps=50, temperature=0.7)
)
```

### 3. Embeddings de Proteína com ESM C

Gere embeddings de alta qualidade para tarefas downstream como predição de função, classificação ou análise de similaridade.

**Quando usar:**
- Extração de representações de proteína para aprendizado de máquina
- Cálculo de similaridades de sequência
- Extração de features para classificação de proteínas
- Transfer learning para tarefas relacionadas a proteínas

**Uso básico:**

```python
from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein

# Load ESM C model
model = ESMC.from_pretrained("esmc-300m").to("cuda")

# Get embeddings
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP...")
protein_tensor = model.encode(protein)

# Generate embeddings
embeddings = model.forward(protein_tensor)
```

**Processamento em lote:**

```python
# Encode multiple proteins
proteins = [
    ESMProtein(sequence="MPRTKEIND..."),
    ESMProtein(sequence="AGLIVHSPQ..."),
    ESMProtein(sequence="KTEFLNDGR...")
]

embeddings_list = [model.logits(model.forward(model.encode(p))) for p in proteins]
```

Veja `references/esm-c-api.md` para detalhes do modelo ESM C, comparações de eficiência e estratégias avançadas de embedding.

### 4. Condicionamento e Anotação de Função

Use a track de função do ESM3 para gerar proteínas com anotações funcionais específicas ou prever função a partir da sequência.

**Geração condicionada a função:**

```python
from esm.sdk.api import ESMProtein, FunctionAnnotation, GenerationConfig

# Create protein with desired function
protein = ESMProtein(
    sequence="_" * 200,  # Generate 200 residue protein
    function_annotations=[
        FunctionAnnotation(label="fluorescent_protein", start=50, end=150)
    ]
)

# Generate sequence with specified function
functional_protein = model.generate(
    protein,
    GenerationConfig(track="sequence", num_steps=200)
)
```

### 5. Geração com Chain-of-Thought

Refine iterativamente designs de proteínas usando a abordagem chain-of-thought generation do ESM3.

```python
from esm.sdk.api import GenerationConfig

# Multi-step refinement
protein = ESMProtein(sequence="MPRT" + "_" * 100 + "KEND")

# Step 1: Generate initial structure
config = GenerationConfig(track="structure", num_steps=50)
protein = model.generate(protein, config)

# Step 2: Refine sequence based on structure
config = GenerationConfig(track="sequence", num_steps=50, temperature=0.5)
protein = model.generate(protein, config)

# Step 3: Predict function
config = GenerationConfig(track="function", num_steps=20)
protein = model.generate(protein, config)
```

### 6. Processamento em Lote com Forge API

Processe múltiplas proteínas eficientemente usando o async executor do Forge.

```python
from esm.sdk.forge import ESM3ForgeInferenceClient
import asyncio

client = ESM3ForgeInferenceClient(model="esm3-medium-2024-08", token="<token>")

# Async batch processing
async def batch_generate(proteins_list):
    tasks = [
        client.async_generate(protein, GenerationConfig(track="sequence"))
        for protein in proteins_list
    ]
    return await asyncio.gather(*tasks)

# Execute
proteins = [ESMProtein(sequence=f"MPRT{'_' * 50}KEND") for _ in range(10)]
results = asyncio.run(batch_generate(proteins))
```

Veja `references/forge-api.md` para documentação detalhada da Forge API, autenticação, limites de taxa e padrões de processamento em lote.

## Guia de Seleção de Modelos

**Modelos ESM3 (Generativos):**
- `esm3-sm-open-v1` (1.4B) - Pesos abertos, uso local, bom para experimentação
- `esm3-medium-2024-08` (7B) - Melhor balanço entre qualidade e velocidade (apenas Forge)
- `esm3-large-2024-03` (98B) - Maior qualidade, mais lento (apenas Forge)

**Modelos ESM C (Embeddings):**
- `esmc-300m` (30 camadas) - Leve, inferência rápida
- `esmc-600m` (36 camadas) - Desempenho equilibrado
- `esmc-6b` (80 camadas) - Qualidade máxima de representação

**Critérios de seleção:**
- **Desenvolvimento local/testes:** Use `esm3-sm-open-v1` ou `esmc-300m`
- **Qualidade em produção:** Use `esm3-medium-2024-08` via Forge
- **Máxima precisão:** Use `esm3-large-2024-03` ou `esmc-6b`
- **Alta vazão:** Use Forge API com batch executor
- **Otimização de custo:** Use modelos menores, implemente estratégias de cache

## Instalação

**Instalação básica:**

```bash
uv pip install esm
```

**Com Flash Attention (recomendado para inferência mais rápida):**

```bash
uv pip install esm
uv pip install flash-attn --no-build-isolation
```

**Para acesso à Forge API:**

```bash
uv pip install esm  # SDK inclui cliente Forge
```

Sem dependências adicionais necessárias. Obtenha token da Forge API em https://forge.evolutionaryscale.ai

## Fluxos de Trabalho Comuns

Para exemplos detalhados e fluxos de trabalho completos, veja `references/workflows.md` que inclui:
- Design inovador de GFP com chain-of-thought
- Geração e screening de variantes de proteína
- Otimização de sequência baseada em estrutura
- Pipelines de predição de função
- Clustering e análise baseada em embeddings

## Referências

Essa skill inclui documentação de referência abrangente:

- `references/esm3-api.md` - Arquitetura do modelo ESM3, referência de API, parâmetros de geração e prompting multimodal
- `references/esm-c-api.md` - Detalhes do modelo ESM C, estratégias de embedding e otimização de desempenho
- `references/forge-api.md` - Documentação da plataforma Forge, autenticação, processamento em lote e deploy
- `references/workflows.md` - Exemplos completos e padrões comuns de fluxo de trabalho

Essas referências contêm especificações detalhadas de API, descrições de parâmetros e padrões de uso avançado. Carregue conforme necessário para tarefas específicas.

## Melhores Práticas

**Para tarefas de geração:**
- Comece com modelos menores para prototipagem (`esm3-sm-open-v1`)
- Use parâmetro de temperatura para controlar diversidade (0.0 = determinístico, 1.0 = diverso)
- Implemente refinamento iterativo com chain-of-thought para designs complexos
- Valide sequências geradas com predição de estrutura ou experimentos em laboratório

**Para tarefas de embedding:**
- Processe sequências em lote quando possível para eficiência
- Cache embeddings para análises repetidas
- Normalize embeddings ao calcular similaridades
- Use tamanho de modelo apropriado baseado em requisitos da tarefa downstream

**Para deploy em produção:**
- Use Forge API para escalabilidade e modelos mais recentes
- Implemente tratamento de erros e lógica de retry para chamadas de API
- Monitore uso de tokens e implemente rate limiting
- Considere deploy em AWS SageMaker para infraestrutura dedicada

## Recursos e Documentação

- **Repositório GitHub:** https://github.com/evolutionaryscale/esm
- **Plataforma Forge:** https://forge.evolutionaryscale.ai
- **Artigo Científico:** Hayes et al., Science (2025) - https://www.science.org/doi/10.1126/science.ads0018
- **Blog Posts:**
  - Lançamento ESM3: https://www.evolutionaryscale.ai/blog/esm3-release
  - Lançamento ESM C: https://www.evolutionaryscale.ai/blog/esm-cambrian
- **Comunidade:** Comunidade Slack em https://bit.ly/3FKwcWd
- **Model Weights:** Organização EvolutionaryScale no HuggingFace

## Uso Responsável

O ESM foi projetado para aplicações benéficas em engenharia de proteínas, descoberta de fármacos e pesquisa científica. Siga o Responsible Biodesign Framework (https://responsiblebiodesign.ai/) ao designing de proteínas inovadoras. Considere implicações de biossegurança e éticas dos designs de proteína antes da validação experimental.