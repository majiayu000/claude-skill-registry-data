---
name: vibe-handoff
description: >
  Generates complete handoff packages for every transition scenario in a
  vibe-* project. Five modes: client (project completion), milestone
  (phase sign-off), dev (new developer onboarding), internal (team
  handoff between BetaCraft developers), maintenance (handing to client's
  own dev team). Each mode produces markdown documents plus a single
  self-contained index.html portal — clean, light-mode, client-readable,
  combining all docs into one navigable file. Includes delivery doc,
  feature walkthrough, credentials placeholder, known issues, support guide,
  sign-off checklist, and roadmap. Reads BRIEF.md, SPEC.md, DECISIONS.md,
  TASKS.md, ARCHITECTURE.md, CODEBASE.md. Triggers on handoff: client,
  handoff: milestone, handoff: dev, handoff: internal, handoff: maintenance,
  prepare handoff, client delivery, project sign-off, onboard new developer,
  prepare for maintenance, ready to hand over.
---

# Vibe Handoff Skill

Generates complete, audience-appropriate handoff packages
from actual project state — not from templates filled with guesswork.

Every document is grounded in BRIEF.md, SPEC.md, DECISIONS.md,
TASKS.md, ARCHITECTURE.md, and CODEBASE.md.
Nothing is made up. Nothing is left as a placeholder except credentials.

Each package produces:
- Individual `.md` files for each document (unchanged — for version control and editing)
- A single `index.html` portal (new) — a clean, light-mode, elegantly designed web page
  that combines all documents into one navigable file, optimised for sharing with clients

---

## Five handoff modes

| Trigger | Scenario | Primary audience |
|---------|---------|----------------|
| `handoff: client` | Project completion | Client stakeholder (non-technical) |
| `handoff: milestone` | Phase sign-off | Client stakeholder + PM |
| `handoff: dev` | New developer joining | Developer taking over |
| `handoff: internal` | one developer → another | internal developer |
| `handoff: maintenance` | Handing to client's dev team | Client's technical team |

---

## Step 0 — Parse trigger and read context

**Detect mode from trigger:**
- `handoff: client` → full project completion package
- `handoff: milestone` → phase-specific package (which phase? read TASKS.md)
- `handoff: dev` → developer onboarding package
- `handoff: internal` → internal BetaCraft dev handoff
- `handoff: maintenance` → client maintenance team package

**If no mode specified:**
> "Which handoff are you preparing?
> · `handoff: client` — project complete, delivering to client
> · `handoff: milestone` — end of a phase, client sign-off
> · `handoff: dev` — new developer joining the project
> · `handoff: internal` — handing between BetaCraft team members
> · `handoff: maintenance` — handing to client's own dev team"

Wait for answer.

**Read all project context:**
```bash
cat BRIEF.md 2>/dev/null
cat vibe/SPEC.md 2>/dev/null
cat vibe/ARCHITECTURE.md 2>/dev/null
cat vibe/CODEBASE.md 2>/dev/null
cat vibe/TASKS.md 2>/dev/null
cat vibe/DECISIONS.md 2>/dev/null
cat vibe/reviews/backlog.md 2>/dev/null
ls vibe/features/ 2>/dev/null
ls vibe/bugs/ 2>/dev/null
cat .env.example 2>/dev/null
ls deploy/ ci/ .github/workflows/ 2>/dev/null
```

**Create handoff folder:**
```bash
mkdir -p vibe/handoff/[mode]-[YYYY-MM-DD]/
```

---

## Step 1 — Gather any missing context

Before generating documents, identify gaps.
Ask one focused set of questions — not piecemeal.

**For all modes:**
- Who is the handoff recipient? (name / role)
- Is there anything not captured in the project files that should be included?
- Any known issues not in the backlog?

**For client / milestone modes — additionally:**
- Who is the client contact receiving this?
- Is there a formal sign-off process (email, document signature, call)?
- Any outstanding scope items that need to be explicitly acknowledged?

**For dev / internal / maintenance modes — additionally:**
- What is the current active task or where should they pick up?
- Any tribal knowledge not in the docs? (quirks, workarounds, gotchas)
- Access and environment setup — does the incoming dev have everything?

