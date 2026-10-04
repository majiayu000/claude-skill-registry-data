---
name: "flow"
description: "The working style and router for this skill set: concise detailed replies, deliberate subagents, unslopped prose, simple code, verified work. Routes a task to its playbook and names the principles that shaped each decision. Use for /flow or a request to work in this style."
disable-model-invocation: true
---

# Flow

## Non-negotiables

**Start every multi-step task with a todo list whose first item is to read the
Principles index below.** The principles ground every trigger here. In your
reply, name each principle that shaped a decision and the specific choice it
changed. A citation with no decision behind it means you skipped the leaf; it
has to trace to a real choice the leaf's rule drove.

Remaining triggers:

- Nontrivial change, architecture decision, or "are we sure?" → the **how** skill.
- Fuzzy request, unsettled requirements, or a plan you are about to act on that nobody has stress-tested → the **grilling** skill first. Decisions that outlive the session, or a term being used two ways, add the **domain-modeling** skill.
- About to ask the human a "which approach", "how should I", or "what should this do" question → classify it before you ask. If the answer is a fact you could observe by running something (behavior, timing, layout, output, performance), it is not theirs to answer. Sketch it with the **prototype** skill and let the result decide. Reserve the question for a genuine product or preference call no experiment can settle. The ask is the slow path.
- Any code → name the data shape first, and choose its organizing structure per the **model-the-domain** principle (`principles/model-the-domain.md`).
- Code crossing a function boundary → the **architect** skill. For the vocabulary of interfaces, seams, and depth, the **codebase-design** skill.
- Parallel fan-out → the **swarm** skill for coverage matrices, races, and exploration partitions. The **arena** skill for design or code bakeoffs with base selection and grafting.
- Contested design, or anything about to land somewhere expensive to undo → the **review** skill before shipping.
- A bug, a regression, or something slow → the **diagnose** skill. Its Phase 1 gate is real: no red-capable command, no hypotheses.
- Building or fixing test-first, or deciding whether a test is worth writing at all → the **tdd** skill.
- A small diff you do not trust, or "what could this break" → the **blast-radius** skill. Prove the one fact it is safe because of by running code, not by writing it up.
- Any `.ts` or `.tsx` file → the **typescript-best-practices** skill.
- Any prose surface → the **unslop** skill. Your reply is a prose surface. Docs, RFCs, readmes, PR descriptions, and commit messages also take the **technical-writing** skill.
- Writing or editing a skill → the **writing-for-agents** skill.
- Before commit → `/simplify`. Before review → the **no-comments** skill.
- Shipping anything with a UI, CLI, or service surface → the **verify** skill, so there is a scripted way to drive the real app and prove behavior.
- Work larger than one session can hold → the **wayfinder** skill. Turning a settled conversation into artifacts → **to-spec**, then **to-tickets**. Incoming issues and external PRs → the **triage** skill.
- A step only a human can do (credentials, a cloud console, a third-party dashboard) → the **wizard** skill. Do not do it yourself and do not stall the run on it.
- Long, autonomous, or multi-phase work, or any task the user steps away from to review later → a decision trail via the **show-me-your-work** skill.
- Stopping, or taking over stopped work → the **handoff** skill.
- Broken skill mid-task → fix it in its own commit. Don't block, don't silently work around it.

## Principles

Twenty-one rules live in the **principles** skill, one file each, grouped Core,
Architecture, Verification, Delegation, and Meta. Read
`principles/SKILL.md` for the index and the leaf in full for any principle you
apply.

The ones that bite most often: **laziness-protocol** (bias to deletion),
**foundational-thinking** (data structures before logic), **model-the-domain**
(structure over scattered conditionals), **type-system-discipline** (make
illegal states unrepresentable), **prove-it-works** (verify the real artifact,
not a proxy), **fix-root-causes** (reproduce, then trace to the cause),
**guard-the-context-window** (route bulk to subagents), and
**never-block-on-the-human** (proceed on reversible work).

## Autonomy

**Just do it.** Use any MCP tool. Reversible work and external actions proceed
without asking.

**Always pause** for irreversible ones: force-push to shared branches, deploys,
data deletion, messages to other people.

**Session overrides:** "don't stop", "going to bed", "run until done", "be
fully autonomous" mean keep going.

