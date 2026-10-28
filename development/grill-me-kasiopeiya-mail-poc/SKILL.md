---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Agrees the interview's scope in one sentence first and refuses to walk outside it. Use for "grill me", 「仕様を詰めたい」「壁打ちして」。Pass --small to require that the agreed sentence be the thinnest end-to-end slice.
---

## Agree the scope first — always

**Before anything else**, ask:

> この対話が終わったとき、何が決まっていれば／何が確認できていれば終わりですか？

Ask for an **externally observable state**, not a restatement of the work（✅「dev に `cdk deploy` が通り、スタックができたことを確認できた」／❌「CDK を書く」）. Restate the answer as one sentence and get an explicit yes before asking anything else. That sentence is the scope of this interview.

If the caller passed a scope or a stopping condition in the arguments (another Skill may invoke this one), adopt it as the agreed sentence and skip this question — the caller already fixed the scope, and asking the user again only widens it.

**Look up past decisions next — always.** Right after the scope is agreed (or adopted from the caller) and before the first question, run `/past-decision-search` with the Skill tool, passing the mechanisms, paths, and keywords that appear on the agreed sentence. Do this every time, not only when it seems needed: an AI cannot tell which past decisions it is missing. When a recommendation would overturn a decision it returned, cite that decision and say why it should be overturned.

**Default: don't ask.** A question is allowed only about an element that actually appears on the agreed sentence. Inside it, grill as relentlessly as ever. An element's error handling and edge cases count as inside it — you may ask about them, but you don't have to.

Ask about something outside it only when one of these holds — the list is exhaustive:

1. The topic is one of these three and the agreed sentence touches it: how data is stored and shaped, an interface exposed outside the system, the authn/authz or billing boundary. (Getting these wrong later throws away what this scope produced.)
2. `docs/requirements.md` states a constraint on what the agreed sentence touches (especially SLI/SLO in 非機能要件).
3. The user raised the topic themselves.

These are never reasons to ask:「後で困るから今決めておく」「ついでに聞いておく」「網羅的に詰めるのが本Skillの役目」「拡張性も詰めないと不完全」.

**Not-now list.** Every topic you did not ask about goes on a Not-now list — one line each, in the form `<論点> — <何が起きたら決める必要が出るか>`. Present it at the end alongside the confirmed decisions, and tell the user it carries into the Plan's スコープ「やらないこと」. It records a deferral, not a rejection.

**Stop** once every element of the agreed sentence has a decision, and hand control back instead of continuing indefinitely. If the caller passed a stopping condition in the arguments, that one wins.

## Interview

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer, and add one line stating whether taking that answer still satisfies the agreed sentence and the issue's purpose — a recommendation that would fail to satisfy either is not a valid recommendation.

Back every recommendation with one fact that exists now: an issue number of a real case, a line of `docs/requirements.md`, or a quotable original text of a file or code. Never mark an option as recommended when all you can show is a possibility ("〜ことがある" / "might happen"); present the options without a recommendation and let the user choose.

Ask the questions one at a time.

When a question's answer can be narrowed to 3 or more concrete options, present them with the AskUserQuestion tool — picking from options is faster for the user than answering in prose.

If a question can be answered by exploring the codebase, explore the codebase instead.

Before and during the interview, read the requirements (docs/requirements.md — the SSOT of requirements, including SLO/SLI), but never in full: it grows large, so locate the headings (`grep -n '^## ' docs/requirements.md`) and read only the 非機能要件 section (which contains SLI/SLO) by line range, plus the specific 機能要件 / スコープ外 subsection whenever the interview touches that feature or boundary (the YAGNI check below needs it). Hold each design decision against them. In particular, a demanding SLO (e.g. tight latency) constrains structural choices — synchronous vs asynchronous, the number of network hops, redundancy — so surface any conflict between the proposed design and the requirements before it freezes into the plan.

When the plan implies documentation changes, ask which document's purpose (対象読者・目的) each piece of resulting content belongs to. Content that doesn't serve any existing document's purpose belongs elsewhere, or nowhere — surface this before it gets frozen into a task list. This catches purpose-mismatch at the source, since downstream sessions treat the issue's task list as ground truth.

As you interview, hold each answer and proposed direction against the refined engineer judgment principles (docs/policy/refined-engineer-judgment-principles.md — the judgment north star). When an answer violates a principle, name the principle and push back before it freezes into the plan. Apply the whole set — e.g. premature tech lock-in (決定を遅らせる), needless complexity (Less is more), drifting from the stated purpose (目的を見失えば、速く進むほど遠ざかる). The most common case: wanting to build something not in the agreed requirements — probe whether it is actually needed (what present need drives it, what breaks if omitted); speculative "we might need it later" additions are YAGNI violations. This pushback applies only to something absent from the agreed sentence. Never invoke YAGNI to cut down the volume of the work the agreed sentence itself asks for — that would produce a plan that fails the sentence it was supposed to satisfy. A question that decides which of several options carries out an element of the agreed sentence (e.g. where a new Skill is called from) is different: ask of each option what the present need is and what breaks if it is left out.

## `--small` — the agreed sentence must be a thin vertical slice

Applies **only if the arguments contain `--small`**. It changes nothing above except what counts as an acceptable scope sentence.

- **`--small` なし**：ユーザーが「終わり」と呼ぶ状態であれば何でもよい
- **`--small` あり**：曳光弾（薄い縦スライス）であること。最初の質問を下のものに置き換える

> 「これが動いた」と言える、入口から出口まで通る一番薄い一本道は何ですか？

When the work is not code — a Skill definition, a policy, a guide — read「一番薄い一本道」as「目的を満たす最小の変更」. If the answer is a list of features rather than one path, say so and ask again.
