---
name: dungeon-crawl-threat-map
description: Analyze a repo or codebase and produce a full threat model, an ASCII architecture diagram, a plain-language walkthrough of what it does, a "worth a second look" checklist of notable authentication, cryptography, and access-control call-outs, and a STRIDE-driven breakdown of threats mapped to the OWASP Top 10 and the OWASP Cheat Sheet Series. Written like a coach or mentor teaching AppSec concepts, not a scan report. Trigger this whenever the user asks to "threat model this repo/codebase," "map the attack surface," "what are the security risks here," "STRIDE this," "generate a threat model diagram," "draw the architecture and threats," "check the auth on this," "any weak crypto in here," or "walk me through the risks in this code." This is not a SAST/SCA scan and doesn't replace one, it's an architecture-level understanding exercise that produces a reusable artifact.
---

```
______ _   _ _   _ _____  _____ _____ _   _   _____ ______  ___  _    _ _     
|  _  \ | | | \ | |  __ \|  ___|  _  | \ | | /  __ \| ___ \/ _ \| |  | | |    
| | | | | | |  \| | |  \/| |__ | | | |  \| | | /  \/| |_/ / /_\ \ |  | | |    
| | | | | | | . ` | | __ |  __|| | | | . ` | | |    |    /|  _  | |/\| | |    
| |/ /| |_| | |\  | |_\ \| |___\ \_/ / |\  | | \__/\| |\ \| | | \  /\  / |____
|___/  \___/\_| \_/\____/\____/ \___/\_| \_/  \____/\_| \_\_| |_/\/  \/\_____/

 _____ _   _ ______ _____  ___ _____  ___  ___  ___  ______ 
|_   _| | | || ___ \  ___|/ _ \_   _| |  \/  | / _ \ | ___ \
  | | | |_| || |_/ / |__ / /_\ \| |   | .  . |/ /_\ \| |_/ /
  | | |  _  ||    /|  __||  _  || |   | |\/| ||  _  ||  __/ 
  | | | | | || |\ \| |___| | | || |   | |  | || | | || |    
  \_/ \_| |_/\_| \_\____/\_| |_/\_/   \_|  |_/\_| |_/\_|    
```

*Accent: Dungeon Violet. Deep purple, the color of an unlit passage on the map screen.*

# Dungeon Crawl: Threat Map

## Why this skill exists

A SAST or SCA tool finds *instances* of bad patterns: this line has an injectable query, this package has a CVE. That's valuable, but it's not the same job as understanding *how a system is shaped* and where that shape creates risk. A perfectly clean line-by-line scan can still sit inside an architecture with no trust boundary between the public internet and an admin API, or a service that trusts every header a client sends it.

This skill does the second job: read the codebase like a new AppSec engineer would on their first week on a team, build a mental model of what it does and how the pieces talk to each other, then reason about where that model breaks under an adversary's pressure. The output is meant to be *kept*, dropped into a wiki or a PR description, handed to a teammate who's never seen this repo, and still make sense a year from now. It teaches while it reports: terms get defined, reasoning is shown, nothing is asserted without either a citation or an explicit "this is architectural, no single line proves it."

This is also, specifically, the skill built to catch OWASP A06:2025 Insecure Design, the category made of flaws in a system's architecture and workflow rather than in any single line of code: a missing authorization check that was never designed in, a password reset flow with no rate limit, a service that trusts a client-supplied header because nobody drew the trust boundary that would have flagged it. A scanner can't find A06 issues because there's no bad pattern to match, the design itself is the vulnerability. That's exactly the gap this skill closes, see Step 6 for how it gets called out.

## When to use this

- The user asks to threat model a repo, service, or specific directory.
- The user asks what the attack surface looks like, or "what could go wrong" with a codebase.
- The user wants an architecture diagram that also shows where the risk sits.
- The user is onboarding to a new codebase and wants a security-focused orientation.
- The user wants something to hand to a team, auditor, or new hire that explains both the system and its risks.

If the user instead pastes a single scanner finding and wants to know if it's exploitable, that's [`player-two-verdict`](../player-two-verdict)'s job, not this one. This skill builds the big picture; that one verifies a specific claim.

## Step 0: Prerequisite check

Confirm the target path (the repo, service, or directory the user named) exists and is readable. This skill has no scripts and no network dependency, it reasons directly over repo files, so there's nothing else to check here. The scope decision (single service vs. a large monorepo) is a judgment call, not an environment check, that stays in Step 1.

## Step 1: Recon the codebase

Figure out what you're actually looking at before modeling anything.

