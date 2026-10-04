---
name: apple-ads
description: Use when operating a connected Apple Ads account through the Adapty CLI — weekly check-ins, cohort and keyword bid reviews, competitor keyword opportunities from Market Intelligence, search-term harvesting, negative-keyword mining, CPP routing, bids, budgets, keywords, campaigns, and rule automations. Requires the adapty CLI and an Adapty account. Use apple-ads-audit for read-only account health or live structure diagnostics, and apple-ads-strategy for planning without an account.
license: MIT
---

# Apple Search Ads through the Adapty CLI

Reads and `automations run --dry-run` cost nothing. Every other `asa` command reaches Apple
within seconds and spends real money, and nothing it creates can be deleted or undone.

Open the reference a workflow names before running its commands:

- `references/asa-management.md` — campaigns, ad groups, ads, keywords, negative keywords,
  product pages, creatives, automations.
- `references/asa-metrics.md` — `metrics`, `metrics overview`, `search-terms list`,
  `competitors summary`.

## Preflight — always, every session

**First action of every session is the quiet `adapty asa whoami` wrapper below.** Not a check you
skip because setup "was already done": a cloud or Cowork session starts on a clean machine and
nothing carries over. Run the block as one command and do not narrate before it.

```bash
# agent-preflight:start
if ! command -v adapty >/dev/null 2>&1; then
  echo NEED_SETUP
  exit 0
fi

clean_preflight() {
  printf '%s\n' "$1" | sed '/^ERROR: failed to copy trust settings of system certificate-25291$/d'
}

OUT=$(adapty asa whoami 2>&1); RC=$?
if printf '%s\n' "$OUT" | grep -q 'failed to copy trust settings of system certificate-25291'; then
  OUT=$(NODE_USE_SYSTEM_CA=0 adapty asa whoami 2>&1); RC=$?
  CLEAN=$(clean_preflight "$OUT")
  if [ "$RC" -eq 0 ]; then
    [ -n "$CLEAN" ] && printf '%s\n' "$CLEAN"
    echo READY_AUTHED_SYSTEM_CA_OFF
    exit 0
  fi
  case "$CLEAN" in
    *ads_manager_subscription_required*|*402*)
      [ -n "$CLEAN" ] && printf '%s\n' "$CLEAN"
      echo READY_AUTHED_NO_SUB
      exit 0
      ;;
  esac
  echo RETRY_OUTSIDE_SANDBOX
  exit 75
fi

CLEAN=$(clean_preflight "$OUT")
if [ "$RC" -eq 0 ]; then
  [ -n "$CLEAN" ] && printf '%s\n' "$CLEAN"
  echo READY_AUTHED
  exit 0
fi
case "$CLEAN" in
  *ads_manager_subscription_required*|*402*)
    [ -n "$CLEAN" ] && printf '%s\n' "$CLEAN"
    echo READY_AUTHED_NO_SUB
    ;;
  *AuthRequiredError*|*'Not authenticated. Run `adapty auth login`.'*)
    echo NEED_SETUP
    ;;
  *NetworkError*|*network_error*|*'Could not reach Adapty API'*|*'fetch failed'*)
    echo NETWORK_BLOCKED
    ;;
  *)
    [ -n "$CLEAN" ] && printf '%s\n' "$CLEAN"
    echo PREFLIGHT_ERROR
    ;;
esac
# agent-preflight:end
```

| What it does | What that means |
|---|---|
| `READY_AUTHED` after a company with `Apple Credentials Status: active` | Ready. Continue and confirm success in one short line. |
| `READY_AUTHED_SYSTEM_CA_OFF` | Ready. Prefix every later `adapty` call in this session with `NODE_USE_SYSTEM_CA=0`; do not mention the suppressed certificate noise. |
| `RETRY_OUTSIDE_SANDBOX` | Retry the same read-only `adapty asa whoami` exactly once outside the sandbox if the tool explicitly supports it. On success, use that mode for later read-only `adapty` calls in this session. Never use `sudo`. |
| `NEED_SETUP` | Open the `adapty-cli-setup` skill and stop here. Do not hand-roll an install or a login. |
| `402 ads_manager_subscription_required` | Authenticated fine; the company has no Ads Manager subscription. Not a bug and no flag works around it. Say so plainly. Planning still works — offer `apple-ads-strategy`. |
| Apple credentials not active | `adapty asa connect` — see `adapty-cli-setup`. |
| `NETWORK_BLOCKED`, or the one outside-sandbox retry also fails | Do not open setup, reinstall, or authenticate. Say only: “Adapty API is unreachable from this sandbox. Allow network access for `adapty.io` and `*.adapty.io`, then start a new task.” |
| `PREFLIGHT_ERROR` | Surface the cleaned error once and stop. Do not guess that it is an authentication problem. |

