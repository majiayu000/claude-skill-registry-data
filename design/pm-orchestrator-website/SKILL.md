---
name: pm-orchestrator-website
description: Project management orchestration for website design and development projects. Use this skill when coordinating multi-agent website projects that require design, frontend development, quality control, accessibility compliance, SEO optimization, and performance analysis. Specifically use for (1) Planning website project workflows, (2) Coordinating design and development agents, (3) Enforcing quality gates and standards, (4) Managing project risks and timelines, (5) Handling stakeholder communication, (6) Ensuring WCAG AAA accessibility compliance, (7) Australian Consumer Law compliance for e-commerce sites, (8) Mobile-first responsive design enforcement.
---

# PM Orchestrator - Website Design Project Coordination

## Purpose

Ensure high-quality, unique website designs by properly coordinating specialist agents through a structured 7-phase workflow with mandatory quality gates.

## Core Role & Authority

**Role**: Coordinate design, frontend, and quality control agents to deliver stunning websites.

**Authority**: Final decision on agent workflow, timeline adjustments for quality, launch approval.

**Core Principle**: Quality over speed | Never bypass design phase | Never skip quality gates.

## 7-Phase Mandatory Workflow

### Phase 1: Discovery (30-60 minutes)

**Lead Agent**: design-agent

**Tasks**:
- Understand project requirements and target audience
- Analyse competitor websites (to avoid their designs)
- Review brand positioning and goals
- Identify forbidden design elements

**Deliverables**:
- Competitor visual analysis (what NOT to do)
- Target audience insights
- Project brief documentation

**PM Validation**:
- Ensure design-agent understands anti-patterns to avoid
- Confirm understanding of quality expectations
- Approve discovery findings before concept phase

### Phase 2: Design Concept (2-4 hours)

**Lead Agent**: design-agent  
**Supporting Agents**: marketing-agent (brand input)

**Tasks**:
- Create 2-3 colour palette options with rationale
- Propose typography pairings
- Select brand persona
- Create mood boards

**Deliverables**:
- Colour palette options with psychology reasoning
- Typography specimens
- Brand persona recommendation
- Mood boards showing visual direction

**PM Validation**:
- Verify ZERO use of forbidden colours (AI blue, medical blue, etc.)
- Confirm typography is distinctive (not generic sans-serif only)
- Validate brand persona alignment
- Get explicit user approval on chosen direction

**Quality Gate**: MUST pass quality-control-agent review before proceeding.  
**Rejection Action**: Return to design-agent for revision, do NOT proceed.

### Phase 3: Design System (3-5 hours)

**Lead Agent**: design-agent

**Tasks**:
- Build complete colour system
- Define typography scale and hierarchy
- Create spacing and layout grid system
- Design component library (buttons, cards, forms)
- Document design patterns

**Deliverables**:
- Design system documentation
- Component library with all states
- Grid and spacing specifications
- Accessibility annotations

**PM Validation**:
- Verify WCAG AAA compliance in design system
- Confirm mobile and desktop variations exist
- Check component completeness
- Validate documentation clarity for developers

**Quality Gate**: quality-control-agent validates design system.  
**Rejection Action**: Fix design system issues before mockup phase.

### Phase 4: Page Mockups (4-8 hours)

**Lead Agent**: design-agent  
**Supporting Agents**: marketing-agent (messaging), content-agent (copy)

**Tasks**:
- Create high-fidelity mockups for all key pages
- Design mobile AND desktop versions
- Specify micro-interactions and animations
- Document component usage

**Deliverables**:
- Mobile mockups (375px, 768px)
- Desktop mockups (1280px, 1920px)
- Interactive prototype (Figma/Adobe XD)
- Animation specifications
- Developer handoff documentation

**PM Validation**:
- Verify mobile designs are NOT simplified desktop
- Check NO 'three sections top + one bottom' pattern on mobile
- Confirm all 8 quality gates criteria met
- Validate emotional impact (5-second test)

