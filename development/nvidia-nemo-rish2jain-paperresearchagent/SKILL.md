---
name: nvidia-nemo
description: NVIDIA NeMo framework for building and training conversational AI models. Use for NeMo Retriever models, RAG (Retrieval-Augmented Generation), embedding models, enterprise search, and multilingual retrieval systems.
---

# NVIDIA NeMo Skill

Comprehensive assistance with NVIDIA NeMo development, the enterprise AI platform for building, customizing, and deploying generative AI agents at scale.

## When to Use This Skill

This skill should be triggered when:

**Core NeMo Components:**
- Working with **NeMo Retriever** for RAG pipelines and document extraction
- Using **NeMo Customizer** for fine-tuning LLMs (LoRA, SFT, DPO, GRPO)
- Implementing **NeMo Guardrails** for content safety and jailbreak prevention
- Building with **NeMo Curator** for data processing and synthetic data generation
- Using **NeMo Evaluator** for benchmarking LLMs, RAG, and agents
- Working with **NeMo Agent Toolkit** for multi-agent orchestration

**NVIDIA Nemotron Models:**
- Deploying Nemotron Nano, Super, or Ultra models for agentic AI
- Using Nemotron RAG models for embedding/reranking
- Implementing Nemotron Safety Guard for content moderation

**Use Cases:**
- Building RAG pipelines with enterprise document retrieval
- Fine-tuning models for domain-specific tasks
- Creating AI agents with tool calling and function execution
- Processing and curating training data at scale
- Implementing multi-modal AI (text, vision, audio, video)
- Deploying guardrails for safe, compliant AI applications

## Quick Reference

### RAG with NeMo Retriever

**Basic Embedding Generation**
```python
import requests

# NeMo Retriever Embedding NIM
url = "https://integrate.api.nvidia.com/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "input": ["What is retrieval-augmented generation?"],
    "model": "nvidia/nv-embedqa-e5-v5",
    "input_type": "query"
}

response = requests.post(url, json=payload, headers=headers)
embeddings = response.json()["data"][0]["embedding"]
```

**Reranking Results**
```python
# NeMo Retriever Reranking NIM
url = "https://integrate.api.nvidia.com/v1/ranking"

payload = {
    "model": "nvidia/nv-rerankqa-mistral-4b-v3",
    "query": {"text": "What is machine learning?"},
    "passages": [
        {"text": "Machine learning is a subset of AI..."},
        {"text": "Python is a programming language..."},
        {"text": "ML models learn patterns from data..."}
    ]
}

response = requests.post(url, json=payload, headers=headers)
ranked_results = response.json()["rankings"]
```

### Model Customization with NeMo Customizer

**Submit Fine-Tuning Job**
```python
# Fine-tune with LoRA
payload = {
    "name": "custom-model-lora",
    "model": "meta/llama-3.1-8b-instruct",
    "method": "lora",
    "dataset": "s3://my-bucket/training-data.jsonl",
    "hyperparameters": {
        "learning_rate": 1e-4,
        "batch_size": 8,
        "epochs": 3,
        "lora_rank": 8
    }
}

response = requests.post(
    "http://nemo-customizer:8000/v1/customization/jobs",
    json=payload
)
job_id = response.json()["id"]
```

**Check Job Status**
```python
# Monitor customization progress
status_response = requests.get(
    f"http://nemo-customizer:8000/v1/customization/jobs/{job_id}"
)

print(f"Status: {status_response.json()['status']}")
print(f"Progress: {status_response.json()['progress']}%")
```

### Guardrails with NeMo Guardrails

**Initialize Guardrails**
```python
from nemoguardrails import RailsConfig, LLMRails

# Load configuration
config = RailsConfig.from_path("./config")
rails = LLMRails(config)

# Apply guardrails
response = rails.generate(
    messages=[{"role": "user", "content": "Tell me about..."}]
)
```

**YAML Configuration for Topic Control**
```yaml
# config.yml
models:
  - type: main
    engine: nvidia_ai_endpoints
    model: meta/llama-3.1-70b-instruct

rails:
  input:
    flows:
      - check jailbreak
      - check topic relevance
  output:
    flows:
      - check hallucination
      - check safety
```

