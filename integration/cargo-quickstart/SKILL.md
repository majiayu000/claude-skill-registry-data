---
name: cargo-quickstart
description: "Guided first-run demo for Cargo — one persona question to 25 real leads with a cost receipt in under two minutes, ending by saving the pull as a recurring play. Triggers: \"show me what Cargo can do\", \"give me a demo\", \"take me on a tour\", \"quickstart\", \"getting started with Cargo\", \"I just installed Cargo\", \"my workspace is empty\", \"does this actually work\". Skip when: the user has a real job to run (build a list, enrich a CSV, find emails) — use cargo-gtm; when they want CLI reference or routing — use the cargo router skill."
version: "1.0.4"
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

# Cargo Quickstart — first value in two minutes

One guided demo: pull ~25 fresh leads matching a buyer persona the user picks, show the cost receipt, then save the pull as a recurring play. The point is not the list — it's that in minute 3 the user owns a running system, not a one-off result.

**A new account starts with 100 free credits — no card.** This demo spends about **5** of them. Say that out loud before the first paid call ("this costs about 5 of your 100 free credits"): it converts the moment from *a purchase decision* into *a look around*, which is the whole job of a quickstart. Never let a new user think the demo is why they'd run out.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## The one question

Ask exactly **one** question before doing anything:

> **"Who do you sell to?"** (a persona in a few words — e.g. "Heads of RevOps at mid-market SaaS")

Everything else — provider, filters, limits — you decide. Don't ask about output format, volume, or providers; defaults below.

## Speed budget — HARD RULES

The demo has a two-minute budget from answer to deliverable. On the fast path:

- **No discovery detours.** Do not run `cargo-ai --version`, `cargo-ai whoami`, `connection connector list`, or any exploratory command first. Auth problems will surface as errors on the first real call — handle them then.
- **One command block per step**, no narration between commands.
- **Paid work is capped at ~5 credits total.** The demo uses LinkedIn-native people search (`salesNavigator.searchLeads`, 0.2/record → 25 records ≈ 5 credits). Nothing else paid runs without asking.
- **Never dead-end.** Every step has a fallback (ladder below). If a rung fails, drop one rung silently and keep moving.

## Fast path

Translate the persona into a `searchLeads` filter (quote the exact title phrase in `keywords`; a bare keyword matches loosely and pollutes the page) and run:

```bash
# 1. Execute — returns a run object; note run.uuid and run.workflowUuid.
#    searchLeads returns a 25-row page minimum (limit below 25 still bills 25 × 0.2 = 5 credits).
cargo-ai orchestration action execute \
  --action '{"kind":"connector","integrationSlug":"salesNavigator","actionSlug":"searchLeads"}' \
  --data '{"keywords": "\"<persona title phrase>\"", "limit": 25}' \
  --wait-until-finished > /tmp/quickstart-run.json

# 2. Fetch the output data (NOT in the execute stdout) — signed URL, then filter to THIS run
RUN_UUID=$(jq -r '.run.uuid' /tmp/quickstart-run.json)
WF_UUID=$(jq -r '.run.workflowUuid' /tmp/quickstart-run.json)
curl -s "$(cargo-ai orchestration run download-outputs \
  --workflow-uuid "$WF_UUID" --output-node-slug action --format json | jq -r '.url')" \
  > /tmp/quickstart-outputs.json

# 3. Show the table (the file holds ALL of the workflow's runs — filter by _uuid;
#    each row's .output is the leads array directly, fields are snake_case)
jq -r --arg u "$RUN_UUID" \
  '[.[] | select(._uuid==$u)][0].output[] | [.full_name, .job_title, .company_name, (.recently_hired // false)] | @tsv' \
  /tmp/quickstart-outputs.json | head -25
```

Show the table (name · title · company · recently-hired), not the raw JSON. `recently_hired: true` rows are the demo's headline — lead with them ("6 of these 25 just started the job — the exact moment to reach out").

### Fallback ladder (on auth/error, drop a rung — don't stop)

1. `salesNavigator.searchLeads` (0.2/record) — primary.
2. `theirStack.searchJobs` (0.5) — reframe as "companies hiring your persona right now" (job postings for the persona's title). Same wow, different angle.
3. `waterfall.searchProspects` (3/record) — **exceeds the ~5-credit demo cap, so this rung asks first**: "The two cheap sources aren't connected; I can pull 5 matches via waterfall for ~15 credits instead — run it, or connect Sales Navigator first (free)?" Run only on an explicit yes, with `limit` capped at 5.
4. Nothing connected at all → run the free path: `cargo-ai connection integration list | head`, show what *could* be wired, and offer to connect one (browser auth) — the demo resumes after.

## The receipt (mandatory, verbatim discipline)

The demo is itself the pilot from [`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md). Close it with a receipt:

- Credits spent + balance remaining (`cargo-ai billing subscription get` — remaining = `subscriptionAvailableCreditsCount − subscriptionCreditsUsedCount`). For a brand-new account, frame it against the **100 free starting credits** rather than as a bare number — "5 spent, 95 of your 100 free credits left" lands very differently from "95 credits remaining".
- Hit-rate: "25 of 25 returned" (or what actually came back, and which rows look off).

## Minute 3 — save it as a play

Immediately offer to make the pull recurring — this is the step that shows what Cargo *is*:

> "Want this to run by itself? I can save this exact search as a play that runs weekly and writes new matches into a model — new `<persona>` leads land without you asking."

On yes, follow [`../cargo-gtm/recipes/save-as-play.md`](../cargo-gtm/recipes/save-as-play.md) with the demo's action + filter as the workflow body and a weekly cron.

## After the demo — route onward

Propose 2–3 next steps grounded in the rows just pulled, per the next-step spec in [`../cargo-gtm/SKILL.md`](../cargo-gtm/SKILL.md) (§4): e.g. "enrich these 25 with firmographics (~0.5 cr each)", "find + verify emails for the best 10 (~1.4 cr each)", or something else entirely. From here, real GTM work belongs to [`cargo-gtm`](../cargo-gtm/SKILL.md) — read it before anything beyond the demo.
