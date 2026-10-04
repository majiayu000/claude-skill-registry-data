---
name: propose-kb-node
description: The nothing-fits path for the KB router. When search-kb returns unmatched (a piece of work has no home in the knowledge base), research the gap, draft a properly-shaped node at the right level (new domain, capability, or functionality) following the shelf template and functionality baseline, and emit a proposal for human review. NEVER writes to the KB — it always stops at a review checkpoint; only an approved proposal is written and re-indexed. Use when search-kb reports unmatched, or when a play hits work the model does not yet cover.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Bash, Read, WebSearch, WebFetch
---

# propose-kb-node

The escalation behind `search-kb`. Runs when routing comes back **unmatched** — the
work has no home in the KB. It proposes a new node for the user to review. It does
**not** change the KB.

## Inputs

- `work` — the piece of work that did not route.
- (optional) the weak hints `search-kb` returned (nearest domains/capabilities).

## Procedure

1. **Confirm the gap.** Run `python3 {KB}/kb.py domains` and reason: does the work
   truly fit nowhere, or is it a missing **functionality** under an existing
   capability, a missing **capability** under an existing domain, or a missing whole
   **domain**? Pick the *smallest* level that closes the gap — prefer adding a
   functionality/capability to an existing shelf over inventing a domain.
   - `KB = core/components/memory/knowledge/domains/.pageindex`

2. **Research.** Use WebSearch/WebFetch to ground the draft in real practice — the
   genuine capabilities/functionalities and vocabulary of that area. Capture 2–4
   sources. Do not invent from thin air.

3. **Draft to the template.** Write the node in the locked shelf shape:
   - new **functionality**: `name — what it is`, a maturity ladder OR flat list, and
     a decisive profile condition (`shape.*`/`nfr.*`/`compliance`, or "the floor").
   - new **capability**: the capability + its functionalities (same baseline).
   - new **domain**: a full shelf — stance, "Intents this domain captures", and
     `## Capabilities` with functionalities — matching the existing shelves and the
     functionality baseline.

4. **Emit a proposal** (shape below) and **STOP at review.** Present it to the user.
   Only after explicit approval does a separate write step add it to the KB and run
   `kb.py rebuild`. Until then nothing is written.

## Output — kb_proposal

```yaml
kb_proposal:
  work: "let users file support tickets and live-chat with an agent"
  gap: "no existing domain covers customer support / helpdesk; nearest (notifications,
        collaboration) only touch messaging, not ticketing or agent workflows"
  level: new-domain            # new-domain | new-capability | new-functionality
  parent: null                 # null for new-domain; else <domain> or <domain>.<capability>
  proposed:
    name: support
    title: "Support: how we build it"
    trigger: "the product handles inbound user issues — tickets, live chat, help center"
    draft: |
      <markdown of the proposed node, in the shelf shape — abbreviated is fine>
  sources:
    - "<url or note from research>"
  status: "PROPOSED — awaiting user review; NOT written to the KB"
```

Emit it as JSON. It must validate against `.pageindex/validate_proposal.py`.

## Rules

- **Never write to the KB or rebuild without explicit approval.** Always stop at the
  review checkpoint.
- **Smallest level that fits.** Don't invent a domain when a capability or
  functionality on an existing shelf closes the gap.
- **Ground in research.** Cite sources; follow the shelf template + functionality
  baseline so an approved proposal drops in cleanly.
- **State the gap plainly** — why the existing model didn't cover it.