**Custom Rail Definition**
```colang
# Custom topic control
define user ask about competitors
  "Tell me about competing products"
  "What do you think of [competitor]"

define bot refuse competitors
  "I can only discuss our own products and services."

define flow
  user ask about competitors
  bot refuse competitors
  stop
```

### Data Curation with NeMo Curator

**Text Processing Pipeline**
```python
from nemo_curator import ScoreFilter, DedupFilter
from nemo_curator.datasets import DocumentDataset

# Load dataset
dataset = DocumentDataset.read_json("data.jsonl")

# Quality filtering
quality_filter = ScoreFilter(
    score_field="quality_score",
    score_threshold=0.7
)
dataset = quality_filter(dataset)

# Deduplication
dedup_filter = DedupFilter()
dataset = dedup_filter(dataset)

# Save processed data
dataset.to_json("processed_data.jsonl")
```

**Synthetic Data Generation**
```python
from nemo_curator.synthetic import PromptTemplate, generate_data

# Define prompt template
template = PromptTemplate(
    system="You are a helpful assistant.",
    user_template="Generate a question about {topic}"
)

# Generate synthetic data
synthetic_data = generate_data(
    template=template,
    topics=["machine learning", "data science"],
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    num_samples=100
)
```

### Evaluation with NeMo Evaluator

**Academic Benchmark Evaluation**
```python
from nemo_evaluator import Evaluator

evaluator = Evaluator()

# Run MMLU benchmark
results = evaluator.evaluate(
    model="meta/llama-3.1-8b-instruct",
    tasks=["mmlu"],
    batch_size=8
)

print(f"MMLU Score: {results['mmlu']['acc']}")
```

**RAG Pipeline Evaluation**
```python
# Evaluate RAG with custom metrics
rag_results = evaluator.evaluate_rag(
    model="custom-rag-pipeline",
    metrics=["faithfulness", "answer_relevance", "context_precision"],
    dataset="custom_qa_dataset.jsonl"
)
```

### Agent Development with NeMo Agent Toolkit

**Define Agent with Tools**
```yaml
# agent_config.yaml
agents:
  - name: customer_support_agent
    model: nvidia/llama-3.1-nemotron-70b-instruct
    tools:
      - web_search
      - knowledge_base_query
      - ticket_creation
    max_iterations: 5
```

**Tool Registration**
```python
from nemo_agent_toolkit import Agent, Tool

# Define custom tool
@Tool(
    name="database_query",
    description="Query customer database for information"
)
def query_database(customer_id: str) -> dict:
    # Tool implementation
    return {"name": "John Doe", "status": "Premium"}

# Create agent
agent = Agent.from_config("agent_config.yaml")
agent.register_tool(query_database)

# Run agent
response = agent.run("What is the status of customer ID 12345?")
```

### Deployment with NeMo NIMs

**Deploy Custom Model as NIM**
```bash
# Pull NIM container
docker pull nvcr.io/nim/meta/llama-3.1-8b-instruct:latest

# Run NIM with custom LoRA
docker run -d \
  --gpus all \
  -p 8000:8000 \
  -e NGC_API_KEY=$NGC_API_KEY \
  -e PEFT_MODEL_PATH=/models/custom-lora \
  -v ./models:/models \
  nvcr.io/nim/meta/llama-3.1-8b-instruct:latest
```

**Query NIM Endpoint**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-used"
)

