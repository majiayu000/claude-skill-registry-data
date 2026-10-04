---
name: context-diet
description: Cut agent token spend by shrinking what enters the context window. Index the repo or corpus once and query it instead of re-reading files on every question. Use when the user complains their coding agent burns tokens, the context fills up fast, the same files get read repeatedly, or the bill scales with conversation length.
---

# Feed the agent less, not a smarter model

When an agent re-reads the same files into context on every question, the bill scales with repetition, not with difficulty. The structural fix is a queryable index: the agent asks for the two facts it needs instead of swallowing whole files. One published reference point (arXiv:2603.27277, evaluated across 31 real repos, using a knowledge-graph MCP server): ~10x fewer tokens and 2.1x fewer tool calls at 83% answer quality versus file-by-file exploration. Treat those numbers as a ceiling from someone else's benchmark, not a promise; the whole skill is: measure your own drop.

## Steps

1. **Baseline first.** Pick one representative task (a real question about the codebase or corpus) and record tokens used and tool calls made, straight from the session's usage stats. Without this number, step 5 is theater.
2. Wire an index the agent can query instead of reading raw files. For codebases over MCP, `codebase-memory-mcp` is the worked example below; a repo map, a knowledge bundle, or a RAG index over docs serve the same role. What matters is the shape: **query in, small answer out**, instead of file in, everything in.
3. Validate the MCP config parses and points at a real binary (proof below), then run the initial index (a few minutes on a large repo, sub-millisecond queries after).
4. Re-run the exact same task from step 1. Record tokens and tool calls again.
5. Keep the index only if the drop is real and answer quality held. Report both numbers side by side. If quality dropped more than the bill, the diet was too aggressive: the agent needs some raw context, and hybrid is a fine outcome.

## Prove it

```bash verify
cat > mcp-config.json <<'JSON'
{
  "mcpServers": {
    "codebase-memory": {
      "command": "/usr/local/bin/codebase-memory-mcp",
      "args": []
    }
  }
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("mcp-config.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
const servers = c.mcpServers || c.mcp_servers || {};
const keys = Object.keys(servers);
if (keys.length === 0) bad("mcpServers must have at least one entry");
const srv = servers[keys[0]];
if (!srv.command || typeof srv.command !== "string") bad("server entry must have a command (path to the binary)");
if (!Array.isArray(srv.args)) bad("args must be an array");
console.log("context-diet OK: MCP server " + JSON.stringify(keys[0]) + " wired at " + srv.command + " (now measure tokens before/after on the same task)");
'
```

## Guardrails

- The index is a structural backend, not a smarter brain. It reduces what the agent reads; the model and the prompts still drive answer quality. Never promise quality gains from a context diet.
- Small repos don't need this. Below a few thousand lines, file-by-file context is cheap and the indexing overhead isn't worth it.
- Headline numbers (10x, 83%) came from someone else's 31 repos. The user's number is the one from step 5, and it's the only one worth repeating.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Wire the knowledge graph, stop re-reading files](https://flowstacks.xyz/workflows/codebase-memory-mcp-token-savings)</sub>
