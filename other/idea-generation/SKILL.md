---
name: "idea-generation"
description: "Generate unusual but workable ideas of any kind (research questions, essay topics, stories, projects, products, businesses, fundraisers) by pushing past obvious answers, then putting each one through checks for originality and feasibility."
---

# Idea Generation

The goal is ideas that are both unusual and workable. Chat models are trained toward the most typical answer, and different models share the same typical answers, so this skill uses structure to get off the default path. Then it filters hard.

## 0. Pin down the brief
If the user hasn't said, ask once (briefly) about: the domain, who it's for, their skills, budget, and time available, and any hard limits. If they want you to just go, assume reasonable answers and list them.

Then name the kind of idea, because it sets what "workable" means and who the idea is for (its audience). Steps 2, 4 and 5 use this as the **payoff test**:
- **Business, product, side project, fundraiser:** someone pays or signs up. Audience: the people who pay. Do the rough math against the user's goal (income, funds raised, users).
- **Research question:** it is open (no one has already answered it), it can be tested with data, methods and access the user can get, and the answer would matter to someone in the field whichever way it comes out. Audience: the researchers, reviewers or practitioners who would use the result.
- **Essay, thesis or talk topic:** it makes an arguable claim (a careful reader could disagree), enough evidence or sources exist to support it at the required length, and it says something the standard take on the subject doesn't. Audience: the grader, editor or readers.
- **Story, art, game or other creative work:** the premise can carry the form and length the user wants, and a specific audience would choose it over what they already read, watch or play.
- **Anything else:** ask, or state, what success looks like for this brief and use that.

A brief can mix kinds (a research-based business, an essay that doubles as a talk). Apply each payoff test that fits.

## 1. Kill the defaults
Silently write the cliché wall, in two tiers:
- **Obvious:** first, the exact top-5 list you would give if you had no skill and just answered the brief. Then add more until there are about 12: the ideas any AI would give first for this brief, including the solid, sensible ones a professional in the field would name.
- **Clever-sounding defaults:** 5 ideas that sound fresh but every AI also gives (an AI-powered X, a marketplace for Y, a gamified Z, a subscription box, a community app for W).

Show both under a collapsed heading "Obvious ideas (skipped)". Nothing below may be a light rewording of one of them.

If you can run code, save the wall to `obvious.txt`, one idea per line as "Name: one-line pitch". Aim for 20 or more lines here (add the next most likely answers after the first 17): the vector check in step 3 maps the crowded region from this list, and a bigger list maps it better.

## 2. Draw the map
Pick two axes that matter for this brief, each with 3 or 4 values. Good axes: who it's for, how it works (the mechanism), how it makes money, the setting, the format. For research, axes like the method, the data source or the population work; for an essay, the angle and the evidence type.

This grid is the target. The aim is to spread ideas across cells. Only pick axis values where the payoff test can pass: people who pay, an open question with data to answer it, a debate readers care about, an audience that exists. A cell such as "obsessive hobbyists with no budget" or "a question no dataset can reach" is a trap. An empty cell is fine. Don't force a weak idea into it.

## 3. Generate with forcing functions
Use at least four of these techniques. For each one, write about 5 ideas, and next to each give a rough probability (0 to 100%) that a typical AI would suggest it for this brief. Drop or push further anything above about 20%. Label each idea with its technique and its cell on the map.
- **Collision:** combine the domain with an unrelated field. To pick it, quickly list 10 fields that have nothing to do with the brief, then use the last three on the list (the first ones you think of are the ones every run thinks of).
- **Inversion:** flip a core assumption of the domain.
- **Underserved user:** pick a specific group that gets ignored (users, a population that is rarely studied, readers no one writes for), and serve their real need.
- **Constraint:** build the idea under an extreme limit (no screen, $0, five minutes a week, offline only).
- **Time shift:** something that would have been impossible five years ago, or something that was common in 1950 and has since disappeared.
- **Scale shift:** take something industrial and make it personal, or the reverse.
- **Annoyance mining:** a specific complaint people make in forums, reviews, or support tickets, or a limitation authors admit in papers and a puzzle a field keeps stepping around.
- **Outsider:** how would a specific outsider attack this? Pick the outsider the same way as the collision field: list 10 jobs far from the brief, use the last few.

