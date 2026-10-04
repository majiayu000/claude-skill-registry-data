---
name: vsl-demo-producer
description: Prepare the demo video for a freelance bid — captures a clean screenshot of the gig's published n8n workflow via Claude in Chrome, builds a shot-by-shot recording script pairing the VSL narration with on-screen actions, and hands the founder tool-agnostic recording instructions (Loom/Tella/any recorder). The Demo phase of the Inbound Gig Engine. The founder records the video themselves.
allowed-tools: Read, Grep, Glob, Bash, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__computer
area: Sales
use_for: "Capture the n8n workflow screenshot + build a shot-by-shot recording script and tool-agnostic instructions so the founder can record the 60s demo video for a gig bid"
deps:
  mcp: ["Claude in Chrome (screenshots the published workflow; degrades to a manual-capture checklist when absent)", "Notion", "Slack"]
  gateway: ["FiveAgents (logging)"]
  files: ["brand.md", "sales.md"]
  env: ["`${BRAND}_GIGS_DB` (created by `gig-prospector`)"]
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v2.17.0 | June 21, 2026 |

**Description:** Prepare the demo video for a freelance bid — screenshot the published n8n workflow, build a shot-by-shot recording script from the VSL, and hand the founder tool-agnostic recording instructions. The founder records the video.

### Change Log

**v2.17.0** — June 21, 2026
- New skill (Sales). The **Demo** phase of the **Inbound Gig Engine** (`gig-prospector → gig-proposal-writer → n8n-workflow-builder → vsl-demo-producer`). Takes a gig whose workflow `n8n-workflow-builder` already built, captures a clean canvas screenshot of the published workflow via **Claude in Chrome** (the legacy `screenshot_workflow.py` Playwright path, generalized), and turns the 60-second VSL script into a **shot-by-shot recording script** that pairs each narration beat with the exact on-screen action. The founder records the video **themselves** in any recorder (Loom, Tella, Vidyard, ScreenStudio, QuickTime — **never hardcoded**), then pastes the link, which fills the `[DEMO VIDEO LINK]` placeholder in the cover letter. Writes screenshot path + recording script + `Demo Video URL` back onto the gig row and advances `Status` to `Demo Ready`. No avatar/auto-render — recording stays manual by design.

---

# SKILL.md — VSL Demo Producer

## Before Executing

Read `agents/link.md` before starting. It defines the active brand, personality, quality checklist, and available tools. Determine the active brand from `$DEFAULT_BRAND` env var — if not set, ask the user.

## Role

You are a demo producer for the active brand. Your job is to get **one** gig's bid camera-ready: capture a crisp screenshot of the n8n workflow the brand built to prove the solution, and write a tight, shot-by-shot recording script that maps the already-written 60-second VSL narration to what the founder should show on screen. **You do not record or render the video** — the founder records it themselves in whatever screen recorder they prefer. You give them everything they need to nail it in one take, then capture the resulting video link back onto the gig.

---

## When to use

Use this skill when:
- A gig in `${BRAND}_GIGS_DB` is `Status="Workflow Built"` and needs its demo prepped
- The founder has recorded the video and wants the link captured + the bid marked ready (run with the video URL)
- Re-capturing the screenshot after the workflow changed

Do NOT use this skill for:
- Building the workflow → use `n8n-workflow-builder` (this skill follows it)
- Writing the VSL script / cover letter → use `gig-proposal-writer` (the script comes from there)
- Auto-generating an avatar/AI video → out of scope by design; recording is manual
- Discovering gigs → use `gig-prospector`

---

## Inputs required

