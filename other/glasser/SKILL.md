---
name: glasser
description: Search, inspect, and run third-party data APIs through one CLI when the environment has no suitable integration. 
category: Business & Marketing
source: antigravity
tags: [api, mcp, claude, ai, agent, workflow, image, security, rag, seo]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/glasser
---


# Glasser

## Overview

Glasser is a commercial API broker that exposes third-party data providers
through one CLI and one account. Use it to fill a data gap after checking the
environment's free tools and the user's existing integrations. Provider output
keeps its native structure, so inspect the selected endpoint before every run.

This skill was contributed by a member of the Glasser team.

## When to Use This Skill

- Use when a task needs current web, news, search, social, business, people,
  places, shopping, image, video, or enrichment data that available tools
  cannot supply.
- Use when the user wants pay-per-call access without creating a separate
  account with the underlying provider.
- Use for marketing and research workflows that need structured evidence from
  a named data provider.
- Prefer the user's explicit provider choice, existing API keys, installed
  integrations, and free tools before Glasser.

## How It Works

### Step 1: Check Availability and Authentication

Use the CLI only if it is already installed or the user has approved its
installation under the host environment's software-installation policy.
Installation instructions are maintained at
<https://glasser.ai/SKILL.md>. Do not download or install executable code
without the review and approval required by the current environment.

Check the CLI and account:

```bash
glasser --version
glasser balance
```

If authentication is missing in an interactive session, run `glasser login`.
It opens a browser-based device flow. Relay the URL and code printed by the CLI
and wait for the command to finish. Never ask the user to paste a Key into chat.

For unattended environments, the user can configure `GLASSER_API_KEY` through
the environment's secret manager. Never write it to a project file or include
it in a command argument.

### Step 2: Discover Candidate Endpoints

Search by capability instead of guessing a provider or endpoint:

```bash
glasser search -q "Google search results"
glasser search -q "company enrichment"
glasser search -q "Reddit posts and comments"
```

Compare the provider, endpoint, and listed price. Search results are ranked by
relevance; rank is not a quality or price recommendation.

### Step 3: Inspect the Contract

Inspect the exact endpoint before constructing input:

```bash
glasser inspect -p serper -e /search
```

Record:

- the current price and all charge clauses;
- required and optional input fields;
- fields that control result volume;
- run mode and timeout;
- the provider that will receive the request.

Schemas, prices, and charge clauses can change. The live `inspect` result is
the contract for the next run.

### Step 4: Authorize the Paid Scope

Only `run` spends the workspace balance. Before the first paid call, show the
user the provider, endpoint, per-call price, charge exceptions, input scope,
and requested result volume. Wait for approval unless the user already gave an
exact scope or budget that covers the call.

Create the provider-native JSON input in a file after inspection. A file avoids
shell-quoting errors and keeps the request reviewable. Do not include unrelated
personal, confidential, or credential data.

### Step 5: Run and Recover Safely

Run the approved request:

```bash
glasser run -p serper -e /search -f request.json --wait
```

The CLI prints an Idempotency-Key. If a timeout or transport failure leaves the
outcome uncertain, repeat the request with that same key:

```bash
glasser run -p serper -e /search -f request.json --idempotency-key <same-key> --wait
```

Do not create a new key for an ambiguous retry. It can create and charge a
second run. For a known run, use `glasser runs get -r <run-id> --wait` instead
of starting another one.

### Step 6: Report Evidence and Cost

For every run used in the answer, report:

1. the provider and endpoint;
2. the Glasser run status;
3. what the provider response says;
4. the exact `Charge` printed by the CLI;
5. the private `Run URL` printed by the CLI.

`COMPLETED` means the provider answered. It does not guarantee that the
provider found a result, so describe both the run status and the payload.

## Examples

### Example 1: Research a Search Results Page

```text
Find a Google SERP endpoint in Glasser, show me its current price and input
schema, and ask before running one query for "best email marketing tools".
```

The agent searches the catalog, inspects the selected endpoint, obtains paid
scope approval, writes input that matches the live schema, and returns sourced
results with the charge and Run URL.

### Example 2: Fill a Company-Data Gap

```text
Our current tools cannot enrich these five companies. Find suitable Glasser
endpoints, compare their prices and required inputs, and stop before spending.
```

The agent returns a provider comparison without making a paid run.

## Best Practices

- Start with the smallest result count that can answer the question.
- Reuse data already retrieved during the current task.
- Keep exact decim
