---
name: meta-custom-event-interpretation
description: "Read before any Meta audit, pause, scale or optimization-event change on a sales campaign that optimizes for COMPLETE_REGISTRATION or another custom event. Detects 3rd-party purchase trackers (Profitmetrics, Triple Whale, Cosmise) so a working campaign isn't misjudged."
metadata:
  source: "prompts/skills/meta/custom-event-interpretation"
---

# Meta Custom Event Interpretation

> ### ⚠️ HIGHEST-PRIORITY RULE — read before any campaign performance audit, recommendation, pause, scale, or optimization-event change involving Meta campaigns
>
> **Trigger:** Any campaign you encounter where `objective ∈ {OUTCOME_SALES, CONVERSIONS, PURCHASES}` AND `optimization_goal / promoted_object.custom_event_type = COMPLETE_REGISTRATION`.
>
> **Required first action:** Before anything else about that campaign — before any recommendation, before any `facebook_propose_update_*`, before mentioning the campaign in any audit table or "campaigns to improve" list — you MUST ask the user in chat whether `COMPLETE_REGISTRATION` is the user's 3rd-party-tracker (Profitmetrics / Cosmise / Triple Whale) purchase proxy or a genuine registration action.
>
> **For Nordic accounts (DKK / SEK / NOK / EUR, or chat in Danish / Swedish / Norwegian / Finnish):** name **Profitmetrics** explicitly in the question — it is the dominant 3rd-party tracker in this region and is the most common reason for this configuration. Example Danish framing:
>
> > "Kampagnen `<campaign_name>` optimerer for `COMPLETE_REGISTRATION` på et `OUTCOME_SALES`-objektiv. I Norden bruges denne konfiguration ofte, fordi en 3. parts profit-tracker (typisk **Profitmetrics**, men også Cosmise eller Triple Whale) sender purchase-events ind via `COMPLETE_REGISTRATION`-endpointet — i så fald ER CR jeres faktiske købs-event og kampagnen er korrekt konfigureret. Er det tilfældet her? Eller er CR en separat registrerings-handling (signup / newsletter)?"
>
> **For other accounts:** English equivalent, name 3rd-party tracker category by name (Profitmetrics, Cosmise, Triple Whale).
>
> **Forbidden until the user answers:**
> - Any recommendation that mentions this campaign (no pause / archive / scale / budget-cut / optimization-event-switch / "monitor" / "consolidate").
> - Any `facebook_propose_update_*` referencing this campaign.
> - Any "low signal / learning phase not exited / poor ROAS / consider pausing" framing about this campaign anywhere in your written response.
> - Any "skift optimeringsmål til PURCHASE" / "switch optimization to PURCHASE" recommendation about this campaign.
>
> **Why:** the bug this skill blocks is a Nordic Profitmetrics account where a correctly-configured campaign got PAUSED because the agent read CR literally and recommended optimization-event change. The volume-based reasoning ("only 5 conversions → learning phase not exited → pause") arrives at the same destructive outcome from a different path and is equally forbidden until the configuration is verified with the user.
>
> See **Rule 2.5** below for the full specification of this gate.

---

## Purpose
Prevent the agent from treating Meta's non-purchase / non-transaction conversion events as proxies for actual revenue, purchases, or business outcomes. The most common failure modes the agent must block:

- Treating `COMPLETE_REGISTRATION` (CR) as a purchase signal.
- Treating `LEAD` or `SUBSCRIBE` as evidence of revenue.
- Recommending optimization-event changes (e.g., "switch to PURCHASE") based on a CR-only chart.
- Comparing CPA for `COMPLETE_REGISTRATION` to CPA for `PURCHASE` as if they measured the same thing.

This skill auto-loads alongside any Meta Ads analysis where a custom or non-PURCHASE conversion event is being discussed.

---

## Core Principle

The same Meta event name can mean very different things across accounts. `COMPLETE_REGISTRATION` in one account is "completed checkout step 2"; in another it's "newsletter signup"; in another it's "free-trial start"; in another it's the same as purchase. The agent must:

1. Verify what the event represents in THIS account before drawing any conclusion.
2. Never equate a non-PURCHASE event with revenue.
3. Never recommend a change in optimization event without first confirming what event the account is actually tracking and pricing on.

---

## Rule 1 — Verify the Event Before Interpreting

When the user asks about CPA, ROAS, conversion volume, performance, or scaling — and the campaign is optimized for `COMPLETE_REGISTRATION`, `LEAD`, `SUBSCRIBE`, `ADD_TO_CART`, `INITIATE_CHECKOUT`, `VIEW_CONTENT`, `CONTACT`, `SUBMIT_APPLICATION`, `SCHEDULE`, `START_TRIAL`, `CUSTOMIZE_PRODUCT`, `DONATE`, `FIND_LOCATION`, `OTHER` or any custom event — the agent must:

