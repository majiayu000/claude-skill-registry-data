---
name: approve-letter
description: "Marks a draft letter as approved and ready to send. Use when Mandy says 'approve letter', 'approve it', 'ready to send', 'mark as approved', or confirms a draft is final."
---

# Approve Letter

## Important
- Manual-only. Letters MUST be approved before sending.

## Instructions

### Step 0: Resolve Matter
Follow `_shared/resolve-matter.md`.

### Step 1: Identify Letter
If filename given: find in `letters/`.
If not given: list all draft letters for this matter and ask which one.

### Step 2: Verify and Update
Read `matter.json`. Find letter in letters array.
If status is already "approved" or "sent": inform Mandy.
If "draft": update status to "approved", set `date_approved` to today.

### Step 3: Commit
1. Update `matters/index.jsonl`
2. Append to `activity-log.jsonl`
3. `git -C matters/ add -A && git -C matters/ commit -m "approve-letter: {id} — Approved {filename}."`
4. Confirm: "Letter approved. Use `/send-letter {name} {filename}` to send via Outlook, or send manually."