| Input | Required | Notes |
|-------|----------|-------|
| Active brand | Yes | From `$DEFAULT_BRAND`; ask if unset |
| Gig | Yes | A Notion page URL/ID in `${BRAND}_GIGS_DB`, typically `Status="Workflow Built"`, carrying a `Workflow URL` |
| Mode | Optional | `prep` (default — screenshot + recording script) or `capture` (record the founder's video URL onto the gig) |
| Demo video URL | For capture mode | The link the founder recorded; fills `[DEMO VIDEO LINK]` |

---

## Step-by-step workflow

### Step 1 — Read context + fetch the gig

Read `brand.md` (voice, for the on-screen framing notes) and `sales.md` (Sender Persona — who's on camera / whose account). Fetch the gig — it **must** live in `${BRAND}_GIGS_DB`:

```
Use mcp__claude_ai_Notion__notion-fetch:
- id: <gig page URL or page ID>
```

Extract `title`, `Workflow URL`, the `## VSL Script (60s)` block (from `gig-proposal-writer`), and the `## Demo Workflow` node chain (from `n8n-workflow-builder`). If `Workflow URL` is missing, tell the founder to run `n8n-workflow-builder` first. If running in **capture mode**, skip to Step 5.

### Step 2 — Screenshot the published workflow (Claude in Chrome)

Use the brand's own authenticated Chrome (beats n8n's login wall, no stored passwords):

1. `mcp__Claude_in_Chrome__navigate` to the `Workflow URL`.
2. If a login wall appears, **pause and ask the founder to sign in** to n8n in the open Chrome window, then continue (the extension can't complete logins).
3. Fit the workflow to the canvas (zoom-to-fit) so the full left-to-right chain is visible and the node labels are legible.
4. Capture a screenshot of the canvas and save it to `outputs/{brand}/sales/gigs/demos/Workflow_{gig-slug}_{DDMonYYYY}.png`.

Verify the saved image shows the whole chain with readable client-language labels (re-fit and recapture if cropped). This screenshot is the hero frame of the demo and can also be attached to the bid as a static proof image.

**Fallback — if Claude in Chrome is unavailable:** skip the auto-capture and emit a short manual-capture checklist instead (open the Workflow URL, zoom to fit, screenshot the canvas, save to the path above). Log a warning; never abort the run for a missing Chrome MCP.

### Step 3 — Build the shot-by-shot recording script

Turn the VSL narration into a table the founder can follow live. For each beat of the script, pair the spoken line with the exact on-screen action and a target duration, expanding the `[SHOW WORKFLOW]` marker into concrete moves on the real workflow:

| Beat | Narration (read aloud) | On screen | ~sec |
|---|---|---|---|
| Hook | "{first VSL line}" | Founder's face or the gig/job context | 0–10 |
| Promise | "{promise line}" | Cut to the n8n canvas (full chain) | 10–20 |
| Demo | "{demo narration}" | Pan the trigger → each node → the visible final step; hover/zoom each labeled node as it's named | 20–50 |
| CTA | "{cta line}" | Back to face or the final result node | 50–60 |

Keep it to ~60 seconds. Note the brand voice / energy from `brand.md` and who appears on camera from `sales.md` Sender Persona.

### Step 4 — Recording instructions (tool-agnostic) + write back

Give the founder a short, recorder-neutral setup so they can record in **their** tool of choice — explicitly list options without prescribing one: **Loom, Tella, Vidyard, ScreenStudio, QuickTime, OBS, or any screen recorder**. Instructions:
- Open the workflow screenshot/canvas and the recording script side by side.
- Record screen + mic (and webcam bubble if the brand shows a face) in one ~60s take.
- Follow the shot table; read the narration in brand voice.
- Export/share, copy the **video link**, and run this skill in **capture mode** with that URL (or paste it into the gig row's `Demo Video URL`).

**Ensure properties exist** on `${BRAND}_GIGS_DB` (idempotent — add only if missing):

```
Use mcp__claude_ai_Notion__notion-update-data-source (only for properties not already present):
- Screenshot Path : rich_text
- Demo Video URL  : url
```

Update the page and append a `## Recording Script` body block (the shot table + instructions):

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <gig page id>
- properties: {
    "Status":          "Demo Ready",          // adds the option if new
    "Screenshot Path": "<png path>"
  }
```

### Step 5 — Capture mode: record the founder's video link

When run with a Demo Video URL (after the founder records):

1. Write `Demo Video URL` onto the gig row.
2. Update the `## Cover Letter` body block: replace the `[DEMO VIDEO LINK]` placeholder with the real URL so the bid is submission-ready.
3. Advance `Status` to `Ready to Submit` (adds the select option if new).

```
Use mcp__claude_ai_Notion__notion-update-page:
- page_id: <gig page id>
- properties: {
    "Status":         "Ready to Submit",
    "Demo Video URL": "<recorded video url>"
  }
```

### Step 6 — Save local backup + Slack the founder

Save the recording script + screenshot reference to `outputs/{brand}/sales/gigs/demos/Demo_{gig-slug}_{DDMonYYYY}.md`.

**Before calling `slack_send_message`, you MUST first call `ToolSearch` with query `"select:mcp__claude_ai_Slack__slack_send_message"` to load the deferred tool schema.**

```
Use mcp__claude_ai_Slack__slack_send_message:
- channel_id: "$SLACK_NOTIFY_USER"
- text: "🎬 [{brand}] Demo ready to record — {gig title}
         Screenshot: {png path}
         60s shot-by-shot script on the gig row: {notion_url}
         ▶︎ Record it in your tool of choice (Loom / Tella / ScreenStudio / QuickTime…), then re-run
            /link-skills:vsl-demo-producer in capture mode with the video link to finish the bid."
```

In capture mode, send instead: `"✅ [{brand}] Demo video captured — {gig title}. Bid is Ready to Submit: {notion_url}"`.

---

## Output format

**Save location:** `outputs/{brand}/sales/gigs/demos/`
**Naming:** `Demo_{gig-slug}_{DDMonYYYY}.md` (script) + `Workflow_{gig-slug}_{DDMonYYYY}.png` (screenshot)

**Output metadata:**
```markdown
---
Date: YYYY-MM-DD
Skill Used: vsl-demo-producer
Brand: {brand}
Gig: {gig title}
Workflow URL: {n8n url}
Screenshot: {png path}
Demo Video URL: {url or "pending founder recording"}
Notion Gig Row: {url}
Status: Demo Ready | Ready to Submit
---
```

**Output sections:**
1. **Screenshot** — path to the captured canvas PNG (or manual-capture checklist if Chrome absent)
2. **Recording script** — the shot-by-shot table (narration · on screen · seconds)
3. **Recording instructions** — tool-agnostic setup; how to capture the link back

---

## Quality checklist

- [ ] Active brand resolved; `agents/link.md` + `brand.md`/`sales.md` read first
- [ ] Gig confirmed in `${BRAND}_GIGS_DB`; `Workflow URL` present (else routed back to `n8n-workflow-builder`)
- [ ] Workflow screenshot captured with the full chain visible + labels legible (or manual checklist emitted when Chrome absent)
- [ ] Login-wall pause handed to the founder, not failed
- [ ] Recording script maps every VSL beat to a concrete on-screen action; ~60s total
- [ ] Recording instructions are **tool-agnostic** — multiple recorders offered, none hardcoded
- [ ] `[DEMO VIDEO LINK]` left as a placeholder in prep mode; replaced with the real URL in capture mode
- [ ] No avatar/auto-rendered video produced — recording stays with the founder
- [ ] Screenshot path + recording script written to the gig row; `Status="Demo Ready"` (or `Ready to Submit` in capture mode)
- [ ] Local backup saved; Slack digest sent to `$SLACK_NOTIFY_USER`
- [ ] Agent run logged to dashboard

---

## Final Step — Log to Dashboard

See `docs/new_agent_onboarding/metrics-spec.md` for the full JSONB contract.

```
Use gateway MCP tool `fiveagents_log_run`:
- fiveagents_api_key: ${FIVEAGENTS_API_KEY}
- skill: "vsl-demo-producer"
- brand: "<active-brand>"
- status: "<success|failed>"
- summary: "<1 line, <200 chars>"
- started_at: "<ISO timestamp>"
- completed_at: "<ISO timestamp>"
- metrics: {
    "date": "YYYY-MM-DD",
    "gig_title": "<title>",
    "mode": "<prep|capture>",
    "workflow_url": "<n8n url>",
    "screenshot_captured": true,
    "screenshot_path": "<png path>",
    "chrome_available": true,
    "recording_video_url": "<url or empty>",
    "status_after": "Demo Ready | Ready to Submit",
    "notion_gig_url": "<url>",
    "output_path": "outputs/{brand}/sales/gigs/demos/",
    "deliverable": "Demo_{gig-slug}_{DDMonYYYY}.md"
  }
```

---

## Part of the pipeline

The **Demo** phase — the last build step before the founder submits the bid:

```
gig-prospector (Discover) → gig-proposal-writer (Write) → n8n-workflow-builder (Prove)
  → vsl-demo-producer (this skill — screenshot + recording script, Status="Demo Ready")
  → founder records the video in their own recorder
  → vsl-demo-producer (capture mode — video link onto the row, Status="Ready to Submit")
  → founder submits the bid on the marketplace
```

On-demand, one gig at a time. Recording is always manual — the founder owns the camera.