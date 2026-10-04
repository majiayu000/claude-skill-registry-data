---
name: cargo-connection
description: "Connect Cargo to an external system and find out what it can do — authenticate connectors, browse the integration catalog, and resolve the `connectorUuid` and `actionSlug` a workflow node needs. Triggers: \"connect my HubSpot\", \"is Salesforce connected\", \"what integrations do you support\", \"can Cargo talk to <tool>\", \"what actions does <provider> have\", \"I need the connector UUID\", \"set up the API key for\", \"it is asking for credentials again\", \"why is this connector failing auth\", \"list my connectors\". Integrations: amplemarket, amplitude, attio, bigQuery, calendly, closecom, contrast, csv, customerio, dbt, emailBison, expandi, googleAds, googleSheets, heyReach, http, hubspot, hubspotMcp, instantly, instantlyV2, intercom, jira, kitt, lemlist, lgm, linkedinAds, linkedinMatchedAudience, livestorm, manus, marketo, metabase, microsoftTeams, mixpanel, netsuite, netsuiteSoap, notionMcp, octave, onesignal, outreach, pipedrive, postgresql, redshift, resend, rift, salesforce, salesforceMcp, salesloft, Sendgrid, sillage, slack, smartlead, snowflake, sql, stripe, and 82 more. Skip when: choosing between enrichment providers for a GTM job — use cargo-gtm and its provider playbooks."
version: "1.5.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Connections

Connector and integration management: listing connectors, discovering available integrations, and managing authenticated connector instances.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> See `references/examples/connectors.md` for connector CRUD and discovery examples.
> See `references/examples/integrations.md` for listing available integrations and OAuth flows.
> For third-party connector rate limit handling and retry config in workflows, see `cargo-orchestration/references/polling.md` and `cargo-orchestration/references/troubleshooting.md`. Native integrations do not have rate limits.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Key concepts

**Integration:** The external service type (e.g. HubSpot, Clearbit, Salesforce). Integrations define what actions are available.

**Connector:** An authenticated instance of an integration. One integration can have multiple connectors (e.g. two different HubSpot accounts). Connectors are what you reference in workflow node graphs.

## Discover resources first

**Looking for an action? Search for it — don't browse the catalog.** Two keyword
searches cover the whole surface, and both beat paging `integration list` or
reading a whole `integration get` payload:

```bash
cargo-ai orchestration action list <query>                # START HERE — connector + native + tools + agents.
                                                          # Returns a ready-to-run action object (connectorUuid
                                                          # resolved) and the action's credit costs.
cargo-ai connection action search <query> --credits-only  # connector catalog only, but filters by category
                                                          # and by "is it paid" — which `action list` cannot.
```

Reach for the catalog commands when you need the *integration*, not an action —
its auth fields, its extractors, or the full input schema of an action you have
already picked:

```bash
cargo-ai connection connector list                        # all authenticated connectors
cargo-ai connection integration list                      # all available integration types
cargo-ai connection integration list --search "hubspot"   # search by name
cargo-ai connection integration get <slug>                # one integration's actions + input schemas
cargo-ai connection native-integration get                # built-in Cargo actions only (NOT third-party)
```

> **Deprecated integrations still appear in the catalog.** `integration list` returns them with
> `isDeprecated: true` and a display name ending in `(deprecated)`. Existing connectors keep
> working — deprecation breaks nothing — but never wire a *new* workflow to one. Two were
> deprecated in CLI 1.0.92, the self-referential `cargo` integration among them. Read the flag
> rather than keeping a list: check `isDeprecated` before proposing any integration you found by
> browsing instead of by `action list`.

### Which action search?

| | `orchestration action list` | `connection action search` |
|---|---|---|
| Covers | connector, native, **tools, agents** | connector catalog only |
| Returns | a runnable `action` object with `connectorUuid`, workspace connectors, `credits`, autocompletes | `integrationSlug` + `actionSlug`, category, `credits` — you assemble the action yourself |
| Filters | `--kind`, `--integration-slug`, `--limit` | `--category`, `--integration`, **`--credits-only`**, `--limit` |
| Needs | CLI ≥ 1.0.66 | CLI ≥ 1.0.36 |

Default to `action list` — it is the one that hands you something you can execute.
Switch to `action search` for the two questions it alone answers: *which paid
actions match this?* (`--credits-only`) and *what does this category offer?*
(`--category`). Both rank an action-slug or name hit above an integration hit,
above a description hit, and require **all** query terms to match.

### `integration get` vs `native-integration get`

These two commands return **different sets of actions** and are not interchangeable:

| Command | Third-party service actions (HubSpot, Salesforce, Clearbit, …) | Built-in Cargo actions (HTTP, transforms, utilities) | When to use |
|---|---|---|---|
| `integration get <slug>` | ✓ | ✗ | You need actions for a specific third-party service — **use this for HubSpot, Salesforce, Clearbit, etc.** |
| `native-integration get` | ✗ | ✓ | You need Cargo-native capabilities that don't belong to any specific third-party connector |

