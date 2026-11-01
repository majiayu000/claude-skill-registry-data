---
name: sync-docs
description: Check Pieceful docs, ADRs, roadmap, task board, and code for drift or contradictions and report them. Use for /sync-docs or before a milestone checkpoint.
---

# /sync-docs: find drift

1. Compare:
   - **requirements ↔ feature specs:** every F-xx has a spec or a "not written" entry
   - **feature specs ↔ tasks ↔ roadmap:** milestones and statuses agree
   - **ADRs ↔ docs:** accepted decisions are reflected; nothing contradicts them
   - **docs ↔ code** (from M0): structure, commands, API, data model
   - **links:** every relative link resolves
   - **public voice:** no personal or raw notes in public docs
2. Report a short list: `file: problem → suggested fix`. Most severe first.
3. **Fix only after the owner agrees**, and only what they approve. Don't commit.
