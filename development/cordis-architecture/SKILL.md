---
name: cordis-architecture
type: reference
description: Reference for Cordis meta-framework architecture, spatiotemporal composability, revertible effects, reactive coeffects, dynamic composition calculus, and component lifecycles. ALWAYS read before designing, implementing, or refactoring dynamic plugin systems, agent harnesses, or extensible architectures.
---

Source: https://github.com/cordiverse/paper/blob/main/paper.pdf

Architecture and design principles for spatiotemporal composability from the Cordis meta-framework. Cordis formalizes and implements dynamic software composition—loading, unloading, and reconfiguring components at runtime—by lifting effect and coeffect theory to runtime mechanisms.

### Core Premise

Dynamic composition requires managing software along two orthogonal dimensions:

- **Temporal composability (Time)**: When removing a component, every modification (resource allocation, event listener, state mutation) made to the shared environment must be completely and safely reversed.
- **Spatial composability (Space)**: Components must declare, discover, and resolve inter-component dependencies reactively, coordinating lifecycles when dependencies appear, disappear, or change identity.

Classical systems use coarse-grained workarounds (process restarts, container redeploys) that discard process-local state (caches, connections, in-flight tasks). Cordis manages effects and dependencies at fine granularity within a single address space.

---

### Theoretical Foundations

#### 1. Revertible Effects (Temporal Dimension)

- **Effect Context ($\partial\Gamma$)**: An effect context $\partial\Gamma \coloneqq \Gamma \times (\Gamma \to \Gamma)$ pairs current state $\gamma$ with an accumulator $\varphi$ (the composite of inverses).
- **Twisted Composition ($\mathfrak{T}_\Gamma$)**: Inverses compose in reverse order: $$(f_1, g_1) \circ (f_2, g_2) \coloneqq (f_1 \circ f_2, g_2 \circ g_1)$$
- **Tracking & Recovery**:
  - $\operatorname{track}_\Gamma(f, g) \coloneqq (\gamma, \varphi) \mapsto (f(\gamma), \varphi \circ g)$
  - $\operatorname{recover}_\Gamma(\gamma, \varphi) \coloneqq (\varphi(\gamma), \operatorname{id}_\Gamma)$
  - **Soundness Invariant**: Applying the accumulated inverse recovers the prior state up to the paper's observational equivalence ($\simeq$). The inverse witness is an obligation on the component; the runtime does not verify it.
- **Effect Functions ($\mathfrak{E}_\Gamma$)**: An effect function $e: \Gamma \to \Gamma \times (\Gamma \to \Gamma)$ returns its state-specific inverse alongside the modified state.
- **Effect Composition ($\diamond$)**: $$f \diamond g \coloneqq \gamma \mapsto \operatorname{let}\; (\delta, s) = g(\gamma) \;\operatorname{in}\; \operatorname{let}\; (\varepsilon, t) = f(\delta) \;\operatorname{in}\; (\varepsilon, s \circ t)$$
- **Effect Independence**: Effects $e_1, e_2$ are independent when their generated transformation monoids $\mathfrak{M}(e_1)$ and $\mathfrak{M}(e_2)$ commute and neither disturbs the inverse yielded by the other. This allows withdrawing an effect from an interleaved execution without side-effect leaks.

#### 2. Reactive Coeffects (Spatial Dimension)

- **Coeffect Specification ($d$) & Provision ($p$)**: Components declare required keys ($d \subseteq K$) and provided keys ($p \subseteq K$).
- **Two-Layer Resolution**: $k \mapsto \rho(k) \mapsto \sigma(\rho(k))$
  - `@@store` ($\sigma$): Value store mapping realm symbols to typed values.
  - `@@isolate` ($\rho$): Realm table mapping coeffect keys to realm symbols.
  - `@@intercept` ($\iota$): Interception table mapping keys to metadata.
- **Reactive Notification**: Context changes are classified against component specifications as **activating**, **deactivating**, or **neutral**.
- **Scoped Isolation (`isolate`) & Interception (`intercept`)**: Contexts structurally inherit tables from parents. Modifying isolation or interception creates child context scopes without mutating ancestor environments.

#### 3. Unified Context Paradigm

