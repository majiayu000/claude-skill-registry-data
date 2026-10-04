---
name: sflow-import
description: Import an agent skill, artifact template, agent, or generated-artifact source from a public link or a trusted marketplace after the person reviews its exact content and hash.
disable-model-invocation: true
argument-hint: "[preview LINK|market:ID/ENTRY --as skill|template|agent | add ... --sha256 HASH | list | check | remove IMPORT]"

---
# Import skills, templates and agents from a link

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Preview first: `singularity-flow import preview <LINK> --as skill|template|agent --json`. Show the
   source, `sha256`, size, warnings and the full `text`. Ask what it is for: which agent and steps for a
   skill, which steps for a template. Never supply these yourself.
2. Add only the reviewed bytes, with the person's words for agent, ID and steps:
   `singularity-flow import add <LINK> --as <KIND> [--agent AGENT] [--id ID] [--phases A,B] --sha256 <HASH> --propose --json`.
   Use `--replace` only when the person asks to update an existing import; `--without-defaults` only
   when they say the imported agent must not take over steps.
3. Generated sources are rows, not content: `singularity-flow import add --as generated --agent A --id ID --url-template URL --phase P --target artifacts/P/F.md --propose --json`.
4. `singularity-flow imports --json` lists imports; `singularity-flow imports check --json` re-reads sources
   and gives the exact update command; `singularity-flow imports remove <IMPORT> --propose --json` removes one.

Marketplaces: `singularity-flow marketplace browse <ID> --json` lists entries; preview and add
`market:<ID>/<ENTRY>` like a link. MCP: `singularity-flow mcp sources <SERVER> --json` refuses with what would
run; add `--launch` only after the person allows it, then preview `mcp:<SERVER>/prompt|resource|tool/<NAME>`. Trust a new one (`singularity-flow marketplace add <ID> --index <URL> --propose --json`)
only when the person asks.

Never edit `singularity/imports.lock.yml`, `singularity/agents.lock.yml` or vendored files by hand, fetch the link
yourself, or add content the person has not seen. A refusal ends the turn: relay it.