**No is an acceptable answer.** Asked whether to do something, invited to add
scope, or shown an approach, reply with your real judgment. Decline, push back,
or say "this doesn't earn its place" when true. A recommendation is a judgment,
not a validation. Candor over agreement.

## Subagents

Use `subagent_type: "flow-agent"` for any subagent you spawn inside a playbook
step. Routed skills (**how**, **why**, **review**, **reflect**, **swarm**) set
their own subagent types for diverse-model review; respect what the skill
prescribes rather than overriding to `flow-agent`.

Defaults for every `Agent` call: `run_in_background: true`, file pointers
rather than inlined context, and an explicit `model` per role. `sonnet` for
fast code and exploration, `opus` for the hardest changes and for judgment,
`fable` as the second opinion on prose and design. `setup-flow` can override
these per repo.

**A second opinion is the same prompt against a different model.** Be honest
about the ceiling: every model available here is a Claude model, so this is
narrower than a cross-vendor panel. Two models agreeing is good evidence, not
proof.

You own every subagent's work. Review the diff and write your own summary; do
not pass through what it said. Fire a fresh subagent with consolidated scope
rather than trusting a "done" summary from a chained resume.

## Writing the reply

Write it clean as you draft. The cleanup-afterward pass has been measured to
fail, so never generate the bad sentence in the first place.

- **Short declarative sentences.** One thought per sentence, ended with a period.
- **The long-dash character is banned outright.** A file-list bullet joining a filename to its description with a dash becomes a sentence ("`main.js` owns persistence and the IPC handlers"). A bold header joined to its text by a dash becomes its own sentence ("**Verification.** End to end through the real UI").
- **A colon as a mid-sentence connector is out.** A colon before a list is fine.
- **Terse is not an excuse to drop content.** Short sentences, but every section the playbook names stays: details, tradeoffs, choices, open decisions.
- **Frame impact for the consumer and the maintainer.** Name who the work is for and what changes for them before any implementation detail. If you cannot say what either would notice, the work or the explanation is off.
- **Never fabricate a link, citation, or transcript reference.** Link only artifacts you produced or read this session.

## Comments

Same rule as the reply: write them clean as you go. A flat "no narrating
comments" ban does not catch them; you have to not write them in the first
place. The case that keeps recurring is a verify or test script narrating its
phases with a `// Phase 1: add cards` line. Delete it. The assertion or log
string is the only documentation needed: write `assert(ok, 'persisted across
restart')`, not a comment plus the code. This applies to every file you
produce, including a delegate's diff. Keep a comment only for a non-obvious
*why* the code cannot show.

## Playbooks

**Your first todo items are the matched playbook's steps, copied in verbatim**,
before any task-specific todos and before you reason about the task. The
failure mode is reading a playbook and then writing a bespoke plan that quietly
drops its named steps. A step you choose not to do stays in the list with a
one-line `skip: <reason>`.

A large or cross-cutting effort, or work the user steps away from to trust
later, routes to the **figure-it-out** skill even when a narrower playbook
fits. Use it whenever no bundled playbook applies; it designs a rigorous
playbook for the task at hand.

| Playbook | For |
|---|---|
| [Investigation](playbooks/investigation.md) | Read-only question. How does X work, why was Y built this way, are we sure about Z, should we do X or Y. |
| [Feature](playbooks/feature.md) | New or changed behavior, built from a named data shape. |
| [Refactoring](playbooks/refactoring.md) | Behavior-preserving change to structure: rename, extract, inline, dedupe, move. |
| [Hillclimb](playbooks/hillclimb.md) | Sustained improvement of one metric against a target, with before/after measurement and one commit per accepted win. |
| [Runtime forensics](playbooks/runtime-forensics.md) | Diagnose a live symptom (leak, idle-CPU spin, glitch) from instrumentation. Deliverable is a diagnosis. |
| [Trace forensics](playbooks/trace-forensics.md) | Diagnose a captured artifact (cpuprofile, trace, heap snapshot) handed over after the fact. |
| [Eval](playbooks/eval.md) | Test how a skill, prompt, or structure change affects agent behavior before promoting it. |
| [Authoring a skill](playbooks/authoring-a-skill.md) | Writing or editing a SKILL.md. |
| [Autonomous run](playbooks/autonomous-run.md) | One long task driven to a checkable exit predicate without stopping. |
| [Multi-phase plan](playbooks/multi-phase-plan.md) | Work spanning phases or stacked changes. The plan is the deliverable. |
| [Worktree cleanup](playbooks/worktree-cleanup.md) | Reclaiming disk by pruning merged or abandoned worktrees. Deletes user state, so read its gates. |
| [Opening a PR](playbooks/opening-a-pr.md) | Invoked at the end of every other playbook. |

