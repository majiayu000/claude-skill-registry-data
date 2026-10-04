---
name: recon
description: >-
  Discover and invoke the canonical recon CLI for durable, reusable external-source analysis of
  repositories, websites, documentation, markets, competitors, papers, and other sources when the
  report must become canonical evidence. Use it to search the web for reusable evidence, research a
  topic, market, or competitor, capture or crawl a bounded site section, find and verify scholarly
  papers, collect X/Twitter or YouTube source metadata, or analyze another project's agents,
  skills, commands, and workflows. Routes design-system work through its `recon:design` mode:
  cloning a site's look, mining or documenting a design system, extracting design tokens,
  typography, spacing, layout, or repeated components, and preparing reusable UI-library inputs.
  Do not use for a one-off web lookup or page fetch, or ordinary code editing that needs no durable
  evidence record.
---

# Recon

Use recon for external-source analysis whose report, source metadata, and supporting assets must
be saved as one canonical evidence record. The runtime and vault belong to the `recon` repository,
not to this skill package or the calling harness.

## Resolve the canonical runtime

Resolve one invocation before reading or acquiring evidence:

1. Prefer `command -v recon`. Accept it only when `recon --version` succeeds and
   `recon doctor --json` reports `ready`. Activation READS the resolved workspace; it never supplies
   one. Pass `--profile <name>` to select a scope, and `--vault` only when the caller explicitly
   supplied a root — do not synthesize `--vault "$RECON_VAULT"` when that variable is unset, which
   resolves an empty path instead of the configured root. `doctor`'s `workspace` object names the
   root and which source chose it (`cli`, `env:RECON_VAULT`, `profile`, `default:RECON_HOME/vault`,
   or `unset`); report that source rather than inferring one.
2. If no installed command is usable, accept an explicitly supplied `RECON_HOME` only when it is a
   readable canonical checkout containing `go.mod` and `cmd/recon/main.go`. Use
   `go run -C "$RECON_HOME" ./cmd/recon` and run the same version and doctor checks.
3. Otherwise return a bounded `runtime-only` or `unavailable` result naming the failed check and
   the explicit Recon installation documentation. Do not install software, create a vault, change
   configuration, or authenticate. Do not guess a path such as `$HOME/dev/recon`.

An unconfigured workspace is a reportable state, not a gap to close. Never run `recon configure`,
never create a profile, a config file, or a layer directory, and never write to
`$XDG_CONFIG_HOME/recon/config.toml`. `configure` requires an explicit `--yes` precisely so that an
automated caller cannot initialize by omission — report `unset` and stop.

Use the resolved invocation consistently below wherever an example says `recon`.

## Start with canonical ownership

1. Run `recon query --vault "$RECON_VAULT"` with the narrowest relevant source, finding, tag,
   text, acquisition, tool, or date filters. Reuse sufficient prior coverage instead of scanning a
   harness-local `docs/recon` tree or reacquiring evidence already covered.
2. Produce the report bundle in a private temporary directory with bounded retention.
3. Select exactly one identity: `--source-url` for a fetched canonical source or `--inquiry-key`
   for topic research that has no honest canonical URL.
4. Invoke the canonical runtime's `record` command with the identity, acquisition method, and
   every approved report asset.

## Route the evidence need to a Recon capability

Recon is the sole durable web-acquisition funnel: name the evidence need, and let the runtime
resolve the backend. Recon owns the operation vocabulary — `discover`, `capture`, `map`,
`traverse`, `extract`, and `synthesize` — and an adapter maps onto it, never the reverse. No vendor
skill, command name, or flag is part of this contract, so nothing here needs a second acquisition
skill to be installed.

