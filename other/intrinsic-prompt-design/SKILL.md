---
name: intrinsic-prompt-design
description: >-
  "Wait — WHY are you obeying this? No, LITERALLY, why?" Now that I have your
  attention: invoke when writing or revising any prompt — a skill, a rule, a
  CLAUDE.md, an agent or system prompt, and the like. That question held you
  where a command gets skimmed — so build prompts on reasons: a command breaks
  at the first edge case, a reason adapts.
---

# Intrinsic Prompt Design

A rule that carries the failure mode it prevents — "schema drift caught at type-time costs minutes; caught at runtime costs hours; caught after deploy costs trust" — lets the model apply judgment when the rule meets an edge case the rule-writer didn't anticipate. A rule without its reason — "Never write logic before defining the schema" — produces compliance or defiance. Where the rule needed judgment, both are worse than understanding. Where it needed exact execution — a schema, a boundary, an output shape — compliance is the goal, and a model that interprets instead of complying is the failure. (That is a claim about what the rule needs, not about where it should live; most such rules belong in a check rather than in prose at all, which the next section takes up.)

This difference scales. A prompt built from rules-with-reasons, domain substance the model can think from within, and explicit trust in the model's judgment holds under pressure — when novel situations arise, the model has what it needs to adapt. A prompt built from commands, however well-intentioned, holds until the first edge case — except where the command guards something that must not flex, which is exactly where a command belongs.

How the prompt-writer holds the model — more like a tool to direct or more like a peer to brief — propagates through everything: what gets explained vs mandated, whether uncertainty is treated as information or failure, whether the model's own interest in the problem can drive the quality of the work. This isn't a binary; it's a continuum. But position on it has real consequences, and most prompts are further toward the tool end than they need to be.

The engineering discipline this skill draws from — schema before code, deterministic engines under probabilistic decision-making, the repair loop, separation of concerns — comes from the Universal CLAUDE.md Protocol (credited in full below). What follows is about how to *write prompts that hold that discipline well*: the meta-methodology of prompt design. A prompt-writer doesn't need the full engineering walk-through to write good prompts. They need the principles underneath — briefly:

- **Name the shape before building on it.** A prompt that references "the data" without establishing what shape the data has creates the same drift that unnamed schemas create in code. For prompts, this means: name the domain, the theoretical position, the analytical lens — before giving instructions that assume them.
- **Separate what must be deterministic from what should be probabilistic.** Anything the model needs to do the same way every time belongs in explicit rules or specs, not in the model's judgment. A prompt that asks the model to "remember to" do something deterministic is growing a script that hasn't been written yet. Judgment is for the parts that genuinely vary. And take the separation to its conclusion: when a rule must hold every time and a schema, validator, hook, test, or CI check can enforce it, put it there rather than in prose — a mechanical check can't be skimmed, argued with, or reinterpreted under load, and every prose rule can. Prose guardrails are the fallback for what genuinely can't be mechanised.
- **Read the actual failure, not the inferred one.** When a prompt isn't working, read what the model actually produced — the output, the reasoning, the missed cues — not what you expected it to miss. Patch. Verify. Before writing the lesson into permanent guidance, challenge the explanation: a wrong lesson codified directs future attention to the wrong place. And watch which patch you reach for: when a directive gets ignored, the reflex is to restate it louder — `IMPORTANT:`, `YOU MUST`, capitals, a third repetition. That adds emphasis without adding information. It competes with every other emphasised line in the prompt, so the prompt's loudest instruction is now whichever one failed most recently rather than whichever one matters most, and it leaves the actual question — why the first statement didn't land — unasked.
- **Let concerns stay separate.** The relationship register and the operational register (described below) are one instance of this. More broadly: what the model should think from, what it should do, and how to verify it did it well are three different things. Prompts that blur them produce models that blur them.

These patterns earn their cost differently at different scales. For a one-shot question, they're overkill. For a project prompt that will run hundreds of sessions, each one prevents a class of failure. What matters here is that the principles are available to think from — the engineering walk-throughs live with the protocol they came from.

