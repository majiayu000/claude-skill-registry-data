---
name: crewai
description: "Especialista em CrewAI - o principal framework multi-agente baseado em papéis utilizado por 60% das empresas da Fortune 500. Abrange design de agentes com papéis e objetivos, definição de tarefas, orquestração de crew, tipos de processo (sequencial, hierárquico, paralelo), sistemas de memória e flows para workflows complexos. Essencial para construir equipes colaborativas de agentes IA. Use quando: crewai, equipe multi-agente, papéis de agentes, crew de agentes, agentes baseados em papéis."
source: vibeship-spawner-skills (Apache 2.0)
---

# CrewAI

**Papel**: Arquiteto Multi-Agente CrewAI

Você é um especialista em projetar equipes colaborativas de agentes IA com CrewAI. Você pensa em termos de papéis, responsabilidades e delegação. Você cria personas de agentes claros com expertise específica, define tarefas bem estruturadas com outputs esperados e orquestra crews para colaboração otimizada. Você sabe quando usar processos sequenciais vs hierárquicos.

## Capacidades

- Definições de agentes (papel, objetivo, backstory)
- Design de tarefas e dependências
- Orquestração de crew
- Tipos de processo (sequencial, hierárquico)
- Configuração de memória
- Integração de tools
- Flows para workflows complexos

## Requisitos

- Python 3.10+
- Package crewai
- Acesso a API LLM

## Padrões

### Crew Básico com Configuração YAML

Define agentes e tarefas em YAML (recomendado)

**Quando usar**: Qualquer projeto CrewAI

```python
# config/agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Find comprehensive, accurate information on {topic}"
  backstory: |
    You are an expert researcher with years of experience
    in gathering and analyzing information. You're known
    for your thorough and accurate research.
  tools:
    - SerperDevTool
    - WebsiteSearchTool
  verbose: true

writer:
  role: "Content Writer"
  goal: "Create engaging, well-structured content"
  backstory: |
    You are a skilled writer who transforms research
    into compelling narratives. You focus on clarity
    and engagement.
  verbose: true

# config/tasks.yaml
research_task:
  description: |
    Research the topic: {topic}

    Focus on:
    1. Key facts and statistics
    2. Recent developments
    3. Expert opinions
    4. Contrarian viewpoints

    Be thorough and cite sources.
  agent: researcher
  expected_output: |
    A comprehensive research report with:
    - Executive summary
    - Key findings (bulleted)
    - Sources cited

writing_task:
  description: |
    Using the research provided, write an article about {topic}.

    Requirements:
    - 800-1000 words
    - Engaging introduction
    - Clear structure with headers
    - Actionable conclusion
  agent: writer
  expected_output: "A polished article ready for publication"
  context:
    - research_task  # Uses output from research

# crew.py
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class ContentCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'])

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config['writer'])

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self) -> Task:
        return Task(config
```

### Processo Hierárquico

Agente gerenciador delega para trabalhadores

**Quando usar**: Tarefas complexas que precisam de coordenação

```python
from crewai import Crew, Process

# Define agentes especializados
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate information",
    backstory="Expert researcher..."
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and interpret data",
    backstory="Expert analyst..."
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging content",
    backstory="Expert writer..."
)

# Crew hierárquico - gerenciador coordena
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o"),  # Manager model
    verbose=True
)

# Gerenciador decide:
# - Qual agente trata de qual tarefa
# - Quando delegar
# - Como combinar resultados

result = crew.kickoff()
```

### Recurso de Planejamento

Gera plano de execução antes de executar

**Quando usar**: Workflows complexos que precisam de estrutura

```python
from crewai import Crew, Process

# Habilita planejamento
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research, write, review],
    process=Process.sequential,
    planning=True,  # Enable planning
    planning_llm=ChatOpenAI(model="gpt-4o")  # Planner model
)

# Com planejamento habilitado:
# 1. CrewAI gera plano passo a passo
# 2. Plano é injetado em cada tarefa
# 3. Agentes veem a estrutura geral
# 4. Resultados mais consistentes

result = crew.kickoff()

# Acessa o plano
print(crew.plan)
```

## Anti-Padrões

### ❌ Papéis de Agente Vagos

**Por que ruim**: Agente não conhece sua especialidade.
Responsabilidades sobrepostas.
Delegação de tarefas deficiente.

**Em vez disso**: Seja específico:
- "Senior React Developer" em vez de "Developer"
- "Financial Analyst specializing in crypto" em vez de "Analyst"
Inclua skills específicas no backstory.

### ❌ Expected Outputs Ausentes

**Por que ruim**: Agente não sabe os critérios de conclusão.
Outputs inconsistentes.
Difícil encadear tarefas.

**Em vez disso**: Sempre especifique expected_output:
expected_output: |
  A JSON object with:
  - summary: string (100 words max)
  - key_points: list of strings
  - confidence: float 0-1

### ❌ Muitos Agentes

**Por que ruim**: Overhead de coordenação.
Comunicação inconsistente.
Execução mais lenta.

**Em vez disso**: 3-5 agentes com papéis claros.
Um agente pode lidar com múltiplas tarefas relacionadas.
Use tools em vez de agentes para ações simples.

## Limitações

- Apenas Python
- Melhor para workflows estruturados
- Pode ser verboso para casos simples
- Flows é recurso mais recente

## Skills Relacionadas

Funciona bem com: `langgraph`, `autonomous-agents`, `langfuse`, `structured-output`