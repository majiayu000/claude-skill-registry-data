---
name: intent
description: "Manages intent — features, enhancements, bugs and the reasoning behind them — recorded as prose in the knowledge base with a lifecycle. Use when capturing new work, moving work through backlog, refinement or implementation, releasing or cancelling work, or asking what is pending, in flight, or no longer valid."
allowed-tools: Bash(.claude/skills/kb/kb *), Bash(cat *), Bash(ls *), Bash(git *), Bash(gh *), Read, Edit, Write
metadata:
  version: 0.1.0
---

# intent — Managing What the Project Means to Do

This skill is the process; the mechanics live in the `kb` skill. Every command below is `.claude/skills/kb/kb intent
…`. There is no separate implementation — see [decision 0002](../../../kb/bundles/morphir/morphir-scala/decisions/0002-intent-tooling-lives-in-the-kb-skill.md)
for why, and do not try to split them without reading it first.

```bash
.claude/skills/kb/kb intent list --open
```

## The one distinction that matters

**Intent** is future-tense and has a lifecycle — what the project means to do. **Capability** is present-tense and is
simply either true or stale — what the system does today. They are different documents in different bundles, and
conflating them is what makes knowledge bases rot.

Releasing is where they meet: marking an Intent Released **requires** linking the Capability it produced. That single
obligation is what stops the knowledge base falling behind the code.

Full glossary: [kb/CONTEXT.md](../../../kb/CONTEXT.md).

## Lifecycle

```
Backlog ──▶ Refinement ──▶ InProgress ──▶ Released
   └──────────┴─────────────┴──────────▶ Cancelled / Superseded
```

| State | Means | Owes |
| ----- | ----- | ---- |
| `Backlog` | Accepted as real work, not yet specified | — |
| `Refinement` | Being specified; the design is not settled | — |
| `InProgress` | Design settled, actively being built | — |
| `Released` | Shipped | A Capability link, for user-visible kinds |
| `Cancelled` | Decided against | A reason |
| `Superseded` | Replaced by another Intent | A successor |

Transitions are **not** policed — work genuinely jumps stages, and a one-line fix may go Backlog straight to
Released. What is enforced is what a record owes *wherever it currently sits*.

**Deprecated is not a state.** You deprecate a shipped Capability, not a backlog item. Retiring something is *new*
Intent, of `kind: deprecation`, followed later by one of `kind: removal`.

## Kinds

User-visible — these appear in release notes:

`feature` · `bug` · `performance` · `security` · `deprecation` · `removal`

Internal — these do not:

`refactor` · `docs` · `test` · `build` · `spike`

`breaking: true` is separate from kind, because a feature *or* a bug fix can break compatibility. It is what drives a
major bump.

Only user-visible kinds must link a Capability on release. Internal work often has nothing for the knowledge base to
learn, and inventing a document for "added three labels" is the noise this design avoids.

## Working with it

**Capture.** GitHub Issues is the inbox — anyone may file there. An issue becomes Intent when a maintainer decides it
is real work worth durable prose. Most issues never do.

```bash
.claude/skills/kb/kb intent new --title "…" --description "…" --kind feature --issue 1234
```

Then write the **Problem** section. Resist describing a solution there — the Feature Request template's Job Story
form ("When *[trigger]*, I want to *[goal]*, so I can *[outcome]*") is a good discipline.

**Progress.**

```bash
.claude/skills/kb/kb intent refine 0007
```

```bash
.claude/skills/kb/kb intent start 0007
```

**Finish.** Each verb demands what its state owes, at the moment you have the answer:

```bash
.claude/skills/kb/kb intent release 0007 --capability morphir/morphir-scala:/wasm-linking.md --artifact pkg:maven/org.finos.morphir/morphir-langkit@0.4.0
```

```bash
.claude/skills/kb/kb intent cancel 0007 --reason "…"
```

```bash
.claude/skills/kb/kb intent supersede 0007 --by 0012
```

**After any change**, regenerate the index and the database:

```bash
.claude/skills/kb/kb refresh
```

## Asking questions

```bash
.claude/skills/kb/kb intent list --open
```

```bash
.claude/skills/kb/kb intent list --user-visible --state Released
```

Anything more involved goes through SQL against the `v_intent` view:

```bash
.claude/skills/kb/kb query --sql "SELECT state, kind, count(*) FROM v_intent GROUP BY 1,2 ORDER BY 3 DESC"
```

## Keeping it honest

```bash
.claude/skills/kb/kb intent check
```

Errors are unmet obligations — a Released record with no Capability, a Cancelled one with no reason, a `superseded_by`
naming nothing. Warnings are staleness: an Intent sitting in Refinement or InProgress past the bundle's
`stale_after_days` is the honest signal that nobody is working on it. Move it on, or move it back to Backlog and say
so.

Backlog is deliberately never stale. A backlog is *meant* to sit.

## Portability

Nothing is hardcoded. The intent bundle is the one whose `index.md` frontmatter carries `intent: true`, and its
settings live there too:

```yaml
intent: true
system: pkg:maven/org.finos.morphir/morphir-core
capability_bundle: morphir/morphir-scala
stale_after_days: 60
```

`system` and released `artifacts` are [Package URLs](https://github.com/package-url/purl-spec) — a global vocabulary,
so the same skill works in a Python or npm repository unchanged. Capability links use `bundle-label:/path.md`
instead, because a Capability is a document in this knowledge base, not a registry-backed package.
[decision 0003](../../../kb/bundles/morphir/morphir-scala/decisions/0003-two-identifier-schemes-for-intent.md) records why both exist.

In a repository with no intent bundle yet:

```bash
.claude/skills/kb/kb intent init --system pkg:pypi/example --capability-bundle example
```