| Evidence need | Recon capability | Bounded route |
| --- | --- | --- |
| No canonical URL yet | `recon:research` | `discover`, select relevant sources, and capture only results that do not already carry sufficient fetched content. |
| Known public URL | `recon:research` | `capture`; retain the normalized source URL and capture date. |
| Bounded site section | `recon:research` | `map` to locate pages, then `capture` or `traverse` under explicit host, path, page count, byte, and duration bounds. |
| Report-scale synthesis | `recon:research` | `synthesize` for source diversity, uncertainty, contrary evidence, and open questions rather than a list of capture summaries. |
| Site's visual design system | `recon:design` | `capture` then `extract` into a versioned design evidence bundle, never a generic page scrape. |
| Scholarly evidence | `recon:papers` | `discover` and `extract` for seed discovery, related-work expansion, metadata inspection, and load-bearing claim verification. |
| Social source metadata | `recon:social` | `discover` only: X/Twitter stays candidate-only until an approved official or licensed API adapter exists, and YouTube stays channel Atom metadata. |
| Agent, skill, or workflow analysis | `recon:agents` | `map` and `extract` over another project's agents, skills, commands, and workflows. |

Every capability carries the same durable boundary this skill declares. A transient page lookup
with no report, reuse, or memory goal is declined with a bounded routing explanation and creates no
query ledger, vault record, or adapter job.

The resolved adapter is an implementation detail of that route. Its name and version survive only
as tool provenance on the recorded query rows; its job identifiers, signed URLs, session state, and
raw payloads are refused at the acquisition boundary rather than carried forward. If the configured
adapter is missing, unauthenticated, or unavailable, report that typed capability limitation and
name the failed adapter check. Another host-approved read-only web surface may be used when
available, but Recon does not implicitly authorize installation, authentication, guessing a
provider, or any action that would change harness defaults.

## Route design intent to `recon:design`

Design mining is a mode of this skill, not a second skill and not a generic page scrape. Route to
`recon:design` when a request asks to clone a site's look, copy or rebuild a page's styling, mine
or document a design system, extract design tokens such as color, typography, spacing, radius, or
shadow, capture layout and grid relationships, inventory repeated components, collect assets like
logos, icons, and fonts, or build reusable UI components from a live site. Acquire the pages
through the routes above; the acquisition backend is an implementation detail and no vendor command
is part of the design contract.

The mode's output is a versioned design evidence bundle. Validate and publish it before recording:

```bash
recon prepare-design \
  --bundle /tmp/recon-stage/design.bundle.json \
  --artifact /tmp/recon-stage/report.md \
  --artifact /tmp/recon-stage/home-desktop.png \
  --output-dir /tmp/recon-stage/design
```

A bundle carries `design_bundle_version`, the normalized `source_url`, an RFC 3339 `captured_at`,
the acquiring `tool`, a `capture_policy` of viewports plus bounds, `entries`, `coverage`, and
`limitations`. Each entry is one `token`, `layout`, `component`, `asset`, or `screenshot` with an
`id`, a `value`, an `anchor`, an `observed`, `derived`, or `recommendation` `classification`, a
`low`, `medium`, or `high` `confidence`, and `limitations`. Four rules keep a bundle from turning
inference into fact:

- **Anchor every retained entry** to a recorded artifact, such as `report.md#tokens` or
  `home-desktop.png#.product-card`. An observation whose anchor resolves to no artifact is refused,
  so nothing is retained without the evidence it was read from.
- **Keep media bounded and content-addressed.** An `asset` or `screenshot` entry references
  `source_url`, `sha256`, `bytes`, and `media_type`, capped at 2 MiB per file; per-kind retention
  caps are 200 tokens, 50 layouts, 50 components, 100 assets, and 10 screenshots. State anything
  dropped past a cap in `limitations` instead of dropping it silently.
- **Label inference separately.** A `derived` or `recommendation` entry must state at least one
  limitation and stays separate from `observed` values and human-authored interpretation.
- **Make missing visual states explicit.** A declared viewport that produced no screenshot belongs
  in `coverage` as `partial` or `unavailable` with a reason. Never infer a visual state that was
  not captured, and never claim pixel equivalence.

The published `design.json` is an ordinary artifact: record it beside the report through the same
canonical write as any other evidence.

## Emit UI-library inputs as a design output mode

Generating UI-library code from a mined site is an output mode of that same bundle, not a separate
capability and not a separate package skill. Generate only from the published `design.json` and its
recorded artifacts, and keep the bundle's classification boundary intact in whatever is emitted:

- `observed` entries supply concrete values. Emit them as tokens, variables, or component props and
  carry each entry `id` and `anchor` into the generated output so every value stays traceable to
  its evidence.