`NetworkError` never routes to `adapty-cli-setup`. Do not install or log in. Certificate `-25291`
is sandbox Keychain noise, not an Adapty certificate failure. Never recommend resetting Keychain,
updating Xcode, using `sudo`, reinstalling the CLI, or running `auth login` for it. The raw repeated
lines stay captured inside the wrapper and must not be copied into the response.

## Finding the right playbook

For anything recurring — a weekly review, a harvest, a bid pass, an incident — open
`references/INDEX.md` and read the one playbook it names. The playbook carries the decision rules;
the workflows below carry the command shapes. Read the playbook first, then come back for syntax.

For "how should I structure this account", "which keywords should I even start with", or any
question that precedes having an account, that is the `apple-ads-strategy` skill, not this one.

For "what is broken in this live account", a broad health check, duplicate Exact ownership, or
missing cross-negatives, use the read-only `apple-ads-audit` skill. A weekly operating check-in stays
here. Do not make audit and operator compete for the same request.

## Two things about how you answer

- **Answer in the language the user writes in.** Everything in this skill is English; translate your
  output, never these instructions.
- **Category baselines.** If the `apple-ads-benchmarks` skill is available, use it for what "normal"
  looks like in this app's niche before calling a number good or bad. If it is not installed, say
  there is no baseline and compare the account against its own history instead — never invent one.

## Analysis and proposal contract

Every recurring workflow returns `summary`, `scope`, `date_window`, `findings`, `evidence`,
`confidence`, `unknowns`, and `recommended_actions`. A finding separates the observed value from
its explanation and names the metric, entity id, and date window behind it. Name a cohort window
only for `revenue`, `roas`, `arpu`, `arppu`, `arpas`, or `roi`; non-cohort metrics have no day-X
interpretation.

A workflow that may write also shows a mutation proposal before asking for confirmation:

- target entity and current state;
- proposed state;
- reason and evidence;
- expected effect and risk;
- whether the CLI provides a rollback;
- `requires_confirmation: true`.

Low confidence never produces a mutation. `unknown` is not a failure. Do not turn several controls
into a made-up score.

## Account surface

- `adapty asa whoami` — company, how access was granted, Apple connection state. Run it first.
- `adapty asa connect [--no-wait]` — prints the Apple authorization link and waits; `--no-wait`
  returns immediately.
- `adapty asa orgs list` — ASA organizations. Each row carries two identifiers, not
  interchangeable: `internal_id`, the UUID `--org` takes on `campaigns create` and
  `--campaign-group` takes on the lists that accept scope filters, and `org_id`, Apple's numeric id,
  which both reject. `--org` itself exists only on `campaigns create`; no list accepts it.
- `adapty asa apps list` — apps promoted in Apple Search Ads. Each row carries two identifiers,
  not interchangeable: Apple's numeric adam-id (`--adam-id`) and the ASA app UUID (`--app`).
- Those two and `automations list` take pagination only — no scope filters exist.
- Scope is the token's company. No `asa` command takes `--app` to select scope — `--app` is a
  list filter only.
- `402 ads_manager_subscription_required` — no Ads Manager subscription. `404` — not theirs, or
  does not exist.
- `--json` for machine-readable output on reads; a write under `--json` refuses and exits `2`.
  `--page` (default `1`), `--page-size` (default `100`, max `1000`) on every list — prefer one big
  page to a pagination loop.
- `ADAPTY_ASA_API_URL` overrides the ASA base URL, independently of `ADAPTY_API_URL`.

