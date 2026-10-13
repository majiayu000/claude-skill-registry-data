---
name: bulk-edit
description: Rewrite tracked files safely with a script. Use for edits too large or repetitive to perform by hand.
---

# Rewriting a tracked file with a script

A scripted rewrite is the right tool past a few dozen edits. It is also how a
whole file gets silently corrupted in one command, so the discipline below is not
optional. Every rule here comes from a rewrite that went wrong in this repo.

## Never match by line number

Line numbers drift the moment anything above them changes — including your own
earlier edits in the same session, and including a concurrent branch merge. Anchor
on something stable: a heading, a function signature, a unique marker.

The corollary: if you plan the edit from an agent's report, that report's line
numbers are already stale by the time you apply it. Re-derive them, or match on
text.

## Dry-run first, and make the dry-run informative

The script should be able to run without writing, and print enough to be judged:
how many units it matched, how many it will change, how many it did **not**
recognise, and the resulting size. An unmatched unit is the interesting number —
it usually means the matcher is broken, not that the file is unusual.

Default unmatched units to **keep unchanged**. A matcher bug should cost you a
missed improvement, never a deletion.

## Refuse to write on detected corruption

Put the check inside the script, not in your head:

```js
const mojibake = (result.match(/â€/g) || []).length;
if (mojibake > 0) {
	console.error(`REFUSING TO WRITE: ${mojibake} mojibake sequence(s)`);
	process.exit(1);
}
```

This exact guard exists because a rewrite of `docs/PROJECT_MEMORY.md` shipped 212
mojibake sequences into the canonical memory. The corruption entered upstream —
the replacement blocks had been extracted with `Get-Content` without
`-Encoding UTF8`, which decodes as ANSI on PowerShell 5.1 — and the write step
copied it faithfully. **A rewrite is only as clean as the data you feed it: check
the input, then check the output.**

## Enforce the repository's LF contract

Normalize source text before matching and write LF, as declared by
`.gitattributes`:

```js
const src = raw.replace(/\r\n?/g, '\n');
// … edit …
if (out.includes('\r')) throw new Error('refusing to write non-LF text');
fs.writeFileSync(p, out, 'utf8');
```

Do not use a bulk rewrite to normalize unrelated files in an active dirty
worktree. Line-ending migration is a separate, explicitly reviewed change.

## Prove you did not lose anything

Structure the check as a before/after comparison, not a glance at the diff:

```js
const keys = (t) => [...t.matchAll(/^###\s+(.+)$/gm)].map(normalise);
const lost = keys(before).filter((k) => !keys(after).includes(k));
const added = keys(after).filter((k) => !keys(before).includes(k));
```

Read `before` from git (`git show HEAD:<path>`), not from a copy you made — the
copy may already carry the damage.

Then probe for the load-bearing content by meaning, not by heading: if the file
is a memory or a spec, grep the result for the handful of statements that must
survive. A section can be renamed legitimately; a rule disappearing is a bug.

Finally read `git diff --stat`. A rewrite that reports the whole file changed is
usually an encoding or line-ending accident, not real work.

## Then run the gates

Run `node ./tools/test/verify-change.cjs` and every selected gate. Ordinary
Markdown selects JS; historical performance reports select strict conventions.
`doc-paths` only rejects obsolete roots in driver documentation, not arbitrary
broken links. Verify rewritten links directly. See the `verify-change` skill.