- **Language and framework**: read manifests and lockfiles (`package.json`, `requirements.txt`/`pyproject.toml`, `pom.xml`/`build.gradle`, `go.mod`, `Gemfile`, `composer.json`, `*.csproj`, etc). Note every language present, not just the dominant one, mixed-language repos carry mixed risk.
- **Entry points**: HTTP routes, CLI commands, message queue consumers, scheduled jobs/cron, webhooks, GraphQL resolvers, gRPC services. Anything an external actor or another system can trigger.
- **External integrations**: databases, third-party APIs, cloud services, auth providers (OAuth/SSO), payment processors, queues, caches.
- **Secrets and config handling**: where credentials, API keys, and tokens come from (env vars, secret manager, hardcoded, `.env` files) and how config is loaded per environment.
- **Scope check**: if this is a large monorepo with many unrelated services, don't silently pick one. Ask the user which service or directory to scope to. Modeling "the whole monorepo" at once produces a diagram too dense to be useful and threats too generic to act on.

## Step 2: Map the architecture

From Step 1's inventory, build:

- **Components**: the app/service itself, its datastores, its external dependencies, anything that runs code (workers, functions, jobs).
- **Trust boundaries**: every place data crosses from a less-trusted context into a more-trusted one, internet → app, app → database, app → third-party API, unauthenticated → authenticated zone, user tier → admin tier. This is the backbone of the STRIDE pass in Step 5: threats live at these boundaries.
- **Data flows**: what moves between components, especially anything carrying user input or sensitive data (credentials, PII, payment data, tokens).

This map is what the ASCII diagram in the final output renders. Keep it to the components and boundaries that actually matter for security reasoning, not a complete infra diagram.

## Step 3: Explain what it does

Before any threat talk, write a plain-language summary of the system: what it's for, who uses it, and its key features. Someone with zero security background and no prior exposure to this codebase should be able to read this section and understand what they're looking at. This grounds everything that follows, a threat only makes sense once the reader knows what's being threatened.

## Step 4: Build the "Worth a Second Look" inventory

Before the deep STRIDE dive, run a fast, targeted scan for specific patterns worth flagging on their own, using what Steps 1-3 already surfaced. This is a checklist, not a narrative, the reader should be able to skim it in under a minute and know exactly what to go verify.

This list doesn't need to avoid overlap with the STRIDE section that follows. An item can appear here as a quick flag and also get a full STRIDE writeup later, when that happens, point back to it ("see Threats (STRIDE) → [component]") instead of repeating the reasoning. Not everything here needs to graduate to a full STRIDE threat either, some things are worth a look without full treatment, e.g. a hardcoded value in a test fixture.

Five categories. Only populate one when something genuinely notable turns up, skip a category, or the whole section, rather than forcing filler entries just to look thorough:

- **Authentication**: for entry points from Step 1, flag anything that looks off, this is not a full per-route inventory. An endpoint that looks like it should require auth but has no visible auth middleware/decorator/guard in its chain; inconsistent auth across near-identical routes (some protected, some not); auth that's only checked client-side; a route whose name or behavior implies privilege (admin, delete, export, internal) with no visible protection; session/token lifecycle problems, no token expiration, no session invalidation on logout or password change, refresh-token reuse with no rotation or revocation.
- **Cryptography**: weak or broken algorithms (MD5, SHA-1, DES, ECB mode) used anywhere security-relevant, password hashing, token signing, encryption; hardcoded keys, secrets, salts, or IVs in source; a non-cryptographic random source (`Math.random()`, `rand()`) used for anything security-sensitive, tokens, session IDs, reset codes; homegrown crypto instead of a vetted library; disabled or overridden TLS/certificate validation.
- **Access Control**: an authorization check that's assumed rather than enforced, a role read from a client-supplied field, an admin action gated only by hiding a UI element instead of a server-side check; object-level checks missing where a user-supplied ID fetches or modifies a record with no ownership or tenant check (IDOR-shaped code); authorization logic duplicated inconsistently across handlers instead of centralized; a permission or auth check that fails open, defaulting to allow if the check itself errors, times out, or can't reach a dependency.
- **Business Logic Abuse**: race conditions on state-changing endpoints, a TOCTOU gap on a balance or inventory check; workflow-bypass, a multi-step process where a later step's endpoint can be hit directly, skipping validation an earlier step was supposed to enforce; price, quantity, or other parameter manipulation via client-controlled values trusted server-side.
- **Other**: an open catch-all for anything else worth a second look that doesn't fit the four buckets above, e.g. dangerous deserialization, `eval`-like dynamic execution of external input, debug or test endpoints and feature flags left enabled, verbose error output that could leak internals, webhook handlers with no signature/HMAC verification that treat an inbound callback payload as trusted, server-side fetches of a user-controlled URL with no allowlist or egress restriction (SSRF), or credentials/API keys/tokens appearing in log statements, error messages, or client-shipped bundles/source maps.

Each entry gets a `file:line` and function/symbol citation, one to two sentences max, phrased as a nudge to go look rather than a fully reasoned verdict, e.g. "Check this out: `/admin/export` has no auth guard in its handler chain, unlike every other `/admin/*` route in this file." No Likelihood/Impact rating here, that reasoning belongs to Step 8.

