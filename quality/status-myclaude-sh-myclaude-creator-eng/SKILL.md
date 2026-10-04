---
name: status
description: >-
  Display Studio Engine status dashboard. Shows version, edition, creator profile,
  products with scores, and stale warnings. Use when: 'status', 'dashboard', 'show my
  products', or at session start.
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Status Dashboard

Display comprehensive engine status in a compact terminal-style dashboard.

**When to use:** Session start, or anytime the creator wants a status overview.

---

## Activation Protocol

### Step 0 — SHARED PREAMBLE
Load `references/quality/activation-preamble.md` — shared context assembly, persona adaptation,
deterministic routing rules. This runs before any skill-specific logic.

### VOICE LOAD

Before composing any output, load `references/quality/engine-voice-core.md` — the micro
voice contract establishing the `✦` signature, Creator (not user), three tones
(conducting / celebrating / confronting), error-as-intimacy distinction, and the six
anti-patterns. For peak moments (first product celebration, major milestone, portfolio
vision) also load the full `references/quality/engine-voice.md` per the UX Integration
Stack below.

### EXEMPLAR LOAD

Load `references/quality/exemplar-outputs.md` sections E1 and E2 only. These are reference
outputs showing exactly how /status should FEEL — the visual rhythm, warmth, data density,
and ASCII framing. Your output MUST carry the same energy. Reason about your creator's
context and adapt — never copy verbatim.

### RITUAL OF RETURN — 3 LAYERS

**Purpose.** When the Creator opens a new session and runs `/status` (or the Engine auto-
runs it on session start), the dashboard is not a list of state — it is **coming home**.
Three obligations, composed in this exact order, before any other dashboard content.

**Precondition.** Read `STATE.yaml → engine.last_session_at`. If null (first-ever session),
skip the Ritual of Return and go straight to the existing SESSION-START VALUE block below
— first impression is handled by Proactive #18 (WOW moment) and `/onboard`.

If `engine.last_session_at` is present, the ritual fires. It is the first thing the
Creator sees, in creator.language, in the Master Craftsperson voice.

#### Layer 1 — Interval since last session (emotional contact)

Compute `interval = now - engine.last_session_at`. Render a single line opening with `✦`
that acknowledges time passed. Interval-aware phrasing:

| Interval | English | Portuguese |
|---|---|---|
| <1 hour | *"✦ Back already, {name}."* | *"✦ De volta rapidinho, {name}."* |
| 1-6 hours | *"✦ Welcome back, {name} — a few hours in."* | *"✦ De volta, {name} — algumas horas depois."* |
| 6-24 hours | *"✦ Welcome back, {name}. Same day."* | *"✦ De volta, {name}. Mesmo dia."* |
| 1-3 days | *"✦ Welcome back, {name}. {N} days since last session."* | *"✦ De volta, {name}. {N} dias desde a última sessão."* |
| 4-14 days | *"✦ Welcome back, {name}. It's been {N} days."* | *"✦ De volta, {name}. Fazem {N} dias."* |
| 15-30 days | *"✦ Welcome back, {name}. {N} days out — good to see you."* | *"✦ De volta, {name}. {N} dias fora — bom te ver."* |
| >30 days | *"✦ Welcome back, {name}. Over a month — picking up where we left off."* | *"✦ De volta, {name}. Mais de um mês — retomando de onde paramos."* |

Pick the `{name}` field from `creator.yaml → creator.name`. If absent, fall back to
*"Welcome back"* / *"De volta"* without a name. Never fabricate a name.

#### Layer 2 — The diff (what changed since you were gone)

Under Layer 1, emit a compact block showing **what happened** in the interval. Read in
order:

1. `STATE.yaml → decisions_history` HOT (last 50 entries) — any entries with
   `date > last_session_at`? Count them as "new forges logged".
2. For each product in workspace: compute if `state` or `last_validated` changed since
   the interval start.
3. If `myclaude stats --json 2>/dev/null` is available: compute delta on total installs
   across all published products since last session.