response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    temperature=0.7,
    max_tokens=500
)
```

## Key Concepts

### NeMo Ecosystem Architecture

**NeMo Suite Components:**
- **NeMo Retriever**: RAG components (embedding, reranking, extraction)
- **NeMo Customizer**: Model fine-tuning and alignment (LoRA, SFT, DPO, GRPO)
- **NeMo Guardrails**: Safety orchestration and content moderation
- **NeMo Curator**: Data processing and synthetic data generation
- **NeMo Evaluator**: Benchmarking and evaluation pipelines
- **NeMo Agent Toolkit**: Multi-agent orchestration and optimization

**NVIDIA Nemotron Models:**
- **Nano (8B)**: Edge deployment, fast inference, cost-efficient
- **Super (70B)**: Single GPU, balanced accuracy/compute
- **Ultra (405B)**: Data center scale, highest accuracy
- **Nano VL**: Vision-language for document intelligence
- **RAG Models**: Embedding and reranking for retrieval

### RAG Pipeline Components

**1. Document Extraction (NeMo Retriever)**
- Multi-modal extraction: text, charts, tables, graphs
- 15x faster PDF processing than traditional methods
- Maintains document structure and relationships

**2. Embedding (Nemotron Embedding Models)**
- State-of-the-art accuracy on ViDoRe, MTEB benchmarks
- Multi-lingual support
- Optimized for enterprise documents

**3. Vector Storage (cuVS)**
- GPU-accelerated indexing and search
- 35x better storage efficiency
- Scalable to billions of embeddings

**4. Reranking (Nemotron Reranking Models)**
- Final relevance scoring
- 50% better accuracy over baseline
- Context-aware ranking

### Customization Methods

**LoRA (Low-Rank Adaptation)**
- Parameter-efficient fine-tuning
- Fast training, low memory
- Ideal for multiple task adaptations

**SFT (Supervised Fine-Tuning)**
- Full model fine-tuning
- Task-specific optimization
- Higher resource requirements

**DPO (Direct Preference Optimization)**
- Alignment without reward model
- Human feedback integration
- Simpler than RLHF

**GRPO (Group Relative Policy Optimization)**
- Advanced RL alignment
- Multi-objective optimization
- Enterprise-grade policy learning

### Guardrails Architecture

**Rail Types:**
- **Input Rails**: Pre-LLM validation (jailbreak, topic control)
- **Output Rails**: Post-LLM checks (safety, hallucination)
- **Dialog Rails**: Conversation flow management
- **Retrieval Rails**: RAG grounding verification

**Orchestration:**
- Parallel rail execution for low latency
- GPU acceleration for speed
- Enterprise-grade scaling

## Reference Files

### api.md
**NeMo Customizer API Documentation**
- REST API endpoints for model customization
- Job submission and monitoring
- LoRA, SFT, DPO, GRPO configuration
- Hyperparameter tuning guides
- Integration with NIM deployment

### retriever.md
**NeMo Retriever Models & Pipeline**
- Embedding model APIs (NV-Embed-v2)
- Reranking model usage (NV-RerankQA)
- Document extraction workflows
- Vector database integration (cuVS)
- RAG pipeline architecture
- Performance benchmarks (ViDoRe, MTEB)

### rag.md
**RAG Implementation & Best Practices**
- End-to-end RAG pipeline examples
- NeMo Evaluator for RAG metrics
- Knowledge base integration
- Multi-modal retrieval strategies
- AI-Q Blueprint for enterprise RAG

### other.md
**Comprehensive NeMo Ecosystem**
- **NeMo Curator**: Data processing, synthetic generation
- **NeMo Guardrails**: Safety orchestration
- **NeMo Agent Toolkit**: Multi-agent systems
- **Nemotron Models**: Model family overview
- **NeMo Evaluator**: Benchmarking workflows
- Integration patterns across components

## Working with This Skill

### For Beginners

**Start Here:**
1. Review the **Key Concepts** section to understand the NeMo ecosystem
2. Explore **Quick Reference** for hands-on examples
3. Read `retriever.md` for RAG fundamentals
4. Try the basic embedding and reranking examples

**First Project Ideas:**
- Build a simple RAG chatbot with NeMo Retriever
- Fine-tune a small model with NeMo Customizer
- Add basic guardrails to an existing LLM app

### For Intermediate Users

**Focus Areas:**
1. **RAG Optimization**: Study `rag.md` for advanced retrieval patterns
2. **Model Customization**: Use `api.md` to fine-tune with LoRA/SFT
3. **Multi-Agent Systems**: Explore NeMo Agent Toolkit in `other.md`
4. **Evaluation**: Implement benchmarking with NeMo Evaluator

**Common Workflows:**
- Build production RAG with reranking
- Create domain-specific models via fine-tuning
- Implement comprehensive guardrails
- Orchestrate multi-agent workflows

### For Advanced Users

**Enterprise Patterns:**
1. **Data Flywheels**: Curator → Customizer → Evaluator → Production
2. **Multi-Modal RAG**: Vision + text retrieval with Nemotron Nano VL
3. **RL Alignment**: Advanced GRPO/DPO for policy optimization
4. **Agent Orchestration**: Complex multi-agent systems with MCP

**Performance Optimization:**
- GPU acceleration with cuVS for vector search
- Parallel rail execution in Guardrails
- Batch processing in Curator
- Distributed evaluation in NeMo Evaluator

**Scaling Strategies:**
- Kubernetes deployment of NIM microservices
- Multi-GPU customization jobs
- Enterprise data processing pipelines
- Production monitoring and observability

### Navigation Tips

**Quick Lookups:**
- API endpoints → `api.md`
- RAG metrics → `rag.md`
- Model specs → `other.md` (Nemotron section)
- Safety rails → `other.md` (Guardrails section)

**Deep Dives:**
- Complete RAG pipeline → `retriever.md` + `rag.md`
- Fine-tuning workflow → `api.md` + `other.md` (Customizer)
- Agent development → `other.md` (Agent Toolkit)
- Data processing → `other.md` (Curator)

## Integration Patterns

### NeMo + NIM Deployment
```
Data Curation (Curator)
  → Model Training/Fine-tuning (Customizer)
  → Evaluation (Evaluator)
  → Deployment (NIM)
  → Monitoring (Agent Toolkit)
  → Safety (Guardrails)
