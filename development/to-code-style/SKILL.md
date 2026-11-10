---
name: to-code-style
description: "Turn a session's friction and the user's style rulings into proposed updates to the style docs (config/docs/code-style.md, packages/framework/docs/code-style.md) / packages/framework/docs/vocabulary.md / docs/prose-style.md / AGENTS.md: what the docs failed to tell you, and the rules the user set. Runs on this session or on another agent's. Prose rulings go to /to-writing-style."
disable-model-invocation: true
---

Legend: 🪤 what went wrong · 📝 what to write.

Mine a session for **friction** (every place the project's own docs cost time) and for **style rulings** (every shape of code the user had changed). Propose the edits that would spare the next session.

The spine test, applied to every candidate:

> **Propose only what a doc could have told you before the session started.**

What you _decided_ about what a feature does belongs in a spec, an issue, or a commit message. A ruling about _how code is shaped_, for this feature or any, belongs in a style doc, even though it was decided this session. What you had to _find out_ belongs in the docs. A retro that restates conclusions has failed even if every line is true.

Do steps 0-3 silently. The user sees only step 4.

## 0. Pick the session

- No argument: this session.
- A session ID or path: that transcript.
- "The last session": the newest transcript that is not your own, found by [`docs/session-transcripts.md`](../../../docs/session-transcripts.md).

Say which file you chose in one line. When the session is not yours, also:

- **Read its handoff first**, if it left one ([`docs/agents/planning.md`](../../../docs/agents/planning.md#handoffs)). It says what the session was trying to do.
- **Read the user's turns before anything else**, with the command in [`docs/session-transcripts.md`](../../../docs/session-transcripts.md), which also says which `type:"user"` entries are the user's.
- **Bound the session's changes by its first and last timestamps**, and take them from `git log` and `git diff` over that window. The branch may hold other work.
- **Check every candidate against the docs as they are now.** A later session may have added it already. `git log -- docs AGENTS.md` shows what the reviewed session itself changed.

## 1. Hunt

Name every instance of these kinds. Be relentless: the easy two surface on their own, and stopping there is the failure mode.

- **Misdirection**: a doc line that was read and acted on and pointed wrong. Usually not false: stale, or written in a tense that implies a live defect where the code already handles it, or precise about a mechanism and silent about whether it currently bites.
- **Rediscovery**: a fact derived by reading source, probing, or measuring. Measurements are the richest kind, because they cannot be looked up at all.
- **Stated rule**: a preference or rule the user articulated that no doc holds. Scan the user's own turns for "I prefer", "as a general rule", "always", or a correction of an approach the agent proposed.
- **Style ruling**: a shape of code the user objected to and had changed, stated as a rule or not. Read the session's diff as well as the conversation: each refactor the user directed is a candidate. The rule is the generalization of the change ("named accessors, never inline lookups"), not the change itself. A ruling counts even if it cost the session nothing, and even if a style doc already gestures at it. A rule the docs hold but the agent or the codebase broke goes in as a sharpened line, not a new one.
- **Review miss**: a shape the developer had changed after `/code-review` passed it. Name the standard the reviewer lacked, or the line it had and skipped; the second goes in as a sharpened line.

**Prose rulings are not yours.** A ruling on reader-facing prose ([`prose-files.md`](../../../docs/agents/prose-files.md#terms)) goes to `/to-writing-style`; drop it here with that reason.

**Include wrong turns, and weight them heavily.** A confident claim that had to be retracted is the strongest possible signal: something about this codebase invites that specific error, and a doc line can disarm it for everyone after. Under-reporting these is the default; resist it.

In your own session you observed the friction. In another's you infer it, from:

- a user turn correcting the agent;
- the agent retracting itself ("actually", "I was wrong");
- three or more reads or greps around one question, ending in a conclusion (a rediscovery);
- a doc read followed by an action that contradicts it (misdirection).

Tag each item `observed` or `inferred`, and rank `inferred` lower. If a stated rule sounds situational, quote the user's words and do not generalize it; you cannot tell whether it was meant as a rule.

Done when every wrong turn, rediscovered fact, user-stated rule and style ruling is either carried to step 2 or dismissed with a stated reason. Friction you hit while doing the review is not the session's; report it separately.

## 2. Keep what passes all four tests

- **Beforehand**: could a doc have stated this before the session began? (Conclusions, decisions, and summaries fail here. Style rulings pass.)
- **Ownership**: is it already assigned to a spec, issue, or PR from this session, or already in the docs now? Leave it there and say so; do not write it twice.
- **Lookup**: can the next agent find it with one file read or one command? Leave it to the environment, where it cannot go stale. Cache only what cannot be found by looking: the unwritten convention, the reason behind a choice, the measurement, the gotcha no config confesses. Before proposing a check, read `config/eslint.js` and the `lint` scripts: a rule that exists but is off or scoped away is the finding.
- **Durability**: will it still be true in three months? Counts and tallies of generated data go stale; the invariant behind them does not.

## 3. Route and rank

- **A mechanical ruling** (a fixed syntax shape, a banned API, an import shape, a file location) becomes a check, not a line: an entry in `styleSyntax` in `config/eslint.js`, or a `config/docLint.js` rule for docs. Propose the selector and message. A style doc line is for judgement calls only a person can make.
- **packages/framework/docs/vocabulary.md** and **`packages/framework/src/AGENTS.md`**: the architecture words and the tiers. README.md is derived prose for people, never the home of a fact. A design principle is one line in packages/framework/docs/design.md plus its reasoning in `docs/design/`.
- **config/docs/code-style.md** and **packages/framework/docs/code-style.md**: code shape. The charter is rules distilled from the user's own refactors, so a **stated rule** or **style ruling** almost always lands in one of them, as one line: the framework's if it names Sheets, a tier, `Val` or a framework path, otherwise the general one in `config/`. Reasoning and worked examples live under each file's `docs/code-style/`; a rule that needs an example adds the line to the style doc and the example to the fragment. For a ruling, the before and after from the session's diff is the example.
- **docs/prose-style.md**: how developer-facing prose is shaped ([defined in `prose-files.md`](../../../docs/agents/prose-files.md#terms)). A stated rule or ruling on the shape of a doc, skill or AGENTS.md lands here as one line, with its reasoning under `docs/prose-style/`.
- **AGENTS.md**: loaded every turn, so it earns a line only if that line changes turn-one behavior. Everything else goes in the targets above, or under `docs/agents/`, with a pointer at most.
- **Any other doc** (architecture mechanics, hosts, generated data, testing, Claude Code hooks): the file [`prose-files.md`'s map](../../../docs/agents/prose-files.md#map) gives it.

Rank by time the change would have saved, and say so. A ranked list lets the user take the top three and stop.

## 4. Present, then wait

**Weigh the recommendations you put to the developer against the Codebase Priorities, [`docs/agents/codebase-priorities.md`](../../../docs/agents/codebase-priorities.md).**

One block per item, most valuable first, numbered so the user can answer "1, 3, skip 2":

```
🪤 **F1** - **<title>** (misdirection | rediscovery | stated rule | style ruling | wrong turn; observed | inferred): <what cost time, in one or two sentences. Quote the doc line if there was one.> (session ab12, 22:53)

📝 `<file>`: <the exact line to add or change, in a code block if it is more than a sentence>

---

🪤 **F2** - ...
```

- The 🪤 half says what went wrong, with no fix in it. For a style ruling it quotes the code as it was and what the user objected to. The 📝 half says what to write, with no story in it. Either half should read alone.
- Give the wording, not a description of it. The user is approving the edit, not the idea.
- The `(session ab12, 22:53)` pointer is for another agent's session: the short session ID and the timestamp of the turn, so the user can check it.
- End with one line for what you dropped: `Dropped: <item> (owned by #123), <item> (one grep away)`. When you noticed other sites still in the old shape of a style ruling, add `Other sites still in the old shape: <n>`. Report them; do not fix them.

Then stop. Do not edit until the user approves; an agent running this skill does not approve for itself.

## 5. On approval of items

Write only the approved items. Before writing an AGENTS.md or skill line, call the Skill tool with `writing-for-agents`. Then `npx prettier --check` the touched files. Then ask whether to commit, and on which branch: the reviewed session may have left work in flight, and a docs-only commit should not ride along with it.