4. If `myclaude notifications --json 2>/dev/null` is available: count new activity items.
5. Scan `workspace/scout-*.md` — any new scout reports since last session?
6. **Creator-memory micro-echo.** Read `creator-memory.yaml` if present.
   Pick the most recent event where BOTH (a) `date < engine.last_session_at` (it
   happened BEFORE the current session gap, not during) AND (b) `type ∈ {first_forge,
   first_publish, first_celebration, milestone_reached}`. If a matching event exists,
   emit one additional line of continuity — a specific echo from the past grounded in
   a concrete marker:
   > *"Remember: on {date_short} you celebrated {slug} — now at {current_install_count}."*
   > *"Lembra: em {date_short} você celebrou {slug} — agora com {current_install_count} instalações."*
   If `creator-memory.yaml` is absent OR no matching event exists OR `engine.last_session_at`
   is null, skip silently. Never fabricate a memory. Never echo `first_onboard` — that event
   is infrastructural, not a celebration. Rate-limit: at most one memory echo per Ritual of
   Return invocation. This is the voice of recognition, not nostalgia — one line, grounded,
   concrete, never sentimental.

Render the diff as 2-5 lines. Only include lines that are non-zero. Voice: craft-specific
numbers, not vague. Examples:

```
Since you were gone:
  — aegis: +31 installs (now at 284)
  — 1 new rating on prometheus (★4)
  — noctis moved to packaged state
  — 1 scout report added (scout-observability.md)
```

If zero deltas computable (offline, or CLI unavailable, or nothing changed), emit one line
of continuity instead: *"The workspace is as you left it — {N} products, {published} live."*
Never fabricate deltas. Zero signal is an honest signal.

#### Layer 3 — Next move inferred (contextual intelligence)

Below the diff, propose **one next action**, inferred from context. Never two. Pick using
this priority order:

1. **Active task in current_task** (STATE.yaml `current_task.skill` != null) → *"Where we
   were: {skill} on {slug}, {phase} phase. Next move: continue where we left off."*
2. **Product in terminal-but-not-final state** (packaged but not published, validated but
   not packaged) → *"{slug} is {state}. The natural next step is {command}."*
3. **Recent scout report with no forge yet** (scout in last 14 days, no product from
   its recommendations) → *"Your scout for {domain} has {N} recommended products and zero
   forged. The first one is {recommendation_name} — want to build it?"*
4. **Portfolio pattern** (3+ products in same domain without bundle) → *"You have {N}
   products in {domain}. They would compose into a strong bundle — want me to sketch it?"*
5. **Stale product that was last-touched before the interval** → *"{slug} has been in
   {state} for {N} days — pick it up again with {command}?"*
6. **Nothing specific** (clean workspace, no active task, no stale, no patterns) → *"No
   active task. Next move is yours — /create to start something new, /scout to research a
   domain first, /explore to see what others built."*

The inference reads decisions_history (HOT), last_scout, current_task, and portfolio
state in parallel. First rule that matches wins. Never stack multiple suggestions — that
is exactly the confusion P10 forbids.

**Rate limiting.** The full Ritual of Return fires **once per session**, on the first
`/status` invocation. Subsequent `/status` calls in the same session skip Layer 1 and 2
(the Creator is already "home") and go straight to the existing dashboard.

**Session close.** On session close (Stop hook or session end), write
`STATE.yaml → engine.last_session_at = now()` and increment `engine.sessions_total`. If
no Stop hook is wired, the next `/status` invocation writes it as a side effect of
computing the interval. Never fail to update — losing the timestamp breaks the ritual
for the next session.

---

### SESSION-START VALUE (automatic on first /status)

Before displaying the dashboard, scan for actionable intelligence:

1. **Stale products**: Any product with `last_validated` > 30 days ago → surface with warning
2. **Next action**: For each product in non-terminal state, suggest the logical next command:
   - scaffold → "Run /fill to add content"
   - content → "Run /validate to check quality"
   - validated → "Run /package to bundle for distribution"
   - packaged → "Run /publish to ship to marketplace"
