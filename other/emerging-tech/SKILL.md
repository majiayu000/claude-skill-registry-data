---
name: emerging-tech
description: "Architecture assistance for 2026-2030 technologies (6G, Matter IoT, Vector DBs). Use when: 6g, iot, matter, vector, embedding, semantic search, rag, edge native, post-quantum."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/core/emerging-tech.skill.md"
  tags: "core"
  core: "false"
  context_cost: "medium"
---
# Emerging Tech Skill

## Goal
To future-proof applications for the next wave of connectivity and intelligence.

## Capabilities

### 1. 6G & Edge-Native Design
-   **Ultra-Low Latency**: Design systems for <1ms loops (Haptic Internet).
-   **Compute Continuum**: Seamlessly move workloads between Device <-> Edge <-> Cloud.
-   **Agentic IoT**: Devices that negotiate with each other autonomously (M2M economy).

### 2. Matter Protocol (IoT)
-   **Interoperability**: One protocol for Apple/Google/Amazon smart home ecosystems.
-   **Local Control**: Devices work without internet (privacy-first).
-   **Thread/Wi-Fi 6**: Understanding the mesh network topology.

### 3. Vector Computing (AI Memory)
-   **Semantic Search**: Replacing keyword search with "meaning" search (Embeddings).
-   **RAG Pipelines**: Retrieval-Augmented Generation for grounding LLMs.
-   **Databases**: Pinecone, Weaviate, pgvector strategy.

## Steps
1.  **Latency Matters**: In 6G apps, the speed of light is the bottleneck. Move data closer to the user.
2.  **Privacy by Design**: Matter devices talk locally. Don't send sensitive sensor data to the cloud unless necessary.
3.  **Embed Everything**: Text, Images, Audio. If it's data, it can be a vector.

## Deliverables
-   `vector-strategy.md`: Plan for embedding data.
-   `matter-config.yaml`: Device capability profile.
-   `edge-placement.drawio`: Diagram of compute distribution.

## Security & Guardrails

### 1. Skill Security (Emerging Tech)
- **Protocol Vulnerability Awareness**: When implementing bleeding-edge protocols (Matter, 6G), explicitly track and enforce the latest CVEs and security advisories, as novel tech often experiences a "wild west" period of rapid vulnerability discovery.
- **Vector DB Poisoning Protection**: Ensure the vector embedding pipeline sanitizes input data to prevent "Semantic Poisoning," where adversarial text is injected to skew RAG retrieval toward malicious recommendations or prompt injections.

### 2. System Integration Security
- **IoT Matter Isolation**: Matter local-network device configuration must employ micro-segmentation, ensuring that compromised Smart Home devices cannot pivot to attack the primary Application layer or the user's secure subnet.
- **Post-Quantum Cryptography Readiness**: For designs spanning into 2030, architectural recommendations must advocate for cryptographic agility, replacing hardcoded RSA/ECC implementations with PQC-ready hybrid negotiation protocols.

### 3. LLM & Agent Guardrails
- **Speculative Hallucination Constraints**: Agents advising on 6G or future IoT standards must clearly delineate between ratified standards and speculative draft RFCs, preventing the implementation of unstable, insecure proprietary extensions.
- **RAG Data Leakage**: When pulling memory from Vector DBs, the LLM must obey strict tenant boundaries (Access Control Lists attached to vector metadata) to ensure User A's embedded data is never retrieved to answer User B's query.
