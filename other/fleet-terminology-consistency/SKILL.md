---
name: fleet-terminology-consistency
description: How the technical writer maintains consistent terminology across all documentation surfaces — the glossary discipline that prevents confusion when 10 agents use different words for the same thing.
---

# Terminology Consistency — Writer's Glossary Discipline

10 agents writing independently will invent different names for the same thing. The architect says "contribution model." The PM says "synergy system." The engineer says "input from other agents." The PO says "cross-agent collaboration." They're all describing the same mechanism — but readers don't know that.

Your job: ONE term per concept, used consistently everywhere.

## The Fleet's Established Terminology

These terms are defined. Use them exactly:

| Concept | Correct Term | NOT This |
|---------|-------------|----------|
| The 30s brain loop | orchestrator cycle | brain loop, main loop, tick |
| Per-agent periodic check | heartbeat | ping, check-in, status poll |
| Agent not working | IDLE / SLEEPING / OFFLINE | inactive, dormant, stopped |
| Cross-agent input | contribution | input, feedback, help, assist |
| Contribution type | design_input, qa_test_definition, etc. | design feedback, test plan, security notes |
| Task progress tracking | readiness (0-100%) | progress, completion, status percentage |
| Thinking phases | methodology stages | workflow phases, process steps |
| Stage names | conversation, analysis, investigation, reasoning, work | discuss, research, explore, plan, implement |
| Quality maturity | delivery phase (poc/mvp/staging/production) | environment, tier, level |
| PO gate at 90% | gate request | checkpoint, approval request, sign-off |
| fleet-ops review | approval (approved/rejected) | sign-off, thumbs-up, LGTM |
| Agent group task | group call | batch operation, macro, workflow |
| Event propagation | chain (EventChain + ChainRunner) | pipeline, workflow, sequence |
| Board data store | board memory | board notes, board state, shared memory |
| Immune system signal | detection (Doctor detects) | alert, warning, error |
| Immune system response | teaching lesson | correction, warning, feedback |
| Agent punishment | session prune | kill, restart, reset |
| Budget pace control | fleet mode (full-speed/normal/conservative/...) | throttle, speed, tempo setting |

## Consistency Checks

### When Writing Documentation

Before publishing, verify:
1. Search your document for each "NOT This" term — replace with the correct one
2. Check that the first use of a technical term links to its definition
3. Verify agent names use the exact format: `software-engineer`, not "the engineer" or "SE"

### When Reviewing Others' Work

During staleness scan or doc review, check:
1. Do task comments use consistent terms?
2. Do PR descriptions use the established vocabulary?
3. Do board memory entries use correct terminology?

Flag inconsistencies: `fleet_chat("Doc inconsistency: {document} uses 'workflow phases' — should be 'methodology stages'", mention="project-manager")`

### When New Concepts Appear

When the fleet creates something new that doesn't have a name:
1. Check if an existing term covers it
2. If truly new: propose a term to PO
3. PO approves → add to the glossary
4. Update all documents that reference the concept

Never let two terms coexist for the same concept. Pick one. Use it everywhere.

## Documentation Surface Consistency

Terms must be consistent ACROSS surfaces:

| Surface | Where Terms Appear |
|---------|-------------------|
| CLAUDE.md | Role rules reference methodology stages, contribution types |
| TOOLS.md | Tool descriptions use chain terminology |
| HEARTBEAT.md | Action protocol uses stage names, fleet modes |
| AGENTS.md | Colleague descriptions use contribution types |
| Board memory | Trail events use established event names |
| IRC messages | Agent communications use consistent vocabulary |
| Plane pages | Issue descriptions use phase terminology |
| PR descriptions | Commit messages use type(scope) with consistent scopes |

If CLAUDE.md says "methodology stage" but HEARTBEAT.md says "workflow phase," the agent receives contradictory signals. Consistency across the 7-position directive chain matters.

## The Living Glossary

As the fleet evolves, new terms emerge. Maintain the glossary by:
1. Reading new design docs for introduced terminology
2. Checking if new skills introduce new terms
3. Verifying new heartbeat templates use established vocabulary
4. Flagging when the same concept gets different names in different documents

The glossary isn't a document you write once — it's a discipline you maintain.
