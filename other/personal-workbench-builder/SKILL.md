---
name: personal-workbench-builder
description: Build personalized, user-named desktop-and-mobile PWA workbenches through a novice-friendly five-question setup, smart module assumptions, local preview, validation, and static publishing. Default to a no-login lightweight version with current-device storage and no CloudBase dependency; add account-based cloud sync only when explicitly requested. Use when a user wants to create, customize, rename, install, synchronize, or publish a personal dashboard, productivity workspace, tracker, journal, learning hub, content planner, project desk, or similar modular web app without technical or product-design knowledge.
---

# Personal Workbench Builder

Turn an ordinary-language request into a named, responsive, installable workbench. Keep the conversation non-technical. Do not build until the user confirms the requirement summary, and do not publish until the user explicitly approves the preview.

## Workflow

### 1. Run the five-question fast setup

Default to a two-pass conversation for beginners. Reuse facts already supplied and never ask the user to repeat them. Read [interview-guide.md](references/interview-guide.md) for exact beginner-facing wording.

Ask these five outcome-oriented questions together:

1. What should the workbench be called? Allow “recommend three names” or a temporary name.
2. Which visual style should it use? Offer four described styles, a reference-image option, and “recommend for me.”
3. Which modules should it contain? Ask only for plain-language module names or goals.
4. Where will it be used: phone, computer, or both, and should records stay only on each current device or remain synchronized across devices? Present no-login current-device saving as the recommended lightweight default. Explain that it persists after closing the page but does not follow the user to another device; synchronized records require an account.
5. Should the finished workbench have a public address that opens on phone and computer? Do not use unexplained terms such as deployment, hosting, PWA, database, CloudBase, or Supabase. If stable mainland access is required, record that as a separate constraint instead of promising that every free static host can provide it.

Infer purpose and audience from the answer when clear. Default audience to the requester alone. Do not ask users to design fields, actions, or statistics. Instead, read [module-patterns.md](references/module-patterns.md), generate sensible module assumptions, and show those assumptions in the second pass. Ask a focused follow-up only when a missing answer would materially change the product, security, cost, or legality.

Require the user to choose or confirm `appName` before building. Offer three tailored names when they are unsure. Collect optional `shortName`, `englishName`, and `subtitle`; generate three subtitle candidates when blank. Allow renaming after preview. Use [naming-and-themes.md](references/naming-and-themes.md) for naming, slug, icon, and theme rules.

Offer “advanced customization” only when the user requests detailed control. Never make the old field-by-field interview the default.

### 2. Show smart assumptions and confirm once

In the second pass, show one compact configuration card containing the name, subtitle, purpose, modules, inferred fields/actions/statistics, style, device use, the selected data mode, AI/external dependencies, phone installation, and whether a web address will be prepared. Label inferred details as recommended defaults and let the user reply “start building” or list changes.

If the user said “I don't know,” choose a safe recommended default rather than reopening a long interview. Resolve only true blockers. Explain that “opens on both devices” and “keeps the same records on both devices” are different outcomes.

Do not silently substitute a generic final name. Do not claim external data is live unless a lawful, working source is configured.

### 3. Create the specification

Write `workbench-spec.json` using [workbench-spec.md](references/workbench-spec.md). Validate it before generation:

```bash
python3 <skill-dir>/scripts/validate_spec.py workbench-spec.json
```

Generate a project:

```bash
python3 <skill-dir>/scripts/init_workbench.py \
  --spec workbench-spec.json \
  --output <project-directory>
```

The generator copies `assets/starter`, applies the selected theme, injects the specification, generates PWA metadata and a name-based icon, and writes publishing metadata. Never edit files inside the installed Skill while creating a user's project.

### 4. Customize only where needed

The starter handles generic task, habit, journal, learning, content, health, schedule, and custom modules. Extend the generated project when the confirmed requirements exceed those patterns.

