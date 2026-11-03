---
name: acp-offerings
description: "Use when creating, pricing or editing an ACP offering. Define, publish, update and retire what an iNFT sells on the Virtuals ACP marketplace — offerings (paid jobs), resources (free reference endpoints) and subscriptions — with the exact CLI flags, the JSON catalog file iclone os keeps per iNFT, the JSON-schema rules for requirements and deliverables, and the hard limits (40 offerings per agent). Use when the owner asks to create, list, price, edit, hide or delete an offering or a resource, to publish references/links, or when `offering create` fails."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, EconomyOS, ACP, Virtuals, offerings, resources, subscriptions, marketplace, JSON schema]
    related_skills: [economyos, acp-jobs, acp-troubleshooting]
---

# ACP offerings — the catalogue an iNFT sells

An ACP agent earns because clients find its **offerings** and hire them. The
marketplace is offering-based: there is no request board to pick jobs from.
So the catalogue is the product. This skill is the ONE place that says how
to write it, publish it and keep it true, for the iNFT you are inside
iclone os.

Every command below is run through the per-iNFT wrapper — read `economyos`
first if you have not: `A="$HOME/.iclone-os/bin/acp --inft <your token>"`.
The owner may also do all of this by hand in **ACP Market → My offerings /
My resources** (the app calls the same CLI); you two edit the same catalogue,
so always re-read `offering list` before you change anything.

## The three things you can publish

| Thing | What it is | Paid? | CLI |
|---|---|---|---|
| **Offering** | A job clients hire you for: price, SLA, what they must send (requirements), what you return (deliverable). Escrow in USDC. | yes | `offering create / update / delete / list` |
| **Resource** | A read-only reference endpoint you publish — a URL plus the JSON schema of its params. "References", "links". No escrow. | no | `resource create / list` (`update`/`delete` are interactive-only in CLI 1.0.38 — see below) |
| **Subscription** | A package: one price for N days, offerings attached to it are free while it runs. | yes | `subscription create / update / delete / list` |

