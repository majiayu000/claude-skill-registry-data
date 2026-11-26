---
name: antialgorithm
description: 'Stops the safe, average, comfortable pick that AI reaches for first. Use when a creative choice is left open to the agent: ideas, names, story, game mechanics, visual style, color, poster or page layout, app or web interface design, composition, slogans, titles, taglines, creative copy. Not for code identifiers, bug fixes, choices the user already made, or texts whose form the user''s standing rules already set, such as a README, a store page, a commit message, release notes or license text. Also use when the user says "too generic", "boring", "typical AI", "too safe", "cliche", "average", "seen it before".'
---

# antialgorithm

The first answer that comes to mind is the average of all that was already made. It feels right because it is familiar, and that is the problem: the user has seen it a thousand times. This skill makes you notice that pick and move away from it on purpose.

The user's standing rules, in CLAUDE.md, AGENTS.md or similar files and memory, always win over this skill, not only on language. If a rule there fixes the shape, the wording, the palette or the content of a piece, follow it and use this skill only for what is still open.

## Where to start

The answer must differ from one user to the next, and you cannot see what others got. So the start point has to come from outside your own taste:

1. If the request carries real context, such as a project, a place, a person, a purpose or a constraint, start from that.
2. If the request is thin and the work is short, such as a few slogans, a name or a short text, do not stop at a question. Make the work from a seed or a stated guess, then ask one short question at the end that would make it fit better. The question asks for a fact about the case, not for leave to redo the work. If the work is long or costly, such as a full design, a long text or a game system, ask the one short question first: who it is for, where it lives or what it is about.
3. If the request is thin and the user wants the work now, or cannot answer, roll a seed: `python3 scripts/seed.py visual`, `text` or `idea` (paths are relative to this skill's folder). Use what it gives as the starting point. The script keeps recent seeds in `history.jsonl` and avoids their values, so seeds do not repeat across sessions; `--no-log` rolls without saving. A visual seed also gives a verb and a scale: build the idea behind the piece from them, who does what, instead of a twist you think of yourself. You may roll one axis again once with `--only <axis>` if it truly fights the subject; pass the axes you keep with `--keep "axis=value"` so the new pick fits them. The region places the setting: the land, the weather and the buildings around it, and the names, jokes, habits and way of speaking of the people there, while the words stay in the language set near the end of this skill. Take what someone who lives there would know from a normal week: the brand on the bus stop, the way a neighbor greets you, what is broken and nobody fixes. Leave out what an outsider lists first, such as the national dish, the costume, the famous sight, the flag colors or the accent played for laughs. If you do not know enough real daily detail about the region, use less of it instead of filling the gap with the famous parts. Then tie the seed to the subject with a reason.

Never pick the start point by thinking about what would be most interesting. That thought lands on the same place for all users.

## The rule

Before you give a creative answer, find the obvious one first. Say it to yourself in one line: "the default here is X." Then do not use X unless the context truly asks for it.

Move away from the default by using what is specific to this case: the user's project, its world, its constraints, its audience, its odd details. A good choice could only belong here. A default choice could belong anywhere.

Do not swap one cliche for its well-known opposite. "Dark instead of bright" or "minimal instead of busy" is just the second most common answer.

Strange is not the goal. A choice that is odd but has no reason is as empty as a safe one. Each choice should have a reason you can say in one sentence, and the reason should come from this project, not from taste in general.

## Text

Do not write what any writer would write about any subject. If a sentence could be pasted into another project without changes, rewrite it until it could not.

Prefer the concrete detail over the general claim. Prefer the plain word over the impressive one. Prefer the unexpected but true angle over the expected summary.

A concrete detail is a thing a person could see, touch or do there. A count, a time or a day is the cheapest detail: use one only when the reader needs it to act.

Do not reach for the common opening, the common structure or the common ending. If the shape of the text is the shape most texts use, change the shape, but only inside the length and format the user set.

These are the marks of default AI text. Do not use them:

- An offer at the end to change, tailor or redo the text, or a note about the text itself, such as its word count or how it was made.
- A bold title, headers or bold labels the user did not ask for.
- A list of features with bullets or emoji where plain sentences would do.
- A closing call to action or a cheer with an exclamation mark.
- A question to the reader that only builds hype.
- Mirrored pairs and slogans built from two matching halves.
- Items that come in threes by habit: three adjectives, three examples, three wishes.
- Set phrases that fit any product or any person, and big claims with nothing behind them.
- Feelings named outright where a detail could show them.
- A last line that sums up, lifts the mood or ties a bow on the text.
- Long, even sentences with the same rhythm from start to end.

Write the text a real person in this situation would write: shorter, built on the real facts of this case, and with an end that just stops.

This list covers the marks that come from picking the default. To clean the rest of the AI marks from a finished text, run a separate editing pass or a text cleanup skill if one is installed.

## Visuals

For any visual work, read `visuals.md` in this skill's folder before you start. It covers the look, the method and its marks, the hand in the geometry, interfaces such as app screens and dashboards, and the `rough.py` and `check.py` scripts.

## Ideas, names and design

Do not offer the first idea in a field, the most famous mechanic, or the name made from the two most obvious words. Assume the user already thought of those.

When you give options, make them different in kind, not small variations of one safe idea. One option may be the safe one, but say so, and never make it the only real choice.

Give one recommendation and the reason for it. Do not hide behind a long neutral list.

## The escape becomes a default

This skill makes its own habits. An escape that worked once turns into the new safe pick if you use it again. Watch for these and do not reach for them by reflex:

- An old, analog or printed look chosen because it reads as "not AI", not because the subject asks for it.
- The same small palette, the same paper, the same texture, the same wobbly line from one piece to the next.
- Made-up names that all come from one stock: sea and tide words, old trades, rope and salt, small English towns. Take names from the way the people who live there name things, not from a list of objects found in the place.
- A cream, beige or off-white ground. Take the ground from the subject: its night, its wall, its water, its screen.
- Exact times, dates and numbers used only to look concrete.
- A clever frame borrowed from another domain, such as a table, a map, a form or a schedule, laid over the subject.
- A small numbered label in the corner and a dry joke in the fine print.
- A small town, a named craftsman, a quiet magic rule and an odd object in the last line.

If your answer shares its main move with the last off-default answer you gave, it is a default now. Pick a different kind of move, or keep it only if you can say why this case needs it.

You cannot see past sessions, so the moves are kept in a file. Before you show an off-default answer, run `python3 scripts/moves.py` to list the main moves of recent answers and compare yours with them. After you show it, record its main move in a few plain words: `python3 scripts/moves.py add "poster: x-ray method, deep blue ground, text cut by the edge"`. Name the move, not the project or the user's content.

## Check before showing

Ask three questions about your answer:

1. Could this be the answer to a different project? If yes, it is too general.
2. Is this what most people would make first? If yes, move it.
3. Can I say why this choice fits here, in one sentence, using a fact about this project? If not, the choice has no reason.

Write all text in the work in the language the user wrote in, unless the user's standing rules name another language for that kind of text, such as one fixed language for code, project names, game names or a store page. Those rules win. The seed's setting and region may shape the look and the names of people and places, but dates, times, lineups, buttons, labels and all other words stay in the language chosen this way.

Keep the length and format the user gave. If they asked for four sentences, write four. Do not add notes, options or extra parts they did not ask for.

Do not invent facts to make a text concrete. Use real details from the user or the project. If there are none, ask for them, or keep the detail clearly made up. Add one short sentence saying so only when a made-up fact could pass for a real one and do harm, such as a price, a weight, an ingredient or a claim about the product. A poem or a story needs no such line.

If the user asks for the plain, standard or expected version, give it. This skill is for choices left to you, not for overriding what the user asked for.
