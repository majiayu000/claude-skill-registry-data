---
name: purging-icon-slop
description: "Use whenever Kyle says icon slop, de-slop the icons, visual identity cleanup, icon inventory, icon audit, replace generic icons, custom SVG icons, typed icon registry, ban lucide, ban heroicons, no emoji icons, 'the UI looks like a default shadcn template', 'these icons are generic', 'make the icons ours', or hands over any app/template/skill library and wants generic AI-generated icons replaced with original domain SVGs — even if he never says 'icon' and just says the UI looks AI-generated or template-y. Also triggers on: no-restricted-imports icon rule, icon guardrails, icon policy, feature card emoji, sparkles/bolts/brains/shields cleanup, icon CI check."
metadata:
  version: "1.0.0"
  source-session: "2026-07-09 icon de-slop of Kyle's skill/plugin library"
---

# Purging Icon Slop

Replaces generic AI icon slop (emoji icons, Heroicons/Lucide/react-icons on
product surfaces, sparkles/bolts/brains/shields/robots) with a typed,
hand-authored domain icon system, then adds lint/CI/audit guardrails so the
slop cannot return.

## TL;DR

Inventory every icon → classify utility vs domain → build/reuse the typed
icon pack → str_replace the slop → wire guardrails where a `package.json`
actually exists → verify with audit script + `tsc --strict` + a rendered
24/32/48px sheet. Never trust your own SVG paths until you've screenshotted them.

---

## Decision Tree

```
What is the target?
  ├─ Nothing cloned / no folder connected → STOP. Ask which repo/folder.
  │    "Here, skills and plugins" = the ~/.claude skill/template library.
  ├─ App repo (has package.json) → full treatment: icon pack in
  │    src/components/icons/ + ESLint rule + package scripts + CI workflow
  └─ Skill/template library (no package.json) → icon pack as skill asset,
       audit script + SKILL.md policy gates; ESLint/CI land only in the
       app SCAFFOLD scripts (e.g. web-artifacts-builder/init-artifact.sh)

Per icon found:
  ├─ close/search/menu/chevron/settings/upload/download/trash/
  │  external-link/back/forward/copy/edit/spinner, sort arrows,
  │  ✓/✕ status glyphs, semantic status dots → UTILITY: keep
  ├─ Emoji in an icon slot, or library icon on brand/hero/feature/
  │  dashboard/empty-state/onboarding/marketing/AI-agent surface
  │    → REPLACE with a domain SVG from the registry
  └─ In a vendor-synced plugin or Anthropic core skill (pptx, synced/*)
       → DO NOT EDIT (resync reverts). Flag as remaining exception.

Where does the canonical pack live? (Kyle's ecosystem)
  └─ executing-branded-frontends/templates/components/icons/
     {custom-icons,utility-icons,icon-registry}.tsx + icon-policy.md
     Audit: executing-branded-frontends/scripts/icon-audit.sh <dir>
     Reuse and extend it — do not create a second pack.

Single-file artifact (no npm)?
  └─ Inline the needed domain icons with a comment pointing at the
     canonical pack. NEVER hand it a lucide import it can't resolve.
```

---

## Usage Examples

**User: "Remove the icon slop from this app and lock it down"**
→ Icon inventory table → classify → copy/extend canonical pack into
`src/components/icons/` → replace non-utility usage → merge ESLint rule,
add `icons:audit`/`lint`/`typecheck` scripts + CI → run verification suite.

**User: "These feature cards use emoji icons, make them ours"**
→ Author one domain SVG per feature meaning (not per feature name), inline
if single-file, register in the union, render-sheet check at 24/32/48.

**User: "Make sure lucide never shows up in product surfaces again"**
→ Guardrails only: ESLint `no-restricted-imports` (utility file exempted),
grep audit script, SKILL.md/anti-slop-audit gate items, CI workflow.

---

## The Typed Icon System (reusable pattern)

Three files. Closed union → unknown icon names fail at compile time.

