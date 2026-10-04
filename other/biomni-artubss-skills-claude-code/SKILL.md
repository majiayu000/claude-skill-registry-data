---
name: biomni
description: Framework autônomo de agente de IA biomédica para executar tarefas de pesquisa complexas em genômica, descoberta de fármacos, biologia molecular e análise clínica. Use esta skill ao conduzir pesquisa biomédica em múltiplas etapas, incluindo design de triagem CRISPR, análise de RNA-seq de células únicas, previsão ADMET, interpretação GWAS, diagnóstico de doenças raras ou otimização de protocolos de laboratório. Aproveita o raciocínio de LLM com execução de código e bancos de dados biomédicos integrados.
---

# Biomni

## Visão Geral

Biomni é um framework de agente de IA biomédica de código aberto do SNAP lab da Stanford que executa autonomamente tarefas de pesquisa complexas em vários domínios biomédicos. Use esta skill ao trabalhar com tarefas de raciocínio biológico em múltiplas etapas, analisar dados biomédicos ou conduzir pesquisas abrangendo genômica, descoberta de fármacos, biologia molecular e análise clínica.

## Capacidades Principais

Biomni se destaca em:

1. **Raciocínio biológico em múltiplas etapas** - Decomposição autônoma de tarefas e planejamento para consultas biomédicas complexas
2. **Geração e execução de código** - Criação dinâmica de pipelines de análise para processamento de dados
3. **Recuperação de conhecimento** - Acesso a ~11GB de bancos de dados biomédicos integrados e literatura
4. **Resolução de problemas entre domínios** - Interface unificada para genômica, proteômica, descoberta de fármacos e tarefas clínicas

## Quando Usar Esta Skill

Use biomni para:
- **Triagem CRISPR** - Design de triagens, priorização de genes, análise de efeitos de knockout
- **RNA-seq de células únicas** - Anotação de tipos celulares, expressão diferencial, análise de trajetória
- **Descoberta de fármacos** - Previsão ADMET, identificação de alvo, otimização de compostos
- **Análise GWAS** - Interpretação de variantes, identificação de gene causal, enriquecimento de vias
- **Genômica clínica** - Diagnóstico de doenças raras, patogenicidade de variantes, mapeamento fenótipo-genótipo
- **Protocolos de laboratório** - Otimização de protocolo, síntese de literatura, design experimental

## Início Rápido

### Instalação e Configuração

Instale Biomni e configure chaves de API para provedores de LLM:

```bash
uv pip install biomni --upgrade
```

Configure chaves de API (armazene em arquivo `.env` ou variáveis de ambiente):
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Opcional: chaves do OpenAI, Azure, Google, Groq, AWS Bedrock
```

Use `scripts/setup_environment.py` para assistência interativa de configuração.

### Padrão de Uso Básico

```python
from biomni.agent import A1

# Inicialize agente com caminho de dados e escolha de LLM
agent = A1(path='./data', llm='claude-sonnet-4-20250514')

# Execute tarefa biomédica autonomamente
agent.go("Sua pergunta ou tarefa de pesquisa biomédica")

# Salve histórico de conversas e resultados
agent.save_conversation_history("report.pdf")
```

## Trabalhando com Biomni

### 1. Inicialização do Agente

A classe A1 é a interface principal para biomni:

```python
from biomni.agent import A1
from biomni.config import default_config

# Inicialização básica
agent = A1(
    path='./data',  # Caminho para lago de dados (~11GB baixado no primeiro uso)
    llm='claude-sonnet-4-20250514'  # Seleção de modelo de LLM
)