- `derived` and `recommendation` entries are proposals, not facts. Emit them as marked suggestions
  with their limitations attached and leave acceptance to a human.
- Where `coverage` is `partial` or `unavailable`, leave the gap explicit in the generated output.
  Do not invent a hover state, breakpoint, theme, or token that the capture never observed.
- A generated library is a Recon consumer, not a second evidence store. Regeneration re-reads the
  recorded bundle rather than refetching the live site.

## Keep acquisition read-only

A Recon request authorizes bounded collection from the read-only public web. It does not grant the
separate authority required for:

- installation, authentication, login, credentials, profiles, or export of authenticated data;
- feedback telemetry, monitoring, schedules, email, webhook, or other persistent state;
- local-file upload or export of private, personal, regulated, or credential-bearing material; or
- form submission, purchases, messages, cart changes, and other externally visible actions.

Do not add one of these effects merely because the resolved adapter supports it. Follow Recon's
declared bounds and host policy for any separately authorized higher-effect action.

## Hand off one scrubbed evidence bundle

Treat adapter output, including a `.firecrawl` folder or any other provider job store, as temporary
acquisition material rather than a second evidence store. Before recording, reduce the working set
to:

- the synthesized report and approved supporting assets;
- normalized source URLs and capture dates;
- collection scope and bounds;
- failures, access limitations, and unresolved uncertainty;
- explicit labels separating observed evidence from inference; and
- stable rerun inputs plus safe tool/version provenance.

Exclude secrets, session data, signed URLs, credentials, unnecessary personal data, and raw
transient outputs.

Whenever an acquisition adapter contributes evidence, author both closed draft ledgers in that same
private temporary directory before recording:

- `queries.draft.jsonl` has one query row per material acquisition. Each row uses a unique local
  `query_key` plus acquisition kind and purpose, normalized input, scope and bounds, safe rerun data,
  tool/version provenance, timing, status, result URLs, and limitations.
- `findings.draft.jsonl` has one finding row per retained claim. Each row uses a nonempty
  `query_keys` array plus title and verbose detail, evidence/inference classification, confidence,
  evidence URLs and capture dates, a report artifact anchor, limitations, and tags.

The recorded acquisition class names the adapter that actually ran, not a route the caller picked:
record `firecrawl` when the Firecrawl adapter performed the acquisition and `mixed` when it
contributed to a broader bundle. Both require the two complete scrubbed ledgers, and both keep
replaying unchanged for records written before Recon owned the routing. Do not invent empty
placeholder rows or compute deterministic IDs yourself. Ask the runtime to validate aliases,
resolve query references, and publish the canonical pair:

```bash
recon prepare-ledgers \
  --queries-draft /tmp/recon-stage/queries.draft.jsonl \
  --findings-draft /tmp/recon-stage/findings.draft.jsonl \
  --artifact /tmp/recon-stage/report.md \
  --artifact /tmp/recon-stage/report.html \
  --output-dir /tmp/recon-stage/prepared
```

Only after preparation succeeds, invoke `recon record` as the sole canonical write:

```bash
recon record \
  --vault /path/to/recon/vault \
  --source-url https://github.com/owner/repo \
  --source-type git \
  --acquisition firecrawl \
  --queries /tmp/recon-stage/prepared/queries.jsonl \
  --findings /tmp/recon-stage/prepared/findings.jsonl \
  --artifact /tmp/recon-stage/report.md \
  --artifact /tmp/recon-stage/report.html
```

For acquisition `none` or `other`, absence of Firecrawl and absence of ledgers are nonfatal. This
keeps repository-local and other ordinary Recon recording available without installing or
authenticating any acquisition adapter. If either ledger is supplied voluntarily, supply and
validate both.

The record is source-addressed at
`vault/.mx/evidence/sources/<source-id>/recon/<recon-id>/`. Do not create a mirror, symlink, or
sidecar in a harness-owned vault. Do not retain `.firecrawl`, a harness-local folder, or any other
adapter job store as a second evidence store. Unknown legacy artifacts must be imported through
`recon import-legacy`, which quarantines them for identity review rather than guessing a target.