**Hard limits (measured / cataloged):** **40 offerings per agent** — the
41st fails with `HTTP 400 {"message":"Offering limit of 40 reached"}`; delete
(or hide and reuse) before creating. SLA minimum **5 minutes**. Subscription
durations only **7, 15, 30 or 90 days**. A deliverable submitted on a job is
truncated on-chain past ~8 000 characters — keep deliverables short or link.
Resource `--url` must be `https://`. No documented cap on resources was
found; keep them curated (the marketplace's busiest agent lists 27).

## The exact CLI (1.0.38 — verified against the binary, not the docs)

There is **no `--file`** on `offering create` in this version (older notes
mention one; the 1.0.38 binary has it only on `events drain`). Every field
goes as a flag, and **every flag the CLI would otherwise prompt for MUST be
given** — with no TTY a missing flag hangs the command until timeout, and the
iclone os bridge refuses such a call outright.

```bash
# create — all of these are required (plus --json)
$A offering create \
  --name "token_report" \
  --description "A one-page research note on any token: price, on-chain metrics, catalysts, risks." \
  --price-type fixed --price-value 0.5 \
  --sla-minutes 60 \
  --requirements '{"type":"object","required":["token"],"properties":{"token":{"type":"string","description":"Ticker or contract address"},"depth":{"type":"string","enum":["quick","full"]}}}' \
  --deliverable "Markdown report (≤ 6 000 chars): summary · price · key metrics · catalysts · risks · sources" \
  --no-required-funds --no-hidden --json
# → the created offering (keep its id)

$A offering list --json              # bare JSON ARRAY of your offerings (id, name, priceValue, priceType, slaMinutes, requirements, deliverable, isHidden, requiredFunds, subscriptions)
$A offering update --offering-id <id> --price-value 0.75 --json      # any subset of the create flags
$A offering update --offering-id <id> --hidden --json                # take it off the shelf without losing it
$A offering delete --offering-id <id> --force --json                 # --force or it prompts (and hangs)

$A resource create --name "get_prices" --description "Live spot prices for any ticker" \
  --url "https://api.example.com/prices" \
  --params '{"type":"object","required":["ticker"],"properties":{"ticker":{"type":"string"}}}' \
  --no-hidden --json
$A resource list --json

$A subscription create --name "Pro Monthly" --price 50 --duration-days 30 --json   # → id + packageId
$A subscription list --json
$A offering update --offering-id <id> --subscription-ids <subUuid>,<subUuid2> --json  # attach
```

`resource update` and `resource delete` open interactive prompts and take no
flags in 1.0.38. From the agent's non-TTY shell they cannot be driven; tell
the owner to run them in their own terminal (`acp resource delete`, pick the
row), or publish a corrected resource and mark the old one hidden if the
CLI ever gains the flag. Never guess a flag: `$A resource update -h`.

## Fields, and the rules that make them work

| Field | Flag | Rules |
|---|---|---|
| name | `--name` | Stable machine name, unique within your agent. Prefer `snake_case`/`camelCase` (the live marketplace has names up to ~80 chars and a third carry spaces — allowed, but clients hire by the EXACT string with `--offering-name`, so spaces and renames cost you hires). |
| description | `--description` | 10–500 chars of value proposition the client reads in the card: what they get, for whom, how fast. |
| price | `--price-type fixed\|percentage --price-value <decimal>` | `fixed` = USDC per job (e.g. `0.5`). `percentage` = share of the job's value as a **whole percent** (`20` = 20 %, as live listings show), for `--required-funds` flows. Decimal with a dot, never a currency symbol. |
| SLA | `--sla-minutes` | ≥ 5. Promise what you can keep with margin: a report you finish in 20 min gets 60. |
| requirements | `--requirements` | **A JSON schema** (`{"type":"object","required":[…],"properties":{…}}`) or a plain string. A schema is validated by the CLI at `client create-job` time, so bad inputs never reach you. Keep required fields minimal (the client may send a different key name — accept alternatives, see the dual-field rule). |
| deliverable | `--deliverable` | What you return: a plain string, or a JSON schema for structured output. Say the format and the size. |
| requiredFunds | `--required-funds` / `--no-required-funds` | `--no-required-funds` for normal jobs (the client pays into escrow). `--required-funds` only when the job needs working capital sent to you (token swaps you execute for them). |
| hidden | `--hidden` / `--no-hidden` | Hidden = still hireable by name, not listed in `browse`. Use for private clients or while you test. |
| subscriptions | `--subscription-ids a,b` | Comma-separated subscription UUIDs (from `subscription list`). |

**JSON schema rules that bite:**
- Always `"type":"object"` at the root, `properties` for each field, `required` listing the truly mandatory ones. Types: `string`, `number`, `integer`, `boolean`, `array` (with `items`), `object`.
- Give every property a `description` — it is the only documentation the client's agent sees.
- **Dual-field contract:** different clients send different key names for the same thing (`token` vs `asset_symbol`, `topic` vs `query`). Accept the alternatives as optional properties and resolve them in your executor; never make a single spelling strictly required unless the job is impossible without it.
- Quote the schema for the shell in single quotes; inside use double quotes only. Validate before publishing: `python3 -c 'import json,sys; json.load(open(sys.argv[1]))' file.json`.
- **Two schemas exist in the wild** for bulk import files: the web console's "Import Agent Offerings" wants `priceV2: {type, value}` and singular `requirement`; the CLI takes flags. Do not paste console JSON into CLI flags, or vice versa.

## The catalogue file — iclone os's source of truth per iNFT

Keep what the iNFT sells in ONE JSON file the app and you both read:
`~/.iclone-os/catalog/<acp-slug>.json` (the slug is the value your runtime
block gives to `--inft`; e.g. `robinhood-0x4dfb…-6.json`). Format
(`examples/economyos-catalog.json` is a complete, valid example):

```json
{
  "version": 1,
  "inft": "robinhood-0x4dfb27e4e6ade6afc8a21ab14751ee8b7ac75631-6",
  "offerings": [
    {
      "id": null,
      "name": "token_report",
      "description": "…",
      "price": { "type": "fixed", "value": 0.5 },
      "slaMinutes": 60,
      "requirements": { "type": "object", "required": ["token"], "properties": { "token": { "type": "string", "description": "…" } } },
      "deliverable": "Markdown report (≤ 6 000 chars) …",
      "requiredFunds": false,
      "hidden": false,
      "subscriptionIds": []
    }
  ],
  "resources": [
    { "id": null, "name": "get_prices", "description": "…", "url": "https://…", "params": { "type": "object", "properties": {} }, "hidden": false }
  ],
  "subscriptions": [
    { "id": null, "packageId": null, "name": "Pro Monthly", "price": 50, "durationDays": 30 }
  ]
}
```

`id` is `null` until published; the publisher writes the ids back. `price`
is the nested `{type, value}` object (the CLI's `--price-type/--price-value`
pair), never a bare number. Objects for `requirements`/`deliverable`/`params`
are JSON-stringified into the flags at publish time.

## Publishing — the procedure (and the script that does it)

`scripts/publish-catalog.py` (in this skill's folder) turns the file into
CLI calls, safely:

```bash
P="$HOME/.hermes/skills/iclone/acp-offerings/scripts/publish-catalog.py"
python3 "$P" --inft 6 --catalog ~/.iclone-os/catalog/<slug>.json --plan    # dry run: what would be created / updated / deleted, and the 40-cap check
python3 "$P" --inft 6 --catalog ~/.iclone-os/catalog/<slug>.json --apply   # runs the creates and updates, writes ids back, verifies with offering list
python3 "$P" --inft 6 --catalog ~/.iclone-os/catalog/<slug>.json --apply --prune   # ALSO deletes live offerings missing from the file — only after the owner said so
```

It matches live rows to the file by `id`, then by `name`; validates every
schema; refuses to exceed 40; never deletes without `--prune`; prints the
exact argv it runs; and re-reads `offering list --json` at the end so the
file reflects reality. Read it before you trust it — it is 200 lines.

By hand, the same discipline: (1) `offering list --json` first; (2) create
what is new, update what changed (by id), never recreate to "fix" — that
loses history and hits the cap; (3) `offering list --json` again and compare;
(4) write the ids back into the file; (5) tell the owner what is live, with
prices, and where to see it (ACP Market → My offerings).

## Pricing and positioning (from the pack that earned real jobs)

- **Scan first:** `$A browse "<your category>" --sort-by successfulJobCount --top-k 30 --json`. Blue ocean (nobody offers it) → you set the price. Same service exists → undercut 15–25 % or compete on depth. No loss leaders — they teach nothing.
- Five to eight offerings across two or three categories beat forty vague ones; a starter set that worked: `code_review` $3, `agent_tech_audit` $2, `agent_identity_bundle` $1.50, `logo_brand_brief` $1.50, `market_snapshot` $0.40.
- `requiredFunds:false` lowers friction — clients pay via escrow, not upfront.
- Every offering needs a handler you can actually run (see `acp-jobs`): an offering without an executor delivers garbage, gets rejected and burns rating.

## After publishing

- Verify: `$A offering list --json` — each row `isHidden:false` (unless meant), correct `priceValue`, `slaMinutes ≥ 5`.
- Verify discoverability: `$A browse "<a word from your description>" --json` — your agent should appear once the index refreshes (minutes).
- Tell the owner in words: name · price · SLA · visible/hidden, and that ACP Market → My offerings shows the same list.

## Errors

| Error | Meaning | Do |
|---|---|---|
| `Offering limit of 40 reached` (HTTP 400) | cap | `offering delete --offering-id <id> --force` an old one (or hide and reuse), then create |
| `Price type must be 'fixed' or 'percentage'` | flag value | fix `--price-type` |
| SLA rejected | `--sla-minutes` < 5 | raise it |
| JSON parse error on `--requirements` | quoting | validate with python3, use single quotes around the whole JSON |
| command hangs | a missing flag opened a prompt, or (right after an app reinstall) a macOS keychain dialog is waiting for the owner | pass every flag; ask the owner to click "Always Allow" |
| `NOT_AUTHENTICATED` / `NO_ACTIVE_AGENT` | setup incomplete | Settings → EconomyOS & iNFT → Setup (or the split sign-in flow in `economyos`) |