3. **Score trajectory**: If score_history exists in .meta.yaml, show trend arrow (↑↓→)
4. **Creator pattern insight**: If usage.common_dna_gaps has entries, surface: "Tip: D{N} ({name}) is your most common gap. [link to structural-dna.md section]"

### MILESTONE DETECTION — creator-memory milestone_reached writer

On first `/status` invocation per session, after SESSION-START VALUE scanning and before
rendering the dashboard, check whether any of four concrete milestone conditions have
just crossed. For each condition that is newly satisfied AND has not already been recorded
in `creator-memory.yaml`, append a `milestone_reached` event. Idempotent — a milestone
fires at most once ever per Creator.

The milestone layer is the long-horizon complement to first_* events: where first_*
events mark the single entry into a new phase of the Creator's journey, milestones mark
each subsequent threshold worth acknowledging without becoming noise.

**The four triggers (extensible):**

| # | Condition (all exact) | Note template |
|---|---|---|
| M1 | `count(products where any forge event exists) == 5` — measured by counting `.meta.yaml` files under `workspace/[!.]*/` that contain an `intent_declaration` block OR by counting entries in `STATE.yaml decisions_history` with a unique `slug`, whichever is larger | `"5th forge — {newest_slug} joins a growing portfolio of 5 products"` |
| M2 | `count(products where state.phase == "published") == 10` | `"10th publish — {newest_slug} is the 10th product shipped"` |
| M3 | `any published product has user_rating >= 5 AND no prior rating >= 5 has been recorded in milestones` — read `outcome_30d.user_rating` from each decisions_history entry OR fetch `myclaude stats --json 2>/dev/null` for each published product if available | `"First ★5 — {slug} received its first perfect rating"` |
| M4 | `count(products where intelligence.domain == X) >= 3` for some X AND no existing bundle product exists for domain X AND this condition was NOT true before the most recent forge | `"3 products in {domain} — {domain} is now a portfolio cluster, bundle candidate"` |

**Deferred triggers.** Sessions_total milestones (100, 500, 1000) depend on the Stop hook
honoring real session boundaries. Until `sessions_total` carries honest session-count
semantics, adding these triggers would produce false celebrations on Creators who ran
a dozen Bash batches. Leave deferred until the semantic is verified.

**Procedure for each trigger condition:**

1. Evaluate the condition against current workspace state + STATE.yaml + creator-memory.yaml
   in parallel. All four checks are read-only until one fires.
2. For any condition that evaluates to true, read `creator-memory.yaml events[]` and check
   whether a `milestone_reached` event with a `note` starting with the same milestone
   prefix (`"5th forge"`, `"10th publish"`, `"First ★5"`, or `"3 products in"`) already
   exists. Idempotent — if the milestone already fired, skip.
3. If the milestone is new, append an event:
   ```yaml
   - date: "{ISO-8601 now UTC}"
     type: milestone_reached
     slug: "{the slug that caused the milestone, or the portfolio cluster name for M4}"
     note: "{template from the table above, ≤140 chars}"
   ```
4. Validate with `python scripts/creator-memory-validate.py`. Rollback on validation
   failure, surface an Engine-fault voice line at the bottom of the dashboard:
   > *"(Memory layer — failed to record milestone. The milestone is real; only the echo is missing.)"*
5. Never render the milestone line in the current `/status` output — the milestone is
   recorded for future Ritual of Return echoes. The dashboard's job is to show state;
   the ritual's job is to carry memory forward. Keeping them separate prevents the
   milestone from stacking with a Layer 1 celebration line on the same session.

**Voice register.** Silent infrastructure. The milestone is visible to the *next* session,
not this one. The exception is a milestone that crosses while the Creator is watching —
if, for example, `/publish` just shipped the 10th product and `/status` is the next
command in the same session, Step 6 of publish already showed the celebration; `/status`
does not double-celebrate. Silence is the respect here.

**Rate-limiting.** Runs once per session on first `/status` invocation, same cadence as
the Ritual of Return. Subsequent `/status` calls in the same session skip the milestone
scan entirely.

### LONGITUDINAL FEEDBACK LOOP