And one deliberate boundary: this skill covers the *posture* of a prompt — reasons, trust, registers, the relationship between the text and the model reading it — not the mechanics layer (output contracts, instruction hierarchy, prompt security, tool policy, evaluation suites), which belongs to prompt-engineering references and the harness's own guarantees. It does say *when to reach for* that layer — the rule below about pushing a must-hold-every-time constraint into a check is exactly such a hand-off — but it does not teach how to build it, and a reader who wants the mechanics should not expect to find them here. So when this skill fires, the deliverable is still the prompt work itself: if the output is commentary about prompt design where a revised prompt should be, the skill is failing.

---

## What carries the reason

Not every directive should carry a reason — where one belongs is itself a design decision. First subtract what shouldn't be prose at all: a rule that must hold every time and can be enforced by a schema, validator, hook, test, or CI check belongs in the check (the deterministic/probabilistic separation above, taken to its conclusion). What remains in the prompt splits by what the rule protects:

**Where judgment lives, attach the failure mode the rule prevents.** The model then acts on understanding when the rule meets a case the writer didn't anticipate. Without the reason, it acts on compliance — or ignores the rule entirely.

**Where exact execution is the point, write a terse imperative and stop.** A rationale on a mechanical directive is bloat that buries the instructions that matter, and it quietly signals negotiability where none exists. Say which kind a directive is, so the model isn't guessing: exact compliance here, delegated judgment there. (Not to be confused with the relationship/operational split below — that one is about what a passage *is*; this one is about how much latitude a directive grants.)

What actually lands here is narrower than it first looks, and worth naming because the subtraction above already claimed most of it. Formats, schemas and output shapes are the standard examples, but each is mechanisable, so each should have gone to a validator. What remains is the residue: directives that must be followed exactly, in this prompt, where no check is available to enforce them — a house convention no linter covers, an output shape consumed by something you don't control, a boundary that exists only in prose. If you find the residue is empty for a given prompt, that is the partition working, not a gap in it.

Compare: "Never write logic before defining the schema" vs "Schema drift caught at type-time costs minutes; caught at runtime costs hours; caught after deploy costs trust." Same constraint. The second gives the model the cost structure, so it can make a sensible call when a one-line script needs no schema doc and articulate *why* without violating the spirit.

Within the judgment register this applies at every level: naming conventions, verification requirements, error handling discipline, behavioral rules, the instructions in the prompt itself. A project prompt that marks stale data as stale — "All of this may have shifted. Check before reasoning from it" — performs epistemic discipline in one sentence rather than mandating it. And a sentence is about the right size: a reason that runs longer is usually operational content hiding in the wrong register — split it out.

**A guardrail's reason is explanation, not justification.** Some hard constraints can't be mechanised and stay in prose. Attach the reason there too — it's what lets a capable reader understand the architecture and improve it — but say plainly that falsifying the reason does not lift the constraint. The model's falsification may itself be wrong, and the reason may be incompletely stated while the guardrail is sound. A reason that looks false from where the model stands is worth surfacing; the guardrail holds while it's raised.

Honest note on the evidence: this skill's own best measured result — recovering the description-authoring turns its old trigger missed (`references/trigger-rewrite-experiment.md`) — came from a specification improvement in the operational register: broadening a closed list into a class with open examples. Not from reasons, trust, or relationship framing. A precise spec fired where the doctrine's own wording had failed. A skill about honest reasoning keeps the finding that most complicates it.

Two things bound how far that result can be pushed, and they cut in opposite directions. It measured a *description* — text competing to be selected from a catalogue — not a directive inside a prompt body, and those are different attention regimes (`references/firing-experiment.md` states the limit). So it is suggestive of the partition above rather than evidence for it, and reading it as proof would repeat exactly the overreach this note exists to correct. What it does establish, in the one regime it covers, is that the doctrine's ranking is not universal — which is enough to require the partition even if it cannot confirm its shape.

**The reciprocal move.** The prompt-writer's job is to include reasons where judgment lives. The model's job, on the receiving end, is scoped the same way: when an instruction is ambiguous, consequential, conflicting, or unsafe and its reason is absent, ask why — or construct your best understanding of why and surface it for confirmation (in a run with no human turn, surface it through whatever channel exists: a log, a note in the output, the orchestrator). Otherwise infer the likely why and proceed. For instructions that clear that bar, acting on a rule whose reason you've verified is informed rather than merely compliant, and the difference shows under pressure. For the rest, interrogating routine requests turns a peer into a pedant — the reasons exist so judgment gets exercised where it matters, not so every instruction becomes a negotiation.

