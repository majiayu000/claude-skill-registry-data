---
name: orbit-ip-cleanroom
description: IP / copyright clean-room audit for a WordPress plugin — when a plugin is built in the same space as a competitor whose code, zip, or WP.org download was studied, this scans the plugin so "understanding the flow" never becomes copying the work. Extracts the reference's reserved identifiers (text domain, function/class prefixes, custom hooks, option keys, REST namespaces, block names, shortcodes, handles), then scans OUR plugin for any of them leaking in, plus copied strings/readme/assets, GPL-compatibility of bundled libs, and a provenance manifest. Use when the user says "clean-room this plugin", "did we copy", "competitor zip", "IP check", "copyright check", "is our plugin too close to theirs", or before any WP.org release. Detailed runbook + escalation policy is read live from brain (orbit/07-security). Engineering risk-reduction, NOT legal advice.
---

# 🪐 orbit-ip-cleanroom — IP / copyright clean-room audit

The check for the everyday situation: a plugin is built in the same niche as a competitor whose work was studied (a shared zip, a WP.org download, a "build like X" reference). This skill makes sure understanding the flow never turns into copying the expression.

> **Engineering risk-reduction, NOT legal advice and no safe harbor.** Anything this skill marks **STOP** must be escalated to the project's legal / IP owner before proceeding — never resolved silently inside the skill.

> **Rule -2 — brain is the live runbook.** Before running, read your IP clean-room runbook from brain FIRST:
> ```
> brain_search(wing="orbit/07-security", query="ip-cleanroom RUNBOOK")
> brain_search(wing="orbit/00-cto",      query="ip clean-room hard-rule STOP conditions")
> ```
> The brain drawer holds the current escalation contact, the authorization/EULA checklist, and any org-specific policy. The repo ships the mechanics; brain ships the policy. Brain wins when they disagree.

---

## ⚖️ Two myths to kill before anyone touches a reference

1. **"WordPress is all GPL, so I can copy their code."** FALSE. GPL is a *license with conditions*, not a transfer of copyright. Copying a competitor's GPL PHP into our plugin and shipping it as ours — especially after stripping their copyright headers — is **both copyright infringement and a GPL violation** (GPL requires you keep their copyright notices and attribute; you cannot relicense their expression as ours). GPL lets us reuse the WordPress APIs and ideas freely; it does not let us lift another author's expression.
2. **"It's just a reference, I'll rewrite it in my own words."** Paraphrasing copied code is still a derivative work — structure, sequence, and organization are protected (abstraction-filtration-comparison test). The only clean path for genuinely derived logic is rebuild-from-spec by an actor that never saw their code.

> **🛑 STOP — premium / obfuscated plugins.** If the reference is an encrypted / obfuscated / ionCube / licensed *pro* plugin and you are decompiling or deobfuscating it, **STOP**. That likely violates the vendor EULA and the DMCA anti-circumvention rules (17 U.S.C. §1201) — a separate offense from copyright. Escalate to legal before any further work. Do not proceed inside this skill.

---

## Workflow

Use a neutral run dir `.clean-room/<plugin-slug>/` (gitignored — quarantined reference code must never ship). Create a `TaskCreate` list and work the phases.

### Phase 1 — Intake & quarantine the reference (`--mode intake`)
Never unzip a competitor plugin into our plugin's tree or repo. Quarantine it.
```bash
bash scripts/ip-intake-scan.sh <reference.zip-or-dir> .clean-room/<slug>/
```
This:
- Records source, how it was obtained, and date (chain of custody → `intake-record.md`).
- Detects the license (readme.txt `License:`, plugin header `License:`, LICENSE file). Flags **copyleft beyond plain GPL** (AGPL → SaaS implications) and **proprietary / encrypted** code (→ STOP above).
- Extracts the reference's **reserved identifiers we must NOT reuse**: text domain, function/class prefixes, option/transient keys, custom hook & filter names, REST namespaces, block names, shortcode tags, CSS/JS handle prefixes, DB table names → `reserved-identifiers.txt`.
- Lands everything in `.clean-room/<slug>/reference/` (quarantine), never in the shipped tree.