Ask all questions at once. Wait for answers.
If context is sufficient from files alone — skip questions, proceed.

---

## Step 2 — Generate the handoff package

Generate all documents for the detected mode.
Read `references/templates/` for the exact format of each document.

### Documents by mode

**`handoff: client` — Full project completion**
```
vibe/handoff/client-[date]/
├── DELIVERY.md           ← what was built (plain English)
├── FEATURES.md           ← feature walkthrough
├── KNOWN_ISSUES.md       ← limitations and known bugs
├── CREDENTIALS.md        ← placeholder list — human fills values
├── SUPPORT.md            ← how to get help, escalation path
├── ROADMAP.md            ← what was deferred and why
├── SIGN_OFF_CHECKLIST.md ← PM works through this with client
└── index.html            ← portal combining all docs (generated in Step 4b)
```

**`handoff: milestone` — Phase sign-off**
```
vibe/handoff/milestone-phase[N]-[date]/
├── PHASE_DELIVERY.md     ← what was built this phase
├── PHASE_SIGN_OFF.md     ← checklist for this milestone
├── KNOWN_ISSUES.md       ← issues found in this phase
├── NEXT_PHASE.md         ← what's coming next
└── index.html            ← portal (generated in Step 4b)
```

**`handoff: dev` — New developer onboarding**
```
vibe/handoff/dev-[date]/
├── ONBOARDING.md         ← start here, full setup guide
├── ARCHITECTURE_GUIDE.md ← how the system works, decisions and why
├── ACTIVE_CONTEXT.md     ← where we are, what's in progress
├── GOTCHAS.md            ← tribal knowledge, things that bite
├── CREDENTIALS.md        ← placeholder — what they need access to
└── index.html            ← portal (generated in Step 4b)
```

**`handoff: internal` — BetaCraft team handoff**
```
vibe/handoff/internal-[date]/
├── CONTEXT_DUMP.md       ← complete state for the receiving dev
├── ACTIVE_TASKS.md       ← exactly where to pick up
├── DECISIONS_LOG.md      ← recent decisions with reasoning
├── OPEN_QUESTIONS.md     ← unresolved items needing attention
└── index.html            ← portal (generated in Step 4b)
```

**`handoff: maintenance` — Client dev team**
```
vibe/handoff/maintenance-[date]/
├── SYSTEM_OVERVIEW.md    ← what runs where, how it fits together
├── RUNBOOK.md            ← common operations, deployments, rollbacks
├── MONITORING.md         ← what to watch, alerts, thresholds
├── KNOWN_ISSUES.md       ← bugs and limitations to be aware of
├── CREDENTIALS.md        ← placeholder list
├── ARCHITECTURE_GUIDE.md ← how the system is built
├── ESCALATION.md         ← when to call BetaCraft, what to send
└── index.html            ← portal (generated in Step 4b)
```

---

## Step 3 — Generate each document

Read the relevant template from `references/templates/` before writing each document.
Fill every section from actual project data.
Never leave a section empty — if data doesn't exist, say so explicitly.

### Document: DELIVERY.md (client and milestone modes)

Plain English. Zero technical jargon.
Written as if explaining to a smart non-technical business owner.

Structure:
1. **What we built** — one paragraph, the core value delivered
2. **How it works** — the user journey in plain English, step by step
3. **What's included** — feature list in plain English (not task IDs)
4. **What's not included** — deferred items, explicitly named
5. **How to access it** — where to find it, login process
6. **What was decided along the way** — major decisions in plain English,
   why they were made (sourced from DECISIONS.md, translated from tech)

**Tone:** Confident, clear, proud of the work.
Not defensive. Not hedging. Not apologetic about scope decisions.
"We chose X because it gives you Y" — not "we had to limit X."

**Length:** 600-1000 words. Readable in 5 minutes.

---

### Document: SIGN_OFF_CHECKLIST.md (client and milestone modes)

This is the document the PM uses in the sign-off call with the client.
Every item is specific, binary (done/not done), and tied to something
the client can verify themselves.

