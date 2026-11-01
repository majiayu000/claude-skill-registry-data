---
name: barbatos-docs-sync
description: "Keeps Barbatos.Wpf docs in step with the code after a public API change: each package's README.md (concept-first, the nuget.org landing page) versus API-REFERENCE.md (member-by-member, GitHub only), Documentation Menu anchors, the root README.md and API-REFERENCE.md, templates/README.md, [Obsolete] renames, house voice, and the sample. Use after adding, renaming or removing public API, when asked to document a feature, on \"what else before this ships\" or \"did I forget anything\", or when a menu link goes nowhere or a README logo or link is blank on nuget.org. For the code change itself use barbatos-package-authoring. Vietnamese prompts too - cập nhật tài liệu, viết docs cho tính năng mới, còn thiếu gì trước khi ship, mục lục README bị lệch, link anchor bị hỏng, quên cập nhật API reference."
---

# Documentation upkeep

Every package carries two hand-written documents - `src/<Package>/README.md` (concept-first)
and `src/<Package>/API-REFERENCE.md` (member-by-member) - on top of the XML docs in the code.
Per CLAUDE.md, a public API change is not done until both are updated - so run this as the
closing step of any `src/` change, even when only the code was asked for. This skill is the
procedure for that and for the root and template docs around them. It is not about writing the
code (`barbatos-package-authoring`) or the template files themselves (`barbatos-templates`).
The path-scoped rule `.claude/rules/docs.md` loads a short form of this automatically whenever
one of these documents is opened.

## Sources of truth

- The documents: [Core README](../../../src/Barbatos.Wpf.Core/README.md) /
  [API reference](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md),
  [Aquarius README](../../../src/Barbatos.Wpf.Aquarius/README.md) /
  [API reference](../../../src/Barbatos.Wpf.Aquarius/API-REFERENCE.md),
  [Router README](../../../src/Barbatos.Wpf.AquariusRouter/README.md) /
  [API reference](../../../src/Barbatos.Wpf.AquariusRouter/API-REFERENCE.md),
  [Valee README](../../../src/Barbatos.Wpf.AquariusValee/README.md) /
  [API reference](../../../src/Barbatos.Wpf.AquariusValee/API-REFERENCE.md), the root
  [README.md](../../../README.md) and [API-REFERENCE.md](../../../API-REFERENCE.md), and
  [templates/README.md](../../../templates/README.md).
- What gets packed: [Directory.Build.targets](../../../Directory.Build.targets) (the `None`
  item packing `README.md` to `\README.md`) and [Directory.Build.props](../../../Directory.Build.props)
  (`PackageReadmeFile`, `GenerateDocumentationFile`). Nothing packs `API-REFERENCE.md`.
- The code wins over every document. Read the member, its XML `<summary>`/`<remarks>`, and what
  it throws before writing about it - never copy a signature from the old doc.