## Step 5: Threat model with STRIDE

Walk every component and every trust-boundary crossing identified in Step 2 against STRIDE. Define each category in one clause the first time you use it in the output, don't assume the reader already knows the acronym:

- **Spoofing**: an attacker pretends to be someone or something they're not (a user, a service, a trusted source).
- **Tampering**: data or code gets modified in a way it shouldn't be, in transit or at rest.
- **Repudiation**: an action happens and there's no reliable record of who did it, so it can be denied.
- **Information Disclosure**: data is exposed to someone who shouldn't see it.
- **Denial of Service**: the system (or a piece of it) can be made unavailable.
- **Elevation of Privilege**: someone gains access or capability beyond what they should have.

For each applicable threat: name the component or boundary it applies to, cite the specific `file:line` and function/symbol backing it where the code makes the threat concrete, or mark it explicitly as **design-level** when it follows from the architecture rather than a specific line (e.g. "no trust boundary exists between the public API and the internal admin routes" isn't a single-line finding). Don't force all six letters onto every component, only include the ones that genuinely apply, a read-only static file server has a very different STRIDE profile than an auth service.

## Step 6: Map to OWASP Top 10 and the Cheat Sheet Series

For threats that are web-application-relevant, tag the matching OWASP Top 10:2025 category and name the specific Cheat Sheet Series sheet(s) that give remediation guidance, using `${CLAUDE_PLUGIN_ROOT}/references/owasp-top10-cheatsheet-map.md` as the lookup. Don't tag every threat with a category, force-fitting a category onto something that doesn't fit teaches the wrong lesson.

If a threat doesn't fit any of the 10 categories but is still a specific, well-known vulnerability class (GraphQL, WebSocket, JWT, gRPC, and similar have their own sheets but no Top 10 category of their own), check `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`, the full 120-sheet catalog, directly by topic before giving up on a citation. Cite the sheet without an OWASP Top 10 tag in that case, the category tag and the cheat sheet citation are independent, a threat can get one without the other. Only skip the citation entirely when nothing in the full catalog is a genuine match either (e.g. a pure CLI tool with no web-facing surface still gets STRIDE, just no OWASP tag or cheat sheet).

### A06:2025 Insecure Design gets special weight here

Give A06 more attention than the other categories in this step. It's the category this skill is uniquely positioned to find, since it covers architectural and workflow gaps rather than coding mistakes, exactly what Steps 2 and 4 are already reasoning about. Watch specifically for:

- A trust boundary from Step 2 that has no control guarding it at all, not a weak control, an absent one. This maps to CWE-501 (Trust Boundary Violation) and is the clearest A06 signal the diagram can surface.
- A workflow with no limit on repetition or scale: password reset, login, invite, or any endpoint an attacker could hammer with no rate limit or lockout.
- A privilege or role check that's assumed rather than enforced, e.g. a role stored client-side, or an admin action gated only by hiding the UI element, not by a server-side check. Maps to CWE-269 (Improper Privilege Management).
- A file upload or user-supplied path with no type, size, or destination restriction. Maps to CWE-434 (Unrestricted Upload of File with Dangerous Type).
- A feature that assumes trusted, well-behaved input or a cooperative user, with no consideration of what happens if that assumption is wrong.

Most A06 findings will be design-level with no single line to cite, that's the expected shape of this category, not a gap in the evidentiary standard. Say so plainly and cite the Threat Modeling Cheat Sheet as the remediation path: A06's own guidance is to build threat modeling into the design process, which is exactly what this report is doing after the fact.

## Step 7: Factor in language-specific attack vectors

Cross-check the languages and frameworks detected in Step 1 against `${CLAUDE_PLUGIN_ROOT}/references/language-attack-vectors.md`. Only surface a vector if the codebase has actual supporting code for it, an import, a sink, a pattern you can cite by file:line. Don't dump the reference table's full contents into the output, that's noise, not signal, and undermines the "evidence-based" standard the rest of the report holds to. This table covers a handful of common languages, not every ecosystem `cartridge-scanner` can detect; if a detected language isn't in the table, say nothing here rather than treating the absence as "no language-specific risk," this section only reports what it actually checked.

## Step 8: Rate each threat

Use a plain Likelihood × Impact matrix, not DREAD, not raw CVSS. Each axis gets three levels, and define what each level means in this codebase's context the first time you use it:

- **Likelihood**: Low (would require an unusual or difficult set of conditions), Medium (plausible with moderate effort or existing access), High (straightforward, low effort, or already partially exposed).
- **Impact**: Low (limited/contained, e.g. a non-sensitive info leak), Medium (meaningful damage, e.g. one user's data, partial outage), High (severe, e.g. full data breach, full system compromise, all users affected).

Combine into an overall risk tier: 🔴 High (High/High, High/Medium, or Medium/High), 🟡 Medium (the remaining mixed combinations), 🟢 Low (Low/Low, Low/Medium, Medium/Low). State the combination plainly, e.g. "Likelihood: Medium, Impact: High → 🔴 High risk," don't make the reader infer the tier.

## Step 9: Write the output

### Voice

This is the opposite emphasis from a terse verdict block, the goal here is understanding, not speed.

- No em dashes.
- Write like a mentor walking a teammate through their own system for the first time. Conversational, contractions are good, but every claim about the code is still backed by a file:line citation or explicitly marked architectural/design-level.
- Define a term the first time it's used: STRIDE letters, OWASP category names, "trust boundary," "attack surface," anything a working developer without a security background might not know. Don't redefine it every time after that.
- Be exhaustive. This is meant to be a complete artifact someone keeps, not a quick take, cover every component and boundary from Step 2, don't stop at the first few interesting findings. The one deliberate exception is "Worth a Second Look": keep that section genuinely notable-only, a checklist, not a narrative.
- Don't lecture past the point of usefulness. Define a term once, clearly, then move on, don't pad the report with security-101 tangents unrelated to this codebase.
- No unsupported claims. Every threat traces to either a citation or an explicit "design-level" label. If you're genuinely unsure whether something is exploitable, say so and explain what would need to be true to confirm it, don't state it as fact and don't omit it either.
- Prioritize clearly at the end: the reader should walk away knowing what to fix first without having to re-read the whole report.

### Format

Use this structure. Omit a section only if it's genuinely empty for this codebase (e.g. no web-facing surface means no OWASP section), and say so in one line rather than silently dropping it.

```
# Threat Model: [repo/service name]

## Architecture

[ASCII diagram: boxes for each component from Step 2, arrows for data
flows, a clearly marked line or label for each trust boundary. Keep
it readable in a monospace font, prefer simple box-drawing characters
over anything fancy.]

## What this does

[Plain-language overview: purpose, users, key features. No security
framing yet, just grounding.]

## Worth a Second Look

[Only the categories with genuinely notable entries, omit the rest.
If nothing notable turned up anywhere, say so in one line instead of
dropping the section silently.]

### Authentication
- 🔑 `path/file.ext:line`, `functionOrSymbolName()`: [what's notable, 1-2 sentences]

### Cryptography
- 🔐 `path/file.ext:line`, `functionOrSymbolName()`: [what's notable, 1-2 sentences]

### Access Control
- 🚪 `path/file.ext:line`, `functionOrSymbolName()`: [what's notable, 1-2 sentences]

### Business Logic Abuse
- ⚖️ `path/file.ext:line`, `functionOrSymbolName()`: [what's notable, 1-2 sentences]

### Other
- 🔎 `path/file.ext:line`, `functionOrSymbolName()`: [what's notable, 1-2 sentences]

## Threats (STRIDE)

### [Component or boundary name]

- 🔴/🟡/🟢 **[STRIDE category]**: [one-clause definition on first use]
  [what the threat is, in plain language]
  Evidence: `path/file.ext:line`, `functionOrSymbolName()`: [what's
  there] (or: "Design-level: [why no single line applies]")
  Likelihood: [level] · Impact: [level] → [risk tier]
  OWASP: [category, if applicable], see [Cheat Sheet name]

[repeat per applicable STRIDE category per component/boundary]

## Language-specific notes

[Only vectors with real supporting code, cited by file:line. Omit
this section entirely if nothing from the language table actually
applies here.]

## Prioritized actions

1. [🔴 highest-risk item first, plain-language fix guidance]
2. [...]
[ordered highest risk to lowest, this is what the reader acts on first]

## Glossary

[Every term defined inline above, collected here for reference:
STRIDE letters used, OWASP categories used, "trust boundary,"
anything else introduced in this report.]
```

## Step 10: Offer to save

After producing the report, follow the save prompt defined in `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`. Frame it as making the report reusable, something the team can revisit, diff against next time, or hand to someone new, not just chat scrollback that disappears.

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/references/owasp-top10-cheatsheet-map.md`: OWASP Top 10:2025 categories mapped to relevant Cheat Sheet Series sheets, used in Step 6.
- `${CLAUDE_PLUGIN_ROOT}/references/owasp-cheat-sheet-series.md`: the full OWASP Cheat Sheet Series catalog, used in Step 6 as a fallback direct lookup for threats outside the Top 10's 10 categories.
- `${CLAUDE_PLUGIN_ROOT}/references/language-attack-vectors.md`: language/runtime to common attack vector lookup, used in Step 7.
- `${CLAUDE_PLUGIN_ROOT}/references/save-states.md`: the shared save-to-file convention, used in Step 10.
