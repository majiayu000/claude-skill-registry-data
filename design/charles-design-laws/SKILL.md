---
name: charles-design-laws
description: "The 20 design laws as one procedure for designing or reviewing a screen or a flow: cut what doesn't help, take work off people, group what belongs together, point the eye at one thing, carry people to the end, then polish. Each law says what people do, what to build and how to check it. Use when designing, building or reviewing a screen or a flow (forms, settings, dashboards, checkout, onboarding), or when a screen feels confusing, cluttered or hard to use. Triggers on: UX laws, laws of UX, design laws, UX review, review my screen, critique this UI, why does this feel confusing, hard to use, aesthetic-usability effect, law of proximity, Von Restorff effect, Zeigarnik effect, Tesler's law, law of Prägnanz, Pragnanz, serial position effect, progressive disclosure, law of common region, goal-gradient effect, law of similarity, recognition over recall, Pareto principle, 80/20, Occam's razor, Parkinson's law, uniform connectedness, paradox of the active user, cognitive load, default effect, peak-end rule."
---

# Goal

A screen or flow people get through without stopping to think: it shows only what their task needs, asks for nothing the app could work out, reads in groups at a glance, puts one thing first, and ends by telling them it worked. Each of the 20 laws below says what people do, what to build because of it, and how to check it, so building a screen and reviewing one walk the same steps.

The laws are as Jon Yablonski's Laws of UX states them, plus three from elsewhere: progressive disclosure (Jakob Nielsen), recognition over recall (Laws of UX's page on working memory, and Nielsen's sixth usability heuristic) and the default effect (Johnson and Goldstein, 2003). Motion, target sizes, how many choices to offer, chunking, conventions, messy input and response times are outside these 20 laws (charles-ux-animation covers them with Fitts's, Hick's, Miller's, Jakob's and Postel's laws and the Doherty threshold), so a problem there goes in the list of problems no law covers.

# Steps

Walk steps 1 to 8 in order, every time. Each step works on what the one before it left: decide what's on the screen and what it asks of people before arranging it, arrange it before choosing what stands out, make each screen work before the flow across screens, and polish last. A later step never rescues an earlier one: a polished screen nobody can finish is still a screen nobody can finish. For a flow, run steps 2 to 5 on each screen, then step 6 across the whole flow.

Run every check on the rendered screen at the width most people use it at (a 390 × 844 px phone when you don't know), then re-run only the layout checks (Pareto, proximity, Von Restorff, the five-second look) at any other width it supports. The five-second look and "the place people look first" judge the first screenful. Judge layout and looks on the render, and behaviour (what a button does, what's saved, autofill hints) in the code. Each step says what it applies to; skip a law nothing in scope can trigger. In a build, a failed check means fix it and check again, and anything the request asked for gets built even when a law argues against it: build it, and name the law it breaks in what you deliver.

