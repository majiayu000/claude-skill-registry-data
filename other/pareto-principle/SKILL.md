---
name: pareto-principle
description: Isolate the 20% of inputs driving 80% of results, and explicitly name what you're deprioritizing. Outputs a blockquote (vital 20%) plus a list (deprioritized 80%). Use for ruthless prioritization, "what should we focus on", or step 4 of a strategic analysis.
---

# Pareto Principle (80/20)

## Concept

In most systems, ~80% of the outcome comes from ~20% of the inputs. Strategy consultants use this constantly: figure out which 20% of customers, products, channels, or root causes drive the lion's share of impact, and ignore the rest until later.

The discipline isn't naming the vital 20%. It's having the spine to **explicitly deprioritize the 80%**. If everything is important, nothing is.

## Required output format

Two parts, in this order:

1. A Markdown blockquote naming the vital 20%.
2. A bulleted list under "Actively deprioritized (the 80%):" naming what's being set aside.

```markdown
> **The vital 20%:** [Specific factors/segments/causes that drive the majority of impact.]

**Actively deprioritized (the 80%):**
- Item 1
- Item 2
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| 1–4 items in the vital 20% | If the 80/20 genuinely points to one thing, use one. Don't pad. |
| 5–10 items in the deprioritized list | List enough to make the deprioritization visible — but if there are only 3 real alternatives, list 3. |
| Specificity in the vital 20% | Don't flex — "our top customers" is too vague. Name them. |
| Explicit deprioritization | Don't flex — implicit deprioritization is no deprioritization. |

**The hardest discipline:** writing down something that genuinely matters into the deprioritized list. If your 80% list is full of things that don't matter, you haven't really prioritized. Real Pareto says: "Yes, X matters. We're not doing X this quarter."

## Example — engineering tech debt

**Problem:** A mid-stage SaaS engineering team has 47 tracked tech-debt items. Leadership wants a focused six-month plan.

> **The vital 20%:** Three items account for ~80% of incident pain and velocity drag: (1) the legacy auth middleware causing 60% of P2 tickets and forcing every new feature to add custom session handling, (2) the deploy pipeline averaging 47 minutes (preventing the team's stated daily-deploy cadence), and (3) the absence of integration tests on the billing module (the source of 4 of the last 6 customer-impacting incidents).

**Actively deprioritized (the 80%):**
- Migrating the frontend from React 17 to React 18 (real, but no business pull)
- Refactoring the admin dashboard (technically owed but low-traffic surface)
- Rewriting the email templating system (works fine, just ugly)
- Splitting the monolith into services (premature for current scale)
- Upgrading the logging library (operational only, no incidents tied to it)
- Switching ORMs (engineer preference, not business need)
- Modernizing the build tool (current setup works, savings minimal)

Notice: several deprioritized items are real concerns. The point is naming them as **not-this-half** so the team has cover to focus.

## Common mistakes

- **The "everything is 20%" cop-out.** A list of 12 priorities labeled "vital 20%" is just a backlog with extra steps.
- **Implicit deprioritization.** Mentally noting what you're not doing isn't the same as writing it down. Stakeholders will assume you're doing everything.
- **Soft language.** "We could consider focusing on..." dilutes the point. The blockquote is a commitment.
- **Deprioritizing trivial things.** If everything in your 80% list is obvious filler, the framework isn't biting.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user has a long list of options and needs to commit to a few.
- **As part of full analysis:** `strategy-consultant` — Pareto is step 4 of 5. Run `mece-framework` and `issue-trees` first to enumerate the 100% before you can isolate the 20%.

---

## Acknowledgment & License

Adapted from **Analyst Academy** on YouTube — [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
