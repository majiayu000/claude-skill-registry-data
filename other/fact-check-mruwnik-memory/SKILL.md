---
name: fact-check
description: Verify factual claims through web research. Use when you need to fact-check a statement, verify information from a source, research a question, or find the canonical link for something. Runs memory's prebuilt fact-check agent and waits for its verdict.
---

# Fact Checker

Fact-checks run on memory's prebuilt `fact-check` agent (web search and fetch, a cited verdict), paid with the user's own provider key. It needs the `agents` scope.

1. Get the claim, plus where the user saw it if they know. Say what is asked: `Verify:` for a claim, `Research:` for an overview, `Link:` for the canonical link.
2. Start it:

   ```
   agent_run(input="Verify: <claim>\nSource: <url or 'not provided'>", agent="fact-check")
   ```

3. Tell the user the `run_id`, then call `agent_wait(run_id=..., wait=300)`. It returns as soon as the run writes a new step, not only when it finishes: re-call with the last step's `seq` as `after_seq` while `run.status` is `pending` or `running`.
4. On `done`, report `run.result.data`: the `verdict` (`confirmed`, `refuted`, `partly`, `uncertain` or `n/a`), the `summary`, the `sources`, and any `follow_up`. Otherwise report `run.error`.

For a thorough, multi-angle investigation, use the `deep-dive` or `investigation-team` skills in this session instead: they need subagents, which a server-side run doesn't have.

Past fact-checks: `agent_list_runs(agent="fact-check")`.
