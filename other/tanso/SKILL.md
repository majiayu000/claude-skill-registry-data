---
name: tanso
description: >-
  Use Tanso, an AI Search CLI for exploring Chinese internet signals. Use when the user asks to search Chinese web sources, Zhihu, Zhihu hotlists, Bocha, Volcengine Ark, Chinese internet topics, source-backed briefs, contradiction checks, counterintuitive topic discovery, popular answers, live provider testing, or current Chinese web signals.
---

# Tanso

Use `tanso` to explore Chinese internet signals through provider APIs and return source-backed answers. Prefer `--json` for agent workflows.

## Before Running

Check availability:

```bash
tanso version
tanso config show --json
```

If `tanso` is missing and the user asked for setup, install it:

```bash
npm install -g @geekjourneyx/tanso
```

Never print `.env`, API keys, bearer tokens, raw config files, or CI secrets. Treat redacted config values as expected.

## Choose A Source

Use the narrowest source that matches the task:

| Need | Command |
| --- | --- |
| Multi-source default search | `tanso "<query>" --json --limit 5` |
| All search and answer sources | `tanso all "<query>" --json --limit 5` |
| Broad web evidence | `tanso bocha "<query>" --json --limit 5` |
| Web-grounded direct answer | `tanso volc "<query>" --json --limit 1` |
| Zhihu opinions and discussions | `tanso zhihu "<query>" --json --limit 5` |
| Zhihu-backed global web search | `tanso zhihu web "<query>" --json --limit 5` |
| Current Zhihu hotlist | `tanso zhihu hot --json` |
| Available source IDs | `tanso sources --json` |

Use Zhihu for opinion-rich questions, Bocha for broad corroboration, Volcengine for synthesized direct answers, and hotlist for current attention.
Use `tanso --help` or `tanso <command> --help` to inspect the installed command surface before assuming a command exists.

For Zhihu global search only, filters are valid:

```bash
tanso zhihu web "<query>" --filter 'host=="example.com"' --search-db realtime --json
```

## Research Workflow

1. Rewrite the user request into 2-5 concrete Chinese queries with aliases, product names, and time qualifiers when useful.
2. Start with `--limit 3` to `--limit 5`; increase only when coverage is weak.
3. Inspect `status`, `results`, `source_status`, and `errors` in JSON output.
4. Cross-check important claims across sources before presenting them as facts.
5. Separate source claims from your inference. Mention provider failures when they reduce confidence.

## Answer Shape

For research answers:

```markdown
**Conclusion**
One concise answer.

**Evidence**
- Source, title, URL, key point.
- Source, title, URL, key point.

**Assessment**
What is likely true, what is uncertain, and what to verify next.
```

For topic discovery:

```markdown
**Topic Candidates**
1. Topic: why it matters, source signal, suggested angle.
2. Topic: why it matters, source signal, suggested angle.

**Counterintuitive Point**
What contradicts common assumptions.

**Next Step**
Exact follow-up searches or validation steps.
```

## Failure Handling

| Signal | Action |
| --- | --- |
| `credential_missing` or exit `4` | Check redacted config; ask for the relevant provider key if needed. |
| Exit `2` | Remove incompatible flags and rerun the simplest valid command. |
| Exit `5` | Retry once with a smaller limit, then switch provider. |
| Exit `6` | Narrow the query and reduce `--limit`. |
| Exit `7` | Rewrite with alternate Chinese terms or broaden to Bocha/Zhihu global search. |

When one provider fails, continue with configured alternatives if the user asked for research rather than debugging.

## Guardrails

- Do not scrape browsers or websites when a Tanso provider can answer the task.
- Do not use `--filter` or `--search-db` outside `tanso zhihu web`.
- Do not treat `tanso sources --json` as proof that credentials work; `configured` only means local credential material is present.
- Do not present one provider's output as verified fact when sources conflict.
- Do not expand a narrow question into broad trend research unless the user asks for topic discovery.
