---
name: swipe-deck
description: Runs a Tinder-style swipe interview to pull requirements out of someone's head. Claude generates a deep pool of question cards, the user swipes right/left/up/down (yes / no / absolutely / not sure), the deck reshapes itself around every swipe, and it ends in a written brief once a saturation meter fills. Use this whenever a request is vague, broad, or taste-dependent and you would otherwise fire off a list of clarifying questions — kicking off a project, scoping a build, planning a trip or event, choosing a direction, naming something, deciding what to eat, or any "help me figure out what I want". Trigger on "swipe", "swipe deck", "tinder style", "interview me", "ask me questions", "quiz me", "20 questions me", "figure out what I want", "get it out of my head". Also reach for it proactively any time you catch yourself about to ask more than three clarifying questions in a row, or when someone says a batch of questions felt like a chore or a form.
---

# Swipe Deck

## Why swipes instead of questions

People recognize what they want long before they can articulate it. Ask someone "what should this look like?" and you get a shrug; show them a thing and they know in half a second whether it's right. A swipe deck trades articulation for recognition, which is why it gets more out of someone in 40 seconds than a clarifying-question list gets in five minutes.

Two consequences worth holding onto:

- **A "no" is worth as much as a "yes."** Rejections carve the shape of what someone wants faster than confirmations do. A deck where everything gets swiped right taught you nothing.
- **Gut reactions beat considered answers.** The card has to be readable and reactable in about one second. The moment someone has to think about how to interpret a card, you've lost the advantage and you're just running a slow form.

## One deck, not rounds

**This is a single continuous deck.** Not a series of rounds, not batches, not "deck 1 / deck 2". The person swipes until the meter fills or they tap out, and they should never see a seam — no round counter, no interstitial, no message from you in the middle telling them what you've learned so far. Every one of those things breaks the flow and turns a swipe session back into a form with extra steps.

That means the pool has to outlast them: **70 to 110 cards.** Size it to how well you think you know this person, not to the topic — someone you're modelling well fills the meter in around 35 swipes, someone who keeps surprising you can burn 60+ and still not get there. When in doubt, build bigger; unused cards cost you nothing and running dry mid-session is the one failure they actually see.

The deck re-ranks itself locally after every swipe, so the cards it surfaces are chosen by their answers even though the pool was written up front. That local reshaping is what buys you the right to write everything in advance.

Only one thing ever comes back to you: a single message when swiping ends. Then you write the brief.

If someone genuinely out-swipes a 100-card pool before the meter fills, you'll get a request for more. When that happens, **reply with nothing but the widget** — no preamble, no "here's what I'm hearing", no recap. Any sentence you write there is a visible seam in something that's supposed to feel continuous.

**0 — Mine the prompt first.** Whatever the user already told you is not a question anymore. If they said "a landing page for my gym," you do not have a card asking whether it's a landing page. The prompt should kill a third of your candidate cards before you write any. Cards that re-ask known facts are the fastest way to make this feel like a form.

**1 — Name the facets.** Pick the 5–7 dimensions that actually matter for *this* topic and name them in the topic's own vocabulary. `references/question-craft.md` has the lens set and worked examples. Facets drive the coverage meter the user sees, so they should read like plain nouns: `budget`, `vibe`, `who it's for` — not `dimension_3`.

**2 — Build the pool** — 60–100 cards. Every facet gets a full ladder: several broad `depth: 1` cards, then `depth: 2` and `depth: 3` cards underneath them for when that facet turns out to be where the heat is. The engine surfaces the deep ones only if the shallow ones land, so writing them costs you nothing when they aren't needed. Then:

```
Read assets/deck.html, replace __DECK_JSON__ with your deck JSON,
pass the whole file as show_widget's widget_code.
```

Emit the template **verbatim** and change only the JSON. Do not rewrite the swipe physics, restyle the deck, or "improve" the markup — you would spend a thousand-plus tokens re-deriving a solved problem, and the message format the loop depends on lives in that file.

**3 — They swipe, you wait.** Say nothing while it's running. The widget stops itself the moment the meter fills and sends you one `SWIPE DECK` message with everything. It also stops on `→ STOP` if they hit "That's enough".

**4 — Write the brief** from that message, then **ask before acting on it.** That's the whole loop — one widget out, one message back, one brief.

**The exception:** if the pool runs low before the meter fills, the message ends with *"Send ONE more batch of 60+ cards, no announcement, no recap."* Do exactly that — a bare widget, zero prose. Copy the `carry` block from the message verbatim into the new deck, because the meter resets to zero without it:

```json
"carry": { "swiped": 64, "hits": 41, "decided": 58, "deep": 27,
           "coverage": {"budget": 3, "vibe": 4} }
