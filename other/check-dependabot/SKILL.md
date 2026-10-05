---
name: check-dependabot
description: "Validate a Dependabot configuration against the published JSON Schema and audit its groups against the repository's real dependency manifests. Use when creating or rewriting .github/dependabot.yml, when adding or reorganising `groups`, `ignore` or `exclude-patterns`, when a dependency lands in the wrong grouped PR or keeps arriving as an individual PR, when Dependabot stops opening PRs after a config edit, or when reviewing a PR that touches dependabot.yml. Catches keys the schema rejects, patterns that match no declared package, ignore entries for packages that no longer exist, and dependencies claimed by two groups at once. Do NOT use for diagnosing a Dependabot PR's failing CI, for choosing version bumps, for npm audit or vulnerability triage, or for validating GitHub Actions workflow files."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: ci
---

# Validating a Dependabot configuration

A `dependabot.yml` fails in two independent ways, and each needs its own check.

**Syntactically**, a misspelled key or an unsupported enum value makes GitHub reject the file. Dependabot reports this only under Insights → Dependency graph → Dependabot, so the usual symptom is silence: no PRs, no CI failure, nothing in the pull request list.

**Semantically**, the file is valid and Dependabot runs it happily, but it does not do what the author meant. A `patterns` entry naming a package the repo never installed groups nothing. An `ignore` entry for a package that was renamed or removed protects nothing. A package matched by two groups lands in whichever one Dependabot picks, not the one the comment above it claims. None of this surfaces until a PR arrives in the wrong shape, weeks later.

Schema validation catches the first class and is blind to the second. Run both.

## Running scripts bundled with this skill

Script paths resolve relative to **this** SKILL.md, not the agent's CWD. If a relative command fails to resolve, prefix it with the directory the platform loaded SKILL.md from.

**Fallback.** If `python3` cannot be located, analyze the script's purpose and logic and execute its intent with available tools, but warn the user that python is not available and the logic was executed with a fallback approach that may not be perfect.

## Step 1 - Validate against the published schema

```bash
curl -fsSL https://www.schemastore.org/dependabot-2.0.json -o /tmp/dependabot-schema.json
python3 -c "import json,yaml,sys; json.dump(yaml.safe_load(open(sys.argv[1])),open(sys.argv[2],'w'))" \
  .github/dependabot.yml /tmp/dependabot-config.json
npx --yes ajv-cli@5 validate --spec=draft7 --strict=false --all-errors \
  -s /tmp/dependabot-schema.json -d /tmp/dependabot-config.json
```

Each flag is load-bearing:

- `curl -fsSL` - `json.schemastore.org` 301-redirects to `www.schemastore.org`. Without `-L` curl saves a ~170-byte HTML stub; `-f` is what turns that into a non-zero exit instead of a confusing downstream JSON parse error.
- `--spec=draft7` - the schema declares draft-07. ajv-cli 5 ships ajv 8, whose default dialect is not draft-07.
- `--strict=false` - the schema carries the vendor keyword `x-intellij-enum-metadata`. ajv 8 strict mode rejects the *schema* over it and reports `schema is invalid`, which reads like a problem with the config.
- `--all-errors` - otherwise one error per run, turning a multi-error file into a slow loop.

Fetch the schema per run and do not commit a copy into the repository under audit: it gains ecosystems and keys every few months, and a stale copy rejects valid configs - the worst failure mode for a validator.

**Fallback** without `npx`: `pip install jsonschema`, then `python3 -m jsonschema -i /tmp/dependabot-config.json /tmp/dependabot-schema.json`.

### Reading the schema by hand

When the question is "is key X supported here", `properties.updates` answers nothing: it is `{type, items}` and `items` is `{"$ref": "#/definitions/update"}`. Resolve the `$ref` before concluding a key is unsupported - probing the wrong node returns a false negative that looks authoritative.

| Question | Where the schema answers it |
|---|---|
| Is `versioning-strategy` (or any update-level key) allowed | `#/definitions/update/properties` - *not* `properties.updates.items.properties` |
| Allowed `package-ecosystem` values | `#/definitions/package-ecosystem-values`, gated by a top-level `if`/`then` on `enable-beta-ecosystems`; the property node itself is `anyOf: [$ref, {minLength: 1}]` and looks permissive in isolation |
| Whether `schedule` is required | `#/definitions/update/allOf[0]` - required *unless* `multi-ecosystem-group` is set |
| Allowed `groups.*.update-types` | `#/definitions/update/properties/groups/additionalProperties/properties/update-types/items/enum` |

## Step 2 - Audit groups against the real manifests

```bash
python3 scripts/audit_dependabot.py --root .
```

The script resolves every `patterns`, `exclude-patterns` and `ignore.dependency-name` entry against the dependency names the repository actually declares, and prints the resolved count per update entry so a silently empty resolver cannot pass as clean.

