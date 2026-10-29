---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: update-playwriter-skill
description: >
  Self-improve the playwriter skill: reflect on past playwriter mistakes and
  unclear docs from this session, then update
  /Users/morse/Documents/GitHub/playwriter/playwriter/src/skill.md with minimal
  diffs, commit it, and return a critique link. Load when the user asks to
  update, improve, or store learnings into the playwriter skill.
---

based on your past interactions with playwriter think deeply:

- what were the mistakes that made you lose the most time and context window?
- what were some things that playwriter skill made not clear enough and we should update and write about more in detail?
- if we had problem controlling a website what would have been some information that would have helped and prevent mistakes?
- what are some functions and playwriter APIs we should have called but we didn't because the skill was not clear enough?

then create a plan and apply it to update the file `/Users/morse/Documents/GitHub/playwriter/playwriter/src/skill.md` with the improvements and added sections

prefer updating existing sections instead of always adding new ones

plan well the best place to put each part

keep diffs minimal

after the change you should commit the update with prefix `playwriter skill self improvement: <why this change is needed>`

then return to the user the critique diff of the change made. using critique cli for that commit hash

be concise and clear.