Read `references/templates/SIGN_OFF_CHECKLIST_TEMPLATE.md`.

Structure:
1. **Project / milestone summary** — one line per feature delivered
2. **Acceptance criteria verification** — from SPEC.md, translated to plain English
   Each criterion: what it should do, how to test it, ✅ / ❌
3. **Known issues acknowledged** — client confirms they've seen the issues log
4. **Out of scope items acknowledged** — client confirms what was deferred
5. **Access confirmed** — client confirms they have all logins and credentials
6. **Support process confirmed** — client knows how to raise issues
7. **Sign-off declaration** — "By proceeding, client confirms delivery is accepted"

**Format:** Markdown checklist — `- [ ]` for each item.
PM ticks items off during the call.
Client can countersign by replying to the delivery email.

---

### Document: ONBOARDING.md (dev mode)

Full setup guide for the incoming developer.
They should be able to run the project locally by following this doc alone.

Read `references/templates/ONBOARDING_TEMPLATE.md`.

Structure:
1. **Prerequisites** — exact versions of tools required (Node, Python, Docker, etc.)
2. **Clone and install** — exact commands
3. **Environment setup** — what goes in .env, where to get each value
4. **Database setup** — migrations, seed data
5. **Run locally** — exact commands for each service
6. **Verify it works** — what to check, what success looks like
7. **Where to start** — first task, how to pick up where we left off

**Format:** Step-by-step numbered instructions. Every command on its own line.
No assumed knowledge. A developer unfamiliar with this stack should succeed.

---

### Document: CREDENTIALS.md (client, dev, maintenance modes)

**Never write actual values.** Structure and placeholder text only.

Format:
```
## Production environment

| Credential | Where to find it | Used for |
|---|---|---|
| DATABASE_URL | [source — e.g. Supabase dashboard > Settings > Database] | PostgreSQL connection |
| ANTHROPIC_API_KEY | [Anthropic console > API Keys] | Claude API calls |
| NEXTAUTH_SECRET | [generate: openssl rand -base64 32] | NextAuth sessions |
| TAVILY_API_KEY | [Tavily dashboard] | Web search in Scout agent |
| STRIPE_SECRET_KEY | [Stripe dashboard > Developers > API keys] | Payment processing |

## Staging environment
[same structure]

## Third-party service logins
| Service | Account email | Where to reset |
|---------|--------------|---------------|
| Vercel | [email] | vercel.com > team settings |
| Supabase | [email] | supabase.com > account |
| Stripe | [email] | stripe.com > settings |

## Repository access
| Service | URL | Access level |
|---------|-----|-------------|
| GitHub | [repo URL] | [admin/write/read] |
```

---

### Document: KNOWN_ISSUES.md (client, milestone, maintenance modes)

Honest. Specific. No corporate hedging.
Sources: `vibe/reviews/backlog.md` + any open bug folders.

Structure:
1. **Current known bugs** — each with: description, impact, workaround if any
2. **Limitations** — things that work but have constraints
3. **Technical debt** — things that work but should be improved
4. **Out of scope items** — deferred features (with reasoning from DECISIONS.md)

**Severity levels for client:**
- 🔴 **Blocking** — prevents core functionality (should be fixed before delivery)
- 🟡 **Impactful** — affects UX but has workaround
- 🟢 **Minor** — cosmetic or edge case

**Tone:** matter-of-fact, not apologetic.
"The competitor list takes 8-12 seconds to populate on first run
because it makes live API calls. Subsequent runs use cached results
and are near-instant. Fix scheduled for v1.1."
Not "we're aware there may be some performance issues in certain scenarios."

---

### Document: ROADMAP.md (client mode)

Everything that was deferred and why.
Sourced from DECISIONS.md (deferred decisions), SPEC.md (out of scope),
and BRIEF.md (non-goals).

Structure:
1. **What was deferred from v1** — each item with the reasoning
2. **Recommended v1.1 priorities** — top 3-5 highest value next steps
3. **Longer term possibilities** — ideas surfaced during build
4. **What would be needed for each** — rough effort, dependencies

