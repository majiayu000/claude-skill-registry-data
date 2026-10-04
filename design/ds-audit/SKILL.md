---
name: ds-audit
description: Expert audit of a project's design system across TWO dimensions — (1) clean codebase and (2) AI-native structure (can an LLM read it and build on-brand reliably). Scores explicit criteria with evidence, then returns turnkey fixes that point to the design-system-template files to copy. Use when the user says "audit my DS", "is my design system AI-native", "check/score my design system", "what's missing", "am I ready to build UI with Claude here", or when onboarding an existing or new project to the design system. Most projects already have code — the job is to diagnose and fill the gaps using the template as the model, not rebuild from scratch.
---

# DS Audit — clean codebase + AI-native, with turnkey fixes

Two questions, scored separately:

1. **Is the codebase clean?** — no hardcoded values, one canonical component per role, no dead code, predictable structure, types safe, a baseline of accessibility. (Can a human or agent work in it without tripping over mess?)
2. **Is it AI-native?** — brand in machine-readable tokens, rules where the agent reads them, real reused components, a living storybook, a versioned source of truth, a deterministic gate. (Can an LLM *read it and build on-brand reliably*?)

**Canonical reference & template:** `eFounders/design-system-template` (repo) · Storybook `https://design-system-template-storybook.vercel.app` · Registry `https://design-system-template-registry.vercel.app/r/{name}.json`. Every fix below points to a real file in that template to copy and adapt.

**A project that already has code is the default.** Most audits run on a project that *already has* code and maybe a partial DS. The goal is **never to rebuild what works** — diagnose, then drop in the missing pieces using the template's files as ready-made models, aligned to the project's existing brand and naming. Starting from scratch (nothing yet) is the rare case → duplicate the template or run `/ds-bootstrap`.

## How to run

