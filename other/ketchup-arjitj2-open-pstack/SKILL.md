---
name: ketchup
description: "Catch the user up on what changed in this chat since their last message, in a few plain sentences and small visuals. Give each action item just enough context to make the call. Use for /ketchup."
disable-model-invocation: true
---

# Ketchup

Invoke manually as `/pstack:ketchup` in Claude Code, or select `pstack:ketchup` or mention `$pstack:ketchup` in Codex. Do not load it implicitly.

Catch the user up on everything in this chat since the last actual human-authored message before this invocation. Exclude the invocation itself, system messages, heartbeat and scheduler prompts, automated notifications, and subagent results when choosing that anchor, even if the host presents them as user-role events. Automated events after the anchor still belong in the catch-up. If the true anchor or intervening activity cannot be established, state the gap and use only confirmed current-chat context. Do not search unrelated chats. Assume the user remembers their last message and nothing after it. Help them understand each change, not only where it stands.

Use [`/bro`](../bro/SKILL.md)'s voice, not its task: plain words, short sentences, no jargon, like one person catching up another. Say what changed for the user, not how you did it. Say "the tests pass", not "CI is green". Leave out hashes, file paths, commands, build numbers, and test counts unless the user needs one to act. Call each PR, branch, or agent by a name the user would know, not by a label you invented. If a fact needs context to make sense, give the context or leave the fact out.

## Gather what changed

Keep this turn read-only. Collect your own work since that message, reports from subagents, and messages from anyone else in this chat. Check the current state of each PR, CI run, or agent this chat touched through existing CLI, API, or connector readers. Inspect a UI only under explicit user authorization for the current task and scope. General task authorization or an app mention does not grant it. If status requires unauthorized UI or an unavailable reader, name the concrete limitation and leave that status unchecked. Say which tasks are still running.

Treat earlier agent prose as claims, not verified current state. Check it against available artifacts and human instructions before repeating its implications. Distinguish verified implemented behavior, proposed options, and unknowns. A proposed parameter does not prove its mechanism exists. Operational bounds, costs, guarantees, and causal rationale require evidence for the underlying mechanism and supported assumptions; arithmetic from option labels alone is not that evidence. Before writing a comparison, identify the mechanism in the inspected artifact. An admission predicate is not a cache store, and a proposed expiry setting does not establish a freshness bound or lower backend load. If that mechanism is absent, label each option as a proposed policy with unknown effects. Check every visual label against this distinction before sending; a shorter label must not turn a proposal into a guarantee.

Do not edit files, accounts, issues, PRs, installations, model sheets, or scheduler state. Do not dispatch or resume work, start Babysit repairs, approve, merge, ship, or cancel anything.

Make visuals only from what you already have. Check each number you will show against the facts it comes from, and say so when you correct one.

An action item is a decision or step only the user can take, such as a product choice, an approval, an irreversible action, or access you lack. Include any still waiting on the user, even one raised before their last message. Work you can still do yourself is not an action item. Never make up a call to fill the reply. A step the user did not ask for and the work does not need is not an action item, unless it is irreversible and waiting on the user: give it one action line, no visual, and skip what happens if the user does not answer.

## Write the reply

Keep the whole reply well under 150 words, not counting visuals; words in Markdown tables still count. When something is easier to grasp as a picture than as sentences, draw it: how a design or system works, a PR stack or dependency chain with each PR's state, a before and after of a fix, or options side by side. Never draw a status list or boxes with nothing connecting them. Never give a fact twice, in text or across visuals. If media already explains a change, its summary may add only a status the media does not show. Leave out work that changed nothing for the user. When words run short, cut from what happened before you cut from the action items.

Open with one sentence that says how many things need the user, or that nothing does. If nothing happened and nothing waits on the user, say so and stop.

Then show what happened, pictures first. Embed inline the screenshots and videos the work produced, then any diagram that explains a change. Then sum up in one short bullet per thing the user asked for: what came of it, and whether it is done, still running, failed, or not checked. Write each line the way you would say it out loud: "Search was slow from a missing index", not "Search review: done" or "Slow search: missing index". Name any bug found and fixed on the way. Each line must stay true when read alone. Never mark something done that still waits on the user, and leave out anything the action items say. Under the summary, give at most three short lines that change what the user knows or must do. Then name in one line any work left that you can do yourself.

Then list the action items as plain bullets, never as a diagram or box. Keep each action and its no-answer consequence in the same bullet. Give each two lines, or one for an unasked irreversible step: the decision with your recommendation and why, then what happens if the user does not answer. Ask the call the user owns, such as merge, approve, or pick. A step you would take first goes in your recommendation. So does anything that must happen first, and anything that cannot be undone. Write "unknown" for a part you do not know. Link to the detail.

Show a choice after the list. If the screenshots above already show its options, write each option's gain and cost under its screenshot instead of drawing a new visual; otherwise, compare the options side by side in a visual, with the current state when there is one. A Markdown table does not satisfy this comparison. Give every option the work weighed, each with what it gets the user and what it costs. Keep them out of the rest of the text.

## Visuals

A visual is a picture: a screenshot, a video, a Mermaid diagram, an available chart or diagram tool, or a generated image. A Markdown table is not a visual, even with before and after columns.

Keep each visual small enough to read at a glance: at most six boxes, with at most eight words in each. Write labels as plain words a person would say, not tags like "Tests: pass". A fact that needs a sentence belongs in the text, or nowhere.

Embed screenshots and videos inline when the change is visible, not only as links. If a visible change has none, mark its summary line "No screenshot yet," and say there what changed on screen. Draw diagrams and charts from facts you have: a Mermaid diagram for how things connect and an available chart tool for numbers. Never invent a number, and never draw or generate a picture of a screen you did not capture. Link only artifacts that exist.
