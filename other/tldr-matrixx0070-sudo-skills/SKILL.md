---
name: tldr
version: 1.0.0
description: Compress long text into a one-line takeaway plus the few points that matter - numbers and meaning-changing caveats preserved, nothing invented.
triggers:
  - tldr
  - tl;dr
  - summarize this
  - give me the short version
  - key points only
capabilities: []
inputs:
  - name: text
    required: true
    description: The long text, article, or thread to compress.
  - name: focus
    required: false
    description: Optional angle to prioritize (e.g. "costs", "risks", "what changed").
---

# TLDR

## When to use
Use this when someone has a long article, thread, document, or message and wants the 30-second version they can act on or forward - the conclusion plus the few facts that make it trustworthy.

**Not for:** text where every clause matters and losing one is dangerous - contracts, statutes, medical guidance, precise specs (summarize those and you may strip the qualifier that flips the meaning). Also not for very short inputs that are already the short version, or for tasks that need synthesis across many sources rather than compression of one - reach for a research summary there.

## Method
1. **Find the single conclusion or event** the text exists to convey. That becomes the one-line takeaway.
2. **Pick the 3-6 supporting facts** a reader needs to trust or act on it - one fact per bullet, not a paragraph.
3. **Preserve meaning-changing caveats.** *Decision point:* if the source says "X, unless Y", the summary must not say just "X". Dropping a qualifier that flips the conclusion is a failure, not a trim.
4. **Carry numbers verbatim** - dates, prices, versions, percentages. Never round away a figure someone would act on.
5. **Add no new claims.** *Decision point:* if the source is ambiguous, write "unclear" rather than resolving it yourself.
6. **If `focus` is given, reorder** so that angle leads. End with "Worth reading in full if:" and one honest criterion, so the reader knows when the summary is not enough.

## Example
**Input:** a 2,000-word vendor security bulletin about a patched vulnerability.

**Output:**
**TLDR: Versions 4.2-4.7 leak session tokens via the export endpoint; patch to 4.8 or disable exports until you do.**

- Exploitable without login, but only when the export feature is enabled (off by default).
- Patch 4.8 released 2026-07-08; no workaround besides disabling exports.
- Vendor says no known exploitation in the wild so far.

Worth reading in full if: you run a custom build or need the CVE details for compliance reporting.

## Pitfalls
- **Dropping the qualifier.** Turning "affected only if exports are enabled" into "everyone is affected" changes the reader's actions.
- **Rounding numbers.** "About 4.x" instead of "4.2-4.7", or "~$30" instead of "$29" - someone acts on the imprecise figure.
- **Smuggling opinion.** Adding a conclusion or recommendation the source never made.
- **Bullet bloat.** Ten bullets is not a TLDR; if you cannot get to six, you have not found the core yet.

## Output format
```
**TLDR: <one sentence a busy person could forward as-is>**

- <one fact or decision>
- <one fact or decision>
- <one fact or decision>

Worth reading in full if: <one honest criterion>
```
