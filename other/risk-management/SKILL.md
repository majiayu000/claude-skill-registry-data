---
name: risk-management
description: Risk identification, assessment, and mitigation at every pipeline phase.
---

# Risk Management

## Risk Matrix
| Likelihood → | Low | Medium | High |
|Impact ↓|---|---|---|
| **High** | Monitor | Mitigate | Block |
| **Medium** | Accept | Monitor | Mitigate |
| **Low** | Accept | Accept | Monitor |

## Common Risks by Phase

### Intake
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Vague requirements | High | High | Ask Nick clarifying questions BEFORE starting pipeline |
| Scope too large for appetite | Medium | High | Break into phases. Ship v1, iterate. |

### Research
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Market already saturated | Medium | High | Scout's demand validation score catches this |
| No clear ICP | Medium | Medium | Require ICP before moving to design |

### Design
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| V0 generates off-brand output | Medium | Medium | Pixel iterates. Max 3 attempts per screen. |
| Too many screens for appetite | Medium | High | Scope hammer — cut to core screens only |

### Build
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Maks deviates from design | High | Medium | Require Maks to reference Pixel's V0 preview |
| Complex feature (auth, payments) | Medium | High | Flag at intake. Have Forge pre-review architecture. |
| Build runs over time | Medium | Medium | Scope hammer at 60% of time budget |

### Review
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Forge blocks repeatedly | Low | High | Circuit breaker: 3 loops max, then escalate |
| Security vulnerability found | Low | Critical | Fix before ship. No exceptions on P0 security. |

### QA
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Animation/JS bug hides content | Medium | High | Test with JS disabled as baseline |
| Images fail to load | Medium | Medium | Prefer local assets over external CDN |
| Responsive breakpoints broken | Medium | Medium | Test at 375px, 768px, 1280px every round |

### Launch
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Product not differentiated | Medium | High | Scout's research should catch this at research phase |
| Launch materials generic | Low | Medium | Launch has 10 skills — provide good context |

## Pre-Mortem (run at Intake for complex projects)
Before starting, ask: "If this project fails, why?"
- Write down 3 most likely failure modes
- For each: what would you do to prevent it?
- Build those preventions into the plan

## Lessons Learned
- **Brew & Bean (2026-03-20):** Scroll animation (useScrollReveal) hid all sections. Took 3 QA rounds to fix. Lesson: always test with animations disabled as baseline. Require CSS fallback for any JS-driven visibility.
- **Brew & Bean (2026-03-20):** External CDN images (apiframe.pro) intermittently failed through Next.js optimization. Lesson: download images to local assets for production.

## Changelog
- 2026-03-20: Initial risk management framework
- 2026-03-20: Added QA risks and lessons learned from Brew & Bean
