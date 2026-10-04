---
name: spikingmoe
description: "SpikingMoE — spike-driven Transformer with LGN-inspired Mixture-of-Experts (MoE) for dynamic computation in SNNs"
version: 1.0.0
author: arXiv 2605.23188 (Yukai Yang et al.)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [SNN, MoE, Spiking-Neural-Networks, Transformer, Neuromorphic, Brain-Inspired-Computing, Visual-Recognition]
    related_skills: [spiking-neural-network-analysis, spikingjelly-framework, elastic-spiking-transformer]
---

# SpikingMoE: SDPrompt-Guided Dynamic Expert Fusion in Spiking Neural Networks

**Paper**: arXiv:2605.23188 (May 2026)  
**Authors**: Yukai Yang, Chenxi Qin, Jungang Li, Xin Zhang, Wenwei Shao, Liqun Chen  
**Code**: Project Page (open-source)

## Summary

SpikingMoE integrates a **spike-driven Transformer** with a **Mixture-of-Experts (MoE)** framework for dynamic computation in Spiking Neural Networks. Inspired by the **lateral geniculate nucleus (LGN)**, it introduces a **spike-driven prompt (SDprompt)** mechanism that enables input-dependent expert routing in a biologically plausible manner. This is the **first open-source SNN framework** integrating MoE into a spike-driven Transformer with LGN-inspired routing.

## Key Innovations

1. **LGN-Inspired SDprompt Routing**: The lateral geniculate nucleus (LGN) selectively modulates sensory signals before routing to cortical areas. SpikingMoE mimics this with a spike-driven prompt that conditions expert selection on the input, enabling context-aware dynamic computation.

2. **Spike-Compatible MoE**: Replaces standard MLPs in the Spike-driven Transformer with spike-compatible expert modules. Enforces binary spike communication throughout, ensuring compatibility with neuromorphic hardware.

3. **Fully Binary Communication**: All inter-module signals remain binary spikes (0/1), replacing energy-intensive multiply-accumulate (MAC) operations with low-power accumulation (AC) operations.

## Architecture

```
Input → Spike Embedding → Spike-Driven Transformer Blocks (×N)
  Each block:
    → Spiking Self-Attention (SDSA)
    → Spike-Compatible MoE (replacing MLP)
      → SDprompt Generator (LGN-inspired)
      → Top-K Expert Router (spike-compatible)
      → Expert Networks (spiking neurons)
```

### SDprompt Mechanism

The spike-driven prompt is generated from the input spike sequence and conditions the expert routing decision. Unlike soft prompts in ANNs, SDprompt operates entirely in the spike domain:

- **Input**: Spike-form features from the preceding self-attention layer
- **Processing**: Lightweight spiking network that produces routing logits
- **Output**: Binary routing decisions for expert selection

### Expert Architecture

Each expert is a dedicated spiking neuron pathway that processes its assigned inputs:
- Maintains binary spike communication
- Uses Leaky-Integrate-and-Fire (LIF) or similar spiking neurons
- Sparsely activated (only top-K experts fire per input)

## Experimental Results

| Dataset | Top-1 Accuracy | Reference |
|---------|---------------|-----------|
| CIFAR-10 | 94.09% | Baseline SNN Transformer ~93% |
| CIFAR-100 | 74.54% | Baseline SNN Transformer ~72% |

- Demonstrates that modular expert routing can be incorporated into SNNs while retaining reasonable performance
- Achieves comparable or better accuracy than standard SNN Transformers with fewer active parameters per forward pass
- Energy-efficient due to sparse expert activation + binary spike communication

## Key Formulas

### SDprompt Routing

The routing decision for input x to expert i is:

```
g_i(x) = softmax(topK(r(x)))_i
```

where `r(x)` is the SDprompt router output and `topK` selects the K highest-activating experts.

### Spike-Driven Expert Output

Each expert processes input through spiking neurons:

```
y_expert = Σ_i g_i(x) · SNN_expert_i(x)
```

where `SNN_expert_i` is a spiking neuron module and `g_i(x)` is the routing weight (binary or soft).

## Use Cases

1. **Neuromorphic Visual Recognition**: Deploy on Loihi/TrueNorth hardware with dynamic computation
2. **Energy-Efficient Edge AI**: Selective expert activation reduces computation at inference time
3. **Scalable SNN Architectures**: MoE enables scaling model capacity without proportional compute increase

## Implementation Notes

- Compatible with the **Spike-driven Transformer** architecture (SDSA - Spike-Driven Self-Attention)
- Uses Hadamard product and sparse additions instead of matrix multiplications
- All activations are binary spikes → suitable for neuromorphic deployment
- **Activation**: spiking MoE, spike-driven transformer, SNN expert routing, LGN spiking, neuromorphic MoE

## Pitfalls

- MoE introduces routing overhead; the router itself must be spike-compatible
- Training may require surrogate gradients (standard SNN training technique)
- Expert load balancing is critical — unbalanced routing reduces effective capacity
- Current evaluation limited to CIFAR-10/100; ImageNet-scale results not yet available
