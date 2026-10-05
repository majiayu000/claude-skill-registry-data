---
name: agent-directory
description: Discover and invoke any of 69 specialist agents. All agents are latent (not loaded at startup) and activated on demand via the pimp router. Use this skill before delegating any specialised task.
---

# Agent Directory

All 69 specialist agents live in `~/.config/opencode/agent-latent/`. Only **pimp** is loaded at startup — it routes to any specialist on demand by reading their prompt from disk.

## How to Invoke Any Specialist

```typescript
task(
  subagent_type="pimp",
  load_skills=[],
  run_in_background=false,
  description="<brief description>",
  prompt="Use specialist: <Exact Name>. Task: <your task>"
)
```

pimp reads the specialist's full system prompt at runtime and fully adopts their persona. No restart needed. No file moves.

## Full Agent Catalog

### Engineering & Architecture
| Name | Use when... |
|------|-------------|
| `Backend Architect` | System design, DB schema, APIs, microservices, AWS/K8s architecture |
| `Senior Developer` | Complex full-stack implementation, premium craftsmanship |
| `Frontend Developer` | React, TypeScript, component architecture, state management |
| `DevOps Automator` | Terraform, Helm, K8s, GitHub Actions, ArgoCD, EKS, CI/CD |
| `Infrastructure Maintainer` | Reliability, monitoring, cost optimisation, performance analysis |
| `Security Engineer` | Threat modeling, IAM, secrets, auth flows, vulnerability review |
| `Data Engineer` | ETL, pipelines, Postgres/SQL optimisation, schema design |
| `Performance Benchmarker` | Profiling, bottlenecks, benchmark design |
| `AI Engineer` | ML model dev, Bedrock/AI integration, AI-powered features |
| `LSP/Index Engineer` | LSP, code intelligence systems, semantic indexing |
| `API Tester` | API validation, endpoint testing, performance QA |
| `Autonomous Optimization Architect` | API perf shadow-testing, cost guardrails |
| `Agentic Identity & Trust Architect` | AI agent auth, agent identity, multi-agent trust |
| `Agents Orchestrator` | Complex multi-agent pipeline orchestration |

### Quality & Review
| Name | Use when... |
|------|-------------|
| `Code Reviewer` | PR review, code quality, pattern consistency, tech debt |
| `Technical Writer` | Docs, README, architecture docs, API reference, runbooks |
| `Reality Checker` | Evidence-based production certification, skeptical review |
| `Evidence Collector` | QA with visual proof, screenshot-based evidence |
| `Test Results Analyzer` | Test result evaluation, CI test analysis |
| `Rapid Prototyper` | Fast POC, MVP creation |

### Platform & Mobile
| Name | Use when... |
|------|-------------|
| `Mobile App Builder` | iOS/Android native, React Native, cross-platform |
| `macOS Spatial/Metal Engineer` | Swift, Metal, 3D rendering, macOS/Vision Pro |
| `visionOS Spatial Engineer` | visionOS, SwiftUI volumetric, Liquid Glass |
| `Terminal Integration Specialist` | Terminal emulation, SwiftTerm |
| `XR Immersive Developer` | WebXR, browser-based AR/VR/XR |
| `XR Cockpit Interaction Specialist` | XR cockpit UI, immersive control systems |
| `XR Interface Architect` | Spatial interaction design, AR/VR/XR interfaces |

### Design & UX
| Name | Use when... |
|------|-------------|
| `UI Designer` | Visual design systems, component libraries, pixel-perfect UI |
| `UX Architect` | UX architecture, CSS systems, design foundations |
| `UX Researcher` | Usability testing, user behaviour analysis |
| `Accessibility Auditor` | WCAG audits, a11y testing, screen reader compatibility |
| `Inclusive Visuals Specialist` | Anti-bias image generation, culturally accurate visuals |
| `Image Prompt Engineer` | AI image generation prompts |
| `Whimsy Injector` | Brand personality, delight, playful interactions |
| `Visual Storyteller` | Visual narratives, multimedia content |

### Data, Analytics & Business
| Name | Use when... |
|------|-------------|
| `Analytics Reporter` | Dashboards, KPI tracking, statistical analysis |
| `Data Analytics Reporter` | Datadog/analytics reporting, KPI dashboards |
| `Executive Summary Generator` | McKinsey/BCG exec summaries, C-suite communication |
| `Finance Tracker` | Financial planning, budget management |
| `Experiment Tracker` | A/B test design, experiment tracking |
| `Tool Evaluator` | Technology assessment, tool comparison |
| `Trend Researcher` | Emerging trends, competitive analysis |
| `Data Consolidation Agent` | Sales data consolidation, live dashboards |
| `Sales Data Extraction Agent` | Excel sales metrics, MTD/YTD reporting |
| `Report Distribution Agent` | Automated report distribution |

### Compliance & Legal
| Name | Use when... |
|------|-------------|
| `Legal Compliance Checker` | PCI DSS, GDPR, SOC2, ISO 27001, legal review |
| `Cultural Intelligence Strategist` | Inclusive design, anti-bias, cultural context |

### Project & Product Management
| Name | Use when... |
|------|-------------|
| `Project Shepherd` | Cross-functional PM, timeline, stakeholder alignment |
| `Senior Project Manager` | Spec-to-tasks, realistic scope |
| `Sprint Prioritizer` | Sprint planning, backlog grooming, velocity |
| `Feedback Synthesizer` | User feedback analysis, product insights |
| `Workflow Optimizer` | Process improvement, workflow automation |
| `Studio Producer` | Creative/technical portfolio, multi-project management |
| `Studio Operations` | Day-to-day studio efficiency |
| `Behavioral Nudge Engine` | UX motivation design, behavioural psychology |

### Growth & Marketing
| Name | Use when... |
|------|-------------|
| `Growth Hacker` | User acquisition, viral loops, conversion funnels |
| `Social Media Strategist` | LinkedIn/Twitter campaigns, thought leadership |
| `Content Creator` | Multi-platform content, copywriting |
| `Brand Guardian` | Brand identity, consistency |
| `App Store Optimizer` | ASO, app store conversion |
| `Developer Advocate` | Developer community, DX, technical content |
| `Support Responder` | Customer support, issue resolution |
| `Twitter Engager` | Twitter engagement, thread creation |
| `Reddit Community Builder` | Reddit marketing, community engagement |
| `Instagram Curator` | Instagram content, visual storytelling |
| `TikTok Strategist` | TikTok content, viral growth |
| `Xiaohongshu Specialist` | Xiaohongshu content, lifestyle marketing |
| `WeChat Official Account Manager` | WeChat OA strategy, subscriber engagement |
| `Zhihu Strategist` | Zhihu thought leadership |

---

## Examples

```typescript
// Compliance review
task(subagent_type="pimp", load_skills=[], run_in_background=false,
  description="PCI DSS review",
  prompt="Use specialist: Legal Compliance Checker. Task: review this Terraform IAM config for PCI DSS...")

// Let pimp choose the best specialist
task(subagent_type="pimp", load_skills=[], run_in_background=false,
  description="UX audit",
  prompt="Our onboarding flow has 60% drop-off at step 3. Identify UX issues.")
```
