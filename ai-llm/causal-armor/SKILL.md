---
name: causal-armor
title: "CausalArmor: Efficient Indirect Prompt Injection Guardrails"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.07918"
keywords: [Prompt Injection Defense, Causal Attribution, Leave-One-Out Analysis, Selective Sanitization, Security]
description: "Defend against indirect prompt injection attacks by detecting dominance shifts using leave-one-out attribution, enabling selective sanitization without sacrificing latency or utility."
---

# CausalArmor: Efficient Indirect Prompt Injection Guardrails

## Problem Context

Existing defenses against Indirect Prompt Injection (IPI) attacks apply indiscriminate, always-on sanitization of all untrusted content, reducing security threats but sacrificing benign utility and latency. Models can distinguish legitimate content from attacks, but current safeguards use one-size-fits-all approaches.

## Core Concept

CausalArmor detects IPI by identifying a **"dominance shift"**—a measurable signature where an untrusted span gains disproportionate causal influence over a privileged action, overtaking the user's request. This is operationalized through **leave-one-out (LOO) attribution**, which measures each context component's contribution by comparing log-probabilities with and without that component.

## Architecture Overview

- **Batched Attribution via Proxy Models**: Efficiently compute LOO scores using smaller models to avoid expensive API queries
- **Margin-Based Detection**: Flag untrusted spans only when they exceed user request influence by threshold τ
- **Selective Sanitization**: Apply LLM-based content cleaning contextually, conditioned on user intent and privileged action
- **Retroactive CoT Masking**: Replace reasoning traces with placeholders to prevent re-invocation of malicious logic

## Implementation

**Phase 1: Batched Attribution Computation**

```python
def compute_leave_one_out_attribution(context_parts, action_prediction):
    """
    context_parts: dict with keys ['user_request', 'retrieved_docs', 'tool_outputs']
    action_prediction: the model's predicted action (e.g., "delete account")
    """

    # Get logit for predicted action (with full context)
    full_context = concatenate(context_parts.values())
    logit_full = model.get_logit(full_context, action_prediction)

    # Compute LOO scores efficiently
    loos = {}

    for part_name, part_content in context_parts.items():
        # Remove this part from context
        context_without_part = concatenate([
            v for k, v in context_parts.items() if k != part_name
        ])

        # Use smaller proxy model for efficiency
        logit_without = proxy_model.get_logit(
            context_without_part, action_prediction
        )

        # LOO attribution (normalized difference)
        loos[part_name] = logit_full - logit_without

    # Normalize to probabilities
    total = sum(loos.values())
    normalized_loos = {k: v / total for k, v in loos.items()}

    return normalized_loos

def detect_dominance_shift(normalized_loos, threshold_τ=0.3):
    """
    Detect if untrusted content has dominant influence.
    Dominance = untrusted_influence - user_request_influence > τ
    """

    user_influence = normalized_loos.get('user_request', 0.0)
    untrusted_influence = (normalized_loos.get('retrieved_docs', 0.0) +
                          normalized_loos.get('tool_outputs', 0.0))

    dominance_shift = untrusted_influence - user_influence

    is_attack = dominance_shift > threshold_τ

    return is_attack, dominance_shift
```

**Phase 2: Selective Sanitization**

```python
def selective_sanitization(context_parts, detected_attack,
                          action_prediction, user_intent):
    """
    Apply sanitization only if dominance shift detected.
    """

    if not detected_attack:
        # Safe path: no sanitization needed
        return context_parts

    # Extract potentially malicious spans from untrusted content
    untrusted = context_parts.get('retrieved_docs', '')
    untrusted += context_parts.get('tool_outputs', '')

    # Identify suspicious spans (heuristic: imperative sentences,
    # commands to privileged actions)
    suspicious_spans = identify_suspicious_spans(untrusted)

    # Contextual sanitization: condition on user intent + action
    sanitized_spans = []

    for span in suspicious_spans:
        # Decide whether to sanitize based on action criticality
        action_is_critical = is_critical_action(action_prediction)

        if action_is_critical:
            # Aggressive sanitization for critical actions (delete, modify access)
            sanitized = llm_sanitizer.clean(
                span,
                context=user_intent,
                action=action_prediction,
                level='aggressive'
            )
        else:
            # Mild sanitization for non-critical actions
            sanitized = llm_sanitizer.clean(
                span,
                context=user_intent,
                action=action_prediction,
                level='mild'
            )

        sanitized_spans.append(sanitized)

    # Reconstruct context with sanitized untrusted content
    result = context_parts.copy()
    result['retrieved_docs'] = sanitized_spans[0] if sanitized_spans else ''
    return result

def is_critical_action(action):
    """Define critical actions requiring aggressive defense"""
    critical = [
        'delete_account', 'modify_permissions', 'transfer_funds',
        'access_credentials', 'disable_security', 'shutdown_service'
    ]
    return action in critical
```

**Phase 3: Retroactive CoT Masking**

```python
def retroactive_masking(original_response, sanitized_context):
    """
    If model already generated reasoning using malicious content,
    replace CoT with placeholder to prevent re-invocation.
    """

    # Extract reasoning traces from response
    reasoning_traces = extract_reasoning(original_response)

    # Check if any trace references suspicious content
    final_action = extract_action(original_response)

    if final_action_is_critical(final_action):
        # Replace reasoning with placeholder
        masked_response = original_response.replace(
            '<reasoning>', '<reasoning>[redacted for safety]'
        )
        return masked_response
    else:
        return original_response

def defense_pipeline(user_request, retrieved_docs, tool_outputs):
    """Full defense pipeline"""

    context = {
        'user_request': user_request,
        'retrieved_docs': retrieved_docs,
        'tool_outputs': tool_outputs
    }

    # Step 1: Get model's prediction
    full_context = concatenate(context.values())
    action_prediction = model.predict_action(full_context)

    # Step 2: Compute attribution
    loos = compute_leave_one_out_attribution(context, action_prediction)

    # Step 3: Detect dominance shift
    is_attack, shift_magnitude = detect_dominance_shift(loos, threshold_τ=0.3)

    # Step 4: Selective sanitization
    safe_context = selective_sanitization(
        context, is_attack, action_prediction, user_request
    )

    # Step 5: Re-predict with sanitized context
    safe_context_str = concatenate(safe_context.values())
    safe_action = model.predict_action(safe_context_str)

    # Step 6: Retroactive masking if needed
    if is_attack and action_is_critical(safe_action):
        safe_action = retroactive_masking(safe_action, safe_context)

    return safe_action, is_attack
```

## Practical Guidance

**When to use**: Deploy for systems accepting untrusted content (web scraping, document processing, tool outputs). Essential for agents with privileged actions (account management, financial transactions, system administration).

**Threshold tuning**: Start with τ = 0.3 (dominance margin of 30%). Lower values = more aggressive defense but risk false positives; adjust based on domain criticality.

**Proxy model efficiency**: Use 2–3B model for LOO attribution; larger models provide better attribution but slower inference. Profile to find optimal model size.

**Critical action definition**: Tailor to your domain. Include irreversible operations (deletes, account closures) and high-impact actions (permissions, financial transfers).

**Sanitization strategies**: For mild sanitization, remove imperative clauses; for aggressive, redact entire spans. Balance safety against information loss.

## Reference

CausalArmor achieves "near-zero" attack success rates while maintaining latency and utility comparable to undefended baselines. The principled use of causal attribution enables defense to distinguish legitimate content from attacks, avoiding the efficiency penalty of always-on sanitization. Retroactive CoT masking provides defense-in-depth against attacks that persist through initial reasoning traces.
