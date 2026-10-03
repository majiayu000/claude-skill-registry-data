---
name: webapp-ai-llm
description: "Webapp Ai Llm."
domain: cybersecurity
---

|
| **Input Rail** | A guardrail that intercepts and validates user input before it reaches the LLM, blocking injection attempts and redacting sensitive data |
| **Output Rail** | A guardrail that validates LLM-generated output before it reaches the user, filtering toxic content and enforcing schema compliance |
| **Colang** | NVIDIA's domain-specific language for defining conversational guardrail flows, with Python-like syntax for specifying user intent patterns and bot responses |
| **PII Redaction** | The process of detecting and masking personally identifiable information (names, emails, SSNs) in text before processing |
| **Content Policy** | A configuration file defining which topics, patterns, and content categories are allowed or blocked by the guardrail system |
| **Self-Check Rail** | A NeMo Guardrails technique where the LLM itself evaluates whether its input or output violates defined policies |
| **Hallucination Detection** | Output validation that checks whether the LLM response is grounded in the provided context, flagging fabricated claims |

## Tools & Systems

- **NVIDIA NeMo Guardrails**: Open-source toolkit for adding programmable input, dialog, and output rails to LLM applications using Colang flow definitions and YAML configuration
- **Guardrails AI**: Python framework for structured output validation with a hub of pre-built validators for PII, toxicity, JSON schema compliance, and more
- **Microsoft Presidio**: Open-source PII detection and anonymization engine supporting 30+ entity types with configurable NLP backends
- **Colang 2.0**: Event-driven interaction modeling language for defining guardrail flows with Python-like syntax, supporting multi-turn dialog control
- **OpenAI Guardrails Python**: OpenAI's client-side guardrails library for prompt injection detection and content policy enforcement