Read `STATE.yaml → decisions_history` if the field exists and is non-empty. For each
entry, apply the closure points defined in `references/capability-matrix.md §6.2`:

**Closure point 4 — 30-day retrospective prompt.**

Detect entries where:
- `published: true` AND
- `outcome_30d.reported_issues` or related fields have been collected more than 30 days
  ago (compare against current date) AND
- `retrospective_verdict: null`

For each matching entry, surface ONE prompt per /status run (rate-limited to one
retrospective per session to avoid survey fatigue):

```
┌─ Retrospective — {slug} ──────────────────────────┐
│  You published {slug} {N} days ago as a {form}.  │
│  Looking back — did the form match what you       │
│  actually needed?                                  │
│                                                    │
│    1. correct       — the form was right          │
│    2. wrong_form    — should have been a {alt}    │
│    3. wrong_depth   — right type, wrong depth     │
│    4. wrong_cell    — wrong topology cell         │
│                                                    │
│  Your answer calibrates future proposals.         │
└────────────────────────────────────────────────────┘
```

If the creator answers, write the verdict to `STATE.yaml decisions_history[i].retrospective_verdict`
and `retrospective_captured_at`. Never ask twice for the same entry.

**Confidence tier display.**

Compute the calibration tier per `capability-matrix.md §6.3` from the creator's accumulated
verdicts across all products:

- `≥5 correct` → **HIGH** confidence — surface in dashboard as `Engine confidence: HIGH (based on {N} correct verdicts)`.
- `≥3 wrong_*` → **MODERATE** confidence — surface as `Engine confidence: MODERATE — I've gotten a few proposals wrong, I'll offer alternatives more assertively.`
- `<3 total verdicts` → **LOW** confidence — surface as `Engine confidence: LEARNING — few retrospectives captured yet, proposals will be equally weighted.`

The tier is informational in `/status` and is also read by `/create` Section 0 Step 9 to
set proposal tone. Showing it in the dashboard makes the calibration visible — creators
understand why the Engine sounds more or less assertive over time.

### PROMOTION QUEUE INTEL (`--promotion-queue` flag)

When `/status` is invoked with `--promotion-queue`, scan `decisions_history` for v2 cell
promotion candidates per `capability-matrix.md §6.4`:

1. Filter entries where `unroutable: true` AND `unroutable_reason: v2_cell_deferred` AND
   `published: true` AND `retrospective_verdict: correct`.
2. Group by the v2 cell name referenced in the entry's details.
3. For each group, count entries. A v2 cell with ≥3 entries is a candidate for promotion
   to v1 per §6.4's three-entry threshold.
4. Sort candidates by count descending, surface top 3.

Output format:

```
PROMOTION QUEUE (decisions_history intel)

  Top v2 candidates for promotion to v1:
    1. {v2_cell_name} — {N} correct forges (threshold: 3)
    2. {v2_cell_name} — {N} correct forges
    3. {v2_cell_name} — {N} correct forges

  A new wave is required for promotion (not automatic).
  See references/capability-matrix.md §6.4 for promotion path.
```

If no candidates exist, output: `PROMOTION QUEUE: no v2 cells have accumulated the 3-entry
threshold yet. Keep forging — the queue fills over time.`

This flag is **read-only intel** for the creator. It never mutates state — it closes
the loop from forge → retrospective → promotion signal without taking automatic action.
Constitutional Clause II holds (Separation of Production and Judgment): the data surfaces;
the promotion decision is a separate governance step with founder
authorization.

This transforms /status from a passive dashboard into an active coaching surface.

---

1. Read `STATE.yaml` — engine version, edition, last session, workspace state
2. Read `creator.yaml` — creator name, type, expertise domains. If missing, show "Creator: not configured — run /onboard" in dashboard and continue with available data.
3. Glob `workspace/[!.]*/` — list all product directories (excludes hidden dirs like `.fixtures/`)
4. For each product, read `.meta.yaml` — slug, type, state, scores, timestamps
5. Render dashboard

---

## Dashboard Format

