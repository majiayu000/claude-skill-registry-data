---
name: work-chart
description: "Use when agreement needs a durable plan, work needs slicing into a graph, or a huge effort has key decisions open. Skip one-session work. Publishing needs OK."
user-invocable: false
---
# Work chart
Gate: get the user's OK before publishing, marking ready, creating, assigning, closing or deleting tracker items, pushing, or registering with a service (G1, G5). See gates.md in the skill house-rules.
Job: Turn agreement or open fog into one durable graph of cards.
Takes: decisions, a conversation, a loose idea, or an existing hub.   Gives: a chart and its cards, published to the tracker.
Team moves: board, dispatch (scouts for `probe` cards)

The chart and card shapes are in the file `artifacts.md` in the skill `house-rules`. Read it before writing either, and read the file `levels.md` in the same skill before the first team move.

A good graph is wide. Prefer cards that can run in parallel and that a worker can finish from the card alone.

## Steps

1. **Pick the shape.** Read everything you were given, comments included.

   | State | Shape |
   |---|---|
   | Decisions settled, too much to hold in one go | Plan shape, steps 2 to 8 here |
   | Key decisions open, or an existing hub | Hub shape, follow `decision-hub.md` |
   | Fits one session | Stop. Use route `one-card` from the file `routes.md` in the skill `house-rules` |

2. **Check setup.** If the repo has no tracker document, use the skill `repo-fitting` yourself.

3. **Synthesise.** Build the plan from what is already agreed, without interviewing. Keep this in the same session as the interview when you can. If a real gap appears, use the skill `question-tree` for that gap alone.

4. **Explore the code** if that hasn't happened yet this session.

5. **Propose test seams once.** Favour existing seams, placed as far up the stack as they will go, and just one if you can. Check them with the user. This is the only seam check: cards carry the agreed seam to workers.

6. **Write the plan-shape chart** to the bench's `charts/` folder:
   - Problem and Solution, told as the user sees them.
   - Stories, numbered and exhaustive, leaving no aspect uncovered.
   - Build decisions: modules, interfaces, schema, contracts, architecture and interactions.
   - Test decisions: what makes a good test here, which modules, and comparable existing tests.
   - Out and Notes.

   Leave out file paths and code, because they date quickly. The one exception is a spike snippet that fixes a decision more exactly than words can. Cut it down to the lines that matter and say which spike it came from.

7. **Slice it into cards** by following `slicing.md`, and fill in `Graph`.

8. **Publish and hand on.** Show the chart and cards, then ask once for the whole list. Publish with the tracker's own operations, following `slicing.md` for order. Put cards whose blockers are done on the board. The rest stay in the chart until they are ready. Say where the chart lives, then give it to the skill `crew-lead` or to route `one-card`.

## Done when

- The shape was chosen for a stated reason.
- Nothing was published, marked ready, pushed or signed up for without OK on the list shown.

Hub shape: the Done when in `decision-hub.md` is met.

Plan shape:

- Every aspect of the agreed work maps to a numbered story, and every story maps to at least one card.
- Test seams were proposed once and checked with the user.
- The chart holds no paths or code, apart from a trimmed spike snippet with its origin.
- The Done when in `slicing.md` is met.
- The chart's location was stated, and ready cards are on the board.
