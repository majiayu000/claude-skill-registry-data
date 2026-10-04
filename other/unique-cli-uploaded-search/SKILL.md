---
name: unique-cli-uploaded-search
description: >-
  Search the documents uploaded for the CURRENT task/row (e.g. an Agentic
  Table row's attached files) via the `unique-cli uploaded-search "<query>"`
  command, with the same per-turn citation tracking as `unique-cli search`
  so cited facts render as `<sup>N</sup>` footnotes and clickable reference
  chips on the Unique platform. ALWAYS use this skill when the user refers to
  documents they uploaded/attached to this task, or when you need facts from
  the task's own attached files. These uploaded files are scoped to the chat,
  NOT to a knowledge-base folder, so they will NEVER appear in
  `unique-cli search` results no matter the folder or metadata filters. Use
  `unique-cli search` for the knowledge base and this command for the task's
  uploaded documents; the two are complementary and citation numbering is
  shared across them within a turn.
---

# Unique CLI -- Uploaded Document Search

Documents **uploaded for the current task** (for example an Agentic Table
row's attached files) are **not** part of the knowledge-base folder scope.
They are scoped to the chat, so they will **never** appear in
`unique-cli search` results — no folder or metadata filter can surface them.
Use `unique-cli uploaded-search` to retrieve them.

## Basic Usage

```bash
# Search the documents uploaded for this row/task
unique-cli uploaded-search "target asset classes and investment strategy"

# Limit results
unique-cli uploaded-search "fee structure" --limit 50
```

There is **no** `--folder`/`--metadata` for `uploaded-search` — the set of
uploaded documents is fixed by what was attached to the task.

If no documents were uploaded for this task, the command reports that and you
should fall back to `unique-cli search` for the knowledge base.

## When to use which command

| You want to search… | Command |
|---------------------|---------|
| The knowledge base (folders the task scope grants) | `unique-cli search "<query>"` |
| Documents uploaded for **this** row/task | `unique-cli uploaded-search "<query>"` |

## Output Format

Each result is rendered as a `<sourceN>...</sourceN>` block, identical to
`unique-cli search`. `N` is **1-based** and **shared with `unique-cli search`
within the same turn** — both commands append to the same per-turn citation
manifest, so numbering stays continuous across them (a `search` call that
emitted `<source1>`–`<source3>` is followed by an `uploaded-search` call whose
first result is `<source4>`).

```
Found 1 result(s):

<source1>
<|document|>investment-mandate.pdf</|document|>
<|page|>2</|page|>
<|info|>cont_abc123</|info|>
...the mandate targets EMEA equities with a 5% cap per issuer...
</source1>
```

## Citation Rules

Cite a fact from `uploaded-search` results with `[sourceN]`, **exactly** as you
would for `unique-cli search` — the two share the same namespace and manifest.
The Unique platform converts each `[sourceN]` marker in your final answer into a
`<sup>N</sup>` footnote and a clickable reference chip.

```
The uploaded mandate caps single-issuer exposure at 5% [source1].
```

**Rules** (enforced by the platform's reference post-processor):

1. **`[sourceN]` is for KB and uploaded-document results.** Web results from
   `unique-cli web-search` use `[websourceN]` — never mix the two namespaces.
2. Only cite numbers you saw in the **current** turn's `search` /
   `uploaded-search` output. Numbers from previous turns are stale and will be
   silently dropped.
3. Write `source` in singular form with the number in digits: `[source1]`,
   `[source2]` — not `[Source 1]` or `[source one]`.
4. Prefer citing each fact with a single, most-relevant source.
5. Do not invent source numbers for remembered or inferred facts.

## Command Reference

```
unique-cli uploaded-search <query> [--limit <N>]
```

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--limit` | `-l` | 200 | Max results |

## Prerequisites

Requires these environment variables:

```bash
UNIQUE_USER_ID    # User ID (required)
UNIQUE_COMPANY_ID # Company ID (required)
UNIQUE_API_KEY    # API key — optional on localhost / secured cluster
UNIQUE_APP_ID     # App ID — optional on localhost / secured cluster
```

Install: `pip install unique-sdk`