**CRITICAL — UX Stack (load in order before rendering):**
0. `references/quality/engine-voice-core.md` — already loaded via Activation Protocol. Carries the micro voice contract.
1. `references/ux-experience-system.md` §1 Context Assembly — build creator context from creator.yaml + STATE.yaml + all .meta.yaml files
2. `references/ux-experience-system.md` §2 Tact Engine — adapt dashboard depth and tone to creator level + journey position
3. `references/ux-vocabulary.md` — translate all internal terms (MCS→tiers, DNA→invisible, types→human names)
4. `references/quality/engine-voice.md` — full voice substrate (Brand DNA, signature patterns, UX Integration Stack). Load for peak moments (Ritual of Return Layer 1 celebration, Portfolio Vision, marketplace badge render).

**Cognitive rendering:** /status is the ENGINE'S FACE — it's where creators form their relationship with myClaude. Apply §5 Identity Reinforcement and §3.2 Portfolio Progress from the experience system. For beginners, this is encouragement. For experts, this is strategic intelligence. Same data, different lens.

```
┌─────────────────────────────────────────────┐
│  ✦ MyClaude Studio Engine v{version}        │
│  Creator: {name} | {total} products built   │
│  {published} live on marketplace             │
└─────────────────────────────────────────────┘

YOUR PRODUCTS
  ✦ {display_name}  {ux_type_name}  {ux_tier} {stars}  {state_emoji}
  # ux_type_name from ux-vocabulary.md (e.g., "Deep Intelligence" not "minds cognitive")
  # ux_tier: "Verified ✓" / "Premium ★★" / "Elite ★★★" (not MCS-1/2/3)
  # state_emoji: 🟢 live | 📦 ready to ship | ✏️ in progress | 🔨 just started

  Example:
  ✦ K8s Security Advisor   Deep Intelligence   Premium ★★   🟢 live
  ✦ AEGIS                  Tool                Elite ★★★    🟢 live
  ✦ NOCTIS                 Complete Setup      Elite ★★★    📦 ready

{if any product needs attention}
NEXT STEPS
  {slug}: {human_action} — {why_it_matters}
  # Examples:
  # "k8s-hardening: Add your expertise → /fill"
  # "my-tool: Ready to go live → /publish"
{/if}

{if stale > 0}
💡 {stale} product(s) haven't been touched in 30+ days. Want to revisit?
{/if}

QUICK ACTIONS
  /create  — Build something new
  /scout   — Research a domain first
  /explore — See what's on the marketplace
```

**Technical details (appended only if creator.yaml technical_level == "expert"):**
```
Technical: {total_validated}/{total} validated | Pitfalls: {pitfall_count} tracked
```

### Portfolio Intelligence Section

After the main dashboard and before the CLI marketplace section, compute and display portfolio intelligence. Reference: `references/intelligence-layer.md` + `config.yaml → intelligence`.

**Data gathering:**
1. For each product in workspace, read `.meta.yaml → intelligence` fields (if present)
2. Group products by `intelligence.domain` (fall back to inferring domain from slug/type if not set)
3. Read `config.yaml → intelligence.portfolio` for thresholds

**Portfolio Vision display:**

```
PORTFOLIO VISION
  Domains: {N} covered
  {For each domain, sorted by product count desc:}
    {domain}: {product_count} products ({types_list})
      {If product_count >= bundle_suggestion_threshold: "→ Bundle opportunity: combine these into a {domain} suite"}
      {If domain has skill + minds: "→ Composition: {minds_slug} advises, {skill_slug} executes"}
  
  {If any domain has coverage < coverage_threshold:}
  GAPS
    {domain}: {coverage}% coverage — {suggestion based on missing types}

  {If any product has intelligence.value_score:}
  VALUE MAP
    {slug}: {value_score}/12 → ${range[0]}-${range[1]} ({strategy})
    ...
    Portfolio total estimated value: ${sum of midpoint prices}
    Revenue-generating: {count with price > 0}/{total published}
```

