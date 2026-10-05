---
name: prior-art
description: |
  SOP for locating, auditing, and importing production-tested reference patterns and peer-reviewed literature.
  Trigger when:
  - Designing or implementing non-trivial algorithms, system protocols, design patterns, or major library integrations.
  - Prompt contains: prior art, reference implementation, research patterns, standard implementation, arXiv, RFC.
---

# Prior Art & Reference Patterns Skill

**Search → Audit → Adapt → Clean**

This skill is **the procedure the ambient Outward-Search Reflex invokes** ([ambient.md](../../ambient.md) §"Outward-Search Reflex"). The mandate is ambient — every walker that reaches a design fork, a missing fact, or a non-trivial pattern runs this procedure before halting. The skill documents the *how*: tiered search, shallow-clone workspace hygiene, ≥2-reference grounding, and cleanup before every commit.

> **Adversarial path anchor.** This lens is also invoked on the Verification Dual's adversarial path ([rules.md](../../rules.md) §2 Invariant 1): the Dual's thesis — externalize correctness, never trust the generator's confidence — applies to external knowledge. Internal confidence is not evidence; a context-free search in decorrelated sources (production code, RFCs, literature) closes the condition where no deterministic evaluator exists.

---

## 1. Search Hierarchy Directive

When addressing a non-trivial architectural or algorithmic task, you must systematically search for existing work using the following priority tiers:

```mermaid
graph TD
    A["Start Search Walk"] --> B{"Tier 1: Production Code Available & Permissive?"}
    B -- "Yes" --> C["Audit Code & Extract Invariants (MIT/Apache-2.0)"]
    B -- "No / Restricted (GPL)" --> D{"Tier 2: Official Standards / RFCs Available?"}
    D -- "Yes" --> E["Map Normative Protocol Constraints from Specification"]
    D -- "No" --> F{"Tier 3: Academic Papers / Formal Specifications (arXiv, TLA+)?"}
    F -- "Yes" --> G["Extract Mathematical Theorems & State Transitions"]
    F -- "No" --> H["Halt Sequence: Insufficient Constraints to Warop IBC"]
```

### Tier 1: Production-Grade Code (Permissively Licensed)
- Search for active open-source projects on GitHub that implement the pattern or algorithm.
- Look for high maintenance signals: active commits, issues resolved, star density, and test suite coverage.
- Confirm permissive licensing (e.g., MIT, Apache 2.0, BSD-3-Clause). Do not read copy-restricted code (e.g., GPL, AGPL, proprietary) to avoid licensing contamination.

### Tier 2: Official Standards & RFCs
- If no permissive implementation exists, locate the defining standard (e.g., IETF RFCs, W3C specifications, IEEE standards).
- Extract normative constraints using BCP 14/RFC 2119 keywords (`MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `MAY`, `OPTIONAL`).

### Tier 3: Academic Literature & Formal Models
- If no standard exists, search peer-reviewed research repositories (arXiv, ACM Digital Library, IEEE Xplore) or formal specification repos (e.g., TLA+ specifications, Alloy models).
- Extract proven liveness and safety invariants, pseudocode transition rules, and state machine constraints.

### The Termination Gate
If no verified prior art, standard, or literature can be located for a highly complex algorithm, you **MUST halt** and transition to manual clarification. Greenfield sequence walks without empirical or mathematical groundings are forbidden.

---

## 2. Git Cloning Sanity Guidelines

To inspect codebases in the wild without cluttering the local workspace, you must adhere to the following git cloning rules:

### A. Workspace Isolation
- All external clones must reside in a dedicated workspace directory named `.prior_art_cache/`.
- Cloning to directories outside the workspace (such as `/tmp/` or `/home/`) is strictly prohibited.

### B. Network & Storage Optimization
- **Shallow Clones (`--depth 1`):** Always append `--depth 1` to `git clone` to avoid downloading historical commits and large historical objects.
- **Sparse Checkouts:** If only specific files or subdirectories are needed, configure a sparse checkout to retrieve only those files.

#### Sparse Clone Template Command:
```bash
# 1. Clone without checking out files, using blobless filtering
git clone --depth 1 --filter=blob:none --sparse --no-checkout <repo_url> .prior_art_cache/<repo-name>

# 2. Configure sparse checkout paths
cd .prior_art_cache/<repo-name>
git sparse-checkout set <target-directory-or-file>

# 3. Checkout target files only
git checkout
```

### C. Cleanup Lifecycle
- **Purge Gate:** Cloned repositories are temporary staging buffers. 
- You **MUST** run `rm -rf .prior_art_cache/` before executing any commit boundary or finalizing a task. No external source code repositories may remain in the active workspace at commit boundaries.

---

## 3. Document Findings in the Active Sketch

When prior art is located and utilized, record findings in the active sketch ledger. For each source, capture: the URL or citation, the architectural/design pattern or algorithm, its key strengths, how its invariants will be adapted to the target codebase, and the license (MIT, Apache-2.0, BSD-3-Clause). For literature, record the title, DOI or arXiv/RFC identifier, the proven safety or liveness invariants extracted, and any pseudocode or state-machine parameters.

---

## 4. Invariant Auditing (The Copy-Paste Guard)

Do not copy code directly from external repositories. All extracted prior art must be audited against:
1. **Spatial Simplicity (Hickey Audit):** Enforce that the imported logic is decoupled from the external codebase's dependencies and complected abstractions.
2. **Temporal Volatility (Lowy Audit):** Ensure that the imported logic aligns with our target module's axes of change and boundaries.
