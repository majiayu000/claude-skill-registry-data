---
name: seo-action-plan
description: Use when turning validated SEO, AEO, GEO, technical, or measurement findings into an approval-ready, evidence-linked action plan without claiming guaranteed ranking, citation, traffic, or conversion outcomes.
---

# SEO Action Plan

## Purpose

Turn evidence-backed findings into a sequenced implementation plan that a content, engineering, analytics, product, or legal owner can approve and execute. This skill plans work; it does not change a site, publish content, modify crawler controls, deploy code, or approve its own recommendations.

Use it after `seo-aeo` or `seo-geo` has produced a validated `optimization-brief.json`, or after a conventional SEO specialist has produced a validated `seo-findings.json` bundle. For a normal conversational audit without a validated artifact, provide a clearly labelled **provisional action list** and name the evidence needed before it becomes a formal plan.

## Non-negotiable boundaries

- Do not promise inclusion, ranking, citation, referral, traffic, revenue, or conversion lift.
- Do not invent a platform requirement. In particular, do not prescribe `llms.txt`, special “AI schema”, chunk sizes, bot access, or a crawler-control change unless the supplied evidence and the applicable platform documentation support it.
- Separate an observed issue from its likely cause and from the proposed change.
- Never treat a crawler request or bot log as evidence of retrieval, grounding, citation, referral, or conversion.
- Do not turn a speculative or experimental finding into a normal implementation action. Keep it as a monitored experiment or decline it.
- Require human approval for production, policy, legal, accessibility, analytics, or crawler-control changes. The plan’s approval status starts as `pending`.

## Formal-plan workflow

Read `references/action-plan-protocol.md` before creating `action-plan.json`.

1. **Check the input gate.** Require an immutable, validated upstream bundle. An AEO/GEO input contains `optimization-brief.json`, `research-pack.json`, and its referenced raw evidence. A conventional SEO input contains `seo-findings.json` and the raw evidence it names. Run:

   Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run:

   ```powershell
   python "<suite-root>/scripts/validate_seo_action_plan.py" validate-plan <plan>/action-plan.json --bundle <plan>
   ```

   Validate a conventional input directly before packaging it when possible:

   ```powershell
   python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <findings>/seo-findings.json --bundle <findings>
   ```

   The runtime skill locator resolves the installed support package containing the suite-level validators and contracts; a retained repository checkout is optional.

   The plan bundle must preserve each upstream bundle below `inputs/`; do not edit its artifacts after validation. Use Action Plan `1.2.0` when it contains SEO Findings `1.1.0`, Optimization Brief `1.1.0`, or expanded action/verification types. Action Plan `1.1.0` remains valid for legacy SEO Findings `1.0.0`, and `1.0.0` remains valid for legacy Optimization Brief `1.0.0`-only plans.

2. **Map the evidence.** For every proposed action, link at least one finding and at least one resolving evidence record. Keep locale, engine, surface, target, and claim scope intact. An action may combine findings only when their scopes are compatible.

3. **Choose a real owner and a reversible path.** Assign the responsible team/role, required approver, effort, risk, dependencies, acceptance criteria, verification method, guardrail, and rollback method. `seo-action-plan` itself cannot be the implementation owner.

   Action Plan `1.2.0` requires `risk_flags`. Declare every applicable policy, crawler/indexing, legal/privacy, accessibility, experiment-wide, or irreversible risk. Any declared flag is high risk and requires the matching approval and rollback; do not hide sensitive work behind a generic technical or content label.

4. **Use confidence honestly.** `high` needs confirmed evidence; `medium` cannot rest on experimental evidence; `low` is an explicitly monitored hypothesis. Decline changes that lack sufficient evidence, conflict with platform documentation, or would create legal/accessibility risk.

5. **Write only executable, reviewable instructions.** Say what will change, what will not change, how it will be checked, and which observable signal would justify keeping or reverting it. Use a source-specific metric: search-console visibility, analytics/referrals, manual content review, recrawl, log review, or a repeatable visibility run. Do not collapse these into a universal score.

6. **Validate before handoff.** Use `validate-plan`; fix every error. A passing file proves structural traceability, not that the recommendation will work or that the upstream evidence is current.

## Routing from the plan

- **Content/editorial:** send approved actions to `seo-content`; preserve the evidence and claim boundaries in the content brief.
- **Technical implementation:** send approved actions to `seo-technical`; include rollback and platform-specific crawler/control evidence.
- **Structured data:** send approved actions to `seo-schema`; require visible-content alignment and rich-result eligibility checks, never a rich-result promise.
- **International targeting:** send approved actions to `seo-hreflang` or `seo-sitemap` when the action’s locale or discovery scope requires it.
- **Commerce and local:** send product/feed actions to `seo-commerce` and location/profile/NAP actions to `seo-local`.
- **Media and publishing:** send video actions to `seo-video` and publisher/news/Discover actions to `seo-news-discover`.
- **Agent, architecture, and authority:** send task-flow/protocol actions to `seo-agentic`, taxonomy/internal-link/site-graph actions to `seo-architecture`, and backlink/mention/source-landscape actions to `seo-authority`.
- **Measurement:** send conventional search/site performance work to `seo-performance` and AI-answer observations to `ai-visibility-monitor`; keep their metric families separate.
- **Prioritization and coordination:** send cross-team approved work to `optimise-seo` or `seo-plan`.

## Provisional action list

If a formal input bundle is unavailable, do not fabricate one. Respond with a short table or list containing:

- observation and its source/capture;
- proposed action and owner;
- evidence gap or uncertainty;
- approval needed;
- verification and rollback;
- the exact artifact or observation needed to upgrade it to a validated formal plan.

Label all such items `provisional`; do not write them to `action-plan.json`.

## Output checklist

For a formal plan, return:

- `action-plan.json`, validated against the checked-in contract;
- a readable action summary grouped by priority and owner;
- explicit declined actions and limitations;
- a statement that approval is pending and that outcomes are not guaranteed.

Do not include raw secrets, personal data, copied customer analytics, or unlicensed content in the plan bundle.