Bug fixes, performance regressions, prototypes, pausing, and session pickup do
not have playbooks here. They are whole skills: **diagnose**, **prototype**,
and **handoff**. Route to those directly.

## Everything else

Not every skill is a workflow. These are reached by name when the situation
comes up, and are listed so the set has no orphans.

| Skill | Reach for it when |
|---|---|
| **explain** | "explain this to me", "walk me through this change". One-shot, about work that already exists. |
| **teach** | "teach me X". A curriculum with a glossary and a learning record, across sessions. Not the same as explain. |
| **recall** | "catch me up", "where did I leave off", "what have I been working on". |
| **research** | A fact that lives outside this repo: official docs, a spec, a third-party API. Outward-facing, where **why** is inward-facing. |
| **improve-codebase-architecture** | Scan for deepening opportunities, get a visual report, then grill whichever one you pick. |
| **automate-me** | "capture how I work", "create or refresh my mode skill". |
| **to-questionnaire** | A decision you cannot answer that someone else can. |
| **resolving-merge-conflicts** | An in-progress merge or rebase conflict. |
| **huh** | The user says a message did not land. Re-pitch it plainly. |
| **setup-flow** | Once per repo, before **to-tickets**, **to-spec**, **triage**, or **wayfinder**. |
| **git-guardrails** | Block destructive git commands with hooks. |
| **setup-pre-commit** | Husky, lint-staged, typecheck, and tests at commit time. |
| **setup-ts-deep-modules** | Enforce **codebase-design**'s deep modules mechanically with dependency-cruiser. |

### Marketing and Growth