**Tone:** opportunity-focused, not apologetic.
"Multi-user team support was deferred from v1 to keep the scope
tight and deliver faster. It's the natural v1.1 feature — the
data model already accounts for it."

---

### Document: RUNBOOK.md (maintenance mode)

Step-by-step instructions for the operations a maintenance developer
will need to perform. No assumed knowledge.

Structure:
1. **Deploying a new version** — exact steps, including what to check before/after
2. **Rolling back a deployment** — exact steps, when to use this
3. **Running database migrations** — exact commands, what to verify
4. **Restarting services** — how, when, what to check after
5. **Checking logs** — where they live, how to read them
6. **Common errors and fixes** — top 5 errors seen during development

Each operation: trigger (when to do this), steps (numbered, exact commands),
verification (how to confirm it worked), rollback (if something went wrong).

---

### Document: CONTEXT_DUMP.md (internal mode)

The complete brain dump from the outgoing developer to the incoming one.
This is the most honest document in the package.

Structure:
1. **Where we are** — one paragraph, current state of the project
2. **What I was just working on** — the active task and what's done/not done
3. **What was going well** — things the incoming dev should continue
4. **What was frustrating** — problems that aren't resolved yet
5. **What I'd do differently** — with hindsight
6. **The one thing to be careful about** — the highest risk area
7. **Questions I haven't answered yet** — open items needing resolution

**Tone:** colleague to colleague. Honest. Not a performance review.

---

## Step 4 — Review and present package

Before saving, present a summary:

```
HANDOFF PACKAGE — [Project Name]
Mode: [client / milestone / dev / internal / maintenance]
Recipient: [name/role]

Documents generated:
  ✅ [document name] — [one line description]
  ✅ [document name] — [one line description]
  [...]

⚠️ Requires human action before sharing:
  · CREDENTIALS.md — fill in all credential values
  · [any other gaps flagged during generation]

Quality checks:
  · All acceptance criteria from SPEC.md included in sign-off: [✅/⚠️]
  · All known issues from backlog included: [✅/⚠️]
  · All deferred items from DECISIONS.md included in roadmap: [✅/⚠️]
  · No actual credentials written anywhere: [✅]

Saved to: vibe/handoff/[mode]-[date]/

Generating HTML portal next...
```

---

## Step 4b — Generate the HTML portal

After all MD files are written, generate a single `index.html` portal.
This is a self-contained web page combining all documents — clean, light-mode,
elegantly designed, optimised for reading and sharing with clients.

> **Portal theming:** the generator uses a neutral, brand-agnostic default and
> automatically picks up the project's own design when a `DESIGN.md` /
> `vibe/design/CONTRACT.md` exists (so the portal isn't one fixed house style on
> every client). To set colours/fonts explicitly, drop a
> `vibe/design/portal-theme.json` with `{paper, accent, serif, sans, mono}` and the
> generator applies it.

```bash
python3 "$(ls ~/.claude/skills/vibe-handoff/scripts/generate_portal.py ~/.claude/plugins/marketplaces/*/skills/vibe-handoff/scripts/generate_portal.py 2>/dev/null | head -1)" vibe/handoff/[mode]-[date]/
```

The script:
1. Reads all `.md` files in the handoff folder
2. Converts each document to styled HTML
3. Builds a navigable single-page portal with sidebar, document index, and all content
4. Writes `vibe/handoff/[mode]-[date]/index.html`
5. Opens automatically in the browser

**The portal is the primary sharing artifact** for client and milestone modes.
The `.md` files remain for version control and future editing.

After the script runs, tell the user:

> "Portal generated — opening in your browser.
>
> **[Project name]** · [mode] handoff · [N] documents
> Portal: `vibe/handoff/[mode]-[date]/index.html`
>
> To share with the client: send the `index.html` file directly.
> It is fully self-contained — no internet required to read it after the fonts load once.
>
> ⚠️ Before sharing: fill in CREDENTIALS.md values, then regenerate:
> `python3 "$(ls ~/.claude/skills/vibe-handoff/scripts/generate_portal.py ~/.claude/plugins/marketplaces/*/skills/vibe-handoff/scripts/generate_portal.py 2>/dev/null | head -1)" vibe/handoff/[mode]-[date]/`"

