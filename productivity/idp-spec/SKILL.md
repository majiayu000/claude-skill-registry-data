---
name: idp-spec
description: Intelligent Delegation Profile — deterministic delegation for multi-agent systems
version: 0.1.0
execution-mode: advisory
argument-hint: "[create_token | validate_token | DelegationContext | GovernanceBus]"
category: fleet-ops
status: candidate
---
# IDP Spec

Intelligent Delegation Profile (IDP) — deterministic, cryptography-backed specification for safe, verifiable delegation in multi-agent systems. Implements the six-tuple IDP framework: `DCTX → CONTRACT → EVIDENCE → ATTEST → DCT → GOVERNANCE_BUS`.

## When to Use

- Creating and validating delegation capability tokens (DCTs) with HMAC signatures
- Establishing delegation contexts (intent, task, delegator, delegatee, contract)
- Logging governance events to an append-only bus with cryptographic provenance
- Managing delegation budgets and context lifecycle
- Enforcing deterministic delegation policies in multi-agent workflows

## Usage

```bash
[idp-spec] create_token(issuer="scheduler", subject="worker", ops_allowed=["read"], binding=..., secret=b"key")
[idp-spec] validate_token(dct, secret=b"key", binding=binding)
[idp-spec] GovernanceBus(base_dir=Path("./_state/governance")).append(...)
```

## Python API

```python
from idp_spec import (
    # Delegation tokens
    DelegationCapabilityToken,
    DelegationTokenManager,
    TokenBinding,
    Caveat,
    ResourceSelector,
    create_token,
    validate_token,
    # Delegation context
    DelegationContext,
    DelegationBudget,
    DelegationContextManager,
    # Governance bus
    GovernanceBus,
    GovernanceEntry,
)

# 1. Create a capability token
binding = TokenBinding(task_id="task-001", contract_id="contract-001")
dct = create_token(
    issuer="scheduler",
    subject="briefing_service",
    ops_allowed=["generate", "write_briefing"],
    binding=binding,
    secret=b"my-secure-key",
)

# 2. Validate token
valid, _ = validate_token(dct, secret=b"my-secure-key", binding=binding)

# 3. Create context & log to governance bus
dctx = DelegationContext(
    intent_id="intent-001",
    task_id="task-001",
    delegator_id="scheduler",
    delegatee_id="briefing_service",
    contract_id="contract-001",
)
bus = GovernanceBus(base_dir=Path("./_state/governance"))
bus.append(
    intent_id=dctx.intent_id,
    task_id=dctx.task_id,
    tuple_type="DCT",
    tuple_data={"token_id": dct.token_id},
    contract_id=dctx.contract_id,
    capability_token_id=dct.token_id,
)
```

## Key Concepts

- **Six-tuple chain**: `DCTX → CONTRACT → EVIDENCE → ATTEST → DCT → GOVERNANCE_BUS` — each step produces a typed, signed artifact.
- **Delegation Capability Token (DCT)**: HMAC-signed token with issuer, subject, allowed operations, caveats, resource selectors, and token binding.
- **Token binding**: `TokenBinding` links a token to a specific task and contract — prevents token replay across contexts.
- **Caveats**: Restrictions on token usage (expiry, rate limits, scope constraints).
- **Delegation context**: `DelegationContext` captures the full delegation intent (who delegates what to whom, under which contract). `DelegationBudget` tracks resource limits.
- **Governance bus**: `GovernanceBus` provides append-only logging of governance events with typed entries (`GovernanceEntry`).
- **Feature flag**: `ENABLE_IDP=true` activates full enforcement. Default: disabled (backward-compatible pass-through).
- **Token manager**: `DelegationTokenManager` handles token lifecycle (creation, validation, revocation, rotation).

## Install

```bash
cd /work/active/oss/packages/python/idp-spec/
pip install -e ".[test]"
```

## Package

- **Repo**: `hummbl-io/oss`
- **Path**: `packages/python/idp-spec/`
- **License**: MIT OR Apache 2.0
- **Dependencies**: stdlib only (optional: `hummbl-governance>=1.1.0` via `[governance]` extra)