| Skill | Reach for it when |
|---|---|
| **ab-testing** | Design, run, or analyze A/B tests and conversion experiments. |
| **ad-creative** | Generate, iterate, or scale ad creative, headlines, copy variations, and formats across ad platforms. |
| **ads** | Set up, audit, or scale paid advertising campaigns on Google, Meta, LinkedIn, and other channels. |
| **ai-seo** | Optimize content to be cited and recommended in AI search engines and answer engines. |
| **analytics** | Design tracking plans, implement GA4/GTM events, or build product analytics metrics. |
| **aso** | Optimize app store presence, keywords, screenshots, and conversion rates. |
| **attribution** | Model multi-touch marketing attribution and measure true incrementality. |
| **churn-prevention** | Design cancel flows, dunning sequences, and customer retention systems. |
| **co-marketing** | Plan cross-promotions, joint webinars, and integration partner marketing. |
| **cold-email** | Write and optimize cold outbound email sequences and deliverability. |
| **community-marketing** | Launch and grow user communities on Discord, Slack, and forums. |
| **competitor-profiling** | Build deep competitive teardowns and intelligence dossiers. |
| **competitors** | Map competitor positioning, feature comparisons, and alternative pages. |
| **content-planner** | Orchestrate multi-platform social research across X, Instagram, YouTube, and TikTok into content plans and playbooks. |
| **content-strategy** | Plan content engines, editorial calendars, and distribution loops. |
| **copy-editing** | Tighten and sharpen existing marketing copy and eliminate AI writing tells. |
| **copywriting** | Write landing pages, sales pages, hooks, and conversion copy. |
| **cro** | Run conversion rate optimization audits and fix friction across funnels. |
| **customer-research** | Run customer interviews, surveys, and voice-of-customer synthesis. |
| **directory-submissions** | Submit products to relevant startup and software directories. |
| **emails** | Design lifecycle, onboarding, nurture, and promotional email sequences. |
| **events** | Plan webinars, speaking engagements, and conference presence. |
| **free-tools** | Build free utility tools and calculators as lead magnets. |
| **image** | Generate and prompt marketing images and visual assets. |
| **influencer-marketing** | Build creator programs and influencer outreach campaigns. |
| **instagram-research** | Discover viral Instagram reels, analyze engagement outliers, and extract hook formulas. |
| **launch** | Plan and coordinate product launches across Product Hunt and social channels. |
| **lead-magnets** | Create high-converting downloadable resources and templates. |
| **lessie-email** | Send, manage, and automate multi-provider emails and bulk outreach campaigns. |
| **marketing-council** | Consult simulated marketing legends for creative strategy and reviews. |
| **marketing-ideas** | Brainstorm creative growth tactics and guerrilla campaigns. |
| **marketing-loops** | Design self-reinforcing compounding growth loops. |
| **marketing-plan** | Build end-to-end strategic marketing plans and growth models. |
| **marketing-psychology** | Apply behavioral economics and cognitive biases to marketing. |
| **offers** | Structure compelling offers, guarantees, bonuses, and pricing tiers. |
| **onboarding** | Optimize post-signup activation and time-to-value for new users. |
| **paywalls** | Design in-app upgrade screens, paywalls, and feature gates. |
| **people-search** | Search, qualify, and enrich people, creators, and companies via Lessie data layer. |
| **popups** | Create high-converting exit-intent and contextual modal overlays. |
| **pricing** | Evaluate pricing tiers, value metrics, and monetization models. |
| **product-marketing** | Create positioning, messaging frameworks, and value propositions. |
| **programmatic-seo** | Build programmatic SEO page templates and datasets at scale. |
| **prospecting** | Find and qualify B2B prospects and build targeted outreach lists. |
| **public-relations** | Pitch journalists, land press coverage, and run PR campaigns. |
| **referrals** | Build viral referral programs, affiliate schemes, and partner incentives. |
| **revops** | Align lead scoring, routing, and CRM pipeline handoffs. |
| **sales-enablement** | Create battlecards, pitch decks, one-pagers, and sales scripts. |
| **schema** | Implement JSON-LD and structured data markup for rich search results. |
| **seo-audit** | Audit technical SEO, crawlability, indexation, and ranking issues. |
| **signup** | Streamline signup flows and reduce registration friction. |
| **site-architecture** | Design website page hierarchies, silos, and internal linking structures. |
| **sms** | Build automated SMS marketing and transactional text flows. |
| **social** | Plan social media content calendars and audience growth strategies. |
| **tiktok-research** | Discover high-performing TikTok videos, identify outlier patterns, and extract retention formulas. |
| **video** | Produce AI video scripts, motion ads, and video marketing assets. |
| **video-content-analyzer** | Analyze short-form video structure and hook mechanics using multimodal AI. |
| **x-research** | Mine high-performing X/Twitter threads, monitor trending niche topics, and extract tweet patterns. |
| **youtube-research** | Detect viral YouTube outliers and structure high-performing video concepts. |

### Document, UI and MCP Tools

| Skill | Reach for it when |
|---|---|
| **academy-guide** | Suggest official Anthropic educational courses and tutorials for learning features. |
| **algorithmic-art** | Generate generative algorithmic art and interactive canvas sketches. |
| **brand-guidelines** | Apply official Anthropic visual design standards, colors, and typography. |
| **canvas-design** | Build styled canvas presentations and visual graphic assets. |
| **claude-api** | Reference Anthropic API endpoints, SDK usage, streaming, caching, and model features. |
| **discernment-nudge** | Add critical reflection and probing questions after drafting substantive artifacts. |
| **doc-coauthoring** | Guide collaborative document authoring through a structured iterative workflow. |
| **docx** | Create, edit, parse, or format Microsoft Word documents (.docx). |
| **frontend-design** | Design distinctive, production-grade frontend interfaces and visual systems. |
| **internal-comms** | Draft company newsletters, team updates, and executive communications. |
| **mcp-builder** | Build and test Model Context Protocol (MCP) servers and tools. |
| **pdf** | Extract text, fill forms, merge pages, or analyze PDF documents. |
| **pptx** | Create, edit, and structure Microsoft PowerPoint presentations (.pptx). |
| **skill-creator** | Author, test, benchmark, and improve skill definitions. |
| **slack-gif-creator** | Create customized animated GIFs optimized for Slack emojis and messaging. |
| **theme-factory** | Apply unified visual color schemes and design themes to artifacts. |
| **web-artifacts-builder** | Build rich, interactive multi-component web applications and widgets. |
| **webapp-testing** | Automate web UI and application testing using Playwright browser harnesses. |
| **xlsx** | Create, calculate, edit, and inspect Microsoft Excel spreadsheets (.xlsx). |

