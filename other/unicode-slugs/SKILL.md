---
name: unicode-slugs
description: Build URL slugs from titles that may contain accents, punctuation or repeated separators. Use when writing or fixing a slugify function.
---

# Unicode-safe slugs

1. Normalize with `String.prototype.normalize('NFKD')` so accented letters split into a base letter
   and combining marks.
2. Remove the combining marks: `.replace(/[̀-ͯ]/g, '')`.
3. Lowercase, then replace every run of characters that are not `a-z` or `0-9` with one hyphen.
4. Trim hyphens from both ends.
5. Run the project's tests before saying you are done.
