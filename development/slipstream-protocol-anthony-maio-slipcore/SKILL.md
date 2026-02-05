---
name: slipstream-protocol
description: Slipstream Protocol v2 - Semantic Quantization for Multi-Agent Communication
---

# Slipstream Protocol Reference

## Overview

Slipstream (SLIP) is a semantic quantization protocol for efficient multi-agent coordination. Instead of transmitting verbose natural language, agents communicate via compact references to a shared semantic codebook (UCR).

**Key benefit**: 70-80% token reduction vs JSON-wrapped messages.

## Wire Format

```
SLIP v1 <src> <dst> <anchor> [payload...]
```

- `SLIP v1` - Protocol marker and version
- `<src>` - Source agent identifier
- `<dst>` - Destination agent identifier
- `<anchor>` - UCR semantic anchor (the intent)
- `[payload...]` - Optional unquantizable content

## Core Anchors (UCR v1.0)

### Requests
| Anchor | Description |
|--------|-------------|
| `RequestTask` | Ask agent to do something |
| `RequestPlan` | Ask for a plan |
| `RequestReview` | Ask for code/plan review |
| `RequestHelp` | Ask for assistance |
| `RequestCancel` | Request cancellation |
| `RequestResource` | Request resource allocation |

### Information
| Anchor | Description |
|--------|-------------|
| `InformComplete` | Report task completion |
| `InformProgress` | Share progress update |
| `InformBlocked` | Report being blocked |
| `InformStatus` | General status update |
| `InformResult` | Share computed result |

### Proposals
| Anchor | Description |
|--------|-------------|
| `ProposePlan` | Suggest a plan |
| `ProposeChange` | Suggest a modification |
| `ProposeAlternative` | Suggest alternative approach |
| `ProposeRollback` | Suggest reverting changes |

### Evaluations
| Anchor | Description |
|--------|-------------|
| `EvalApprove` | Approve/accept something |
| `EvalReject` | Reject something |
| `EvalNeedsWork` | Request revisions |
| `EvalComplete` | Mark as complete |

### Meta/Control
| Anchor | Description |
|--------|-------------|
| `Accept` | Accept a proposal/request |
| `Reject` | Decline a proposal/request |
| `MetaAck` | Acknowledge receipt |
| `MetaHandoff` | Hand off responsibility |
| `MetaEscalate` | Escalate issue |
| `Fallback` | Unquantizable (see payload) |

## Examples

```
# Simple request
SLIP v1 alice bob RequestReview

# With payload
SLIP v1 planner executor RequestTask implement_auth_module

# Report completion
SLIP v1 developer team InformComplete user_service

# Approve with note
SLIP v1 reviewer author EvalApprove lgtm

# Fallback for complex content
SLIP v1 devops sre Fallback check kubernetes pods for OOMKilled
```

## Python Usage

```python
from slipcore import slip, decode, quantize, think_quantize_transmit

# Create message directly
wire = slip("alice", "bob", "RequestReview")
# -> "SLIP v1 alice bob RequestReview"

# Think-Quantize-Transmit pattern
wire = think_quantize_transmit(
    "Please check the auth code for security issues",
    src="dev", dst="reviewer"
)
# -> "SLIP v1 dev reviewer RequestReview"

# Decode
msg = decode(wire)
print(msg.anchor.canonical)  # "Request review of work"
```

## UCR Semantic Manifold

Each anchor is a position in a 4-dimensional semantic space:

| Dimension | Range | Meaning |
|-----------|-------|---------|
| ACTION | 0-7 | observe, inform, ask, request, propose, commit, evaluate, meta |
| POLARITY | 0-7 | negative to positive valence |
| DOMAIN | 0-7 | task, plan, observation, evaluation, control, resource, error, general |
| URGENCY | 0-7 | background to critical |

## Extension Layer

Core anchors: 0x0000-0x7FFF (standard, immutable)
Extension anchors: 0x8000-0xFFFF (installation-specific)

```python
from slipcore import ExtensionManager

manager = ExtensionManager()
anchor = manager.add_extension(
    canonical="Request Kubernetes scaling",
    mnemonic="RequestK8sScale",
)
```

## Design Principles

1. **No special characters** - Avoids BPE fragmentation
2. **Space-separated** - Clean tokenization
3. **CamelCase anchors** - Often single tokens
4. **Semantic not syntactic** - Meaning over compression