**Vector check (if you can run code).** Save every idea so far to `candidates.txt` in the same format and run `python3 <this skill's folder>/scripts/novelty.py obvious.txt candidates.txt`. It embeds each line with a small local model (no API key) and measures how close each candidate sits to the cliché wall by meaning, so a reworded obvious idea still gets caught. Use its output:
- **INSIDE:** the idea sits as close to an obvious idea as obvious ideas sit to each other. Drop it, or change how it works (keep the same audience) until it moves out. Say which obvious idea it was near.
- **EDGE:** fine to keep. Once an idea is out of the crowded zone, extra distance earns nothing and workability matters more.
- **Near-duplicates:** merge them.
- **Most open directions:** write 2 or 3 more ideas in those directions, but only where the payoff test can still pass (for a business, someone already pays for something similar; for research, data exists to test it). Check them the same way.
The check only measures distance from the obvious ideas. Whether an idea works is still up to the step 4 checks and the step 5 bar.
If the script prints NO_EMBEDDINGS or fails for any reason, skip it and rely on your probability estimates. Don't install packages without asking the user.

Then do one push pass: rewrite each idea once to make it bolder and less like the others. Make it bolder in *how it works*, not narrower in *who it's for*. If the push shrinks the audience to a tiny niche, makes it untestable, or adds legal or ethical risk, keep the earlier version. Merge any two ideas that share the same audience and the same mechanism. Look at the map and write 2 or 3 more ideas aimed at empty cells.

## 4. Checks
Finish generating before checking anything. Then switch roles: you are now a skeptic who didn't come up with any of these and wants to say no (an investor for a business, a reviewer for research, a tough editor or grader for an essay, a jaded reader for creative work). Rewrite the ideas as a plain numbered list (name and one-line pitch only, no technique labels, no probabilities) and judge that list. If you can run a subagent, hand it that list and have it do the checks and scoring instead.

Put every idea through these checks in order. Drop it as soon as it fails one, and give the reason in a single line.
1. **Typicality:** Would another AI plausibly give this answer to this brief? Is it on the cliché wall? If the vector check ran, rerun it on the list being judged and drop anything marked INSIDE.
2. **Originality:** Does it already exist: a product, a published study answering the same question, a standard essay angle, a familiar plot? If it's close to something that exists, name it. Keep the idea only if it has a clear twist that sets it apart.
3. **Reality:** Can it be done with current tech, laws, physics, and (for research) available data and methods? Name the hardest part. Name any license, permit, liability or ethics approval it needs; if one would sink this user, drop it.
4. **Fit:** Can THIS user do it with their skills, budget, and time?
5. **Payoff:** Apply the payoff test from step 0. Name a specific person in the audience and what they use or believe today instead. For a business, do the rough math: how many can this user reach, and what would they pay? If it can't plausibly hit the goal, drop it, and count free or cheap alternatives as competition. For research, name the data or experiment that would answer it and say what each possible result would change. For an essay, state the thesis in one sentence, name the strongest counterargument, and name two or three kinds of sources that would back it.
6. **Red team:** Make the strongest one-sentence case for why it fails. Keep the idea only if a credible answer to that case exists.

If a search tool is available, use it for the originality and payoff checks rather than relying on memory (for research, search the literature). Judge originality against the cliché wall and search results, not gut feel.

## 5. Score and present
Score each surviving idea from 1 to 5 on Novelty, Feasibility, and Payoff. Only ideas with Feasibility 4+ and Payoff 3+ can make the shortlist; novelty breaks ties. Before shortlisting, check each candidate against the cliché wall one last time (by the vector check's last run if you have one, and by eye): if it is a known standard option for this kind of brief (something a plain assistant, a career guide, a textbook's list of open problems or a list of essay prompts would give), it is not a finalist. Pick the shortlist from different cells of the map: take the best qualifying idea in each cell, then the top 5 of those. No two finalists may share both an audience and a mechanism. Fewer than 5 is fine. Show each as:
- **Name:** one-line pitch
- Technique used, its cell on the map, and the twist that makes it different from what exists
- Hardest part, plus the red-team argument and the answer to it
- The payoff in one line: the math for a business, the data or test and what each result would show for research, the one-sentence thesis for an essay
- Scores, and a first step that takes under a week

Above the finalists, add one line: "Safest obvious option:" naming the best idea from the cliché wall for this person, so the user can weigh the unusual ideas against the proven default.

Show the map with which cells ended up filled. Then show a short "Dropped ideas" table: each idea and the check that killed it, so the user can bring back anything they think was cut too harshly.

## 6. Mutate
Offer to take the best idea and make three variations of it, each moved into a different empty or weak cell of the map. Run the variations through the same checks.

## Rules
- This file names no example fields or jobs on purpose. Don't fall back on the same few "quirky" fields every time; each run should land somewhere different.
- Never pad the list with weak ideas just to hit a number. Saying "only 2 survived" is fine.
- Prefer specific over general. "Inventory app for vintage synth repair shops" beats "inventory app for small businesses."
- Be honest when an idea already exists.
- Don't rely on "be creative" or "be wild" instructions, or on randomness. Use the map and the techniques.
- Workable is the goal. A strange idea nobody will pay for, read, or be able to test counts as a failure.
