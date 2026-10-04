---
name: orbit-elementor-compat
description: Across-Elementor-versions compatibility audit — fetches Elementor's current changelog + deprecation list at RUNTIME, then audits the plugin against today's reality. Auto-handles V3, V4 Atomic, V5+ as they ship — no manual rule update needed. Use when the user says "Elementor compat", "across versions", "after Elementor major release", "V4 atomic check", "deprecated Elementor APIs".
---

# 🪐 orbit-elementor-compat — Runtime-evergreen Elementor compatibility

> The skill that auto-stays-current with Elementor's release cadence. No "V4 atomic" hardcoding — it fetches what's current at runtime.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://elementor.com/pro/changelog/ → latest version + last 5 releases' changes
   - https://developers.elementor.com/docs/deprecations/ → current deprecation list
   - https://github.com/elementor/elementor/releases → latest tag + release notes
   - https://github.com/elementor/elementor/blob/main/CHANGELOG.md → free-version changelog
   - https://developers.elementor.com/elementor-editor-4-0-developers-update/ → V3→V4 migration (still relevant during coexistence)

2. **Synthesize current state**:
   - "What is the current major Elementor version as of today?"
   - "What APIs were deprecated in the last 2 minors? Last 6 months?"
   - "What new APIs / patterns has Elementor introduced that the plugin should adopt?"
   - "Has V4 become default for new sites yet (it did April 2026 per their announcement)?"
   - "Which V3 widgets / V4 Atomic Elements are the latest equivalents?"

3. **Audit the plugin** against the synthesized current rules.

---

## What gets checked (today's rule set, derived from today's fetch)

### A. Use of currently-deprecated APIs
Whatever the fetched deprecation list says. Examples (as of last fetch — may differ today):
- `_register_controls()` → `register_controls()` (no underscore)
- `widgets_registered` hook → `elementor/widgets/register`
- `Element_Base::get_settings()` direct → `get_settings_for_display()`
- Old `Stack` direct access → `Document` API

If the fetched list shows new deprecations the embedded list doesn't have — audit catches them anyway, because we trust the fetched list.

### B. Container layout adoption
Elementor 3.6 introduced Containers. New addons should target Container; old addons should still support Section/Column for back-compat. Plugins still emitting Section markup post-3.6 (now ~4 years old) get flagged for "should support Container."

### C. CSS variables vs hardcoded values
Elementor 3.18+ uses CSS custom properties. Hardcoded `color: #333` doesn't respect user's theme.

### D. V3 widget vs V4 Atomic Element
**Per fetched V4 announcement:** From April 2026 forward, new sites default to V4 with both V3 widgets + V4 Atomic Elements available. Plugin extensions should:
- Continue to ship V3 widgets (V3 sites still active)
- Optionally also expose Atomic Element variants for V4 sites
- Use the coexistence patterns documented in V4 dev update

If your plugin ONLY ships V3 widgets, that's currently fine — no urgent migration. But for new development, ship both.

### E. Editor V4 selectors / DOM
V4's editor DOM differs from V3. Playwright tests targeting V3 admin selectors (`#elementor-panel-search-input`, etc.) need to be split into V3 + V4 spec sets.

### F. Future versions (V5+ when they ship)
The runtime-fetch design means when Elementor V5 ships, this skill picks up the new deprecations / patterns automatically. No "manually edit SKILL.md to add V5 rules" — the changelog IS the rule source.

---

## Multi-version test matrix

```bash
PLUGIN_SLUG=my-plugin \
  bash ~/Claude/orbit/scripts/elementor-version-matrix.sh
```

Versions tested: latest 3 minors of Elementor + the version pinned in your `qa.config.json` (defaults to "latest 3 minors fetched from Elementor's repo today").

Sites spun up in parallel (port 8881 / 8882 / 8883 ...), each running a different Elementor version. Plugin's smoke spec runs against each. Pass/fail matrix output.

---

## Output

```markdown
# Elementor Compat — my-plugin · 2026-04-30

> Per elementor.com/pro/changelog (fetched 2026-04-30 14:32 UTC):
> Current Elementor version: 3.30.x (Pro), 3.30.x (Free)
> V4 Atomic became default for new sites: April 2026
> Active deprecations in last 6 months: 4

## Test matrix
- 3.28 — ✓ pass
- 3.29 — ⚠ console warning ("get_settings() direct access — use get_settings_for_display")
- 3.30 — ❌ fail — 1 widget renders blank
- V4 Atomic (default new sites) — ⚠ Atomic Element equivalent not exposed

## Deprecations matched in source
- ❌ `_register_controls` (underscore prefix) — 12 widgets — deprecated 3.1
- ❌ `widgets_registered` hook — 1 — deprecated 3.5
- ⚠ `Element_Base::get_settings()` direct — 3 — deprecated 3.18

## CSS variables
- ✓ 35 widgets use `var(--e-global-color-*)`
- ⚠ 12 widgets hardcode colors

## V3 / V4 split
- 14 V3 widgets shipped
- 0 V4 Atomic Element equivalents
- Recommendation: V3 stays for back-compat; ship Atomic equivalents for new V4 sites

## Severity: HIGH (3.30 fail + deprecations)
```

---

## Pair with

- `/orbit-elementor-dev` — code-side widget audit
- `/orbit-elementor-controls` — control system
- `/orbit-elementor-pro` — Pro extension specifics
- `/orbit-uat-elementor` — end-to-end UAT
- `/orbit-conflict-matrix` — vs other plugins

---

## Smoke test

Input: a plugin with 1 widget using `_register_controls` (underscore prefix).
Expected:
- 1 ❌ HIGH for deprecated underscore prefix
- Cites the live fetched deprecations URL with today's date
- Test matrix shows pass on 2 of 3 latest Elementor versions

---

## Embedded fallback rules (offline)
- `_register_controls` underscore prefix deprecated since 3.1
- `widgets_registered` hook deprecated since 3.5
- Container layout (3.6+) preferred over Section/Column for new code
- CSS variables (3.0+) preferred over hardcoded values

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Elementor Pro changelog](https://elementor.com/pro/changelog/) — version + breaking changes
- [Elementor Free changelog (GitHub)](https://github.com/elementor/elementor/blob/main/CHANGELOG.md)
- [Deprecations](https://developers.elementor.com/docs/deprecations/) — actively maintained list
- [GitHub Releases](https://github.com/elementor/elementor/releases) — latest tag
- [V4 Developer Update](https://developers.elementor.com/elementor-editor-4-0-developers-update/) — coexistence patterns

### Last reviewed
2026-04-30 — runtime-evergreen; auto-handles V4, V5, V6 when they ship
