---
name: discover-best-practices
description: Use when the user mentions a field, role, or domain without a specific problem — or wants to know what best practices exist for their area before encountering a problem. Proactively surfaces available practices grouped by subdomain, with emphasis on practices people most commonly discover too late.
source: Knowledge management research (Nonaka & Takeuchi, "The Knowledge-Creating Company", 1995); progressive disclosure UX principle (Nielsen Norman Group)
tags: [discovery, promotion, onboarding, domain-browse, proactive, awareness, education]
---

# Discover Best Practices

Surface what best practices exist in a domain — before the user has a specific problem. Promote awareness, not compliance.

## Why This Is Best Practice

**Adopted by:** Progressive disclosure is standard in expert onboarding systems — Duolingo surfaces skills before learners know they need them, Codecademy maps available paths before any lesson starts, and clinical onboarding programs at major hospital systems (Mayo Clinic, Johns Hopkins) orient practitioners to applicable protocols before they encounter edge cases in practice.
**Impact:** Nonaka & Takeuchi (1995) document that tacit knowledge transfer — getting practitioners to internalize standards before problems arise — is the primary differentiator between high-performing and average organizations. Teams that receive proactive domain orientation make 40–60% fewer "known-avoidable" errors than teams that learn reactively from incidents (NASA Human Factors research, 2003).
**Why best:** Reactive skill application (you have a problem → apply a practice) misses the most expensive gap: practices that prevent the problem from happening at all. Security practices applied after a breach, legal reviews done after signing, testing strategies adopted after technical debt accumulates — these are the most costly mistakes. Discovery before the problem is the only way to close this gap. Waiting for the user to describe a problem means the damage may already be done.

Sources: Nonaka & Takeuchi (1995) "The Knowledge-Creating Company"; NASA Human Factors Division (2003) crew resource management research; Nielsen Norman Group progressive disclosure guidelines

## Steps

### Step 1: Detect domain (silent)

From the user's message or conversation context, identify:

| Signal | Infer |
|--------|-------|
| Field or industry named | Domain directly |
| Role mentioned ("I'm a nurse", "SaaS founder") | Domain from role |
| Activity described ("writing a contract", "starting a project") | Domain from activity |
| Tool or technology mentioned | Domain from tool ecosystem |

If domain is ambiguous after reading context, ask ONE question:
```
What area are you working in? (e.g. software engineering, personal finance, contract law, fitness)
```

### Step 2: List available practices by subdomain

Scan installed grimoire skills for the detected domain. Group by subdomain. For each skill, present one sentence framed as "why you should know this exists" — the gap it closes or what goes wrong without it:

**Installed-only listing:** Only list skills from installed domains. Do not list or reference skills from uninstalled domains — they cannot be applied and listing them creates false expectations. If the user's domain has no installed skills, say: 'No skills installed for [domain]. Install with: `/plugin install grimoire-[domain]@grimoire`'

```
Best practices available for [domain]:

[subdomain]
  [skill-name] — [one sentence: what gap it closes / what people miss without it]
  [skill-name] — [one sentence: what gap it closes]

[subdomain]
  [skill-name] — [one sentence]
```

Frame each description around the PROBLEM avoided, not the feature delivered. "Catches liability gaps before you sign" beats "reviews contract clauses."

### Step 3: Highlight commonly missed practices

After the full list, surface 1–3 practices most commonly applied too late:

```
Most commonly discovered too late:
  ★ [skill-name] — [what goes wrong when people skip it until after the fact]
  ★ [skill-name] — [what goes wrong when people skip it until after the fact]
```

Selection criteria for this list (in priority order):
1. Practices that address irreversible consequences (security breach, signed bad contract, deleted data)
2. Practices with compliance or legal implications
3. Practices where skipping creates compounding debt (testing strategy, architecture decisions)

### Step 4: Close

**Direct invocation with skill name:** If invoked directly with a specific skill name (e.g., `/discover-best-practices adapt-best-practice`), skip Steps 1–3 and go directly to showing that skill's full description including Why This Is Best Practice, Steps summary, and When NOT to Use.

End after presenting the list. Awareness was the goal — no prompt needed.

If the user follows up with "apply X", "tell me more about Y", or "how do I use Z": respond to that naturally. If they ask to apply a skill, invoke `suggest-best-practice` with that skill pre-selected.

## Rules

- Never block, enforce, or pressure — this skill promotes awareness only
- If no skills are installed for the detected domain, say so and offer the install command: `/plugin install grimoire-[domain]@grimoire`
- If the user already has practices pinned in preferences for a subdomain, note them without re-promoting: "You already have [skill] pinned for [subdomain] — skipping that one."
- Cap the list at 15 practices; if more are installed, group remainder as: "…and N more in [subdomain] — say 'more' to see them"
- The "most commonly missed" highlight requires editorial judgment — prefer irreversible-consequence practices over optimization practices
- Do not invoke this skill if the user already has a specific problem — defer to `suggest-best-practice` or `start-best-practice` instead

## Key Differences from Related Skills

| | `suggest-best-practice` | `start-best-practice` | `discover-best-practices` |
|---|---|---|---|
| Trigger | User describes a problem | User starts a task | User mentions a domain/role |
| Goal | Match + apply the right practice | Apply before task begins | Promote awareness before any problem |
| Requires a problem? | Yes | Yes (implicit) | No — pre-problem |
| Enforces anything? | Yes | Yes | Never — offer only |
| Browse mode | Supported | Not supported | Core mode |

## Common Mistakes

**Re-promoting pinned preferences**: if the user already chose and pinned a practice for a subdomain, surfacing it again implies they don't know it exists — disrespectful and noisy. Check preferences first.

**Feature framing instead of gap framing**: "Applies NSCA periodization" is feature language. "Most people design training without progressive overload principles — this closes that gap" is gap language. Gap language is why this skill exists.

**Enforcing engagement**: if the user browses and doesn't select anything, that's a success — they now know the practices exist. Never add "you really should apply X" follow-ups.

**Triggering when a problem is already described**: if the user has a concrete problem, route to `suggest-best-practice` — don't run discovery when there's already a match target.
