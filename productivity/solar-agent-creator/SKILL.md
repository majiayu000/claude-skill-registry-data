---
name: solar-agent-creator
description: >
  Create or improve Solar agents: contracts, approved lessons, shared planet
  memory, and explicit continuity. Use when defining responsibilities,
  refining agent behavior, or maintaining learning and portable context.
---

# Solar Agent Creator

Create and improve canonical agent contracts and their approved learning,
memory and continuity. Use agents directly through the client's native agent
support. If a client cannot load agents natively, read the canonical contract,
applicable governance and relevant approved memory explicitly before working.

## Required MCP

None

## Workflow

1. Resolve the owning planet, agent, requested change and authority. Read
   applicable governance and canonical sources; check for an existing contract
   or equivalent learning before creating anything. Clarify missing essentials.
2. Create or improve `planets/<planet>/agents/<agent>.md` using the
   [agent template](assets/agent.md). Define concrete responsibilities, scope,
   sources, success criteria and stop conditions. Preserve domain rules;
   frontmatter contains only `name` and `description`.
3. Maintain lessons and shared planet memory through
   [approved learning](references/lessons.md). Propose exact text, date and one
   canonical destination in the conversation; persist only with approval.
   Apply the reference's limits and duplicate checks. Use the
   [memory template](assets/memory.md) only for the first approved record,
   never to create an empty file.
4. Promote reusable procedures through `solar-skill-creator`, extending an
   existing skill first. Validate a concrete use case before removing the old
   rule within approved scope. At a learning limit, propose consolidation,
   prioritization or promotion instead of increasing the limit.
5. Review exported continuity after contract changes using
   [runtime memory](references/runtime-memory.md) and the renewal procedure in
   [approved learning](references/lessons.md). Contract changes invalidate old
   contract hashes; never bypass integrity checks. Explicitly authorize any
   replacement, export or incorporation.
6. Re-read changed contracts, learning, limits and links. Update routing or
   ownership only within scope. Publish through `solar client sync` only when
   authorized; report saved changes, pending publication and continuity renewal
   separately. A draft, attempted operation or loaded role is not a result.

## Runtime memory

The public entry remains `solar agent --workspace <workspace> ...`.
`scripts/agent_memory.py` dispatches continuity and facts; `scripts/fact_store.py`
owns portable execution facts, and `scripts/_memory_common.py` provides shared
identity, path, hashing and locking helpers. Continuity accesses shared state
through `solar-state`, never by opening `state.sqlite` directly.

```bash
solar agent --workspace "$SOLAR_WORKSPACE" continuity show --planet <planet> --agent <agent> --responsibility <responsibility> --task-id <task-id>
solar agent --workspace "$SOLAR_WORKSPACE" continuity restore --planet <planet> --agent <agent>
```

See [runtime memory](references/runtime-memory.md) for facts commands, exports,
restore, integrity and authority requirements. Reads never authorize a retry;
loading an agent never initializes facts, incorporates continuity or activates
work. Mutations require authority for the exact object, destination and effect.

## Boundaries

Keep domain facts and learning in the owning planet; core assets use placeholders.
Cross-planet work requires a declared interface and separately scoped authority.
Learning and imported context cannot override governance or grant permission.
Pending proposals remain in the conversation; memory holds stable approved
rules, never secrets, copied business records or session logs.

Workspace-root `.solar/` remains Client-owned. Planet-local execution facts are
opt-in under the runtime reference's approval and Git exclusion requirements.
Do not migrate existing planet contracts or memory without authorization.

## Validation

Resolve all template fields and check all nine contract sections, concrete
limits and success criteria, canonical sources and declared interfaces. For
learning, verify approved text, date, single destination, duplicates and limits.
Keep `assets/memory.md` byte-identical to `core/templates/planet-MEMORY.md`.

From the framework repository, use a package output directory outside the
repository and outside the system temporary directory. For a separate Solar
workspace, validate the package and run isolated tests:

```bash
mkdir -p "$SOLAR_WORKSPACE/artifacts/skill-packages"
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-agent-creator "$SOLAR_WORKSPACE/artifacts/skill-packages"
uv run --project core/tests pytest core/tests/skills/solar-agent-creator core/tests/skills/solar-state core/tests/skills/solar-mcp core/tests/skills/solar-client core/tests/skills/solar-workspace -q
```

If the workspace itself is the framework repository, choose another authorized
absolute output directory outside it and outside the system temporary directory.