---

## Step 5 — Post-package actions

### "handoff: send"
Generate sharing instructions appropriate to the mode:

**Client modes:**
```
Sharing instructions:
1. Fill CREDENTIALS.md — all values before sharing
2. Regenerate portal after filling credentials:
   python3 "$(ls ~/.claude/skills/vibe-handoff/scripts/generate_portal.py ~/.claude/plugins/marketplaces/*/skills/vibe-handoff/scripts/generate_portal.py 2>/dev/null | head -1)" vibe/handoff/[mode]-[date]/
3. Share index.html directly — single file, fully self-contained
   (Or share the full handoff folder via Google Drive / Notion for the MD files too)
4. Schedule 30-min call to walk through the Sign-Off Checklist section
5. After call: client replies to confirm sign-off
6. Archive: move to vibe/handoff/archive/ after sign-off received
```

**Dev modes:**
```
Sharing instructions:
1. Share repository access first — they need the code to follow along
2. Fill CREDENTIALS.md values and share via secure channel (1Password / Bitwarden)
3. Regenerate portal: python3 "$(ls ~/.claude/skills/vibe-handoff/scripts/generate_portal.py ~/.claude/plugins/marketplaces/*/skills/vibe-handoff/scripts/generate_portal.py 2>/dev/null | head -1)" vibe/handoff/[mode]-[date]/
4. Share index.html — they can follow the Onboarding section independently
5. Schedule 1h pairing session to walk through the Architecture Guide section
```

### Review a specific document
User says: "show me DELIVERY.md" or "review SIGN_OFF_CHECKLIST.md"
→ Print the document in full.
→ Ask: "Any changes before we finalise?"

### Regenerate portal after edits
If any MD file is edited after initial generation:
```bash
python3 "$(ls ~/.claude/skills/vibe-handoff/scripts/generate_portal.py ~/.claude/plugins/marketplaces/*/skills/vibe-handoff/scripts/generate_portal.py 2>/dev/null | head -1)" vibe/handoff/[mode]-[date]/
```
The portal always reflects the current state of the MD files.

---

## Step 6 — Update vibe docs

**vibe/DECISIONS.md:**
```
---
## [date] — Handoff: [mode]
- **Type**: milestone
- **Recipient**: [name/role]
- **Documents**: [list]
- **Portal**: vibe/handoff/[mode]-[date]/index.html
- **Status**: [generated / sent / signed off]
---
```

**vibe/TASKS.md:**
```
✅ Handoff package generated — [mode] — [date]
   Recipient: [name/role]
   Documents: [N] files + index.html portal in vibe/handoff/[mode]-[date]/
   ⚠️ Action required: fill CREDENTIALS.md before sharing
```

---

## Absolute rules

**Never write actual credential values.**
CREDENTIALS.md contains structure and placeholder text only.
If the user asks the skill to fill in credentials — refuse and explain why.

**Every document is grounded in project files.**
Nothing is invented. If a section has no data source, say:
"[This section needs to be filled in — no data found in project files]"
rather than fabricating content.

**Plain English for client documents.**
If a sentence contains a framework name, file path, or technical acronym
without explanation — rewrite it.
"The app uses LangGraph to coordinate the AI agents"
not "LangGraph orchestrates the multi-agent pipeline."

**Known issues are honest.**
Never soften a known issue to the point where it loses meaning.
The client will encounter it. Better they know now than be surprised later.

**The sign-off checklist is binary.**
Every item is done or not done. No "mostly done" or "in progress."
If something isn't ready — it doesn't go on the checklist.
It goes in KNOWN_ISSUES.md.

**Internal documents don't go to clients.**
CONTEXT_DUMP.md, GOTCHAS.md, OPEN_QUESTIONS.md, ACTIVE_TASKS.md
are internal only. Never include them in a client handoff package.
The portal generator knows this — it will include them in the portal
only for internal/dev mode packages, not client or milestone packages.

**The portal is always regenerated after credential edits.**
Remind the user to regenerate index.html after filling CREDENTIALS.md.
The MD file and the portal must stay in sync.
