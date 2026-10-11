---
name: research-before-recommending
description: Full-strength research protocol (multi-candidate comparison, registry/freshness/slopsquatting verification, deprecation cross-check, cited evidence, mini-ADR) for HIGH-STAKES or explicit-ask implementation decisions — a core dependency (auth, database, crypto), a load-bearing algorithm, or an architecture pattern. Triggers when the user explicitly asks for a "best", "modern", "SOTA", or "recommended" choice, or when about to introduce a hard-to-reverse dependency/algorithm. For low-stakes, easily-reversible picks, use the lighter check in the dependencies rule instead — don't invoke this skill for those.
---

# Research before recommending

This is the full-strength version of the `dependencies.md` rule (always
active) — use it for high-stakes or explicit-ask decisions: introducing a
core dependency (auth, database, crypto), picking a load-bearing algorithm,
or when I explicitly ask for "the best" / "recommended" option. For a
low-stakes, easily-reversible pick, the lighter registry/staleness/e18e check
in `dependencies.md` is enough — don't run the full protocol below on every
small choice.

Do not name a library, framework, or algorithm until this protocol completes. Avoid defaulting to a training-distribution favorite (Mulberry32, Express, Mongoose, Redux, Moment, Lodash…) — that is the failure mode this skill exists to prevent. ~20% of libraries cited by LLMs do not exist on the registry (slopsquatting); a confident recommendation without verification is a security risk.

## Mandatory protocol

1. **Define the choice space in one sentence.** State the constraint set: language, runtime, perf budget, ecosystem, deal-breakers. Pull from the project's CLAUDE.md / AGENTS.md and stated requirements.
2. **List 3-5 candidates explicitly.** Even when you "know" the answer, write the alternatives. If you cannot list three, you have not researched enough.
3. **Verify each candidate exists on the registry.** Do not trust memory:
   - `bun pm view <pkg>` / `npm view <pkg>` / `cargo info <pkg>` / `pip index versions <pkg>` — confirms existence + latest version + last publish date.
   - If the package does not resolve, drop it (slopsquatting hit).
   - Last release > 12 months → flag as stale unless the library is mature-stable-by-design (`ms`, `nanoid`, etc.).
4. **Cross-check against deprecation lists.**
   - WebFetch `https://e18e.dev/docs/replacements/`. If your candidate is on the list, the replacement is the new candidate.
   - Known deprecated defaults: Moment → Temporal / date-fns / luxon, Lodash → es-toolkit / native, Request → undici / fetch, Bower → never, jQuery → native DOM unless the project already uses it.
5. **Web-research each candidate** (WebSearch + WebFetch):
   - Official docs — does it endorse this for *our* use case?
   - Bundle size if client-side — bundlephobia / packagephobia / pkg-size.
   - OpenSSF Scorecard — `https://api.securityscorecards.dev/projects/github.com/<owner>/<repo>` for maintenance, vulnerabilities, code-review score (target ≥ 5).
   - Known weaknesses / failure modes for *our* specific constraint.
6. **Prefer live-data MCPs over training memory** when installed:
   - `mcp__context7__*` for versioned library docs.
   - `mcp__deepwiki__*` for repo-level interactive docs.
   - Branch first via MCP, then web-search to fill gaps.
7. **Cite at least 3 independent sources** per major claim. A single blog post is not research.
8. **Compare on the user's actual axes**, not generic "fastest". Pull axes from CLAUDE.md, project memory, or stated priorities.

## Output format (exact structure)

```
## Recommendation
1st: <pick>  — <one-line why>
2nd: <alt>   — <one-line why>
3rd: <alt>   — <one-line why>

## The pick
<name + version + concrete code/config snippet, respecting project rules>

## Why not the others
- <alt>: <one-line trade-off>
- <alt>: <one-line trade-off>

## Evidence
- Registry resolution: <name>@<version>, last publish <YYYY-MM-DD>
- OpenSSF Scorecard: <score>/10
- Bundle size (if client): <kb> gzipped
- e18e replacements check: <on-list with replacement <X> | not-on-list>

## Sources
- <url 1 — what it confirms>
- <url 2 — what it confirms>
- <url 3 — what it confirms>
```

## Mini-ADR (when project has `docs/adr/` or `docs/adrs/`)

Write the decision as `docs/adr/NNNN-<topic>.md` with sections: **Context**, **Decision**, **Alternatives considered**, **Consequences**, **Sources**. Use the next free NNNN. If no ADR directory exists, ask the user before creating one — do not invent the path.

## Anti-patterns (any of these = you failed)

- ❌ "X is the standard" without citing a 2026-fresh source.
- ❌ "I'll use Y" without listing rejected alternatives.
- ❌ Trusting training-distribution defaults (Mulberry32, Express, Lodash, Moment…).
- ❌ Recommending without registry resolution — slopsquatting risk.
- ❌ Comparing on benchmarks from a different language (Rust SIMD ≠ JS perf).
- ❌ Hedging ("you might consider"). Pick one. Defend it. Or say "I don't know" out loud.
