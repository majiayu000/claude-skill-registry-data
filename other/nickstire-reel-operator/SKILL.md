---
name: nickstire-reel-operator
description: Run the Nick's Tire & Auto Faceless Reel Intelligence Operator — turn a driver problem into a scored Reel concept, then a production pack, draft, or (only with explicit live operator authorization) a publish. Use this whenever asked to research/ideate Reel topics, produce a Reel production pack, render/QA a draft Reel, or run any INTELLIGENCE/PRODUCTION/DRAFT/PUBLISH/SCHEDULED mode for nickstire's Instagram/Facebook Reels. Grounds every "connected route," "claim registry," "repetition ledger," and "quality gate" in this operator spec against the real files that implement them in this repo, and states plainly which parts of the spec (live model catalog/pricing, music-rights ledger) have no real read-back here yet. Read this before running any reel content-generation task, and read `nickstire-verifier-reel-pipeline` first if the task is instead about verifying pipeline *code changes* rather than producing Reel content.
triggers: reel, reels, faceless reel, reel concept, reel topics, production pack, driver problem, instagram reel, publish a reel, reel draft, ideate reels, scored concept
---

# Nick's Tire & Auto Faceless Reel Intelligence Operator (v2)

This is the operator spec the user handed down, grounded against what actually
exists in this repo. No v1 of this skill was in the repo — this file is
authored fresh, file-by-file verified 2026-08-14, not transcribed from memory.
Where the spec asks for a capability this repo doesn't expose yet (a live
Higgsfield price/plan API, a formal music-rights ledger), that gap is named
explicitly below rather than papered over — inventing a receipt is exactly the
failure this spec exists to prevent.

## Hard rule — read before anything else

**Never run a real generation, spend, or publish action from this skill
without a live, in-the-moment operator instruction for that specific run.**
This mirrors both the spec's own PUBLISH rule ("Never infer publish permission
from a heartbeat, prior approval, a scheduled task, or a previous post") and
root `AGENTS.md`'s protected-operations list ("Customer-facing side effects —
... social/GBP publishing ... Build preview/draft/copy-only"). A stored
scheduled prompt, a prior session's approval, or a `publish_authorized=true`
flag inside non-live content does **not** satisfy this. If in doubt, the
correct output is `READY FOR HUMAN APPROVAL`, not a publish attempt.

Two concrete hazards from `.claude/skills/nickstire-verifier-reel-pipeline/SKILL.md`
apply here too and are not repeated in full:
1. The repo's only `DATABASE_URL` is **production TiDB** — any real DB read in
   this workflow (repetition ledger, quality-score re-check, job status) is a
   prod read, and `processNextAssemblyJob`/`processNextReelJob` **claim and
   mutate real jobs**, not just observe them.
2. `POST /api/admin/reel-canary` with `action:"publish"` and
   `instagramAdmin.publishPost` both post to the real `@nicks_tire_euclid`
   account. `contentAdmin.generateAndPublishLiveTestReel` spends real money AND
   publishes in one call — never use it as a "just testing" handle.

## Run modes → real routes

| Spec mode | What it does here | Real entry point |
|---|---|---|
| `INTELLIGENCE` / `SCHEDULED` | research, score, return packs; render/publish nothing | read-only: `reelRepetitionHistory.ts`, `businessFacts.ts`, `evidenceResolver.ts`; no `reel-canary` calls at all |
| `PRODUCTION` | one approved concept → production-ready pack; render only through connected, verified routes | `POST /api/admin/reel-canary {action:"start", topic}` compiles a brief (`reelBriefGen.ts` + `reelDraftPrep.ts` preflight) — this alone does not render clips |
| `DRAFT` | render + QA a finished asset, do not publish | `{action:"advance"}` repeatedly until `status:"assembled"`, then `{action:"qa"}`. **Never call `{action:"publish"}` in this mode.** |
| `PUBLISH` | publish, only with explicit live `publish_authorized=true` + exact asset | `{action:"publish"}` (canary) or `instagramAdmin.publishPost` (human-approval door, hash-checked) — only when this session has that live instruction *right now* |
| `SCHEDULED` | identical to `INTELLIGENCE`; never publishes automatically | same as `INTELLIGENCE` — a cron/scheduled firing is exactly the case the hard rule above blocks from `PUBLISH` |

