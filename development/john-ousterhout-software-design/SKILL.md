---
name: john-ousterhout-software-design
type: reference
description: Reference for Ousterhout's A Philosophy of Software Design principles. ALWAYS read before designing modules, interfaces, or abstractions, or deciding how to split or combine code.
---

Design principles from John Ousterhout's A Philosophy of Software Design. The developer's primary job is managing complexity, not writing code.

### Core Premise

- **Complexity is the root problem**: It accumulates incrementally through many small additions, each of which seems harmless on its own.
- **Strategic programming**: Invest up front in good design (~10-20% overhead) rather than tactical "get it working fast" code that accrues complexity debt.
- **Shorter is not simpler**: Fewer lines of code do not necessarily mean simpler software. Simplicity is achieved by hiding complexity behind a clean interface, not by minimizing code length.

### The Principles

- **Complexity is incremental**: Complexity is the accumulation of many small, seemingly harmless choices -> Resist complexity on every change, even small ones.
- **Strategic vs tactical programming**: Tactical programming focuses on getting features working quickly but accumulates debt -> Shift to strategic programming, investing ~10-20% overhead in good design.
- **Deep modules**: Shallow modules have interfaces nearly as complex as their implementations -> Design deep modules whose simple interfaces hide complex functionality.
- **Information hiding / information leakage**: Internal details leaked to other modules cause changes to ripple -> Hide design decisions inside the module; eliminate shared knowledge between modules.
- **General-purpose modules are deeper**: Special-purpose modules are shallow and leak details -> Design modules to be general-purpose in their interface but optimized for current needs, not speculative futures.
- **Different layer, different abstraction**: Adjacent layers with the same abstraction level signal shallow modules -> Ensure that stacked layers change their level of abstraction.
- **Pull complexity downward**: Forcing callers to handle complex details scatters complexity across the codebase -> Trap complexity inside the module so callers have a simple interface.
- **Better together OR better apart**: Splitting code too eagerly produces shallow modules; keeping unrelated code together confuses purpose -> Combine tightly coupled code; split only when modules serve unrelated purposes.
- **Comments describe the non-obvious**: Comments repeating code clutter and rot -> Write comments that capture the "why" (design decisions, constraints, rationale) instead of "what".
- **Define errors out of existence**: Exception-heavy interfaces force caller handling and scatter logic -> Design APIs that make errors impossible or mask/handle them internally.
- **Design it twice**: Committing to the first design option usually produces suboptimal, complex abstractions -> Explore at least two distinct alternative designs before writing implementation code.
- **Strategize modifications**: Patching features onto an existing design degrades it over time -> Refactor the design first so the new feature can be added cleanly.
- **Shorter is not simpler**: Minimizing lines of code often compresses logic, making it harder to read -> Focus on reducing cognitive load and hiding complexity, not line counts.
- **Consistency**: Inconsistent patterns across the codebase force readers to re-learn context -> Follow established naming, structural, and behavioral conventions.

### Module Design

- **Deep modules**: Keep interfaces simple relative to the functionality delivered. Module depth is measured as functionality delivered divided by interface complexity. Shallow modules add cognitive load without hiding complexity.
- **Information hiding**: Hide design decisions, data structures, and implementation details so they can change without affecting users. Information leakage — where details of one module are known to another — is the primary driver of change-ripple complexity.
- **Pull complexity downward**: When complexity is unavoidable, trap it inside a single deep module rather than exposing it to callers. One slightly more complex internal implementation is better than scattering handling across dozens of call sites.
- **Better together OR better apart**: Combine modules if they are tightly coupled, share information, are always used together, or are hard to understand in isolation. Split modules only when their responsibilities serve completely unrelated purposes. Err toward fewer, deeper modules, as eager splitting produces shallow modules and leaks information.
- **Different layer, different abstraction**: As control passes from one layer to another, the abstraction level must change. Pass-through forwarding methods (which merely call a method in another class with the same signature) indicate a shallow, middle-man layer and information leakage.
- **General-purpose modules**: Design modules to solve general problems, but do not generalize speculatively. General-purpose interfaces are simpler and deeper, but generality should come from pulling complexity downward, not from guessing future requirements.

### Interface Design

- **Deep interfaces**: Design interfaces to be simple to use while offering powerful behavior underneath. A clean, minimal signature should hide all coordination and implementation detail.
- **Define errors out of existence**: Exception-heavy interfaces are shallow and force callers to handle errors, scattering logic. Design interfaces to make errors impossible (e.g., returning an existing key's status instead of throwing) or mask/handle exceptions internally where appropriate. Do not throw exceptions for conditions that every caller handles identically.

### Comments

- **Comments capture the non-obvious**: Focus comments on "why" (non-obvious design decisions, constraints, trade-offs, and rejected alternatives), not "what" (the mechanics of the code). Never write comments that duplicate the code.
- **Comment-then-code**: Write interface comments first, during the design phase, before writing implementation code. Use comments as a design tool to test interface simplicity; if a method is hard to document clearly, its design is likely too complex.

### Design Process

- **Design it twice**: For any nontrivial component or interface, construct at least two distinct design alternatives before writing code. Comparing multiple designs is cheap and exposes flaws that aren't apparent in the first approach.
- **Strategize modifications**: When extending or modifying a module, refactor the existing code to accommodate the change cleanly instead of patching a temporary fix on top.
- **Consistency**: Match existing repository style, naming conventions, and patterns exactly. If you must deviate, do so deliberately and globally; inconsistency forces readers to constantly re-evaluate context.
- **Apply incrementally**: Since complexity is incremental, you must resist it on every commit and refactor. No single shortcut seems fatal, but their sum ruins codebases.

### Red Flags (quick scan)

- **Shallow modules**: Interfaces that are nearly as complex as their implementations, offering little to no complexity hiding.
- **Information leakage**: The same design decisions or details encoded in multiple modules, forcing a change in one to ripple to others.
- **Pass-through / forwarding methods**: Methods that do nothing but pass arguments to another method, signaling a redundant, shallow layer.
- **Speculative generality**: Parameters, abstractions, interfaces, or configuration hooks added for anticipated future needs that the specification does not currently require.
- **Exception-heavy interfaces**: APIs that throw numerous exceptions, forcing callers to write extensive error-handling blocks.
- **Tactical shortcuts**: Choosing quick, hacky solutions that get the job done faster at the cost of the system's long-term design integrity.