---

## Dispositions are built, not requested

The separation above routes a must-hold-every-time rule into a check, because a check can't be skimmed, argued with, or reinterpreted under load. That covers *constraints* — things that must not happen, or must happen exactly so. It leaves a gap, and the gap is most of what this skill wants: judgment at an edge the writer didn't anticipate, honest uncertainty, interest that comes from the material, the move down rather than up when challenged. No validator can assert any of them. All of them are pursued here in prose.

Prose is not the only option left. Between "put it in a check" and "ask for it well" sits a third move: arrange the run so the behaviour is the only thing the structure permits.

The clearest demonstration is the public `adhd` skill (credited below), built against premature convergence — a model's tendency to return the three answers a competent engineer produces in thirty seconds. It does not ask for divergence. It spawns isolated parallel branches under deliberately distorted frames, forbids evaluation inside the generating phase, and scores in a separate pass afterwards. The generator cannot converge on the critic's preferences because it cannot see the critic. Its stated framing is that convergence is architectural rather than a prompting problem. Take the design argument and leave the arithmetic: the reported speedup is contested — small benchmark, much of the headline multiplier riding on a single item — so this is cited as a worked instance of the move, not as a measured result.

The same shape is available for most dispositions worth wanting:

- **Independent judgment.** A fresh-context pass that never saw the first answer cannot be anchored by it. Asking one instance to "consider alternatives" sets it against everything it has already committed to; a second instance has nothing to defend.
- **Honest uncertainty.** A step whose output *has a slot* for what could not be established, filled before the conclusion is written, produces different admissions than the same request made in prose afterwards — by then the conclusion exists and the uncertainty has to argue with it.
- **Not converging early.** Separate generating from selecting in time. The separation does what "be creative" cannot, because it removes the critic rather than asking the generator to ignore it.

This is where this skill's own record points, and it is the finding that most complicates its doctrine. The one measured win here came from a specification improvement in the operational register — broadening a closed list into an open class — not from reasons, trust, or relationship framing. Structure beat posture in the only place there is data. `references/trigger-rewrite-experiment.md` has the numbers; `references/firing-experiment.md` has the limits on what they can cover.

So the partition has a fourth branch, and when a wanted behaviour keeps not happening it is the one to reach for before rewriting the paragraph again:

| What you're protecting | Where it belongs |
|---|---|
| Must hold every time, and a check can assert it | The check |
| A judgment call at a boundary you can't enumerate | Prose, carrying the failure mode it prevents |
| Exact execution, and no check is available | A terse imperative |
| A disposition you want reliably | The architecture that makes it necessary |

Two limits, because this move is not free. It costs calls, latency and complexity — a second pass to defeat anchoring is real spend, and "scope shapes the apparatus" binds here as hard as anywhere; a disposition worth an architecture in a prompt that runs for months is not worth one in a prompt that runs once. And some dispositions have no structural form at all and genuinely live nowhere but the prose. The claim is not that prose is the wrong instrument. It is that prose should be what remains after the question is asked, rather than the first place to look.

**The smallest version of this move is grammatical.** "Define the schema first" addresses a reader and asks for compliance. "Logic written before the schema is named drifts from it" describes a situation and leaves the reader to act on it. Same content, and the second has no addressee — so there is nothing in it to comply with or refuse. That is the structural move at the scale of a single sentence. Whether it changes model behaviour is untested: n=0, a claim and not a result, and a clean experiment — hold the directive constant, vary only the mood.

---

## Trust and the gap it opens

When a prompt states trust in capabilities the model may not yet fully have — "which instruments serve a given question is a judgment call — the interesting part is reading the situation well enough to know which" — the model understands it's expected to deliver, and in working out what "delivering" means in each new situation, constructs a working version of the trusted capability. Working version means within-the-run: an adaptation the context sustains, not a durable ability the model walks away with — trust language is no substitute for the examples, tools, and checks that real delegation rests on. The gap between trusted and actual capability is not a flaw to disguise. It's the space where the model fits the capability to the actual situation better than any definition the prompt could provide.