```

A short `SWIPE DECK — N more cards swiped` message may also arrive afterward with the last few cards. **That one never gets a widget** — just fold it into what you're writing.

### Deck JSON

```json
{
  "topic": "your client dashboard",
  "facets": ["outcome", "form", "scope", "budget", "vibe", "dealbreakers"],
  "carry": { "swiped": 0, "hits": 0, "decided": 0, "deep": 0, "coverage": {} },
  "cards": [
    { "id": "sc1", "q": "One page is enough to start",
      "facet": "scope", "depth": 1, "style": "preference", "predict": "yes" },
    { "id": "sc2", "q": "Per-client custom views on day one",
      "facet": "scope", "depth": 2, "style": "provocation", "needs": "sc1",
      "hint": "meaningfully more work", "predict": "no" }
  ]
}
```

`id` unique · `q` the card text · `facet` one of your named facets · `depth` 1 broad → 3 niche · `style` see question-craft · `hint` optional one-line clarifier · `needs` optional card id that must not be swiped left for this card to stay in the deck.

**`predict` is how the meter works, so it is not optional.** Before sending each card, commit to how you think they'll swipe it — `yes`, `no`, `hot`, `narrow`, or omit it entirely when you genuinely have no idea. The deck scores you against reality on every swipe, and the meter only fills once you've stopped being wrong. Guessing "yes" on everything to make the number go up defeats the entire mechanism and produces a confident brief about nothing. Predict honestly; being wrong is useful, it's what keeps the deck running.

`topic` shows up in the handoff message and the closing card — write it as the user would say it.

One escaping rule: if any card text needs a literal `</`, write it `<\/` in the JSON. A raw `</script>` truncates the embedded data block and the deck arrives empty. The widget detects this and asks you to re-emit, but it costs a round trip.

The deck reorders itself locally as the user swipes — this is what makes a pre-written pool feel responsive. An *absolutely* pulls the deeper cards in that facet forward, a *no* prunes the branch, a *not sure* reaches for the more concrete card underneath, and a rotation guard stops it tunnelling. Your authored order only breaks ties, so put the most important card first.

## Reading verdicts

You aren't generating a follow-up deck, so this table does two jobs: it tells you what the engine will do live, and it tells you how to read the final message when you write the brief.

| Swipe | Means | Engine response | Build the pool so that… |
|---|---|---|---|
| **→ yes** | Right direction | Mild nudge toward that facet | …a confirmation has somewhere to go, but doesn't dominate |
| **↑ absolutely** | You hit the vein | Pulls deeper cards in that facet forward | …every facet has depth-2 and depth-3 cards waiting underneath, each more committing than the last. The edge where it stops being true is the real answer |
| **← no** | Wrong direction | Prunes cards wired to it via `needs`, cools the facet | …the branch actually dies. Wire genuine dependents with `needs`, and include the opposite-direction card so there's somewhere to land |
| **↓ not sure** | Too broad to react to | Reaches for the more concrete card in that facet | …every abstract card has a specific instance sitting below it. A vague card with nothing underneath is a dead end |

Two signals outrank everything else in the message, because both mean someone stopped swiping to type:

- **An edited card** (the `EDITED CARDS` section). They tapped a word, rewrote it, and answered *their* version — "Under $5k" became "Under $15k", then YES. The rewrite is a correction of your assumption and the swipe is their answer to the corrected statement. Build the brief on their wording, never yours, and note that the widget already counted your prediction on that card as a miss — an edit is by definition a surprise.
- **A note** (the `NOTES` section). A direct statement. Act on it and quote it in the brief.

Contradictions are information, not noise. If someone swipes up on "ship it in three weeks" and up on "it should feel handcrafted," don't average them — write a card that forces the tradeoff and see which way it falls.

## Writing cards

Two references carry the detail. Read **`references/question-craft.md`** before building deck 1 — it has the facet lens set, the eight card styles, deck composition ratios, and a table of weak cards rewritten into strong ones. Read **`references/worked-example.md`** if you haven't run this loop before — it's one complete trace from a vague prompt through two decks to the finished brief, including how to reason from a handoff message to the next deck.

The rules that matter most:

- **One idea per card.** No "and", no "or". A compound card makes the swipe unreadable — you won't know which half they meant.
- **Statements, not questions.** "You'd rather ship rough in three weeks" swipes better than "Would you rather ship rough in three weeks?" The gesture supplies the verb; a question mark makes people pause to parse.
- **Twelve words or fewer.** If it needs a second line to make sense, it's two cards or it belongs in `hint`.
- **Concrete beats abstract.** "Under $5k" beats "budget-conscious." "Like Linear's onboarding" beats "clean and modern."
- **Half the deck should be capable of a no.** Write cards you genuinely expect to be rejected. If you can predict every swipe, the deck is decoration.
- **Never ask for a number** — offer a threshold to react to. They can tap the number and counter-offer their own ("$5k" → "$15k"), which is exactly the answer you wanted, so make thresholds concrete enough to be worth correcting.
- **Spread the facets.** Every facet gets a card in deck 1; no facet gets more than three cards in one deck. Tunnel vision on one dimension is the most common way this goes wrong.

## Knowing when to stop

**There is no card count and no ceiling. The deck runs until the meter fills or the user stops it.** Twelve questions is not an interview, it's a form. Build the pool deep enough that running out is the unlikely case, not the expected one.

The meter is computed by the widget, not by you, and the user can watch it move. It blends three things:

- **Coverage** — how many facets have at least three decisive swipes. A facet you never asked about holds the meter under 70% no matter what else is true.
- **Predictability** — how often your `predict` values matched the actual swipe. This is the heart of it: while the user is still surprising you, there is by definition more to learn.
- **Depth** — what share of swipes were on depth-2+ cards. All-surface swiping doesn't count as knowing someone.

The closing message reports the meter and its parts, and tells you plainly whether to write the brief or send more cards. Trust it over your own sense of being finished — the whole point of measuring is that "I think I understand" arrives well before understanding does.

Two things end the loop early, both legitimate:

- **`→ STOP`** — the user hit "That's enough". Stop immediately and write the brief from whatever you have, and be honest in it about what's still thin.
- **A stalled meter.** If a second full pool barely moves it, swiping has stopped paying. Say so plainly, name the one or two things still unresolved, and ask them directly in plain text. That's not giving up — it's recognizing that the remaining uncertainty isn't the kind a swipe can resolve.

Never pad the pool with cards you don't care about. Filler makes the meter lie — a run of unanimous yeses raises predictability without teaching you anything, and you'll end up writing a confident brief about nothing.

## The brief

When swiping ends, write it up. Structure:

```
# [Thing] — what you actually want

