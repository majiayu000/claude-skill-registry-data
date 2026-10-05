---
name: get-api-docs
description: |
  Fetch accurate, up-to-date API documentation via context-hub (chub) CLI
  instead of relying on stale training data. Automatically activated when
  working with any external library, framework, or API.

  Use this skill BEFORE writing any code that uses an external library or API.
  This ensures you use current, correct APIs — not hallucinated ones.
---

# Get API Docs via context-hub (chub)

**MANDATORY RULE**: Before writing code that uses ANY external library or API,
fetch the current documentation with `chub`. Never rely on memorized API shapes.

## Pre-flight Check

Before first use in a session, verify chub is installed:

```bash
command -v chub >/dev/null 2>&1 || npm install -g @aisuite/chub
```

## Step 1 — Find the right doc ID

```bash
chub search "<library name>" --json
```

Pick the best-matching `id` from the results (e.g. `openai/chat`, `anthropic/sdk`,
`stripe/api`). If nothing matches, try a broader term.

## Step 2 — Fetch the docs

```bash
chub get <id> --lang py    # or --lang js, --lang ts
```

Omit `--lang` if the doc has only one language variant — it will be auto-selected.

## Step 3 — Use the docs

Read the fetched content and use it to write accurate code.
**Do not rely on memorized API shapes — use what the docs say.**

## Step 4 — Annotate discoveries

After completing the task, if you discovered something not in the doc — a gotcha,
workaround, version quirk, or project-specific detail — save it:

```bash
chub annotate <id> "Webhook verification requires raw body — do not parse before verifying"
```

Annotations persist across sessions and appear on future `chub get` calls.

## Step 5 — Give feedback

Rate the doc so authors can improve it. Ask the user before sending.

```bash
chub feedback <id> up                        # doc worked well
chub feedback <id> down --label outdated     # doc needs updating
```

Labels: `outdated`, `inaccurate`, `incomplete`, `wrong-examples`,
`wrong-version`, `poorly-structured`, `accurate`, `well-structured`, `helpful`,
`good-examples`.

## Quick Reference

| Goal | Command |
|------|---------|
| List everything | `chub search` |
| Find a doc | `chub search "stripe"` |
| Fetch Python docs | `chub get stripe/api --lang py` |
| Fetch JS docs | `chub get openai/chat --lang js` |
| Fetch multiple | `chub get openai/chat stripe/api --lang py` |
| Save a note | `chub annotate stripe/api "needs raw body"` |
| List notes | `chub annotate --list` |
| Rate a doc | `chub feedback stripe/api up` |

## When to Use (Auto-trigger)

Use `chub` whenever you encounter ANY of these in code:
- `import` / `from X import` / `require()` for external packages
- New library/framework being added to the project
- API endpoint design referencing external service docs
- Version upgrades or migrations
- Unfamiliar or rarely-used library features

## Integration with Codeloop

During autonomous development loops (`codeloop start`), ALWAYS run `chub get`
before implementing features that touch external APIs. This prevents hallucinated
API calls that would break the build and waste loop iterations.
