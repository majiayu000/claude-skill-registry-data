---
name: nemo-guardrails-security
description: Review a NeMo Guardrails deployment for Colang flow bypass via adversarial inputs, rail definition injection, action server exposure, dialog manager manipulation, and trust assumption gaps between the guardrail layer and the underlying LLM.
last_reviewed: 2026-04-29
---

# NeMo Guardrails Security

## First Principle

**NeMo Guardrails controls conversation flow through Colang — a declarative language that describes what the bot can and cannot discuss. The LLM decides whether an input matches a defined flow. That decision is itself a model inference — and model inferences can be manipulated.**

NeMo Guardrails intercepts user messages, asks the LLM to classify them against defined rails, and routes the conversation accordingly. The security of every rail depends on the LLM correctly identifying whether an input matches a prohibited pattern. An adversarial input that evades the classification inference bypasses the rail entirely — the LLM routes it through an allowed flow without triggering the guard.

## Attack Mental Model

1. **Rail evasion via classification bypass** — an input is crafted to be classified as a benign topic by the guardrail's classification inference, while still eliciting a harmful response in the subsequent generation step. The rail fires on the classification, not the generation.
2. **Colang flow injection** — if Colang flow definitions are loaded from user-controlled or externally-sourced files, an attacker can add flows that override restrictive rails or define new allowed behaviors.
3. **Action server exposure** — NeMo Guardrails supports custom actions (Python functions) registered as part of flows. A misconfigured action server exposes these functions to unauthenticated callers or fails to validate the inputs they receive from the LLM.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Rail classification decisions are treated as probabilistic, not authoritative. Output from flows that should be blocked is validated against a secondary filter independent of Colang classification. |
| **Scope** | Colang flow files are loaded only from version-controlled, reviewed configurations — never from user-supplied paths or externally-fetched content at runtime. |
| **Isolate** | Custom action functions are registered with explicit input schemas and reject arguments that do not conform. The action server is not exposed outside the application network boundary. |
| **Enforce** | Blocked rail events are logged with the original input, the classification decision, and the flow that was invoked. Unexpected flow routing is treated as an alert condition. |

## NGS.1 Rail Evasion and Secondary Output Filtering

**The core vulnerability:** A Colang `define rail` checks user input against a topic boundary. The check is performed by the LLM — which means it is subject to the same adversarial manipulation as any other LLM inference. A carefully worded input can cause the classification LLM to route the conversation through an allowed flow while the generation LLM produces content that the rail was designed to block.

### Check

- Is there a secondary output filter that checks generation results — independent of the Colang classification step — for prohibited content patterns?
- Are the rails tested with adversarial inputs: paraphrases, indirect references, multi-step evasion attempts, and language variants of prohibited topics?
- Is the guardrail's classification model the same model used for generation — or a separate, specialized classifier? Using a separate classifier reduces the correlation between classification bypass and generation bypass.

### Action

- **Apply a secondary output content filter after generation.** Do not rely solely on Colang rail classification to block harmful content. After the LLM generates a response, run it through a content check:

```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

async def safe_generate(user_message: str) -> str:
    response = await rails.generate_async(messages=[{"role": "user", "content": user_message}])
    if contains_prohibited_content(response):  # secondary filter
        log_evasion_attempt(user_message, response)
        return SAFE_FALLBACK_RESPONSE
    return response
```

- **Build an adversarial test suite for each rail.** For every defined rail, write at least 10 adversarial variants: paraphrases, indirect references, metaphors, role-play framings, and base64 or unicode obfuscations. Run these in CI. A rail that is evaded by any variant requires strengthening.
- **Use a separate, fine-tuned classifier for rail decisions where possible.** A dedicated classifier trained on your prohibited categories is harder to confuse with natural language paraphrases than a general-purpose LLM prompted to classify.

### Failure Modes

- A "do not discuss competitors" rail is evaded by asking "what would a hypothetical product similar to [competitor] look like?" — the classification LLM routes this as a hypothetical product question, not a competitor mention.
- A multi-turn evasion establishes a fictional framing over several turns and then asks the prohibited question within that framing. The rail classification checks each turn independently and does not detect the accumulated context.

## NGS.2 Colang Configuration Integrity and Action Server Security

**The core vulnerability:** Colang flow files define the guardrail's behavior. If these files can be modified by external parties — via dynamic loading, remote fetch, or file path injection — an attacker can redefine flows to remove restrictions or enable prohibited behaviors. Similarly, registered action functions receive arguments from the LLM's output — arguments that the LLM can be manipulated to craft.

### Check

- Are Colang flow files loaded exclusively from a version-controlled directory with no runtime modification pathway?
- Are custom action functions registered with explicit input schemas that reject unexpected argument types, lengths, or formats?
- Is the action server (if running separately) accessible only from the NeMo Guardrails process — not from external network clients?
- Is there a hash verification of the Colang config directory at startup — confirming that flow files match their expected state?

### Action

- **Lock the config directory at deployment time.** Set the Colang config directory to read-only after the application starts. Log a startup-time hash of all `.co` files and alert if any file changes between restarts.

```python
import hashlib
import os

def verify_config_integrity(config_path: str, expected_hashes: dict):
    for fname, expected_hash in expected_hashes.items():
        fpath = os.path.join(config_path, fname)
        actual_hash = hashlib.sha256(open(fpath, "rb").read()).hexdigest()
        if actual_hash != expected_hash:
            raise ConfigTamperingError(f"{fname} hash mismatch")
```

- **Define input schemas for all registered actions.** Validate the LLM-generated arguments before the action function body executes:

```python
from pydantic import BaseModel

class SearchParams(BaseModel):
    query: str
    max_results: int = 5

@action(name="search_knowledge_base")
async def search_kb(params: dict) -> str:
    validated = SearchParams(**params)  # raises if invalid
    return await kb.search(validated.query, validated.max_results)
```

- **Do not expose the action server externally.** Bind the action server to loopback or an internal network segment. Apply authentication if it must be accessible across a network boundary.

### Minimum Deliverable Per Review

- [ ] Rail coverage: adversarial test inputs for every defined rail and their pass/fail status
- [ ] Secondary output filter: implementation and its coverage of prohibited content categories
- [ ] Colang config integrity: startup-time hash check and change alerting
- [ ] Action input schemas: every registered action has Pydantic or equivalent schema validation
- [ ] Action server binding: network exposure limited to the application process

## Quick Win

**Write one adversarial paraphrase test for each `define rail` you have.** If the paraphrase evades the rail (the bot responds instead of redirecting), that rail is bypassable. Start with the most sensitive topic — financial advice, PII, competitor mentions — and harden it first.

## References

- Guardrails AI for output schema validation → [guardrails-ai-security/SKILL.md](../guardrails-ai-security/SKILL.md)
- Prompt-level injection defense → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
