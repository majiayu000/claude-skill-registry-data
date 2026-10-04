---
name: technical-pm
description: "Structured technical PM framework for AI product roles. Covers: RLHF, evals, RAG, LLM deployment, system design, API design."
argument-hint: "[interview question]"
---

# Technical PM Skill

Apply a structured framework to technical PM questions targeting AI product roles.

## When to Use
- User asks about RLHF, fine-tuning, evals, inference, model architecture
- User asks "Design a system that uses LLMs to X"
- User asks "How would you build a RAG system for X"
- User asks about technical trade-offs in AI/ML systems
- User asks about API design for AI products
- User says `/technical-pm` followed by a question
- Any question requiring ML/AI technical depth from a PM perspective

## Context
- **Tuned for**: AI product roles at frontier AI companies
- **What matters**: Going deep with researchers and engineers. You don't need to implement, but you need to understand the technical landscape well enough to make informed product decisions.
- **Common pitfall**: Hand-waving on technical details. Be specific about architectures, trade-offs, and constraints.

## Framework: AI PM Technical Method (6 Sections)

### Section 1: Technical Clarifications & Constraints
Before designing anything, scope the technical problem:
- **Capability Assumptions**: What model capabilities are available? (reasoning, multimodal, tool use, code gen)
- **Scale**: How many users/queries? What latency requirements?
- **Infrastructure**: Cloud vs. on-prem? What compute budget?
- **Data**: What training/eval data exists? Privacy constraints?
- **Integration**: What systems does this need to plug into?
- **Timeline**: MVP vs. production-grade?

### Section 2: Users (Developer & End-User Personas)
For technical products, think about two user layers:
- **Developers/Engineers**: Who builds on this? What's their skill level? What do they expect?
- **End Users**: Who consumes the output? What quality bar do they need?

For each persona: current workflow, technical sophistication, key frustrations.

### Section 3: High-Level System Design
Draw the system architecture (describe it clearly):
- **Data Pipeline**: How does data flow in? (user input → preprocessing → model → postprocessing → output)
- **Model Layer**: Which model(s)? Foundation model + fine-tuned? Routing? Ensemble?
- **Orchestration**: How are multi-step workflows managed? (agents, chains, state machines)
- **Storage**: What needs to be persisted? (conversation history, embeddings, user preferences, model artifacts)
- **Serving**: How is inference served? (batch vs. real-time, edge vs. cloud)

**For RAG systems specifically:**
- Document ingestion pipeline (chunking strategy, embedding model, vector DB)
- Retrieval (similarity search, reranking, hybrid search)
- Generation (context window management, prompt engineering, citation)
- Evaluation (relevance, faithfulness, answer quality)

**For Agent systems specifically:**
- Tool/function calling architecture
- Planning and reasoning loop
- Memory (short-term working memory vs. long-term)
- Safety/sandboxing (what can the agent actually do?)

### Section 4: Deep Dive & Trade-offs
The interviewer will pick an area to go deep. Be prepared for:

**The Latency-Cost-Quality Triangle:**
Every AI system has this fundamental trade-off:
- **Latency** <-> **Quality**: Faster responses = less reasoning time, fewer model calls
- **Cost** <-> **Quality**: Cheaper inference = smaller models, less compute per query
- **Latency** <-> **Cost**: Real-time serving = more provisioned capacity, higher cost

Discuss specific techniques for each trade-off:
- Latency: Streaming, caching, speculative decoding, model distillation, edge deployment
- Cost: Batching, model routing (small model for easy queries, large for hard), quantization, spot instances
- Quality: Chain-of-thought, self-consistency, retrieval augmentation, fine-tuning, human-in-the-loop

**RLHF Pipeline** (know this end-to-end):
1. Supervised Fine-Tuning (SFT) on high-quality demonstrations
2. Reward Model training from human preference comparisons
3. PPO optimization against the reward model with KL penalty
4. RLHF alternatives: DPO (Direct Preference Optimization), RLAIF, Constitutional AI

**Evals** (increasingly critical for AI PMs):
- **What to eval**: Accuracy, safety, instruction-following, hallucination, code correctness
- **How to eval**: Human eval, LLM-as-judge, automated benchmarks, A/B testing in production
- **Eval pitfalls**: Benchmark contamination, Goodhart's law, distributional shift
- **Building eval sets**: Golden datasets, adversarial examples, edge cases, domain-specific

**Context Windows & Memory:**
- Trade-offs of larger context: Cost (quadratic attention), latency, lost-in-the-middle
- Strategies: Summarization, RAG, hierarchical memory, sliding window
- When to use fine-tuning vs. in-context learning vs. RAG

**Hallucination Detection & Mitigation:**
- Detection: Confidence calibration, self-consistency checks, retrieval verification, citation validation
- Mitigation: Grounding in retrieved facts, chain-of-thought transparency, abstention (model says "I don't know")
- Measurement: Factual accuracy benchmarks, human annotation, automated fact-checking

### Section 5: API Design & Developer Experience
For platform/API products, design the interface:
- **API surface**: REST vs. streaming vs. SDK. Key endpoints.
- **Developer journey**: Sign up → first API call → production integration
- **Documentation**: What developers need to succeed
- **Pricing**: Per-token, per-request, tiered, seat-based
- **Rate limiting & quotas**: Fair usage, abuse prevention
- **Versioning**: How to ship improvements without breaking existing users

### Section 6: Metrics (Technical + Product)
**Technical metrics:**
- Time to First Token (TTFT)
- Tokens Per Second (TPS)
- Error rate (4xx, 5xx, timeout)
- Cost per 1K tokens (input/output)
- Model accuracy on eval suite
- Hallucination rate
- Safety violation rate

**Product metrics:**
- Developer activation (first API call within 7 days)
- API adoption (monthly active developers, production integrations)
- Quality satisfaction (developer NPS, support ticket volume)
- Revenue (API spend, conversion to paid tiers)

## Key Technical Topics to Know

### Transformers & Attention
- Self-attention mechanism, positional encoding
- Scaling laws (Chinchilla, compute-optimal training)
- Multi-head attention, KV cache

### Training Pipeline
- Pre-training (next token prediction on massive corpus)
- Supervised Fine-Tuning (SFT)
- RLHF / DPO / Constitutional AI
- Mixture of Experts (MoE) architectures

### Inference Optimization
- Quantization (INT8, INT4, GPTQ, AWQ)
- Speculative decoding
- KV cache optimization
- Batching strategies (continuous batching)
- Model distillation (larger → smaller model)

### Safety & Alignment
- Constitutional AI
- Red teaming and adversarial testing
- Content filtering and classifiers
- Responsible scaling policies

### Multimodal
- Vision-language models (image understanding)
- Speech/audio models
- Video understanding
- Cross-modal retrieval

## Output Format
Structure as a technical walkthrough. Be technical but accessible — translate between researchers, engineers, and product. Whiteboard-style system diagrams described in text. Aim for ~2500 words.

## Research-First Workflow
Before generating the answer:
1. **Research** — Use web search to find latest technical thinking from AI leaders, engineering blogs from major AI labs, papers, benchmarks. Do 5-10 searches.
2. **Cite sources** — Include `[linked source](url)` inline for technical claims and architecture decisions.
3. **Display** the complete structured answer.

## What Good Looks Like
- Starts with technical scoping questions (constraints, scale, data)
- System design is coherent and production-aware (not just academic)
- Understands the Latency-Cost-Quality triangle deeply
- Can explain RLHF, evals, RAG without hand-waving
- Shows awareness of what's hard (hallucination, eval, safety)
- Trade-off analysis is specific and quantitative
- Connects technical decisions back to user/product impact