```tsx
// custom-icons.tsx — domain icons only, zero imports from icon libraries
import type { ReactNode, SVGProps } from "react";
export type IconProps = SVGProps<SVGSVGElement> & { title?: string };

function IconBase({ title, children, ...props }: IconProps & { children: ReactNode }) {
  return (
    <svg viewBox="0 0 48 48" width="1em" height="1em" fill="none"
      stroke="currentColor" strokeWidth={3} strokeLinecap="round"
      strokeLinejoin="round" role={title ? "img" : undefined}
      aria-hidden={title ? undefined : true} {...props}>
      {title ? <title>{title}</title> : null}
      {children}
    </svg>
  );
}
// export function DomainThingIcon(props: IconProps) { return <IconBase {...props}>…paths…</IconBase> }
```

```tsx
// icon-registry.tsx
export type IconName = "deploy-path" | "approval-gate" | /* … */ "close";
const registry = { /* every name → component */ } satisfies Record<IconName, ComponentType<IconProps>>;
export function AppIcon({ name, ...props }: IconProps & { name: IconName }) {
  const Icon = registry[name];
  return <Icon {...props} />;
}
```

Icon quality bar: original geometry tied to the actual domain meaning
(e.g. HITL = gate posts + pause ticks + queued/released items; deployment =
build layers rising to a live node), 2–4 meaningful details, no decorative
noise, consistent stroke frame, legible at 24px. Emoji and library icons
communicate nothing; the replacement must say what the feature *does*.

`utility-icons.tsx` is the ONLY file allowed to import lucide/heroicons in
npm apps — and only for: close, search, menu, chevron, settings, upload,
download, trash, external link, back/forward, copy, edit. In artifacts,
hand-author these too (zero-dep versions exist in the canonical pack).

---

## Guardrails

**ESLint (flat config) — merge WITHOUT overwriting the template config:**

```bash
mv eslint.config.js eslint.config.base.js
# new eslint.config.js:
#   import base from './eslint.config.base.js'
#   export default [...[].concat(base), { files: [...], ignores:
#     ['src/components/icons/utility-icons.tsx'], rules: { 'no-restricted-imports':
#     ['error', { paths: [heroicons outline/solid, lucide-react, react-icons,
#     bootstrap-icons], patterns: ['react-icons/*','@fortawesome/*','@heroicons/*'] }] } }]
```

`[].concat(base)` survives Vite template drift (tseslint.config() returns an array).

**Grep audit (backstop for HTML + non-linted files):** quote-anchored import
regex `(from[[:space:]]*|require\()['\"](@heroicons/|lucide-react|react-icons|@fortawesome/|bootstrap-icons)`,
emoji-in-icon-slot regex, unsafe-SVG regex (`dangerouslySetInnerHTML.*svg`,
base64 svg). Exempt `components/icons/utility-icons.tsx`. Exit 1 on hits.
Canonical copy: `executing-branded-frontends/scripts/icon-audit.sh`.

**Scripts + CI:** `icons:audit`, `lint`, `typecheck` in package.json;
`.github/workflows/icon-audit.yml` runs all three. In skill-library mode,
gates go into SKILL.md sections and the anti-slop-audit checklist instead.

---

## Verification Suite (all five, every time)

1. `icon-audit.sh <every touched tree>` → passes
2. `tsc --strict --noEmit` on the icon pack → passes
3. Negative test: compile `<AppIcon name="sparkles" />` → MUST fail (TS2322)
4. `npx esbuild file.jsx --loader:.jsx=jsx --outfile=/dev/null` on edited JSX
5. Render sheet: `renderToStaticMarkup` every registry icon at 24/32/48px →
   HTML → playwright screenshot (`/opt/pw-browsers/chromium`) → LOOK at it.
   Also screenshot one real consuming component in context.

---

## Gotchas (all hit in the source session)

1. **grep bracket expressions with emoji match BYTE-wise** without a UTF-8
   locale — `[⚡✨…]` flagged ✓ because ✓ (E2 9C 93) shares bytes with
   ✨ (E2 9C A8). Fix: `export LC_ALL=C.UTF-8` at the top of the audit script.
