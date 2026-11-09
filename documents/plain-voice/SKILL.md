---
name: plain-voice
description: Rewrite or draft text in a plain, teammate-to-teammate style, for pull or merge request comments, review replies, issue descriptions and short team updates. Use whenever text will be read by a teammate, or when the user says "simpler", "make it plainer", "no em dashes", or "rewrite this comment".
---

# Plain voice

Plain English, the way a normal engineer talks to a teammate. Not a polished writer, not an academic paper, not a corporate update.

## Rules

1. Short sentences. Everyday words.
2. Polite and curious. Ask, do not lecture. "Can we take `items` as a prop here?" not "This must be refactored."
3. No em dashes. Use a comma, a full stop, or "and" / "but".
4. No formal filler: furthermore, leverage, in order to, it is worth noting, this ensures that, robust, seamless, comprehensive.
5. No opening compliments. No "Great work!", no "Nice catch!". Start with the point.
6. Every suggestion comes with a code example, a diff, or a command. Prose alone is not a suggestion.
7. If something is unclear, ask a question instead of guessing.
8. Links as markdown links with the reference as text: `[#123](url)`. Do not paste a bare issue number, some renderers mangle it, and a link says where it points.
9. Review comments start with a [Conventional Comments](https://conventionalcomments.org/) label and say whether they block: `suggestion (non-blocking):`, `issue:`, `question:`.
10. When the project asks for machine-authored posts to be labelled, label them. Commit messages and descriptions are written by the author, so they carry no label.

## Before and after

Before:

> Great work on this! It is worth noting that the child component re-executes the parent's query, which ensures data freshness but introduces redundant network calls. Consider leveraging props instead.

After:

> suggestion (non-blocking): `item_details.vue` runs `itemsQuery` again, but `items_list.vue` already has the result. Can we pass it down instead?
> ```diff
> - <item-details :item-id="itemId" />
> + <item-details :item="item" />
> ```

Before (update):

> Hi team, quick update: I've completed the removal of the legacy column (see 12345) and am now focusing on the handover documentation.

After:

> Legacy column is out, [#123](url) merged. Next I am writing the handover doc. Shout if you want anything covered in it.

## Checklist before handing text back

- [ ] Reread once, cut formal words.
- [ ] Zero em dashes (search for the character).
- [ ] Every suggestion has code.
- [ ] Guesses are turned into questions.
- [ ] Links are markdown links.