- Tests that pin documented claims - change the claim and the test together:
  `tests/Barbatos.Wpf.Aquarius.UnitTests/KeepAliveTests.cs` (the KeepAlive comparison table:
  `TabControl` and `Frame`/`Page` really unmount, `Directives.Show` does not),
  `tests/Barbatos.Wpf.AquariusRouter.UnitTests/RouterNavigationGuardOrderTests.cs`
  ([The Full Pipeline Order](../../../src/Barbatos.Wpf.AquariusRouter/README.md#the-full-pipeline-order)),
  `tests/Barbatos.Wpf.Core.UnitTests/McpFeatureTests.cs` (the `EnvironmentVariables`
  nested-initializer syntax the Core README shows).
- [check-docs.mjs](check-docs.mjs) in this folder measures everything below that a script can.
  Run it before and after every docs edit, from the repo root:

```bash
node .claude/skills/barbatos-docs-sync/check-docs.mjs          # menus, links, anchors, namespaces
node .claude/skills/barbatos-docs-sync/check-docs.mjs --types  # + public types API-REFERENCE never names
```

## Where each document is read

| Layer | Packed into the `.nupkg`? | Read on | Consequence |
| --- | --- | --- | --- |
| XML doc comments in `src/` | Yes (`GenerateDocumentationFile`) | IntelliSense | Must agree with API-REFERENCE |
| `src/<Package>/README.md` | Yes, as the package readme | nuget.org **and** GitHub | Links must survive nuget.org |
| `src/<Package>/API-REFERENCE.md` | **No** - nothing packs it | GitHub only | Reached from the README by absolute URL |
| Root `README.md`, `API-REFERENCE.md`, `templates/README.md` | No | GitHub only | Relative links are fine |

What the published nuget.org pages actually do (seen in their HTML):

- Heading ids are the same GitHub slugs, so in-page `#anchor` links and the menu work there.
- A **relative** link (`[x](API-REFERENCE.md#rules)`) renders as `href=""` - dead. Every link that
  leaves a package README uses the absolute form
  `https://github.com/Barbatos-Labs/Barbatos.Wpf/blob/main/<path>#anchor`, as the "Read the Full
  API Reference" link and every cross-package link already do.
- An image whose host is not on NuGet's allow-list renders as `src=""`. `github.com/...?raw=true`
  is **not** allowed; `img.shields.io` and `raw.githubusercontent.com` are
  (`https://raw.githubusercontent.com/Barbatos-Labs/Barbatos.Wpf/main/build/<x>-logo.svg` serves
  `image/svg+xml`).
- `> [!IMPORTANT]` renders as an alert on both sites.
- nuget.org keeps the readme of the version that was pushed; a README fix reaches it only with
  the next release.

## The split - do not duplicate

| File | Answers | Register |
| --- | --- | --- |
| `README.md` | "What is this, how do I use it, why is it shaped this way?" | Prose, worked examples, comparison tables, the rationale for every non-obvious decision |
| `API-REFERENCE.md` | "What exactly does this member take, return, default to, throw?" | Terse signature blocks and member lists/tables, modeled on the .NET API docs |

The API reference links back for the *why* - Router:
`See [Navigation Guards](README.md#navigation-guards) for firing semantics and pipeline order.`;
Core: `see [Optional desktop features](README.md#optional-desktop-features) in the README`. The
README links forward once, from its `## API Reference` section.

Record exact behavior in API-REFERENCE: the exception type and when (`Computed<T>.Value`'s setter
throws `InvalidOperationException` on the read-only form; `PathTokenizer.Tokenize` throws
`ArgumentException` / `FormatException`), what `null` means, cached versus recomputed
(`FieldMeta.Dirty` is a live comparison, never cached), defaults, and `internal` setters
("All setters are `internal`" on `FieldMeta`).

## Package README skeleton

All four follow this; match it when adding a package or a top-level section.

```
# Barbatos.Wpf.<Package>
![Barbatos.Wpf.<Package> logo](<image URL>)
### *One-line positioning statement*
**Bold one-paragraph summary naming the main types.**
four badges: NuGet version, NuGet downloads, GitHub stars, license
---
## 📖 Documentation Menu
## Getting Started
### Introduction        #### What is Barbatos.Wpf.<Package>? (Aquarius also says what it is
                        NOT), a > **Prerequisites** blockquote carrying a "Familiar with
                        <ported library>?" note (Core: a separate "Familiar from .NET MAUI?"
                        blockquote)
### Quick Start         dotnet add package, the xmlns line (aq / aqr / aqv; none for Core),
                        minimal wiring; Router and Valee end with "See `samples/<Sample>` ..."
                        listing what the sample demonstrates
## <feature sections>   ### subsections; #### for steps and asides (normally not in the menu)
## Deliberately Out of Scope    Router and Valee; Aquarius has "## Patterns that are already
                                native" instead; Core has neither
## Ecosystem
### Repository layout   src/, samples/, tests/ - one bullet each
## API Reference        one paragraph + the 👉 absolute link to API-REFERENCE.md (Core also
                        lists its namespaces before it and adds a closing line)
## Community            Core: ### Maintainers / ### Support / ### License; the other three:
                        one sentence linking https://github.com/Barbatos-Labs/Barbatos.Wpf#community
```

Every `##` is preceded by a `---` rule. The Core README has no xmlns (Core has no
`XmlnsDefinition`); a new Core desktop feature also gets a row in the
[Optional desktop features](../../../src/Barbatos.Wpf.Core/README.md#optional-desktop-features)
table (`Feature | Builder method | Options section | Runtime service | Enabled by default?`) and,
if it is large, its own `##` section the way Dialogs, SplashScreen and Periodic services have.

## Documentation Menu and anchors

- The menu sits under `## 📖 Documentation Menu`: `* **[Title](#anchor)**` for a `##`,
  two-space-indented `* [Title](#anchor)` for a `###`, four spaces for the rare `####` (Core's
  "Removing an interceptor at runtime"). Order and nesting follow the body.
- **Every `##` and `###` gets an entry.** A section without one is effectively unfindable. Link
  text may be shortened (`[Modal routes](#modal-routes---a-route-that-renders-into-a-window)`);
  the anchor may not.
- Anchors are GitHub slugs of the rendered heading text: lowercase; every character that is not
  a letter, digit, space, `-` or `_` dropped (backticks, `.`, `:`, `/`, `<>`, `()`, `'`, emoji);
  each space becomes `-`; a repeated heading gets `-1`, `-2`, ... in document order.

| Heading | Anchor |
| --- | --- |
| `` ### `Valee.Mask` - guiding what gets typed `` | `#valeemask---guiding-what-gets-typed` |
| `### If (v-if / v-else / v-else-if)` | `#if-v-if--v-else--v-else-if` |
| `## 📖 Documentation Menu` | `#-documentation-menu` (leading hyphen) |
| `` ### `Field<T>` (sealed class) : `ObservableObject`, `IField`, `IDisposable` `` | `#fieldt-sealed-class--observableobject-ifield-idisposable` |
| `` ## `Barbatos.Wpf.Aquarius.Reactivity` Namespace `` | `#barbatoswpfaquariusreactivity-namespace` |
| Core API-REFERENCE's repeated `#### Properties` | `#properties`, `#properties-1`, ... |

Consequences: never link to a repeated `#### Properties` / `#### Methods` heading - link the
type's own heading. A Router/Valee type heading carries its base list, so changing a base type
changes the anchor; grep every doc for the old anchor. Renaming any heading means grepping for
its old slug across all ten documents.

## API-REFERENCE structure - two dialects

Match the dialect of the file you are in; do not convert one into the other.

| | Core, Aquarius | Router, Valee |
| --- | --- | --- |
| Opening | one paragraph, "modeled after the official .NET API documentation" | one paragraph + `See the [README](README.md) for a concept-first walkthrough` |
| Namespace table | `Namespace \| Description`, bold links | `Namespace \| Contents` |
| Namespace heading | `` ## `Barbatos.Wpf.Hosting` Namespace `` | `` ## Namespace: `Barbatos.Wpf.AquariusRouter.Matching` `` |
| Type heading | `` ### `WpfApp` Class `` / `` ### `Watch` Static Class `` | `` ### `PathToken` (sealed record) ``, `` ### `Form` (sealed class) : `ObservableObject`, ... `` |
| Members | `csharp` signature block, then bullets `` - **`Services`** (`IServiceProvider`) ... ``; Core groups them under `#### Properties` / `#### Methods`, and opens its larger namespaces (Hosting, LifecycleEvents, Dispatching, ApplicationModel, ApplicationModel.Communication, Apsu) with `### Classes` / `### Interfaces` / `### Classes / Interfaces` / `### Extension Methods` summaries | `Member \| Type \| Meaning` tables (`Member \| Default \| Meaning` for options records) |

Aquarius, Router and Valee API references also state, under the namespace table, that all their
namespaces map onto one XAML namespace (Router and Valee name `[assembly: XmlnsDefinition]` in
`AssemblyInfo.cs`); the Aquarius and Router README Quick Starts list those namespaces after the
xmlns line. A new namespace touches those sentences, the namespace table, the root
`API-REFERENCE.md`, and (code side, `barbatos-package-authoring`) `AssemblyInfo.cs`.

## Root and template documents

- **Root `README.md`** - the GitHub landing page. One row per package in the `## Packages`
  table (logo, badges, the one-paragraph summary, absolute `README · API Reference` links), the
  TFM and dependency paragraph, the `dotnet add package` block, `## Templates` (install commands,
  example invocations with `--Include*` flags, IDE notes), `## Repository layout`, and
  `## Community`, whose `#community` anchor the Aquarius/Router/Valee READMEs link to - do not
  rename it. Update it when a package summary, the package list or the templates change.
- **Root `API-REFERENCE.md`** - one bullet per package listing its public namespaces, linking the
  package's API reference by absolute URL. Update it whenever a namespace or package is added or
  removed (`check-docs.mjs` reports `ROOT` lines).
- **`templates/README.md`** - the layout tree (an empty leaf shows `.gitkeeper (none yet)`), the
  Install and Uninstall command blocks, one `##` section per template named
  `` `short-name` - Title (kind) ``, and for `barbatos-wpf-app`: the default package version quoted
  in prose, the count of Core flags in
  [Picking which modules to include](../../../templates/README.md#picking-which-modules-to-include),
  and the per-flag descriptions. The template commands are repeated in the root README's
  Templates section and in the Aquarius README's Quick Start - change all three together.
  Template mechanics (symbols, conditionals, testing) are `barbatos-templates`.

## House voice

The prose records decisions and evidence, not mechanics.

- **Say what a design was chosen over, and why.** Valee README: "Built on Aquarius's `Watch.On`
  specifically (not `Watch.Effect`) - `Watch.On` only reacts to the source's *value* changing,
  never to `Errors`/`Meta` changes a validation pass itself causes, which is what keeps two
  mutually-dependent fields from infinite-looping."
- **Say what was verified, and how.** "(confirmed empirically)" in the Valee API reference on
  `RequiredAttribute` short-circuiting; "confirmed by testing" in `templates/README.md`; "confirmed
  via `IsLoaded`" in the KeepAlive table, backed by `KeepAliveTests`. Write it only after running
  it, and prefer a test that keeps it true.
- **Name the limits.** Core README on push transports: "Worth being explicit about the limits of
  this: **Firebase Cloud Messaging and Windows Notification Service don't map onto a
  client-managed persistent connection the way SignalR does** ..."
- **Map the port.** Each Introduction has a "Familiar with ...?" blockquote (Vue's Composition
  API, Vue Router, vee-validate; "Familiar from .NET MAUI?" in Core, plus "Familiar from Vue's
  Pinia?" opening Core's Apsu section); where the port diverges from the original, say so and
  why, in place.
- **Keep "already native" notes** instead of growing API:
  [Already native: v-bind, v-for, v-html](../../../src/Barbatos.Wpf.Aquarius/README.md#already-native-v-bind-v-for-v-html),
  "Already native: error display" (Valee), "Patterns that are already native" (Aquarius). A
  rejected idea goes to
  [Deliberately Out of Scope](../../../src/Barbatos.Wpf.AquariusRouter/README.md#deliberately-out-of-scope)
  as `**Thing** - reason`, plus what to do instead.
- **Callouts only where it bites.** Only `> [!IMPORTANT]` is used, only in the Core docs: the
  SDK-suffixed TFM, the DeviceIdentity not-legal-advice note, synchronous splash-screen work, the
  pre-DI static facades, and Apsu's sync-action deadlock note (README and API reference). Other
  asides are bold-led blockquotes (`> **Prerequisites**`, `> **Familiar with Vue Router?**`). No
  `[!NOTE]`.
- **Dashes follow the file:** the Core README and API reference mostly use `—`; Aquarius,
  Router, Valee, the root README and `templates/README.md` use only ` - `.
- Prose wraps at about 95 characters; table rows and long link lines stay on one line.
- No marketing adjectives, no "simply"/"just", no narrating what the code obviously does.

## Checklist for one API change

1. **Read the code** - signature, defaults, exceptions, XML docs. Fix the XML docs too if they
   disagree with the behavior.
2. **`API-REFERENCE.md`** - the member row/bullet or type section in the file's dialect; in
   Core a new type also gets a row in its namespace's `### Classes` / `### Interfaces` table,
   where that namespace has one.
3. **`README.md`** - the feature section: a worked example adapted from the sample (say which
   file), the rationale, the Vue mapping or divergence, any out-of-scope or already-native note.
4. **Menu** - an entry for every new `##`/`###`, in body order.
5. **Cross-links** - README to API reference by absolute URL, API reference back by
   `README.md#...`; sibling packages by absolute URL (a Router feature relying on Aquarius
   `Setup` links the Aquarius README).
6. **Root `README.md`** if the package summary, package list or templates changed;
   **root `API-REFERENCE.md`** if a namespace or package was added or removed.
7. **The sample** - extend the package's own sample (a tab, route or field; one sample per
   package) with a comment saying what it demonstrates and why, and update the README's
   "See `samples/...`" sentence that lists what the sample shows. Valee sample text goes into
   both `Locales/en-US.json` and `Locales/vi-VN.json`; a Core feature that binds `Barbatos:Xxx`
   can show the file override in the Core sample's `appsettings.json`.
8. **Templates** - if a template uses the changed API or should offer the feature (a new
   `--IncludeXxx` flag), load `barbatos-templates` and update `templates/README.md` plus the
   copies listed above.
9. **Rename or removal** - while the `[Obsolete]` member exists it stays documented with its
   replacement, as `AppGuid` -> `AppId` is in
   [AppInfo / PublisherInfo](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md#appinfo--publisherinfo)
   and in the Core README's `` > **`AppGuid` is deprecated:** `` blockquote. Then find every
   other mention of the old name:

   ```bash
   grep -rn "OldName" --include=*.md --include=*.cs --include=*.xaml --include=*.json \
     src samples templates tests .claude README.md API-REFERENCE.md
   ```
10. **Pinned claims** - if the change alters behavior a test pins (see Sources of truth), update
    the test and the claim together.
11. **Run `check-docs.mjs`** and fix every line your change introduced.
12. **Agent skills** - for any API or behaviour change, not only a rename, grep `.claude/skills`
    for the member and fix every claim the change invalidated.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| A menu or "see below" link goes nowhere | Anchor guessed or heading renamed (the Aquarius README once linked `(#if-v-if)` for `### If (v-if / v-else / v-else-if)`) | Slug the real heading; run `check-docs.mjs` |
| The namespace table's links do nothing | Anchor missing a segment (`#barbatoswpfreactivity-namespace` for `Barbatos.Wpf.Aquarius.Reactivity`) | `#barbatoswpfaquariusreactivity-namespace` |
| Link works on GitHub, dead on nuget.org | Relative link in a package README | Absolute `https://github.com/Barbatos-Labs/Barbatos.Wpf/blob/main/...` URL |
| Logo blank on nuget.org, fine on GitHub | Image host not on NuGet's allow-list (`github.com/...?raw=true`) | `raw.githubusercontent.com/...` |
| New section exists but nobody finds it | No menu entry | Add it, nested under its real parent |
| A link to `#properties` lands on the wrong type | Repeated headings are suffixed `-1`, `-2` | Link the type heading |
| An anchor broke after a type change | Router/Valee type headings include the base list | Re-slug; grep the old anchor |
| Root and template docs contradict each other | One copy updated, the other not | `templates/README.md` is the detailed source; fix the root README to match |
| README fix not visible on nuget.org | nuget.org shows the readme of the pushed version | Ships with the next release |

## Known drift (measured with check-docs.mjs)

None open: `check-docs.mjs` and `check-docs.mjs --types` both report "No problems". When a run
reports something you cannot fix in the same change, list it here, one bullet per file, and
drop the bullet once it is fixed.

## Related skills

- `barbatos-package-authoring` - the API change itself, `[Obsolete]` mechanics, `AssemblyInfo.cs`,
  versioning and release.
- `barbatos-templates` - the `dotnet new` templates behind `templates/README.md`.
- `barbatos-wpf-testing` - writing the test that backs a "confirmed by running it" claim.
- The feature skills (`barbatos-wpf-host`, `barbatos-wpf-essentials`, `barbatos-aquarius-view`,
  `barbatos-aquarius-router`, `barbatos-valee-form`, `barbatos-apsu-store`, `barbatos-mcp-ai`) -
  domain knowledge for what the section should say.
