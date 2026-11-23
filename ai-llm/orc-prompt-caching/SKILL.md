---
name: orc-prompt-caching
description: Configure and verify provider prompt caching in ORC nodes and composed trees, including shared delegates, model changes, concurrent users, warming and cache misses. Use for reusable prompt prefixes and inference cost; application result caches are a different mechanism.
---

# ORC prompt caching

Prompt caching reuses provider computation for a matching **cacheable prefix**, not the entire prompt, an output or a private user record. It neither skips an ORC node nor returns a previous user's answer. A different model, serving route or contract can need its own warm prefix. Node names alone are not a cache partition.

## Configure the actual loaded stack

Start with [operational checks](references/operational-checks.md) for a no-call resource/source check, an explicitly guarded model-only warm example, and allowlisted usage/ownership measurements. Companion links resolve to sibling skills bundled in this repository. Keep the collection together when copying it. A missing companion indicates an incomplete copy; it is not a requirement to install personal skills.

After declaring concrete, described blackboard inputs and outputs, an ordinary generation node can use:

```clojure
(sheet/llm "review"
  :model "anthropic/claude-haiku-5.5"
  :instruction "Review the supplied evidence under the declared assessment contract."
  :reads [:request] :writes [:assessment]
  :options {:output-mode :json-schema
            :prompt-cache? true
            :generic-tool-description? true})
```

Choose completion allowance and deadlines for the task; the example's short instruction is not a cache-eligibility demonstration. Both cache controls default off. The tool-description option removes duplicated instruction text in function mode; it does not remove field meanings. Use [model/SIO](../orc-model-sio/SKILL.md) for strict contracts, model configuration and request capture.

Released ORC `4966c8e35e3bb5939570bfc645eac52a8d18eb6e` places the marked instruction and variable data in two content parts of ONE user message. A **private, unpublished candidate** makes them two USER messages under the same existing flag. Do not claim that candidate is installed or promote the instruction into a system role. Read [cache boundaries](references/cache-boundaries.md) when diagnosing misses or adopting another revision.

## Design reuse without weakening the tree

- Inventory generation roles separately: routing, specialist work, synthesis, assessments and any researcher subcalls. Set supported options and verify the actual mode for each reached role; one cached router does not warm every delegate.
- Keep necessary stable instructions and contracts stable; keep user/work facts, volatile observations and invocation IDs in typed runtime inputs. The flag marks the instruction prefix, not every large blackboard reference. Preserve nested descriptions and provenance. Never pad production prompts merely to obtain cache hits.
- Keep disjoint parallel writes and isolated delegate blackboards. A reusable child can preserve an internal contract across callers; explicit typed exports can maintain separate parent results. Do not merge output keys or loosen schemas to manufacture a shared prefix. See [specialist composition](../orc-compose-specialists/SKILL.md).
- Warm model-only requests only when expected reuse justifies their cost. A rare specialist with a distinct prefix needs its own eligibility/warming decision. Warming must not perform or replay domain actions. Read [warming and many-user serving](references/warming-and-serving.md).
- Verify serialized request, actual provider/model, cache reads AND writes, actual cost, parsed values and canonical execution ownership. Missing counters are unknown, not zero; a marker or shorter latency proves no hit. Cache misses remain ordinary model calls subject to the same budgets and contracts.

The [qualification record](references/qualified-evidence.md) distinguishes hosted ORC/SQLite proofs, request-only controls, private source and unresolved routes. Use it before extending a claim to another provider, model, output mode or research role. No per-model application parser is part of this recipe.
