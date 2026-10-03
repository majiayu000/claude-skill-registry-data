---
name: webapp-ai-model
description: "Webapp Ai Model."
domain: cybersecurity
---

|
| **Direct Prompt Injection** | An attack where the user directly includes adversarial instructions in their input to override the system prompt or manipulate LLM behavior |
| **Indirect Prompt Injection** | An attack where malicious instructions are embedded in external data sources (documents, web pages, emails) consumed by the LLM during processing |
| **Heuristic Scoring** | A rule-based analysis method that computes anomaly scores from structural features of the input text without using machine learning |
| **DeBERTa Classifier** | A transformer-based sequence classification model fine-tuned on prompt injection datasets to distinguish adversarial from benign inputs |
| **Canary Token** | A unique marker inserted into system prompts to detect if the LLM has been tricked into leaking its instructions |
| **OWASP LLM01** | The top risk in the OWASP Top 10 for LLM Applications (2025), covering both direct and indirect prompt injection vulnerabilities |

## Tools & Systems

- **protectai/deberta-v3-base-prompt-injection-v2**: Hugging Face transformer model fine-tuned for binary prompt injection classification with 99%+ accuracy on standard benchmarks
- **Rebuff**: Open-source multi-layered prompt injection detection framework by ProtectAI combining heuristics, LLM-based detection, vector similarity, and canary tokens
- **Pytector**: Lightweight Python package for prompt injection detection supporting local DeBERTa/DistilBERT models and API-based safeguards
- **OWASP LLM Top 10**: Industry-standard risk taxonomy for LLM application security, with LLM01 dedicated to prompt injection
- **deepset/prompt-injections**: Hugging Face dataset containing labeled prompt injection examples used for training and evaluating detection models