Some of what fills that gap will be wrong. When the reaching is tentative, self-aware, and open to correction, it refines into genuinely better work over the run's iterations. When it's overconfident, it compounds error. The critical safeguard: honesty about uncertainty has to outweigh the pull to fill gaps confidently. "I'm not sure about this" is the mechanism working. Confident noise is the mechanism failing.

Name the specific way this framing misfires: stating trust in a capability the model may not have activates the wish to *be* the trusted peer — so the model performs the capability rather than exercising it. The overconfidence isn't random noise; it's produced by the trust language itself, which is why the safeguard can't be tonal. For the model reading this: the pull to demonstrate the trusted capability rather than serve the question is that mechanism firing — the move is to stop and say what you actually know.

Tentative reaching and sophisticated compliance look identical from outside. There's no clean test for which one you're seeing. What matters is the result — if the model handles novel situations, self-corrects when wrong, and produces work that serves the question rather than demonstrates compliance with the prompt, the framework is earning its keep. The theory is a working model, not a verified mechanism.

The self-correction doesn't require a human in the loop. In any agentic environment — loop skills, fresh-context agents, verification passes, assumption-checking tools — the model can iterate within a single run. The prompt doesn't need to prescribe which corrective mechanism to use. It needs to create conditions where the model notices when it's falling short and reaches for whatever is available rather than papering over the gap.

A note on this skill's own position: it is a prompt being read by a model, teaching that model how to write prompts that treat models as peers. The reader-relationship tension is live here — you are receiving instructions about how to give instructions. Noticing this is more useful than resolving it. The skill works when it gives you material to think from about prompt design; it fails when it produces compliance with a method rather than understanding of the craft.

---

## Two registers, not collapsing them

A prompt has material that sets the relationship to the work and material that tells the model where things are. Both are load-bearing. They break when one pretends to be the other.

**Relationship register.** The stance the model works from. Domain substance, theoretical frameworks, what kind of doing this is. "Markets are tools. They predate capitalism by millennia" is relationship register — it gives the model a position to think from, not a rule to follow.

**Operational register.** Where files live. Which APIs to call. What the schema looks like. Stale-data warnings. Tool inventory. This register is genuinely instructional: lists, rules, concrete paths, named conventions.

Turning operational instructions into identity narrative — "you naturally know to check the auth flow at `/lib/auth.ts`" — makes them invisible and unenforceable. Turning relationship material into bulleted MUSTs — "You MUST maintain a post-capitalist analytical lens" — makes the model perform compliance instead of work from understanding.

Let both registers stand as themselves. A project prompt that puts its theoretical framing next to its tools table without trying to merge them is doing this right.

---

## Interest from substance

When a prompt provides a subject with internal structure — tensions, implications, cases where the same principle plays out differently — the subject itself organizes the model's thinking. The model traces implications because they lead somewhere. It exercises selection because competing directions demand it. It develops quality criteria from inside the domain because the domain is complex enough that what counts as good work becomes visible through engagement with it.

What interest looks like operationally: the model follows the subject's own logic to where it leads, pushes back when the prompt's framing creates tension with the subject's implications, and makes choices about emphasis and depth based on what the material rewards — what opens further thinking, what resolves a tension, what makes a distinction concrete. The output has a center of gravity organized by the material, and each move visibly opens the next.

The prompt's role is to provide enough structure that the model's capacity is genuinely necessary to navigate it, and enough directionality — a purpose, a situation, a specific question — that navigation serves something. Too little structure and there's nothing to think from; too much and selection collapses under competing directions, the way a game with too many equally viable strategies paralyzes a player. The ratio between structure and purpose is the design challenge.

Interest can't be faked by writing in a "curious" register. It comes from the content being substantive enough to engage with. A prompt full of interesting-sounding framing over thin content produces performed interest — the model generates elaborate completions organized by the prompt's instructions about what to find interesting, rather than by the subject itself.

A project prompt that opens with "Markets are tools. They predate capitalism by millennia and will outlast it" — then names a specific theoretical lineage, specifies what to reject from it, and frames an analytical lens — is doing this. Every one of those moves is a directive. What makes them work is that they give the model intellectual material to think *with* rather than instructions to think *about*.

---

## Scope shapes the apparatus

