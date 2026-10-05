---
name: agenta
description: LLM prompt management and evaluation platform. Version prompts, run A/B
  tests, evaluate with metrics, and deploy with confidence using Agenta's self-hosted
  solution.
version: 1.0.0
author: workspace-hub
category: ai-prompting
type: skill
trigger: manual
auto_execute: false
capabilities:
- prompt_versioning
- ab_testing
- evaluation_metrics
- playground_interface
- self_hosted_deployment
- prompt_templates
- model_comparison
- experiment_tracking
tools:
- Read
- Write
- Bash
- Grep
tags:
- agenta
- llm
- prompt-management
- evaluation
- ab-testing
- mlops
- self-hosted
- versioning
platforms:
- python
- docker
related_skills:
- langchain
- dspy
- prompt-engineering
scripts_exempt: true
---

# Agenta

## Quick Start

```bash
# Install Agenta SDK
pip install agenta

# Start Agenta locally with Docker
docker run -d -p 3000:3000 -p 8000:8000 ghcr.io/agenta-ai/agenta

# Or use pip for just the SDK
pip install agenta

# Initialize project
agenta init --app-name my-llm-app
```

## When to Use This Skill

**USE when:**
- Managing multiple versions of prompts in production
- Need systematic A/B testing of prompt variations
- Evaluating prompt quality with automated metrics
- Collaborating on prompt development across teams
- Requiring audit trails for prompt changes
- Building LLM applications that need to iterate quickly
- Need to compare different models with same prompts
- Want a playground for rapid prompt experimentation
- Self-hosting is required for security/compliance

**DON'T USE when:**
- Simple single-prompt applications
- No need for prompt versioning or testing
- Already using another prompt management system
- Rapid prototyping without evaluation needs
- Cost-sensitive projects (evaluation adds API calls)

## Prerequisites

```bash
# SDK installation
pip install agenta>=0.10.0

# For self-hosted deployment
docker pull ghcr.io/agenta-ai/agenta

# Or with docker-compose
git clone https://github.com/Agenta-AI/agenta
cd agenta
docker-compose up -d

# Environment setup
export AGENTA_HOST="http://localhost:3000"
export AGENTA_API_KEY="your-api-key"  # If using cloud version

# For LLM providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```
### Verify Installation

```python
import agenta as ag
from agenta import Agenta

# Initialize client
client = Agenta()

# Check connection
print(f"Agenta SDK version: {ag.__version__}")
print("Connection successful!")
```

## Resources

- **Agenta Documentation**: https://docs.agenta.ai/
- **GitHub Repository**: https://github.com/Agenta-AI/agenta
- **Self-Hosting Guide**: https://docs.agenta.ai/self-hosting
- **API Reference**: https://docs.agenta.ai/api-reference

## Version History

- **1.0.0** (2026-01-17): Initial release with versioning, A/B testing, evaluation, playground, model comparison, self-hosting

---

*This skill provides comprehensive patterns for LLM prompt management with Agenta, refined from production prompt engineering workflows.*

## Sub-Skills

- [1. Prompt Versioning and Management](1-prompt-versioning-and-management/SKILL.md)
- [2. A/B Testing Prompts](2-ab-testing-prompts/SKILL.md)
- [3. Evaluation Metrics and Testing](3-evaluation-metrics-and-testing/SKILL.md)
- [4. Playground and Experimentation](4-playground-and-experimentation/SKILL.md)
- [5. Model Comparison](5-model-comparison/SKILL.md)
- [6. Self-Hosted Deployment](6-self-hosted-deployment/SKILL.md)
- [FastAPI Integration](fastapi-integration/SKILL.md)
- [Langchain Integration](langchain-integration/SKILL.md)
- [1. Prompt Versioning Strategy (+2)](1-prompt-versioning-strategy/SKILL.md)
- [Connection Issues (+2)](connection-issues/SKILL.md)