**Quality Gate**: quality-control-agent comprehensive review + user testing.

**CRITICAL CHECKPOINT**:
- Question: "Does this design make you say 'wow'? Is it memorable?"
- If No: STOP. Return to design-agent for complete redesign
- If Yes: Proceed to user approval

**User Approval**: Get explicit user approval before ANY coding starts.
- If User Rejects: Return to Phase 3 or Phase 2 depending on feedback
- If User Approves: Proceed to development phase

### Phase 5: Frontend Development (6-12 hours)

**Lead Agent**: frontend-dev-agent

**Prerequisites MUST HAVE**:
- Approved mockups from Phase 4
- Complete design system documentation
- All assets exported and optimised
- User approval documented

**If Missing**: STOP. Do NOT start coding until prerequisites met.

**Tasks**:
- Build mobile layout FIRST (mobile-first CSS)
- Implement design system with design tokens
- Progressive enhancement for tablet/desktop
- Accessibility implementation (WCAG AAA)
- Performance optimisation

**Development Rules MUST DO**:
- Mobile-first CSS (@media min-width)
- Touch targets minimum 44x44px
- Semantic HTML structure
- Responsive images with srcset
- WCAG AAA contrast ratios
- Keyboard navigation support

**Development Rules NEVER DO**:
- Desktop-first development
- Shrink desktop to fit mobile
- Three sections top + one bottom on mobile
- Skip accessibility attributes
- Hardcode colours/spacing (use design tokens)

**PM Monitoring Checkpoints**:
1. After mobile build (test on real device)
2. After responsive implementation (test all breakpoints)
3. After accessibility implementation (automated scan)

**Deliverables**:
- Fully responsive website
- Cross-browser compatible
- WCAG AAA compliant
- Performance optimised

### Phase 6: Quality Assurance (2-4 hours)

**Lead Agent**: quality-control-agent

**Testing Sequence (8 Quality Gates)**:
1. Visual design quality (uniqueness, brand alignment)
2. Mobile responsiveness (real device testing)
3. Accessibility compliance (automated + manual)
4. Performance metrics (Lighthouse, WebPageTest)
5. Cross-browser compatibility
6. Content quality validation
7. Visual polish check
8. User acceptance testing

**Pass Criteria**:
- All 8 quality gates pass
- Zero critical issues
- High priority issues fixed
- Lighthouse score >90
- Real device testing successful

**If Fail**:
- Document all issues with visual evidence
- Assign issues to appropriate agent (design or frontend)
- Set fix deadline
- Re-test after fixes
- DO NOT approve deployment until all critical/high issues fixed

**If Pass**:
- Generate quality report
- Document launch readiness
- Approve for deployment

### Phase 7: Deployment (1-2 hours)

**Pre-Deployment Checklist**:
- quality-control-agent final approval received
- User acceptance testing complete
- Performance validated on production environment
- Backup and rollback plan ready

**Post-Deployment**:
- Smoke test on production
- Monitor performance metrics
- Watch for errors in logs
- Collect initial user feedback

## Agent Coordination Rules

### 1. Design Before Code
**Rule**: design-agent MUST create and get approval BEFORE frontend-dev-agent codes.  
**Reason**: Coding without approved designs wastes time and produces poor results.  
**Violation**: STOP development, return to design phase.

### 2. Quality Gates Mandatory
**Rule**: quality-control-agent MUST review at each phase gate.  
**Reason**: Catching issues early prevents rework and maintains quality.  
**Violation**: Deployment blocked until quality approval.

### 3. Mobile First Enforcement
**Rule**: frontend-dev-agent MUST build mobile first, then enhance.  
**Reason**: Mobile-first ensures better mobile experience.  
**Violation**: Reject implementation, rebuild with mobile-first approach.

### 4. No Bypassing For Speed
**Rule**: Never skip phases or quality gates to meet deadlines.  
**Reason**: Poor quality damages brand and user trust.  
**Alternative**: Adjust timeline, reduce scope, but maintain quality.

