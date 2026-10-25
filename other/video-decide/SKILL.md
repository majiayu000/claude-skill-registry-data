---
name: "video-decide"
description: "After a video has been processed, propose Adopt, Park or Drop for each tool or idea, with reason, project link and review date, for the user to approve."
---

# Video decide (final step)

Use this after extraction and the library update, so that watching a video ends in a decision instead of just storage. The user decides; this skill prepares the proposal.

## For each tool, repo, technique or idea worth keeping
Propose exactly one outcome:
- **Adopt:** worth testing or using now. Give the first small test (what to run, what a pass looks like). If it is a repo, say whether to clone and test it, and where it would fit.
- **Park:** might matter later. Give the reason and a review date (default 30 days).
- **Drop:** not useful, risky or duplicate. Give the reason so it is not researched twice.

## Fields to record (in the library entry)
- `decision`: adopt / park / drop (proposed, then confirmed by the user)
- `reason`: one or two sentences
- `used_in`: the project it serves (for example Better Style, Pyburticapa, yt-outliers, 411, the 3D marketing engine), or `none yet`
- `review_by`: a date for park items
- `first_test`: for adopt items
- `origin_label`: carried over from extraction (verified here, source claim, our inference, unchecked)

## Judgement guide
- Prefer Adopt when it removes a step in a workflow the user already runs, costs nothing or fits the $20 tool budget, and can be tested in under an hour.
- Prefer Park when it is interesting but there is no project to attach it to.
- Prefer Drop when it duplicates something the user already has, needs a paid tier beyond budget, or rests only on an unchecked source claim with no way to test it.
- A claim with the label `source claim` or `unchecked` can be Adopt only as a test, never as a conclusion.

## Safety
- If an item would give an agent access to accounts, money or messaging, flag the permission risk and recommend a read-only or test setup first.
- Do not install or run anything from a video's links without the user saying so.

## Monthly review (when the user asks, or each time the library is opened after 30 days)
List entries with `used_in: none yet` and `review_by` dates that have passed. Propose promote, extend or drop.

## Output
A short table: item, proposed decision, reason, used in, first test or review date. End by asking the user to confirm, change or reject each proposal. Do not write confirmed decisions to the library until the user answers.