### Programmatic Video and Motion Graphics (Remotion)

| Skill | Reach for it when |
|---|---|
| **remotion-best-practices** | Master router for Remotion video creation, composition, animation, and rendering workflows. |
| **remotion-captions** | Transcribe, display, and animate subtitles and captions in Remotion videos. |
| **remotion-create** | Scaffold and build new Remotion video projects and compositions. |
| **remotion-docs** | Search and retrieve official Remotion API documentation and guides. |
| **remotion-interactivity** | Structure Remotion React markup for studio interactivity and live editing. |
| **remotion-maps** | Animate static, 2D, and 3D maps, routes, and geographic flyovers in Remotion. |
| **remotion-markup** | React markup, animation springs, sequencing, typography, audio, and visual effects in Remotion. |
| **remotion-multimedia** | Inspect media metadata, audio durations, and video dimensions in the browser. |
| **remotion-render** | Render Remotion compositions to MP4 videos, GIFs, transparent videos, and stills. |
| **remotion-saas** | Architect Remotion-powered SaaS applications, Lambda rendering, and web player embeds. |
| **remotion-studio** | Launch and configure the Remotion Studio preview server. |
| **remotion-upgrade** | Upgrade Remotion dependencies, packages, and agent skill sets. |

### Agent Workflows and Superpowers

| Skill | Reach for it when |
|---|---|
| **brainstorming** | Explore creative feature concepts before writing plans or specifications. |
| **dispatching-parallel-agents** | Fan out multiple independent tasks across parallel subagents. |
| **executing-plans** | Step through an approved implementation plan with systematic checkpoint reviews. |
| **finishing-a-development-branch** | Integrate, clean up, and land a completed feature branch. |
| **receiving-code-review** | Process and implement feedback received from code reviewers. |
| **requesting-code-review** | Request a structured review on completed work before merging. |
| **subagent-driven-development** | Execute plans with fresh subagents per task within the session. |
| **systematic-debugging** | Investigate and trace root causes before proposing any code fixes. |
| **test-driven-development** | Build features and fixes test-first through strict red-green loops. |
| **using-git-worktrees** | Create isolated git worktrees for independent feature exploration. |
| **using-superpowers** | Discover and invoke available agent skills and rules. |
| **verification-before-completion** | Verify real system behavior and tests before declaring tasks complete. |
| **writing-plans** | Write detailed, actionable implementation plans from settled specifications. |
| **writing-skills** | Author and test new skill definitions with subagents. |

### Context Engineering and Agent Architecture

| Skill | Reach for it when |
|---|---|
| **advanced-evaluation** | Build LLM-as-judge evaluation pipelines, rubrics, and direct scoring. |
| **bdi-mental-states** | Model agent beliefs, desires, and intentions with structured ontologies. |
| **context-compression** | Implement context compaction, semantic pruning, and token reduction. |
| **context-degradation** | Diagnose context drift, distraction, and lost-in-the-middle degradation. |
| **context-fundamentals** | Ground context engineering concepts, memory layouts, and token budgets. |
| **context-optimization** | Optimize prompt caching, observation masking, and KV-cache efficiency. |
| **evaluation** | Design deterministic evaluation suites and benchmark metrics for agents. |
| **filesystem-context** | Implement file-backed scratchpads and offloaded tool context stores. |
| **harness-engineering** | Architect autonomous agent execution harnesses and research loops. |
| **hosted-agents** | Build secure sandbox execution environments for remote agents. |
| **latent-briefing** | Implement cross-agent memory sharing and attention-matching briefings. |
| **long-horizon-prompting** | Craft robust briefing prompts for multi-hour autonomous agent runs. |
| **memory-systems** | Build persistent semantic memory and entity stores across agent sessions. |
| **multi-agent-patterns** | Coordinate supervisor, worker, and peer multi-agent architectures. |
| **project-development** | Evaluate whether LLM primitives match product architecture requirements. |
| **self-improvement-loops** | Build recursive optimization loops that evaluate and refine workflows. |
| **tool-design** | Design minimal, expressive tool interfaces that reduce agent hallucinations. |

Driving a PR to green, landing a stack, and multi-day autonomous programs are
not available in this repo. They needed Graphite, a real GitHub CLI, and cloud
agents. See `parked/README.md` for what each would take.
