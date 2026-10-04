---
name: denario
description: Sistema multiagente de IA para assistência em pesquisa científica que automatiza fluxos de trabalho de pesquisa desde análise de dados até publicação. Esta skill deve ser usada ao gerar ideias de pesquisa a partir de conjuntos de dados, desenvolver metodologias de pesquisa, executar experimentos computacionais, realizar buscas de literatura ou gerar papers prontos para publicação em formato LaTeX. Suporta pipelines de pesquisa end-to-end com orquestração de agentes personalizável.
---

# Denario

## Visão Geral

Denario é um sistema multiagente de IA projetado para automatizar fluxos de trabalho de pesquisa científica desde a análise inicial de dados até manuscritos prontos para publicação. Construído sobre os frameworks AG2 e LangGraph, ele orquestra múltiplos agentes especializados para lidar com geração de hipóteses, desenvolvimento de metodologia, análise computacional e redação de papers.

## Quando Usar Esta Skill

Use esta skill quando:
- Analisar conjuntos de dados para gerar novas hipóteses de pesquisa
- Desenvolver metodologias estruturadas de pesquisa
- Executar experimentos computacionais e gerar visualizações
- Conduzir buscas de literatura para contexto de pesquisa
- Escrever papers em formato LaTeX a partir de resultados de pesquisa
- Automatizar o pipeline completo de pesquisa desde dados até publicação

## Instalação

Instale denario usando uv (recomendado):

```bash
uv init
uv add "denario[app]"
```

Ou usando pip:

```bash
uv pip install "denario[app]"
```

Para implantação em Docker ou construção a partir do código-fonte, consulte `references/installation.md`.

## Configuração da API LLM

Denario requer chaves de API de provedores de LLM suportados. Os provedores suportados incluem:
- Google Vertex AI
- OpenAI
- Outros serviços LLM compatíveis com AG2/LangGraph

Armazene chaves de API com segurança usando variáveis de ambiente ou arquivos `.env`. Para instruções detalhadas de configuração, incluindo setup do Vertex AI, consulte `references/llm_configuration.md`.

## Fluxo de Trabalho de Pesquisa Essencial

Denario segue um pipeline de pesquisa estruturado em quatro etapas:

### 1. Descrição dos Dados

Defina o contexto da pesquisa especificando dados e ferramentas disponíveis:

```python
from denario import Denario

den = Denario(project_dir="./my_research")
den.set_data_description("""
Available datasets: time-series data on X and Y
Tools: pandas, sklearn, matplotlib
Research domain: [specify domain]
""")
```

### 2. Geração de Ideias

Gere hipóteses de pesquisa a partir da descrição de dados:

```python
den.get_idea()
```

Isso produz uma pergunta de pesquisa ou hipótese baseada nos dados descritos. Alternativamente, forneça uma ideia personalizada:

```python
den.set_idea("Custom research hypothesis")
```

### 3. Desenvolvimento de Metodologia

Desenvolva a metodologia de pesquisa:

```python
den.get_method()
```

Isso cria uma abordagem estruturada para investigar a hipótese. Também pode aceitar arquivos markdown com metodologias personalizadas:

```python
den.set_method("path/to/methodology.md")
```

### 4. Geração de Resultados

Execute experimentos computacionais e gere análise:

```python
den.get_results()
```

Isso executa a metodologia, realiza computações, cria visualizações e produz descobertas. Também pode fornecer resultados pré-calculados:

```python
den.set_results("path/to/results.md")
```

### 5. Geração de Paper

Crie um paper em LaTeX pronto para publicação:

```python
from denario import Journal

den.get_paper(journal=Journal.APS)
```

O paper gerado inclui formatação apropriada para o journal especificado, figuras integradas e código-fonte LaTeX completo.

## Jornals Disponíveis

Denario suporta múltiplos estilos de formatação de journal:
- `Journal.APS` - Formato da American Physical Society
- Jornals adicionais podem estar disponíveis; consulte `references/research_pipeline.md` para a lista completa

## Iniciando a GUI

Execute a interface gráfica do usuário:

```bash
denario run
```

Isso inicia uma interface web para gerenciamento interativo do fluxo de trabalho de pesquisa.

## Fluxos de Trabalho Comuns

### Pipeline de Pesquisa End-to-End

```python
from denario import Denario, Journal

# Initialize project
den = Denario(project_dir="./research_project")

# Define research context
den.set_data_description("""
Dataset: Time-series measurements of [phenomenon]
Available tools: pandas, sklearn, scipy
Research goal: Investigate [research question]
""")

# Generate research idea
den.get_idea()

# Develop methodology
den.get_method()

# Execute analysis
den.get_results()

# Create publication
den.get_paper(journal=Journal.APS)
```

### Fluxo de Trabalho Híbrido (Personalizado + Automatizado)

```python
# Provide custom research idea
den.set_idea("Investigate the correlation between X and Y using time-series analysis")

# Auto-generate methodology
den.get_method()

# Auto-generate results
den.get_results()

# Generate paper
den.get_paper(journal=Journal.APS)
```

### Integração de Busca de Literatura

Para funcionalidade de busca de literatura e exemplos adicionais de fluxo de trabalho, consulte `references/examples.md`.

## Recursos Avançados

- **Orquestração multiagente**: AG2 e LangGraph coordenam agentes especializados para diferentes tarefas de pesquisa
- **Pesquisa reproduzível**: Todas as etapas produzem saídas estruturadas que podem ser versionadas
- **Integração com journals**: Formatação automática para periódicos de publicação alvo
- **Entrada flexível**: Manual ou automatizada em cada etapa do pipeline
- **Implantação em Docker**: Ambiente containerizado com LaTeX e todas as dependências

## Referências Detalhadas

Para documentação abrangente:
- **Opções de instalação**: `references/installation.md`
- **Configuração de LLM**: `references/llm_configuration.md`
- **Referência completa de API**: `references/research_pipeline.md`
- **Fluxos de trabalho de exemplo**: `references/examples.md`

## Resolução de Problemas

Problemas comuns e soluções:
- **Erros de chave de API**: Certifique-se de que as variáveis de ambiente estão definidas corretamente (consulte `references/llm_configuration.md`)
- **Compilação LaTeX**: Instale distribuição TeX ou use imagem Docker com LaTeX pré-instalado
- **Conflitos de pacotes**: Use ambientes virtuais ou Docker para isolamento
- **Versão do Python**: Requer Python 3.12 ou superior