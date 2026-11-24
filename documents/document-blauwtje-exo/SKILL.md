---
name: document
description: "Writes and edits prose read later: README, doc page, PR body, changelog line, release notes. Use when the user asks for one. Not for chat replies or code comments."
argument-hint: "the document or text to write or edit"
model: sonnet
effort: medium
metadata:
  author: exo
  tags: [documentation, writing, changelog]
---

# Document

## Purpose

Prose for a reader who was not in the session says who does what, by which mechanism, in the plain word. Avoid text that sounds finished and says little, and avoid the opposite, telegraphic text without articles and verbs that the reader must decode.

## Prerequisites

`node` and `git` for the release notes script, otherwise none.

## Instructions

### Process

1. **Pick one mode per document.** A tutorial teaches by doing, a how-to gets a known task done, a reference lists what exists, an explanation says why. A how-to opens on the command, with no welcome or tour. For "how does X work" about code, give the flow from trigger to effect with file:function names, then where things live and what surprises a newcomer; state your reading of an ambiguous question and go on.
2. **State the fact, not the benefit.** Give the number, behavior or error that changed. When asked to sell or impress, still write only what the input states, because an unmeasured effect is invented.
3. **Name the actor and the mechanism.** Use the active voice with the real file, option, flag and command names, and one name per thing.
4. **Write whole sentences.** One thought per sentence, under 25 words. Put the condition before the instruction and the warning before the step it guards. Put "only" and "not" next to the word they limit.
5. **Change only what the request names.** Run the doc's link or reference check when one exists.
6. **Scan the draft for the tics below and rewrite each hit.** When reviewing someone else's text, quote each hit.

### Tics

- Trailing "-ing" benefit phrase ("ensuring stable memory"), inflated significance, a vague source, a promise about the future. State the number or cut it.
- Quality adjectives with no measurement (robust, seamless, significantly). Give the measured change.
- Stock vocabulary (delve, pivotal, landscape, showcase, leverage, utilize, facilitate), "serves as" for "is", "not just X but Y", lists of three for rhythm, and "simply" or "just".
- Em dashes, a colon for drama, bold on ordinary words, Title Case headings, emoji, curly quotes around code, headings on a one-paragraph text.
- Chat traces: "Here is...", praise, "I hope this helps", "That's it!", a section that describes itself, a summary repeating the list above it.
- Hedges stacked ("could potentially"), filler ("in order to", "it is worth noting"), aphorisms, abstract metaphors (backbone, guardrail), and "feels smoother" where a mechanism belongs.
- A passive verb with no actor, a pronoun with two possible referents, a noun stack, a semicolon joining sentences.

### Release notes

When the user asks for release notes or the changelog lines a range misses:

1. Run `node "${CLAUDE_SKILL_DIR}/scripts/release-notes-draft.mjs" --repo <checkout> [--from <ref>] [--to <ref>]`. `--from` defaults to the last `v*` tag reachable from `--to`, `--to` to `HEAD`.
2. Rewrite each line to say what the user sees. Fill each `Upgrade: not stated in the commit.` line from the commit diff, and keep the `Upgrade:` line under each breaking entry.
3. In the changelog, follow its existing format for a breaking change.
4. Name the range used in one line, so the user can rerun it. Edit the changelog only when the user names it, and never tag, bump or release.

### Judgment

- The codebase's name outranks the plain word: `maxBytes` stays `maxBytes`.
- A fact, number or term the reader needs outranks every tic fix, and a tic inside a quotation, command or code sample stays as written.

## Examples

A request to write release notes for the commits since the last tag:

```
node "${CLAUDE_SKILL_DIR}/scripts/release-notes-draft.mjs" --repo <checkout>
```

The skill rewrites each drafted line to say what the user sees, fills each `Upgrade:` line from the commit diff and names the range in one line.

## Limitations

- The pull request body layout of `exo:ship` and the brief sections of `exo:spec` outrank this skill's layout, and product interface strings follow the product's copy rules.

## Troubleshooting

| Error | Cause | Solution |
| --- | --- | --- |
| `No user-facing commits in <range>.` | No commit in the range has a user-facing type. | Pass `--from <ref>` with an older ref. |
| `Upgrade: not stated in the commit.` | The commit has no upgrade footer. | Fill the line from the commit diff. |

## Available Scripts

| Script | Purpose | Arguments |
| --- | --- | --- |
| `release-notes-draft.mjs` | Drafts release notes from the commits of a range. | `--repo <checkout>`, `--from <ref>`, `--to <ref>` |