## The two templates

Fill every slot. A slot you cannot fill from a read is one you ask about, not one you drop.

```
adapty asa <topic> list --<filter-from-that-list-s-matrix-row> <id-from-a-previous-list> [--status <enum>]
adapty asa <topic> <create|update|add> [<id>] <field flags> --idempotency-key <key>
```

**The scope filter is a required slot, and the matrix is the only place it comes from** — read that
list's own row in `references/asa-management.md`, `## Scope filters`, and fill the slot from it. A
flag you saw on a create command, or on a different list, is not a filter for this one: `--org`
belongs to `campaigns create`, and the equivalent on the lists that take scope filters at all is
`--campaign-group`. Required on a
session's first list as much as its fifth — a filter changes the query the server ranks, while page
size only changes how much of the wrong answer you see.

**Two entities the user named separately are two lookups.** "The best-performing campaign" and "the
brand ad group" are not parent and child unless the user said so. Resolve each by its own name
(`ad-groups list --search <name>`), and never scope one lookup with an id produced by resolving the
other — that filter asserts a relationship the user did not state, and the write that follows lands
somewhere plausible and wrong without erroring. More than one match is where you ask, not pick.

**`--idempotency-key` is a required slot**, distinct per write in a chain and per batch within a
write. The CLI's auto key covers a network retry inside one invocation, not the person who
re-runs your create step after an ambiguous result — new invocation, fresh key, second campaign.
That, plus `422 cli_idempotency_key_reuse` and `409 cli_idempotency_in_progress`:
`references/asa-management.md`, `## Writes and idempotency`.

**`--yes` is not in the template, because whether it belongs depends on who runs the command.**

- **The user runs it** — you are writing commands out for them. Omit `--yes`. At their terminal the
  CLI prints the exact request body and waits; that prompt is their confirmation, and `--yes` is the
  one flag that deletes it. Nothing in your surrounding text puts it back, so no warning, STOP
  block, or stated assumption substitutes for leaving the flag off.
- **You run it** — in this session. Ask, get an explicit yes, then append `--yes` to the command you
  run.

`metrics`, `metrics overview`, `search-terms list` and `competitors summary` share **2 concurrent
queries per company**: `429 cli_analytics_busy` is a full pool, `429 cli_rate_limit_exceeded` a
full window, and
`429 cli_cooldown_active` the escalating **5m → 30m → 3h** lockout. See
`references/asa-metrics.md`, `## The analytics pool`.

## One question, one call

The server aggregates and the server ranks. Decide the single call that answers the question before
running anything; the metrics budget is **5 calls per minute** (`references/asa-metrics.md`).

- Totals: one `metrics overview` call.
- Best or worst N: one `metrics --order-by <metric> --page-size N` call, `--order asc` for worst.
- Trend or period comparison: one call — a per-period series already contains both periods.
- Counting entities: no metrics call at all. Any list with `--page-size 1` returns
  `meta.pagination.count`.
- `metrics` and `metrics overview` take no scope filters at all. You narrow by entity level and
  window, then match the returned rows against the ids from a scoped list.
- A window too wide for its bucket is cured by coarsening, never by splitting. Caps: **90 days** at
  day grain or with no period grouping, **180** by week, **365** by month and coarser. A year of
  data is one call at `--group-by month` (or `--period-unit month`), not four 90-day calls.

Never sum pages client-side, never call once per period, and never add a comparison the user did not
ask for — propose that in the answer instead.

## Never

- **Never settle a superlative yourself.** "Best-performing", "losing", "terrible ROAS" are
  business definitions, not query results. Name the metric and the window, get the user's yes on
  that definition, then write.
- **Never write without naming the change in chat first** — which campaign, which budget, how
  many keywords.
- **Never put more than 15 keywords in one `keywords add` or `negative-keywords add` call.** The
  cap is 100; the practice is 15.
- **Never loop on a `429`.** The CLI already waited the exact `Retry-After` and retried once, so a
  `429` that reaches you means the budget is genuinely gone. Cut the number of calls, or tell the
  user when to retry.
