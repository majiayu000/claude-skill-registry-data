---
name: "tech-hiring-machine-learning-ai-engineering"
description: "ML/AI engineers build, train, evaluate, and deploy machine learning models and AI systems. The role spans research-adjacent (novel model development) to engineering-adjacent (putting models reliably into production). In 2025, GenAI/LLM comp"
---

# Machine Learning & AI Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Machine Learning & AI Engineering

### What This Role Does
ML/AI engineers build, train, evaluate, and deploy machine learning models and AI systems. The role spans research-adjacent (novel model development) to engineering-adjacent (putting models reliably into production). In 2025, GenAI/LLM competency is a strong differentiator. Distinguish clearly between ML Research Scientists (new algorithms) and ML Engineers (production systems).

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | ML Engineer, Junior AI Engineer, Applied ML Engineer |
| Mid | ML Engineer, AI Engineer, Applied Scientist |
| Senior | Senior ML Engineer, Senior AI Engineer, Research Engineer |
| Staff+ | Staff ML Engineer, Principal AI Engineer, ML Architect |
| Research track | Research Scientist, ML Research Engineer, AI Researcher |
| Specialist | LLM Engineer, MLOps Engineer, GenAI Engineer |

### Skill Tiers

**Tier 1 — Must-have:**
- Python (advanced): PyTorch or TensorFlow/JAX, NumPy, pandas
- ML fundamentals: supervised/unsupervised learning, loss functions, backpropagation, regularisation
- Model evaluation: precision/recall, AUC-ROC, confusion matrix, cross-validation
- SQl and data manipulation at scale
- Git and code review culture (ML engineers are engineers first)

**Tier 2 — Differentiator:**
- Transformers / attention mechanisms — practical, not just theoretical
- MLOps: MLflow, Weights & Biases, DVC, experiment tracking
- Model deployment: TorchServe, Triton Inference Server, FastAPI serving, ONNX
- Feature engineering, feature stores (Feast, Tecton)
- Distributed training (DDP, FSDP, DeepSpeed) for large models
- Vector databases: Pinecone, Weaviate, Qdrant, pgvector
- RAG architectures, LLM orchestration (LangChain, LlamaIndex)

**Tier 3 — Bonus:**
- CUDA / GPU programming
- Research publications, arXiv papers, NeurIPS/ICML/ICLR credits
- Reinforcement learning (especially RLHF for LLM fine-tuning)
- Custom model architecture development
- Multimodal systems (vision-language, audio)

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("ML engineer" OR "machine learning engineer" OR "AI engineer" OR "applied scientist") (PyTorch OR TensorFlow OR "deep learning" OR LLM OR "large language") -recruiter -talent

# Research-focused
site:linkedin.com/in/ ("research scientist" OR "research engineer") ("NeurIPS" OR "ICML" OR "ICLR" OR "machine learning" OR "deep learning") -recruiter

# GenAI/LLM specialist
site:linkedin.com/in/ ("LLM engineer" OR "GenAI" OR "generative AI") (RAG OR "fine-tuning" OR LangChain OR "vector database") -recruiter

# arXiv — find cutting-edge researchers
site:arxiv.org "reinforcement learning from human feedback" 2024 OR 2025
site:arxiv.org "large language models" "production" 2025

# GitHub
language:python topic:machine-learning followers:>30 pushed:>2025-01-01
site:github.com "joined on" (PyTorch OR "LLM" OR "fine-tuning" OR "RAG") "machine learning"
```

### Seniority Signals

- **Junior → Mid:** Can take a defined problem, select appropriate methods, train and evaluate a model independently
- **Mid → Senior:** Identifies when ML is (and isn't) the right tool; drives the full ML system from data quality to production monitoring
- **Senior → Staff:** Sets ML strategy across teams; creates internal tools that accelerate others; strong opinions on model governance and evaluation
- **Research vs. Engineering:** Ask "how long does it typically take to go from idea to something in production at your current company?" Research scientists often struggle to answer < 6 months. Engineers should describe fast iteration cycles.

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| ML fundamentals screen | 45 min: ML concepts, Python, coding | Depth of understanding beyond library calls |
| Take-home / ML project | Build a model for [problem], write up approach, 4–6 hours | Methodology, evaluation rigour, communication |
| System design | Design an ML system end-to-end (data → model → serving → monitoring) | Production thinking, not just research thinking |
| Paper/project deep dive | Discuss their best work in depth | True ownership, ability to defend decisions |
| Behavioural | STAR — collaboration with data engineers, PMs, business stakeholders | ML doesn't succeed in silos |

**Key question:** "What happens to your model's performance 6 months after deployment?" — great candidates immediately discuss distribution shift, monitoring, and retraining pipelines.

### Red Flags
- Can only call `sklearn.fit()` without understanding what it's doing
- No experience with data quality issues — "the data was already clean"
- Has never deployed a model to production
- Evaluation methodology is only accuracy on a test set (no discussion of business metrics)
- No understanding of ML system design beyond the model itself
- Treats LLMs as magic — can't explain tokenisation, context windows, or hallucination

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $110k – $150k |
| Mid | $155k – $200k |
| Senior | $185k – $260k |
| Staff | $230k – $310k |
| Principal / Research Scientist | $280k – $380k+ |

*ML/AI commands a significant market premium in 2025. LLM/GenAI specialists often see +20–30% vs. traditional ML.*