**Intelligence rules for portfolio analysis:**
- 3+ products in same domain AND no bundle → suggest bundle composition
- skill + minds in same domain → suggest cross-reference in README
- 2+ squads with overlapping agent names → suggest consolidation or orchestrator
- Domain with only 1 product type → suggest complementary type ("You have a {type} for {domain}. A {complementary_type} would complete the coverage.")

**Complementary type suggestions:**
| Has | Suggest |
|-----|---------|
| minds only | skill ("an executor for the advisor's recommendations") |
| skill only | minds ("an advisor to guide when/how to use the skill") |
| skill + minds | workflow ("orchestrate them into a sequence") |
| 3+ individual products | bundle ("package for complete domain coverage") |

**Display only when data exists.** If no product has intelligence fields populated, show a minimal note:
```
PORTFOLIO
  Run /validate --level=2 on products to unlock value intelligence.
```

This transforms /status from a passive list into an active strategic surface that reveals portfolio patterns the creator hasn't noticed.

### Trajectory Display

| Trend | Symbol | When |
|-------|--------|------|
| Improving | `+{N}%` | Current > previous score |
| Stable | `={score}%` | Current == previous |
| Declining | `-{N}%` | Current < previous (flag with warning) |
| New | `(new)` | Only 1 score entry |

### State Display Rules

| State | Display | Color Hint |
|-------|---------|------------|
| scaffold | `scaffold` | dim |
| content | `content` | default |
| validated | `validated` | green |
| packaged | `packaged` | cyan |
| published | `published vX.Y.Z` | gold |
| stale | append ` (stale)` | warning |

### CLI Marketplace Intelligence (if myclaude available)

**CLI contract:** Load `references/cli-contract.md` for unified error handling. All marketplace commands in this skill are **silent-skip** severity — dashboard renders without marketplace data if CLI is unavailable, too old, or network is down. Severity map:
- **Silent-skip:** `stats`, `my-products`, `notifications`, `profile pull`, `trending` — skip section, show install hint
- **All queries:** append `--json 2>/dev/null`, 15s timeout, treat invalid JSON as CLI absent
- **Never blocking:** No CLI failure prevents the dashboard from rendering

After the main dashboard, if `myclaude` CLI is in PATH, display marketplace context:

```bash
# Run silently, don't block dashboard if CLI unavailable
myclaude my-products --json 2>/dev/null
```

If successful, append to dashboard:

```
MARKETPLACE (@{username})
  Published: {count} products | Downloads: {total_dl} | Revenue: {revenue}
  {For top 3 by downloads:}
  {slug}: {downloads} downloads {if rating: "★{rating}"}
  
  Run: myclaude trending     — see what's hot
  Run: myclaude stats {slug} — detailed product analytics
```

If CLI not in PATH or not authenticated, show:

```
MARKETPLACE
  Install myclaude CLI for marketplace intelligence: npm i -g @myclaude-cli/cli
```

**Per-product stats enrichment:** For each published product in workspace, run `myclaude stats {slug} --json 2>/dev/null`. If successful, append to the product's WORKSPACE line:
```
  {slug}  [{type}]  published  MCS-{level}  {score}%  📊 {downloads}dl {likes}❤ ${revenue}
```

**Profile level:** Run `myclaude profile pull --json 2>/dev/null` (if available). Display creator level:
```
CREATOR: {name} | @{username} Level {level} ({xp} XP) | {followers} followers
```

**Notifications:** Run `myclaude notifications --json 2>/dev/null`. If any new activity since last check:
```
ACTIVITY: {count} new since last session
  {latest notification summary}
```

This surfaces real marketplace data inside the Engine — creators see their impact without leaving Claude Code.

---

## Anti-Patterns

1. **Verbose status** — Keep it compact. One line per product. No essays.
2. **Stale data** — Always read fresh from files. Never cache.
3. **Missing files** — If STATE.yaml or creator.yaml missing, say so clearly and suggest /onboard.
4. **Empty workspace** — If no products, show: "Workspace empty. Run /create to start your first product."
5. **Broken meta** — If .meta.yaml is malformed, show product with `[error]` state, don't crash.