# Configuração avançada
default_config.llm = "gpt-4"
default_config.timeout_seconds = 1200
default_config.max_iterations = 50
```

**Provedores de LLM Suportados:**
- Anthropic Claude (recomendado): `claude-sonnet-4-20250514`, `claude-opus-4-20250514`
- OpenAI: `gpt-4`, `gpt-4-turbo`
- Azure OpenAI: via configuração do Azure
- Google Gemini: `gemini-2.0-flash-exp`
- Groq: `llama-3.3-70b-versatile`
- AWS Bedrock: Vários modelos via API Bedrock

Consulte `references/llm_providers.md` para instruções detalhadas de configuração de LLM.

### 2. Fluxo de Trabalho de Execução de Tarefas

Biomni segue um fluxo de trabalho autônomo de agente:

```python
# Etapa 1: Inicializar agente
agent = A1(path='./data', llm='claude-sonnet-4-20250514')

# Etapa 2: Executar tarefa com consulta em linguagem natural
result = agent.go("""
Design uma triagem CRISPR para identificar genes que regulam autofagia em
células HEK293. Priorize genes com base em essencialidade e relevância
de via.
""")

# Etapa 3: Revise código gerado e análise
# O agente autonomamente:
# - Decompõe tarefa em sub-etapas
# - Recupera conhecimento biológico relevante
# - Gera e executa código de análise
# - Interpreta resultados e fornece insights

# Etapa 4: Salve resultados
agent.save_conversation_history("autophagy_screen_report.pdf")
```

### 3. Padrões de Tarefas Comuns

#### Design de Triagem CRISPR
```python
agent.go("""
Design uma triagem de knockout CRISPR em todo o genoma para identificar genes
que afetam [fenótipo] em [tipo de célula]. Inclua:
1. Design de biblioteca sgRNA
2. Critérios de priorização de genes
3. Genes de hit esperados com base em análise de via
""")
```

#### Análise de RNA-seq de Células Únicas
```python
agent.go("""
Analise este conjunto de dados de RNA-seq de células únicas:
- Realize controle de qualidade e filtragem
- Identifique populações celulares via clustering
- Anote tipos de célula usando genes marcadores
- Conduza expressão diferencial entre condições
Caminho do arquivo: [caminho/para/dados.h5ad]
""")
```

#### Previsão ADMET de Fármacos
```python
agent.go("""
Preveja propriedades ADMET para estes candidatos a fármaco:
[Strings SMILES ou IDs de compostos]
Foco em:
- Absorção (permeabilidade Caco-2, HIA)
- Distribuição (ligação a proteína plasmática, penetração BBB)
- Metabolismo (interação CYP450)
- Excreção (clearance)
- Toxicidade (responsabilidade hERG, hepatotoxicidade)
""")
```

#### Interpretação de Variantes GWAS
```python
agent.go("""
Interprete resultados GWAS para [traço/doença]:
- Identifique variantes significativas em todo o genoma
- Mapeie variantes para genes causais
- Realize análise de enriquecimento de vias
- Preveja consequências funcionais
Arquivo de estatísticas resumidas: [caminho/para/gwas_summary.txt]
""")
```

Consulte `references/use_cases.md` para exemplos abrangentes de tarefas em todos os domínios biomédicos.

### 4. Integração de Dados

Biomni integra ~11GB de fontes de conhecimento biomédico:
- **Bancos de dados de genes** - Ensembl, NCBI Gene, UniProt
- **Estruturas de proteínas** - PDB, AlphaFold
- **Conjuntos de dados clínicos** - ClinVar, OMIM, HPO
- **Índices de literatura** - Resumos PubMed, ontologias biomédicas
- **Bancos de dados de vias** - KEGG, Reactome, GO

Os dados são baixados automaticamente para o caminho especificado no primeiro uso.

### 5. Integração do Servidor MCP

Estenda biomni com ferramentas externas via Model Context Protocol:

```python
# Servidores MCP podem fornecer:
# - Bancos de dados de fármacos da FDA
# - Busca na web por literatura
# - APIs biomédicas personalizadas
# - Interfaces de equipamentos de laboratório

# Configure servidores MCP em .biomni/mcp_config.json
```

### 6. Framework de Avaliação

Compare o desempenho do agente em tarefas biomédicas:

```python
from biomni.eval import BiomniEval1