```

### Enterprise RAG Stack
```
Documents
  → Extraction (NeMo Retriever)
  → Vector DB (cuVS)
  → Embedding (Nemotron RAG)
  → Reranking (Nemotron RAG)
  → LLM (Nemotron + NIM)
  → Guardrails (NeMo Guardrails)
  → Response
```

### Data Flywheel
```
User Interactions
  → Data Collection
  → Curation (Curator)
  → Fine-tuning (Customizer)
  → Evaluation (Evaluator)
  → Deployment (NIM)
  → Loop Back
```

## Model Selection Guide

| Use Case | Recommended Model | Deployment |
|----------|------------------|------------|
| Edge AI, IoT | Nemotron Nano 8B | Single device |
| Chatbots, agents | Nemotron Super 70B | Single GPU |
| Enterprise RAG | Nemotron Ultra 405B | Data center |
| Document intelligence | Nemotron Nano VL | GPU workstation |
| Embedding | NV-Embed-v2 | NIM microservice |
| Reranking | NV-RerankQA | NIM microservice |

## Performance Benchmarks

**NeMo Retriever:**
- #1 on ViDoRe V1, V2 leaderboards (visual document retrieval)
- #1 on MTEB VisualDocumentRetrieval
- 15x faster PDF extraction vs. traditional methods
- 35x better storage efficiency with cuVS

**Nemotron Models:**
- Up to 6x faster throughput vs. leading 8B models
- 60% lower token generation with thinking budget
- State-of-the-art accuracy on agentic benchmarks

## Resources

### Official Links
- [NeMo Developer Portal](https://developer.nvidia.com/nemo)
- [NeMo GitHub](https://github.com/NVIDIA/NeMo)
- [NGC Catalog](https://catalog.ngc.nvidia.com/)
- [API Documentation](https://docs.nvidia.com/nemo/)

### Learning Resources
- NeMo Tutorials and Webinars (see reference docs)
- AI-Q Blueprint for RAG patterns
- NVIDIA DLI Courses on Generative AI
- Technical blogs and case studies

### Community
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
- Discord channels for NeMo users
- GitHub issues for bug reports
- Feature voting for roadmap input

## Notes

- NeMo is the **enterprise AI platform** for the full agent lifecycle
- All components are **API-first** and **cloud-native**
- Models support **OpenAI-compatible APIs** for easy integration
- **Nemotron models** are open with training data and recipes
- **NIM microservices** enable deployment on any GPU-accelerated system
- Supports **MCP (Model Context Protocol)** for tool integration

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Check for new models, features, and API changes regularly