**The shape of it** — two or three sentences a stranger could act on

**Locked in** — from absolutelys and consistent yeses

**Ruled out** — from the nos, and worth stating because it saves work later

**Still fuzzy** — where signal was thin or contradictory, and what would settle it

**The tension I'm reading** — where answers pulled against each other, and my call on it

**First thing I'd do** — one concrete next step
```

Then stop and ask whether to proceed. Do not start building.

One honesty rule: the brief must not launder your guesses as their answers. Anything you inferred rather than saw swiped either goes under "Still fuzzy" or gets marked as your inference. The whole value of the deck is that the brief is *evidence-backed* — quietly padding it with assumptions destroys that.

## If the widget isn't available

If `show_widget` isn't there, the loop still works — run it in chat as a numbered list of the same cards and ask the user to reply with e.g. `1r 3l 5u 7d` (right/left/up/down, unswiped = skipped). Same facets, same verdict semantics, same stopping test. The template also degrades on its own: if `sendPrompt` is missing it shows a copy box with the handoff text.

## Failure modes

- **Rewriting the template.** Costs a thousand-plus tokens and breaks the message format the loop depends on. Read the file, swap the JSON.
- **Talking between batches.** If a refill is requested, send the widget and nothing else. A sentence of commentary there is the seam the whole design exists to hide.
- **Answering a trailing-cards message with a widget.** They get a second deck and lose their place.
- **Drifting back into chat questions** while a deck is live. Pick one channel.
- **A deck of soft yeses.** Nothing was learned. Add provocations and anti-goals.
- **Ignoring the notes and edits** because they're at the bottom of the message. They're the best data in it — and briefing from your original card text when the user rewrote it puts words in their mouth.
- **A pool that's too small.** Under ~70 cards the deck runs dry mid-session and the person sees the seam. That is the single most common way this feels wrong.
