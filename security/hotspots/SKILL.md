---
name: hotspots
description: Maps security-sensitive code locations in a codebase to focus review effort.
  Use when the user asks to identify security-sensitive areas in a codebase,
  map the attack surface, or find where a security review should focus. Also
  invoke when asked to triage or prioritize security effort across a
  repository.
---

# Security Hotspot Analysis (A06:2025)

## What this checks

Maps security-sensitive code so reviewers know where to focus.
Missed hotspots mean entire attack surfaces go unreviewed.

Single source of truth: this skill delegates to the
`hotspot-mapping` subagent in `.claude/agents/hotspot-mapping.md`. The
subagent's JSON output is the canonical hotspot shape; this skill
adds an architecture summary and renders the result as a priority
table.

## Vulnerable patterns

This skill does not target a single antipattern — the
`hotspot-mapping` subagent identifies areas where vulnerabilities
are statistically most likely (trust boundaries, auth/sessions,
access control, data layer, crypto/secrets, external calls). See
the agent's category taxonomy for the full list.

## Procedure

**Step 1 — Architecture summary.** Read `README*`, `ARCHITECTURE*`,
`docs/`, `SECURITY*`, and `CONTRIBUTING*`. Produce a 3-6 bullet
summary: what the system does, major components, trust boundaries,
auth model, data stores, external integrations. Without this
framing the table below is just a list of files.

**Step 2 — Dispatch the subagent.** Use the **Agent** tool to
dispatch one `hotspot-mapping` subagent. Pass it the architecture
summary as context. The subagent returns a JSON array of hotspots,
each with `file`, `lines`, `name`, `category`, `priority`, `why`.

**Step 3 — Render.** Display the architecture summary, then the
hotspots as a Markdown priority table. Sort rows by priority
(Critical → High → Medium), then by category, then by file. Do
not show the raw JSON.

Report shape:

```
## Architecture summary

- <bullet 1>
- <bullet 2>
- ...

## Hotspots

| Priority | Category | File | Lines | What |
|----------|----------|------|-------|------|
| Critical | AUTH & SESSIONS | src/auth/oauth.py | 60-72 | reads redirect_uri from OAuth response without validating against the registered callback list |
| Critical | DATA LAYER | src/api/handlers/users.py | 42-58 | concatenates request.args['q'] into a raw SQL LIKE clause |
| ...

---

*Run the matching auto-invoking skill against each hotspot, or
launch `/security-review` for a full audit.*
```

## Verification

- [ ] One `hotspot-mapping` subagent was dispatched
- [ ] Architecture summary precedes the table (3-6 bullets from
      the repo's own documentation)
- [ ] Output table has `Priority | Category | File | Lines | What`
      columns
- [ ] Rows are sorted by priority (Critical first)
- [ ] At least one hotspot in each broad category present in the
      repo (auth, data layer, etc.) is represented — recall matters
      more than padding

## References

- CWE-693 ([Protection Mechanism Failure](https://cwe.mitre.org/data/definitions/693.html))
- CWE-657 ([Violation of Secure Design Principles](https://cwe.mitre.org/data/definitions/657.html))
- [OWASP A06:2025 Insecure Design](https://owasp.org/Top10/A06_2021-Insecure_Design/)