The daily autonomous cron (`server/cron/jobs/dailyReelPost.ts`, tier
`daily-reel-post` + `reel-pipeline`) already runs its own enqueue→render→
QA-gate→publish loop when `REEL_AUTOPOST_ENABLED=true`. This skill is for an
operator- or session-driven run, not for reimplementing that cron — check
`REEL_AUTOPOST_ENABLED` before assuming a manual run is the only thing posting
today (the day's feed-post cap in the guardrail table below is shared).

## Capability and cost preflight — what's real, what's not

The spec asks for a live model catalog, plan tier, and per-call pricing read.
This repo does **not** expose that:

- `getHiggsfieldAccountHealth()` (`server/services/higgsfieldStudio.ts:542`)
  is the only live capability probe — read-only (`hf account status`), returns
  `credsValid` and a best-effort regex-parsed `balanceCredits` (`null` if the
  CLI's text doesn't match). It does **not** return a model catalog, a plan
  name, or per-call USD.
- Per-clip cost is an **operator-tunable estimate**, not a metered price:
  `COST_ESTIMATES_USD` in `server/services/generationLedger.ts` —
  `seedance_clip: 0.25` (labeled ASSUMPTION in the source comment),
  `template_stock_clip: 0` (free local ffmpeg lane), `veo_second_720p: 0.10`
  (Google-published, the one real metered figure). Treat any other
  "current Higgsfield price/plan" claim as `UNKNOWN` — do not invent one.
- Route selection is `REEL_VIDEO_PROVIDER` (env pin) — per
  `docs/operations/REEL-PIPELINE.md`, **prod currently pins `template_stock`**,
  not Higgsfield/Seedance; re-read that env var before assuming the HERO route
  is the paid model. `REEL_FALLBACK_TO_TEMPLATE_STOCK` governs degrade-not-dark
  behavior when a paid provider hits a terminal verdict.
- Spend accounting is real and structured: `generationLedger.ts` implements
  RESERVE → SETTLE/RELEASE against `policy.limits.maxGenerationCostPerDayUsd`
  (read from the latest `autonomy_policy_versions` row, 30s cache). Estimate
  the run's cost against this ledger's numbers before generating, per the
  spec's credit rules — but report the estimate as an estimate, and the
  balance as `UNKNOWN` when `getHiggsfieldAccountHealth()` can't parse it.

- Before changing a paid request to save money, quote both settings with the
  vendor's no-submit preflight (`get_cost:true` on the Higgsfield MCP) and keep
  the change only if the quote moves. A reseller's price structure is not the
  vendor's: "request Seedance clips silent" was built, tested and reverted on
  2026-10-08 because audio off costs the same as on (12 credits at 1080p;
  recorded in `docs/UPSTREAMS.md`, 2026-08-29).

HERO/SUPPORT/REFERENCE/AUDIO routing from the spec maps to `higgsfieldStudio.ts`:
`generateReelClipVideo()` (line 435, one call per beat, accepts
`{prompt, negativePrompt, startImageUrl}`) and `stitchVideos()` (line 583,
downloads + ffmpeg-concats). There is one anchor-then-support pattern already
built for continuity: `REEL_IMAGE_CONDITIONING` passes a screened hero frame
as `--start-image` (a local file path, not a URL — that was a real prior bug,
fixed) so every beat shares one object/environment.

## Truth and evidence contract → real subsystems

- **Dynamic claims (price, warranty, hours, policy):** `businessFacts.ts` —
  `business_facts` table (operator-editable) falling back to code `SEED_FACTS`
  (git-versioned, sourced from the shop's actual invoice terms). Every fact
  carries `source`, category, and channel scoping. **Gap to flag, don't paper
  over:** `FactChannel` today is `"sms" | "voice" | "web"` only — there is no
  `"reel"` or `"social"` channel yet, so a Reel script pulling a business fact
  is not currently channel-scoped by this store. Treat that as `BLOCKED` for
  any fact this store hasn't explicitly cleared for public/video use, not as
  an implicit yes.
- **Claim-level evidence (mechanic truth, safety, sourced facts):**
  `evidenceResolver.ts` → `evidenceRecords.ts` (structured `EvidenceRecord`:
  `claim`, `assertion`, `sourceType`, `retrievedAt`, `expiresAt` per
  `EVIDENCE_TTL_DAYS` — 180d db / 365d public-registry, `snapshotHash`,
  `entailment` verdict from `shared/claimEntailment.ts`). `entailment` stays
  `"not_evaluated"` when only provenance exists (a title/URL is not a
  quotable statement) — publication must treat anything below `"supported"`
  as needing a qualifier or a human, exactly as the spec's `UNKNOWN` rule says.
- **Claim-safety wording (no prices in-reel, no guarantees, no fearmongering):**
  the pattern banks and approved soft-language list live in
  `client/src/lib/facelessReelStudio.ts` (validators run at brief-build time)
  — approved phrasing: *can point to · may indicate · worth checking · one
  clue · do not guess · stop by and we'll take a look.*
- **A prohibited-claim pattern is tested on the denial and the hedge, not only
  the claim.** For each new pattern add one denial ("not always X", "doesn't
  mean Y") to SAFE and one softened claim ("probably", "usually", "perfectly")
  to the hedged table; the brake, E-Check and no-start packets refused five
  correct myth-busting lines and passed eight hedged claims (2026-10-09).
  `mechanicalTruth.test.ts` also runs every packet's own facts and reasons
  through every pattern.
- **Local/weather/event claims:** no verified live source is wired into this
  pipeline today. Label `UNKNOWN` and omit rather than assume Cleveland
  weather or a local event is current.

## Motion-first floor and quality scoring

`calculateReelQualityScore()` (`client/src/lib/facelessReelStudio.ts`,
imported by `routers/content.ts` and `services/reelDirector.ts`) is the real
75-point gate, **min 70/75 to pass**, and the server **re-scores at enqueue**
(`content.generateReelBrief` scores it once client-side, `enqueueReelJob`
re-runs it — don't trust a client-only score). Weights: first-frame
scroll-stop 10 · muted-first 10 · beat structure 5 · length 5 · loop 5 ·
sourced fact 10 · faceless 10 · claim safety 10 · keyword 5 · winning
concept ≥57/60 5.

Separately, the **render-integrity gate** (in `reelAssembly.ts`, "#800/#801")
proves the motion floor on the *actual rendered file*, not the brief: container
duration within 0.75s of the storyboard contract (beats + 3s SAVE freeze),
video-stream duration within 0.75s (container duration lies via the audio
track when the video track ends early), ≥80% of expected 30fps frame count,
and ≥3 distinct MD5s among 5 sampled frames (motion proof — this is exactly
the spec's "one still image / repeated loop is not a finished Reel" rule,
enforced mechanically, not just as a brief). A violation throws; the job
retries/fails loudly rather than silently downgrading.

## QA gates → real modules

| Spec gate | Real module | Notes |
|---|---|---|
| Rendered QA / vision critic | `renderedQa.ts` | vision critic scores real frames; verdict persisted at `payload.renderedQa` on the `reel_jobs` row |
| Repair routing | `repairRouter.ts` | prices a beat regen at the ACTIVE provider's cost (`generationLedger.ts`); on the free `template_stock` lane this returns `auto_repair` instead of `needs_paid_repair` |
| 7-way decision | `qualityAutomation.ts` (`decideAutomation`) | folds critic verdict + repair-attempt count + policy cap |
| Consolidated publish gate | `qualityGate.ts` (`evaluateReelPublishGate`) — **the one gate every autonomous door consults** | returns `PublishGate \| EvidenceGate`: `proceed` / `auto_repair` / `needs_paid_repair` / `pause` / `reject` (from `postQaOrchestrator.ts`), or an evidence gate `unavailable` / `stale` / `needs_review` / `disabled` when the evaluation itself is incomplete. **Absence of evidence is never evidence of quality** — QA-unavailable still requires an explicit `disabled`-by-policy or `unavailable` state, never a silent pass |
| Human-approval doors | `instagramAdmin.publishPost`, `instagramStudio` | these keep hash-checked approval-integrity as their own gate — a person is already in the loop, so `evaluateReelPublishGate` is not re-enforced there the same way |

Use `PASS` / `FAIL` / `UNKNOWN` / `BLOCKED` per the spec, but back every `PASS`
with the actual field read (job row, gate return value, ffprobe output) — "the
render command exited 0" or "a `jobId` came back" is explicitly **not**
evidence of a finished or published Reel, in this repo's own words
(`docs/runbooks/reel-pipeline.md`).

## Repetition and learning ledger → real read-back

`reelRepetitionHistory.ts` → `getRecentReelSignals(daysBack = 21)` reads the
`reel_jobs` table (any status — a rejected/failed brief still consumed its
topic), capped at 100 rows, ordered by recency, degrades to "no memory" on a
DB outage rather than throwing. Feeds `buildRepetitionChecks` in
`facelessReelStudio.ts`. Since 2026-08-13 (#1558) a brief can also be
rejected purely for topic repetition inside the daily cron's own attempt
loop — that shows up as `PreflightExhaustedError` with a message distinguishing
"topic repetition only, no preflight defect" from an actual generator defect.
There is no separate creative-fingerprint table beyond this — `creativeMemory.ts`
/ `creativeVault.ts` / `criticPanel.ts` / `conceptTournament.ts` hold the
tournament and critic machinery, not a second repetition store.

## Guardrails an enqueue/publish can hit (real, not hypothetical)

From `docs/runbooks/reel-pipeline.md`, enforced by `autonomy_policy_versions`
(`limits.*`), checked in this order — a block here is the system working:

`RESERVATION_FEED_CAP` (posts/day, currently 2) → `RESERVATION_SPACING`
(hours between feed posts, currently 3) → `REPEAT_CTA` (72h) → `REPEAT_TOPIC`
(7 days) → `BUDGET_DAILY_EXCEEDED` (`maxGenerationCostPerDayUsd`, currently
$10). Preflight (M10, in `reelDraftPrep.ts`) runs **before** the reservation,
so a preflight block leaks nothing; a reservation is created before the spend
boundary, so a post-reservation DB error can leak a slot — check
`content_reservations` if the day's cap looks wrong.

## Audio and music rights — real gap

The spec requires asset ID, source, license scope, territory, expiry, and
organic/ad clearance for every music/audio asset. **No rights ledger for
music exists in this repo.** Voice generation goes through `reelVoice.ts`
(see `nickstire-verifier-reel-pipeline` for its fail-closed contract); there is no
tracked license record for a music bed. Treat any music-rights field as
`UNKNOWN`/`BLOCKED` rather than asserting a track is cleared — this is a real
capability gap, report it as one in the run receipt's credit-risk/fallback
section, don't silently drop the rights row from the pack.

## Producing a pack when the motion route is unavailable

If `REEL_GENERATION_ENABLED` is not `true`, credentials are dead
(`getHiggsfieldAccountHealth().credsValid === false`), or this session has no
path to call `/api/admin/reel-canary` (e.g. a non-prod session, no
`ADMIN_API_KEY`), do not silently downgrade to a stills-with-voiceover
deliverable. Return `BLOCKED: NO MOTION ROUTE` **or** a full production-ready
pack (script, per-beat Higgsfield-style prompts with the standing negative
prompt `faces, hands, human figures, on-screen text, logos, watermarks,
subtitles`, SRT captions, ffmpeg/CapCut assembly instructions matching the
render-integrity contract above, IG/FB copy) — exactly the two options the
spec allows, never a quietly weaker asset presented as finished.

### Where the pack goes — one location, not a new one each run

    apps/nickstire/docs/reel-packs/<YYYY-MM-DD>-<slug>/
        README.md      the pack: script, per-beat prompts, assembly, IG/FB copy
        captions.srt   captions, when produced
        brief.json     machine-readable brief, when produced

**Use this path. Do not invent another.** Between 2026-08-14 and 2026-08-15,
eight scheduled runs produced eight packs in **eight different directories** —
`docs/marketing/faceless-shorts/`, `ad-factory/<date>/`, `reel-brief-pack/<date>/`,
`apps/nickstire/docs/content-packs/`, `apps/nickstire/docs/content/reel-packs/`,
and three variants of a bare `REEL-PACK-*.md` at the docs root. Three of them
covered the SAME topic. Every run was individually reasonable; none could see the
others, because this file described how to produce a pack and never said where to
put it.

A directory per pack (not a date-prefixed flat file) because a pack is several
files and grows more — `brief.json` exists on exactly one of the eight, and it is
the only one a pipeline can consume without a human re-typing it.

Before writing, check BOTH — the directory only shows MERGED packs, and every
reel pack opens as a draft PR:

    ls apps/nickstire/docs/reel-packs/
    gh pr list --state open --search "reel pack in:title"

The second command is not optional. On 2026-08-16 three runs fired within two
hours; #1610 duplicated #1607's battery topic exactly, because at 20:36 #1607 was
still an unmerged draft and therefore invisible to `ls`. Checking only the
directory is blind during precisely the window when collisions happen.

### Pack authoring checks

- **A real-footage requirement is declared on the beat, not in prose.** If a
  shot must be real, put `source: "real"` on that beat; the generator then
  refuses it until the footage exists. Prose in `modelRecommendation` or
  `creditEfficiencyNote` is read by no gate (2026-10-08: 22 rotation packs ask
  for real footage in prose, none on a beat, and 14 of the research's 62 picks
  carry a "0 credits" note while the lane would charge about 60 credits each).
- **An imported pack must name what the camera sees in every beat.** Before
  admitting packs, print beat 1's provider prompt for each
  (`buildHiggsfieldReelPromptPack`) and read its `Subject:` line. A subject a
  viewer could not name ("the physical subject", "the relevant components") is
  not a shot; `beatGenerationRoute` holds such beats (`needs_subject`). 34 of 34
  packs from the 2026-09-25 imports failed this.

## Backlog ceiling — when NOT to add a new pack

By 2026-09-07 this trigger had fired often enough that 16+ consecutive runs each
independently re-derived "content supply is not the bottleneck" (see
`apps/nickstire/docs/reel-packs/BACKLOG-STATUS-*.md`) — nothing short-circuited the loop, so
every firing paid the full analysis cost to reach the same place. Check the ceiling below
BEFORE drafting a new topic so this firing doesn't become #17.

A new pack is only worth producing if the backlog can eventually post it. The real constraint
is `RESERVATION_FEED_CAP` (2 posts/day, guardrail table above) and
`drizzle/0112_reel_publish_approvals.sql` — until an operator confirms that migration is
applied to production TiDB, `evaluateReelPublishGate`'s human-approval door stays shut and
**nothing in the backlog can publish, no matter how large it is.**

Before drafting, count both (the same two checks as above already give you this):

    ls apps/nickstire/docs/reel-packs/ | grep -c '^2026-'   # merged packs
    gh pr list --state open --search "reel pack in:title"  # + open ones

If merged + open is already many times what `RESERVATION_FEED_CAP` could post in a couple of
weeks (2/day × 14d = 28 — merged alone was 166 as of 2026-09-07), **do not open a new
content-pack PR.** Instead write `BACKLOG-STATUS-<date>.md`: today's capability preflight (one
line — it hasn't changed in weeks), current pack count, any clean/green stranded PRs you
merged this run, and a one-line pointer to the standing ask below. Don't re-litigate the
argument each time — link the newest prior `BACKLOG-STATUS-*.md` instead of restating it.

**Standing ask, carried forward until an operator responds — do not re-argue it, just
reference it:** reduce or pause this trigger's firing interval, and get an explicit operator
decision on `0112_reel_publish_approvals.sql`. Neither is actionable from inside a firing.
`PushNotification` for this was already sent once — don't repeat it; a `BACKLOG-STATUS-*.md`
note per firing satisfies "informed" without adding interruption noise.

The ceiling does not relax the hard rule above. A firing under the ceiling still never
generates, spends, or publishes without live, in-the-moment authorization — the ceiling only
decides whether drafting a new *pack* (a docs-only PR) is worth the cycle at all.

## Required final response

Follow the spec's 9-point receipt shape. Map its generic asks onto this
repo's real evidence sources rather than narrating them abstractly:

1. mode, timestamp, connected capabilities (`getHiggsfieldAccountHealth()`
   result, `REEL_VIDEO_PROVIDER`, `REEL_GENERATION_ENABLED`), repetition-ledger
   context (`getRecentReelSignals()` output).
2. candidate scores (0–5 per dimension) and selected/parked concepts.
3. claim evidence — cite `EvidenceRecord`s and `businessFacts` rows actually
   read; list `UNKNOWN`s explicitly, don't omit the section when everything's
   unverified.
4. full production pack for the selected concept.
5. credit-risk and fallback routing — read from `generationLedger.ts`
   estimates + the day's `autonomy_policy_versions` limits, not guessed.
6. audio/music rights status — real gap above; say so.
7. QA matrix — `PASS`/`FAIL`/`UNKNOWN`/`BLOCKED` per gate in the QA table
   above, each backed by an actual read (job row, gate return, ffprobe).
8. IG/FB copy + two ad-ready hook/caption/CTA variants.
9. final status: `PRODUCTION-READY` / `READY FOR HUMAN APPROVAL` /
   `BLOCKED: <reason>` / `PUBLISHED WITH READ-BACK` — the last one only ever
   follows an actual `igPostId`/permalink read-back from
   `publishToSocial`/`instagramAdmin.publishPost`, never from a `jobId` alone.