### Phase 2 — Decide: learn, or reimplement?
- **Learning the flow / which WP APIs & hooks they use / the UX / the feature set** = studying *ideas*. Fine. Capture it as a behavioral spec, in your own words, with zero code excerpts.
- **Needing their actual code, structure, strings, or assets** = derived. Reimplement (Phase 4), ideally with a fresh source-denied agent / separate session.

### Phase 3 — Audit our plugin for leakage (`--mode audit`)
Scan OUR plugin against the reserved-identifier list and the generic copyright signals:
```bash
bash scripts/ip-leak-scan.sh <our-plugin-path> .clean-room/<slug>/reserved-identifiers.txt
```
Flags any of the reference's identifiers, distinctive strings, copied readme/changelog wording, or GPL/author headers appearing in our code. Triage 🟢/🟡/🔴 per `references/leak-signals.md`:
- 🟢 cosmetic (a stray comment) → scrub.
- 🟡 → human judgment (extent + distinctiveness).
- 🔴 copied code/structure/strings/assets, or any reused custom hook/option/class name → reimplement.

### Phase 4 — Clean-room reimplement the 🔴 parts
Rebuild from a behavioral spec (discovery → spec → fresh source-denied agent → verify). For WordPress, additionally verify:
- All identifiers use **our** prefix / text-domain, none from the reference.
- `readme.txt`, plugin header, `block.json`, changelog, and screenshots/descriptions are original.
- Any bundled assets (icons, banners, images, fonts, JS/PHP libs) are licensed for **redistribution in a product** — bundling is redistribution and most stock licenses forbid it without an extended license.

### Phase 5 — Provenance & WP-store hygiene
```bash
bash scripts/ip-manifest.sh <our-plugin-path> .clean-room/<slug>/ "<reference-id>" "<pinned-version>" "<model>"
```
- Ship a `THIRD-PARTY-NOTICES` / `CREDITS` file listing every bundled library + its license (retain MIT/BSD notices; honor attributions). WP.org requires 100% GPL-compatible — verify no bundled lib is incompatible (no proprietary; mind AGPL).
- **Trademark / name check:** our plugin name, slug, and tagline must not use the competitor's mark or be confusingly similar. Check WP.org slug availability, USPTO/EUIPO, and domain.

---

## WordPress-specific leak signals (the ones devs forget)

These are the reference author's **expression**, not WordPress's — reusing them signals copying and can break compatibility. Full severity table in `references/leak-signals.md`.

- **Text domain** and the **translatable strings** themselves (UI copy is copyrightable).
- **Function / class / namespace prefixes** (e.g. `xyz_`, `XYZ_Plugin`).
- **Custom hook & filter names** the author invented (`do_action('their_custom_event')`).
- **Option keys, transient keys, post-meta keys, DB table names, cron event names.**
- **REST API namespace/routes, AJAX action names, nonce action strings.**
- **Block names** (`namespace/block`), **shortcode tags**, **widget IDs**.
- **CSS class prefixes & JS handle names.**
- **readme.txt** sections, FAQ wording, changelog phrasing; **screenshots** and **banner/icon** art.

> WordPress's *own* names (`add_action`, `wp_enqueue_script`, `init`, `the_content`) are the platform API — required and fine. Only the **author-invented** names above are their expression.

---

## Final gate (block release on any unmet item)

- [ ] No reference identifier, string, readme/meta wording, or asset in our plugin (leak-scan clean).
- [ ] 🔴 items reimplemented from spec; similarity to reference is low.
- [ ] 100% GPL-compatible; THIRD-PARTY-NOTICES shipped; bundled assets cleared for redistribution.
- [ ] Name / slug / trademark cleared.
- [ ] Provenance manifest written; user told what is clean vs. still-pending.
- [ ] If a premium / obfuscated plugin was involved → escalated to legal, not silently used.

---

## Ownership & wiring

- **Owner:** `orbit-security` — same family as its GDPR / PCI / trademark compliance charter (everything that can get a plugin pulled or a user harmed).
- **Release gate:** `orbit-release` runs this as a hard pre-ship gate — no clean provenance, no release.
- **Review:** `orbit-code-reviewer` flags reference-identifier leakage during PR review.
- Runs in `/orbit-gauntlet --mode full` and `--mode release`.

Plugin-agnostic — no plugin name is hardcoded. Detailed runbook, escalation contact, and org policy live in brain (`orbit/07-security`), read live on every run.