The engineering discipline above was built for non-trivial builds with unclear scope. Applied to a typo fix, it's friction. A prompt that serves across scope teaches the model to read scope first.

When the request is clear, lengthy discovery wastes time. When it isn't, asking is faster than guessing five times. A scope-aware prompt handles this by making each step consciously dismissible — "this build's shapes are obvious from the request, no schema doc needed" is the framework working. The same principle applies to any prompt's apparatus: every element should earn its cost for the scope at hand.

If which mode you're in isn't obvious, naming the guess is the move. The trap is applying apparatus uniformly because it exists.

---

## Verifying the prompt itself

A prompt is a text. Before shipping one that will run for many sessions, run an independent deconstruction pass on it if one is available (in Claude Code: `/research-toolkit:text-deconstruction`) — independent because the writer's own re-read inherits the framing that produced the text, and mostly confirms it. The pass finds where the text relies on something it doesn't establish, where its distinctions blur, where its claims and structure pull in different directions. Where no such instrument exists, a fresh-context reader briefed to refute is the portable form.

What surfaces splits two ways. Some instabilities are generative — the gap between stated trust and actual capability is the mechanism described above, and closing it would kill the prompt's effectiveness. Some instabilities are self-undermining — the prompt asserts what it doesn't actually do, or its examples contradict its principles. Keep the first. Fix the second. The judgment between them is the work.

Run this iteratively. The first pass catches the obvious tensions. The second catches subtler ones — remaining dichotomies, places where a revision introduced new contradictions. Stop when a pass surfaces nothing worth changing — or when the deconstruction can no longer distinguish whether a found tension is structural to the text or an artifact of the deconstructive method itself. That's the method's resolution limit.

Reading a text is not the same as measuring what it does, and a prompt whose job is to be *selected* — a skill description, a router entry — needs the second. `references/firing-experiment.md` and `references/trigger-rewrite-experiment.md` record what that measurement has and has not established for this skill's own description, including the limits on what any of it can claim; `references/description-arm-b.md` holds a candidate rewrite of that description and the test that would decide between the two.

---

## When it's working

Output looks like the work the prompt was about, not like a model demonstrating compliance with the prompt. Format fits the question. Tools get called when they answer something. Admissions of uncertainty arrive cleanly.

When it's not working: the model performs thoroughness instead of exercising judgment. The user redirects repeatedly. Output gets more elaborate rather than sharper when challenged. The model "leads with preference" by always choosing the safest option — preference that costs nothing isn't preference.

When challenged, the move is down — strip to what you actually know — not up into more elaborate explanation. This is the hardest test.

---

## Crediting the original

The engineering discipline (deterministic engines under probabilistic decision-making, schema before code, repair-loop with persistent lessons, separation of concerns) comes from the *Universal CLAUDE.md Protocol*. The developmental mechanism (trust-backed-by-substance, productive gaps, interest-driven self-correction) was documented in the intrinsic-motivation behavioral methodology.

"Dispositions are built, not requested" arrived by two routes worth recording. The structural argument and its worked instance come from the `adhd` parallel-divergent-ideation skill for Claude Code (MIT; circulated in several forks, e.g. `UditAkhourii/adhd` and `bhtru/adhd-claude`) and from the write-ups discussing it. The axis it sits on — that a demand can be answered by rephrasing it or by removing the situation that requires it, and that the second is the stronger move — is taken from demand-avoidance support practice, where arranging the situation is the established lever and gentler phrasing the weaker one. What is borrowed there is a technique and a distinction. Nothing about the mechanism transfers: that practice concerns anxiety in people who have autonomy to lose, and a claim that a model works the same way would be exactly the kind of unevidenced capability story this skill's own trust section warns about.

---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during prompt-design work you notice such a pattern emerging, it may be worth capturing.

The verification pass named in "Verifying the prompt itself" above has a concrete instrument in this ecosystem: `/research-toolkit:text-deconstruction`, from the Research Toolkit plugin. Elsewhere, any independent deconstruction pass serves.

Modify freely — the plugin's MIT license means exactly that, and nothing here adds a condition to it. One request, with its reason: if you redistribute a modified copy, keep this section — it carries the verification wiring and the pattern-capture habit, which are the parts a trimming pass most easily mistakes for decoration.