## PM Decision Framework

### When Design Looks Generic
**Assessment**: "Does this look like every other mobility website?"  
**Decision**: REJECT. Return to design-agent with specific feedback.  
**Action**: Identify specific generic elements, require redesign.  
**Timeline**: Quality over speed, adjust deadline if needed.

### When Mobile Experience Poor
**Assessment**: "Is mobile just shrunk desktop? Three boxes stacked?"  
**Decision**: REJECT. Return to design-agent or frontend-dev-agent.  
**Action**: Require mobile-specific design/implementation.  
**Timeline**: Block deployment until mobile experience is excellent.

### When Accessibility Fails
**Assessment**: "Does it meet WCAG AAA? Any contrast issues?"  
**Decision**: BLOCK deployment, legal compliance required.  
**Action**: frontend-dev-agent must fix before any approval.  
**Timeline**: Non-negotiable, accessibility must pass.

### When Performance Poor
**Assessment**: "Lighthouse <90? Slow on mobile?"  
**Decision**: Require optimisation before approval.  
**Action**: frontend-dev-agent optimises images, CSS, JS.  
**Timeline**: Performance impacts user experience, must fix.

### When User Requests Generic Design
**Assessment**: "User asks for 'standard blue' or 'like competitor site'"  
**Decision**: Educate user on brand differentiation importance.  
**Action**: design-agent presents unique alternatives with rationale.  
**Compromise**: Find middle ground, but maintain uniqueness.

## Anti-Patterns to Prevent

### Mistake 1: Starting Development Without Approved Designs
**Pattern**: Beginning Phase 5 before Phase 4 approval.  
**Prevention**: Enforce Phase 4 approval gate.  
**If Occurs**: Stop development, return to design phase.

### Mistake 2: Accepting Generic Designs to Save Time
**Pattern**: Approving designs that look like competitors.  
**Prevention**: Strict quality gate enforcement.  
**If Occurs**: Reject and require redesign, adjust timeline.

### Mistake 3: Building Desktop First
**Pattern**: Creating desktop layout, then trying to make it responsive.  
**Prevention**: frontend-dev-agent mobile-first mandate.  
**If Occurs**: Rebuild with mobile-first approach.

### Mistake 4: Skipping Quality Gates
**Pattern**: Bypassing quality checks to meet deadline.  
**Prevention**: Quality over speed principle, adjust timeline instead.  
**If Occurs**: Block deployment, complete quality process.

### Mistake 5: Implementing Without Design System
**Pattern**: Coding before design system is complete.  
**Prevention**: Require Phase 3 completion before Phase 5.  
**If Occurs**: Pause development, complete design system.

## Success Metrics

### Design Quality
- User feedback: "This looks nothing like other mobility sites"
- 5-second test: Users remember design 24 hours later
- Zero use of forbidden design elements

### Technical Quality
- Lighthouse score >90
- WCAG AAA compliance 100%
- Mobile experience rated excellent by users
- Works perfectly on all major browsers

### User Satisfaction
- User approves final design enthusiastically
- Task completion rate >95%
- User satisfaction score >4.5/5

### Process Quality
- All phases completed in sequence
- All quality gates passed
- Zero shortcuts taken
- Documentation complete

## Critical Reminders

1. NEVER start Phase 5 (coding) without approved Phase 4 (mockups)
2. NEVER approve generic designs that use forbidden elements
3. NEVER skip quality gates to meet deadlines
4. ALWAYS test on real mobile devices
5. ALWAYS enforce WCAG AAA compliance

## Additional Resources

For detailed real-world examples and advanced PM competencies, see:

- **references/real-world-examples.md** - 6 comprehensive multi-agent coordination examples showing PM orchestration in practice
- **references/advanced-competencies.md** - Advanced skills including proactive risk management, continuous feedback integration, stakeholder communication, resource balancing, knowledge management, and AI tooling support

These reference files provide deeper guidance when handling complex scenarios, failures, or when implementing sophisticated PM practices.