1. **Target a git repo.** Inside a project → confirm `git rev-parse --is-inside-work-tree` and audit the working tree. Given a GitHub repo → shallow-clone (`gh repo clone <owner/repo> <tmp> -- --depth=1 --single-branch`), audit the clone, remove it. Always note the branch/commit.
2. **Locate the DS — don't assume, Glob/Grep.** Tokens (`globals.css`, `tokens.css`, `styles.css`, `tailwind.config`), `components.json` (shadcn), `components/ui/` or a bespoke folder, `CLAUDE.md`/`AGENTS.md`, `DESIGN.md`, a storybook/preview, CI, a `ds-check`-style script.
3. **Run the tooling that gives deterministic evidence** (don't eyeball what a tool can prove):
   - `npx tsc --noEmit` → type health
   - lint/format if present (`npm run lint`)
   - if a `ds-check` exists, run it; if not, that itself is a finding
   - grep for hardcoded colors (`#[0-9a-f]{3,8}`, `rgb(`, `hsl(`) and duplicate component names/files
4. **Score BOTH dimensions**, every item ✅ pass / 🟠 partial / ❌ missing, each with **evidence** (`file:line` or one-line observation). Open the files — a checklist with no references is not an audit.
5. **Classify** and **return the report** (format below) with a **turnkey plan**, highest-leverage first.

## Dimension 1 — Clean codebase (8)

- [ ] **No hardcoded colors/px** where a token exists (use the gate / grep).
- [ ] **One canonical component per role** — no `Button`/`PrimaryButton`/`AppButton` sprawl, no same component defined in two places.
- [ ] **No dead code / orphans** — unused files, unreferenced exports, commented-out blocks, leftover scaffolding (e.g. default framework assets).
- [ ] **Predictable structure & naming** — one obvious home per concern (tokens, components, docs); consistent file/casing conventions.
- [ ] **No unused dependencies** (and no duplicate libraries doing the same job — two icon sets, two date libs).
- [ ] **Type safety** — `tsc` clean, no `any` sprinkled, props typed.
- [ ] **Accessibility baseline** — keyboard reachable, visible focus, correct roles/ARIA, sufficient contrast on the tokens.
- [ ] **A working quality setup** — lint/format configured and passing; a CI that runs it.

## Dimension 2 — AI-native structure (16)

### A · Tokens — the material
- [ ] **Semantic tokens named by role** (`--primary`, `--muted-foreground`…), mapped from primitives — not raw values in components.
- [ ] **Intent documented** (use for / not for) so the agent picks the right token. *(R. Kavcic)*
- [ ] **Light + dark** both defined.
- [ ] **Brand isolated to a few knobs** (`--brand-*`, font, `--radius`, density) — change them and everything re-skins.
- [ ] **shadcn contract respected** (`--background`, `--card`, `--primary`, `--ring`…).

### B · Conventions — readable by the agent
- [ ] **A `CLAUDE.md`/`AGENTS.md` at the root** pointing to tokens, components, rules. *(Highest-leverage single item.)* This is the in-repo agent index — it covers the "where everything lives" job.
- [ ] **Component specs** the agent can read: for / not-for, variants, states, tokens. *(R. Kavcic & TJ Pitre)*
- [ ] **A portable `DESIGN.md`** — the visual identity in one droppable file, for tools without registry access.
- [ ] **UX patterns + hard rules explicit** — the 5 states (empty/loading/error/partial/ideal), one primary action, one icon library, never invent a value.

### C · Components, composition & storybook
- [ ] **Real, reused components** (shadcn-based), themed by the tokens.
- [ ] **A composition layer** — layout primitives (`Container`/`Section`/`Stack`/`PageHeader`) + a `COMPOSITION.md` (how to combine into screens, page archetypes), not just isolated components. Without it the agent colours components right but lays the page out inconsistently.
- [ ] **A living storybook** that renders the REAL components — not a hand-made mirror that drifts. *(Noé)*
- [ ] **A references doc (bonus)** — `docs/REFERENCES.md`, the north-star patterns to match (interaction + feel), rendered with the project's own tokens/components. Anchors novel screens; a nice-to-have, never dock a project for skipping it.

### D · Distribution
- [ ] **A versioned source of truth projects consume** (registry or package) — updating = re-pull, not re-paste. *(Noé)*
- [ ] **Brand-agnostic base** — each project sets its own brand.

### E · Verification
- [ ] **A deterministic gate on PRs** — hardcoded values / unknown tokens fail the build (`ds-check`-style).
- [ ] **A duplicate-component audit** in that gate (catches sprawl/copies automatically).
- [ ] **A prototyping skill from the codebase** (`/prototype`, from the `design-skills` repo) — proof the DS is actually used to build.

## Turnkey fixes — copy from the template

For every ❌/🟠, propose the fix AND the file to copy from `design-system-template` (adapt paths + brand to the audited project; never paste a brand over theirs).

| Gap | Turnkey fix | Copy / model from the template |
|---|---|---|
| No obvious tokens file | Create `app/tokens.css` (two-tier primitives→semantic, light+dark) + import in the CSS entry | `app/tokens.css`, wired by `app/globals.css` |
| Hardcoded colors/px | Add the gate, then replace flagged values with tokens | `scripts/ds-check.mjs` + `.github/workflows/ds-check.yml` |
| Duplicate components | Keep one canonical, delete copies — the gate's duplicate audit finds them | duplicate check inside `scripts/ds-check.mjs` |
| No `CLAUDE.md` | Drop it in, adjust the paths/rules to the project | `CLAUDE.md` |
| No `DESIGN.md` | Generate from the tokens (frontmatter + Brand/Color/Type/Spacing/Components) | `DESIGN.md` |
| No component specs | Write a specs doc (for/not-for, variants, tokens) | `docs/COMPONENTS.md` |
| No / fake storybook | Wire a storybook that imports the REAL components + token foundations | `.storybook/`, `*.stories.tsx`, `registry/new-york/docs/*.mdx` |
| No composition layer (only isolated components) | Add layout primitives + a composition doc (when to use each + page archetypes) | `components/ui/{container,section,stack,page-header}.tsx` + `docs/COMPOSITION.md` |
| No references doc *(bonus)* | Add `docs/REFERENCES.md`: north-star patterns to match, rendered with the project's own tokens/components | `docs/REFERENCES.md` |
| Not distributed | Stand up a shadcn registry (or package) | `registry.json` → `public/r/*.json`, `components.json` |
| Dead code / scaffolding | Remove orphans and default framework assets | — (the cleanup itself) |

Bundle these into the plan in leverage order. The single highest-leverage item is almost always a root `CLAUDE.md` + an obvious tokens file — they make everything else legible to the agent.

## Report format

```
# DS Audit — <project>  (branch <x> @ <sha>)

**Verdict:** <(a) no DS yet | (b) has a DS, not AI-native | (c) AI-native with gaps | (d) solid>
**Clean codebase:** <X/8>   ·   **AI-native:** <Y/16>   ·   one-line summary

## Dimension 1 — Clean codebase
- ✅/🟠/❌ <criterion> — <evidence: file:line / tool output>
…

## Dimension 2 — AI-native structure
A · Tokens
- ✅/🟠/❌ <criterion> — <evidence>
… (every group)

## Turnkey plan (highest-leverage first)
1. <gap> → <fix> — copy from `design-system-template/<file>`  ·  why it matters
2. …

## Mode
Existing project (fill gaps, keep what works) | From scratch (duplicate the template)
```

## Tailor to the verdict

- **(a) No DS yet** → from scratch: duplicate the template (Use this template) or run **`/ds-bootstrap`**; re-brand via the knobs.
- **(b) Has a DS, not AI-native** → an existing project, the common case. The gap is usually the **conventions + verification layer**: drop in `CLAUDE.md`, `DESIGN.md`, component specs, the `ds-check` gate; make the storybook render real components. **Don't rebuild the tokens/components that already work** — point the conventions at them.
- **(c) AI-native with gaps** → close the specific failed items; wire/upgrade the gate (incl. the duplicate audit); align token naming to the shadcn contract.
- **(d) Solid** → keep it consuming the versioned base; maintain only.

Be honest and specific. Cite evidence. Propose fixes that are copy-and-adapt from the template, not from scratch.
