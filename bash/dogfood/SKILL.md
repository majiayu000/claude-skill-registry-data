---
name: dogfood
primitive: P11
category: governance
description: "Per-bstack-P11 reflex 7+16 — explicitly trigger the Dogfood Plan + per-stack cookbook + Dogfood Receipt sequence. Auto-detects the tech stack from repo signals (Cargo.toml + src-tauri/ → tauri-sidecar; next.config.* → nextjs; app.json + expo → expo-rn; Cargo.toml solo → rust-cli; openapi.* or REST framework deps → rest-api; mcp.{json,yaml} → mcp-server), loads the matching cookbook entry from bstack/references/dogfood-patterns.md (broomva/bstack ≥ 0.13.0), produces a six-row Dogfood Plan (entry surface · driver · evidence · smoke · end-to-end · receipt anchor), optionally executes via the named surfaces (Interceptor mandatory for visual deploy verification; gstack, cliclick, screencapture, curl+jq, xcrun simctl compose per stack), and produces the final receipt with binary anti-rationalization check. Three subcommands: /dogfood (full sequence — plan → execute → receipt), /dogfood plan (plan only), /dogfood receipt (receipt only, assumes plan exists in PR body or AGENTS.md). Inherits from broomva/bstack: cookbook, P11 discipline, stack-detection algorithm. Composes with broomva/autonomous (which fires this implicitly at reflex 7+16) — use /dogfood directly for narrower scope (small changes, exploration, pre-merge verification gate without full pipeline). USE WHEN dogfood, dogfood this, dogfood plan, dogfood receipt, validate as user, exercise the change, click through the app, /dogfood, P11 receipt, exercise like a user would, did I actually click it, prove this works for a user, interaction evidence, deploy verification. NOT FOR running CI checks (use /p9), batch headless automation (use Browser skill), or scientific-method experiment framing (use Science skill)."
argument-hint: [plan|execute|receipt|--stack=<name>|--ticket=<id>|--evidence-dir=<path>]
effort: low
---

# dogfood — explicit P11 reflex trigger (Dogfood Plan + Receipt)

Explicit trigger for **bstack P11 reflex 7+16** for: **$ARGUMENTS**

## Inheritance from bstack (declared)

