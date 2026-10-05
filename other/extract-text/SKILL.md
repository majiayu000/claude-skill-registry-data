---
name: extract-text
description: >-
  Extracts hard-coded user-facing strings from TypeScript or JavaScript source
  and externalizes them into locale files as YAML, JSON, or MsgResource
  (`.msg.js` via `@worldware/msg` / `@worldware/msg-cli`). For MsgResource,
  scaffolds with msg-cli (init, create project, create resource) after prompting
  for project and title. Replaces literals with i18n lookups. Use when
  localizing a file, extracting strings for translation, externalizing
  hard-coded text, or when the user mentions i18n, l10n, YAML, JSON locales,
  MsgResource, msg-cli, or extract-text.
license: MIT
paths:
  - "**/*.{ts,tsx,js,jsx}"
  - "**/*.{yml,yaml,json}"
  - "**/*.msg.{js,ts}"
metadata:
  author: agent-skills-template
  version: "1.2"
  category: i18n
---

# Extract Text

Externalize hard-coded UI copy from TS/JS into locale entries and wire the source to look up those keys.

## Instructions

1. Identify the target file(s) and the project's locale layout (path, format, key style, i18n API).
2. **Choose the output format** (YAML, JSON, or MsgResource) using [Format selection](#format-selection).
3. If the project already has a convention for keys and lookups, **match it**. Otherwise use the defaults below.
4. Extract only **user-facing** strings. Leave code identifiers, URLs, CSS classes, log messages, test fixtures, and non-copy constants alone unless the user asks otherwise.
5. Propose keys, show a before/after for the source file, and the locale entries — then apply the edits.

## Format selection

Resolve the target format **before** writing files:

1. **User said a format** → use it (YAML, JSON, or MsgResource).
2. **Infer from the project** (strongest signal wins):
   - `@worldware/msg`, `msg-cli`, `i18n/resources`, or `*.msg.js` / `*.msg.ts` → **MsgResource**
   - Locale / translation `*.json` (and no MsgResource layout) → **JSON**
   - Locale `*.yml` / `*.yaml` → **YAML**
3. **Unclear or conflicting signals** → ask the user which they prefer: YAML, JSON, or MsgResource. Do not guess.

When the format is **MsgResource**, follow [MsgResource scaffolding](#msgresource-scaffolding) before adding strings. Do not hand-write new project or resource files — use `@worldware/msg-cli`.

## Defaults (when no project convention exists)

| Concern | Default |
| ------- | ------- |
| Format | Ask the user if none can be inferred |
| YAML path | `locales/en.yml` |
| JSON path | `locales/en.json` |
| MsgResource path | Created by `msg create resource` under `directories.i18n` (often `src/i18n/resources/<title>.msg.js`) |
| Key shape | Nested dotted keys for YAML/JSON: `feature.section.name`. Flat string keys for MsgResource `.add('feature.section.name', ...)` |
| Lookup | Prefer the project's i18n helper (`t`, `i18n.t`, `useTranslation`, `resource.get`, `MsgMessage`, etc.). If none, use `t('key')` and note that the caller must provide `t`. |
| Value | Exact original string (preserve punctuation and placeholders) |

## Workflow

Copy and track:

```
Extract progress:
- [ ] 1. Choose output format (infer or ask)
- [ ] 2. If MsgResource: scaffold via msg-cli (init → project → resource)
- [ ] 3. Locate hard-coded strings
- [ ] 4. Choose keys
- [ ] 5. Add locale entries (YAML / JSON / MsgResource)
- [ ] 6. Replace literals with lookups
- [ ] 7. Verify imports / types still work
```

## MsgResource scaffolding

Use **`@worldware/msg-cli`** (`npx msg …` or a local/global `msg`). Do not invent project/resource files by hand. Details and flags: [references/FORMATS.md](references/FORMATS.md).

Run these checks in order; **stop and ask** whenever required input is missing.

1. **Init** — If `package.json` lacks `directories.i18n` / `directories.l10n` (or the i18n/l10n layout is missing), tell the user `msg init` has not been run and ask permission to run it. Offer defaults (`src/i18n`, `res/l10n`) or custom `--i18nDir` / `--l10nDir`. On approval: `npx msg init` (add path flags if they chose custom dirs). Do not proceed until init succeeds.
2. **Project** — List existing files under the i18n `projects` directory.
   - **None** → Prompt to create one. Ask for: `projectName`, source locale, one or more target locales, and optionally `--format` (`MF1` | `MF2` | `NONE`, default `MF2`). On approval: `npx msg create project <projectName> <source> <targets...> [-f <format>]`.
   - **Some exist** → Still **ask which project** to use (list names). Do not assume.
3. **Resource** — **Ask for the resource title** (file stem, e.g. `Messages` → `Messages.msg.js`). Then create it: `npx msg create resource <projectName> <title>`.
   - If the file already exists, ask whether to **reuse it** (append `.add` only) or recreate with `--force` (destructive). Default to reuse when the user is extracting into that resource.
4. **Extract** — Replace sample `.add(...)` stubs from the CLI with real keys/values (or append after them), then wire source lookups.

Never run `msg init`, `create project`, or `create resource` with guessed names/locales — always confirm with the user first.

### 1. Locate hard-coded strings

Scan JSX/TSX text nodes, string props (`title`, `label`, `placeholder`, `aria-label`, `alt`, button/link children), and user-visible template literals.

**Skip:** import paths, `data-testid`, enum/const names used only in logic, GraphQL/SQL, and developer-only error strings.

### 2. Choose keys

- Scope by feature or screen: `settings.profile.save`, not `save`.
- Reuse an existing key when the copy and meaning match.
- Keep keys stable and descriptive; do not encode the full English sentence in the key.
- For interpolations, keep placeholders consistent with the project (`{{name}}`, `{name}`, `{$name}`, or `%{name}`).

### 3. Add locale entries

Merge without clobbering unrelated keys. Use the format-specific shapes in [references/FORMATS.md](references/FORMATS.md).

**YAML**

```yaml
settings:
  profile:
    save: Save changes
    greeting: Hello, {{name}}
```

**JSON** (nested key-value)

```json
{
  "settings": {
    "profile": {
      "save": "Save changes",
      "greeting": "Hello, {{name}}"
    }
  }
}
```

If the project stores **msg translation JSON** (`title` / `attributes` / `messages[]`), match that shape instead of nested key-value.

**MsgResource** — after scaffolding with msg-cli, append (or replace CLI samples with) chained `.add` calls:

```js
resource
  .add('settings.profile.save', 'Save changes')
  .add('settings.profile.greeting', 'Hello, {name}');
```

Match placeholder syntax to the project format (MF1 `{name}` vs MF2 `{$name}`). See [references/FORMATS.md](references/FORMATS.md).

### 4. Replace literals

```tsx
// before
<button>Save changes</button>
<p>Hello, {name}</p>

// after (typical t() helper)
<button>{t('settings.profile.save')}</button>
<p>{t('settings.profile.greeting', { name })}</p>
```

For MsgResource-based UIs, follow the project's pattern (e.g. `messages.get('key')?.format({ name })` or `<MsgMessage … />`) instead of inventing a new API.

Ensure the lookup helper is in scope — add the existing import/hook pattern.

### 5. Verify

- No remaining hard-coded copy in the touched UI paths (unless intentionally left).
- YAML/JSON is valid; MsgResource file still exports a valid resource.
- Placeholder names in the locale file match call-site params.

## Examples

**Input (component):**

```tsx
export function EmptyState() {
  return (
    <div>
      <h1>No projects yet</h1>
      <p>Create your first project to get started.</p>
      <button type="button">Create project</button>
    </div>
  );
}
```

**YAML / nested JSON keys:** `projects.empty.title`, `projects.empty.body`, `projects.empty.cta`

**MsgResource adds:**

```js
resource
  .add('projects.empty.title', 'No projects yet')
  .add('projects.empty.body', 'Create your first project to get started.')
  .add('projects.empty.cta', 'Create project');
```

**Output (component)** — adjust to the project's lookup API:

```tsx
export function EmptyState() {
  return (
    <div>
      <h1>{t('projects.empty.title')}</h1>
      <p>{t('projects.empty.body')}</p>
      <button type="button">{t('projects.empty.cta')}</button>
    </div>
  );
}
```

## Additional resources

- Output formats (YAML, JSON, MsgResource): [references/FORMATS.md](references/FORMATS.md)
- Key naming and edge cases: [references/KEY-GUIDE.md](references/KEY-GUIDE.md)
