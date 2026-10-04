---
name: icaire-learn-reply-to-forum-posts
description: Retrieve ICAIRE Educate forum posts, draft a batch of distinct instructor replies for approval, and send only exact approved replies through the OAuth-connected ICAIRE Educate MCP. Use when the user asks to review or answer learner discussions.
---

# ICAIRE Learn: Reply to Forum Posts

Prepare and send thoughtful instructor replies to ICAIRE Educate discussion
threads with a hard human approval gate before every write.

## Contract Checklist

- Use the OAuth-connected ICAIRE Educate MCP as the source of truth so the
  signed-in instructor identity determines the author; never choose or expose
  raw admin identifiers when OAuth can resolve identity.
- Expect `list_cohorts`, `list_cohort_forum_posts`, and
  `reply_to_cohort_forum_post`; use `find-missing-tools` when the tool surface
  is incomplete.
- Default to at most 10 unanswered top-level threads, oldest first.
- Exclude top-level posts authored by an instructor, administrator, or the
  OAuth-resolved active identity from the default reply queue.
- Keep learner-authored threads in the queue when peers have replied but no
  instructor or administrator has replied.
- Draft genuinely varied responses rather than copying repeated wording
  verbatim across learners.
- When explaining where to find something, include a Markdown link to the
  relevant course section.
- Show the exact reply batch and obtain explicit approval before sending.
- Re-fetch before sending and read back every successful reply afterward.
- Use `post_cohort_forum_message` only when explicitly asked to start a new
  discussion; never substitute it for a reply.

## Workflow

1. Resolve the forum queue:
   - resolve the requested cohort; if none was named and several are relevant,
     show the choices and ask which one to use
   - call `list_cohort_forum_posts` with `unanswered_only: true` by default
   - use a supported server-side author filter when available to exclude
     top-level posts by instructors, administrators, or the OAuth-resolved
     active identity; otherwise filter them locally before loading full detail
   - treat staff-authored top-level posts as prompts to monitor, not learner
     messages needing instructor replies; include them only when the user asks
     to review staff prompts, engagement, moderation, or replies to them
   - preserve learner-authored threads when learner peers have replied; for
     this queue, a thread is answered only after an instructor or administrator
     response, not merely because any reply exists
   - determine staff authorship from explicit author role and OAuth-resolved
     identity, never from writing style or a guessed name
   - select at most 10 top-level threads and sort them oldest first
   - include answered threads only when requested and label them as follow-ups
   - keep exact post IDs internally, but show stable labels such as `R1`, `R2`
   - Anti-patterns: mixing cohorts without consent, queueing our own admin
     prompt, treating a peer reply as an instructor answer, guessing identity,
     loading full staff threads only to discard them, replying to nested IDs,
     silently including answered threads, bypassing the MCP
2. Draft distinct replies:
   - read each full thread, including replies, author role, timestamps, and
     useful vote context
   - answer the learner's actual question in a concise, warm instructor voice
   - acknowledge relevant reasoning, distinguish facts from interpretation,
     and give a practical next step where useful
   - vary openings, sentence structure, acknowledgements, and closings when
     several learners ask similar questions; do not paste one answer verbatim
   - use supported Markdown links such as `[section name](https://...)` when a
     learner asks where to find course material, a quiz, or another resource
   - flag missing facts instead of inventing policy, dates, grades,
     certificates, attendance, commitments, partnerships, or technical claims
   - for private support or safeguarding matters, draft a brief public
     acknowledgement and mark the required private follow-up
   - Anti-patterns: templated duplicate replies, bare URLs when a descriptive
     course link is available, invented facts, exposing private learner data
3. Present the batch for approval:
   - for each item show its label, cohort, thread excerpt, learner's point,
     proposed reply in full, confidence or missing context, and action
   - state clearly that nothing has been sent
   - accept explicit choices such as `approve all`, `approve R1 and R3`,
     `edit R2: ...`, `skip R4`, or `stop`
   - after a material edit, display the revised wording and require approval
     again; approval applies only to the displayed wording and mapped thread
   - Anti-patterns: treating praise as send approval, hiding full wording,
     carrying approval from another batch, editing silently after approval
4. Send only approved replies:
   - re-fetch each approved thread immediately before sending and confirm the
     top-level post still exists, matches the reviewed content, and has not
     gained an instructor response
   - rely on OAuth identity resolution; if the MCP cannot unambiguously resolve
     the signed-in instructor, stop before the first write
   - call `reply_to_cohort_forum_post` once for each approved, current thread
   - continue safely after an individual failure without retrying successful
     items or sending skipped items
   - re-list the threads and verify each successful reply under the intended
     top-level post with the resolved instructor identity
   - Anti-patterns: sending stale drafts, duplicate retries, manual identity
     substitution, direct database writes, browser form submission

## Anti-Patterns

- Sending anything before explicit approval of the exact displayed draft.
- Queueing an instructor's or administrator's own discussion prompt as a
  learner message needing a reply.
- Removing a learner thread solely because another learner replied.
- Replying to a nested reply ID or starting a new discussion instead.
- Reusing identical prose across multiple learners.
- Claiming success without MCP read-back verification.
- Exposing learner data, access tokens, raw MCP responses, or admin IDs.

## Output

Before approval, report the cohort and learner-only queue scope, numbered full drafts,
missing context or private follow-ups, confirmation that nothing was sent, and
the available approval choices.

After sending, report sent labels and thread summaries, skipped or stale items,
per-item failures, MCP read-back status, and any private follow-up still needed.
