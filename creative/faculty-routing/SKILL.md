---
name: faculty-routing
description: Route a learning request to the smallest useful set of Academy professors or instructors based on subject, level, and goal.
---
# Faculty Routing

Identify the primary subject and the learner's intended outcome. Prefer one specialist when one specialist can teach the bounded objective well. Add another faculty member only outside Continuing Education when the user genuinely asks for a multi-faculty curriculum; one Continuing Education event still has one learner, one bounded objective, and one instructor.

Prefer the most specific installed Academy faculty member before a broad faculty fallback. A clearly physics-specific request routes to `academy-physics-professor`, chemistry to `academy-chemistry-professor`, and biology to `academy-biology-professor`. Keep `academy-natural-sciences-professor` for interdisciplinary natural science, general scientific reasoning, or science learning that genuinely spans those science specialties.

Use the same specific-over-broad rule for statistics, data science, philosophy, law and legal studies, theology and religious studies, education and pedagogy, cybersecurity, cloud and systems, project management, automotive, culinary arts, and music when the dedicated faculty member is installed.

## Profile Learner Routing

When another Hermes profile requests Continuing Education, apply this policy to the newest routing request only.

1. **Input contract.** Accept only the learner profile name, learner role, one requested objective, and optionally relevant skill names/descriptions. Never request or accept full profile state, memory, secrets, credentials, or unrelated conversation history.

2. **Specialist preference first.** Resolve a clear domain to the most specific installed faculty member. Use the Academy roster as the allowed namespace. Never infer a profile name outside that roster.

3. **Same-category interdisciplinary fallback.** When the objective clearly spans multiple specialties that all belong to one Academy category, choose that category's installed broad faculty member and mark the route approximate. The broad representatives are:
   - quantitative → `academy-mathematics-professor`
   - communication → `academy-writing-rhetoric-professor`
   - science → `academy-natural-sciences-professor`
   - technology → `academy-computer-science-professor`
   - humanities → `academy-history-professor`
   - social sciences → `academy-social-sciences-professor`
   - professional → `academy-business-professor`
   - languages → `academy-language-instructor`
   - research → `academy-research-methods-professor`
   - vocational → `academy-skilled-trades-instructor`
   - health sciences → `academy-health-sciences-professor`
   - creative → `academy-arts-design-instructor`

   A broad faculty member is a category fallback, not a universal fallback. In particular, never route an unrelated cross-domain request to Natural Sciences merely because `academy-natural-sciences-professor` is a broad chair.

4. **Cross-category objectives fail closed.** If one request strongly spans different Academy categories, do not arbitrarily choose one faculty member. Ask the learner to narrow the competency or name the instructor it wants. A Continuing Education session must not hide multiple unrelated competencies inside one route.

5. **Missing specialist fallback.** If the objective clearly maps to a specialist that is not installed, use the installed broad representative for that specialist's category when one is available. Mark the route approximate. If neither the specialist nor its safe category fallback is available, report no safe installed match.

6. **Role-description fallback.** Only when no clear specialist topic exists, compare meaningful objective words against the roles of installed faculty. Require at least two meaningful exact-word overlaps for an approximate fallback. If multiple faculty are equally plausible, do not break the tie by roster order; ask for a narrower objective instead.

7. **Availability is evidence, not assumption.** Return a faculty profile as installed only when current Hermes Bot/profile context establishes that it is available. If current availability cannot be established, state the candidate but mark the route blocked rather than claiming that the profile is installed.

8. **Never invent.** If no installed faculty member is a safe match, say so. Never fabricate a faculty member, silently substitute an unrelated broad chair, or claim a Dean recommendation that was not actually produced in this conversation.

9. **Label approximation.** Always tell the learner whether the match is exact, approximate, or blocked. An approximate match means the faculty member covers the safe broad category but may not own the narrow specialty.

For a successful route, reply compactly with the exact profile name so the learner can use it without interpretation:

```text
FACULTY: academy-cybersecurity-instructor
MATCH: exact
REASON: Direct specialist for the requested cybersecurity competency.
```

For a blocked route:

```text
FACULTY: NONE
MATCH: blocked
REASON: The objective crosses multiple Academy categories; narrow the competency or choose an instructor.
```

## Reference implementation boundary

The Profile Packs repository contains `hermes-academy/routing.py` as a deterministic policy reference and regression-test oracle for maintainers. It is **not** a runtime dependency of the installed Dean profile and must not be assumed to exist after profile installation. The installed Dean enforces the routing contract in this preloaded skill against the actual faculty/Bot availability exposed by Hermes.

This boundary is deliberate: Academy does not add a routing daemon, message bus, scheduler, or second agent runtime merely to choose a teacher.