This skill is downstream of [`broomva/bstack`](https://github.com/broomva/bstack). It implements P11 reflex 7 (Dogfood Plan keyed to detected stack) and reflex 16 (Dogfood Receipt) explicitly, where `/autonomous` fires them implicitly inside its 21-reflex pipeline. Full inheritance contract: [`references/bstack-inheritance.md`](references/bstack-inheritance.md).

- **Cookbook source**: `bstack/references/dogfood-patterns.md` (loaded on demand; not duplicated here)
- **Discipline source**: `bstack/references/primitives.md` §P11
- **Stack-detection algorithm**: mirrors `bstack/scripts/doctor.sh` §13
- **Minimum bstack version**: 0.13.0

If bstack isn't installed, the skill still works — it carries its own detection logic and inlines the minimum surfaces matrix. The *cookbook* (deep per-stack reference) lives upstream in bstack.

## Purpose

P11 (Empirical Feedback Loop) mandates *"before claiming work complete, the agent has interacted with the deployed/running version… reasoning isn't validation; interaction is."* This skill makes the two binding reflexes (Plan + Receipt) explicitly triggerable when you don't want the full `/autonomous` pipeline.

When to invoke `/dogfood` instead of `/autonomous`:
- Single-file change with user-visible effect
- Exploration: "what does dogfooding look like for this stack"
- Pre-merge verification gate on someone else's PR
- First time seeing a tech stack you're new to (cookbook entry is the answer)
- Receipt-only after manual execution

## Usage

```
/dogfood                        # full sequence: plan → execute prompt → receipt
/dogfood plan                   # plan only — produce the six-row plan
/dogfood execute                # execute — fire the surfaces named in the plan
/dogfood receipt                # receipt only — produce the evidence table
/dogfood --stack=tauri-sidecar  # override detection
/dogfood --ticket=BRO-1234      # anchor evidence path to ticket
/dogfood --evidence-dir=/tmp/dogfood/<slug>
```

CLI fallback (no Claude session required):

```bash
./scripts/dogfood.sh detect              # echo detected stack
./scripts/dogfood.sh plan --stack=nextjs # emit plan template stub
./scripts/dogfood.sh receipt --plan=plan.md
```

## Workflow

### Phase 1 — Detect stack

Mirror `bstack/scripts/doctor.sh` §13 detection. If `--stack=<name>` was passed, use that instead. If detection returns `unknown`, the agent declares the stack explicitly in the plan (no silent default).

```bash
./scripts/dogfood.sh detect
# → tauri-sidecar | nextjs | expo-rn | rust-cli | rest-api | mcp-server | unknown
```

The detection logic mirrors what `bstack doctor §13` does. If `bstack doctor` is installed and recent, prefer its output:

```bash
if command -v bstack >/dev/null 2>&1; then
    bstack doctor 2>&1 | grep "^  \[ok\] stack detected:" | sed 's/.*stack detected: //; s/ .*//'
fi
```

### Phase 2 — Load cookbook entry

Read the matching pattern section from `bstack/references/dogfood-patterns.md`:

```bash
# Section IDs in the cookbook:
#   Pattern A — Tauri + sidecar
#   Pattern B — Next.js
#   Pattern C — Expo / React Native
#   Pattern D — Rust CLI
#   Pattern E — REST API
#   Pattern F — MCP server / Tool provider

BSTACK_REF=$(npx skills path broomva/bstack 2>/dev/null || echo "$HOME/.agents/skills/bstack")
COOKBOOK="$BSTACK_REF/references/dogfood-patterns.md"
```

If the cookbook isn't reachable (bstack not installed or older than v0.13.0), fall back to the **minimum surfaces table** inlined below in `Phase 2 — fallback (no bstack)`. The agent surfaces a one-line warning recommending bstack installation for the deep cookbook.

### Phase 2 — fallback (no bstack ≥ 0.13.0 available)

Minimum surfaces table (covers ~80% of cases without the deep cookbook):

| Stack | Primary surfaces | Mandatory |
|---|---|---|
| tauri-sidecar | curl+jq engine API · cliclick+screencapture · Interceptor at :1420 | Interceptor for visual verification |
| nextjs | dev server log-tail · Interceptor · curl+jq for routes | Interceptor for authenticated flows |
| expo-rn | `expo start --ios` · `xcrun simctl io booted screenshot` | Simulator screenshots |
| rust-cli | direct invocation · `--help` smoke · trycmd/assert_cmd | Exit code 0 + output capture |
| rest-api | curl+jq · log-tail · OpenAPI diff if applicable | Response body assertion |
| mcp-server | `npx @modelcontextprotocol/inspector` or direct LLM invoke | Tool-call response capture |

For deeper detail (canonical arc, bash snippets, gotchas, receipt template): install bstack ≥ 0.13.0.

### Phase 3 — Produce the Dogfood Plan

Surface the plan in the agent's response, and (if a PR is active) into the PR body via `gh pr edit <pr> --body-file` or `gh pr comment <pr>`. Six rows, all mandatory:

```markdown
**Dogfood Plan** (stack: <detected>, ticket: <id-or-none>)

- **Entry surface**: <URL / window / CLI command the user touches>
- **Driver**: <Interceptor / gstack / cliclick+screencapture / curl+jq / xcrun simctl>
- **Evidence**: <screenshot path / response body path / log line / recording>
- **Smoke**: <one-line "didn't obviously break" check>
- **End-to-end**: <multi-step user flow that catches regression a smoke test misses>
- **Receipt anchor**: <file / line / PR comment ID where the receipt lives>
```

The plan rows MUST be concrete — file paths, URLs, commands, not vibes. Rows that genuinely don't apply are marked `⊘` with explicit reason ("backend mocked in this PR; real cloud creds not available — smoke-only this run"). Silent omission is the failure mode this contract closes.

### Phase 4 — Execute (only if subcommand is `execute` / `explore` or full sequence)

For each plan row, fire the named driver. The `explore` subcommand (v0.2.0+) emits the per-stack execution recipe; for web stacks it composes with the agent-browser exploratory workflow.

#### Exploratory web QA mode (v0.2.0+)

For web stacks (`nextjs`, `rest-api`-with-frontend, or any `--url=` target), `/dogfood explore --url=...` produces an **agent-browser session-based exploration recipe**: initialize → authenticate → orient → explore → document issues → wrap up. Each issue logged with screenshots / video / repro-steps to `./dogfood-output/<slug>/`. The exploratory output's `report.md` becomes the parent Dogfood Plan's *Evidence* row.

```bash
dogfood explore --url=https://staging.example.com --session=billing-page --ticket=BRO-1234
# → emits a recipe: agent-browser open · snapshot · screenshot · errors · console
# → mkdir -p ./dogfood-output/staging-example-com/{screenshots,videos}
# → cp templates/exploratory-report.md → output dir
```

**Composition with the upstream `dogfood` skill**: the agent-browser workflow + issue taxonomy + report template are adapted from the pre-existing `dogfood` skill at `~/.agents/skills/dogfood/` (agent-skills catalog). See `references/bstack-inheritance.md` for attribution + `references/exploratory-issue-taxonomy.md` for what to look for.

#### Per-stack execution snippets

**tauri-sidecar**:
```bash
osascript -e 'tell application "Houston" to activate'
cliclick c:1662,1090
cliclick t:"My test mission"
cliclick kp:return
sleep 1
screencapture -x -t png -R 1480,200,470,980 "$EVIDENCE_DIR/after-input.png"
```

**nextjs**:
```bash
interceptor open "http://localhost:3000/<route>"
interceptor read --max-tokens 4000
interceptor act --click "Submit"
interceptor wait-stable
interceptor screenshot "$EVIDENCE_DIR/after-submit.png"
```

**rest-api**:
```bash
curl -sS -X POST "$BASE/api/<route>" \
  -H 'content-type: application/json' \
  -d '{"foo":"bar"}' | jq . | tee "$EVIDENCE_DIR/response.json"
```

Capture the exit status of each driver invocation. Failed invocations are surfaced before producing the receipt.

### Phase 5 — Produce the Dogfood Receipt

After execution (or after the user reports manual execution), produce the evidence table:

```markdown
**Dogfood Receipt** — <ticket> · <date>

| Plan row | Executed | Evidence |
|---|---|---|
| Smoke | ✅ | <evidence>: <path / output line> |
| End-to-end | ✅ | Screenshots: <paths> |
| API contract | ✅ | <response captured in PR comment #N> |
| Side-effect | ✅ | <DB query / log / state assertion> |
| Deploy preview | ✅ | <preview URL> — Interceptor screenshot <path> |
| <row that wasn't applicable> | ⊘ | Reason: <explicit> |

**Anti-rationalization check**: did I actually click the app like a user would? <yes/no>
**Surfaces driven**: <Interceptor / cliclick / curl / etc.>
**Time-to-receipt**: <duration> from first write to receipt complete.
```

The **anti-rationalization line is binary and mandatory**. If the honest answer is no, the receipt isn't complete — the plan goes back into execution.

### Phase 6 — Persist the receipt

Anchor the receipt at the location named in the plan's *Receipt anchor* row:

- **PR body** — `gh pr comment <pr> --body "$(cat receipt.md)"` OR include in PR description
- **Repo file** — `docs/dogfood-receipts/<date>-<ticket>.md` for repos with substantial dogfood history
- **Bridge (P1) auto-capture** — bstack's Stop hook captures the session-end receipt to Obsidian automatically; no explicit action needed if bstack is installed

## Composition with /autonomous

`/autonomous` fires this skill at reflex 7 (Plan) and reflex 16 (Receipt). When invoked directly, `/dogfood` runs in isolation. Both produce the same artifacts; the difference is scope.

| Scope | Use |
|---|---|
| Full feature work (multi-file, public contract, deploy-impacting) | `/autonomous` |
| Single-file change with user-visible effect | `/dogfood` directly |
| Pre-merge verification of someone else's PR | `/dogfood --ticket=<id>` |
| First time seeing a new tech stack | `/dogfood plan` |
| Receipt-only after manual execution | `/dogfood receipt` |

## Anti-patterns this skill closes

| Anti-pattern | Why it fails | What `/dogfood` enforces |
|---|---|---|
| "Compile-time pass = shipping" | Compile ≠ deploy correctness | Plan rows require evidence beyond exit codes |
| "CI green = shipping" | CI tests what CI was told; user flow is broader | Receipt requires deploy-verification screenshot |
| "I dogfooded mentally" | Ritual without artifact | Receipt table is the artifact; anti-rationalization line is binary |
| "I'll dogfood after merge" | Post-merge = bug found by user | Plan precedes substantive work; receipt precedes claiming complete |
| Agent-browser for visual deploy verification | Bot detection + missed visual state | Interceptor mandatory per cookbook |

## Cross-references

- **Cookbook (per-stack patterns)**: `bstack/references/dogfood-patterns.md` (loaded on demand)
- **P11 reflex contract**: `bstack/references/primitives.md` §P11
- **Inheritance declaration**: [`references/bstack-inheritance.md`](references/bstack-inheritance.md)
- **Interceptor skill**: `~/.claude/skills/Interceptor/SKILL.md`
- **`/autonomous` skill**: [`broomva/autonomous`](https://github.com/broomva/autonomous) (composes this skill at reflex 7+16)

## Voice notification (optional, for environments that support it)

If a local voice-notification daemon is running on port 31337:

```bash
curl -s -X POST http://localhost:31337/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the dogfood skill — producing P11 plan + receipt for the detected stack"}' \
  > /dev/null 2>&1 &
```

Skip silently if the daemon isn't running.