- The context `ctx` is a first-class runtime entity ($\Gamma^\infty$) unifying effect tracking and coeffect resolution.
- **Observational Equivalence ($\simeq$)**: Operations on disjoint or commutative keys commute, guaranteeing that runtime dynamic operations yield normal forms equivalent to static assembly.

---

### Calculus of Dynamic Composition

A running system is modeled as a set of **fibers** in a registry $F_\gamma$. Each fiber is a tuple $\langle d, p, e, \pi, \sigma, \tau, \theta \rangle$:

- $d$: Declared coeffects (dependencies).
- $p$: Provided coeffects.
- $e$: Applied effect function / iterator.
- $\pi$: Parent fiber identifier (forming a hierarchy rooted at $\text{root}$).
- $\sigma$: Private coeffect table.
- $\tau$: Administrative retirement flag ($\top$ or $\bot$).
- $\theta$: Lifecycle state machine.

#### Lifecycle States & Transitions

```
                [L-Begin] (target != ⊥)
   INACTIVE(⊥) --------------------------> RELOADING / LOADING
       ^                                      |            |
       |                               [L-Finish]      [L-Divert / L-Raise]
   [L-Unload]                                 |            |
   (guarded)                                  v            v
       |                                   ACTIVE ----> UNLOADING
       +-----------------------------------------------+ [L-Leave]
```

1. **Orchestration Rules**:
   - `O-Insert`: Registers a new fiber in $F_\gamma$ in state $\text{Inactive}(\bot)$.
   - `O-Retire`: Sets retirement flag $\tau_n \leftarrow \top$, forcing target view to $\bot$.
   - `O-Remove`: Removes an inactive, unreferenced fiber from $F_\gamma$.
2. **Activation Rules**:
   - `L-Begin`: Starts transition from $\text{Inactive}(\bot)$ to $\text{Reloading}$ when $\text{target}_n \neq \bot$.
   - `L-Iter`: Advances an iteration step of effect iterator $i$, accumulating inverse $h$.
   - `L-Finish`: Completes iterations, moves fiber to $\text{Active}$ with committed view $\omega$.
3. **Interruption & Failure Rules**:
   - `L-Divert`: Triggered when the target view shifts during a transition. It either aborts or lands the in-flight iteration, then routes to $\text{Unloading}$; the inertial implementation lands the iteration.
   - `L-Raise`: Triggered on effect execution failure; routes to $\text{Unloading}(\xi)$ to execute accumulated inverses before resting at $\text{Inactive}(\xi)$.
4. **Deactivation Rules**:
   - `L-Leave`: When target view shifts away from committed $\omega$, transitions from $\text{Active}$ to $\text{Unloading}$ (marking component out of service before teardown).
   - `L-Unload`: Runs accumulator $g$, recovers all installed effects in LIFO order, and transitions to $\text{Inactive}$. **Guard**: Defers unload until all dependent fibers have finished deactivating.

#### Metatheoretic Guarantees

- **Preservation**: Registry well-formedness (disjoint provisions, valid trees, total committed views) is preserved across all transitions.
- **Recovery Exactness (Terminal Recovery)**: Under pairwise independence, an acyclic precedence relation, and the paper's other hypotheses, running a fiber's accumulator removes that fiber's contribution and recovers the environment up to observational equivalence. Terminal recovery does not promise to undo external emissions.
- **Coeffect Ordering**: Providers strictly outlive dependents ($b_{\text{provider}} < b_{\text{dependent}}$ and $u_{\text{dependent}} < u_{\text{provider}}$). Dependents never observe half-torn-down providers.
- **Resolution Coherence**: A transition executes against a single consistent resolution view $\omega$; any dependency shift immediately triggers safe deactivation.
- **Progress**: The lifecycle is deadlock-free and terminates in finite steps when dependency precedence $\prec$ is acyclic.
- **Confluence**: Under pairwise independence, totality on provisions, acyclic precedence, no failed fibers, and the paper's well-formedness conditions, lifecycle schedules reach equivalent quiescent states matching a from-scratch static assembly. The theorem concerns lifecycle state, not emissions.

---

### Meta-Framework Implementation Architecture

```
+-------------------------------------------------------------+
|               Application Tier (e.g. Koishi)               |
|         Domain Vocabulary, Services, Plugins, Console       |
+-------------------------------------------------------------+
|                    Component Loader                         |
|   Declarative Config Tree | Incremental Reconciliation | HMR|
+-------------------------------------------------------------+
|                      Core Library                           |
|   ctx.effect | ctx.use | ctx.get/set | Proxy Access | Fibers|
+-------------------------------------------------------------+
```

