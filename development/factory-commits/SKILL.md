---
name: factory-commits
description: Commit message and branch convention — Conventional Commits format with a Linear issue reference required in subject or body. Includes the canonical commitlint.config.cjs, Husky hook snippet, and opencommit configuration. Read whenever setting up a new project or wiring AI-assisted commits.
---

# Factory commits

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the commitlint / Husky / opencommit shape we use), and **Failure mode** when there's one to name.

## Tie every commit to a Linear issue

**Principle.** Every commit references a Linear issue ID in the subject or body; the commit hook enforces it.

**Why.** Code changes without ticket linkage are unsearchable history — six months later, "why did we change this?" has no answer that doesn't require a full archaeology session. Linear linkage makes the graph dense: ticket → PR → commit → context → decision. Each link is cheap up front; the lookup savings compound. Enforcement via commit-msg hook is the difference between "we should" and "we do."

**Recipe.** A commit message MUST:

1. Start with a Conventional Commits header: `<type>(<scope>)?: <subject>` (scope optional).
2. Contain a Linear issue ID (`<TEAM>-<NUM>`, e.g. `NON-45`) somewhere — subject **or** body.
3. Use a Linear magic word + ID for the commit that should close the issue.

A commit message SHOULD keep the subject under 72 chars, imperative mood, no trailing period. Put the *why* in the body when the diff doesn't make it obvious.

**Failure mode.** Commits with no Linear linkage — months later, archaeology requires reading the diff itself because there's no ticket trail.

## Subject describes the change; magic word lives in the body

**Principle.** The subject describes what changed; the Linear magic word goes in the body.

**Why.** "feat(auth): closes NON-45" looks tidy but conflates two things — what the commit does and what ticket it closes. The subject is the scannable description; the body is where automation hooks. Keeping the magic word in the body means the subject reads as a changelog entry, not a ticket-management instruction.

**Recipe.**

```
✓ feat(auth): add SSO callback handler

  Closes NON-45.

✓ fix: prevent duplicate org invites (Fixes NON-87)

✓ refactor(forms): extract field registry — refs NON-103

✗ feat: add login flow
   (no Linear ID anywhere — commit-msg hook rejects)

✗ feat(auth): closes NON-45
   (subject is the magic word; subject should describe the change)
```

## Linear magic words — close vs link

**Recipe only** — the closing-word/linking-word distinction is provided by Linear; pick the right one per commit.

| Effect | Words |
|---|---|
| Closes issue on merge to default branch | `close`, `closes`, `closed`, `closing`, `fix`, `fixes`, `fixed`, `fixing`, `resolve`, `resolves`, `resolved`, `resolving`, `complete`, `completes`, `completed`, `completing`, `implements`, `implemented`, `implementing` |
| Links issue without closing | `ref`, `refs`, `references`, `part of`, `related to`, `contributes to`, `toward`, `towards` |

**Default to a closing word** on the last commit of a branch — that's usually the one that lands on main and you want the ticket to flip to Done automatically.

## Branch convention — issue ID parseable from branch name

**Principle.** The Linear issue ID is parseable out of the branch name; slash commands depend on this.

**Why.** `/submit` and `/close` need to know which Linear issue the current branch belongs to. Asking the user every time is friction; storing it in a config file drifts. The branch name is the only state that's already correct by definition (you just made the branch for that issue). Format: `<user>/<teamkey>-<num>-<short-topic>`. The case-insensitive `<teamkey>-<num>` pattern is what the slash commands grep for.

**Recipe.**

```
nishu/non-45-commit-conventions  →  NON-45
nishu/eng-218-rate-limiter-fix   →  ENG-218
```

Get the canonical branch name from Linear: `Cmd+Shift+.` on an issue copies it to clipboard.

## commitlint config — the canonical drop-in

**Recipe only** — drop the config into the project root, install the hook, done.

```js
/** @type {import('@commitlint/types').UserConfig} */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'subject-case': [2, 'never', ['pascal-case', 'upper-case']],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72],
    'body-leading-blank': [2, 'always'],
    'footer-leading-blank': [2, 'always'],

    // Adds `release` as a first-class type — used by /release for version-cut commits.
    'type-enum': [
      2,
      'always',
      ['build', 'chore', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'release', 'revert', 'style', 'test'],
    ],

    // Linear ID required in subject or body (custom rule below).
    'linear-id-present': [2, 'always'],
  },
  plugins: [
    {
      rules: {
        'linear-id-present': (parsed) => {
          // Release commits roll up many issues — IDs live in the tag annotation, not the subject.
          if (parsed.type === 'release') return [true];
          const id = /[A-Z][A-Z0-9]+-\d+/;
          const haystack = [parsed.subject, parsed.body, parsed.footer]
            .filter(Boolean)
            .join('\n');
          return [
            id.test(haystack),
            'commit must reference a Linear issue (e.g. NON-45) in subject or body',
          ];
        },
      },
    },
  ],
};
```

Install in the project:

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional @commitlint/types husky
pnpm exec husky init
echo 'pnpm exec commitlint --edit "$1"' > .husky/commit-msg
chmod +x .husky/commit-msg
```

(Swap `pnpm` for `npm`/`yarn`/`bun` per project.)

## opencommit — wire the AI commit writer to the commitlint config

**Principle.** AI-assisted commit writing reads the project's commitlint config; the model phrases commits to pass the rules, not invent its own conventions.

**Why.** A model that writes commits without reading the project's rules will use its training-set defaults, which drift across projects. Pointing opencommit at `@commitlint` makes the model's output the project's rule-conformant shape — fewer rejections, less manual rewriting. The cost is one config line; the benefit is every AI commit fits the project.

**Recipe.**

```bash
oco config set OCO_AI_PROVIDER=ollama
oco config set OCO_MODEL=qwen2.5-coder:3b
oco config set OCO_API_URL=http://localhost:11434
oco config set OCO_PROMPT_MODULE=@commitlint
oco config set OCO_OMIT_SCOPE=true   # model invents bad scopes; let humans add if needed
oco config set OCO_DESCRIPTION=true  # body needed to hold the magic-word + Linear ID
```

The model writes the conventional header; you append the `Fixes NON-XX` line if it didn't infer the ID from branch context.

## `release:` as a first-class type — not `chore(release):`

**Principle.** Release commits get their own Conventional Commits type; they aren't chores.

**Why.** A release is a first-class category in the changelog — it deserves a section, not to be buried in `chore`. Adding `release:` to the `type-enum` makes the release commit greppable, lets the `/release` command emit it consistently, and lets changelog tools group it on its own. The exemption from `linear-id-present` is deliberate — releases roll up many issues whose IDs live in the tag annotation, not the subject.

**Recipe.**

```
✓ release: v0.1.1 — Linear factory setting update
✓ release: v0.2.0 — drawer-CRUD scaffolding
```

Release commits are exempt from `linear-id-present` (see the rule body).

## When the rule doesn't apply

**Recipe only** — narrow exemptions.

- **The factory-kit itself** — meta-repo, not connected to Linear. Use Conventional Commits but skip the ID requirement. Drop the `linear-id-present` rule from the kit's own `commitlint.config.cjs`.
- **Drive-by typo fixes during another task** — fold into the parent commit; don't create a separate ID-less commit.
- **Initial commit / scaffold commits** — exempt; tag with `chore: initial scaffold`.
- **Release commits** — `release:` type is exempt by the custom rule (see above).

## Related

- `factory-submit` and `factory-close` — depend on the branch convention for issue-ID parsing
- `factory-release` — parses these Conventional Commits to auto-generate release notes; `--no-verify` commits will land under `**other:**` and need manual rewording