Reviewing instead? Change nothing, and walk the same steps. Every failed check and every broken Build rule is a finding. Later steps check what earlier findings would leave, so skip anything an earlier finding removes. Write each problem once, under the law whose rule names it (a tour goes under the paradox of the active user, not Occam's razor); when two laws name it, use the one in the earlier step. When a later finding removes something an earlier row fixed, drop the earlier row. Report the way Deliver says.

## 1. Name the job

Before changing or judging anything, write down:

- **The job:** what the screen or flow is for, in one sentence.
- **The tasks:** what people come to do, most-used first. Rank from usage data when there is any (analytics, logs, the product's own counts); otherwise rank from the product's core task, and say that's what you did. Mark every task you inferred, rather than read on the screen or were told, with "(assumed)". The business's own goals for the screen (a marketing opt-in, an upsell) are tasks too: ranked below everything people came to do, kept in view, and never the one thing that stands out.
- **The inventory:** every element on the screen, every question it asks people (each field, choice and setting), and every step of the flow.
- **What's missing:** walk each task from start to finish against the inventory, and list anything it needs that isn't there (a field, a way to pay, a way back). Each missing piece is a **broken** finding.

Why: every law below is judged against a task. "Doesn't help", "most important" and "what's left" mean nothing until the tasks are written down, and steps 2 and 3 walk the inventory item by item. Every tree below walks what's on the screen, so a missing piece only shows up if you look for it here.

## 2. Cut what doesn't help

The Pareto principle ranks the inventory, Occam's razor and progressive disclosure decide what stays in view, cognitive load removes the decoding, and the law of Prägnanz simplifies what's left. Walk every item through this tree first:

```
Does a task on the list need it?
├── No → delete it (Occam's razor).
└── Yes → Do most people need it on most visits?
    ├── Yes → keep it in view, sized and placed by its rank (Pareto principle).
    └── No → put it behind one row that opens in place (progressive disclosure).
```

These always stay in view, whatever the tree says: what people need before they commit (a price, a fee, a required field, what a delete removes), the ways back and to help (Back, Cancel, Help), and the business's goals from step 1.

### Pareto principle

- **People:** use is uneven: roughly 80% of it comes from about 20% of the features.
- **Build:** rank the actions by use. The top fifth (at least one) gets the largest size, the place people look first and the default; the rest shrink, group into one menu or move a level down. Design and polish in rank order too, because effort spread evenly mostly lands where few people look.
- **Check:** list the actions from most to least prominent (size first, then position). The order matches the use rank, and a rarely used action as big or as high as the top one is a finding.

### Occam's razor

- **People:** read, judge and skip every part on a screen, so of two designs that work equally well, the one with fewer parts is easier to use.
- **Build:** never add an element no task needs. For each element already there, ask what breaks if it's gone: "nothing" means delete it, and "it adds interest" or "it fills space" counts as nothing. The usual extras: an eyebrow or badge above a headline, an icon beside every label, a second button that repeats the first, a caption that restates its heading, decorative avatars and ticks. The screen is done when nothing else can go.
- **Check:** cover each element in turn (on the screenshot, or by hiding it in code). If every task still works and reads as clearly, it goes. Walk the screen twice, because one cut exposes the next.

### Progressive disclosure

- **People:** learn a screen faster and make fewer mistakes when it shows the few options most of them need, and the rest only when they ask.
- **Build:** the first view holds everything most people need on most visits. The rest goes behind one row that opens in place, so people keep what they've entered and where they are, and the row is named for what it holds ("Add a coupon"; "More options" only for a mix). A follow-up field appears only after the answer that needs it (the company name after "Business account"). Never more than two levels, because people get lost moving between deeper ones. Never hide what people need before they commit: a cost found after the click reads as a trick.
- **Check:** each control in view is used on most visits, and each one behind the disclosure isn't. Open the disclosure: it expands in place, and nothing inside it opens a third level.

### Cognitive load

- **People:** spend mental effort on every element, and when a screen asks for more than they can hold, they slow down, miss details and feel overwhelmed.
- **Build:** remove every bit of work that doesn't help the task. Label lines and slices on the chart itself, never with a legend people match by colour. Show names, not codes ("Visa ending 4021", not a card ID), and put units beside values. Icon-only buttons are only for icons everyone reads the same way (search, close, back); every other icon gets a text label. One primary task per screen: a second task gets its own screen or its own region, because two tasks compete for the same attention.
- **Check:** ask the screen's main question (Which line is Web? What do I owe? Where's my order?) and trace the eye to the answer. Every trip away from the content and back (to a legend, a key, a footnote, a tooltip) is load to remove.

### Law of Prägnanz

- **People:** read a complex or ambiguous image as the simplest form they can, because that takes the least effort, and they process and remember simple figures better than complex ones.
- **Build:** draw every chart, icon and card in its simplest form. Charts are flat: no 3D, perspective, exploded slices or gradient fills. A card has one edge (a border or a 1px shadow ring, never both) and casts what reads as one shadow: soft layers that blend into one are fine, but never a second offset or coloured shadow, a glow, an outline or a gradient on top. Icons come from one set, at one stroke weight. Shapes repeat: one corner radius per element size, equal gaps, aligned edges.
- **Check:** describe each chart, icon and card in one short sentence of shapes ("a flat donut in three blues", "a white card with a thin border"). If the sentence needs "3D", "glow", "a coloured shadow" or "a second shadow", simplify until it doesn't.

## 3. Take work off people

Applies to every screen that asks people anything or has to teach them anything. Tesler's law decides who answers each question in the inventory, the default effect picks what's preselected, recognition over recall replaces memory with something to pick, the paradox of the active user moves teaching to the point of use, and Parkinson's law makes the task shorter than people expect. Anything this step adds (a hint, a list of recents) goes back through step 2's tree.

### Tesler's law

- **People:** carry whatever complexity the product doesn't. Every task has some that can't be removed, only moved, and Larry Tesler's case was that one engineer spending an extra week beats millions of people each spending an extra minute.
- **Build:** walk every question still in the inventory after step 2 through this tree:

```
Can the app already know the answer (the account, the device's time zone and locale, an earlier answer)?
├── Yes → fill it in, shown and editable. Never ask.
└── No → Can it work the answer out from something people give (the city from a postcode, the card type from its first digits)?
    ├── Yes → ask only for that one thing, and fill in the rest.
    └── No → Do most people give the same answer, and does a wrong guess cost nothing?
        ├── Yes → preselect it (default effect, below).
        └── No → ask, with a control that holds the format (a date picker, a searchable list),
                 never a format people type to match ("YYYY-MM-DD").
```

- **Check:** mark every question left after step 2 known, worked out, preselected or asked. Every "asked" has a reason the app can't know it.

### Default effect

- **People:** keep whatever is already selected, so the default is the choice most people end up with. Johnson and Goldstein (2003) found organ-donor consent far higher in countries where donating was the default.
- **Build:** preselect the option that's best for most people (free standard shipping, today in a date picker). Never preselect anything that costs money, shares data or signs people up (an upgrade, an add-on, marketing email, tracking): those default to the free, private, off choice, because a costly default gets accepted unseen and found on the bill, which makes every other default suspect, and under the GDPR a pre-ticked box isn't consent. When the right answer depends on the person and a wrong guess costs them (a size, a recipient, a dose), preselect nothing.
- **Check:** list every choice with its default. Each is the best option for most people, the free, private or off option, or empty because it depends on the person.

### Recognition over recall

- **People:** recognize what's on screen far more easily than they recall it, because working memory holds about 4 to 7 chunks and each fades within about 20 to 30 seconds.
- **Build:** a search box opens on up to 5 recent searches or suggestions before people type. A picker puts recently used items first. Up to 5 choices show as visible options (radio buttons, a segmented control), never a blank field to type into or a closed dropdown. Visited links look visited, and deep pages show where people are (breadcrumbs). Never make people carry a value from one screen to the next: show it where it's needed (the plan and price on the confirm step, the code beside the field that wants it).
- **Check:** find every place people type from memory (an empty search, someone else's name, a code, something from an earlier screen). Each offers recents, suggestions or the value itself on screen.

### Paradox of the active user

- **People:** skip manuals, tours and tutorials and start using the product at once, because they want the task in front of them done, even when learning first would save them time.
- **Build:** no tour, carousel, tutorial or manual before the first action. Teach at the point of use: a one-line hint beside the control it explains ("Tap + to add a task"), shown until people first use that control and then gone, since a lesson already learned is clutter. An empty state says what to do first and offers it as a button. Help people go looking for (docs, a help centre, a ? beside a hard field) stays one tap away and never covers the screen.
- **Check:** open the product as a new person. You can act on the first screen at once, nothing blocks it to explain, and every control whose use isn't clear from its label has its hint beside it.

### Parkinson's law

- **People:** let a task stretch to fill the time it's given, and feel better about one that finishes sooner than they expected.
- **Build:** every field carries its autofill hint so the system fills it (`autocomplete` on the web, `textContentType` on iOS, `autofillHints` on Android), return visits reuse saved details (address, payment), and the common answer is one tap. A long task (setup, a long form) says how long it takes before it starts ("About 2 minutes") and finishes inside that. When the product sets a time box for people's work (a meeting, a focus session, a deadline), the default is the short one: 25-minute meetings, not an hour.
- **Check:** do the task as a returning person. Everything the browser or the account knows is already filled in, and it finishes inside the time the screen promised.

## 4. Group what belongs together

Applies to every screen with more than one group. Mark the groups first, from the tasks (contact details and address; text style and alignment), then give each one the lightest signal that shows it, because every box and line is one more shape to read before the content:

```
Can space alone show the group?
├── Yes → proximity. No box, no line.
└── No (a dense toolbar, a group among unrelated items, a group people act on as one: a card they tap, drag or dismiss)
    ├── The members sit together → one shared background or border (common region).
    └── The members are a sequence or far apart (order steps, a timeline, a label and its point)
        → join them with a line (uniform connectedness).
Then, across the whole screen: same job, same look (similarity).
```

### Law of proximity

- **People:** see things placed near each other as a group, and assume they share a purpose.
- **Build:** the gap between groups is at least twice the largest gap inside one. A label sits closer to its own field than to the field above it. A list that holds two groups is never evenly spaced.
- **Check:** measure the gaps on the rendered screen (DevTools, or pixels on a screenshot). Every gap between groups is at least 2× the gaps inside them, and every label is nearer its own field.

### Law of common region

- **People:** see elements inside one clearly bounded area (a shared background or a border) as a group.
- **Build:** when space can't show a group, put it on one background or inside one border: a tinted segment behind related toolbar buttons, a card around one settings section. One region holds one group, never two unrelated ones. Never put a region inside a region inside a region: by the third boundary nobody can tell which box a control belongs to.
- **Check:** name the group each region holds in two words. If you can't, or the name covers two things, split the region or remove it. A group that space already shows has no region.

### Law of uniform connectedness

- **People:** see elements joined by a line or a frame as more related than elements with no connection.
- **Build:** join the steps of a sequence (an order tracker, a checkout, a setup checklist, a timeline) with one line, filled up to the current step. Tie a label to a far-off point with a leader line instead of trusting position. Never draw a line between unrelated things, because a decorative line reads as a relationship.
- **Check:** every sequence on the screen is joined, and every line or arrow joins things that are related.

### Law of similarity

- **People:** see elements that look alike as related and expect them to work alike, even when they're far apart.
- **Build:** give each role one look and use it everywhere: one style for every secondary action, one link style that body text never uses, one style for every destructive action, one anatomy for every card of a type. Things that work differently look different: a link or a tag never looks like a button.
- **Check:** list each role on the screen (primary action, secondary action, link, destructive action, tag, each card type) with the styles it appears in. Every role has exactly one style, and no two roles share one.

## 5. Point the eye at one thing

Applies to every screen, menu and list.

### Von Restorff effect

- **People:** notice and remember the one item that differs from the similar items around it.
- **Build:** exactly one element per view breaks the pattern: the top-ranked action from step 2, in the one accent colour. Never two, because two standouts compete and neither wins. Pair the colour with a second difference (size, weight, fill or position), because colour alone fails people with colour blindness or low vision. Keep it inside the content it belongs to, never in a banner strip or a side box, where people skip it as an ad. If motion makes the difference, it stops under reduced motion and the element still stands out.
- **Check:** shrink the screenshot to a quarter of its width, or blur it, then view it in greyscale. Exactly one thing stands out, it's the primary action, and it still stands out without colour. Check each view on its own: the screen, and any dialog or overlay over it.

### Serial position effect

- **People:** remember the first and last items of a series best and the middle ones least.
- **Build:** in every nav, tab bar, menu and list you order by hand, the most important items go first and last and the least-used go in the middle (the core task first, the next most-used last, settings and rarely used items between them). A list sorted by data (date, name, price) keeps its sort, because people scan it by that key. Every screen opens with what it's for.
- **Check:** read each hand-ordered list from first to last. The two ends hold the two most important items, and nothing important sits in the middle third.

## 6. Carry people to the end

Applies to any task that takes more than one step or one visit (onboarding, checkout, setup, a profile to fill in, a loyalty card), and to every flow that ends on a result.

### Goal-gradient effect

- **People:** speed up as they get closer to a goal, and a head start counts: in Kivetz, Urminsky and Zheng's 2006 café study, a 12-stamp coffee card that came with 2 free stamps was filled faster than a blank 10-stamp card, though both needed 10 coffees.
- **Build:** every step shows how far along people are and what's left, as a count ("Step 2 of 4", "1 more for a free coffee") or a bar. Count work already done: a step the person or the product finished (creating the account) shows as done, and progress never reads zero once they've started. The head start is real (a finished step, a free stamp), and progress never goes backward, because a drop reads as lost work.
- **Check:** walk the task. Every step shows where you are and what's left, and the first screen after any action shows progress above zero.

### Zeigarnik effect

- **People:** remember unfinished or interrupted tasks better than finished ones.
- **Build:** when a task has separate parts (setup, a profile, a course), show them as open items: a checklist with what's done ticked and the rest left open ("Add a product", "Connect payments"), never a plain list that hides what's left. Every task, a single form included, saves progress as people go and on return opens where they stopped ("Continue setting up your shop"). When there's more than fits, show that more exists (a cut-off last row, "12 more"). Once every item is done, the checklist goes away, because a finished list left on screen is clutter.
- **Check:** leave a task halfway and come back in a new session. It opens where you stopped, with what's left listed as open items.

### Peak-end rule

- **People:** judge an experience mostly by how it felt at its most intense moment and at its end, not by the average of every moment, and remember bad moments more vividly than good ones.
- **Build:** end every flow on a success screen that says what happened, with the specifics ("$240 sent to Sam Lee"), what happens next, and one action to move on. Never end on a bare redirect, or on a toast that fades over the page people started from. Give the flow's peak (the moment the product delivers: the first result, the payment going through) the most care. Fix the worst moment (an error, a long wait, a confusing step) before polishing an average one. Celebrate (confetti, a sound) only a real milestone like a first success, because if everything celebrates, nothing does; a routine finish gets a quiet confirmation.
- **Check:** read the last screen of each flow on its own: it says what happened and what's next. Name the flow's worst moment: it's fixed or it's a finding.

## 7. Polish last

### Aesthetic-usability effect

- **People:** see a good-looking interface as easier to use and forgive its small flaws, which also means good looks hide usability problems, in testing too.
- **Build:** once steps 2 to 6 hold, polish everything people see. No browser default reaches the screen (a system serif, a grey bevelled button, an unstyled select). Type, spacing, corner radii and colours come from one set of tokens. Every control has its hover, focus, pressed, disabled and loading states. Replace the default focus ring with a designed one and never remove it, because keyboard users lose their place.
- **Check:** judge steps 2 to 6 before the looks, and never let polish pass a screen they failed. After polishing, no browser default is left and every control has every state.

## 8. Verify

The checks above each test one law. These three catch what falls between them:

- [ ] **Five seconds:** look at the screen for 5 seconds, then away. You can name its job and its one primary action.
- [ ] **New person:** finish each task on the list as someone who has never seen the product. Count what you typed, chose and had to remember; each one is a finding unless a law above says it has to stay.
- [ ] **Leave and return:** quit a flow halfway and come back. You land where you stopped.

When you can't render the screen, don't build an app to render it: list the checks you couldn't run and what each would catch.

# Deliver

**Building:** the changed screen or flow, then one line for each law that changed something (the law, and what changed), anything you built on request that breaks a law (the law, and why it matters), then the checks you ran with their results, and the ones you couldn't run.

**Reviewing:** open with the job and the tasks from step 1, then what's missing (each piece is **broken**, so it comes before everything else), then one line naming the flow's worst moment. Then one table row per fix; when one change fixes several elements under one law (cut the eyebrow, the emoji and the caption), they share a row:

| Severity | Law | Where | Before | After |
| --- | --- | --- | --- | --- |
| broken | Default effect | Shipping step, `ShippingOptions.tsx:42` | Express ($9) is preselected | Standard (free) is preselected; Express stays one tap away |

Severity is **broken** (a task fails or ends wrong: something it needs is missing, people can't find the primary action, pick the wrong thing, lose what they entered to an error or a reload, or pay or share data through a default they didn't choose), **friction** (it works, but it's slower, harder or more confusing than it needs to be, including anything that pulls attention off the task: a banner, motion, a second accent) or **polish** (only the looks, including small decoration that sits still, like an emoji on a label). Sort by severity; within a severity, a problem on a higher-ranked task comes first. After the table: the problems no law covers (a failed step 8 check that no row explains goes here), then the checks you couldn't run. If the request named a symptom (people drop off, it feels confusing), end with one line naming the missing pieces and rows that most likely cause it.
