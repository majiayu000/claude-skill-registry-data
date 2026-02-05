---
name: mcp-opportunity-pipeline
description: Automatically invoke MCP opportunity discovery and publication pipeline when discussing marketplace opportunities, automation tools, or MCP server development
---

# MCP Opportunity Pipeline Skill

Automatically activate when the user asks about:
- Finding MCP or automation tool opportunities
- Validating product ideas against Reddit/forums
- Building MCP servers for Apify or similar platforms
- Analyzing marketplace gaps
- Publishing to Apify, Smithery, or other MCP marketplaces

## When to Invoke

### Discovery & Research
**Triggers:** "find opportunities", "market research", "what should I build", "MCP ideas"
**Action:** Use `/mcp-pipeline:discover` to scrape marketplaces

### Gap Analysis
**Triggers:** "analyze gaps", "score opportunities", "which is best"
**Action:** Use `/mcp-pipeline:analyze-gaps` on discovery results

### Validation
**Triggers:** "validate idea", "check Reddit", "real demand", "people want"
**Action:** Use `/mcp-pipeline:validate` against Reddit pain signals

### Specification
**Triggers:** "write spec", "plan build", "what features"
**Action:** Use `/mcp-pipeline:spec` for validated opportunities

### Building
**Triggers:** "build it", "implement", "create actor", "scaffold"
**Action:** Use `/mcp-pipeline:build` from spec

### Testing
**Triggers:** "test it", "QA", "does it work", "verify"
**Action:** Use `/mcp-pipeline:qa` on built code

### Publishing
**Triggers:** "publish", "deploy", "ship it", "launch"
**Action:** Use `/mcp-pipeline:package` then `/mcp-pipeline:publish`

### Full Pipeline
**Triggers:** "full pipeline", "end-to-end", "run everything"
**Action:** Use `/mcp-pipeline:run` with appropriate parameters

## Pre-Check Behavior

Before running expensive operations:

1. **Check for existing outputs:**
   ```
   outputs/discover/    → Skip discover if recent data exists
   outputs/analyze/     → Skip analyze if recent analysis exists
   outputs/validate/    → Skip validate if recent validation exists
   ```

2. **Suggest incremental runs:**
   - If discovery exists but not analysis, suggest `/mcp-pipeline:analyze-gaps`
   - If validation exists but not spec, suggest `/mcp-pipeline:spec`

3. **Warn about costs:**
   - Discovery scrapes multiple sites (rate limits)
   - Validation searches Reddit (API usage)
   - Building creates deployable code

## Configuration Reference

Load from `.claude-plugin/config.json`:
- Marketplace settings
- Subreddit lists
- Scoring weights
- QA thresholds
- Publishing settings

## Output Locations

| Stage | Output Path |
|-------|------------|
| Discover | `outputs/discover/raw-opportunities-{date}.json` |
| Analyze | `outputs/analyze/gap-opportunities-{date}.json` |
| Validate | `outputs/validate/validated-opportunities-{date}.json` |
| Spec | `outputs/spec/{name}-spec.md` |
| Build | `outputs/build/{name}/` |
| QA | `outputs/qa/{name}-qa-report.json` |
| Package | `outputs/package/{name}/` |
| Publish | `outputs/publish/publication-log.json` |

## Example Conversations

### "I want to find MCP opportunities"
→ Check if recent discovery exists
→ If not, run `/mcp-pipeline:discover --phase casual`
→ Then suggest `/mcp-pipeline:analyze-gaps`

### "Which opportunity should I build?"
→ Check if analysis exists
→ Present top opportunities with scores
→ Suggest validation for top picks

### "Build the Notion sync tool"
→ Check if spec exists
→ If not, generate spec first
→ Run `/mcp-pipeline:build --name notion-sync`
→ Then run QA

### "I want to ship something to Apify this week"
→ Run full pipeline: `/mcp-pipeline:run --phase casual --target apify`
→ Stop at each stage for approval
→ End with publish (dry-run first)

## Error Recovery

| Error | Recovery |
|-------|----------|
| No discover data | Run discover first |
| Low validation scores | Pivot to different opportunity |
| QA failures | Fix issues, re-run build + QA |
| Publish failure | Check credentials, retry |

## Important Notes

- Always check existing outputs before re-running stages
- Validate ideas before building (save time)
- Use dry-run before actual publish
- Marketing posts require manual review/submission
