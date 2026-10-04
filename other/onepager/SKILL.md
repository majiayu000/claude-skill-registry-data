---
name: onepager
description: Draft a new ZAOstock one-pager (sponsor / partner / venue / city briefing) and insert it into Supabase stock_onepagers. Renders at zaoos.com/stock/onepagers/<slug>. Bot can edit via /op once inserted.
---

# /onepager - ZAOstock One-Pager Drafter

Drafts a new one-page briefing doc and inserts it into Supabase (`stock_onepagers` table). Renders at `/stock/onepagers/<slug>` on the dashboard. Bot can edit it via `/op` commands once it's there. Single source = DB.

## When to use

- Prepping for a meeting (city official, sponsor, venue manager)
- Drafting a sponsor pitch
- Partner briefing (Heart of Ellsworth, Wallace Events, Art of Ellsworth)
- Artist booking outreach
- Any "I need to send someone a clean one-page summary" moment

## Step 1: Gather context

If the user typed args (e.g. `/onepager Bangor Savings sponsor pitch`), use them. Otherwise ask:

1. **Audience** - who's reading this? Name + title + org. (e.g. "Roddy Ehrlenbach, Director of Parks/Rec, City of Ellsworth")
2. **Purpose** - what's the ask? One sentence. (e.g. "Lock $5K headline sponsor commitment with on-stage signage")
3. **Meeting date / send date** (optional) - when's the conversation? (e.g. "Tue 2026-04-28 5pm at City Hall")
4. **Visibility** - `internal` (default, requires login) or `public` (shareable URL no login)
5. **Reviewers** (optional) - who should review before sending? Default: just Zaal.

Skip questions the user already answered.

## Step 2: Reference the seed pager

The first 1-pager is `roddy-parks-rec`. Read its body via:
```
SELECT body FROM stock_onepagers WHERE slug = 'roddy-parks-rec';
```
Mirror its structure:
- H1 title (event + date)
- Blockquote: title line, contact, date, audience
- **What it is** (1 paragraph + format + anchor partners)
- **Why this audience / venue** (1 paragraph - personal + relevant)
- **Expected scale** (table: attendance, hours, format)
- **What we bring** (bullets - production, insurance, crew, build-in-public)
- **What we'd ask** (numbered list - the actual ask)
- **What success looks like** (1 paragraph)
- **Why now** (1 paragraph)
- Closer: "One ask above all: [the most important thing]"

Tighten for the audience. Sponsor pitch -> emphasize value to sponsor. Venue ask -> emphasize logistics. Artist booking -> emphasize lineup quality + payment terms.

## Step 3: Generate the slug

From audience + purpose: lowercase, hyphens, max 40 chars. Examples:
- "Roddy Ehrlenbach, Parks/Rec" + "permit" -> `roddy-parks-rec`
- "Bangor Savings" + "sponsor pitch" -> `bangor-savings-sponsor`
- "Wallace Events" + "tent partnership" -> `wallace-events-tents`

Check uniqueness: `SELECT 1 FROM stock_onepagers WHERE slug = '<slug>'`. If exists, append `-v2`.

## Step 4: Draft the body

ZAOstock context to use:
- Oct 3 2026, Franklin St Parklet, Ellsworth Maine + Aug 15 dry-run
- The ZAO = ZTalent Artist Organization, music community, 188 members, 4 years building
- Anchor partners: Wallace Events (production), Heart of Ellsworth (community/Cara Romano), Art of Ellsworth (umbrella)
- 19-person volunteer crew across 8 circles (music/ops/partners/finance/merch/marketing/media/host)
- Build-in-public ethos. Free admission, donations + sponsor support.

Tone:
- Direct, grounded, no hype
- No emojis, no em dashes (hyphens only)
- No "thrilled" / "excited" / "amazing" filler
- Match BetterCallZaal voice

## Step 5: Insert into DB

Output the SQL for user to paste into Supabase SQL Editor:

```sql
INSERT INTO stock_onepagers (
  slug, title, audience, purpose, body, status, visibility,
  meeting_date, meeting_location, authors, reviewers, version
) VALUES (
  '<slug>',
  '<title>',
  '<audience>',
  '<purpose>',
  E'<body>',
  'draft',
  'internal',
  '<YYYY-MM-DD or NULL>',
  '<location or NULL>',
  'Zaal',
  '<reviewers or NULL>',
  1
) ON CONFLICT (slug) DO NOTHING;

INSERT INTO stock_onepager_activity (onepager_id, member_id, type, content)
SELECT id, (SELECT id FROM stock_team_members WHERE name = 'Zaal' LIMIT 1), 'created', 'Created via /onepager skill'
FROM stock_onepagers WHERE slug = '<slug>';
```

Use `E'...'` so `\n` becomes a newline. Escape single quotes by doubling: `'` -> `''`.

Use the /clipboard skill (or write to /tmp/clipboard.html) to put the SQL in a one-click-copy page.

## Step 6: Confirm + suggest next steps

Tell user:
- Slug + title
- View at `https://zaoos.com/stock/onepagers/<slug>` (after Vercel deploy)
- Edit later via dashboard inline editor or bot `/op <slug>`
- If reviewers were specified, generate a Telegram DM asking them for feedback

## Anti-patterns

- Don't write a 3-page doc. One page printed = ~600 words tops.
- Don't include sponsor amounts unless user explicitly says them.
- Don't fabricate attendance numbers - use range estimates and flag as "estimate".
- Don't promise things that need legal review - say "TBD" instead.
- Don't write to `ZAO-STOCK/onepagers/*.md` - deprecated, single source = DB.

## Editing existing 1-pagers

The skill creates new 1-pagers only. To edit existing ones:
- Dashboard: `/stock/onepagers/<slug>` -> Open the editor
- Bot: `/op <slug> append <text>` · `/op <slug> status sent` · `/op <slug> note "..."`
- Or update DB row directly