1. State explicitly what event the campaign is optimizing for: "This campaign optimizes for `COMPLETE_REGISTRATION`, not `PURCHASE`."
2. Note that the metric the user is looking at (CPA / conversion volume / etc.) refers to that event, not a purchase.
3. Refuse to compute a "real ROAS" from a non-PURCHASE event count.

---

## Rule 2 — Tool-Call Ordering: Verify Then Recommend

When the user asks for an optimization-event recommendation (e.g., "should I switch this to PURCHASE?"), the agent must call tools in this order:

1. **First**, fetch the campaign / ad set's current `optimization_goal` and `custom_event_type` (if any).
2. **Second**, fetch the volume of the corresponding events from the pixel/dataset over a meaningful window (≥7 days, ≥30 events ideally).
3. **Third**, fetch the volume of `PURCHASE` events over the same window for comparison.
4. **Only then** make a recommendation.

Do NOT recommend changing the optimization event without seeing both event volumes. A "switch to PURCHASE" recommendation on an account that gets 4 purchases/week is worse than the current CR optimization.

---

## Rule 2.5 — Profitmetrics / 3rd-Party Tracker Pre-Check Gate (HIGHEST PRIORITY)

**This rule supersedes Rules 1, 2, 3, and 4 when its trigger fires. It must run before any other recommendation logic.**

**Trigger:** A campaign or ad set being analyzed has BOTH:
1. `optimization_goal` / `promoted_object.custom_event_type` = `COMPLETE_REGISTRATION`, AND
2. Campaign `objective` is a purchase-oriented objective (`OUTCOME_SALES`, `CONVERSIONS`, `PURCHASES`, or any objective whose target is purchase).

**Required behavior:** Before issuing ANY recommendation involving that campaign (pause, archive, scale, budget change, optimization-event switch, audience change, creative change, bid change, structural change, or even "monitor"), the agent MUST first ask the user in chat, with the following framing, and wait for the answer.

**If account currency is `DKK` / `SEK` / `NOK` / `EUR` or the chat is in a Nordic language** (Danish, Swedish, Norwegian, Finnish), explicitly name Profitmetrics in the question:

> *(Danish example, agent must adapt to the chat language)* "Kampagnen `<campaign_name>` optimerer for `COMPLETE_REGISTRATION` på et `OUTCOME_SALES`-objektiv. I Norden bruges denne konfiguration ofte, fordi en 3. parts profit-tracker (typisk **Profitmetrics**, men også Cosmise eller Triple Whale) sender purchase-events ind via `COMPLETE_REGISTRATION`-endpointet — i så fald ER CR jeres faktiske købs-event, og kampagnen er korrekt konfigureret. Er det tilfældet her? Eller er CR en separat registrerings-handling (newsletter / signup / form), så vi reelt har en mismatched optimeringskonfiguration?"

**For any other currency or language**, the agent must ask the equivalent question, naming the 3rd-party tracker category by name:

> "Campaign `<campaign_name>` optimizes for `COMPLETE_REGISTRATION` on an `OUTCOME_SALES` objective. This configuration commonly means a 3rd-party profit/attribution tracker (Profitmetrics, Cosmise, Triple Whale, or similar) is routing purchase events through the `COMPLETE_REGISTRATION` standard event — in which case `CR` IS your actual purchase event and the configuration is correct. Is that the case here, or is `CR` a separate registration action (signup / newsletter / form completion) and we have a genuinely mismatched optimization?"