**Example:** To find HubSpot-specific actions, use `integration get hubspot` — `native-integration get` will not return them.

## Quick reference

```bash
cargo-ai connection connector list --integration-slug <slug>
cargo-ai connection connector create --integration-slug <slug> --slug <slug> --name <name>
cargo-ai connection connector update --uuid <uuid> --name <name>
cargo-ai connection connector remove <connector-uuid>
cargo-ai connection connector get <connector-uuid>
cargo-ai connection connector autocomplete --connector-uuid <uuid> --slug <slug> --params '<json>'
cargo-ai connection integration list
cargo-ai connection integration get <slug>
cargo-ai connection integration get-documentation <slug>
cargo-ai connection native-integration get
```

## Connectors

Connectors are authenticated connections to external services.

```bash
# List all connectors
cargo-ai connection connector list

# Create a connector
cargo-ai connection connector create \
  --integration-slug clearbit \
  --slug clearbit_production \
  --name "Clearbit - Production"

# Update a connector
cargo-ai connection connector update --uuid <connector-uuid> --name "Clearbit - Staging"

# Remove a connector
cargo-ai connection connector remove <connector-uuid>

# Check if a connector slug is taken
cargo-ai connection connector exists-by-slug --slug clearbit_production
```

**Note:** Creating a connector requires `--slug` (unique identifier) in addition to `--name` (display name) and `--integration-slug`. For OAuth-based integrations, the authentication flow is completed separately via `connection integration complete-oauth`.

## Integrations

Integrations define the available services and their connector actions.

```bash
# List all available integrations
cargo-ai connection integration list

# Filter by category
cargo-ai connection integration list --category enrichment

# Search by name
cargo-ai connection integration list --search "hubspot"

# Find by exact slug(s)
cargo-ai connection integration list --slugs clearbit

# Only integrations that have actions (usable in workflow nodes)
cargo-ai connection integration list --has-actions true

# Only integrations that have extractors (can sync data into models)
cargo-ai connection integration list --has-extractors true

# Get built-in Cargo actions and extractors (NOT third-party connector actions)
cargo-ai connection native-integration get
```

**Integration categories:** `engagement`, `marketing`, `sales`, `finance`, `analytics`, `freeform`, `success`, `support`, `enrichment`, `storage`, `custom`.

