---
name: padosoft-i18n-hygiene
description: >-
  Use this skill when working on a translation catalogue — adding a string, auditing for unused or missing
  keys, replacing hardcoded text, aligning locales, checking plural forms. Also when the user says a label
  shows as a raw key in the interface, that a language is missing strings, that the translation files have
  grown full of things nobody uses, that a text was never translated, or asks to clean up the
  localisation. It gives the search that actually finds a key's usages, the rule for deleting one safely,
  what counts as user-visible text, and the invariants a catalogue has to keep across every locale. Do not
  use it to choose a localisation library, to translate the copy itself, or for date and number formatting
  performance.
license: MIT
compatibility: >-
  Any application with a key-based translation catalogue. Examples assume nested keys in dot notation and a
  library with a plural suffix convention.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A key is only unused once you have searched for every form it can be written in.
  profiles: laravel, node, react-native
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: i18n, translations, locales, missing keys, hardcoded text, plurals, catalogue, localisation
---

# i18n catalogue hygiene

A translation catalogue decays in two directions at once: it fills with keys nothing uses, and it misses the
ones something does. Both are invisible in review — one adds noise nobody reads, the other shows a raw key
to a user in a language nobody on the team speaks.

**The rule: a key is only unused once you have searched for every form it can be written in. And a key
exists in every locale, or in none.**

---

## 1. Start from a generated inventory, not from the files

Extract the full list of defined keys with a script, in a flat dotted form. Reading the catalogue files by
eye misses nested branches and gives you no way to diff the locales against each other.

That inventory is the input to everything below, and it is also the thing to regenerate at the end to prove
the state you claim.

## 2. Finding a key's usages is harder than it looks

**Searching for the key as a string is the search that misses.** Depending on the library and its
configuration, the same key appears in the code as:

| Form | Looks like |
|---|---|
| A plain string | `t("account.header.welcome")` |
| A typed selector | `t(($) => $.account.header.welcome)` — **no string anywhere** |
| A dynamic leaf | `t(($) => $.account.header[variable])` — only the **parent** appears |
| A runtime key | `t(buildKey(...))`, `tDynamic("account.header." + name)` |
| A template literal | `` t(`tabs.${routeName}`) `` — only the prefix appears |
| Deferred, in a config object | a thunk stored somewhere and called later |

So a key counts as used when it appears in **any** of these forms. Search for the full path, for the parent
followed by an index access, and for the prefix inside a template literal:

```bash
rg -n '\$\.account\.header\.welcome\b' src/          # selector
rg -n '\$\.account\.header\[' src/                   # dynamic leaf on the parent
rg -n 'account\.header\.welcome' src/                # string, runtime key, config
rg -n 'account\.header\.' src/ | rg '`|\+'           # composed at runtime
```

**Never delete a key whose parent namespace is used with a variable.** That is the one deletion that reaches
production as a raw key on screen, in a branch nobody clicks in development.

## 3. What is user-visible text

When replacing hardcoded strings, look at the places that are not obviously copy:

- text passed as children to a text or button component;
- `title`, `label`, `placeholder`, and the **accessibility label** — that last one is text a user hears, and
  it is the one most often left hardcoded;
- the title and body of a notification, an alert, a confirmation dialog;
- anything handed to a share or export action;
- error and empty-state messages, including the generic fallback.

**Not** user-visible: component display names, style class names, test identifiers, numbers, punctuation,
single symbols, and anything under a development-only area.

## 4. The invariants of the catalogue

- **A key exists in every locale, or in none.** A missing key falls back to the key itself or to the base
  language, and both are a defect in front of a user. Adding a string means adding it everywhere, in the
  same change — untranslated placeholders in the other locales are better than absence, because they are
  visible and greppable.
- **Plural forms follow the library's convention exactly**, with every form the language requires present.
  A partially declared plural resolves to the singular for the counts nobody tested.
- **Interpolation placeholders match across locales.** A translation that dropped a placeholder renders a
  sentence with a hole, and one that invented a placeholder renders the literal.
- **The catalogue files are encoded consistently**, with real accented characters rather than escapes —
  mixed forms make diffs unreadable and comparisons unreliable.
- **Ordering is stable**, so a diff shows what changed rather than everything.

## 5. Work by namespace, and prove the result

Process one namespace at a time. The audit is a whole-catalogue problem, but the decisions are local, and a
single pass over everything produces a change nobody can review.

At the end, regenerate the inventory and state the numbers: keys before and after, orphans removed,
hardcoded strings replaced, keys added per locale. Those numbers are the evidence that the audit happened —
see **`padosoft-evidence-boundaries`**.

---

## Gotchas

- **The typed-selector API makes the keys disappear from the source.** A team that migrates to it and keeps
  its old "find unused keys" script starts deleting keys that are all in use.
- **A key used only in a rarely-reached branch looks unused.** Runtime composition, feature flags and
  error paths are where the false positives live.
- **Adding a key to the base language only is the most common way to ship a raw key**, because the base
  language is the one the developer is looking at.
- **A fallback to the base language hides the problem from the team and shows it to the customer**, who is
  the only person who did not want to read that language.
- **Backend-provided text is a second catalogue.** If some labels come from an API or a content system,
  the audit has to say which keys are runtime-provided rather than treat them as missing.

## Checklist

- [ ] Inventory generated from a script, not read by eye
- [ ] Every key searched in **all** its forms before being called unused
- [ ] No key deleted whose parent is accessed with a variable
- [ ] Hardcoded text replaced, accessibility labels included
- [ ] Every new key added to every locale in the same change
- [ ] Plural forms complete for every language that needs them
- [ ] Interpolation placeholders identical across locales
- [ ] Encoding and ordering consistent
- [ ] Inventory regenerated; before and after numbers stated

## Final report

```
Namespaces processed: <list>
Keys: <before> → <after>   ·   orphans removed: <n>
Hardcoded replaced: <n> (of which accessibility labels: <n>)
Keys added: <n> × <locales>
Plural/placeholder mismatches fixed: <n>
Runtime-provided keys excluded from the audit: <which>
```
