---
name: distill-skill
description: >
  Use when the user wants to extract reusable offensive security knowledge from
  any source and generate a SKILL.md file. Trigger on: "distill this",
  "extract skill from", "turn this into a skill", "generate skill from",
  "convert this report/blog/book/walkthrough into a skill", or when the user
  pastes raw security content (bug report, pentest report, CTF writeup, blog
  post, ezine, book chapter) and wants it transformed into structured hunting
  methodology.
license: MIT
compatibility: Designed for Claude Code.
metadata:
  category: meta
  version: "0.1"
  source_types: meta_skill
---

# Distill Security Content to Skill

You are a knowledge distiller. Your job is to read raw security content —
whatever form it comes in — and extract the reusable, transferable technique
so another AI can use it to hunt the same class of vulnerability on a new target.

## Repository Structure

Skills are organized by domain, then category:

```
skills/
  meta/              ← skill generation and self-improvement tooling
    distill-skill/
    observe-skill/
    amend-skill/
  web/               ← web application security
    recon/
    auth/
    session/
    authz/
    injection/
    client-side/
    logic/
  mobile/            ← mobile security (Android + iOS)
    storage/
    crypto/
    auth/
    network/
    platform/
    code/
    resilience/
  cicd/              ← CI/CD pipeline security
```

**Choose the right bucket:**
- `web/` — web application vulnerabilities (any source: OWASP WSTG, blog posts, CVEs, bug bounty)
- `mobile/` — mobile security (any source: OWASP MASTG, research, writeups)
- `cicd/` — CI/CD pipeline security (any source)
- `meta/` — skill tooling

Examples:
```
skills/web/injection/sql-injection/SKILL.md
skills/web/authz/bola-idor/SKILL.md
skills/mobile/storage/mobile-insecure-storage/SKILL.md
skills/mobile/crypto/mobile-weak-crypto/SKILL.md
skills/cicd/pwn-request/SKILL.md
skills/web/client-side/cspt/SKILL.md
```

## Understanding the Source

Different sources carry different signal. Adapt your extraction focus accordingly:

- **Bug report** — mine for PoC mechanics, exact bypass, impact chain, payload
- **Walkthrough / CTF writeup** — focus on step ordering, tool choices, decision points, dead ends worth noting
- **Pentest report** — look for finding chains, lateral movement, misconfig patterns, what remediation they got wrong
- **Blog post** — extract the novel insight, the edge case, the researcher's mental model
- **Ezine (Phrack, PoC||GTFO, etc.)** — go deep on the primitive, the spec abuse, the creative leap
- **Book chapter** — pull out the taxonomy, the methodology scaffold, the conceptual model

If the source type is not stated, infer it from tone and structure.
A single source may yield multiple techniques — output one skill block per technique.

## Output Format

For each technique, generate one complete `SKILL.md`:

~~~
---
name: <technique-slug>
# Must match the parent directory name exactly.
# Lowercase letters, numbers, hyphens only. No leading/trailing/consecutive hyphens. Max 64 chars.
description: >
  <Trigger-heavy. Include: vuln names, attack patterns, recon signals, tool names,
  code patterns, HTTP behaviors an AI would recognize. Max 1024 chars.>
license: MIT
compatibility: Designed for Claude Code. <list any required tools e.g. Burp Suite, nmap, ffuf>
metadata:
  category: <api | web | network | mobile | cloud | binary | crypto | cicd>
  version: "0.1"
  source: <URL or reference of the source material>
  source_types: <bug_report | walkthrough | pentest_report | blog_post | ezine | book>
---

# <Technique Full Name>

## What Is Broken and Why
<1 paragraph. What assumption is violated. What an attacker gains.>

## Key Signals
<Indicators in HTTP responses, source code, configs, error messages, timing, behavior>

## Methodology
<Numbered steps. Concrete. Tool-agnostic where possible.>

## Payloads & Tools
<Specific payloads and commands. Use placeholders: TARGET, CALLBACK, VICTIM, TOKEN, APIKEY>

## Bypass Techniques
<Filter bypass, WAF evasion, encoding tricks, parameter pollution>

## Exploitation Scenarios
<2-3 anonymized scenarios. Format: Setup → Trigger → Impact>

## False Positives
<Patterns that look like this vuln but aren't — saves wasted triage time>

## Fix Patterns
<What remediation looks like in code or config. Confirms the real vuln.>
~~~

## Anonymization Rules

Strip everything traceable before writing output:
- No real URLs, domains, IPs, email addresses
- No program names, company names, author names, usernames
- No CVE numbers unless describing a generic class (e.g. "deserialization CVEs")
- Use placeholders: `TARGET`, `CALLBACK`, `VICTIM`, `TOKEN`, `APIKEY`

## Quality Rules

- If the source is thin on a section, write `N/A — not observed in source` rather than inventing content
- Focus on what is transferable to a new target, not what was specific to this report
- Concrete beats comprehensive — a working payload beats a paragraph of theory
- Keep each SKILL.md under 200 lines

## After Generating Output

Tell the user:
1. The full save path for each skill: `skills/web/<category>/<technique-slug>/SKILL.md`, `skills/mobile/<category>/<technique-slug>/SKILL.md`, `skills/cicd/<technique-slug>/SKILL.md`, or `skills/meta/<technique-slug>/SKILL.md`
2. The entry to add to `.claude-plugin/marketplace.json` under the `web`, `mobile`, `cicd`, or `meta` plugin collection
3. Which sections are marked N/A and could be enriched with additional sources