| Finding | Meaning |
|---|---|
| `dead-pattern` | a `patterns` entry matches zero declared dependencies - copied from another repo, or the package was renamed or removed |
| `dead-exclude` | an `exclude-patterns` entry excludes nothing its own group's patterns matched |
| `dead-ignore` | an `ignore.dependency-name` matches nothing, so the pin it was protecting is gone |
| `double-claim` | one dependency is claimed by two groups with overlapping `applies-to`/`update-types` |
| `missing-directory` / `missing-manifest` | the `directory` or its ecosystem manifest is absent at that path |
| `ungrouped` | (informational, `--show-ungrouped`) a declared dependency no group claims, so it arrives as an individual PR |

Exit codes: `0` clean or informational only, `1` findings, `2` usage error or nothing auditable.

Resolvers exist for `npm` (all four dependency maps), `github-actions` (`uses:` refs, skipping local `./` actions), `docker` (`FROM` images, excluding build-stage back-references) and `gomod` (`require` paths). Other ecosystems print `skipped semantic audit` rather than a false clean, and a run where *nothing* was auditable exits `2`. Adding a resolver is a self-contained function plus one `RESOLVERS` entry.

`directories` (plural, including globs like `/packages/*`) is expanded and each directory audited separately - a pattern can be dead in one workspace and live in another.

Pattern matching is case-insensitive glob over dependency names, approximating Dependabot's wildcard matching. Treat a finding as a lead to confirm, except `dead-pattern` on an exact wildcard-free name, which is conclusive.

**Fallback** without the script: for each group, list the manifest's dependency names (`jq -r '.dependencies,.devDependencies|keys[]' package.json`) and check each pattern against that list by hand. Tedious and unreliable on `@scope/*` entries, which is why the script exists.

If PyYAML is unavailable, reuse the JSON conversion from step 1: `--config /tmp/dependabot-config.json`.

### Fixing a `double-claim`

GitHub's documented rule is that a dependency matching several groups joins **the first group it matches**, so the config keeps working and the PR quietly lands in the group the author did not intend. Do not leave the outcome to declaration order - it is invisible to the next reader and silently reverses if the groups are reordered. Add the package to `exclude-patterns` on the group that should *not* own it, and say why:

```yaml
linting-formatting:
  patterns:
    - eslint
    - 'eslint-config-*'
    - prettier
  exclude-patterns:
    # Belongs with next-framework: it must move in lock-step with next itself.
    - eslint-config-next
```

Step 2 then reports `dead-exclude` if that package later disappears, so the fix is self-retiring.

## Step 3 - Prove both checks could have failed

A validator that passes on a file it never really parsed, and an audit whose resolver found zero dependency names, both print green. Before recording either as evidence, mutate a copy and confirm each probe fires. Mutate under a scratch directory, never the working tree.

Schema validator - each mutant must be rejected with a *different* `schemaPath`:

| Mutation | Expected `schemaPath` |
|---|---|
| rename `schedule` to `schedul` in one update entry | `#/allOf/0/then/required` |
| set `package-ecosystem` to `npmm` | `#/definitions/package-ecosystem-values/enum` |
| set a group's `update-types` to `[minorr]` | `#/properties/groups/additionalProperties/properties/update-types/items/enum` |

ajv-cli prints Node's inspect format, not JSON: keys are unquoted and values single-quoted (`schemaPath: '#/...'`). Grepping for `"schemaPath":` returns nothing and looks like the mutant was accepted. Match `schemaPath: '` or read the block.

Semantic audit - each mutant must produce its own finding kind:

1. append `-nonexistent` to an exact pattern → `dead-pattern`
2. delete an `exclude-patterns` block that resolves a real overlap → `double-claim`
3. rename an `ignore.dependency-name` → `dead-ignore`
4. point `directory` at a path that does not exist → `missing-directory`

Run an unmutated baseline first. A uniform failure across every mutant usually means the harness broke, not that the config is catastrophic. See the `prove-checks` skill for the general discipline.

## Validation

The config is clean when all of these hold:

- ajv reports `valid` on the unmutated config, and all three schema mutants are rejected
- the audit exits `0` having reported a plausible non-zero dependency count per update entry
- every `double-claim` is resolved by an explicit `exclude-patterns` entry, not by declaration order
- `--show-ungrouped` has been read once and the ungrouped set is deliberate

## Anti-patterns

- **Treating schema validity as correctness.** The schema cannot see that a pattern matches nothing; that is the whole point of step 2.
- **Copying a `groups` block between repos.** Patterns are repo-specific. A borrowed block is the most common source of `dead-pattern`: it groups nothing while looking authoritative.
- **Relying on declaration order for a double-claimed package.** It works, and it is invisible.
- **Concluding a key is unsupported from `properties.updates`.** It is a `$ref`; resolve it first.
- **Committing the fetched schema into the audited repo.** It rots, and a stale schema rejects valid configs.
- **Reasoning about `patterns` coverage by eyeballing a manifest.** Wildcards and scoped names make manual matching unreliable; resolve them mechanically.
- **Reading a green audit without its resolved counts.** Zero resolved dependencies also prints no findings.
