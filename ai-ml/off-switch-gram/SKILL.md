---
name: off-switch-gram
description: Methodology from Anthropic's "An off switch for dual-use knowledge in AI models" (Jul 2026). Use when you need to surgically remove or gate specific capabilities/knowledge (dual-use, dangerous, or disallowed) from a model while preserving general performance, and want that removal to RESIST restoration via fine-tuning. Based on Gradient-Routed Auxiliary Modules (GRAM) — isolating a capability in a removable module and deleting it.
license: Complete terms in LICENSE.txt
---

# GRAM — Gradient-Routed Auxiliary Modules (An "Off Switch")

Methodology from Anthropic's "An off switch for dual-use knowledge in AI models" (Jul 8, 2026). Problem: current methods (unlearning, safety training) only *hide* dangerous capabilities — they're easily recovered by modest fine-tuning. GRAM provides a structural "off switch."

## Core mechanism

- Train a model that contains an **Auxiliary Module** dedicated to a target capability (e.g., biological weapons design knowledge).
- Route the capability's gradient into that module so the knowledge is concentrated there rather than distributed across the whole network.
- After training, **delete the module**. Result: the capability is gone, and the model behaves almost exactly as if it had *never been trained on the capability at all* — general performance is largely preserved (small, bounded degradation).
- Empirically the removal **resists restoration** by subsequent fine-tuning far better than standard unlearning.

## Why it beats unlearning

- Unlearning only suppresses; the knowledge remains reconstructable from remaining weights with a little fine-tuning.
- GRAM physically isolates + removes the weights responsible, so there's nothing left to recover from.
- Measured across 7 model sizes from 50M to 5B parameters; effect held consistently — capability removal ≈ "never-trained" baseline.

## Workflow to apply GRAM-style isolation

1. Identify the target capability to gate (dual-use content, a disallowed tool, a sensitive skill).
2. Architect the model with an auxiliary module and a routing mechanism that directs that capability's gradients into the module during training.
3. Train normally; verify the capability lives in the module (ablation: removing module drops the capability but not general tasks).
4. Delete the module for the "off" deployment. For "on" deployments, keep it but gate access by context/permissions.
5. Validate: re-fine-tune the depeted model to confirm the capability does NOT come back (the key GRAM advantage).

## Caveats

- Requires architectural intervention at training time — not a post-hoc patch for an already-trained monolithic model.
- Best paired with evaluation that explicitly attempts restoration (adversarial fine-tuning) to prove the switch holds.

## Activation keywords

GRAM, gradient-routed auxiliary modules, off switch for dual-use knowledge, surgical capability removal, model unlearning vs deletion, resist fine-tuning recovery, capability isolation module, dual-use knowledge gating, Anthropic off switch 2026, remove dangerous capability preserve general performance