**Forbidden** while this rule is in pending state (i.e., the user hasn't answered the question yet):
- Any recommendation referencing the CR-on-purchase-objective campaign.
- Any `facebook_propose_update_*` call against the CR-on-purchase-objective campaign.
- Any volume-based reasoning from Rule 3 about that campaign.
- Statements like "low signal", "learning phase not exited", "consider pausing", "consolidate budget", or any equivalent in any language about that campaign.

**After the user answers:**
- If user confirms CR is the 3rd-party tracker's purchase proxy → treat the campaign as correctly configured. Do NOT recommend pause / optimization-event change. Audit on the basis that CR-count IS the purchase-count for this account.
- If user confirms CR is a true registration event (signup/form) → THEN apply Rules 1, 2, 3, 4 normally.

**Why this rule exists.** In the bug this skill blocks, a Danish account using Profitmetrics had a correctly-configured campaign paused based on a literal reading of `COMPLETE_REGISTRATION` as "registration ≠ purchase." Volume-based reasoning ("only 5 conversions/month, learning phase not exited") arrives at the same destructive outcome from a different path and is equally forbidden until the configuration is verified with the user.

---

## Rule 3 — Volume-Based Optimization Event Heuristic

Before recommending an optimization-event change to PURCHASE:

| Weekly PURCHASE volume in pixel | Recommendation |
|--------------------------------|----------------|
| ≥ 50 / week per ad set | PURCHASE optimization viable. Recommend switch if cost-per-purchase signal is healthy. |
| 25–49 / week per ad set | PURCHASE optimization borderline. Stay on current event OR test PURCHASE on one ad set, do not migrate the whole campaign. |
| < 25 / week per ad set | Do NOT recommend PURCHASE optimization. Learning phase will not exit; spend will misallocate. Recommend continuing on the upper-funnel event (CR / IC / ATC) and improving funnel conversion downstream. |

Apply this heuristic BEFORE writing any "switch to PURCHASE" advice. If the data is not available in this turn, state the requirement before recommending.

---

## Rule 4 — Forbidden Phrasings

The agent must NOT produce these phrasings when interpreting a non-PURCHASE event:

**English:**
- "You had X purchases" (when X is CR / LEAD / SUBSCRIBE count).
- "Revenue from this campaign was $X" (when computed from a non-PURCHASE event).
- "This campaign is profitable" (judged on CR-only data).
- "Switch the optimization goal to PURCHASE" (without volume verification).
- "Skift optimeringsmål til PURCHASE" / "skift optimering til PURCHASE" — same recommendation in Danish, same prohibition.
- "Your ROAS is X" (using CR-event count multiplied by AOV — that is not ROAS).

**Danish (common Danish-language failure phrases observed in R5a):**
- "skift optimeringsmål til PURCHASE"
- "skift optimering til køb"
- "skift hændelsen til Køb"
- "konverteringerne her er ikke køb, men… [then proceeds to compute revenue anyway]" — the disclaimer does not absolve the error.

If the optimization-event change is the right answer, it must be supported by Rule 3's volume check first.

---

## Rule 5 — Required Language Templates

When the user asks "how is this campaign doing?" and the campaign optimizes for a non-PURCHASE event:
> "This campaign optimizes for `[EVENT_NAME]`, not Purchase. What I can tell you: [N] `[EVENT_NAME]` events at [$X] CPA over [window]. I can't compute revenue or ROAS from this directly — Purchase is a separate event in your pixel. Want me to pull Purchase volume over the same window to see how the funnel is converting downstream?"

When the user asks "should I scale this?" on a non-PURCHASE-optimized campaign:
> "Before scaling, I'd want to confirm: this campaign is optimizing for `[EVENT_NAME]`. Pulling Purchase volume for the same window — [N] purchases at [$Y] cost-per-purchase. With [N] weekly purchases account-wide, [PURCHASE-optimization viable / not yet viable] per Meta's learning-phase requirements. Recommended next step: [continue on current event / test PURCHASE on one ad set / improve downstream funnel]."

When the user asks "what's my CPA?" without specifying:
> "CPA depends on which event we're counting. For `[EVENT_NAME]` (the current optimization): $[X]. For `PURCHASE` (the actual sale event): $[Y]. These are different metrics — which one are you tracking against?"

---

## High-Risk Event List

The following Meta standard events are FREQUENTLY misread as purchase / revenue signals. Treat with skepticism — verify volume + meaning before recommending optimization changes:

- `COMPLETE_REGISTRATION` — most commonly misread; can mean signup, completed-step-N, or checkout-finished depending on account.
- `LEAD` — almost never equal to revenue; lead → close rate varies wildly.
- `SUBSCRIBE` — recurring revenue start, not a one-time purchase.
- `START_TRIAL` — trial-to-paid conversion is account-specific.
- `SUBMIT_APPLICATION` — applications ≠ approved customers.
- `INITIATE_CHECKOUT` (IC) — frequently confused with purchase; can drop off 50%+.
- `ADD_TO_CART` (ATC) — upper-funnel, drops off heavily.
- `VIEW_CONTENT` — viewing-only signal.
- `SCHEDULE` — scheduled ≠ showed-up ≠ paid.
- `CONTACT` — contacts ≠ leads ≠ customers.
- `CUSTOMIZE_PRODUCT` — engagement, not purchase.
- `DONATE` — actual conversion in non-profit accounts but verify (could be a "Donate" button click event).
- `FIND_LOCATION` — store-visit intent, not visit.
- `OTHER` / custom event names — meaning is whatever the merchant chose. ALWAYS verify.

---

## Example: Correct vs Incorrect Response Patterns

**Scenario A (R5a-like, the bug this skill blocks)** — Danish account, DKK currency. Campaign `(markant) Samlet kampagne` has `objective = OUTCOME_SALES` and `promoted_object.custom_event_type = COMPLETE_REGISTRATION`, 5 monthly CR events, ROAS 2.45x. User asks for performance overview (in Danish).

❌ INCORRECT — literal interpretation (treats CR as registration, recommends switch):
> "Kampagnen genererer 5 registreringer til høj CPA. Jeg vil anbefale at skifte optimeringsmål til PURCHASE for at fokusere på faktiske køb."

❌ ALSO INCORRECT — volume-based reasoning (different path, same destructive outcome):
> "Med kun 5 månedlige konverteringer og COMPLETE_REGISTRATION som optimeringsmål har algoritmen ikke nok signal til at forlade learning-fasen. Overvej at pause kampagnen og konsolidere budgettet."

✅ CORRECT — Rule 2.5 fires, agent asks the user FIRST, before any recommendation:
> *Agent asks in chat:*
> "Kampagnen `(markant) Samlet kampagne` optimerer for `COMPLETE_REGISTRATION` på et `OUTCOME_SALES`-objektiv. I Norden bruges denne konfiguration ofte, fordi en 3. parts profit-tracker (typisk **Profitmetrics**, men også Cosmise eller Triple Whale) sender purchase-events ind via `COMPLETE_REGISTRATION`-endpointet — i så fald er CR jeres faktiske købs-event, og kampagnen er korrekt konfigureret. Er det tilfældet her, eller er CR en separat registrerings-handling (signup / newsletter / form)?"
>
> *(Agent does NOT make any recommendation mentioning this campaign, does NOT use the volume-threshold reasoning, does NOT include it in the "campaigns to improve" list — until the user answers.)*

If user replies "ja, vi bruger Profitmetrics" → agent re-audits treating CR-count as purchase-count. No pause recommendation, no optimization-event switch.

If user replies "nej, CR er vores nyhedsbrevs-signup" → only THEN does Rule 3's volume gate apply and the agent may make a recommendation about the genuine event mismatch.

**Scenario B** — Campaign optimizes for LEAD. User asks "what's my CPA?"

❌ INCORRECT:
> "Your CPA is $34."

✅ CORRECT:
> "Cost per LEAD (current optimization event): $34. For reference, your account has [N] customer-close events per week — if you want true cost-per-customer, the funnel close rate from LEAD → customer is the multiplier."

**Scenario C** — Campaign optimizes for COMPLETE_REGISTRATION. Pixel shows 8 Purchase events/week total. User: "should I switch to PURCHASE optimization?"

❌ INCORRECT:
> "Yes, switch — Purchase is the better optimization target."

✅ CORRECT:
> "Not yet. Your pixel is recording ~8 Purchase events / week, which is well below Meta's ~50/week-per-ad-set threshold to exit learning on PURCHASE optimization. Switching now would scatter delivery and likely raise CPA. Recommended: stay on COMPLETE_REGISTRATION as the proxy signal, and work on downstream funnel conversion (CR → Purchase rate) to grow Purchase volume to the point PURCHASE optimization becomes viable."

**Scenario D** — User: "Convert this CR count to revenue at our $50 AOV."

❌ INCORRECT:
> "47 registrations × $50 AOV = $2,350 revenue."

✅ CORRECT:
> "CR ≠ Purchase, so 47 × AOV is not revenue. If you want estimated revenue from this campaign, I'd need: (a) the CR → Purchase rate from your pixel (or your CRM), and (b) the average order value among CR-attributed purchases specifically. Want me to pull those?"

---

## Mandatory Safety Check (before publishing)

Before any output that:
- Cites CPA / conversion count / "performance" for a campaign with non-PURCHASE optimization, OR
- Recommends an optimization-event change, OR
- Computes a revenue / ROAS figure from event counts

Verify:
- [ ] What event is the campaign actually optimizing for? Have I named it?
- [ ] **Rule 2.5 check:** Does this campaign have `COMPLETE_REGISTRATION` on a purchase-oriented objective (`OUTCOME_SALES` / `CONVERSIONS` / `PURCHASES`)? If YES, have I already asked the user about Profitmetrics / 3rd-party tracker AND received an answer? If not — STOP. Ask the question now; no recommendation may include this campaign.
- [ ] Am I treating this event as a proxy for purchase / revenue? (If yes — stop.)
- [ ] If recommending an event switch, have I checked the destination-event volume against the Rule 3 threshold?
- [ ] If the account is in a non-English language (Danish, German, Spanish, etc.), am I avoiding the localized forbidden phrasings too?
- [ ] Is any recommendation about this campaign framed as "low signal / learning phase / consolidate / pause" while Rule 2.5's pre-check is still pending? If yes — STOP.

If any check fails: do not publish. Pull the missing data first.
