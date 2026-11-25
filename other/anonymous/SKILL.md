---
type: skill
description: A skill that answers to neither of the two names it could have.
---

<!-- expect: FAILS -->

`exactlyOneOf: [name, title]` fails in its other direction here:
`FRONTMATTER__EXACTLY_ONE_OF_NONE_PRESENT`, with `satisfied` reported as the empty set. Its
opposite is `../legacy/SKILL.md`, which satisfies both arms. One constraint, two
codes, because a consumer holding only "exactlyOneOf failed" cannot tell whether to
add a name or delete one.