Use `integration get <slug>` to discover all actions available for a specific third-party service (e.g. HubSpot, Salesforce). Use `native-integration get` only for built-in Cargo actions — it does **not** return HubSpot or other service-specific actions. Actions are referenced by `actionSlug` in workflow node graphs (see the `cargo-orchestration` skill's `references/nodes.md`).

## Connector autocomplete — fetching available values for action fields

Some action fields don't accept freeform input — their allowed values must be fetched dynamically from the connector. When you inspect an action's config (via `integration get <slug>` or `native-integration get`), look at the `uiSchema` alongside the `jsonSchema`. If a field's `uiSchema` contains `"ui:widget": "IntegrationAutocompleteWidget"`, the valid values for that field **must** be retrieved using `connector autocomplete`.

### How to detect autocomplete fields

When an action's config looks like this:

```json
{
  "jsonSchema": {
    "type": "object",
    "properties": {
      "objectType": { "type": "string", "description": "The object type" }
    }
  },
  "uiSchema": {
    "objectType": {
      "ui:widget": "IntegrationAutocompleteWidget",
      "ui:options": {
        "slug": "listObjects",
        "allowRefresh": true
      }
    }
  }
}
```

The `objectType` field requires autocomplete. The `ui:options.slug` (`"listObjects"`) is the autocomplete slug you pass to `connector autocomplete`.

### How to call connector autocomplete

```bash
cargo-ai connection connector autocomplete \
  --connector-uuid <connector-uuid> \
  --slug <autocomplete-slug> \
  --params '{}'
```

| Flag               | Required | Description                                                       |
| ------------------ | -------- | ----------------------------------------------------------------- |
| `--connector-uuid` | yes      | The UUID of the connector to autocomplete against                 |
| `--slug`           | yes      | The autocomplete slug from `uiSchema[field]["ui:options"].slug`   |
| `--params`         | yes      | JSON object of parameters (use `{}` when none are needed)         |
| `--value`          | no       | Search string to filter results                                   |
| `--refresh`        | no       | Bypass cache and fetch fresh results                              |

### Autocomplete with parameters

Some autocomplete fields depend on the value of another field. This is indicated by a `params` object in `ui:options`:

```json
{
  "uiSchema": {
    "objectType": {
      "ui:widget": "IntegrationAutocompleteWidget",
      "ui:options": { "slug": "listObjects" }
    },
    "propertyName": {
      "ui:widget": "IntegrationAutocompleteWidget",
      "ui:options": {
        "slug": "listObjectProperties",
        "params": { "objectType": "$this.$parent.objectType" }
      }
    }
  }
}
```

Here, `propertyName` depends on the selected `objectType`. Replace the `$this.$parent...` expression with the actual value you chose:

```bash
# 1. First, get the list of object types
cargo-ai connection connector autocomplete \
  --connector-uuid <uuid> --slug listObjects --params '{}'

# 2. Then, get properties for the chosen object type
cargo-ai connection connector autocomplete \
  --connector-uuid <uuid> --slug listObjectProperties \
  --params '{"objectType": "contacts"}'
```

### Response format

```json
{
  "results": [
    { "label": "Contacts", "value": "contacts" },
    { "label": "Companies", "value": "companies" },
    { "label": "Deals", "value": "deals" }
  ]
}
```

Use the `value` field in your node config. The `label` is the human-readable display name. Results may also include optional `description` and `parent` fields.

### End-to-end example: configuring a HubSpot action

```bash
# 1. Find your HubSpot connector UUID
cargo-ai connection connector list --integration-slug hubspot

# 2. Get HubSpot actions and inspect their config + uiSchema
cargo-ai connection integration get hubspot
# → The "findRecords" action has objectType with autocomplete slug "listObjects"

# 3. Fetch available object types
cargo-ai connection connector autocomplete \
  --connector-uuid <hubspot-connector-uuid> \
  --slug listObjects --params '{}'
# → Returns: contacts, companies, deals, tickets, etc.

# 4. Fetch properties for the chosen object type
cargo-ai connection connector autocomplete \
  --connector-uuid <hubspot-connector-uuid> \
  --slug listObjectProperties \
  --params '{"objectType": "contacts"}'
# → Returns: email, firstname, lastname, phone, etc.

# 5. Use these values in your workflow node config
```

## Using connector actions in workflows

Connector actions are used as nodes in workflow graphs. To use an action:

```bash
# 1. Find your connector UUID
cargo-ai connection connector list
# → Filter the output by integrationSlug to find the right connector

# 2. Discover the action — search first, and only then read its schema
cargo-ai orchestration action list <keywords> --integration-slug <integration-slug>
cargo-ai connection integration get <integration-slug>
# → actions are keyed by actionSlug, with config.jsonSchema (input) for each
# → many actions also carry output.schema — the JSON Schema of what the action
#   emits; use it to wire downstream nodes instead of guessing (absent on some actions)
# → Or use get-documentation for a plain text overview
# → Or use native-integration get for built-in Cargo actions (not third-party)

# 3. Reference the connector and action in a node graph
# See cargo-orchestration references/nodes.md for the full node syntax
```

### Reading an action's input schema — and where the inputs go

An action's **input** fields live at `actions.<slug>.config.schema` in the `integration get <slug>` output (`config.jsonSchema` is the same schema decorated for the form UI). Read it before calling an action — don't guess field names.

```bash
# the required input fields for an action:
cargo-ai connection integration get linkedin \
  | jq '.integration.actions.connectProfile.config.schema'
# → required: linkedinProfileUrl, identityIds
```

Two footguns:

- **For a top-level action (`action execute` / `execute-batch`), the input values go in `--data`, NOT in the action's `config`.** The fields described by `config.schema` are the `--data` payload; the action definition carries no `config` key at all. **Misplacing them is no longer a loud failure:** older backends rejected the call with `A top-level action does not use action.config; pass the action's inputs via data instead.`, newer ones drop `config` on the way in and run the action with **no inputs at all** — you get a missing-required-field error from the provider, or an empty result, not a message about `config`. If an action comes back empty for no obvious reason, check that the inputs are in `--data`. (Inside a workflow **node graph** those same fields go in the node's `config` — see `cargo-orchestration/references/nodes.md`. The "`--data`, not `config`" rule is specific to `action execute`/`execute-batch`.)
- **Some inputs must be resolved first via autocomplete.** If a field's `uiSchema` carries `IntegrationAutocompleteWidget`, fetch its values with `connector autocomplete` (above). Notably, LinkedIn engagement/extraction actions (`connectProfile`, `visitProfile`, `extractEventAttendees`, `extractProfileViewers`) require `identityIds` — the connected account that *acts* — resolved via the `listIdentityIds` autocomplete. A `must match format "uuid"` error means that identity is missing.

Example connector node (Clearbit company enrichment):

```json
{
  "uuid": "node-uuid",
  "slug": "enrich",
  "kind": "connector",
  "integrationSlug": "clearbit",
  "actionSlug": "enrichCompany",
  "connectorUuid": "<clearbit-connector-uuid>",
  "config": {
    "domain": {
      "kind": "templateExpression",
      "expression": "{{nodes.start.domain}}",
      "instructTo": "none",
      "fromRecipe": false
    }
  },
  "childrenUuids": ["end-node-uuid"],
  "fallbackOnFailure": false,
  "position": { "x": 0, "y": 166 }
}
```

## Help

Every command supports `--help`:

```bash
cargo-ai connection connector list --help
cargo-ai connection connector create --help
cargo-ai connection integration list --help
```