evaluator = BiomniEval1()

# Avalie tipos de tarefas específicas
score = evaluator.evaluate(
    task_type='crispr_design',
    instance_id='test_001',
    answer=agent_output
)

# Acesse conjunto de dados de avaliação
dataset = evaluator.load_dataset()
```

## Melhores Práticas

### Formulação de Tarefas
- **Seja específico** - Inclua contexto biológico, organismo, tipo de célula, condições
- **Especifique outputs** - Indique claramente os outputs desejados de análise e formatos
- **Forneça caminhos de dados** - Inclua caminhos de arquivo para conjuntos de dados a analisar
- **Defina restrições** - Mencione limites de tempo/computacionais se relevantes

### Considerações de Segurança
⚠️ **Importante**: Biomni executa código gerado por LLM com privilégios completos do sistema. Para uso em produção:
- Execute em ambientes isolados (Docker, VMs)
- Evite expor credenciais sensíveis
- Revise código gerado antes da execução em contextos sensíveis
- Use ambientes de execução em sandbox quando possível

### Otimização de Desempenho
- **Escolha LLMs apropriados** - Claude Sonnet 4 recomendado para equilíbrio de velocidade/qualidade
- **Defina timeouts razoáveis** - Ajuste `default_config.timeout_seconds` para tarefas complexas
- **Monitore iterações** - Rastreie `max_iterations` para prevenir loops descontrolados
- **Armazene dados em cache** - Reutilize lago de dados baixado entre sessões

### Documentação de Resultados
```python
# Sempre salve histórico de conversas para reprodutibilidade
agent.save_conversation_history("results/project_name_YYYYMMDD.pdf")

# Inclua em relatórios:
# - Descrição original da tarefa
# - Código de análise gerado
# - Resultados e interpretações
# - Fontes de dados usadas
```

## Recursos

### Referências
Documentação detalhada disponível no diretório `references/`:

- **`api_reference.md`** - Documentação completa da API para classe A1, configuração e avaliação
- **`llm_providers.md`** - Configuração de provedor de LLM (Anthropic, OpenAI, Azure, Google, Groq, AWS)
- **`use_cases.md`** - Exemplos abrangentes de tarefas para todos os domínios biomédicos

### Scripts
Scripts auxiliares no diretório `scripts/`:

- **`setup_environment.py`** - Configuração interativa de ambiente e chaves de API
- **`generate_report.py`** - Geração aprimorada de relatório PDF com formatação personalizada

### Recursos Externos
- **GitHub**: https://github.com/snap-stanford/biomni
- **Plataforma Web**: https://biomni.stanford.edu
- **Artigo**: https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1
- **Modelo**: https://huggingface.co/biomni/Biomni-R0-32B-Preview
- **Conjunto de Dados de Avaliação**: https://huggingface.co/datasets/biomni/Eval1

## Solução de Problemas

### Problemas Comuns

**Download de dados falha**
```python
# Ative manualmente download do lago de dados
agent = A1(path='./data', llm='seu-llm')
# Primeira chamada .go() baixará dados
```

**Erros de chave de API**
```bash
# Verifique variáveis de ambiente
echo $ANTHROPIC_API_KEY
# Ou verifique arquivo .env no diretório de trabalho
```

**Timeout em tarefas complexas**
```python
from biomni.config import default_config
default_config.timeout_seconds = 3600  # 1 hora
```

**Problemas de memória com conjuntos de dados grandes**
- Use streaming para arquivos grandes
- Processe dados em chunks
- Aumente alocação de memória do sistema

### Obtendo Ajuda

Para problemas ou dúvidas:
- GitHub Issues: https://github.com/snap-stanford/biomni/issues
- Documentação: Verifique arquivos em `references/` para orientação detalhada
- Comunidade: SNAP lab de Stanford e contribuidores de biomni