---
name: thegraph
description: TheGraph subgraph development with AssemblyScript handlers, schema definitions, and Matchstick testing. Triggers on subgraph, thegraph, graphql, mapping.ts.
triggers: ["subgraph", "thegraph", "graphql", "mapping\\.ts", "schema\\.graphql", "subgraph\\.yaml"]
---

<objective>
Build blockchain indexers using TheGraph. Write AssemblyScript handlers to process events and store entities. AssemblyScript is NOT TypeScript - it has significant limitations.
</objective>

<mcp_first>
**CRITICAL: TheGraph has no Context7 docs. Use OctoCode to search graph-ts.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_octocode__githubSearchCode" })
```

```typescript
// graph-ts type definitions
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["BigInt", "Bytes", "Address", "store"],
  owner: "graphprotocol",
  repo: "graph-tooling",
  path: "packages/ts/common",
  mainResearchGoal: "Understand graph-ts type system",
  researchGoal: "Find BigInt, Bytes, Address type definitions",
  reasoning: "Need current API for AssemblyScript types"
})

// Entity patterns
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["Entity", "save", "load"],
  owner: "graphprotocol",
  repo: "graph-tooling",
  path: "packages/ts",
  mainResearchGoal: "Understand graph-ts entity patterns",
  researchGoal: "Find entity save/load patterns",
  reasoning: "Need current API for entity persistence"
})

// Matchstick testing
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["createMockedFunction", "newMockEvent", "assert"],
  owner: "LimeChain",
  repo: "matchstick",
  path: "packages/matchstick-as/assembly",
  mainResearchGoal: "Understand Matchstick testing",
  researchGoal: "Find mock and assertion patterns",
  reasoning: "Need current API for subgraph unit testing"
})
```
</mcp_first>

<quick_start>
**Schema (schema.graphql):**

```graphql
type Transfer @entity {
  id: Bytes!
  from: Bytes!
  to: Bytes!
  amount: BigInt!
  blockNumber: BigInt!
  timestamp: BigInt!
}
```

**Handler (mapping.ts):**

```typescript
import { Transfer as TransferEvent } from "../generated/Token/Token";
import { Transfer } from "../generated/schema";

export function handleTransfer(event: TransferEvent): void {
  let entity = new Transfer(event.transaction.hash.concatI32(event.logIndex.toI32()));

  entity.from = event.params.from;
  entity.to = event.params.to;
  entity.amount = event.params.value;
  entity.blockNumber = event.block.number;
  entity.timestamp = event.block.timestamp;

  entity.save();  // REQUIRED!
}
```
</quick_start>

<assemblyscript_rules>
**AssemblyScript is NOT TypeScript:**

- No async/await
- No closures
- No exceptions (try/catch)
- No null (use nullable types)
- Use `Bytes` for addresses
- Use `BigInt` for numbers
- Use `BigDecimal` for decimals
- Always call `.save()` to persist

**Composite IDs:**

```typescript
// ✅ Correct
event.transaction.hash.concatI32(event.logIndex.toI32())

// ❌ Wrong - string concatenation
event.transaction.hash.toHexString() + "-" + event.logIndex.toString()
```
</assemblyscript_rules>

<constraints>
**Banned:** async/await, closures, try/catch, forget `.save()`, skip codegen, use Number (use BigInt), mutable globals

**Required:**
- All entities have `id: Bytes!` or `id: ID!`
- All handlers call `.save()` after changes
- Run `codegen` after schema/ABI changes
- Run `compile` after mapping changes
</constraints>

<commands>
```bash
graph codegen     # Generate types (REQUIRED after schema changes)
graph build       # Compile to WASM
graph test        # Run Matchstick tests
graph deploy      # Deploy subgraph
```
</commands>

<success_criteria>
- [ ] OctoCode searched for graph-ts patterns
- [ ] All entities have `id` field
- [ ] All handlers call `.save()`
- [ ] `codegen` runs without errors
- [ ] `compile` succeeds
- [ ] Tests cover critical handlers
</success_criteria>