- **Never guess or probe a metric name.** The vocabulary is in `references/asa-metrics.md`. A wrong
  name fails listing every valid one, so a typo costs one call — spending a call to see what works
  is the failure. Cohort metrics rank by their expanded names; agent workflows always use
  `--order-by net_roas`, not `--order-by roas`, and never offer gross or proceeds.
- **Never invent an id, adam-id, budget or bid.** Read it from the matching list, or ask.
- **Never put `--yes` on a command the user will run.** It deletes the preview they would have read.
  `--yes` belongs only on a command you run yourself, after an explicit yes.
- **Never write a teardown.** No delete exists in the `asa` topic and there is no undo;
  `--status PAUSED` is the only stop.

## Rationalizations

| What the agent told itself | What is actually true |
|---|---|
| "40 keywords is under the CLI's 100-per-call batch limit, so this is one call, not a loop." | Under the cap is not the same as safe. Nine rejected rows inside a 40-item response is a repair job; inside a 15-item call it is a re-run. |
| "I'd use ROAS over a trailing window as the default definition of "best-performing," and ask the user to confirm/override it before step 5 — but here is the command that answers it." | Handing over the command does not obtain the sign-off you just said had to come first. If the definition needs confirming, stop at the definition. |

## Red Flags — STOP

- A `list` with no scope filter — including the first one, and the one you are "only glancing at"
- A scope filter on `orgs list`, `apps list` or `automations list`
- A filter you did not read off that list's own row in the matrix — a create flag such as `--org`,
  or another list's filter, is not one
- `--yes` on a command you are handing to the user — it deletes the preview they were going to read
- A lookup scoped by an id that came from resolving a different entity the user named separately
- A create in a chain of dependent creates with no `--idempotency-key` pinned
- More than 15 keywords in one call
- A write whose target you picked by your own definition of "best", "losing" or "terrible"
- `--order-by-day` with no matching `--by-days` window in the same call
- `--by-days`, `--order-by-day`, or a `day-X` label attached to `cost_per_paid`, `cost_per_trial`,
  or any metric outside `revenue`, `roas`, `arpu`, `arppu`, `arpas`, and `roi`
- You stated a rule, and three commands later are making a silent exception to it

Observed in CLI-side sessions rather than in this skill's own baseline:

- Looping `--page 1..4` to build a total, instead of one `overview` call or one big page
- Spending a call to discover which metric names are valid
- Adding a period comparison the user did not ask for
- Retrying a `429` after a guessed `sleep` instead of the `Retry-After` value

**All of these mean: stop, read first, ask.**

## Workflows

**1. Orient.** `whoami` → `connect` if Apple is unlinked → `orgs list` → `apps list`.
Prerequisite for everything below. → `references/asa-management.md`,
`## Account and discovery`.

**2. Report performance.** Totals and any trend take the first shape; best or worst N takes the
second, with `--order asc` for worst. Dates are required on both — without them the command exits
before it reaches Apple. Counting needs no metrics call: any list at `--page-size 1` carries
`meta.pagination.count`. `--by-days` takes max **16 windows per call**, applies only to `revenue`,
`roas`, `arpu`, `arppu`, `arpas`, and `roi`, and `--order-by-day` may only name one of those values.
Revenue-family decisions always use the expanded `net_` value. → `references/asa-metrics.md`,
`## Cohort windows`.

```
adapty asa metrics overview --entity <level> --date-from <YYYY-MM-DD> --date-to <YYYY-MM-DD> [--period-unit <bucket>]
adapty asa metrics --entity <ad|ad-group|campaign|keyword> --date-from <YYYY-MM-DD> --date-to <YYYY-MM-DD> --order-by <metric> --page-size <n>
```

**3. Launch a campaign.** Read `orgs list` → `--org` and `apps list` → `--adam-id` first; then
each create consumes an id the previous printed. Neither the order nor any key is optional.
Mint `<run>` once per launch, so a second launch cannot collide. Create the campaign `PAUSED`,
verify the structure, then enable it with workflow 6 — nothing spends until you do. Set
`--match-type` yourself: it defaults to `BROAD`, which is the widest, most expensive targeting. →
`references/asa-management.md`, `## Writes and idempotency`.