- Default to `local`: no signup, records automatically persist on the current device through IndexedDB with a localStorage fallback.
- For shared phone/computer records, use CloudBase after reading [cloud-and-ai.md](references/cloud-and-ai.md). Keep local writes working offline and upload them idempotently after login.
- Do not ask a lightweight-version user to log in. Do not describe current-device persistence as cross-device synchronization or backup.
- Use Supabase only when the user explicitly chooses the overseas advanced path.
- Add AI only through a server function. Provide an honest demo fallback until credentials are configured.
- For `learning` modules, read [specialized-modules.md](references/specialized-modules.md) and default to the daily-scene learning layout: settings, scene dialogue, direct-play lesson videos, five words with pronunciation, scenario questions, and completion.
- For `content` modules involving trends, hotspots, inspiration, or topic research, read [specialized-modules.md](references/specialized-modules.md) and default to the ranked inspiration layout: tracks/keywords, source disclosure, daily ranked cards, engagement data, analysis, borrowing guidance, source links, and idea status.
- Treat voice recognition as progressive enhancement and retain an explicit text-input action. Read [mobile-pwa-and-voice.md](references/mobile-pwa-and-voice.md) before adding voice input.
- Preserve desktop sidebar, mobile drawer, keyboard-safe forms, safe-area padding, and PWA installation help.

### 5. Validate and preview

Install dependencies, build, and run checks:

```bash
npm install
npm run build
python3 <skill-dir>/scripts/check_project.py <project-directory>
```

Preview at 1440, 768, 390, and 375 CSS pixels. Test long names, empty states, many records, reload persistence, offline shell, forms, mobile drawer, and install instructions. For learning and hotspot modules, verify the specialized layout instead of accepting a generic add-record form. For phone installation, verify WeChat-to-system-browser guidance, iPhone Share/Add to Home Screen steps, Android install prompt, standalone display, and the distinction between installation and synchronization. Check that no API keys, deployment credentials, private screenshots, or local file paths appear in `dist`.

Ask the user to approve the workbench name, modules, interactions, and appearance. If they rename it, update the spec and regenerate metadata with:

```bash
python3 <skill-dir>/scripts/apply_spec.py --spec workbench-spec.json --project <project-directory>
```

Rebuild and preview after renaming.

### 6. Publish only after explicit approval

For a lightweight workbench, read [static-publishing.md](references/static-publishing.md). Default to plain static hosting with no CloudBase SDK, environment, authentication, or database. GitHub Pages is the first zero-backend option when the user accepts its mainland-network limitation. Never publish merely because the user asked for a preview.

Use the local preview as the approval stage. After approval, authenticate only the publishing account, create an isolated site or repository, and return the HTTPS address. End users open the lightweight site without login. Explain that GitHub Pages cannot guarantee mainland availability; a stable mainland custom domain generally requires compliant domestic hosting and domain filing.

If the user explicitly requests synchronized records, read [cloud-and-ai.md](references/cloud-and-ai.md) and [cloudbase-publishing.md](references/cloudbase-publishing.md). Only then configure CloudBase authentication and a private database, after environment and cost confirmation. CloudBase is an optional sync/backend path, not the lightweight hosting default.

Return the HTTPS address and concise iPhone/Android installation steps. Offer a custom domain only as a later production upgrade.

Before returning the address, read [mobile-pwa-and-voice.md](references/mobile-pwa-and-voice.md) and confirm the generated site contains a visible install entry, privacy-safe illustrated guidance, correct PWA metadata, and honest storage wording. Never embed a user's private setup screenshots into the guide.

If the user explicitly requests an overseas service, read [overseas-publishing.md](references/overseas-publishing.md) and treat Netlify plus Supabase as an advanced alternative, not the default.

## Safety boundaries

- Never put Tencent Cloud `SecretId`, `SecretKey`, temporary tokens, CloudBase server credentials, or AI keys in browser code, source control, generated archives, or chat. Browser code may contain only a CloudBase Publishable Key and environment ID.
- Do not scrape authenticated platforms or imply guaranteed “daily hottest” data without a permitted data source.
- Do not overwrite an existing output directory unless the user explicitly authorizes it.
- Do not delete local data during cloud migration; copy first and deduplicate.
- Keep publication as a separate, user-confirmed state change.

## Bundled resources

- `assets/starter/`: reusable Vite + React + PWA project.
- `assets/themes/`: four visual systems plus custom-theme fallback.
- `scripts/`: deterministic specification, generation, validation, and packaging utilities.
- `references/`: load only the guide relevant to the current stage.

When the user asks to install or share the Skill across WorkBuddy, Codex, or Claude Code, read [installation.md](references/installation.md).