#### 1. Core Library Primitives

- **`ctx.effect(callback)`**:
  - Executes an effect function or generator.
  - Returns a self-disposal closure with an `armed` guard ensuring at most one recovery execution.
  - Automatically prepends the inverse to `ctx.dispose` (LIFO ordering).
- **`ctx.set(key, value)` & `ctx.get(key)`**:
  - `ctx.set` wraps binding mutation in `ctx.effect`, notifying dependents on both install and dispose.
  - `ctx.get` resolves $k \to \rho(k) \to \sigma(\rho(k))$.
- **`ctx.use(component, config)`**:
  - Instantiates a component into a `Fiber`.
  - Attaches child lifecycle to parent context via `ctx.effect(callback)`.
  - Disposing parent automatically tears down all child fibers.
- **`ctx.isolate(key, realm)` & `ctx.intercept(key, metadata)`**:
  - Derives child context branch with scoped realm table or interception metadata.
- **Proxy-Mediated Access (`ctx[key]`)**:
  - Enforces dependency contracts at property access time.
  - Resolves against `fiber.committed` view.
  - Throws `INACTIVE_ACCESS` if accessed while dependency is inactive.
  - Throws `UNDECLARED_ACCESS` if key is not declared in component injection metadata (`inject`).

#### 2. Component Loader & Declarative Configuration

- **Configuration Tree Entry**:
  - `id`: Stable identifier for keyed diffing.
  - `url`: Module specifier/path.
  - `config`: Component configuration payload.
  - `isolate`: Scoped isolation flags (`true` for local realm, string for named realm).
  - `intercept`: Interception rules.
  - `disabled`: Administrative toggle.
- **Incremental Reconciliation**:
  - Diffing tree modifications and applying targeted operations (`config` update, `isolate` patch, or reload) without tearing down unrelated branches.
  - Grouping via `@cordisjs/group` and file inclusion via `@cordisjs/include`.
- **Managed Isolation Realms (Delimiters $\delta_k$)**:
  - Unique tag per key inherited down the context hierarchy to track context derivation and seamlessly migrate bindings when entries move.
- **Hot Module Replacement (HMR)**: The paper describes this as the `@cordisjs/hmr` component.
  1. _Classification_: Fixed-point propagation marking changed modules as accepted/declined.
  2. _Stale Detection_: Finds affected component entries whose import graphs reach accepted changes.
  3. _Transactional Reload_: Disposes stale fibers, invalidates module cache with rollback backup, and imports fresh component modules. Restores backup if re-import fails.

---

### Practical Architectural Guidelines

1. **Effect Hygiene & Revertibility**:
   - Every tracked stateful mutation must yield an inverse that restores the prior state up to the required equivalence. The runtime does not prove this property.
   - Wrap reversible acquisitions (event listeners, timers, server listeners, database handles) in `ctx.effect`. Treat irreversible emissions, such as sent packets or printed output, as outside the tracked boundary.
2. **Distinguish Acquisitions vs Emissions**:
   - _Acquisitions_ (internal state, registrations, connections) belong inside context tracking.
   - _Emissions_ (sending a network packet, printing a log, writing a terminal line) cross the system boundary and cannot be undone; do not attempt artificial inversion.
3. **Declare Dependencies Explicitly**:
   - Always declare consumed services in `inject` / coeffect specifications.
   - Never access global singletons or bypass context proxy resolution.
4. **Preserve Acyclic Precedence ($\prec$)**:
   - Ensure service dependencies form a directed acyclic graph (DAG).
   - Resolve circular dependencies by decoupling interfaces or using event-driven messaging. The paper's progress and confluence results require an acyclic precedence relation.
5. **Scoped Isolation for Service Multiplexing**:
   - Use `ctx.isolate` when running multiple instances of a service (e.g., multiple bot accounts, separate database connections) within the same process.
6. **Per-Fiber Failure Containment**:
   - Component failures route through `UNLOADING` to `INACTIVE(error)` after recovering accumulated effects. The failed fiber does not retry automatically, does not block siblings, and does not propagate the failure to its parent.
   - Design components to degrade gracefully when optional coeffects are absent.
