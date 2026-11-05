---
name: vale-alerts
description: Give each Vale alert an editor's verdict - rewrite the sentence or suppress the one rule. Use when Vale reports an error, warning, or suggestion, or before adding a term to a Vale vocabulary.
---

# Vale alerts

Goodhart's law applies: a change that silences an alert but makes the sentence
worse is a regression, even though the report goes green. Give every alert an
editor's verdict: rewrite or suppress.

## Verdicts

**Rewrite.** The flagged span shows where a smell surfaced, which is seldom
where the problem started. Reread the whole sentence and ask what it is trying to say.
Restructure over substitute: when `a number of` is flagged, name the things.
When a hedge is flagged, make the call and state it plainly. Keep the meaning
true: replace `several` with `5` when you counted five. When nobody counted,
keep only the precision you possess. A sentence that satisfies the rule but
reads worse than before means the verdict was wrong, so suppress instead.

**Suppress.** A false positive keeps its prose, such as quoted material, a term of
art, deliberate emphasis, or honest vagueness. A rule you find yourself suppressing at
every occurrence is worth raising with a maintainer. Changing the rules
themselves is a separate decision, outside the scope of fixing prose.

**Spelling and term alerts** (`Vale.Spelling`, `Vale.Terms`) usually ask a
use-mention question: is the string a word, or a literal that belongs in code
font? Read [`VOCABULARY.md`](VOCABULARY.md) before you add an entry to a
vocabulary.

## Suppressing one passage

<!-- vale ai-tells.FigurativeIdioms = NO -->
<!-- "Blast radius" is the term of art for how far a suppression reaches. -->

Keep a suppression's blast radius to one rule over one passage, with Vale's
[comment markers](https://vale.sh/docs/keys/commentdelimiters). Prose about a
valley trips a `Vale` casing term that expects the product name:

<!-- vale ai-tells.FigurativeIdioms = YES -->

```markdown
<!-- vale Vale.Terms = NO -->
<!-- The paragraph below names the valley, not the linter. -->

The vale lay under morning fog.

<!-- vale Vale.Terms = YES -->
```

Name the rule exactly as the report prints it, and turn it back on right after
the passage. Pair each marker with a comment that states why the rule is off
there, so the next editor can tell a deliberate exception from a leftover.

## Done

Reread each sentence you changed as an editor who never saw the report. You
are done when every alert has a verdict and every touched sentence reads at
least as well as it did before.