2. **Import-ban regexes match comments.** A policy comment saying "No imports
   from lucide-react" failed the audit. Anchor on the quote:
   `(from\s*|require\()['"]lib`, not `import[^\n]*lib`.
3. **You cannot judge SVG paths from coordinates.** A malformed zero-radius
   arc (`a 0 0 0 0 0 0 0`) read as plausible in code. Render + screenshot
   before shipping; that's how it was caught.
4. **Single-file artifacts can't import npm icon packages.** Kyle's HTML/JSX
   artifacts are self-contained — a lucide import is a runtime failure, not a
   style violation. Inline domain icons with a pointer comment to the pack.
5. **Don't overwrite the Vite ESLint config** to inject rules — rename to
   `eslint.config.base.js` and wrap. Overwriting breaks on template drift and
   violates the merge-don't-overwrite rule.
6. **Vendor-synced plugins and Anthropic core skills revert on resync.**
   Edits to `plugins/synced/*` (auth0, wix, valtown…) or `pptx` are wasted.
   Flag, don't patch.
7. **Session-container skill edits may not sync back to other devices.**
   Always zip the changed files (relative to `~/.claude/`) and SendUserFile
   as a restore point.
8. **Prove the type guardrail with a failing compile**, not by reading the
   types. `name="sparkles"` → TS2322 is the acceptance evidence.
9. **str_replace only on existing files** (Kyle hard rule). New icon pack
   files are net-new (Write OK); every template/SKILL.md change is an Edit.
10. **The audit itself needs an exemption list** for its own pattern strings
    and the policy docs, or it flags itself (`grep -v icon-audit`).

---

## Self-Verification Checklist

- [ ] Inventory table produced (icon, file, surface, class, verdict, replacement, why)
- [ ] Zero emoji-as-icon and zero library icons on domain surfaces in touched trees
- [ ] Registry union compiles; invalid name fails compile (evidence captured)
- [ ] Audit script passes on every touched tree; false-positive fixes retained
- [ ] Rendered sheet reviewed at 24/32/48 + one in-context screenshot
- [ ] Guardrails placed where they can execute (package.json present) — not in .md-only trees
- [ ] Vendor/synced content untouched; exceptions listed in final report
- [ ] Changed files zipped and delivered
- [ ] Final report: Inventory / Plan / Files Changed / Verification / Exceptions / Next Steps + CLAIMS and GAPS footers

---

## CLAIMS

- [SOURCED] `satisfies Record<IconName, ComponentType<IconProps>>` + closed
  union rejects unknown names at compile time — reproduced with TS2322 in the
  source session (tsc 5.6, strict).
- [SOURCED] Byte-wise emoji matching in grep bracket expressions without
  UTF-8 locale — reproduced: ✓ flagged by an emoji class it isn't in.
- [SOURCED] Chromium at `/opt/pw-browsers/chromium` + playwright-core renders
  local HTML for icon sheets in the Cowork cloud container.
- [GENERATED] `[].concat(base)` wrapper survives future Vite eslint template
  changes — reasoned from tseslint.config() returning an array; not tested
  against a live scaffold run.

## COUNTEREXAMPLE

- An icon drawn as raw inline SVG slop (a generic shield path with no keyword)
  passes every grep gate — only the human render-sheet review catches it.
- A perfectly typed registry doesn't stop someone rendering `<svg>` ad-hoc in
  a component; the policy + audit checklist are the only guard there.

## CONTRADICTIONS

! "Ban generic libraries" vs. installing lucide-react in every scaffolded app —
  resolved by confinement (utility file + ESLint exemption), not removal;
  removing the install entirely would be cleaner but breaks shadcn components
  that import lucide internally.
! "Never rebuild a file to deliver a change" vs. scaffold scripts that heredoc
  whole configs — scaffold-time file creation is authoring, not editing; the
  rule applies once a file exists outside the scaffold run.
