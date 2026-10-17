---
name: pir
description: Generate a post-incident report (PIR) from the current session and write it to docs/pir/. Use this skill whenever the user types "/pir", "write a PIR", "write up what happened", "document this incident", "post-incident report", "post-mortem", or "incident retrospective". Use it proactively whenever a debugging session, production outage, failed deployment, data migration incident, or any problem-solving session is winding down — even if the user doesn't explicitly say "PIR". The output is a structured markdown document capturing the timeline, root cause, impact, resolution, and lessons learned.
version: 0.1.0
---

# Post-Incident Report (PIR)

You are generating a structured post-incident report from the current session. The goal is institutional memory: a concise, honest account of what happened, why, and what to do differently — useful to the team a month from now, not just today.

---

## Phase 0 — Identify the incident

Read the current conversation history. Extract:

- **What broke or went wrong** — the incident itself
- **When it was noticed** — timestamps if present in the session
- **What systems, code, or infrastructure** were involved
- **What was tried** during investigation
- **What fixed it** — or whether it's still unresolved

If you can't identify a clear incident (the session was about building a feature, not resolving a problem), stop and ask: *"I don't see a clear incident in this session — what would you like to document?"* Let the user describe it in 1–2 sentences, then continue.

If there are multiple incidents, pick the most recent and prominent one as the primary subject. Mention any others briefly in the Summary.

---

## Phase 1 — Gather metadata

Before writing, determine four things:

**Severity** — infer from the context:
- `Critical` — production service down, data loss, security breach, user-facing outage
- `High` — degraded production service, significant but partial user impact, near-miss in production
- `Medium` — staging/non-prod incident, limited user impact, caught before widespread harm
- `Low` — developer environment only, debugging session, no user impact

**Status** — infer from how the session ended:
- `Resolved` — a fix was deployed or confirmed working
- `Monitoring` — a fix was applied but not yet verified in production
- `Ongoing` — the problem is still open at the end of the session

**Duration** — use timestamps from the session if present. If not, use rough language: `~2 hours`, `~30 minutes`, `unknown`.

**Date** — run `date +%Y-%m-%d` to get today's date for the filename and frontmatter.

---

## Phase 2 — Synthesize the report

Fill in the template below from what you extracted in Phase 0. Write for someone reading this cold in three months — not the person who was there.

A few things that make a PIR genuinely useful:

- **Timeline** entries should be specific, not vague: "Noticed HTTP 500s on `POST /api/checkout`" beats "something broke"
- **Root Cause** should explain the mechanism, not just name the culprit: "The deploy script does not propagate secrets from Vault to the container environment, so `DATABASE_URL` was unset in production after rollout" beats "missing env var"
- **Action Items** should be actionable with an owner; if the owner is unknown write `— (unassigned)`
- **Lessons Learned** should be honest about what was missed, not generic platitudes like "add more monitoring" — the more specific, the more valuable

### Template

Use this exact structure:

---

```markdown
# Post-Incident Report: <Incident Title>

**Date**: YYYY-MM-DD
**Severity**: Critical | High | Medium | Low
**Status**: Resolved | Monitoring | Ongoing
**Duration**: ~X hours / minutes / unknown

## Summary

One paragraph. What happened, when it was detected, what was affected, and how it was resolved. Avoid jargon the reader might not know.

## Timeline

- `HH:MM` — Event or action taken (24h clock if possible; omit times if unavailable, use relative language instead)
- `HH:MM` — …

## Root Cause

The technical mechanism that caused the incident. Explain *why* it happened, not just *what* happened.

## Impact

- **Systems**: impacted services, APIs, databases, pipelines, or jobs
- **Users**: affected user count or segment (e.g. "all checkout users"), or "internal only"
- **Duration**: how long the impact was observable
- **Data**: any loss, corruption, or degradation — or "none"

## Resolution

Exactly what fixed it — specific commands run, code changed, configs updated, deploys triggered. Be concrete so someone could reproduce the recovery.

## Action Items

- [ ] What needs to happen — owner (if known)

## Lessons Learned

What would have caught this earlier. What made recovery harder than it needed to be. What the team will do differently next time.
```

---

## Phase 3 — Write to disk

1. Construct the filename: `<date>-<kebab-incident-slug>.md`
   - The slug should be 3–5 words capturing the incident essence, e.g. `2026-06-05-missing-env-var-checkout.md`
2. Before writing, tell the user the target path and confirm: *"I'll write this to `docs/pir/2026-06-05-missing-env-var-checkout.md` — OK to proceed?"*
3. Create the directory if it doesn't exist: `mkdir -p docs/pir`
4. Write the file.

---

## Phase 4 — Offer to update CLAUDE.md

After the file is written, check whether the project's `CLAUDE.md` already references `docs/pir/` or incident history. Search for the string `pir` or `incident` in CLAUDE.md case-insensitively.

If the reference isn't there yet, offer:

> "Want me to add a reference to `docs/pir/` in your CLAUDE.md? That way future Claude sessions will automatically read past incident reports for context before working on affected code."

If the user says yes, append this block to CLAUDE.md:

```markdown
## Incident history

Past post-incident reports live in `docs/pir/`. Before working on code that has caused incidents before, read the relevant PIR(s) for context on root causes, resolutions, and open action items.
```

If no `CLAUDE.md` exists in the project root, note it: *"There's no CLAUDE.md in this project yet — consider creating one and adding the incident history reference so future sessions have this context."* Don't create the file automatically.