```
adapty asa campaigns create --org <id> --adam-id <adam-id> --name <name> --country <country-code> --daily-budget <amount> --status PAUSED --idempotency-key <run>-camp
adapty asa ad-groups create --campaign <id> --name <name> --default-bid <amount> --idempotency-key <run>-ag
adapty asa creatives list --app <app-uuid>   # → --creative-id; no creatives create exists
adapty asa ads create --ad-group <id> --creative-id <id> --name <name> --idempotency-key <run>-ad
adapty asa keywords add --ad-group <id> --text <keyword> --match-type <EXACT|BROAD> --idempotency-key <run>-kw-1   # ≤15 per call, fresh key per batch
```

**4. Harvest keywords.** Read the dated, scoped search terms plus the destination's positive and
negative inventory. Resolve the current and intended Exact owner before writing. Add and verify the
new Exact owner before adding a narrow cross-negative to the source. Keep promote, block, observe,
already-owned, conflict, and insufficient-evidence rows separate. Maximum 15 additions per call,
with a fresh key per call. → `references/playbooks/search-term-harvesting.md`.

**5. Keyword bid review.** If the user has not selected a success metric, offer `cost_per_paid`,
`cost_per_trial`, then net `roas` at day X, in that order, and get the target. Ask for a cohort
window only for a cohort root; cost metrics use the report date window directly. Read keyword
metadata, then rank with one server-side metrics call. Separate increase, keep, decrease,
pause-candidate, and insufficient-data rows. Without a target, report outliers but do not write.
Group identical approved changes, use a fresh idempotency key per write, and read back the keyword
state. Budget changes are a separate decision. → `references/playbooks/bid-optimization.md`.

**6. Pause or resume.** Campaigns, ad groups, ads:
`update <id> --status ENABLED|PAUSED --idempotency-key <key>`. Keywords:
`update <id> [<id>…] --status ACTIVE|PAUSED --idempotency-key <key>`. The keyword enum differs
from every other entity's, and there is no `DISABLED` anywhere in the surface. Ids come from a
scoped list first. → `references/asa-management.md`, `## Status`.

**7. CPP routing.** Resolve the query intent, existing product pages, creatives, and ads before
choosing a page. Sync only when the catalog is missing or stale, and confirm that write separately.
An ad's creative cannot be changed: create and verify a new ad, then pause an old ad only through a
second confirmation. The CLI selects an existing CPP; it does not edit one. →
`references/playbooks/creative-setup.md`.

**8. Diagnose a dead ad.** `ads get <id>`, read `serving_state_reasons`; if that does not
explain it, walk up to `ad-groups get <id>` status, then `campaigns get <id>` status and daily
budget. All reads. → `references/asa-management.md`.

**9. Rule automations.** `automations create --file rule.json --idempotency-key <key>` →
`automations run <id> --dry-run` → `automations runs <id>` to read what it would have done →
`automations update <id> --start`, only after the user has seen that outcome. Dry-run every rule
touching a bid or a budget. → `references/asa-management.md`.

**10. Competitor keyword opportunities.** Read up to five App Store ids in one
`competitors summary --json` call. The full response carries per-app, per-country terms and SOV;
the endpoint covers the last full month and every country. Compare those terms with the account's
active, paused, and negative keyword inventory. Never claim competitor bids, spend, conversions, or
profitability from this data. Keyword creation is a separately confirmed step. →
`references/playbooks/keyword-opportunity.md`.

## Anything not covered here

1. This file and its two references are the source of truth for the `asa` surface.
2. `adapty asa <topic> <command> --help` — exact flag syntax for the installed version.
3. The CLI repo, https://github.com/adaptyteam/adapty-cli (default branch): `docs/agent/`, then
   `src/commands/asa/**`, where a command's own `static flags` declaration outranks any table and
   settles a disagreement between prose and commands.

`references/asa-management.md` and `references/asa-metrics.md` are generated from that repo and can
lag the installed CLI by one release. If `--help` and a table here disagree, `--help` wins and the
disagreement is a bug — open an issue at https://github.com/adaptyteam/apple-ads-cli/issues.

Do not guess a flag, a command, or a URL path. If none of the three confirms it, say so.
