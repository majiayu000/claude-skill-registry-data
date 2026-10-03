---
name: simulate-network-latency
description: "Use when injecting packet loss/jitter/high latency to stress-test netcode rollback and prediction algorithms."
---

# simulate-network-latency - Skill Definition

## 1. Overview

Injects controlled network degradation (packet loss, jitter, high latency) to stress-test netcode rollback and prediction algorithms. Validates the robustness of client-server synchronization under extreme conditions, identifying desynchronization points that would break multiplayer gameplay. Output: structured `network_test.md` with failure categorization and severity mapping.

## 2. When to Use

Use when:
- You have multiplayer netcode and want to stress-test rollback and prediction under degraded conditions.
- Players report desyncs, hit registration issues, or movement stutter that may be network-related.
- Validating rejoin/reconnection behavior after transient high latency or packet loss.

Do not use when:
- The game is single-player with no netcode — this skill targets multiplayer synchronization.
- Basic connectivity isn't established yet — fix the happy path first.

## 3. Triggers & Red Flags

* **Triggers**: `simulate-network-latency`, `network test`, `packet loss`, `latency test`, `rollback`, `prediction`, `netcode`, `network simulation`, `lag testing`.
* **Red Flags**:
    * **Critical Desynchronization (Desync)**: Observed divergence in game state between clients that cannot be reconciled by existing mechanisms.
    * **Prediction/Reconciliation Failure**: Client prediction consistently fails to align with server truth under moderate conditions.
    * **Unrecoverable Connection Drop**: Total failure to handle rejoin or reconnection attempts after transient high latency/loss scenarios.

## 3. Core Pattern

1. **Condition Profiling** — Define a matrix of test scenarios ranging from LAN to Worst-case (Satellite) conditions, specifying Ping, Packet Loss, and Jitter for each scenario.
2. **Stress Testing Execution** — Monitor key metrics including Player Movement (prediction accuracy), Combat Hits (registration precision), State Sync (consistency), and Resilience.
3. **Failure Categorization & Severity Mapping** — Classify failures by severity: Low (negligible), Medium (noticeable), High (degrading experience), or Critical (unplayable/desync).
4. **Root Cause Analysis (RCA)** — For high-severity failures, identify technical causes (e.g., insufficient prediction windows or lack of validation).
5. **Specification Export** — Write the finalized analysis into `{TARGET_FOLDER}/docs/network_test.md`.

## 4. Intercepts & Guards

* **[Desync Detection Intercept]**: If two clients show divergent game states: *"I've detected a critical state desynchronization between Client A and Client B at [Time/Event]. This is a 'Critical' failure that must be resolved before further testing."*
* **[Prediction Failure Intercept]**: If client prediction fails to reconcile with server truth: *"The rollback mechanism failed to reconcile the position of [Entity] during [Condition]. This indicates an insufficient prediction window. Should we increase the buffer or refine reconciliation logic?"*

## 5. Strategic Imperative

**Treat "Network Unreliability" as the baseline reality.** Never assume a stable connection; if high-severity failures occur under extreme conditions, they MUST be addressed before multiplayer release is considered viable.
