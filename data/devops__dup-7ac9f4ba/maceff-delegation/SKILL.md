---
name: maceff-delegation
description: Use when preparing to delegate to MacEff subagents. Read policies to discover current delegation patterns through timeless questions that extract details without prescribing answers.
allowed-tools: Read, Task
---

Prepare effective delegation to MacEff subagents by reading policy to understand current delegation architecture and constraints.

---

## Policy Engagement Protocol

**Read MacEff framework policies to understand delegation patterns**:

1. Delegation guidelines - Complete delegation architecture:
   ```bash
   macf_tools policy navigate delegation_guidelines
   macf_tools policy read delegation_guidelines --from-nav-boundary
   ```

2. Subagent definition - Reading-list patterns:
   ```bash
   macf_tools policy navigate subagent_definition
   ```
   Scan for sections about specialist capabilities and constraints. Read those sections.

**Why CLI tools**: Caching prevents redundant reads, line numbers enable precise citations.

---

## Questions to Extract from Policy Reading

After reading policies, extract answers to:

1. **Delegation Decision Framework** - What determines when delegation is appropriate vs inappropriate?
2. **Information Architecture** - What information must specialists receive? How should it be provided?
3. **Authority Mechanisms** - How are decision-making permissions handled?
4. **Deliverables Structure** - What artifacts do specialists produce? Where?
5. **Success Definition** - How should completion criteria be specified?
6. **Constraint Communication** - What limitations must specialists understand?
7. **Execution Architecture** - What are the specialist capabilities and limitations?
8. **Validation Protocols** - How should results be verified post-delegation?

---

## Execution

Apply patterns discovered from policy reading to current delegation context.

---

## Critical Meta-Pattern

**Policy as API**: This skill uses `macf_tools policy` CLI commands for reading policies. CLI tools handle framework path resolution, provide caching, and output line numbers for citations.
