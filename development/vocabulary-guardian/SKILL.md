---
name: vocabulary-guardian
description: "Ubiquitous language guard: harvests identifiers from code, schema and API definitions, has the LLM cluster synonyms that name the same domain concept (customer/client/account/kunde), reports naming divergences with all locations and proposes one canonical term per concept including rename impact estimate. Never renames anything. Read-only. Trigger: /vocab"
trigger: /vocab
---
# /vocab

Customer, Client, Account, Kunde - four names, one concept, a constant
misunderstanding. Harvests identifiers from code, schema and API definitions,
clusters synonyms into domain concepts and proposes one canonical name per cluster.

## What this is for

- The same domain thing is called `customer`, `client`, `account` in the system,
  `kunde` in the DB - language drift creates bugs, makes searches impossible,
  poisons every onboarding.
- **Read-only skill. No automatic renaming** - only proposal +
  rough impact estimate. Distinction from `/co-change` (Sprint 04
  consistency-enforcer): that deals with duplicated LOGIC, this deals with divergent
  LANGUAGE for the same concept.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/vocab -help` or `/vocab -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir` and optionally a domain hint from the user (free text:
what is the business about - helps clustering). Confirm.

### Step 3 - Harvest

```powershell
& "<SKILL_DIR>/scripts/term-harvest.ps1" -ProjectDir "<path>"
```

### Step 4 - Concept clustering

Group terms into domain concepts: synonyms (customer/client/account),
translation pairs (kunde/customer), abbreviations (cust/usr/acct as candidates
to cluster with full form). Spelling variants (`order_item`/`orderItem`) do NOT
count as divergence - same word choice, only convention. Include the user's
domain hint. Framework/technical terms (parser, handler, config, React props,
Django fields) set aside as "technical vocabulary".

### Step 5 - Divergence check per cluster

Are they REALLY the same concept? Read example locations (Read when uncertain).
Distinguish honestly:

- **synonym-divergence**: same thing, different names - the main finding.
- **homonym-warning**: same name, different things - even more dangerous!
- **legitimately-different**: e.g. `client` = API client, `customer` = buyer
  - no finding, but document in glossary.

### Step 6 - Canonical proposal

Per divergence cluster: choose the dominant/most precise term (frequency +
schema anchoring as criteria, state reasoning), estimate impact roughly
(number of non-canonical term locations; small < 20 / medium / large > 100).

### Step 7 - Write report

File `vocab-report.md` in the current working directory:

1. **Summary** - X concepts, Y with divergence, Z homonym warnings.
2. **Glossary table** - concept, canonical proposal, all names with frequency.
3. **Divergences in detail** - example locations, canonical reasoning, impact.
4. **Homonym warnings**.
5. **Technical vocabulary** (list only).
6. **Open questions** (all `suspected` clusters).

Evidence requirement: each cluster assignment with >= 2 example locations;
homonym warnings with evidence for both meanings.

### Step 8 - Summarize

State the report path, concepts with most synonyms first.

## Usage

```
/vocab                     # interactive
/vocab <dir>               # vocabulary analysis
/vocab <dir> "<domain>"    # with domain hint
/vocab -help
```


